## Metadata
- **Date:** 26-05-2026
- **Source:** 10_business_acumen_and_problem_decomposition.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-10 · Business Acumen and Problem Decomposition

The most common failure mode in data science is not a bad model. It is a good model pointed at the wrong question. You can spend three weeks tuning a gradient booster, hit 0.91 AUC, ship it, and discover nobody changes their behavior because of it — because the decision the model was supposed to inform was never actually a decision anyone was about to make. The technical work was real. The business work never happened.

This is the gap that separates senior data scientists from junior ones, and it widens every year. Algorithms have commoditized. Libraries have commoditized. The hard, illegible, unautomatable part of the job is sitting with a stakeholder long enough to figure out what they're actually trying to do, what would change if they got it right, and how anyone would know. The 2026 data scientist who can do this is rare and expensive. The one who cannot is increasingly replaceable, because the parts they're good at — fitting models, writing transforms, generating charts — are the parts that tools and LLMs now do faster than they do.

The mental model worth holding is that every data science project is downstream of a decision. Someone, somewhere, is going to do something differently because of your work — or they aren't, in which case your work doesn't matter no matter how clever it is. Your job is to find that decision, name it precisely, and work backwards from it. What are the options on the table? Who picks between them? What information would tip the choice? What's the cost of getting it wrong in each direction? These questions sound like they belong to a product manager. They don't. They belong to whoever has the leverage to shape what gets built, and if you abdicate them, you forfeit that leverage.

The skill breaks down into a few moves you make, in order, before you write any code. First, you translate a vague request — "we want to understand churn better" — into a concrete decision and a concrete metric. Understanding churn is not a goal; reducing churn among annual subscribers in the second renewal cycle by intervening with a discount offer is a goal. The metric falls out of the decision: not "predict who will churn" but "rank users by expected response to a discount, where the cost of the discount is X and the value of a retained subscription is Y." The math changes once the decision is named. Often the model you would have built is not the model you should build.

Second, you estimate the value at stake. This is uncomfortable for technical people because it requires guessing, but a rough estimate is infinitely better than no estimate. If your churn model improves retention by one percentage point and an annual subscription is worth $200 and you have 50,000 subscribers in the relevant cohort, that's $100,000 a year — and now you know whether spending two months on it is reasonable. More importantly, you know whether spending two months on a 2% improvement is reasonable, which is the question that actually comes up. Cost-benefit reasoning is what tells you when to stop tuning and ship.

Third, you manage the conversation around what the model can and cannot do. Executives will hear "machine learning" and assume omniscience. Engineers will hear "machine learning" and assume nondeterminism they don't want to deal with. Product managers will hear "machine learning" and assume a feature they can ship next sprint. None of these are accurate, and your job is to make the actual capability legible — what inputs it needs, what outputs it gives, what it gets wrong, what it cannot ever know. This is where projects die quietly: not in a meeting where someone rejects the work, but in the six months where everyone assumed something different about what was being built.

Fourth, you prioritize ruthlessly. You will always have more requests than time. The trap is treating them as a queue to be drained rather than a portfolio to be picked from. The right question is not "which of these can I do?" but "which of these, if done, changes the most about how the business operates?" Most analytics requests, honestly examined, fail this test. Killing them — diplomatically — is more valuable than completing them.

Finally, there is the ethical layer, which is not a separate concern bolted on at the end but part of problem decomposition itself. A model that predicts which customers to deny credit to is doing causal work in the world, whether or not its builder thought of it that way. A recommendation system that optimizes engagement is selecting for the content that holds attention, which is not always the content that serves users. You don't need a philosophy degree to think clearly about this. You need to ask, early, who benefits and who pays — and to notice when the answer is uncomfortable.

The skill this topic builds is not technical but it is concrete: you become the person in the room who can take a fuzzy business problem and walk it down to a buildable specification, with a clear definition of success, an estimate of value, and an honest account of what could go wrong. That person sets the agenda. Everyone else executes against it.

## Level 2 candidates

**Translating questions to metrics** — Covers the move from a vague business goal ("understand churn," "improve experience") to a single measurable, trackable number that a model or analysis can be built against. Worth a deep dive because most projects fail here, and the failure mode is invisible — the metric looks reasonable until you realize it doesn't tell you what to do next.

**Cost-benefit and ROI estimation** — Covers how to put dollar values on model improvements before building them, and how to reason about whether a 2% precision gain is worth two months of work. Worth its own treatment because the math is simple but the framing is unfamiliar to most technical people, and getting it wrong wastes quarters of effort.

**Stakeholder management for technical work** — Covers how to communicate model capabilities and limitations to executives, PMs, and engineers without either overselling or burying the lede. Worth depth because the failure modes are domain-specific (executives, PMs, and engineers each misunderstand differently) and the moves to manage each are different.

**Prioritization under constraints** — Covers how to choose between competing requests when you can only build one thing, and how to say no to work without burning the relationship. Worth a deep dive because most data scientists default to a queue model and lose years of leverage that way.

**Ethical considerations and bias** — Covers how to recognize when a technically sound model causes harm — through biased training data, feedback loops, or misaligned objectives — and the practical moves to detect and mitigate it. Worth depth because the standard treatments are either too abstract (philosophy) or too narrow (one fairness metric), and the practitioner needs the working version in between.

---