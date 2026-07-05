# Anthropic (Claude) — Prompting Rubric

Entry format: **Rule** — why it matters. `applies:` model families. `source:` URL.
`verified:` date. Entries older than 7 days (or missing your model) must be refreshed via
Context7/Exa before use.

> **SEED NOTICE:** All entries below were seeded from training data on 2026-01-15 and are
> intentionally stamped stale so the first real run refreshes them from live docs.

## claude-sonnet-4.x / claude-opus-4.x (incl. claude-sonnet-4-6, claude-opus-4-8)

- **Be explicit and direct; add the "why".** Claude 4 models follow instructions with high
  precision — vague prompts underperform; brief motivation context improves compliance.
  `applies:` all 4.x. `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
  `verified:` 2026-01-15
- **Use XML tags to delimit sections** (`<document>`, `<instructions>`, `<examples>`,
  `<output_format>`) — reduces instruction/data bleed. `applies:` all Claude.
  `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
  `verified:` 2026-01-15
- **Long context: documents first, instructions/query last.** For 20K+ token inputs, put
  documents at the top and the task at the end — significant quality gain on long-context
  tasks. `applies:` all Claude. `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips
  `verified:` 2026-01-15
- **System prompt = role only; task instructions in the user turn.**
  `applies:` all Claude. `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts
  `verified:` 2026-01-15
- **Multishot: 3–5 diverse examples in `<examples>` tags**, covering edge cases, not
  near-duplicates. `applies:` all Claude.
  `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
  `verified:` 2026-01-15
- **Prompt caching: order content stable→volatile** (tools → system → documents → few-shot
  → variable user input) with cache breakpoints after stable blocks; a single early-varying
  token invalidates the prefix. `applies:` all Claude.
  `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
  `verified:` 2026-01-15
- **Structured output: prefer the native structured-output/tool-schema path over
  prose-described JSON**; keep schemas lean, describe fields in schema descriptions not the
  prompt body. `applies:` 4.x+. `source:` https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
  `verified:` 2026-01-15
- **Prefilling: never prefill the assistant turn with extended thinking enabled.**
  Prefill (e.g. `{`) is valid only with thinking off. `applies:` 4.x thinking models.
  `source:` https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
  `verified:` 2026-01-15
- **Extended thinking: high-level guidance ("think deeply about…") beats prescriptive
  step-by-step CoT**; don't hand-script reasoning steps the model does natively.
  `applies:` 4.x thinking models. `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips
  `verified:` 2026-01-15
- **Frame instructions positively** (what to do, not long "do not" lists); Claude 4.x
  over-complies with negations at the expense of the task. `applies:` all 4.x.
  `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
  `verified:` 2026-01-15
- **Ask for parallel tool calls explicitly when independent** — 4.x models parallelize well
  when told to. `applies:` 4.x tool use.
  `source:` https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
  `verified:` 2026-01-15

## claude-5 family (claude-fable-5 / claude-mythos-5)

- **REFRESH REQUIRED — no seeded entries.** Family newer than seed data; fetch the Claude 5
  prompting/migration guide before auditing any claude-5 prompt. `verified:` never
