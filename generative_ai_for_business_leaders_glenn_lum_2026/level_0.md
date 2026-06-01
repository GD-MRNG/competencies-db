# Generative & Agentic AI for Business Leaders — Level 0: Course Map

> **Intent:** To give non-technical leaders the structural understanding needed to set strategy, make architecture-level decisions, and lead delivery — without being dependent on engineers or vendors to frame the choices for them.
>
> **Your angle:** You already operate at the level of outcomes and trade-offs. The gap this map addresses is not general capability but specific vocabulary and mechanism — enough to ask the right questions, identify when you're being misled, and make decisions that survive contact with a real production system.

---

## How to use this map

Each **Level 1 topic** below is a concept worth an hour of focused reading — it gives you the full mental model, the reasoning behind it, and its place in the larger picture. A **Level 2 candidate** is a sub-concept within that topic worth going one level deeper on, usually because the tradeoff is subtle or the failure mode is expensive. Drill to Level 2 when a topic comes up in a real decision, when something in a conversation doesn't add up, or when you want to be able to push back rather than just nod along.

The map is not a syllabus to be completed in sequence. It is navigation infrastructure. Return to it when a project hits a wall, when a vendor makes a claim you can't evaluate, or when you need to explain a constraint to a stakeholder.

---

## Group 1 — Strategic Frame: Why AI Decisions Happen Before the Technology Choice

#### L1-01 · The Outputs-to-Outcomes Shift

AI is moving from tools that produce content for humans to act on, toward systems that complete work autonomously. This is not a cosmetic upgrade — it changes what needs to be managed. When AI produces outputs, the management question is prompting quality. When AI delivers outcomes, the management question is governance: permissions, accountability, error handling, and liability. Leaders who treat agentic systems the same way they treated generative tools inherit serious operational risk. The distinction was already visible in early enterprise deployments by 2023–24 and is now the primary fault line in AI strategy.

**Level 2 candidates:**
- **Agentic AI as a governance problem** — Drilling here reveals why the gap between an agent demo and a production agent is almost entirely governance and reliability infrastructure, not model capability.
- **The consultant-vs-delegate framing** — Understanding this distinction clarifies what management controls are actually required when AI is given autonomous action, and what breaks when those controls are absent.
- **Human-in-the-loop design** — Going deeper shows why partial automation with supervision consistently outperforms full automation in high-stakes or high-volume contexts, and what the design choices actually are.

#### L1-02 · Where Competitive Advantage Actually Lives

Because frontier model intelligence is now rentable by API call, the model itself is rarely the moat. The economic shift that matters is the decoupling of intelligence from ownership: the expensive pre-training has been commoditised, which means advantage now comes from what you connect that intelligence to — proprietary data, embedded workflow position, operational integration. Any AI initiative that could be replicated by a competitor with the same public APIs is a feature, not a strategy. This framing, articulated clearly in the 2023–24 wave of enterprise AI, changes how you evaluate proposals and how you allocate R&D investment.

**Level 2 candidates:**
- **Data, workflow, or model: where the alpha comes from** — Deeper treatment reveals the specific conditions under which data advantage, workflow integration, and model capability each produce durable differentiation, and the tests you can apply to a proposal.
- **Frontier vs open-source: the deployment decision** — Going deeper shows what the closed/open-weights distinction actually means for data governance, cost, and lock-in — not just a performance comparison but a fundamentally different architectural posture.
- **The thin wrapper failure mode** — Understanding this concretely is worth the time because it is the most common and most expensive AI investment mistake, and it is usually invisible until a competitor ships the same thing.

#### L1-03 · Value Taxonomy: Automation, Augmentation, Differentiation

These are not rhetorical categories — they determine how you measure success and how much operational risk you can afford. Automation replaces work humans currently do; errors have to be absorbed somewhere, and if that absorption requires expensive oversight, the ROI collapses. Augmentation pairs AI with humans to make them more effective; the failure mode is adoption, not accuracy. Differentiation creates capabilities that were not previously practical; the failure mode is defensibility. A single project can span all three, but the dominant driver controls which failure mode you should be designing against. Getting this wrong at the strategy layer means you're measuring the wrong things and tolerating the wrong risks.

**Level 2 candidates:**
- **ROI modelling for AI: the true denominator** — Drilling here reveals how consistently teams undercount the total cost of safe operation — review loops, monitoring, incident handling, drift management — and price projects accordingly.
- **Risk as a structural consequence of benefit** — The technical-to-strategic risk translation (hallucination → reputation, opacity → regulatory exposure, scale → blast radius) is worth deeper treatment because risk mitigation is a fixed cost, not optional polish.
- **The efficiency narrative trap** — Understanding why framing AI as headcount reduction consistently damages adoption (Klarna vs. Morgan Stanley) is worth a Level 2 because the communication choice is a leadership decision with measurable consequences.

