---
name: linkedin-draft
description: Drafts one saved thought from Supreet's private inbox in his observed voice. Invoke only for the next or a named idea. Never publishes.
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
   - `examples.md` here for real posts and structures
   - `~/.linkedin-content/profile.md` for voice, private notes, and public claims
   - `<this-skill-directory>/../../references/epistemic-gate.md` for claim evidence
   - `<this-skill-directory>/../../references/idea-inbox.md` for confidentiality and blocked items
   The profile controls voice, register, and surface habits.
3. Sync new messages from the Slack inbox channel into `~/.linkedin-content/inbox/` using
   `<this-skill-directory>/../../references/slack.md` and the connected Slack plugin. Then select
   the named `status: new` idea, or the oldest new idea. Skip every other status. Never invent a
   topic when the inbox is empty.
4. Read the whole idea and its added context.
5. Identify what happened or what Supreet believes, why he can say it, what is public, and what is
   missing. Apply the confidentiality filter. Record failures, but finish step 6 before blocking.
   An internal number needs a named artifact and date range. A
   per-customer operational metric also needs that customer's clearance, even when unnamed.
   “One customer” is not de-identification when the public customer set is narrow. Never invent a
   descriptor to make a customer publishable. These failures block unconditionally.
6. Research and check prior posts before classification:
   - first-hand personal story: zero or one search, only for a factual claim that needs checking
   - outside-in pondering: two to four searches, enough to verify the outside idea and commonness
   - milestone: one to three searches, focused on the announcement and any stated fact
   Investigate every externally checkable claim even after a blocker. Do not draft. Check
   `~/.linkedin-content/posted/` for the same underlying point. Research never upgrades
   a thin idea. See [Research rules](#research-rules).
7. Classify after research:
   - source type: `PERSONAL` for first-hand moments, decisions, or changed beliefs; `PONDERING` for
     an outside-in idea; `MILESTONE` for real company, product, team, or event news
   - register: `MICRO` for one short, self-contained take; `ESSAY` only when the supplied material
     supports a developed argument
   A note can be `PONDERING + MICRO`. Research never changes the register.
8. Apply table.

   | Finding | Action |
   |---|---|
   | Confidentiality failure, unevidenced internal number, or missing customer clearance | Block. |
   | External contradiction in a side detail | Cut the whole false claim. Report it and the evidence above the draft. Never soften, hedge, or silently rewrite it. |
   | External contradiction in the load-bearing point | Block because removing it leaves no post. |
   | Near-identical to one identifiable outside post under the research test | Block and name the post and URL in `blocked_on`. |
   | Commonplace or other outside overlap | Draft. Report the shared claim and closest links above it. |
   | Overlaps Supreet's prior post | Block. |
   | Missing context | Ask at most one short question. |

   Removing a load-bearing point leaves no post; other details are side details. Cut-and-report
   applies only to externally checkable facts. Report findings without limit. The limit is one
   context question. Append its answer verbatim under `# Added context` and repeat steps 5–7. If it
   could change classification, wait. If the material stays shallow, use the no-draft path.
9. Draft one idea with a supported structure:
   - setup → reversal requires `PERSONAL` material for the reversed belief or advice
   - outside idea explained correctly → implication is normally `PONDERING + ESSAY`
   - concrete scene → claim requires a first-hand `PERSONAL` scene
   - two-column judgment requires a judgment Supreet supplied
   - a 2–4 line micro fits any source type when complete without build-up
   Milestones may state the news directly. Never manufacture a structure, scene, analogy, quote,
   number, customer, or feeling.
10. **Never reuse a sentence, opening, analogy, or distinctive phrase from examples or research.**
    Profile discourse markers may recur, but never copy the clause after one. Match the register: essays usually
    use deliberate emoji and 4–6 relevant hashtags; micro posts often use neither. In notes,
    label every claim `[MEASURED]`,
    `[OBSERVED]`, `[INFERRED]`, or `[OPINION]` and run all seven checks in the epistemic gate. Check
   claims of absence as carefully as positive claims. A claim that cannot carry a label gets cut,
   not hedged. If a required cut removes the load-bearing point, take the no-draft path.
11. Write post text without frontmatter to a temporary file and execute:

```bash
python3 <this-skill-directory>/scripts/validate_draft.py <temporary-file>
```

Fix blockers and judge warnings. A pass only clears this PII, secrets,
confidentiality-marker, and formatting scanner. It cannot detect invention, borrowed claims, thin
material, unsupported numbers, or missing customer clearance.

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
    - **Draft:** If research found a side contradiction or outside overlap, first show
      `Contradictions, cuts, and overlaps`. Name the exact cut and why it is false, or the shared core
      claim, with source links. Then show the entire draft.
      Below it, list sourced facts and rejected or unconfirmed research with links. Post the same
      package to the Slack approvals channel. Ask what he wants changed. Do not publish. Tell him:
      `Approve in the Slack thread, or run /linkedin-publish when the final text is ready.`
    - **No draft:** Change the idea to `status: blocked` and set `blocked_on: "<specific evidence,
      confidentiality, contradiction, near-identical overlap, or context needed>". Include every
      blocker and contradiction found during investigation. Then report:

      ```text
      No draft.
      Blocked on: <specific reason>
      To unblock: <one concrete action per resolvable blocker, or "archive this idea">
      ```

## Research rules

Research supports Supreet's idea. It never supplies one.

- **Fact-check what he wrote.** Check numbers, dates, names, regulations, and recalled details.
- **Fill a gap he left open.** Find the figure, mechanism name, or year he gestured at.
- **Explain a borrowed idea correctly.** For a `PONDERING` post the outside concept must be accurate,
  because he explains it properly before mapping it.
- **Check outside overlap.** Write each as `subject → core assertion`. Near-identical means one
  identifiable post matches both fields and either (a) its first one or two sentences use the same
  rhetorical move and key concepts in the same roles, or (b) it develops the same two supporting
  points in the same order. A supplied distinction that changes the assertion means no match. Then
  block and name its title and URL in
  `blocked_on`. Shared topic, claim, or vocabulary alone is commonplace: draft and report the shared
  claim with links to the closest pieces above it.
- **Check whether Supreet already posted it.** Search `~/.linkedin-content/posted/` by underlying
  idea, not exact wording. There is no API read access to his feed, so flag any local overlap to him
  before drafting and stop.

Use public sources only. Supreet's own LinkedIn profile and posts are allowed as first-party
provenance even when LinkedIn requires login. No other gated source and nothing from internal
systems may be used as web research. A web fact is never written as his experience, customer, or
result. Do not add statistics for authority. **Facts may be sourced; wording may not.**

## Quality bar

Prefer `PERSONAL` and `PONDERING` when several ideas are equally strong. Do not turn internal
engineering details into a CEO post unless Supreet supplied the buyer impact or changed belief.

No evidence, no post. An honest opinion is evidence of what Supreet believes, but never present it as
a measured industry result.
