## Metadata
- **Date:** 22-05-2026
- **Source:** \section_2\combined_intermediate_summaries.md
- **Model:** Claude-Opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Architecting AI: Inference-Time vs Training-Time

The most expensive mistake leaders make with AI is reaching for fine-tuning when they actually have a retrieval problem. It looks like the sophisticated choice — you are teaching the model your business, after all — but in nine cases out of ten the model didn't need teaching. It needed the right context at the right moment. Understanding why is the difference between architecting AI as a competitive advantage and burning a quarter's R&D budget on a black box that disappoints.

Every commercial AI decision sits somewhere on a single spectrum: how you combine a model's general reasoning with your organisation's specific knowledge and behaviour. There are only two real levers. You can change what the model sees at the moment of the request, or you can change the model itself. Everything else — RAG, prompting, agents, fine-tuning, training from scratch — is a variation on one of those two moves. The leader's job is to know which lever is appropriate, what each one costs, and what risks each one buys you.

Inference-time optimisation means leaving the model alone and getting smarter about the context you hand it. Multi-shot prompting, chain-of-thought, and most importantly retrieval-augmented generation all live here. RAG is conceptually trivial: when a user asks a question, your code looks up relevant material in your own data, stuffs it into the prompt alongside the question, and lets the model answer with that context in front of it. The model doesn't "know" your business; it just gets handed the right page from the manual every time. The mechanism that makes this scale — turning text into vectors so you can do fuzzy meaning-based lookups rather than brittle keyword searches — is the engineering substance behind RAG, but the strategic substance is simpler: your knowledge stays in your database, where it is auditable, updatable, and easy to govern.

Training-time optimisation means modifying the model's weights with your data. Fine-tuning takes a pre-trained base — usually an open-source model like Llama, occasionally a frontier model via API — and continues training it on your examples. Done well, a fine-tuned 8B parameter model can outperform GPT-4 on a narrow task, which is genuinely remarkable and genuinely seductive. Done badly, you spend months on GPU clusters discovering that your data wasn't good enough, your model has forgotten things it used to know (the failure mode is called catastrophic forgetting), and you cannot explain why it produces any particular answer. This is real R&D: high risk, uncertain outcomes, and a long path to production.

The tradeoffs fall out cleanly once you see the spectrum. RAG handles changing facts; fine-tuning handles fixed style. RAG is explainable because you can show the source document; fine-tuning is opaque because the knowledge is dissolved into the weights. RAG ships in a weekend; fine-tuning is a research project. The decision question is almost always: are you teaching the model facts, or teaching it a way of thinking? Facts go in the prompt. Reasoning patterns and tone go in the weights. A legal firm that wants AI to draft in their house style using twenty years of contracts and reference this morning's court rulings doesn't choose between the two — it fine-tunes for style and uses RAG for the rulings. Hybrid is normal.

Agents sit on top of all this as a third move that is mostly inference-time scaling in disguise. The "magic" of an agent calling tools or browsing the web is, mechanically, the model emitting a string that your code interprets as an instruction to run a function, then feeding the result back into another prompt. Workflows — orchestrated sequences of LLM calls with code-defined paths — are predictable and testable. Truly autonomous agents, which decide their own steps, are flexible but unpredictable in both behaviour and cost; an infinite loop in an agent isn't a bug, it's a budget event. The strategic question is how much autonomy you actually need versus how much you are buying because the word sounds impressive.

None of these decisions are purely technical, which is why they cannot be left to the engineering team alone. Model choice has infosec implications (sending data to OpenAI is a different conversation than running Llama on your own infrastructure). Fine-tuning has talent implications (you need data scientists comfortable with experimental failure). Agentic systems have legal and audit implications (you cannot easily explain what an autonomous loop did or why). The right decision-making posture is what data scientists already know and most of the rest of the organisation has to learn: science-first. You build a small evaluation dataset, define a business metric, prototype the cheapest option, measure, and iterate. You do not commit to fine-tuning before you have proven that better prompting and better retrieval cannot solve the problem. Most "intelligence" failures in production are retrieval failures or prompting failures wearing a more flattering costume.

The skill this builds is the ability to look at any AI proposal — yours or someone else's — and immediately ask the right question: is this a context problem or a capability problem? If you can answer that, you can choose the cheapest tool that solves it, defend the choice to a cross-functional room, and avoid the trap of treating complexity as a feature. Complexity is a cost. The leaders who win with AI are the ones who reach for the simplest lever first and only escalate when the evidence demands it.

