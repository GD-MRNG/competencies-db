## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers encounter the three cloud pricing models — on-demand, reserved, and spot — as a dropdown menu or a line in a Terraform config. They appear to be three price tags for the same underlying resource: a virtual machine, a block of compute, a managed instance. Pick the cheaper one and move on.

This framing is wrong in a way that costs real money. On-demand, reserved, and spot are not three prices for the same thing. They are three different contracts that encode different assumptions about how your workload behaves over time, how much risk you're willing to absorb, and how your architecture responds to interruption. Choosing between them is not procurement. It is an architectural decision that propagates into how you design for failure, how you plan capacity, and what your system can tolerate when the contract's conditions activate.

The Level 1 post established that cost is an engineering responsibility and that architectural patterns have different cost profiles. This post explains the mechanics underneath the pricing models themselves — what you are actually purchasing in each case, why the discounts exist, and how the choice of pricing model constrains or liberates the systems you build on top of it.

## What the Cloud Provider Is Actually Selling

To understand the three models, you need to understand what the provider is optimizing on their side of the transaction. Cloud providers operate enormous fleets of physical hardware. Their fundamental economic challenge is **capacity utilization**: keeping as much of that hardware busy as possible, because idle servers cost them money (power, cooling, depreciation) without generating revenue.

The three pricing models are the provider's mechanism for segmenting demand by predictability.

**On-demand** customers are the least predictable. They spin up instances at arbitrary times, for arbitrary durations, and tear them down without notice. The provider must maintain enough spare capacity to serve this unpredictable demand, which means keeping servers idle as a buffer. On-demand prices are the highest because the customer is paying for optionality — the right to consume capacity at any time, for any duration, with no commitment. The premium you pay is the cost of the provider holding inventory for you.

**Reserved** customers are highly predictable. By committing to a specific quantity of compute for one or three years, they give the provider a demand signal that is stable enough to plan around. The provider can allocate capacity with confidence, reduce the buffer they need to maintain, and even make hardware purchasing decisions based on aggregate reservation commitments. The discount (typically 30% to 72% off on-demand, depending on the term length and payment structure) is the provider paying you for that predictability.

**Spot** customers absorb the provider's excess. At any given moment, some fraction of the provider's fleet is idle — reserved capacity that isn't being used yet, on-demand buffer that isn't needed right now, or capacity that was just freed by another customer. Spot pricing lets the provider sell this surplus rather than let it sit idle. The discount is steep (often 60% to 90% off on-demand) because the provider retains the right to reclaim that capacity with minimal notice when someone who is paying more needs it. You are buying leftover inventory, and you get a leftover-inventory price.

## On-Demand: No Commitment, No Constraints, No Discount

On-demand is the default. You request an instance, the provider provisions it from available capacity, and you pay a fixed per-hour (or per-second) rate for as long as it runs. There is no contract, no minimum, and no commitment beyond the current billing increment.

The non-obvious property of on-demand is that its simplicity is its cost. You are paying the highest rate not because the compute is better, but because you are giving the provider zero information about your future behavior. Every on-demand instance represents demand that could disappear in the next minute or persist for the next year, and the provider prices accordingly.

On-demand makes sense for workloads that are genuinely unpredictable: development environments, spike handling, short experiments, or any capacity you aren't confident you'll still need in three months. It also serves as the implicit baseline against which the other two models are measured. When someone says a reserved instance saves 40%, the comparison is always against on-demand.

The architectural implication is minimal. On-demand imposes no constraints on your system design. It doesn't shape how you handle failure or plan capacity. It simply costs more.

## Reserved: Commitment as a Financial Instrument

Reserved pricing is the most mechanically misunderstood of the three models. Engineers often think of it as "pre-purchasing" an instance — as if you are paying for a specific physical server that sits waiting for you. That is not what happens.

A reservation is a **billing construct**. When you purchase a reserved instance (or a savings plan, which is the more flexible evolution of the same concept), you are making a financial commitment to a certain volume of compute usage over a defined term. In return, any usage that matches the reservation's parameters is billed at the discounted rate instead of the on-demand rate. If you run matching instances, the discount applies automatically to your bill. If you don't, you still pay for the reservation.

This distinction matters because it reveals the core risk: **a reservation you don't use is more expensive than on-demand.** If you commit to a three-year reserved instance for a service that gets decommissioned after six months, you pay for the remaining thirty months of unused capacity. The discount only materializes as savings if your actual usage meets or exceeds the commitment.

### Payment Structures and Their Tradeoffs

