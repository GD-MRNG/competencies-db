# How to Read Any System

## Introduction

**Purpose**
A procedure, not a reference. This guide exists to get you oriented in any production system you've never seen before — before you read a single source file. The feeling of being lost in an unfamiliar codebase is not a knowledge gap. It's an orientation gap, and it has its own remedy.

**Principles**
- A system is not understood by reading its files. It's understood by locating a small, fixed set of subsystems and tracing what flows through them.
- Files are where a system is stored, not how it is shaped. Trying to learn what every file does is reading in the wrong order.
- Every codebase has a handful of files that matter — its anchors — and thousands of leaves hanging off them. Hunt the anchors. Read a leaf only when something leads you to it.

**Outcomes**
You're oriented when you can answer: how does work get in? What path does it travel? Where does state live? What does this system call, and what happens when those calls fail? How does a change get from source to production? Where do you look first when it breaks at 3am?

**How to use**
Work through the skeleton first to know what you're looking for. Then run the four traces in order — they build on each other. The output is a one-page map you write down, not a fading mental impression.

---

## The Skeleton

Nine subsystems that exist in every running system, defined by responsibility rather than folder name. This is what you're looking for — regardless of language, framework, or how the repo is organised.

**1. Entry points** — every way work gets in: routes, message consumers, scheduled jobs, CLI commands, the startup bootstrap. The system's real table of contents.
*Keywords: routes, consumers, handlers, entrypoints, bootstrap*
*→ L1-03 (Service Architecture), L1-01 (Networking)*

**2. The request path** — the route work travels from entry to response. Learn one and you learn how all of them are laid out.
*Keywords: middleware, handler chain, request lifecycle, controller*
*→ L1-03, L1-01*

**3. The domain core** — the business rules, the reason the system exists. Usually a small island in a sea of plumbing. Worth finding early.
*Keywords: domain logic, business rules, services, use cases*
*→ L1-03*

**4. State and data** — the stores, the schema, the data model. Often the truest map of the domain, because data cannot quietly drift out of date the way comments can.
*Keywords: schema, migrations, data model, stores, source of truth*
*→ L1-03*

**5. Outbound dependencies** — what it calls, and what it does when those calls fail. Places the system inside the wider topology instead of treating it as an island.
*Keywords: clients, adapters, third-party integrations, timeouts, retries*
*→ L1-01, L1-03, L1-13 (Reliability)*

**6. The control surface** — config, secrets, and feature flags: everything that changes behaviour without changing code.
*Keywords: environment variables, secrets management, feature flags, config*
*→ L1-09 (Configuration Management)*

**7. Build and delivery** — how source becomes an artifact and reaches production, and how a bad release rolls back. The road your own change will travel.
*Keywords: CI pipeline, build scripts, deployment, rollback*
*→ L1-05 (CI), L1-07 (CD), L1-06 (Artifact Management)*

**8. Runtime topology** — where it actually runs: environments, replicas, network shape.
*Keywords: environments, replicas, load balancer, infra, cloud*
*→ L1-02 (Compute Abstractions), L1-01*

**9. Observability** — logs, metrics, traces, and alerts. The difference between a system and a black box.
*Keywords: logs, metrics, traces, dashboards, alerts, on-call*
*→ L1-11 (Observability)*

---

## The Four Traces

The skeleton tells you what to find. Tracing tells you how to find it without drowning. Follow one thing depth-first — don't browse the tree breadth-first.

**1. Walk around the car first**
Before opening any source, read the configuration at the repository root — the dependency manifest, container files, CI workflow, infrastructure definitions, build scripts. In about a minute this tells you the language, the framework, how it builds, how it deploys, and how to run it. The highest-yield minute available, and the step most people skip on their way to getting lost in `src/`.
*Keywords: package manifest, Dockerfile, CI config, README, Makefile*
*→ L1-04 (Source Control), L1-05 (CI)*

**2. Trace one request**
Pick a single representative endpoint and follow it end to end: entry → handler → core → data → outbound → response. Because a system applies the same layering to every request, this one walk teaches the grammar all the others obey. You see the intake, spine, engine, memory, and linkages in a single pass.
*Keywords: request lifecycle, handler, middleware, query, response*
*→ L1-01, L1-03*

**3. Trace one change**
Follow a commit from source control through CI to a built artifact, then through deployment into staging and production. Note how a bad release is undone. This is the trace that lets you act on the system, not merely understand it.
*Keywords: commit, pipeline, artifact, deploy, rollback*
*→ L1-04, L1-05, L1-06, L1-07*

**4. Trace one failure**
Ask where you would look first if it broke at 3am. Find the logs, dashboards, and alerts before you ever need them.
*Keywords: logs, alerts, dashboards, runbook, on-call*
*→ L1-11, L1-13*

---

## The Output

Orientation should leave an artifact, not a fading feeling. After your four traces, write down — in about a dozen lines:

- The stack and how to run it locally
- Where the entry points live
- One fully traced request, end to end
- Where the domain core sits
- The data stores and source of truth
- The external dependencies
- The config and secrets it needs to boot
- How it ships and how to roll back
- Where it runs
- Where the logs are

A mental model decays. A map does not.

---

## Resource Map

**Tier 1 — Foundational Knowledge** *(the physics of how software runs)*
The mental models that make the skeleton legible. Without these, locating subsystems is pattern matching without understanding.
*Primary to all four traces*
*L1-01 · Networking Fundamentals*
*L1-02 · Compute Abstractions*
*L1-03 · Service Architecture Awareness*

---

**Tier 2 — The Delivery Lifecycle** *(how code becomes a running system)*
The assembly line from source to production. Tracing one change is a walk through this tier in a real system.
*Primary to Trace 3*
*L1-04 · Source Control*
*L1-05 · CI*
*L1-06 · Artifact Management*
*L1-07 · CD*
*L1-08 · Infrastructure as Code*
*L1-09 · Configuration Management*
*L1-10 · Database Change Management*

---

**Tier 3 — Continuous Disciplines** *(what separates reliable systems from fragile ones)*
The cross-cutting concerns that apply at every stage. Tracing one failure is a walk through this tier in a real system.
*Primary to Trace 4*
*L1-11 · Observability*
*L1-12 · Security*
*L1-13 · Reliability Engineering*

---