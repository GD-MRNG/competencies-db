# AI Engineer Production Track: Deploy LLMs & Agents at Scale — Level 0: Course Map

> **Intent:** To give practitioners the ability to take an LLM or agent from a working prototype to a live, observable, maintainable system — one that handles real users, real costs, and real failure modes. This domain sits at the intersection of AI engineering and cloud platform engineering, and it is the gap that most ML practitioners have not filled.
>
> **Your angle:** You already understand what LLMs and agents *do*. This track is about what it takes to *deploy and operate* them — the 60–80% of the work that has nothing to do with prompts or model selection. Come at it as a practitioner who needs to make architectural decisions and own the infrastructure, not as a student learning cloud services for the first time.

---

## How to use this map

Each **Level 1 topic** below is a domain you can spend days inside. The description tells you why it exists and what it unlocks — read those before deciding where to drill. **Level 2 candidates** are the sub-concepts that reward a dedicated session: understanding the tradeoff, the failure mode, or the design decision at that level is what separates a practitioner who can deploy from one who can *operate*.

Descend to Level 1 when you are actively building in that area or hitting the edges of your current understanding. Descend to Level 2 when you have a concrete problem to solve — a deployment that won't scale, a cost you can't explain, an agent that fails silently.

---

## Topic Inventory

### Group 1 · Deployment Foundations

This is the substrate. Every production AI system runs on top of these primitives, regardless of which model, agent framework, or cloud it uses. Getting comfortable here means you can operate autonomously in any environment.

---

#### L1-01 · Cloud Deployment Primitives

The five deployment archetypes — traditional server, IaaS (EC2), PaaS (App Service / Beanstalk), container-as-a-service (App Runner / Azure Container Apps / Cloud Run), container orchestration (EKS / AKS), and serverless functions (Lambda / Azure Functions / Cloud Functions) — define the decision space for every production deployment you will ever make. AWS pioneered and hardened these, and the others followed, so AWS familiarity transfers directly. The choice of archetype determines your scaling model, your cost structure, your operational overhead, and what happens when traffic spikes at 3am.

**Level 2 candidates:**
- **Container vs. serverless trade-off** — Understanding this drives most architectural decisions: when you need persistent state, long-running inference, or predictable cold-start behaviour, containers win; when you need event-driven bursting with zero idle cost, Lambda wins — and the wrong choice bleeds money or reliability.
- **Docker and the container build lifecycle** — The discipline of packaging your frontend, backend, and dependencies into a reproducible image is what makes "works on my machine" irrelevant; drilling here shows you where image bloat and layer caching actually live.
- **AWS IAM: users, roles, and policies** — Every AWS deployment fails or succeeds on permissions before it touches a model; understanding the distinction between root users, IAM users, roles, and attached policies is the minimum to operate safely.
- **Elastic Container Registry (ECR) and image promotion** — The registry is the artifact store that connects your local build to a live service; understanding image tagging and promotion policies is what makes multi-environment deployments reproducible.
- **AWS App Runner** — The simplest container-to-production path on AWS reveals the trade-off between managed ease and control; it is the right entry point before ECS/EKS becomes necessary.
- **Cost visibility and billing hygiene** — Knowing how to read the Billing and Cost Management console and set up cost alerts before you deploy anything is the practice that separates engineers who sleep well from those who don't.

---

#### L1-02 · Infrastructure as Code with Terraform

Before Terraform, deploying to three environments meant clicking through the same console screens three times and hoping they matched. Terraform, introduced by HashiCorp in 2014, makes infrastructure a reproducible artifact: you describe what you want, and the tool reconciles the world to that description. For AI engineers, this matters because your environments — dev, staging, prod — must be structurally identical, and manual configuration drift is where production incidents are born. Understanding Terraform is the prerequisite to understanding every automated deployment pattern that follows.

