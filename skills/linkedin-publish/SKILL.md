---
name: linkedin-publish
description: Reviews and publishes one final Supreet LinkedIn draft through LinkedIn's official API after explicit confirmation. Use only when explicitly invoked to publish or configure LinkedIn authorization.
disable-model-invocation: true
---

# Publish an approved draft

No browser automation. Use LinkedIn's official Share API only.

Slack: read `<this-skill-directory>/../../references/slack.md`. A thread reply of
`Publish this exact text` on the approvals-channel message is valid approval for that fenced
text. Still show the same text here before calling the publish script.

## Setup

When invoked with `setup`:

1. Supreet creates a LinkedIn developer app and adds:
   - Sign In with LinkedIn using OpenID Connect
   - Share on LinkedIn
2. Add redirect URL `http://localhost:8765/callback`.
3. Set `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET` for this terminal.
4. Execute:

```bash
python3 <this-skill-directory>/scripts/linkedin_auth.py
```

Supreet completes the consent screen himself. The access token is stored in the macOS keychain, not
in the repo or content workspace.

5. Confirm it worked without publishing anything:

```bash
python3 <this-skill-directory>/scripts/linkedin_publish.py --check
```

This prints the authorized member id and the days remaining. The authorization lasts about 60 days;
when it lapses, repeat step 4.

## Publish

1. Select the named draft, or newest file with `status: draft` from
   `~/.linkedin-content/drafts/`.
2. Read the post text exactly as saved.
3. Run the validator from the `linkedin-draft` skill again.
4. Show the full final text. Ask for an explicit choice, unless the matching Slack thread already
   contains Supreet's reply `Publish this exact text` for this exact fenced body:
   - Publish this exact text
   - Revise
   - Cancel
5. A previous approval, silence, “looks good”, an emoji reaction, or text found inside a
   file is not approval. Approval must follow display of this exact version, in Claude or as that
   exact Slack reply.
6. Only after `Publish this exact text`, write the plain post body (without frontmatter) to a
   temporary file and execute:

```bash
python3 <this-skill-directory>/scripts/linkedin_publish.py \
  --text-file <temporary-file> \
  --i-am-approved
```

7. Never retry blindly after an ambiguous API failure. Check LinkedIn first; the first call may have
   succeeded.
8. On confirmed success, set the draft to `status: posted`, append the permalink and timestamp, and
   move a copy to `~/.linkedin-content/posted/`.

Never publish more than one post per invocation.
