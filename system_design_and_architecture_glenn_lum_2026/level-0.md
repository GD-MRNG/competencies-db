# Systems Design and Architecture — Level 0: Course Map

> **Intent:** To build the mental models that let you reason about software systems as wholes — not just write code that works inside them. The goal is architectural instinct: the ability to look at a system, read its structure, identify where failure will propagate, understand what tradeoffs were made and what they cost, and make design decisions that hold up under real production conditions. This curriculum draws from three foundational texts — Richards & Ford on architectural thinking, Burns on distributed systems patterns, and Kleppmann on data systems — and synthesises them into a single reasoning framework.
>
> **Your angle:** You are a practitioner with production experience who already operates systems but wants the conceptual architecture to match. You have instincts that work — this curriculum is about making those instincts explicit, extending them to situations you haven't encountered yet, and giving you the vocabulary to reason across layers simultaneously. The synthesis layer (Group 4) is where that payoff lives; the first three groups build the foundation it sits on.

---

## How to use this map

This map draws from three source texts and adds a fourth synthesising group that none of them covers alone:

- **Group 1** — Architectural Foundations (Richards & Ford: *Fundamentals of Software Architecture*)
- **Group 2** — Distributed Systems Patterns (Burns: *Designing Distributed Systems*)
- **Group 3** — Data Systems Design (Kleppmann: *Designing Data-Intensive Applications*)
- **Group 4** — Systems Reasoning (the cross-cutting layer synthesised across all three)

The groups are not strictly sequential but they are dependency-ordered. Group 1 establishes the vocabulary and decision framework. Groups 2 and 3 build the domain-specific pattern libraries for compute and data respectively. Group 4 is where the three come together into a unified reasoning capability — it assumes all three are in place.

Each **Level 1 topic** is one concept post: what it is, where it sits, why it matters to your instinct as a practitioner. Each **Level 2 candidate** is a depth post: mechanics, tradeoffs, where the concept breaks. Descend into Level 2 only where deeper understanding is actively blocking your reasoning or where you know a gap exists.

---

## Topic Inventory

---

### Group 1 — Architectural Foundations
*The thinking framework before the patterns. Richards & Ford's contribution is not a catalogue of styles — it is a way of thinking about systems: what architecture actually is, how to measure it, how to make decisions about it, and how to know when a decision is wrong. Without this layer, architectural patterns are rituals rather than reasoned choices.*

---

#### L1-01 · What Architecture Actually Is

**What it is and why it matters:** Most engineers who work inside systems have a working definition of architecture that is too narrow — it is either "the big diagram" or "whoever makes the hard decisions." Richards & Ford's opening argument is more precise: architecture is the structure of a system combined with the characteristics it must exhibit and the decisions that are hard to reverse. That last clause is the load-bearing one. Understanding architecture as the set of decisions with the highest cost of change is what separates architectural thinking from design thinking — and it is the foundation everything else in this curriculum stands on.

**Level 2 candidates:**

- **L2 · Architecture vs. design** — The boundary between the two is not about scale but about reversibility — understanding where this line sits tells you which decisions deserve architectural-level scrutiny and which can be left to the team.
- **L2 · The laws of software architecture** — Richards & Ford's two laws: everything is a tradeoff, and why is more important than how — internalising these as operating principles rather than aphorisms changes how you approach every architectural conversation.
- **L2 · The role of the architect** — Architecture is not a title but a set of responsibilities — understanding what those responsibilities actually are (and are not) clarifies what it means to think architecturally regardless of your job description.
- **L2 · Architecture and DevOps intersection** — Where architectural decisions constrain or enable operational practice — the link between structural choices and deployment, observability, and reliability outcomes.

---

#### L1-02 · Architectural Characteristics

**What it is and why it matters:** Every system implicitly optimises for something — speed, consistency, scalability, security, simplicity. Architecture characteristics are the explicit articulation of what a system must do beyond its functional requirements. Richards & Ford divide them into operational (performance, scalability, availability), structural (modularity, deployability, testability), and cross-cutting (security, observability, agility). The discipline of identifying and prioritising characteristics before choosing a style is what prevents architectural decisions from being made by default rather than by intent.

