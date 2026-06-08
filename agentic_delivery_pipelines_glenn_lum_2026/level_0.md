# Autonomous Agentic Delivery Pipelines — Level 0: Course Map

> **Intent:** To understand the engineering principles that make it safe, reliable, and cost-effective to delegate software development tasks — implementation, review, testing, and iteration — to autonomous agents operating inside existing development workflows.
>
> **Your angle:** You already build software and understand CI/CD. Come to this as a systems designer, not a user of AI tools. The question isn't "how do I use this agent" — it's "what architectural decisions make an agent-augmented pipeline trustworthy enough to run without supervision?" Most of what you'll find here is old engineering thinking applied to a new execution context.

---

## How to use this map

This document is a navigation tool, not a learning resource. Each Level 1 topic names a concept significant enough to warrant its own study. Each Level 2 candidate under it is a sub-concept worth drilling into — either because it explains a tradeoff, unlocks an adjacent topic, or breaks in surprising ways if you skip it.

When you find a Level 1 topic that maps to a gap in your current mental model, descend to Level 2. When you find one you already understand deeply, use it to orient yourself relative to the topics around it. The sequencing note at the end tells you where to start.

---

## Topic Inventory

### I. Foundations: The Principles That Predate Agents

These are the load-bearing ideas. They were not invented for agentic systems — they were applied to them. Understanding them at source makes the agent-specific patterns obvious rather than novel.

---

#### L1-01 · Shift Left on Feedback

Coined in the early 2000s in the context of software testing, but the underlying idea is older: the cost of fixing a defect grows exponentially with distance from its origin. Every layer of tooling in a modern delivery pipeline — linters, type checkers, unit tests, integration tests, deployment gates — is an application of this principle. Applying it to an agent means asking the agent to review its own output before it reaches a human, at the moment correction is cheapest. This is not a new idea; it is the same idea in a new execution context.

**Level 2 candidates:**
- **Feedback loop latency** — Why the time between a mistake and its detection determines the practical cost of iteration, and what this implies for where you place review steps in an automated pipeline.
- **Defect amplification** — How a flaw that takes seconds to fix at creation takes hours to fix post-deployment, and why this asymmetry justifies seemingly redundant early checks.
- **Static vs. dynamic analysis** — What the boundary between checking code without running it and checking it at runtime reveals about which class of errors each approach can and cannot catch.
- **The test pyramid** — Why the ratio of unit to integration to end-to-end tests exists, and what breaks when teams invert it.
- **Self-review as a quality gate** — What happens structurally when the creator of an artefact reviews it before handoff, and why a fresh context reviews more reliably than a stale one.

---

#### L1-02 · Deterministic Gates Around Probabilistic Outputs

Machine learning systems generate candidates — they do not enforce constraints. Every production ML system that operates reliably does so because deterministic validation wraps the probabilistic generation. Content moderation pipelines, fraud detection, recommendation systems, and now code generation agents all share this architecture. The model is never the last line of defence. This principle explains why hooks, linters, and test runners matter more in an agentic pipeline than in a human one — the human brings implicit constraint-checking that the agent does not.

**Level 2 candidates:**
- **Input validation vs. output validation** — Why checking what goes into a model and what comes out of it are distinct problems requiring distinct mechanisms.
- **Hard stops vs. soft signals** — What the difference between a gate that blocks execution and a gate that emits a warning reveals about where you have genuine enforcement vs. where you are relying on interpretation.
- **Idempotency** — Why operations that can be safely retried are easier to automate reliably, and what you have to redesign when an operation is not idempotent.
- **Schema enforcement** — How constraining the shape of a model's output before downstream systems consume it prevents an entire class of integration failures.
- **Sandboxing** — What it means to limit the blast radius of a probabilistic system's mistakes by controlling what it can read, write, and execute.

---

#### L1-03 · Separation of Concerns Across Layers

