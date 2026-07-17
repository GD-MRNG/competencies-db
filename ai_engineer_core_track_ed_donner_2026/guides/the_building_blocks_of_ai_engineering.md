# The Building Blocks of AI Engineering

There's a specific moment that separates "using AI" from "engineering with AI." It's when you stop treating the model as a chat window and start treating it as a component — something you call, feed inputs to, get outputs from, and wire into a larger system alongside your own code.

That shift changes almost everything about how you think. This article walks through the building blocks that shift rests on — not as an exhaustive spec, but as the mental model you need before you start stacking more advanced patterns (agents, production infrastructure) on top.

The Model Is a Service, Not a Personality

The single most useful reframe in AI engineering: a model call is just an HTTP request with JSON in and JSON out. client.chat.completions.create() doesn’t care whether the model runs on OpenAI, Anthropic, Google, a fine‑tuned open‑source model, or your own laptop — it’s a function, and functions can be swapped, tested, and composed.

That reframe unlocks a harder truth underneath it: the model has no memory. Every single call is a fresh start — the model has genuinely forgotten everything from a moment ago, including your last message, unless you send it again. What feels like a flowing conversation in a chat app is actually an illusion built by re-sending the entire conversation history with every new message. This is worth sitting with, because almost every confusing agent bug and every "why did it forget what I just told it" moment traces back to someone assuming memory that was never actually there. You, the engineer, are responsible for reconstructing context every time — the model isn't going to do it for you.

Tokens Are the Unit Everything Else Is Built On

The model doesn't read your text the way you do. It breaks everything — your prompt, its own reply, code, images — into tokens: small chunks, roughly a handful of characters each. This sounds like a low-level detail, but it cascades upward into three things that actually matter to you: how much you can fit into one request (the context window), how much you'll be billed (pricing is per token), and why a model sometimes seems to "forget" something from early in a long conversation (it's competing for space with everything else you've sent).

This is also where a common expensive mistake lives: stuffing every document you have into every prompt "just to be safe." It feels thorough. It's actually slow, costly, and often makes the output worse, because the model has to sift more noise to find the signal. Knowing your token budget, and being deliberate about what earns a place in it, is a real skill — not a footnote.

Why Any of This Works At All

You don't need to be able to implement a transformer from scratch, but it helps to know the one-sentence version: the model is trained to predict the next most likely token, given everything before it. That's the entire mechanism. What's strange — genuinely still a bit of an open puzzle — is that doing this one simple thing, at enormous scale, produces something that looks like reasoning, coding ability, and creative writing. Nobody explicitly programmed those skills in; they emerged from the scale of the pattern-matching. Knowing this is mostly useful for calibrating expectations: it explains both why the model can do things that look genuinely intelligent, and why it can also confidently produce something completely wrong — it's predicting what's plausible, not consulting a fact-checker.

Where the Model Actually Runs

You have two real options, and the choice cascades through everything downstream. Local inference — running a model on your own hardware via something like Ollama — gives you full data privacy and no per-token bill, at the cost of being limited by your own machine's memory and the fact that smaller models are simply less capable. Cloud APIs give you access to the largest, most capable models available, with zero infrastructure to manage, at the cost of paying per token and sending your data to someone else's servers.

Neither is universally right. The decision usually comes down to two questions: does the task need frontier-level reasoning, and does the data need to stay private? A quick internal prototype might live entirely on a local model; a customer-facing product handling sensitive data might need both, depending on what's being processed where.

The Prompt Is Architecture, Not Decoration

It's tempting to think of a prompt as a polite request. In practice, a well-built prompt is doing real architectural work: it sets the persona, the constraints, the expected format, and the reasoning pattern the model should follow. A tight, well-considered system message is worth more than a dozen scattered examples — it's the cheapest, fastest lever you have for shaping behavior, well before you'd ever reach for something as expensive as fine-tuning.

This is also where techniques like few-shot examples (showing the model what "good" looks like) and chain-of-thought prompting ("think through this step by step") live. They're not tricks — they're ways of making your intent more legible to a system that's guessing at what you want from text alone.

