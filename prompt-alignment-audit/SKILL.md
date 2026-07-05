---
name: prompt-alignment-audit
description: Use when reviewing, auditing, or optimizing any LLM prompt (system prompt, extraction prompt, template) against provider guidance — when a prompt underperforms, after a model upgrade or version switch, before shipping a new production prompt, or when asked whether a prompt follows current Anthropic/OpenAI/Gemini best practices. Also use when asked to "check my prompt", "improve this prompt", or fetch the latest prompting guidance (--refresh).
---

# Prompt Alignment Audit

Audit a prompt against the **current, model-version-specific** recommendations of its
provider, then produce a citation-backed report and a fully justified rewrite. A rewrite is
a hypothesis: prove it with the project's eval harness when one exists; otherwise state
plainly that confidence is compliance-based.

**Never edit a production prompt file without explicit user approval.**

## Cost policy (non-negotiable)

All heavy reading — doc research, prompt-file reading, per-dimension audits — is done by
**Sonnet subagents** (`model: "sonnet"`) returning compact structured findings. The
orchestrator never reads raw provider docs and never pastes full documents into context.

## Phase 1 — Discover

- Bare invocation: scan the project for prompts and model IDs. Grep for model strings
  (`claude-`, `gpt-`, `gemini-`, `o3`, `o4`), prompt/controller files, template files.
  Audit everything found.
- With an argument: audit only that file or pasted prompt (ask for the target model if not
  stated and not inferable).
- Detect an eval harness: ground-truth files, accuracy runners, `make accuracy`/eval
  targets. Note it for Phase 5.
- Capture the API configuration around each prompt (extended thinking, structured
  output/tools, caching, temperature) from the calling code — audit agents need it to
  judge config-dependent rules.
- No prompts found → say so and ask for a path. Never guess.

## Phase 2 — Rubric freshness

Rubrics live in `rubrics/<provider>.md`, sectioned by model family, every rule carrying
`source:` and `verified:` fields.

- For each detected provider+model: if its rubric section is missing or `verified:` is
  **older than 7 days**, refresh it before auditing.
- **`--refresh`** (or the user asking for latest guidance) → refresh relevant sections
  regardless of dates.
- Refresh = dispatch one Sonnet research agent per provider: Context7 first (official
  docs), Exa second (model-specific prompting guides, release notes, migration guides).
  The agent rewrites that rubric section in place — same entry format, new `verified:`
  date, real source URLs. Official docs outrank secondary sources; conflicts are kept and
  flagged, not silently resolved.
- Research tools unreachable → proceed on the existing rubric and stamp the report with a
  staleness warning.
- Unknown model ID → use the nearest family section, flag the substitution, attempt a live
  lookup for the new model.

## Phase 3 — Audit fan-out

Dispatch parallel Sonnet subagents, one per dimension in `references/audit-dimensions.md`
(structure/tagging, instruction placement, system-prompt usage, output-format alignment,
examples, caching layout, model-specific features, anti-patterns). Each agent receives:
the prompt text, the relevant rubric section, its single dimension brief — and returns
findings in this exact shape, nothing else:

```
{rule, citation, severity: critical|major|minor, location, current_text, issue, suggested_fix}
```

## Phase 4 — Synthesize + rewrite

Merge findings, dedupe overlaps, rank by severity. Write the rewritten prompt following
`references/rewrite-rules.md`: every change maps to a named rubric rule; domain content
(definitions, legal terms, schema field names, business rules) is preserved **verbatim**.
Then dispatch one adversarial Sonnet agent to compare old vs new for meaning drift; fix
anything it catches before showing the user.

## Phase 5 — Verify + report

- Eval harness exists → offer to run old-vs-new and include scores in the report.
- No harness → the report states its confidence is compliance-based, in those words.
- Deliver the report per `references/report-template.md`: severity-ranked findings table
  with citations, then the justified side-by-side diff.
- Apply changes to source files **only after the user approves**.

## Red flags — stop and correct

| Thought | Reality |
|---|---|
| "The rubric is 9 days old, close enough" | 7 days means 7. Refresh first. |
| "I'll just read the provider docs myself" | Sonnet agents read docs. You read findings. |
| "This rewrite is obviously better, apply it" | Nothing is applied without user approval. |
| "Compliance = better performance" | Only an eval run proves better. Say which one you have. |
| "I'll tidy the domain wording while I'm at it" | Domain content is verbatim. Structure changes only. |
| "Generic Claude advice covers sonnet-4-6" | Guidance is per model version. Use the right section. |
