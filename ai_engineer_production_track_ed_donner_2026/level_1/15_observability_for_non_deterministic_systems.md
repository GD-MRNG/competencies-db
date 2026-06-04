## Metadata
- **Date:** 05-06-2026
- **Source:** 15_observability_for_non_deterministic_systems.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-15 · Observability for Non-Deterministic Systems

The instinct most engineers bring to observability is forensic: something broke, go read the logs, find the line that says ERROR, fix it. That instinct works for deterministic systems, where a request either succeeds or fails for a reason the code can articulate. It breaks down completely for agents. An agent doesn't fail with a stack trace; it fails by choosing the wrong tool, looping on a bad assumption, or confidently returning a wrong answer that no log line will ever flag as an error. The system did exactly what it was told to do. The problem is what it decided to do.

This is the gap that observability for agentic systems has to close. You are no longer monitoring a pipeline; you are monitoring a decision-maker. The unit of observation is not "did the request return 200" but "did the reasoning process make sense." That requires capturing not just inputs and outputs, but the full chain of intermediate steps — every prompt sent, every tool invoked, every model response, every branch the agent considered. A traditional log line tells you what happened. A trace tells you why.

The mental shift is to stop thinking of an agent run as a function call and start thinking of it as a tree. The root is the user's request. Each node is an LLM call or a tool invocation. The branches are the decisions the agent made — call this API, then reason about the result, then call another, then summarize. When something goes wrong, the failure mode is almost always structural: the tree is too deep (the agent looped), the wrong branch was taken (it picked the wrong tool), or a node returned something subtly off that contaminated everything downstream. You cannot diagnose any of that by tailing logs. You need to see the shape of the run.

This is why a category of specialized tooling has emerged — platforms built specifically to capture, store, and visualize agent traces. Langfuse and Smithery are two names worth knowing, though the space is moving quickly enough that you should check what's current rather than assume any tool is canonical. The field shifts: new platforms launch, existing ones get acquired or pivot, and the open-source landscape changes month to month. What stays constant is the shape of the problem these tools solve: they let you replay an agent's reasoning step by step, see the latency and cost of each call, and annotate runs as good or bad so you can build evals from real production behavior.

The failure modes you'll be hunting are specific to non-deterministic systems and worth naming directly. Infinite loops happen when an agent keeps calling the same tool with slight variations, convinced the next call will give it what it needs — your trace will show twenty consecutive identical-looking nodes. Hallucination shows up when the agent confidently produces output unsupported by any tool result; the trace reveals that it never actually looked anything up before answering. Wrong tool selection looks like a clean execution that produces a useless answer; the trace shows the agent picked the search tool when it should have picked the calculator. None of these are exceptions. None of them will trigger an alert based on HTTP status codes. They are only visible if you can see the agent's thought process laid out.

The operational consequence is that drift detection becomes a first-class concern. Your agent works on Monday. On Tuesday, the model provider silently updates the underlying model, or your prompts get slightly modified, or a tool's response schema changes. The agent still returns 200s. Costs creep up because it's now taking eight tool calls to do what used to take three. Accuracy on your evals drops two percentage points. Without traces and the metrics built on top of them, you learn about this from a customer complaint three weeks later. With traces, you have dashboards showing average steps per run, average cost per request, and tool selection distributions — and you see the change the day it happens.

There is one more dimension that traditional observability didn't have to worry about as acutely: privacy. Traces capture everything, which means they capture the user's actual prompts, the actual data the agent retrieved, and the actual responses it generated. If your users are entering PII, medical information, or proprietary business data, your trace store is now a sensitive data store. This has implications for retention policies, access controls, and what you're allowed to ship to a third-party observability vendor. It is not a problem you can defer; the right time to think about it is when you choose your tracing stack, not after a compliance audit.

The skill this topic builds is the ability to debug systems that don't fail loudly. Production AI engineering is, more than anything else, the discipline of seeing what your system is actually doing — not what you assumed it would do when you wrote the prompt. Traces are how you see. Build them in from day one. The cost of adding observability later, after your agent is already in production and behaving strangely, is an order of magnitude higher than the cost of wiring it up correctly the first time. The agents that survive contact with real users are the ones whose builders can replay any run and explain what happened.

## Level 2 candidates

**Trace capture and visualization** — Covers how to instrument every LLM call, tool invocation, and intermediate decision so the full reasoning tree is recoverable, and how to visualize that tree as a timeline or hierarchy. Worth a deep dive because the instrumentation patterns (spans, parent-child relationships, metadata schemas) determine what questions you can later ask of your data — get this wrong and you'll have lots of traces but no insight.

**Annotation and human feedback** — Covers the workflow of marking individual traces as good or bad, attaching reviewer comments, and turning that labeled corpus into evals or fine-tuning data. Worth deeper treatment because the feedback loop from production traces back into evaluation is the single most important mechanism for improving agent quality over time, and most teams build it badly or not at all.

**Cost and latency attribution** — Covers how to break down where time and tokens are actually being spent across an agent run — which model call, which tool, which retry. Worth its own treatment because cost optimization in agentic systems is almost always a matter of finding the two or three steps doing 80% of the spending, and you cannot find them without attribution.

**Drift detection** — Covers how to detect when agent behavior shifts over time — accuracy degrading, costs climbing, latency creeping, tool selection patterns changing. Worth a dedicated piece because the techniques (baselines, statistical tests, anomaly alerts on aggregate metrics) are non-obvious and the alternative — finding out from users — is unacceptable.

**PII and privacy in traces** — Covers what data traces inadvertently capture, how to redact or hash sensitive fields before they hit your trace store, and how retention and access policies need to be designed for compliance. Worth deeper coverage because it intersects with security, legal, and vendor selection decisions that are difficult and expensive to reverse once made.

---