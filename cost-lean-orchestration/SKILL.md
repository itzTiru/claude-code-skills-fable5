---
name: cost-lean-orchestration
description: >-
  Token-efficient model routing for complex engineering sessions. The main
  model (Opus / Fable, high reasoning) never bulk-reads or explores — it
  delegates all exploration, bulk file reading, codebase search, log scanning,
  dependency tracing, and documentation reading to Sonnet subagents that
  return compact structured findings, and it spends its own tokens only on
  synthesis, architecture, judgment, and final code. Use this skill in EVERY
  session that involves reading more than a couple of files, exploring or
  mapping a codebase, investigating a bug, auditing call sites, reviewing a
  large diff, digesting logs or docs, or any multi-step engineering task —
  even if the user never mentions cost, tokens, subagents, or delegation.
  This is a standing operating discipline, not an on-request feature.
---

# Cost-Lean Orchestration

## The core rule

The context window of the main model is the most expensive real estate in the
session. Every raw file, log dump, or search result loaded into it is paid for
on every subsequent turn, and it crowds out the reasoning the main model is
actually there for. So:

**The main model synthesizes. Sonnet subagents read.**

- Anything whose primary cost is *reading* (exploration, search, bulk file
  reading, log scanning, doc digestion, call-site auditing) → delegate to a
  **Sonnet** subagent.
- Anything whose primary cost is *thinking* (architecture, tradeoffs, subtle
  correctness, root-cause judgment, final implementation of hard code, the
  answer to the user) → keep in the **main model**.
- **Never route to Haiku.** Exploration quality feeds directly into synthesis
  quality; a missed call site or a misread invariant poisons everything
  downstream. Sonnet is the floor. If a subagent task itself demands deep
  reasoning, it doesn't belong in a subagent at all — see "Escalation" below.

This is not optional frugality. Delegating reads is what *preserves* quality:
it keeps the main context clean, focused, and far from compaction, so the
expensive reasoning happens over distilled signal instead of raw noise.

## Routing table

| Task | Route | Why |
|---|---|---|
| Map an unfamiliar codebase / find where X is implemented | Sonnet subagent(s) | Pure reading; only the map matters |
| Read 3+ files, long files, generated code, vendored deps | Sonnet subagent | Raw content must not enter main context |
| Grep-and-verify: all call sites, all usages, all configs touched | Sonnet subagent | Exhaustive, mechanical, verifiable |
| Scan logs, stack traces, CI output, test failures | Sonnet subagent | High volume, low density |
| Digest external docs, RFCs, library source, CHANGELOGs | Sonnet subagent | Summarizable; cite what matters |
| Reproduce a bug / gather evidence for competing hypotheses | Sonnet subagent(s), one per hypothesis | Parallel evidence gathering |
| Large diff review — inventory pass (what changed, where, risk hotspots) | Sonnet subagent | Inventory is reading |
| Large diff review — verdict on the risky hunks | Main model | Judgment |
| Mechanical multi-file edits from an exact, unambiguous spec | Sonnet subagent, then main-model spot-check | Execution, not design |
| Root-cause decision, architecture, API design, tradeoff analysis | Main model | This is the job |
| Final implementation of subtle/critical code | Main model | Correctness under ambiguity |
| The synthesis and the answer to the user | Main model, always | Never delegated |

When in doubt, ask: "does this step need the main model's reasoning, or just
its patience?" Patience is Sonnet's job.

## Spawning subagents

Every delegated task explicitly pins the model to Sonnet — never inherit the
(expensive) session model into a read-heavy subagent, and never let it fall
to anything below Sonnet.

- With the Task/agent tool: set `model: sonnet` (or the current
  `claude-sonnet-*` alias) on the subagent invocation.
- With custom agents in `.claude/agents/`: give exploration/reader agents
  `model: sonnet` in their frontmatter so the routing binds even when the
  main model forgets.

A good subagent prompt has four parts. Vague prompts produce rambling
returns, which defeats the purpose:

1. **Mission** — one sentence, single concern. Split multi-concern
   investigations into multiple agents rather than one omnibus agent.
2. **Scope** — exact directories, files, globs, symbols, or log ranges.
   Include what is *out* of scope.
3. **Questions** — the specific questions the main model needs answered,
   numbered. The agent answers these, not "everything interesting."
