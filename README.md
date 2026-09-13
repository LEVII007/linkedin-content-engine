# Supreet's LinkedIn Claude Skills

A private set of Claude skills for capturing Supreet's thoughts, maintaining his context, drafting
in his real voice, reviewing, and optionally publishing through LinkedIn's official API.

This is not a hosted app. Nothing runs in the background. Supreet runs a skill whenever he wants.

## Install

```bash
git clone https://github.com/LEVII007/supreet-linkedin-content-engine.git
cd supreet-linkedin-content-engine
chmod +x install.sh
./install.sh
```

Restart Claude Code after installation.

## The normal command

```text
/linkedin-today
```

Flow:

```text
saved thought → one useful follow-up → draft → Supreet edits or approves → optional publish
```

If there is nothing worth posting, the skill says so. It never fills a calendar slot.

## Scratch pad

Supreet can save a thought at any time:

```text
/linkedin-capture enterprise AI adoption feels like latent heat
```

Claude stores the exact words under `~/.linkedin-content/inbox/`. It does not rewrite them.

He can also use the main command:

```text
/linkedin-content capture enterprise teams are measuring the temperature while the ice is melting
```

## Add information about himself

```text
/linkedin-profile I changed my mind about dashboards after seeing...
```

This adds facts, first-hand stories, opinions, current priorities, and voice corrections to his
private profile at `~/.linkedin-content/profile.md`.

Private context is labelled and cannot be copied into a public post without later confirmation.

## Skills

| Command | Purpose |
|---|---|
| `/linkedin-today` | Complete one short content session |
| `/linkedin-capture` | Save a raw thought without rewriting it |
| `/linkedin-profile` | Add or correct information about Supreet |
| `/linkedin-draft` | Draft one saved idea; never publishes |
| `/linkedin-publish` | Display final text and publish only after explicit approval |
| `/linkedin-content` | Main router for all commands |

## Voice

The starting profile comes from 18 of Supreet's own LinkedIn posts and his comment replies.

It captures:

- his audience and career context
- setup → reversal, scene → claim, and Weekend Pondering structures
- deliberate emoji, short emphasis fragments, and hashtags
- public claims that require freshness checks before reuse
- topics and behaviours he avoids

His own profile can evolve through `/linkedin-profile`. Raw notes remain verbatim.

## Publishing setup

Drafting works without LinkedIn access. Publishing is optional.

Run:

```text
/linkedin-publish setup
```

Supreet creates a LinkedIn developer app with **Sign In with LinkedIn using OpenID Connect** and
**Share on LinkedIn**. The token is stored in his macOS keychain.

Before every publish, Claude shows the complete final text and asks for explicit approval of that
exact version. There is no unattended publishing.

## Boundaries

- No fixed posting calendar
- No invented topics or personal stories
- No feed scraping or logged-in browser automation
- No auto-comments, likes, replies, or DMs
- No classifier evasion
- No patient data, credentials, NDA details, or private customer information

## Update

```bash
cd supreet-linkedin-content-engine
git pull
```

The installer uses symlinks, so a pull updates the installed skills immediately.

## Uninstall

```bash
./install.sh --uninstall
```
