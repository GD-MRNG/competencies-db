## Metadata
- **Date:** 05-06-2026
- **Source:** 14_the_system_architecture_wiring_it_all_together.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-14 · The System Architecture: Wiring It All Together

The moment you stop thinking of "the AI" as a thing and start thinking of it as a place where logic could live, you've crossed into system architecture. Up to this point, every topic in the track has handed you a tool: a model call, a prompt, a tool definition, a retriever, a fine-tuning loop, a schema. Each one solves a real problem. But a production system is not a collection of tools — it's a set of decisions about where each piece of behavior should be encoded, and why. Get those decisions wrong and no amount of prompt tweaking will save you.

The mental model worth holding is this: in an AI system, logic can live in four different places, and each place has wildly different properties. It can live in the model itself, shaped by the prompt — fast to change, cheap to iterate, but fuzzy and non-deterministic. It can live in your application code as ordinary rules and conditionals — perfectly reliable, but rigid and blind to nuance. It can live in the model's weights via fine-tuning — durable and consistent, but expensive to update and risky to validate. Or it can live in the inference-time context via retrieval — fresh, swappable, and auditable, but paid for in tokens on every single request. Choosing where a given piece of behavior belongs is the central act of AI architecture.

The trap most people fall into is putting everything in the prompt. It's the path of least resistance: when something goes wrong, you just add another sentence to the system message. This works until the prompt is three pages long, the model starts ignoring half of it, and you can't tell which instruction is doing what. The opposite trap is putting everything in code: writing elaborate rule engines that try to anticipate every edge case, defeating the entire point of using a model in the first place. The skill is knowing which kind of problem each layer is built to solve, and resisting the urge to use one layer for everything.

A rough decision tree helps. If the knowledge changes daily — prices, inventory, news, the contents of your database — it belongs in retrieval. You don't want it baked into weights or hardcoded in prompts, because by tomorrow it's wrong. If it's a behavioral pattern unique to your domain — your company's tone, a specialized output format, a niche reasoning style the base model handles poorly — that's a fine-tuning candidate, because you're shaping how the model behaves rather than what it knows. If it's a well-defined deterministic rule — "transactions over $10,000 require manager approval," "never email customers between 10pm and 7am" — hard-code it. Letting the model decide whether to follow a hard rule is how you ship a system that occasionally doesn't. And if it's a behavior that's genuinely fuzzy and needs to be tuned often, the prompt is the right home.

Real systems are almost never single-model affairs. A mature architecture often looks like an ensemble: a cheap, fast model triages incoming requests and decides what kind of work is needed; a more capable model handles complex reasoning when the triage flags it; a fine-tuned specialist handles a narrow domain task it's been trained for; structured outputs enforce a schema at the boundary where the AI hands off to ordinary code; hardcoded rules guard the actions that must never be wrong. The model isn't the system. The model is one component in a system that you, the architect, are responsible for shaping.

Every architectural choice plays out on the same underlying surface: cost, accuracy, and latency, which are almost always in tension. A frontier model gives you accuracy but costs more and runs slower. A local quantized model is cheap and private but less capable. RAG adds accuracy on fresh knowledge but adds tokens and a retrieval hop. Fine-tuning amortizes capability into the weights but front-loads enormous cost. Structured outputs give you reliability but constrain the model and add latency. There is no configuration that wins on all three axes. The job is to find the operating point that's acceptable for your use case, then iterate on it as your usage patterns reveal where the real bottlenecks are.

The other thing a real architecture has to plan for is failure, because every component will fail. The model will hallucinate. The vector database will go down. The API will time out at the 99th percentile right when your most important customer is using it. Graceful degradation — falling back to a cached response, a smaller model, a sensible default, or a clear error — is not a polish item you add at the end. It's part of the design from the start, because the failure modes of an AI system are stranger and more frequent than those of conventional software, and a system that crashes on the first hallucinated tool call isn't a production system at all.

What this topic ultimately builds is a habit of mind. When you face a new requirement, you stop asking "what should I tell the model to do?" and start asking "where in the system does this belong?" That question, asked consistently, is what separates someone who can demo an impressive prototype from someone who can ship something that survives contact with real users, real data, and real money.

## Level 2 candidates

**Ensemble Approaches** — How to combine multiple models (a cheap planner directing more expensive workers, or a triage model routing to specialists) rather than asking one model to do everything. Worth a deeper dive because the patterns for orchestrating multi-model pipelines — cost routing, confidence-based escalation, planner/worker splits — are non-obvious and have outsized leverage on both cost and quality.

**RAG vs. Fine-Tuning vs. Hard-Coded Logic** — A detailed decision framework for where any given piece of behavior should live, with worked examples of each pattern and the failure modes when you pick wrong. Worth deepening because the "obvious" choice is often wrong, and the cost of relocating logic later (re-training, re-indexing, rewriting) is high enough that getting this right at design time pays back many times over.

**Cost-Accuracy-Latency Surface** — How to actually measure and visualize the trade-off space for a specific use case, and how to find your operating point rather than guessing at it. Worth its own treatment because the abstract idea is easy but the concrete practice — instrumenting requests, building comparison harnesses, deciding what "good enough" means — is where most teams stall.

**Error Handling and Graceful Degradation** — Concrete patterns for designing fallbacks: cached responses, smaller-model retries, circuit breakers around flaky providers, structured error surfaces when the model produces garbage. Worth deeper exploration because AI failure modes (hallucination, schema violations, tool-call loops) don't map cleanly onto conventional error handling, and the patterns are still being codified.

---