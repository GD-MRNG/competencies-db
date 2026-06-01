# AI Engineer Agentic Track: The Complete Agent & MCP Course — Level 0: Course Map

> **Intent:** To go from understanding LLMs as API endpoints to building, deploying, and reasoning about multi-agent systems — systems where autonomous processes plan, use tools, hand off to each other, and run without human intervention on each step. This is the difference between building products that call AI and building products that *are* AI.
>
> **Your angle:** You're not here to learn what an agent is — you've seen Claude Code, you've used Cursor, you have the intuition. You're here to build the engineering discipline: to understand *why* agent loops work the way they do, which framework to reach for when, and what the tradeoffs actually are beneath the abstractions. Come in at the reasoning layer, not the tutorial layer.

---

## How to use this map

**Level 1 topics** are the navigational units — each one is a concept cluster substantial enough to deserve a focused session. Read the description before going in; it tells you what the session will reveal and what it unlocks in adjacent topics.

**Level 2 candidates** are the sub-concepts inside each L1. They're listed as directions, not definitions. Before drilling into one, ask: is this the gap that's blocking me? If yes, go deep. If not, move on and come back.

Descend when you hit friction — when reading or building something produces a question you can't answer. The map is for orientation, not for linear completion.

---

## Topic Inventory

### Group 1: Foundations — What Agents Actually Are

#### L1-01 · The Agent Loop

The simplest possible definition of an agent is an LLM called in a while loop with tools. That's not reductive — it's clarifying. Everything else in this course is scaffolding around that loop: making it more reliable, more composable, more observable, and more autonomous. Understanding the loop from first principles — calling OpenAI directly, parsing tool call responses, routing to Python functions, feeding results back into the next message — gives you the mental model that every framework is abstracting over. If you've seen Claude Code's to-do tracking behavior and thought it was magic, building this once yourself removes the mystique permanently.

**Level 2 candidates:**
- **Tool call mechanics (JSON schema)** — Understanding why tools are described as JSON schemas, not function signatures, reveals the full protocol between model and caller and explains why tool definitions are the primary lever for agent behavior.
- **The finish_reason / tool_call dispatch pattern** — The branching logic that determines whether an LLM response triggers a function call or terminates the loop is the structural core of every agent; getting this wrong silently produces broken agents.
- **The role of system prompts in agent behavior** — System prompts do more work in agentic contexts than in chat; understanding what belongs there versus in the tool description versus in the user message shapes whether the agent stays on task.
- **To-do / planning state as a tool** — Using an in-memory task list as a tool is the simplest implementation of agent planning; it illustrates why tool use improves outcomes beyond just adding capabilities.
- **Reasoning effort and model selection** — Newer reasoning models behave differently under tool use than standard models; the tradeoffs between reasoning tokens and speed define where these models are and aren't appropriate in a loop.

---

#### L1-02 · Agentic Design Patterns

Before frameworks impose their opinions, there's a vocabulary of patterns that recur across every framework and every production agent system. These patterns — orchestrator/subagent, evaluator/optimizer, handoff, parallelism — are the design grammar. A practitioner who knows the patterns can read any framework's documentation and immediately map it onto something familiar. The patterns also tell you what's missing from any given framework and when to reach outside it.

**Level 2 candidates:**
- **Orchestrator / subagent split** — Separating the agent that decides what to do from the agents that do it is the architectural decision that determines how a system scales and how failures are contained.
- **Evaluator-optimizer loop** — Having a second agent check the output of the first before passing it downstream is the cheapest form of quality control in agentic systems and explains why human review alone doesn't scale.
- **Parallelism via async** — Understanding that parallel agent calls are just concurrent coroutines waiting on I/O is the mental model that turns "20 web searches at once" from magic into a simple scheduling problem.
- **Handoffs vs. tool calls** — The distinction between an agent calling a function and an agent handing control to another agent is where framework philosophies diverge most sharply.
- **Human-in-the-loop checkpoints** — Designing where humans can interrupt, redirect, or confirm is a first-class architectural concern, not an afterthought; LangGraph's checkpointing model makes this concrete.

