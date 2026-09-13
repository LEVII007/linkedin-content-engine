---
name: linkedin-content
description: |
  Operate Supreet's private Slack-first LinkedIn content engine. Use when setting up, testing,
  diagnosing, or manually running the orchestration; reviewing an internal GitHub content issue;
  renewing LinkedIn OAuth; or updating Supreet's observed voice profile.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: "[setup | check | run | renew-linkedin | update-voice]"
version: 2.0.0
license: MIT
---

# Supreet LinkedIn Content Engine

The executable system is under `src/content_engine`. GitHub Actions runs it every 30 minutes.
Supreet's only interface is one private Slack channel.

## Product rule

No thought from Supreet, no post. No explicit ✅ from Supreet, no publish.

Never add feed scraping, browser-driven LinkedIn actions, auto-comments, auto-likes, auto-DMs, or
detection evasion.

## Commands

### `setup`

Follow `README.md` in order:

1. Private Slack channel with Supreet and the app only.
2. Slack app from `slack-app-manifest.yml`.
3. GitHub secrets and variables via `scripts/configure_github.sh`.
4. LinkedIn OAuth via `scripts/linkedin_auth_github.py`.
5. Run the workflow manually with `PUBLISH_ENABLED=false`.
6. Enable publishing only after the Slack draft loop is verified.

Never ask Supreet to use GitHub Issues. They are internal state.

### `check`

Run:

```bash
python -m unittest discover -s tests -v
git diff --check
gh run list --workflow orchestrate.yml --limit 5
```

Report facts separately:

- drafting loop works
- Slack approval works
- publishing remains disabled/enabled
- a real LinkedIn publish is tested/untested

### `run`

Trigger the workflow:

```bash
gh workflow run orchestrate.yml
```

Do not enable publishing as part of a test.

### `renew-linkedin`

LinkedIn tokens normally last about 60 days. Supreet must complete the consent screen himself:

```bash
python scripts/linkedin_auth_github.py --repo OWNER/REPO
```

The token must never be printed, committed, pasted into Slack, or exposed in workflow logs.

### `update-voice`

Read new posts or Supreet's edits. Update `references/voice-supreet.md` only from repeated,
observable patterns. One unusual post is not a new voice rule.

His profile wins over `references/post-shapes.md`. The drafting model must not use the profile's
public claim index as permission to insert facts absent from the current thought or thread.

## State machine

Private GitHub Issues hold state:

`new → needs_context → review → approved → publishing → posted`

Alternative terminal states: `skipped`, `failed`.

Only Supreet's Slack user ID is accepted for:

- top-level scratch-pad ideas
- context and edit replies
- approval reactions

Mark `publishing` before the LinkedIn request. If a run dies after that point, do not retry
automatically; inspect LinkedIn first to avoid a duplicate.
