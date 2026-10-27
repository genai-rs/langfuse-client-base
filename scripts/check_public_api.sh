#!/usr/bin/env bash
# Compare the working tree's public Rust API against a reference git ref.
#
# Usage: scripts/check_public_api.sh [git-ref]
#   git-ref defaults to the latest tag (the last release).
#
# The reference src/ is extracted with `git archive`, so the comparison never
# depends on crates.io or on network access. Exit code 1 means the public API
# differs; set ALLOW_API_CHANGES=1 to report without failing (for releases
# that intentionally change the API and ship a migration note).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REF="${1:-$(git -C "$PROJECT_ROOT" describe --tags --abbrev=0)}"
REPORT_DIR="$PROJECT_ROOT/target/reports"
REPORT="$REPORT_DIR/public-api-diff.json"

mkdir -p "$REPORT_DIR"
REF_SRC="$(mktemp -d)"
trap 'rm -rf "$REF_SRC"' EXIT

git -C "$PROJECT_ROOT" archive "$REF" src | tar -x -C "$REF_SRC"

flags=(--reference-label "git:$REF" --candidate-label "working-tree")
if [ "${ALLOW_API_CHANGES:-0}" != "1" ]; then
    flags+=(--fail-on-change)
fi

status=0
python3 "$PROJECT_ROOT/migration/compare_public_api.py" \
    "$REF_SRC/src" "$PROJECT_ROOT/src" "${flags[@]}" > "$REPORT" || status=$?

python3 - "$REPORT" <<'EOF'
import json, sys
try:
    report = json.load(open(sys.argv[1]))
except json.JSONDecodeError:
    sys.exit("compare_public_api.py produced no report; see the error above")
print(f"Public API: {report['source_heads']['reference']} -> {report['source_heads']['candidate']}")
for key, value in report["counts"].items():
    print(f"  {key}: {value}")
EOF
echo "Report: $REPORT"

if [ "$status" -ne 0 ]; then
    echo "Public API differs from $REF. Review the report, and set ALLOW_API_CHANGES=1 only for an intentional change with a migration note." >&2
fi
exit "$status"
