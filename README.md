# LinkedIn Content Engine

Turns real work into LinkedIn posts. A Claude skill.

Drop half-formed thoughts into a Slack channel during the week. The pipeline goes and finds the
actual evidence behind each one — the commit, the eval output, the meeting transcript — scores what
it found, drafts only what clears the bar, and publishes only what you approve, through LinkedIn's
official API.

**No fixed calendar. No engagement bots. No feed scraping. No unattended publishing.**

---

## The one rule

**No evidence, no post.**

Every claim traces to a retrievable artifact. If the evidence cannot be found, the draft is not
written. An empty inbox means zero posts that week, and that is the correct outcome.

## Why it works this way

A content calendar creates seven slots a week and demands they be filled. Nobody has seven real
things to say in a week. The gap between the slots and the substance is where invented content comes
from — and an invented specific in a post about your own work is a fabricated claim about your own
work.

So the queue sets the cadence, not the clock. Expect one post a week, often zero. Two to five a
month of verifiable material beats thirty of filler.

## Pipeline

```
Slack #content-inbox   →  fragments, any length, no format
        ↓ ingest           (+ Granola transcripts, git history)
Notion Content Queue   →  New
        ↓ enrich           retrieve the real artifact behind each pointer
Notion Content Queue   →  Sourced + evidence + provenance
        ↓ draft            score evidence/non-obviousness/standing; draft only what passes
Notion Content Queue   →  Draft
        ↓ validate         secrets / PII / clinical identifiers — blocks before a human sees it
Slack DM to reviewer   →  Draft
        ↓ HUMAN APPROVAL   ← react ✅ to approve, or reply with edits. only the reviewer crosses it.
LinkedIn ugcPosts API  →  Posted
```

Four scheduled tasks: `content-ingest`, `content-enrich`, `content-draft`, `content-publish`. Task 3
is the only one that writes prose, and it is expected to produce nothing on a quiet week.

**The reviewer doesn't need to be technical.** Approval is a Slack reaction on the draft DM — no
Notion, no pull request, no diff. Notion is the record; Slack is the interface.

## Install

```bash
git clone <this repo> ~/Documents/linkedin-content-engine
cd ~/Documents/linkedin-content-engine
chmod +x install.sh && ./install.sh
```

Then in Claude Code:

```
/linkedin-content setup
```

Setup walks through: creating `#content-inbox`, creating the Notion queue, creating the LinkedIn app,
OAuth, selecting the observed voice profile, and installing the tasks. Supreet's profile is already
built from 18 of his own posts and his comment replies.

## Publishing

Official API only.

- **Product:** Share on LinkedIn — self-serve, no review queue
- **Scope:** `w_member_social`
- **Endpoint:** `POST https://api.linkedin.com/v2/ugcPosts`
- **Limit:** 150 requests/member/day

Access tokens last ~60 days and self-serve apps do not get refresh tokens, so re-auth is a manual
30-second browser click-through every couple of months. Task 4 warns 7 days ahead.

## What this deliberately cannot do

**Find posts to comment on.** Reading the LinkedIn feed requires the `r_member_social` scope, which
is closed to new applicants. The only workaround is driving a logged-in browser session, which
violates LinkedIn's User Agreement. Not implemented, and no redesign of the queue changes that.

Substitute: pull candidate discussion topics from sources that do have APIs — RSS, PubMed, news — and
post the comments yourself.

## Layout

| Path | What |
|---|---|
| `SKILL.md` | The skill. Pipeline, stages, setup. |
| `modules/content-engine.md` | Operating manual — throughput, review workflow, failure modes |
| `references/idea-inbox.md` | Capture rules, Notion schema, confidentiality filter |
| `references/substance-retrieval.md` | Where to find evidence and how to record provenance |
| `references/epistemic-gate.md` | Claim labelling, seven checks |
| `references/post-shapes.md` | Five shapes that work, six anti-shapes |
| `references/voice.md` | How to build a voice profile from real samples |
| `references/voice-supreet.md` | Active profile: audience, structures, habits, public claim index, draft checklist |
| `references/publishing-api.md` | Auth, scopes, payloads, token lifetime |
| `references/task-catalog.md` | Full prompts for the four tasks |
| `scripts/validate_draft.py` | Pre-review safety check — secrets, PII, clinical identifiers |
| `scripts/linkedin_auth.py` | OAuth → macOS keychain |
| `scripts/linkedin_publish.py` | Publish one approved post |

## Attribution

Forked from [backpropagation6/claude-linkedin-automation](https://github.com/backpropagation6/claude-linkedin-automation)
by Giovanni Liguori, MIT licensed. The installer, the skill packaging, and the epistemic gate's
structure come from there.

The topic sourcing, evidence retrieval, scoring, approval gate, and API publishing are new. The
anti-detection playbook, the engagement and DM automation, the news scout, and the seven-day pillar
calendar are deleted. `CHANGELOG.md` lists every change and the reason.

MIT.