**Level 2 candidates:**
- **Terraform state and remote backends** — State is how Terraform knows what it already created; remote state (in S3) is what makes it safe for a team or a CI runner to apply changes without destroying what someone else built — drilling here shows you what `terraform destroy` is actually deleting.
- **Workspaces for environment isolation** — Workspaces are the mechanism that lets you deploy the same configuration to Azure and GCP simultaneously, or maintain dev/test/prod from a single codebase without duplication; understanding their scope prevents the classic mistake of destroying the wrong environment.
- **Terraform modules and reuse** — A module is a reusable infrastructure component; understanding how to parameterise a Lambda-plus-API-Gateway block means you stop copy-pasting Terraform and start composing it.
- **Serverless architecture components: Lambda, API Gateway, S3, CloudFront** — These four services form the backbone of a cost-effective serverless AI backend; understanding how they wire together and where the latency and cold-start costs live is what lets you size and price a system before building it.
- **DNS, SSL certificates, and domain configuration** — A production URL is not a free gift from the cloud; registering a domain, routing it through Route 53, and attaching an ACM certificate reveals the full path from "deployed container" to "trusted HTTPS endpoint."

---

#### L1-03 · CI/CD and GitOps for AI Systems

The final form of production discipline is that a `git push` to the right branch triggers a tested, gated deployment — not a human running commands. GitHub Actions, introduced in 2018, made this accessible without a dedicated Jenkins server. For AI engineers, CI/CD matters most because model calls, API keys, and environment-specific configs create more failure modes than a typical web app. The deployment pipeline is also where you enforce that no one manually tweaks production — a discipline that becomes critical once agents are running on schedules and modifying live data.

**Level 2 candidates:**
- **GitHub Actions: workflows, triggers, and secrets** — Understanding how to wire a `push` to `main` into a build-test-deploy sequence — with secrets injected rather than hardcoded — is the minimum viable CI/CD for any AI system.
- **Promote-between-environments strategy** — The pattern of deploying to dev automatically, promoting to staging on approval, and gating prod on a manual step is what transforms a deployment pipeline from a convenience into a safety system.
- **Docker build and ECR push in CI** — The step where your pipeline builds the image and pushes it to the registry is where most first-time failures happen; drilling here reveals how layer caching and multi-stage builds affect build time and image size.
- **Destroy workflows and cost control automation** — Having a CI workflow that can `terraform destroy` a non-production environment on a schedule is the difference between a cloud account that accumulates idle resources and one that stays clean.

---

### Group 2 · Cloud Platforms and Multi-Cloud Awareness

A practitioner who has only operated in one cloud is one vendor lock-in away from helplessness. More practically, different clouds offer different AI-specific managed services — Bedrock on AWS, Vertex on GCP, Azure OpenAI Service — and the right service for a given project may not be the one your company already uses.

---

#### L1-04 · AWS AI Services: Bedrock and SageMaker

Amazon Bedrock, launched in 2023, is AWS's managed foundation model API — it provides access to Anthropic Claude, Meta Llama, Mistral, and others behind the same IAM and VPC controls as every other AWS service. SageMaker is the older, heavier platform for training, fine-tuning, and deploying custom models with full infrastructure control. For most AI engineers deploying third-party LLMs, Bedrock is the right surface; SageMaker becomes relevant when you need fine-tuning, custom inference endpoints, or model registries. Understanding both means you can match the tool to the problem rather than defaulting to the OpenAI Python client for everything.