---

### Group 2: Frameworks — Four Ways to Orchestrate

#### L1-03 · OpenAI Agents SDK

Released in early 2025 as the successor to Swarm, the OpenAI Agents SDK is the lightest of the four frameworks covered and the instructor's clear preference. It takes the agent loop from L1-01 and formalizes exactly two things: agents (an LLM + instructions + tools) and handoffs (one agent transferring control to another). Everything else remains in plain Python. The lightness is the point: you can see what's happening at every step, the abstractions don't leak, and the async-first design makes multi-agent parallelism natural. The deep research project built here — parallel web search agents feeding a writer agent, with a Gradio UI — is the clearest illustration in the course of what SDK-native multi-agent design looks like.

**Level 2 candidates:**
- **Agent as a typed wrapper, not a class hierarchy** — The SDK's agent definition is intentionally thin; knowing what it does and does not do for you clarifies when you need to add your own scaffolding.
- **Handoffs as first-class primitives** — The handoff mechanism is the SDK's core differentiator from writing raw loops; understanding when to use it versus when to keep logic in a single agent is the key design decision.
- **Guardrails (input/output validation)** — The SDK's guardrail system lets you validate and transform at the edges of agent interaction; knowing its constraints (first input / last output only) shapes where validation logic can live.
- **Async IO and the event loop in agent context** — Concurrency in this framework is implemented with Python's asyncio; understanding coroutines at the level of "pause on I/O, resume on completion" is required to debug timing issues in multi-agent flows.
- **Tracing and observability** — Traces are the primary debugging surface in agentic systems; the SDK's built-in tracing, and when to supplement it with an external tool like LangSmith, defines your operational visibility.
- **Deploying via Gradio and Hugging Face Spaces** — Turning an agent pipeline into a shareable web app is a one-command operation with Gradio; this unlocks the ability to ship and share agentic prototypes without infrastructure work.

---

#### L1-04 · CrewAI

CrewAI adds a layer of opinion on top of the agent loop that the OpenAI SDK deliberately avoids: named roles, backstories, explicit task objects, and two process modes (sequential vs. hierarchical). The metaphor is a team of professionals, each with a specialty. This makes it more expressive for business-domain problems where role-clarity matters, and more readable for non-engineers reviewing agent configurations. The cost is reduced transparency — more happens in the framework, less is visible in your code. The software engineering team project (engineering lead, developer, test writer, frontend) is the clearest case in the course where the role metaphor pays off in code legibility.

**Level 2 candidates:**
- **Agent vs. Task as separate constructs** — CrewAI's separation of "who does the work" (agent) from "what work is done" (task) is a meaningful design choice; understanding it reveals why the framework is more opinionated than the SDK and what that costs you in flexibility.
- **Sequential vs. hierarchical process modes** — The choice of process mode is the primary architectural lever in CrewAI; hierarchical mode introduces a manager LLM whose quality directly determines team performance.
- **Structured outputs for inter-agent communication** — Using Pydantic models to define what one agent passes to the next is the pattern that makes CrewAI's pipelines type-safe and debuggable.
- **Crews vs. Flows** — Flows are CrewAI's more deterministic workflow mode; understanding the crews/flows boundary maps onto the broader agent vs. pipeline design decision that applies across all frameworks.
- **Dynamic task creation via callbacks** — Creating task objects at runtime, based on the output of a preceding task, is how you build systems where the scope of work isn't known at code-write time.
- **CrewAI Enterprise vs. open-source framework** — The monetization architecture of the platform shapes its documentation, defaults, and upgrade pressure; knowing where the free tier ends helps you navigate the upselling.

---

#### L1-05 · LangGraph

