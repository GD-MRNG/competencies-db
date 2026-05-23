# Software Engineering (From Coder to Engineer) — Level 0: Course Map

> **Intent:** To close the gap between writing code and engineering software. Software is not valuable when it is written — it is valuable when it is running. Everything between a developer typing a line of code and a user benefiting from it is the domain of operational engineering. This curriculum maps that domain in full.
>
> **Your angle:** You have been writing software for years and can ship features. What this curriculum builds is the layer underneath: the mental models that explain *why* deployments fail, *why* systems degrade under load, *why* architectural decisions made in one tier produce consequences in another. The goal is not to learn more tools — it is to become someone who can reason across the full lifecycle of a running system, not just the part where code is written.

---

## How to use this map

The three tiers are **concentric, not sequential.** Tier 1 is the ground — the physics of how software runs. Tier 2 is the assembly line built on that ground — how code becomes a deployed artifact. Tier 3 is the continuous disciplines that apply at every stage — what separates reliable systems from fragile ones.

Most real problems span multiple tiers simultaneously. A deployment failure might originate in a networking misconfiguration (T1), be discovered because of a missing health check (T3), and be hard to roll back because of an incompatible database migration (T2). The ability to reason across tiers simultaneously is what the curriculum defines as operational seniority.

Each **Level 1 topic** is a concept post: what it is, why it matters, where it sits in the larger picture. Each **Level 2 candidate** is a depth post: the mechanics, the tradeoffs, where it breaks. Descend into Level 2 only for sub-concepts where deeper understanding is actively blocking your reasoning.

---

## Topic Inventory

---

### Tier 1 — Foundational Knowledge
*The mental models that must be in place before the rest of the map makes sense. Gaps here don't manifest as "I don't know how to configure X" — they manifest as "I don't understand why anything is failing and I don't know where to start."*

---

#### L1-01 · Networking Fundamentals

**What it is and why it matters:** Every distributed system is a networked system, and most production failures have a networking dimension even when they don't look like it. This topic establishes the mental model for how packets move, how names resolve to addresses, how connections are established and secured, and how traffic is shaped at boundaries. Without it, tools like load balancers, service meshes, and firewalls are configuration rituals rather than reasoned decisions. The OSI model is not trivia — it is a layered map that tells you where to look when something breaks.

**Level 2 candidates:**

- **L2 · The OSI Model and TCP/IP Stack** — Understanding the layers tells you which tool operates at which level of abstraction — and why a problem visible at Layer 7 can be caused by something at Layer 3.
- **L2 · IP Addressing and Subnetting (CIDR)** — Without this, network segmentation, VPC design, and firewall rules are guesswork; with it, they become legible decisions about who can reach what.
- **L2 · DNS: The Resolution Chain** — DNS failures are among the most common and most misdiagnosed production incidents — drilling here reveals the full resolution chain so you can trace where it breaks.
- **L2 · TCP vs UDP: The Reliability Tradeoff** — Every protocol built on top of these made a deliberate choice; understanding the tradeoff explains why HTTP, DNS, and video streaming each chose differently.
- **L2 · HTTP and TLS: The Application Layer in Detail** — The protocol your services speak every second — understanding it at depth reveals why latency, retries, and certificate failures behave the way they do.
- **L2 · Load Balancing: Layer 4 vs Layer 7** — The distinction between routing connections and routing requests explains why the choice of load balancer determines what you can and cannot do with traffic shaping.
- **L2 · Network Security Boundaries: Firewalls, Security Groups, and NACLs** — These are the enforcement points of network policy — understanding how they differ tells you which layer a security misconfiguration actually lives in.
- **L2 · NAT and Private Networking** — The mechanism that lets private networks reach the internet without being directly exposed — essential for reasoning about egress, connectivity failures, and cloud network topology.

---

#### L1-02 · Compute Abstractions

