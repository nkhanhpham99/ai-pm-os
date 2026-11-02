#!/usr/bin/env bash
# Tests for scripts/privacy-lint.sh. Sensitive sample strings are built by
# concatenation so the lint can scan this file too (only the lint script itself
# is exempt).
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINT="$HERE/../scripts/privacy-lint.sh"
PASS=0
FAIL=0
TMPS=()

cleanup() { for d in "${TMPS[@]:-}"; do [ -n "$d" ] && rm -rf "$d"; done; }
trap cleanup EXIT

new_repo() {
  local d
  d="$(mktemp -d)"
  TMPS+=("$d")
  git -C "$d" init -q -b main
  echo "$d"
}

# run_lint ARGS... -> sets OUT and RC
run_lint() {
  OUT="$(bash "$LINT" "$@" 2>&1)"
  RC=$?
}

ok() { PASS=$((PASS + 1)); echo "ok   - $1"; }
bad() { FAIL=$((FAIL + 1)); echo "FAIL - $1: $2"; }

assert_rc() { # name expected
  if [ "$RC" -eq "$2" ]; then ok "$1"; else bad "$1" "expected exit $2, got $RC; output: $OUT"; fi
}
assert_out_has() { # name needle
  case "$OUT" in *"$2"*) ok "$1" ;; *) bad "$1" "output lacks '$2': $OUT" ;; esac
}

USERS_PATH="/Us""ers/someone/project"
HEX32="0123456789abcdef""0123456789abcdef"
REAL_EMAIL="jane.doe""@corp.test"

test_clean_repo_passes() {
  local r; r="$(new_repo)"
  echo "hello world" > "$r/README.md"
  run_lint "$r"
  assert_rc test_clean_repo_passes 0
}

test_users_path_fails() {
  local r; r="$(new_repo)"
  echo "see $USERS_PATH" > "$r/notes.md"
  run_lint "$r"
  assert_rc test_users_path_fails 1
  assert_out_has test_users_path_fails_names_file "notes.md:1:"
}

test_deny_file_term_fails() {
  local r; r="$(new_repo)"
  local deny="$r.deny"; TMPS+=("$deny")
  echo "zebra-secret-term" > "$deny"
  echo "we ship the ZEBRA-Secret-Term soon" > "$r/plan.md"
  run_lint --deny-file "$deny" "$r"
  assert_rc test_deny_file_term_fails 1
  assert_out_has test_deny_file_term_names_file "plan.md:1:"
}

test_deny_file_clean_passes() {
  local r; r="$(new_repo)"
  local deny="$r.deny"; TMPS+=("$deny")
  printf '# comment\n\nzebra-secret-term\n' > "$deny"
  echo "nothing to see" > "$r/plan.md"
  run_lint --deny-file "$deny" "$r"
  assert_rc test_deny_file_clean_passes 0
}

test_lint_scans_dotfiles_and_json() {
  local r; r="$(new_repo)"
  echo "path=$USERS_PATH" > "$r/.hiddenrc"
  echo "{\"id\": \"$HEX32\"}" > "$r/data.json"
  run_lint "$r"
  assert_rc test_lint_scans_dotfiles_and_json 1
  assert_out_has test_lint_scans_dotfiles ".hiddenrc:1:"
  assert_out_has test_lint_scans_json "data.json:1:"
}

test_lint_flags_private_design_files() {
  local r; r="$(new_repo)"
  echo "audit" > "$r/AUDIT-x.md"
  git -C "$r" add AUDIT-x.md
  mkdir -p "$r/docs"
  echo "design" > "$r/docs/2026-11-02-ai-pm-os-design.md"
  git -C "$r" add docs
  run_lint "$r"
  assert_rc test_lint_flags_private_design_files 1
  assert_out_has test_flags_audit_file "AUDIT-x.md"
  assert_out_has test_flags_design_file "ai-pm-os-design.md"
}

test_ignored_private_files_not_flagged() {
  local r; r="$(new_repo)"
  printf 'AUDIT-*.md\n.private/\n' > "$r/.gitignore"
  echo "audit" > "$r/AUDIT-x.md"
  mkdir -p "$r/.private"
  echo "$USERS_PATH" > "$r/.private/notes.md"
  run_lint "$r"
  assert_rc test_ignored_private_files_not_flagged 0
}

