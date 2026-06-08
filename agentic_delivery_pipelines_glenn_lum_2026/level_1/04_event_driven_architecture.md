## Metadata
- **Date:** 05-06-2026
- **Source:** 04_event_driven_architecture.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-04 · Event-Driven Architecture

The instinct of most developers, when they need two things to talk to each other, is to have one call the other directly. A function invokes another function. A service hits another service's endpoint. A scheduler polls a queue. This works, and it works for a long time, which is why the limitation is rarely felt until the system has already grown around it. The limitation is that the caller has to know the callee exists, where it lives, and when to talk to it. Every new participant in the system means editing the caller. The coordination logic accumulates in the centre, and the centre is where systems get brittle.

Event-driven architecture inverts this. Instead of a component calling out to whatever needs to happen next, it emits a signal — an event — describing something that just occurred. It does not know who is listening. It does not care. Other components subscribe to the kinds of events they care about and react when one arrives. The producer's job ends at "this happened." The consumer's job begins at "this happened, so I will do that." Neither needs a reference to the other.

This separation — formalised through the 1980s and 1990s as distributed systems forced people to take it seriously — is doing more work than it appears to. It means you can add a new consumer of an event without touching the producer. You can replace a producer without touching its consumers, as long as the event shape stays compatible. You can record every event that flows through the system and replay them later to understand what happened. You can fan one event out to ten subscribers, or route different events to different handlers, without any of them being aware of the others. The coupling that would normally bind these components together has been replaced by a shared vocabulary of events.

If you have used GitHub Actions, AWS Lambda triggers, webhooks, or any modern CI/CD system, you have already used this pattern even if you did not name it. A push to a branch is an event. A pull request being opened is an event. A scheduled cron tick is an event. Workflows subscribe to the events they care about and run when triggered. Nobody writes a central scheduler that knows about every workflow. The workflows declare what they care about, and the platform routes events to them. The platform is the message bus; your workflows are the consumers.

For agent pipelines, this pattern is not a stylistic preference — it is what makes the system composable in the first place. An agent that runs in response to an event ("a PR was opened," "a comment was posted," "a test failed") can be added, removed, or replaced without rewriting the rest of the pipeline. You can have one agent that proposes code, a second that reviews it, a third that runs tests, and a fourth that posts results — and none of them needs to know the others exist. They each subscribe to the events they care about and emit their own. The pipeline emerges from their interactions rather than being centrally orchestrated. This is the only way to build a pipeline that you can extend incrementally without the integration cost growing quadratically.

The pattern also gives you observability almost for free. Because events are discrete, named, and (if you are careful) recorded, you have a natural timeline of what the system did. When something goes wrong with an autonomous agent — and it will — the question "what actually happened, in what order, in response to what trigger" is the first question you need to answer. A system built around event flows answers this question structurally. A system built around direct calls requires you to instrument it after the fact, and the instrumentation is always incomplete.

There are costs to be honest about. Event-driven systems are harder to reason about end-to-end because the control flow is not in one place — it is implicit in the subscription graph. Debugging requires you to trace events through the bus rather than stepping through a call stack. Failures are partial and asynchronous: a consumer can fail silently while the producer happily continues emitting. Events can arrive twice, out of order, or not at all, which means your consumers have to be designed for that reality (the connection to idempotency is not coincidental). And the loose coupling that makes the architecture extensible also makes it easy to build pipelines that re-trigger themselves in loops, where one agent's output becomes another agent's input becomes the first agent's input again. The freedom requires discipline.

The mental model to leave with is this: event-driven architecture is a way of trading direct knowledge for shared vocabulary. Components stop knowing about each other and start knowing about the events they produce and consume. Everything that follows — the composability, the observability, the ability to add an agent to your pipeline without rewriting it, the new failure modes you have to design against — falls out of that single shift. When you look at a CI/CD system, a serverless platform, or an agent pipeline and ask why it is structured the way it is, this is almost always the answer.

## Level 2 candidates

**Event sourcing** — Recording every state change as an immutable event rather than overwriting current state, so the system's history is reconstructible. Worth deeper treatment because the audit trail and replay capabilities it enables are disproportionately valuable for non-deterministic agents, and the design constraints it imposes (no in-place mutation, careful event versioning) are non-obvious.

**Pub/sub vs. point-to-point messaging** — The distinction between broadcasting events to all interested subscribers and routing them to a specific consumer queue. Worth a deeper look because the choice has direct implications for coupling, scaling, and what happens when a consumer is offline — and most teams pick one by accident rather than design.

**Idempotent event handling** — Designing consumers so that processing the same event twice produces the same result as processing it once. Worth its own treatment because it is the structural prerequisite for safe retries, and the patterns for achieving it (deduplication keys, conditional writes, natural idempotency) are a discipline in their own right.

**Trigger design** — The choice of what event fires a workflow, which determines blast radius, cost, and the risk of self-triggering loops. Worth deeper exploration because trigger mistakes are the most common cause of runaway agent pipelines, and the design heuristics for safe triggers (specificity, branch filtering, turn limits) are not intuitive until you have been bitten.

**Dead letter queues** — The explicit failure path for events that cannot be processed successfully. Worth a Level 2 because the question of "what happens to the events we drop on the floor" is almost always under-designed, and unattended systems without a dead letter strategy lose data silently in ways that are hard to detect after the fact.

---