Most providers offer three payment options for reservations: **all upfront**, **partial upfront**, and **no upfront**. The all-upfront option gives the deepest discount because the provider gets the entire payment immediately — they can invest that capital, and they bear no collection risk. Partial upfront splits the cost between an initial lump sum and a reduced monthly rate. No upfront spreads the entire cost across the term at a slightly higher rate, but still substantially below on-demand.

The choice between these is a capital allocation decision. All-upfront reservations produce the best unit economics but tie up cash and create the most painful write-off if the reservation goes unused. No-upfront reservations are less capital-efficient but more forgiving if your plans change, since the sunk cost at any point is lower.

### Savings Plans vs. Reserved Instances

AWS introduced Savings Plans as a more flexible version of reserved instances, and other providers have followed with similar constructs. A traditional reserved instance is scoped to a specific instance family, region, and sometimes availability zone. A savings plan commits to a dollar-per-hour spend rather than a specific instance type. If you commit to $10/hour of compute usage, any usage across eligible instance types in eligible regions is billed at the savings plan rate up to that threshold, and on-demand above it.

This matters architecturally because savings plans decouple the financial commitment from the infrastructure commitment. You can change instance types, migrate between regions, or refactor your service fleet without invalidating your cost savings — as long as your total compute spend stays at or above the committed level. This is a significant improvement for teams that expect their infrastructure to evolve over the commitment term.

### Scoping and Application

Reservations apply at the billing level, not the infrastructure level. A reserved instance for `m5.xlarge` in `us-east-1` doesn't attach to a specific running instance. It applies to any `m5.xlarge` usage in `us-east-1` across your account (or across your organization, depending on scope settings). This means reservations can float across instances as you scale up and down, which is useful — but it also means understanding where your reservations are applying requires reading the billing data carefully, not just looking at your infrastructure.

## Spot: Cheap Capacity with a Kill Switch

Spot instances are the model most likely to be underestimated in both their savings potential and their operational implications.

When you launch a spot instance, you receive a standard compute instance at a steep discount. That instance runs identically to an on-demand instance — same hardware, same performance, same networking. The difference is entirely in the contract: the provider can reclaim that instance with a **two-minute warning** (on AWS; the notice period varies by provider) whenever they need the capacity back for on-demand or reserved customers.

The two-minute window is not a grace period for you to find an alternative. It is a termination notice. Your workload gets two minutes to checkpoint state, flush buffers, deregister from load balancers, or do whatever it needs to do before it is forcibly shut down. If your application has not been designed to handle this, two minutes is nothing.

### What Drives Spot Reclamation

Reclamation frequency is not random. It is a function of supply and demand for a specific instance type in a specific availability zone. Popular instance types in busy regions get reclaimed more frequently. Obscure instance types or less popular zones may run for weeks without interruption. AWS publishes historical interruption frequency data by instance type, which is the single most useful signal for deciding whether spot is viable for a given workload.

This creates a non-obvious strategy: **instance type diversification**. Instead of requesting a single instance type, you configure your spot fleet to accept any of several instance types that meet your performance requirements. A workload that needs 8 vCPUs and 32 GB of RAM might accept `m5.2xlarge`, `m5a.2xlarge`, `m6i.2xlarge`, or `r5.2xlarge`. By spreading demand across multiple pools, you reduce the probability that all your instances get reclaimed simultaneously, and you increase the likelihood that at least one pool has available capacity.

### The Architectural Requirement

Spot is not a pricing option you apply to existing architecture. It is a pricing option that requires a specific class of architecture.

Workloads that run well on spot share common properties: they are **stateless** or can checkpoint and resume, they are **horizontally scalable** so that losing one node doesn't lose the whole job, and they either tolerate **partial results** during interruptions or have a mechanism to retry failed units of work. Batch processing, CI/CD builds, data pipeline stages, render jobs, and stateless web tier workers behind a load balancer are canonical examples. A singleton stateful database is not.

The critical design pattern is **graceful degradation on interruption**. Your system must detect the reclamation signal, stop accepting new work, complete or checkpoint in-progress work, and terminate cleanly — all within the notice window. This is real engineering work. It requires interrupt signal handlers, external state stores, and often a fallback to on-demand capacity to maintain availability during spot shortages.

## Where These Models Break and Where They Get Misused

**The unused reservation.** This is the most common and most expensive failure mode. A team purchases reserved instances based on current usage, then refactors a service, migrates to containers, or changes instance types. The reservations continue billing. At scale, organizations can accumulate hundreds of thousands of dollars in unused reservations. Mitigation requires either convertible reservations (which offer smaller discounts) or, preferably, savings plans scoped to flexible compute rather than specific instance types. It also requires a process — someone needs to monitor reservation utilization monthly.

