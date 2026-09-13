---
name: linkedin-draft
description: Turns one saved thought from Supreet's private inbox into a sourced LinkedIn draft in his observed voice. Use only when explicitly invoked for the next or a named idea. Never publishes.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch
---

# Draft one post

Workspace:

- profile: `~/.linkedin-content/profile.md`
- ideas: `~/.linkedin-content/inbox/*.md`
- drafts: `~/.linkedin-content/drafts/*.md`
- posted: `~/.linkedin-content/posted/*.md`

## Steps

1. If the workspace or profile is missing, tell Supreet to run `/linkedin-profile setup`.
2. Read these before selecting a structure:
   - `examples.md` in this skill directory for five real posts and their observed structures
   - `~/.linkedin-content/profile.md` for Supreet's voice, private notes, and public claim index
   - `<this-skill-directory>/../../references/epistemic-gate.md` for per-claim labels and evidence
     rules
   - `<this-skill-directory>/../../references/idea-inbox.md` for confidentiality and blocked-item
     rules
   The profile wins over generic rules. Its register-specific examples and rules control surface
   habits.
3. Select the named idea only if it has `status: new`, or select the oldest new idea. Skip `blocked`,
   `drafted`, and all other statuses. Never invent a topic when the inbox is empty.
4. Read the whole idea and its added context.
5. Identify what happened or what Supreet believes, why he can say it, which details are public, and
   what is missing.
   Apply the confidentiality filter now. Record every failure, but do not draft or take the no-draft
   path yet. An internal number needs a named dashboard, query, or other artifact and date range. A
   per-customer operational metric also needs that customer's clearance, even when unnamed.
   “One customer” is not de-identification when the public customer set is narrow. Never invent a
   descriptor to make a customer publishable. These failures block unconditionally.
6. Research and check prior posts before classification:
   - first-hand personal story: zero or one search, only for a factual claim that needs checking
   - outside-in pondering: two to four searches, enough to verify the outside idea and commonness
   - milestone: one to three searches, focused on the announcement and any stated fact
   Even when step 5 found a blocker, investigate every remaining externally checkable claim. Do not
   draft. Check `~/.linkedin-content/posted/` for the same underlying point. Research never upgrades
   a thin idea. See [Research rules](#research-rules).
7. Classify on two separate axes after research:
   - source type: `PERSONAL` for first-hand moments, decisions, or changed beliefs; `PONDERING` for
     an outside-in idea; `MILESTONE` for real company, product, team, or event news
   - register: `MICRO` for one short, self-contained take; `ESSAY` only when the supplied material
     supports a developed argument
   A note can be `PONDERING + MICRO`. Research volume never changes the register.
8. Apply this decision table after investigation. Keep the blocking triggers in steps 5, 6, and 10.

   | Finding | Action |
   |---|---|
   | Confidentiality failure, unevidenced internal number, or missing customer clearance | Block. |
   | External contradiction in a side detail | Cut the whole false claim. Report it and the evidence above the draft. Never soften, hedge, or silently rewrite it. |
   | External contradiction in the load-bearing point | Block because removing it leaves no post. |
   | Already commonplace or overlaps a prior post | Block. |
   | Missing context | Ask at most one short question. |

   The load-bearing point supplies the main conclusion or reason to post. A side detail can be
   removed while preserving Supreet's supplied opinion, observation, or argument. Cut-and-report
   applies only to externally checkable facts. Report blockers and contradictions without limit;
   the one-question limit applies only to context. Append an answer verbatim under `# Added context`
   and repeat steps 5–7. If it could change classification, wait for it. If the material remains
   shallow, use the no-draft path.
9. Draft one idea using a supported structure:
   - setup → reversal requires `PERSONAL` material for the reversed belief or advice
   - outside idea explained correctly → implication is normally `PONDERING + ESSAY`
   - concrete scene → claim requires a first-hand `PERSONAL` scene
   - two-column judgment requires a judgment Supreet supplied
   - a 2–4 line micro post fits any source type when complete without build-up
   Milestones may state the news directly. Never manufacture a structure, scene, analogy, quote,
   number, customer, or feeling.
10. Do not reuse sentences, openings, or analogies from examples or research. Profile discourse
    markers may recur, but never copy the clause after one. Match the chosen register: essays usually
    use deliberate emoji and 4–6 relevant hashtags; micro posts often use neither. In working notes,
    label every claim `[MEASURED]`,
    `[OBSERVED]`, `[INFERRED]`, or `[OPINION]` and run all seven checks in the epistemic gate. Check
   claims of absence as carefully as positive claims. A claim that cannot carry a label gets cut,
   not hedged. If a required cut removes the load-bearing point, take the no-draft path.
11. Write the post text only, without frontmatter, to a temporary file and execute:

```bash
python3 <this-skill-directory>/scripts/validate_draft.py <temporary-file>
```

Fix blockers. Warnings require judgment. A pass means only that this PII, secrets,
confidentiality-marker, and formatting scanner found no blocker. It cannot detect invention,
borrowed claims, thin material, unsupported numbers, or missing customer clearance.

12. Save:

```markdown
---
idea: <idea-id>
status: draft
created: <ISO timestamp>
sources:
  - <url> — <what it supports>
rejected_research:
  - <url or check> — <what it contradicted or failed to confirm>
claim_labels:
  - <claim> — <label and provenance>
---

<plain LinkedIn post text>
```

13. Change the source idea to `status: drafted`.
14. End on exactly one path:
    - **Draft:** If research contradicted a side detail, first show `Contradictions and cuts`, naming
      the exact claim removed, why it is false, and the source link. Then show the entire draft.
      Below it, list sourced facts with links and anything research rejected or failed to confirm.
      Ask what he wants changed. Do not publish. Tell him:
      `Run /linkedin-publish when the final text is ready.`
    - **No draft:** Change the idea to `status: blocked` and set `blocked_on: "<specific evidence,
      confidentiality, contradiction, commonness, overlap, or context needed>". Include every
      blocker and contradiction found during investigation. Then report:

      ```text
      No draft.
      Blocked on: <specific reason>
      To unblock: <one concrete action per resolvable blocker, or "archive this idea">
      ```

## Research rules

Research supports Supreet's idea. It never supplies one.

Use it for five things:

- **Fact-check what he wrote.** Check numbers, dates, names, regulations, and recalled details.
- **Fill a gap he left open.** Find the figure, mechanism name, or year he gestured at.
- **Explain a borrowed idea correctly.** For a `PONDERING` post the outside concept must be accurate,
  because he explains it properly before mapping it.
- **Check whether the point is already commonplace.** If recent posts make the materially same
  point, report it, block the idea, and stop. Supreet can sharpen the angle or archive it.
- **Check whether Supreet already posted it.** Search `~/.linkedin-content/posted/` by underlying
  idea, not exact wording. There is no API read access to his feed, so flag any local overlap to him
  before drafting and stop.

Use public sources only. Supreet's own LinkedIn profile and posts are allowed as first-party
provenance even when LinkedIn requires login. No other gated source and nothing from internal
systems may be used as web research. A fact found online is never written as his own experience,
customer, or result. Do not add statistics for authority. Never reuse wording from a research
source; facts may be sourced, sentences may not.

## Quality bar

Prefer `PERSONAL` and `PONDERING` when several ideas are equally strong. Do not turn internal
engineering details into a CEO post unless Supreet supplied the buyer impact or changed belief.

No evidence, no post. An honest opinion is evidence of what Supreet believes, but never present it as
a measured industry result.
