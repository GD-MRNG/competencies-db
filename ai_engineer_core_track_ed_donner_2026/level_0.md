# AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents — Level 0: Course Map

> **Intent:** To develop end-to-end capability for building production-grade AI systems — from calling frontier APIs through fine-tuning your own model and orchestrating autonomous agents.
>
> **Your angle:** You're not here to understand LLMs abstractly. The course is structured so that every concept earns its place by doing something. Arrive with software instincts; leave with the ability to make principled architectural decisions: when to RAG vs fine-tune, when to quantize, when a single LLM call beats an agent framework.

---

## How to use this map

This map reflects a deliberate 8-week sequence. Level 1 topics are the major conceptual and practical stations. Level 2 candidates are the sub-concepts where the real leverage lives — things that break in surprising ways if you skip them, or unlock adjacent territory once you grasp them.

Descend to Level 1 when you want the full picture of a station: its historical motivation, its tradeoffs, its dependencies on other stations. Descend to Level 2 when something in a Level 1 explanation prompts a genuine "but why does that work?" — those are the questions that separate a practitioner from a user.

---

## Topic Inventory

---

### Group 1 — Foundations: APIs, Models, and the Development Environment

This cluster establishes the operational baseline. Nothing in Groups 2–4 is reachable without fluency here. The emphasis is on removing the mystery from how models are called, how open-source models run locally, and why the hardware story matters.

---

#### L1-01 · The Chat Completions API and the Inference Loop

The API that launched the modern LLM era — OpenAI's `chat.completions.create` — formalised a conversation paradigm that every major provider now mimics. Before this, interacting with language models required custom pipelines; the Chat Completions interface gave developers a uniform surface. Understanding it means understanding tokens (the unit of I/O), context windows (the constraint on memory), streaming (for real-time UX), and response formats (JSON mode for structured output). This is the bedrock everything else in the course is built on top of.

**Level 2 candidates:**
- **Tokens and tokenisation** — drilling here reveals why the same text has different costs across models and why whitespace and punctuation behave unexpectedly at context boundaries.
- **Context window mechanics** — understanding this unlocks why "the illusion of memory" exists and why RAG is necessary at all: the model sees only what fits in its window.
- **Streaming responses** — what breaks if you don't understand how tokens arrive incrementally, and why UX and server architecture both depend on it.
- **Structured output / JSON mode** — the difference between asking a model to "return JSON" and actually enforcing a schema; what fails downstream when you assume the former works.
- **Multi-shot prompting** — how adding worked examples in the prompt is the fastest, cheapest way to shift model behaviour before you ever touch fine-tuning.
- **System vs user messages** — the design decision baked into the API architecture: what each role is for, and what breaks when you collapse them.

---

#### L1-02 · Frontier Model Landscape: GPT, Claude, Gemini, DeepSeek, Grok

From 2020 to 2025, the frontier model landscape went from a near-monopoly (GPT-3) to a competitive market with meaningfully different architectures, training philosophies, and character. Each provider exposes roughly the same API surface but produces measurably different outputs on reasoning, creativity, safety, and cost. Knowing how to call all of them through one client library (the OpenAI SDK pattern, reusing `base_url`) is a practical skill; knowing when to choose one over another is a strategic one. This topic also introduces the reasoning vs chat vs hybrid model distinction — one of the most consequential model-selection variables.

**Level 2 candidates:**
- **Reasoning effort and inference-time scaling** — what changes when you increase `reasoning_effort` from `minimal` to `high`, and why more compute at inference time is a substitute for a bigger model at training time.
- **OpenAI-compatible client pattern** — the trick of reusing the OpenAI Python client against Anthropic, Google, and local endpoints; understanding this is what makes multi-provider workflows practical.
- **Model character and alignment differences** — why DeepSeek and Grok answer the Prisoner's Dilemma differently to Claude and GPT; the training and alignment choices that produce these differences.
- **OpenRouter as an abstraction layer** — when a routing/aggregation layer earns its place, and what you lose when you add one.
- **API cost and rate limits** — why cost-per-token, rate limits, and time-to-first-token are the three variables that determine whether a model choice is commercially viable.

---

#### L1-03 · Running Open-Source Models Locally with Ollama

