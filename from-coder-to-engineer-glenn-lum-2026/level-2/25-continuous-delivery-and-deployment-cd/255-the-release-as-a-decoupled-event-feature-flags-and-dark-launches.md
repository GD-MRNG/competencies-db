## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams adopt feature flags as a simple idea: wrap new code in a conditional, toggle it on when you're ready. An `if` statement with a remote control. That mental model is accurate enough to get started and incomplete enough to cause real damage at scale. The gap is this: a feature flag is not a conditional in your code. It is a **runtime decision point** that creates an entirely separate control plane for feature activation — one that runs parallel to your deployment pipeline, has its own availability requirements, its own failure modes, and its own operational costs. Teams that treat flags as disposable conditionals end up with a system they cannot reason about: untestable state combinations, zombie flags that nobody dares remove, and a flag service whose outage takes down features that have been "fully released" for months. Understanding the actual mechanics — how flag evaluation works, how targeting and progressive delivery function under the hood, and what dark launches really require — is what separates using feature flags from being in control of them.

## How Flag Evaluation Actually Works

A feature flag, at the point of evaluation, needs to answer a question: for *this* context (this user, this request, this environment), should this code path be active? The mechanics of answering that question have significant implications.

The simplest implementation is a remote evaluation model: every time your application hits a flagged code path, it calls an external service that returns the flag's state. This is architecturally clean and operationally disastrous. Flag evaluations happen on hot paths — potentially every incoming request, potentially multiple times per request if several flags are in play. Adding a synchronous network call to each evaluation means your flag service's latency is now added to every flagged code path, and your flag service's availability is now a hard dependency for your entire application.

This is why production-grade flag systems use **local evaluation with a synced rule set**. The pattern works like this: the flag service maintains the canonical set of flag rules (targeting rules, percentage allocations, default values). An SDK embedded in your application periodically fetches this rule set — or receives it via a persistent connection like server-sent events — and caches it locally in memory. When your code evaluates a flag, the SDK resolves it locally against the cached rules. No network call per evaluation. Evaluation latency drops to microseconds instead of milliseconds.

The cost is **eventual consistency**. When you toggle a flag in the management interface, there is a propagation delay before all application instances have the updated rule set. For most use cases — releasing a feature, ramping a percentage rollout — a few seconds of propagation delay is irrelevant. For emergency kill switches, those seconds matter, and you need to understand what your propagation window actually is.

Every flag evaluation also needs a **default value** — what happens when the SDK cannot reach the flag service at all, when the cached rules have expired, or when the flag key doesn't exist. This default is not a formality. It is the behavior your system exhibits when your flag infrastructure is unavailable. If your default for a new, unreleased feature is `true`, a flag service outage releases the feature to everyone. Defaults should always be the *safe* state: for unreleased features, `false`; for kill switches, the "feature is enabled" state (so the kill switch only activates when you explicitly flip it, not when the flag service goes down).

## The Taxonomy of Flags and Why It Matters

Not all feature flags serve the same purpose, and conflating their types is the root cause of the most common operational failure: flag accumulation.

**Release flags** control the rollout of a new feature. They are born when the feature enters development, they are toggled on when the feature is released, and they should be **removed** shortly after. Their entire lifecycle should be measured in days to weeks. The code path behind a release flag is intended to become the only code path. The flag is scaffolding.

**Operational flags** (often called **kill switches**) give you runtime control over system behavior in production. They let you disable an expensive computation, shed load on a non-critical feature during an incident, or force a degraded mode. Unlike release flags, operational flags may be permanent. They are not scaffolding — they are circuit breakers built into your architecture.

**Experiment flags** control A/B tests or multivariate experiments. They route users into cohorts and must maintain consistent assignment for the duration of the experiment to avoid polluting results. Experiment flags have a defined lifecycle tied to the experiment's duration and analysis, but they carry additional requirements around assignment consistency and statistical validity that release flags do not.

**Permission flags** gate access based on entitlement — a user's plan tier, an account-level setting, a contractual agreement. These are effectively configuration, and they often persist indefinitely.

