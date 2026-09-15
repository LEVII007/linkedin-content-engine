# Slack config

This file is the template. The live copy is `~/.linkedin-content/slack.md`.

Fill in every `TODO`. Until they are filled, the skills work on local files only and say so.
Run `/linkedin-setup slack` and Claude will look these up and write them for you.

## Channels

Names are for humans. **IDs are what the skills use** — a channel can be renamed, an ID cannot.

| Role | Name | ID |
|---|---|---|
| Ideas | `#linkedin-inbox` | TODO |
| Approvals | `#linkedin-approvals` | TODO |

## Approver

Only this person can approve a post. A reply from anyone else is ignored, even if the words match
exactly.

| Field | Value |
|---|---|
| Name | TODO |
| Slack user ID | TODO |

## Rules

- Never read or post to a channel not listed above.
- A Slack user ID looks like `U01ABCDEFGH`. A channel ID looks like `C01ABCDEFGH`.
- If an ID is missing or still says TODO, treat Slack as not configured.