**What it is and why it matters:** Physical hardware is never what software actually runs on — there are always layers of abstraction between the code and the silicon. Each layer (virtual machines, containers, serverless) trades isolation for overhead, flexibility for constraint. Understanding what each abstraction actually does — how containers isolate processes, how orchestrators schedule work, how serverless shifts operational responsibility — is what lets you choose the right compute model for a given problem rather than defaulting to whatever the team used last time.

**Level 2 candidates:**

- **L2 · Virtual Machines and the Hypervisor Model** — The first major abstraction layer above hardware — understanding it explains the performance ceiling containers were invented to break through.
- **L2 · Containers: Namespaces, cgroups, and the Isolation Model** — Containers are not lightweight VMs; they are isolated processes — drilling here reveals exactly what is and is not isolated, which is where most container security misconceptions live.
- **L2 · The Container Image: Layers, Registries, and Immutability** — The image is the unit of deployment in containerised systems — understanding its layered structure explains build caching, image bloat, and supply chain attack surfaces.
- **L2 · Container Orchestration: The Scheduling Problem** — Orchestrators like Kubernetes exist to solve one hard problem: placing workloads on machines efficiently under changing conditions — understanding the scheduling model explains most Kubernetes operational behaviour.
- **L2 · Serverless and the Event-Driven Compute Model** — Serverless shifts the unit of billing and scaling from machines to invocations — understanding what that shift costs and buys prevents it from being adopted as a trend rather than a decision.
- **L2 · Compute Resource Models: CPU, Memory, and I/O as First-Class Constraints** — Resource limits and requests are not bureaucratic configuration — they are the language the scheduler uses to place workloads safely, and misconfiguring them is the source of most resource-related production incidents.

---

#### L1-03 · Service Architecture Awareness

**What it is and why it matters:** Before a line of code is deployed, architectural decisions have already determined what failure modes are possible, how services will find each other, and whether the system will degrade gracefully or catastrophically. This topic is about reading and reasoning about those decisions — understanding the spectrum from monolith to microservices, the implications of sync vs async communication, and why distributed systems fail in ways that single-process systems do not. You do not need to design architectures here; you need to understand the one you are operating inside.

**Level 2 candidates:**

- **L2 · The Monolith vs Microservices Spectrum** — The choice is not binary, and each point on the spectrum creates a different set of operational problems — understanding the tradeoffs prevents cargo-culting microservices as the default.
- **L2 · Synchronous vs Asynchronous Communication** — The choice between request-response and event-driven communication determines how failure propagates — sync failures are immediate and visible; async failures are delayed and silent.
- **L2 · The API as a Contract: REST, gRPC, and Event Schemas** — APIs are not implementation details but commitments between services — drilling here reveals why breaking changes in an API break systems that appear unrelated.
- **L2 · Service Discovery: How Services Find Each Other** — In dynamic environments where IPs change constantly, service discovery is the infrastructure that replaces hardcoded addresses — understanding it explains a category of connectivity failures that are otherwise mysterious.
- **L2 · Idempotency and Distributed State** — In a system where messages can be delivered more than once, idempotency is the property that prevents duplicate operations from corrupting state — the concept that makes retry-safe design possible.
- **L2 · The Data Ownership Problem: Why Shared Databases Break Service Independence** — A shared database is a hidden coupling point that makes services impossible to deploy or scale independently — understanding this explains why the microservices migration always gets stuck on the database.
- **L2 · Failure Modes in Distributed Systems: Partial Failure and Cascading Failure** — Distributed systems don't fail completely — they fail partially, and partial failures can cascade in ways that are harder to reason about than total failures.

---

### Tier 2 — Core Lifecycle Stages
*The assembly line. Code enters as text in a developer's editor and exits as a running, validated, observable process in production. Every stage is a potential bottleneck, quality gate, or failure point.*

---

#### L1-04 · Source Control and Collaboration

