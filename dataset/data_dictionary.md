# Data dictionary - knowledge corpus + eval set

A small synthetic knowledge base for a fictional SaaS company, **Northwind Cloud**.
**Sample material - Square 1-owned (synthetic), free for learners.** 10 markdown
documents in `corpus/` plus 8 evaluation queries in `eval_queries.jsonl`.

> Warning: this corpus is deliberately messy in two ways your pipeline must
> handle. There is a **near-duplicate** policy doc (refunds, two versions) and a
> **conflict** (data retention, two different numbers). In both cases the docs
> carry an `updated` date - the **fresher** doc is the correct one. Dedupe on
> near-identical content, and break ties by freshness. Don't hard-code which doc
> wins; let your retrieval + freshness logic find it.

## `corpus/<id>.md` - one knowledge document each

Every document begins with front matter, then a markdown body:

```
---
id: kb-refunds-2026
title: Refund policy (updated)
updated: 2026-02-20
tags: [billing, refunds, policy]
---

# Refund policy (updated)

If you are not satisfied, you may request a refund within 30 days ...
```

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable document identifier (also the filename stem). Cite this in answers. |
| `title` | string | Human-readable document title. |
| `updated` | date (ISO `YYYY-MM-DD`) | Last-updated date. **Use this to resolve duplicates/conflicts - newest wins.** |
| `tags` | list of strings | Topic tags, e.g. `billing`, `security`, `api`. |
| *body* | markdown | The help-centre content to chunk, embed, and retrieve over. |

### The dirt to handle
- **Near-duplicate pair:** `kb-refunds-2024` (older) and `kb-refunds-2026` (newer)
  cover the same policy with different numbers. Your dedupe step should detect the
  near-duplicate; your freshness logic should prefer `kb-refunds-2026`.
- **Conflict pair:** `kb-data-retention-standard` (90 days, older) and
  `kb-data-retention-business` (365 days, newer) disagree. Newest wins.

## `eval_queries.jsonl` - one JSON object per line

| Field | Type | Description |
|---|---|---|
| `query` | string | A natural-language question to answer from the corpus. |
| `expected_sources` | list of strings | Document `id`(s) that a correct retriever should surface for this query. |
| `fresh_source` | string | The single doc that should win after duplicates/conflicts are resolved by freshness. |
| `note` | string or null | Human note explaining the duplicate/conflict, where relevant. |

**What to build with it:** use `expected_sources` to score retrieval (did the
right doc come back in the top-k?) and `fresh_source` to check that your freshness
tie-breaking picks the current policy, not the stale one.

_Licence: Sample material - Square 1-owned (synthetic). No attribution required.
Regenerate with `generate_dataset.py` (seed 42)._
