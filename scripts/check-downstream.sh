#!/usr/bin/env bash
# Check the crates.io consumer's default branch against this checkout without
# changing either repository. Usage:
#   scripts/check-downstream.sh [candidate-directory] [base-main-commit]
# DOWNSTREAM_COMMIT overrides the consumer commit (default: the consumer's
# default branch, resolved to a full SHA at run time). Results survive checkout
# cleanup in DOWNSTREAM_RESULTS_DIR (summary.md, report.json and the logs).
# DOWNSTREAM_REPORT_PATH, when set, also receives a copy of report.json. CANDIDATE_TREE_SHA, when set, must equal
# the candidate's index tree, and the tracked working tree must match it.
set -euo pipefail

candidate=$(cd "${1:-$(dirname "$0")/..}" && pwd -P)
baseline_sha=$(git -C "$candidate" rev-parse "${2:-origin/main}^{commit}")
candidate_sha=$(git -C "$candidate" rev-parse HEAD)
consumer_repository=${DOWNSTREAM_REPOSITORY:-https://github.com/genai-rs/langfuse-ergonomic.git}
if [[ -n "${DOWNSTREAM_COMMIT:-}" ]]; then
    consumer_sha=$DOWNSTREAM_COMMIT
    consumer_ref='DOWNSTREAM_COMMIT override'
else
    # The wrapper depends on the crates.io release line, so its default branch
    # is the compatibility target. Resolve it once so both variants agree.
    remote_head=$(git ls-remote --symref "$consumer_repository" HEAD)
    consumer_ref=$(awk '$1 == "ref:" && $3 == "HEAD" { print $2 }' <<< "$remote_head")
    consumer_sha=$(awk '$2 == "HEAD" && $1 != "ref:" { print $1 }' <<< "$remote_head")
fi
if [[ ! "$consumer_sha" =~ ^[0-9a-f]{40}$ ]]; then
    echo "Consumer commit must be a full commit SHA (DOWNSTREAM_COMMIT or the resolved default branch), got: ${consumer_sha:-<empty>}" >&2
    exit 1
fi
results=${DOWNSTREAM_RESULTS_DIR:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/downstream-results}
mkdir -p "$results"
results=$(cd "$results" && pwd -P)
scratch=$(mktemp -d "${RUNNER_TEMP:-${TMPDIR:-/tmp}}/downstream.XXXXXX")
candidate_result=NOT_RUN
baseline_result=NOT_RUN
consumer_requirement=UNKNOWN
candidate_version=UNKNOWN
baseline_version=UNKNOWN
candidate_diff=$(git -C "$candidate" diff --binary HEAD | shasum -a 256 | cut -d ' ' -f 1)
candidate_tree=${CANDIDATE_TREE_SHA:-}
report_path=${DOWNSTREAM_REPORT_PATH:-}
if [[ -n "$report_path" ]]; then
    mkdir -p "$(dirname "$report_path")"
    report_path="$(cd "$(dirname "$report_path")" && pwd -P)/$(basename "$report_path")"
fi
if [[ -n "$candidate_tree" ]]; then
    # The candidate is the working tree; prove it is the validated tree.
    if [[ ! "$candidate_tree" =~ ^[0-9a-f]{40}$ ]]; then
        echo "CANDIDATE_TREE_SHA must be a full tree SHA, got: $candidate_tree" >&2
        exit 1
    fi
    if [[ "$(git -C "$candidate" write-tree)" != "$candidate_tree" ]]; then
        echo 'The candidate index does not match CANDIDATE_TREE_SHA.' >&2
        exit 1
    fi
    if ! git -C "$candidate" diff --quiet; then
        echo 'The candidate working tree has unstaged changes to tracked files.' >&2
        exit 1
    fi
fi

# Hash the complete checkout state, not just Git's status text. Porcelain does
# not change when an already-dirty file is edited again. Include every file,
# symlink, and directory outside .git (including ignored and untracked files),
# plus the exact index entries and Git status. Nothing in the source tree is
# silently excluded from this guard.
source_fingerprint() {
    python3 - "$1" <<'PYFINGERPRINT'
import hashlib
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
digest = hashlib.sha256()
def add(data):
    digest.update(len(data).to_bytes(8, 'big'))
    digest.update(data)

status = subprocess.check_output(
    ['git', '-C', str(root), 'status', '--porcelain=v2', '-z',
     '--untracked-files=all', '--ignored=matching'])
index = subprocess.check_output(['git', '-C', str(root), 'ls-files', '--stage', '-z'])
add(status)
add(index)
for directory, names, files in os.walk(root, topdown=True, followlinks=False):
    names[:] = sorted(name for name in names if name != '.git')
    files.sort()
    parent = Path(directory)
    for name in names:
        path = parent / name
        if path.is_symlink():
            add(b'L' + os.fsencode(path.relative_to(root)))
            add(os.fsencode(os.readlink(path)))
    for name in files:
        path = parent / name
        relative = os.fsencode(path.relative_to(root))
        if path.is_symlink():
            add(b'L' + relative)
            add(os.fsencode(os.readlink(path)))
        elif path.is_file():
            add(b'F' + relative)
            add(path.stat().st_mode.to_bytes(4, 'big'))
            with path.open('rb') as source:
                while chunk := source.read(1024 * 1024):
                    add(chunk)
        else:
            add(b'O' + relative)
print(digest.hexdigest())
PYFINGERPRINT
}
source_fingerprint_before=$(source_fingerprint "$candidate")

finish() {
    local status=$?
    trap - EXIT
    local source_fingerprint_after=''
    local source_guard=PASS
    if ! source_fingerprint_after=$(source_fingerprint "$candidate"); then
        echo '::error::Could not fingerprint the candidate checkout after the downstream check.' >&2
        status=1
        candidate_result=FAIL
        source_guard=ERROR
    elif [[ "$source_fingerprint_after" != "$source_fingerprint_before" ]]; then
        echo '::error::Downstream check modified the candidate checkout.' >&2
        status=1
        candidate_result=FAIL
        source_guard=FAIL
    fi
    if ! rm -rf "$scratch"; then
        echo '::error::Could not remove the temporary downstream-check directory.' >&2
        status=1
    fi
    {
        echo '## Downstream compatibility'
        echo
        echo "- Consumer repository: \`$consumer_repository\`"
        echo "- Consumer commit: \`$consumer_sha\` ($consumer_ref)"
        echo "- Consumer langfuse-client-base requirement: \`$consumer_requirement\`"
        echo "- Candidate langfuse-client-base version: \`$candidate_version\`"
        echo "- Base-main langfuse-client-base version: \`$baseline_version\`"
        echo "- Candidate source commit: \`$candidate_sha\` (working tree, including generated changes)"
        echo "- Candidate tracked diff SHA-256: \`$candidate_diff\`"
        if [[ -n "$candidate_tree" ]]; then
            echo "- Candidate tree: \`$candidate_tree\` (verified against the index and tracked working tree)"
        fi
        echo "- Base-main commit: \`$baseline_sha\`"
        echo
        echo '| Consumer against | Result |'
        echo '| --- | --- |'
        echo "| Candidate | $candidate_result |"
        echo "| Base main (diagnostic only) | $baseline_result |"
        echo
        echo "Candidate failure blocks. Base-main failure is diagnostic. SKIP means the version does not satisfy the consumer requirement (a breaking release the consumer has not adopted yet), so nothing was built. Candidate source-state guard: $source_guard. Exit status: $status."
        echo 'Full command output is in candidate.log and baseline.log.'
    } > "$results/summary.md"
    cat "$results/summary.md"
    python3 - "$results/report.json" "$consumer_repository" "$consumer_sha" "$consumer_ref" \
        "$consumer_requirement" "$candidate_sha" "$candidate_tree" "$candidate_diff" \
        "$baseline_sha" "$candidate_version" "$candidate_result" "$baseline_version" \
        "$baseline_result" "$source_guard" "$status" <<'PYREPORT' || status=1
import json
from pathlib import Path
import sys
(path, repository, consumer, ref, requirement, candidate, tree, diff, baseline,
 candidate_version, candidate_result, baseline_version, baseline_result, guard, status) = sys.argv[1:]
Path(path).write_text(json.dumps({
    'consumer_repository': repository,
    'consumer_commit': consumer,
    'consumer_ref': ref,
    'consumer_requirement': requirement,
    'candidate_commit': candidate,
    'candidate_tree': tree or None,
    'candidate_tracked_diff_sha256': diff,
    'baseline_commit': baseline,
    'candidate': {'version': candidate_version, 'result': candidate_result},
    'baseline': {'version': baseline_version, 'result': baseline_result, 'diagnostic_only': True},
    'source_guard': guard,
    'exit_status': int(status),
}, indent=2) + '\n')
PYREPORT
    # Copied after the source-state guard ran, so it may live in the candidate.
    if [[ -n "$report_path" && ! "$report_path" -ef "$results/report.json" ]] &&
        ! cp "$results/report.json" "$report_path"; then
        status=1
    fi
    if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
        cat "$results/summary.md" >> "$GITHUB_STEP_SUMMARY"
    fi
    exit "$status"
}
trap finish EXIT

# Never enable live consumer tests, even when invoked from a credentialed shell.
unset LANGFUSE_PUBLIC_KEY LANGFUSE_SECRET_KEY LANGFUSE_BASE_URL LANGFUSE_HOST
export CARGO_BUILD_JOBS=${CARGO_BUILD_JOBS:-2}
# Keep Cargo outputs and all patched consumer files outside the candidate.
export CARGO_TARGET_DIR="$scratch/target"

mkdir -p "$scratch/base-main" "$scratch/candidate-consumer" "$scratch/baseline-consumer"
git -C "$candidate" archive "$baseline_sha" | tar -x -C "$scratch/base-main"
git init -q "$scratch/consumer"
git -C "$scratch/consumer" fetch --depth=1 "$consumer_repository" "$consumer_sha"
git -C "$scratch/consumer" checkout -q --detach FETCH_HEAD
test "$(git -C "$scratch/consumer" rev-parse HEAD)" = "$consumer_sha"
# The helper validates the consumer's crates.io dependency and applies Cargo's
# version-requirement rules (pre-release tags are compared on the core version).
cat > "$scratch/requirement.py" <<'PYREQUIREMENT'
import re
import sys
import tomllib

def load(path):
    with open(path, 'rb') as manifest_file:
        return tomllib.load(manifest_file)

def requirement(path):
    dependency = load(path).get('dependencies', {}).get('langfuse-client-base')
    if isinstance(dependency, str):
        return dependency
    if not isinstance(dependency, dict) or not isinstance(dependency.get('version'), str):
        sys.exit('ERROR: consumer must declare langfuse-client-base with a version requirement')
    other = sorted({'git', 'path', 'registry', 'package', 'workspace'} & dependency.keys())
    if other:
        sys.exit('ERROR: consumer langfuse-client-base dependency is not a crates.io dependency: ' + ', '.join(other))
    return dependency['version']

def version(path):
    package = load(path).get('package', {})
    if package.get('name') != 'langfuse-client-base' or not isinstance(package.get('version'), str):
        sys.exit('ERROR: ' + path + ' is not an langfuse-client-base manifest')
    return package['version']

def core(text):
    match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', text)
    if not match:
        sys.exit('ERROR: invalid version ' + repr(text))
    return tuple(int(part) for part in match.groups())

def matches(current, comparator):
    if comparator == '*':
        return True
    match = re.fullmatch(r'(\^|~|=|>=|>|<=|<)?\s*(\d+)(?:\.(\d+|\*))?(?:\.(\d+|\*))?(?:-[0-9A-Za-z.-]+)?', comparator)
    if not match:
        sys.exit('ERROR: unsupported version requirement ' + repr(comparator))
    op, major, minor, patch = match.groups()
    major = int(major)
    minor = None if minor in (None, '*') else int(minor)
    patch = None if minor is None or patch in (None, '*') else int(patch)
    lower = (major, minor or 0, patch or 0)
    # The first version above a partial requirement: 1 -> 2.0.0, 1.2 -> 1.3.0.
    after = (major + 1, 0, 0) if minor is None else (major, minor + 1, 0) if patch is None else (major, minor, patch + 1)
    if op in (None, '^'):
        if major > 0 or minor is None:
            upper = (major + 1, 0, 0)
        elif minor > 0 or patch is None:
            upper = (0, minor + 1, 0)
        else:
            upper = (0, 0, patch + 1)
        return lower <= current < upper
    if op == '~':
        return lower <= current < ((major + 1, 0, 0) if minor is None else (major, minor + 1, 0))
    if op == '=':
        return lower <= current < after
    if op == '>=':
        return current >= lower
    if op == '>':
        return current >= after
    if op == '<':
        return current < lower
    return current < after

command, *arguments = sys.argv[1:]
if command == 'requirement':
    print(requirement(arguments[0]))
elif command == 'version':
    print(version(arguments[0]))
elif command == 'satisfies':
    current = core(arguments[0])
    # Exit 3 means a valid version outside the requirement; other failures are errors.
    sys.exit(0 if all(matches(current, part.strip()) for part in arguments[1].split(',')) else 3)
else:
    sys.exit('ERROR: unknown command ' + command)
PYREQUIREMENT
consumer_requirement=$(python3 "$scratch/requirement.py" requirement "$scratch/consumer/Cargo.toml")
candidate_version=$(python3 "$scratch/requirement.py" version "$candidate/Cargo.toml")
baseline_version=$(python3 "$scratch/requirement.py" version "$scratch/base-main/Cargo.toml")
for variant in candidate baseline; do
    git -C "$scratch/consumer" archive HEAD | tar -x -C "$scratch/$variant-consumer"
done

check_consumer() (
    label=$1
    base=$2
    consumer="$scratch/$label-consumer"
    config="$scratch/$label.toml"
    cd "$consumer" || return
    # Replace the crates.io release with the local manifest. Cargo resolves
    # in this temporary copy; the consumer's own lockfile is never written back.
    {
        echo '[patch.crates-io]'
        python3 -c 'import json, sys; print("langfuse-client-base = { path = " + json.dumps(sys.argv[1]) + " }")' "$base"
    } > "$config" || return
    echo '+ cargo metadata --format-version 1 --all-features'
    cargo --config "$config" metadata --format-version 1 --all-features > "$scratch/$label.json" || return
    # Inspect Cargo's actual resolved graph. A source assertion or matching
    # package name alone cannot prove the wrapper uses the local candidate.
    python3 - "$scratch/$label.json" "$consumer/Cargo.toml" "$base/Cargo.toml" <<'PYMETADATA' || return
import json
from pathlib import Path
import sys
import tomllib
metadata = json.loads(Path(sys.argv[1]).read_text())
with open(sys.argv[2], 'rb') as f:
    consumer = tomllib.load(f)
with open(sys.argv[3], 'rb') as f:
    base = tomllib.load(f)
expected = Path(sys.argv[3]).resolve()
packages = [p for p in metadata['packages'] if p['name'] == 'langfuse-client-base']
if len(packages) != 1 or Path(packages[0]['manifest_path']).resolve() != expected:
    sys.exit('ERROR: Cargo did not resolve exclusively to the requested local base manifest')
root = metadata['resolve']['root']
root_package = next((p for p in metadata['packages'] if p['id'] == root), None)
if root_package is None or root_package['name'] != 'langfuse-ergonomic':
    sys.exit('ERROR: resolved workspace root is not the langfuse-ergonomic package')
root_node = next((n for n in metadata['resolve']['nodes'] if n['id'] == root), None)
base_id = packages[0]['id']
if root_node is None or not any(d['name'] == 'langfuse_client_base' and d['pkg'] == base_id for d in root_node['deps']):
    sys.exit('ERROR: Cargo dependency graph does not link the wrapper directly to the candidate manifest')
if packages[0]['version'] != base['package']['version']:
    sys.exit('ERROR: resolved langfuse-client-base version does not equal the candidate manifest')
print('Verified Cargo edge: langfuse-ergonomic ->', expected)
PYMETADATA
    echo '+ cargo check --locked --all-targets --all-features'
    cargo --config "$config" check --locked --all-targets --all-features || return
    echo '+ cargo test --offline --locked --all-features'
    # Metadata fetched/resolved dependencies. Tests now run offline with the
    # same verified temporary lockfile and local crates.io patch.
    cargo --config "$config" test --offline --locked --all-features || return
)

# A version outside the consumer requirement is a breaking release the consumer
# has not adopted yet. Cargo would ignore the patch, so report SKIP instead.
run_variant() {
    local label=$1 base=$2 version=$3
    local satisfies=0
    python3 "$scratch/requirement.py" satisfies "$version" "$consumer_requirement" || satisfies=$?
    if [[ "$satisfies" == 3 ]]; then
        echo "SKIP: langfuse-client-base $version does not satisfy the consumer requirement $consumer_requirement" \
            > "$results/$label.log"
        cat "$results/$label.log" >&2
        echo SKIP
    elif [[ "$satisfies" != 0 ]]; then
        echo FAIL
    elif check_consumer "$label" "$base" > "$results/$label.log" 2>&1; then
        cat "$results/$label.log" >&2
        echo PASS
    else
        cat "$results/$label.log" >&2
        echo FAIL
    fi
}

candidate_result=$(run_variant candidate "$candidate" "$candidate_version")
# Always run base main too, including after candidate failure, for attribution.
baseline_result=$(run_variant baseline "$scratch/base-main" "$baseline_version")
if [[ "$candidate_result" == FAIL ]]; then
    echo '::error::Downstream candidate compatibility failed; inspect candidate.log and baseline.log.' >&2
    exit 1
fi
if [[ "$candidate_result" == SKIP ]]; then
    echo "::notice::Downstream check skipped: langfuse-client-base $candidate_version does not satisfy the consumer requirement $consumer_requirement." >&2
fi
if [[ "$baseline_result" == FAIL ]]; then
    echo '::warning::Base-main consumer check failed; the candidate did not fail. See baseline.log.' >&2
fi
