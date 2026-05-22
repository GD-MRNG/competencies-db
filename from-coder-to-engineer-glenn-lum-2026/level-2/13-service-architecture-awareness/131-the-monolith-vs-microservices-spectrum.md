## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams talk about monoliths and microservices as if they are choosing between two buildings. In practice, they are choosing where to put walls inside one building — and every wall they add changes the plumbing, the wiring, the fire code, and who holds the keys to which rooms. The Level 1 post laid out what monoliths and microservices are and sketched the surface-level tradeoffs. What it did not cover is the thing that actually determines whether an architecture succeeds or fails: the mechanics of what happens at a service boundary, why the space between monolith and microservices is where most real systems live, and why drawing a boundary in the wrong place costs more than having no boundary at all.

## What a Service Boundary Actually Does

When all your code runs in one process, a function call between the order module and the inventory module is a stack frame. It completes in nanoseconds. It either succeeds or throws an exception that you catch in the same call stack. The data it operates on can participate in a single database transaction — either the order is placed and inventory decremented atomically, or neither happens.

The moment you extract the inventory module into a separate service, that function call becomes an HTTP request or a gRPC call. This is not just "slower." It is a categorical change in the failure model. The call can now fail in ways that a function call cannot: the network can partition, the remote service can be up but slow (the worst failure mode in distributed systems, because it holds resources open), the response can arrive after your timeout fires, or the service can process the request successfully but the acknowledgment can be lost on the way back. You now have a state where *you don't know whether the operation succeeded*, which is a condition that does not exist inside a single process.

This also means the data involved in that interaction can no longer participate in a local transaction. If the order service writes an order to its database and then calls the inventory service to decrement stock, and that call fails, you now have an order with no corresponding inventory adjustment. You are in the world of **distributed data consistency**, and your options are some form of saga pattern (a chain of compensating operations), eventual consistency (accepting that the two data stores will be temporarily out of sync), or the outbox pattern (writing events to your local database transactionally and publishing them asynchronously). All of these are real engineering work with real edge cases. None of them are free.

Every service boundary you introduce is a commitment to solving this class of problem at that boundary, forever.

## The Spectrum Between Monolith and Microservices

The binary framing obscures the architecture most teams actually need. Between a single-process monolith and fine-grained microservices sits a range of options, and the transitions between them have specific mechanical properties.

### The Modular Monolith

A **modular monolith** is a single deployable unit where the internal code is organized into well-defined modules with explicit boundaries — enforced through access control at the code level, separate module directories or packages, and defined interfaces between modules. Critically, the modules may or may not share a database, but if they do, they access only their own tables through their own data access layer.

The mechanical advantage is significant: you get the deployment simplicity and transactional integrity of a monolith while building the internal separation that would make future extraction possible. A module boundary enforced in code is dramatically cheaper to maintain than a service boundary enforced over the network. You can refactor across it using your IDE. You can test across it without standing up infrastructure. You can reason about it with a debugger.

The discipline required is real, though. Without enforcement — whether through build system constraints, architecture tests (tools like ArchUnit), or code review rigor — module boundaries erode. Someone writes a direct SQL join across module tables because it's expedient, and now those modules are coupled at the data layer in a way that would block future extraction.

### Coarse-Grained Services

The next step on the spectrum is a small number of independently deployable services, each owning a significant business domain. This is not microservices — it is closer to what was historically called **service-oriented architecture**, though that term carries a lot of baggage. Think three to eight services for a mid-sized system: an order service, a user service, a payments service, a notification service.

At this granularity, each service boundary represents a major organizational boundary (usually aligned to a team), and the interaction patterns between services are well-understood and relatively infrequent compared to the intra-service communication within each one. The ratio of network calls to local calls is still heavily weighted toward local. This is where many production systems that call themselves "microservices" actually operate.

### Fine-Grained Microservices

At the far end, each service does one narrow thing: a pricing service, a tax calculation service, a cart service, a checkout orchestration service, an address validation service. The mechanical reality here is that a single user-facing request touches many services. A checkout operation might involve eight to twelve network hops. Latency is additive. Failure probability is multiplicative — if each service has 99.9% availability, twelve services in a synchronous chain gives you roughly 98.8% availability for that operation, before you have done anything wrong.