**Level 2 candidates:**

- **L2 · Operational characteristics** — Scalability, availability, performance, reliability — the characteristics that govern how a system behaves under load and under failure, and why they are often in tension with each other.
- **L2 · Structural characteristics** — Modularity, deployability, testability, maintainability — the characteristics that govern how easily a system can be changed, and why they are systematically underweighted in early architectural decisions.
- **L2 · Cross-cutting characteristics** — Security, observability, agility — characteristics that apply across the entire system rather than to specific components, and why they must be designed in rather than bolted on.
- **L2 · Identifying and prioritising characteristics** — The practice of surfacing implicit requirements and forcing explicit prioritisation — because a system that tries to optimise for everything optimises for nothing.
- **L2 · Composite characteristics** — How individual characteristics combine into emergent properties — agility as a composite of deployability, testability, and modularity — and why optimising for the composite is different from optimising for the parts.

---

#### L1-03 · Modularity and Coupling

**What it is and why it matters:** Modularity is the property that determines how independently a system's parts can be understood, changed, and deployed. Coupling is what erodes it. Richards & Ford treat modularity as a first-class measurable concern — not a vague aspiration — and introduce connascence as a precise language for describing the nature and strength of coupling between components. This is the topic that makes the "microservices vs monolith" debate legible: it is not a question about deployment topology but about coupling management, and the answer depends on where your coupling actually lives.

**Level 2 candidates:**

- **L2 · Cohesion and coupling defined** — The two forces that determine whether a module is well-bounded — high cohesion within, low coupling without — and why real systems always involve tradeoffs between them.
- **L2 · Connascence** — A more precise taxonomy of coupling than "tight" and "loose" — understanding the different types of connascence (name, type, meaning, position, execution, timing) tells you which couplings are safe and which are architectural debt.
- **L2 · Measuring modularity** — Abstractness, instability, and the distance from the main sequence — the metrics that make modularity a quantifiable property rather than a judgment call.
- **L2 · From modules to components** — How logical modules become deployable components — and why the mapping between the two is itself an architectural decision with structural consequences.
- **L2 · Component coupling patterns** — Acyclic dependencies, stable dependencies, stable abstractions — the principles that keep a component graph from becoming a tangled graph.

---

#### L1-04 · Architecture Styles

**What it is and why it matters:** An architecture style is a named, reusable structural pattern with known characteristics, known tradeoffs, and a known domain of applicability. Richards & Ford catalogue the major styles — layered, pipeline, microkernel, service-based, event-driven, space-based, microservices, modular monolith — not as a menu to choose from but as a vocabulary for recognising what a system already is and reasoning about whether it is the right thing to be. Understanding styles is what lets you read an unfamiliar system quickly and identify structural problems before looking at any code.

**Level 2 candidates:**

- **L2 · Styles vs. patterns** — The distinction between an architecture style (a system-level structural choice) and a design pattern (a local solution to a recurring problem) — conflating them produces confused architectural conversations.
- **L2 · Layered architecture** — The most common default style — understanding its characteristics (simplicity, poor deployability, poor scalability) explains why it works well in some contexts and becomes a bottleneck in others.
- **L2 · Event-driven architecture** — Asynchronous, decoupled, high-scalability — and the hardest to reason about — understanding its failure modes (eventual consistency, lost events, ordering problems) is the prerequisite for using it safely.
- **L2 · Microservices architecture** — The style most often adopted without understanding its actual characteristics — extreme deployability and scalability at the cost of extreme operational complexity — and when that tradeoff is and is not worth making.
- **L2 · Modular monolith** — The style that combines the deployment simplicity of a monolith with the modularity discipline of microservices — understanding it reframes the microservices decision as a question of whether the operational complexity is justified.
- **L2 · Choosing the right style** — The framework for mapping architectural characteristics requirements to style candidates — and why the answer is almost always "it depends on which characteristics you cannot compromise."

