# Audit Dimensions

One Sonnet subagent per dimension. Each agent receives: (1) the prompt text, (2) the
rubric section for the target model, (3) its dimension brief below, (4) the API
configuration discovered in Phase 1 (extended thinking on/off, structured output/tool
use, caching, temperature) — or "config unknown" if not discoverable. When a rule's
applicability depends on configuration the agent wasn't given, it still reports the
finding but prefixes the issue with `CONDITIONAL (applies only if <config>):`. It returns ONLY a JSON
list of findings:

```json
[{"rule": "…", "citation": "source URL", "severity": "critical|major|minor",
  "location": "section/line", "current_text": "…", "issue": "…", "suggested_fix": "…"}]
```

Empty list if the dimension is clean. No prose, no doc excerpts.

Severity: **critical** = provider explicitly warns against it or it breaks the feature
(e.g. prefill with extended thinking, CoT-prompting an o-series model). **major** =
documented recommendation violated with likely quality impact (ordering, tagging,
schema-in-prose). **minor** = style/polish with marginal impact.

## Dimensions

1. **structure-tagging** — Are sections delimited the way this provider recommends (XML
   tags for Claude, headers/delimiters for OpenAI)? Do instructions and data bleed
   together?
2. **placement-ordering** — Long-context ordering: documents vs instructions position,
   query placement, instruction repetition rules for this model.
3. **role-system-usage** — Is the system prompt role-only? Task instructions leaking into
   system, or persona leaking into user turns?
4. **output-format** — Is the output spec aligned with the model's native structured
   path (tool schema / json_schema strict / responseSchema)? Prose-described JSON where a
   schema belongs? Format described once, unambiguously?
5. **examples-fewshot** — Right number and diversity of examples for this model family
   (3–5 diverse for Claude/Gemini; minimal for o-series). Examples consistent with the
   stated format? Edge cases covered?
6. **caching-layout** — Stable→volatile ordering; variable content (dates, filenames,
   user input) appearing before stable blocks; cache breakpoint placement.
7. **model-specific** — Rules unique to this model version: extended-thinking dos/don'ts,
   eagerness/verbosity controls, parallel tool-call guidance, migration notes.
8. **anti-patterns** — Known failure modes for this family: heavy negation framing,
   conflicting instructions, hand-scripted CoT on reasoning models, redundant politeness
   padding, instruction duplication that drifts.
