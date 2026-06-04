## Metadata
- **Date:** 05-06-2026
- **Source:** 13_multi_agent_architecture_and_decomposition.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-13 · Multi-Agent Architecture and Decomposition

The instinct, when a single agent starts struggling, is to give it more: a longer system prompt, more tools, a bigger context window, a smarter model. This instinct is almost always wrong. Past a certain complexity threshold, adding capability to a single agent makes it worse, not better — the prompt becomes a sprawling document of conflicting instructions, the tool list confuses the model into picking the wrong one, and the context fills with irrelevant history that degrades reasoning. The right move at that threshold is not to scale the agent up, but to break it apart.

Decomposition is the practice of splitting a complex problem into a small team of specialized agents, each with a narrow job. The canonical shape is a Planner that decides what needs to happen, Workers that execute specific tasks, and a Judge that checks the output before it ships. None of these agents knows or cares about the others' internals. The Planner doesn't write code; it writes a plan. The Workers don't decide strategy; they execute. The Judge doesn't do the work; it evaluates whether the work is acceptable. Each agent gets a focused system prompt and a deliberately small set of tools — and that focus is the entire point.

The reason this works comes down to how language models behave under cognitive load. A model given one job and four tools makes better decisions than the same model given six jobs and twenty tools. When you remove options, you remove ways for the model to be wrong. A Worker whose system prompt says "you extract structured invoice data from PDFs and return JSON in this schema" cannot wander off and try to summarize the document instead, because it has no tool for summarizing and no instruction to do so. Constraint is a reliability mechanism. Decomposition is how you apply constraint at the architectural level rather than fighting for it inside a single prompt.

This unlocks two practical capabilities that single-agent systems struggle to provide. The first is separation of concerns: you can test, evaluate, and improve each agent independently. If your end-to-end accuracy drops, you can run the regression suite against each agent in isolation and identify which one regressed. Compare that to debugging a monolithic agent, where the only thing you can measure is whether the final output is good or bad, with no visibility into where the reasoning went sideways. The second is parallel execution: if your Planner produces five independent subtasks, five Workers can run concurrently, and your wall-clock latency drops to roughly one Worker's runtime instead of five. A single agent reasoning sequentially cannot do this, no matter how clever the prompt.

The cost of this architecture is, predictably, cost. You are now making N model calls instead of one, and often the Planner and Judge calls use a more expensive model than the Workers. A task that cost you one API call now costs five or ten, and your latency floor is the slowest agent in the critical path. You also inherit a new class of bugs that don't exist in single-agent systems: agents disagreeing about shared state, the Planner producing a plan that no Worker can actually execute, the Judge rejecting outputs in an infinite loop. Multi-agent systems are not free reliability — they are a trade where you pay in complexity and dollars to buy back consistency and scalability.

This is why decomposition is a tool you reach for when you need it, not a default. A single agent loop is the right starting point for almost any new system. You decompose when a specific symptom appears: the system prompt has grown into a multi-page document the model can no longer follow, the tool list has crossed the threshold where the model picks wrong, the task genuinely contains independent subproblems that could run in parallel, or you need to evaluate parts of the pipeline separately because end-to-end accuracy is too coarse a signal to debug. Absent one of these forcing functions, decomposition adds cost and latency without buying you anything.

When you do decompose, the architectural choices that follow matter. Hierarchical designs (a Planner directing Workers) are easier to reason about and debug, but they bottleneck on the Planner's quality. Flat, peer-to-peer designs distribute decision-making but introduce coordination overhead and are notoriously hard to make reliable in production. State management — how agents share what they've learned without stepping on each other — becomes a first-class problem. And because each agent is making its own model calls, observability stops being a nice-to-have and becomes the only way you can understand what your system is actually doing.

The skill this topic builds is recognizing the threshold at which a single agent stops being the right answer, and having the vocabulary and patterns to design the team that replaces it. Most production AI systems that work well at scale are not heroic single agents — they are small, well-coordinated teams of narrow agents, each doing one thing reliably, with the seams between them carefully engineered. Build that intuition, and you stop trying to make one agent do everything. Start trying to make several agents each do one thing perfectly.

## Level 2 candidates

**Hierarchical vs. flat architectures** — Covers the choice between a Planner-directed hierarchy and peer-to-peer agent coordination, and the trade-offs in latency, reliability, and reasoning quality. Worth deeper treatment because the choice has long-term consequences for debuggability and scaling, and the failure modes of flat architectures (deadlocks, coordination thrash) are subtle enough that they deserve their own walkthrough.

**System prompt specialization** — The craft of writing narrow, focused system prompts for each agent in a decomposed system, and how reducing context noise improves accuracy. Worth depth because the discipline of writing a *small* prompt — and resisting the temptation to add "just one more instruction" — is counterintuitive and benefits from worked examples.

**Independent evaluation and metrics** — How to measure each agent's accuracy in isolation, identify the bottleneck agent, and build regression tests at the component level rather than only end-to-end. Worth depth because evaluation in multi-agent systems is materially different from evaluating a single model call, and getting it right is what makes the architecture maintainable.

**Parallel execution and synchronization** — Running Workers concurrently with async patterns, gathering results, and handling partial failures gracefully. Worth depth because the implementation details (timeouts, partial result handling, what to do when one Worker fails and four succeed) are where naive parallelization breaks in production.

**State management across agents** — Maintaining a shared world state — conversation history, extracted data, intermediate results — so agents don't conflict or duplicate work. Worth depth because this is the most common source of subtle bugs in multi-agent systems and the patterns (shared blackboard, message passing, immutable state snapshots) have meaningful trade-offs.

**Judge agents and output validation** — Designing the validator agent that checks Worker outputs before they ship, including how to avoid the infinite-loop failure mode where the Judge keeps rejecting and the Workers keep retrying. Worth depth because Judge design is its own craft and the difference between a useful Judge and a broken one is mostly about prompt design and stopping criteria.

---