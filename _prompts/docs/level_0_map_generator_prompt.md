# level_0_map_generator_prompt.md — Documentation

> This file documents the Level 0 map generator prompt. Read it before using the prompt for the first time, and return to it when output quality feels off.

---

## What this prompt does

It generates a **Level 0 course map** — the entry document in the competencies-db system — for any topic you supply. The output is a structured, navigable map of a domain: not a summary, not a study guide, but an inventory of what the domain contains, how its parts relate, and where to go first.

The document it produces has two layers:

- **Level 1 topics** — one per major concept in the domain. Each is a candidate for a Level 1 concept post.
- **Level 2 candidates** — 4–7 sub-concepts under each Level 1 topic. Each is a candidate for a Level 2 depth post.

You do not generate everything in the map. The map is a worklist and a navigation tool. You descend only into the topics and sub-concepts where deeper mastery is worth the effort right now.

---

## What makes this prompt different from a summary prompt

A summary prompt produces a condensed version of what a domain contains. This prompt produces something structurally different: a **dependency-ordered, direction-carrying map** designed for re-entry after absence.

The specific constraints that create that difference:

- **Direction over definition.** Every description — Level 1 and Level 2 — is written to tell the learner what drilling into this topic will reveal or unlock, not just what it is. A description that could appear in a dictionary is a failure mode.
- **Dependency ordering.** Groups and topics within groups are sequenced so that things that must be understood before others come first. The map reflects the logical structure of the domain, not alphabetical or arbitrary order.
- **Honest depth signalling.** The Level 2 candidates are explicit about what the Level 1 overview cannot give you. The gap between L1 and L2 is part of the information.
- **Learner profile baked in.** The prompt carries a fixed learner profile — top-down, contextual, historically-grounded, returning practitioner — so the output is calibrated to how this particular person learns, not a generic reader.

---

## How to use it

**Basic use:**

1. Open `prompt--level-0-generator.md`
2. Replace `{TOPIC}` with your subject — e.g. `Macroeconomics`, `Kubernetes`, `Negotiation Theory`, `Thermodynamics`
3. Paste the full prompt into a long-context model (Claude Sonnet or equivalent)
4. Save the output as `<topic-slug>/level-0.md` in your competencies-db repo

**For topics with a specific intellectual tradition:**

Add a sentence after the `{TOPIC}` declaration specifying the tradition, thinkers, or texts the map should draw from. Example:

> You are generating a Level 0 course map for the topic: **Geopolitical Economy**
> The intellectual tradition this map draws from is: Radhika Desai, Michael Hudson, Ben Norton, and Marx.

This anchors the groupings, the sequencing, and the Level 2 candidates to the specific body of work rather than producing a generic academic overview. For topics with a strong tradition (critical theory, Austrian economics, phenomenology), this addition significantly improves output quality.

**For technical topics:**

No addition needed beyond `{TOPIC}`. The prompt handles technical material (CS, systems, engineering) without modification because the dependency structure of technical domains is usually clear enough for the model to infer correctly.

---

## Output structure

A well-formed output contains:

| Section | Purpose |
|---|---|
| Header blockquote | Intent + learner angle. Calibrates the document to purpose and person. |
| How to use this map | Brief prose. Explains L1/L2 distinction and when to descend. |
| Topic Inventory | 2–4 groups. Each group contains L1 topics with L2 candidates. |
| Sequencing note | Closing prose. States the dependency chain and names the highest-leverage entry points. |

The sequencing note is the most practically useful section for a returning practitioner. It tells you where to start, which is often non-obvious in a complex domain.

---

## What good output looks like

A Level 1 description should:
- Open with historical context or the problem the concept was invented to solve
- Explain where the concept sits relative to adjacent topics
- Tell you what becomes possible once you understand it
- Be 3–5 sentences, no more

A Level 2 candidate description should:
- Be one sentence
- Answer one of: what does this unlock, what breaks without it, what historical decision does it explain, what does it connect to
- Give a reason to descend — or implicitly, a reason to skip

**The test for a bad description:** Could it appear unchanged in a textbook glossary? If yes, it failed. Glossary definitions label. These descriptions direct.

---

## Failure modes to watch for

**Generic groupings.** If the output groups topics as "Introduction", "Advanced Topics", "Applications" — those are organisational placeholders, not structural insights. Regenerate with an explicit note to name groups meaningfully.

**Definition-style Level 2 descriptions.** "An important technique in X" or "How Y works" adds no direction. If you see this pattern, the model defaulted to summary mode. Add emphasis to the direction rule in the prompt or regenerate.

**Missing sequencing note.** If the output ends at the topic inventory without a sequencing section, the most practically useful part is absent. The sequencing note is what converts a map into a starting point.

**Flat structure.** If all topics feel equally important and equally unconnected, the dependency ordering failed. A well-formed map has clear layers — some topics are genuinely prerequisite to others, and the map should make that visible.

**Over-coverage.** A domain forced into 20+ Level 1 topics is probably splitting concepts that belong together, or including applied variations that should be Level 2 candidates. The map should cover a domain at the grain size of *major conceptual moves*, not every subtopic.

---

## How this fits into the competencies-db pipeline

```
{TOPIC} + intellectual tradition
        ↓
level_0_map_generator_prompt.md
        ↓
<topic-slug>/level-0.md          ← this prompt's output

        ↓ (one topic at a time)
<topic-slug>/level-1/<topic-slug>.md

        ↓ (selected sub-concepts only)
<topic-slug>/level-2/<topic-slug>--<sub-concept-slug>.md

        ↓ (selected sub-concepts only)
<topic-slug>/level-3/<topic-slug>--<sub-concept-slug>--<exercise-slug>.md
```

The Level 0 output is the worklist for everything downstream. The Topic Inventory's L1 topics become the filenames in `level-1/`. The L2 candidates under each topic become the filenames in `level-2/`, carrying the parent slug: `distributed-systems--cap-theorem.md`.

Levels 4 and 5 are not generated from course material — they require real experience, decisions, and audiences. The pipeline from this prompt ends at Level 3.

---

## The compounding logic

The map compounds knowledge in two ways.

First, it **forces honest placement**. To put a concept in a group, sequence it relative to others, and write a direction-carrying description, you have to understand it well enough to locate it — not just recognise it. That encoding step is where shallow recognition becomes retrievable structure.

Second, it **creates re-entry infrastructure**. Knowledge decays with disuse, but structure decays slower than detail. When you return to a domain after months away, the map tells you where you were, what you understood, and where the entry points are. You are never starting from zero — you are navigating back into a structure that already exists.

The Level 2 candidates are particularly important for this. They preserve the *next move* at the moment when your understanding was sharpest — so when you return, you don't have to reconstruct what to do next, you just pick up the worklist.

---

## Maintenance

This prompt should be updated if:

- The learner profile changes significantly (new domains of experience, different learning goals)
- A systematic failure mode appears that isn't covered by the prompt's existing constraints
- The competencies-db level structure itself changes

The learner profile is the most likely thing to need updating over time. It is currently calibrated for a returning practitioner with software development experience and a top-down, historically-grounded learning style. If that profile drifts, the calibration drifts with it.