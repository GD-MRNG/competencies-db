# The Building Blocks of AI in Production

The first two pieces in this series — The Building Blocks of AI Engineering and The Building Blocks of AI Agents — covered getting a model to do reliable work (engineering) and getting it to decide its own next steps (agents). This one covers the part nobody puts in a demo: what it takes to keep that system standing once real people are relying on it.

Here's the humbling truth about this layer: the AI logic is maybe 20% of the actual work. The other 80% is what people call Platform Engineering — the unglamorous scaffolding that turns "it worked when I ran it" into "it worked for the ten thousandth stranger who used it while I was asleep." A brilliant model sitting on broken infrastructure will fail in production. A perfectly ordinary model on well-engineered infrastructure will scale and make money. This is the layer where that difference gets decided.

Split the Frontend From the Backend, on Purpose

The single most important early decision: your user-facing interface should never talk directly to your model provider. There needs to be a backend in between — something that holds your API keys, validates what comes in, and does the actual expensive work — with the frontend only ever talking to that. Skip this split and you've effectively published your API key to anyone who opens their browser's developer tools, and you've coupled your user interface's uptime directly to your model provider's uptime. The first real traffic spike exposes exactly how bad an idea that was.

There's a related design problem worth solving early: models are slow — five to thirty seconds isn't unusual for a full response. Streaming the response token-by-token as it's generated, rather than making someone stare at a blank screen until it's all done, is the difference between a product that feels responsive and one that feels broken, even though the actual total wait time hasn't changed at all.

Secrets Are Not an Afterthought

An API key isn't a password — it's closer to a passport into your cloud account, and treating it casually is one of the fastest ways to have a very bad week. The baseline is simple: secrets live in environment variables, never hardcoded into source code, and in production they belong in a proper secret manager rather than a .env file copied around by hand.

The deeper principle underneath this is least privilege: every piece of your system — a function, a container, a person — should have access to only the minimum it actually needs to do its job. If one API key gets compromised, the damage should be contained to whatever that one key could touch, not your entire database. This is the kind of thing that costs almost nothing to do right at the start and costs enormously more to retrofit after something's gone wrong.

Package It So It Runs the Same Everywhere

"It works on my machine" is really a confession that it doesn't reliably work anywhere else. Containerization — packaging your code, your runtime, and every dependency into a single portable image — solves this directly: the same image runs identically on your laptop, your CI pipeline, and your cloud provider, because it's not depending on whatever happens to already be installed on each of those machines.

One practical trap worth knowing in advance: if you build on one chip architecture (an Apple Silicon laptop, say) and deploy to another (a typical cloud x86 server), the image can silently fail to run unless you've explicitly built it for the right target platform. It's a small detail that causes a disproportionate amount of "but it worked when I tested it" confusion.

Make Your Backend Handle Waiting Gracefully

A model call blocks for several seconds. If your backend handles requests one at a time, synchronously, each of those seconds ties up a whole thread doing nothing but waiting — and a hundred simultaneous users would mean a hundred idle threads, which is a fast way to fall over. Asynchronous backends solve this by letting a single thread juggle many waiting requests at once, picking each one back up the moment its response is ready rather than sitting idle in between. For AI workloads specifically, where every request involves this kind of waiting, this isn't a nice-to-have optimization — it's close to mandatory.

Choose Your Cloud Posture Deliberately

There's a real tradeoff between Platform-as-a-Service options (push your code, the platform handles deployment and scaling for you) and Infrastructure-as-a-Service (much more control, much more responsibility). PaaS gets you live in minutes and is the right call for an early prototype or MVP. IaaS costs you real setup time but gives you the control and portability that enterprise compliance requirements or serious cost optimization eventually demand.

Neither choice is permanent, but switching later is real work, so it's worth being deliberate rather than defaulting to whichever one a tutorial happened to use. A reasonable rule of thumb: start on a PaaS to prove the idea works, and move to more controlled infrastructure once you have a concrete reason — a compliance requirement, a cost problem, or a scaling need the platform can't accommodate.

Describe Your Infrastructure Instead of Clicking It Into Existence

Manually clicking through a cloud console to set things up feels fast in the moment and creates a system nobody can fully reconstruct or explain six months later. Infrastructure as code — using a tool like Terraform to describe, in a file, exactly what infrastructure should exist — turns your infrastructure into something version-controlled, reviewable, and reproducible, the same way you already treat application code. Every change gets a commit message and a review, instead of living only in someone's memory of what they clicked.

Pick the Right Home for Your Data

Your model calls are stateless, but your application isn't — you need somewhere to keep conversation history, user records, and (if you're doing retrieval) embeddings. These are genuinely different jobs calling for genuinely different tools: a relational database for structured records like users and transactions, a vector store for semantic search over embeddings, a cache for the things you look up constantly and don't want to recompute, and a queue for work that shouldn't block the request that triggered it.

