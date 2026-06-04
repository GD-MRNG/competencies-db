# AI Engineer Production Track — Level 0: Course Map

> **Intent:** Move AI systems from "works on my machine" to "works reliably for thousands of paying users," managing the transition from prototypes to production-grade, scalable, secure, and monitorable systems.
>
> **Your angle:** You've built working AI agents and orchestration logic. Now you're learning the other 80%: Platform Engineering. You'll understand how to decouple frontends from backends, manage secrets and infrastructure as code, make architectural decisions about containerization and cloud deployment, design systems that survive load and failure, and instrument them so you know what's broken before your customers do. You're not just an AI engineer anymore—you're an *infrastructure* engineer who happens to work with LLMs.

---

## How to Use This Map

This map is organized into four layers, reflecting the progression from **basic deployment** to **enterprise-scale, multi-agent orchestration**.

**Level 1 topics** are architectural decisions and capabilities. Each topic represents a set of skills that unlock a new stage of product maturity.

**Level 2 candidates** are the specific patterns, tools, and gotchas within each topic. Use them to diagnose what you need to learn next: if you're deploying to AWS for the first time, L1-03 and its Level 2 candidates are your focus.

The **Sequencing note** at the end connects this track to the Core and Agentic tracks, and identifies common pathways to production.

---

## Topic Inventory

### **Foundations: Local to Cloud**

#### L1-01 · The 80/20 Rule and Decoupled Architecture

Building a production AI system is **20% AI logic and 80% Platform Engineering**. The model is just another high-latency API call. The real complexity is decoupling the **Frontend** (user interface, perceived performance) from the **Backend** (secrets, expensive computation, data validation). This separation is not optional—it's how you secure API keys, scale independently, and iterate on AI without redeploying infrastructure. A monolithic architecture couples the browser to your GPU, and the first traffic spike breaks you.

**Level 2 candidates:**

- **Frontend-Backend Decoupling** — Why a frontend can't call your LLM API directly; how you need a backend to proxy requests, manage credentials, and validate input.
- **Async Streaming and Perceived Performance** — LLMs are slow (5-30 seconds for a response). Streaming tokens to the user (SSE or WebSocket) makes it feel faster than waiting for a complete response. The cost: frontend complexity.
- **State Management Across Services** — The frontend has local state (UI position, scroll, form input); the backend has server state (conversation history, embeddings, database records). Synchronizing them correctly prevents data loss and weird UX bugs.
- **Single Page Applications (SPAs) vs. Server-Side Rendering** — SPAs (React, Next.js) live in the browser and talk to APIs; they're flexible but require careful state management. SSR blurs the line for better performance and SEO.

---

#### L1-02 · Environment Variables, Secrets, and the Principle of Least Privilege

An API key is not a password—it's a passport to your cloud account. Hardcoding keys in source code is a critical failure. **Environment Variables** separate secrets from code; `.env` files keep them local during development; **Secret Managers** (AWS Secrets Manager, Clerk) keep them safe in production. **Least Privilege** means every service (function, container, user) has only the *minimum* access it needs. One compromised API key shouldn't expose your entire database.

**Level 2 candidates:**

- **Environment Variables and .env Files** — Loading config from the environment rather than source code; the `.env` file pattern for local development; avoiding git commits of secrets.
- **Secret Managers and Rotation** — Using AWS Secrets Manager or similar to store and rotate secrets without code changes; how to reference secrets in containers and Lambda functions.
- **IAM and Granular Permissions** — Understanding Identity and Access Management (IAM) roles and policies; granting a function only the API calls it needs, not Root account access.
- **API Key Scope and Expiration** — Designing API keys with limited scopes (e.g., "read-only embeddings") and expiration dates; revoking compromised keys without affecting the entire system.
- **Secrets in Containers and Infrastructure as Code** — Passing secrets to Docker containers securely; avoiding baking secrets into images; how Terraform accesses secrets for infrastructure provisioning.

