# Post Shapes

Pick the shape that fits the material. Never force material into a shape.

If none of these fits, write it plainly without a shape. A shape is a convenience, not a
requirement — and "it didn't fit a template" is not a reason to change the content.

---

## 1. The wrong assumption

Best shape for a bug or misunderstanding that survived a while. Most technical findings are this.

```
[what you believed, stated plainly]
[what was actually happening]
[how you found out]
[the number, on its own line]
[what you'd check first if you hit this]
```

Works because the reader is probably holding the same wrong assumption right now.

## 2. The undocumented boundary

For "this vendor feature does not work the way the docs imply."

```
[what the docs/API suggest]
[what actually happens]
[how you verified it — this part is mandatory, it's what makes it credible]
[the workaround, or that there isn't one]
```

Verification is the whole post. Without it this is a complaint.

## 3. The measurement

For an eval, benchmark, or before/after with real numbers.

```
[what you measured and why it mattered]
[the setup, briefly — enough to judge whether it was fair]
[the result]
[what surprised you]
[what it does not prove]
```

The last line is what separates this from marketing. Include it.

## 4. The short one

For a finding that needs no scaffolding. Three to five sentences, no structure.

```
[the finding]
[the one detail that makes it real]
[the implication, or nothing]
```

Do not pad this. The brevity is the form.

## 5. The reversal

For when you changed your mind about something, with the reason.

```
[what you thought and why it was reasonable]
[what changed it — specific event or data]
[what you think now]
[what you're still unsure about]
```

Requires actually having changed your mind. Do not manufacture the arc.

---

## Anti-shapes

Do not write these, regardless of what the material is:

- **The numbered lesson list.** "5 things I learned about X." Reads as generated because it usually is.
- **The humblebrag case study.** "Client was struggling. We stepped in. Now they're up 40%."
- **The fake dialogue opener.** "A founder asked me last week..." — unless someone actually did, and
  the transcript is in `Provenance`.
- **The one-line-per-paragraph cadence.** Every sentence on its own line with blank lines between.
  It signals "written for the algorithm" more than any word choice does.
- **The manufactured specific.** Upstream required "one micro-anecdote with a day, a person, and a
  physical object" per case study. Never do this. If a specific detail is not in `Evidence`, it does
  not go in the post — a fabricated detail about your own work is a fabricated claim about your work.
- **The broad closing takeaway.** "And that's why observability matters." Stop at the finding.

## Formatting

- Plain text. LinkedIn renders no markdown; `**bold**` publishes as literal asterisks.
- Line breaks work and are the only structural tool available. Use them for real breaks, not rhythm.
- Hashtags: at most two, only if genuinely searched terms. Zero is fine and usually better.
- Links suppress reach a little. If the link matters more than the reach, keep it in the body.