This granularity buys you maximum deployment independence and team autonomy. But the operational infrastructure required to make it work is substantial: service mesh or API gateway for routing and traffic management, distributed tracing as a non-negotiable requirement (not a nice-to-have), centralized logging with correlation IDs threaded through every request, circuit breakers and bulkheads to prevent cascade failures, and a deployment pipeline mature enough to handle dozens of independent release cycles without coordination chaos.

## The Data Boundary Is the Hard Part

Teams consistently underestimate this: splitting code into separate services is straightforward. Splitting the data is where architectural decisions become genuinely difficult and often irreversible.

When two modules in a monolith share a database, they can join across tables, enforce foreign key constraints, and participate in the same transaction. The moment those modules become separate services with separate databases — which is the whole point, because a shared database between services is a coupling mechanism that defeats the purpose of the split — you lose all of that.

Concretely: if the order service needs to display an order with the customer's name and address, and that data now lives in the user service's database, the order service has to call the user service at query time, or maintain a local cache or read-model of user data that it keeps synchronized. The first option adds latency and a failure dependency to every order query. The second option means you are building and maintaining a data synchronization mechanism — and accepting that the order service's copy of the user's name might be stale by seconds or minutes.

This is not a theoretical concern. It is the daily mechanical reality of operating a system with split data ownership. Every reporting query that used to be a SQL join is now either an API aggregation call or a denormalized read model that must be kept in sync. Every data integrity guarantee that the relational database used to enforce for free is now your application's responsibility.

The question to ask before splitting a data boundary is not "can we split this?" It is: "What queries, transactions, and consistency guarantees cross this boundary, and are we prepared to replace all of them with application-level solutions?"

## Coupling Does Not Disappear — It Moves

Extracting a service does not remove coupling between two parts of a system. It moves the coupling from the code layer (where it is visible, searchable, and enforceable by the compiler) to the network layer (where it is implicit, runtime-dependent, and discoverable only through tracing and testing).

A **distributed monolith** is what you get when you split a system into services that still need to be deployed together, still share data schemas, or still fail together. You have all the operational complexity of microservices — network boundaries, serialization overhead, distributed debugging — with none of the benefits. This is not a rare edge case. It is the most common failure mode of microservice migrations.

The mechanical signature of a distributed monolith: you cannot deploy Service A without also deploying Service B. A schema change in Service A's API requires synchronized changes in three other services. Your services communicate through a shared database rather than through APIs. A failure in one service reliably cascades into failures in services that are supposed to be independent.

What went wrong is usually that the boundary was drawn along technical lines (a "database service," an "auth service," a "logging service") rather than along domain lines where the actual independence exists. If two services must change in lockstep for most feature work, they are not independent services — they are a monolith with a network call in the middle.

## Tradeoffs and Failure Modes

### Premature Decomposition

The most expensive architectural mistake is splitting too early, before you understand the domain well enough to draw boundaries correctly. Moving a boundary between modules in a monolith is a refactoring exercise — hours or days of work. Moving a boundary between services means migrating data, rewriting API contracts, updating every consumer, and changing the operational topology. It is weeks or months of work, and it often doesn't happen because the cost is prohibitive, so the wrong boundary persists and becomes load-bearing.

This is why the standard advice — start with a monolith, extract services when you have evidence that the boundary is correct — is not conservative timidity. It is engineering risk management. You are deferring irreversible decisions until you have the information to make them well.

### The Hidden Cost of Organizational Coordination

Microservices shift coordination costs from code-level integration to API contract negotiation and operational coordination. In a monolith, adding a field to a shared data structure is a code change with compiler-checked impact. In a microservices architecture, adding a field to a service's API requires versioning, backward compatibility analysis, consumer migration, and potentially running two versions simultaneously. The total person-hours spent on the change may be higher, not lower.

This cost is worth paying when teams genuinely need independent release cycles — when the alternative is a weekly deployment meeting with fifteen teams arguing over merge conflicts. It is not worth paying when two developers on the same team are maintaining both sides of the API.

### Observability as a Prerequisite, Not a Feature

In a monolith, you can troubleshoot a production issue with application logs and a stack trace. In a microservices architecture, a single user request may traverse a dozen services. Without distributed tracing (OpenTelemetry, Jaeger, Zipkin), you cannot reconstruct what happened. Without correlation IDs threading through every service hop, your logs are a disconnected pile of events. This is not an enhancement you add later — it is foundational infrastructure that must exist before the second service goes into production. Teams that skip this spend months debugging issues that would be trivial to diagnose in a monolith.

## The Mental Model

