---
name: linkedin-capture
description: Captures Supreet's raw LinkedIn post thoughts into his private local inbox without rewriting them. Use only when explicitly invoked to save an idea, observation, story, link, voice-note transcript, or rough thought for later.
disable-model-invocation: true
---

# Capture a thought

Supreet dumps ideas in Slack `#linkedin-inbox` (see `~/.linkedin-content/slack.md`).
Mirror every capture to `~/.linkedin-content/inbox/` so drafting can track status.

Read `<this-skill-directory>/../../references/slack.md` and use the connected Slack plugin.
If Slack is not connected, save locally and say so.

## Steps

1. Use the text after the skill name as the thought. If empty, ask only: “What’s on your mind?”
2. Keep his text verbatim. Do not clean grammar, summarize, add a title, or turn it into a post.
3. If it contains patient data, credentials, NDA material, pricing, contract details, an
   unannounced roadmap, or an identifiable customer, do not save it. Ask him to remove the private
   detail first.
4. Create the inbox directory if needed.
5. Write a new file named `YYYY-MM-DD-HHMMSS-<short-id>.md`. Never overwrite a file.

```markdown
---
id: <short-id>
status: new
blocked_on:
captured: <ISO timestamp>
source: claude
slack_ts:
slack_permalink:
---

# Raw thought

<verbatim text>

# Added context
```

6. Post the same verbatim thought to the inbox Slack channel. Write `slack_ts` and
   `slack_permalink` back into the local file.
7. Reply with one line: `Saved to Slack and local inbox. Add more in #linkedin-inbox anytime.`

If Supreet gives a link, preserve both the link and his words about why it matters. A bare link is
not enough; ask what caught his attention.