The reason this taxonomy is operationally important: release flags are the most numerous and the most dangerous to leave in place, because they contain dead code paths (the old behavior) that diverge further from the living codebase with every subsequent change. A release flag that remains in the codebase six months after the feature was fully released is not harmless. It is a conditional branch that nobody tests, that interacts with every subsequent change in the same area, and that will fail in unexpected ways when someone finally tries to remove it or accidentally toggles it.

## Sticky Targeting and Progressive Delivery

When you "roll out a feature to 5% of users," the mechanics of how that 5% is selected and maintained are non-trivial.

The naive approach — generate a random number on each request and activate the flag if it's below 0.05 — is wrong. A user refreshing the page would randomly oscillate between the old and new experience. For any feature with state or user-visible behavior, this is unacceptable.

Production systems use **deterministic hashing** for percentage-based targeting. The flag SDK takes a stable identifier (typically the user ID) and the flag key, hashes them together, and maps the hash output to a value between 0 and 100. If the user's hash value falls below the rollout percentage, they get the new experience. Critically, because the hash is deterministic, the same user always gets the same result for the same flag, regardless of which application instance serves the request. Increase the rollout from 5% to 20%, and the original 5% of users remain in the cohort — you're widening the bucket, not re-randomizing it.

This is what enables **progressive delivery**: the practice of incrementally increasing a rollout percentage while monitoring key metrics at each stage. You deploy the code. You enable the flag for 1%. You watch error rates, latency percentiles, and business metrics for that cohort. If everything is clean, you move to 5%, then 20%, then 50%, then 100%. At any point, you can set the percentage back to 0% and every user immediately reverts to the old behavior — no deployment, no rollback, no database migration concern. The toggle is a configuration change that propagates in seconds.

The nuance practitioners miss: the metrics you compare must be **segmented by flag state**. Watching your global error rate while 2% of traffic is on the new code path will not surface a problem — the 98% of healthy traffic will drown out the signal. Your monitoring must be able to answer: "What is the error rate *for users who are evaluating this flag as true* versus *those evaluating it as false*?" This requirement — flag-aware observability — is what separates teams that use progressive delivery from teams that think they use progressive delivery.

## Dark Launches: Running Invisible Code in Production

A dark launch is not the same as a feature that is flagged off. When a flag is off, the new code path does not execute. In a dark launch, the new code path **does execute** — but its results are not returned to the user. The old code path still serves the response. You are running both paths simultaneously: one is live, one is shadow.

The purpose is to observe the new code path's behavior under real production load: its latency characteristics, its error rates, its resource consumption, its output correctness — all with real traffic patterns that synthetic tests cannot replicate.

The implementation typically works like this: the application receives a request. It routes the request through the old (live) code path and returns that result to the user. Concurrently — or sequentially, depending on latency tolerance — it also routes the request through the new code path. The new path's result is logged, compared to the old path's result, and discarded. Metrics from the new path are emitted to your observability stack. If the new path throws an exception, it is captured and reported but does not affect the user's response.

The critical constraint is **side effects**. If the new code path writes to a database, enqueues a job, sends a notification, or calls an external API that charges money, you cannot simply run it in shadow mode without consequence. Dark launches require either that the new code path is read-only, or that its side effects are explicitly intercepted and neutralized. Common approaches include routing writes to a separate shadow database, wrapping external calls in no-op adapters during shadow execution, or structuring the dark launch to cover only the computation and comparison logic while deferring the write path to a separate, later rollout phase.

This constraint is why dark launches are most naturally applied to **read paths and computation**: a new search ranking algorithm, a new recommendation engine, a new pricing calculation, a new query optimization. You can compare the new output against the old output for every request and build statistical confidence that the new path is correct before you ever expose it to a user.

## Tradeoffs and Failure Modes

### Combinatorial State Explosion