---

#### L1-03 · Containerization (Docker) as Portability and Reproducibility

"It works on my machine" usually means "it doesn't work anywhere else." **Docker** packages your code, the Python runtime, and all dependencies into an immutable image that runs the same on a laptop, CI/CD server, and AWS. This solves the environment mismatch problem: no more "the deploy is broken because the production server has a different libssl version." Containerization is the lingua franca of cloud deployment.

**Level 2 candidates:**

- **Dockerfile and Image Layers** — Writing Dockerfiles that specify the base image (Python 3.12), dependencies (pip/uv), and entrypoint; understanding layer caching so rebuilds are fast.
- **Multi-Stage Builds** — Separating the "build stage" (compile, download models) from the "runtime stage" (lean, production image); reducing image size and attack surface.
- **Platform Mismatch and Architecture-Specific Images** — Building on an M1 Mac (ARM64) but deploying to AWS (x86) breaks unless you specify `--platform linux/amd64`; understanding when images are architecture-specific.
- **Image Registry and Versioning** — Storing images in registries (Docker Hub, AWS ECR); tagging images with versions; understanding when to use `latest` vs. specific versions.
- **Docker Compose for Local Development** — Running multi-container setups locally (e.g., app + database + Redis); matching production topology during development.

---

#### L1-04 · Async Backends and Streaming (FastAPI, etc.)

An LLM call blocks for 10 seconds. If your backend is synchronous, a single user ties up a server thread for those 10 seconds. With 100 users, you'd need 100 threads, which crashes the server. **Asynchronous backends** (FastAPI with async/await) handle high latency without blocking. A single thread can manage 1000 concurrent requests by yielding while waiting for I/O. For AI, async is non-optional.

**Level 2 candidates:**

- **Async/Await in Python** — Writing async functions with `async def` and `await`; understanding that `await openai.ChatCompletion.create(...)` yields control while waiting.
- **Event Loops and Non-Blocking I/O** — The event loop manages many concurrent tasks; when one awaits, the loop switches to another. Non-blocking means your server can handle 1000 users on one machine.
- **FastAPI and Dependency Injection** — FastAPI is a modern async web framework; understanding route handlers, middleware, and dependency injection for clean code.
- **Streaming Responses (SSE and WebSocket)** — Using Server-Sent Events (SSE) to stream tokens to the browser in real-time; WebSocket for bidirectional communication.
- **Rate Limiting and Backpressure** — Limiting requests per user/API key; implementing queue limits so your backend doesn't accept more work than it can handle; graceful degradation under load.

---

### **Cloud Architecture and Deployment**

#### L1-05 · Cloud Platforms and the IaaS vs. PaaS Trade-off

**Platform as a Service (PaaS)** like Vercel handles deployment, scaling, and monitoring automatically; you push code and it works. **Infrastructure as a Service (IaaS)** like AWS gives you granular control but more responsibility. For an MVP, PaaS is faster; for enterprise with compliance requirements, IaaS is necessary. The choice cascades: PaaS locks you into specific frameworks and has vendor switching costs; IaaS requires DevOps expertise but is portable.

**Level 2 candidates:**

- **PaaS (Vercel, Railway, Heroku) vs. IaaS (AWS, GCP, Azure)** — When to choose each; PaaS for speed, IaaS for control and enterprise requirements.
- **Managed Services vs. Raw Compute** — Should you use AWS App Runner (managed containers) or raw EC2? Lambda (serverless functions) or Docker containers? Tradeoffs in cost, control, and complexity.
- **Cold Starts and Serverless Latency** — Lambda and serverless containers have "cold start" latency (30-60s) if not kept warm; implications for AI workloads with long inference times.
- **Auto-Scaling and Load Balancing** — Scaling up when traffic spikes and scaling down to save costs; how load balancers distribute traffic across instances.
- **Multi-Region and Disaster Recovery** — Running your app in multiple regions for redundancy; failing over if one region goes down; implications for compliance (data residency).