**The unprotected spot deployment.** A team deploys a service on spot instances because of the cost savings, but the application has no interruption handling. When reclamation hits, requests drop, jobs fail, and the team scrambles. The savings evaporate into incident response time. Spot demands upfront investment in interruption-tolerant design; the cost savings are the return on that investment, not a free discount.

**The on-demand plateau.** Many organizations run entirely on on-demand for years because nobody has the mandate or the information to do anything else. This is not a failure of awareness — it is usually a failure of process. Reservation and spot decisions require usage data, forecasting, and ongoing management. Without a FinOps function or at least a designated owner, the default is the most expensive option.

**Overcomplicated blending.** Pursuing the theoretical optimum — the perfect mix of reserved, spot, and on-demand — can become its own cost center. Teams build elaborate automation to shift workloads between pricing models, maintain reservation portfolios, and track spot interruption rates. The operational overhead of managing this complexity sometimes exceeds the savings it produces, particularly for smaller-scale deployments where the absolute dollar difference is modest.

## The Model to Carry Forward

The three pricing models map to two axes: **time commitment** and **interruption tolerance**. On-demand sits at zero commitment and zero interruption risk — maximum flexibility, maximum cost. Reserved sits at high time commitment and zero interruption risk — you trade the ability to change your mind for a lower rate. Spot sits at zero time commitment but high interruption risk — you trade reliability for the lowest rate.

Every workload has a position on these two axes. A production database has near-zero interruption tolerance and predictable long-term demand — it belongs on reserved. A nightly batch pipeline can tolerate interruptions and doesn't need to run at a specific time — it's a natural fit for spot. A new service whose traffic patterns you don't yet understand belongs on on-demand until you have enough data to commit.

The mistake is treating pricing model selection as a finance exercise. It is an architecture exercise. The pricing model you choose constrains what your system can tolerate, and what your system can tolerate determines which pricing model is safe to use. These decisions compose: a fleet that is architecturally capable of spot can cut compute costs by 60% to 90%; a fleet that isn't will pay on-demand prices forever. The pricing model is downstream of the architecture, and the architecture should be upstream of the cost conversation.

## Key Takeaways

- On-demand, reserved, and spot are not three prices for the same product — they are three contracts that encode different assumptions about workload predictability and interruption tolerance.
- The cloud provider's discounts exist because predictable demand (reserved) and surplus absorption (spot) reduce the provider's own cost of maintaining idle capacity. The discount is not arbitrary; it reflects real value the customer provides to the provider.
- A reserved instance is a billing construct, not a physical allocation — it applies as a discount to matching usage on your bill, and unused reservations cost more than having bought nothing.
- Savings Plans decouple financial commitment from infrastructure commitment, making them more resilient to the architectural changes that frequently invalidate traditional reserved instances.
- Spot instances require architecture designed for interruption: stateless compute, external state, checkpointing, and graceful shutdown within the reclamation notice window. The discount is the return on that engineering investment.
- Instance type diversification across multiple spot pools is the primary mechanism for reducing correlated interruption risk in spot-based workloads.
- The most expensive failure mode at scale is not choosing the wrong pricing model — it is choosing none, defaulting to on-demand, and never revisiting the decision as usage patterns become clear.
- Pricing model selection is an architectural decision that should be made alongside decisions about fault tolerance, statefulness, and scaling strategy — not after the system is already in production.

# Discussion

## Why This Conversation Is Happening

Cloud pricing models look deceptively simple: the same VM, three different prices. That mental model leads teams to optimize for the sticker price instead of the contract. Then the real system pushes back. A team buys reservations, changes instance types six months later, and keeps paying for capacity they no longer use. Another team moves production workers to spot to save money, then learns during an interruption event that “cheap” also meant “can disappear in two minutes.”

What breaks is not just the bill. Architecture decisions get made under false assumptions. If you think reserved means “my instance is guaranteed,” you may misunderstand what protection you actually bought. If you think spot is just discounted compute, you may deploy stateful or interruption-intolerant workloads onto something the provider is explicitly allowed to reclaim. And if you never move past on-demand, you silently accept the most expensive contract forever, often because nobody translated usage predictability into an engineering decision.

The core reason to care is this: these pricing models encode different failure modes and different obligations for your system. If you don’t understand the mechanics, you either overpay for flexibility you don’t need, or you buy a discount whose conditions your architecture cannot survive.

---

## What You Need To Know First

