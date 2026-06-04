## Metadata
- **Date:** 05-06-2026
- **Source:** 11_testing_and_validation_in_ai_systems.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-11 · Testing and Validation in AI Systems

The instinct most engineers bring to testing an AI system is the instinct they built over years of writing unit tests for deterministic code. You write a function, you assert that `add(2, 2) == 4`, and if the assertion holds, the function is correct. That instinct is not just unhelpful for AI systems — it is actively misleading. The function under test no longer returns the same value twice. The same prompt, the same model, the same temperature setting, and you can still get two different answers. Your entire testing vocabulary — assertions, coverage, pass/fail — was built on an assumption that no longer holds.

This is the first thing to internalise: testing an AI system is not about proving correctness, because correctness in the strict sense is unavailable to you. It is about characterising behaviour. You are trying to answer a different question than the one unit tests answer. Instead of "does this function return the right value," you are asking "across a representative population of inputs, does this system produce outputs that satisfy my criteria often enough?" That word "often enough" is doing a lot of work, and it is where the discipline lives.

The mental model that replaces unit testing is the eval. An eval is a test set plus a grading function plus a target score. The test set is a curated collection of inputs that represents the situations your system will encounter — not exhaustively, but representatively. The grading function decides whether an output is acceptable, which is harder than it sounds because acceptability often involves judgement (is this summary faithful? is this answer helpful?). The target score is the bar you have decided your system must clear — say, 92% of outputs rated acceptable by an LLM-as-judge or a human reviewer. Evals are the closest thing AI engineering has to a passing test suite, and you should think of them as the unit of trust in your system.

Layered on top of evals is regression testing, which is structurally the same idea but aimed at a different question: when something changes, did anything that used to work stop working? In a deterministic system, regression testing is mostly automatic — you rerun the test suite. In an AI system, the things that change are sneakier. A model provider rolls out a new minor version. A prompt gets tweaked to fix one edge case. A temperature parameter gets nudged. Any of these can quietly tank accuracy on inputs you were not looking at. Regression evals are what catch this. You run the same test set against the new configuration and compare scores. If accuracy on your benchmark drops from 94% to 89%, you know something changed, even if you cannot yet say what.

Then there is the adversarial dimension, which has no real analogue in traditional testing. Your system will be probed by users who want to make it misbehave — jailbreaks that try to override the system prompt, prompt injections smuggled in through retrieved documents or tool outputs, inputs crafted to extract data the model should not reveal. Edge-case testing in an AI system means deliberately constructing these inputs and verifying that the system refuses, sanitises, or otherwise handles them safely. This is closer to security testing than to functional testing, and it requires you to think like an attacker, not like a user.

The metric you are tracking through all of this is accuracy on a benchmark, not code coverage. Coverage tells you which lines of code your tests touched, which is almost meaningless when the interesting behaviour lives inside a model you did not write. What matters is whether the system, treated as a black box, produces outputs that meet your bar on inputs that matter. This shift is uncomfortable for engineers who have spent years optimising for green checkmarks, because benchmarks do not give you green checkmarks. They give you numbers, and you have to decide what those numbers mean.

The practical consequence is that your test infrastructure for an AI system looks different. You still have unit tests for the deterministic parts — your parsing logic, your retry wrapper, your token counter. Those parts are still deterministic and still deserve traditional tests. But around the model calls, you build an eval harness: a way to run a test set, score the outputs, store the results, and compare runs over time. You build it once and you run it constantly — before merging prompt changes, before swapping models, before rolling out to all users. You pair it with canary deployments so that even when your evals say a change is good, you only expose a small fraction of real users to it first and watch the live metrics before committing.

The skill this topic builds is the ability to make confident changes to a non-deterministic system. Without evals, every prompt tweak is a leap of faith and every model upgrade is Russian roulette. With evals, you have a feedback loop. You can say, with numbers behind you, that the new prompt is better than the old one, or that the cheaper model is good enough for this use case, or that yesterday's deploy quietly regressed on a class of inputs that matters. That confidence is what separates engineers who ship AI systems from engineers who ship demos.

## Level 2 candidates

**Deterministic vs. Probabilistic Testing** — Covers where traditional unit tests still belong in an AI system (parsing, retries, token counting, schema validation) versus where evals take over. Worth a deeper treatment because new engineers tend to either over-apply unit tests to model outputs or abandon unit testing entirely; the line between them is subtle and worth drawing carefully.

**Evaluation Benchmarks and Metrics** — Covers the design of test sets, the choice of grading functions (LLM-as-judge, human review, rule-based), and how to define "correct" for fuzzy outputs like summaries or answers. This is the deepest topic under L1-11 and the one most readers will get wrong on their first attempt; it deserves a full Level 2 with concrete patterns and failure modes.

**Regression Testing and Change Detection** — Covers how to detect that a prompt edit, model swap, or parameter change has silently degraded accuracy on inputs you were not looking at. Worth going deeper on the tooling (eval-on-PR, score deltas, dashboards) and on the discipline of treating prompts and model configs as versioned artefacts.

**Adversarial Testing and Security** — Covers jailbreaks, prompt injection through tool outputs and retrieved content, and the construction of red-team test sets. Worth its own deep dive because the threat model evolves quickly and the defences are not obvious — and this overlaps significantly with L1-16 (the lethal trifecta), so the two should be designed to reinforce each other.

**A/B Testing and Canary Deployments** — Covers the operational side of validating changes against real traffic: exposing a small percentage of users to the new version, comparing live metrics (accuracy, cost, latency, user satisfaction), and rolling forward or back based on signal. Worth a Level 2 because the statistical and infrastructure considerations (sample size, segmentation, rollback automation) are non-trivial and easy to botch.

---