Before Ollama (2023), running an open-source LLM locally required assembling a pipeline from Hugging Face weights, quantisation tooling, and custom inference code. Ollama packaged this into a single CLI, exposing an OpenAI-compatible endpoint — the same API surface, local hardware. This matters because it gives you a zero-marginal-cost inference environment for development and experimentation, and it concretely illustrates the difference between a *packaged runtime* and the actual model weights and code underneath.

**Level 2 candidates:**
- **GGUF format and quantised model files** — how models are packaged into a single file for efficient CPU/GPU inference, and why this differs architecturally from running raw PyTorch weights.
- **Local vs cloud inference tradeoffs** — what you actually pay for when you "run for free" locally: power, latency, and hardware constraints.
- **Model size and parameter count** — why 270M parameters produces a very different experience to 8B, and what the number actually tells you about what the model can absorb.
- **Ollama as an OpenAI-compatible server** — the specific port/endpoint pattern, and why this architectural choice matters for switching between local and cloud inference without code changes.

---

#### L1-04 · Hugging Face Platform and Libraries

Hugging Face is the infrastructure layer for the open-source AI ecosystem. It plays two distinct roles that are easy to conflate: (1) the Hub — a GitHub-style repository of 2M+ models, 500K+ datasets, and deployable Spaces; and (2) the Python libraries — `transformers`, `datasets`, `peft`, `accelerate`, `trl`, and `hub` — that let you download, run, and modify models in code. The distinction between running a model via Ollama (a packaged binary) and running it via Hugging Face Transformers (Python code you can step through and modify) is one of the most important conceptual splits in the course.

**Level 2 candidates:**
- **The Hub vs the Transformers library** — why these are two separate things with the same name, and why conflating them causes real confusion when trying to download a model in code.
- **Transformers `pipeline` API vs raw `AutoModelForCausalLM`** — what the pipeline abstraction hides from you, and when you need to bypass it to access the model's internals.
- **Tokenisers as a separate object** — why tokenisation is decoupled from the model, and what breaks if you use the wrong tokeniser for a given set of weights.
- **PEFT and the LoRA adapter pattern** — why `peft` exists as a separate library rather than being part of `transformers`, and what it enables that vanilla fine-tuning cannot.
- **Hugging Face Datasets library** — how it handles datasets too large to fit in memory, and why efficient iteration matters for fine-tuning at scale.
- **Google Colab as a GPU rental environment** — why a T4 with 15GB VRAM is sufficient for most week-3 and week-7 workloads, and how to reason about memory headroom.

---

### Group 2 — Retrieval-Augmented Generation

RAG is the highest-leverage inference-time technique for giving an LLM expertise it wasn't trained on. It is architecturally simple — retrieve relevant context, inject it into the prompt — but the engineering details of the retrieval step are where most production RAG systems succeed or fail.

---

#### L1-05 · The RAG Architecture: From Dictionary Lookup to Vector Search

RAG was independently invented and named around 2020 (Lewis et al., Facebook AI Research), but the core insight — put relevant knowledge in the prompt — is far older. The innovation was making "relevant" fuzzy rather than exact: instead of string-matching on keywords, you measure semantic similarity in a high-dimensional vector space, so that "Who is Avery?" can retrieve a document indexed under "Lancaster." Understanding RAG means understanding why exact-match retrieval is brittle, what a vector embedding is, and what happens at each stage of the retrieve-then-generate pipeline.

**Level 2 candidates:**
- **The brittleness of keyword-based retrieval** — what breaks when you try to match on substrings, and why this failure mode motivates everything that follows.
- **Vector embeddings and encoder models** — the distinction between auto-regressive LLMs (generate the next token) and encoder models (compress a sequence to a fixed-length vector), which is the conceptual foundation of semantic search.
- **Cosine similarity as a retrieval signal** — what it measures, why it works for semantic search, and when it fails (e.g. highly asymmetric documents).
- **Chunking strategy** — how you split source documents before embedding them, and why chunk size and overlap are among the highest-impact RAG hyperparameters.
- **Retrieval evaluation: precision and recall** — how you measure whether your retriever is finding the right documents, separately from measuring whether the LLM is answering correctly.
- **Knowledge base as a separate architectural concern** — why the knowledge base (embedding store + retrieval logic) is a first-class component rather than a prompt engineering detail.