**What it is and why it matters:** The assembly line begins here. Source control is not just a backup mechanism — it is the foundation of every other practice in the lifecycle. Branching strategies determine how teams integrate work and how frequently. The pull request is the primary quality gate before code reaches CI. Understanding the Git object model — not just the commands — is what lets you recover from merge disasters and reason about what a rebase or squash actually does to history. Every downstream problem that originates in "we can't deploy because the branch is broken" traces back to decisions made here.

**Level 2 candidates:**

- **L2 · The Git Object Model: Commits, Trees, and Refs** — Git's commands are only legible once you understand the DAG underneath them — this is the model that makes rebasing, cherry-picking, and recovering from mistakes predictable rather than terrifying.
- **L2 · Branching Strategies: Trunk-Based Development vs GitFlow** — The branching strategy determines how frequently code integrates and how long bugs stay hidden — trunk-based development and GitFlow represent two fundamentally different theories about where risk lives.
- **L2 · Merge Strategies: Merge Commits, Rebase, and Squash** — Each merge strategy produces a different history and a different set of tradeoffs around bisectability, authorship, and rollback — the choice matters more than most teams realise.
- **L2 · The Pull Request as a Quality Gate** — The PR is the point where code transitions from individual to collective — understanding its role as a quality gate rather than a formality changes how you structure reviews and what you look for.
- **L2 · Conflict Resolution: Textual vs Semantic Conflicts** — Textual conflicts are what Git surfaces; semantic conflicts are what Git misses — understanding the difference explains why passing CI on a merge is not the same as correctness.
- **L2 · Monorepo vs Polyrepo: Repository Structure as an Architectural Decision** — The choice of repository structure is a decision about coupling, tooling overhead, and team autonomy — it has downstream consequences for CI, dependency management, and deployment.

---

#### L1-05 · Testing Strategy

**What it is and why it matters:** Testing is not about coverage numbers — it is about building confidence at the right level of the stack, at the right cost, at the right speed. The testing pyramid exists because different tests answer different questions and carry different costs. A codebase with 90% unit test coverage can still fail catastrophically in production if integration and contract surfaces are untested. Understanding testing as a *strategy* — a deliberate allocation of confidence-building effort — is what separates engineers who write tests from engineers who design testable systems.

**Level 2 candidates:**

- **L2 · The Testing Pyramid: Cost, Speed, and Coverage as a Design Constraint** — The pyramid is a resource allocation model — understanding it explains why a test suite with too many E2E tests is a reliability problem, not just a speed problem.
- **L2 · Test Doubles: Mocks, Stubs, Fakes, and Spies** — The distinctions between these are not pedantic — each one makes different guarantees and introduces different risks, and conflating them leads to tests that pass while the system breaks.
- **L2 · What Test Coverage Measures and What It Misses** — Coverage measures lines executed, not behaviour verified — drilling here prevents coverage targets from becoming a false signal of system correctness.
- **L2 · Contract Testing: How Services Agree on Interfaces** — Contract tests are the mechanism that lets services evolve independently without silently breaking each other — the practice that makes microservices deployable in practice, not just in theory.
- **L2 · Testing in Production: Feature Flags, Canary Analysis, and Observability as Tests** — Some properties can only be tested under real load with real users — understanding this reframes production monitoring as a testing discipline rather than a failure response.
- **L2 · The Cost of Flaky Tests** — A flaky test is not a minor inconvenience — it is a trust corrosion mechanism that causes engineers to ignore CI failures, which is the exact behaviour CI exists to prevent.

---

#### L1-06 · Continuous Integration (CI)

**What it is and why it matters:** CI is a discipline before it is a tool. The discipline: every developer integrates their work into the shared codebase frequently — ideally daily — and every integration is validated automatically. The tool is just the automation that makes this feedback fast enough to be useful. Teams that run a CI tool without the discipline get the overhead without the benefit: long-lived branches, large merges, and build failures that nobody owns. Understanding CI as a practice first is what makes the tooling decisions legible.

**Level 2 candidates:**

