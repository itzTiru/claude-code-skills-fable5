#!/usr/bin/env bash
# Claude Code PreToolUse hook: safety check before any `git push`.
# Scans commits that are about to leave this machine (present locally, absent
# from all remotes) for scratch/junk files, secret-looking content, and AI
# co-author trailers. Clean -> silent allow. Findings -> "ask" the user.
set -u

input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')

# Honor an explicit `cd <dir> && git push` prefix; otherwise use the cwd.
dir=$(printf '%s' "$cmd" | sed -n 's|^cd[[:space:]]\{1,\}\([^&;]*\).*|\1|p' | head -1 | sed 's/["'"'"']//g; s/[[:space:]]*$//')
if [ -n "$dir" ]; then cd "$dir" 2>/dev/null || exit 0; fi
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

unpushed_range="--branches --not --remotes"
findings=""

junk=$(git log $unpushed_range --name-only --pretty=format: 2>/dev/null | sort -u | grep -iE \
  '(^|/)(scratch|tmp_|temp_|sample_|test_output|debug_|dump_)[^/]*$|\.(log|tmp|bak|swp|pyc)$|(^|/)(__pycache__|node_modules|\.pytest_cache|\.ruff_cache|\.DS_Store|\.vscode)(/|$)|(^|/)\.env(\.[^/]*)?$|\.(pem|p12|pfx)$|(^|/)id_(rsa|ed25519)[^/]*$' \
  | head -20)
if [ -n "$junk" ]; then
  findings="Junk/scratch/sensitive files in unpushed commits:
$junk

"
fi

secrets=$(git log $unpushed_range -p --pretty=format: 2>/dev/null | grep -E '^\+[^+]' | grep -oEn \
  "sk-ant-[A-Za-z0-9_-]{8,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[bap]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY|(api[_-]?key|apikey|secret|token|password)[\"']?[[:space:]]*[:=][[:space:]]*[\"'][A-Za-z0-9_/+.-]{16,}[\"']" \
  | grep -viE 'getenv|environ|load_dotenv|example|placeholder|your[_-]?key|<[A-Z_]+>|\$\{' | head -10)
if [ -n "$secrets" ]; then
  findings="${findings}Secret-looking content in unpushed commits:
$secrets

"
fi

# Repos that deliberately keep AI attribution opt out with:
#   git config shipit.allowAiTrailers true
if [ "$(git config --get shipit.allowAiTrailers 2>/dev/null)" = "true" ]; then
  trailers=""
else
  trailers=$(git log $unpushed_range --pretty='%h %(trailers:key=Co-Authored-By,valueonly,separator=%x20)' 2>/dev/null \
    | grep -iE 'claude|copilot|cursor|codex|gpt|gemini|devin|aider|noreply@anthropic|noreply@openai' | head -10)
fi
if [ -n "$trailers" ]; then
  findings="${findings}AI co-author trailers in unpushed commits (house rule: strip these):
$trailers
"
fi

if [ -n "$findings" ]; then
  jq -n --arg r "$findings" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"ask",permissionDecisionReason:("Pre-push check flagged:\n\n"+$r+"\nPush anyway?")}}'
fi
exit 0