Each boolean flag doubles the number of possible states your system can be in. Ten boolean flags produce 1,024 possible configurations. You will not test all of them. You cannot. The practical consequence: you must treat flags as having **minimal interaction**. Each flag should control an isolated code path that does not depend on the state of other flags. When two flags *do* interact — feature B only makes sense if feature A is enabled — that dependency must be explicit in the flag rules, not implicit in the code. Implicit flag dependencies are a category of bug that is nearly impossible to catch in testing and manifests only in the specific state combination that production happens to encounter.

### The Zombie Flag Problem

The most predictable failure mode of feature flags is accumulation. Teams add flags with discipline and remove them with negligence. Within a year, a codebase can accumulate hundreds of flags, the majority of which are release flags whose features were fully rolled out months ago. Each zombie flag is a branch in your code that makes the surrounding logic harder to read, harder to modify, and harder to test. The fix is not cultural ("let's be better about cleanup") — it is mechanical. Set expiration dates on release flags at creation time. Emit warnings or fail CI builds when a release flag exceeds its expiration. Treat flag removal as part of the feature's definition of done, not as a follow-up task.

### The Flag Service as Infrastructure

Once your system depends on feature flags for release control, the flag evaluation system is on the critical path. If you are using local evaluation with a synced rule set, the blast radius of a flag service outage is limited to the propagation of changes — existing cached rules continue to work. But if your caching layer has a bug, if the SDK's initialization fails on application startup, or if a bad rule set propagates that causes evaluation errors, you can experience widespread, correlated failures across every flagged code path simultaneously. The flag system deserves the same operational rigor — monitoring, redundancy, incident response — as any other infrastructure dependency.

## The Mental Model

A feature flag system is a **runtime routing layer** for feature activation. It is not a convenience wrapper around `if/else`. It is infrastructure that accepts targeting rules as input, evaluates them against request context on every relevant code path, and controls which version of your system's behavior any given user experiences. It runs parallel to your deployment pipeline: deployments put code on machines, the flag system decides which code paths are active for whom.

This means it carries the responsibilities of infrastructure: it needs availability guarantees, failure modes you have reasoned about, lifecycle management for the rules it evaluates, and observability that is aware of flag state. The decoupling of release from deployment is genuinely powerful — it transforms releases from irreversible deployment events into reversible configuration changes. But that power comes from operating a new system, not from adding conditionals to an existing one.

## Key Takeaways

- Feature flag evaluation should happen locally against a cached rule set, not via synchronous remote calls on every evaluation — the flag service's latency and availability should not be on the hot path of every request.

- Default flag values are not a formality; they define your system's behavior during flag infrastructure outages, and they should always resolve to the safe state (unreleased features off, kill switches inactive).

- Release flags, operational flags, experiment flags, and permission flags have fundamentally different lifecycles; treating them identically is the root cause of flag accumulation and technical debt.

- Percentage-based rollouts use deterministic hashing of user identity and flag key, not random sampling, so that users experience consistent behavior across requests and the rollout cohort is stable as percentages increase.

- Progressive delivery only works if your observability is segmented by flag state — watching global metrics while a small percentage of traffic is on a new code path will not surface regressions.

- A dark launch executes the new code path without exposing its results to users, which means it is only safe for read-only or side-effect-free paths unless you explicitly neutralize writes and external calls.

- Implicit dependencies between flags — where the behavior of one flag only makes sense given a particular state of another — are a category of bug that is nearly impossible to detect in testing and should be made explicit in flag rules.

- Flag removal must be enforced mechanically (expiration dates, CI checks, automated warnings), not culturally; no team sustains manual cleanup discipline across hundreds of flags over time.

# Discussion

## Why This Conversation Is Happening

Feature flags become popular because teams want to separate **shipping code** from **releasing behavior**. That sounds simple: deploy now, turn on later. But the moment you do that, you have introduced a new system that makes runtime decisions about what your application does for different users. If you still think of that system as "just an `if` statement," you miss where the real risk moved.

What breaks in practice is predictable. Teams put flag checks on hot request paths and accidentally make a flag service outage affect normal app behavior. They leave release flags in place for months, so the codebase quietly fills with stale branches nobody tests. They do percentage rollouts without stable targeting and users bounce between old and new experiences. They think they are doing safe progressive delivery, but their monitoring is too coarse to detect that the 2% on the new path is failing badly.

