---
name: linkedin-setup
description: Sets up and checks the LinkedIn content skills — workspace folders, profile, Slack channels and approver, and LinkedIn publishing authorization. Use only when explicitly invoked to install, configure, reconnect, or diagnose the LinkedIn skill suite.
disable-model-invocation: true
argument-hint: "[check | slack | linkedin | profile]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Set up the LinkedIn skills

Four parts. Each can be run alone. With no argument, run all four in order, then `check`.

| Argument | Does |
|---|---|
| *(none)* | Everything, in order, then `check` |
| `check` | Diagnose only. Changes nothing. |
| `slack` | Find the channels and the approver, write the config |
| `linkedin` | Walk through the developer app and authorize publishing |
| `profile` | Create the private profile |

Never do a part that is already done. Report what you skipped and why.

Ask one question at a time. The person running this may not be a programmer — do not ask them to
edit files, read code, or run commands you could run yourself.

---

## Part 1 — Workspace and profile

1. Create `~/.linkedin-content/`, and `inbox/`, `drafts/`, `posted/` inside it.
2. If `~/.linkedin-content/profile.md` does not exist, copy
   `<this-skill-directory>/../../references/voice-supreet.md` there and append
   `## Notes supplied by Supreet`.
3. **Never overwrite an existing profile.** If one exists, say so and move on.

The bundled profile describes Supreet's observed voice. If someone else is using these skills,
say so plainly: the voice file must be replaced with their own, built from 3–5 things they
actually wrote. Do not silently write posts in the wrong person's voice.

---

## Part 2 — Slack

Read `<this-skill-directory>/../../references/slack.md` first.

1. **Check the connector.** Look for a tool whose name ends in `slack_read_channel`.
   If there is none, stop this part and say:

   > Slack isn't connected to Claude yet. Open Claude's settings, go to Connectors, and add Slack.
   > Then run `/linkedin-setup slack` again. Everything else works without it — ideas just stay
   > on this machine.

2. **Find the channels.** Search for the ideas channel and the approvals channel by name
   (`#linkedin-inbox`, `#linkedin-approvals` unless told otherwise). For each one:
   - Found exactly one → record its **ID**.
   - Found none → say the channel does not exist and ask the person to create it in Slack and
     invite themselves. Do not create it for them; a channel is a persistent workspace change.
   - Found several → show the matches and ask which one. Never guess.

3. **Find the approver.** Ask whose LinkedIn account this posts to. Look that person up and record
   their **Slack user ID**. Confirm the full name back before writing it.

4. **Write the config** to `~/.linkedin-content/slack.md`, using
   `<this-skill-directory>/../../references/slack-channels.md` as the shape. Fill in every field.
   Leave nothing as `TODO`.

5. **Verify.** Read one message from each channel by ID. If either read fails, say which and stop.

Explain the approver field in one sentence: only that person's reply can publish a post, and it is
checked by Slack user ID, so a matching name is not enough.

---

## Part 3 — LinkedIn publishing

This part is optional. Everything up to "here is your draft" works without it — publishing is the
only thing that needs LinkedIn authorization.

The person whose account this posts to must do steps 1–3 themselves. They type their own password;
never ask for it, and never offer to enter it.

1. **Check the Page.** LinkedIn requires a developer app to be attached to a Company Page, even for
   posting to a personal profile. Ask whether they administer one. If not, stop here — the rest
   cannot proceed, and that is worth knowing before spending time on it.
2. **Create the app** at <https://www.linkedin.com/developers/apps>, attached to that Page. On the
   Products tab add both:
   - Sign In with LinkedIn using OpenID Connect
   - Share on LinkedIn

   Both are self-serve and granted immediately. There is no review queue.
3. **Add the redirect URL** `http://localhost:8765/callback` on the Auth tab.
4. Have them paste the Client ID and Client Secret. Set them for the current terminal only:

```bash
export LINKEDIN_CLIENT_ID=...
export LINKEDIN_CLIENT_SECRET=...
```

   Never write these into the repo or into `~/.linkedin-content/`.

5. Run the authorization. A browser opens; they approve as themselves.

```bash
python3 <this-skill-directory>/../linkedin-publish/scripts/linkedin_auth.py
```

6. Confirm it worked:

```bash
python3 <this-skill-directory>/../linkedin-publish/scripts/linkedin_publish.py --check
```

   Success prints the authorized member id and how many days the authorization has left.
   Nothing is published.

Tell them plainly: the token lasts about 60 days, then step 5 must be repeated. It is one browser
click. See `<this-skill-directory>/../../references/publishing-api.md` for scopes and limits.

---

## Part 4 — Check

Read-only. Report a table of pass/fail, then a short list of what to do about each failure.

| Check | How | If it fails |
|---|---|---|
| Skills installed | `ls ~/.claude/skills/linkedin-*` | Re-run `./install.sh` |
| Workspace exists | `~/.linkedin-content/{inbox,drafts,posted}` | Run `/linkedin-setup profile` |
| Profile exists | `~/.linkedin-content/profile.md` is non-empty | Run `/linkedin-setup profile` |
| Profile is the right person's | Its voice matches whoever is posting | Replace it with their own samples |
| Slack connector | A `slack_read_channel` tool exists | Add Slack in Claude's Connectors settings |
| Slack config | `~/.linkedin-content/slack.md` has no `TODO` | Run `/linkedin-setup slack` |
| Channels readable | Read one message from each ID | Re-run `/linkedin-setup slack` |
| Approver ID set | A `U...` id is present | Re-run `/linkedin-setup slack` |
| Validator runs | `validate_draft.py --self-test` passes | Report the failing case; do not draft |
| LinkedIn token | `linkedin_publish.py --check` prints a member id | Run `/linkedin-setup linkedin` |

Never report a check as passing without actually running it.

End with the single next thing to do. If everything passes, that is:

> Ready. Drop a thought in the ideas channel, then run `/linkedin-today`.
