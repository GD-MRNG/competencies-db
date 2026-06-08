# Agentic Coding Tools — Level 0: Course Map

> **Intent:** To reason clearly about any coding agent — past, present, or future — without being captured by product marketing or category hype. To make principled decisions about adoption, configuration, trust, and risk.
>
> **Your angle:** You already use these tools. The goal isn't familiarity — it's building a durable conceptual frame that lets you evaluate new entrants, debug unexpected behaviour, and design workflows that don't accumulate invisible debt.

---

## How to use this map

Each **Level 1** topic is a load-bearing concept — something that changes how you reason about the whole domain once you understand it properly. Each **Level 2 candidate** is a place to go deeper when a Level 1 explanation leaves a gap or raises a question. Descend to Level 2 when something breaks in practice and you don't know why, or when you're making a design or adoption decision that the Level 1 framing doesn't resolve.

---

## Topic Inventory

---

### I. The Nature of Agency

#### L1-01 · The Perception–Planning–Execution Loop

The fundamental architecture underneath every coding agent, regardless of form factor. Borrowed from robotics and formalised in AI research through the ReAct paradigm (Yao et al., 2022), this loop is what distinguishes an agent from a code generator: it observes state, reasons about action, acts, then observes again. Understanding this loop tells you where agents fail — not randomly, but predictably at each phase transition — and why adding more tokens or a better model often isn't the fix.

- **Observation grounding** — what happens when the agent's model of the environment diverges from reality, and why this compounds across loop iterations rather than self-correcting
- **ReAct vs. fixed pipelines** — what you give up in flexibility by replacing the loop with a structured pipeline, and what you gain in reliability and cost
- **Loop termination conditions** — how an agent decides it is done, and why miscalibrated termination produces both over-confident truncation and infinite retry spirals
- **State representation** — why the way the agent encodes what it knows between steps determines whether it can reason across a long task at all

#### L1-02 · The Scaffold

The control loop, tool interface, memory strategy, and error handling that wraps the model. The scaffold is the actual engineering product; the model is a component inside it. Two agents using the same model with different scaffolds produce dramatically different results. Most evaluations and marketing comparisons confound these two things, which makes them nearly useless for decision-making.

- **Agent-computer interface (ACI) design** — why the format and vocabulary through which an agent interacts with a machine is a first-class design decision, not just plumbing
- **Context compaction strategies** — how different approaches to summarising or pruning context create different failure modes, and what gets silently lost
- **Tool schema design** — why ambiguous or overlapping tool definitions cause the model to hallucinate tool calls, independent of model capability
- **Scaffold-model attribution** — why benchmark scores cannot be used to compare models across different scaffolds, and what that means for vendor claims

---

### II. Context and Memory

#### L1-03 · The Context Window as a Contract

The agent can only act on what it has been given. This sounds obvious but has non-obvious consequences: any gap between what the agent knows and what it needs to know is filled by the model's priors — which means plausible-sounding confabulation, not an error message. Context isn't just input; it is the complete specification of the agent's world at a moment in time.

- **Context rot** — how agent output quality degrades over long sessions even before hitting the hard context limit, and why it's often invisible until a catastrophic error
- **Retrieval-augmented context** — what RAG adds to a coding agent versus what it cannot substitute for, and where the seam between retrieved and authoritative context creates trust problems
- **Instruction files (CLAUDE.md, .cursorrules, etc.)** — why persistent project-level context is the highest-leverage configuration surface most engineers underuse
- **Context poisoning** — how malicious or noisy content in retrieved context can silently redirect agent behaviour without triggering any visible error

#### L1-04 · Memory Across Sessions

A single context window is stateless. Anything the agent learns in one session must be explicitly externalised to survive to the next. This sounds like a limitation but is actually a design surface: what you choose to persist, and in what form, shapes the agent's long-run behaviour more than any single prompt.

- **Episodic vs. semantic memory** — the tradeoff between storing what happened (recoverable but expensive) and storing what was learned (efficient but lossy)
- **Auto-generated memory artifacts** — what agents write to disk autonomously between sessions, and why you should audit these rather than treat them as background infrastructure
- **Cross-session consistency failure** — how decisions made in an early session silently constrain or contradict decisions in a later one when memory is absent or incomplete

---

### III. Trust, Authority, and Security

#### L1-05 · Trust Boundaries

Every input channel into an agent — files it reads, repos it clones, tools it calls, servers it connects to — is a surface from which instructions can arrive. The agent cannot reliably distinguish a legitimate instruction from a malicious one embedded in data. Trust does not transfer automatically from you to every surface you connect the agent to. This is the foundational security concept for agentic systems, and it is architectural, not a patching problem.

