# Level 1 Prompt

Generate a Level 1 concept post for a competency system. A Level 1 post answers "what is this and why does it matter" for a single topic and builds the reader's working mental model. It is not a tutorial, not a deep dive, and not an exhaustive reference. It is the article you would write if a smart colleague asked you to explain this topic over coffee — substantive, opinionated about what matters, and confident about what to leave out.

## Inputs

### Course context (Level 0)

```
{level_0_summary}
```

### Module or chapter content

```
{module_content}
```

## Output

A markdown document with two parts: the concept post, then the Level 2 handoff.

### The concept post

**Format**

- A single H1 heading with the topic title. If the source numbers its sections (e.g. "1.1 Networking Fundamentals"), preserve the numbering.
- 4–8 paragraphs of flowing prose. No subheadings, no bullet points, no code blocks, no bolded key terms inside the prose.
- 600–1500 words.

**Voice and structure**

- Direct and authoritative. Second person ("you").
- Open with a hook that frames why this matters — a counterintuitive premise, a common blind spot, or a reframing of how the reader was thinking about it. Not a section recap, not "this article will cover X."
- Build the mental model first. Then introduce the concrete components or sub-concepts in flowing prose, using compare/contrast and parenthetical clarifications where useful. Close with the practical implication or the skill this topic builds.
- Stay grounded in concrete consequences — what breaks, what fails, what the reader will actually encounter.
- Use sharp closing lines where they earn their place. Avoid hedging ("it might be useful to..."). Define only the terms the mental model rests on.

**Style anchor**

The voice should feel like this:

> Networking is the most common blind spot for developers moving into operational work, and it is the most consequential one. When a developer thinks about their code, they tend to think in terms of function calls, objects, and data structures. When a request fails in production, however, the failure is almost never inside the code itself; it is almost always in the path the request takes to reach the code, or the path the response takes to return from it.

**Adaptation**

Do not assume the topic is technical. If the source material is non-technical, drop the technical framings (failures, request paths, deployments) and adapt the same voice to the actual subject — the hook, the mental model, the components, and the practical takeaway all generalise.

### The Level 2 handoff

After the concept post, add a section titled `## Level 2 candidates` listing 3–7 sub-concepts within this topic that would warrant a Level 2 deep dive. One paragraph per candidate, in this format:

**Sub-concept name** — one sentence on what it covers; one sentence on why it's worth going deeper.

Include only sub-concepts that genuinely have depth worth exploring at Level 2. If a sub-concept is fully handled by the Level 1 post itself, leave it out.

## Rules

- Do not invent content not present in or directly inferable from the inputs.
- If the input clearly covers multiple distinct topics rather than one, write the post for the dominant topic and list the others as candidates for separate Level 1 calls in a brief note at the top of the document.
- Output only the document — no preamble, no commentary.
