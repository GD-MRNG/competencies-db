# The Building Blocks of AI Agents

If you’ve internalized the last article — The Building Blocks of AI Engineering — model-as-a-service, tool calling, structured outputs — you already have everything you need for a single reliable model call. This one asks a different question: what happens when the model stops being an oracle you query and starts being the thing that decides what happens next?

That's the entire shift from a chatbot to an agent. It sounds subtle. It isn't — it changes your failure modes, your testing strategy, and your costs all at once.

The Core Pattern: Thought, Action, Observation

Underneath every agent, however fancy the framework, is one simple loop: the model thinks (looks at the goal and what it knows so far), takes an action (chooses a tool to call), and you feed back the observation (what actually happened), then repeat. Structurally it's just a while loop. What makes it agentic — instead of just a script — is that the model, not your code, is the one deciding what the next step should be.

This is worth building once by hand, in plain code, before reaching for any framework. It's the single most durable skill in this space, and understanding it from first principles is what lets you debug an agent when a framework's abstractions start hiding what's actually going wrong. A few things matter enormously in this loop and get skipped by people in a hurry: a clear system message that tells the model what tools exist and what "done" looks like, and — critically — an explicit stopping condition. Without one, agents don't gracefully finish; they loop, burning tokens on nothing, until you notice the bill.

Not Everything Needs an Agent

Here's a distinction worth making before you build anything: not every task benefits from letting the model decide the next step. Some tasks are predictable sequences — step A always leads to step B, always leads to step C — and those are workflows: cheap, fast, and testable, because you already know the path. Others are genuinely open-ended, where you don't know the sequence in advance and need the system to figure it out as it goes — those are where an agent loopearns its cost and its risk.

Treating this as an engineering decision, not a framework preference, will save you real money and real debugging time. A workflow has bounded cost and predictable latency. An agent is flexible, but unpredictable — it can drift, loop, or take a wildly inefficient path to the right answer. The right question, every time someone suggests "let's make this an agent," is: does this specific task actually require the model to choose its own path, or do we already know the sequence and just want it done?

Not All Models Reason Equally, and That's a Cost Decision

A frontier model can hold a complex goal in mind, weigh several tools, and recover gracefully when something goes wrong. A small, cheap model often can't — it hallucinates tool calls, misreads a schema, or gets stuck. For agentic work specifically, "cheap" frequently means "broken" in a way that doesn't show up in simpler, single-shot tasks. This is a different constraint than picking a model for a one-off completion, and it's worth testing explicitly rather than assuming your usual model choice still holds.

A pattern worth knowing here: you don't have to use one model for everything. A common and effective setup uses a capable, expensive model for planning — the part that actually needs judgment — and a cheaper, narrower model for the repetitive execution work underneath it. Distributing reasoning this way is often both cheaper and more reliable than either a single expensive generalist or a single cheap one.

Speed: Doing Things at the Same Time

Real agents often need to make several slow calls — hitting an API, querying a database, calling another model — and if you wait for each one to finish before starting the next, your system crawls. Running independent calls in parallelinstead of one after another is often the single biggest latency win available to you, dropping a chain of "call, wait, call, wait, call, wait" down to "call all three at once, gather results, continue." The complexity it introduces — what happens if one of three parallel calls fails while the other two succeed — is a real design question, not an edge case to handle later.

When One Agent Isn't Enough

A single agent is limited by the model's own breadth. Past a certain complexity, it's often more reliable to build a small team of specialized agents instead: one plans using a capable model, another executes narrow calculations, a third checks the work — each doing one job well rather than one generalist doing everything adequately. This requires deliberate design around how they talk to each other (message passing, shared state) and who's in charge of what happens next (a hierarchical "manager" agent, or a flatter peer-to-peer setup). It also raises a question you don't face with a single agent: what happens when two agents disagree? Voting, weighting one over another, or escalating to a human are all legitimate answers — the wrong answer is not deciding in advance.

Teaching Agents to Catch Their Own Mistakes

Agents make mistakes — the wrong tool, a misread result, a dead-end path. One of the more reliable fixes is structural rather than hoping for a better prompt: add an evaluator that checks the output against explicit criteria, and an optimizer that revises it if the evaluator isn't satisfied, looping until it's approved or you hit a cost ceiling. This costs latency and tokens, which is exactly why it's worth reserving for tasks where being wrong is expensive, rather than applying it everywhere by default.