test_noreply_email_allowed() {
  local r; r="$(new_repo)"
  echo "Co-authored by 12345+someone""@users.noreply.github.com and dev""@example.com" > "$r/AUTHORS.md"
  run_lint "$r"
  assert_rc test_noreply_email_allowed 0
}

test_real_email_fails() {
  local r; r="$(new_repo)"
  echo "contact $REAL_EMAIL" > "$r/CONTACT.md"
  run_lint "$r"
  assert_rc test_real_email_fails 1
  assert_out_has test_real_email_names_file "CONTACT.md:1:"
}

test_other_builtin_patterns_fail() {
  local r; r="$(new_repo)"
  echo "vault: iCloud~md""~obsidian/Documents" > "$r/a.md"
  echo "https://team.sl""ack.com/archives/C123" > "$r/b.md"
  echo "tool mcp__""0123abcd-xyz" > "$r/c.md"
  echo "token ey""JhbGciOiJIUzI1NiJ9.payload" > "$r/d.md"
  run_lint "$r"
  assert_rc test_other_builtin_patterns_fail 1
  assert_out_has test_pattern_icloud "a.md:1:"
  assert_out_has test_pattern_slack "b.md:1:"
  assert_out_has test_pattern_mcp "c.md:1:"
  assert_out_has test_pattern_jwt "d.md:1:"
}

test_fixtures_dir_skipped() {
  local r; r="$(new_repo)"
  mkdir -p "$r/tests/fixtures"
  echo "$USERS_PATH" > "$r/tests/fixtures/sample.md"
  run_lint "$r"
  assert_rc test_fixtures_dir_skipped 0
}

test_binary_file_scanned() {
  local r; r="$(new_repo)"
  printf '\x89PNG\r\n\x00\x00%s\x00\x01' "$USERS_PATH" > "$r/image.png"
  run_lint "$r"
  assert_rc test_binary_file_scanned 1
  assert_out_has test_binary_file_names_file "image.png"
}

test_default_root_is_cwd() {
  local r; r="$(new_repo)"
  echo "$USERS_PATH" > "$r/notes.md"
  OUT="$(cd "$r" && bash "$LINT" 2>&1)"; RC=$?
  assert_rc test_default_root_is_cwd 1
}

test_invalid_deny_regex_exits_2() {
  local r; r="$(new_repo)"
  local deny="$r.deny"; TMPS+=("$deny")
  echo "(secret-thing" > "$deny"
  echo "secret-thing" > "$r/plan.md"
  run_lint --deny-file "$deny" "$r"
  assert_rc test_invalid_deny_regex_exits_2 2
  assert_out_has test_invalid_deny_regex_names_line "deny#1: invalid regex"
}

test_invalid_deny_regex_in_clean_repo_not_clean() {
  local r; r="$(new_repo)"
  local deny="$r.deny"; TMPS+=("$deny")
  printf 'fine-term\n[unclosed\n' > "$deny"
  echo "nothing to see" > "$r/plan.md"
  run_lint --deny-file "$deny" "$r"
  assert_rc test_invalid_deny_regex_in_clean_repo_not_clean 2
  assert_out_has test_invalid_deny_regex_second_line "deny#2: invalid regex"
}

test_unreadable_file_fails_closed() {
  if [ "$(id -u)" -eq 0 ]; then ok "test_unreadable_file_fails_closed (skipped as root)"; return; fi
  local r; r="$(new_repo)"
  echo "hello" > "$r/locked.md"
  chmod 000 "$r/locked.md"
  run_lint "$r"
  chmod 644 "$r/locked.md"
  assert_rc test_unreadable_file_fails_closed 2
}

test_clean_repo_passes
test_users_path_fails
test_deny_file_term_fails
test_deny_file_clean_passes
test_lint_scans_dotfiles_and_json
test_lint_flags_private_design_files
test_ignored_private_files_not_flagged
test_noreply_email_allowed
test_real_email_fails
test_other_builtin_patterns_fail
test_fixtures_dir_skipped
test_binary_file_scanned
test_default_root_is_cwd
test_invalid_deny_regex_exits_2
test_invalid_deny_regex_in_clean_repo_not_clean
test_unreadable_file_fails_closed

echo "---"
echo "passed: $PASS, failed: $FAIL"
[ "$FAIL" -eq 0 ]
