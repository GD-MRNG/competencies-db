## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams that adopt microservices get the deployment topology right. Separate repositories, separate CI pipelines, separate containers. Clean boxes on the architecture diagram. Then they connect three, five, or fifteen of those boxes to the same PostgreSQL instance, reading and writing to the same tables, and wonder why they still can't deploy a service without coordinating with two other teams.

The shared database is where microservice independence goes to die — not as a vague architectural concern, but in the specific, mechanical sense that a shared schema is a shared contract, and a shared contract between independently deployed services means every schema change is a cross-team coordination event. You've built a distributed monolith: all the operational complexity of a distributed system with none of the deployment independence you were after.

Understanding *why* this happens — at the level of the coupling mechanics, not the architectural principle — is what separates teams that successfully decompose systems from teams that end up with something worse than the monolith they started from.

## The Schema Is an Unversioned API

When Service A and Service B both connect to the same database and query the `orders` table, they share a dependency on that table's structure: its column names, types, constraints, indexes, and relationships to other tables. This is a contract. It functions exactly like an API contract between the two services — it defines the shape of the data one service produces and another consumes.

The difference between this contract and an actual API is that nobody treats it like one. There's no versioning. There's no backward compatibility policy. There's no contract test. There's no deprecation path. When a developer on Service A's team needs to rename a column, split a table, or change a foreign key relationship, they're making a breaking change to every other service that touches that table. But unlike a breaking change to a REST endpoint — which would be caught by integration tests, flagged in API reviews, and managed through versioning — a schema change often isn't discovered until something fails in production.

This is the core mechanic: **a shared database creates an implicit, unversioned, untested API between every service that touches it.** The coupling isn't visible in any service's codebase. It lives in the schema itself, and it becomes apparent only when someone tries to change it.

## How Schema Coupling Defeats Deployment Independence