**Level 2 candidates:**
- **Bedrock model invocation and streaming** — The Bedrock API differs from OpenAI's in its authentication model (SigV4, not API keys), its model IDs, and its streaming format; drilling here closes the gap between "I know how to call GPT-4" and "I can call any foundation model from AWS infrastructure."
- **Amazon Nova and model selection trade-offs** — Nova is Amazon's own family of foundation models; understanding where Nova outperforms and underperforms third-party models on cost, latency, and capability helps you make the model selection case to a client or manager.
- **SageMaker endpoints and custom inference** — A SageMaker real-time endpoint is the production surface for a custom or fine-tuned model; understanding cold starts, instance types, and autoscaling here is the prerequisite for owning fine-tuned model deployments.
- **S3 Vectors and embedding storage** — S3 Vectors (AWS's native vector storage) is where the knowledge base for a RAG system lives when you stay inside the AWS ecosystem; drilling here reveals the ingestion pipeline, index design, and query patterns that determine retrieval quality.

---

#### L1-05 · Multi-Cloud Deployment Patterns: Azure and GCP

Azure and GCP are not simply "AWS with different names." Azure's AI portfolio — Azure OpenAI Service, Azure Container Apps, Azure Functions — has enterprise identity integration (Entra ID) baked in from the start. GCP's strengths are in data pipelines (BigQuery, Dataflow) and Vertex AI for MLOps. As an AI engineer, you do not need deep expertise in all three clouds, but you need enough fluency to deploy the same containerised application across them using Terraform — which is exactly what Terraform workspaces enable. Most production enterprise environments are multi-cloud by accident or by policy.

**Level 2 candidates:**
- **Azure Container Apps vs. AWS App Runner** — These are the two most comparable managed container services; understanding the operational and pricing differences helps you advise on cloud selection when both are on the table.
- **GCP Cloud Run** — Cloud Run is Google's serverless container platform and arguably the simplest path from a Docker image to a public HTTPS endpoint across all three major clouds; it is also the right comparison point when evaluating App Runner's pricing.
- **Terraform provider differences across clouds** — The same Terraform pattern — container registry, deployed container, API gateway — requires different provider syntax and resource names across AWS, Azure, and GCP; knowing where they diverge tells you how much re-use is actually achievable.
- **Azure OpenAI Service vs. direct OpenAI API** — The Azure-hosted version of GPT-4 and other OpenAI models provides enterprise compliance guarantees (data residency, no training on your data) that matter in regulated industries; understanding when to recommend it versus the direct API is a commercial skill.

---

### Group 3 · Agentic AI Architecture and Engineering

This is where the AI content intensifies. Agents introduce a class of production failure modes that do not exist in simple LLM API call applications — they loop, they call external tools, they write to databases, and they can fail silently while accumulating cost. Building production agents requires both the architectural judgement to design the right system and the engineering discipline to make it observable and recoverable.

---

#### L1-06 · Agent Architecture Design

Anthropic's 2023 post on building effective agents established the field's vocabulary: *workflows* are systems where code orchestrates LLM calls in fixed paths; *agents* are systems where the LLM itself decides what to call next. Since that post, two further patterns have crystallised: the *multi-agent* architecture (a planner/orchestrator dispatches to specialised worker agents) and the *single agent with agentic loop* (one LLM with a long context and a to-do list, calling itself repeatedly until done — the pattern you feel when using Claude Code). The practical question is never "which is correct" but "which performs better on this specific problem given your metric" — and the answer is always experimental.

**Level 2 candidates:**
- **Multi-agent vs. single-agent with loop trade-off** — Understanding when breaking concerns into separate agents improves performance (complex specialisation, parallel work) versus when it degrades it (coordination overhead, context loss between hops) is the central architectural judgement call in agentic AI.
- **Planner / orchestrator / worker decomposition** — The pattern of having one LLM reason about what needs to happen and dispatch to specialised workers mirrors classic software decomposition; drilling here shows where context engineering for each worker becomes the bottleneck.
- **Agentic loop design and termination conditions** — A loop without a well-designed termination condition is an infinite loop; understanding how agents manage their own to-do lists, detect task completion, and handle failures is what separates a demo from a system that can run unsupervised.
- **When to start simple: the one-LLM-call baseline** — Every agent evaluation should begin with a single LLM call and a metric; understanding why practitioners skip this step — and what it costs them — is the most important lesson in agentic architecture.
- **Context engineering vs. prompt engineering** — Context engineering (curating everything in the agent's context window — memory, tools, history, instructions) is the discipline that replaces prompt tweaking once you are building systems; drilling here shows how the quality and structure of context determines agent reliability.

---

#### L1-07 · MCP (Model Context Protocol) and Tool Integration

MCP, formalised by Anthropic in 2024, is a standardised protocol for giving agents access to external tools and data sources without bespoke integration code. Before MCP, connecting an agent to a database, a web browser, or a third-party API required custom tool definitions for each model client. With MCP, you build or deploy an MCP server once and any compliant agent can use it. In production, MCP servers are typically deployed as their own containers — giving them independent scaling, logging, and failure isolation from the agent that calls them. Understanding MCP is now a prerequisite for building agents that interact with the real world.

**Level 2 candidates:**
- **MCP server deployment and containerisation** — An MCP server is not a library call — it is a running service; understanding how to deploy it as its own container, expose it to your agent, and manage its lifecycle is what makes MCP production-ready rather than demo-ready.
- **Tool selection and MCP server composition** — An agent equipped with multiple MCP servers (web search, stock data, a database) behaves very differently depending on how those tools are described; drilling here reveals how tool descriptions shape agent behaviour.
- **Building custom MCP servers** — When no existing MCP server covers your data source or API, you write one; understanding the server interface and the tool definition format is the skill that unlocks arbitrary tool integration.
- **Playwright-based browsing via MCP** — The browsing MCP server uses Playwright to give agents a real web browser; this introduces timeout failures, anti-bot detection, and page-structure dependency that do not exist in pure API calls — drilling here reveals the failure modes of agentic web research.

---

#### L1-08 · Data Pipelines, Vector Storage, and RAG

A production agent that cannot look up information beyond its training cutoff is a prototype. RAG (Retrieval-Augmented Generation) is the pattern that fixes this: external data is chunked, embedded, stored in a vector store, and retrieved at inference time. The engineering challenge is that the *ingest pipeline* — the system that keeps your vector store current — is a continuous, scheduled process with its own failure modes, costs, and monitoring requirements. In the AWS ecosystem, this pipeline typically involves Lambda (for trigger/scheduling), S3 (for raw storage), a vector store (S3 Vectors, Pinecone, or similar), and an agent loop for web research.

**Level 2 candidates:**
- **Embedding models and chunking strategy** — The quality of retrieval is determined before a single query is issued; understanding how chunk size, overlap, and embedding model choice affect recall and precision is what separates a RAG system that works from one that embarrasses you in front of users.
- **S3 Vectors as a serverless vector store** — AWS's native vector storage removes the need for a separate vector database in many architectures; drilling here reveals the index design, query interface, and cost model that determine when it is and is not the right choice.
- **Scheduled ingest with Lambda and EventBridge** — Running a research agent on a schedule (every two hours, every night) via EventBridge triggering a Lambda is the production pattern for keeping a knowledge base current; understanding retry behaviour and failure alerting here is critical.
- **Agent-driven web research pipelines** — Using an agent with browsing and search tools to populate a vector store is qualitatively different from a traditional ETL pipeline — the agent decides what to fetch, what to summarise, and what to store; drilling here reveals how to structure the agent's research brief and how to detect when it goes off-track.
- **API Gateway throttling and rate limiting** — When your data ingest pipeline exposes an API endpoint, rate limiting and API key management are the controls that prevent runaway agent loops from generating unexpected bills.

---

### Group 4 · Production Operations and Enterprise Readiness

This is the material that distinguishes an AI engineer who can ship from one who can operate. Systems that work in demos fail in production because of authentication edge cases, cost spikes at scale, silent agent failures, and the absence of observability. This group covers what makes an AI system trustworthy enough to hand to a business.

---

#### L1-09 · Authentication, Subscriptions, and SaaS Plumbing

Clerk (for authentication) and Stripe (for subscription billing) are the two managed services that allow a solo AI engineer to ship a subscription SaaS without building auth or payment infrastructure from scratch. Clerk handles session management, OAuth providers, and user identity; Stripe handles plan gating, webhooks, and payment processing. Understanding how these wire into a Next.js + FastAPI stack — and how to enforce plan-based access at the API level — is the difference between a demo and a product you can charge for.

**Level 2 candidates:**
- **Clerk session tokens and API-level enforcement** — The browser holds a JWT; the backend must validate it on every request; understanding where validation lives in a FastAPI app is what prevents your paid features from being accessible without a subscription.
- **Subscription plan gating** — Mapping Clerk subscription plans to feature flags or rate limits on the backend is the engineering pattern behind a freemium product; drilling here shows the state-management edge cases (lapsed subscriptions, concurrent sessions, plan upgrades mid-session).
- **Static frontend served by backend container** — Compiling a Next.js frontend to static assets and serving them from FastAPI inside a single Docker container is the pattern that makes a full-stack app deployable as one unit; understanding the build step and the FastAPI static file mount removes the need for a separate CDN for small-scale deployments.
- **HTTPS and domain ownership in production** — A production SaaS needs a real domain, a real SSL certificate, and a real DNS configuration; understanding the ACM + Route 53 + CloudFront or equivalent chain is non-negotiable for anything you put in front of a customer.

---

#### L1-10 · Observability, Monitoring, and Security for AI Systems

In a traditional web app, observability means logging HTTP requests and tracking error rates. In a production AI system, the interesting failures are semantic, not syntactic: the agent that loops forever, the retrieval step that returns irrelevant chunks, the LLM call that silently degrades in quality after a model version bump. Observability for AI systems therefore has to include logging at the agent step level, cost per conversation, latency per tool call, and — increasingly — some form of output quality monitoring. CloudWatch on AWS is the entry point; purpose-built LLM observability platforms (LangSmith, Weights & Biases, etc.) are the next layer.

**Level 2 candidates:**
- **CloudWatch logs and structured logging for LLM calls** — Emitting structured logs (model name, token count, latency, tool called) from every LLM interaction is the minimum viable observability for a production agent; drilling here shows what you need to reconstruct a failed agent run after the fact.
- **Cost per request and token usage tracking** — An agent that calls five LLMs in a loop can cost 50× more per request than expected; understanding how to instrument token usage and set budget alerts before you go live is cheaper than discovering the spike after your monthly bill arrives.
- **Scalability patterns: SQS for task queue resilience** — Wrapping a long-running agent task in an SQS queue means a timeout or error triggers an automatic retry rather than a silent failure; drilling here reveals the dead-letter queue pattern and when it is worth the added infrastructure complexity.
- **Security boundaries: IAM roles for Lambda, VPC placement** — Each Lambda function should have the minimum IAM permissions it needs and nothing more; understanding least-privilege role assignment and when to put a function inside a VPC is what prevents a compromised agent from becoming a cloud account breach.
- **Explainability and output validation** — Understanding how to add output schema validation (structured outputs, JSON mode), confidence checks, and human-in-the-loop gates to an agent pipeline is the engineering practice that makes an AI system trustworthy enough for regulated use cases.
- **Multi-agent observability: tracing across hops** — When a planner calls three worker agents, a single request spans multiple LLM calls, multiple tool invocations, and potentially multiple containers; understanding how to propagate a trace ID across that chain is what makes debugging a production multi-agent system tractable.

---

## Sequencing Note

The logical dependency chain runs through three layers. You cannot reason sensibly about agent architecture without first being able to deploy a basic container and understand what it costs to run. You cannot build a resilient data ingest pipeline without understanding serverless scheduling and vector storage. And you cannot make observability decisions without having built something that fails in a way you need to observe.

**The recommended entry point for this learner profile** is L1-01 and L1-02 in parallel — getting a container live on AWS and learning Terraform to define that infrastructure declaratively. These two topics unlock everything else and are where the majority of the friction concentrates for practitioners coming from an ML or application background.

**The highest-leverage sequence thereafter:** L1-03 (automate the deployment) → L1-06 (understand agent architecture before building agents) → L1-07 (MCP for tool integration) → L1-08 (data pipelines and RAG) → L1-10 (make it observable). L1-04 and L1-05 can run in parallel with the middle of this chain once L1-01 is solid; L1-09 is best addressed at the point where you are ready to put something in front of users.

**The dependency to watch:** L1-08 depends on L1-06. Engineers who build data pipelines before understanding agent architecture tend to build pipelines that are structurally incompatible with the agents that need to use them — a costly rework. Get the architecture right first.

## Source

https://www.udemy.com/course/generative-and-agentic-ai-in-production/