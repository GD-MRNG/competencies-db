## Metadata
- **Date:** 26-05-2026
- **Source:** 06_causal_inference_from_correlation_to_action.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-06 · Causal Inference: From Correlation to Action

Most of the questions you will be asked in your career are causal, even when they are dressed up as predictive. "Will this campaign lift revenue?" "Did the new onboarding flow reduce churn?" "Should we keep paying for this ad channel?" None of these are answered by a model that predicts well. They are answered by a model that tells you what would have happened otherwise — the counterfactual. And the counterfactual is the one thing your data does not contain.

This is the gap that separates analytics from data science. An analyst can tell you sales are correlated with temperature. You can tell them temperature is not moving sales — both are downstream of the season, and the only way to know if air conditioning affects revenue is to vary it deliberately. The analyst's chart is not wrong. It is just answering a different question than the one the business asked. Most of the costly mistakes in data work come from this confusion: a correlation is presented, a decision is made as if it were causal, and six months later the team is wondering why the lever didn't move the outcome.

The cleanest way out of this is the randomized experiment. When you flip a coin to decide who gets the treatment, you guarantee that the treatment group and the control group are, on average, identical in every way except for the treatment itself. Confounders cannot hide. This is why A/B testing is the gold standard, and why companies that can experiment cheaply (web products, recommendation systems) have an enormous advantage in knowing what actually works. If you can run an experiment, run it. Most of causal inference exists because you often cannot.

You cannot run an experiment when it is unethical (you cannot randomly assign people to smoke), expensive (you cannot rebuild the supply chain twice), slow (you cannot wait three years to learn whether a policy worked), or impossible (the event already happened). In those cases, you are stuck with observational data — data where treatment was not randomly assigned, where the people who got the treatment differ systematically from the people who did not, and where any naive comparison between them confounds the effect of the treatment with the effect of being the kind of unit that gets treated. Causal inference is the toolkit that lets you make progress anyway.

The mental model worth holding is this: you are trying to construct, from observational data, something that resembles the experiment you wish you could have run. Every method is a different strategy for doing that. Propensity score matching pairs each treated unit with an untreated unit that looked similar on observable characteristics before treatment, simulating random assignment within those pairs. Difference-in-differences compares the change in outcomes for a treated group against the change in outcomes for a similar untreated group, on the assumption that without treatment they would have moved in parallel. Synthetic controls construct a weighted combination of untreated units that tracked the treated unit closely before the intervention, then use that synthetic twin as the counterfactual after. Instrumental variables exploit some external source of variation — a lottery, a policy quirk, a natural cutoff — that affects the treatment but is otherwise unrelated to the outcome, letting you isolate the causal channel. Each method makes assumptions, and the assumptions are almost always more important than the math.

The reason this matters more in 2026 than in 2023 is that these techniques have left the academic journals and entered production. Tech companies estimate the lift of marketing campaigns with synthetic controls when they cannot hold out a region. Banks evaluate policy changes with difference-in-differences over branch-level data. Doubly robust estimators — which combine outcome modeling with propensity weighting so that you only need one of the two to be right — are now standard in causal inference libraries. The barrier is no longer access to the methods. The barrier is knowing when each one applies, and being honest about whether its assumptions hold.

There is also a quieter shift you should notice: the rise of causal interpretability tooling around predictive models. SHAP values and similar techniques will tell you which features drove a prediction, and it is tempting to read this as "which features cause the outcome." This is mostly wrong. A SHAP plot tells you what the model used. The model used whatever correlated with the target in training data. Treating these as causal effects — and worse, acting on them — is one of the most common modern failure modes. If a feature has a high SHAP value, that is a hypothesis worth testing causally, not a conclusion.

The skill this topic builds is a habit of mind more than a procedure. Before you fit anything, you ask: what would have happened to these units if they had not been treated? Where in my data is the answer to that question, and where am I being forced to assume? When the answer is "nowhere" and "everywhere," you know you are in correlational territory and you should say so out loud. The data scientists who get trusted with real decisions are the ones who can hold this distinction firmly in front of stakeholders who would prefer to forget it. Correlation is cheap. Causation is what the business is actually paying you for.

## Level 2 candidates

**Causal graphs and confounding** — Covers how to draw a directed acyclic graph that encodes which variables influence which, and how to read off it whether a given comparison is identified. Worth depth because most causal mistakes come from controlling for the wrong variable (a mediator, a collider) and a DAG is the only reliable way to see this before you regress.

**Randomized experiments and RCTs** — Covers what makes an experiment rigorous: randomization unit, sample size, stratification, handling of non-compliance and spillovers. Worth depth because most "A/B tests" in industry are subtly broken in ways that invalidate the causal claim, and the failure modes are not obvious from the dashboards.

**Propensity score methods** — Covers how to estimate the probability of treatment from covariates and use it for matching, weighting, or stratification. Worth depth because it is the most common production technique for observational causal estimation, and the diagnostics (overlap, balance) are where the work actually happens.

**Synthetic controls and difference-in-differences** — Covers how to estimate the effect of an event or policy by constructing a counterfactual from untreated units across time. Worth depth because these are the methods you reach for when you have a single treated unit (a market, a country, a product launch) and pre/post data, which is an extremely common shape.

**Instrumental variables** — Covers how to use an exogenous source of variation to identify a causal effect when treatment is endogenous. Worth depth because the method is powerful when it works and disastrous when the exclusion restriction fails, and learning to defend or attack an instrument is its own skill.

**Doubly robust estimation** — Covers methods that combine an outcome model and a propensity model so that consistency requires only one of them to be correct. Worth depth because it has become the practical default in modern causal libraries and changes how you think about model misspecification risk.

**Causal interpretability vs. feature importance** — Covers the difference between what SHAP, permutation importance, and similar tools actually tell you and what people read into them. Worth depth because misreading these tools as causal is one of the most consequential mistakes in applied ML, and the correction is conceptual rather than technical.

---