#!/usr/bin/env bash
set -euo pipefail

readonly WRAPPER_REPOSITORY="${WRAPPER_REPOSITORY:-https://github.com/genai-rs/langfuse-client-base.git}"
readonly WRAPPER_REVISION="${WRAPPER_REVISION:-9e7393f8416cb43d455fd1e7ad8b4cb4b765cce3}"
readonly BASELINE_SHA="${BASELINE_SHA:?BASELINE_SHA is required}"
readonly CANDIDATE_TREE_SHA="${CANDIDATE_TREE_SHA:?CANDIDATE_TREE_SHA is required}"
readonly REPORT_PATH="${REPORT_PATH:-validation-output/downstream-compatibility.json}"
readonly WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/downstream-compat.XXXXXX")"
trap 'rm -rf "$WORK_DIR"' EXIT

fail() { echo "downstream compatibility: $*" >&2; exit 1; }
[[ "$BASELINE_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "invalid baseline commit SHA"
[[ "$CANDIDATE_TREE_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "invalid candidate tree SHA"
[[ "$(git write-tree)" == "$CANDIDATE_TREE_SHA" ]] || fail "index does not match candidate tree"

if ! git cat-file -e "$BASELINE_SHA^{commit}" 2>/dev/null; then
  git fetch --no-tags --depth=1 origin "$BASELINE_SHA"
fi
git archive "$BASELINE_SHA" | tar -x -C "$WORK_DIR"
mkdir -p "$WORK_DIR/candidate"
git archive "$CANDIDATE_TREE_SHA" | tar -x -C "$WORK_DIR/candidate"

if [[ -n "${WRAPPER_SOURCE:-}" ]]; then
  cp -R "$WRAPPER_SOURCE" "$WORK_DIR/wrapper"
  actual_wrapper_sha="${WRAPPER_ACTUAL_SHA:-$WRAPPER_REVISION}"
else
  git init -q "$WORK_DIR/wrapper"
  git -C "$WORK_DIR/wrapper" fetch --quiet --depth=1 "$WRAPPER_REPOSITORY" "$WRAPPER_REVISION"
  git -C "$WORK_DIR/wrapper" checkout --quiet --detach FETCH_HEAD
  actual_wrapper_sha="$(git -C "$WORK_DIR/wrapper" rev-parse HEAD)"
fi
[[ "$actual_wrapper_sha" == "$WRAPPER_REVISION" ]] || fail "wrapper resolved to unexpected revision $actual_wrapper_sha"

# Prime the pinned wrapper's locked dependency set before the offline checks.
if [[ -f "$WORK_DIR/wrapper/Cargo.lock" ]]; then
  cargo fetch --locked --manifest-path "$WORK_DIR/wrapper/Cargo.toml"
else
  cargo generate-lockfile --offline --manifest-path "$WORK_DIR/wrapper/Cargo.toml"
fi

mkdir -p "$(dirname "$REPORT_PATH")"
export CARGO_BUILD_JOBS=2
run_case() {
  local label="$1" source="$2" target="$WORK_DIR/target" resolved=not_resolved status=unknown
  local config=(--config "patch.crates-io.langfuse-client-base.path=\"$source\"")
  if ! cargo metadata --format-version 1 --offline --manifest-path "$WORK_DIR/wrapper/Cargo.toml" "${config[@]}" >"$WORK_DIR/$label-metadata.json" 2>"$WORK_DIR/$label-metadata.err"; then
    status=resolution_failed
  else
    resolved="$(python3 -c 'import json,sys; print(next(p["manifest_path"] for p in json.load(open(sys.argv[1]))["packages"] if p["name"] == "langfuse-client-base"))' "$WORK_DIR/$label-metadata.json")"
    if [[ "$(cd "$(dirname "$resolved")" && pwd -P)" != "$(cd "$source" && pwd -P)" ]]; then
      status=wrong_resolution
    else
      local check_status test_status
      if CARGO_TARGET_DIR="$target" cargo check --all-targets --all-features --offline --locked --manifest-path "$WORK_DIR/wrapper/Cargo.toml" "${config[@]}" >"$WORK_DIR/$label-check.log" 2>&1; then
        check_status=passed
      else
        check_status=failed
      fi
      if CARGO_TARGET_DIR="$target" cargo test --all-targets --all-features --offline --locked --manifest-path "$WORK_DIR/wrapper/Cargo.toml" "${config[@]}" >"$WORK_DIR/$label-test.log" 2>&1; then
        test_status=passed
      else
        test_status=failed
      fi
      printf '%s\n' "$check_status" > "$WORK_DIR/$label.check-status"
      printf '%s\n' "$test_status" > "$WORK_DIR/$label.test-status"
      if [[ "$check_status" == passed && "$test_status" == passed ]]; then
        status=passed
      else
        status=failed
      fi
    fi
  fi
  printf '%s\n' "$status" > "$WORK_DIR/$label.status"
  printf '%s\n' "$resolved" > "$WORK_DIR/$label.resolved"
}

baseline_status=unknown
candidate_status=unknown
baseline_check=not_run
baseline_tests=not_run
candidate_check=not_run
candidate_tests=not_run
run_case baseline "$WORK_DIR"
run_case candidate "$WORK_DIR/candidate"
baseline_status="$(cat "$WORK_DIR/baseline.status")"
candidate_status="$(cat "$WORK_DIR/candidate.status")"
baseline_check="$(cat "$WORK_DIR/baseline.check-status" 2>/dev/null || echo not_run)"
baseline_tests="$(cat "$WORK_DIR/baseline.test-status" 2>/dev/null || echo not_run)"
candidate_check="$(cat "$WORK_DIR/candidate.check-status" 2>/dev/null || echo not_run)"
candidate_tests="$(cat "$WORK_DIR/candidate.test-status" 2>/dev/null || echo not_run)"
python3 - "$REPORT_PATH" "$BASELINE_SHA" "$CANDIDATE_TREE_SHA" "$actual_wrapper_sha" "$baseline_status" "$candidate_status" "$(cat "$WORK_DIR/baseline.resolved")" "$(cat "$WORK_DIR/candidate.resolved")" "$baseline_check" "$baseline_tests" "$candidate_check" "$candidate_tests" <<'PY'
import json, pathlib, sys
path, baseline, candidate, wrapper, baseline_status, candidate_status, baseline_resolved, candidate_resolved, baseline_check, baseline_tests, candidate_check, candidate_tests = sys.argv[1:]
pathlib.Path(path).write_text(json.dumps({
    "baseline_commit": baseline,
    "candidate_tree": candidate,
    "wrapper_commit": wrapper,
    "baseline": {"status": baseline_status, "check": baseline_check, "tests": baseline_tests, "resolved_manifest": baseline_resolved},
    "candidate": {"status": candidate_status, "check": candidate_check, "tests": candidate_tests, "resolved_manifest": candidate_resolved},
}, indent=2) + "\n")
PY

if [[ "$baseline_status" != passed ]]; then
  echo "downstream compatibility: baseline failed ($baseline_status); candidate result is diagnostic only" >&2
  [[ ! -f "$WORK_DIR/baseline-check.log" ]] || cat "$WORK_DIR/baseline-check.log" >&2
  [[ ! -f "$WORK_DIR/baseline-test.log" ]] || cat "$WORK_DIR/baseline-test.log" >&2
  [[ ! -f "$WORK_DIR/candidate-check.log" ]] || cat "$WORK_DIR/candidate-check.log" >&2
  [[ ! -f "$WORK_DIR/candidate-test.log" ]] || cat "$WORK_DIR/candidate-test.log" >&2
  exit 1
fi
if [[ "$candidate_status" != passed ]]; then
  echo "downstream compatibility: candidate fails pinned wrapper compatibility" >&2
  cat "$WORK_DIR/candidate-check.log" "$WORK_DIR/candidate-test.log" >&2 || true
  exit 1
fi
echo "downstream compatibility: baseline and candidate pass pinned wrapper $actual_wrapper_sha"
