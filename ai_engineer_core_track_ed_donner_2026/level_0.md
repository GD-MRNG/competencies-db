# AI Engineer Core Track — Level 0: Course Map

> **Intent:** Build the ability to architect and deploy functional AI systems that move beyond isolated model calls—understanding how to run models locally, orchestrate them across providers, and wire them into autonomous feedback loops.
>
> **Your angle:** You have professional development experience. This track teaches you to think of AI as decoupled inference (separable from your application logic), manage context explicitly (models are stateless), and navigate the central tradeoffs (cost vs. reasoning, latency vs. capability, autonomy vs. control). You're learning to be the architect of the system, not a consumer of ChatGPT.

---

## How to Use This Map

This map is organized into three layers, reflecting the stack from **Infrastructure** to **Orchestration**.

**Level 1 topics** are the conceptual anchors—each one represents a significant shift in what you can build. Start with a topic that addresses an immediate problem you're facing.

**Level 2 candidates** are the sub-concepts within each topic. Use them to diagnose knowledge gaps: if a description makes you think "I don't know how that works," descend into it.

The **Sequencing note** at the end identifies which topics unlock which others and suggests entry points based on your project type.

---

## Topic Inventory

### **Foundations: The Model as a Tool**

#### L1-01 · Decoupled Inference

The separation of the "brain" (the model) from the "body" (your application code) is the foundational idea of AI Engineering. Before this concept existed, AI was locked inside a product (a website like ChatGPT); after it, AI becomes a programmable utility. This distinction unlocks the entire stack: you can now swap models, run them locally or remotely, and wire their outputs into larger systems. The critical insight is that **inference is a service**, not magic.

**Level 2 candidates:**

- **Local vs. Remote Trade-off** — Why running a model on your own hardware feels fast but limited, while cloud APIs feel expensive but unrestricted; how to choose based on data sensitivity and task complexity.
- **Model as a Function** — Understanding that a model call (`client.chat.completions.create()`) is just HTTP + JSON; the architecture doesn't care if the model is on your laptop or OpenAI's servers.
- **The Statelessness Problem** — Models have no built-in memory; every call is a fresh start. This is the single most important realization for an AI Engineer, because it means *you* are responsible for reconstructing context.
- **The Illusion of Memory** — The pattern of re-sending the full conversation history (messages list) with every API call to simulate continuity; why this is necessary and when it breaks down.
- **Provider Agnosticism** — How the OpenAI API standard (chat.completions) became near-universal, allowing you to swap between providers (cloud labs, open-weight models via Ollama, etc.) without rewriting your core logic; verify which providers are currently compatible, as the ecosystem shifts.

---

#### L1-02 · Tokenization and Context Windows

The model doesn't read text the way humans do. It converts your words into **tokens**—atomic units of meaning (roughly 4 characters per token, but it varies). This seemingly low-level detail cascades upward: it determines how much you can fit in a prompt, how much you'll be billed, and whether the model will "forget" the beginning of a long conversation. Understanding tokens is understanding the economic and architectural constraints of your system.

**Level 2 candidates:**

- **Token Encoding (Tiktoken)** — How text becomes integers, why different models use different tokenizers, and how to count tokens programmatically before you send them.
- **Context Window Limits** — The maximum number of tokens a model can ingest in one call (4K to 200K+); how this became a primary differentiator between models and shaped the design of RAG systems.
- **The Cost-Context Tradeoff** — Why throwing all your company's documents into every prompt feels efficient but is actually expensive (you pay per token, per request) and leads to latency and context degradation.
- **Batching and Streaming** — Requesting multiple completions in parallel (batch processing) vs. receiving tokens one at a time (streaming); when to use each to optimize latency and cost.

---

#### L1-03 · The Transformer Architecture as a Pattern Recognition Engine

