# Substance Retrieval

Stage 2. The difference between this pipeline and a content generator.

## The principle

A fragment is a **pointer**, not content. `"pub_count was measuring name commonality lol"` is not a post
— it is a note saying *go look at that thing*. This stage goes and looks.

Specificity is **retrieved**, never invented. If a draft needs a number, the number comes from an
artifact. If no artifact can be found, the draft does not get written. There is no step in this pipeline
where a plausible-sounding detail may be supplied by the model.

The upstream repo this was forked from required "1 specific micro-anecdote (day, person, physical
object)" in every case-study post. That instruction exists only because its generator had no real
material. Manufacturing a specific detail about your own work is fabricating a claim about your own work.
This stage exists so that rule is never needed.

## Where to look

Work down this list. Stop when you have hard evidence; record everything you used.

1. **The repos.** `git log -S<term>`, `git log --grep`, then read the actual diff. A commit that fixed the
   thing is the strongest possible evidence: it has a date, an author, a before, and an after.
2. **Eval and test output.** Result files, benchmark JSON, CI logs. Numbers with a reproducible command
   behind them are the best material there is.
3. **Granola transcripts.** For anything that came out of a conversation — a customer's phrasing of a
   problem, an advisor's objection, a decision and its reasoning.
4. **Notion docs.** Decision records, findings docs, project pages.
5. **The user's own memory files.** `~/.claude/projects/*/memory/` — prior verified findings, already
   distilled. Treat as a strong lead, but re-verify anything it asserts about current code before
   publishing: memories reflect what was true when written.
6. **External sources**, for anything about the wider world — a vendor's docs, a standard, a paper. Cite
   the URL. Never assert a third party's behaviour from memory; go read their current docs.

## What counts as evidence

| Strength | Looks like |
|---|---|
| **5** | A measured result with a reproducible command or a commit: *"identity-gated query cut false matches 97.4%, `atlas/eval/pubmed_identity.py`, run 2026-08-14"* |
| **4** | A concrete artifact without a clean number: a commit that fixed it, a transcript quote, a vendor doc page contradicting expected behaviour |
| **3** | A firsthand observation the user made, recorded somewhere at the time, but not measured |
| **2** | The user remembers it. Nothing written down. |
| **1** | Inference, pattern-matching, or "this is generally true" |

**3 and below cannot support a factual claim in a post.** They can support a labelled opinion. The
distinction must survive into the draft.

## Recording provenance

Fill `Evidence` with what you found, and `Provenance` with where each piece came from, specifically
enough that the reviewer can re-check it in under a minute:

```
Evidence:
- pub_count previously matched on author surname only → matched every same-named
  author in PubMed
- identity-gated query (surname + affiliation + specialty) cut false matches 97.4%
- two traps found: (1) middle-initial variants break exact match,
  (2) affiliation strings change between papers for the same person

Provenance:
- synthio-atlas @ 4f2c1ab "fix: identity-gate pubmed author query" (2026-08-14)
- eval output: synthio-atlas/eval/out/pubmed_identity_2026-08-14.json
- memory: atlas-pubmed-name-collision.md (re-verified against current query builder)
```

## When retrieval fails

Set `Status = New`, fill `Blocked on`, and say precisely what is missing:

> `Blocked on: no eval output found for the 97.4% figure — only referenced in a Slack message. Need
> either the eval JSON or a re-run before this can be claimed as measured.`

Then stop. Do not draft it. Do not write around the gap with hedged language — a hedge on a number you
cannot find is still a claim you cannot support.

## De-identification

Retrieval reaches into customer calls and internal docs. Before evidence leaves this stage:

- Strip customer, prospect, and individual names. Generalise to a category: *"a large oncology network"*.
- Strip pricing, contract terms, and anything unannounced.
- Strip all patient-related and clinical record data, without exception.
- Keep the technical finding. That is the postable part, and it survives de-identification intact.

If the finding is inseparable from the identity, archive the row. Say so in `Blocked on`.
