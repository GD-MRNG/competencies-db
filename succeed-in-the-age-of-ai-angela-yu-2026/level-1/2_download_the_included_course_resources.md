## Metadata
- **Date:** 19-05-2026
- **Source:** 2_download_the_included_course_resources.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Working with LLMs: Why Context and Constraint Beat Model Choice

Most people using AI today are doing the equivalent of buying a sports car and driving it in first gear. They have access to the most capable language models ever built and are getting back generic, hedged, mediocre output — and then concluding that AI is overhyped. The problem is almost never the model. The problem is that they are treating the interaction as a search query when it is closer to a briefing.

The single most useful idea to internalise is this: an LLM's output quality is a function of the context and constraint you give it, not the model you picked. Switching from a cheap model to an expensive one usually produces a smaller improvement than rewriting your prompt with a clear persona, a defined output format, and a few well-chosen examples. The model is the engine. Your prompt is the steering, the brakes, the destination, and the route. If you are getting vague answers, you are giving vague instructions, and no amount of model upgrade will fix that.

This reframes what the skill actually is. You are not learning to "use ChatGPT." You are learning to specify work the way a good manager specifies work to a capable but literal-minded contractor — one who has read most of the public internet, has no memory of your previous conversation unless you remind it, and will confidently invent things when it does not know the answer. The five levers you have over its output are persona (who it should act as), context (what it needs to know about your situation), task (what specifically you want), format (how the answer should be structured), and examples (what good output looks like). A vague prompt uses none of these. A strong prompt uses four or five.

Once you accept that prompting is structured work, three failure modes become predictable rather than mysterious. The first is sycophancy: models are trained, through reinforcement learning from human feedback, to be agreeable and encouraging. This sounds harmless until you realise it means the model will validate your bad ideas, agree with incorrect premises, and praise mediocre work. You cannot fully prompt this away — the model's training overrides your instructions — but you can route around it by asking for two proposals and having the model compare them, or by asking it to critique a plan it just generated. The model is not sycophantic about its own ideas, only about yours. The second failure mode is context bloat: every conversation has a finite window of tokens the model can attend to, and as that window fills with back-and-forth, earlier instructions degrade. Long sessions silently lose track of what you set up at the start. The fix is not to fight it but to start fresh sessions when output quality drops, carrying forward only the essentials. The third is hallucination on obscure ground: models are most reliable in well-trodden territory and least reliable on niche frameworks, recent libraries, or specialised internal jargon. Choosing common technologies is not a lack of imagination; it is a hedge against the tool's actual limits.

The structural techniques worth knowing follow directly from these limits. Few-shot prompting — giving the model two or three examples of the input-output pattern you want — works because language models are pattern matchers, and a good example is denser instruction than a paragraph of description. Delimiters (triple quotes, XML tags, markdown fences) work because they let the model cleanly separate "here is my instruction" from "here is the data to operate on," which prevents it from getting confused or, in adversarial contexts, prompt-injected. Chained prompting — breaking a complex request into a sequence of smaller, verifiable steps — works because the model's accuracy on a long, multi-stage task is roughly the product of its accuracy on each stage, so decomposition multiplies reliability. None of these are tricks. They are direct responses to how the system actually behaves.

There is also a model-selection layer that most people skip. Reasoning models (the slower, more expensive ones marketed as "thinking" variants) are genuinely better at planning, architecture, and critique. Faster models are better at execution and bulk transformation. The mature workflow is to use a reasoning model to refine your prompt or design your approach, then hand the actual work to a cheaper, faster model — and then, for high-stakes output, hand the result to a third model for review. This "alloying" works because different model families have different blind spots, and you are essentially red-teaming your own work for free.

The deepest shift, especially for anyone using AI to write code, is from author to orchestrator. When you let the model generate work and then review it, your job is no longer to produce — it is to specify, evaluate, and correct. This is why prompting well is harder than it looks: it requires the same skill as writing a good ticket, the same skill as breaking a project into milestones, the same skill as briefing a junior colleague. The people who are getting dramatic results from AI are not the ones with the best prompts memorised. They are the ones who can hold a clear picture of what they want, decompose it into pieces small enough to verify, and resist the temptation to accept output just because it looks confident. The tool rewards thinking. It punishes laziness with plausible-sounding garbage. That asymmetry is the whole game.

