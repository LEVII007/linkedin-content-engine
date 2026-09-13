# Idea Inbox

The only source of topics. If it is not in here, it does not get written about.

## Why a raw inbox and not a calendar

A calendar creates seven slots a week and demands they be filled. Nobody has seven real things to say in
a week. The gap between slots and substance is exactly where invented content comes from — and invented
specifics in a post about your own business are fabricated claims about your own business.

An inbox inverts it: substance arrives when it arrives, and cadence follows. Expect roughly one post a
week. Some weeks zero. That is the system working.

## Capture: Slack `#content-inbox`

Active capture. Friction is the enemy, so the bar is deliberately on the floor.

**Rules for the human:** none. Drop the thought. Don't structure it, don't finish the sentence, don't
explain it. If it needs explaining, the retrieval step will go find the explanation.

Valid fragments:

```
cms 403s from india, silent empty
pub_count was measuring name commonality lol
phoneme tags just... don't do anything on prod?
RAG is not enough for this and everyone keeps assuming it is
MoveParticipant is cloud-only. two days to find that out.
oncologist on the MOC call said something about facts vs recommendations
```

Every one of those is enough. Each names a real thing that happened; retrieval fills in the rest.

### Threads count

If someone replies to a fragment in-thread, the whole thread is one fragment. Discussion adds context —
keep it, it usually contains the "why it matters" that the original one-liner omitted.

### Anything not a fragment

Ignore messages that are logistics (`"on a call, back in 20"`), links with no comment, or replies that
only react (`"nice"`, emoji-only). Do not archive them from Slack — just don't ingest them.

## Passive sources

No capture effort required. These run whether or not anyone remembers to write anything down.

| Source | What to pull | How |
|---|---|---|
| **Granola** | Meeting transcripts — customer calls, internal reviews, advisor sessions | `query_granola_meetings` / `get_meeting_transcript`, last 7 days |
| **Git** | Commit messages, PR titles/descriptions, merged branch names across the user's repos | `git log --since` over each repo |
| **Notion** | New or substantially edited docs in project spaces | `notion-search` by last-edited |

Passive sources are noisier than the Slack channel. Treat a passive hit as a *weaker* pointer: it still
needs the same evidence retrieval in stage 2, and it does not get a scoring bonus for being automatic.

**Confidentiality filter, applied at ingest.** Passive sources contain things that must never become
posts. Drop, without recording: customer and prospect names, anything said under NDA, pricing and
contract terms, unannounced roadmap, individual performance discussion, and any patient-related or
clinical data. When a genuinely interesting finding is entangled with a customer's identity, keep the
finding and strip the identity — "a large oncology network", never the name. If it cannot be
de-identified, drop it.

## Notion queue schema

Database: **Content Queue**

| Property | Type | Notes |
|---|---|---|
| `Fragment` | Title | The raw text, verbatim. Never cleaned up. |
| `Captured` | Date | When it hit the inbox |
| `Source` | Select | `slack` / `granola` / `git` / `notion` / `manual` |
| `Source link` | URL | Slack permalink, commit URL, meeting link |
| `Class` | Select | `POINTER` / `OPINION` / `QUESTION` / `NOISE` |
| `Status` | Select | `New` → `Sourced` → `Draft` → `Approved` → `Posted`. Plus `Archived`. |
| `Evidence` | Rich text | What was retrieved, with paths/numbers/dates. Stage 2 output. |
| `Provenance` | Rich text | Where each piece of evidence came from, so a reviewer can re-check it |
| `Score` | Rich text | `evidence/non-obviousness/standing`, e.g. `5/4/5` |
| `Draft` | Rich text | The post text. Stage 3 output. |
| `Labels` | Rich text | Epistemic labels per claim. Reviewer-facing, stripped before publishing. |
| `Blocked on` | Rich text | Why this did not clear the bar, if it did not |
| `Permalink` | URL | Set after publishing |
| `Posted` | Date | Set after publishing |

### Status transitions

- Claude may move rows: `New → Sourced`, `Sourced → Draft`, `Sourced → New` (with `Blocked on` filled),
  anything `→ Archived`, and `Approved → Posted` after a successful API call.
- **Only the human moves `Draft → Approved`.** This is the single gate. There is no automation, no
  timeout, and no inferred approval that crosses it.

### Rows never expire

A fragment from two months ago is still good material. Do not archive for age. The queue is an asset;
a thin week draws on it.

## Dedup

Before inserting, check the last 90 days of rows for the same underlying finding — not the same wording.
`"cms 403s from india"` and `"part D data comes back empty, akamai?"` are one fragment. Merge into the
existing row: append to `Fragment`, add the new `Source link`. Do not create a second row, and do not
post the same finding twice.