The decision between monolith and microservices is not a choice between simplicity and sophistication. It is a decision about where to pay the cost of boundaries. Every boundary you draw — whether it is a module boundary in code or a service boundary over the network — exists to enable independent change. The value of that independence is directly proportional to how often the things on each side of the boundary need to change independently, and the cost is directly proportional to how often they need to coordinate.

A well-structured monolith with clean module boundaries gives you most of the organizational benefits at a fraction of the operational cost. Extracting a service is justified when the coordination cost of keeping it in the monolith exceeds the operational cost of maintaining it as a separate system — and that calculation depends on team structure, deployment frequency, scaling requirements, and domain boundaries that you can only identify through experience with the actual system.

The question is never "should we use microservices?" The question is: "Where do the real boundaries in our system lie, and what is the cheapest boundary mechanism that gives us the independence we actually need?"

## Key Takeaways

- **Every service boundary converts a function call into a network call**, introducing failure modes that do not exist inside a single process — including the state of not knowing whether an operation succeeded.

- **Splitting data is the hard part of service extraction**, not splitting code. Every cross-boundary query, transaction, and foreign key constraint must be replaced with an application-level mechanism.

- **A distributed monolith — services that must deploy, change, or fail together — is the most common outcome of poorly planned microservice migrations**, and it carries the costs of both architectures with the benefits of neither.

- **The modular monolith is a legitimate architectural choice**, not a waypoint on the road to microservices. It provides internal separation with dramatically lower operational cost than network boundaries.

- **Observability infrastructure (distributed tracing, correlation IDs, centralized logging) is a prerequisite for operating microservices**, not a feature to add after migration. Without it, debugging distributed failures is effectively guesswork.

- **Premature service extraction is expensive to reverse.** Moving a boundary between modules is a refactor; moving a boundary between services is a migration. Defer service boundaries until you have evidence the boundary is correct.

- **The value of a boundary is proportional to the independence it enables; the cost is proportional to the coordination it requires.** Draw boundaries where change frequency diverges, not along technical layers.

- **The right question is not "monolith or microservices" but "where are the real boundaries, and what is the cheapest mechanism that provides the independence we need?"**

# Discussion

## Why This Conversation Is Happening

Teams get hurt by architecture decisions when they treat “microservices” and “monolith” as labels instead of mechanics. The damage usually shows up in very practical ways: a checkout request now depends on six network hops and sometimes hangs; a simple feature requires coordinated deploys across multiple services; a reporting query that used to be one SQL join becomes an unreliable chain of API calls. The system becomes harder to change, not easier.

The reason this topic matters is that boundaries are expensive, and the expense is not just performance. A service boundary changes what can fail, how data stays consistent, how debugging works, and how teams coordinate changes. If you do not understand what that boundary actually does, you can accidentally build a distributed monolith: all the operational pain of microservices, while the parts still have to move together.

The core engineering problem is deciding where independence is worth paying for. If you put a boundary in the wrong place, you buy permanent coordination overhead, data-sync work, and distributed failure modes for little or no gain. If you avoid all boundaries, one part of the system can start constraining every other part. The article is really about how to recognize that tradeoff in concrete terms.

---

## What You Need To Know First

### 1. Local call vs remote call
A local function call happens inside one running process. It is fast, shares memory, and fails in relatively simple ways: it returns, or it throws an error you can handle in the same execution flow. A remote call goes over a network to another process. That means latency is much higher and failure is ambiguous: the other side may be down, slow, unreachable, or may have completed the work even though you never got the response.

### 2. Database transaction
A transaction is the database mechanism that lets several changes succeed or fail as one unit. If placing an order and decrementing stock happen in the same transaction, you do not end up with only half the work applied. This matters because once the work spans multiple services and databases, that easy atomic guarantee is usually gone.

### 3. Coupling
Coupling means two parts of a system must know about each other or change together. Some coupling is unavoidable. The important question is where it lives. In a monolith, coupling is often in code, types, and direct calls. In a distributed system, that same dependency may move into API contracts, deployment sequencing, runtime availability, and data synchronization.

### 4. Domain boundary
A domain boundary is a split based on business responsibility, not technical layer. “Orders” and “payments” can be domain boundaries because they represent distinct business capabilities. “Database service” or “logging service” are often technical slices that many other parts must touch, which tends to create central bottlenecks rather than real independence.

---

## The Key Ideas, Connected

### 1. A service boundary is not just a packaging choice; it changes the physics of the interaction.
Inside a monolith, one module calling another is just code executing in one process. The caller and callee share the same runtime, can usually share the same transaction, and failures are immediate and local. Once you split one side into a separate service, that interaction becomes a network exchange.

