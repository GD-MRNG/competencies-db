## Metadata
- **Date:** 22-05-2026
- **Source:** \section_3\combined_intermediate_summaries.md
- **Model:** Claude-Opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Leading AI Delivery: Why Execution Is Different

Most AI projects don't fail because the model isn't smart enough. They fail because leaders treated them like software projects. AI delivery looks like software delivery — there's a backlog, a roadmap, sprints, a launch — but underneath, it is research and development wearing software clothing. The moment you commit to a fixed output on a fixed date for a system whose feasibility you have not yet proven, you are gambling your reputation on a probabilistic outcome. This is the trap that turns impressive demos into projects that quietly stall in proof-of-concept purgatory.

The first thing to internalise is that AI development is non-deterministic. Traditional engineering is "if you build X, it will do Y." AI is "if you build X, it will probably do something close to Y, most of the time, until the world drifts and it doesn't anymore." That single shift forces you to manage three layers of uncertainty at once: feasibility uncertainty (can the data and the algorithms actually solve this problem?), operational uncertainty (can the organisation absorb a tool that doesn't always do the same thing twice?), and maintenance uncertainty (how fast will performance degrade as the world moves on from the data the model was trained on?). Model drift is not an edge case. It is a permanent operational tax on every AI system you put into production.

This is why the spine of AI leadership is the metric-first approach. You do not define the project by the technology — "we are deploying agents," "we are building a RAG system" — because the technology is a moving target and most of it will be obsolete in eighteen months. You define the project by the North Star metric it moves: churn down by fifteen percent, advisor productivity up by thirty percent, fraud losses down by half. The metric is what you commit to, what you instrument from day one, and what you use to decide which experimental approach is working when the science gets ambiguous. Without it, you cannot tell whether your project is succeeding, and neither can anyone else.

Once the metric is set, ideation becomes portfolio construction rather than technology shopping. Predictive AI (forecasting, fraud, churn, maintenance) is your low-risk, clear-ROI workhorse. Generative AI (content, copilots, knowledge assistants, synthetic data) is your augmentation layer. Agentic AI (autonomous workers, end-to-end process automation) is your high-upside moonshot, where the failures are also the most spectacular — the McDonald's drive-thru that took an order for two hundred and seventy chicken McNuggets and went viral did so because the team had removed the human from the loop in a noisy, public, high-volume environment. The right portfolio mixes all three, weighted by your organisation's actual appetite for R&D risk.

Then comes the part most leaders underestimate: roughly seventy percent of the difficulty in AI delivery is people and process, not technology. You cannot scale a data science team without first scaling the data engineering team that feeds it clean data — the pipes have to exist before the brain is worth investing in. You cannot deploy an autonomous system without designing the human-in-the-loop guardrails that prevent viral failure. And you cannot drive adoption with an efficiency narrative — Klarna's AI assistant achieved real technical ROI but suffered a cultural backlash because the messaging tilted toward job displacement. Morgan Stanley achieved ninety-eight percent advisor adoption by framing the same kind of system as making every advisor as smart as their best expert. The technology was comparable. The narrative was not.

The roadmap itself has to bend to all of this. The phase you cannot skip — and the phase business stakeholders will pressure you hardest to skip — is the research phase, where you validate that the data actually has predictive power before committing to a deployment date. The technique that lets you survive that pressure is what I'd call the "date for a date." You don't promise stakeholders when the system will ship. You promise them the date by which you will know enough to commit to a date. Subsequent milestones stay marked tentative until R&D clears the gate. This feels like a cop-out to executives used to deterministic delivery. It is in fact the most honest planning instrument available to you, and the alternative — a confidently-stated launch date built on unvalidated science — is the single most common way AI projects embarrass their leaders in production.

The skill this all builds toward is translation. You sit between a science team that legitimately cannot promise outcomes and an executive team that legitimately needs to plan around them. Your job is not to pick a side. It is to convert scientific uncertainty into business predictability — through phase gates, contingency time, plan Bs, transparent metrics, and communication that is early, frequent, and free of hype. The leaders who do this well end up with durable AI capabilities. The ones who don't end up with a graveyard of impressive demos that never reached production, because they had no data pipes, no talent scaffolding, no cultural buy-in, and no honest roadmap to survive contact with reality.

Respect the science, or the science will embarrass you in production.

## Level 2 candidates

**AI project ideation and portfolio construction** — Covers how to generate, filter, and prioritise AI ideas across predictive, generative, and agentic categories using criteria like proprietary data advantage, measurability, and pain-point fit. Worth its own Level 2 because the traps (solution-seeking-a-problem, generic "improve efficiency" projects, underestimating data requirements) are subtle and each deserves a worked example.

**The data engineer vs data scientist distinction and team scaffolding** — Covers the full cast of roles needed to deliver AI (data scientists, ML engineers, AI engineers, data engineers, MLOps, plus the business and product roles that surround them) and how the build-vs-buy decision shifts which roles you actually need. Worth deeper treatment because the role taxonomy is genuinely confusing, the labels are used inconsistently across companies, and resourcing decisions made early lock in delivery risk for the life of the project.

**Org models for AI: centralised, embedded, and hybrid** — Covers the trade-offs between an AI Center of Excellence, embedded line-of-business teams, and the hub-and-spoke and matrix variants in between. Worth a Level 2 because the right answer is maturity-dependent and most organisations evolve through several models — knowing the failure modes of each saves a costly reorg.

**Phase-gated AI roadmapping and the "date for a date"** — Covers the mechanics of structuring a five-phase roadmap (plan, research, build, deploy, measure) with tentative milestones, contingency planning, and metric checkpoints that account for R&D uncertainty. Worth deeper treatment because the techniques for translating uncertainty into stakeholder-legible commitments are specific, learnable, and the difference between a credible plan and a fantasy.

**Change leadership for AI adoption** — Covers the human side of AI rollout: managing perceived job-displacement threats, framing augmentation rather than efficiency, identifying internal champions, and using staged rollouts. Worth its own Level 2 because the case studies (Morgan Stanley's success, Klarna's mixed reception, McDonald's failure) each illustrate distinct adoption mechanics and the communication choices behind them.

**Model drift and the operational tax of production AI** — Covers why AI systems degrade in production over time, what monitoring and retraining cadences look like, and how to budget for ongoing maintenance rather than treating launch as the finish line. Worth deeper treatment because most leaders dramatically underestimate this cost and discover it only when ROI quietly erodes a year post-launch.

**Governance cadences for AI initiatives** — Covers the steering-committee, working-group, and standup structure that keeps cross-functional AI projects aligned, including how recruitment and feasibility risk should be standing agenda items. Worth a Level 2 because AI's uncertainty makes governance more consequential than for typical tech projects, and the lightweight version for startups looks meaningfully different from the enterprise version.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

AI projects often fail in a very specific way: they look healthy from the outside, get a flashy demo, get put on a roadmap like normal software, and then stall when the real system has to work repeatedly in production. The problem is not usually that nobody knew the term "AI." The problem is that teams planned and governed uncertain, probabilistic systems as if they were deterministic software features. That mismatch shows up as missed launch dates, weak adoption, brittle automations, and systems that quietly decay after release.

If you do not have a working model of why AI delivery is different, you make the wrong commitments at the wrong time. You promise dates before feasibility is proven. You fund model work before the data pipeline exists. You remove humans from workflows that still need supervision. You declare victory at launch and then get surprised when performance drifts. The result is not just technical disappointment; it is organisational damage: wasted budget, leadership distrust, and a backlog full of AI projects nobody wants to touch again.

This topic matters because AI delivery is not just "software, but with models." It changes what can be promised, how progress is measured, when risk is real, and what parts of the organisation actually determine success. If you do not see those mechanics clearly, you inherit a delivery model that sets you up to fail.

---

## What You Need To Know First

**1. Deterministic vs probabilistic systems**  
A deterministic system gives the same output for the same input if it is working correctly. Most traditional software aims for this. A probabilistic system produces outputs that are statistically good enough, not perfectly repeatable; its behavior is shaped by data and model quality, so performance is about rates, distributions, and confidence, not exact certainty. You need this distinction because the article's whole argument rests on AI behaving more like the second than the first.

**2. Proof of feasibility**  
Before you can promise delivery, you need evidence that the problem is actually solvable with the data and methods available. In AI, this usually means testing whether your data contains signal strong enough for the model to achieve a useful level of performance. This is different from building the production system. A team can be excellent at engineering and still fail if the underlying prediction or generation task is not feasible.

**3. North Star metric**  
A North Star metric is the business outcome the project is meant to move, such as reducing fraud loss or increasing support productivity. It is not the model metric alone, like accuracy or F1 score, though those may matter underneath. You need this because AI projects can easily become technology-first experiments unless anchored to a measurable business effect.

**4. Human-in-the-loop**  
This means a person remains part of the workflow to review, approve, correct, or supervise the AI system at important points. It is often the practical boundary between a useful system and a dangerous one, especially when the AI can make mistakes in public, at scale, or in high-stakes settings. This matters because the article treats full autonomy as much riskier than augmentation.

---

## The Key Ideas, Connected

**AI delivery looks like software delivery on the surface, but underneath it behaves like R&D.**  
A backlog, roadmap, sprints, and launch plan can make an AI initiative feel familiar, but that familiarity is misleading. In normal software, once requirements are clear, the main uncertainty is implementation effort: can we build the thing correctly and on time? In AI, there is an earlier and deeper uncertainty: will the data and methods produce useful behavior at all? That means part of the project is not "construction" but "discovery." You are not just building a system; you are testing whether the intended capability exists in a usable form.

**Because AI is probabilistic, uncertainty is built into delivery rather than being an exception.**  
Traditional software mostly fails when code is wrong or infrastructure breaks. AI can be "working" and still be unreliable, inconsistent, or weak in edge cases because its outputs are probabilistic. The article breaks this into three uncertainties: feasibility, operational, and maintenance. Feasibility uncertainty asks whether the task can be solved well enough. Operational uncertainty asks whether the organisation can live with a tool that does not behave identically every time. Maintenance uncertainty asks how performance changes as the world and data change. These are not separate from delivery; they are what delivery has to manage.

**Once uncertainty is intrinsic, fixed output commitments made too early become dangerous.**  
If you commit to shipping a specific AI capability by a specific date before proving feasibility, you are pretending a research question is already answered. That is why AI projects so often get trapped in proof-of-concept purgatory: the team can make something impressive enough for a demo, but not robust enough for production promises. The failure is not just "bad estimation." The deeper mechanism is that the organisation demanded certainty before the evidence existed to support it.

**Because you cannot manage uncertainty well without a stable target, AI projects must be defined by business metrics, not by technologies.**  
The article insists on a metric-first approach for exactly this reason. Terms like "agent," "RAG," or "copilot" describe implementation style, not business success. They are unstable anchors because the tools change fast and because multiple technical approaches may serve the same business goal. A metric like churn reduction or productivity increase gives the project a fixed point: it tells you what counts as success even if the technical path changes. Once the science gets messy, the metric is what lets you compare experiments and decide whether any of them are worth continuing.

**Once the metric is fixed, ideation turns from technology shopping into portfolio construction.**  
If the question is "how do we use agents?" you will collect fashionable ideas. If the question is "how do we move this metric?" you can generate options across different AI categories and compare them by risk and likely return. That is why the article separates predictive, generative, and agentic AI. Predictive use cases are usually more constrained and measurable, so they tend to have clearer ROI and lower delivery risk. Generative use cases often help humans do work faster or better, so they are often augmentation tools. Agentic systems aim for autonomy across tasks or workflows, which creates higher upside but also larger and more visible failure modes.

**This portfolio framing matters because the categories differ mainly in where failure shows up and how expensive it is.**  
Predictive systems fail by making bad forecasts or classifications. That can still be costly, but it is often easier to benchmark and contain. Generative systems fail by producing incorrect, awkward, or unsafe content, which is more variable and often requires review. Agentic systems fail by taking actions in the world without enough judgment, which amplifies mistakes into operational incidents. The McDonald's drive-thru example is useful because it shows what happens when you combine noisy inputs, public interaction, high volume, and no human backstop: errors become spectacle. That is not a random anecdote; it is the natural consequence of autonomy in a context with poor tolerance for mistakes.

**Because higher-risk AI modes amplify organisational weakness, most delivery difficulty shifts away from the model and into people, process, and infrastructure.**  
The article's claim that roughly seventy percent of the difficulty is non-technical is not saying technology does not matter. It is saying the main bottlenecks usually sit elsewhere. A data scientist cannot rescue a project fed by missing, dirty, or inaccessible data. An autonomous workflow cannot be safely deployed without human review design, escalation paths, and ownership boundaries. A good internal tool can still fail if employees see it as a threat rather than an aid. In other words, the model sits inside a larger system, and that larger system determines whether its capability becomes value.

**This is why data pipelines and team scaffolding have to come before scaling model ambition.**  
The article's line that "the pipes have to exist before the brain is worth investing in" captures a real dependency. Models consume structured, reliable, timely data. If that data does not arrive consistently, or arrives in unusable form, the model cannot be trained or operated well no matter how strong the science team is. So the dependence is concrete: data engineering is not support work that can lag behind; it is the precondition for repeatable AI delivery. Teams that ignore this often overhire model talent early and then watch them spend their time wrangling broken inputs instead of producing value.

**Even when the system works technically, adoption depends on whether people understand it as augmentation or threat.**  
This is where the article's examples of Klarna and Morgan Stanley matter. Comparable underlying capability can land very differently depending on framing. If leadership presents the system primarily as efficiency through labor reduction, users interpret it as a replacement mechanism and resist it. If leadership presents it as raising everyone's capability, users are more likely to engage. The mechanism here is not vague "culture." It is incentive perception: people adopt tools they believe make them better at their jobs and resist tools they believe are being used to make them unnecessary.

**Because feasibility is uncertain and the rest of the organisation still needs plans, AI roadmaps must be phase-gated rather than linearly committed.**  
This is the planning answer to the uncertainty described earlier. You separate discovery from commitment. In the research phase, the point is to validate signal and constraints, not to fake certainty. Only after that gate is cleared do later dates become meaningfully commit-able. Without phase gates, every milestone inherits the false assumption that feasibility was already known. With phase gates, planning becomes honest about what has been proven and what has not.

**The "date for a date" exists because stakeholders need predictability, but the science cannot honestly give final delivery dates early.**  
This is one of the article's most practical ideas. You do not promise ship date first. You promise the date by which you will know whether shipping is feasible and what a realistic plan looks like. That sounds softer, but it is actually more rigorous because it aligns commitment with evidence. It translates research uncertainty into a business-manageable milestone: not "the system will be live by September," but "by September we will know whether the current approach can meet the threshold and can then commit to a real launch plan." This is how you avoid lying with confidence.

**The leadership skill tying all of this together is translation between scientific uncertainty and business planning needs.**  
The science team cannot promise what the evidence does not support. The executive team still needs to allocate budget, sequence initiatives, and communicate expectations. Good AI leadership is not choosing one side over the other. It is building mechanisms that let uncertainty exist without turning planning into chaos: metrics, phase gates, contingency time, fallback options, guardrails, and regular communication. That is what turns AI from a collection of demos into a durable capability. Without that translation layer, uncertainty either gets suppressed until production failure exposes it, or allowed to remain so vague that the business cannot act.

**So the central lesson is that AI delivery succeeds when you respect uncertainty as a design condition, not a temporary inconvenience.**  
Everything in the article flows from this. If AI is probabilistic, you need metrics. If metrics are fixed, you can construct a portfolio instead of chasing tools. If risks differ across use cases, you need guardrails and human-in-the-loop design. If feasibility is unknown early, you need phase gates and a date for a date. If production performance decays, launch cannot be the finish line. The underlying mechanics are consistent: AI changes delivery because the capability itself is uncertain, variable, and perishable.

---

## Handles and Anchors

**1. "AI projects are research projects wearing product clothes."**  
Use this when explaining why normal software planning fails here. The outside shape looks familiar, but the inside contains discovery risk that cannot be estimated away. If you remember only one thing, remember that the roadmap is wrapping around unresolved science.

**2. "Do not commit to the tool; commit to the metric."**  
This captures the article's planning discipline. Models, frameworks, and AI fashions change quickly. The business outcome is the stable thing. If a colleague asks how to keep an AI project grounded, this sentence is a good answer.

**3. Ask: "Where does uncertainty still live in this system, and who absorbs it?"**  
This is a practical diagnostic question. If uncertainty lives in feasibility, then the roadmap needs a research gate. If it lives in outputs, then humans may need to review them. If it lives in drift, then monitoring and retraining must be budgeted. If nobody is explicitly absorbing the uncertainty, the organisation is probably pushing it into production by accident.

---

## What This Changes When You Build

**An engineer who understands this will approach roadmapping differently because feasibility must be proven before delivery can be promised.**  
The unaware engineer inherits the default software pattern: define scope, estimate effort, set launch date. In AI, that often creates fake precision. The informed engineer inserts a research phase with explicit exit criteria and uses a "date for a date" rather than a premature ship commitment.

**An engineer who understands this will approach project selection differently because not all AI categories carry the same risk profile.**  
The unaware engineer treats predictive, generative, and agentic work as variations of the same idea and may chase the most novel interface. The informed engineer asks where failure lands, how observable it is, whether a human can intervene, and whether the organisation actually has the risk appetite for autonomy. That changes whether they choose a forecast model, a copilot, or an end-to-end agent.

**An engineer who understands this will invest in data infrastructure earlier because model quality depends on the reliability of the input pipeline.**  
The unaware engineer may push to hire model talent or start prompt/application work before the data foundations exist. The consequence is expensive specialists spending time compensating for broken ingestion, missing features, or inconsistent schemas. The informed engineer sees clean, accessible, governed data as a prerequisite, not a parallel nice-to-have.

**An engineer who understands this will design human-in-the-loop controls deliberately because AI errors are often acceptable only when they are catchable.**  
The unaware engineer hears "automation" and removes human review too early, especially in customer-facing or high-volume systems. The informed engineer asks where approval, escalation, override, sampling, or audit review belongs. They know that partial automation with supervision often produces better business results than full automation with public failures.

**An engineer who understands this will plan for post-launch monitoring and retraining because model drift is an operating cost, not an anomaly.**  
The unaware engineer treats production launch as completion and budgets only for initial build. The informed engineer instruments the North Star metric and the model's operational metrics from day one, expects performance to change over time, and arranges ownership for recalibration or retraining. That changes staffing, cost forecasts, and how ROI is judged over the life of the system.

</details>