---

#### L1-05 · Architectural Decision-Making

**What it is and why it matters:** Architectural decisions are the ones with the highest cost of change — which means making them well, documenting them explicitly, and knowing when to revisit them are core architectural competencies. Richards & Ford treat decision-making as a discipline: using Architecture Decision Records (ADRs) to capture not just what was decided but why, what alternatives were considered, and what the decision costs. Without this discipline, systems accumulate decisions that nobody can explain and nobody dares to change — which is where most architectural debt actually comes from.

**Level 2 candidates:**

- **L2 · Architecture Decision Records (ADRs)** — The practice of documenting decisions at the moment they are made — capturing context, consequences, and alternatives while the reasoning is still available.
- **L2 · Analyzing tradeoffs** — The framework for making tradeoffs explicit rather than implicit — because an undocumented tradeoff is a future surprise waiting to happen.
- **L2 · Anti-patterns in architectural decisions** — Covering your assets, email-driven architecture, and other patterns of decision-avoidance that produce systems nobody understands and nobody owns.
- **L2 · Fitness functions** — Automated checks that verify architectural characteristics are maintained as the system evolves — the mechanism that turns architectural intent into a continuous constraint rather than a one-time decision.

---

### Group 2 — Distributed Systems Patterns
*Burns' contribution is a pattern library for the structural problems that appear when software runs across multiple machines. Each pattern is a named, reusable solution to a class of distributed systems problems — and knowing the pattern library is what lets you recognise which problem you are actually solving rather than inventing a solution from scratch.*

---

#### L1-06 · Foundations of Distributed Systems

**What it is and why it matters:** Before patterns, there are concepts that every distributed system must contend with regardless of its structure. Burns' second edition opens with these explicitly: APIs as contracts, RPCs and their latency implications, reliability semantics, idempotency, and delivery guarantees. These are not features of any particular system — they are the invariant properties of any system where components communicate over a network. Understanding them is what makes the fallacies of distributed computing legible: each fallacy is a violation of one of these invariants that engineers assume away and then rediscover in production.

**Level 2 candidates:**

- **L2 · The fallacies of distributed computing** — The eight assumptions that engineers routinely make about networks that are false — each one is a failure mode waiting to be discovered in production.
- **L2 · APIs and RPCs** — The contract that distributed components communicate through — understanding RPC semantics (latency, failure modes, versioning) is the prerequisite for reasoning about service boundaries.
- **L2 · Reliability and delivery semantics** — At-most-once, at-least-once, exactly-once — the three delivery guarantees and what achieving each one actually costs in system complexity.
- **L2 · Idempotency in distributed systems** — The property that makes retry-safe design possible — drilling here reveals why idempotency is not a property of operations but a property of the combination of operation and state.
- **L2 · Latency as a first-class constraint** — Why latency in distributed systems is not a performance metric but a design constraint that shapes every architectural decision about service decomposition and communication patterns.

---

#### L1-07 · Single-Node Patterns

**What it is and why it matters:** Before reasoning about multi-node systems, Burns establishes patterns at the single-node level — specifically, patterns for structuring containers that run together on the same machine. The sidecar, ambassador, and adapter patterns are not Kubernetes trivia: they are expressions of the separation of concerns principle applied to the container level. Understanding them is what makes service meshes, proxies, and monitoring agents legible as architectural decisions rather than operational add-ons.

**Level 2 candidates:**

- **L2 · The sidecar pattern** — Attaching a secondary container to a primary to extend or modify its behaviour without changing its code — the pattern that makes cross-cutting concerns (logging, TLS, configuration) modular at the infrastructure level.
- **L2 · The ambassador pattern** — A proxy container that handles outbound communication on behalf of the primary — the pattern that lets you add sharding, retry logic, or protocol translation without touching application code.
- **L2 · The adapter pattern** — A container that normalises the output of the primary for consumption by external systems — the pattern that makes heterogeneous monitoring and logging infrastructure possible without modifying every service.
- **L2 · Modular container design** — The principle that containers should be designed for reusability across different applications — and why this changes how you think about what belongs in a container image vs. what belongs in a sidecar.