That matters because the call is no longer simply “slower.” It now has entirely new states: the request may arrive but the response may not; the service may be alive but overloaded; your timeout may fire even though the remote side later finishes the work. The article’s most important move is to get you to stop thinking of service extraction as moving code and start thinking of it as changing the failure model. Once that is true, the next problem appears naturally: if the interaction changed, then the data guarantees around that interaction also changed.

### 2. Once a boundary is remote, you usually lose the easy transaction story.
In one process with one database, order creation and inventory decrement can be wrapped in one local transaction. The system can say: either both happen, or neither does. That gives you a simple integrity model.

After splitting order and inventory into separate services with separate databases, that guarantee no longer comes for free. If the order write succeeds and the inventory call fails or times out, you have partial completion. That is why patterns like sagas, eventual consistency, and the outbox pattern exist: they are replacements for guarantees you used to get from locality. This leads directly to the next idea: the hardest part of extraction is not code separation, but data separation.

### 3. Splitting code is easy compared with splitting data ownership.
Developers often imagine service extraction as “move this module into another repo and add an API.” The article argues that this is the easy part. The hard part is what happens to queries, transactions, foreign keys, and joins once the data is no longer in one place.

If order data and user data live in different services, you cannot casually join them in SQL anymore. Now you either fetch remote data at request time, which adds latency and runtime dependency, or you copy some user data locally, which adds synchronization work and staleness. In other words, every convenience the shared database gave you must now be rebuilt at the application layer. And once data is the hard part, the architecture choice stops being “monolith versus microservices” and becomes “what kind of boundary can we afford here?”

### 4. Because boundaries have different costs, there is a spectrum, not a binary choice.
If the real issue is how expensive a boundary is, then the choice is not only “single monolith” or “many tiny services.” There are intermediate boundary mechanisms with different cost profiles. The article uses modular monolith, coarse-grained services, and fine-grained microservices as points on that spectrum.

A modular monolith gives you internal separation without paying network costs. You can enforce module boundaries in code, keep one deployment unit, and preserve local transactions. Coarse-grained services add some independence where it matters most, but keep the number of remote interactions manageable. Fine-grained microservices maximize deploy autonomy, but multiply network hops, operational tooling needs, and availability math. Once you see the spectrum this way, the next idea becomes clearer: the question is not whether coupling exists, but what form it takes after you draw a boundary.

### 5. Coupling never disappears; a service boundary can merely relocate it.
A common mistake is to think extracting a service makes two parts of the system independent by default. The article pushes against that. If two parts still need coordinated schema changes, synchronized deploys, shared tables, or tightly ordered releases, they are still coupled.

What changed is where the coupling lives. In a monolith, the dependency is visible in code and often checked by the compiler or test suite. In a distributed system, that same dependency may now be hidden in API versions, deployment playbooks, message schemas, and runtime dependencies. This is why distributed monoliths happen: engineers move code across a network boundary without creating real business independence. And once you realize that false independence is possible, the next question is what a bad boundary actually looks like in practice.

### 6. A distributed monolith is the failure mode where services are separate in infrastructure but not in behavior.
The article defines this mechanically, not rhetorically. You know you have a distributed monolith when one service cannot be deployed safely without others, when feature work requires lockstep changes across multiple services, when they share a database schema, or when one service outage predictably drags down others.

This is a worse state than either side of the supposed tradeoff. You pay for network calls, distributed debugging, and more deployment machinery, but you do not gain independent evolution. That usually happens because the boundaries were drawn around technical layers rather than domain seams. And that observation leads naturally to the article’s next major claim: premature decomposition is expensive because getting boundaries wrong becomes hard to undo.

### 7. Wrong service boundaries are much more expensive to fix than wrong module boundaries.
In a monolith, if two modules were split incorrectly, you can usually refactor the code, move classes, adjust interfaces, and update tests. It is work, but the system is still local and unified. In a service architecture, correcting the same mistake may require moving ownership of data, changing APIs, migrating consumers, backfilling state, and altering operational routing.

That asymmetry explains why “start with a monolith” is not just cultural advice or simplicity bias. It is a way of delaying expensive, hard-to-reverse decisions until the domain is understood well enough to justify them. Once the cost of reversal is visible, another hidden cost becomes easier to appreciate: architecture also changes how humans coordinate.

