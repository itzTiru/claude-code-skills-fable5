# Rewrite Rules

The rewrite is the findings applied — nothing more.

1. **Every change maps to a finding.** Each edit cites the rubric rule (and its source
   URL) that motivated it. An edit with no finding behind it is reverted.
2. **Domain content is verbatim.** Definitions, legal terms, schema field names, business
   rules, thresholds, examples' factual content — copied exactly. The rewrite may MOVE
   domain content (ordering/tagging) but never rephrase it. If a domain sentence is
   genuinely defective (ambiguous, contradictory), flag it as a finding for the user
   instead of fixing it silently.
3. **Preserve intent under structure change.** When converting prose to schema/tags,
   every requirement in the original must be locatable in the rewrite. Build a
   requirement checklist from the original; tick each against the rewrite.
4. **Adversarial drift check.** After writing, dispatch one Sonnet agent with old + new
   prompt and one question: "List every instruction, constraint, or fact present in one
   version but absent or weakened in the other." Fix everything it reports; rerun until
   clean.
5. **Output shape:** side-by-side per section — original block, rewritten block, then
   `Why:` one line per change with rule + citation. Unchanged sections listed by name
   only ("unchanged").
6. **Approval gate.** The rewrite lives in the report until the user approves; only then
   edit source files, preserving surrounding code (string quoting, f-string interpolations,
   indentation) exactly.
