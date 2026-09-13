---
name: linkedin-draft
description: Turns one saved thought from Supreet's private inbox into a sourced LinkedIn draft in his observed voice, researching the web to check his facts and fill gaps. Use only when explicitly invoked to draft the next idea or a named idea. Never publishes.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch
---

# Draft one post

Workspace:

- profile: `~/.linkedin-content/profile.md`
- ideas: `~/.linkedin-content/inbox/*.md`
- drafts: `~/.linkedin-content/drafts/*.md`

Voice reference, read before writing: `examples.md` in this skill directory — five posts Supreet
actually published, each annotated with what to copy.

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
6. Research the idea on the web. His notes will often be raw, half-finished, or from memory, so this
   step exists to make the post more informed — never to change what it is about. See
   [Research rules](#research-rules).
7. If one important detail is still missing, ask one short question. Append his answer verbatim
   under `# Added context`, then continue. If the material remains shallow, stop and leave it `new`.
8. Draft one idea only. Use an observed structure that the material genuinely supports:
   - setup → reversal
   - outside idea explained correctly → enterprise/pharma implication
   - concrete scene → claim
   - two-column judgment
   - 2–4 line micro post
9. Never manufacture the structure. No invented scene, analogy, quote, number, customer, or feeling.
   Do not reuse sentences, openings, or analogies from `examples.md`.
10. Match his observed surface habits: deliberate emoji, short emphasis fragments, and 4–6 relevant
    hashtags. Do not add these if they make the post less natural.
11. Write the final post to a temporary file and execute:

```bash
python <this-skill-directory>/scripts/validate_draft.py <temporary-file>
```

Fix blockers. Warnings require judgment; they are not automatic failures.

12. Save:

```markdown
---
idea: <idea-id>
status: draft
created: <ISO timestamp>
sources:
  - <url> — <what it supports>
---

<plain LinkedIn post text>
```

13. Change the source idea to `status: drafted`.
14. Show the entire draft. Below it, list every sourced fact with its link, and anything the research
    contradicted or failed to confirm. Then ask what he wants changed. Do not publish. Tell him:
    `Run /linkedin-publish when the final text is ready.`

## Research rules

Research supports Supreet's idea. It never supplies one. If the inbox is empty, there is nothing to
research.

Use it for four things:

- **Fact-check what he wrote.** Numbers, dates, company names, regulatory details, and anything he
  recalled from memory.
- **Fill a gap he left open.** A figure he gestured at, the correct name of a mechanism, the year
  something happened.
- **Explain a borrowed idea correctly.** For a `PONDERING` post the outside concept must be accurate,
  because he explains it properly before mapping it.
- **Check whether the point is already commonplace.** If ten people published the same take last
  month, tell him. He can sharpen the angle or drop it.

Hard limits:

- A fact found online is never written as his own experience, customer, or result.
- If research contradicts something he said, raise it before drafting. Never silently correct him.
- If a claim cannot be verified, either cut it or attribute it to what he actually knows.
- Do not add statistics to make a post sound authoritative. Every number must earn its place.
- Public sources only. Nothing behind a login, and nothing from internal systems.
- Cap it at a few searches. This is verification, not a literature review.

## Quality bar

Prefer `PERSONAL` and `PONDERING` when several ideas are equally strong. Do not turn internal
engineering details into a CEO post unless Supreet supplied the buyer impact or changed belief.

No evidence, no post. An honest opinion is evidence of what Supreet believes, but never present it as
a measured industry result.