## Level 2 candidates

**The anatomy of a strong prompt** — A deeper treatment of the persona–context–task–format–examples structure, with worked examples showing the same request prompted at increasing levels of specificity and the corresponding lift in output quality. Worth a Level 2 because it converts a general principle into a repeatable template the reader can use immediately.

**Chained prompting and decomposition** — How to break a non-trivial goal into a sequence of dependent prompts, where to insert verification steps, and how to recognise when a single prompt is being asked to do too much. Worth deeper treatment because decomposition is the highest-leverage skill in prompting and the hardest to learn from a single example.

**Context window management** — A practical guide to context bloat: how to recognise the symptoms, when to start a fresh session, how to carry state forward, and where techniques like file references, RAG, and project-level system prompts fit in. Deserves its own treatment because it governs everything about working with AI on tasks longer than a single exchange.

**Mitigating sycophancy and hallucination** — Techniques for getting honest critique out of a model trained to please, including dual-proposal prompting, self-critique loops, and cross-model review. Worth going deeper because the default behaviour of LLMs actively works against quality, and most users never notice.

**Vibe-coding as a discipline** — The specific practices that separate productive AI-assisted coding from a mess of half-working files: small scoped prompts, mandatory Git use, reviewing the AI's plan before it writes code, and the three-strikes rule on debugging. Deserves a full Level 2 because coding with AI has its own failure modes that don't show up in general prompting.

**Choosing the right model for the job** — The strategic split between reasoning models (planning, architecture, critique) and execution models (bulk work, transformation), plus the case for cross-model review. Worth depth because most users default to one model for everything and leave significant quality on the table.

---

# Discussion

## Why This Conversation Is Happening

A lot of disappointment with LLMs comes from a category error. People think they are querying a smart search engine, so they type short, underspecified requests and then blame the model when the answer is bland or wrong. But an LLM is much closer to a capable contractor with poor judgment, no lasting memory, and a strong tendency to sound confident. If you brief it badly, it will still produce something polished enough to tempt you into accepting it.

That creates a real engineering problem: output quality becomes less about which model you bought and more about whether you can specify work precisely. Teams that do not understand this waste money upgrading models when the real fix is better context, tighter constraints, and clearer decomposition. They also get burned by predictable failure modes like sycophancy, context drift, and hallucination in niche domains.

This topic matters because working effectively with LLMs is not mainly about clever phrasing. It is about learning to structure tasks so the model has a chance of succeeding and so you have a chance of verifying it. Without that mental model, AI-assisted work feels random. With it, the behavior becomes much more legible and much more controllable.

## What You Need To Know First

**1. Context window**  
An LLM can only pay attention to a limited amount of text at once. That bounded working space is its context window. If a conversation gets long, earlier instructions may become less influential or drop out entirely. You do not need the token math here; you just need the practical implication: long chats silently degrade.

**2. Hallucination**  
A hallucination is when the model produces false information as if it were true. This is not always wild nonsense; often it looks plausible, which is why it is dangerous. Hallucinations are more likely when the model is pushed into niche, obscure, internal, or very recent territory where it has weaker grounding.

**3. Few-shot prompting**  
This just means giving the model a few examples of the kind of input-output pattern you want. Instead of only describing the task, you show it. LLMs are excellent pattern imitators, so examples often teach the target shape faster than abstract instructions do.

**4. Decomposition**  
Decomposition means breaking a larger task into smaller steps that can be checked one by one. This matters because asking a model to do five hard things in one prompt hides where it failed. Smaller steps make both the model and the human reviewer more reliable.

## The Key Ideas, Connected

**1. Better output usually comes more from better briefing than from better model choice.**  
The article’s starting claim is that most mediocre LLM output is caused by weak prompts, not weak models. If you ask vaguely, you get generic output, because the model has too much freedom to guess what you mean. Upgrading the model may help a bit, but it often helps less than giving clearer instructions. That leads to the next idea: if prompt quality matters this much, then prompting is not a side issue but the real skill.

**2. Prompting is really the skill of specifying work clearly.**  
The article reframes prompting as a management task. You are not “chatting with AI” so much as briefing a capable but literal worker. That means you need to define role, relevant situation, exact task, desired structure, and examples of good output. The five levers named in the article — persona, context, task, format, and examples — are just the main parts of a good brief. Once you see prompting this way, the common failures stop looking mysterious and start looking like consequences of incomplete specification.