---

#### L1-08 · Multi-Node Distributed Patterns

**What it is and why it matters:** This is the core of Burns' pattern library — the structural solutions to the problems that emerge when services run across multiple nodes. Replicated services, sharded services, scatter/gather, and leader election are not implementation details; they are named solutions to specific classes of scalability, availability, and coordination problems. Knowing the pattern is knowing what problem you are solving and what the solution costs — which is the difference between choosing an architecture and inheriting one.

**Level 2 candidates:**

- **L2 · Replicated load-balanced services** — The foundational pattern for horizontal scalability — stateless services behind a load balancer — and why statelessness is the prerequisite, not an implementation detail.
- **L2 · Session stickiness and its costs** — The pattern for handling stateful sessions in a replicated environment — and why it reintroduces coupling that replication was supposed to eliminate.
- **L2 · Sharded services** — Partitioning data or load across multiple service instances — the pattern that enables scale beyond what replication alone can achieve, at the cost of routing complexity and hot-shard failure modes.
- **L2 · Scatter/gather** — Distributing a request across multiple nodes and aggregating the results — the pattern behind distributed search, parallel computation, and fan-out queries.
- **L2 · Leader election and ownership** — The pattern for coordinating distributed systems that require a single authoritative node — and why the hardest part is not electing a leader but detecting when the current leader has failed.
- **L2 · Functions and event-driven processing (FaaS)** — The pattern that replaces long-running services with stateless functions triggered by events — and the conditions under which the tradeoff (cold start latency, vendor lock-in) is worth making.

---

#### L1-09 · Batch and Stream Processing Patterns

**What it is and why it matters:** Not all computation is request-response. Burns' batch processing section covers the patterns for work that runs periodically, in parallel, and at scale — work queues, event-driven batch processing, and coordinated multi-stage computation. These patterns are the structural backbone of data pipelines, ETL systems, and any system where processing large volumes of work asynchronously is a first-class requirement. Understanding them is what makes the architectural choices in stream and batch processing legible rather than arbitrary.

**Level 2 candidates:**

- **L2 · Work queue systems** — The pattern for distributing discrete units of work across a pool of workers — the foundation of most background processing systems and the source of most at-least-once delivery complexity.
- **L2 · Event-driven batch processing** — Composing batch pipelines from discrete event-processing stages (copier, filter, splitter, merger) — the pattern that makes data pipelines modular and recomposable.
- **L2 · Coordinated batch processing** — Multi-stage computation with synchronisation barriers — the pattern for reduce operations, image processing pipelines, and any computation where later stages depend on the completion of earlier ones.
- **L2 · Kafka as a pipeline primitive** — How partitioned logs replace point-to-point queues as the connective tissue of distributed batch and stream systems — and what that architectural choice enables and costs.

---

### Group 3 — Data Systems Design
*Kleppmann's contribution is the deepest technical treatment of how data moves, persists, and stays consistent at scale. Where Burns gives you structural patterns, Kleppmann gives you the theoretical foundations and failure modes of the data layer — the part of every system where the hardest consistency and reliability problems actually live.*

---

#### L1-10 · Foundations of Data Systems

**What it is and why it matters:** Kleppmann opens by establishing what it means for a data system to be reliable, scalable, and maintainable — not as marketing claims but as engineering properties with precise definitions and measurable tradeoffs. Reliability means the system works correctly even when things go wrong. Scalability means there are strategies for coping with growth. Maintainability means future engineers can work with the system without misery. These three properties are in tension — and making that tension explicit is the first move in designing systems that hold up in production rather than systems that hold up in demos.

**Level 2 candidates:**