LangGraph is the heavyweight in the course — not in complexity of learning, but in the depth of what it solves. Where the SDK and CrewAI treat agents as the atomic unit, LangGraph treats the *workflow* as the atomic unit, modeled as a directed graph of nodes. This makes it the right tool when you need persistence across sessions (checkpointing), human-in-the-loop interrupts, time-travel debugging, or fine-grained control over state transitions. The trade-off is explicitness: you define the graph structure, state schema, and transition logic yourself. The sidekick personal assistant built in this week — with persistent memory, tool dispatch, push notifications, and file-writing — is the example where LangGraph's checkpointing visibly pays off.

**Level 2 candidates:**
- **State schema and the StateGraph object** — The graph's state is a typed dictionary that flows through nodes; designing this schema is the first and most consequential decision when starting a LangGraph project.
- **Nodes, edges, and conditional routing** — The difference between a fixed edge (always goes to B after A) and a conditional edge (decides at runtime) is how you implement agent autonomy within the graph model.
- **Checkpointing and persistence** — LangGraph's checkpointing is what lets an agent resume mid-task after a failure, support human review at a defined point, or maintain conversation history across sessions; this is its primary advantage over lighter frameworks.
- **LangChain vs. LangGraph vs. LangSmith** — The three products serve different layers (glue code, workflow graph, monitoring); confusing them leads to choosing the wrong tool and reading the wrong documentation.
- **Human-in-the-loop interrupt patterns** — The ability to pause a graph at a node and wait for human input is LangGraph's answer to the auditability concerns that keep agentic systems out of production; understanding the implementation details determines whether it's usable in your context.
- **SQLite memory vs. in-memory checkpointing** — The choice of persistence backend determines whether agent memory survives restarts; the difference between conversation-scoped and user-scoped memory shapes multi-user deployments.

---

#### L1-06 · AutoGen

AutoGen (Microsoft, v0.4+) takes a different philosophical bet from the other three: it separates the *runtime fabric* for agents (AutoGen Core) from the *high-level agent abstractions* (AutoGen AgentChat). Core is an event-driven, actor-model runtime that can coordinate agents distributed across processes or machines — closer in spirit to an agent operating system than to a framework. AgentChat, sitting on top of Core, is a lightweight SDK-alike that will feel immediately familiar after the earlier frameworks. The week's project — an agent that creates other agents at runtime, each with unique personas, who then converse and generate ideas — is the course's most experimental and forward-looking example.

**Level 2 candidates:**
- **AutoGen Core vs. AgentChat** — The two layers serve different audiences and solve different problems; using AgentChat for familiar patterns and Core when you need distributed or heterogeneous agent communication is the key architectural split.
- **Event-driven vs. request/response messaging** — Core's actor model uses async message passing rather than function calls; understanding why this enables distribution and heterogeneity (and what it costs in simplicity) is the conceptual leap this framework requires.
- **The Microsoft / AG2 fork situation** — A significant portion of the AutoGen community is using AG2 (the forked version from the original creators), which controls the PyPI package name; understanding the split prevents documentation confusion and incorrect installs.
- **Runtime agent creation** — The ability to instantiate agents dynamically at runtime — where one agent defines and spawns others — is AutoGen Core's most distinctive capability and the design pattern the week's project explores.
- **Observability in a distributed agent system** — When agents run across threads or processes, tracing what happened and why becomes significantly harder; AutoGen's approach to this is one of its stated design goals.

---

### Group 3: Protocol & Production — MCP and the Ecosystem Layer

#### L1-07 · Model Context Protocol (MCP)

Anthropic released MCP in late 2024 and it achieved widespread adoption by early 2025. It is not a framework — it's a protocol: a standard for how agent applications connect to externally developed tools, resources, and prompts. The USB-C analogy is apt: MCP's value is almost entirely in its adoption rather than its technical novelty. Before MCP, every agent tool integration was bespoke. With MCP, any tool built to the standard can be dropped into any MCP-compatible host (Claude Desktop, the OpenAI Agents SDK, others) without custom integration work. Understanding MCP means understanding: what the host/client/server architecture looks like, how tool discovery works over the wire, and what the thousands of community-built MCP servers give you out of the box.

