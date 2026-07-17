# Cloud Infrastructure — Level 0: Course Map

> **Intent:** Cloud providers compete by wrapping the same underlying problems in different product names, consoles, and pricing models. A practitioner who learns the products learns one vendor. A practitioner who learns the underlying problems — what must be true of *any* system that rents compute, storage, and network to a stranger — can walk into AWS, GCP, Azure, Huawei Cloud, Alibaba Cloud, or a provider that doesn't exist yet, and immediately know what to look for. This map exists to build that second kind of knowledge.
>
> **Your angle:** You already operate these systems daily — this isn't a first exposure to compute, deployment, or observability. The gap this map targets is the layer *underneath* the console: knowing which invariant question a given feature is actually answering, so unfamiliar terminology resolves instantly into structure you already understand, instead of feeling like a new thing to learn from scratch.

---

## How to use this map

This is Level 0 — the terrain, not the trail. Each Level 1 topic below is a domain you could spend a week or a career in; the paragraph under it tells you *why it exists* and *what changes once you understand it*, not how to operate it. The Level 2 candidates under each are the specific sub-questions worth descending into — treat them as a menu, not a syllabus. Descend into a Level 2 candidate when a real system you're working with is currently a black box to you at that point, or when a Level 1 paragraph names a tradeoff you can't yet explain in your own words. If nothing here feels unresolved, you don't need to descend — the map has done its job by confirming you already own the territory.

---

## Topic Inventory

### Group A — Foundations: The Rented Primitives

Everything else in this map is built on top of four things you are, at root, renting from someone else: a place for code to run, a place for data to persist, a way for bytes to move between the two, and a way to prove who is allowed to touch any of it. These four are foundational not because they're simple, but because every other domain silently assumes you've already made decisions here.

#### L1-01 · Compute
What it is and why it matters: Before cloud, "compute" meant a physical machine you owned, racked, and depreciated over years — every abstraction since (VMs, containers, functions) exists to answer the same question with less ownership and more elasticity. Each generation of compute abstraction trades control for velocity: a VM gives you the OS but you patch it; a container gives you portability but you manage orchestration; a function gives you neither but you pay per invocation and accept cold starts. Understanding compute means understanding *where the line is drawn* between what the provider manages and what you do — because that line is where outages, cost surprises, and security gaps live. Once you can place any compute product on that spectrum, you can predict its failure modes before you've used it.

Level 2 candidates:
- **Provisioning models** — reveals why "serverless" isn't free of servers, just free of your visibility into them, and what you give up for that.
- **Scaling triggers** — explains why autoscaling based on CPU alone silently fails for I/O-bound workloads.
- **Instance lifecycle** — the difference between a crash you recover from and a crash that loses state, and why that difference is a design decision, not an accident.
- **Bin-packing and scheduling** — why your "guaranteed" capacity can still experience noisy-neighbor effects.
- **Interruptible vs. reserved capacity** — the economic logic behind why providers sell you the same hardware at wildly different prices depending on how much control you give up.
- **Shared responsibility boundary** — the line that shifts with every abstraction layer, and why "the provider handles it" and "you handle it" redraw themselves every time you move up the stack.
- **Tenant isolation guarantees** — what physically stops another customer's workload from touching yours, and why that guarantee gets weaker as density and cost efficiency go up.

#### L1-02 · Storage
What it is and why it matters: Storage abstractions diverged the moment workloads diverged — a video file, a bank transaction, and a filesystem mount have incompatible access patterns, and no single storage system optimizes for all three. The object/block/file split you see in every provider isn't arbitrary; it's a direct encoding of *how* data will be read and written, not just *how much* of it there is. What breaks people is assuming durability and consistency are the same guarantee — a system can lose zero bytes and still hand you stale reads. Once you understand which access pattern a storage product was built for, you can predict its consistency behavior without reading the fine print.