## Level 2 candidates

**RAG architecture and the vector data store** — Covers the mechanics of encoding models, vector similarity search, chunking strategies, and how a knowledge base is actually constructed and queried. Worth deeper treatment because the quality of a RAG system lives or dies on retrieval quality, and leaders making infrastructure decisions (which vector store, which encoder, what chunk size) need more than the conceptual sketch.

**Fine-tuning: when it actually wins** — Covers the cases where fine-tuning genuinely outperforms RAG — narrow specialised tasks, tone and format internalisation, small models beating frontier models — along with the data, compute, and talent prerequisites. Worth going deeper because the asymmetry of risk and reward here is severe and the decision criteria are subtle.

**Agents vs workflows** — Covers Anthropic's distinction between orchestrated workflows (prompt chaining, routing, evaluator-optimiser) and autonomous agents, plus the function-calling mechanism that makes "tool use" possible. Worth going deeper because the hype-to-substance ratio is currently the worst in AI and leaders need a clear framework to push back on agent-shaped solutions to non-agent-shaped problems.

**Agent frameworks and the build-vs-buy spectrum** — Covers the landscape from heavyweight (AutoGen, LangGraph) to lightweight (CrewAI, OpenAI Agents SDK) to native, including the abstraction-debt argument from Anthropic's engineering team. Worth going deeper because this is a genuine architectural fork with long-term implications for control, cost, and team capability.

**The cross-functional decision toolkit** — Covers the practical framework for running AI decisions as collaborative, science-led processes, including the stakeholder map, the cost/benefit/risk matrix, and the experimental mindset shift. Worth going deeper because the tooling and ritual of how decisions get made is what separates organisations that scale AI from organisations that produce one good demo and stall.

**Inference-time scaling and the cost of "thinking"** — Covers how chain-of-thought, agentic loops, and evaluator-optimiser patterns trade compute time for output quality, and the unit economics implications. Worth going deeper because inference cost is becoming the dominant operational variable in AI products and most leaders haven't internalised that "smarter" usually means "more expensive per call."

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

A lot of AI projects go wrong before any code is even written, because the team misdiagnoses the problem. They see poor answers and assume the model needs to be “taught the business,” so they jump to fine-tuning. But often the model’s reasoning is already good enough; it is failing because it was not given the right facts at request time. That mistake is expensive: months of model work, unclear results, higher operational risk, and a system that is harder to debug than the simpler alternative they skipped.

This matters because inference-time and training-time are not just technical implementation details. They create different systems with different failure modes. If your knowledge changes daily and you bake it into model weights, the system goes stale and becomes hard to audit. If you rely only on retrieval for something that is really about consistent style or domain-specific behaviour, outputs stay uneven no matter how much context you stuff into the prompt. Without a working model of the difference, teams spend money solving the wrong problem.

---

## What You Need To Know First

**1. A model has “weights,” and those weights are the learned parameters of its behaviour.**  
When people say a model “knows” something, they usually mean patterns from training have been encoded into those weights. You cannot inspect them like a document or database row. They shape how the model tends to respond, but they are not a clean storage layer for facts you want to update or cite later.

**2. A prompt is the temporary context the model sees for one request.**  
At inference time, the model gets an input window: instructions, user question, and maybe extra documents. It answers based on that current context plus whatever general behaviour is already in its weights. The important distinction is that prompt-time context is easy to change per request; the weights are not.

**3. Retrieval means looking up relevant information from an external store before asking the model to answer.**  
Instead of expecting the model to contain all your company knowledge internally, your system fetches the most relevant documents and includes them in the prompt. That is the basic mechanism of RAG. The model is not becoming more knowledgeable in a permanent sense; your system is just putting the right evidence in front of it at the moment it answers.

**4. Fine-tuning is additional training on examples that push the model toward a narrower behaviour.**  
You take an existing model and continue training it on your own task data: desired outputs, formats, tone, classifications, or domain-specific patterns. This can make the model act more consistently on that kind of task, but it is slower, riskier, and less transparent than retrieval because you are changing the model itself rather than feeding it better context.

---

## The Key Ideas, Connected

**1. Most AI architecture choices reduce to two levers: change the context, or change the model.**  
The article’s core simplification is that many AI buzzwords are variations on one of these two moves. Either you leave the model alone and improve what it sees when asked a question, or you modify its weights so it behaves differently by default. This framing matters because it cuts through tool names and focuses on mechanism: are you solving the problem by supplying information at runtime, or by permanently changing model behaviour? Once you see that, you can ask which mechanism actually matches the failure you have.

