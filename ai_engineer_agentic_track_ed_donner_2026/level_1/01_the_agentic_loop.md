## Metadata
- **Date:** 05-06-2026
- **Source:** 01_the_agentic_loop.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-01 · The Agentic Loop (Thought-Action-Observation)

The moment you stop writing the next step and let the model write it for you, you've crossed a threshold that most developers don't notice until something breaks. A chatbot is a function: you send a message, it returns a message, and you decide what to do with it. An agent is a loop: you give it a goal, and it decides — repeatedly, until it's done — what to do next. The code that separates these two worlds is almost embarrassingly small. A `while` loop, a list that grows, and a conditional that checks whether the model asked to call a tool. That's it. The profundity isn't in the code; it's in who holds the steering wheel.

In the agentic loop, the model is no longer the oracle you consult — it's the dispatcher that consults you. Each iteration follows the same three beats. The model evaluates the current state of the world (the goal, the conversation so far, the tools available) and produces a thought about what should happen next. It emits an action, typically a structured request to call one of your tools with specific arguments. Your code executes that tool, captures the result, appends it to the message history, and hands control back to the model. The model reads the new state, including the result of its own previous action, and decides what to do next. Sometimes that's another tool call. Sometimes it's a final answer, which is your cue to exit the loop.

The thought step is where most of your engineering work shows up indirectly. You don't see the thinking — you see its consequences in which tool gets called and with what arguments. This is why the system message and the tool schemas you provide matter so much: they are the entire environment the model uses to plan. A vague system message produces a meandering agent. A bloated tool list produces an agent that picks the wrong instrument. Tool descriptions that read like API documentation produce agents that confidently invoke tools they don't understand. Everything you want the agent to be good at, you have to set up before the loop ever runs.

The action step is where a common misconception lives. The model doesn't actually call your function. It generates text — text that happens to look like a function call, formatted as JSON, conforming (you hope) to the schema you specified. Your code is what calls the function. This distinction sounds pedantic until you remember that the model can generate malformed JSON, hallucinate tool names that don't exist, or supply arguments of the wrong type. Treating the model's output as a suggestion you parse and validate, rather than a function invocation you trust, is the difference between a loop that recovers gracefully and one that crashes on its third iteration.

The observation step is the cheapest to write and the easiest to underestimate. You run the tool, you take the result, you stick it back into the message history with a label that tells the model what it's looking at. This is how the agent perceives the world. If the tool returns a 4MB blob of HTML, that's what gets stuffed into the next prompt. If it returns a cryptic error message, the agent has to interpret it. The observation is the agent's only feedback channel, and the quality of what you put back into context determines whether the next thought is a smart adjustment or a confused repetition of the last action.

Then there's the question of when to stop. The loop terminates naturally when the model decides not to call any more tools and instead produces a final answer. But "naturally" is doing a lot of work in that sentence. Models get stuck. They call the same tool with the same arguments three times in a row, hoping for a different result. They convince themselves they need one more piece of information before they can answer, and then one more, and then one more. Without explicit guardrails — a maximum iteration count, a token budget, a watchdog that detects repetition — you will, eventually and inevitably, ship an agent that burns through your API credits overnight chasing a goal it was never going to reach. Stop conditions aren't a polish item. They're part of the loop's definition.

The reason this entire pattern is worth mastering in raw Python before you reach for a framework is that frameworks hide the loop. They give you nice abstractions — `agent.run(goal)` — and when those abstractions work, they work beautifully. When they don't, you're debugging someone else's mental model of how the loop should behave, on top of debugging your own agent. If you've written the loop yourself, you know exactly where to put the print statement. You know what the message history looks like at iteration 7. You know why the model picked that tool. Frameworks become a productivity multiplier the moment you understand what they're multiplying. Until then, they're a layer of mystery sitting on top of a fundamentally simple pattern.

What you're really building, when you build an agentic loop, is the smallest possible system in which the model is the decision-maker and your code is the execution substrate. Every more sophisticated pattern in this track — multi-agent teams, evaluator-optimizer cycles, graph-based workflows, MCP-mediated tool ecosystems — is a variation or extension of this one. Get the loop right, and the rest is composition. Get it wrong, and no amount of orchestration on top will save you.

## Level 2 candidates

**The Thought Step: Planning and Tool Selection** — How the model evaluates the current state and chooses which tool to invoke, and how the system message and schemas shape that choice. Worth a deep dive because the quality of tool selection is the single biggest determinant of whether an agent feels intelligent or feels broken, and the levers you have to influence it are subtle.

**The Action Step: Tool Calling and JSON Generation** — Why the model isn't really calling your function — it's generating text that looks like a call — and what that means for validation, parsing, and error recovery. Deserves its own treatment because the failure modes here (malformed JSON, hallucinated tool names, wrong argument types) are where prototypes die in production.

**The Observation Step: Tool Execution and Context Reconstruction** — How tool results get folded back into the message history, and how the shape of that feedback determines what the agent can perceive. Worth going deeper because choices like truncation, summarisation, and result formatting cascade into every subsequent thought the agent has.

**Loop Termination and Stop Conditions** — The mechanisms for ending a loop gracefully: explicit final answers, iteration caps, token budgets, repetition detection, and timeout policies. A full Level 2 topic because this is where most production incidents originate, and the design space is richer than "set max_iterations=10."

**The Role of the System Message in Agentic Contexts** — How the system message primes the model to behave like a goal-seeking agent rather than a conversational responder, including goal framing, tool usage policies, and recovery instructions. Worth its own post because agentic system messages are a distinct discipline from one-shot prompting, and small wording choices compound across iterations.

---