- **L2 · What CI Actually Means: The Discipline vs the Tool** — The discipline of frequent integration is the point — the tool only works if the discipline is in place, and conflating the two explains why many teams have CI pipelines but not CI.
- **L2 · The Anatomy of a CI Pipeline: Triggers, Stages, and Feedback Loops** — Understanding how a pipeline is structured — what triggers it, how stages gate each other, where feedback surfaces — is the prerequisite for designing pipelines that are fast and trustworthy rather than slow and ignored.
- **L2 · Build Reproducibility: Why the Same Source Should Always Produce the Same Artifact** — A build that produces different outputs from the same inputs is a pipeline that cannot be trusted — drilling here reveals the sources of non-determinism and why eliminating them matters.
- **L2 · Fast Feedback as a Design Constraint** — A CI pipeline that takes 45 minutes to run will be worked around rather than waited for — speed is not a nice-to-have but a behavioural constraint on how developers actually integrate.
- **L2 · The CI/CD Boundary: What CI Produces and Where It Goes** — CI ends with a validated artifact; CD begins with that artifact — understanding the handoff clarifies responsibilities and reveals where most pipeline failures are actually misclassified.

---

#### L1-07 · Artifact and Dependency Management

**What it is and why it matters:** The artifact — a container image, a JAR, a compiled binary — is the actual unit of deployment, not the source code. Understanding what an artifact is, how it is versioned, and where its dependencies come from is foundational to reasoning about reproducibility, security, and the supply chain. Most teams have fragile artifact practices until a dependency vulnerability or a broken transitive dependency makes the cost visible. By then, the remediation is expensive.

**Level 2 candidates:**

- **L2 · What an Artifact Is: The Unit of Deployment** — The shift from "deploying code" to "deploying artifacts" is the shift that makes deployments reproducible — understanding the distinction clarifies why rebuilding from source in production is a failure mode.
- **L2 · Semantic Versioning: What a Version Number Communicates** — SemVer is a contract about compatibility — understanding what MAJOR, MINOR, and PATCH signal is the prerequisite for reasoning about whether a dependency upgrade is safe.
- **L2 · Dependency Graphs and Transitive Dependencies** — The dependencies you declare are not the only dependencies you ship — drilling here reveals the hidden complexity of transitive graphs and why a single version bump can change dozens of packages.
- **L2 · Artifact Registries: Storage, Distribution, and Promotion** — Registries are not just storage — they are the mechanism by which artifacts move through environments and by which promotion policies are enforced.
- **L2 · Dependency Pinning vs Version Ranges: The Reproducibility Tradeoff** — Pinning guarantees reproducibility at the cost of manual updates; ranges accept non-determinism in exchange for automatic patches — the tradeoff determines how your build behaves six months from now.
- **L2 · Supply Chain Security: Why Your Dependencies Are Your Attack Surface** — The SolarWinds and Log4Shell incidents made visible what was always true: your attack surface includes every package your build pulls in — understanding this reframes dependency management as a security practice.

---

#### L1-08 · Continuous Delivery and Deployment (CD)

**What it is and why it matters:** Continuous Delivery means the artifact is always in a state that *could* be deployed to production. Continuous Deployment means it is deployed automatically. The distinction matters enormously — one is a capability, the other is a policy. Most of the engineering work in CD is about making deployment safe at any frequency: choosing the right deployment strategy, managing the environment pipeline, and deciding how to handle a bad release once it is live. The philosophy here — roll back vs roll forward — is a design decision with real operational consequences.

**Level 2 candidates:**

