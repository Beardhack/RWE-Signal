#!/usr/bin/env bash
set -euo pipefail

scan_paths=(site sources reports config README.md)
failed=0

for command_name in grep cut sort; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "::error title=Publication privacy check failed::Required command '$command_name' is unavailable."
    exit 1
  fi
done

check() {
  local label="$1"
  local pattern="$2"
  local matches

  matches="$(grep -RInE --binary-files=without-match -- "$pattern" "${scan_paths[@]}" || true)"
  if [[ -n "$matches" ]]; then
    echo "::error title=Publication privacy check failed::$label detected in publication files."
    printf '%s\n' "$matches" | cut -d: -f1-2 | sort -u
    failed=1
  fi
}

check "Local Windows user path" '[A-Za-z]:\\Users\\'
check "Local file URL" 'file:///'
check "Local macOS user path" '/Users/[^/]+/'
check "Local Linux home path" '/home/[^/]+/'
check "Email address" '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
check "GitHub token" 'github_pat_|gh[pousr]_[A-Za-z0-9_]+'
check "Slack token" 'xox[baprs]-[A-Za-z0-9-]+'
check "AWS access key" 'AKIA[0-9A-Z]{16}'
check "Private key" '-----BEGIN [A-Z ]*PRIVATE KEY-----'
check "Authorization credential" '[Aa]uthorization[[:space:]]*[:=]|[Bb]earer[[:space:]]+[A-Za-z0-9._~-]+'

if (( failed )); then
  echo "Publication blocked. Remove or redact the flagged data before deploying."
  exit 1
fi

echo "Publication privacy check passed."
