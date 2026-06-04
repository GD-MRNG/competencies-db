## Metadata
- **Date:** 05-06-2026
- **Source:** 10_tool_granularity_and_composition.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-10 · Tool Granularity and Composition

The first instinct when designing tools for an agent is to mirror the API you already have. You have a database client with twenty methods, so you expose twenty tools. You have a browser automation library, so you hand the agent the whole thing. This feels efficient — you're not hiding anything, you're not building extra scaffolding — but it is the wrong instinct, because it treats tool design as an integration problem when it is actually a behaviour design problem. The shape of the tools you give the agent is the shape of the actions the agent will take. Granularity is not a packaging decision. It is a policy decision.

The mental model worth holding is a spectrum. At one end, coarse-grained tools wrap large, opaque capabilities: "fetch any URL," "run this SQL," "summarise this document." The agent does very little to compose them — one call usually accomplishes one goal. At the other end, fine-grained tools expose small, specific operations: "click the element matching this selector," "read row 47 from this table," "extract the third paragraph." The agent has to chain many of them to achieve anything. Most real systems sit somewhere in between, and the question is not which end is correct but where on the spectrum each particular capability belongs.

Coarse tools trade safety for flexibility. Because they expose broad capability, the agent can combine them in ways you did not anticipate, which is often the entire point — you wanted a reasoning system precisely so it could solve problems you had not pre-decomposed. But the same breadth that makes them flexible makes them dangerous. A tool called "run SQL" can read a row, and it can also drop the production database. The model's reasoning is the only thing standing between intent and consequence, and the model's reasoning is, on any given day, somewhere between excellent and embarrassing. Coarse tools assume the agent will use them well. That assumption gets weaker as the stakes get higher.

Fine tools trade flexibility for safety. Each tool does one thing, and that thing is bounded — "click this button" cannot delete your database because the operation simply isn't expressible. The cost is that the agent must do more work to accomplish anything, which means more reasoning steps, more tokens, more chances for the loop to drift or stall. It also means you have to anticipate the operations the agent will need. If you forget to expose the "scroll" tool, the agent cannot scroll, even if scrolling is obviously what the task requires. Fine-grained tool sets are easier to reason about and harder to make complete.

The right granularity depends on three things, and you have to weigh them together. The first is the task: routine, well-understood tasks tolerate (and benefit from) coarser tools, because the agent does not need to improvise. Novel, exploratory tasks may need finer tools so the agent can compose its way through unfamiliar territory. The second is the model's reasoning ability: a frontier model can handle a coarse tool responsibly more often than a small model can, because it understands the consequences of what it is about to call. Give a weak model a coarse tool and you get confident catastrophe. The third is your risk tolerance: in a system where mistakes are cheap and reversible, coarse tools are fine. In a system where a single bad call costs real money or real data, you want the agent's freedom curtailed by the shape of the tools themselves, not just by a prompt asking it nicely to be careful.

This is why the interesting questions live at the edges of the tool surface, not in the middle. What you choose to expose, and at what altitude, is where you encode your trust in the model. A useful exercise: for each tool, imagine the worst plausible misuse and ask whether you can live with it. If you can't, the tool is too coarse for the agent you have. Either narrow it, split it into safer primitives, or wrap it in a guardrail — a dry-run mode, a confirmation step, a human approval gate for the destructive variant. None of those are exotic patterns. They are the natural response to noticing that "the agent could choose to do this" is not the same as "the agent should be able to do this."

There is a second-order effect worth naming: composition. When you give the agent several tools, you are implicitly giving it every combination of those tools. The emergent behaviour can be genuinely useful — agents will discover sequences you would not have written by hand — and it can also be genuinely surprising. A pair of tools that are each safe in isolation may compose into something that isn't. "Read file" and "send email" are both innocent; together they are an exfiltration pipeline. Granularity decisions don't end at the individual tool. They extend to the set, and the set has properties the individuals don't.

The skill this topic builds is taste about interfaces. Most of what makes an agentic system reliable or chaotic is decided before the loop ever runs, in the moment you sketch out which tools exist and what they can do. Get the granularity right and the agent's job becomes tractable: it has the verbs it needs, none of the verbs it shouldn't, and the space of bad outcomes is bounded by construction. Get it wrong and no amount of prompt engineering downstream will save you. The agent will either be too constrained to solve the problem, or too empowered to solve it safely. Tool design is where you make that bet.

## Level 2 candidates

**High-Level vs. Low-Level Tool Design** — Covers the concrete tradeoffs of exposing capabilities at different altitudes — when to wrap a whole workflow as one tool versus when to expose the primitives. Worth deepening because the decision is rarely binary in practice, and there are recognisable patterns (façade tools, tiered toolkits) that experienced designers reach for.

**Tool Composition and Emergent Behaviour** — Covers what happens when the agent combines tools in unanticipated ways, and how to tell the difference between useful creativity and a dangerous gap in your design. Worth deepening because composition is where the surprises live, and most teams discover it the hard way in production.

**Safety and Guardrails** — Covers the techniques for letting the agent hold powerful tools without letting it misuse them: dry-run modes, canary tokens, confirmation steps, scoped permissions, human approval for destructive variants. Worth deepening because each technique has a specific shape and a specific failure mode, and the catalogue is large enough to warrant its own treatment.

**Tool Observability and Tracing** — Covers logging every tool call with enough context that you can later explain why the agent chose it and what happened. Worth deepening because observability for tool use has specific requirements (input/output capture, decision context, correlation across loop iterations) that generic logging misses.

**Tool Caching and Memoization** — Covers when to cache tool results to avoid redundant calls, and the invalidation logic that makes caching safe rather than dangerous. Worth deepening because the failure modes of stale cached results in an agentic loop are subtle — the agent reasons confidently on data that is no longer true — and the right caching policy depends on the tool's semantics.

---