- **L2 · Delivery vs Deployment: The Most Important Distinction in CD** — Conflating these two leads to teams that think they have CD because they have automation, when what they have is fast deployment of unvalidated artifacts — the distinction clarifies what the practice is actually trying to achieve.
- **L2 · Deployment Strategies: Blue/Green, Canary, Rolling, and Recreate** — Each strategy makes a different tradeoff between blast radius, rollback speed, resource cost, and complexity — choosing blindly is choosing to accept the worst tradeoffs of each.
- **L2 · The Environment Pipeline: Promoting an Artifact Through Stages** — The environment pipeline is the mechanism by which confidence accumulates before production — understanding it explains why environment parity matters and why staging failures that don't match production failures are a pipeline design problem.
- **L2 · Rollback vs Roll Forward: Two Philosophies for Handling Bad Releases** — Rolling back assumes the previous state is safe; rolling forward assumes it is faster to fix than to revert — the right choice depends on the nature of the failure and the cost of each path.
- **L2 · The Release as a Decoupled Event: Feature Flags and Dark Launches** — Separating deployment from release — shipping code dark and enabling it separately — is the practice that removes the most risk from any individual deployment.

---

#### L1-09 · Configuration and Feature Management

**What it is and why it matters:** A single artifact must behave differently in development, staging, and production without being rebuilt for each environment. Configuration is the mechanism that enables this — and its mismanagement is the source of a specific category of production incidents: the environment that works in staging but breaks in production because a configuration value was wrong, missing, or hardcoded. Secrets are a special case of configuration that carry security implications if mishandled. Feature flags extend this model into a runtime control plane that decouples deployment from behaviour.

**Level 2 candidates:**

- **L2 · The Twelve-Factor Config Principle: Why Configuration Is Not Code** — The principle that configuration belongs in the environment rather than in the codebase is the rule whose violation explains the majority of environment-specific failures.
- **L2 · Configuration Hierarchy and Override Models** — Real systems have configuration at multiple layers — defaults, environment overrides, secrets — understanding the hierarchy is what lets you reason about which value wins and why.
- **L2 · Secrets Management: Why Secrets Are Different from Configuration** — Secrets require rotation, audit trails, and access controls that general configuration does not — treating them the same way is the practice that puts credentials in version control.
- **L2 · Feature Flags: The Full Operational Model** — Feature flags are not just toggle switches — they are a runtime control plane with their own lifecycle, debt accumulation, and failure modes that must be managed explicitly.
- **L2 · Configuration Drift: How Reality Diverges from Declared State** — Drift is the accumulation of untracked manual changes — understanding how it happens and how to detect it is the prerequisite for trusting that your environments are what you think they are.

---

#### L1-10 · Infrastructure as Code (IaC)

**What it is and why it matters:** IaC is the practice of defining infrastructure — servers, networks, databases, permissions — as versioned, reviewable code rather than as manual console clicks. The foundational shift is from imperative ("do these steps") to declarative ("this is the desired state") — a shift that makes infrastructure reproducible, auditable, and subject to the same review and testing practices as application code. The risks are also real: state files become sources of truth that must be protected, and drift between declared and actual state is a slow-moving reliability hazard.

**Level 2 candidates:**

- **L2 · Declarative vs Imperative Infrastructure: The Model That Changes Everything** — The declarative model — describing what you want rather than how to get it — is what makes IaC reproducible across environments and recoverable after failure.
- **L2 · State: The Source of Truth and Source of Risk** — The state file is what lets IaC tools know what already exists — understanding its role explains why state corruption is one of the most dangerous failure modes in IaC and why remote state with locking is not optional.
- **L2 · Idempotency: Why Applying Twice Must Be Safe** — An IaC apply that is not idempotent cannot be safely re-run after a partial failure — this property is the guarantee that makes automated infrastructure management trustworthy.
- **L2 · The Plan/Apply Cycle: Preview as a Safety Mechanism** — The plan step — showing what will change before changing it — is the mechanism that makes infrastructure changes reviewable and the primary safeguard against destructive accidents.
- **L2 · Modules and Code Reuse in Infrastructure** — Modules are the abstraction mechanism of IaC — understanding how to design them well is the difference between infrastructure that scales to large teams and infrastructure that becomes a copy-paste nightmare.
- **L2 · Drift Detection: When Reality Diverges from Code** — Drift — infrastructure that has changed outside of IaC — is the silent erosion of the guarantees IaC exists to provide; detecting it is the practice that keeps the declared state trustworthy.

