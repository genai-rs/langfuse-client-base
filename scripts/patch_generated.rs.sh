#!/usr/bin/env bash
set -euo pipefail

ROOT=${1:-.}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$ROOT" && pwd)"

# Add bon dependency if missing
toml="$ROOT/Cargo.toml"
if [ -f "$toml" ] && ! grep -q '^bon[[:space:]]*=' "$toml"; then
  tmp="$(mktemp)"
  awk 'BEGIN{added=0} /\[dependencies\]/{print; if(added==0){print "bon = \"3\""; added=1} next} {print} END{if(added==0) print "[dependencies]\nbon = \"3\""}' "$toml" > "$tmp"
  mv "$tmp" "$toml"
fi

# Add reqwest-middleware dependency if missing (should be added by generator, but ensure it's there)
if [ -f "$toml" ] && ! grep -q 'reqwest-middleware' "$toml"; then
  tmp="$(mktemp)"
  awk '/^reqwest = /{print; print "reqwest-middleware = { version = \"0.4\", features = [\"json\", \"multipart\"] }"; next} {print}' "$toml" > "$tmp"
  mv "$tmp" "$toml"
fi

# Add #[bon::builder] to public async API functions
for f in "$ROOT"/src/apis/*.rs; do
  [ -f "$f" ] || continue
  tmp="$(mktemp)"
  awk 'NR==1{prev=""} {
    if ($0 ~ /^pub async fn /) {
      if (prev !~ /bon::builder/) { print "#[bon::builder]" }
      print $0
    } else {
      print $0
    }
    prev=$0
  }' "$f" > "$tmp"
  mv "$tmp" "$f"
done

# Add bon::Builder derives to structs
python3 "$SCRIPT_DIR/add_bon_builders.py" "$ROOT"

# parse_deep_object must not panic on non-object values; emit a plain key/value pair instead
python3 - "$ROOT/src/apis/mod.rs" <<'PY'
import sys

path = sys.argv[1]
text = open(path).read()
old = '    unimplemented!("Only objects are supported with style=deepObject")\n'
new = (
    "    // Non-object values (e.g. array items) are emitted as a plain key/value pair.\n"
    "    let value = match value {\n"
    "        serde_json::Value::String(s) => s.clone(),\n"
    "        _ => value.to_string(),\n"
    "    };\n"
    "    vec![(prefix.to_string(), value)]\n"
)
if old in text:
    open(path, "w").write(text.replace(old, new))
PY

# rustdoc (-D warnings) rejects bare URLs in doc comments: wrap them in <...>
find "$ROOT/src" -name '*.rs' -print0 | xargs -0 perl -pi -e 'if (m{^\s*//[/!]}) { s{(?<![<(\[`"/\w])(https?://[^\s<>)\]`"]*[^\s<>)\]`".,;:])}{<$1>}g }'
