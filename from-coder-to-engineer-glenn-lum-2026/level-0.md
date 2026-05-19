# From Coder to Engineer: An Operational Engineering Curriculum

## Summary

This curriculum is fundamentally about the territory between writing code and engineering software. Its governing premise is that software is not valuable when it is written; it is valuable when it is running. Everything that happens between a developer typing a line of code and a user benefiting from it is the domain of operational engineering — and that domain is what this course maps. DevOps is treated not as a job title or a toolchain but as the cultural and technical philosophy that treats the entire journey from code to running system as a first-class engineering concern.

The course exists to address a specific gap the author encountered firsthand: entering the industry in 2020 without onboarding or a mentor, surrounded by tribal knowledge locked inside senior engineers' heads. The "why" behind tools, decisions, and conventions was rarely articulated, leaving junior engineers executing rituals rather than making informed decisions. This curriculum is the response — a deliberate attempt to surface the mental models that make tools legible, so that when a reader encounters something unfamiliar they can reason about it from first principles rather than inherit a configuration from whoever set it up before them.

The orientation matters more now than ever because AI-assisted development is shifting the craft away from typing code and toward directing, evaluating, and owning outcomes. The engineers who thrive in that environment will be the ones who invested in principles rather than in any particular tool or syntax. This curriculum is built for that shift.

A learner who works through this material should come away able to reason across the full lifecycle of a running system: to understand why a deployment failed even when the symptom appears in a different layer than the root cause; to evaluate architectural and operational tradeoffs explicitly rather than by default; to recognize when a new technology represents a genuine shift versus a rebranding of existing ideas; and ultimately to operate as someone who designs, delivers, and owns systems rather than someone who only writes the code that runs inside them.

The material is organized into three tiers that are concentric rather than sequential. Tier 1 is the foundational "physics" of how software runs. Tier 2 is the lifecycle assembly line by which code becomes a deployed artifact. Tier 3 is the set of cross-cutting disciplines — observability, security, reliability, cost, and emerging technology — that apply continuously at every stage. Most real problems span multiple tiers simultaneously, and the ability to reason across them is what the curriculum defines as operational seniority.

Each topic is developed across a five-level depth progression (inferred from the included framework document): a Concept post that establishes why the topic matters, a Depth post that develops the underlying mechanics and tradeoffs, a Build post that walks through a concrete implementation, a Debug and Design post grounded in real failure cases and design judgments, and a Teach and Lead post that operates at organizational scale. The published material currently visible covers Levels 1 and 2 across all topics.

## Topics

### Tier 1: Foundational Knowledge

**Networking Fundamentals** — The mental models for how packets move, how addresses and names resolve, how connections are established and secured, and how traffic is controlled at the boundary. Covers the OSI/TCP-IP stack, CIDR, DNS, TCP vs UDP, HTTP/TLS, L4 vs L7 load balancing, firewalls and security groups, and NAT.

**Compute Abstractions** — The layers of abstraction that turn physical hardware into the runtime environments software actually executes in. Covers virtual machines and hypervisors, container isolation primitives (namespaces, cgroups), container images and registries, orchestration and scheduling, serverless and event-driven compute, and CPU/memory/IO as first-class constraints.

**Service Architecture Awareness** — The structural decisions that govern how systems are decomposed into services and how those services interact. Covers the monolith-to-microservices spectrum, sync vs async communication, API contracts (REST, gRPC, event schemas), service discovery, idempotency and distributed state, data ownership, and the failure modes of distributed systems.

### Tier 2: Core Lifecycle Stages

**Source Control and Collaboration** — The assembly line begins with how code is versioned, reviewed, and merged. Covers the Git object model, branching strategies (trunk-based vs GitFlow), merge strategies, the pull request as a quality gate, conflict resolution, and monorepo vs polyrepo as an architectural decision.

**Testing Strategy** — The discipline of building confidence that code does what it should before and after it ships. Covers the testing pyramid, test doubles, what coverage measures and misses, contract testing between services, testing in production via flags and observability, and the cost of flaky tests.

**Continuous Integration (CI)** — The practice of integrating code continuously and validating it automatically. Covers CI as a discipline distinct from its tooling, the anatomy of a pipeline, build reproducibility, fast feedback as a constraint, and the handoff boundary to CD.

**Artifact and Dependency Management** — The unit that actually gets deployed and the supply chain it comes from. Covers what an artifact is, semantic versioning, dependency graphs and transitive dependencies, artifact registries and promotion, pinning vs version ranges, and supply chain security.

**Continuous Delivery and Deployment (CD)** — How an artifact moves from build to production with safety. Covers the critical distinction between delivery and deployment, deployment strategies (blue/green, canary, rolling, recreate), the environment promotion pipeline, rollback vs roll-forward philosophies, and decoupling release from deployment via feature flags.

**Configuration and Feature Management** — How a single artifact behaves differently across environments without being rebuilt. Covers the twelve-factor config principle, configuration hierarchies and overrides, secrets management as distinct from configuration, the operational model of feature flags, and configuration drift.

**Infrastructure as Code (IaC)** — Treating infrastructure as a versioned, reviewable, reproducible artifact. Covers declarative vs imperative models, state as source of truth and source of risk, idempotency, the plan/apply cycle, modules and reuse, and drift detection.

### Tier 3: Cross-Cutting Disciplines

**Observability and Monitoring** — The ability to understand what a running system is doing and why. Covers monitoring vs observability (known unknowns vs unknown unknowns), the three pillars (metrics, logs, traces), metric types and aggregation tradeoffs, distributed tracing, the SLI/SLO/SLA framework, and alerting philosophy.

**Security (DevSecOps)** — Security as a continuous, embedded practice rather than a late-stage audit. Covers shifting left, threat modeling, the OWASP Top 10, static and dynamic analysis (SAST/DAST), least privilege, secrets and credential management, and supply chain security (SBOMs, signing, provenance).

**Reliability Engineering** — Designing and operating systems that fail well. Covers SLIs/SLOs and error budgets, distributed system failure modes, resilience primitives (circuit breakers, retries, timeouts), chaos engineering, toil as a reliability tax, and runbooks and incident response.

**Cost Awareness (FinOps Thinking)** — Treating cost as an engineering constraint rather than a finance department problem. Covers cloud billing models (on-demand, reserved, spot), right-sizing, cost attribution and tagging, data transfer and egress as architectural costs, commitment-based discounts, and waste identification.

**Emerging Technology** — A framework for evaluating new technologies as they appear, rather than chasing them. Covers the tradeoff map every new technology embodies, locating new tech in the existing stack, the maturity gradient, separating genuine architectural shifts from hype, transfer learning from foundational knowledge, and the adoption decision in production contexts.