Level 2 candidates:
- **Object storage semantics** — why "eventually consistent" broke assumptions engineers didn't know they were making, and when it stopped mattering.
- **Block storage and IOPS** — the throughput ceiling that explains why a "bigger" disk sometimes performs worse.
- **File storage and shared mounts** — why concurrent-write semantics on a shared filesystem are the quiet source of the hardest bugs in distributed systems.
- **Managed databases** — what "managed" actually offloads (patching, failover) versus what it doesn't (schema design, query performance).
- **Backup, snapshot, and point-in-time recovery** — the difference between "we keep a copy" and "we can restore to any second," and why only one of those is usually true.

#### L1-03 · Networking
What it is and why it matters: Every cloud network is, underneath the product names, an answer to one question repeated at every layer: what is the default posture — open until closed, or closed until opened? Providers converged on private-by-default virtual networks because the alternative (public-by-default) produced a decade of breaches that were architecture failures, not code failures. Latency, too, is not a performance detail you optimize in code — it's a physical constraint set by where the provider chose to put a data center relative to where your users are. Once you understand networking as trust boundaries plus physical distance, every "why is this slow" or "why is this exposed" question resolves into one of those two things.

Level 2 candidates:
- **Isolation and segmentation** — why a single flat network was the default failure mode of early cloud adoption, and what replaced it.
- **Traffic routing and load balancing** — the difference between routing failure (nothing answers) and routing degradation (something answers, slowly).
- **Access control at the network layer** — why "firewall rules" are a blunt instrument compared to identity-based access, and when you still need them anyway.
- **DNS and service discovery** — the invisible layer that, when it fails, makes every other system look broken simultaneously.
- **Regions, zones, and physical locality** — why "multi-region" is a resilience decision and a latency decision that pull in opposite directions.

#### L1-04 · Identity & Access
What it is and why it matters: Every other domain in this map assumes a working answer to "who is this, and what are they allowed to do" — identity isn't one domain among ten, it's the precondition for the other nine. The shift from static credentials to short-lived, identity-bound access is the single biggest security lesson the industry learned the hard way: a leaked long-lived key is a breach with no natural expiry. Least-privilege isn't a compliance checkbox, it's a blast-radius decision made in advance of an incident you haven't had yet. Once you understand identity as "credential plus scope plus lifetime," you can evaluate any provider's IAM system by asking what happens when each of those three is compromised.

Level 2 candidates:
- **Authentication vs. authorization** — the distinction that explains why "logged in" and "allowed to do this" are separate failure points, not one.
- **Machine identity** — why code acting as an identity is a different threat model than a human acting as one, and why conflating them is a common mistake.
- **Least-privilege policy design** — the tradeoff between operational friction now and blast radius later.
- **Secrets and credential rotation** — why a secret that never expires is a liability the moment it's created, not the moment it leaks.
- **Federation and delegated trust** — how an organization avoids re-creating identity from scratch for every provider it uses.

---

### Group B — Operating What You've Rented

Once compute, storage, network, and identity exist, the next question is how code and change move through them safely and observably over time. This group is about *process* layered on top of the primitives — the difference between having infrastructure and running a system on it.

#### L1-05 · Deployment & Delivery
What it is and why it matters: Deployment used to mean someone manually copying files to a server at 2am; every practice in this domain exists to remove a human from that failure-prone loop. The shift to declarative infrastructure (describe the end state, let the system converge to it) over imperative scripting (describe the steps) is the same lesson computing has relearned in every domain: state drifts, and the fix is to make the *desired* state the source of truth, not the history of commands that produced it. Release strategies like canary and blue/green exist because "deploy" and "expose to all users" used to be the same event — separating them is what makes rollback possible before damage, not after. Once you see deployment as risk management rather than file transfer, every pipeline stage reveals which risk it's mitigating.

Level 2 candidates:
- **Declarative vs. imperative infrastructure** — why "it worked when I ran the script" and "it works" are different claims.
- **Progressive delivery** (canary, blue/green) — the mechanism that turns "deploy" from a single irreversible event into a reversible gradient.
- **Artifact immutability** — why rebuilding "the same" deployment from source twice is a bug, not a feature.
- **Rollback vs. roll-forward** — the difference between undoing a change and deploying a fix, and why the wrong choice under pressure makes incidents worse.
- **Environment parity** — the specific ways dev/staging/prod quietly diverge, and why that divergence is where "works on my machine" incidents are born.