- **Prompt injection (direct vs. indirect)** — the difference between attacking the system prompt and attacking the data the agent reads, and why indirect injection is the harder problem to defend
- **MCP server trust** — why connecting to a community-published MCP server is closer to installing an unsigned browser extension than calling an API, and what the actual risk surface looks like
- **Cross-agent propagation** — how a successful injection in one agent in a multi-agent system propagates to co-running agents through inter-agent trust relationships
- **Supply chain injection** — how attackers embed instructions in public repositories specifically to be found and executed by agents performing routine dependency or codebase searches

#### L1-06 · The Blast Radius Principle

Agent actions differ in reversibility. The appropriate level of human oversight should be calibrated to the blast radius of the action, not to the agent's expressed confidence. File edits, commits, pushes, deployments, and external API calls sit at different points on this spectrum. Flattening them into a single trust level — "the agent has access" — is the most common and consequential misconfiguration in production agentic workflows.

- **Reversibility taxonomy** — how to classify agent actions by the effort required to undo them, and where the practical irreversibility threshold sits for your environment
- **Minimal permission scoping** — why granting an agent broad access because it's convenient is a structural risk decision, not just an operational one
- **Human-in-the-loop checkpoints** — how to identify the specific action types that warrant synchronous human review versus async audit, without collapsing the autonomy that makes agents useful

---

### IV. Autonomy, Evaluation, and Legibility

#### L1-07 · The Autonomy Dial

Autonomy is not binary. Every tool in the market can be operated at multiple points on a spectrum from line-by-line suggestion to multi-hour unsupervised execution. The right setting is determined by task reversibility, how well the problem is specified, and your current capacity to verify output — not by what the tool defaults to or what the marketing suggests.

- **Task delegability criteria** — the characteristics that make a task safe to delegate (verifiable output, bounded scope, reversible actions) versus ones that make it a liability
- **Prompt specificity vs. output quality** — why underspecified prompts combined with high autonomy produce plausible but misaligned outputs that are harder to catch than obvious errors
- **Autonomy creep** — how workflows gradually expand agent permissions over time without a corresponding increase in oversight, and how to detect it before something goes wrong

#### L1-08 · Observability and Legibility

The meta-principle: agency without legibility is liability. As autonomy increases, your ability to understand what the agent actually did — not just what it produced — becomes the primary risk control. Diffs, tool call logs, intermediate reasoning traces, and audit trails are not debugging conveniences; they are the mechanism by which you retain ownership of code an agent has modified.

- **Diff-level legibility** — why reviewing agent-produced diffs requires different mental habits than reviewing human-produced ones, and what patterns signal low-confidence generation
- **Reasoning traces** — what chain-of-thought output does and doesn't tell you about why the agent took an action, and where it can mislead
- **Audit trail design** — what to log about agent sessions so that failures are post-mortem reconstructible, and what the minimum viable record looks like
- **Benchmark legibility** — why published SWE-bench scores confound model capability with scaffold design, and how to construct your own evaluation for your specific codebase

#### L1-09 · Multi-Agent Coordination

Running multiple agents in parallel is not straightforwardly better than running one well-configured agent. Coordination introduces overhead, trust complexity, and new failure modes. The gains are real but bounded — and above a certain single-agent capability threshold, adding agents can degrade results. Understanding when coordination helps requires understanding what the actual bottleneck is.

- **Orchestrator–subagent patterns** — how task decomposition across agents creates dependency and synchronisation problems that don't exist in single-agent workflows
- **Capability saturation** — why multi-agent coordination yields diminishing returns once a single agent already handles the task reliably, and how to identify that threshold
- **Shared context problems** — how agents working on the same codebase in parallel can produce conflicting states that are coherent locally but broken when merged

---

## Sequencing Note

The dependency chain runs in the order presented. The loop (L1-01) and scaffold (L1-02) are the conceptual foundation — without them, discussions of evaluation, security, and autonomy float free of mechanism. Context (L1-03, L1-04) is the next load-bearing layer, because most practical failures in production trace to context problems before they trace to anything else.

Trust and blast radius (L1-05, L1-06) should be understood before you expand any agent's permissions in a real codebase — these are the topics where ignorance carries the most asymmetric downside. Autonomy and legibility (L1-07, L1-08) are the operational translation of the meta-principle and are worth revisiting every time you add a new tool or extend an existing workflow. Multi-agent coordination (L1-09) is last because it only becomes relevant once single-agent workflows are well-understood and genuinely bottlenecked.

The highest-leverage entry point for a working engineer is L1-05 + L1-06 — not because they are foundational, but because the cost of not understanding them is immediate and concrete, while the payoff from understanding them applies retroactively to every tool you already use.