Larry Constantine's original formulation from the 1960s: systems should be decomposed so that each component has a single, well-defined responsibility. In agent pipelines, this maps directly onto the distinction between what belongs in a configuration file (standards), what belongs in a library (reusable logic), what belongs in a runtime hook (enforcement), and what belongs in a generation step (output). Mixing these layers — putting enforcement in a prompt, putting standards in a per-run instruction — is the root cause of most unreliable agent setups.

**Level 2 candidates:**
- **Cohesion and coupling** — How measuring how related a component's internals are (cohesion) and how dependent it is on other components (coupling) gives you a vocabulary for evaluating whether a decomposition is sound.
- **Configuration as code** — What becomes possible when system behaviour is declared in version-controlled files rather than set through UI or implicit convention, and why this matters for reproducibility.
- **The single responsibility principle** — Why a component that does one thing fails more predictably and is easier to replace than one that does several, and how this applies to agent roles.
- **Interface boundaries** — How explicit contracts between components allow you to swap implementations without changing callers, and what agent systems gain from enforcing this at the tool level.
- **Policy vs. mechanism** — The Unix design principle that a tool should provide the mechanism and the caller should specify the policy — and why violating this in agent pipelines leads to brittle, hard-to-generalise workflows.

---

### II. Core Theory: Reliability and Control

These topics deal with how you build systems that behave predictably when their components are inherently non-deterministic or partially autonomous.

---

#### L1-04 · Event-Driven Architecture

Developed formally through the 1980s and 1990s alongside the growth of distributed systems, event-driven architecture decouples producers of signals from consumers of them. Instead of a central coordinator polling for state changes, components emit events and subscribers react to them. This is the structural pattern underneath GitHub Actions, AWS Lambda triggers, and every CI/CD pipeline. For agent workflows it matters because it makes pipelines composable, observable, and incrementally extendable without rewriting the core loop.

**Level 2 candidates:**
- **Event sourcing** — How recording every state change as an immutable event rather than overwriting current state gives you a complete audit trail and the ability to replay history — critical for debugging non-deterministic agent behaviour.
- **Pub/sub vs. point-to-point messaging** — What the tradeoff between broadcasting events to all subscribers and routing them to specific consumers reveals about coupling and scalability.
- **Idempotent event handling** — Why designing event consumers so they produce the same result if the same event arrives twice is a prerequisite for safe automated retries.
- **Trigger design** — How the choice of what event fires a workflow determines its blast radius, cost profile, and susceptibility to infinite loops.
- **Dead letter queues** — What happens to events that fail processing, and why having an explicit failure path is necessary for any automated system that runs unattended.

---

#### L1-05 · Context Isolation

Processes have separate memory spaces. Microservices have network boundaries. Database transactions have isolation levels. The underlying principle in every case is the same: shared mutable state between concurrent actors is a source of unpredictable behaviour. In agentic systems, this manifests as context window contamination — an agent that has been reasoning about a problem for a long session has accumulated anchoring bias, failed approaches, and stale assumptions that distort its output. Isolating contexts is not just about parallelism; it is about cognitive hygiene for non-deterministic reasoners.

**Level 2 candidates:**
- **Process isolation** — What the OS-level boundary between processes buys you in terms of fault containment, and what it costs in terms of inter-process communication overhead.
- **Session memory and anchoring bias** — Why a long reasoning session accumulates assumptions that bias subsequent outputs, and what the structural solution (fresh context) borrows from human code review practice.
- **Bulkhead pattern** — How partitioning a system so that failure in one component cannot cascade to others applies equally to distributed services and agent subprocesses.
- **Stateless vs. stateful workers** — What you gain in scalability and predictability by designing workers that hold no session state, and what you give up in capability.
- **Context window as a scarce resource** — Why treating the attention window of a language model as a finite resource to be managed — not a dump for all available information — changes how you design agent workflows.

---

#### L1-06 · Principle of Least Privilege

