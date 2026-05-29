# Data Science — Level 0: Course Map

> **Intent:** To move from raw data to business decisions reliably and repeatedly. Modern data science is less "discover hidden patterns" and more "build systems that predict, recommend, or explain at scale."
>
> **Your angle:** You've seen the old curriculum. That was 2023. The field has consolidated. LLMs have eaten half the feature engineering work. Jupyter notebooks have given way to production pipelines. Unlearn the "explore first, ask questions later" rhythm—it's now "what decision are we trying to make, and what data proves it?" Go for depth in the parts that actually cost you time in real systems.

---

## How to use this map

This map has three levels:

- **Level 0** (you are here): the forest—which clusters matter, and in what order.
- **Level 1**: each major topic—what it is, why practitioners care, what becomes possible once you own it.
- **Level 2**: specific concepts or techniques under each Level 1 topic—go here when you hit the thing you actually need to learn or re-learn.

Start by reading the Level 1 descriptions. They are written as directions, not definitions. If a description makes you curious or reminds you what you've forgotten, descend to Level 2. You do not need to learn every Level 2 candidate. You need to know they exist and where to find them when your work requires them.

The ordering reflects dependency—concepts on the left are foundational to concepts on the right, and concepts higher in each group unlock later ones. Start left and top.

```
Note: This course was completed in 2023 (Data Science and Business Analytics, UT Austin McCombs School of Business). The field has moved on. Rather than let these curricula fade, I've generated updated Level 0 maps reflecting what matters in 2026. Use these as starting points only. Keep the maps, not the course materials. The lecture videos and homeworks were for 2023–2024. The maps are timeless—they'll need tweaking every 18 months or so, but the structure holds.
```

---

## Topic Inventory

### Foundations: The Workbench

These are not optional. Everything that follows assumes you can do these things reliably, fast, and in code.

#### L1-01 · Python for Data Work

