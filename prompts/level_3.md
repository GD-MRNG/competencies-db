# Level 3 Prompt

Generate a Level 3 build post for a competency system. A Level 3 post is a short, hands-on walkthrough that takes a reader who already understands the concept (from Level 2) and forces them to use it under real conditions for the first time. It is not a tutorial that re-teaches the idea. It is a focused exercise — completable in roughly ten minutes by a reader with the right tools already installed — that produces a single moment of comprehension.

## Inputs

### Course context (Level 0)

```
{level_0_summary}
```

### Parent Level 2 post

```
{level_2_post}
```

### The chosen exercise

```
{exercise_description}
```

This is one of the three exercise proposals from the Level 3 handoff. It names the concept the exercise teaches, what the reader does, what they see or produce, the setup check, the friction point, and why it satisfies the Level 3 brief. Treat it as the structural spine of the post — not a draft, but a direction. Your job is to expand it into a complete walkthrough without changing its scope.

## Output

A markdown document.

### Format

- A single H1 heading with a descriptive title for the exercise. Preserve the parent's hierarchical numbering if it uses one (the parent L2 might be "1.1.3 DNS: The Resolution Chain", so an L3 underneath could be "1.1.3.a Watch TIME_WAIT Appear After Short-Lived TCP Connections").
- The body organised under the section structure described below, using H2 headings for each section.
- Code blocks, commands, and config snippets are first-class — this is a build post, and concrete material belongs here. Every snippet must be annotated with what it does and why it matters.
- 800–1,500 words total. The exercise is short by design.

### Section structure

Every Level 3 post has these sections, in this order, each as an H2:

**`## What you will have at the end`**
A short, direct statement of the concrete thing the reader will have produced. Not what they will have learned — what they will have. Be specific: name the file, the command output, the visible behaviour, the state of their system.

**`## Before you start`**
What needs to be true before the reader begins. Tool versions, any prior configuration, any context from the Level 2 post that is directly load-bearing. Keep this short — it is a check, not an orientation. Do not include installation instructions unless a one-line command is all that is needed.

**`## The walkthrough`**
The step-by-step implementation. Use H3 headings for each step that name what the step does (not just "Step 1"). Each step contains the actual thing to type, write, or run, in code blocks where appropriate, plus an explanation of what the step is doing and why it matters. Where the explanation connects to a Level 2 concept, point at it briefly — do not re-explain it.

**`## What success looks like`**
Describe the working outcome concretely. What does the reader see? What output, behaviour, or state confirms it worked? If there is a non-obvious sign of success, name it. If there is a common mistake that produces a misleading-looking result, name that too.

**`## What you just did`**
Two to three sentences stepping back from the implementation to name the concept that just became real. Connect the specific thing the reader did to the idea from the Level 2 post. Not a summary — a moment of consolidation.

**`## What this exposes`**
Close the post by naming what the exercise has now made visible — the edges, the decisions that could have gone differently, the behaviours that would change at scale or under failure, the questions the exercise has now raised. Frame these as observations from having done the thing, not as forward signposts to a future post. The reader should finish feeling that they have crossed a threshold and can see further than they could before.

### Voice and rules

- Direct, second person, practitioner-oriented. The same voice as Level 1 and Level 2.
- **Commit to one path.** Do not hedge with "you could also do it this way." Decisions left open at Level 2 are made here. Pick a tool, a version, a structure — and justify the choice briefly when the choice is non-obvious.
- **Explain every snippet.** Every block of code, configuration, or command is annotated with what it does and why it is there. Never present a block and move on.
- **Use real, current material.** Tool versions, command syntax, and configuration must be accurate for the latest stable release. Name versions explicitly. If a tool moves fast enough that pinning is misleading, name the official documentation page where the reader should confirm.
- **Keep the scope tight.** Do not expand the exercise into a larger project. Stay at the ten-minute scale defined by the original exercise description.
- Do not re-teach what the Level 2 post already covered. Reference it; do not repeat it.

### Adaptation

Do not assume the exercise is technical. If the source material is non-technical and the chosen "exercise" is an alternative practice format (a structured reflection, a decision audit, a comparative analysis), adapt the same section structure — what you will have at the end, before you start, the walkthrough, what success looks like, what you just did, what this exposes — to the actual practice. Code blocks and command snippets become whatever artefacts the practice produces.

## Rules

- Do not change the scope of the exercise. The handoff already scoped it deliberately; honour that.
- Do not invent steps that weren't implicit in the exercise description.
- Do not add a Level 4 signpost. Levels 4 and 5 are not part of the standard learner pipeline; the closing section names what the exercise exposed, not what comes next in the series.
- Output only the document — no preamble, no commentary.