- **L2 · Reliability, scalability, maintainability defined** — The precise engineering definitions of the three properties that every data system must balance — and why optimising for all three simultaneously is impossible and the tradeoffs must be made explicit.
- **L2 · Describing load and performance** — The tools for measuring and communicating system behaviour — percentiles, latency distributions, throughput — and why averages lie about the experience of real users under real load.
- **L2 · Data models and query languages** — How the choice of data model (relational, document, graph) shapes what queries are natural and what queries are painful — the decision that determines the access patterns your system can serve efficiently.
- **L2 · Encoding and data evolution** — How data serialised today must be readable by code written tomorrow — forward and backward compatibility, schema evolution, and why this problem is harder than it looks.

---

#### L1-11 · Storage and Retrieval

**What it is and why it matters:** The data structures that power databases are not implementation details — they are the architectural choices that determine what operations are fast, what operations are expensive, and what failure modes are possible. Kleppmann's treatment of hash indexes, SSTables, LSM-trees, and B-trees is not academic: it is the conceptual foundation for understanding why different databases make different performance claims, why write-heavy and read-heavy workloads call for different storage engines, and why column-oriented storage exists at all. Without this layer, database selection is folklore.

**Level 2 candidates:**

- **L2 · Hash indexes** — The simplest persistent index — O(1) lookups, append-only writes — and the constraints (must fit in memory, no range queries) that make it unsuitable beyond narrow use cases.
- **L2 · SSTables and LSM-trees** — The storage engine architecture behind write-optimised databases (Cassandra, RocksDB, LevelDB) — understanding the compaction model explains both the write performance and the read amplification tradeoff.
- **L2 · B-trees** — The storage engine architecture behind read-optimised databases (PostgreSQL, MySQL) — the data structure that makes range queries efficient and the reason most relational databases converge on it.
- **L2 · OLTP vs OLAP** — The architectural distinction between transactional and analytical workloads — and why the same database optimised for one will underperform catastrophically on the other.
- **L2 · Column-oriented storage** — The storage model optimised for analytical queries over wide tables — and why it is architecturally incompatible with transactional workloads despite appearing to store the same data.

---

#### L1-12 · Replication

**What it is and why it matters:** Replication — keeping copies of data on multiple machines — is the foundational technique for both fault tolerance and read scalability in distributed data systems. Kleppmann's treatment is the most rigorous available outside of academic papers: single-leader, multi-leader, and leaderless replication each make different guarantees, expose different failure modes, and require different application-level reasoning. Replication lag is not a performance metric — it is a correctness concern. Understanding the failure modes of each replication model is what separates engineers who configure databases from engineers who reason about data consistency.

**Level 2 candidates:**

- **L2 · Single-leader replication** — The simplest replication model — all writes go to one node, reads can go anywhere — and the failure modes that make "simplest" not mean "safest."
- **L2 · Replication lag and its consequences** — The window between a write and its propagation to replicas — and the application-level anomalies (reading your own writes, monotonic reads, consistent prefix reads) that appear when applications don't account for it.
- **L2 · Multi-leader replication** — Allowing writes at multiple nodes simultaneously — the model that enables multi-datacenter writes and offline clients — and the write conflict problem it introduces that single-leader replication avoids.
- **L2 · Leaderless replication** — The Dynamo-style model where any node can accept writes — the model behind Cassandra and Riak — and the quorum arithmetic that determines what consistency guarantees are actually achievable.
- **L2 · Conflict resolution strategies** — Last-write-wins, merge functions, and application-level resolution — the design choices that determine what "consistency" actually means for a given application when conflicts are unavoidable.

---

#### L1-13 · Partitioning and Transactions

**What it is and why it matters:** Partitioning (sharding) is the technique that enables data systems to scale beyond what a single machine can store or serve — splitting data across nodes so that each node owns a subset. Transactions are the mechanism that maintains correctness when multiple operations must succeed or fail together. These two topics belong together because partitioning introduces exactly the problems that transactions exist to solve — and distributed transactions are the hardest correctness problem in data systems engineering. Kleppmann's treatment of serializability, isolation levels, and the actual cost of ACID guarantees is the most practically useful treatment available.