### 8. Microservices often trade code coordination for organizational and operational coordination.
In a monolith, changing a shared structure may be a code edit plus compiler errors showing you what else must change. In microservices, the equivalent change may require API versioning, backward compatibility support, consumer rollout planning, and two versions operating at once.

So the gain is not “less coordination.” It is “different coordination.” This is valuable when teams truly need independent release cycles or have different scaling and ownership needs. It is wasteful when the same small team owns both sides and could have changed one codebase directly. And this in turn explains why observability becomes essential: once coordination and debugging happen across runtime boundaries, you need infrastructure that can show the path a request took.

### 9. In distributed systems, observability is part of the system, not an optional extra.
In a monolith, a stack trace and local logs can often tell you what happened. In a system where a request crosses many services, those tools stop being enough. You need correlation IDs to tie events together, centralized logs so the evidence is in one place, and distributed tracing so you can see which hop was slow or failed.

This is not polish. It is what makes the system operable. Without it, a production incident becomes guesswork across multiple teams and services. And with that in place, the article’s final mental model becomes justified: the architecture decision is really about buying independence with boundaries, and choosing the cheapest boundary that gives you the independence you actually need.

### 10. The right architecture question is: where are real independent-change seams, and what is the cheapest boundary mechanism that fits them?
This is the article’s conclusion, but it follows from all the earlier mechanics. Service boundaries create harder failure modes, harder data consistency problems, and more operational overhead. Module boundaries are cheaper but provide less hard isolation. Therefore the job is to match boundary cost to actual need.

If two parts rarely need to change independently, a network boundary is probably overpaying. If they truly need separate release cycles, ownership, scaling, or fault isolation, then a service boundary may be worth the permanent cost. The key is that boundary value comes from enabling independent change, while boundary cost comes from the coordination and runtime complexity introduced. That is the central model to keep.

---

## Handles and Anchors

### 1. “A service boundary turns a function call into a negotiation.”
A local call is immediate and direct. A remote call is a conversation across unreliable space: timeouts, retries, serialization, versioning, unknown completion state. If you remember this sentence, you will naturally ask different questions before extracting a service.

### 2. Think of coupling like water: you can reroute it, but you do not get to remove it.
In a monolith, coupling flows through code references, shared types, and direct database access. In microservices, it flows through APIs, schemas, deployment order, and data replication. If someone claims a new service “decouples” the system, ask: where did the dependency move?

### 3. Ask this boundary test:
“What queries, transactions, and changes cross this boundary today, and what mechanism will replace each one?”
If the answer is vague, the boundary is probably being drawn too early. This question forces the abstract idea of “splitting a service” into concrete replacement work.

---

## What This Changes When You Build

### 1. An engineer who understands this will separate modules in code before separating them over the network because code boundaries are cheaper to correct.
The unaware engineer often jumps to service extraction as soon as a module feels important. That inherits network failure modes and data consistency problems early. The informed engineer first creates a modular monolith with explicit interfaces, protected access patterns, and ownership rules, because this lets the team discover the real seams while changes are still cheap.

### 2. An engineer who understands this will treat data ownership as the first design problem in service extraction, not the last implementation detail.
The default mistake is to split code first and leave a shared database in place “temporarily,” or to discover too late that core queries depended on joins across the proposed boundary. The informed engineer starts by listing cross-boundary reads, writes, transactions, and invariants, because those determine whether the split is viable and what new mechanisms must exist.

### 3. An engineer who understands this will choose coarser service boundaries unless there is strong evidence for finer ones because hop count directly affects latency, availability, and debugging complexity.
The unaware engineer often equates smaller services with better architecture. The consequence is a user request that traverses many synchronous dependencies. The informed engineer notices that each extra hop adds latency and multiplies failure probability, so they keep services broad enough that most work stays local.

### 4. An engineer who understands this will invest in observability before expanding service count because distributed failures are otherwise hard to reconstruct.
The default move is to add tracing and correlation later, after “the migration.” By then the team is already operating blind. The informed engineer knows the second or third service is the moment centralized logging, trace propagation, and request correlation stop being nice-to-have and become required operating equipment.

### 5. An engineer who understands this will use independent change as the test for a boundary, not technical neatness.
The default decomposition is often by layer or utility: auth service, database service, reporting service. These look tidy on diagrams but create broad dependencies and synchronized changes. The informed engineer asks which parts of the business actually evolve, scale, and deploy independently. That leads to boundaries around domains, not around technical categories.

---
