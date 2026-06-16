Got it — the intent carries the user description implicitly. Here's the revised prompt:

---

You are producing a single-page field guide from a Level 0 course map. The output is a practical reference — a trigger and orientation tool — not a summary or a study guide. It should be something the user pulls up when facing a real problem, not when preparing to learn.

You will be given:
- A Level 0 course map covering a domain
- An intent describing what the guide is for and who it is for

---

**Your output has four sections. Produce them in this order.**

**1. Introduction**
Four subsections:

*Purpose* — One short paragraph. What is this guide for? Name the specific moment the user should reach for it. Be concrete — "when you are looking at X and need to decide Y" is better than "to help you think about Z."

*Principles* — Three principles that underpin everything in the guide. Each principle should be written consequence-first: not just the idea, but what goes wrong when you ignore it. No platitudes. Each one should feel specific to this domain.

*Outcomes* — Written as a list of things the user can do or answer when applying this well. Not knowledge they possess — capabilities they demonstrate. Start each with "you can."

*How to use* — Two to three sentences. Name the order the sections should be read in, when to follow a reference vs stay at the surface, and what the guide is not for.

**2. The Core Framework**
The main questions, steps, or components that structure thinking in this domain. The form depends on the intent:
- If the intent is analytical (evaluating, designing, deciding) — use questions
- If the intent is procedural (reading, navigating, diagnosing) — use ordered steps
- If the intent is a taxonomy (types, layers, categories) — use named components

Each entry has:
- A title (the question, step, or component)
- Two to four sentences: what it is probing or doing, and why it matters
- Keywords: three to six terms that would appear in real discussions of this concept — specific enough to be useful, not so generic as to be decorative
- Section references: the L1 codes from the course map that are most relevant, with their titles

**3. Gut Checks**
Four to six lighter questions or heuristics that surface when something feels off but can't be named. These are not part of the main framework — they are diagnostic. Each one should be phrased as a question the user asks themselves, followed by two to three sentences on what the question is actually probing and what a bad answer looks like. Include keywords and section references as in section 2.

**4. Resource Map**
Organise the source material by group or tier as it appears in the course map. For each group:
- One sentence on what it covers and why it matters to this guide
- Which parts of the framework it is primary to
- The L1 section codes and titles it contains

---

**Tone and style rules**
- Write for a practitioner with production experience and working instincts. This guide makes those instincts explicit — it does not teach from scratch.
- Every sentence should earn its place. Cut anything that is true but not useful at the moment this guide is reached for.
- Principles and gut checks should feel like things a senior engineer would actually say, not textbook definitions.
- Keywords should be terms that appear in real codebases, real conversations, and real incident reports — not chapter headings.
- Section references are navigation aids, not citations. Only include them where they would genuinely help someone go deeper on a specific gap.
- The guide should fit on one page when printed. If a section runs long, cut the weakest entries rather than summarising.

---

**Inputs:**

Level 0 map: `{level_0_map}`

Intent: `{intent}`