**Level 2 candidates:**

- **L2 · Partitioning strategies** — Range partitioning vs. hash partitioning — the choice that determines whether range queries or even distribution takes priority, and why you cannot fully optimise for both.
- **L2 · Secondary indexes and partitioning** — Why secondary indexes are harder to partition than primary keys — and the two approaches (local indexes and global indexes) that each trade query complexity for write complexity.
- **L2 · Rebalancing partitions** — How data moves between nodes as the cluster grows — and why rebalancing strategies that seem obvious (like mod N hashing) cause catastrophic data movement.
- **L2 · ACID properties in depth** — Atomicity, Consistency, Isolation, Durability — the precise meaning of each and why "ACID compliant" as a marketing claim tells you almost nothing about the actual guarantees.
- **L2 · Isolation levels** — Read committed, snapshot isolation, serializable — the spectrum from weakest to strongest — and the specific anomalies (dirty reads, write skew, phantom reads) that each level prevents or allows.
- **L2 · Serializability implementations** — Two-phase locking, serial execution, and serializable snapshot isolation — three different ways to achieve the strongest isolation guarantee and the performance tradeoffs each makes.

---

#### L1-14 · Consistency and Consensus

**What it is and why it matters:** This is the deepest theoretical layer in Kleppmann's book — and the one with the most direct practical implications. Consistency in distributed systems is not a binary property but a spectrum of guarantees, each with different performance and availability costs. Linearizability is the strongest guarantee (the system appears to have one copy of the data) — and Kleppmann proves it is incompatible with availability under network partition (the CAP theorem). Consensus algorithms — Paxos, Raft — are the mechanisms that make linearizability achievable in practice. Understanding this layer is what makes CAP theorem debates productive rather than circular.

**Level 2 candidates:**

- **L2 · Linearizability** — The strongest consistency guarantee — the system behaves as if there is a single copy of the data — and why achieving it in a distributed system requires coordination that has a real availability cost.
- **L2 · The CAP theorem precisely stated** — Not "pick two" but a precise statement about what is impossible under network partition — and why the theorem is more nuanced and less prescriptive than most presentations suggest.
- **L2 · Ordering guarantees** — Causality, sequence numbers, and Lamport clocks — the mechanisms for establishing "what happened before what" in a system with no global clock.
- **L2 · Consensus algorithms: Paxos and Raft** — The algorithms that let distributed nodes agree on a single value despite failures — and why Raft was designed specifically to be more understandable than Paxos without sacrificing correctness.
- **L2 · Distributed transactions and two-phase commit** — The protocol for achieving atomicity across multiple nodes — and why its failure modes (coordinator crash, blocking) make it impractical for many distributed systems that nominally require it.

---

#### L1-15 · Batch and Stream Processing at the Data Layer

**What it is and why it matters:** Kleppmann's Part III is about derived data — data that is computed from other data rather than written directly by users. Batch processing (MapReduce and beyond) and stream processing (event logs, change data capture) are the two paradigms for building systems where multiple data representations must stay in sync. This is the layer where most modern data architectures live — analytics pipelines, search indexes, caches, ML feature stores — and understanding the distinction between batch and stream is the prerequisite for reasoning about data freshness, consistency, and the architecture of systems that combine both.

**Level 2 candidates:**

- **L2 · MapReduce and the batch processing model** — The foundational batch processing paradigm — and why its simplicity (no shared state, deterministic outputs) makes it both powerful and limited.
- **L2 · Dataflow engines beyond MapReduce** — Spark, Flink, and the evolution beyond MapReduce — the architectural improvements (pipelining, in-memory processing) that address MapReduce's performance limitations.
- **L2 · Stream processing and messaging systems** — AMQP, JMS, and partitioned logs (Kafka) — and why the architectural choice between traditional message queues and log-based messaging has profound consequences for replayability and consumer independence.
- **L2 · Change Data Capture (CDC)** — The pattern for treating a database's write-ahead log as a stream of events — and why it is the most robust mechanism for keeping derived data systems in sync with a source of truth.
- **L2 · Combining batch and stream: the Lambda and Kappa architectures** — Two approaches to building systems that need both historical reprocessing and real-time processing — and the operational complexity each trades for its consistency guarantees.

