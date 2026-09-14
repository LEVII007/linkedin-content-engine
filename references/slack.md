# Slack, via the connected plugin

Do not write Slack API code. Use the Slack plugin or MCP already attached to this session
(Claude Slack, Codex Slack, or any equivalent). If Slack is not connected, say so and continue
with local files only.

Channel names live in `~/.linkedin-content/slack.md`. Read that file before any Slack call.
Never read or post to any other channel.

| Role | Default channel |
|---|---|
| Ideas | `#linkedin-inbox` |
| Drafts for approval | `#linkedin-approvals` |

If those channels do not exist, ask Supreet to create them, or to put the real names or channel IDs
in `slack.md`. Do not guess.

## Ideas in `#linkedin-inbox`

That channel is the live idea list. A message from Supreet is a raw thought. Keep the text
verbatim. A thread under that message is added context, not a second idea.

Skip bot posts, join/leave noise, and reactions-only messages. Skip a message already mirrored in
`~/.linkedin-content/inbox/` (match `slack_ts` or permalink).

When `/linkedin-capture` runs in Claude, still write the local inbox file, then post the same
verbatim thought to `#linkedin-inbox` so Slack stays the place he dumps ideas. Include the local
`id` in the Slack message so later runs can match them.

Do not post patient data, credentials, NDA material, pricing, contract details, an unannounced
roadmap, or an identifiable customer to Slack.

## Drafts in `#linkedin-approvals`

After a draft is saved locally, post it to `#linkedin-approvals` as a new message. Show, in order:

1. Any contradictions, cuts, or overlaps (same text the drafting skill shows in chat)
2. The exact LinkedIn post, in a fenced code block, nothing else inside the fence
3. Sourced facts and rejected research, with links
4. The local idea id and draft filename
5. This instruction:

```text
Reply in this thread with exactly one of:
- Publish this exact text
- Revise: <what to change>
- Skip
A reaction, emoji, or “looks good” is not approval.
```

If posting fails, keep the local draft and tell him the Slack step failed.

## Approval

Valid approval is a thread reply on that exact draft message: `Publish this exact text`.
It must come from Supreet. It applies only to the fenced text in that message.

Then follow `linkedin-publish`. Still show the same text in Claude and still require the
`--i-am-approved` publish path. Slack approval does not skip the LinkedIn API gate.

`Revise:` goes back to the drafting skill. `Skip` sets the idea to `blocked` with
`blocked_on: skipped in Slack`.
