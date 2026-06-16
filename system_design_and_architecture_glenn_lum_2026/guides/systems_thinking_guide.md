# Systems Thinking Guide

## Introduction

**Purpose**
A trigger, not a textbook. This guide exists to shift you into architectural thinking mode when you're looking at a problem — before you write code, before you propose a solution. The questions here are prompts to slow down on the decisions that are hard to reverse.

**Principles**
- Every architectural decision buys something and costs something else. If you can't name both sides, the decision hasn't been made — it's been deferred.
- The decisions that matter are the ones that would hurt to undo. Those deserve scrutiny. Everything else can be left to the team.
- A system you can only reason about when it's working is a system you don't fully understand. Failure modes are part of the design, not a postscript to it.

**Outcomes**
You're applying this well when you can name what a system is optimising for and what it's sacrificing. When you can identify where the coupling actually lives, not just where it's intended to live. When you can describe how a failure starts and where it stops. When you can trace a symptom to the layer where the root cause is.

**How to use**
Run through the five questions when approaching a new problem, a design decision, or an unfamiliar system. They follow a rough sequence — from intent, to structure, to failure, to diagnosis. Use the keywords to orient yourself. Follow the section references only when you need to go deeper.

---

## The Questions

**1. What are we actually optimising for?**
Every system makes tradeoffs implicitly or explicitly. This question forces you to name the 2-3 characteristics that matter most — speed, consistency, availability, simplicity, deployability — before any structural decisions are made. A system that hasn't named its priorities is optimising by accident.
*Keywords: characteristics, prioritisation, availability, consistency, deployability*
*→ L1-02, L1-16*

---

**2. Where are the hard-to-reverse decisions?**
Architecture lives here — not in the big diagram, but in the decisions that would be expensive or painful to undo. These deserve explicit documentation: what was decided, what alternatives were considered, and what the decision costs. Everything else can be left to the team.
*Keywords: reversibility, ADRs, decision cost, architectural vs design*
*→ L1-01, L1-05*

---

**3. How tightly coupled is this?**
If I change X, what else breaks? Coupling isn't always bad but it must be intentional. The nature of the coupling matters as much as its existence — some coupling is safe, some is structural debt. Where your coupling lives determines where your failure domains are and how independently components can be deployed and changed.
*Keywords: connascence, cohesion, service boundaries, dependency direction*
*→ L1-03, L1-19*

---

**4. How does this fail?**
Not if — how. Where does failure start and where does it stop? Does it fail loudly or silently? Is it recoverable? Partial failures in distributed systems propagate in non-obvious ways. A system you can't reason about in failure is a system you don't fully understand.
*Keywords: partial failure, cascading failure, idempotency, recoverability, delivery semantics*
*→ L1-06, L1-14, L1-17*

---

**5. What layer is this problem actually in?**
Is this a structure problem (how things are organised), a data problem (how state moves and stays consistent), or a distribution problem (what happens across multiple machines)? Symptoms appear in one layer; root causes often live in another. The fix belongs in the layer where the cause is.
*Keywords: cross-layer tracing, structure vs data vs distribution, root cause*
*→ L1-08, L1-10, L1-19*

---

## Gut Checks

Lighter questions to layer on top of the five. Run these when something feels off but you can't name why.

**"What would have to be true for this decision to be wrong?"**
Forces you to surface the assumption the tradeoff is resting on. If you can't answer it, the decision isn't well understood yet.
*Keywords: assumptions, fitness functions, revisability*
*→ L1-05, L1-16*

---

**"Where does state live, and who owns it?"**
The source of most distributed system pain. Service boundaries and data ownership are the same decision — getting them misaligned produces the distributed monolith: all the operational complexity of microservices with none of the independence.
*Keywords: data ownership, service boundaries, replication lag, distributed monolith antipattern*
*→ L1-12, L1-13, L1-19*

---

**"Is this complexity justified by real load or imagined load?"**
Most premature complexity comes from anticipated scale that never arrives. The cost of a scalable solution is real now; the benefit is hypothetical. Name the actual load before reaching for a distributed solution.
*Keywords: scalability vs simplicity, premature optimisation, load*
*→ L1-10, L1-16*

---

**"If this component disappeared, what breaks immediately vs eventually?"**
Tells you the real coupling, not the intended coupling. Immediate breakage is tight coupling. Eventual breakage reveals consistency dependencies. Silent non-breakage reveals whether the component was actually necessary.
*Keywords: coupling, failure domains, eventual consistency*
*→ L1-03, L1-14, L1-17*

---

## Resource Map

**Group 1 — Architectural Foundations** *(Richards & Ford: Fundamentals of Software Architecture)*
The vocabulary and decision framework. What architecture is, how to identify and prioritise characteristics, how to measure and manage coupling, the major architecture styles, and how to make and document decisions.
*Primary to questions 1, 2, 3*
*L1-01 · What Architecture Actually Is*
*L1-02 · Architectural Characteristics*
*L1-03 · Modularity and Coupling*
*L1-04 · Architecture Styles*
*L1-05 · Architectural Decision-Making*

---

**Group 2 — Distributed Systems Patterns** *(Burns: Designing Distributed Systems)*
The structural patterns for systems that run across multiple machines. The fallacies of distributed computing, single-node container patterns, multi-node scalability patterns, and batch processing.
*Primary to questions 4, 5*
*L1-06 · Foundations of Distributed Systems*
*L1-07 · Single-Node Patterns*
*L1-08 · Multi-Node Distributed Patterns*
*L1-09 · Batch and Stream Processing Patterns*

---

**Group 3 — Data Systems Design** *(Kleppmann: Designing Data-Intensive Applications)*
The foundations of how data persists, moves, and stays consistent at scale. Storage engines, replication, partitioning, transactions, isolation levels, and stream processing.
*Primary to questions 4, 5 and the state ownership gut check*
*L1-10 · Foundations of Data Systems*
*L1-11 · Storage and Retrieval*
*L1-12 · Replication*
*L1-13 · Partitioning and Transactions*
*L1-14 · Consistency and Consensus*
*L1-15 · Batch and Stream Processing at the Data Layer*

---

**Group 4 — Systems Reasoning** *(Synthesis across all three)*
The cross-cutting layer. Tradeoff reasoning, failure reasoning, evolutionary architecture, and cross-layer diagnosis. Where the other three groups become a unified way of thinking rather than separate pattern libraries.
*Primary to all five questions*
*L1-16 · Tradeoff Reasoning*
*L1-17 · Failure Reasoning*
*L1-18 · Evolutionary Architecture*
*L1-19 · Cross-Layer Reasoning*

---