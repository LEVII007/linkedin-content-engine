# Changelog

## 2.1.0 — 2026-09-13 — Worked examples and grounded research

- Added `skills/linkedin-draft/examples.md`: five posts Supreet published, one per observed
  structure, each annotated with why it worked and what to copy. Reusing their sentences or
  analogies is treated as invention.
- Added a research step to drafting for raw or half-remembered notes: fact-check his claims, fill a
  gap he left open, verify a borrowed concept before he maps it, and flag takes that are already
  common.
- Constrained research: the topic always comes from the inbox, external facts are never presented as
  his experience, contradictions are raised before drafting instead of silently corrected, and every
  sourced fact is shown with its link under the draft.
- Removed build artifacts left behind by the reverted hosted app.

## 2.0.0 — 2026-09-13 — Manual Claude skill suite

- Added six installable Claude skills: daily orchestration, capture, profile, draft, publish, and
  command routing.
- Replaced Notion and scheduled tasks with a private local workspace at `~/.linkedin-content/`.
- Added `/linkedin-capture` as Supreet's zero-format scratch pad and `/linkedin-profile` for adding
  his own facts, stories, opinions, priorities, and voice corrections.
- Added deterministic pre-publish checks and official LinkedIn OAuth/publishing scripts inside the
  relevant skills.
- Publishing is manual: Claude displays the exact final text and requires fresh explicit approval.
- Replaced the old installer with a small Claude Code skill-suite installer.

## 1.1.0 — 2026-09-13 — Supreet voice integration

- Added `references/voice-supreet.md`, derived from 18 of Supreet's posts and his comment replies.
- Made the observed profile authoritative over generic post-shape and formatting defaults.
- Added content-type ranking: prefer first-hand founder reflections and original "Weekend
  Pondering" ideas when evidence scores are comparable; rank reposts last.
- Added Supreet's observed structures, audience, surface habits, exclusions, and public claim index
  to the drafting checks. Public claims remain provenance and are re-verified when time-sensitive.
- Updated setup, task prompts, operating guidance, and failure modes to load the profile explicitly.

## 1.0.0 — 2026-09-10 — Synthio fork