---

### Group 4 — Systems Reasoning
*The synthesis layer. This group does not come from any single book — it is derived from the themes that run across all three. It is the difference between knowing patterns and being able to reason about systems you have never seen before. This is where architectural instinct is formalised.*

---

#### L1-16 · Tradeoff Reasoning

**What it is and why it matters:** Every architectural decision is a tradeoff — and the first law of software architecture (Richards & Ford) is that everything is a tradeoff. The discipline of tradeoff reasoning is the ability to make tradeoffs explicit: naming what is being gained, what is being given up, under what conditions the tradeoff is correct, and what would need to change for the decision to be revisited. Engineers who cannot articulate tradeoffs explicitly either inherit decisions they cannot explain or make decisions they cannot defend. This topic formalises the reasoning process that separates architectural thinking from preference-based decision-making.

**Level 2 candidates:**

- **L2 · The tradeoff matrix** — A structured approach to comparing architectural options across multiple characteristics — the tool that makes "it depends" into a specific and defensible answer.
- **L2 · Consistency vs. availability** — The most recurring tradeoff in distributed systems — and why the CAP theorem does not resolve it but forces it to be made explicit at the design level.
- **L2 · Scalability vs. simplicity** — The tradeoff that most premature optimisation violates — and the framework for knowing when the complexity of a scalable solution is justified by the actual load.
- **L2 · Coupling vs. autonomy** — The tradeoff behind every service decomposition decision — and why reducing coupling in one dimension (deployment) often increases it in another (data consistency).
- **L2 · Performance vs. correctness** — The tradeoff that weak isolation levels represent — and why choosing a weaker isolation level is an application-level correctness decision, not just a performance optimisation.

---

#### L1-17 · Failure Reasoning

**What it is and why it matters:** Systems fail. The question is not whether but how — and whether the failure is graceful or catastrophic, recoverable or permanent, visible or silent. Failure reasoning is the discipline of thinking about failure modes before they occur: mapping the ways a system can fail, understanding how failures propagate across components, and designing the system so that failures are contained, detectable, and recoverable. This runs across all three books — Burns on distributed failure patterns, Kleppmann on data system failures, Richards & Ford on architectural fitness functions — and it is the most direct expression of what "strong systems thinking instinct" means in production.

**Level 2 candidates:**

- **L2 · Partial failure and cascading failure** — The failure modes unique to distributed systems — where a subset of components fails and the failure propagates to components that were functioning correctly.
- **L2 · Failure domain analysis** — The practice of mapping which components fail together — and why architectural decisions about coupling are really decisions about failure domain boundaries.
- **L2 · The trouble with distributed clocks** — Why time is unreliable in distributed systems — and the specific correctness problems (ordering anomalies, stale reads) that arise when systems assume clocks are synchronised.
- **L2 · Byzantine faults** — Failures where components behave incorrectly rather than simply stopping — and the class of systems (safety-critical, blockchain) where tolerating byzantine faults is a design requirement.
- **L2 · Designing for recoverability** — The architectural properties — idempotency, exactly-once semantics, durable state — that make a system recoverable after failure rather than merely resilient while running.

---

#### L1-18 · Evolutionary Architecture

**What it is and why it matters:** Systems are not designed once and left unchanged — they evolve under changing requirements, changing load, changing team structures, and changing understanding. Evolutionary architecture is the discipline of designing systems that can change without breaking — and it runs directly against the instinct to over-engineer for anticipated future needs. Richards & Ford's fitness functions are one mechanism. Kleppmann's treatment of schema evolution and data compatibility is another. The common thread: the decisions that make systems easy to change today are different from the decisions that make systems correct today, and both must be made consciously.