Don't Marry One Vendor

No single AI provider stays on top forever, and the landscape shifts every few months. The practical defense is designing your code so it talks to models through a standard interface rather than hard-wiring yourself to one company's SDK. Most providers converged on something close to the same request format, which means a small abstraction layer lets you swap providers by changing a configuration value, not by rewriting your application. Whichever specific models are "best" right now will be out of date by the time you read this — the durable skill is designing for swap-ability, not memorizing this month's leaderboard.

Giving the Model Hands: Tool Calling

By itself, a model can't check today's weather, query your database, or know what time it is — it only knows what's in its training data and whatever you put in the prompt. Tool calling is the fix: the model generates a structured request (something that looks like {"function": "search_database", "args": {...}}), your code actually executes it, and you feed the real result back in. The model never runs anything itself — it just describes, in a format your code can parse, what it wants done.

This is the mechanism that turns a model from "a very articulate guesser" into something that can actually act on real, current, ground-truth data. It's also where a lot of production bugs live: if the model's request doesn't match the format your code expects, the whole loop breaks — which is why the next building block matters so much.

Two Ways to Add Knowledge: RAG and Fine-Tuning

There are two fundamentally different ways to make a model "know" something it wasn't trained on, and conflating them is one of the most expensive mistakes in the field.

Retrieval-Augmented Generation (RAG) looks something up at the moment it's needed: you retrieve relevant documents from your own data and hand them to the model alongside the question. Nothing about the model itself changes — it's reasoning over material you just handed it, the way you'd hand a colleague a briefing before a meeting. This is the right tool when the knowledge changes often or needs to stay auditable.

Fine-tuning instead changes the model's actual weights, using your own examples — it's closer to teaching a habit than handing over a reference document. It's the right tool for a stable behavioral pattern (a house style, a consistent output format) rather than a fact that might change next week. It's also more expensive, harder to debug, and carries a real risk of the model "forgetting" abilities it used to have as a side effect of learning new ones. The simple rule of thumb: changing facts → retrieval; stable behavior → weights.

Making the Output Trustworthy: Structured Outputs

Left alone, a model's output is fuzzy — "usually valid JSON, mostly." That's fine for a chat window and completely unacceptable for a system feeding a database or triggering a transaction. Structured outputs (sometimes called constrained decoding) mathematically force the model to only generate tokens that satisfy a schema you've defined — the invalid options are removed from consideration at every single step of generation, not just wished away with instructions. This is the difference between hoping the model's JSON parses and knowing it will, and it's the piece that lets you wire AI into strict, unforgiving software systems with confidence.

The Final Mile: Wiring It All Together

A real production system is never just one model call — it's a combination of models, retrieval, maybe a fine-tuned specialist, and ordinary hard-coded logic, with a deliberate architecture deciding where each piece of "intelligence" should live. Underneath that, you need the unglamorous infrastructure: serving layers that keep latency reasonable, caching so you're not paying to recompute the same thing twice, and monitoring that tells you the difference between "the model hallucinated" and "the API is just down." None of this is exciting, and all of it is what actually separates a demo from something people can depend on.

Observability deserves its own callout here: if you can't see what the system did — which tool it called, what it retrieved, why it produced a given answer — you can't actually improve it. Instrumenting this from day one is far cheaper than reconstructing it after something's gone wrong in front of a user.

Where This Goes Next

Everything above is deliberately scoped to a single model call, made reliable. It's the floor, not the ceiling. Once you're comfortable with decoupled inference, context management, tool calling, and structured outputs, the natural next step is the agentic layer — where the model stops being an oracle you query and starts being the decision-maker choosing what happens next. That’s a different set of tradeoffs entirely, and it’s exactly where the next piece in this series picks up: The Building Blocks of AI Agents.


Portfolio Note: I publish these articles as part of my professional portfolio. They reflect how I approach technical problems, structure solutions, and communicate complex ideas clearly.