Formulated by Jerome Saltzer and Michael Schroeder in their 1975 paper on computer security: every component should operate with the minimum permissions required to perform its function. This limits the blast radius when something goes wrong — and in autonomous systems, things go wrong in ways that are harder to predict than in human-operated ones. Scoping what an agent can read, write, execute, and call is not a bureaucratic constraint; it is the primary mechanism for making autonomous behaviour safe to run without supervision.

**Level 2 candidates:**
- **Permission scoping** — How defining the exact set of capabilities a process needs — and denying everything else by default — creates an audit trail of what a system can and cannot affect.
- **Blast radius** — The practice of designing systems so that when a component fails or misbehaves, the maximum possible damage is bounded — and what this implies for how you partition agent tool access.
- **Token-based vs. role-based access** — What the difference between "this credential does X" and "this role can do X" reveals about how access control scales across environments and teams.
- **Audit logging** — Why recording every privileged action an autonomous system takes is a prerequisite for post-incident analysis, and what the absence of logs implies about accountability.
- **Fail-safe defaults** — The design principle that a system should deny access by default and require explicit grants — and why this is harder to implement than it sounds in practice.

---

### III. Applied: Engineering for Autonomous Operation

These topics deal with the practical design decisions that distinguish an agent pipeline that runs reliably in production from one that requires constant supervision.

---

#### L1-07 · DRY and the Encoding of Decisions

Don't Repeat Yourself, articulated by Hunt and Thomas in *The Pragmatic Programmer* (1999), is at its core a claim about where knowledge lives in a system. Every piece of knowledge should have a single, authoritative representation. When the same instruction appears in multiple places — in prompts, in documentation, in scripts — it diverges. When it diverges, the system behaves inconsistently. In agent pipelines, this means standards belong in configuration files, reusable patterns belong in skill libraries, and enforcement belongs in hooks — not scattered across workflow YAML files where they will be duplicated, forgotten, and contradicted.

**Level 2 candidates:**
- **Single source of truth** — What it means for a piece of knowledge to have exactly one authoritative representation, and what breaks when that principle is violated across a distributed system.
- **Configuration drift** — How environments that start identical diverge over time when configuration is not declaratively managed, and why this is more damaging in automated pipelines than in human-operated ones.
- **Abstraction as DRY** — Why extracting shared logic into a reusable component is not just about reducing line count but about ensuring that a change to the logic needs to happen in exactly one place.
- **Skill and template libraries** — How encoding reusable agent instructions as versioned, named artefacts rather than inline prompts gives you the same benefits as a shared code library.
- **Documentation as code** — What treating documentation with the same versioning, review, and update discipline as source code prevents, and why it matters more when agents read documentation as operational input.

---

#### L1-08 · Human-in-the-Loop Design

Automation does not eliminate human judgment — it relocates it. The design question is not "should humans be involved?" but "at which checkpoint is human judgment highest-value and non-substitutable?" Systems that involve humans at every step are not automated. Systems that involve humans at no step are not safe. The engineering discipline is identifying the irreducible checkpoints — architectural tradeoffs, ambiguous requirements, final merge decisions — and designing everything else to flow without interruption.

**Level 2 candidates:**
- **Checkpoint selection** — How to identify which decisions in a workflow genuinely require human judgment vs. which ones have been kept human by inertia, and what criteria distinguish them.
- **Automation bias** — The documented tendency for human reviewers to accept automated outputs without scrutiny when the automation is trusted, and what interface design can do to counteract it.
- **Escalation paths** — How a well-designed automated system recognises the boundaries of its competence and routes to a human rather than proceeding with low confidence.
- **Merge gates and branch protection** — Why the final integration step is the natural human checkpoint in a code delivery pipeline, and what it means to design everything upstream of it as automatable.
- **Accountability without presence** — How you maintain clear responsibility for system behaviour when no human was involved in producing the specific output being deployed.

---