---

### Tier 3 — Cross-Cutting Disciplines
*These practices don't belong to any single lifecycle stage — they apply continuously across all of them. They are the difference between a system that works and a system that is reliable, secure, and sustainable over time.*

---

#### L1-11 · Observability and Monitoring

**What it is and why it matters:** A system you cannot observe is a system you cannot operate. Monitoring tells you when something you already expected to break has broken. Observability tells you why something you didn't anticipate is behaving unexpectedly — the unknown unknowns. The distinction matters because production systems fail in ways their designers did not predict, and the ability to ask arbitrary questions of a running system is what separates engineers who can debug novel failures from those who can only respond to known alerts. The three pillars — metrics, logs, traces — are not interchangeable; each answers a different class of question.

**Level 2 candidates:**

- **L2 · Monitoring vs Observability: Known Unknowns vs Unknown Unknowns** — Monitoring checks the things you thought to instrument; observability lets you interrogate the things you didn't — understanding the distinction determines what you build when you instrument a system.
- **L2 · The Three Pillars: Metrics, Logs, and Traces** — Each pillar answers a different question about system behaviour — metrics tell you what happened, logs tell you what was recorded, traces tell you where time went across service boundaries.
- **L2 · Metrics: Counters, Gauges, Histograms, and What Gets Lost in Aggregation** — Aggregating metrics loses information — understanding which metric types preserve what properties is the difference between alerting that catches real problems and alerting that averages them away.
- **L2 · Distributed Tracing: How Requests Travel Across Service Boundaries** — In a microservices system, a single user request may touch dozens of services — tracing is the only tool that makes the full path visible and latency attributable to a specific component.
- **L2 · The SLI/SLO/SLA Framework: Defining Reliability from the User's Perspective** — SLOs are the mechanism by which reliability becomes a measurable engineering commitment rather than a vague aspiration — understanding the framework is the prerequisite for having a meaningful conversation about what "reliable" means.
- **L2 · Alerting Philosophy: Symptoms Over Causes, and the Cost of Alert Fatigue** — Alerting on causes produces noise; alerting on symptoms produces signal — and alert fatigue is the failure mode where too much noise causes real failures to be ignored.

---

#### L1-12 · Security (DevSecOps)

**What it is and why it matters:** Security is not a gate at the end of the delivery pipeline — it is a property of how systems are designed and built continuously. The shift left principle: the earlier a vulnerability is found, the cheaper it is to fix. By the time a security audit catches something in production, the cost is an order of magnitude higher than if the same issue had been caught in code review or a pre-commit hook. Understanding the recurring vulnerability classes, the principle of least privilege, and how secrets and supply chains are attack surfaces is the foundation for making security a practice rather than a checklist.

**Level 2 candidates:**

- **L2 · Shifting Security Left: From Audit to Embedded Practice** — Security checks embedded in the development workflow catch vulnerabilities when they cost minutes to fix; the same checks run as post-deployment audits catch them when they cost weeks.
- **L2 · Threat Modeling: Thinking About What Can Go Wrong Before You Build** — Threat modeling is the practice of reasoning about attack surfaces before they exist — drilling here gives you a structured way to find security problems in design rather than in incident retrospectives.
- **L2 · The OWASP Top 10: The Recurring Vulnerability Classes** — These ten classes recur across codebases and stacks because they exploit structural patterns rather than specific bugs — understanding the class is more durable than knowing any individual CVE.
- **L2 · Static and Dynamic Analysis: SAST and DAST** — SAST finds what the code says it does; DAST finds what the running system actually does — understanding the difference clarifies what each tool catches and what each misses.
- **L2 · The Principle of Least Privilege: Why Permissions Should Be Minimal by Default** — Every permission granted beyond what is needed is an attack surface — least privilege is the design principle that limits the blast radius of any compromised credential or service.
- **L2 · Secrets and Credential Management: Injection, Rotation, and Audit** — Secrets require a different operational model from configuration — understanding injection patterns, rotation requirements, and audit trails is the practice that keeps credentials out of logs and version control.
- **L2 · Supply Chain Security: SBOMs, Signing, and Dependency Provenance** — The software supply chain is an attack surface that extends far beyond your own code — understanding SBOMs and signing is the practice that makes that surface visible and verifiable.

