# Claude Code skills (Fable 5)

Skills I use with Claude Code every day. Each folder is one skill in the standard
layout: a SKILL.md plus optional reference files. To install one, copy its folder into
`~/.claude/skills/` and it loads on your next session.

What's here:

- prompt-alignment-audit: checks a prompt against the provider's current guidance for
  the exact model it targets (Anthropic, OpenAI or Gemini), then proposes a rewrite
  where every change cites the rule behind it. Rubrics refresh from live docs once
  they're older than a week.
- human-article-writing: long-form drafts and rewrites that don't read like a language
  model wrote them. It bans the usual tells and refuses to invent sources, stats or
  anecdotes.
- fable-book: points at a PDF, Markdown, or HTML source and re-authors it as an
  iPad-ready book in the Anthropic Fable theme: warm ivory pages at the iPad Air 11"
  aspect ratio, serif typography, tappable contents, bookmarks, hand-drawn butterfly
  cover art, and botanical vignettes on pages with room to spare.
- cost-lean-orchestration: keeps the expensive model out of bulk reading. Exploration
  goes to cheaper subagents under a strict return format, and the main model spends its
  tokens on reasoning and the final code.

Built with Claude Code on Fable 5, tuned as I go. Suggestions welcome.