Walk through a concrete scenario. You have an `orders` service and a `billing` service. Both read and write to an `orders` table:

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  customer_id UUID NOT NULL,
  status VARCHAR(50) NOT NULL,
  total_amount DECIMAL(10,2) NOT NULL,
  billing_address TEXT,
  created_at TIMESTAMP NOT NULL
);
```

The orders service manages order lifecycle — creation, status transitions, fulfillment. The billing service reads from this table to generate invoices and writes back payment status.

Now the orders team needs to support multi-currency pricing. They need to change `total_amount` to store a value alongside a currency code. Maybe they split it into `amount` and `currency`, maybe they add a separate column, maybe they restructure entirely.

Any of these changes will break the billing service. The billing service has queries like `SELECT total_amount FROM orders WHERE ...` baked into its code. It has logic that assumes `total_amount` is a plain decimal representing a single currency.

So the orders team can't just deploy their change. They need to coordinate with the billing team. They need to agree on a migration strategy. They need to deploy in lockstep or design a multi-phase migration where both old and new columns coexist. They need to verify their changes against the billing service's queries.

This is the exact coordination overhead microservices were supposed to eliminate. Two separately deployable services that cannot, in practice, be deployed separately.

This isn't a one-time cost. It recurs on every schema change that touches a shared surface. Over time, teams learn to avoid schema changes, so the schema calcifies and becomes a constraint on how fast any service can evolve. Or teams make changes without coordinating, and things break at runtime.

## The Read Path Is Not Innocent

A common rationalization: "We only *read* from that table. We're not writing, so there's no real coupling."

This is wrong. Read-only access to another service's tables creates coupling in two distinct ways.

First, **you are coupled to the schema's shape.** If the owning service restructures its tables — normalizes, denormalizes, renames columns, changes types — your queries break. The coupling is identical to the write case.

Second, **you are coupled to the schema's semantics.** When the billing service reads `status = 'completed'` from the orders table, it's making an assumption about what "completed" means in the orders domain. If the orders team later introduces a distinction between "completed" and "fulfilled" to handle partial fulfillment, the billing service's interpretation of that field is wrong. The data hasn't changed shape, but its meaning has shifted, and the billing service has no way to know.

This semantic coupling is subtler and more dangerous than structural coupling. Schema changes produce errors. Semantic drift produces *wrong behavior* that passes all validation checks.

## The Write Path and Ownership Ambiguity

When multiple services write to the same table, the problems compound. You get ambiguity about who owns the data and who's responsible for its integrity.

Consider our orders table. The orders service sets `status` to `'pending'` on creation. The billing service sets it to `'paid'` after successful payment. The fulfillment service sets it to `'shipped'` after dispatch. Three services writing to the same column.

Who enforces valid state transitions? In a monolith, a single `Order` model contains the business logic: an order can move from `pending` to `paid`, never from `shipped` back to `pending`. With three services writing to the same column, that business logic is either duplicated across all three codebases (and inevitably diverges), or it doesn't exist at all and you rely on convention.

This is how you get an order with `status = 'shipped'` that was never paid for. Not because anyone made an obvious mistake, but because the state machine that should govern that column is scattered across three codebases with no single point of enforcement.

**Data ownership** means one service is the authoritative source for a piece of data: it controls writes, enforces invariants, and defines what the data means. When a database is shared, ownership is ambiguous by default, and ambiguous ownership is effectively no ownership.

## What the Alternatives Actually Look Like

If services can't share a database, how does Service B get data that Service A owns? Three fundamental patterns, differing in when the data moves and what consistency guarantees you retain.

### API-Mediated Access

Service B calls Service A's API at query time. Service A exposes only what it chooses, in a format it controls, with versioning it manages. The underlying schema is fully encapsulated — Service B never sees the table structure.

The cost: Service B now depends on Service A being available at query time. If Service A is down or slow, Service B degrades. You've traded schema coupling for runtime coupling. For many use cases this is a good trade — runtime coupling is visible, measurable, and manageable with circuit breakers and timeouts. Schema coupling is invisible and discovered during incidents.

For high-throughput read paths or queries that would need to join data across multiple services, synchronous API calls introduce latency and fragility that may not be acceptable.

### Event-Carried State Transfer

Service A publishes events carrying the data Service B needs. When an order is created, Service A emits an `OrderCreated` event containing the order ID, customer ID, amount, and currency. Service B consumes this event and stores a local copy in its own database, in whatever schema suits its domain.

Service B now has zero runtime dependency on Service A. It queries its own local store at any time. It owns its schema and can restructure its local representation without coordinating with anyone.

The cost: the data in Service B's local store is **eventually consistent** with Service A's authoritative data. If Service A updates an order and Service B hasn't processed the event yet, Service B is working with stale data. The event structure between the services becomes the new contract — it needs versioning and backward compatibility management just like a REST endpoint.

### Change Data Capture

A mechanical variant of event-carried state transfer: instead of the application publishing explicit domain events, a tool like Debezium reads the database's write-ahead log and publishes row-level changes as events. Service B consumes these and materializes its own read model.

This is valuable when you can't modify Service A's code to publish events — common during incremental migrations away from a shared database. It carries the same eventual consistency costs, plus an additional one: the events are shaped like database mutations (inserts, updates, deletes on specific columns) rather than domain events, which makes them harder for consumers to interpret meaningfully. You're leaking schema structure through the back door, which partially reintroduces the coupling you were trying to eliminate.

## Where This Breaks and What It Costs

### The Distributed Monolith Trap

The most common failure: teams adopt microservices, keep the shared database, and end up with a system that has all the operational costs of distribution (network failures, partial failures, distributed tracing) and none of the benefits (independent deployment, team autonomy). This is strictly worse than a monolith. The monolith at least gave you local transactions and a single debugger.

The response should not be to panic-split the database. Prematurely separating data stores without understanding domain boundaries leads to a different failure.

### Splitting Along Wrong Boundaries

If you separate databases along incorrect service boundaries, you end up performing expensive cross-service joins or multi-service transactions for operations that should be local. A team that splits `orders` and `order_items` into separate services with separate databases will spend enormous effort replicating what a single SQL join did for free.

The database split must follow the domain boundary, not the other way around. If two tables are almost always queried together and participate in the same transactions, they belong to the same service. Splitting them introduces distributed coordination for zero architectural benefit.

### Underestimating the Consistency Cost

Teams that move from a shared database to event-carried state transfer often underestimate how much of their system's correctness was silently relying on strong consistency. When the billing service could read directly from the orders table, it always saw the latest state. Now it works from a local copy that might be seconds — or during an outage, minutes — behind.

This produces concrete bugs: a customer cancels an order, but the billing service hasn't received the cancellation event and charges them anyway. The refund path now has to handle a case that never existed when both services read from the same source of truth.

The answer isn't to avoid eventual consistency. It's to design explicitly for it. But you can't design for it if you don't understand that leaving the shared database means giving up an implicit consistency guarantee that was silently keeping things correct.

### The "Just One More Query" Erosion

Even teams that start with clean ownership erode it incrementally. A developer needs one column from another service's table for a report. A direct database connection is five minutes of work. Building the proper API endpoint that doesn't exist yet is a week. The expedient choice wins. Six months later, fifteen services read from each other's tables through a web of cross-schema queries, and you're back to a shared database in all but name.

This is a governance problem, not a technical one. Direct database access to another service's schema must be treated as a boundary violation, not a shortcut.

## The Model to Carry Forward

A database is not just storage — it is a contract surface. When two services share a database, the schema becomes an implicit API between them: unversioned, untested, and invisible in any service's dependency graph. Every schema change becomes a cross-team coordination event, which is the precise coupling that service decomposition exists to eliminate.

The principle: **each service should own its data the way it owns its code.** The service controls the internal representation, enforces the invariants, and exposes only an explicit, versioned interface for others to consume. The database is an implementation detail of the service, not a shared integration layer.

This creates real costs — you lose cross-service joins, you lose distributed ACID transactions, you take on eventual consistency. These costs are the price of deployment independence, and they are worth paying only when you actually need that independence. Understanding this tradeoff is the conceptual prerequisite to reasoning about sagas, event sourcing, CQRS, and every other pattern that exists to manage data across service boundaries.

## Key Takeaways

- A shared database between services creates an implicit, unversioned API at the schema level — every schema change becomes a cross-team coordination event that defeats the deployment independence microservices are supposed to provide.

- Read-only access to another service's tables is still coupling: you depend on both the shape and the semantic meaning of the data, both of which can change without warning.

- When multiple services write to the same table, data ownership becomes ambiguous, business invariants get scattered across codebases, and state corruption becomes a matter of time rather than possibility.

- The distributed monolith — microservices sharing a database — is strictly worse than a well-structured monolith because you absorb the costs of distribution while gaining none of its benefits.

- Splitting a database along the wrong service boundaries forces expensive cross-service coordination for operations that should be local; the data split must follow the domain boundary, not precede it.

- API-mediated access trades invisible schema coupling for visible runtime coupling — generally a favorable trade because runtime dependencies can be measured, monitored, and mitigated.

- Event-carried state transfer eliminates runtime coupling but introduces eventual consistency, which requires explicit design for every case where stale data could produce incorrect behavior.

- Data ownership boundaries erode through incremental shortcuts; maintaining them is a governance discipline, not a one-time architectural decision.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

A lot of teams adopt microservices to get one specific benefit: the ability for one team to change and deploy its service without waiting on other teams. That promise breaks the moment multiple services depend on the same database schema. Now a column rename, a type change, or even a subtle shift in what a field means can break another service without either team noticing until runtime. What looked like “independent services” at the repo and container level is still one tightly coupled system at the data level.

When engineers don’t have a concrete model of this, they make decisions that feel harmless in the moment: “we only need one read query,” “it’s the same table anyway,” “we’ll coordinate this migration later.” The failure mode is not abstract architectural impurity. It is blocked deployments, fragile migrations, hidden inter-team dependencies, and production bugs caused by one service changing data another service quietly relied on.

The deeper reason this matters is that data boundaries are where service boundaries become real or fake. If you misunderstand that, you can end up with the worst combination available: distributed-system complexity on the outside, monolith-level coupling underneath.

---

## What You Need To Know First

### 1. What a service boundary is
A service boundary is the line around what one service owns and is responsible for. Inside that boundary, the service can organize code and data however it wants. Outside that boundary, other services should interact only through explicit interfaces, like APIs or events. If other services can reach inside and depend on internal tables directly, the boundary is mostly pretend.

### 2. What a schema is
A database schema is the structure of stored data: tables, columns, types, constraints, indexes, and relationships. It is not just storage layout. Any code that queries the database depends on that structure being what it expects. If the structure changes, that code may fail or behave differently.

### 3. The difference between strong consistency and eventual consistency
Strong consistency means when you read data, you expect to see the latest committed value immediately. Eventual consistency means copies can lag; for some period of time, different parts of the system may see different versions of reality. Shared-database access often gives you strong consistency by default. Many decoupled-service patterns do not.

### 4. What “ownership of data” means
Owning data means one service is the authority for that data: it decides how it is stored, who can change it, and what rules must always be true. If multiple services write the same records directly, ownership is blurred. Once ownership is blurred, invariants usually stop having one reliable enforcement point.

---

## The Key Ideas, Connected

### 1. A shared database schema acts like an API contract whether you acknowledge it or not.
If two services both use the same table, they both depend on that table’s shape and meaning. That is functionally an interface between them. The important part is that the dependency exists even if nobody wrote an API spec or drew a boundary on a diagram.

This matters because service independence depends on being able to change internals without breaking consumers. But if another service is querying your tables directly, your schema is no longer internal. It has become part of what they consume. That leads directly to the next idea: if the schema is an interface, then schema changes behave like interface changes.

### 2. Shared schemas are usually unversioned interfaces, so changes become breaking changes by surprise.
With a normal API, teams usually expect versioning, compatibility rules, and tests that tell them when they broke a consumer. Shared database access often skips all of that. A team changes a column name or data type because it looks like an internal refactor, but another service was depending on it.

The mechanism here is simple: the consuming service has SQL queries, ORM mappings, assumptions about nullability, and business logic tied to the old structure. Since the dependency lives in the database rather than an explicit service contract, the producer often cannot even see who they are about to break. Once this is true, deployment independence starts to disappear, because any schema change now requires coordination.

### 3. Once schema changes can break other services, deployments stop being truly independent.
Suppose one team needs to split `total_amount` into `amount` plus `currency`. If another service reads `total_amount`, the first team cannot safely deploy alone. They have to coordinate rollout order, compatibility windows, migration sequencing, and testing across teams.

That is the mechanical reason a shared database defeats microservice independence. It is not that “shared databases are bad” in the abstract. It is that internal changes are no longer internal. Every change to shared data structures becomes a cross-team event. Repeated enough times, this teaches teams to either move slowly or take risky shortcuts. That opens the next issue: even “read-only” consumers cause this problem.

### 4. Read-only access still creates real coupling, both structural and semantic.
Teams often think writes are dangerous but reads are harmless. Structurally, that is false because read queries still depend on tables and columns existing in a certain shape. If the producer normalizes a table, renames fields, or changes a type, readers break too.

More subtly, readers depend on what the data means, not just how it is shaped. A billing service that reads `status = 'completed'` is making a business interpretation, not just a technical one. If the order domain later distinguishes `completed`, `fulfilled`, and `partially_fulfilled`, the old reader may still run successfully while doing the wrong thing. This is more dangerous because structural mismatches often fail loudly; semantic mismatches often fail quietly. That brings us to the even worse case: shared writes.

### 5. When multiple services write the same data, ownership becomes ambiguous and invariants scatter.
If several services can update the same table or column, who is responsible for ensuring the data remains valid? In a single owned model, one place enforces rules like allowed state transitions. With multiple writers, each service either reimplements those rules, partially implements them, or assumes others will behave correctly.

The mechanism of failure is scattered authority. One service sets status to `pending`, another to `paid`, another to `shipped`. If no single owner controls the state machine, invalid transitions become possible. Not because any one service is obviously broken, but because the business rule is no longer enforced atomically in one place. Once you see that, the design requirement becomes clearer: a service boundary must include data ownership, not just code ownership.

### 6. Real service boundaries require each service to own its data and expose explicit interfaces instead of table access.
If a service owns its data, other services do not query its tables directly. They get what they need through something explicit: an API, events, or a replicated view. That makes the contract visible. Now the producer can decide what is public, how long compatibility is preserved, and how consumers should migrate.

This changes the type of coupling rather than removing coupling entirely. You cannot eliminate dependency between collaborating services; you can only choose a dependency shape that is visible and governable. That leads naturally to the next idea: the alternatives each trade one kind of coupling for another.

### 7. API calls trade hidden schema coupling for visible runtime coupling.
If Service B asks Service A for data through an API, Service B no longer depends on A’s internal tables. A can restructure its database freely as long as the API contract remains stable. That is a major improvement in encapsulation.

But now Service B depends on Service A being reachable and responsive at request time. The coupling has moved from build/deploy time to runtime. That is often a better trade because latency, timeouts, retries, and outages can be measured and mitigated directly. You can see them in dashboards. Hidden schema coupling usually shows up later, during a migration or incident. Still, for high-volume reads or join-heavy workflows, synchronous calls may be too expensive, which is why another pattern exists.

### 8. Event-based replication trades runtime dependency for eventual consistency.
Instead of calling the owning service every time, a consumer can receive events and keep a local copy of the data it needs. Now it reads from its own database and can shape that data for its own needs. This restores local query performance and removes the need for the producer to be up during each read.

The cost is lag. The local copy may be stale. That means some behaviors that were previously correct under shared strong consistency may now require redesign. The key mechanism is time: state changes propagate asynchronously, so two services can momentarily disagree. This is not a side issue; it directly changes what workflows are safe. If stale data can trigger harmful actions, those actions need guards, compensation, or redesigned sequencing.

### 9. Change data capture helps with migration, but it can leak the old coupling model back in.
CDC tools publish database changes by reading the database log, which is useful when you cannot easily change an existing service to emit proper domain events. That makes it a practical migration bridge away from a shared database.

But CDC events are often shaped like row mutations, not business facts. Consumers end up depending on table structure and low-level field changes, which partly recreates the original problem. The producer’s schema is still leaking outward, only now through an event stream instead of direct SQL. So CDC is often useful tactically, but less clean strategically unless carefully wrapped in a more stable domain contract.

### 10. The hard part is not only technical separation, but choosing the right boundary and paying the consistency costs consciously.
If you split data stores along the wrong lines, you create expensive cross-service joins and distributed workflows for things that should have stayed local. If you split along the right lines but ignore eventual consistency, you create correctness bugs in places that used to rely on immediate shared state.

That is why “every service gets its own database” is not a magic rule by itself. The deeper rule is: service boundaries must align with ownership and transactional reality. Data that changes together, is validated together, and is usually queried together often belongs in the same service. Once you split, you are choosing explicit contracts and weaker consistency in exchange for autonomy. That trade only makes sense if the boundary is real.

---

## Handles and Anchors

### 1. The database is not just storage; it is a contract surface.
If another service can see your tables, your schema is no longer an internal detail. That single sentence helps explain why “shared DB” is an integration decision, not a storage decision.

### 2. Shared database coupling is like letting other teams import your private classes directly.
It feels fast because they can reach exactly what they want. But now you cannot refactor internals safely, because your internals have become someone else’s dependency. A proper API is like a public interface; direct table access is like exposing private implementation details.

### 3. Ask this question: “If I rename this column tomorrow, who must coordinate?”
If the answer includes other services or teams, then that data is already a shared contract. This is a practical test for whether your architecture really has independent service boundaries.

---

## What This Changes When You Build

### 1. An engineer who understands this will treat cross-service table access as interface design, not convenience.
Instead of saying “we only need one query,” they will ask what contract is being created and who will own it over time. The unaware engineer inherits a direct SQL dependency because it is cheap today, then pays for it later in blocked schema changes and hidden consumers.

### 2. An engineer who understands this will separate “service boundary” from “deployment unit” and verify data ownership explicitly.
They will not assume separate repos and containers mean services are independent. They will ask: who owns writes, who enforces invariants, and can one team change internal representation without coordinating? The unaware engineer mistakes topology for autonomy and discovers the coupling only during migrations.

### 3. An engineer who understands this will design migrations as compatibility problems whenever a schema is shared, and will prefer to eliminate the sharing instead of normalizing the pain.
If they are stuck with a shared schema temporarily, they will use additive changes, backfills, dual reads/writes, and staged rollouts because they know direct changes are breaking changes. The unaware engineer treats schema changes as local refactors and creates production failures when downstream queries or assumptions break.

### 4. An engineer who understands this will choose between API access and event replication based on the failure they are willing to own.
If they need fresh authoritative data at request time, they may choose an API and accept runtime dependency. If they need local reads and independence, they may choose events and accept staleness. The unaware engineer often chooses ad hoc per-call shortcuts and ends up with both forms of pain: hidden schema coupling plus runtime fragility.

### 5. An engineer who understands this will place service boundaries around cohesive transactional domains, not around table names or org charts.
They will keep data together when it is validated together, changed together, and queried together. The unaware engineer may split too early or along the wrong line, forcing distributed joins, awkward sagas, and consistency bugs where a local transaction would have been enough.

---

</details>
