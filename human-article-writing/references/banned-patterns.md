# Banned patterns catalog

The authoritative list of patterns that must never appear in output. Derived from documented research on AI-generated text detection. Organized by category. "Banned" means banned in the skill's own prose; quoting someone else's words is exempt.

## 1. Banned vocabulary

Never use these words/phrases in body prose. The issue is not the word in isolation but that these are statistically overrepresented in LLM output and co-occur; even two or three in one piece is a strong tell. Synonyms not on this list are fine.

**Core banned list (all eras):**
delve, tapestry (abstract), landscape (abstract, e.g. "the AI landscape"), testament, pivotal, crucial, robust, meticulous / meticulously, intricate / intricacies, interplay, underscore (verb), showcase (verb), boasts (meaning "has"), garner, bolstered, vibrant, enduring, fostering / foster, cultivating, encompassing, enhance / enhancing, highlighting (as analysis), emphasizing (as analysis), align with / aligns with, resonate with, valuable insights, key (as adjective: "key role", "key moment"), seamless / seamlessly, leverage (verb), elevate (figurative), realm, embark, navigate (figurative: "navigating the complexities"), ever-evolving, evolving landscape, rapidly changing world, in today's world, groundbreaking, renowned, nestled, in the heart of, rich history / rich heritage, natural beauty, diverse array, comprehensive (as filler), holistic, multifaceted, paradigm shift (unless quoting), game-changer / game-changing, unlock (figurative), harness (figurative), empower (figurative), transformative, revolutionize / revolutionary (as praise), state-of-the-art (as filler), cutting-edge (as filler), at the forefront, cornerstone (figurative), beacon (figurative), catalyst (figurative filler), synergy, dynamic (as praise), profound (as filler), remarkable (as filler), notable / notably (as filler), significant / significantly (when a concrete number or fact could replace it).

**Significance-inflation phrases (banned):**
stands as / serves as / marks a / represents a (in place of "is"), is a testament to, is a reminder of, plays a vital/significant/crucial/pivotal/key role, underscores its importance, highlights its significance, reflects broader (trends/shifts), symbolizing its ongoing/enduring/lasting, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, focal point, indelible mark, deeply rooted, far-reaching implications, cannot be overstated.

**Sentence-opener bans:**
"Additionally," at the start of a sentence (use "Also," "And," or restructure), "Moreover," "Furthermore," as mechanical connectors, "In today's fast-paced...", "In the world of...", "In an era of/where...", "As technology continues to...", "It's important to note that...", "It's worth noting that...", "Interestingly," (as filler), "Ultimately," (as a wrap-up crutch).

**Wrap-up bans:**
"In summary", "In conclusion", "Overall,", "To sum up", "At the end of the day" (as a closer), any final paragraph that restates the piece.

## 2. Banned syntactic constructions

**Copula avoidance.** Do not replace *is/are/has* with fancier verbs:
- Bad: "The protocol serves as the interface layer." Good: "The protocol is the interface layer."
- Bad: "The tool boasts a plugin system." Good: "The tool has a plugin system."
- Bad: "X refers to the practice of..." Good: "X is..." (unless genuinely defining a term).
- Prefer the plain verb generally: wrote > authored, used > utilized, tried > attempted, moved > relocated, showed > demonstrated (when plain fits), began > commenced, ended > concluded, about > approximately (in casual registers), died > passed away.

**Negative parallelism family.** All of these are heavily overused by LLMs:
- "Not just X, but Y" / "Not only X but also Y"
- "It's not X, it's Y" / "This isn't X. It's Y."
- "X is not merely..., it is..."
- "no X, no Y, just Z"
- "X rather than Y" as a repeated framing device
Hard limit: at most one deliberate contrast construction per entire article, and prefer zero. Titles chosen by the user are exempt but flag the risk.

**Rule of three.** Exactly-three parallel items ("fast, cheap, and reliable"; three parallel clauses; three-bullet lists) are an AI fingerprint when repeated. Break the symmetry: use two items, four items, or make the items grammatically uneven ("policies, state, and the need to prove the thing behaves").

**Participle analysis tails.** Sentences must not end with an "-ing" clause that bolts on interpretation:
- Banned shape: "..., highlighting the importance of X." / "..., underscoring Y." / "..., reflecting broader trends." / "..., ensuring Z." / "..., contributing to W." / "..., demonstrating its ongoing relevance."
- Fix: if the interpretation is worth keeping, make it its own sentence with a concrete, defensible claim; otherwise delete it.

**Weasel attributions.** Banned: "experts argue", "critics say", "observers have noted", "industry reports suggest", "many believe", "several publications", "scholars agree", "it is widely regarded". Either name the specific source (person, paper, outlet, with a real link) or state it as your own view.

**Overgeneralized sourcing.** Do not present one source as many ("reviewers praised..." citing one review). Do not imply a list is non-exhaustive ("outlets such as X, Y, and Z") unless you know more exist.

**Didactic disclaimers.** Banned: "it's important/critical/crucial to note/remember/consider", "it's worth noting", "keep in mind that", "one must remember", "may vary depending on...".

**Knowledge-hedging boilerplate.** Banned: "while specific details are limited", "based on available information", "not widely documented", "as of my last update", and any similar disclaimer. If information is missing, say so plainly and specifically ("I couldn't find load-test numbers for this") or ask the user.

