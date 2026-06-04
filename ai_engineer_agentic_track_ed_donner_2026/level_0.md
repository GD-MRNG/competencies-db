# AI Engineer Agentic Track — Level 0: Course Map

> **Intent:** Build autonomous systems that reason dynamically, choose tools, observe outcomes, and iterate toward goals without hard-coded workflows or human intervention between steps.
>
> **Your angle:** You've mastered basic model calling and prompting. Now you're learning the next level: how to architect systems where the model becomes the decision-maker, not the oracle. You'll understand the loop (Thought-Action-Observation), the tradeoffs between control and autonomy, and how to scale from a single agent to teams of specialized reasoning engines. You're building the "brain" that delegates work.

---

## How to Use This Map

This map is organized into three layers, reflecting the progression from **simple reasoning loops** to **complex multi-agent orchestration** to **standardized tool ecosystems**.

**Level 1 topics** are conceptual anchors—each one represents a capability you can unlock. Start with a topic that solves an immediate problem: "I need this system to choose its own tools" or "My agents keep getting stuck in loops."

**Level 2 candidates** are the sub-concepts within each topic. Use them to identify what you need to understand next: if a description resonates with your current blocker, descend into it.

The **Sequencing note** at the end identifies dependencies and offers entry points based on your current project stage.

---

## Topic Inventory

### **Foundations: From Static to Dynamic**

#### L1-01 · The Agentic Loop (Thought-Action-Observation)

The core pattern that transforms a model from a one-shot oracle into a reasoning engine is the **Control Loop**. The model thinks (evaluates the goal and context), selects an action (a tool to call), and you observe the result, then loop back. This is simple in concept—a `while` loop—but profound in implication: the model now determines the next step, not you. This is the threshold between chatbots (static, request-response) and agents (dynamic, goal-seeking). Mastering this loop in raw Python before moving to frameworks is the single most durable skill in agentic AI.

**Level 2 candidates:**

- **The Thought Step: Planning and Tool Selection** — How the model evaluates the current state (goal + context) and decides which tool to invoke; why good System Messages and schemas determine whether the model makes smart choices or hallucinates.
- **The Action Step: Tool Calling and JSON Generation** — The model generates structured requests (tool name + arguments as JSON); understanding that the model is just generating text that looks like a function call.
- **The Observation Step: Tool Execution and Context Reconstruction** — You execute the tool locally, capture the result, and append it to the message history; this is how the agent "sees" the outcome and adapts the next thought.
- **Loop Termination and Stop Conditions** — Knowing when the agent is done (it chooses not to call a tool, or explicit termination criteria). Preventing infinite loops through token budgets, iteration limits, or explicit success/failure detection.
- **The Role of the System Message in Agentic Contexts** — How the System Message primes the model to think like an agent; being explicit about available tools and the goal structure.

---

#### L1-02 · Workflows vs. Agents (Control vs. Autonomy)

Not every task needs an agent loop. Some are predictable sequences (workflows) with fixed paths; others are discovery-based and require dynamic reasoning (agents). Understanding this distinction is an engineering decision, not a framework choice. A workflow is cheap and predictable; an agent is flexible but risky (loops, hallucinations, costs). The choice cascades through your architecture: error handling, model requirements, testing strategy.

**Level 2 candidates:**

- **Prompt Chaining and Linear Workflows** — Sequential steps where each step's output is the next step's input; no branching or tool selection. When you know the path in advance, workflows save tokens and cost.
- **Dynamic Agent Loops** — The agent decides the next step based on current state; multiple possible paths. When you don't know the sequence, agents handle discovery at the cost of unpredictability.
- **Hybrid Patterns: Multi-Step Reasoning with Tool Use** — Combining fixed structure (steps A → B → C) with dynamic tool selection within each step; a middle ground between workflows and pure agents.
- **Risk Tolerance and Cost Implications** — Workflows have bounded cost and predictable latency; agents are unbounded and can drift. How to decide based on task criticality and budget.
- **Testing and Evaluation for Each Pattern** — Workflows can be tested with deterministic cases; agents require fuzzier metrics (does the outcome satisfy the goal?) and more extensive edge-case testing.

---

#### L1-03 · Model Reasoning and the Cost-Capability Trade-off

