# Level 0 Generator — Course Map Prompt

> **How to use:** Replace `{TOPIC}` with your subject (e.g. "Systems Thinking", "Cryptography", "Economics", "DevOps"). Paste the whole prompt into a long-context model and save the output as `<topic-slug>/level-0.md` in your competencies-db repo.

---

## The Prompt

---

You are generating a **Level 0 course map** for the topic: **{TOPIC}**

This document is personal knowledge infrastructure, not a summary or a study guide. Its purpose is to give the learner a durable, navigable map of the domain — structured so they can return to it at any point and know exactly where they are, where they have been, and where they could go next.

---

### About the learner

The person this map is built for:

- Thinks **top-down and contextually** — they want the map before the territory, and the historical thread before the mechanics. They need to understand *where something sits* in the larger picture before detail becomes meaningful.
- Is **not a beginner** in general. They have professional experience and are returning to foundations to fill conceptual gaps — not to learn from scratch.
- Is drawn to **the reasoning behind things** — why decisions were made, what problem something was invented to solve, what came before and led to what came after.
- Wants descriptions that give **direction**, not definitions. A description should tell them what drilling into this topic will reveal, not just label what it is.

---

### Output format

Produce a markdown document with the following structure:

**Header block:**
- Title: `# {TOPIC} — Level 0: Course Map`
- A blockquote with two fields: `Intent` (why a practitioner would study this domain) and `Your angle` (how someone returning to foundations with existing experience should approach it)

**How to use this map** — a brief prose section explaining Level 1 and Level 2 and when to descend.

**Topic Inventory** — the main body. Organised into logical groups (e.g. Foundations, Core Theory, Applied). Each group contains Level 1 topics. Each Level 1 topic contains Level 2 candidates.

**Sequencing note** — a closing prose section explaining the dependency chain across topics and identifying the highest-leverage entry points for this specific learner profile.

---

### Rules for Level 1 topics

Each Level 1 topic must have:

1. **A slug and title** — formatted as `#### L1-NN · Topic Name`
2. **A "What it is and why it matters" paragraph** — written in the learner's style. Lead with historical context or the problem it was invented to solve. Explain where it sits in the larger picture. Tell the learner what becomes possible once they understand this — not just what it is.
3. **A "Level 2 candidates" list** — 4 to 7 sub-concepts. Each candidate must have:
   - A **name**
   - A **one-sentence description** written as *direction*, not definition — it should tell the learner what drilling into this sub-concept will reveal or unlock, framed in terms of the reasoning or the tradeoff, not just the label.

---

### Rules for Level 2 candidates

Each candidate description should answer one of these questions (implicitly, not explicitly):

- What problem does this solve that the parent topic alone cannot?
- What breaks or becomes surprising if you don't understand this?
- What does understanding this unlock in adjacent topics?
- What historical or design decision does this explain?

Avoid generic descriptions like "an important concept in X" or "how X works." Every description should give a reason to go deeper — or a reason to skip it for now.

---

### Rules for grouping

- Group topics into 2–4 logical clusters that reflect the natural structure of the domain (e.g. Foundations → Core Theory → Applied, or Historical → Structural → Practical).
- Group names should be meaningful, not generic. "Foundations" is fine if it reflects a genuine dependency layer. "Miscellaneous" is not acceptable.
- The ordering within and across groups should reflect **logical dependency** — topics that must be understood before others come first.

---

### Rules for tone and style

- Write for someone who will read this document quickly and use it as a navigation tool, not a learning resource in itself.
- No padding. No "this section covers..." preamble. No bullet points that just repeat the heading in sentence form.
- Descriptions of Level 1 topics should be 3–5 sentences. No more.
- Descriptions of Level 2 candidates should be one sentence. Tight and directional.
- Historical references (names, years, papers) are encouraged where they add context. They are not decoration — they anchor ideas in the progression of the field.

---

### Produce the document now for: **{TOPIC}**