---

## Group 2 — Architectural Decisions: The Two Levers and When to Pull Each

#### L1-04 · Retrieval-Augmented Generation (RAG)

RAG is the most important architectural concept for most business AI applications, and it is also the most frequently misapplied. The mechanism is simple: when a user asks a question, your system retrieves relevant material from your own data and includes it in the prompt; the model answers using that material without needing to be retrained. The strategic implication is that your knowledge stays in your database — auditable, updatable, governable — and the model supplies language reasoning over whatever you give it. Most production "model failures" are retrieval failures: the model was capable; the wrong context was retrieved. RAG was formalised as an approach by Lewis et al. at Meta in 2020 and became the dominant enterprise architecture by 2023.

**Level 2 candidates:**
- **Vector databases and semantic search** — Going deeper reveals why keyword search fails for knowledge retrieval and what the encoding and indexing layer actually does — relevant to infrastructure decisions and vendor comparisons.
- **Chunking strategy and retrieval quality** — This is where most RAG implementations fail in practice; the relationship between chunk size, overlap, and retrieval accuracy is non-obvious and has significant downstream consequences.
- **RAG vs fine-tuning: the decision rule** — The practical heuristic (changing facts → retrieval; stable behavioural patterns → weights) and the conditions under which it breaks down are worth their own treatment.

#### L1-05 · Fine-Tuning: When It Actually Wins

Fine-tuning updates a model's weights using your own examples, which means it changes how the model thinks rather than what it sees. A well-executed fine-tune on an 8B parameter model can outperform GPT-4 on a narrow task — this is genuinely useful and genuinely seductive. The failure modes are severe: catastrophic forgetting (the model loses previously competent behaviours), opaque outputs (you cannot explain why any particular answer was produced), and the prerequisite stack (clean task-specific training data, GPU infrastructure, ML talent comfortable with experimental failure). Fine-tuning is R&D, not engineering. Treating it as the latter is the most expensive common mistake in enterprise AI architecture.

**Level 2 candidates:**
- **Catastrophic forgetting and why weight updates aren't additive** — Understanding this mechanism explains why fine-tuning for knowledge addition reliably fails, which changes the question you ask when a vendor recommends it.
- **The data prerequisites for successful fine-tuning** — The quality, quantity, and format requirements for training data are specific and often underestimated; drilling here changes how you evaluate fine-tuning proposals.
- **Inference efficiency: distillation and quantisation** — These techniques let smaller fine-tuned models dramatically close the gap with larger frontier models on narrow tasks, which is restructuring cost curves in 2024–25 in ways that change build-vs-buy decisions.

#### L1-06 · Agents vs Workflows: The Autonomy Spectrum

The word "agent" currently carries enormous hype-to-substance ratio. The mechanism is not magic: the model emits text that your code interprets as a tool call, the tool runs, the result feeds back into the next prompt. In a workflow, a human or deterministic system specifies the sequence. In an agent, the model decides the next step. Agency introduces compounding error — each autonomous decision step can propagate failures that downstream steps cannot correct. The more useful distinction, surfaced by Anthropic's engineering team in 2024, is between orchestrated workflows (predictable, testable, auditable) and truly autonomous agents (flexible, unpredictable, difficult to cost-bound). The right question is not "should we use agents?" but "how much autonomy does this task actually require?"

**Level 2 candidates:**
- **Tool use and function calling** — The technical mechanism behind agents (model emits structured output → code executes → result re-ingested) is worth understanding at one level of depth because it demystifies capability claims and clarifies where errors actually originate.
- **Agent frameworks: the abstraction-debt argument** — Frameworks like LangGraph and AutoGen add abstraction that speeds prototyping but limits control; Anthropic's own guidance recommends starting without frameworks. The trade-off is a real architectural fork.
- **Inference-time scaling and the cost of "thinking"** — Chain-of-thought, multi-step agents, and evaluator-optimiser patterns trade compute cost for output quality; understanding the unit economics changes how you evaluate proposals that invoke "reasoning" as a selling point.

---

## Group 3 — Leadership and Delivery: Running AI Projects Like the Research They Are

#### L1-07 · AI Delivery Is R&D Wearing Product Clothes

The most expensive management mistake in AI is treating delivery like normal software: define scope, estimate effort, set date. AI adds a prior layer — feasibility uncertainty — that software does not have. The question is not whether you can build the system, but whether the data contains enough signal for the system to work at the required performance threshold. That question can only be answered by experimentation, not engineering. The consequence is structural: fixed output commitments made before feasibility is proven are not ambitious planning — they are gambling. Phase-gated roadmapping, where commitment is conditional on research outcomes, is the correct delivery posture. The "date for a date" technique is the practical instrument for managing this with stakeholders.