Different models have different "reasoning effort"—the ability to think through multi-step problems and select the right tools from a list. A frontier model can handle complex tool selection and self-correction; a small model (3B parameters) might hallucinate tool calls or fail to follow schemas. The cost per token scales accordingly. For agentic systems, "cheap" often means "broken"—small models frequently choose the wrong tool, misunderstand schemas, or get stuck. This is a different constraint than for single-shot generation. Which specific models qualify as "frontier" for agentic tasks shifts with every release cycle; check current benchmarks rather than treating any named model as a fixed reference point.

**Level 2 candidates:**

- **Reasoning Complexity and Model Selection** — How to assess whether a task requires a frontier model or whether a small model suffices; the relationship between task complexity, context length, and model capability.
- **Tool Selection Reliability** — Why frontier models are more reliable at picking the right tool from a list; how small models hallucinate or misinterpret schemas; measuring accuracy of tool selection independent of execution.
- **Self-Correction and Recovery** — Whether the model can recognize a bad tool result and adjust; some models are better at "this didn't work, let me try a different approach" than others.
- **Scaling Reasoning via Multi-Turn Interaction** — Using cheaper models for specific, narrow tasks (workers) while using frontier models for planning (planner); distributing reasoning across multiple agents.
- **Token Budgets and Cost Control** — Setting iteration limits, token budgets, or explicit exit conditions on agentic loops; preventing runaway costs when agents get stuck or explore fruitlessly.

---

### **Orchestration: Building Multi-Agent Systems**

#### L1-04 · Asynchronous Execution and Concurrency Patterns

Real-world agents make multiple high-latency calls (to APIs, databases, or other models). If you wait for each call to complete sequentially, your system crawls. **Asynchronous execution** allows multiple tool calls to happen in parallel; you gather the results and feed them back to the reasoning engine. This is where system latency drops from "call 1, wait → call 2, wait → call 3, wait" to "call 1, 2, 3 in parallel, gather results, then proceed." The pattern is essential for production agentic systems but introduces complexity (managing concurrent state, handling partial failures).

**Level 2 candidates:**

- **Async/Await Patterns in Python** — Writing non-blocking code so multiple tool calls run simultaneously; understanding event loops and coroutines.
- **Parallel Tool Execution** — When the model requests multiple tools in one response, executing all of them concurrently instead of serially; reassembling results for the next reasoning step.
- **Handling Partial Failures and Timeouts** — What happens when one of three parallel tool calls fails? Implementing graceful degradation: retry logic, fallbacks, or reporting partial results.
- **Distributed Tracing and Observability** — Understanding which operations are blocking the system (critical path analysis); identifying bottlenecks in concurrent execution.
- **Queue-Based Orchestration** — Using message queues (Redis, RabbitMQ) to decouple tool execution from the reasoning loop; useful when tools are slow or agents are numerous.

---

#### L1-05 · Multi-Agent Teams and Specialized Reasoning

A single agent is limited by the model's breadth. A **team** of specialized agents is often more reliable: one agent plans using a capable frontier model, another executes calculations (possibly a cheaper or fine-tuned model), another verifies (possibly a different model entirely). Each agent has a narrow job, making it more reliable than a generalist. This requires **communication patterns** (how agents pass messages, coordinate state) and **orchestration logic** (which agent runs next, when to escalate to a human).

**Level 2 candidates:**

- **Agent Roles and Specialization** — Designing each agent to handle a specific task (Planner, Researcher, Reviewer, Executor); understanding the tradeoff between generalist (one big agent) and specialist (many small ones).
- **Message Passing Between Agents** — How agents communicate: shared state, queues, or event streams? Design decisions affect debugging difficulty and scalability.
- **Hierarchical and Flat Architectures** — In a hierarchy, a "Manager" agent decides which subordinate agents to call (Director pattern). In flat architectures, agents coordinate peer-to-peer or via a shared runtime.
- **Consensus and Conflict Resolution** — When multiple agents disagree on the answer (e.g., one estimates $10, another $15), how does the system decide? Voting, weighted ensemble, or escalation to a human.
- **State Management Across Agents** — Tracking what each agent has done, what the current "world state" is, and preventing agents from undoing each other's work; atomicity and idempotency.

---

#### L1-06 · Evaluator-Optimizer Patterns for Self-Correction

An agent can make mistakes: choosing the wrong tool, misinterpreting a result, or pursuing a dead-end. An **Evaluator** agent (or a second pass by the same model) examines the output and either approves it or flags it for revision. An **Optimizer** then fixes it. This pattern turns brittle single-pass reasoning into iterative, self-correcting systems. The cost is latency and tokens, but the reliability gain is often worth it for critical tasks.

**Level 2 candidates:**