The result is a system that feels flexible but becomes hard to reason about. You can no longer answer basic operational questions with confidence: Which users are on which path? What happens if the flag service is unavailable? Can I remove this flag safely? If a rollout causes harm, can I see it quickly enough to stop it? This topic matters because feature flags are not merely a coding convenience; they are release infrastructure, and infrastructure has mechanics you have to understand.

---

## What You Need To Know First

**1. Hot path**  
A hot path is code that runs very frequently or sits directly in the request/response path where latency matters. If you add even a small amount of work there — especially a network call — you add that cost to lots of real traffic. Feature flag checks often sit on hot paths, so their evaluation method matters a lot.

**2. Caching and eventual consistency**  
Caching means keeping a local copy of data so you do not have to fetch it remotely every time. Eventual consistency means different machines may not see an update at exactly the same moment, but they will converge after some delay. In flag systems, local cached rules make evaluation fast, but toggles take a little time to propagate everywhere.

**3. Deterministic hashing**  
Hashing turns an input like `user_id + flag_key` into a numeric value in a repeatable way. Deterministic means the same input always gives the same output. That is what lets a rollout choose "the same 5% of users" every time instead of re-picking randomly on each request.

**4. Side effects**  
A side effect is any operation that changes state outside the current computation: writing to a database, sending an email, charging a card, enqueueing a job. This matters for dark launches because you can safely run extra computation in the background, but you usually cannot safely duplicate writes or external actions.

---

## The Key Ideas, Connected

**A feature flag is a runtime decision point, not just a conditional in code.**  
The important shift is this: the `if` statement in your code is only the final place where a decision gets applied. The real question is who decides and based on what information. In a flag system, that decision depends on rules managed outside the deployable application: rollout percentages, user targeting, environment settings, entitlements, kill switches. That means feature activation has been moved into a separate control plane that operates while the system is live. Once you see that, the next question becomes: how is that decision actually made at runtime?

**Runtime flag decisions must be evaluated in a way that does not put remote latency on every request.**  
If every flag check makes a synchronous call to a remote flag service, then your application inherits that service's latency and availability on every flagged code path. Since flagged code often runs per request, and sometimes multiple times per request, this is a direct performance and reliability problem. You have effectively inserted a network dependency into hot execution paths. That is why serious flag systems do not evaluate remotely each time. Once remote-per-check is unacceptable, you need a different mechanism.

**So production systems use local evaluation against a locally cached copy of the rules.**  
The flag service holds the canonical rule definitions, but the application SDK keeps a synced copy in memory and evaluates decisions locally. That changes the mechanics completely: the request path no longer waits on the network; it just applies local rules to the current context. Evaluation becomes fast enough to use freely. But this speed comes from accepting a trade: your local copy may be slightly out of date for a short time. That leads directly to the next idea.

**Local evaluation is fast because it trades strict immediacy for eventual consistency.**  
When someone flips a flag in the UI, not every application instance sees that change instantly. Rules propagate over polling or a streaming connection, and there is a delay. Usually that is acceptable: waiting a few seconds for a rollout to move from 5% to 20% is fine. But in an emergency kill-switch situation, those seconds define how quickly you can stop harm. So the mechanism matters: the same architecture that protects your hot path also creates a propagation window. Once you accept that rule updates are not instantaneous, you must decide what happens when rule data is unavailable or invalid.

**That is why default values are operational behavior, not a syntax detail.**  
A flag default is what your system does when evaluation cannot use the intended rule set: the SDK cannot initialize, the flag key is missing, the cache is stale, or the flag service is unreachable. In those moments, the default becomes the actual runtime behavior. So a default is not "just there to satisfy the API"; it is your outage posture. If an unreleased feature defaults to `true`, then flag infrastructure failure can release it globally. If a kill switch defaults to the wrong state, an outage changes incident behavior in exactly the wrong direction. Once defaults define failure behavior, you start to see that not all flags should be treated as the same kind of object.

