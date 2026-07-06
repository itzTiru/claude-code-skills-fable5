---
name: human-article-writing
description: Write, rewrite, or edit articles, LinkedIn posts, blog posts, essays, newsletters, and other long-form prose so the result reads as high-quality, natural human writing with none of the stylistic patterns typical of AI-generated text. Use this skill whenever the user asks for an article, post, essay, opinion piece, or long-form draft, whenever they ask to "humanize", "rewrite", "polish", or "fix the tone" of existing text, and whenever they mention AI-sounding writing, detection, or wanting text that reads like a person wrote it — even if they don't say "article" explicitly.
---

# Human-quality article writing

This skill produces long-form prose that reads like it was written by a skilled, opinionated human, and edits existing drafts to the same standard. It encodes a large catalog of known AI-writing patterns (vocabulary, syntax, structure, formatting, and content habits) as hard constraints, plus the positive habits of strong human writers.

The goal is not disguise for its own sake. Text that avoids these patterns is genuinely better writing: more specific, less padded, more honest about uncertainty, and more pleasant to read. Treat every rule here as a craft rule first.

## Workflow

Follow these steps in order for both new drafts and rewrites.

**1. Read the full pattern catalog.** Before writing a single sentence, read `references/banned-patterns.md`. It is the authoritative list of what must never appear in output. Do not rely on memory of it; the details matter (specific words, specific constructions, specific formatting habits).

**2. Establish grounding.** Collect the real facts, sources, and claims the piece will rest on. Rules:
- Never invent sources, quotes, statistics, links, or publication dates. If a link is provided by the user or found via search, use it verbatim; never construct a plausible-looking URL.
- Never invent first-person experience ("I have seen this in production", "teams I talk to"). If a personal anecdote would strengthen the piece, insert a clearly marked placeholder like `[YOUR EXAMPLE: a time a deploy broke because of X]` and tell the user to fill it, or ask them for a real one before drafting.
- If a claim can't be sourced, either cut it or state it as opinion ("my read is...", "I suspect...").

**3. Plan the argument, not the outline.** Decide what the piece claims, who disagrees and why, and what the reader should do or believe at the end. A human article is an argument with a spine; an AI article is a survey with headings. Prefer 3–6 sections with sentence-case headings over 8+ symmetric sections. It is fine (often better) for sections to be unequal lengths.

**4. Draft in a human register.** Apply the voice rules below and the full catalog from step 1.

**5. Self-audit.** Run the checklist at the bottom of this file against the finished draft, line by line. Fix every hit, then re-read the whole piece aloud in your head for rhythm. If two consecutive sentences have the same shape, break one.

**6. Deliver honestly.** When presenting the draft, flag any placeholders the user must fill, any claims that need their verification, and any stylistic risks you accepted deliberately (for example, a contrast-heavy title the user chose).

## Core voice rules

These are the highest-leverage rules. The full catalog in `references/banned-patterns.md` extends them.

**Say it plainly.** Use *is*, *are*, *has*. Never replace them with *serves as*, *stands as*, *boasts*, *features*, *represents*, *marks*, or *refers to*. Use *wrote* not *authored*, *used* not *utilized*, *tried* not *attempted*, *moved* not *relocated*, *died* not *passed away*.

**Be specific or be silent.** Cut every sentence that asserts importance, significance, legacy, or "broader trends" without a concrete fact behind it. "The framework changed how three of our services handle retries" survives; "the framework plays a pivotal role in the evolving landscape" dies. Specificity is the single strongest human signal.

**One idea per sentence, varied rhythm.** Mix short declaratives with longer ones. Let some paragraphs be two sentences. Never let every paragraph run 4–5 sentences of equal length.

**Have a stake.** First person, real opinions, honest hedges ("I'd argue", "I'm not sure this holds at scale", "the public data here is thin"). Disagree with someone real. Concede something. AI text is agreeable and stakeless; human text picks a fight and admits limits.

