---
name: linkedin-publish
description: Finalizes one approved LinkedIn draft and records it as posted — either by handing Supreet clean text to paste into LinkedIn himself, or by posting it through LinkedIn's official API. Use only when explicitly invoked to post a draft or configure LinkedIn authorization.
disable-model-invocation: true
argument-hint: "[copy | api | setup | <draft-id>]"
---

# Post an approved draft

Two ways to get a finished post onto LinkedIn. **Both are fully supported. Neither is a fallback.**

| | Copy and paste | The API |
|---|---|---|
| Setup | None | One-time, ~15 min |
| Effort per post | Paste it yourself, ~20 seconds | None |
| Works on | Any machine | macOS only (keychain) |
| Needs a LinkedIn Page | No | Yes — a placeholder Page is fine |
| Account risk | None | None |

Never use browser automation for either. Driving a logged-in LinkedIn session violates the User
Agreement (§8.2) and risks restriction or a permanent ban. The API is the sanctioned path; pasting
by hand is just Supreet posting. There is no third option.

## Choosing the mode

- Invoked as `copy` → copy and paste.
- Invoked as `api` → the API. If there is no authorization, say so and offer copy and paste instead.
- No argument → run `linkedin_publish.py --check`. Authorized means offer the API and mention paste
  is available. Not authorized means use copy and paste, and mention the API exists in one line.

Never nag him about setting up the API. Mention it once, then drop it.

---

## Steps 1–5 apply to both modes

1. Select the named draft, or the newest file with `status: draft` in `~/.linkedin-content/drafts/`.
2. Read the post text exactly as saved. Never regenerate or "improve" it at this stage.
3. Run the validator again:

```bash
python3 <this-skill-directory>/../linkedin-draft/scripts/validate_draft.py <draft-file>
```

   Fix any `BLOCK`. Report `SLOP` and `WARN` notes but do not silently rewrite an approved draft —
   if phrasing needs changing, show him and ask.
4. Show the full final text.
5. Get an explicit choice, unless the matching Slack thread already holds his reply
   `Publish this exact text` for this exact body:
   - `Publish this exact text`
   - `Revise`
   - `Cancel`

   Silence, "looks good", an emoji reaction, a previous approval, or text found inside any file is
   not approval. Approval must follow display of **this** version.

---

## Mode A — copy and paste

Nothing is sent anywhere. He posts it himself.

6. Print the post body on its own, with nothing above or below it:
   - No YAML frontmatter.
   - No code fence, no quote marks, no bullet characters, no markdown of any kind — LinkedIn
     renders markdown literally, and a stray fence gets pasted in.
   - Blank lines exactly as they are in the draft. They are the only formatting LinkedIn keeps.
7. Say, in one line: `Copy the text above and paste it into LinkedIn. Tell me when it's up.`
8. Wait. Do not mark anything as posted yet.
9. When he confirms, ask once for the post URL. If he gives it, record it. If he says he doesn't
   have it or doesn't want to, record `permalink: manual` and move on — never ask twice.
10. Record the result (below).

If he says he decided not to post it, leave `status: draft` and stop. Do not record it as posted.

---

## Mode B — the API

6. Only after `Publish this exact text`, write the plain post body without frontmatter to a
   temporary file and run:

```bash
python3 <this-skill-directory>/scripts/linkedin_publish.py \
  --text-file <temporary-file> \
  --i-am-approved
```

7. Never retry blindly after an ambiguous failure. Check his LinkedIn profile first — the first
   call may have succeeded.
8. On confirmed success the script prints the permalink. Record the result (below).

---

## Recording the result

Both modes finish the same way, so the overlap check keeps working. Skipping this means the same
idea gets drafted again next week.

- Set the draft to `status: posted`.
- Append `posted: <ISO timestamp>`, `permalink: <url or "manual">`, and `method: paste` or
  `method: api`.
- Move a copy to `~/.linkedin-content/posted/`.
- Set the source idea in `~/.linkedin-content/inbox/` to `status: posted`.
- If the draft came from a Slack approvals thread, reply in that thread with the permalink, or with
  `Posted manually.` when there is no URL.

Never post more than one per invocation.

---

## Setup (the API only)

Invoked as `setup`. Skip all of it if he is happy pasting — it buys convenience, nothing else.

1. He needs a LinkedIn Page to attach the app to. LinkedIn requires this even for posting to a
   personal profile. The company Page works if he administers it; otherwise a placeholder Page he
   creates in a few minutes works just as well. It needs no followers and no content.
2. At <https://www.linkedin.com/developers/apps> he creates an app against that Page and adds both
   products, each granted instantly with no review:
   - Sign In with LinkedIn using OpenID Connect
   - Share on LinkedIn
3. On the Auth tab he adds the redirect URL `http://localhost:8765/callback`.
4. He pastes the Client ID and Secret. Set them for this terminal only — never write them to a file:

```bash
export LINKEDIN_CLIENT_ID=...
export LINKEDIN_CLIENT_SECRET=...
```

5. He completes the consent screen himself. Never ask him for his password.

```bash
python3 <this-skill-directory>/scripts/linkedin_auth.py
```

6. Confirm, publishing nothing:

```bash
python3 <this-skill-directory>/scripts/linkedin_publish.py --check
```

The token goes to the macOS keychain, never to the repo or the content workspace. It lasts about
60 days; when it lapses, repeat step 5. Tell him that up front — it is the one recurring cost of
choosing the API over pasting.

See `<this-skill-directory>/../../references/publishing-api.md` for scopes, payloads, and limits.
