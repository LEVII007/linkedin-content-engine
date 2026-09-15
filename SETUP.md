# Setup

**How to use this file:** open Claude Code in this folder and say:

```text
Read SETUP.md and set this up for me.
```

Claude follows the steps below and asks you for the few things only you can provide.
You can also just read it and do it yourself — it is written for both.

Expect about 20 minutes. Most of that is LinkedIn's developer app, which is step 5 and optional.

---

## What you are setting up

A set of Claude skills that turn your own half-formed thoughts into LinkedIn posts.

```text
you drop a thought in Slack  →  Claude drafts it in your voice  →  you approve the exact words  →  it posts
```

Nothing runs in the background. Nothing posts without you approving that exact text. There is no
scheduler, no calendar, and no auto-commenting.

If you have no thoughts saved, it writes nothing and says so. That is the intended behaviour.

---

## Before you start

| You need | Why | Check |
|---|---|---|
| macOS | The LinkedIn token is stored in the macOS keychain | `uname` prints `Darwin` |
| Claude Code | Runs the skills | `claude --version` |
| Python 3.9+ | Two small scripts | `python3 --version` |
| git | To clone this | `git --version` |
| A Slack workspace | Where you drop ideas and approve drafts | You can post in it |
| A LinkedIn Company Page you administer | LinkedIn requires one to create a developer app, even to post to your personal profile | Step 5 |

**On Linux or Windows:** everything works except publishing. The two scripts in
`skills/linkedin-publish/scripts/` use the macOS `security` command for the keychain and would need
changing. You would copy the final text into LinkedIn by hand.

**No Company Page?** Steps 1–4 still work. You get finished drafts in Slack and paste them in
yourself. Only automatic publishing needs the Page.

---

## Step 1 — Install

```bash
git clone https://github.com/LEVII007/linkedin-content-engine.git
cd linkedin-content-engine
chmod +x install.sh
./install.sh
```

This links the skills into `~/.claude/skills/` and creates your private workspace at
`~/.linkedin-content/`. Your thoughts, drafts, and posts live there — not in this repo, and not in
git.

**Restart Claude Code.** Skills are only picked up at startup.

---

## Step 2 — Run setup

In Claude Code:

```text
/linkedin-setup
```

It walks through everything below and asks one question at a time. The rest of this file explains
what it is doing and what it needs from you, so you can answer without guessing.

---

## Step 3 — Connect Slack

Slack is where you drop ideas and where drafts come back for approval.

This repo contains **no Slack app**. It uses the Slack connector already built into Claude.

1. Open Claude's settings → **Connectors**.
2. Add **Slack** and authorize your workspace.
3. Restart Claude Code.

To confirm, ask Claude: `can you see my Slack?`

**If you skip this:** everything still works, but ideas and drafts stay on your machine only, and
you lose the drop-a-thought-from-your-phone part — which is most of the value.

---

## Step 4 — Create the two channels

Create these in Slack yourself and join both. Claude will not create them for you; a channel is a
permanent change to your workspace.

| Channel | What goes in it |
|---|---|
| `#linkedin-inbox` | Your raw thoughts. Any length. No format. |
| `#linkedin-approvals` | Finished drafts, waiting for your yes. |

Private channels are fine. Different names are fine — tell Claude and it records the real ones.

Then run:

```text
/linkedin-setup slack
```

Claude looks up both channels, records their **IDs** (not names — names can be renamed), asks who
the approver is, records that person's **Slack user ID**, and writes it all to
`~/.linkedin-content/slack.md`.

### Why the approver ID matters

Only that one person can approve a post. The check is on Slack user ID, not display name — so
someone else in the channel typing the approval words does nothing.

Approval is a thread reply on the draft message, with exactly:

```text
Publish this exact text
```

An emoji, a thumbs up, "looks good", or silence is **not** approval. Neither is a reply on an older
draft. The approval applies only to that exact version of that exact post.

---

## Step 5 — Connect LinkedIn *(optional)*

Only needed for automatic publishing. Skip it and you still get finished drafts to copy in.

You must do this yourself — it is your account, and you type your own password. Nobody, Claude
included, should ask you for it.

1. Go to <https://www.linkedin.com/developers/apps> and create an app.
2. Attach it to a Company Page you administer. LinkedIn requires this even for personal posting.
3. On the **Products** tab, add both:
   - Sign In with LinkedIn using OpenID Connect
   - Share on LinkedIn

   Both are self-serve and granted instantly. There is no review or waiting list.
4. On the **Auth** tab, add the redirect URL:

   ```text
   http://localhost:8765/callback
   ```

5. Copy the Client ID and Client Secret. In your terminal:

   ```bash
   export LINKEDIN_CLIENT_ID=your-client-id
   export LINKEDIN_CLIENT_SECRET=your-client-secret
   ```

