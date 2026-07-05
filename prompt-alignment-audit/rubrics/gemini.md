# Google (Gemini) — Prompting Rubric

Entry format: **Rule** — why. `applies:` model families. `source:` URL. `verified:` date.
Entries older than 7 days (or missing your model) must be refreshed via Context7/Exa.

> **SEED NOTICE:** Seeded from training data on 2026-01-15; intentionally stale so the
> first real run refreshes from live docs.

## gemini-2.x / gemini-3.x

- **Use `system_instruction` for role/behavior**, keep task content in user turns.
  `applies:` 1.5+. `source:` https://ai.google.dev/gemini-api/docs/system-instructions
  `verified:` 2026-01-15
- **Long context: query/instructions AFTER the large content** — for million-token
  contexts, place documents/media first, the question at the end. `applies:` all
  long-context Gemini. `source:` https://ai.google.dev/gemini-api/docs/long-context
  `verified:` 2026-01-15
- **Few-shot examples are strongly recommended** (unlike o-series) — consistent format,
  shown not told. `applies:` all Gemini.
  `source:` https://ai.google.dev/gemini-api/docs/prompting-strategies
  `verified:` 2026-01-15
- **Structured output via `responseSchema` + `responseMimeType: application/json`**, not
  prose-described JSON. `applies:` 1.5+.
  `source:` https://ai.google.dev/gemini-api/docs/structured-output
  `verified:` 2026-01-15
- **Context caching for repeated large prefixes** — order stable→volatile as with Claude.
  `applies:` 1.5+. `source:` https://ai.google.dev/gemini-api/docs/caching
  `verified:` 2026-01-15
- **Thinking models (2.5+, 3.x): set thinking budget via API**, avoid hand-scripted CoT.
  `applies:` 2.5+. `source:` https://ai.google.dev/gemini-api/docs/thinking
  `verified:` 2026-01-15
