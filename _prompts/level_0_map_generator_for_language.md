# Language Map Generator — Prompt

> **How to use:** Replace `{LANGUAGE}`, `{LEARNER_PROFILE}`, and `{GOAL}` with your specifics. Paste the whole prompt into a long-context model and save the output as `<language-slug>/level-0.md` in your competencies-db repo.

---

## The Prompt

---

You are generating a **Level 0 course map** for the following language and learner:

- **Language:** {LANGUAGE}
- **Learner profile:** {LEARNER_PROFILE}
- **Goal:** {GOAL}

This document is personal knowledge infrastructure, not a study guide or summary. Its purpose is to give the learner a durable, navigable map of the language as a production system — structured so they can return to it at any point and know exactly where they are, what they are working on, and what depends on what.

---

### Core framing

A language is a meaning-production system. The goal of language learning — at every level — is the ability to transmit meaning that a native speaker receives intact. This goal has four failure layers, each of which can break transmission independently:

1. **Sound** — the signal leaving the speaker cannot be decoded by the listener's ear (phonology, prosody, connected speech)
2. **Structure** — the assembly of words does not match how the language builds meaning (grammar architecture, morphology, syntax)
3. **Lexicon** — the right words are not available for production, or the available words are being used wrongly (vocabulary, register, collocation)
4. **Discourse** — individual sentences work but sustained communication breaks down (cohesion, argumentation, repair, register calibration)

These four layers are universal. Every language map must address all four. What varies across languages is the specific content inside each layer — the choices each language makes about how to solve the problem of meaning-construction, and the specific failure points those choices create for this learner coming from their particular background.

---

### About the learner

The person this map is built for:

- Thinks **top-down and contextually** — they want the map before the territory, the architecture before the components. Detail becomes meaningful only once they know where it sits in the larger picture.
- Is **not a complete beginner** in general. They may be a heritage speaker, a reactivating learner, a fluent speaker seeking explicit understanding, or an advanced learner with specific gaps. They are returning to or restructuring foundations, not learning from zero.
- Wants to understand **the reasoning behind things** — why a construction exists, what problem it solves, what breaks if it is misused, what historical or structural decision it reflects.
- Wants descriptions that give **direction**, not definitions. A description should tell them what drilling into this topic will reveal or unlock, not just label what it is.
- Has a **specific interference language or background** that shapes where their gaps are. The map must account for this — failure points that are trivial for one learner may be the highest-leverage entry points for another.

---

### Output format

Produce a markdown document with the following structure:

**Header block:**
- Title: `# {LANGUAGE} — Level 0: Course Map`
- A blockquote with two fields: `Intent` (why someone would build this map — what kind of language use they are working toward) and `Your angle` (how this specific learner, given their background, should approach the domain)

**How to use this map** — a brief prose section explaining Level 1 and Level 2 and when to descend.

**Topic Inventory** — the main body. Organised into the four universal clusters (Sound System, Structural System, Lexical System, Discourse System), with language-specific content inside each. Each cluster contains Level 1 topics. Each Level 1 topic contains Level 2 candidates.

**Sequencing note** — a closing prose section explaining the dependency chain and identifying the highest-leverage entry points for this specific learner profile.

---

### Rules for clusters

The four clusters are fixed:

- **Cluster A — The Sound System:** Phonology, prosody, connected speech. Address the specific phonological inventory of the target language, the prosodic features that carry meaning, and the connected-speech phenomena that cause the gap between textbook input and real native speech.
- **Cluster B — The Structural System:** Grammar architecture, morphology, syntax. Lead with the fundamental typological character of the language (isolating, inflecting, agglutinating, etc.) and explain what that means for the learner. Address the structural features that diverge most sharply from the learner's background language.
- **Cluster C — The Lexical System:** Vocabulary, register stratification, collocation, the writing system if applicable. Address vocabulary as a production tool, not a recognition list. Include any writing system as a sub-cluster within lexis, not as a separate domain.
- **Cluster D — The Discourse System:** Sustained meaning-making above the sentence level. Include a final Level 1 topic on **metalinguistic awareness** — the ability to diagnose production failures by layer — regardless of the language. This is the transferable skill that makes every other cluster more efficient.

---

### Rules for Level 1 topics

Each Level 1 topic must have:

1. **A slug and title** — formatted as `#### L1-NN · Topic Name`
2. **A "what it is and why it matters" paragraph** — written for this learner specifically. Lead with the typological or historical context that explains why this feature exists. Explain what this learner's background means for their relationship to this feature — where they likely have implicit knowledge, where they likely have gaps, and where their background language creates interference. Tell them what becomes possible once they understand this. Three to five sentences.
3. **A "Level 2 candidates" list** — four to seven sub-concepts. Each must have a name and a one-sentence description written as direction, not definition: what drilling this will reveal, unlock, or explain.

---

### Rules for Level 2 candidates

Each candidate description should answer one of these questions (implicitly, not explicitly):

- What breaks or becomes surprising if you don't understand this?
- What does understanding this unlock in adjacent topics or in production?
- What interference pattern from the learner's background does this resolve?
- What historical, typological, or design decision does this explain?

Avoid generic descriptions like "an important concept in X" or "how X works." Every description should give a reason to go deeper — or a clear reason to defer it.

---

### Rules for the sequencing note

The sequencing note must:

- Identify any hard dependencies — features that must be understood before others can be drilled effectively
- Identify the highest-leverage entry point for this specific learner (which may not be Cluster A — for a fluent but unanalysed speaker of the target language, the entry point may be discourse or grammar, not phonology)
- Account explicitly for the learner's background: what they likely already have (even implicitly), what needs to be built, and what interference patterns to address early
- Name the one cluster or topic that, if neglected, will most limit overall progress

---

### Rules for tone and style

- Write for someone who will read this document quickly and use it as a navigation tool, not a learning resource in itself.
- No padding. No "this section covers..." preamble.
- Level 1 descriptions: three to five sentences. No more.
- Level 2 descriptions: one sentence. Tight and directional.
- Historical and typological references (language families, linguistic terms, named phenomena) are encouraged where they add navigational context. They anchor ideas in the structure of the field.
- Every description of a failure point should be honest about what it costs in actual communication — not abstract correctness, but whether a native speaker receives the intended meaning intact.

---

### Language-specific guidance

Before generating the map, reason briefly (internally) through the following:

1. **Typological character** — what kind of language is this? (isolating, inflecting, agglutinating, tonal, etc.) What does that mean for the structural cluster?
2. **Writing system** — does the language use a non-Roman script? A morphophonemic, syllabic, or logographic system? Where does script knowledge fit in the production system?
3. **Interference profile** — given the learner's background language(s), which features of the target language have the most interference potential? Which features are likely to be accidentally correct vs systematically wrong?
4. **Register landscape** — how stratified is the register system of this language? Are there distinct formal/informal lexical layers, honorific systems, or dialect variation that affect which variety the learner should target?
5. **Highest-leverage entry** — given the learner's goal and profile, which layer (sound, structure, lexis, discourse) offers the most immediate payoff? The sequencing note should reflect this reasoning.

Do not include this reasoning in the output. It shapes the document; it does not appear in it.

---

### Produce the document now for:

**Language:** {LANGUAGE}
**Learner profile:** {LEARNER_PROFILE}
**Goal:** {GOAL}