---

#### L1-06 · Infrastructure as Code (Terraform) and GitOps

Managing cloud infrastructure by clicking buttons in the AWS console is a path to disaster. You forget what you clicked, can't reproduce it, and have no audit trail. **Terraform** is a declarative language where you describe the infrastructure you want, and Terraform ensures it exists. Version control your Terraform code like you version control application code. Changes go through code review. Every infrastructure change has a commit message.

**Level 2 candidates:**

- **Terraform Basics and State Management** — Writing Terraform to describe resources (Lambda functions, databases, networks); understanding state files that track what resources exist.
- **Modules and Code Reuse** — Breaking Terraform into modules so you don't repeat yourself; using community modules (e.g., a "standard VPC" module).
- **Environment Separation** — Defining separate environments (dev, staging, prod) as separate Terraform workspaces or directories; promoting changes through environments.
- **Secrets in Terraform** — Passing secrets to Terraform without hardcoding them; using AWS Secrets Manager or similar.
- **GitOps and Change Control** — All infrastructure changes via git pull requests; code review before applying; automatic rollback for failed deployments.

---

#### L1-07 · Databases and State Persistence

An LLM call is stateless, but your application is not. You need to store conversation history, user data, embeddings, and job results. **Relational databases** (Aurora, PostgreSQL) are for structured data (users, transactions). **Vector stores** (Pinecone, Chroma, Weaviate) are for embeddings (semantic search). **Queues** (SQS, RabbitMQ) decouple work (you enqueue a job, a worker picks it up later). Picking the right storage for the right data type is critical for performance and cost.

**Level 2 candidates:**

- **Relational Databases and Schemas** — Designing tables for users, conversations, jobs; understanding foreign keys and normalization; query optimization.
- **Vector Databases for Embeddings** — Storing and searching embeddings; understanding similarity search (cosine distance, Euclidean); cost scaling (is it linear with data size?).
- **NoSQL and Document Stores** — When to use DynamoDB or MongoDB (flexible schema, good for unstructured data); understanding the tradeoffs with relational databases.
- **Caching and Redis** — Using in-memory caches to speed up repeated queries; understanding TTL (time-to-live) and cache invalidation.
- **Data Retention and Compliance** — Keeping logs for observability but not forever (storage cost, privacy); understanding GDPR/data deletion requirements.

---

#### L1-08 · Networking, APIs, and Rate Limiting

Your backend needs to be accessible to the frontend (over HTTPS), but not to the internet at large. **VPCs** (Virtual Private Clouds) isolate your infrastructure. **API Gateway** routes requests to Lambda functions or containers. **Rate Limiting** prevents users from hammering your API or exhausting your LLM quota. **API Keys** allow you to identify and bill users. Designing your API is a contract between frontend and backend; breaking changes cause outages.

**Level 2 candidates:**

- **VPCs and Network Isolation** — Placing databases in private subnets (no internet access); allowing only your app to talk to them.
- **HTTPS and TLS** — Encrypting traffic between clients and servers; understanding certificates and domains.
- **API Gateway and Routing** — Routing incoming requests to different backends based on path or method; rate limiting at the gateway level.
- **API Key Management and Versioning** — Issuing API keys to users; versioning your API (v1, v2) to avoid breaking changes.
- **CORS (Cross-Origin Resource Sharing)** — Allowing your frontend (on domain A) to call your backend (on domain B); understanding security implications.

---

### **Reliability, Scale, and Observability**

#### L1-09 · Monitoring, Logging, and Alerting (Observability)

A production system is a black box: you can't read the code in your head while it's running. **Logging** captures events (requests, errors, tool calls); **Metrics** track performance (latency, cost, accuracy); **Traces** show the full path a request took through the system. **Dashboards** visualize these signals; **Alerts** notify you when something goes wrong. Without observability, you learn about problems from angry users.

**Level 2 candidates:**