The practical guidance here is to resist over-engineering early: start with a standard relational database and a cache, add a vector store the moment you're doing retrieval, and only reach for something more specialized once you've actually hit a specific, measured bottleneck a simpler setup can't handle.

Watch the System, Don't Guess About It

A production system is a black box the moment it's running somewhere you can't watch line-by-line. Logging records what happened; metrics track how it's performing over time (latency, cost, accuracy); traces follow one request's entire journey through every service it touched; alerts tell you the moment something crosses a threshold you care about. Skip this layer and the way you find out about problems is angry users — which is the most expensive and most reputation-damaging way possible to learn something was broken.

This matters more, not less, for AI systems specifically, because the standard question shifts. It's not just "did this request succeed or fail" — it's "which tool did the agent call, in what order, and why did it end up here." Ordinary logging tells you a request happened. Understanding an AI system's behavior requires tracing its actual decision path.

Design for Things Going Wrong, Because They Will

Model APIs time out, rate-limit you, and occasionally just go down. A system built assuming none of that will ever happen is a system that will page you at 3 a.m. the first time it does. The standard toolkit: retries with exponential backoff for genuinely transient failures, a circuit breaker that stops hammering a service once it's clearly down instead of retrying forever, and graceful degradation — if retrieval is slow, fall back to the base model rather than making the user wait or fail outright.

Worth calling out specifically: idempotency. If a request gets retried automatically, make sure retrying it can't accidentally double-charge a user or duplicate an action. This is the kind of failure mode that's invisible in testing and only shows up once, expensively, in production.

Testing an AI System Isn't Like Testing Normal Software

Ordinary software is deterministic: input X reliably produces output Y, so a test either passes or fails cleanly. AI systems are stochastic — the same prompt can produce a different, still-reasonable answer each time. This means your testing strategy needs a second layer alongside your normal unit tests: evals, which check whether an output satisfies the criteria you actually care about, even when the exact wording varies. Layer on regression testing — did swapping a model or tweaking a prompt quietly break something that used to work — and, if the system is user-facing, some deliberate adversarial testing: can someone jailbreak it, or manipulate it through a crafted input. Coverage percentages mean less here than they do in ordinary software; what matters is whether your eval set actually represents the real things users will ask.

Cost Is a Design Decision, Not Just a Bill

LLM APIs are billed per token, and that cost scales directly with your user count and the model capability you're reaching for — the gap between a frontier model and a smaller one can be an order of magnitude, and across a year that's a genuinely large number. The fix isn't cutting corners blindly; it's being deliberate: routing easy requests to a cheap model and only reserving the expensive one for the requests that actually need it, caching so a hundred users asking the same question doesn't mean a hundred separate calls, and knowing exactly which feature or user segment is driving your spend so you can make an informed tradeoff instead of an anxious guess.

Scaling Past a Single Agent

Once a single agent's context becomes a bottleneck, or a task genuinely spans multiple domains of expertise, decomposing into a small team of specialized agents — a planner, workers, a validator — starts paying for itself despite costing more calls overall. At real scale, this usually gets paired with job queues: instead of a web request blocking while an agent thinks for thirty seconds, you enqueue the work, a pool of workers picks it up in the background, and the frontend polls or gets a webhook once it's done. This is also where dedicated observability for non-deterministic systems earns its keep — being able to see an agent's entire decision tree, not just a line in a log file, is what actually lets you find where it went wrong.

Security Deserves to Be Designed In, Not Bolted On

There's a specific, dangerous combination worth naming directly: an agent that has access to private data, receives untrusted input (anything a user can type), and can communicate externally through tools. Put those three together and you have a real vulnerability — someone crafts a prompt that convinces the agent to leak data or call an attacker's endpoint on their behalf. Defending against this means validating input before it reaches the model, validating the model's output before anything gets executed on it, and sandboxing what your tools are actually allowed to do — the same least-privilege instinct from the secrets section, applied to the agent's capabilities instead of its credentials. If you're operating under compliance requirements (SOC 2, HIPAA, GDPR), audit logging and data handling need to be part of the architecture from day one, not a checklist added right before a customer's security review.

A Practical Checklist Before You Ship

If you take one concrete thing from this article, take this: before anything goes in front of real users, it's worth being able to say yes to all of the following — secrets are in environment variables, never in code; the Docker image actually builds and runs; tests and evals both pass; logs are accessible and alerts are configured for latency, error rate, and cost; there's real error handling around failed model calls; your database schema is versioned; and there's an actual incident response plan, not just a hope that nothing breaks.

None of this is exciting. All of it is what determines whether the system you built in the last two articles is a demo or a product.

The Whole Series, in One Line

Engineering gets you a model call you can trust. Agents get that model to decide what happens next. Production is what lets a stranger, at 2 a.m., with a bad internet connection, use the thing you built and have it just work — and quietly keep working long after you've stopped watching it.


Portfolio Note: I publish these articles as part of my professional portfolio. They reflect how I approach technical problems, structure solutions, and communicate complex ideas clearly.

