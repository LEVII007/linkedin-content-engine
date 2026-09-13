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
   The profile wins over generic voice rules. For surface habits, the register-specific examples
   and rules in the profile win over any general checklist.
3. Select the named idea only if it has `status: new`, or select the oldest new idea. Skip `blocked`,
   `drafted`, and all other statuses. Never invent a topic when the inbox is empty.
4. Read the whole idea and its added context.
5. Check substance and confidentiality before research:
   - What exactly happened or what does Supreet believe?
   - Why can he specifically say it?
   - Which details are public?
   - What is still missing?
   Apply the confidentiality filter now. An internal number needs a named dashboard, query, or other
   artifact with its date range. A per-customer operational metric also needs that customer's
   clearance, even when unnamed. “One customer” is not de-identification when the public customer
   set is narrow. Never invent a descriptor to make a customer publishable. If a check fails, go to
   the no-draft path in step 14.
6. Research and check prior posts before classification. Scale the work to the apparent material:
   - first-hand personal story: zero or one search, only for a factual claim that needs checking
   - outside-in pondering: two to four searches, enough to verify the outside idea and commonness
   - milestone: one to three searches, focused on the announcement and any stated fact
   Research never upgrades a thin idea. Check `~/.linkedin-content/posted/` for the same underlying
   point. See [Research rules](#research-rules).
7. Classify on two separate axes after research:
   - source type: `PERSONAL` for first-hand moments, decisions, or changed beliefs; `PONDERING` for
     an outside-in idea; `MILESTONE` for real company, product, team, or event news
   - register: `MICRO` for one short, self-contained take; `ESSAY` only when the supplied material
     supports a developed argument
   A note can be `PONDERING + MICRO`. Research volume never changes the register. Material that only
   supports a micro post stays micro.
8. Report every contradiction and blocker before drafting; this reporting has no numerical limit.
   If context is missing, ask at most one short question. Append the answer verbatim under
   `# Added context`, then repeat steps 5–7. If the answer could change the source type or register,
   do not proceed without it. If the material remains shallow, use the no-draft path.
9. Draft one idea only. Use a structure that the source type and register support:
   - setup → reversal
     requires `PERSONAL` material for the belief or advice being reversed
   - outside idea explained correctly → enterprise/pharma implication
     is the normal `PONDERING + ESSAY` structure
   - concrete scene → claim
     requires `PERSONAL` first-hand material
   - two-column judgment
     requires a real judgment Supreet supplied
   - 2–4 line micro post
     fits any source type when the thought is complete without build-up
   Milestones may state the news directly. Never manufacture a structure, scene, analogy, quote,
   number, customer, or feeling.
10. Do not reuse sentences, openings, or analogies from `examples.md` or from any page found during
    research. Short discourse markers listed in the profile, such as “Here's the thing:”, may recur;
    they are cadence, not borrowed sentences. Never copy the clause that follows one. Match the
    surface habits for the chosen register: essays usually use deliberate emoji and 4–6 relevant
    hashtags; micro posts often use neither. In working notes, label every claim `[MEASURED]`,
    `[OBSERVED]`, `[INFERRED]`, or `[OPINION]` and run all seven checks in the epistemic gate.
    “Roughly”, “about”, and “~” do not rescue an unsupported number. Check claims of absence as
    carefully as positive claims. A claim that cannot carry a label gets cut; a failed gate takes
    the no-draft path.
11. Write the post text only, without frontmatter, to a temporary file and execute:

```bash
python3 <this-skill-directory>/scripts/validate_draft.py <temporary-file>
```

Fix scanner blockers. Warnings require judgment; they are not automatic failures. A pass means only
that this PII, secrets, confidentiality-marker, and formatting scanner found no blocker. It cannot
detect invention, borrowed claims, thin material, unsupported numbers, or missing customer
clearance. The earlier gates still control whether a draft is safe.

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
    - **Draft:** Show the entire draft. Below it, list every sourced fact with its link and anything
      research rejected, contradicted, or failed to confirm. Ask what he wants changed. Do not
      publish. Tell him: `Run /linkedin-publish when the final text is ready.`
    - **No draft:** Change the idea to `status: blocked` and set `blocked_on: "<specific evidence,
      confidentiality, commonness, overlap, or context needed>"`. Then report:

      ```text
      No draft.
      Blocked on: <specific reason>
      To unblock: <one concrete action, or "archive this idea">
      ```

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
- **Check whether the point is already commonplace.** If recent posts make the materially same
  point, especially with a closely matching opening, report the overlap before drafting, set the
  idea to `blocked`, and stop. Supreet can sharpen the angle or archive it.
- **Check whether Supreet already posted it.** Search `~/.linkedin-content/posted/` by underlying
  idea, not exact wording. There is no API read access to his feed, so flag any local overlap to him
  before drafting and stop.

Hard limits:

- A fact found online is never written as his own experience, customer, or result.
- If research contradicts something he said, report every contradiction before drafting and stop.
  Never silently correct him.
- If a claim cannot be verified, either cut it or attribute it to what he actually knows.
- Do not add statistics to make a post sound authoritative. Every number must earn its place.
- Public sources only. Supreet's own LinkedIn profile and posts are allowed as first-party
  provenance even when LinkedIn requires login. No other gated source and nothing from internal
  systems may be used as web research.
- Never reuse wording from a research source. Facts may be sourced; sentences may not.

## Quality bar

Prefer `PERSONAL` and `PONDERING` when several ideas are equally strong. Do not turn internal
engineering details into a CEO post unless Supreet supplied the buyer impact or changed belief.

No evidence, no post. An honest opinion is evidence of what Supreet believes, but never present it as
a measured industry result.
