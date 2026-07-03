# AI Data Governance — Level 0: Course Map

> **Intent:** Any organization that uses AI tools, builds an AI-powered product, or both, is making a continuous stream of decisions about what data flows into AI systems, what comes out, who's accountable, and what happens when something goes wrong. AI data governance is the discipline of making those decisions deliberately instead of by accident. A practitioner studies this domain to move from "we have some policies about AI" to a coherent model of where data goes, what could go wrong at each point, and which controls actually address which risks.
> **Your angle:** This map assumes you already have general professional experience with data, security, or product work, and are filling in the parts specific to AI systems rather than starting from zero. It's written to serve two overlapping audiences at once — someone whose company *consumes* AI tools (employees using LLMs, internal copilots) and someone whose company *builds* an AI product (a model or an application wrapping one) — because in practice most organizations sit in both roles simultaneously, and the governance concerns rhyme even when the specifics differ.

---

## How to use this map

This document is a structural map, not an explanation. Its job is to replace a flat, undifferentiated sense of "AI privacy stuff" with a shape: AI data governance isn't one thing, it's four layers, and knowing which layer a problem belongs to is most of what "understanding the domain" means at this level.

- **Why it exists** (Foundations) — the disciplines this converges from, and the accountability structures that make governance someone's actual job rather than nobody's.
- **How data actually moves** (Data Through the AI Lifecycle) — from sourcing, through classification, through however it enters a running system, to what happens once it's absorbed into a model or needs to be deleted.
- **Which controls address which risks** (Risk & Control Domains) — access control, model-behavior risk, and vendor risk, mapped to the specific failure modes they're built to catch.
- **How organizations operationalize it** (Operationalizing Governance) — ownership, monitoring, and the cultural conditions that determine whether any of the above survives contact with real usage.

Reading this document gets you that shape — enough to place a specific problem correctly and know what to ask for next. It does not get you the content of any given node: no worked implementation, no vendor questionnaire, no incident walkthrough. Each Level 1 topic is a domain you could spend real time in — deep enough, once actually written out, to inform a policy, a vendor evaluation, or a system design. The "what it is and why it matters" paragraph here only tells you whether that domain is relevant to your situation right now; the Level 2 candidates are pointers to the sub-questions you'd hit once you descended into it, not answers to them. This isn't meant to be read start to finish — skim the four-layer structure above, identify which layer your actual problem sits in, then descend.

---

## Topic Inventory

### Foundations

#### L1-01 · Why AI Data Governance Exists
AI data governance isn't a discipline invented from scratch — it's the point where data governance, information security, and product risk management all converge on a new set of data flows. What makes it feel new is that AI systems introduce data behaviors those older disciplines weren't built to anticipate: a model can absorb data into its weights rather than just storing it in a row, and a single request can trigger retrieval, generation, and action in ways a traditional application doesn't. Understanding this convergence early prevents two common mistakes: treating AI governance as an entirely separate function from existing data/security practice, or assuming existing practice covers it without modification.

**Level 2 candidates:**
- **The three converging disciplines** — seeing data governance, infosec, and AI/product risk as one lineage explains why most "AI governance" controls are recognizable adaptations, not inventions.
- **What's actually new about AI systems** — isolates the small number of genuinely novel problems (data absorbed into weights, emergent agentic behavior) from the much larger set of familiar problems wearing new labels.
- **The consumer/builder distinction** — most organizations are simultaneously a consumer of some AI tools and a builder of others, and the two roles carry different obligations worth telling apart early.
- **Why this became urgent now** — the historical trigger (widespread LLM adoption from 2022 onward outpacing existing policy) that explains why this field is being actively written rather than settled.

#### L1-02 · Regulatory & Standards Landscape
Data protection law existed before AI and largely still applies to it — GDPR, CCPA, and sectoral regimes like HIPAA govern personal data regardless of what system processes it. What's changed is the arrival of AI-specific instruments (the EU AI Act, sector guidance, national AI strategies) layered on top, plus voluntary standards (NIST's AI RMF, ISO/IEC 42001) that organizations adopt to demonstrate mature practice even without a legal mandate. Knowing which layer a given requirement comes from — general data law, AI-specific law, or voluntary standard — determines whether it's a legal obligation, a contractual expectation, or a best practice.

**Level 2 candidates:**
- **General data protection law applied to AI** — why GDPR's existing obligations (lawful basis, data subject rights) didn't disappear just because a new kind of system is processing the data.
- **AI-specific regulation (EU AI Act and peers)** — the first wave of law written with AI systems specifically in mind, including risk-tiered obligations that scale with how consequential a use case is.
- **Voluntary standards (NIST AI RMF, ISO 42001)** — frameworks organizations adopt for credibility and structure even where no law requires them, increasingly referenced in vendor contracts and audits.
- **Sectoral overlays (HIPAA, GLBA, and peers)** — why healthcare, finance, and other regulated industries face additional constraints on top of general AI governance.
- **Jurisdictional fragmentation** — the practical headache of operating across regions with different, sometimes conflicting AI and data rules simultaneously.

