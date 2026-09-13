# Idea Inbox

The active scratch pad is one private Slack channel shared only by Supreet and the Slack app.

## What Supreet writes

Anything, with no template:

```text
enterprise AI adoption feels like latent heat
the customer asked why another dashboard would help
McKinsey taught me how to find the answer, founding means owning it
```

A top-level message starts one idea. Replies in its thread add context. Links are useful only when
Supreet adds one sentence explaining why they matter.

## What the app does

Every 30 minutes it:

1. Reads recent top-level channel messages.
2. Accepts only messages authored by `SLACK_APPROVER_USER_ID`.
3. Creates one private GitHub Issue per new Slack timestamp.
4. Uses thread replies as supporting context.
5. Asks one short follow-up question in the original thread when the thought is too thin.
6. Posts a draft as a new top-level Slack message.
7. Treats replies to that draft as edit requests.
8. Treats Supreet's ✅ reaction as approval.

Bot messages and messages from every other user are ignored by ingestion.

## Internal state

GitHub Issues are the durable queue. Supreet never needs to open them.

| Status | Meaning |
|---|---|
| `content:new` | Captured, not drafted |
| `content:needs-context` | One follow-up question is waiting in Slack |
| `content:review` | Draft is visible in Slack |
| `content:approved` | Supreet reacted ✅ |
| `content:publishing` | LinkedIn request is in flight or needs manual inspection |
| `content:posted` | Published and permalink stored |
| `content:skipped` | Not suitable for a post |
| `content:failed` | Safety, API, or ambiguous publishing failure |

The issue body stores machine-readable metadata between HTML comment markers. Do not edit it by
hand. The Slack message remains the source of truth for Supreet's words and approval.

## Confidentiality

Supreet should avoid putting patient data, credentials, NDA material, pricing, contract terms,
unannounced roadmap, or identifiable customer details in the channel.

The engine also scans drafts before review and again before publish. Detection is a safety net, not
permission to put sensitive data in Slack or GitHub.

## Deduplication

The active implementation deduplicates by exact Slack message timestamp. It does not yet merge two
different messages that express the same underlying idea. If duplicate ideas reach review, Supreet
can ignore one; add semantic dedup only after real usage shows it is needed.