The Transformer (2017, Vaswani et al.) unified text, code, and images under one architecture: sequences of tokens processed by **self-attention** layers. You don't need to implement self-attention from scratch, but you need to understand the *story*—that the model is **predicting the next most likely token** based on everything it has seen before, and this simple iterative process produces reasoning, code generation, and creative writing. This is the "why" behind emergent capabilities.

**Level 2 candidates:**

- **Self-Attention and "Understanding Context"** — How the model attends to relevant parts of the input; why it can sometimes "know" about something mentioned 50 tokens ago and sometimes loses it.
- **Emergent Capabilities** — Why a model trained to predict the next token can suddenly solve math problems or write code it never "saw" in training; the philosophical puzzle of how compression becomes intelligence.
- **The Scaling Laws** — Larger models (more parameters) generally perform better; more data helps too. This relationship is predictable (the Scaling Laws), which is why companies bet billions on frontier models.
- **From Text to Multimodal** — How the same Transformer backbone can be extended to handle images, audio, or video by converting them to tokens; the architecture doesn't care what kind of sequence it processes.

---

### **Core Infrastructure: Building with Models**

#### L1-04 · Local Inference: Ollama and Environment Hermeticity

Running a model on your own hardware (your laptop, a local GPU server) gives you full privacy, zero per-token costs, and the ability to prototype without API keys. The trade-off: you're limited by your hardware (RAM for the model, VRAM for inference speed), and smaller models are less "intelligent." **Ollama** packages models and their dependencies into a simple local service; **UV** ensures your Python environment is reproducible and fast. This combination lets you spin up a private AI lab in minutes.

**Level 2 candidates:**

- **Model Weight Distribution and Quantization** — Why a 70B-parameter model can fit on consumer hardware; how quantization (storing weights in lower precision) trades off accuracy for speed and memory.
- **Ollama as a Service** — Running Ollama as a background daemon, querying it via OpenAI-compatible HTTP endpoints; how this abstracts away the complexity of model serving.
- **UV and Dependency Hell** — Why older tools (pip, conda) leave you guessing about reproducibility; how UV locks exact versions and compiles dependencies in a way that "just works" across machines.
- **The Hardware Bottleneck** — Understanding VRAM requirements, batch sizes, and when your GPU is the constraint vs. when your CPU or disk I/O is; profiling your bottleneck before optimizing.

---

#### L1-05 · API-Based Inference: Frontier Models and Vendor Ecosystems

Cloud APIs give you access to **frontier models**—the largest, most capable models available at any given time—with zero hardware setup and automatic scaling. The cost is operational: you pay per token, you depend on a third-party's uptime, and you send your data to their servers. The strategic choice (local vs. cloud) dominates your architecture. The landscape of providers and their relative capabilities shifts quickly; treat any specific lab or model name as an illustrative example rather than a current ranking, and verify the latest state at community leaderboards or official lab sites.

**Level 2 candidates:**