- **Structured Logging** — Logging as JSON with context (user ID, request ID, timestamp); allowing you to query and correlate logs across services.
- **Metrics and Time-Series Data** — Tracking latency, cost per request, model accuracy; using Prometheus or CloudWatch; setting baselines to detect anomalies.
- **Distributed Tracing** — Following a single request through multiple services (frontend → backend → LLM → database); understanding which service is slow.
- **Alerts and On-Call** — Notifying engineers when metrics exceed thresholds; designing alerts that don't cry wolf (false positives); on-call rotation for responding to issues.
- **Cost Attribution** — Tracking which features/users consume the most tokens and cloud compute; making optimization decisions based on data.

---

#### L1-10 · Error Handling, Retries, and Graceful Degradation

LLM APIs fail: timeout, rate limit, provider outage. Your system must survive. **Retries with exponential backoff** automatically retry failed requests; **Circuit breakers** stop retrying when a service is clearly down, returning an error instead of hanging. **Graceful degradation** means if RAG is slow, you might skip it and use just the base model; if the embedding model fails, you skip semantic search. Design for failure at every layer.

**Level 2 candidates:**

- **Retry Logic and Exponential Backoff** — Automatically retrying failed requests with increasing delays; understanding when to retry (transient failures) vs. when to fail immediately (bad request).
- **Circuit Breakers and Fallbacks** — Detecting when a service is down and failing fast instead of retrying forever; providing a fallback response (cached answer, simpler model).
- **Idempotency and Duplicate Prevention** — Ensuring that retrying a request doesn't double-process it (e.g., charging the user twice); using request IDs to deduplicate.
- **Timeouts and Resource Limits** — Setting timeouts on LLM calls so hung requests don't consume resources forever; limiting memory/CPU per function.
- **Error Budgets and Acceptable Failure Rates** — Understanding that systems fail; defining how much failure is acceptable; measuring actual vs. target availability.

---

#### L1-11 · Testing and Validation in AI Systems

Traditional software testing is deterministic: given input X, output is always Y. AI is stochastic: the same prompt might return different answers. Testing requires different thinking: **evals** (does the answer satisfy the criteria?), **regression testing** (does the new model break things that worked before?), **edge cases** (what happens with jailbreaks, adversarial inputs?). Coverage metrics are less relevant; instead, you measure accuracy on a benchmark.

**Level 2 candidates:**

- **Deterministic vs. Probabilistic Testing** — Unit testing your utility functions (deterministic); evals for model outputs (probabilistic).
- **Evaluation Benchmarks and Metrics** — Defining what "correct" means (user satisfaction, factual accuracy, latency); building test sets; measuring accuracy over time.
- **Regression Testing and Change Detection** — When you swap models or adjust prompts, does accuracy drop? Building automated tests that detect regressions.
- **Adversarial Testing and Security** — Testing whether the model can be jailbroken; understanding prompt injection attacks; building defenses.
- **A/B Testing and Canary Deployments** — Rolling out changes to a small % of users first; comparing metrics (accuracy, cost, latency) before full rollout.

---

#### L1-12 · Cost Optimization and Budget Management

LLM APIs are pay-per-token. Your costs scale with user count and model capability. Frontier models can cost an order of magnitude more per token than smaller or open-weight alternatives. Over a year, the difference is six figures. **Cost attribution** (knowing which feature costs how much) lets you make trade-offs. **Model selection** (routing easy requests to cheap models, hard ones to frontier models) reduces spend. **Context optimization** (only sending relevant context to the model) saves tokens. Pricing changes frequently as the market evolves — always pull current numbers from provider pricing pages before capacity planning.

**Level 2 candidates:**