**2. Inference-time optimisation works by giving the model better input at the moment it answers.**  
Prompting techniques, chain-of-thought scaffolds, and RAG all sit here. Mechanically, nothing inside the model changes; your system just constructs a better prompt. That means the model’s success depends heavily on whether the right context is included, in the right form, at the right time. This naturally leads to RAG, because once you accept that many failures are context failures, you need a repeatable way to fetch the right context rather than hand-writing prompts forever.

**3. RAG is a system for attaching current, external knowledge to a request without retraining the model.**  
The plain version is: user asks a question, your code searches your knowledge base, retrieves likely relevant material, adds it to the prompt, and the model answers using that material. The important mechanism is separation of responsibilities. The database stores knowledge; the model performs language reasoning over what it is given. That separation explains RAG’s strengths: facts remain auditable, updateable, and governable because they still live outside the model. But it also reveals the dependency that follows: if the retrieved material is poor, the model’s answer will also be poor, even if the model itself is capable.

**4. Because RAG depends on retrieval quality, many “model failures” are really retrieval failures.**  
If the system fetches the wrong document, misses the relevant paragraph, or chunks content badly, the model cannot reason over information it never received. This is why the article says many production intelligence failures wear a flattering costume: people blame the model because the final answer looks unintelligent, but the underlying mechanism is often that the prompt lacked the needed evidence. Once you understand this, you also see why teams overreach into fine-tuning too early: they are trying to fix missing context by altering the model’s internals.

**5. Training-time optimisation changes the model’s default behaviour by updating its weights.**  
Fine-tuning is not “giving the model documents.” It is repeatedly showing examples so the model internalises patterns. Those patterns might be style, format, task-specific judgement, or a specialised way of mapping inputs to outputs. This is a different mechanism from retrieval. Instead of saying “here are today’s facts,” you are saying “respond like this, in situations like these.” That difference explains why fine-tuning is better for durable behavioural patterns than for constantly changing information.

**6. Fine-tuning is powerful when the goal is stable behaviour, but risky when used as a knowledge storage strategy.**  
If you want consistent house style, a particular extraction format, or strong performance on a narrow repeated task, changing the weights can help because you want the model to carry that tendency everywhere. But if you try to encode changing business facts into weights, you create problems: updates are slow, evidence is hard to inspect, and outputs become harder to explain. The article mentions catastrophic forgetting because weight updates do not add capabilities cleanly like appending to a database; they can interfere with behaviour the model already had. That is why training-time work behaves more like R&D than product assembly.

**7. The practical decision rule is: put changing facts in context; put stable patterns in weights.**  
This is the article’s main operational split. Facts such as policies, rulings, product docs, inventory, or current account information change over time and often need citation. Those belong in retrieval. Style, format, tone, and specialised response habits are persistent behavioural preferences; those are what fine-tuning can encode. This rule leads directly to the idea of hybrid systems, because real business problems often require both current facts and consistent behaviour.

**8. Hybrid systems are normal because many applications need both external knowledge and internalised behaviour.**  
A legal drafting assistant is a good example: the latest rulings should come from retrieval because they change and must be traceable, while the firm’s drafting style can be fine-tuned because it is a repeated behavioural pattern. The mechanism here is compositional: retrieval supplies situation-specific facts, and the model’s weights supply stable response tendencies. Understanding that prevents the false choice of “RAG or fine-tuning” when the actual architecture may be “RAG plus fine-tuning, each doing the job it is mechanically suited for.”

**9. Agents mostly add orchestration on top of these same mechanisms, usually at inference time.**  
The article demystifies agents by reducing them to a loop: the model emits text that your system interprets as a tool call, code executes the tool, the result is fed back into another prompt, and the cycle continues. In other words, the “agency” is often not a fundamentally new intelligence layer; it is inference-time control flow around model calls. That matters because it changes how you evaluate them: not as magic, but as a tradeoff between flexibility and predictability.

**10. Workflows are easier to test because the path is code-defined; autonomous agents are harder to bound because the path is model-chosen.**  
If you predefine the sequence—retrieve, classify, draft, review—you know where cost comes from and where errors can occur. If the model decides what to do next at each step, you gain flexibility but lose predictability. That is why an infinite loop in an agent becomes a budget event: the model keeps selecting more actions, and each action costs money and creates more state to reason about. The failure mode comes directly from the mechanism of autonomy. More freedom in control flow means more difficulty constraining behaviour, explaining decisions, and forecasting spend.

