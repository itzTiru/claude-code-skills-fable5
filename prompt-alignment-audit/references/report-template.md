# Report Template

```markdown
# Prompt Alignment Audit — <prompt name / file:line>

**Target model:** <exact model ID> · **Rubric verified:** <date per section used>
**Guidance freshness:** current | STALE (research tools unreachable — rubric dated <date>)
**Verification:** eval-backed (<harness name>) | compliance-based only

## Findings (<n> total: <c> critical, <m> major, <k> minor)

| # | Severity | Dimension | Rule violated | Location | Issue |
|---|----------|-----------|---------------|----------|-------|
| 1 | critical | …         | <rule> ([source](url)) | … | … |

## Rewrite (proposal — not applied)

### <section name>
**Original:**
<block>
**Rewritten:**
<block>
**Why:** #1 <rule> — <one line>. #4 <rule> — <one line>.

### <unchanged sections>: <names>, unchanged.

## Eval results (only if harness ran)
| Prompt | <metric> |
|--------|----------|
| original | … |
| rewritten | … |

## Next step
Approve to apply to <file(s)>, or request changes.
```

Rules: findings table sorted by severity; every rule cites its source URL; if the model ID
was substituted with a nearest-family rubric, say so under the header; if confidence is
compliance-based, the report says "compliance-based only" verbatim.
