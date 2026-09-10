# Epistemic Gate

Runs in stage 3, before a draft reaches the human. Adapted from
[Clarity Gate](https://github.com/frmoretto/clarity-gate) by Francesco Marinoni Moretto, via the
upstream repo.

## What changed from upstream

Upstream's stated reason for this gate was that a wrong fact in a comment could *"expose the
automation to the original poster and their network."* The gate existed to protect the disguise.

Here it exists because publishing something false under your own name is bad on its own terms. The
checks are similar; the purpose is not. And it now runs at **source time** — against retrieved
evidence — rather than as a polish pass over already-written prose. A gate applied after the fact
can only soften wording. Applied before, it can stop a claim from being made.

## The labels

Every factual claim in a draft carries exactly one, recorded in the row's `Labels` field. Labels are
working notes for the reviewer and are stripped from the published text.

| Label | Means | Requires |
|---|---|---|
| `[MEASURED]` | A number produced by a run you can point at | An eval output, test result, or commit in `Provenance` |
| `[OBSERVED]` | You saw it happen, recorded at the time | A transcript, log, doc, or dated note |
| `[INFERRED]` | A conclusion drawn from the above | The underlying `[MEASURED]`/`[OBSERVED]` items it rests on |
| `[OPINION]` | A view, held for reasons | Nothing — but it must read as a view in the published text |

**A claim that cannot carry a label gets cut, not hedged.** Softening an unsupported claim into
"it seems that..." leaves an unsupported claim in the post. Delete the sentence.

## The seven checks

1. **Fact vs inference.** For each sentence: is this measured, observed, inferred, or opinion? Mixing
   an inference into a list of measurements makes the whole list read as measured.

2. **Uncertainty matches evidence.** `[MEASURED]` gets stated flat: "cut false matches 97.4%."
   `[INFERRED]` gets its reasoning visible: "which suggests the matcher was keying on surname alone."
   `[OPINION]` gets owned: "I think", "my read is". Never state an inference flat, and never hedge a
   measurement — false modesty about real data is its own inaccuracy.

3. **Source attribution.** Any claim about a third party's product, a standard, or a paper needs a
   URL checked against the *current* version. Vendor behaviour changes. A remembered API limitation
   is not a source.

4. **Temporal coherence.** Is this still true? A finding from four months ago may have been fixed —
   by you. Re-verify against current code before publishing. Memory files record what was true when
   written, not what is true now.

5. **Claims about other people's situations.** The hardest one to get right. You do not know why
   another team made a choice. Convert assertion into observation plus question:
   - ✗ "Nobody had signed off on the deploy."
   - ✓ "The pattern I see is a gap in deploy ownership."

6. **Self-assessment bias.** You are the least reliable narrator of your own result. Check: is the
   comparison fair? Was the baseline real or convenient? Would a competitor describe this number the
   same way? State what the result does *not* show.

7. **Absence as proof.** "No one is doing this" almost always means "I did not find anyone doing
   this." "It's impossible" usually means "I could not find a way." Say the weaker, true thing.

## Scoring

Count checks passed. This gates the draft, not the reviewer.

| Result | Action |
|---|---|
| 7/7 | Send to review |
| 6/7 | Fix the failing check, re-run |
| 5/7 | Fix both, re-run. If either failure is check 1 or 3, treat as below. |
| ≤4/7 | Do not send. Return the row to `Sourced` with `Blocked on` naming the failed checks. The problem is the evidence, not the wording. |

## Rules of thumb

- If you cannot name the artifact behind a number, the number does not go in the post.
- "Roughly", "about", "~" are fine on a measured number with a real range. They are not a way to
  publish a number you do not have.
- One finding, one post. Bundling a weak claim with a strong one launders the weak one.
- If the honest version of a post is boring, the post is boring. Do not fix that by making it less
  honest — return the row to the queue and wait for better material.
- When the gate and the reviewer disagree, the reviewer wins. They are accountable for the words;
  this file is not.
