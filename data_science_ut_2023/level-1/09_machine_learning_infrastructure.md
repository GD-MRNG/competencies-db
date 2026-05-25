## Metadata
- **Date:** 26-05-2026
- **Source:** 09_machine_learning_infrastructure.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-09 · Machine Learning Infrastructure

The model is not the product. The system that runs the model is the product, and most data scientists learn this the hard way — usually around the time a model that scored beautifully in a notebook starts returning nonsense in production, or stops returning anything at all because an upstream column got renamed. In 2023 you could hand a pickle file to a platform team and walk away. In 2026 that handoff has collapsed. The platform team is smaller, the models are more numerous, and the expectation is that you understand enough about how your model lives in production to keep it alive there.

You don't need to become an MLOps engineer. You need a working mental model of three systems and the seams between them: the training system, the serving system, and the data substrate they both depend on. Get those right and the algorithm choice almost stops mattering. Get them wrong and no amount of XGBoost tuning will save you.

Start with the training system. Its job is not to produce a model — its job is to produce a model you can reproduce six months from now when something breaks. That means three things working together: code you can pin to a version, data you can pin to a snapshot, and a record of what you tried and why you picked this one. Containers (Docker, OCI) exist because "it worked on my machine" is not a debugging strategy when your machine has a different NumPy than the training cluster. Experiment tracking exists because in three months you will not remember whether the production model was trained with learning rate 0.01 or 0.05, and the difference will matter. The discipline here is boring and it pays off exactly when you most need it to: when something has gone wrong and you have an angry stakeholder waiting.

The serving system is where most of the surprises live. The first question is whether you score on a schedule (batch) or on demand (online), and the answer changes everything downstream. Batch scoring — running the model nightly over a table and writing predictions back — is cheap, forgiving, and right for most problems. Online scoring — responding to a request in 100 milliseconds while a user waits — is expensive, latency-sensitive, and right when the prediction needs to reflect something that just happened. Confusing the two is a classic failure mode: someone builds a beautiful real-time recommender for a use case where yesterday's predictions would have been fine, and burns six months on infrastructure that didn't need to exist. The reverse is worse: you ship a batch model into a workflow that needed online predictions, and your "personalization" is always one day stale.

The data substrate is where the house actually gets built on sand. Your model depends on features, and features depend on upstream data sources that you do not control. An analyst renames a column. A logging change drops a field. A vendor updates their API and the ID format shifts from int to string. None of these are bugs in your model. All of them will break your model. The fix is not heroic monitoring — it is treating your dependencies as contracts. You version what you can, you log what you can't, and you make peace with the fact that debugging a production failure six months from now will require reproducing the exact data the model saw, not just the code that ran. If you cannot reproduce the inputs, you cannot reproduce the bug, and you are guessing.

Resource allocation is the last piece that surprises people. A model that runs in 50 milliseconds on your laptop may run in 800 milliseconds on shared hardware under load, which is the difference between shipping and not shipping. You need a rough sense of where the wall is — when CPU is fine, when you need GPU, when the model is too big to fit alongside the four other things sharing that container. You don't need to optimize prematurely. You do need to know whether your inference budget is realistic before you pick the architecture, because retrofitting a smaller model into a system designed for a larger one is the kind of project that consumes a quarter.

What ties all of this together is a single question you should learn to ask before you start building: when this fails in production at 3am, what will I need to figure out what happened? If the answer is "the logs, the data snapshot, the model version, and the experiment record," you have an infrastructure. If the answer is "I'll figure it out," you have a notebook with ambitions. The skill this topic builds is not the ability to operate Kubernetes. It is the ability to design your work so that the next person — including future you — can debug it without a séance.

The algorithm is the easy part. The system around the algorithm is where the work lives, and where models actually earn or lose their value.

## Level 2 candidates

**Containerization and versioning** — How Docker and OCI containers give you reproducibility across environments, and why versioning code without versioning data snapshots is only half a solution. Worth a deep dive because the failure modes are subtle (silent dependency drift, mismatched CUDA versions) and the recovery cost is high.

**Experiment tracking and hyperparameter logging** — How to instrument training so you can answer "why did we pick this model?" months later, and what tools (MLflow, Weights & Biases, plain structured logs) actually buy you. Worth depth because the discipline is easy to skip and brutal to retrofit.

**Model serving: batch vs. online** — When to score on a schedule versus in real time, and the architectural consequences of each choice. Worth depth because this decision drives latency budgets, cost, infrastructure complexity, and team boundaries — and reversing it later is painful.

**Resource allocation and scaling** — How to estimate inference cost and latency before you commit to a model architecture, and when GPUs are necessary versus performative. Worth depth because the math is unintuitive and the wrong call here can quietly kill a project.

**Dependency management** — How to keep a six-month-old model working when the underlying libraries have moved on, and the tradeoffs between pinning everything (brittle) and pinning nothing (chaos). Worth depth because every team eventually inherits a model whose environment no longer exists.

**Debugging production failures** — How to reproduce a bug that only happened once, in production, three days ago, with data you no longer have. Worth depth because this is where the abstract case for logging, versioning, and data snapshots becomes painfully concrete.

---