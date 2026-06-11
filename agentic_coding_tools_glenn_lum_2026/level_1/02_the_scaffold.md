## Metadata
- **Date:** 11-06-2026
- **Source:** 02_the_scaffold.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-02 · The Scaffold

When people argue about which coding agent is best, they almost always argue about the model. Claude versus GPT versus Gemini, this benchmark score against that one, the new release that supposedly changes everything. This framing is wrong in a specific and load-bearing way: the model is a component, not the product. The product is the scaffold around it — the control loop that decides when to call the model, the tool interface that lets it act, the memory strategy that decides what it remembers, and the error handling that decides what happens when something goes wrong. Swap the scaffold and keep the model, and you get a different agent. Swap the model and keep the scaffold, and you often get something surprisingly similar.

This matters because it inverts the usual story about why one agent outperforms another. Two teams can wire the same frontier model into their products and ship tools that feel nothing alike — one that completes a refactor cleanly across twelve files, another that loses track of what it was doing after the third tool call. The difference isn't intelligence. It's engineering: how the loop is structured, how tools are described, how context is pruned when it overflows, how failures are surfaced back into the next iteration. The scaffold is where almost all the practical decisions live, and it is where almost all the practical failures originate.

The first piece of the scaffold is the control loop itself — the code that orchestrates the perception–planning–execution cycle. This includes when the model is invoked, how its output is parsed, how tool calls are dispatched, and crucially, how the loop terminates. A loop that stops too early truncates work confidently; a loop that doesn't stop spirals into expensive retry behaviour. None of this is the model's decision. It is the scaffold's.

The second piece is the agent–computer interface: the set of tools the agent can call and the schemas that describe them. This is not plumbing. The names you give tools, the parameters you expose, the descriptions you write, the way overlapping capabilities are disambiguated — all of this shapes what the model will attempt and how often it will hallucinate calls that don't exist. A poorly designed tool surface produces phantom function calls and malformed arguments from the same model that, given a cleaner interface, would behave reliably. Tool schema design is where a surprising amount of agent quality is won or lost, and it is invisible from the outside.

The third piece is context management. Every agent eventually outgrows its context window on a non-trivial task, and what happens at that boundary is a scaffold decision. Some scaffolds summarise aggressively, some prune the oldest turns, some maintain structured external memory and re-inject relevant slices. Each strategy has a failure mode — silent loss of a critical earlier instruction, summaries that paper over a contradiction, retrieval that surfaces stale information as if it were current. The agent's behaviour over a long session is largely a function of which compaction strategy you've chosen, even though users almost never see the choice being made.

The fourth piece is error handling: what the scaffold does when a tool call fails, when the model produces unparseable output, when a test exits non-zero, when a network call times out. Whether these errors are surfaced back into the loop as structured feedback, swallowed silently, or escalated to the user determines whether the agent can self-correct or whether it confabulates around the problem. This is where the feedback environment from the previous topic actually gets wired in — the verifiability of code only helps if the scaffold is built to channel that signal back into the next iteration.

The practical consequence is that benchmark scores and marketing comparisons confound model and scaffold in a way that makes them nearly useless for decision-making. When SWE-bench Verified reports a number for "Claude" or "GPT," it is reporting a number for a specific scaffold wrapping that model, evaluated on a specific harness. Change the scaffold and the score changes. Vendors know this; published numbers are produced by teams that have spent significant engineering effort tuning the scaffold around the model under test. The number tells you what is achievable with that pairing under ideal harnessing — not what you will get when you drop the same model into a different product.

The skill this builds is attribution. When an agent fails, the useful question is not "is the model bad?" but "which part of the scaffold did this fail in?" Was the tool description ambiguous? Did the loop terminate prematurely? Did context compaction discard the instruction the agent needed? Did an error get swallowed instead of surfaced? Once you can locate the failure in a specific scaffold component, you can act — change the configuration, write a better instruction file, restructure the tools, choose a different product. Until you can, every failure looks like a mysterious model deficiency, and the only available response is to wait for a better model. The scaffold is where your leverage actually lives.

## Level 2 candidates

**Agent–computer interface (ACI) design** — Covers how tool names, schemas, descriptions, and parameter shapes determine what the agent attempts and how often it misuses or hallucinates tools. Worth depth because ACI design is one of the highest-leverage and least-understood scaffold surfaces, and the principles transfer across every product you'll evaluate or build.

**Context compaction strategies** — Covers the concrete approaches scaffolds use to handle context overflow: summarisation, pruning, structured external memory, retrieval re-injection, and the specific failure modes each produces. Worth depth because compaction is invisible by default and silently shapes long-session behaviour, and recognising which strategy a tool uses lets you predict where it will degrade.

**Control loop and termination design** — Covers the engineering of the loop itself — when the model is invoked, how output is parsed and dispatched, and how termination conditions are calibrated. Worth depth because miscalibrated termination is a leading cause of both confident truncation and expensive retry spirals, and the design space is richer than "loop until done."

**Scaffold–model attribution in benchmarks** — Covers how to read published evaluation scores critically, separating model contribution from scaffold contribution, and how to construct evaluations that isolate the variable you actually care about. Worth depth because benchmark literacy is a prerequisite for making adoption decisions that don't rest on vendor framing.

**Error surfacing and feedback wiring** — Covers how scaffolds route tool failures, parse errors, and external signals back into the loop, and why the choice between swallowing, surfacing, and escalating determines whether self-correction works. Worth depth because this is where the feedback environment concept becomes concrete engineering, and where many "the agent gave up" failures actually originate.

---