## Metadata
- **Date:** 05-06-2026
- **Source:** 03_separation_of_concerns_across_layers.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-03 · Separation of Concerns Across Layers

Most unreliable agent setups are not unreliable because the model is bad. They are unreliable because someone put enforcement in a prompt, or standards in a per-run instruction, or reusable logic in a workflow YAML file. The model is doing exactly what you asked. You asked it to do too many different kinds of things in the same place.

Separation of concerns is older than the systems you are trying to apply it to. Larry Constantine articulated it in the 1960s as a structural property of well-designed software: each component should have a single, well-defined responsibility, and the boundaries between components should be drawn so that a change in one place does not ripple unpredictably through the rest. The principle survived every paradigm shift since — structured programming, object orientation, microservices, serverless — because it is not really about any of those paradigms. It is about the human cost of reasoning about a system where responsibilities overlap. When two components are both partly responsible for the same thing, neither of them is fully responsible for it, and that ambiguity is where bugs live.

The reason this principle becomes acute in agent pipelines is that you now have four distinct kinds of things that can carry instructions, and they look superficially similar. There is the configuration file, which encodes standards — the rules and conventions the system commits to. There is the library, which encodes reusable logic — the patterns and skills you want to invoke repeatedly without restating them. There is the runtime hook, which encodes enforcement — the deterministic check that runs whether the agent cooperates or not. And there is the generation step itself, which produces output — the actual creative or analytic work you are delegating. In a human-operated workflow these layers are often blurred because the human silently does the integration work. An agent does not. An agent treats whatever you put in front of it as a flat instruction surface.

The failure mode is predictable. You decide your team's Python code should use a particular formatter. You write that into the prompt: "always format with X." It works for a while. Then a new task comes along, the prompt grows, the formatting instruction gets buried, the agent forgets, and suddenly half your PRs are inconsistently formatted. You did not have a standards problem; you had a layering problem. The standard belonged in a configuration file that the formatter reads, and the formatter belonged in a pre-commit hook. The agent should never have been asked to remember it, because remembering it was not the agent's job.

The same failure mode shows up in the other direction. Teams put reusable logic — a multi-step refactoring pattern, a test scaffolding template — into a runtime hook, because hooks are where things "actually run." Now the logic is invisible to the agent, cannot be invoked on demand, and has to be duplicated the next time someone wants the same pattern in a different context. Or teams put enforcement into a prompt — "do not commit secrets" — and treat that as a control. It is not a control. It is a suggestion that happens to be in the right grammatical mood. A control is a thing that returns a non-zero exit code.

The vocabulary that makes this concrete is cohesion and coupling. A component is cohesive when its internals are all about the same thing — a formatter formats, a linter lints, a test runner runs tests. It is loosely coupled when it depends on as little of the rest of the system as possible. When you mix layers, you reduce cohesion (the prompt is now about both task instructions and enforcement and standards) and increase coupling (changing your formatting convention now requires editing the prompt, the docs, and three workflow files). The system becomes harder to change in exactly the way that matters: incrementally, without breaking adjacent things.

The practical heuristic is to ask, for every instruction you are about to write, which layer it belongs in. If it is a rule the team has committed to, it goes in configuration — version-controlled, declarative, read by tools. If it is a pattern you will want to invoke more than once, it goes in a library or skill artefact — named, versioned, callable by reference. If it must be true regardless of whether the agent cooperates, it goes in a hook — deterministic, blocking, auditable. Only what is genuinely about the specific task at hand belongs in the generation step. When you find yourself writing the same instruction in two layers, one of them is wrong.

What this builds, over time, is the ability to look at a misbehaving pipeline and diagnose the layer violation rather than the surface symptom. The agent that "keeps ignoring our style guide" is almost never an agent problem; it is a configuration that was never written, or a hook that was never installed, or a standard that lives only in a Slack message. Once you can see the layers, the fixes stop being prompt-engineering exercises and start being architectural ones. That shift — from "how do I phrase this better" to "where does this instruction belong" — is the whole game.

## Level 2 candidates

**Cohesion and coupling** — The vocabulary for measuring how related a component's internals are and how dependent it is on its neighbours. Worth a deep dive because it gives you the diagnostic language for evaluating whether a proposed decomposition is sound before you commit to it, rather than discovering the mistake after the system is in production.

**Configuration as code** — What becomes possible when system behaviour is declared in version-controlled files rather than set through UI or implicit convention. Worth deeper treatment because the reproducibility and reviewability properties it unlocks are the mechanism by which standards stop drifting, and the failure modes when you violate it (snowflake environments, undocumented overrides) are subtle and expensive.

**The single responsibility principle** — Why a component that does one thing fails more predictably and is easier to replace than one that does several. Worth its own treatment in the context of agent roles specifically, because the temptation to build "generalist" agents that handle multiple stages of a pipeline is strong and the consequences are not obvious until the agent starts behaving inconsistently.

**Interface boundaries** — How explicit contracts between components let you swap implementations without changing callers. Worth deeper exploration because tool interfaces are the layer at which agent systems most often leak — an agent that knows too much about what a tool does internally becomes brittle when the tool changes.

**Policy vs. mechanism** — The Unix design principle that a tool should provide the mechanism and the caller should specify the policy. Worth a separate treatment because violating it in agent pipelines (hardcoding decisions into the tool layer that should be configurable per workflow) is one of the most common ways reusable infrastructure ends up not being reusable.

---