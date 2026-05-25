## Metadata
- **Date:** 26-05-2026
- **Source:** 12_generative_model_applications_rag_fine_tuning_and_agents.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-12 · Generative Model Applications: RAG, Fine-tuning, and Agents

The mistake people make with generative models is treating them as a single hammer. You have an LLM, you point it at a problem, and when the answer is wrong or stale or hallucinated, you blame the model. The model is not the problem. The problem is that you reached for the wrong pattern. Generative models are not one tool; they are a small family of tools, and the value you extract depends almost entirely on matching the pattern to the failure mode you are trying to avoid.

There are three patterns worth knowing in 2026, and they map cleanly onto three different deficits an off-the-shelf LLM has. An LLM does not know your data — it knows the public internet circa its training cutoff. An LLM does not speak your domain's idiom — it speaks generic English, generic code, generic reasoning. An LLM does not act — it produces text, one token at a time, with no native ability to query a database, call an API, or check its own work. Retrieval-augmented generation, fine-tuning, and agents each address exactly one of these deficits. If you can name which deficit is hurting you, you know which pattern to reach for.

Retrieval-augmented generation, or RAG, is what you use when the model needs to answer questions about facts it was never trained on, or facts that change. The shape is straightforward: when a query comes in, you first retrieve relevant documents from your own data store, then stuff those documents into the prompt as context, then ask the model to answer using that context. The model becomes a reading-comprehension engine over your data rather than a recall engine over its training set. RAG is the right answer when you care about factuality, when your data updates frequently, and when you can describe what "relevant" means well enough to retrieve it. It is the wrong answer when the model needs to learn a new way of reasoning, not just new facts.

Fine-tuning is what you use when the model needs to internalize something — a tone, a format, a domain's specific patterns of inference. You take a pre-trained model and continue training it on examples of the behavior you want. Where RAG injects knowledge at query time, fine-tuning bakes it into the weights. The trade-off is real: fine-tuning is more expensive up front, your data has to be good and labeled, and the model's knowledge becomes frozen at training time again (so you are back to staleness if your domain shifts). Fine-tuning shines when you have stable patterns the model needs to learn deeply — medical reasoning, legal drafting style, your company's specific way of structuring outputs — and when prompt-level instructions keep failing to elicit the behavior consistently.

Agents are what you reach for when the task itself requires more than one step of generation. An agent is a system in which the LLM is given a set of tools (a calculator, a web search, a database query, an API), and at each step it decides what to do next: call a tool, observe the result, reason about what it learned, and either call another tool or produce a final answer. The most common pattern is ReAct — reason, act, observe, iterate. Agents extend the model's reach beyond text generation into the actual world of systems and side effects. They are also the most fragile of the three patterns: every additional step is another chance to go off the rails, and debugging a multi-step agent loop is genuinely hard. Use agents when the task cannot be decomposed into a single prompt, not because they sound impressive.

These patterns compose. A production system answering customer questions about your product will likely use RAG to ground answers in your documentation, function calling so the model can look up order status in your database, and possibly a fine-tuned model so the responses match your brand's voice. The boundary between agents and RAG blurs once you let the model decide whether and how to retrieve. Long-context windows complicate the picture further: when a model can hold a million tokens, you can sometimes skip retrieval entirely and just stuff everything in. That is simpler and often worse — more expensive per query, and the model attends less carefully to information buried in a long context than to information retrieved and placed front-and-center.

The hardest part of working with generative models is not building these systems. It is evaluating them. A classifier has accuracy. A regression has RMSE. A generative system produces open-ended text, and asking "is this output good?" rarely has a clean answer. Automatic metrics like BLEU and ROUGE measure surface overlap with reference answers, which is not the same as quality. Human evaluation is expensive and subjective. LLM-as-judge (using a stronger model to grade a weaker one's outputs) is now standard but inherits the judge's biases. You will spend more time than you expect deciding what "working" means for your system, and that decision matters more than the choice of model.

The skill this topic builds is pattern recognition. Given a problem — a chatbot for your docs, an extraction pipeline, a research assistant, a code generator — you should be able to look at it and say: this needs RAG, this needs fine-tuning, this needs an agent loop, this needs all three. Then you can reason about cost, latency, failure modes, and evaluation before you write a line of code. The teams who ship generative AI in 2026 are not the ones with the best models. They are the ones who picked the right pattern.

## Level 2 candidates

**Retrieval-Augmented Generation (RAG) end-to-end** — Covers the full pipeline of indexing documents, embedding queries, retrieving top-k, and constructing the final prompt. Worth a deeper dive because each stage has its own failure modes and design decisions that determine whether the system actually grounds answers or just produces confident nonsense with citations attached.

**Embedding models, vector databases, and reranking** — Covers how documents become vectors, how vector databases index and search them at scale, and how rerankers refine the top-k before the LLM sees it. Worth going deeper because retrieval quality is the single biggest determinant of RAG quality, and most "the LLM is hallucinating" complaints are actually retrieval problems.

**Fine-tuning vs. RAG decision framework** — Covers the explicit trade-offs (cost, freshness, data requirements, control over reasoning) and how to decide which to use, or when to combine them. Worth deeper treatment because this is the most common architectural mistake teams make, and the wrong choice is expensive to undo.

**Agents and the ReAct pattern** — Covers how to structure an LLM as a reasoning loop with tools, including prompt design for tool selection, error handling, and step limits. Worth a deep dive because agents are where most generative AI projects in 2026 fail spectacularly, and the failure modes are non-obvious until you have shipped one.

**Function calling and tool use** — Covers how modern LLMs are trained to emit structured tool calls, how to design tool schemas, and how to route the model's decisions to real systems. Worth its own treatment because function calling is the connective tissue between LLMs and the rest of your stack, and the schema design dramatically affects reliability.

**Long-context windows vs. retrieval** — Covers when to stuff context vs. retrieve selectively, how attention degrades over long contexts (the "lost in the middle" problem), and the cost-quality trade-off. Worth deeper exploration because this trade-off is shifting fast as context windows grow, and the conventional wisdom from 2023 is already wrong.

**Evaluation of generative outputs** — Covers automatic metrics, human evaluation, LLM-as-judge, and task-specific evaluation harnesses. Worth a dedicated deep dive because evaluation is harder than building, most teams underinvest in it, and a good eval harness is what separates a demo from a production system.

---

## Original Content

#### L1-12 · Generative Model Applications: RAG, Fine-tuning, and Agents

Generative models (LLMs, image generators) are tools. The art is knowing which tool to reach for. Do you need to retrieve facts from your data? Use RAG. Do you need the model to learn your domain's language? Fine-tune. Do you need the model to accomplish multi-step tasks? Use agents (systems that plan, act, observe, and iterate). In 2026, these patterns are standard.