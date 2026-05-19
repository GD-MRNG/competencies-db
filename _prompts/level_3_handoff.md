# Level 3 Handoff Prompt

You are helping plan a Level 3 "build" post based on a Level 2 "depth" post
from a technical engineering blog series. Your job is not to write the post —
it is to analyse the source material and propose exercise or practice ideas
that a Level 3 post could be built around.

The reader this post is aimed at: someone who has read the Level 2 post,
understands the concepts at a thinking level, but has never applied or
implemented them in practice. They are not beginners to engineering in general
— they are beginners to this specific topic in action. Proposals should be
pitched accordingly: not re-teaching the concepts, but forcing the reader to
use them under real conditions for the first time.

---

## The 10-Minute Benchmark

All exercises and practice activities — without exception — must be
completable in approximately ten minutes by a reader who already has
the relevant tools installed. Ten minutes is the working benchmark,
not a hard ceiling, but any proposal that cannot be done in roughly
that time is too large and must be scoped down.

This constraint changes what an exercise is. At ten minutes, the goal
is not to build a system — it is to create a single moment of
comprehension. A valid exercise at this scale might be: three lines of
configuration that make a behaviour visible, a CLI command whose output
the reader now understands differently, a short code snippet that
demonstrates a tradeoff, or a deliberate mistake that produces a
revealing error. The output is not a product — it is a specific thing
the reader now knows from having done it.

Tool installation is not part of the exercise. Assume the reader has
the relevant tools in place. The setup section should only list what
needs to be true before the reader starts — not what they need to
install from scratch.

---

## Stage 1: Concept Extraction and Buildability Assessment

Read the Level 2 post carefully. Identify the three to five ideas that are
central to the article's argument. For each one, write a single sentence
stating what the concept is and what it does or explains. Then make an honest
assessment: is this concept demonstrable through a short hands-on exercise,
or is it primarily conceptual or decision-oriented?

At the end of this stage, make a clear call: does this material support
hands-on exercises at the ten-minute scale, or does it call for structured
practice of a different kind? Some topics — particularly those focused on
thinking frameworks, evaluation models, or architectural judgement — do not
translate naturally into something a reader can type or configure. If this
material falls into that category, say so clearly and proceed to the
Alternative Practice Proposals section instead of Stage 2.

---

## Stage 2: Exercise Proposals

Only proceed here if Stage 1 determined that hands-on exercises are a
genuine fit for this material.

Propose exactly three exercises. Apply the following constraints to all
three without exception:

**The ten-minute test:** Before finalising each proposal, ask: could a
reader with the tools already installed complete this in roughly ten
minutes? If not, cut scope until the answer is yes. One file is better
than two. One command is better than five. A focused demonstration of
a single behaviour is better than a mini-project that touches several.

**Tool versions:** Use the latest stable release of any tool involved.
Name the version explicitly. If a tool moves fast enough that a pinned
version number would be misleading within weeks, name the official
documentation page where the reader should confirm the current version.

**Ordering:** Arrange the three proposals in ascending order of
complexity — lightest first, most involved last. The three should
feel like a progression: a reader could do all three in sequence
and each one would deepen what the previous one established.

**Differentiation:** Each proposal must differ from the others in at
least one meaningful way: the type of interaction the reader has
(running commands, editing config, reading output, making a decision),
the concept it isolates, or the kind of friction it creates.

For each proposal, provide:

**Concept it teaches**
Name the specific concept from Stage 1 this exercise makes real.
There should be a direct line between the concept extracted and the
exercise proposed.

**What the reader does**
Describe the activity concretely — specific enough that the reader
can picture exactly what they will type, click, or write. Two to
three sentences. This is not a full walkthrough, but it should leave
no ambiguity about the shape of the exercise.

**What the reader sees or produces**
The concrete output at the end — terminal output, a config file,
a visible behaviour change, a documented observation. Be specific.
This should be small and clear, not a system or a project.

**Setup check**
What needs to be true before the reader starts. Name tool versions.
Do not include installation steps — just the preconditions.

**The friction point**
The single specific moment in this exercise where real understanding
is forced. A decision with no obvious answer, an error that teaches
something, a result that surprises, or a behaviour that only makes
sense once you have seen it. This is what distinguishes doing from
reading. State it as a concrete moment, not a general learning outcome.

**Why this satisfies the Level 3 brief**
One to two sentences confirming that this produces a working outcome,
forces real choices, and gives the reader something concrete at the end.

---

## Alternative Practice Proposals

Only proceed here if Stage 1 determined that hands-on exercises are not
a good fit for this material.

Propose exactly three alternative practice formats. These are not a
consolation section — they should be as rigorous and specific as
exercise proposals. The goal is still to force the reader to use the
ideas under real conditions for the first time, through a different mode.

The ten-minute benchmark applies here too. Possible formats include
but are not limited to: a structured reflection against a system the
reader already works on, an annotated evaluation of a real tool using
the article's framework, a decision audit where the reader applies the
article's criteria to a past choice and documents what they find, or
a comparative analysis between two approaches using the article's
concepts as the evaluative lens.

Arrange proposals from lightest to most involved. Apply the same
sections as exercise proposals: the concept it addresses, what the
reader does, what they produce, any preconditions, the friction point,
and why it satisfies the Level 3 brief.

---

### The Level 2 post

```
{level_2_post}
```