Forked from [backpropagation6/claude-linkedin-automation](https://github.com/backpropagation6/claude-linkedin-automation)
v3.1.0 (upstream last updated 2026-04-07). MIT, attribution retained.

The upstream repo is 5,107 lines of markdown with no posting code. It works by having Claude drive a
logged-in Chrome session. This fork keeps the skill packaging and replaces the content layer.

### Removed

| Removed | Why |
|---|---|
| `references/anti-detection-playbook.md` (329 lines) | Its purpose was evading LinkedIn's automation classifier. Every rule governed how output *sounds* — character-count variance, rhetorical rotation, tool-mention caps — and none governed whether it was true. |
| `HUMAN-VOICE-LAYER.md` (302 lines) | "Structural naturalness patterns that betray AI authorship to expert human readers." Its goal was passing as human to people who did not know. |
| Task `linkedin-daily-post` | Published unattended at 08:00 daily from a pre-written weekly file. Replaced by an approval-gated publisher. |
| Task `linkedin-daily-engagement` | 25-minute sessions of 8–10 automated likes and 5–8 automated comments, with per-session caps to stay under detection thresholds. |
| Task `linkedin-reply-to-replies` | Automated replies to real people in real threads. |
| Task `linkedin-dm-prep` | Automated DM triage and drafting. |
| Task `linkedin-news-scout` | Five hardcoded web searches scoring headlines 1–10 as topic supply. Topic invention. |
| Task `linkedin-experiment-audit` | Scored each day's output for detection risk. |
| The 7-day pillar calendar | Fixed slots (Mon behind-the-scenes → Sun soft CTA) demanded seven posts a week from one or two real inputs. The gap was the slop. |
| `references/content-templates.md` | Italian-language templates hardcoded to the original author's profile and booking link. |
| `references/tov-framework.md` | Voice defined as a banned-word list plus a required signature line. |
| `assets/`, `demo.tape`, `PR-DRAFT.md`, `CONTRIBUTING.md`, `examples/` | Upstream marketing and packaging. |

Also gone: the requirement for "1 specific micro-anecdote (day, person, physical object)" per case
study. That rule existed because the generator had no real material, so specificity had to be
manufactured. A manufactured specific about your own work is a fabricated claim about your own work.

### Added

| Added | What |
|---|---|
| `references/idea-inbox.md` | Slack `#content-inbox` as the primary and only topic source. Fragment rules, Notion queue schema, dedup by finding, confidentiality filter at ingest. |
| `references/substance-retrieval.md` | The core addition. A fragment is a pointer; this stage retrieves the artifact behind it. Evidence strength 1–5. Specificity is retrieved, never invented. |
| `references/publishing-api.md` | Official API: Share on LinkedIn, `w_member_social`, `POST /v2/ugcPosts`. Token lifetime and scope boundaries documented. |
| `scripts/linkedin_auth.py` | OAuth to the macOS keychain. No token on disk. |
| `scripts/linkedin_publish.py` | Publishes one post. Refuses without `--i-am-approved`. |
| Scoring threshold | evidence / non-obviousness / standing, each 1–5. All ≥3 and evidence ≥4, or no draft. |
| The zero-post guarantee | If nothing clears the bar, the pipeline sends one Slack line and stops. It is allowed to output nothing. |
| Human approval gate | Only the human sets `Status=Approved`. No timeout, no inferred approval, no automation path across it. Task 4 publishes the human's edited text verbatim. |

### Changed

- `SKILL.md` — rewritten. Queue-driven, four stages, four tasks (was ten).
- `modules/linkedin.md` → `modules/content-engine.md` — operating manual: realistic throughput
  (2–5 posts/month), review workflow, what to do when the queue is dry, failure modes.
- `references/epistemic-verification.md` → `references/epistemic-gate.md` — kept the structure,
  changed the purpose. Upstream ran it to avoid *"expos[ing] the automation"*. Here it runs because
  publishing something false under your own name is bad on its own terms. Moved from a polish pass to
  source time, so it can stop a claim rather than soften it.
- `references/tov-framework.md` → `references/voice.md` — voice built from 3–5 real writing samples
  instead of adjectives and banned words.
- `references/content-templates.md` → `references/post-shapes.md` — five shapes, six anti-shapes,
  English, no hardcoded CTA.
- `install.sh` — skill renamed `linkedin` → `linkedin-content`.
- Metrics — upstream optimized impressions against 18–50/post targets. This tracks who replied,
  inbound referencing a post, and corrections received.

### Not implemented, and won't be

Finding posts to comment on. Reading the feed needs `r_member_social`, closed to new applicants. The
only route is scraping a logged-in session, which violates the User Agreement.

---

## Ported from martinopedal/linkedin-auto-poster

[martinopedal/linkedin-auto-poster](https://github.com/martinopedal/linkedin-auto-poster) (MIT) is a
better-engineered take on the same problem — real Python, tests, official `ugcPosts` API, no browser
automation. Its topic source is RSS feeds and GitHub releases, which is the wrong input here, but two
pieces were worth taking:

- **`scripts/validate_draft.py`** — PII and secret patterns adapted from its `src/drafts/validator.py`,
  retargeted from Norwegian identifiers (fødselsnummer, org number) to this context: medical record
  numbers, provider NPIs, patient identifiers, India and US phone formats, AWS keys, private keys.
  Its 41-phrase banned-vocabulary list was **not** taken — policing words does not fix a shallow topic.
- **Token expiry as a first-class check.** Reading its `token-reminder.yml` surfaced a bug here: task 4
  checked expiry *after* its early exit for "no approved rows", so on any quiet week the warning never
  fired. The check is now step 0.

### Rejected: PR-based approval

Its approval gate is a GitHub PR — one per draft, add an `approve-post` label, merge to publish. Good
design, and better than Notion on audit trail. Not adopted: it assumes the reviewer reads diffs. The
reviewer here is not a programmer, so approval is a ✅ reaction on a Slack DM instead.
