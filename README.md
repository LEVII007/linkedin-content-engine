# Supreet's LinkedIn Content Engine

A private, Slack-first system that turns Supreet's raw thoughts into LinkedIn drafts in his observed
voice. He reviews in Slack. Nothing publishes without his ✅ reaction.

## What Supreet does

Use one private Slack channel shared only with the app.

1. Drop a thought in any form: `enterprise AI adoption feels like latent heat`.
2. Add context as thread replies if useful.
3. The app either asks one concrete follow-up question or posts a draft.
4. Reply to the draft with edits, or react ✅.
5. An approved draft publishes through LinkedIn's official API on the next run.

No Notion, GitHub, Python, or Claude interface is visible to him.

## Orchestration

```
private Slack channel
  ├─ Supreet's top-level messages → new ideas
  ├─ thread replies → context or edit instructions
  └─ ✅ by Supreet only → explicit approval
              ↓ every 30 minutes
GitHub Actions
  ├─ private GitHub Issues → durable internal state
  ├─ Anthropic API → draft or ask for missing context
  ├─ safety checks → PII, secrets, clinical identifiers
  └─ LinkedIn Share API → publish one approved post
```

GitHub Issues are an internal database. Each idea has exactly one status label:
`content:new`, `content:needs-context`, `content:review`, `content:approved`,
`content:publishing`, `content:posted`, `content:skipped`, or `content:failed`.

The `content:publishing` state prevents blind retries. If a process dies after LinkedIn accepts a
post, the next run stops instead of risking a duplicate.

## Safety boundaries

- Only messages written by `SLACK_APPROVER_USER_ID` become ideas.
- Only that same person's ✅ can approve.
- ✅ and ❌ together do not approve.
- A final safety scan runs immediately before publishing.
- `PUBLISH_ENABLED` defaults to `false`.
- One approved post is published per run.
- No feed scraping, auto-comments, auto-likes, DMs, or detection evasion.
- A factual detail must come from Supreet's thought/thread. The voice profile is not permission to
  insert old company claims.

## Setup

### 1. Create the private Slack scratch pad

Create a private channel such as `supreet-content-inbox`. Initially add only Supreet and the app.

Create a Slack app from `slack-app-manifest.yml`, install it, and invite it to that private channel.
Copy:

- Bot token (`xoxb-...`)
- Channel ID
- Supreet's Slack user ID

The app only needs `chat:write`, `groups:history`, and `reactions:read`.

### 2. Configure GitHub Actions

```bash
chmod +x scripts/configure_github.sh
./scripts/configure_github.sh OWNER/REPO CHANNEL_ID SUPREET_USER_ID
```

The script securely prompts for the Slack bot token and Anthropic API key. It stores:

**Secrets:** `SLACK_BOT_TOKEN`, `ANTHROPIC_API_KEY`

**Variables:** `SLACK_CHANNEL_ID`, `SLACK_APPROVER_USER_ID`, `ANTHROPIC_MODEL`,
`PUBLISH_ENABLED=false`

### 3. Configure LinkedIn

Create a LinkedIn developer app. Add **Sign In with LinkedIn using OpenID Connect** and
**Share on LinkedIn**. Add `http://localhost:8765/callback` as an OAuth redirect URL.

Then run locally:

```bash
export LINKEDIN_CLIENT_ID="..."
export LINKEDIN_CLIENT_SECRET="..."
python scripts/linkedin_auth_github.py --repo OWNER/REPO
```

Supreet must complete the consent screen himself. The script sends the token directly to the private
repository's Actions secrets and never prints it.

Finally enable publishing:

```bash
gh variable set PUBLISH_ENABLED --repo OWNER/REPO --body true
```

Keep it `false` until a full dry run produces a good Slack draft.

### 4. Run once

Open **Actions → LinkedIn content engine → Run workflow**. After that it runs every 30 minutes.
GitHub schedules can start a few minutes late.

## Local development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

Run `linkedin-engine check-config` to verify environment names without making API calls.

## Voice

`references/voice-supreet.md` was derived from 18 of Supreet's own posts and his comment replies.
It is authoritative over generic shapes. Personal founder stories and original “Weekend Pondering”
ideas rank above routine product announcements when the underlying evidence is equally strong.

## Token renewal

LinkedIn access tokens normally expire in about 60 days. Re-run
`scripts/linkedin_auth_github.py` before expiry. The expiry timestamp is stored as a GitHub variable.
The app sends one Slack warning when seven days or less remain.

## Attribution

Forked from [backpropagation6/claude-linkedin-automation](https://github.com/backpropagation6/claude-linkedin-automation)
by Giovanni Liguori under the MIT license. This version removes browser automation, engagement bots,
and detection evasion, and replaces the prompt-only pipeline with executable orchestration.
