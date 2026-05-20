# Structural Companion Prompts

Two prompts that produce a learning companion for an article: one for
an engineering audience, one for an analyst audience. The companion is
the discussion section that follows the article, moving the reader
from surface familiarity with the terminology to a working model of
how the underlying system actually operates.

Files:

- `learningCompanionEngineer.md` — for technical engineering articles
- `learningCompanionAnalyst.md` — for analytical writing (economic,
  geopolitical, structural)

Both prompts take `{content}` as the article body.

---

## What These Prompts Do

The shared premise is that systems — whether technical or
social-political-economic — have real mechanics, and that surface
familiarity with terminology is not the same as understanding how
the mechanics actually operate. The companion's job is to reconstruct
those mechanics for the reader with enough scaffolding that they
finish holding a working model, not just a vocabulary.

Both prompts produce a five-section structure:

1. **Why This Conversation Is Happening** — establishes the
   real-world condition or material reality that makes the topic
   matter. Frames the problem the reader should hold in their head
   before being asked to understand anything.
2. **What You Need To Know First** — two to four prerequisite
   concepts, each explained just enough to remove the blocker. The
   explicit discipline: if a prerequisite needs more than a short
   paragraph, the companion is going too deep.
3. **The Key Ideas, Connected** — the central ideas of the article
   walked through in order, with the mechanism of dependence between
   each one made visible. A chain, not a list.
4. **Handles and Anchors** — two or three portable instruments
   (analogies, comparisons, diagnostic questions, single-sentence
   captures) the reader can carry into future situations.
5. **What This Changes [When You Build / In How You Read The World]**
   — three to five specific implications, written in the form "an
   engineer/analyst who understands this will approach X differently
   because Y." Names the failure mode of the unaware practitioner
   alongside the success of the aware one.

---

## How They Work Internally

The prompts share a pedagogical method. Several instructions are
doing more work than they look like they are doing, and are worth
preserving across any future variant:

- **Numerical guidance.** Two to three paragraphs for the opener,
  two to four prerequisites, three to five implications. These
  bounds prevent the companion from either truncating or
  ballooning, and they force the model to make selection decisions
  rather than enumerating.
- **The "going too deep" test.** "If a prerequisite requires more
  than a short paragraph to explain at this level, you are going
  too deep." This stops the companion from drifting into full
  treatments of background concepts.
- **Chain, not list.** "Each concept should feel like it earns the
  next." Prevents the central section from collapsing into bullet
  points or disconnected paragraphs.
- **The five-minute conversation test.** A handle passes if the
  reader could explain the concept to a colleague in five minutes
  without referring back to the article. Forces handles to be
  genuinely portable.
- **The example-sentence template.** "An engineer/analyst who
  understands this will approach X differently because Y."
  Prevents the final section from collapsing into generalities like
  "this is important" or "engineers should be aware of this."
- **Explicit anti-generalisation instruction.** Both prompts list
  the phrases to avoid by name, which is more effective than asking
  for specificity in the abstract.

The two prompts differ in orientation paragraph and section tuning:

- The **engineer** prompt orients toward mechanics, dependencies,
  failure modes, and tradeoffs. The closing section is "What This
  Changes When You Build."
- The **analyst** prompt orients toward material conditions,
  structural mechanisms, and the gap between surface narrative and
  underlying reality. The closing section is "What This Changes In
  How You Read The World."

The analyst prompt's orientation is more contested terrain than the
engineer's, which is why it states its point of view explicitly in
the opening. The engineer prompt now does the same for parallelism,
though the orientation it names is less contested.

---

## How To Extend Or Adapt

If creating a variant for a new audience (researcher, designer,
operator, clinician), preserve:

- The five-section structure and the section names' grammatical
  parallelism (verb-led second person, present tense).
- The numerical bounds in each section.
- The discipline instructions ("going too deep is failure," "chain
  not list," "avoid these phrases by name," the five-minute test,
  the example-sentence template in the final section).
- The orientation paragraph at the top, naming what kind of
  understanding the companion is trying to produce.

Tune for the new audience:

- The **opener framing** — what real-world condition makes the
  topic worth attention, and what specifically goes wrong without
  understanding it. Engineers face failure modes; analysts face
  misreadings; researchers face confounded inference; designers
  face misfitted artifacts.
- The **prerequisite kinds** — name the categories of background
  concepts that count for that audience (mechanisms, tools,
  conventions, actors, institutions, methods, materials, etc.).
- The **chain reinforcement** — what does "the mechanism of
  dependence" look like in this domain? For engineers it is causal
  or structural; for analysts it is material or institutional; for
  other audiences it may be methodological or experiential.
- The **closing section name and verb** — "What This Changes When
  You Build / Read / Investigate / Design / Treat." The verb should
  name the practitioner's primary action.

What not to add:

- A "balanced perspectives" or "alternative views" section. The
  companion has a point of view: that the article's structural
  reading of the world is the reading worth holding. Adding
  balance turns the companion into a generic critical-thinking
  exercise and dissolves its pedagogical function.
- A "summary" or "key takeaways" section. The companion is not a
  summary; it is a reconstruction with scaffolding.
- Open-ended invitations like "what questions do you have?" or
  "further reading." The companion is a closed pedagogical unit,
  not a discussion prompt.

---

## Tested Against

- Technical infrastructure articles (compute abstractions)
- Primary-source political texts (Mao 1956 interview)
- Heterodox economic commentary (Hudson on the 2026 financial
  crisis)

The prompts behave consistently across these and produce companions
that are recognisably parallel in structure while being substantively
different in voice and content per the source material.