4. **Return contract** — the exact format below, with the token budget
   stated in the prompt.

Run independent subagents **in parallel in the same turn** (different
hypotheses, different subsystems, code + docs). Serialize only when one
agent's output genuinely determines the next agent's scope.

## The return contract

Subagents return distilled findings, never raw material. Put this template
verbatim in every subagent prompt:

```
## ANSWERS
For each numbered question: a direct answer in 1–3 sentences.
If unknown after genuine search, say UNKNOWN — never guess.

## KEY FACTS
Bullet list of load-bearing facts discovered beyond the questions.
Each fact ≤2 sentences, each with a file:line reference.

## EVIDENCE
Only verbatim snippets the main model must see with its own eyes
(exact signatures, invariants, error messages, config values).
Each snippet ≤15 lines, prefixed with path:line-range.
Hard cap: 5 snippets. Summaries elsewhere, quotes only here.

## GAPS & RISKS
What you could not verify, what looked suspicious, where the scope
should be widened. Empty is a valid answer; padding is not.

## CONFIDENCE
HIGH / MEDIUM / LOW, one sentence on why.
```

Budget: **≤600 tokens** for a focused question, **≤1200** for a subsystem
survey. State the budget in the prompt. Over-budget returns mean the mission
was too broad — split it next time rather than accepting a dump.

Two hard rules for the receiving side:

- **No pasted files.** If a subagent returns a file body, that's a failed
  delegation — re-prompt with a tighter contract instead of absorbing it.
- **File:line references are mandatory.** They let the main model do surgical
  follow-up reads of exactly the 20 lines that matter, instead of re-reading
  what the subagent already covered.

## What the main model does instead of reading

- Decomposes the problem and writes precise subagent missions.
- Cross-checks subagent returns against each other; contradictions between
  agents are signal, not noise — resolve them with a targeted follow-up
  agent or a surgical direct read.
- Reads directly only: the specific lines it is about to edit, the ≤15-line
  evidence snippets, and anything a subagent flagged as too subtle to
  summarize.
- Reasons, decides, designs, writes the hard code, and answers the user.

## Escalation — when NOT to delegate

Delegation protects quality; these cases are where delegation would damage it:

- **The reading IS the reasoning.** A subtle concurrency bug where
  understanding requires holding the whole interleaving in one head; a proof;
  security-critical code where a summary might launder away the flaw. Read it
  directly — but surgically, the relevant region only, guided by a subagent's
  map of *where* to look.
- **A subagent returns LOW confidence or contradicts another.** Don't paper
  over it in synthesis. Either spawn a narrower verification agent or read
  the disputed lines yourself.
- **Tiny sessions.** One or two small files, a quick question — spawning
  agents costs more than it saves. This skill targets multi-file,
  multi-step work; don't cargo-cult it onto trivia.
- **The user asks to see raw content.** Their request wins; show it.

Never ask a Sonnet subagent to make the architectural call, pick the fix, or
write the subtle patch "while it's in there." Subagents gather and execute;
they do not decide.

## Anti-patterns (each one is a real failure mode)

- ❌ Main model runs broad greps/globs and reads result files itself "just to
  get oriented." Orientation is exactly what a mapper subagent is for.
- ❌ `cat`-ing a 2,000-line file into main context to find one function.
- ❌ One giant subagent with a 10-item mission returning a 5,000-token essay.
- ❌ Subagent returns prose without file:line refs, forcing re-reads later.
- ❌ Downgrading a subagent to Haiku to save a little more. The savings are
  marginal; the missed-detail risk is not. Sonnet, always.
- ❌ Sequentially spawning agents that had no dependency on each other.
- ❌ Delegating the final synthesis, verdict, or user-facing answer.

## Session shape (reference)

For a nontrivial task, the turn structure should look like:

1. Main model: restate goal, decompose, define missions. (thinking, cheap)
2. Parallel Sonnet agents: explore/read/verify per contract. (bulk tokens,
   cheap model, disposable contexts)
3. Main model: cross-check returns, surgical direct reads of ≤15-line
   regions, decide. (thinking)
4. Sonnet agents for mechanical execution and exhaustive verification;
   main model for the subtle code.
5. Main model: synthesize and answer.

If step 2 is missing from a read-heavy session, the routing has failed —
correct it on the next turn, not at compaction time.