- **Evaluation Criteria and Success Metrics** — Defining what "good" means for the agent's output; how specific and measurable the criteria are determines whether the evaluator can reliably judge.
- **The Evaluator-Optimizer Loop** — Evaluator checks output → Optimizer revises → Evaluator re-checks → repeat until approved. How many iterations before giving up (cost control)?
- **Confidence Scoring and Rejection Sampling** — The model outputs a confidence score with its answer; low confidence triggers re-generation or escalation; useful alternative to explicit evaluation.
- **Prompting for Self-Critique** — Asking the model "what could be wrong with this?" or "what edge cases did you miss?"; often cheaper than adding a separate evaluator.
- **Ensemble and Voting Patterns** — Running the same task multiple times (with different models or prompts) and selecting the best output; expensive but reliable for high-stakes decisions.

---

#### L1-07 · Agentic SDKs and Framework Abstractions

Once your agents are working in raw Python, frameworks (LangChain, CrewAI, Anthropic SDK) provide scaffolding: memory management, logging, retries, and multi-agent coordination. The cost is abstraction—it's easier to write but harder to debug when something breaks. The guidance: master the loop first, use frameworks pragmatically once you understand the underpinnings, but don't let framework-specific knowledge distract from the underlying patterns.

**Level 2 candidates:**

- **When to Use Frameworks vs. Raw API Calls** — Raw API gives full transparency but more boilerplate; frameworks hide details but move your code off the critical path. Tradeoffs depend on team expertise.
- **Memory and State Management in Frameworks** — How frameworks handle conversation history, intermediate results, and shared context between agents; understanding when built-in solutions are sufficient vs. when you need custom logic.
- **Tool Registry and Schema Auto-Generation** — Frameworks often auto-convert Python functions into tool schemas; understanding what gets lost in translation (e.g., nuanced descriptions).
- **Debugging and Tracing in Abstraction Layers** — When a framework agent goes wrong, how to instrument and trace execution; accessing logs and intermediate outputs.
- **Migration and Lock-In Risk** — Frameworks evolve rapidly; code written against one major version may break in the next. Designing for portability: clear abstractions between your logic and the framework.

---

### **Tool Ecosystems: The Connectivity Layer**

#### L1-08 · Tool Definition and Schema Enforcement

The model generates text that *looks* like a tool call, but the actual execution happens in your code. For the loop to work reliably, the model must generate valid schemas (JSON) that your code can parse and execute. **Pydantic** provides type-safe schemas; **Structured Outputs** (Constrained Decoding) force the model to respect the schema at generation time. Without this, "the agent calls a tool" means "the agent generates text, I parse it (probably failing), and the loop breaks."

**Level 2 candidates:**

- **Tool Signature Design** — Defining tool name, description, parameters, and return type; writing descriptions that guide the model to use the tool correctly without over-engineering.
- **Pydantic Schemas and Type Safety** — Defining the input and output types in Python; leveraging type hints so the tool call is validated before execution.
- **Constrained Decoding and Structured Outputs** — Mathematically forcing the model to respect a schema during generation; eliminating hallucinated or malformed tool calls.
- **Parameter Validation and Error Handling** — What happens when the model calls a tool with invalid arguments? Implementing validation that returns a clear error message to the agent, allowing recovery.
- **Tool Descriptions and Semantic Clarity** — How detailed should a tool description be? Too sparse, the model doesn't know when to use it; too verbose, the model gets confused. Iterating on clarity.

---

#### L1-09 · The Model Context Protocol (MCP) as a Standard Interface

**MCP** is a standardized protocol for agents to discover and use tools without custom integration code. Instead of writing a unique connector for each tool, the tool becomes an **MCP Server** that advertises its capabilities (Tools, Resources, Prompts) in a universal JSON format. An agent (the MCP Client or Host) connects to any server and uses its tools, regardless of language or implementation. This is the "USB-C of AI"—standardized plugs and sockets.

**Level 2 candidates:**

- **Client-Server-Host Architecture** — The Host (your agent/application), the Server (the tool provider), and the Client (the mediator). Understanding this separation unlocks tool reuse.
- **Transport Mechanisms: Stdio vs. SSE** — Stdio is local, fast, and secure (IPC); SSE is remote but introduces network latency and auth complexity. Choosing based on deployment model.
- **Tool vs. Resource vs. Prompt** — Tools are functions the agent can invoke; Resources are read-only knowledge bases; Prompts are pre-canned instructions. Understanding which to use for different scenarios.
- **MCP Server Creation and FastMCP** — Wrapping existing Python functions or APIs as MCP Servers; using FastMCP to reduce boilerplate.
- **Ecosystem Integration and Discovering Tools** — Using existing MCP Servers (e.g., from Smithery marketplace) without building custom integrations; evaluating third-party servers for security and reliability.