**1. Capacity utilization**  
Cloud providers run huge fleets of physical servers, and idle hardware is expensive. If a machine is powered, cooled, and depreciating but not earning revenue, that is wasted capacity. Many pricing decisions make more sense once you see that the provider is trying to keep hardware busy while still preserving enough headroom for unpredictable demand.

**2. Stateless vs. stateful workloads**  
A stateless workload can be stopped and restarted somewhere else without losing important in-memory data; the durable state lives outside the instance, like in a database or object store. A stateful workload keeps important live state on the node itself, so interruption is much more dangerous. This matters because spot only works well when losing a machine does not mean losing the system.

**3. Horizontal scaling**  
Horizontal scaling means handling more work by adding more instances rather than making one machine bigger. A horizontally scaled service can often survive one node disappearing because other nodes keep serving traffic or processing jobs. That makes interruption-tolerant pricing models much more usable.

**4. Billing construct vs. resource allocation**  
A billing construct changes how usage is charged; it does not necessarily correspond to a specific machine being physically set aside for you. This distinction is crucial for reserved pricing. If you miss it, you will think you bought guaranteed infrastructure when you actually bought discounted billing for matching usage.

---

## The Key Ideas, Connected

**The three pricing models are different contracts, not different price tags for the same thing.**  
What changes between on-demand, reserved, and spot is not the CPU or memory itself. What changes is the agreement between you and the provider: how predictable your demand is, whether you commit in advance, and whether the provider can interrupt you. Once you see them as contracts, price differences stop looking arbitrary and start looking like payment for different kinds of flexibility and risk. That leads directly to the next question: why does the provider value those contract differences enough to charge so differently?

**The provider is optimizing for predictability and utilization of its hardware fleet.**  
The provider’s problem is not “how do I sell VMs?” but “how do I keep expensive hardware busy without failing demand spikes?” Unpredictable customers force the provider to keep buffer capacity idle just in case. Predictable customers let the provider plan. Interruption-tolerant customers let the provider monetize surplus that would otherwise sit unused. So the discount exists because the customer is helping solve the provider’s utilization problem. Once that is clear, each pricing model becomes understandable as a different way of reducing provider uncertainty.

**On-demand is expensive because you are buying maximum optionality.**  
With on-demand, you can start now, stop anytime, and make no promise about future usage. That freedom is valuable to you, but costly to the provider because they must be ready for uncertain demand patterns. The higher price is effectively the cost of the provider holding flexible inventory available for customers who refuse to commit. This means on-demand is the baseline model: least restrictive architecturally, but most expensive financially. Once you understand that, the logic of reserved pricing becomes clearer: if you remove some of that uncertainty, the provider can price lower.

**Reserved pricing is a discount in exchange for demand commitment, not a dedicated server waiting for you.**  
A reservation does not usually mean “this exact machine is mine.” It means “I commit to paying for a matching amount of usage over time, and qualifying usage gets billed at a lower rate.” Mechanically, that means the reservation lives in billing, not in your infrastructure topology. The provider likes it because your commitment makes future demand more legible; you like it because steady usage becomes cheaper. But this billing-based nature creates the next crucial implication: the risk is not interruption, it is mismatch.

**The failure mode of reserved pricing is unused commitment.**  
Because you are committing financially, not just accepting a runtime behavior, the danger is paying for usage that no longer exists or no longer matches the reservation. If you reserve one instance family and later migrate to another, your old commitment can keep billing while your actual runtime usage goes back to on-demand rates. This is why “reserved is cheaper” is only true when the workload remains stable enough to consume the commitment. That makes flexibility within the reservation itself important, which is where Savings Plans enter.

**Savings Plans exist because infrastructure changes faster than long-term financial commitments.**  
Traditional reserved instances can be too tightly coupled to specific shapes, regions, or scopes. But real systems evolve: services are containerized, instance families are upgraded, workloads move regions. Savings Plans relax the match rules by committing to a spend level rather than one precise infrastructure shape. Mechanically, this means the financial commitment survives more architectural change. That matters because it reduces the mismatch risk introduced by the previous idea. Once you have commitment handled, the other major discount path is not predictability but interruption tolerance.

**Spot pricing is cheap because you are agreeing to consume capacity the provider may reclaim.**  
Spot uses leftover or reclaimable capacity. The provider can sell it cheaply because they are not promising long-term availability; they keep the right to take it back when higher-priority demand appears. So the discount comes from accepting preemption risk. The machine behaves like a normal instance until the contract condition activates: interruption. That means the real question is no longer “is the compute good enough?” but “what happens to my workload when this node disappears?” That pushes us into architecture.