- **Pricing Models and Hidden Costs** — Distinguishing between per-token costs, per-request minimums, batch pricing, and "hidden" tokens (like reasoning steps that you pay for but don't see). Cost estimation before shipping.
- **Rate Limits and Quota Management** — How to structure retries, exponential backoff, and request queuing when you hit rate limits; designing for resilience.
- **Latency and Tail Percentiles** — Understanding that APIs have variable latency; designing systems that tolerate 95th-percentile slowness without cascading failures (timeouts, circuit breakers).
- **API Key Management and Environment Variables** — The `.env` file pattern; why hardcoding secrets is a critical security failure and how to rotate keys in production.

---

#### L1-06 · Prompt Engineering as Architecture

A prompt is not decoration; it is the interface between your intention and the model's output. Effective prompts are **architectural decisions**: they encode the persona, the constraints, the output format, and the reasoning pattern. A tight System Message is worth more than a dozen examples. This is the "glue code" of AI Engineering—it's what allows you to tune a model's behavior without fine-tuning.

**Level 2 candidates:**

- **System Message Design** — The blueprint of the model's role: who it is, what it does, what it cares about. A bulletproof System Message requires iteration; it's your primary lever for controlling behavior.
- **In-Context Learning (Few-Shot Prompting)** — Providing examples inside the prompt to show the model what you want; when examples help and when they just waste tokens.
- **Chain-of-Thought and Reasoning Patterns** — Asking the model to "think step by step" (or even asking it to give a wrong answer first, then correct itself); how to coax a model toward reasoning vs. pattern matching.
- **Structured Output Expectations** — Communicating (through the System Message and examples) that you expect JSON, XML, or Markdown; the precursor to Structured Outputs (Pydantic + Constrained Decoding).

---

### **Model Orchestration: Beyond a Single Call**

#### L1-07 · Model Agnosticism and Provider Switching

No single provider dominates forever. The ability to swap models—different labs for different strengths (reasoning, speed, cost, privacy)—without rewriting your application is a strategic asset. This requires **abstraction**: you write to a standardized interface (chat.completions) and route to different providers via configuration. The OpenAI API became the de facto standard, but you're not locked in if you design for it. Which provider is best for which task changes as new models release; treat capability comparisons as a snapshot, not a constant.

**Level 2 candidates:**

- **API Standardization (OpenAI Compatibility)** — The chat.completions format became universal; how to write provider-agnostic client code using simple URL/API key swaps.
- **Model Capability Matrices** — Understanding that models have different strengths (reasoning depth, speed, context length, cost); building decision trees that select the right model for the task. Specific model rankings shift with every release cycle — check current leaderboards (e.g., LMSYS Chatbot Arena, Hugging Face Open LLM Leaderboard) rather than treating any snapshot as stable.
- **Fallback Strategies** — What to do when a provider is down, rate-limited, or too expensive; designing graceful degradation (use local model, cache previous results, return a sensible default).
- **Benchmarking and Vendor Lock-in Risk** — How to evaluate whether switching is worth the engineering effort; understanding the cost-accuracy-latency surface for different models.

---

#### L1-08 · Tool Calling (Function Calling) and the Bridge to Real Data

Models can't access the internet, your database, or the current date. **Tool Calling** is the mechanism where the model generates a structured request (e.g., `{"function": "search_database", "args": {"query": "..."}}`), your application executes it, and you feed the result back into the conversation. This is how you wire AI into the real world without embedding data directly into the prompt.

**Level 2 candidates:**

- **Tool Definition Format** — Describing a function (its name, parameters, description) in JSON so the model understands what it can call; the schema becomes the contract.
- **The Tool Loop** — The pattern: LLM decides it needs data → generates a tool call → you execute and return the result → you feed it back to the LLM. Repeating until the task is complete.
- **Constraining Tool Use** — Ensuring the model only calls tools you've defined; preventing hallucinated function calls through constrained decoding or validation layers.
- **Parallel Tool Calls** — Modern models can request multiple tools at once (e.g., fetch weather AND search news simultaneously); orchestrating execution and re-injection for speed.

---

#### L1-09 · Retrieval-Augmented Generation (RAG) as a Pattern

RAG solves the problem of knowledge that's too large, too fresh, or too specific to fit in the model's training data. Instead of fine-tuning, you **retrieve relevant documents at inference time** and stuff them into the context. This is the workhorse pattern for Q&A systems, summarization, and any task where "up-to-date factual accuracy" matters more than behavioral adaptation. The trade-off: you're paying for tokens (the retrieved docs in every request) and depending on your retrieval quality.

**Level 2 candidates:**

- **Embedding-Based Retrieval (Vector Databases)** — Converting documents into dense vectors via an embedding model; using vector proximity (cosine similarity) to find relevant documents. Different from keyword matching.
- **Chunking and Metadata** — How to split long documents into digestible chunks so the retriever can be precise; adding metadata (source, date, author) so the model knows *where* information came from.
- **Retrieval Quality vs. Token Waste** — Why fetching 10 irrelevant documents and putting them in the prompt wastes tokens and confuses the model; how to tune the number of results and the retrieval threshold.
- **RAG vs. Fine-Tuning Trade-off** — When to add knowledge via RAG (for fresh, factual data) vs. fine-tuning (for behavioral adaptation, style, format); they solve different problems.

---

#### L1-10 · Model Fine-Tuning: Baking Behavior into Weights

If RAG is "look it up," fine-tuning is "remember it." You start with a pre-trained model and update its weights using your own data. This bakes in specialized knowledge, style, or behavior. Fine-tuning is expensive (compute + data annotation) and risky (overfitting, where the model memorizes your training set and fails on new examples). But when it works—when you've curated clean data and validated on a holdout set—it's powerful.

**Level 2 candidates:**

- **Training Loop and Validation Strategy** — The pattern: forward pass, compute loss, backward pass, update weights. The critical skill is **monitoring validation loss** to catch overfitting before it ruins your model.
- **Prompt Templates and Data Format** — Fine-tuning requires data in a specific format (usually messages lists with system/user/assistant roles); getting the format wrong wastes time and money.
- **Overfitting and the Weights & Biases Valley** — The point where training loss keeps dropping but validation loss starts climbing—that's where your model is memorizing, not generalizing. Go back to that checkpoint.
- **Parameter-Efficient Methods (LoRA, Adapters)** — Alternatives to fine-tuning the entire model; updating only a small subset of parameters to save compute; useful when you have limited budget.

---

### **Production and Autonomy: The Final Mile**

#### L1-11 · Structured Outputs and Constrained Decoding

Raw LLM outputs are fuzzy: "sometimes valid JSON, mostly." **Structured Outputs** (Constrained Decoding) are the mathematical enforcement of a schema during generation. Instead of hoping the model returns JSON, the system zeros out invalid tokens in real-time, guaranteeing the output matches your schema. This is the only reliable way to wire AI into strict software systems (databases, APIs, transactions).

**Level 2 candidates:**

- **Pydantic Schema Definition** — Writing type-safe Python dataclasses that define exactly what the model must return; the schema becomes your contract.
- **Token Elimination During Generation** — How constrained decoding works: at each step, the model generates probability scores for the next token, and the system masks illegal tokens (e.g., any character that violates JSON syntax), forcing a valid path.
- **Performance Cost and Trade-offs** — Structured Outputs add latency because they constrain the model's freedom; measure whether the overhead is worth the reliability gain.
- **Recursive Schemas and Nested Data** — Defining complex, hierarchical outputs (objects containing arrays of objects); ensuring the LLM can generate deeply nested structures without errors.

---

#### L1-12 · Agentic AI and Autonomous Loops

An **agent** is a system that enters a loop: perceive state → reason about options → act via tools → observe results → repeat. The model becomes a decision-maker, not a one-shot oracle. This unlocks autonomy: the agent can monitor feeds, make decisions, and take actions without human intervention between steps. The cost is complexity: you need to manage state, handle failures, define when loops terminate, and (crucially) decide when humans should be in the loop.

**Level 2 candidates:**

- **The Perception-Reasoning-Action-Observation Cycle** — The core loop: the agent sees the current state and goal, decides which tool to use, generates a tool call, you execute it, and the results feed back. Repeating until done or timeout.
- **Agent Frameworks (LangChain, CrewAI) vs. First Principles** — Frameworks speed up scaffolding but obscure the underlying loop; understand the mechanics first before using a framework, or you'll be helpless when it breaks.
- **Goal Specification and Termination Conditions** — Defining what "done" means; preventing infinite loops through explicit termination conditions, token budgets, or iteration limits.
- **Human-in-the-Loop Patterns** — When high-risk actions (financial transfers, deletions) require approval; designing escalation and review checkpoints into agent workflows.

---

#### L1-13 · Serving and Scaling: Infrastructure for Production

Models are stateless functions, but serving them reliably requires infrastructure: load balancing, caching, monitoring, and scaling. **Serverless GPU platforms** (Modal) let you deploy agents without managing Kubernetes. **Vector databases** (Chroma, Pinecone) become your agent's long-term memory. **Interface layers** (Gradio, FastAPI) connect the agent to users. This layer bridges the gap between "working on my laptop" and "deployed in production."

**Level 2 candidates:**

- **Serverless GPU Infrastructure (Modal)** — Deploying models and agents without owning hardware; the cost is cold-start latency (30-60s if the infrastructure isn't "warm"); when it's acceptable and when you need alternatives.
- **Caching and Semantic Deduplication** — Storing frequently-used outputs (embeddings, API calls) to avoid redundant compute; when exact-match caching applies and when you need semantic equivalence.
- **Monitoring and Observability** — Tracking model behavior in production (latency, cost, error rates); understanding when a model is "broken" (hallucinating) vs. when the system is (API down, network issue).
- **Cost Optimization at Scale** — Managing token spend across many requests; understanding when batch processing is worth the latency trade-off; identifying runaway costs before they hit your bill.

---

#### L1-14 · The System Architecture: Wiring It All Together

A production AI system is not a single model—it's an orchestration of models, RAG systems, fine-tuned specialists, and hard-coded workflows. The **architecture** decides where logic lives: in the model (via prompting), in the code (rule engines), in the data (fine-tuning), or in the inference-time context (RAG). Understanding these trade-offs is what separates a prototype from a production system.

**Level 2 candidates:**

- **Ensemble Approaches** — Why multiple models (e.g., a planner + workers) often outperform a single model; using different models for different stages of reasoning.
- **RAG vs. Fine-Tuning vs. Hard-Coded Logic** — The decision tree: Is this knowledge that changes daily? Use RAG. Is this a behavioral pattern unique to your company? Use fine-tuning. Is this a well-defined rule? Hard-code it.
- **Cost-Accuracy-Latency Surface** — Understanding that fast, cheap, and accurate are usually in tension; visualizing the trade-offs for your specific use case; iterating on the best operating point.
- **Error Handling and Graceful Degradation** — Designing for failure: what happens when the model hallucinates, the vector DB is down, or the API times out? Building fallbacks that keep the system running.

---

#### L1-15 · Observability and Iteration: Measuring What Matters

You can't improve what you don't measure. **Observability** means instrumenting your system so you can diagnose problems: Did the agent go off the rails? Is the retriever finding relevant documents? Did a model change break my application? Measuring **latency, cost, accuracy,** and **user satisfaction** is the feedback loop that separates hype from utility.

**Level 2 candidates:**

- **Logging and Tracing** — Recording every model call, tool invocation, and decision point; tracing requests end-to-end to find where failures happen.
- **Evaluation and Test Sets** — Defining what "correct" means for your application; building test cases and benchmarks so changes can be validated automatically.
- **A/B Testing and Canary Deployments** — Rolling out model changes gradually; comparing metrics between old and new versions; ensuring improvements are real before full rollout.
- **Cost Attribution and Token Accounting** — Tracking which features, users, or workflows consume the most tokens; making decisions about cost optimization based on data.

---

## Sequencing Note

**This track is the foundation.** Everything in the Agentic Track and Production Track depends on mastering these concepts. You cannot skip it.

### ⚠️ Critical Warning: Don't Skip to Production

A common mistake: looking at the Production Track and thinking "I'll just learn Docker and cloud deployment, skip the AI fundamentals." **This will fail.** You cannot deploy systems reliably if you don't understand:

- **Context windows** (L1-02): If you don't know how many tokens fit in a prompt, you'll build systems that break when users ask longer questions.
- **Statelessness** (L1-01): If you don't understand that models have no memory, you'll expect features that can't work, wasting weeks debugging phantom bugs.
- **Tool calling** (L1-08): If you don't understand how to wire models to real data, you'll ship hallucinating systems that make up facts.
- **Structured outputs** (L1-11): If you don't understand schema enforcement, your production system will crash when the model's JSON is malformed.

**Do yourself a favor:** Complete the Core Track first. It's 15 topics and takes 2-4 weeks of focused learning. Every hour invested here saves 10 hours of debugging production issues later.

### The Three Tracks Explained

The Core Track has four layers that build on each other:

1. **Foundations (L1-01 to L1-03)**: Start here. Understand that inference is decoupled, models are stateless, and the Transformer is predicting the next token. These concepts underpin everything that follows.

2. **Infrastructure (L1-04 to L1-06)**: Once you understand the model as a service, you need to actually run one. Choose between local (Ollama + UV) or cloud (API-based), and learn to tune behavior through prompting. The decision between local and cloud cascades through all downstream choices.

3. **Orchestration (L1-07 to L1-10)**: Now you can build beyond single calls. Model agnosticism lets you swap providers; tool calling wires the model to real data; RAG and fine-tuning add knowledge at different points in the inference pipeline. These are the techniques that turn a model call into a functional system.

4. **Structured Reliability (L1-11 to L1-15)**: Enforce reliability through structured outputs, manage your architecture, and add observability. This layer bridges to the Agentic Track (autonomous systems) and Production Track (scaling and reliability).

**How this relates to other tracks:**

- **Core → Agentic:** The Agentic Track assumes you understand decoupled inference, context management, tool calling, and structured outputs. Master L1-08 (Tool Calling) and L1-11 (Structured Outputs) before moving to agentic loops.
- **Core → Production:** The Production Track assumes you understand models as services, prompting, and basic architecture. Master all of Core before worrying about containerization and cloud deployment.
- **Core + Agentic + Production:** These tracks are cumulative. You build knowledge in Core, add reasoning loops in Agentic, and productionize in Production.

**High-leverage entry points depend on your problem:**

- **"I need to build a prototype quickly"** → Start with L1-01 (Decoupled Inference), then jump to L1-05 (API-Based Inference). Use an OpenAI API call to get working proof-of-concept in minutes.
- **"I need to keep my data private"** → L1-04 (Local Inference) first, then L1-02 (Tokenization) to understand context limits, then L1-08 (Tool Calling) to wire it to your database.
- **"I need my system to reason over documents"** → L1-01, then L1-09 (RAG). Build a retrieval pipeline before worrying about agent loops.
- **"I need an autonomous system that takes actions"** → Complete Core (all 15 topics), then move to the **Agentic Track**. Don't skip; agentic systems are built on top of reliable single-call inference.
- **"I need to deploy to production"** → Complete Core and Agentic, then move to the **Production Track** for containerization, cloud deployment, and scaling.

**The dependency chain within Core:**

- L1-02 (Tokenization) depends on L1-01 (Decoupled Inference). You can't understand tokens without understanding that you're calling a remote service with constraints.
- L1-04 and L1-05 (Local vs. API) are alternatives; pick one, but understand the other's trade-offs.
- L1-07 (Model Agnosticism) depends on understanding the differences between L1-04 and L1-05; it's how you design to survive changes.
- L1-08 (Tool Calling), L1-09 (RAG), and L1-10 (Fine-Tuning) are independent; you can tackle them in any order, but together they form the "knowledge integration" layer.
- L1-11 (Structured Outputs) and L1-12 (Agentic AI) are closely related; understanding L1-11 makes agentic systems reliable.
- L1-13 (Serving and Scaling), L1-14 (System Architecture), and L1-15 (Observability) apply to everything; don't defer them too long or you'll build systems you can't debug or scale.

**The shortest path through Core:** L1-01 → L1-05 → L1-06 (Prompt) → L1-08 (Tools) → You now understand the basic pattern. Continue with L1-11 (Structured Outputs) before moving to Agentic Track.

**The path to being ready for Agentic Track:** Complete all of Foundations + Infrastructure + Orchestration + Structured Reliability. Then move to the Agentic Track.

**The path to being ready for Production Track:** Complete all of Core + Agentic Tracks. Then move to Production Track for deployment.

## Source

https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/