**Different flag types exist because they solve different operational problems and therefore need different lifecycles.**  
A release flag exists to separate deploy from release for a short period. An operational flag exists to give production control during incidents or degradation. An experiment flag exists to maintain cohorts for measurement. A permission flag exists to encode who is entitled to what. These may all use the same evaluation machinery, but they are not interchangeable in purpose. That matters because if you treat them all as generic flags, you inherit the wrong cleanup behavior and wrong expectations. This is especially dangerous for release flags, which leads to the next point.

**Release flags are dangerous when left behind because they preserve dead alternative code paths.**  
A release flag starts as temporary scaffolding: old behavior and new behavior coexist until the rollout finishes. But once the new behavior is fully released, the old branch is no longer real product behavior; it is dormant code. If the flag remains, that dormant branch still affects readability, testing, and future changes. It drifts out of sync with the living code around it and becomes a latent bug source. This accumulation is not just "messy"; it changes the number of system states you have to reason about. And that becomes much worse once flags interact with targeting and rollout logic.

**Percentage rollouts only work safely if user assignment is stable across requests.**  
If you want to release to 5% of users, you need the same users to keep getting the new behavior. Otherwise a single user can see old-new-old-new across page loads or API calls, which is both a bad user experience and a source of state bugs. Random choice per request does exactly that, so it is the wrong mechanism. What you need is a stable mapping from identity to decision.

**Deterministic hashing provides that stable mapping and makes progressive widening possible.**  
By hashing a stable identifier together with the flag key, the system gets a repeatable numeric bucket for that user and flag. If the threshold is 5%, users whose bucket falls in that range get the feature every time. Raise the threshold to 20%, and the original 5% remain included while more users are added. That stability is what makes gradual rollout meaningful rather than chaotic. Once you can widen the rollout predictably, you can use rollout as an operational feedback loop.

**That feedback loop is progressive delivery: increase exposure in stages while observing real production behavior.**  
The sequence is: deploy the code, turn it on for a small cohort, inspect the results, then increase exposure if healthy. The key mechanism is reversibility without redeploy: because activation is controlled at runtime, you can move from 20% back to 0% quickly. But this only helps if your monitoring can distinguish users on the new path from users on the old path. Otherwise the small cohort's failures are diluted by healthy traffic from everyone else. So the rollout mechanism creates a measurement requirement.

**Progressive delivery depends on flag-aware observability because small-cohort failures disappear in aggregate metrics.**  
If 2% of traffic is broken and 98% is healthy, global error rate may still look fine. The signal is there, but averaged away. To use progressive delivery correctly, you need metrics and logs segmented by evaluation result: who saw the flag as true, who saw it as false, how each cohort behaved. That is not optional instrumentation; it is part of the mechanism that makes staged rollout safe. Once you understand that flags control routing at runtime, another technique becomes easier to place correctly: dark launching.

**A dark launch means executing the new path in production without letting it control the user-visible result.**  
A flagged-off feature simply does not run. A dark-launched feature runs, but in shadow mode: the old path still serves the user, while the new path is executed for observation. This lets you learn how the new path behaves under real load, with real inputs, before exposing it. The value comes from exercising code in production conditions while limiting user impact. But as soon as you execute the new path for real requests, one danger becomes immediate.

**Dark launches are constrained by side effects, because shadow execution is safe only if duplicate actions are neutralized.**  
If the shadow path writes to the production database, sends notifications, charges money, or calls mutable external systems, then "just run both" is no longer harmless. You are not only observing behavior; you are performing actions twice or performing actions that users never authorized. That is why dark launches fit read paths and pure computation best, and why write paths require special handling like shadow databases or no-op adapters. This is another example of the same pattern: the usefulness of the flag technique depends on the underlying mechanics of what the code actually does. Once many flags and rollout strategies are in use, one broad failure pattern emerges.

