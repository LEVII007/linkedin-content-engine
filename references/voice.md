# Voice

Voice is how the material gets said. It is not a substitute for having material.

Upstream defined voice with a banned-word list and a required signature line, and enforced
character-count variance so posts would not look machine-generated. All of that is deleted. The
reason a post reads as human is that a human did the work and approved the words.

## Active profile

`references/voice-supreet.md` — built from 18 of his own LinkedIn posts. It is the authority for
this user. Where it disagrees with the defaults below, **the profile wins**; the conflicts are
listed in its last section.

## How to build this file

Do not ask the user for adjectives. "Direct but warm" produces nothing usable.

Instead, collect **3–5 things they have actually written** — a Slack explanation of a bug, a PR
description, a doc intro, a reply to a customer. Then extract observable patterns:

- Sentence length: do they run short and clipped, or long with subordinate clauses?
- Where does the conclusion go — first sentence or last?
- Do they use numbers in prose, or hold them for a separate line?
- Hedging: do they say "probably" or state and then qualify?
- Technical register: do they name the function/flag, or describe it?
- What do they never do? (exclamation marks, rhetorical questions, emoji, "folks")

Write down what you observe, with a quoted example per pattern. Replace this section with the
result at setup. Patterns beat adjectives because they are checkable against a draft.

## Generic defaults for a new profile

Use these only until an observed profile exists. Once one exists, keep only rules it supports.
They do not override `references/voice-supreet.md`.

1. **Lead with the finding.** The first 140 characters are all most people see. If the finding is
   "PubMed author matching was measuring how common a name is", that goes first — not the setup.
2. **Name real things.** `pub_count`, `MoveParticipant`, `multilingual_v2`, `data.cms.gov`. A
   specific identifier is evidence that you were there. A generic phrase ("the matching logic")
   is what someone writes when they weren't.
3. **One finding per post.** Two findings means two posts. Compressing both weakens each.
4. **Numbers get their own line.** They are the load-bearing part; do not bury them mid-sentence.
5. **State, then qualify.** "This cut false matches 97.4%. It only works where affiliation strings
   are clean, which is maybe 80% of records." Not: "This may have improved things somewhat."
6. **No engagement bait.** No "thoughts?", no "agree?", no "comment below". If the finding is
   interesting, people respond. If it is not, a prompt will not save it.
7. **Say what you got wrong.** The version where you were wrong first is more useful and more
   credible than the version where you were right all along. It is also usually the true one.

## What not to write

- Anything that reads as a lesson for the reader rather than a report of what happened.
- A conclusion broader than the evidence. One repo's result is not an industry trend.
- Advice. This pipeline reports findings; it does not dispense wisdom.
- A claim about a customer, named or identifiable. See the confidentiality filter in
  `references/idea-inbox.md`.
- A claim about a third party's product that was not verified against their current docs.

## Length

Whatever the material needs. There is no target, no variance requirement, and no minimum.

A finding that takes 300 characters should be 300 characters. Padding a real finding to hit a
length target is the same failure as inventing a topic to fill a calendar slot, just smaller.