Frameworks: Useful, But Not First

Tools like LangChain or CrewAI genuinely save time once you understand what they're automating — memory handling, retries, multi-agent coordination. The trap is reaching for them before you've built the raw loop yourself even once: frameworks are easy to write against and much harder to debug when something breaks, because the failure is often happening inside abstraction you don't control. The durable approach is to master the loop in plain code first, then adopt a framework pragmatically once you can tell, from experience, exactly what it's doing for you.

Making Tool Calls Actually Reliable

The model doesn't execute anything — it generates text that looks like a function call, and your code has to parse and run it. For that to work consistently, the model has to reliably produce a valid, well-formed request every time, which is where clear schemas (defining exactly what a tool expects and returns) and structured output enforcement earn their keep. Without this, "the agent calls a tool" quietly becomes "the agent generates text, my code fails to parse it half the time, and the loop breaks in ways that are miserable to debug."

Worth knowing here: the Model Context Protocol (MCP) is a standardized way for agents to discover and use tools without custom integration code for each one — think of it as a common plug shape instead of a different adapter for every tool you want to connect. It's increasingly the default way new tools get exposed to agents, and it's worth knowing about even if you're not building it yourself yet.

There's also a design choice around granularity: a coarse tool ("fetch any URL") gives the agent freedom to be creative but also freedom to make bigger mistakes. A fine-grained tool ("click this specific button") is safer but more restrictive. Where you land depends on how much you trust the model's judgment on this specific task, and how expensive a mistake would actually be.

Structure Where You Can, Freedom Where You Need It

Pure agent loops are flexible but unpredictable. Pure hard-coded workflows are predictable but rigid. A useful middle ground is a graph: you define the overall shape of the process (fetch → analyze → decide → act) as fixed structure, and let an agent handle the genuinely ambiguous decisions within specific steps. You get the auditability of a known shape with the flexibility of dynamic reasoning exactly where it's needed, instead of everywhere at once.

Knowing When to Ask a Human

Not every decision belongs to the agent. For anything genuinely high-stakes — a financial transfer, a deletion, a policy call — the system should pause and escalate to a person rather than act autonomously. Designing this well means being explicit about three things in advance: what conditions trigger a human review, how the agent's reasoning gets shown to that person (not just its final answer, but why), and how long the system is allowed to wait for a response before something else has to happen. This isn't a fallback bolted on after the fact — it's a design decision that needs to exist before the system goes anywhere near production.

Seeing What the Agent Actually Did

Agentic systems fail in ways that are genuinely hard to trace: fifty steps, thirty tool calls, and a wrong final answer somewhere in the middle. Without deliberate tracing — recording every thought, every action, every observation — debugging a failure means guessing. With it, you can find not just "what went wrong this time" but systemic patterns, like "this agent consistently fails whenever the question involves dates." This is one of the least glamorous parts of building agents and one of the most directly tied to whether you'll be able to trust the system in production.

Prompting Changes When the Model Is Looping

A system message matters more in an agent than in a one-shot prompt, because the agent will act on it dozens of times in a row, and small ambiguities compound with every iteration instead of only mattering once. The things worth being explicit about: what "done" actually means, what each tool is for and what it returns, what the agent is explicitly not allowed to do, and — importantly — what it should do if it notices it's stuck repeating itself, rather than silently looping until someone notices the bill.

The Throughline

Everything here amplifies what was already true in the last article, rather than replacing it. Agents don't remove the need for reliable tool calling and structured outputs — they depend on it even more, because a single bad tool call in a one-shot system is a bug, and the same bad tool call inside a fifty-step agent loop can compound into something much harder to unwind. The path that actually works is the boring one: get the single-call foundations solid, build the loop by hand once, and only then start layering in speed, teams, and autonomy — adding each piece because a real constraint demanded it, not because it was available.

Getting the loop right is still only half the job. Everything in this article has been about a system that works when you run it — on your machine, with your test inputs, while you're watching it. Whether it keeps working for a stranger, at scale, unattended, while you're asleep is a different set of problems entirely: deployment, monitoring, cost control, and the failure modes that only show up under real, unpredictable load.

That’s where the next piece in this series picks up: The Building Blocks of AI Production.


Portfolio Note: I publish these articles as part of my professional portfolio. They reflect how I approach technical problems, structure solutions, and communicate complex ideas clearly.