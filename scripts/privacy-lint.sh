#!/usr/bin/env bash
# privacy-lint.sh - fail if any private string or private file would be published.
#
# Usage: bash scripts/privacy-lint.sh [--deny-file PATH] [ROOT]
#
# Scans every git-tracked file plus every untracked, non-ignored file under ROOT
# (default: current directory), dotfiles, JSON and binaries included. Exits 0 if
# clean; otherwise exits 1 and prints one "path:line: <pattern-name>" per hit.
# Skipped: this script itself and tests/fixtures/.
# The deny file holds one case-insensitive extended regex per line (blank lines
# and lines starting with # are ignored). Hits on it are reported as deny#N so
# the private term is never echoed into logs.
set -u

DENY_FILE=""
ROOT="."
while [ $# -gt 0 ]; do
  case "$1" in
    --deny-file)
      [ $# -ge 2 ] || { echo "privacy-lint: --deny-file needs a path" >&2; exit 2; }
      DENY_FILE="$2"
      shift 2
      ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *)
      ROOT="$1"
      shift
      ;;
  esac
done

if [ -n "$DENY_FILE" ]; then
  [ -f "$DENY_FILE" ] || { echo "privacy-lint: deny file not found: $DENY_FILE" >&2; exit 2; }
  DENY_FILE="$(cd "$(dirname "$DENY_FILE")" && pwd)/$(basename "$DENY_FILE")"
fi
[ -d "$ROOT" ] || { echo "privacy-lint: not a directory: $ROOT" >&2; exit 2; }
cd "$ROOT" || exit 2
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "privacy-lint: not a git repo: $ROOT" >&2; exit 2; }

# Files to scan: tracked + untracked-not-ignored, minus self and fixtures.
FILES="$(mktemp)"
HITS="$(mktemp)"
ERRS="$(mktemp)"
trap 'rm -f "$FILES" "$HITS" "$ERRS"' EXIT
git ls-files -co --exclude-standard -z \
  | tr '\0' '\n' \
  | grep -v -e '^scripts/privacy-lint\.sh$' -e '^tests/fixtures/' \
  | while IFS= read -r f; do [ -f "$f" ] && printf '%s\n' "$f"; done > "$FILES"

# scan NAME REGEX : report path:line: NAME for every matching line.
scan() {
  local name="$1" regex="$2"
  [ -s "$FILES" ] || return 0
  tr '\n' '\0' < "$FILES" \
    | xargs -0 grep -a -n -H -i -o -E -e "$regex" 2>>"$ERRS" \
    | sed -E "s/^(.*):([0-9]+):.*$/\1:\2: $name/" >> "$HITS"
}

# Built-in generic patterns.
scan 'abs-user-path'    '/Users/'
scan 'obsidian-icloud'  'iCloud~md~obsidian'
scan 'slack-archive-url' 'slack\.com/archives'
scan 'mcp-connector-id' 'mcp__[0-9a-f]{8}-'
scan 'hex32-id'         '[0-9a-f]{32}'
scan 'jwt-token'        'eyJ[A-Za-z0-9_-]{10,}\.'

# Email addresses, except @users.noreply.github.com and @example.com.
if [ -s "$FILES" ]; then
  tr '\n' '\0' < "$FILES" \
    | xargs -0 grep -a -n -H -i -o -E -e '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' 2>>"$ERRS" \
    | grep -v -i -E '@(users\.noreply\.github|example)\.com$' \
    | sed -E 's/^(.*):([0-9]+):.*$/\1:\2: email-address/' >> "$HITS"
fi

# Private design/audit files must never be tracked (or left unignored).
grep -E -e '(^|/)AUDIT-' -e 'ai-pm-os-design' "$FILES" \
  | sed -E 's/^(.*)$/\1:0: private-filename/' >> "$HITS"

# Deny-file patterns. Validate every pattern first: an invalid regex must stop
# the lint (exit 2), never be silently skipped.
if [ -n "$DENY_FILE" ]; then
  n=0
  invalid=0
  while IFS= read -r pat || [ -n "$pat" ]; do
    n=$((n + 1))
    pat="${pat%$'\r'}"
    case "$pat" in ''|'#'*) continue ;; esac
    printf '' | grep -E -e "$pat" >/dev/null 2>&1
    if [ $? -eq 2 ]; then
      echo "deny#$n: invalid regex" >&2
      invalid=1
    fi
  done < "$DENY_FILE"
  [ "$invalid" -eq 0 ] || exit 2
  n=0
  while IFS= read -r pat || [ -n "$pat" ]; do
    n=$((n + 1))
    pat="${pat%$'\r'}"
    case "$pat" in ''|'#'*) continue ;; esac
    scan "deny#$n" "$pat"
  done < "$DENY_FILE"
fi

# Any grep error (unreadable file, engine failure) means the scan was incomplete:
# fail closed rather than report clean.
if [ -s "$ERRS" ]; then
  echo "privacy-lint: scan errors (result not trustworthy):" >&2
  sort -u "$ERRS" >&2
  exit 2
fi

if [ -s "$HITS" ]; then
  sort -u "$HITS"
  exit 1
fi
exit 0