**Spot only works when the workload is designed so interruption is survivable.**  
If an instance can vanish with minimal notice, then the workload cannot depend on that instance being uniquely important. It must either be stateless, checkpoint progress externally, retry failed work, or spread work across many interchangeable nodes. The architecture must turn machine loss from a system failure into a routine event. Without that design work, spot savings are fake because they are paid back as incidents, dropped jobs, or data loss. Once interruption is accepted as a normal operating condition, the next problem is correlated interruption.

**Diversifying spot instance types reduces the chance that one supply shortage takes out everything at once.**  
Spot reclamation is tied to supply and demand in specific capacity pools: instance type plus location. If you depend on one narrow pool, a shortage there can wipe out your fleet. If your workload can run on several equivalent shapes, you can spread requests across multiple pools and lower the chance of simultaneous loss. The mechanism is simple: failures become less correlated because your fleet is no longer dependent on one constrained market. That leads to the broader framing that connects all three models.

**The real decision space is two-dimensional: commitment over time and tolerance for interruption.**  
Reserved asks, “How sure are you that you will keep needing this amount of compute?” Spot asks, “How okay are you with the provider taking nodes away?” On-demand sits at the corner where you commit to nothing and accept no interruption contract, so it costs the most. Reserved trades away future flexibility for lower price. Spot trades away runtime reliability for lower price. This framing matters because it shows pricing choice is downstream of workload behavior: if the workload is predictable, commitment becomes available; if it is interruption-tolerant, spot becomes available. That is why the article’s final conclusion follows naturally.

**Pricing model selection is an architectural choice because the contract changes what your system must tolerate.**  
A team does not merely “pick the cheapest option.” It chooses what risks are carried by the bill and what risks must be absorbed by the architecture. Reserved pushes risk into planning and lifecycle management. Spot pushes risk into runtime fault tolerance. On-demand pushes risk into ongoing cost. Once you see the mechanics this way, pricing stops being a procurement afterthought and becomes part of system design.

---

## Handles and Anchors

**1. Think of the provider as selling different promises, not different servers.**  
On-demand promises availability without commitment. Reserved promises lower pricing if you commit. Spot promises low pricing but no permanence. Same compute, different promises.

**2. One sentence to hold the tradeoff:**  
**Reserved saves money if your future is predictable; spot saves money if failure is routine.**

**3. A practical diagnostic question:**  
When looking at any workload, ask: **“If this instance disappeared in two minutes, what would actually happen?”**  
If the answer is “nothing important,” spot may fit. If the answer is “we’d lose live state or drop the service,” spot does not fit without redesign.

---

## What This Changes When You Build

**An engineer who understands this will separate baseline capacity from burst capacity because those two behave differently over time.**  
The steady portion of a workload is a candidate for reservations or Savings Plans because it is likely to exist next month and next year. The bursty portion is not, because committing to temporary peaks turns into unused reservation spend. The unaware engineer often reserves based on current total usage rather than stable minimum usage, then overcommits and carries dead spend after traffic patterns change.

**An engineer who understands this will evaluate reserved purchases against expected infrastructure change, not just today’s utilization graph.**  
If a service is likely to migrate instance families, move regions, or get folded into Kubernetes over the next year, a rigid reserved instance may be the wrong commitment even if today’s usage is stable. A more flexible Savings Plan may preserve most of the discount while surviving that change. The unaware engineer sees a larger discount percentage on a narrow reservation and takes it, only to invalidate it during the next platform migration.

**An engineer who understands this will design interruption handling before moving workloads onto spot.**  
They will add signal handling, draining from load balancers, checkpointing, retry semantics, and externalized state because the spot contract guarantees interruption is possible. The unaware engineer flips a node group to spot first and discovers during the first reclaim event that jobs were not idempotent, requests were dropped, or local disk state vanished.

**An engineer who understands this will diversify acceptable instance types and zones for spot fleets because interruption risk is pool-specific.**  
Instead of demanding one exact shape, they define a set of equivalent capacities the scheduler can choose from. That reduces correlated reclamation and improves spot availability. The unaware engineer pins to one popular instance type in one busy zone and concludes that “spot is unreliable,” when the real problem was concentration in a fragile pool.

**An engineer who understands this will assign ownership for commitment management because reserved savings decay without active maintenance.**  
Someone must review utilization, watch for orphaned reservations, and compare actual usage against committed spend. Otherwise the organization drifts: old commitments continue billing while workloads evolve. The unaware engineer assumes reservations are a one-time optimization, but reserved pricing is only efficient when continuously matched to live usage.

---