## 3. Banned structure and formatting

**Headings:** sentence case only. Never Title Case. Never emoji. Never numbered scheme headings ("1. Introduction", "2. Background"). Never a "Conclusion", "Challenges", "Future Outlook/Prospects", or "Final Thoughts" section. Never skip heading levels.

**Lists:** default to prose. In-sentence lists read as "the main costs are latency, tokens, and reviewer time". If a vertical list is genuinely clearer (rare in articles), never use the pattern `**Bold Term:** explanation` or `- **Header** — text`. Plain items only, and keep each item a full sentence or more.

**Bold:** maximum a few bolded phrases per long article, and only when a skimming reader genuinely needs the anchor. Never bold every instance of a term. Never bold "key takeaways".

**Em dashes (—):** zero. Replace with comma, colon, parentheses, or a new sentence. En dashes only for numeric ranges (2019–2023).

**Quotes/apostrophes:** straight only (" and '). No curly marks.

**Emoji:** none.

**Horizontal rules (`---`):** none between sections.

**Tables:** only when comparing genuinely tabular data the reader will scan. Never a two-column "Metric | Figure" table that could be one sentence.

**"Challenges → resolution" arc:** banned as a formula. "Despite these challenges, X continues to..." and "Despite its success, X faces challenges including..." are canned endings.

**Section symmetry:** avoid 6+ sections of near-identical length with parallel heading grammar. Human structure is lumpy; one section can be triple the length of another.

## 4. Banned content habits

**Significance inflation.** Never assert importance, legacy, impact, or connection to "broader trends" without a specific, checkable fact. The test: could this sentence be pasted into an article about a different subject unchanged? If yes, delete it.

**Puffery.** No press-release tone: "commitment to excellence", "world-class", "seamlessly connects", "value-driven experiences", "state-of-the-art facilities". When rewriting marketing-ish drafts, remove puffery; do not add subtler puffery in its place.

**Superficial "sparked debate" claims.** Do not claim something "raises questions", "has prompted discussion", or "has generated debate about X, Y, and Z" unless you can point to the actual debate (who, where, link).

**Both-sidesing to nowhere.** Human argumentative writing takes a position. Do not write "there are valid points on both sides" paragraphs that decline to conclude, unless genuine uncertainty is the honest position, in which case say specifically what is unknown and what evidence would settle it.

**Fabrication (absolute bans):**
- No invented citations, DOIs, ISBNs, page numbers, URLs, or quotes. Every link must come from the user, from search results in this conversation, or be omitted.
- No invented statistics or study findings. "Studies show" with no study is banned twice over (weasel + fabrication).
- No invented personal experience or anecdotes. Use a bracketed placeholder and tell the user to supply the real story.
- No placeholder text left unfilled in the final deliverable without flagging it loudly.

## 5. Markup hygiene (when output is for a specific platform)

- LinkedIn: no markdown renders; deliver clean plain text with blank-line paragraph breaks. Headings become short standalone lines. No asterisks, no hashes.
- Blogs/markdown: normal markdown is fine within the formatting rules above.
- Never emit artifacts like `turn0search0`, `oaicite`, `utm_source=chatgpt.com`, `[cite: 3]`, `:::writing`, or stray code fences. Strip UTM parameters from any URL before including it.

## 6. Positive human signals (actively include)

These correlate with human writing; use them naturally, never mechanically:

- Plain is/are/has constructions, including "there is a" and "it has a".
- Simple wordy connectives humans actually use: "as a result of", "in order to", "the fact that", "a part of".
- True, sourced superlatives and definitives: "the first paper to measure this", "the only vendor that publishes latency numbers".
- Hedges and intensifiers: "very", "perhaps", "tends to", "roughly", "I suspect", "I'm not sure this holds".
- Concrete numbers, names, dates, versions, and prices instead of adjectives.
- First-person stakes: a position the writer defends, a prediction that could be wrong, a concession to the other side.
- Rhythm variance: an occasional two-word sentence. An occasional long one that takes a breath in the middle and keeps going because the thought genuinely needs the room.
- Register-appropriate contractions.
- Ending on the argument, an implication, or a real question to the reader, never a summary.

## 7. Quick regex-style sweep (run before delivery)

Search the final text for each of these; every hit must be justified or removed:

```
— “ ” ‘ ’ 🙂-class emoji
delve | tapestry | landscape | testament | pivotal | crucial | robust |
meticulous | intricate | interplay | underscore | showcase | boasts |
garner | bolster | vibrant | enduring | foster | enhance | leverage |
seamless | groundbreaking | renowned | nestled | comprehensive | holistic |
transformative | game-chang | cutting-edge | state-of-the-art | cornerstone |
ever-evolving | navigate the | realm | embark | harness | empower | unlock
"serves as" | "stands as" | "refers to" | "plays a . role" |
"not just" | "not only" | "it's not .*, it's" | "rather than" (count) |
"highlighting" | "underscoring" | "reflecting" | "ensuring" (sentence-final) |
"experts" | "observers" | "critics say" | "widely regarded" |
"important to note" | "worth noting" | "In summary" | "In conclusion" |
"Overall," | "Ultimately," | "Additionally," | "Moreover," | "Furthermore," |
"Despite these challenges" | "faces several challenges" | "Future Outlook"
```