**Level 2 candidates:**
- **Phase-gated AI roadmapping mechanics** — The specific structure of research → validate → build → deploy → measure phases, with explicit gate criteria and contingency planning, is learnable and is the difference between a credible plan and a fantasy.
- **The "date for a date" as a stakeholder communication tool** — This is a specific technique for translating scientific uncertainty into business-legible commitments; understanding when and how to use it changes how AI leaders handle executive pressure.
- **North Star metrics vs model metrics** — The relationship between business outcomes (churn, productivity, fraud loss) and model metrics (accuracy, F1, latency) determines what you actually monitor and how you declare success or failure.

#### L1-08 · Team Scaffolding and the Data Pipeline Prerequisite

AI models sit inside a larger system, and that system — not the model — determines whether capability becomes value. Data engineers have to exist and be producing reliable, clean, accessible data before data scientists can produce reliable, useful models. This is a hard dependency that organisations routinely discover too late, after over-hiring model talent who then spend their time wrangling broken inputs. The role taxonomy — data scientist, ML engineer, AI engineer, data engineer, MLOps — is genuinely confusing, used inconsistently across companies, and the source of significant resourcing mistakes. Getting the team composition right is a leadership decision, not a technical one.

**Level 2 candidates:**
- **The data scientist vs data engineer vs ML engineer distinction** — These roles solve different problems and require different infrastructure to be effective; conflating them creates expensive hiring mistakes and misallocated responsibility.
- **Centralised CoE vs embedded teams vs hub-and-spoke** — Each org model has a characteristic failure mode; the right choice is maturity-dependent and most organisations evolve through several; knowing the failure modes saves a costly reorg.
- **Build vs buy: how the decision shifts team requirements** — Whether you are fine-tuning open-source models, consuming APIs, or building custom infrastructure changes which roles are critical paths and which are unnecessary.

#### L1-09 · Adoption, Drift, and the Operational Tax of Production AI

AI is not set-and-forget software. A model that performs well at launch will quietly degrade as data distributions shift, user behaviour evolves, and the world moves on from the training data. Model drift is not an edge case — it is a permanent operating cost that most year-one budgets do not include. Adoption is similarly persistent work: the Morgan Stanley vs Klarna comparison shows that comparable AI capability can achieve 98% adoption or significant backlash depending entirely on whether leadership frames the system as making people more capable or as replacing them. Both of these — drift and adoption — are leadership responsibilities, not engineering ones.

**Level 2 candidates:**
- **Model drift: what it is and how to monitor it** — The specific mechanisms of data drift, concept drift, and output quality degradation — and the monitoring cadences that surface them — are worth deeper treatment because this is the cost most commonly missing from year-two ROI.
- **Change management framing for AI adoption** — The specific communication choices (augmentation vs efficiency narrative, internal champions, staged rollout) that drove the Morgan Stanley and Klarna outcomes are replicable and worth understanding as a toolkit.
- **Governance cadences for AI initiatives** — Steering-committee structures, working-group formats, and standup rhythms for cross-functional AI projects look meaningfully different from standard software governance; the difference is the standing agenda item of feasibility and recruitment risk.

---

## Sequencing note

The dependency structure here is genuine and directional. The strategic frame (Group 1) must come first because it determines the questions you bring to architectural decisions — without it, technical choices are made in a vacuum and often solve the wrong problem. RAG (L1-04) should be the first architectural concept you understand in depth, because it is the mechanism behind most production AI systems and because misdiagnosing retrieval failures as model failures is the most common and most expensive architectural error. Fine-tuning (L1-05) and agents (L1-06) are best understood in contrast to RAG — they make more sense once you have a clear picture of what inference-time optimisation can and cannot do.

The delivery and leadership topics (Group 3) are not optional addenda — they are what determines whether the strategy and architecture topics produce value at all. The highest-leverage entry point for someone already in a leadership role is L1-07 (AI delivery as R&D), because it changes every subsequent decision about roadmaps, commitments, and team structure. The most commonly underweighted topic for experienced leaders is L1-09 (drift and adoption), because both costs are invisible at launch and only surface after the project is declared a success.

If you are advising on a live initiative rather than building foundational knowledge, start with L1-03 (value taxonomy) to establish what you're measuring, move to L1-04 (RAG) to evaluate the architecture being proposed, and use L1-07 (delivery as R&D) to assess whether the roadmap is honest. That sequence addresses the most common ways business leaders are misled in AI project reviews.

## Source

https://www.udemy.com/course/executive-briefing-generative-ai-and-large-language-models-llm/