---

#### L1-06 · Vector Databases and LangChain Integration

Once you have embeddings, you need somewhere to store and query them at scale. Vector databases (Chroma, Pinecone, Weaviate, FAISS) are specialised stores built for approximate nearest-neighbour search — returning the most semantically similar vectors to a query in milliseconds across millions of documents. LangChain emerged as an abstraction layer over this entire pipeline: document loaders, text splitters, embedding models, vector stores, and retrieval chains all wired together through a common interface. Understanding LangChain 1.0's API teaches you what the abstraction is hiding; understanding its limitations teaches you when to go without it.

**Level 2 candidates:**
- **Approximate nearest-neighbour (ANN) search** — why you don't do exact nearest-neighbour at scale, and what HNSW (the indexing algorithm most vector DBs use) trades off for speed.
- **LangChain's retrieval chain abstraction** — what the chain does, what it hides, and why building the same pipeline from scratch once is a useful learning exercise.
- **Embedding model choice** — why the embedding model is largely independent of the generation model, and what happens when you use a low-quality embedder with a high-quality generator.
- **Re-ranking after retrieval** — why retrieving the top-k by cosine similarity is not always sufficient, and what cross-encoder re-ranking adds.
- **RAG evaluation: answer faithfulness vs answer relevance** — the two different failure modes of a RAG system, and why a good retriever does not guarantee a good answer.

---

#### L1-07 · Model Selection Strategy and Benchmarks

Picking the right model for a task is arguably the most consequential decision in an LLM system — more impactful than prompt engineering, RAG tuning, or hyperparameter choices. The strategy involves two layers: first, filtering on basics (parameters, context window, cost, license, latency); then evaluating on benchmarks (GPQA, MMLU-Pro, AIME, LiveCodeBench, MUSA, HLE). Both layers have serious limitations: benchmarks suffer from training data contamination, overfitting to metrics, and inconsistent evaluation environments. The course's Connect Four leaderboard — where models play a simple board game — is a useful corrective: even models at apparent PhD-level benchmark performance struggle with spatial reasoning tasks a human child handles easily.

**Level 2 candidates:**
- **The Chinchilla scaling law** — the relationship between parameter count and training data required for optimal performance, why it's a useful heuristic, and why inference-time scaling (reasoning effort, RAG) has reduced its practical importance.
- **Reasoning vs chat vs hybrid models** — what each is trained to do, the speed/quality tradeoff, and why hybrid models don't always dominate.
- **Benchmark contamination and overfitting** — why published benchmark scores are upper bounds on real-world performance, and how to construct your own evaluation.
- **Latency vs throughput** — the difference between time-to-first-token (critical for streaming UIs) and tokens-per-second (critical for batch jobs), and which models are optimised for which.
- **Open-source licensing landscape** — why Llama's license requires a separate agreement for commercial use, what that means in practice, and how license choice constrains your deployment options.
- **Building your own leaderboard** — why the most trustworthy benchmark for your task is one you construct yourself, using your own inputs and a metric aligned with your business objective.

---

### Group 3 — Fine-Tuning: Frontier and Open-Source Models

Fine-tuning is the step beyond inference-time techniques. It modifies the model's weights to improve performance on a specific task — but it is expensive, slow, and often unnecessary. This group covers when fine-tuning is warranted, how to prepare data for it, and the techniques (QLoRA) that make fine-tuning an 8B+ open-source model feasible on a single GPU.

---

#### L1-08 · Data Curation and the Training Pipeline