6. Authorize. A browser opens; approve as yourself:

   ```bash
   python3 ~/.claude/skills/linkedin-publish/scripts/linkedin_auth.py
   ```

7. Confirm, without publishing anything:

   ```bash
   python3 ~/.claude/skills/linkedin-publish/scripts/linkedin_publish.py --check
   ```

   It prints who you are authorized as and how many days are left.

**The authorization lasts about 60 days**, then step 6 must be repeated. LinkedIn does not give
refresh tokens for self-serve apps, so this is unavoidable. It is one browser click.

The token is stored in your macOS keychain. It is never written into this repo or your workspace.

---

## Step 6 — Set your voice

The bundled profile at `references/voice-supreet.md` describes **Supreet's** voice, built from his
real posts. `install.sh` copies it to `~/.linkedin-content/profile.md`.

**If you are not Supreet, replace it.** Otherwise your posts will sound like someone else.

Give Claude 3–5 things you actually wrote — a Slack message explaining something, a document intro,
a reply to a customer. Real writing, not adjectives about your style. "Direct but warm" produces
nothing usable; a paragraph you actually wrote produces a lot.

```text
/linkedin-profile
```

You can add to it at any time — facts about you, stories you can tell, things never to post.

---

## Step 7 — Verify

```text
/linkedin-setup check
```

Every line should pass:

```text
skills installed          ✓
workspace exists          ✓
profile exists            ✓
slack connector           ✓
slack config complete     ✓
channels readable         ✓
approver id set           ✓
validator self-test       ✓
linkedin authorization    ✓
```

Anything failing comes with the one command that fixes it.

---

## Step 8 — Use it

Drop a thought in `#linkedin-inbox` from your phone. Five words is enough:

```text
cms data host blocks india, silently returns empty
```

Then, whenever you feel like it:

```text
/linkedin-today
```

Claude reads your saved thoughts, picks one worth writing, goes and checks the facts behind it,
drafts it in your voice, and posts it to `#linkedin-approvals`. You reply
`Publish this exact text`, or `Revise: ...`, or `Skip`.

Other commands:

| Command | Does |
|---|---|
| `/linkedin-capture <thought>` | Save an idea from inside Claude |
| `/linkedin-draft` | Draft the oldest saved idea |
| `/linkedin-publish` | Publish an approved draft |
| `/linkedin-profile show` | See what the skills know about you |
| `/linkedin-setup check` | Diagnose anything broken |

---

## What it will not do

Worth knowing before you ask for it.

- **It will not find posts to comment on.** Reading your LinkedIn feed needs a permission
  (`r_member_social`) that LinkedIn has closed to new applicants. There is no paid tier that
  unlocks it. The only workaround is driving your logged-in browser, which breaks LinkedIn's User
  Agreement and risks your account. Not built, and not buildable cleanly by anyone.
- **It will not invent topics.** No news scanning, no trending hooks, no content calendar. Every
  post starts from something you said. Web search only verifies and enriches what you already
  claimed.
- **It will not post on a schedule.** Nothing runs in the background.
- **It will not post without you.** Every post needs your explicit approval of that exact text.

Realistic output is a few posts a month, and some weeks none. That is the design, not a fault.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Commands like `/linkedin-today` don't exist | Restart Claude Code. Skills load at startup. |
| `Refusing to replace existing ...` during install | Something is already at that path. Move it, re-run `./install.sh`. |
| Claude says Slack isn't connected | Add Slack in Claude's settings → Connectors, restart. |
| Claude says channels aren't configured | `/linkedin-setup slack` |
| `No LinkedIn authorization` | `/linkedin-setup linkedin` |
| `LinkedIn authorization expired` | Re-run step 5.6. Happens every ~60 days. |
| Drafts sound like someone else | Your profile is still Supreet's. See step 6. |
| "Nothing worth forcing today" | Your inbox is empty or thin. Drop more thoughts in `#linkedin-inbox`. |
| An approval reply did nothing | Check it was a thread reply, exact wording, on the newest draft, from the configured approver. |

---

## Where your data lives

| Path | What | In git? |
|---|---|---|
| `~/.linkedin-content/profile.md` | Your voice and private notes | No |
| `~/.linkedin-content/inbox/` | Raw thoughts | No |
| `~/.linkedin-content/drafts/` | Drafts awaiting approval | No |
| `~/.linkedin-content/posted/` | What went out | No |
| macOS keychain | LinkedIn token | No |

Nothing personal is committed. The repo holds only the skills.

To remove everything: `./install.sh --uninstall`, then delete `~/.linkedin-content/` if you also
want the content gone.