**Feature flags create a state-space problem, so interaction must be controlled deliberately.**  
Every boolean flag adds another branch of behavior. In theory, each additional flag doubles the number of possible configurations. In practice, you will never test all combinations, so safety depends on keeping flags isolated and making dependencies explicit. If feature B only works when feature A is enabled, and that dependency lives only in developers' heads or scattered conditionals, production will eventually encounter a broken combination. That is why stale release flags, implicit dependencies, and unbounded accumulation are not separate issues; they are all forms of losing control over the runtime state space your flag system creates.

**So the right mental model is: feature flags are a runtime routing layer with infrastructure responsibilities.**  
Deployments place code on machines. The flag system decides which behavior each request, user, or account gets at runtime. That means the flag system has to be treated like infrastructure: it needs sound evaluation architecture, safe defaults, lifecycle discipline, observability, and failure planning. The power of decoupling release from deployment is real, but it comes from operating this extra layer competently, not from sprinkling conditionals through the codebase.

---

## Handles and Anchors

**1. "A feature flag is a second control plane."**  
Deployment puts code in production; flags decide whether that code is active for anyone. If you remember only one thing, remember that flags are not part of the deploy step — they are a separate runtime system that can fail, lag, and require monitoring.

**2. Think of percentage rollout as seating assignment, not coin flipping.**  
You do not re-seat every passenger each time the plane takes off. You assign seats once using a stable rule. Deterministic hashing works the same way: it gives each user a stable place in the rollout so they do not bounce between experiences.

**3. Ask this question of any flag: "If the flag system disappeared right now, what behavior would users see?"**  
That question forces you to think about defaults, cached rules, outage behavior, and whether the chosen default is actually safe. It is a very fast way to tell whether the system is being treated as infrastructure or as a convenience.

---

## What This Changes When You Build

**An engineer who understands this will avoid synchronous remote evaluation on request paths because they know that turns the flag service into a latency and availability dependency for normal application behavior.**  
The unaware engineer may choose a clean-looking "ask the flag service each time" design and accidentally make every request slower and more fragile. The informed engineer looks for local SDK evaluation with cached rules and verifies how those rules are refreshed.

**An engineer who understands this will choose defaults based on failure behavior, not convenience, because they know defaults are what the system does during flag infrastructure problems.**  
The unaware engineer often treats the default as boilerplate. The informed engineer asks, "If evaluation fails, is `true` or `false` the safer outcome here?" That changes how unreleased features, kill switches, and permission gates are configured.

**An engineer who understands this will create and manage release flags as temporary scaffolding because they know long-lived release flags become dead branches that quietly increase state complexity.**  
The unaware engineer leaves old release flags in place "just in case." The informed engineer sets an expiration date at creation time, ties removal to the definition of done, and uses CI or automation to force cleanup before drift makes removal risky.

**An engineer who understands this will implement percentage rollout with deterministic identity-based assignment because they know random-per-request selection causes user-visible oscillation and invalidates staged rollout.**  
The unaware engineer may think "5% rollout" means "sample 5% of requests." The informed engineer knows it means "consistently assign 5% of users or accounts" and verifies the stickiness key, such as user ID or tenant ID, is stable and appropriate.

**An engineer who understands this will build flag-state-aware observability into rollout plans because they know aggregate metrics hide failures in small cohorts.**  
The unaware engineer turns on a feature for 1% and watches global dashboards that still look green. The informed engineer ensures metrics, logs, and traces can be filtered by flag evaluation result so regressions on the new path are visible before the rollout widens.

**An engineer who understands this will only dark launch code paths whose side effects are neutralized because they know shadow execution is safe for computation but dangerous for writes and external actions.**  
The unaware engineer may run both old and new paths and accidentally double-write, double-send, or incur real external cost. The informed engineer separates read/computation from write effects, or introduces shadow sinks and no-op adapters before attempting a dark launch.

**An engineer who understands this will design flags to be isolated and make dependencies explicit because they know the real scaling problem is the state space created by interacting flags.**  
The unaware engineer adds flags independently until odd combinations start failing in production. The informed engineer asks up front whether a new flag depends on another, whether the dependency belongs in targeting rules, and whether a different design would reduce combinatorial complexity.
