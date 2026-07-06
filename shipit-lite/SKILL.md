---
name: shipit-lite
description: Use before pushing commits to any remote, when asked "is this safe to push", "check before push", or "shipit" — and whenever the pre-push hook flags findings. Catches scratch/junk files, secret-looking content, and unwanted AI co-author trailers in unpushed commits, and guides the fix for each.
---

# shipit-lite

A last look at what is about to leave the machine. Everything in a pushed commit is
permanent for practical purposes: private repos go public later, force-pushed commits
stay fetchable by SHA, and forks keep copies. Check before the first push, not after.

## Run the check

```bash
bash scripts/pre-push-check.sh <<< '{"tool_input":{"command":"cd <repo> && git push"}}'
```

Or read its three checks and run them by hand. It scans only unpushed commits
(`git log --branches --not --remotes`) for:

1. **Junk/scratch files** — scratch_*, tmp_*, sample_*, debug dumps, `*.log`, `.env`,
   caches, editor dirs, private keys (`*.pem`, `id_rsa*`).
2. **Secret-looking content** — provider key shapes (sk-ant-, sk-, AKIA, ghp_, gho_,
   github_pat_, xox., AIza), PRIVATE KEY blocks, and quoted 16+ char values assigned to
   api_key/secret/token/password. Lines using getenv/environ/dotenv or placeholders are
   excluded.
3. **AI co-author trailers** — Co-Authored-By lines naming Claude, Copilot, Cursor,
   Codex, GPT, Gemini, Devin, or Aider. Repos that deliberately keep attribution opt
   out with `git config shipit.allowAiTrailers true`.

Clean output means clean. Findings mean fix first, push second.

## Fixing findings

**Junk file, last commit only:** `git rm --cached <file>`, add a .gitignore entry, then
`git commit --amend --no-edit`.

**Junk file, older unpushed commits:** rewrite just the unpushed range:
`git rebase -i` isn't available in Claude Code sessions; use
`git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch <path>' <base>..HEAD`.

**Secret:** removing the line is not enough and rewriting history is not enough —
treat the key as burned the moment it was committed, even unpushed, if there is any
doubt. Rotate the key with the provider first, then purge the commits (filter-branch
as above), then add the file or pattern to .gitignore. Never push first "just this
once" intending to rotate later.

**Trailer:** strip from unpushed commits with
`git filter-branch -f --msg-filter 'grep -vi "co-authored-by:"' <base>..HEAD`.
If the repo is supposed to keep attribution, set the opt-out config instead of
stripping.

**Already pushed and public:** history rewriting the remote does not reliably remove
it (cached SHAs, forks, clones). For secrets: rotate immediately. For files/trailers:
rewrite and force-push shrinks exposure but assume copies exist; say so plainly
instead of calling it removed.

## Install as an enforcing hook (recommended)

The skill advises; a hook enforces. In `~/.claude/settings.json`:

```json
"hooks": {
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "bash <path-to-skill>/scripts/pre-push-check.sh",
      "if": "Bash(git push*)",
      "timeout": 30,
      "statusMessage": "Pre-push safety check"
    }]
  }]
}
```

On findings the hook answers the push permission with "ask", so the flagged list is
shown and the user decides. A clean check stays invisible.

## Red flags

| Thought | Reality |
|---|---|
| "It's a private repo, doesn't matter" | Private repos go public. Today's repo did. |
| "I'll rotate the key after pushing" | Rotate first. Pushed keys get scraped in minutes. |
| "Deleted the line in a new commit" | The old commit still has it. Purge or rotate. |
| "The scratch file is harmless" | It shows internals and paths. It also never leaves history. |
| "Force-push removed it from GitHub" | Fetchable by SHA until GC, and forks keep it. |