---

#### L1-10 · Tool Granularity and Composition

A single tool can be coarse-grained ("fetch any URL") or fine-grained ("click this button"). Coarse tools are more flexible (the agent composes them creatively) but give the agent freedom to make mistakes. Fine tools are restrictive but safer (the agent can't accidentally delete your entire database). The right granularity depends on the task, the model's reasoning ability, and your risk tolerance.

**Level 2 candidates:**

- **High-Level vs. Low-Level Tool Design** — "Fetch" (a high-level browser tool) vs. "click element by CSS selector" (low-level). When to abstract vs. when to expose details.
- **Tool Composition and Emergent Behavior** — Can the agent combine tools in ways you didn't anticipate? Is that a feature (flexible problem-solving) or a bug (unpredictable behavior)?
- **Safety and Guardrails** — Preventing the agent from using a tool in dangerous ways; implementing canaries, dry-run modes, or human approval for high-risk operations.
- **Tool Observability and Tracing** — Logging every tool call and result; essential for understanding why the agent made a choice and debugging failures.
- **Tool Caching and Memoization** — If the same tool is called with the same arguments repeatedly, cache the result; saves tokens and cost but requires careful invalidation logic.

---

### **Advanced Patterns and Production**

#### L1-11 · Graph-Based Workflows and LLM Routing

For complex systems, you may combine **graphs** (fixed structure, edges represent steps) with **agents** (dynamic choice). A graph defines the overall flow (fetch data → analyze → decide → act), and agents handle the dynamic parts (analyzing ambiguous data, deciding between options). This is more structured than pure agentic loops but more flexible than hard-coded workflows.

**Level 2 candidates:**

- **Graph Definition and Visualization** — Defining nodes (agents/steps) and edges (transitions); tools like Langgraph for structured agentic workflows.
- **Conditional Routing and Decision Points** — Where the agent (or a classifier) decides which branch to take; implementing decision logic that's transparent and testable.
- **Sub-Graphs and Hierarchical Composition** — Breaking large graphs into reusable sub-graphs; managing complexity through abstraction.
- **State Management in Graphs** — Tracking what data flows between nodes; ensuring state is consistent and preventing race conditions in parallel branches.

---

#### L1-12 · Human-in-the-Loop and Escalation Patterns

Not all decisions should be autonomous. For high-risk actions (financial transfers, deletions, policy decisions), an agent should **escalate** to a human for approval. Designing this requires clear **escalation criteria** (when to ask), **presentation** (how to show the agent's reasoning to a human), and **feedback loops** (how the human's decision gets back to the agent).

**Level 2 candidates:**

- **Approval Workflows** — Defining conditions that trigger human review; routing to the right person based on decision type or amount.
- **Reasoning Transparency** — Presenting the agent's thought process to the human (not just the final answer); building trust through interpretability.
- **Feedback Integration** — When a human approves/rejects a decision, how does that feedback help the agent learn? Real-time correction vs. batch retraining.
- **SLA and Latency for Escalation** — How long can an agent wait for human approval before timing out? Designing for different urgency levels.

---

#### L1-13 · Observability, Debugging, and Tracing Agentic Systems

Agentic systems are hard to debug: the agent took 50 steps, called 30 tools, and the final answer was wrong. Where did it go off track? **Tracing** captures every step of the loop; **structured logging** records decisions and reasoning; **dashboards** show agent behavior in aggregate. This is essential for both understanding what went wrong and identifying systematic issues (e.g., "agents always fail when asked about X").

**Level 2 candidates:**

- **Trace Capture and Export** — Recording the full Thought-Action-Observation loop; formats like JSON or Langsmith for visualization and analysis.
- **Structured Logging and Metrics** — Logging decisions with context (goal, available tools, model output); enabling analysis of failure patterns.
- **Latency Profiling and Bottleneck Detection** — Which step is slow? Is the model thinking time, or tool execution, or network? Identifying where to optimize.
- **Cost Attribution and Token Accounting** — Tracking which agents, tools, or features consume the most tokens; making optimization decisions based on data.
- **Alerting and Monitoring** — Detecting when agents go off track in production (e.g., infinite loops, high error rates); setting thresholds for intervention.

---

#### L1-14 · Agentic AI in Production: Reliability and Scaling

Moving agents from prototypes to production systems requires different thinking: **idempotency** (running the same tool twice should be safe), **atomic operations** (tool calls either fully complete or fully fail), **rate limiting** (preventing agents from overwhelming your infrastructure), **caching** (avoiding redundant computation), and **graceful degradation** (what happens when a tool is down?).

**Level 2 candidates:**

- **Idempotency and Atomic Operations** — Ensuring that if an agent is interrupted mid-execution, restarting it doesn't corrupt state; designing tools for safety.
- **Rate Limiting and Backpressure** — Preventing agents from hammering your APIs or databases; implementing queuing and throttling.
- **Distributed Execution and Load Balancing** — Running multiple agent instances; ensuring fair distribution of work and preventing hot spots.
- **Checkpointing and Recovery** — Saving agent state at intervals; recovering from failures without losing progress.
- **Cold Starts and Serverless Latency** — If agents run on serverless infrastructure, managing startup time; keeping warm with periodic heartbeats or pre-provisioned instances.

---

#### L1-15 · Prompt Engineering for Agentic Contexts

The System Message in an agent is more critical than in a one-shot prompt. The agent will loop many times, and its behavior must be stable and aligned with your intent. Small ambiguities in the System Message compound over iterations. The strategies differ from single-pass generation: **explicit goal definition**, **iterative refinement**, **constraints on tool use**, and **recovery instructions** for when things go wrong.

**Level 2 candidates:**

- **Goal Specification and Success Criteria** — Defining what the agent is trying to achieve (not just a vague task); being explicit about success conditions.
- **Tool-Specific Instructions** — Documenting when each tool should be used, what it returns, and how to interpret results; reducing hallucinations through clarity.
- **Constraints and Safety Boundaries** — Instructing the agent on what it *cannot* do; implementing guardrails through the System Message.
- **Iteration and Stability** — Testing the agent over many runs and varying inputs; refining the System Message until behavior stabilizes.
- **Handling Loops and Stuck States** — Instructing the agent to detect when it's stuck (repeating the same action) and how to recover; strategies like "try a different tool" or "escalate to human."

---

## Sequencing Note

**Prerequisites:** The Agentic Track assumes you've completed the **Core Track**. You must understand decoupled inference, context management, tool calling (L1-08), and structured outputs (L1-11) before diving into agentic loops. **If you haven't, go back to Core first.**

### ⚠️ Critical Warning: Don't Start Here Without Core Track

The most common failure: trying to build agentic systems without understanding the foundation. If you don't know:

- **How tool calling works** (Core L1-08): Your agents will hallucinate tool calls or parse them incorrectly, leading to infinite loops.
- **How context windows work** (Core L1-02): Your agents will hit context limits and you'll have no idea why they suddenly start failing.
- **How structured outputs work** (Core L1-11): Your agents will generate invalid JSON and crash, unable to recover.
- **How models are stateless** (Core L1-01): You'll expect agents to "remember" things you never gave them in context.

**You will waste weeks debugging agent behavior** if you skip Core. Don't do it. Complete Core Track first—it takes 2-4 weeks and saves you months of frustration.

### The Three Tracks Explained

The Agentic Track builds on Core in a natural progression: Core teaches you to make a single model call reliably; Agentic teaches you to make the model decide what to do next.

**Four-stage progression within Agentic:**

**Layer 1: Foundations (L1-01 to L1-03)** — Start by mastering the agentic loop in raw Python. Understand the Thought-Action-Observation pattern and the control vs. autonomy tradeoff. This is non-negotiable; the loop is the bedrock.

**Layer 2: Orchestration (L1-04 to L1-07)** — Once your loop works, scale it: add async execution for speed, move to multi-agent teams for specialization, implement self-correction, and pragmatically adopt frameworks.

**Layer 3: Tools & Ecosystems (L1-08 to L1-10)** — Now optimize tool calling: design schemas that the model reliably respects, adopt MCP for standardized tool integration, and think about tool granularity.

**Layer 4: Production (L1-11 to L1-15)** — Finally, harden the system: add graphs for structure, escalation for safety, observability for debugging, and prompt engineering tailored to agentic loops.

**How this relates to other tracks:**

- **Core → Agentic:** You must complete Core Track before starting Agentic. Critical prerequisites: L1-08 (Tool Calling) and L1-11 (Structured Outputs) from Core.
- **Agentic → Production:** After mastering agentic patterns here, move to Production Track to learn deployment, scaling, and operations. The Production Track teaches you to take working agents and make them reliable, observable, and scalable.

**High-leverage entry points depend on your blocker:**

- **"My agent gets stuck in loops"** → L1-01 (understand termination conditions), then L1-02 (maybe you need a workflow, not an agent), then L1-03 (might be underpowered model).
- **"My single agent can't handle complexity"** → L1-05 (multi-agent teams) and L1-06 (self-correction).
- **"My tools keep failing with bad parameters"** → L1-08 (tool definition) + L1-09 (MCP for standardization).
- **"I need to ship this to production"** → L1-12 (escalation), L1-13 (observability), L1-14 (reliability patterns), then move to **Production Track**.

**The dependency chain:**

- L1-01 (The Loop) is prerequisite for everything. You cannot skip this.
- L1-02 (Workflows vs. Agents) is a decision gate: if the answer is "workflow," you don't need the rest of the track.
- L1-03 (Model Reasoning) informs L1-05 (Multi-Agent Teams): you need frontier models for planning and smaller models for workers.
- L1-04 (Async Execution) depends on having multiple agents or tools to coordinate (so do L1-05 first, or at least understand the motivation).
- L1-08 (Tool Definition) depends on L1-01 (the loop), but L1-09 (MCP) depends on L1-08.
- L1-13 (Observability) and L1-14 (Production Reliability) can be tackled in parallel; they're orthogonal.
- L1-15 (Agentic Prompting) applies throughout, but only becomes critical after L1-01 is solid.

**Shortest path to a working agent:** L1-01 → L1-02 (decide: agent or workflow) → L1-03 (pick a model) → Build in raw Python. Ship a prototype locally.

**Path to a production-ready agentic system:** L1-01 → L1-03 → L1-05 (multi-agent) or L1-08 (tool reliability) → L1-13 (observability) → L1-14 (hardening). Then move to **Production Track** for containerization, deployment, and scaling.

**Path for teams with high-risk tasks (finance, operations):** L1-01 → L1-06 (self-correction) → L1-12 (escalation) → L1-13 (observability). Then move to **Production Track** for compliance and security features.

---

## Quick Reference: Agentic Patterns

**Pattern: Simple Loop (Prototype)**
```
while not done:
  - Call LLM with goal + tools + context
  - If LLM returns tool call: execute → append result → loop
  - If LLM returns final answer: done = True
```
Complexity: 20 lines of code. Risk: None (it's a prototype). Use: First draft.

**Pattern: Async Multi-Agent (Speed)**
```
- Planner agent decides which tools to use
- Execute all tools in parallel
- Gather results
- Optimizer agent refines answer
```
Complexity: Moderate. Risk: Moderate (parallel failures). Use: When latency matters.

**Pattern: Self-Correcting (Reliability)**
```
- Generator creates output
- Evaluator checks it
- If bad: Optimizer revises
- Evaluator re-checks
- Repeat until approved or max iterations
```
Complexity: Moderate. Risk: High cost (multiple passes). Use: High-stakes decisions.

**Pattern: Graph-Based (Structure + Flexibility)**
```
Define graph: Fetch → Analyze → Decide → Act
- Each node can be a hard-coded function or an agent
- Edges are conditional (classifier chooses next step)
- Combine determinism (graph shape) with flexibility (agent reasoning within nodes)
```
Complexity: High. Risk: Moderate (fixed structure prevents some failure modes). Use: Complex, multi-step workflows.

---

## Key Distinctions from the Core Track

Where the **Core Track** teaches you to call a model reliably, the **Agentic Track** teaches you to make the model decide. This shifts the locus of control:

| Aspect | Core Track | Agentic Track |
|---|---|---|
| **Control Flow** | Your code decides the next step | Model (in a loop) decides via tool calls |
| **Failure Mode** | Wrong output | Infinite loop, wrong tool selection, hallucination |
| **Testing** | Deterministic (same input → same output) | Stochastic (same input → different paths) |
| **Latency** | Predictable (N calls, each timed out) | Unpredictable (depends on agent's reasoning depth) |
| **Cost** | Per-token (controllable) | Per-loop (unbounded if loop doesn't terminate) |
| **Debugging** | Trace one call | Trace 50 steps to find where it went wrong |

The agentic track amplifies everything: power (agents solve complex problems), complexity (agents fail in surprising ways), and cost (agents can spiral). Mastering the loop and then scaling carefully is the path forward.

## Source

https://www.udemy.com/course/generative-and-agentic-ai-in-production/