#### L1-03 · Accountability Models & Risk Frameworks
Governance fails less often from missing policy than from unclear ownership — nobody is quite sure who approves a new AI use case, who's accountable if it goes wrong, or who monitors it after launch. This topic covers the organizational patterns that assign that accountability: risk-tiering frameworks that route higher-stakes AI use cases through heavier review, and structural models (borrowed largely from financial services' "three lines of defense") that separate the people building/using a system from the people checking it.

**Level 2 candidates:**
- **Risk-tiering AI use cases** — the practice of routing a customer-facing hiring model and an internal note-summarizer through very different levels of scrutiny, rather than applying one policy to everything labeled "AI."
- **Three lines of defense** — the structural separation between people who operate a system, people who oversee risk, and independent audit — and why collapsing these into one function tends to produce blind spots.
- **RACI for AI systems** — the concrete artifact (who's responsible, accountable, consulted, informed) that turns "someone should own this" into an actual name.
- **Model/system inventories** — the basic prerequisite for any of the above: you can't govern AI use cases you haven't catalogued.

---

### Data Through the AI Lifecycle

#### L1-04 · Data Sourcing, Provenance & Consent
Before data reaches an AI system at all, someone decided where it came from — scraped from the web, licensed, collected with user consent, or generated synthetically — and that decision shapes almost everything downstream, especially for organizations building a model or fine-tuning one. This is the layer most relevant to AI *builders* rather than consumers: an organization training or fine-tuning on its own or third-party data inherits whatever provenance problems that data carried, and those problems tend to resurface later as legal exposure or as the specific unlearning problem covered in L1-07.

**Level 2 candidates:**
- **Consent and lawful basis for training data** — the question that determines whether data can be used for AI training at all, not just whether it's technically accessible.
- **Licensing and IP provenance** — why "we found it online" isn't a data-sourcing policy, and what happens when a model is trained on content it had no right to use.
- **Synthetic data as a sourcing strategy** — an emerging way to sidestep some provenance problems, with its own tradeoffs around fidelity and bias.
- **Provenance tracking through the pipeline** — the practical difficulty of knowing, months later, exactly which data a given model version was trained or fine-tuned on.

#### L1-05 · Classification & Minimization
Not all data carries the same risk, and treating it that way — sending everything to every AI system indiscriminately — is the single most common governance failure at the consumer-of-AI end of the spectrum. This topic covers the practice of labeling data by sensitivity and then constraining what's allowed to reach an AI system based on that label, which is the prerequisite for almost every technical control that follows.

**Level 2 candidates:**
- **Classification schemes** — the labeling system (public, internal, confidential, restricted, or similar) that everything else in this map assumes already exists.
- **Minimization as a design principle** — the discipline of sending an AI system only what a task requires, rather than everything available, whether that's a prompt, a retrieval corpus, or a training set.
- **Policy-as-code enforcement** — turning a classification scheme into an automatic, systematic block rather than relying on individual judgment at the point of use.
- **The cost of over-classification** — the less-discussed failure mode where excessive caution blocks legitimate, low-risk AI use and pushes people toward ungoverned workarounds instead.

#### L1-06 · Inference-Time Data Flows
Once data reaches a deployed AI system, it can enter in several structurally different ways — a direct prompt, a retrieval step that injects external content, an autonomous agent calling tools across multiple systems — and each pattern moves data across the trust boundary differently, with a different point where a control could intervene. This topic matters to consumers and builders alike: it's the layer where "is this specific AI feature safe" gets a real answer, instead of reasoning about "AI" as one undifferentiated thing.

**Level 2 candidates:**
- **Direct prompting** — the simplest pattern, where the trust boundary is crossed exactly once, at the moment a person sends a message.
- **Retrieval-augmented generation (RAG)** — moves the effective boundary earlier, to whatever the retrieval step decides to pull in, which is why access control has to be enforced before generation, not just at the interface.
- **Agentic tool use** — multiplies the exposure surface, since a single task can touch multiple systems, each with its own permission check required.
- **Session memory and caching** — why "one-off request" framing understates the risk for systems that persist context across turns or sessions.
- **Multimodal inputs** — images, audio, and documents carry metadata and embedded information that text-focused controls often miss entirely.

#### L1-07 · Data Absorbed Into Models
This is the layer where AI systems genuinely diverge from prior data-governance frameworks. Data that's used to train or fine-tune a model can become part of its weights rather than sitting in a retrievable, deletable record — which is why "no training on inputs" is often the single most consequential clause in an AI vendor contract, and why the right-to-erasure obligation from L1-02 becomes genuinely difficult to satisfy once training has happened. This topic is most acute for builders fine-tuning their own models, but it also determines what a consumer organization should demand from any vendor whose product might train on their data.

**Level 2 candidates:**
- **Training data memorization** — explains why a model can sometimes reproduce fragments of its training data, and why that counts as a leak rather than a feature.
- **Extraction and membership-inference attacks** — the research question of whether specific data can be shown to have been in a training set, the technical mirror of the legal erasure problem.
- **Machine unlearning** — the still-immature technical effort to remove a data point's influence from trained weights without full retraining.
- **Fine-tuning vs. in-context use** — the fork in the road that determines whether a given piece of data is transient (in a prompt) or potentially permanent (absorbed via training).

#### L1-08 · Retention, Deletion & Erasure
Every point where AI-related data is stored — prompts, completions, logs, embeddings, cached context, training sets — needs its own retention policy, and those policies need to actually satisfy legal deletion obligations, not just look like they do. This topic is where the abstract right-to-erasure problem from L1-02 and L1-07 becomes an operational checklist: what gets deleted, from where, on what trigger, and how you'd prove it happened.

**Level 2 candidates:**
- **Retention windows across the stack** — why prompts, logs, and cached context each need their own retention clock, since they're rarely deleted together automatically.
- **Deletion requests in practice** — the gap between "we honor deletion requests" and actually propagating that deletion through every downstream copy, including vector stores and backups.
- **Erasure limits for trained models** — the honest acknowledgment that some categories of erasure request may not be technically satisfiable once training has occurred, and what that means for policy.
- **Proving deletion (auditability)** — the difference between deleting data and being able to demonstrate to a regulator or customer that it was deleted.

---

### Risk & Control Domains

#### L1-09 · Access Control & Security for AI Systems
AI systems need the same security discipline as any other system handling sensitive data, applied at points that are easy to overlook — the retrieval layer of a RAG system, the logs of a gateway, the vector store behind a chatbot. This topic is the technical backbone for enforcing everything decided in L1-05 (classification) and L1-06 (data flow patterns): least privilege, encryption, and permission checks, applied specifically to the new places AI systems put data.

**Level 2 candidates:**
- **Least privilege for AI access** — access control that follows the data through retrieval and generation, not just gating the login to the AI tool itself.
- **Permission-aware retrieval** — the specific fix for a well-documented RAG failure mode: a system indexing everything can surface content to a user never authorized to see the source.
- **Encryption at rest and in transit** — table-stakes protection for every store in the pipeline — prompts, logs, embeddings — not just the network connection.
- **LLM gateways and DLP** — the retrofit-able control layer that inspects and redacts requests before they leave the network, popular because it doesn't require changing the model or vendor relationship.
- **Prompt injection as a security problem** — why content encountered by an AI system (retrieved documents, browsed pages) can attempt to redirect its behavior, a risk category with no clean precedent in traditional application security.

#### L1-10 · Model Risk: Bias, Fairness & Explainability
Beyond data privacy, AI governance has to account for the risk that a model itself behaves unfairly, unpredictably, or opaquely — producing biased outcomes, making decisions nobody can explain, or degrading in ways that go unnoticed. This matters most acutely for organizations building AI products used in consequential decisions (hiring, lending, healthcare), but even internal-tool consumers inherit some of this risk whenever an AI system's output influences a real decision.

**Level 2 candidates:**
- **Bias and disparate impact** — why a model can produce statistically unequal outcomes across groups even without anyone intending it, and why testing for this is now a standard governance step.
- **Explainability and interpretability** — the tension between the most capable models and the ability to explain why they produced a specific output, which matters most in regulated, high-stakes decisions.
- **Model drift and performance monitoring** — the risk that a model's behavior degrades or shifts after deployment in ways that go unnoticed without ongoing evaluation.
- **Human oversight requirements** — the design decision of where a human must review or approve an AI-influenced outcome before it takes effect.

#### L1-11 · Third-Party & Vendor AI Risk
Almost no organization builds its entire AI stack from scratch — most rely on a model API, a cloud provider, or an embedded AI feature in existing software, which means a meaningful share of their AI risk is actually vendor risk. This topic is the practice of evaluating and monitoring those relationships: what a vendor does with your data, what they do with their own vendors (subprocessors), and how you'd know if either changed.

**Level 2 candidates:**
- **Vendor security and privacy questionnaires** — the practical instrument that operationalizes contract terms (retention, training use) into a repeatable yes/no assessment before onboarding.
- **Subprocessor chains** — the question of whether your vendor is itself sending your data to another vendor, extending the trust chain further than it first appears.
- **Shadow AI** — the risk this whole practice exists to prevent: employees or teams adopting ungoverned AI tools outside any formal vendor review.
- **Ongoing vendor monitoring** — why vendor risk isn't a one-time approval, since contract terms, subprocessors, and model behavior can all change after onboarding.

---

### Operationalizing Governance

#### L1-12 · Organizational Roles & Ownership
Policy without an owner tends to decay — this topic covers who in an organization actually holds AI data governance as a job, from dedicated AI governance functions to shared responsibility across legal, security, data, and product teams. The right structure depends heavily on organization size and whether AI is a core product or a supporting tool, but every structure needs to answer the same question: when something goes wrong, whose job was it to have prevented it.

**Level 2 candidates:**
- **Dedicated AI governance functions** — when an organization is large or exposed enough to justify a standalone team, versus folding the responsibility into existing risk functions.
- **Cross-functional ownership models** — the more common pattern, where legal, security, data, and product teams each own a slice, and the coordination between them becomes the actual governance work.
- **Executive and board accountability** — why AI risk increasingly shows up as a board-level reporting item, not just an operational concern.
- **Policy lifecycle ownership** — who's responsible for updating governance policy as regulation, vendor terms, and internal AI use all continue to change.

#### L1-13 · Monitoring, Auditing & Incident Response
Governance isn't just the policies written before deployment — it's the ongoing practice of checking whether those policies are being followed and having a plan for when they aren't. This topic covers the operational tail of the AI governance lifecycle: logging AI system activity, auditing it against policy, and responding when an AI system does something it shouldn't have (a data leak, a biased decision, a successful prompt injection).

**Level 2 candidates:**
- **Audit logging for AI systems** — what needs to be captured (prompts, retrieved context, actions taken) to reconstruct what happened after the fact.
- **Periodic compliance audits** — the recurring check that policy on paper still matches practice in production, since both tend to drift independently.
- **AI-specific incident response** — why a data leak through an AI system, or a successful prompt injection, needs its own response playbook distinct from a traditional breach.
- **Post-incident policy feedback loops** — the discipline of feeding what an incident revealed back into classification, access control, or vendor policy, so governance actually improves over time.

#### L1-14 · Culture, Shadow AI & Change Management
The best-designed governance framework fails if employees route around it because approved tools are slower or more restrictive than the free consumer app they already know. This closing topic is about the human and organizational side of governance: making the approved path the easy path, communicating policy in a way people actually absorb, and managing the constant churn as new AI capabilities and tools appear faster than policy can be written for them.

**Level 2 candidates:**
- **Why shadow AI happens** — usually a usability gap, not defiance: people route around governance when the sanctioned tool is meaningfully worse than the alternative.
- **Making the compliant path the easy path** — the practical design principle behind successful AI governance rollouts, as opposed to ones that generate workarounds.
- **Training and awareness programs** — the difference between a policy document nobody reads and one that actually changes behavior at the point of use.
- **Governance in a fast-moving landscape** — the standing challenge of writing policy for capabilities (new model types, new agentic features) that outpace the policy-writing cycle itself.

---

## Sequencing note

The dependency chain runs Foundations → Data Lifecycle → Risk & Control Domains → Operationalizing Governance, and it holds regardless of whether you're approaching this as an AI consumer, an AI builder, or both. L1-01 through L1-03 give you the shared vocabulary and structural framing that every later topic assumes — skim quickly if you already have general governance or risk-management background, since little here is AI-specific yet.

L1-04 through L1-08 are the conceptual core, and they diverge by role: L1-04 (sourcing/provenance) and L1-07 (data absorbed into models) matter most if you're building or fine-tuning a model; L1-05 (classification) and L1-06 (inference-time flows) matter most if you're primarily a consumer deciding what's safe to send to AI tools; L1-08 (retention/erasure) matters to both. If you only have time for one topic in this group, L1-06 is the one that generalizes best — it's the layer where "is this AI feature safe" gets answered concretely, for builder and consumer alike.

L1-09 through L1-11 are where governance becomes a set of concrete, implementable controls — this is the layer to descend into when you're actually designing a system or evaluating a vendor rather than building a mental model. L1-12 through L1-14 are the least technical and most organizational, and they're frequently underweighted relative to their actual importance: a technically sound control stack still fails without clear ownership (L1-12), a feedback loop (L1-13), and a culture that doesn't route around it (L1-14).

For someone new to this domain without a specific consumer/builder lean yet, the highest-leverage entry point is **L1-01 → L1-06 → L1-09**: understand why the field exists, then how data actually moves through a deployed AI system, then how that movement gets controlled. Everything else on the map fills in around that spine.