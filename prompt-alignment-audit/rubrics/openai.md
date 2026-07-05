# OpenAI — Prompting Rubric

Entry format: **Rule** — why. `applies:` model families. `source:` URL. `verified:` date.
Entries older than 7 days (or missing your model) must be refreshed via Context7/Exa.

> **SEED NOTICE:** Seeded from training data on 2026-01-15; intentionally stale so the
> first real run refreshes from live docs.

## gpt-5.x

- **Calibrate agentic eagerness explicitly** — GPT-5 follows instructions with surgical
  precision; state persistence/stop conditions, and remove conflicting instructions (they
  degrade it more than older models). `applies:` gpt-5.x.
  `source:` https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide
  `verified:` 2026-01-15
- **Use API controls over prompt hacks** — verbosity and reasoning-effort parameters
  replace "be brief"/"think hard" prose. `applies:` gpt-5.x.
  `source:` https://platform.openai.com/docs/guides/latest-model
  `verified:` 2026-01-15
- **Structured outputs via `json_schema` strict mode**, not prose-described JSON.
  `applies:` gpt-4.x+, gpt-5.x. `source:` https://platform.openai.com/docs/guides/structured-outputs
  `verified:` 2026-01-15

## o-series / reasoning models (o3, o4-mini)

- **Do NOT prompt step-by-step CoT** ("think step by step" hurts — the model reasons
  internally); keep prompts simple and direct. `applies:` o-series.
  `source:` https://platform.openai.com/docs/guides/reasoning-best-practices
  `verified:` 2026-01-15
- **Minimal or zero few-shot** — examples can degrade reasoning models; start zero-shot,
  add only targeted examples. `applies:` o-series.
  `source:` https://platform.openai.com/docs/guides/reasoning-best-practices
  `verified:` 2026-01-15
- **Use `developer` messages per Model Spec** (system→developer mapping). `applies:`
  o-series, gpt-5.x. `source:` https://platform.openai.com/docs/guides/text-generation
  `verified:` 2026-01-15

## gpt-4.x (gpt-4o, gpt-4.1)

- **Delimit with markdown headers/fenced blocks or XML**; instructions at both start and
  end for long context (4.1 long-context guidance). `applies:` gpt-4.1.
  `source:` https://cookbook.openai.com/examples/gpt4-1_prompting_guide
  `verified:` 2026-01-15
- **Agentic prompts: three reminders** (persistence, tool-calling, planning) markedly
  improve 4.1 agent behavior. `applies:` gpt-4.1.
  `source:` https://cookbook.openai.com/examples/gpt4-1_prompting_guide
  `verified:` 2026-01-15
