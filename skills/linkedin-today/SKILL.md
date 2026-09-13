---
name: linkedin-today
description: Runs Supreet's complete manual LinkedIn session: optionally capture a thought, select one saved idea, gather missing context, draft in his voice, review, and publish only after explicit approval. Use only when explicitly invoked for today's LinkedIn work.
disable-model-invocation: true
---

# Today's LinkedIn session

This is the command Supreet normally runs. Keep the session short.

## Route

The installed sibling skills are:

- `linkedin-capture` — save a raw thought
- `linkedin-profile` — add facts, experiences, preferences, and private context
- `linkedin-draft` — turn one saved thought into a draft
- `linkedin-publish` — show the final text and publish after explicit approval

Read the relevant sibling `SKILL.md` and follow it exactly. Do not improvise a second workflow.

## Daily flow

1. If text follows `/linkedin-today`, capture it first as a raw thought.
2. Check `~/.linkedin-content/profile.md`. If missing, run the profile setup procedure.
3. List inbox ideas by status:
   - If there are new ideas, select the oldest strong one.
   - If there are several equally strong ideas, prefer a personal founder moment or “Weekend
     Pondering” idea over a routine product announcement.
   - If there is no real material, say `Nothing worth forcing today.` and stop.
4. Follow the drafting skill. Ask at most one missing-context question at a time.
5. Show the full draft.
6. Ask what Supreet wants:
   - revise
   - save for later
   - publish
7. For revisions, update the saved draft and show the full new version again.
8. For publish, follow the publishing skill. Approval applies only to the exact displayed version.

## Hard boundaries

- Do not create a topic from news, a fixed calendar, or a generic “pharma trend”.
- Do not publish merely because Supreet invoked this skill.
- Do not automate comments, likes, replies, DMs, or feed browsing.
- Do not ask Supreet to open files. Summarize the inbox and show drafts in chat.
- One post maximum per session.

Target session:

`rough thought → one useful question → draft → edit/approve`

Five minutes is good. No post is also a valid result.