---

#### L1-13 · Reliability Engineering

**What it is and why it matters:** Reliability engineering is the discipline of designing systems that fail well — not systems that never fail, because those do not exist. The foundational shift is from "uptime" as a vague goal to error budgets as an explicit engineering constraint: if you have a 99.9% SLO, you have 43 minutes per month to spend on failures and planned downtime before you owe your users something different. That framing makes reliability a negotiation between risk and velocity rather than an unreachable standard. Toil, chaos engineering, and incident response are all expressions of the same underlying commitment: you build for failure because failure is certain.

**Level 2 candidates:**

- **L2 · SLIs, SLOs, and Error Budgets: The Language of Reliability** — Error budgets translate reliability targets into a resource that engineering teams can spend consciously — the framework that makes "how reliable is reliable enough" a decision rather than an argument.
- **L2 · Failure Modes in Distributed Systems: Partial Failure and Cascading Failure** — Distributed systems fail in ways that are qualitatively different from single-process systems — understanding partial failure and cascade patterns is the prerequisite for designing systems that degrade gracefully.
- **L2 · Circuit Breakers, Retries, and Timeouts: The Resilience Primitives** — These three primitives are the building blocks of fault-tolerant service communication — understanding how they interact is what prevents a retry storm from turning a partial failure into a total one.
- **L2 · Chaos Engineering: Deliberately Breaking Things** — Chaos engineering is the practice of injecting controlled failures in production to find weaknesses before they find you — it works only when the system is observable enough to learn from what breaks.
- **L2 · Toil: The Invisible Reliability Tax** — Toil is manual, repetitive operational work that scales with system load rather than being eliminated by automation — measuring it is the first step to reclaiming engineering time from operational debt.
- **L2 · Runbooks and Incident Response: Operationalizing the Failure Model** — A runbook externalises the knowledge that would otherwise live in a senior engineer's head — the practice that determines whether incidents are resolved by reasoning or by panic.

---

#### L1-14 · Cost Awareness (FinOps Thinking)

**What it is and why it matters:** In cloud environments, every architectural decision is also a financial decision — and unlike on-premise infrastructure, the costs are variable, immediate, and often invisible until the bill arrives. FinOps is the practice of treating cost as an engineering constraint to be designed against, not a finance department problem to be managed after the fact. The engineers who understand the cloud billing model — what on-demand vs reserved vs spot means, what data egress costs, what idle resources accumulate — make architectural decisions that reflect real tradeoffs rather than assuming compute is free.

**Level 2 candidates:**

- **L2 · The Cloud Billing Model: On-Demand, Reserved, and Spot** — Understanding the three purchasing models is the prerequisite for making commitment decisions that match actual usage patterns rather than defaulting to on-demand for everything.
- **L2 · Resource Right-Sizing: Utilization vs Allocation** — Allocated resources cost money regardless of utilisation — right-sizing is the practice of aligning what you pay for with what you actually use, which requires measuring both.
- **L2 · Cost Attribution: Tagging, Showback, and Chargeback** — Without cost attribution, cloud spending is invisible at the team or product level — tagging is the foundational practice that makes cost a signal rather than noise.
- **L2 · The Cost of Data Transfer: Architecture Decisions and Network Egress** — Egress costs are the cloud billing line item most frequently missed in architectural planning — understanding them changes decisions about where services are placed and how data moves between them.
- **L2 · Reserved Instances and Savings Plans: Commitment as a Financial Tool** — Committing to usage in exchange for discounted rates is a financial instrument — understanding the mechanics lets you make the commitment decision analytically rather than by intuition.
- **L2 · Waste Identification: Idle Resources, Orphaned Assets, and Oversized Instances** — Cloud waste accumulates silently — idle load balancers, unattached volumes, forgotten environments — and identifying it is the highest-leverage cost reduction action available to most teams.

