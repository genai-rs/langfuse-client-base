#!/usr/bin/env python3
"""Run isolated Cargo fixtures against the downstream checker."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

script = Path(sys.argv[1]).resolve()
results = Path(sys.argv[2]).resolve()
results.mkdir(parents=True, exist_ok=True)

def run(*args, cwd=None, env=None):
    return subprocess.check_output(args, cwd=cwd, env=env, text=True).strip()

def commit(repo, message):
    run("git", "add", ".", cwd=repo)
    run("git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-qm", message, cwd=repo)
    return run("git", "rev-parse", "HEAD", cwd=repo)

with tempfile.TemporaryDirectory(prefix="downstream-crates-io-fixtures-") as directory:
    root = Path(directory)
    base = root / "base with spaces"
    consumer = root / "consumer"
    for repo in (base, consumer):
        (repo / "src").mkdir(parents=True)
        run("git", "init", "-q", str(repo))
    (base / "Cargo.toml").write_text(
        '[package]\nname="langfuse-client-base"\nversion="0.16.1"\nedition="2021"\n')
    (base / "src/lib.rs").write_text('pub fn consumed() -> u8 { 42 }\n')
    good = commit(base, "Compatible base")
    # Same shape as the real wrapper: a plain crates.io requirement on the release line.
    (consumer / "Cargo.toml").write_text(
        '[package]\nname="langfuse-ergonomic"\nversion="0.8.1"\nedition="2021"\nbuild="build.rs"\n'
        '[dependencies]\nlangfuse-client-base = "^0.16.1"\n')
    (consumer / "build.rs").write_text(
        'use std::{env, fs::OpenOptions, io::Write};\n'
        'fn main() { if let Ok(path) = env::var("FIXTURE_MUTATE_CANDIDATE") {\n'
        '  let mut f = OpenOptions::new().append(true).open(path).unwrap();\n'
        '  writeln!(f, "\\n// edited by downstream build script").unwrap();\n'
        '} }\n')
    (consumer / "src/lib.rs").write_text(
        'pub fn use_base() -> u8 { langfuse_client_base::consumed() }\n'
        '#[test] fn offline() { assert_eq!(use_base(), 42); }\n')
    wrapper_sha = commit(consumer, "Depend on the crates.io base and test offline")
    branch = run("git", "symbolic-ref", "HEAD", cwd=consumer)

    git_config = root / "gitconfig"
    git_config.write_text(
        '[user]\n    name = Fixture Runner\n    email = fixture-runner@example.invalid\n')
    # No DOWNSTREAM_COMMIT: the checker resolves the consumer's default branch.
    env = dict(os.environ, DOWNSTREAM_REPOSITORY=str(consumer), CARGO_BUILD_JOBS="2",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(git_config))
    env.pop("DOWNSTREAM_COMMIT", None)

    def case(name, baseline, expected, candidate_result, baseline_result, consumer_ref=branch):
        output = results / name
        output.mkdir(exist_ok=True)
        env["DOWNSTREAM_RESULTS_DIR"] = str(output)
        env["DOWNSTREAM_REPORT_PATH"] = str(output / "copied/report.json")
        base_before = run("git", "status", "--porcelain", cwd=base)
        consumer_before = run("git", "status", "--porcelain", cwd=consumer)
        with (output / "run.log").open("w") as log:
            proc = subprocess.run(["bash", str(script), str(base), baseline], env=env,
                                  stdout=log, stderr=subprocess.STDOUT)
        assert proc.returncode == expected, (name, proc.returncode)
        summary = (output / "summary.md").read_text()
        assert f"| Candidate | {candidate_result} |" in summary, name
        assert f"| Base main (diagnostic only) | {baseline_result} |" in summary, name
        assert f"`{wrapper_sha}` ({consumer_ref})" in summary, name
        assert baseline in summary and "requirement: `^0.16.1`" in summary, name
        assert run("git", "status", "--porcelain", cwd=base) == base_before
        assert run("git", "status", "--porcelain", cwd=consumer) == consumer_before
        assert not (base / "target").exists()
        report = json.loads((output / "report.json").read_text())
        assert (output / "copied/report.json").read_text() == (output / "report.json").read_text(), name
        assert report["candidate"]["result"] == candidate_result, name
        assert report["baseline"]["result"] == baseline_result, name
        assert report["baseline"]["diagnostic_only"] is True, name
        assert report["consumer_commit"] == wrapper_sha, name
        assert report["consumer_requirement"] == "^0.16.1", name
        assert report["baseline_commit"] == baseline, name
        assert report["source_guard"] == "PASS", name
        assert report["exit_status"] == expected, name
        print(f"PASS {name}: exit={proc.returncode}, candidate={candidate_result}, baseline={baseline_result}")

    def mutation_case(name, dirty):
        source = base / "src/lib.rs"
        clean_bytes = source.read_bytes()
        if dirty:
            source.write_bytes(clean_bytes + b"// pre-existing edit\n")
        before_bytes = source.read_bytes()
        before_status = run("git", "status", "--porcelain", "--untracked-files=all", cwd=base)
        output = results / name
        output.mkdir(exist_ok=True)
        env["DOWNSTREAM_RESULTS_DIR"] = str(output)
        env["FIXTURE_MUTATE_CANDIDATE"] = str(source)
        with (output / "run.log").open("w") as log:
            proc = subprocess.run(["bash", str(script), str(base), good], env=env,
                                  stdout=log, stderr=subprocess.STDOUT)
        summary = (output / "summary.md").read_text()
        assert proc.returncode == 1, (name, proc.returncode)
        assert "Candidate source-state guard: FAIL" in summary, name
        assert "Exit status: 1." in summary, name
        assert "| Candidate | FAIL |" in summary, name
        assert source.read_bytes() != before_bytes, name
        source.write_bytes(before_bytes)
        assert run("git", "status", "--porcelain", "--untracked-files=all", cwd=base) == before_status
        if dirty:
            source.write_bytes(clean_bytes)
        del env["FIXTURE_MUTATE_CANDIDATE"]
        assert run("git", "status", "--porcelain", "--untracked-files=all", cwd=base) == ""
        print(f"PASS {name}: mutation detected, process exit=1, summary exit=1")

    mutation_case("mutation-clean-source", dirty=False)
    mutation_case("mutation-already-dirty-source", dirty=True)
    case("compatible", good, 0, "PASS", "PASS")

    # The workflow passes the validated tree and writes the report inside the
    # candidate checkout; neither may trip the source-state guard.
    def tree_case(name, tree, expected):
        output = results / name
        output.mkdir(exist_ok=True)
        report_path = base / "validation-output/downstream-compatibility.json"
        case_env = dict(env, DOWNSTREAM_RESULTS_DIR=str(output),
                        DOWNSTREAM_REPORT_PATH=str(report_path), CANDIDATE_TREE_SHA=tree)
        with (output / "run.log").open("w") as log:
            proc = subprocess.run(["bash", str(script), str(base), good], env=case_env,
                                  stdout=log, stderr=subprocess.STDOUT)
        assert proc.returncode == expected, (name, proc.returncode)
        if expected == 0:
            report = json.loads(report_path.read_text())
            assert report["candidate_tree"] == tree, name
            assert report["candidate"]["result"] == "PASS", name
            assert report["source_guard"] == "PASS", name
            assert f"Candidate tree: `{tree}`" in (output / "summary.md").read_text(), name
        else:
            assert "does not match CANDIDATE_TREE_SHA" in (output / "run.log").read_text(), name
            assert not report_path.exists(), name
        if report_path.exists():
            report_path.unlink()
            report_path.parent.rmdir()
        assert run("git", "status", "--porcelain", "--untracked-files=all", cwd=base) == ""
        print(f"PASS {name}: exit={proc.returncode}")

    tree_case("validated-tree-report-in-candidate", run("git", "write-tree", cwd=base), 0)
    tree_case("tree-mismatch-rejected", "0" * 40, 1)
    (base / "src/lib.rs").write_text('pub fn replacement() -> u8 { 42 }\n')
    removed = commit(base, "Remove consumed symbol")
    case("removed-symbol", good, 1, "FAIL", "PASS")
    assert "cannot find function `consumed`" in (results / "removed-symbol/candidate.log").read_text()
    case("both-fail", removed, 1, "FAIL", "FAIL")
    (base / "src/lib.rs").write_text('pub fn consumed() -> u8 { 42 }\n')
    case("baseline-only-fails", removed, 0, "PASS", "FAIL")

    # A breaking candidate release the consumer has not adopted yet is skipped.
    manifest = base / "Cargo.toml"
    manifest.write_text(manifest.read_text().replace('"0.16.1"', '"0.17.0"'))
    case("breaking-release-skipped", good, 0, "SKIP", "PASS")
    summary = (results / "breaking-release-skipped/summary.md").read_text()
    assert "Candidate langfuse-client-base version: `0.17.0`" in summary
    assert "Base-main langfuse-client-base version: `0.16.1`" in summary
    assert "does not satisfy the consumer requirement ^0.16.1" in (
        results / "breaking-release-skipped/candidate.log").read_text()
    bumped = commit(base, "Release 0.17.0")
    case("both-skipped", bumped, 0, "SKIP", "SKIP")

    # DOWNSTREAM_COMMIT still overrides the default branch.
    (consumer / "README.md").write_text("newer default branch\n")
    commit(consumer, "Advance the default branch")
    env["DOWNSTREAM_COMMIT"] = wrapper_sha
    case("commit-override", bumped, 0, "SKIP", "SKIP", consumer_ref="DOWNSTREAM_COMMIT override")

    # The real wrapper commits a Cargo.lock that pins the crates.io release. A
    # compatible candidate with another version (a patch release) must still
    # replace the locked crate instead of being ignored by Cargo.
    del env["DOWNSTREAM_COMMIT"]
    run("cargo", "generate-lockfile", cwd=consumer)
    lock = (consumer / "Cargo.lock").read_text()
    assert 'name = "langfuse-client-base"\nversion = "0.16.' in lock, "lockfile pins the release"
    assert "registry+https://github.com/rust-lang/crates.io-index" in lock
    locked_sha = commit(consumer, "Commit the lockfile")
    manifest.write_text(manifest.read_text().replace('"0.17.0"', '"0.16.99"'))
    patch_release = commit(base, "Release 0.16.99")
    output = results / "locked-patch-release"
    output.mkdir(exist_ok=True)
    env["DOWNSTREAM_RESULTS_DIR"] = str(output)
    env["DOWNSTREAM_REPORT_PATH"] = str(output / "copied/report.json")
    with (output / "run.log").open("w") as log:
        proc = subprocess.run(["bash", str(script), str(base), patch_release], env=env,
                              stdout=log, stderr=subprocess.STDOUT)
    assert proc.returncode == 0, ("locked-patch-release", proc.returncode)
    summary = (output / "summary.md").read_text()
    assert "| Candidate | PASS |" in summary and f"`{locked_sha}`" in summary
    assert "Candidate langfuse-client-base version: `0.16.99`" in summary
    assert run("git", "status", "--porcelain", cwd=consumer) == ""
    print("PASS locked-patch-release: exit=0, candidate=PASS")
print("All crates.io consumer fixture cases passed; candidate and consumer trees stayed unchanged.")