**11. These architecture choices are cross-functional because the mechanics create business-side consequences.**  
If you send data to a hosted frontier model, that is not just a model-quality decision; it is an infosec and compliance decision. If you choose fine-tuning, you are committing to data quality work, experimentation, and specialised talent. If you deploy autonomous agents, you inherit legal, audit, and operational questions about what actions were taken and why. The article’s point is that technical mechanism and organisational consequence are linked: different architectures produce different governance burdens.

**12. The right operating posture is to test the cheapest plausible lever first and escalate only when evidence demands it.**  
This conclusion follows from the asymmetry of cost and reversibility. Better prompting and retrieval are usually cheaper, faster to prototype, easier to debug, and easier to govern than fine-tuning or highly autonomous agents. So the disciplined question becomes: is this a context problem or a capability problem? If context fixes it, stop there. Only when evaluation shows that context is not enough should you pay the cost of changing weights or adding autonomy. That closes the chain: once you understand the distinct mechanisms, you can choose complexity deliberately instead of inheriting it by hype.

---

## Handles and Anchors

**1. RAG is giving the model an open-book exam; fine-tuning is changing how the student thinks.**  
If the problem is “the student didn’t have the textbook page,” open the book. If the problem is “the student consistently writes in the wrong style or uses the wrong method,” training may help. This analogy captures why changing facts and stable behaviour belong in different places.

**2. Ask: “Am I missing information, or missing a habit?”**  
If the system fails because it lacks current facts, retrieval is the first move. If it fails because even with the facts it still does not respond in the desired format, tone, or domain-specific pattern, then you may need fine-tuning. That question is a good quick diagnostic in architecture conversations.

**3. Complexity is not intelligence; it is a bill.**  
This is the article’s underlying tradeoff. More steps, more autonomy, more training, and more orchestration can improve results, but they also increase cost, unpredictability, and governance burden. A useful reflex is to ask not “what is the most advanced approach?” but “what is the cheapest mechanism that fixes the observed failure?”

---

## What This Changes When You Build

**1. An engineer who understands this will diagnose bad answers by inspecting retrieval and prompt construction before proposing fine-tuning, because many failures are caused by missing or poor context rather than insufficient model capability.**  
The unaware engineer sees weak outputs and jumps to “we need a better model” or “we need to train it on our data.” The consequence is expensive work on the wrong layer while the real issue—bad chunking, poor search, irrelevant retrieved passages, or prompt overload—remains unfixed.

**2. An engineer who understands this will separate dynamic business knowledge from behavioural customisation in system design, because those two things have different update and governance needs.**  
By default, teams often mix them conceptually: “our model should know our policies and sound like us.” A better design is to keep policies, product details, and changing documents in a retrieval system, while handling style and repeated output patterns through prompt templates or fine-tuning if needed. This leads to systems that can be updated without retraining and audited without guesswork.

**3. An engineer who understands this will treat fine-tuning as an experimental investment with data and evaluation prerequisites, because changing weights is not a straightforward configuration choice.**  
The unaware engineer may assume that enough internal documents automatically make fine-tuning worthwhile. In practice, good fine-tuning needs high-quality task examples, clear success metrics, and tolerance for uncertain outcomes. Without that, teams burn time and compute and still cannot explain why behaviour improved or regressed.

**4. An engineer who understands this will prefer workflows over autonomous agents unless the task genuinely needs open-ended decision-making, because code-defined paths are easier to test, cost-bound, and audit.**  
The default temptation is to buy “agentic” capability because it sounds more powerful. But for many production tasks—document processing, support routing, report generation—a structured workflow gives most of the value with far fewer surprises. The consequence of choosing autonomy by default is not just occasional weird behaviour; it is unstable cost, harder debugging, and weaker accountability.

**5. An engineer who understands this will frame AI implementation as an evaluation loop, not a one-time architecture bet, because the only reliable way to choose between retrieval, fine-tuning, and agents is to measure them against the actual business task.**  
The unaware engineer argues from intuition or vendor claims. The stronger approach is to build a small evaluation set, define what “good” means, prototype the least costly option, and only escalate if the results fail. That changes outcomes because it makes complexity something you earn with evidence instead of something you inherit from fashion.

</details>