---

#### L1-15 · Emerging Technology

**What it is and why it matters:** The technology landscape produces a continuous stream of new tools, frameworks, and platforms — and the ability to evaluate them without being captured by momentum is a senior engineering skill. This topic is not about any specific technology; it is about the analytical framework for assessing any technology: where it sits in the existing stack, what tradeoff it makes, how mature it is, and whether the problem it solves is the problem you have. Engineers without this framework either adopt everything early or dismiss everything conservatively — both are expensive failure modes.

**Level 2 candidates:**

- **L2 · The Tradeoff Map: What Every New Technology Is Actually Buying and Paying** — Every technology makes a tradeoff — drilling here gives you the habit of asking "what does this cost" before "what does this offer," which is the question that prevents adoption regret.
- **L2 · Stack Layer Diagnosis: Locating a New Technology in the Known Problem Space** — A new technology that solves a problem you can already locate in your mental model is legible; one that doesn't fit anywhere is either genuinely novel or poorly understood — this skill tells you which.
- **L2 · The Maturity Gradient: Understanding Where a Technology Sits in Its Lifecycle** — Adopting a technology at the wrong point in its lifecycle — too early or too late — has different costs; understanding the gradient makes the timing decision explicit.
- **L2 · Separating Signal from Momentum: Identifying Genuine Architectural Shifts** — Most technology trends are rebranding; a few represent genuine architectural shifts — the skill of distinguishing them is what lets you invest attention where it compounds rather than where it decays.
- **L2 · Transfer Learning: How Foundational Knowledge Extends to New Contexts** — Strong foundational knowledge makes new technologies legible faster — this sub-concept makes explicit the mechanism by which Tier 1 knowledge pays dividends across an entire career.
- **L2 · The Adoption Decision: A Framework for Engaging With Emerging Technology in Production** — The decision to adopt in production is different from the decision to evaluate — drilling here gives you a structured framework for when "interesting" becomes "worth the operational risk."

---

## Sequencing note

The tiers are concentric, not sequential, but there is a practical entry order. **Tier 1** should be established first — not because Tier 2 is impossible to understand without it, but because Tier 1 gaps produce confusion that looks like Tier 2 problems. A deployment failure that is actually a DNS misconfiguration will not be diagnosed correctly by someone who doesn't have L1-01 in place.

Within Tier 1, **Networking Fundamentals (L1-01)** is the highest-leverage starting point for most practitioners — it surfaces in every other topic and is the most common source of unexplained production behaviour. **Compute Abstractions (L1-02)** follows naturally, since containers and orchestration are the primary runtime environment for most modern systems. **Service Architecture Awareness (L1-03)** can be approached in parallel once L1-01 is established.

Within Tier 2, the lifecycle stages are genuinely sequential — Source Control feeds CI feeds Artifact Management feeds CD — so working through them in order (L1-04 through L1-10) follows the logical flow of the assembly line.

**Tier 3 topics can be started earlier than they appear.** Observability (L1-11) in particular is worth establishing before going deep on Tier 2 — having an observability mental model changes how you think about what CI and CD pipelines should produce as feedback. Security (L1-12) and Reliability (L1-13) are most useful once there is a system to reason about securing and operating.

For a practitioner returning to foundations, the single highest-leverage entry is **L1-11 (Observability)** — it is the discipline that makes every other part of the system legible when it fails, and it is the one most commonly underdeveloped in engineers who learned by shipping rather than by operating.