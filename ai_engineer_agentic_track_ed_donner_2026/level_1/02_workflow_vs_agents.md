## Metadata
- **Date:** 05-06-2026
- **Source:** 02_workflow_vs_agents.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-02 · Workflows vs. Agents (Control vs. Autonomy)

The instinct, once you've seen an agent loop work, is to reach for it every time. A model that decides its own next step feels like the obvious upgrade from a model that just answers questions. But most of the production systems being labelled "agentic" today shouldn't be agents at all. They're workflows in costume — fixed sequences of LLM calls dressed up with a reasoning loop they don't need, paying the autonomy tax for capabilities they never use.

The distinction worth internalising is this: a workflow is a sequence you already know. An agent is a sequence you don't. If you can sit down and draw the steps from input to output on a whiteboard — fetch the document, summarise it, classify the summary, write to the database — you have a workflow. The path is fixed. The LLM might be doing the heavy lifting at each step, but your code is deciding what step comes next. Control lives with you. If you cannot draw that diagram because the steps depend on what the model discovers along the way — maybe it needs to search, maybe it needs to calculate, maybe it needs to ask a clarifying question, and the right answer depends on what it finds — then you have an agent. The path is discovered at runtime. Control lives with the model.

This is an engineering decision, not a framework choice. No library makes it for you. LangChain will happily let you build either. The decision comes from looking at the task and asking honestly whether the sequence is knowable in advance. Most teams overestimate how much dynamism their problem requires, because dynamism feels more impressive and the demos are more exciting. But predictability is a feature, not a limitation, and most business tasks have far more structure than they appear to.

The cost asymmetry is what makes getting this wrong expensive. A workflow has bounded cost: N steps, each with a roughly known token count, total latency that's the sum of its parts. You can put it on a dashboard and forecast its monthly bill. An agent has unbounded cost: it loops until it decides to stop, and "decides to stop" is a property of the model's reasoning, not your control flow. An agent that gets confused can loop fifty times calling the same tool with slightly different arguments before exhausting its iteration budget. That's fifty model calls you didn't plan for. Workflows fail by producing wrong outputs; agents fail by producing wrong outputs after burning through your API credits.

The middle ground is where most real systems end up: hybrid patterns where the overall structure is fixed but specific steps are agentic. You know the high-level path — ingest, analyse, decide, act — but within "analyse" the model gets to choose which tools to call based on what it finds. This gives you the predictability of a workflow at the architectural level and the flexibility of an agent at the leaf level. Your error handling, your testing, your cost forecasting all operate against the fixed structure. The dynamic parts are scoped, bounded, and can be reasoned about in isolation. This is usually the right answer when you catch yourself thinking "I want an agent but I'm worried about it going off the rails."

The choice cascades through everything else you build. Error handling for a workflow is conventional — retry this step, fall back to that one, surface the failure. Error handling for an agent has to consider loop detection, stuck states, and tool-selection drift. Testing a workflow is deterministic enough to write proper unit tests against; testing an agent means evaluating outcomes against fuzzy success criteria across many runs, because the same input genuinely can produce different paths. Model requirements diverge too — workflows can often use cheaper models per step because each step is narrow, while agents typically need a frontier model for the planning loop or they hallucinate tool calls and get stuck. Even your observability needs change: workflow tracing is linear, agent tracing is a tree of decisions you have to reconstruct after the fact.

The practical heuristic: start with the simplest thing that could work, and let the task push you toward more autonomy only when it actually demands it. If you can write the steps as a script, write them as a script. If you find yourself writing if-statements that try to predict what the model will need next, that's the signal — your code is trying to do the model's job. Hand it back. But until that signal arrives, the workflow is cheaper, more reliable, easier to debug, and easier to explain to whoever has to maintain it after you. The most senior move in agentic engineering is often deciding not to build an agent.

## Level 2 candidates

**Prompt Chaining and Linear Workflows** — Covers how to design sequential LLM pipelines where each step's output becomes the next step's input, including how to validate intermediate results. Worth a deep dive because most production "AI features" are really chained workflows, and the engineering patterns for making them robust (validation between steps, retry boundaries, partial-result handling) are distinct from agent design.

**Dynamic Agent Loops** — Covers the mechanics of giving the model genuine control over the next step, including how state accumulates across iterations and how tool selection actually works in practice. Worth deeper exploration because the failure modes here (drift, looping, premature termination) are subtle and require dedicated patterns to mitigate.

**Hybrid Patterns: Multi-Step Reasoning with Tool Use** — Covers the middle-ground architectures where fixed structure contains agentic sub-steps, including how to scope autonomy to specific nodes. This is where most real production systems live, and the design choices (where to draw the boundary between fixed and dynamic) are a topic in themselves.

**Risk Tolerance and Cost Implications** — Covers how to forecast and bound the cost of agentic systems, including iteration limits, token budgets, and circuit breakers. Worth its own treatment because cost behaviour is the single biggest difference between workflows and agents in production, and "unbounded" is not a posture you can take to a finance team.

**Testing and Evaluation for Each Pattern** — Covers the divergent testing strategies: deterministic unit tests for workflows versus outcome-based eval suites for agents. Worth deeper exploration because the testing methodology you choose constrains how much you can trust the system, and most teams underinvest here until something breaks in production.

---