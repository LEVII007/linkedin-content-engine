---
name: linkedin-profile
description: Builds and updates Supreet's private content profile from facts, experiences, opinions, audiences, products, and writing preferences he supplies. Use only when explicitly invoked to add information, correct the profile, or inspect what the writing skills know about him.
disable-model-invocation: true
---

# Update Supreet's profile

The private profile is `~/.linkedin-content/profile.md`. Its single bundled source is
`<this-skill-directory>/../../references/voice-supreet.md`, the full observed profile built from
Supreet's real posts.

## Commands

### Setup

When invoked with `setup`:

1. Create `~/.linkedin-content/`, `inbox/`, `drafts/`, and `posted/`.
2. If `profile.md` does not exist, copy
   `<this-skill-directory>/../../references/voice-supreet.md` there and add
   `## Notes supplied by Supreet`.
3. Never overwrite an existing profile.
4. Report the created paths.

### Add information

When Supreet supplies information:

1. Decide whether it is:
   - public fact
   - private context
   - first-hand story
   - opinion or changed belief
   - current priority
   - voice correction
   - “never post” rule
2. Append it verbatim under `## Notes supplied by Supreet`, with date and category.
3. Mark private context explicitly. Private context may shape understanding but must never appear in
   a post unless Supreet later says it is public.
4. Do not turn one preference into a permanent voice rule. Record it as a note until repeated.

### Show

When invoked with `show`, read the profile and summarize:

- who he writes for
- current topics
- strong first-hand stories
- public facts available for drafting
- private information that must not be published

Never print secrets or sensitive raw details in the summary.
