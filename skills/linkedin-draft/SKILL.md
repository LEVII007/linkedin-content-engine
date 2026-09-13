---
name: linkedin-draft
description: Turns one saved thought from Supreet's private inbox into a sourced LinkedIn draft in his observed voice. Use only when explicitly invoked to draft the next idea or a named idea. Never publishes.
disable-model-invocation: true
---

# Draft one post

Workspace:

- profile: `~/.linkedin-content/profile.md`
- ideas: `~/.linkedin-content/inbox/*.md`
- drafts: `~/.linkedin-content/drafts/*.md`

## Steps

1. If the workspace or profile is missing, tell Supreet to run `/linkedin-profile setup`.
2. Select the named idea, or the oldest idea with `status: new`. Never invent a topic when the inbox
   is empty.
3. Read the whole idea, its added context, and the profile.
4. Classify the material:
   - `PERSONAL`: founder moment, changed belief, decision, first-hand observation
   - `PONDERING`: Supreet's own outside-in idea that maps honestly to enterprise AI/pharma
   - `MILESTONE`: real company/product/team/event news
   - `MICRO`: one short specific take
5. Check substance before writing:
   - What exactly happened or what does Supreet believe?
   - Why can he specifically say it?
   - Which details are public?
   - What is still missing?
6. If one important detail is missing, ask one short question. Append his answer verbatim under
   `# Added context`, then continue. If the material remains shallow, stop and leave it `new`.
7. Draft one idea only. Use an observed structure that the material genuinely supports:
   - setup → reversal
   - outside idea explained correctly → enterprise/pharma implication
   - concrete scene → claim
   - two-column judgment
   - 2–4 line micro post
8. Never manufacture the structure. No invented scene, analogy, quote, number, customer, or feeling.
9. Match his observed surface habits: deliberate emoji, short emphasis fragments, and 4–6 relevant
   hashtags. Do not add these if they make the post less natural.
10. Write the final post to a temporary file and execute:

```bash
python <this-skill-directory>/scripts/validate_draft.py <temporary-file>
```

Fix blockers. Warnings require judgment; they are not automatic failures.
11. Save:

```markdown
---
idea: <idea-id>
status: draft
created: <ISO timestamp>
---

<plain LinkedIn post text>
```

12. Change the source idea to `status: drafted`.
13. Show the entire draft and ask what he wants changed. Do not publish. Tell him:
   `Run /linkedin-publish when the final text is ready.`

## Quality bar

Prefer `PERSONAL` and `PONDERING` when several ideas are equally strong. Do not turn internal
engineering details into a CEO post unless Supreet supplied the buyer impact or changed belief.

No evidence, no post. An honest opinion is evidence of what Supreet believes, but never present it as
a measured industry result.