**Level 2 candidates:**
- **Host / client / server architecture** — The three-layer model (host application → MCP client → MCP server) is the core mental model; confusing which layer you're building or consuming from leads to design mistakes.
- **Transport layer: stdio vs. SSE** — The two transport modes determine whether a server runs as a local process or a remote service; this choice defines the deployment model and security surface of any MCP integration.
- **Tool discovery and schema negotiation** — When a client connects to a server, it requests the list of available tools and their schemas; understanding this handshake explains how an agent knows what it can do without hard-coded tool definitions.
- **Building a custom MCP server** — Writing an MCP server from scratch — exposing your own functions as tools — is how you add proprietary capabilities to any MCP-compatible agent without modifying the agent code itself.
- **The MCP tool ecosystem** — Thousands of community-built servers exist for databases, APIs, file systems, calendars, financial data, and more; knowing how to evaluate and integrate these is the practical payoff of the protocol.
- **MCP vs. native tool decorators** — Understanding when to package something as an MCP server versus a local tool (decorator-based, SDK-native) defines your default architecture for new integrations going forward.

---

#### L1-08 · Production Patterns and Framework Selection

This is the synthesizing layer — the set of considerations that don't belong to any single framework but determine whether an agentic system actually ships. By this point in the course, you've built projects in four frameworks and wired them together with MCP. The question is no longer "how do I build this?" but "what should I actually build this with, and how do I make it work reliably in production?" The course closes with explicit framework comparison, advice on agent system design from a practitioner perspective, and the capstone equity trading floor project — a multi-agent, multi-MCP-server system with 40+ tools.

**Level 2 candidates:**
- **Framework selection heuristics** — The choice between SDK, CrewAI, LangGraph, and AutoGen is driven by: how much control you need over state, how much observability matters, whether your workflow is dynamic or deterministic, and what your team's Python fluency is.
- **Prompt engineering inside agents** — System prompts in agentic contexts need to handle tool use guidance, persona maintenance, and failure recovery simultaneously; the craft of writing these is different from chat prompt engineering.
- **Structured outputs for reliability** — Using Pydantic or JSON schema output constraints at inter-agent boundaries is the primary mechanism for making agent pipelines more deterministic and debuggable.
- **Avoiding LLM monoculture** — Using different models for different tasks within a multi-agent system (a fast cheap model for routing, a powerful model for synthesis) is a cost and latency optimization that also improves robustness.
- **Experimentation over intuition** — Agentic system behavior is hard to predict from first principles; the practitioner habit of running experiments rather than reasoning from intuition is the meta-skill the course tries to build.

---

## Sequencing note

The dependency chain here is tight through the first two groups. L1-01 (The Agent Loop) is not optional — it's the bedrock that makes every framework comprehensible rather than magical. Build the loop from scratch at least once before touching any framework. L1-02 (Design Patterns) can be read in parallel with L1-01; it gives you the vocabulary to describe what you're building.

Among the frameworks (L1-03 through L1-06), the recommended order is the course order: OpenAI Agents SDK first (lightest, most transparent), then CrewAI (adds role structure), then LangGraph (adds graph-based state and persistence), then AutoGen (adds distribution and runtime agent creation). This order is a learning gradient from explicit to abstract, and the differences between each framework are clearest when you've just come from the prior one. You don't need to deeply master one before starting the next — a week-long project in each is enough to form a genuine opinion.

The highest-leverage entry points for someone returning to foundations with existing experience are: the agent loop build-from-scratch exercise (L1-01), then the LangGraph checkpointing model (L1-05), then MCP architecture (L1-07). These three together give you the primitives, the production-grade state model, and the ecosystem integration story — enough to architect a real system from scratch and defend the design decisions.

## Source

https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/