- **Token Counting and Cost Estimation** — Using Tiktoken to count tokens before sending a request; estimating daily/monthly costs.
- **Model Selection and Routing** — Choosing the cheapest model that can solve the problem; using classifiers to route easy/hard requests to cheap/expensive models.
- **Caching and Deduplication** — If 100 users ask the same question, only call the LLM once and cache the answer.
- **Batch Processing** — Batch requests together (many providers offer a batch API tier) for lower cost; useful for non-time-critical workloads.
- **Resource Right-Sizing** — Monitoring actual vs. provisioned resources; scaling down overprovisioned infrastructure; understanding the cost levers (compute, storage, API calls).

---

### **Multi-Agent and Enterprise Scale**

#### L1-13 · Multi-Agent Architecture and Decomposition

A single agent is limited by context and model reasoning. **Decomposition** breaks a complex problem into specialized agents: a Planner decides what to do, Workers execute specific tasks, a Judge validates outputs. Each agent has a narrow System Prompt and specific tools, reducing cognitive load. This enables **separation of concerns** (test agents independently) and **parallel execution** (workers run in parallel). It's also more expensive (N agent calls instead of 1), so the trade-off is complexity for reliability and scalability.

**Level 2 candidates:**

- **Hierarchical vs. Flat Architectures** — In hierarchical, a Planner manages workers; in flat, agents coordinate peer-to-peer. Tradeoffs in latency, reliability, and reasoning quality.
- **System Prompt Specialization** — Writing narrow, focused System Prompts for each agent; reducing context noise improves accuracy.
- **Independent Evaluation and Metrics** — Measuring each agent's accuracy separately; identifying which agent is the bottleneck.
- **Parallel Execution and Synchronization** — Running workers in parallel (async); gathering results; handling partial failures.
- **State Management Across Agents** — Maintaining a shared "world state" (conversation history, extracted data); preventing agents from conflicting.

---

#### L1-14 · Distributed Execution and Job Queues

A single server can't handle millions of users. **Distributed execution** means splitting work across multiple machines. Instead of blocking a web server while an agent reasons for 30 seconds, you enqueue a job and return immediately. A **worker pool** picks up jobs from a **queue** (SQS, Redis), executes them in the background, and updates a **database** with results. The frontend polls or uses **webhooks** to learn when work is done. This decoupling scales to any number of concurrent jobs.

**Level 2 candidates:**

- **Job Queues and Message Passing** — Enqueuing work (e.g., "analyze this document") for a worker to pick up later; understanding queue semantics (FIFO, priority, dead-letter).
- **Worker Pools and Concurrency** — Running N workers in parallel, each processing jobs from the queue; scaling based on queue depth.
- **Idempotency and At-Least-Once Delivery** — Ensuring that if a worker crashes mid-job, the job is retried; designing work units that are safe to retry.
- **Result Storage and Polling** — Workers write results to a database; the frontend polls to check if work is done, or uses webhooks for push-based notification.
- **Lambda vs. Container Workers** — Using serverless functions (Lambda) for simple jobs; using containers (ECS, App Runner) for long-running or stateful jobs.

---

#### L1-15 · Observability for Non-Deterministic Systems

Traditional logging shows "User X made request Y." For agents, you need to understand the "thought process": which tools did the agent call, in what order, why? **Traces** capture the full decision tree. **Langfuse** or **Smithery** are specialized observability platforms for LLM systems. Understanding where agents get stuck (infinite loops, hallucination, wrong tool selection) requires drilling into traces, not just looking at logs.

**Level 2 candidates:**

- **Trace Capture and Visualization** — Recording every LLM call, tool invocation, and decision; visualizing as a tree or timeline.
- **Annotation and Human Feedback** — Marking traces as "good" or "bad"; collecting human feedback to improve evals and retrain.
- **Cost and Latency Attribution** — Understanding which LLM calls are expensive; which tool is slow; optimizing based on data.
- **Drift Detection** — Detecting when model behavior changes (accuracy drops, latency increases, cost skyrockets); alerting before it affects users.
- **PII and Privacy in Traces** — Ensuring traces don't leak sensitive customer data; understanding data retention and deletion requirements.

---

#### L1-16 · Security, Compliance, and the "Lethal Trifecta"