Before any weight is updated, you need data. The capstone project — predicting product prices from Amazon descriptions — is a case study in data science as much as LLM engineering. The sequence: find a source (Hugging Face Datasets: `McAuley-Lab/Amazon-Reviews-2023`), load it, inspect it, filter it (price outliers, empty descriptions), build train/validation/test splits, and decide on the evaluation metric (mean absolute error in dollars, because it's both model-centric and business-interpretable). The insight the course returns to repeatedly: data curation had a larger impact on final model quality than any hyperparameter choice.

**Level 2 candidates:**
- **Train / validation / test split rationale** — why you need three pools, not two, and what goes wrong if you use validation data to make final model selection decisions.
- **LLM-assisted data preprocessing** — using a frontier model to rewrite raw product descriptions into a consistent prompt format before fine-tuning, which is itself a novel use of LLMs.
- **Synthetic data generation** — how to use an LLM to produce labelled training examples, the failure modes (LLMs are systematically positive/gushing unless corrected), and when synthetic data substitutes for real data.
- **Business-centric vs model-centric metrics** — why cross-entropy loss is useful during training but mean absolute dollar error is what you report to a stakeholder.
- **Baseline models in traditional ML** — why you should build a linear regression and an XGBoost model before touching an LLM, and what their performance tells you about the information content of the features.

---

#### L1-09 · Fine-Tuning a Frontier Model via API

OpenAI (and Anthropic) expose fine-tuning through an API: you upload a JSONL file of prompt-completion pairs, submit a training job, and receive a model ID pointing to your fine-tuned variant. This removes infrastructure complexity but introduces a different kind of constraint — you can't see the architecture, can't control the LoRA hyperparameters, and can't deploy the result outside the provider's infrastructure. The course treats this as a necessary disappointment: fine-tuning GPT-4o-mini on a price prediction task underperforms zero-shot prompting of GPT-4o, which is the right lesson about when fine-tuning a frontier model is and isn't warranted.

**Level 2 candidates:**
- **JSONL training format** — how prompt-completion pairs are structured, what the model actually sees during fine-tuning, and why format matters for generalisation.
- **When frontier fine-tuning loses to prompting** — the specific conditions under which a smaller fine-tuned model underperforms a larger prompted model, and what this tells you about the cost-performance tradeoff.
- **Transfer learning mechanics** — why fine-tuning works at all (the pre-trained model already "knows" most of what you need; you're updating a small fraction of its knowledge), and what breaks if the fine-tuning dataset is too small or too different from the pre-training distribution.
- **Overfitting to the fine-tuning set** — what it looks like when a model memorises training examples rather than generalising, and how early stopping and validation loss are used to detect it.

---

#### L1-10 · QLoRA: Quantisation + Low-Rank Adaptation

QLoRA (Dettmers et al., 2023) is the technique that made fine-tuning 7B–70B open-source models accessible on a single consumer GPU. It combines two independent tricks: LoRA (Low-Rank Adaptation), which trains small additional matrices that adapt the model's frozen layers rather than updating all 3B weights; and quantisation, which compresses the base model's weights from 32-bit floats to 4-bit integers, reducing memory from ~13GB to ~4GB. The practical consequence: you can fine-tune Llama 3.2 3B on a free Colab T4. The conceptual consequence: you learn to think of a model's parameters as not a monolith but as a frozen base plus learned adapter layers.

**Level 2 candidates:**
- **LoRA rank (r) and alpha hyperparameters** — what `r` controls (the dimensionality of the adapter matrices), why powers of two are conventional (and why the convention matters less than the folklore suggests), and what happens when you increase `r`.
- **Target module selection** — why attention layers (q_proj, v_proj) are the conventional first target for adaptation, and what adding MLP layers gains and costs.
- **4-bit NF4 quantisation** — why 4-bit is 16 discrete positions mapped to floating-point values (not integers), why the accuracy degradation is much smaller than expected, and the MP3 analogy for why lossy compression of neural weights works.
- **The bits-and-bytes library** — the specific Python package that implements bitsandbytes quantisation on CUDA, and why it needs to be installed fresh on each new Colab session.
- **LoRA A and B matrix dimensions** — the linear algebra reason there are two matrices rather than one (so that their product has the right shape to add to the frozen weight matrix), for those who want to ground the intuition in the actual maths.
- **Freezing vs training the base model** — the memory and compute savings that come from freezing all base weights and training only the adapter, and what you lose when you do this.

---

### Group 4 — Agentic AI and Production Deployment

Agents extend LLMs beyond single-turn question-answering into systems that take actions, call tools, and loop until a goal is achieved. Production deployment takes a fine-tuned model and makes it available as an API endpoint. This group covers the architectural patterns, the practical infrastructure (Modal for serverless deployment), and the capstone project that ties all previous groups together.

---

#### L1-11 · Agent Architectures and Tool-Calling

Agents — AI systems that call tools in a loop to achieve a goal — became a practical engineering pattern around 2023–2024, when LLM reliability improved enough to make multi-step tool use viable without constant human intervention. The course builds a seven-agent system for deal-hunting: a scanner agent subscribing to RSS feeds, an ensemble agent pricing products (using both the fine-tuned model and a RAG-backed frontier model), a messaging agent sending push notifications, and a planning agent orchestrating the others. The key lesson is architectural restraint: don't decompose into agents because it sounds like a good design pattern; decompose because it demonstrably solves the business problem more effectively than a single LLM call.

**Level 2 candidates:**
- **Three definitions of "agent"** — the Sam Altman definition (delegates work autonomously), the Anthropic definition (LLM controls the workflow), and the emerging definition (LLM + tools in a loop) — and why the distinctions matter for architecture decisions.
- **Agentic workflow vs true agentic AI** — Anthropic's distinction between orchestrated multi-LLM-call pipelines (where Python controls the order) and systems where the LLM decides what to do next.
- **Tool-calling / function-calling mechanics** — how the model signals that it wants to run a tool (by generating a structured JSON block), how your Python code executes the tool, and how the result re-enters the context.
- **Memory and deduplication in agent loops** — why a planning agent needs to remember which deals it has already surfaced, and the simplest viable implementation of that state.
- **When to use vs avoid agent frameworks** — what Crew.ai, OpenAI Agents SDK, and LangGraph provide, why Anthropic's "Building Effective Agents" recommends building from first principles first, and what you lose by abstracting too early.
- **Multi-agent observability** — why logging and tracing become non-negotiable as soon as you have more than two agents in a loop, and what the minimum viable observability looks like.

---

#### L1-12 · Serverless Deployment with Modal

A fine-tuned model that lives only in Colab has no production value. Modal is a serverless AI infrastructure platform that lets you deploy Python functions — including inference code — to cloud GPUs with one decorator and pay only for actual runtime. The architectural insight: Modal decouples the *definition* of infrastructure (which image, which GPU, which secrets) from its *execution*, so the same Python function runs locally for debugging and on an A10G in production without a code change. This is a narrow but deep lesson in what "production" actually means for an LLM system.

**Level 2 candidates:**
- **Serverless vs persistent GPU instances** — why paying only for inference time (Modal's model) beats reserving a persistent GPU instance for most LLM workloads, and when it doesn't.
- **Modal's decorator pattern** — how `@app.function(image=..., gpu=..., secrets=...)` describes infrastructure as code, and how `.remote()` vs `.local()` switches execution context without changing the function body.
- **Hugging Face secret management in Modal** — the specific pattern for passing HF tokens to cloud-hosted inference functions via Modal Secrets, and what breaks if the key names don't match.
- **Cold start latency** — the tradeoff Modal surfaces between keeping a container warm (cost) and accepting startup latency (UX), and how to reason about it for a deal-scanning use case.
- **Region selection for compliance** — why GDPR and data residency requirements can constrain which Modal regions you're allowed to use, and how to enforce region selection in code.

---

## Sequencing Note

The logical dependency chain runs in one direction: **APIs → open-source models → RAG → fine-tuning → agents**. Each station assumes fluency at the previous one. Attempting RAG before you understand context windows produces brittle systems you can't debug. Attempting QLoRA before you understand the Hugging Face Transformers library produces opaque training failures. Attempting agents before you understand tool-calling mechanics produces systems that are genuinely hard to reason about.

The highest-leverage entry points for someone returning to foundations are **L1-05 (RAG architecture)** and **L1-10 (QLoRA)**. These are the topics where professional LLM engineers most commonly have gap knowledge — they understand the output but not the mechanism. L1-07 (model selection and benchmarks) is the other high-value stop: the ability to make and defend model selection decisions is a recurring professional need that most practitioners underinvest in.

If you're pressed for time: L1-01 through L1-04 can be skimmed if you already code comfortably against LLM APIs. L1-08 (data curation) can be approached at the intuition level rather than the implementation level without blocking later topics. L1-09 (frontier fine-tuning) is worth understanding primarily as a negative lesson — knowing when *not* to do something is as valuable as knowing how.

## Source

https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/