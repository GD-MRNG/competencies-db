## Metadata
- **Date:** 26-05-2026
- **Source:** 06_large_language_models_llms_and_prompting.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-06 · Large Language Models (LLMs) and Prompting

The instinct of every engineer encountering an LLM for the first time is to treat it like a library: read the docs, learn the API, call the function, get the result. This instinct is wrong, and it is the source of most of the bad LLM-powered software in the world. An LLM is not a function with a stable contract. It is a probabilistic system that produces different outputs for inputs that look, to a human, identical. The skill you are building is not "how do I call GPT-4." It is how to specify a task precisely enough that a stochastic text generator reliably does what you want.

Start with what an LLM actually is, because the mental model determines everything else. GPT-4, Claude, LLaMA, and Gemini are Transformers (L1-04) trained to predict the next token, scaled up to trillions of tokens of training data and hundreds of billions of parameters. Nothing about that training objective explicitly teaches reasoning, translation, or code generation. These capabilities emerge from scale. Which means: an LLM is fundamentally a pattern completer that has seen so many patterns it can complete most things you throw at it — but it is still a pattern completer. It does not "know" facts. It does not "understand" your task. It produces text that looks like the text that would follow your input, given everything it has seen.

This framing makes the implications clear. The LLM is not retrained for your task. It is not fine-tuned. It has not seen your data. Everything it does for you, it does in a single forward pass over the text you provide. The text you provide — the prompt — is therefore the entire interface. There is no other lever. If the model produces the wrong output, your only options are to change the prompt, change the model, or wrap the model in a system that compensates (RAG, validation, retries). This is why prompting is an engineering discipline rather than a parlor trick: the prompt is the program.

Once you accept this, the techniques start to make sense as a coherent discipline rather than a grab-bag of folk wisdom. Be specific about format, because "summarize this" produces a different distribution of outputs than "produce a three-sentence summary, no bullet points, written for a technical audience." Provide examples, because few-shot prompting — putting a handful of input-output pairs in the prompt — lets the model infer the pattern you want without any retraining. This is in-context learning, and it is one of the genuinely surprising properties of large models: they can pick up a new task from three or four examples, in a way that a fine-tuned smaller model cannot. Ask for reasoning before the answer, because chain-of-thought prompting ("think step by step") consistently produces better results on tasks that require multiple inference steps. The model is not actually thinking, but generating intermediate reasoning tokens gives the final answer more correct context to condition on.

The other half of the discipline is what you do around the prompt, because a single prompt is rarely enough for production work. You will need structured outputs (asking the model to return JSON, then handling the cases where it does not) so downstream code can consume the result. You will need retrieval-augmented generation when the model needs facts it does not have, which is most of the time, because LLMs hallucinate confidently when asked about things outside their training data. You will need to choose between a large model (slow, expensive, accurate) and a smaller one (fast, cheap, less capable), and often you will route between them — small model for the easy cases, large model for the hard ones. None of this is glamorous. All of it is where production LLM systems live or die.

The failure mode you have to internalize is hallucination. An LLM does not know what it does not know. It will produce a confident, fluent, completely fabricated answer with the same conviction as a correct one. There is no built-in uncertainty signal. This is not a bug to be patched in the next model release; it is a property of the architecture. Mitigations exist — RAG grounds the model in real documents, self-critique prompts ask the model to check its own work, verification steps validate outputs against ground truth — but no mitigation is complete. If your application cannot tolerate occasional confident fabrication, you need a system around the LLM, not just a prompt.

The shift this topic represents is from "build a model" to "specify a behavior." In the 2024 curriculum, building an NLP system meant collecting data, choosing an architecture, training, evaluating, iterating on the model. In 2026, for most language tasks, you start with an LLM and iterate on the prompt. The model is fixed; your job is specification. This is faster (no training loop), cheaper for moderate scale (no GPUs), and more capable (you get reasoning and few-shot learning for free). It is also less controllable, harder to debug, and more expensive at high scale. Knowing when to reach for an LLM versus when to fine-tune a smaller model (L1-07) versus when to build a classical system is the judgment this topic builds.

The skill, in the end, is treating natural language as a programming interface. Prompts are programs: they have specifications, edge cases, regressions, and tests. A good prompt engineer iterates on prompts the way a good developer iterates on code — running them against examples, measuring outputs, isolating failure cases, refactoring for clarity. The mystique around prompting comes from people who treat it as magic incantation. It is not. It is specification and iteration, with a stochastic compiler.

## Level 2 candidates

**Prompt engineering: clarity, examples, constraints** — How to write prompts that produce reliable outputs by being specific about format, providing examples, and setting explicit constraints. Worth depth because the difference between a prompt that works 60% of the time and one that works 95% is almost entirely in the techniques here, and they are non-obvious until you have seen them work.

**Few-shot prompting and in-context learning** — How LLMs learn new tasks from a handful of examples in the prompt, without any retraining. Worth depth because in-context learning is genuinely surprising as a phenomenon, and the practical questions (how many examples, how to choose them, how to order them) have real answers backed by research.

**Chain-of-thought prompting** — Why asking an LLM to reason step by step before producing a final answer measurably improves performance on complex tasks. Worth depth because the variants (zero-shot CoT, self-consistency, tree-of-thought) have different cost-accuracy tradeoffs that matter in production.

**Structured outputs and parsing** — How to prompt an LLM to return JSON or other parseable formats, and how to handle the inevitable parsing failures. Worth depth because most production LLM systems consume outputs programmatically, and the gap between "usually returns valid JSON" and "always returns valid JSON" is where bugs hide.

**Hallucinations and factuality** — How LLMs produce confident false information, why it is architectural rather than a bug, and what techniques (RAG, self-critique, verification) actually mitigate it. Worth depth because every serious LLM application has to take a position on hallucination, and the mitigations have non-obvious tradeoffs.

**Cost and latency optimization** — When to use a large expensive model versus a small cheap one, when to cache, when to distill, when to route between models. Worth depth because production economics often dominate model choice, and the optimization techniques (caching, batching, model cascades) are unfamiliar to people coming from a research mindset.

**Prompt templates and versioning** — How to manage prompts as code: parameterizing them, version-controlling them, testing them against regression suites. Worth depth because prompts drift, models change, and teams that treat prompts as ephemeral strings end up with the LLM equivalent of unmaintained shell scripts in production.

---

## Original Content

#### L1-06 · Large Language Models (LLMs) and Prompting

Large language models (GPT-4, Claude, LLaMA, Gemini) are Transformers trained on trillions of tokens. They can do things no amount of fine-tuning would teach them: reasoning, few-shot learning, translation, code generation. In 2026, you do not need to understand how GPT-4 works internally—you need to understand how to use it. Prompting is an engineering discipline: how to phrase a question so an LLM answers correctly, how to structure few-shot examples, how to chain LLMs together for complex tasks. This is not magic. It is specification and iteration.