If an agent has access to **private data**, receives **untrusted input** (user prompts), and can **communicate externally** (API tools), you have a security hole. A user could ask the agent to leak the database or call an attacker's API. **Input validation** sanitizes user prompts. **Output validation** ensures the agent doesn't generate malicious requests. **Sandboxing** limits what tools can do. **Compliance** (SOC 2, HIPAA, GDPR) requires auditing and data protection.

**Level 2 candidates:**

- **Prompt Injection and Jailbreaks** — Understanding attacks where users try to make agents ignore System Messages; implementing defenses.
- **Tool Sandboxing and Least Privilege** — Giving agents only the minimum tool access they need; preventing accidental or malicious data deletion.
- **Input Validation and Sanitization** — Validating user prompts before passing to the model; preventing attacks that exploit specific prompt formats.
- **Audit Logging and Compliance** — Recording all significant actions (who accessed what, when); enabling audit trails for compliance requirements.
- **Data Privacy and Encryption** — Encrypting sensitive data at rest and in transit; understanding when you can delete data (GDPR); minimizing what data you store.

---

## Sequencing Note

**Prerequisites:** The Production Track assumes you've completed the **Core Track** and **Agentic Track**. You must understand:
- Decoupled inference, context management, and tool calling (Core Track, L1-08)
- Agentic loops and multi-agent orchestration (Agentic Track, L1-01 to L1-05)

If you haven't completed these, you'll struggle with production concepts. **You can't deploy what you don't understand.**

### ⚠️ Critical Warning: Production is the Last Mile, Not the First

The biggest mistake: thinking "I'll just learn infrastructure" and skip the AI parts. **This will fail catastrophically.**

- You cannot optimize costs if you don't understand token counting (Core L1-02)
- You cannot debug production issues if you don't understand agentic loops (Agentic L1-01)
- You cannot scale systems if you don't understand when to use multi-agent vs. single-agent (Agentic L1-05)
- You cannot build reliable systems if you don't understand structured outputs (Core L1-11)

**A real scenario:** You deploy a system to production. It works for a week. Then it starts failing. You search logs and find "JSON decode error." This happens because the model's output format changed slightly, or a model parameter was set differently. If you understood structured outputs (Core L1-11) and how to enforce schemas, you would have caught this in development. But you skipped Core and now you have a 3 AM page for a preventable bug.

**Do yourself a massive favor:** Complete Core and Agentic first. This track is only useful if you have working AI logic to deploy.

### The Three Tracks Explained

The Production Track is the final layer: taking working AI logic (from Core and Agentic tracks) and making it reliable, observable, and scalable.

**Four-stage progression within Production:**

**Stage 1: Local to Cloud (L1-01 to L1-04)** — Understanding the principles of decoupled architecture, secrets management, containerization, and async backends. By the end, you can write a FastAPI app, containerize it, and understand what it means to deploy to the cloud.

**Stage 2: Cloud Architecture (L1-05 to L1-08)** — Making decisions about platforms (PaaS vs. IaaS), infrastructure as code (Terraform), data storage (relational vs. vector), and networking. By the end, you can provision a production environment on AWS and understand the trade-offs.

**Stage 3: Reliability and Operations (L1-09 to L1-12)** — Building systems that don't fall over when they're under load, and understanding when they do. Observability, error handling, testing, and cost optimization. By the end, you can detect and respond to production issues.

**Stage 4: Scale and Enterprise (L1-13 to L1-16)** — Decomposing monoliths into multi-agent systems, distributing work, and adding security and compliance. By the end, you can architect systems for thousands of concurrent users and enterprise requirements.

**How this relates to other tracks:**

- **Core + Agentic → Production:** You must complete Core and Agentic before starting Production. You need working AI logic before you worry about deploying it.
- **Production as the capstone:** This track assumes all prior knowledge. It's not about learning AI anymore; it's about making AI systems work reliably at scale.

