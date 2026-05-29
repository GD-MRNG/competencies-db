## Metadata
- **Date:** 26-05-2026
- **Source:** 08_model_evaluation_and_monitoring.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-08 · Model Evaluation and Monitoring

A model that validates beautifully on your test set and ships to production is, statistically, about to disappoint you. Not because you did the math wrong. Because the test set was a photograph of the world on a Tuesday in March, and production is a movie that keeps playing. The gap between "this model works" and "this model is working" is where most data science projects actually fail — not in the algorithm, not in the feature engineering, but in the months after deployment when nobody is looking and the numbers slowly drift away from reality.

The first reframe you need is that model evaluation is not about the model. It is about a decision. Every model exists to make some decision better than it would be made otherwise — whether to approve a loan, which product to recommend, whether to flag a transaction. The right question is never "what is the AUC?" The right question is "does this model make this decision better than the current process, by enough to justify the cost of building, running, and maintaining it?" AUC and RMSE are instruments. They tell you something about the model in isolation. They do not tell you whether the model is worth deploying. A model with 0.85 AUC that improves conversion by 0.1% may be worthless. A model with 0.65 AUC that catches 30% more fraud than the rules engine may be transformative. Learn to translate model metrics into business metrics, because that translation is what you will be asked to defend.

Offline evaluation — the work you do before deployment — is where you build the case that the model is worth shipping. The mechanics here are well-trodden: hold out data the model has never seen, pick metrics that match the decision (precision when false positives are expensive, recall when false negatives are, calibration when you need probabilities you can act on), and compare against a baseline that is honest. The honest baseline is rarely "predict the mean." It is whatever the business is doing today: a rules engine, a heuristic, last quarter's model. If you cannot beat the current system meaningfully, you do not have a model worth deploying, no matter how clever it is.

Then comes the hard part. Offline evaluation almost always overstates real-world performance, and the gap is structural, not a bug you can fix by trying harder. Your training data was collected under one regime; production runs under another. Users adapt to the model — recommendations change what users click, fraud detectors change what fraudsters try, pricing models change what gets bought. This is the offline-online gap, and you should expect it. The discipline is to deploy with the assumption that your offline numbers are the optimistic case, and to design the rollout (a shadow deployment, a small A/B test, a gradual ramp) so that you find out what the real number is before betting the business on it.

Once a model is live, you have inherited a monitoring problem. The world moves and the model does not. There are three flavors of drift, and they fail differently. Data drift is when the input distribution changes — a new user segment appears, a sensor recalibrates, a marketing campaign shifts traffic. Prediction drift is when your model's outputs shift even if you cannot see the cause. Concept drift is the worst: the relationship between inputs and outputs changes, so the same features now mean something different. A fraud model trained before a new payment method existed will be confidently wrong about it. Monitoring is the practice of catching these before the business does, which means alerting on input distributions, output distributions, and — when ground truth eventually arrives — on actual accuracy.

This is also where retraining becomes a real decision rather than an academic one. The naive answer is "retrain on a schedule." Sometimes that is right. Often it is wrong, because retraining on drifted data can bake the drift into the model and amplify a feedback loop. (A recommender that pushes popular items will see more clicks on popular items, which it then learns to push harder.) Retraining triggered by drift is more disciplined but harder to operate. Continuous retraining sounds modern but introduces its own failure mode: every retrain is a new model, and you have lost the stable thing you were measuring against. The right answer depends on how fast your world moves and how expensive a bad model is — which is, again, a business question.

The skill this topic builds is a kind of professional paranoia. You stop trusting validation curves. You start asking what your training distribution will look like in three months, what happens when the upstream feature pipeline breaks, what the cost is of a silent 5% accuracy drop nobody notices for a quarter. You learn to write down, before deployment, what success looks like and what would make you turn the model off. The data scientists who get senior are not the ones with the best models. They are the ones whose models keep working, and who know the moment they stop.

## Level 2 candidates

**Offline evaluation and metrics** — The mechanics of choosing among accuracy, precision, recall, F1, AUC, RMSE, log loss, and calibration, and matching the metric to the decision the model supports. Worth a deep dive because most metric choices in real projects are made by default, not deliberately, and the wrong default quietly distorts every downstream decision.

**Offline-online gaps** — Why models that validate cleanly underperform in production: distribution shift, feedback loops, label leakage, training-serving skew. Worth depth because diagnosing which gap you have determines whether you fix data, features, or deployment process — and confusing them wastes weeks.

**A/B testing with models** — How to run an online experiment that proves a model improves the decision over the incumbent, including power analysis, novelty effects, interference between treatment and control, and how long to run. Worth depth because this is the bridge between offline confidence and a real business case, and the statistical pitfalls are non-obvious.

**Production monitoring and alerting** — Detecting data drift, prediction drift, and concept drift; choosing thresholds that surface real problems without drowning you in false alarms; what to monitor when ground truth labels arrive late or never. Worth depth because the implementation details (which statistical test, which window, which segment) determine whether monitoring catches problems or becomes noise you mute.

**Retraining strategies** — When to retrain on schedule, on drift triggers, or continuously; how to avoid feedback loops; how to validate a retrained model against the previous one before promotion. Worth depth because retraining policy is where the theoretical "models degrade" meets the operational reality of pipelines, costs, and rollback plans.

**Model cards and documentation** — Documenting intended use, training data, evaluation results, known limitations, and failure modes for the next person (often future you). Worth depth because the practice is shallow on its surface but reveals, in writing, the assumptions you did not realize you were making.

**Business metrics vs. model metrics** — Translating model performance into revenue, conversion, retention, or cost terms, and building the dashboards that let stakeholders see the model's actual contribution. Worth depth because this translation is what gets models funded, defended, and continued — and most data scientists never learn to do it crisply.

---