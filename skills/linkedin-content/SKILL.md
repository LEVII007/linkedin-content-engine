---
name: linkedin-content
description: Routes Supreet's LinkedIn content request to capture, profile, drafting, daily review, or publishing. Use only when explicitly invoked as the main entry point for his installed LinkedIn skill suite.
disable-model-invocation: true
---

# LinkedIn content router

Choose one sibling skill and read its `SKILL.md` before acting:

- No argument, `today`, or a general “help me post” request → `linkedin-today`
- `capture <thought>` or `save this idea` → `linkedin-capture`
- `profile <information>`, `remember this`, or `setup profile` → `linkedin-profile`
- `draft` or `draft <idea-id>` → `linkedin-draft`
- `publish`, `publish <draft-id>`, or `setup publishing` → `linkedin-publish`

If the argument itself looks like a raw idea rather than a command, capture it first, then ask:
`Saved. Want me to draft it now?`

Never publish in the same step as capture. Supreet must see the complete final draft and explicitly
approve that exact version, in Claude or as `Publish this exact text` in the Slack approvals thread.

Ideas live in the Slack inbox channel. Drafts for approval go to the Slack approvals channel.
Read `<this-skill-directory>/../../references/slack.md` and `~/.linkedin-content/slack.md`.
Use the connected Slack plugin.