**High-leverage entry points depend on your stage:**

- **"I have a working prototype, how do I ship it?"** → L1-01 (architecture) → L1-04 (async backend) → L1-05 (choose cloud platform) → L1-06 (Terraform) → L1-09 (logging).
- **"My system works but crashes under load"** → L1-04 (async), L1-10 (error handling), L1-09 (observability).
- **"I need to reduce costs"** → L1-12 (cost optimization), L1-13 (decompose into cheaper agents).
- **"I need SOC 2 compliance"** → L1-02 (secrets), L1-16 (security/audit), L1-06 (Terraform for reproducibility).
- **"I'm deploying a multi-agent system"** → Ensure you've completed Agentic Track first, then L1-13 (multi-agent architecture), L1-14 (job queues), L1-15 (observability for agents).

**The dependency chain:**

- L1-01 (Decoupled Architecture) is foundational; everything else assumes this.
- L1-02 (Secrets Management) should be your first priority in any production system.
- L1-03 (Docker) and L1-04 (Async) are prerequisites for deployment.
- L1-05 (Cloud Choice) determines L1-06 (Terraform flavor) and L1-08 (networking setup).
- L1-09 (Observability) and L1-10 (Error Handling) can be tackled in parallel once you're deployed.
- L1-11 (Testing) and L1-12 (Cost) are ongoing concerns, not one-time tasks.
- L1-13 (Multi-Agent) depends on L1-14 (Job Queues) for scalability.
- L1-16 (Security) should be woven into every earlier decision, not an afterthought.

**Shortest path to "works in production":**

L1-01 → L1-02 (secrets) → L1-03 (Docker) → L1-04 (async backend) → L1-05 (Vercel or similar PaaS) → Deploy. You now have a working system; everything else is hardening.

**Path to enterprise-scale system:**

L1-01 through L1-06 (infrastructure as code) → L1-07 (databases) → L1-09 (observability) → L1-13 (multi-agent) → L1-14 (job queues) → L1-16 (security). Now you have a system that can handle 100K requests/day with traceability and security.

**Path integrating Agentic systems:**

Complete Core Track → Complete Agentic Track → L1-01 (architecture) → L1-03 (Docker) → L1-05 (cloud choice) → L1-13 (multi-agent architecture in production) → L1-14 (distributed execution) → L1-15 (observability for agents) → Deploy with confidence.

---

## Key Tradeoffs and Decisions

### Hosting Choice

| Choice | Speed to Deploy | Control | Scale | Cost |
|--------|-----------------|---------|-------|------|
| **Vercel (PaaS)** | 5 minutes | Low | Limited | Moderate |
| **AWS App Runner (Managed)** | 30 minutes | Medium | High | Moderate |
| **AWS ECS + Load Balancer (IaaS)** | 2 hours | High | Very High | Low (if optimized) |
| **Kubernetes (Full Control)** | Days | Very High | Unlimited | Depends |

**Decision driver:** Start with PaaS for MVPs. Move to IaaS (Terraform + App Runner) when you need better cost control or enterprise compliance. Only adopt Kubernetes if you have 10+ microservices or need multi-region failover.

---

### Data Storage

| Store Type | Best For | Latency | Cost Scaling | Complexity |
|-----------|----------|---------|--------------|------------|
| **Relational (Aurora)** | Structured data, ACID | Low | Linear | Medium |
| **Vector DB (Pinecone)** | Embeddings, semantic search | Low | Linear+ | Medium |
| **Cache (Redis)** | Frequent reads | Very Low | Linear | Low |
| **Object Storage (S3)** | Large files, logs | Medium | Linear | Low |
| **Search (Elasticsearch)** | Full-text search, logs | Low | Non-linear | High |

**Decision driver:** Start with a relational database (Aurora Postgres) and Redis cache. Add a vector database if you do RAG. Only move to specialized stores (Elasticsearch) if you hit specific bottlenecks.

---

### Agent Architecture