#### L1-09 · Feedback Loop Architecture

A feedback loop is any system where output is routed back as input to influence future behaviour. The engineering of feedback loops — their latency, their gain, their stability — is a field in its own right, originating in control theory (Norbert Wiener, 1948) and applied everywhere from thermostats to PID controllers to CI pipelines. In agent workflows, the PR comment loop is a feedback loop: your review is input that modifies the agent's next output. Designing this loop well — with appropriate tightness, clear signal, and guards against oscillation — is the difference between a productive iteration cycle and an infinite loop.

**Level 2 candidates:**
- **Loop gain and stability** — Why a feedback loop that overcorrects oscillates rather than converges, and what the analogous failure mode looks like in an automated CI fix pipeline.
- **Signal vs. noise in review** — How the clarity and specificity of feedback determines whether an agent (or a human) can act on it, and what "actionable" actually means in a review comment.
- **Convergence criteria** — Why every automated loop needs an explicit definition of "done" — whether that is a passing test suite, an approved review, or a confidence threshold — and what happens when this is left implicit.
- **Infinite loop guards** — The structural mechanisms (branch naming conventions, trigger conditions, turn limits) that prevent an automated system from re-triggering itself indefinitely.
- **Latency vs. thoroughness** — The tradeoff between a fast feedback loop that catches errors quickly and a thorough one that catches more errors but slows iteration, and how to tune this for different pipeline stages.

---

#### L1-10 · Observability and Auditability

You cannot debug what you cannot see. Observability — the ability to infer the internal state of a system from its external outputs — was formalised in the context of distributed systems (Charity Majors, Honeycomb, circa 2016) but the engineering need predates it. In autonomous agent pipelines, observability is more important than in human-operated ones because the failure modes are less predictable and the actor cannot explain itself after the fact. An agent that silently produces wrong output is more dangerous than one that fails loudly. Designing for observability from the start is not optional; it is what makes autonomous operation recoverable.

**Level 2 candidates:**
- **Structured logging** — Why emitting logs as parseable key-value pairs rather than human-readable strings makes automated analysis possible, and what you lose when you cannot query your own system's history.
- **Distributed tracing** — How following a single request or task across multiple services or agent steps gives you a causal chain rather than isolated snapshots, and why this matters for debugging emergent failures.
- **The three pillars: logs, metrics, traces** — What each of these captures that the others cannot, and how they compose into a complete observability picture for an automated pipeline.
- **Alerting on absence** — Why monitoring for things that should happen but don't (a pipeline that runs but produces no output) requires different instrumentation than monitoring for errors.
- **Audit trails for autonomous actions** — What it means to maintain a legally and operationally defensible record of what an automated system did, when, and why — and what the absence of this record costs you in incident response.

---

## Sequencing Note

The dependency chain here runs left to right across the three groups. The foundational principles (L1-01 through L1-03) are the conceptual primitives — you can read the rest of this map without them, but the applied patterns will seem arbitrary rather than inevitable. Start there if any of them feel uncertain.

The core theory group (L1-04 through L1-06) is where the foundational principles become structural patterns. Event-driven architecture, context isolation, and least privilege are the three mechanisms most directly responsible for whether an autonomous pipeline is safe to operate unattended. If you are designing a pipeline from scratch, these are the decisions that are hardest to retrofit later.

The applied group (L1-07 through L1-10) is where the principles meet the daily reality of operating an agent-augmented workflow. DRY and human-in-the-loop design are the two highest-leverage entry points for practitioners who already have a pipeline running and want to make it more reliable. Feedback loop architecture and observability are prerequisites for diagnosing why a pipeline that worked yesterday does not work today.

For someone returning to foundations with existing engineering experience, the highest-value starting points are L1-02 (deterministic gates), L1-05 (context isolation), and L1-08 (human-in-the-loop design) — these three sit at the intersection of what is genuinely new about agentic systems and what is a direct application of established engineering discipline.