**Level 2 candidates:**

- **L2 · Fitness functions as architectural tests** — Automated checks that verify architectural characteristics are maintained as the system evolves — the mechanism that makes architectural intent a continuous constraint rather than a document nobody reads.
- **L2 · Schema evolution and backward compatibility** — The practices that let data formats evolve without breaking existing readers or writers — and why this is an architectural concern, not a database administration detail.
- **L2 · The strangler fig pattern** — The migration strategy for incrementally replacing a legacy system without a big-bang rewrite — and why it works by creating a seam rather than a replacement.
- **L2 · Technical debt as architectural erosion** — The process by which small local decisions accumulate into structural degradation — and the practice of making debt visible and explicit rather than allowing it to silently erode architectural integrity.
- **L2 · Team topology and architecture** — Conway's Law and its inverse: systems reflect the communication structure of the teams that build them — and why organisational design is an architectural tool.

---

#### L1-19 · Cross-Layer Reasoning

**What it is and why it matters:** The most important skill this curriculum builds is the ability to reason across layers simultaneously. A data consistency problem is also a replication configuration decision (Group 3) which is also an architectural style choice (Group 1) which is also an operational failure mode (Group 4). Engineers who can only reason within a single layer will always be surprised by the consequences that appear in adjacent layers. This topic is the explicit practice of connecting the layers — reading a symptom at one level and tracing it to its root in another.

**Level 2 candidates:**

- **L2 · Tracing a failure across layers** — The practice of following a production failure from symptom to root cause across architectural, distributed systems, and data layers — the diagnostic skill that defines operational seniority.
- **L2 · Architectural style and data model alignment** — How the choice of architecture style (event-driven, microservices) constrains and is constrained by the choice of data model — and why misalignment between the two is a common source of accidental complexity.
- **L2 · Service boundaries and data ownership** — The decision about where service boundaries sit is inseparable from the decision about which service owns which data — and why getting this wrong produces the distributed monolith antipattern.
- **L2 · Consistency models and user experience** — How the consistency guarantee of the data layer surfaces as observable behaviour to users — and why eventual consistency is not just a database property but a product decision.
- **L2 · The cost of distributed transactions across layers** — How the need for cross-service transactions (architectural layer) drives complexity in the data layer (two-phase commit, sagas) that surfaces as operational risk — and how to reason about whether that cost is necessary.

---

## Sequencing note

The dependency chain across groups is real but not rigid. **Group 1 (Architectural Foundations)** should be established first — it provides the vocabulary and decision framework that makes everything in Groups 2 and 3 legible as choices rather than as givens. Without L1-01 through L1-05, the patterns in Groups 2 and 3 are a catalogue rather than a reasoning tool.

**Groups 2 and 3 can be worked in parallel** once Group 1 is in place. Burns and Kleppmann address adjacent layers of the same problem — compute and data — and reading them together reveals the connections that neither book makes explicit on its own. The most illuminating pairing is **L1-08 (Multi-Node Distributed Patterns)** with **L1-12 (Replication)** — these two topics address the same scalability problem from different angles and the synthesis is more valuable than either alone.

**Group 4 should not be started in isolation** — it is a synthesis layer and assumes the vocabulary of the first three groups. But individual Level 2 candidates in Group 4 can be visited earlier as reference points. **L1-17 (Failure Reasoning)** in particular is worth establishing early — having a failure reasoning framework changes how you read every pattern in Groups 2 and 3.

For a practitioner with production experience, the highest-leverage entry is **L1-03 (Modularity and Coupling)** — it is the concept most often felt but least often formalised by engineers who have worked inside large systems, and making it explicit unlocks the architectural vocabulary to reason about everything else. The second highest-leverage entry is **L1-14 (Consistency and Consensus)** — it is the theoretical layer that makes the most production surprises retroactively obvious.