#### L1-06 · Observability
What it is and why it matters: Logging, metrics, and tracing look like three separate tools but answer three different questions that all matter during an incident: what happened (logs), how much and how often (metrics), and where in a distributed call chain did it happen (traces). Distributed tracing specifically exists because the old debugging model — read the logs on the one server that's broken — stopped working the moment a single request started touching a dozen independent services. The real skill isn't collecting this data, which every provider does by default now; it's knowing which of the three to reach for first when something is on fire. Once you understand observability as answering "is it broken," "how broken," and "where," you can evaluate any provider's tooling by which of those three questions it actually answers well.

Level 2 candidates:
- **Structured logging** — why unstructured log lines become unqueryable the moment your system has more than one instance.
- **Metrics and SLIs/SLOs** — the difference between a number that describes the system and a number that tells you when to page someone.
- **Distributed tracing** — how a single slow request gets attributed to the one service actually responsible, in a chain of a dozen.
- **Alert design** — why more alerts produce worse incident response, not better, past a certain threshold.
- **Push vs. pull telemetry** — the architectural tradeoff behind why some systems must be scraped and others must be shipped to.

#### L1-07 · Reliability & Resilience
What it is and why it matters: Every reliability pattern is a pre-negotiated answer to a failure that hasn't happened yet — retries, circuit breakers, and multi-zone redundancy all trade some cost or complexity today for a smaller blast radius later. The uncomfortable truth this domain forces on you is that failure isn't prevented, it's contained; the question is never "will this fail" but "what fails with it when it does." RPO and RTO exist as concepts because "we have backups" is meaningless without knowing how much data you'd lose and how long you'd be down — two numbers most teams don't actually know until an incident forces them to find out. Once you think in blast radius rather than uptime percentage, you can evaluate any resilience feature by what it actually contains.

Level 2 candidates:
- **Blast radius** — why "highly available" without a defined failure boundary is a marketing claim, not an architecture.
- **Retries, backoff, and circuit breakers** — the difference between a retry that helps and a retry storm that takes down the thing you were trying to protect.
- **Redundancy across zones and regions** — why redundancy that shares a failure domain (same power, same network) isn't redundancy at all.
- **RPO and RTO** — the two numbers that turn "we have a disaster recovery plan" from a claim into a testable commitment.
- **Chaos and load testing** — why resilience assumptions that were never tested under failure are indistinguishable from hope.

---

### Group C — Systems Thinking Across Boundaries

Once you're operating more than one service, new problems appear that don't exist at the single-service level — how independent systems communicate without becoming one fragile system, and how resource usage translates into cost across a whole organization instead of one machine.

#### L1-08 · Data & Integration
What it is and why it matters: A single monolith doesn't need a messaging layer — integration patterns exist precisely because splitting a system into independent services creates a new problem the monolith never had: how do parts that don't share memory or a deploy cycle stay coordinated? The synchronous-vs-asynchronous choice is the central fork in this domain, because a caller that waits couples its own reliability to the reliability of everything downstream, while a caller that doesn't wait has to answer a harder question: what happens to a message that fails, twice removed from the code that sent it. API contracts and schemas exist to let two teams change their systems independently without a phone call — the discipline here is really about organizational boundaries as much as technical ones. Once you see integration as "how do independently-deployed things stay coordinated," you can predict where a distributed system will break under change.

Level 2 candidates:
- **Synchronous vs. asynchronous communication** — the coupling tradeoff that determines whether one slow service can take down five others.
- **Pub-sub and event-driven design** — why decoupling producers from consumers changes what "the system is down" even means.
- **Dead-letter and failure handling** — what happens to work that can't be completed, and why silently dropping it is worse than most alternatives.
- **API gateways and rate limiting** — the boundary that protects a system from its own popularity.
- **Schema and contract versioning** — how two teams change their services independently without breaking each other, and what happens when they don't do this deliberately.

