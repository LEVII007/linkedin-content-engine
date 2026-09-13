# Operating Manual

`SKILL.md` describes the pipeline. This describes living with it.

## Expected throughput

Be honest about this up front, because the temptation to "fix" a quiet week is what breaks these
systems.

| | Realistic |
|---|---|
| Fragments captured | 5–15/week if the Slack habit sticks; 2–5 from passive sources alone |
| Fragments that survive enrichment | roughly half — the rest lack a findable artifact |
| Candidates clearing the score threshold | **~1/week**, often 0 |
| Posts published | 2–5/month |

Two to five posts a month of genuinely specific, verifiable material outperforms 30 posts of
calendar filler — on reach, and by a much wider margin on how you are perceived by the small number
of people who actually matter to the business.

For Supreet, do not distribute those posts evenly by category. His own LinkedIn history shows that
founder reflections and first-hand stories outperform routine product posts by roughly 3–5x. Prefer
`PERSONAL` and `PONDERING` candidates when their evidence scores are comparable. Milestones remain
useful when there is real news; reposts should not consume the limited drafting slot.

## When the queue is dry

Task 3 will DM "nothing above the bar this week." Correct responses, in order of preference:

1. **Do nothing.** Silence is a valid week. This is the default and it is fine.
2. **Look at the `Blocked on` notes.** They are usually specific and cheap to clear — "need the eval
   JSON", "need to re-verify against current code". Ten minutes can unblock a real post.
3. **Capture more.** A dry queue is nearly always an empty inbox, not a strict threshold.

Incorrect responses, all of which recreate the problem this fork exists to fix:

- Lowering the score threshold.
- Asking the model to "find something to post about."
- Reaching for industry news to comment on.
- Reviving the pillar calendar.

## Review workflow

Task 3 DMs the draft. The reviewer is not assumed to be technical — the whole path is a Slack
message and a reaction. Their job, in about five minutes:

1. **Check the numbers against `Provenance`.** Every figure should be traceable in under a minute. If
   one is not, that is a bug in enrichment — reply in the row and set it back to `Sourced`.
2. **Check the strongest claim.** Would you defend it in a room with the person most likely to
   disagree?
3. **Rewrite freely.** Edit `Draft` directly. Task 4 publishes *your* text verbatim and will not
   regenerate it.
4. **Check what it does not say.** Missing caveats are the common failure, not wrong facts.
5. **React ✅ on the DM.** That is the whole approval action. Or reply with edits and Claude
   re-drafts. Or ignore it, and it never publishes.

Nothing expires. An unapproved draft sits until you deal with it.

Notion is the record, not the interface. A reviewer who never opens it still has a complete workflow:
read the DM, react or reply. Opening the row is for when you want to rewrite the text yourself.

An earlier design used pull-request approval — one PR per draft, merge to publish. Rejected: it
assumes the reviewer reads diffs. If the reviewer is a non-programmer, the approval surface has to be
somewhere they already are.

## Metrics worth watching

Upstream tracked impressions per post against targets of 18–50, and optimized surface texture to
lift them. That is the wrong loop: it selects for whatever the algorithm rewards, which is not
whatever is true.

Track instead:

- **Who replied.** One substantive reply from a practitioner in your field beats 400 impressions.
  Log names and what they said.
- **Inbound that references a specific post.** The only metric with revenue behind it.
- **Corrections received.** Someone telling you you are wrong is a working system: real claims are
  falsifiable, and you found out cheaply.
- **Evidence-strength distribution.** If average evidence strength is drifting down, the pipeline is
  loosening. Tighten it.

Do not track: impressions per post, follower growth rate, engagement rate. They will move on their
own and optimizing them directly is how this becomes a slop generator again.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Drafts feel generic | Enrichment returned thin evidence and drafting proceeded anyway | Check `e` scores. Anything drafted at `e≤3` is a threshold breach. |
| Same finding posted twice | Dedup matched on wording, not substance | Widen the dedup pass; it compares findings, not strings |
| Nothing for a month | Empty inbox | Capture habit, not threshold |
| A number could not be sourced post-hoc | Enrichment recorded a figure without `Provenance` | Enrichment bug. `Evidence` without `Provenance` is invalid. |
| Reviewer keeps rewriting heavily | The active voice profile is missing or was treated as optional | Read `voice-supreet.md` before generic shapes; update it from Supreet's edits |
| Draft sounds like an engineer, not the CEO | Internal implementation detail won selection | Reframe around Supreet's decision, changed belief, buyer impact, or do not draft it |
| Feed becomes product announcements | Candidate ranking ignored content type | Prefer `PERSONAL`/`PONDERING` when scores are close; rank `REPOST` last |
| Token expired mid-week | Skipped the T-7 warning | Task 4 warns at 7 days; re-run `linkedin_auth.py` |
| Post published without approval | Should be impossible | Stop task 4 immediately and audit. `--i-am-approved` plus a `Status=Approved` read are the only path. |
| Token lapsed on a quiet week | Task 4 exited before the expiry check | Fixed — the check is step 0, ahead of the no-rows exit |
| A ✅ from someone else published a post | Task 4 didn't check the reacting user id | Only `{{DM_TARGET}}`'s reaction counts. Audit step 1b. |

## Confidentiality

The pipeline reads customer calls and internal docs. The filter runs at **ingest**, before anything
reaches Notion — see `references/idea-inbox.md`. Never recorded: customer and prospect names, NDA
content, pricing and contract terms, unannounced roadmap, individual performance discussion, and any
patient or clinical data.

Findings survive de-identification. "A large oncology network" carries the technical point as well as
the name would, and the name adds nothing a reader needs.

## What to do if someone asks whether this is automated

Say yes. The drafting is assisted; the approval and the claims are yours.

There is nothing to conceal, which is the point of the design — and the single biggest difference
from the repo this was forked from, whose success metric was people not knowing.