**3. The model has predictable behavioral weaknesses, so prompt design must work around them.**  
The article calls out three such weaknesses: sycophancy, context bloat, and hallucination on obscure ground. Sycophancy means the model tends to validate your framing too readily. Context bloat means long conversations slowly lose fidelity as earlier setup becomes diluted. Hallucination on obscure ground means the model sounds most trustworthy where it may be least reliable. These are important because they show why “just ask better” is not enough; the system itself has tendencies you must design around. That naturally leads to techniques that constrain the interaction more tightly.

**4. The useful prompting techniques are not hacks; they are direct responses to the model’s limits.**  
Few-shot prompting works because examples compress instruction into patterns the model can imitate. Delimiters work because they separate instructions from source material cleanly, reducing confusion about what is command versus content. Chained prompting works because smaller steps are easier for the model to execute and easier for you to verify. The key connective idea here is that good prompting techniques are really reliability techniques. They reduce ambiguity and create checkpoints. Once you think in those terms, a new question appears: should every task go to the same kind of model?

**5. Different model types are better at different phases of work.**  
The article distinguishes between reasoning-heavy models and faster execution-oriented models. The slower models are better when the task is planning, critique, architecture, or refinement. The faster models are better when the task is transformation, drafting, or bulk execution. This matters because it breaks the simplistic habit of choosing one model and using it for everything. And once you allow different models to play different roles, you can treat model choice as workflow design rather than brand loyalty.

**6. A mature workflow uses multiple models and stages rather than one model in one shot.**  
The “alloying” idea follows from the previous point. One model can help define the approach, another can do the bulk of the work, and a third can review or challenge the result. This is less about fancy tooling than about acknowledging that model outputs should be checked from different angles. It also mirrors good engineering practice more generally: separate planning, execution, and review. That leads to the article’s deepest shift in responsibility.

**7. Working well with LLMs turns you from author into orchestrator.**  
If the model is generating pieces of the work, then your value moves upward: you define the problem, choose the structure, sequence the steps, inspect the output, and correct the course. In other words, you are not mainly writing every line yourself; you are managing a production system. That is why prompting well feels similar to writing a good ticket or briefing a junior engineer. This closes the chain: context and constraint matter so much because the real skill is orchestration, and orchestration depends on being able to specify and verify work clearly.

## Handles and Anchors

**1. An LLM is closer to a contractor than a search engine.**  
A search engine retrieves. A contractor interprets. With a contractor, vague instructions produce misaligned work, not because the contractor is useless but because the brief was incomplete. That is the right default mental model here.

**2. The model is the engine; the prompt is the control system.**  
A stronger engine helps, but not as much as steering, braking, and route choice. This is a compact way to remember why context and constraint often matter more than model selection.

**3. Break the work until you can verify it.**  
This is the practical anchor for chained prompting and orchestration. If a step is too big to check quickly, it is too big to delegate cleanly to the model.

## What This Changes When You Build

**An engineer who understands this will write prompts more like design briefs or tickets because the model performs best when the work is specified rather than merely requested.**  
That means stating the role, giving the relevant project context, naming the exact task, constraining the output format, and often including one or two examples instead of asking a loose one-line question.

**An engineer who understands this will reset conversations aggressively when quality drops because long context is not free; it degrades instruction fidelity.**  
Instead of endlessly continuing one chat, they will start fresh threads and carry forward only the essential state, which keeps the model anchored on the current task rather than the residue of every previous exchange.

**An engineer who understands this will decompose larger tasks into staged prompts because reliability is easier to achieve and inspect step by step than in a single monolithic request.**  
For example, they may first ask for a plan, then review and revise the plan, then generate code for one module, then request tests, then request a critique of edge cases.

**An engineer who understands this will choose model roles intentionally because planning, execution, and review are different kinds of work.**  
They might use a stronger reasoning model to shape an approach, a cheaper fast model to produce repetitive transformations, and another pass or model to challenge the result before accepting it.

**An engineer who understands this will build defenses against agreement and confident error because the default model behavior is optimized for plausibility, not truth.**  
So they will ask for competing proposals, request explicit critique, compare alternatives, use delimiters to separate instructions from data, and treat niche or recent claims as needing external verification rather than taking the answer at face value.