#### L1-09 · Cost & Resource Management
What it is and why it matters: Cloud pricing looks like a billing detail but is actually a second description of your architecture — every cost line item is a resource decision someone made, often without realizing they were making a financial one. The core tension in this domain is between provisioned cost (you pay whether you use it or not) and consumption cost (you pay only for what you use), and most real cost problems are a mismatch between which model a workload actually fits and which model it was put on. Attribution — knowing which team or feature a cost belongs to — sounds like bureaucracy but is what makes "is this worth it" an answerable question instead of a guess. Once you see cost as an architectural signal rather than a finance-team concern, wasteful spend becomes visible as a design smell, not just a number on an invoice.

Level 2 candidates:
- **Provisioned vs. consumption pricing** — the mismatch that explains most "why is this so expensive" surprises.
- **Egress and data-transfer pricing** — why moving data out is priced differently from moving it in, and why that asymmetry is the real mechanism behind vendor lock-in, not a technical limitation.
- **Rightsizing** — why the instinct to over-provision "to be safe" is itself a recurring cost, not a one-time buffer.
- **Idle and orphaned resources** — how cost accumulates silently from things nobody is actively using or even aware exist.
- **Tagging and attribution** — why cost without ownership is unaccountable, and unaccountable cost never gets fixed.
- **Quotas and budget guardrails** — the difference between a cost control that prevents a mistake and one that only reports it after the fact.

---

### Group D — Governance & Trust

The last domain sits slightly apart from the others: it isn't about making systems work, it's about being able to *prove* how they worked, to auditors, regulators, or your future self during an incident review. It depends on everything above — you can't govern access you haven't modeled, or prove compliance for data you can't locate.

#### L1-10 · Compliance & Governance
What it is and why it matters: Compliance requirements — data residency, encryption, audit trails — exist because "trust us" stopped being an acceptable answer once cloud infrastructure started holding regulated data (health records, financial transactions, government data) at scale. The distinction that matters most here is between a control enforced by *policy* (a rule that can be violated and then caught) and one enforced by *architecture* (a rule that structurally cannot be violated) — the former is cheaper to implement and weaker; the latter is the opposite. Data residency specifically is a reminder that "the cloud" is not placeless — every byte sits on a physical disk in a physical jurisdiction, and that fact has legal consequences independent of anything in your code. Once you understand governance as "what can be proven, to whom, after the fact," you can evaluate any provider's compliance posture by what it actually makes provable versus what it merely promises.

Level 2 candidates:
- **Data residency** — why "the cloud" still has a physical location that carries legal weight, regardless of how abstract the product feels.
- **Encryption at rest and in transit** — the difference between data that's protected from an attacker and data that's protected from the provider itself.
- **Key management** — why who holds the encryption key is a more consequential question than whether encryption exists at all.
- **Audit trails** — the record that turns "we believe this didn't happen" into "we can show this didn't happen."
- **Policy-as-code vs. architectural enforcement** — the tradeoff between a guardrail that's easy to add and one that's actually hard to break.

---

## Sequencing note

The dependency chain runs roughly Group A → Group B → Group C, with Group D (Governance & Trust) sitting alongside all three rather than after them — you can't govern access you haven't modeled in L1-04, or prove data residency for storage you haven't understood in L1-02. Within Group A, Identity & Access (L1-04) is arguably the highest-leverage entry point despite being listed last: it's the one primitive every other domain silently assumes is already solved, and it's the domain where provider terminology diverges most confusingly (roles, policies, service accounts, workload identities) while the underlying question — who is acting, and what can they do — stays identical everywhere.

For a practitioner returning to foundations with existing hands-on experience, the fastest path to new insight is usually **not** Group A — you likely already have working intuition for compute, storage, and networking from daily use. The higher-leverage descent is into Group C (Data & Integration, Cost & Resource Management), where the failure modes are organizational and cross-system rather than single-machine, and where experience with one service in isolation doesn't automatically transfer. Group D is worth a deliberate pass even if it feels adjacent to "real" engineering work — it's the domain most often learned reactively, during an audit or an incident, rather than proactively.