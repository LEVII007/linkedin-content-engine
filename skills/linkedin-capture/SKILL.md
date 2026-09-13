---
name: linkedin-capture
description: Captures Supreet's raw LinkedIn post thoughts into his private local inbox without rewriting them. Use only when explicitly invoked to save an idea, observation, story, link, voice-note transcript, or rough thought for later.
disable-model-invocation: true
---

# Capture a thought

Supreet's private scratch pad is `~/.linkedin-content/inbox/`.

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
captured: <ISO timestamp>
source: claude
---

# Raw thought

<verbatim text>

# Added context
```

6. Reply with one line: `Saved. Add more with /linkedin-capture anytime.`

If Supreet gives a link, preserve both the link and his words about why it matters. A bare link is
not enough; ask what caught his attention.