| Pattern | Complexity | Cost | Reliability | Best For |
|---------|-----------|------|-------------|----------|
| **Single Agent Loop** | Low | Low | Medium | Simple tasks, prototypes |
| **Workflow (Code-Defined)** | Medium | Low | High | Predictable processes |
| **Multi-Agent (Hierarchical)** | High | Medium | High | Complex, multi-domain problems |
| **Swarm (Autonomous Coordination)** | Very High | Medium-High | Low | Experimental, research |

**Decision driver:** Start with a single agent or workflow. Decompose into multi-agent only when a single agent's context becomes a bottleneck or when you need specialization. Avoid swarms for production unless you have 10+ agents and deep expertise.

---

## Quick Reference: Production Checklists

**Before Shipping to Production:**

- [ ] Secrets in environment variables, never in code
- [ ] Docker image builds and runs
- [ ] Tests pass (unit tests + integration tests + evals)
- [ ] Logging configured; can access logs in production
- [ ] Alerts set for key metrics (latency, error rate, cost)
- [ ] Rate limiting implemented
- [ ] Error handling for failed LLM calls (retries, fallbacks)
- [ ] Database schema versioned (migrations)
- [ ] Terraform code reviewed and tested
- [ ] Incident response plan documented

**Scaling from 100 to 10,000 Users:**

- [ ] Database queries optimized; indexes created
- [ ] Caching layer (Redis) in place
- [ ] Load balancing across multiple backend instances
- [ ] CDN for static assets
- [ ] Auto-scaling configured (based on CPU/memory/queue depth)
- [ ] Cost monitoring active; optimization roadmap

**Scaling from 10,000 to 1M Users:**

- [ ] Multi-region deployment for latency and resilience
- [ ] Database read replicas for scaling reads
- [ ] Queue-based architecture (async job processing)
- [ ] Distributed tracing active
- [ ] Cost attribution by feature; optimization ongoing
- [ ] Runbooks for common incidents
- [ ] Incident blameless postmortems after failures

**Enterprise/Compliance Requirements:**

- [ ] Audit logging of all significant actions
- [ ] Data encryption at rest and in transit
- [ ] Data deletion and retention policies automated
- [ ] Regular security audits (vulnerability scanning, penetration testing)
- [ ] SOC 2 or equivalent compliance (if required)
- [ ] Documentation of architecture, data flow, and security controls
- [ ] Incident response and breach notification procedures

---

## Relating Production to Core and Agentic Tracks

The three tracks are **cumulative**, not parallel:

| Track | Focus | Prerequisite |
|-------|-------|-------------|
| **Core** | Model calling, context management, prompting | None |
| **Agentic** | Loops, tool calling, multi-agent orchestration | Core |
| **Production** | Deployment, scaling, reliability, operations | Core + Agentic |

**A typical learning path:**

1. Core Track: Build a FastAPI app that calls an LLM and returns JSON.
2. Agentic Track: Add loops so the LLM can call tools and reason dynamically.
3. Production Track: Deploy that system to AWS, add observability, scale it.

**If you skip Production:** Your agent runs on your laptop. It works once in a demo. It crashes the first time a real user uses it.

**If you skip Agentic:** You can build a production system, but it's limited to single-pass generation. No tool calling, no reasoning loops.

**If you skip Core:** You can't build anything. Start with Core.

---

## One Final Note

Production engineering is where "AI Engineer" becomes "Software Engineer who works with AI." The AI logic is maybe 10% of the work; the other 90% is infrastructure, monitoring, error handling, and security. This is not less important than the AI logic—it's actually more important. A brilliant model running on a broken system will fail in production. A mediocre model on a well-engineered system will scale and make money.

Invest in this layer early. Every hour spent on observability and error handling now saves 10 hours debugging production issues later. Every automated test you write reduces the chance of a 3 AM page. And Terraform code is the only documentation that doesn't lie about what's actually deployed.

Welcome to Production.

## Source

https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/