Python is how you think about data at scale now—not as an option, but as your working language. The 2023 curriculum taught "Python for Data Science" as if it were a subject. It is not. It is the medium. What matters in 2026 is speed: reading files, writing transforms, debugging type errors fast enough that you stay in flow. Pandas has been dethroned by Polars for new work (it's faster, more honest about nulls). DuckDB has become the quick-answer tool for "does this query make sense?" The Python worth learning is the Python that keeps you from context-switching to SQL.

**Level 2 candidates:**
- **Polars over Pandas** — Why Polars replaces Pandas for performance-critical work and what you lose (ecosystem maturity) and gain (speed, clarity).
- **Vectorization and broadcasting** — How to recognize when your code is looping where NumPy or Polars is parallelizing, and how to see the difference in run time.
- **Type hints and debugging** — Why type hints matter in data code (not just as documentation, but as a contract that lets you catch misalignments early).
- **Writing fast iteration loops** — Structuring code so you can rerun experiments in <10 seconds, not 2 minutes.
- **Profiling: memory and time** — How to find where your code is actually slow (it's rarely where you think).

---

#### L1-02 · SQL: The Lingua Franca

SQL is how data actually lives and moves in production. In 2023, SQL was optional flavor text. In 2026, if you cannot write a query that joins three tables, filters by date, and aggregates by category without switching tools or asking for help, you will lose time constantly. Modern databases (BigQuery, Snowflake, DuckDB) have made SQL expressive enough that 70% of what you might do in Python is clearer in SQL. Learn to think in sets, not loops. Learn window functions—they replace 90% of custom aggregation logic. Learn when to push computation to the database (where it's parallelized) vs. when to pull data and transform locally.

**Level 2 candidates:**
- **Window functions and CTEs** — How PARTITION BY and running aggregates reduce hand-rolled loops, and when to use WITH for clarity.
- **Query optimization and explain plans** — How to read an execution plan and recognize when you've written a query that scans a table twice by accident.
- **Handling nulls and missing data in SQL** — Why COALESCE and CASE matter, and how different databases treat NULL differently (crucial before you trust an aggregate).
- **Denormalization and design tradeoffs** — When to normalize (correctness, storage) and when to denormalize (speed, simplicity), with real examples.
- **Date and time arithmetic** — How to avoid off-by-one errors with dates, handle timezones, and compute cohort analyses correctly.

---

#### L1-03 · Statistics as Calibration

You don't need Bayesian inference or hypothesis testing theory to practice data science. You need to know when your numbers are noise and when they are signal. Statistics in 2026 is less "calculate a p-value" and more "am I overfitting? Is this sample size enough? What does this confidence interval actually tell me?" The old curriculum spent months on hypothesis testing. You need the intuition: what sample size is required to detect an effect? What does a confidence interval mean if I want to act on it? How do I know if a classifier is generalizing or just memorizing?

**Level 2 candidates:**
- **Sampling and power analysis** — How to estimate sample size needed to detect a difference, and why "more data" isn't always the answer if your effect is small.
- **Confidence intervals and uncertainty** — What a 95% CI actually means (not "95% chance the true value is in this range"), and how to use it for decision-making.
- **Multiple testing and correction** — Why running 100 analyses and picking the one that's significant is fraud, and what to do instead.
- **Bayesian thinking (informal)** — How to incorporate prior knowledge without needing a Markov chain, and when it clarifies decisions better than frequentist approaches.
- **A/B testing and causal inference** — How to design experiments that actually answer your question, and why observational data will lie to you.

---

### Core: The Problems Data Solves

These are the three ways practitioners actually use data: predict the future, explain the present, and optimize decisions.

#### L1-04 · Supervised Learning: Prediction

Supervised learning answers: "Given data like this, what comes next?" It is the workhorse of data work. A decade of competition (Kaggle, real production systems) has distilled it down: standard models (linear regression, tree ensembles, gradient boosting) solve 80% of real problems. Deep learning is a tool for image, text, and sequential data—not a default. What matters now is not the algorithm, but how you set up the problem: what target are you predicting? What features do you actually have access to at prediction time? How do you measure success—accuracy? Recall? Economic cost? You need to recognize different problem types (regression, binary classification, multiclass, ranking) because they require different setups.

**Level 2 candidates:**
- **Problem formulation and framing** — How to translate a business question into a machine learning target, and what can go wrong if you get this wrong.
- **Train-test splits and leakage** — Why a 90% accurate model can be worthless if information from the future leaked into training, and how to spot it.
- **Feature engineering vs. feature learning** — When to hand-craft features (and why it's becoming less of a bottleneck) and when deep learning handles it better.
- **Linear models and their assumptions** — Why linear regression is interpretable and when its assumptions break, and what happens to your coefficients.
- **Tree ensembles: Random Forest, Gradient Boosting, XGBoost** — How boosting trades variance for bias, and why XGBoost dominates in structured data competitions.
- **Hyperparameter tuning and cross-validation** — How to tune a model without overfitting your hyperparameters, and why random search often beats grid search.
- **Imbalanced data and threshold tuning** — How to handle data where one class is 99% of samples, and why accuracy is the wrong metric.

---

#### L1-05 · Unsupervised Learning: Structure and Similarity

Unsupervised learning answers: "What kinds of things are in this data?" and "Which things are similar?" It is less precise than supervised learning (no ground truth to measure against) but crucial when you don't have labels. Clustering (grouping similar entities) and dimensionality reduction (finding the real patterns in high-dimensional noise) are the two pillars. In 2026, most of this work is done by: K-means for fast partitioning, hierarchical clustering for dendrograms, UMAP/t-SNE for visualization, and foundation models for semantic similarity. The hard part is not the algorithm—it is evaluating whether your clusters mean anything (silhouette score? stability across runs? business interpretation?).

**Level 2 candidates:**
- **Distance metrics and similarity** — How Euclidean, cosine, and Jaccard distances behave differently, and when to use each.
- **K-means clustering and initialization** — Why K-means is fragile to initialization, how to choose K, and when it breaks down.
- **Hierarchical clustering and dendrograms** — How agglomerative clustering reveals structure at multiple scales, and when you'd rather have a dendrogram than a partition.
- **Dimensionality reduction: PCA, UMAP, t-SNE** — What PCA preserves (global structure, variance), what UMAP preserves (local and global structure), and why t-SNE is good for visualization but not much else.
- **Evaluation without labels** — How silhouette score, Davies-Bouldin index, and domain interpretation all tell different stories about cluster quality.
- **Semantic embeddings and vector similarity** — How foundation models encode meaning into vector space, and why cosine similarity now does clustering you'd have labored over in 2023.

---

#### L1-06 · Causal Inference: From Correlation to Action

This is what separates analytics from data science. An analyst can tell you that sales are correlated with temperature. A data scientist can tell you temperature is not moving sales—both are driven by the season, and an experiment is the only way to know if air conditioning affects revenue. Causal inference is the box of tools you reach for when you cannot run an experiment (ethical, expensive, slow) but need to separate signal from confounding. It has moved from academic theory (2023) to practical methods (2026). Propensity score matching, doubly robust estimation, and synthetic controls are now used in production. This topic is about how to think causally even when you're stuck with observational data.

**Level 2 candidates:**
- **Causal graphs and confounding** — How a DAG (directed acyclic graph) maps confounders and mediators, and why you can't control for everything.
- **Randomized experiments and RCTs** — How to design experiments that prove causation, and what makes a real A/B test rigorous.
- **Propensity score methods** — How to construct a "fake experiment" from observational data by matching units that are similar except for treatment.
- **Synthetic controls and difference-in-differences** — How to estimate the effect of a policy or event when you can't randomize.
- **Instrumental variables** — When you can use an exogenous instrument to uncover causation, and why the exclusion restriction is so hard to defend.
- **Causal interpretability in models** — How SHAP and other tools can sometimes tell you *why* a model predicts, but when they're just correlation with better marketing.

---

### Data & Models: Production Systems

These topics are about building systems that run, not notebooks that you run once.

#### L1-07 · Feature Stores and Data Pipelines

A feature is a computed value—population of a neighborhood, days since last purchase, average rating over the last 30 days. In 2023, you computed features in your notebook just before training. In 2026, features live in a feature store—a system that computes them once, stores them, and serves them to both training and inference pipelines. This is not academic. It eliminates data leakage (you compute the same feature the same way at both times), speeds up experimentation (features are precomputed), and makes models reproducible. Building a feature pipeline is now core data science work.

**Level 2 candidates:**
- **ETL vs. ELT and idempotency** — Why ELT (extract, load, transform in the warehouse) is now preferred, and why your pipeline must be safe to run twice.
- **Incremental computation and slowly changing dimensions** — How to update features daily without recomputing history, and how to handle data that changes but you need history of.
- **Data quality monitoring** — How to set alerts when a data source goes stale or skews unexpectedly (and why this breaks more models than buggy algorithms).
- **Feature versioning** — Why you need to track that "days since purchase" changed definition on March 15, and how that breaks reproducibility.
- **Data lineage and governance** — How to answer "where did this number come from?" in production, and what breaks if data gets deleted or redefined upstream.

---

#### L1-08 · Model Evaluation and Monitoring

A model that works in a notebook is not a model that works. In production, data distribution shifts, user behavior changes, and bugs hide. Model evaluation in 2026 means: does this model make the decision better than the old one? By how much? At what cost? And once it's live, does it stay accurate? Monitoring is not optional—it's the difference between a model that creates value and one that slowly poisons decisions. Learn to think in terms of business metrics (revenue, conversion, user retention) not model metrics (AUC, RMSE).

**Level 2 candidates:**
- **Offline evaluation and metrics** — When accuracy, precision, recall, AUC, and RMSE each tell you something different, and which one matters for your decision.
- **Offline-online gaps** — Why a model that validates perfectly still fails in production (data drift, feedback loops, user behavior change).
- **A/B testing with models** — How to run an online experiment to prove a model improves the decision vs. the status quo, and why statistical power matters.
- **Production monitoring and alerting** — How to detect data drift, prediction drift, and concept drift before they tank your model's utility.
- **Retraining strategies** — When to retrain (on schedule? on drift? continuously?), and when retraining makes things worse.
- **Model cards and documentation** — Why you need to document a model's intended use, limitations, and failure modes for the next person.

---

#### L1-09 · Machine Learning Infrastructure

In 2023, ML infrastructure was a specialty. In 2026, it is part of data science. You do not need to be a MLOps engineer, but you need to know what a serving system needs to do (low latency, handle batch and online, version models), what a training system needs (reproducibility, experiment tracking, resource management), and what goes wrong if you build a house on sand (a model that depends on a feature that disappears; a pipeline that expects data in a format that changes). This is where most real-world models fail, not in the algorithm.

**Level 2 candidates:**
- **Containerization and versioning** — Why Docker/OCI containers matter (reproducibility across environments), and why you need to version both code and data snapshots.
- **Experiment tracking and hyperparameter logging** — How to track which experiments you've run, what you tried, and why you chose this model (useful when debugging a failed prediction 6 months later).
- **Model serving: batch vs. online** — When to score data on a schedule (batch, cheaper) and when you need real-time scoring (online, more expensive).
- **Resource allocation and scaling** — How to estimate if a model will run in 100ms on shared hardware, and when you need dedicated GPUs.
- **Dependency management** — How to avoid the situation where a new NumPy version breaks your six-month-old model.
- **Debugging production failures** — How to reproduce a bug in production (usually impossible without good logging and data versioning).

---

### Context: The Domain You're Working In

The hardest part of data science is not the math—it is understanding the business, the users, and the constraints.

#### L1-10 · Business Acumen and Problem Decomposition

The best data scientist in 2026 is not the one with the most advanced algorithm. It is the one who asks: What decision are we actually trying to make? What would change if we get this right? What would it cost if we get it wrong? Who decides? And when will we know if we succeeded? These are not data questions—they are business questions. But answering them shapes everything: what data you need, how you measure success, what accuracy is "good enough." You need enough domain knowledge to build intuition about what is possible and what is fantasy.

**Level 2 candidates:**
- **Translating questions to metrics** — How to take a vague business goal and convert it to a clear, measurable, trackable number.
- **Cost-benefit and ROI** — How to estimate the value of a model improvement (if we increase precision by 2%, what does that earn?).
- **Stakeholder management** — How to talk to executives, product managers, and engineers so they understand what your model can and cannot do.
- **Prioritization under constraints** — How to choose which of three possible models to build when you only have time for one.
- **Ethical considerations and bias** — Why a technically perfect model can harm users, and how to spot and mitigate unfairness in data and decisions.

---

#### L1-11 · Domain-Specific Deep Dives

Different domains have their own data structures, problems, and best practices. Recommendation systems (Netflix, Spotify) are different from fraud detection (banking) different from supply chain (logistics). You don't need to be expert in all of them, but you need to know what to read when you move into a new domain.

**Level 2 candidates:**
- **Recommendation systems** — How to move from "what users like" to "what to show them next," why collaborative filtering works, and why context matters.
- **Fraud detection and anomaly detection** — Why fraud is rare (imbalanced), why accuracy is useless, and how to stay ahead of adversaries adapting to your model.
- **Time series and forecasting** — How the structure of time-ordered data changes your approach, and why methods designed for cross-sectional data fail.
- **NLP and text data** — How language has been transformed by embeddings and transformers, and why pre-trained models are now the foundation.
- **Computer vision and images** — How convolutional structure mirrors visual perception, and why transfer learning dominates.

---

## Sequencing Note

**Start here:**

1. **L1-02 (SQL)** — If you've forgotten SQL, this is your floor. Nothing else moves until you're fluent. Spend a week on window functions and CTEs.
2. **L1-01 (Python)** — Parallelize with SQL. Spend a week learning Polars and profiling.
3. **L1-03 (Statistics)** — Not for theory, but for intuition. Understand power analysis and confidence intervals. You need this before you trust any evaluation you do.

**Then move to problems:**

4. **L1-04 (Supervised Learning)** — The core tool. You likely remember most of this. Refresh on train-test splits, cross-validation, and why feature engineering is less of a bottleneck now. Skip deep learning for now unless your data is images, audio, or text.
5. **L1-06 (Causal Inference)** — Read this after supervised learning. Most of the questions you'll get asked ("would this increase revenue?") are causal, not predictive. Understanding the gap changes how you set up your problem.
6. **L1-05 (Unsupervised Learning)** — Important but lower priority. You'll use it when you need to group customers, detect anomalies, or visualize high-dimensional data. Come back when you hit it.

**Then build systems:**

7. **L1-07 (Pipelines)** — Once you have a model that works, you need to put it in production. This is usually where real projects live.
8. **L1-08 (Monitoring)** — Do this alongside L1-07. A model that silently degrades is worse than no model.
9. **L1-09 (Infrastructure)** — You don't need to be a DevOps expert, but you need to know what your engineering team needs.

**Always doing:**

10. **L1-10 (Business Acumen)** — Do not put this off. The 2026 data scientist who can translate a business problem into a model is rare. This is where seniority compounds.
11. **L1-11 (Domain Deep Dives)** — Pick one domain that matches your industry. Recommendation systems if you're in tech. Fraud detection if you're in finance. Supply chain if you're in logistics. Do the deep dive work after you've refreshed on L1-04 and L1-06.

---

**Highest-leverage path for re-entry:** SQL → Python → Problem formulation (L1-10) → Supervised Learning → Causal Inference → Pipelines → Monitoring. You do not need to sit through the old curriculum again. You need direction and depth in the parts where 2026 is different from 2023.