**Contractions and mild informality are allowed** in registers where the user would use them (LinkedIn, blogs, newsletters). Match the user's own register when rewriting their draft.

**Punctuation discipline:**
- No em dashes (—). Use commas, colons, parentheses, or a full stop instead. This is a hard rule regardless of how natural a dash would feel.
- Straight quotes (") and straight apostrophes (') only. Never curly (“ ” ‘ ’).
- No emoji anywhere (headings, bullets, body) unless the user explicitly asks.

**Formatting discipline:**
- Sentence-case headings ("The failure modes are new"), never Title Case ("The Failure Modes Are New").
- Prose over lists. Convert would-be bullet lists into sentences ("the main costs are latency, tokens, and reviewer time"). If a list is genuinely necessary, never use the bold-inline-header pattern (`**Term:** explanation`).
- Bold sparingly: at most a handful of bolded phrases in a long piece, never mechanical "key takeaway" bolding.
- No horizontal rules between sections. No "Conclusion" / "In summary" / "Final thoughts" section; end on the argument itself, a concrete implication, or a genuine question.

**Structural discipline:**
- No "Not just X, but Y", "It's not X, it's Y", or "X rather than Y" pivots as a recurring device. One deliberate contrast in an entire piece is the ceiling.
- Break the rule of three. Lists of exactly three parallel items are an AI fingerprint; use two, four, or deliberately uneven phrasing.
- No participle-phrase analysis endings ("..., highlighting the importance of...", "..., underscoring...", "..., reflecting broader..."). If the analysis matters, give it its own sentence with a concrete claim.
- No weasel attributions ("experts argue", "observers note", "industry reports suggest"). Name the person, paper, or company, or own the claim yourself.
- No "Despite these challenges..." arcs, no "Challenges" or "Future Outlook" sections, no didactic disclaimers ("it's important to note", "it's worth remembering").

## Rewriting mode

When the user provides an existing draft to humanize or improve:

1. Diagnose first: list the specific patterns present (cite the catalog), so the user learns what was wrong.
2. Rewrite at the sentence level, not by paraphrasing whole paragraphs; preserve the user's facts, structure choices, and any genuinely human quirks already there (an odd aside, a personal detail, an unusual word). Do not sand those off.
3. Do not "fix" things into new tells. The classic failure is replacing bullet spam with triads and em dashes. Re-run the self-audit on your own rewrite.

## Self-audit checklist

Run every item against the finished text. A single miss means revise.

- Search the text for every word in the "banned vocabulary" list in `references/banned-patterns.md`. Zero tolerance in body prose (quoting someone else is fine).
- Search for `—`, curly quotes, and emoji: must be zero.
- Scan every heading: sentence case only, no numbering scheme like "1. Introduction".
- Scan sentence endings for `-ing` analysis clauses.
- Count contrast constructions ("not X but Y" family): more than one, cut down.
- Count exact-three parallel lists: rewrite them.
- Check every bolded phrase: does it need bold? Usually no.
- Check the ending: if the last paragraph starts with "In summary/conclusion/Overall/Ultimately", rewrite it.
- Check every factual claim, name, number, and link against the grounding from step 2. Anything unverified gets flagged to the user or cut.
- Check for invented personal experience: none unless the user supplied it.
- Read for rhythm: any three consecutive sentences with identical structure, vary one.
- Check register consistency: the piece should sound like one person on one day, not a committee.

## What not to over-correct

Avoiding AI tells does not mean avoiding good writing. Keep: perfect grammar, formal register where the venue calls for it, transition words used naturally (not formulaic sentence-initial "Additionally,"), occasional long sentences, superlatives that are true and sourced ("the first paper to measure this"), and hedging qualifiers ("perhaps", "tends to"), which are actually human signals. Do not inject typos or fake sloppiness; the goal is a skilled human, not a careless one.
