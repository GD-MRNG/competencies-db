## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers interact with feature flags at the surface: a function call that returns a boolean, a conditional that gates a code path, a toggle in a dashboard. This makes flags feel simple — they look like configuration. But the system behind that function call is doing substantially more work than most practitioners realize, and the operational consequences of that system's design show up in places that have nothing to do with the feature being flagged. The gap between "I use feature flags" and "I understand what my flag system is actually doing" is where incidents live. A flag isn't an if/else statement. It's a runtime decision engine with distributed state, evaluation semantics that depend on ordering and context, and a lifecycle that interacts with every deployment, rollback, and incident response process you have.

## How Flag Evaluation Actually Works

A feature flag check in your application code looks like a local function call:

```python
if flag_client.is_enabled("new-checkout-flow", user_context):
    render_new_checkout()
else:
    render_old_checkout()
```

What happens inside that call depends entirely on whether you're running a **server-side SDK** or a **client-side SDK**, and the difference matters.

A server-side SDK — the kind running in your backend services — typically connects to the flag management service on startup, downloads the entire set of flag definitions (rules, targeting configuration, percentage allocations, default values), and caches them locally in memory. Evaluation happens entirely within your process. When you call `is_enabled`, the SDK is not making a network request. It's evaluating the flag's rules against the context you passed in, using the locally cached configuration. This is why flag evaluation adds microseconds of latency, not milliseconds — there is no network hop in the critical path.

The SDK keeps this local cache current through one of two mechanisms: **polling** (fetching the full configuration on an interval, typically 30 seconds to a few minutes) or **streaming** (maintaining a persistent connection via SSE or WebSocket, receiving updates pushed from the flag service in near-real-time). Streaming gives you sub-second propagation of flag changes. Polling gives you simpler infrastructure at the cost of a propagation delay window where different instances of your service may be evaluating different versions of a flag's rules.

A client-side SDK — running in a browser or mobile app — works differently. You cannot ship your entire flag ruleset to the client, because it may contain targeting rules that reference other users' attributes, internal business logic, or information you simply don't want to expose. So client-side SDKs send the evaluation context (the current user's attributes) to the flag service, and the service returns the evaluated results for that specific context. This means client-side flag checks do involve a network call, or more precisely, they involve a network call on initialization, with the results cached locally for subsequent checks. The tradeoff: client-side evaluation depends on an initial fetch succeeding, and your application needs a strategy for what to render before that fetch completes.

Both models share a critical design property: **the flag service being unavailable should not break your application.** Server-side SDKs keep serving from their last-known-good cache. Client-side SDKs fall back to hardcoded defaults you provide at initialization. This means flag evaluation is eventually consistent by design. When you toggle a flag in your dashboard, the change does not take effect atomically across your fleet. It propagates over seconds (streaming) or minutes (polling), and any instance that can't reach the flag service continues operating on stale configuration indefinitely.

## Targeting Rules and Evaluation Order

A flag is not just an on/off switch with a percentage. It is a small rules engine. A typical flag definition has this structure: an overall kill switch (flag enabled or disabled), an ordered list of targeting rules, and a default rule that applies when nothing else matches.

Each targeting rule specifies a set of conditions evaluated against the **evaluation context** — the bag of attributes you pass in at call time. That context might include a user ID, an email domain, a country code, an account tier, a device type, or any other attribute your application knows at the point of evaluation. A rule says: "if the context matches these conditions, serve this variant."

The rules are evaluated top-to-bottom, and **the first matching rule wins**. This ordering is not incidental — it's the primary mechanism for expressing priority. A common pattern: the first rule targets a list of specific user IDs (your internal testers) and serves them the new variant. The second rule targets users in a specific region and serves them the new variant at 50%. The default rule serves the old variant. If you reorder the rules, your internal testers might fall into the regional rule instead, and half of them would see the old variant. The evaluation order *is* the logic.

This is where flags stop being configuration and start being code. The targeting rules are business logic expressed as data. They have the same properties as code — they can have bugs, they interact with each other, and the only way to understand what a given user sees is to trace the evaluation path through the full ruleset. A flag with six targeting rules and three variants is a decision tree. Treating it as "just a toggle" is how you end up debugging behavior that isn't in your source code.

## Percentage Rollouts and Consistent Hashing

When a targeting rule says "serve the new variant to 20% of users," the system needs to decide which 20%. The naive approach — generate a random number on each evaluation — fails immediately, because the same user would get different variants on successive page loads. Rollouts need to be **sticky**: a user who gets the new variant on their first visit must get it on every subsequent visit, without storing per-user assignments.

The standard solution is **deterministic hashing**. The SDK takes the flag key and the user's identifier, concatenates them, runs the result through a hash function, and maps the hash output to a value between 0 and 99. If that value falls below the rollout percentage, the user gets the new variant. Same inputs, same hash, same result, every time, on every server instance, with no shared state required.

```
hash("new-checkout-flow" + "user-7829") % 100 → 34
```

If the rollout is at 20%, user 7829 gets the old variant (34 ≥ 20). If you later increase the rollout to 50%, user 7829 now gets the new variant (34 < 50). Critically, every user who was already in the 20% cohort remains in the 50% cohort, because their hash values haven't changed and the threshold only moved in one direction. This **monotonic rollout** property means increasing a percentage never yanks the new experience away from someone who already had it.

The flag key is included in the hash input so that different flags assign different cohorts. Without it, the same 20% of users would be in the "on" group for every flag at 20%, which would make your "random" samples entirely correlated and your A/B test results meaningless.

One subtlety practitioners miss: percentage rollouts are only as good as your user identifier. If you're evaluating a flag before authentication and you don't have a stable user ID, you fall back to something like a session cookie or a device fingerprint. If that identifier changes, the user gets re-bucketed. This is a common source of inconsistent behavior in pre-login experiences.

## The Flag Configuration Surface

A single feature flag is trivial. The problem is that you don't have a single feature flag. A production system at any reasonable scale accumulates tens to hundreds of flags, and each flag with targeting rules is an independent axis of variation in your application's behavior.

Consider what this means for your system's configuration surface. If you have 15 active boolean flags, the theoretical state space of your application is 2^15: 32,768 possible combinations of behavior. Nobody is testing all of those combinations. Nobody is even enumerating them. In practice, many combinations are never exercised — but some of them are exercised, accidentally, by users who happen to fall into a particular intersection of targeting rules across multiple flags.

This is the mechanical reason flag interactions are dangerous. Two flags, each benign in isolation, can produce a broken experience in combination. The new checkout flow assumes a cart data structure that the new inventory display flag doesn't produce. Both flags work independently. Together, for the 3% of users who are in both rollout cohorts, the checkout page throws an error. This class of bug is invisible to unit tests, invisible to integration tests that toggle one flag at a time, and invisible to anyone reading either flag's targeting rules. It only exists in the intersection.

## Flag Lifecycle as an Operational Discipline

The Level 1 post mentioned that flags accumulate and need lifecycle management. The mechanics of *why* this is hard deserve examination.

A flag starts with a clear purpose: gate a feature rollout. The feature ships, the rollout reaches 100%, and the flag should be removed. But removal means: deleting the flag definition from the management service, removing every conditional in the codebase that references it, removing the old code path that is no longer reachable, and verifying that no other flag's targeting rules or no external system references this flag's key. For a flag that touches three services, this is a cross-team code change that requires coordination, review, and deployment. It is, in effect, a small project — and it delivers zero user-facing value.

This is why flags rot. The incentive to create a flag is immediate and strong (you need it to ship safely). The incentive to remove a flag is diffuse and weak (it makes the codebase marginally cleaner). Without a forcing function — a policy, a tech debt budget, an automated alert when flags exceed their planned lifespan — removal doesn't happen.

**Stale flags** are not inert. A flag that has been at 100% for eight months and that "everyone knows" is fully rolled out is still a conditional in your code. If someone accidentally disables it during an incident response — because they're toggling flags trying to isolate a problem and they don't recognize this one — they've just disabled a feature that has been in production for eight months. The blast radius of a stale flag is proportional to how long it has been at 100% without being removed, because that is how much production behavior silently depends on it.

The mechanical fix is **flag metadata and expiration**. Every flag should carry an owner, a creation date, an intended removal date, and a flag type (release flag, experiment flag, operational kill switch, permission flag). Operational kill switches — flags that exist permanently to allow you to disable an expensive code path during an incident — are explicitly long-lived and should be marked as such. Release flags should be aggressively expired. The tooling should surface flags past their expiration date as tech debt, ideally with the same urgency as a failing build.

## The Tradeoffs and Where It Breaks

**Evaluation latency is real on the client side.** If your flag service is slow or unreachable on first load, users see default behavior (typically the old variant) and then potentially flash to the new variant when the evaluated flags arrive. This **flicker** is not a cosmetic problem — it's a trust problem. Users see the interface rearrange itself. Solving this requires either server-side rendering with flag evaluation baked in, or a loading state that waits for flags before rendering — both of which add architectural complexity.

**Testing becomes a coverage problem.** You can't test every flag combination, so you need a strategy. The most practical approach is to test two states per flag — fully on and fully off — and to explicitly test known interactions between flags that affect the same user-facing surface. This is a judgment call, not an automated solution, and it requires that engineers actually know which flags are active and what they affect.

**Flag systems are invisible dependencies.** Your flag service is now in the critical path of every service that uses it (mediated by caching and defaults, but still). Your flag management dashboard is now a production control plane — anyone with access can change production behavior without a deployment, a code review, or an audit trail unless you've explicitly configured one. Treat flag changes as production changes. If your deployment pipeline requires approval and your flag dashboard doesn't, your controls have a gap.

**Debugging is harder.** When a user reports a bug, you need to know not just what code is deployed, but what flag state that user was evaluated against. This means logging flag evaluations per-request, or at minimum, being able to reconstruct a user's flag assignments after the fact. Without this, you're debugging with incomplete information about what code path was actually executed.

## The Mental Model

A feature flag system is a **runtime rules engine** that sits alongside your application code and governs which code paths execute for which users. It is not configuration in the way an environment variable is configuration. It is behavioral logic, expressed as data, evaluated at request time, and distributed across your infrastructure with eventual consistency semantics.

The critical conceptual shift is this: every active flag is a branch in your codebase that exists outside your source control, outside your test suite, and outside your deployment pipeline. The flag system is powerful precisely because it decouples these decisions from your release process — and it is dangerous for exactly the same reason. The discipline required to operate flags well is not about the tooling. It is about treating the flag inventory as production infrastructure that requires the same rigor you apply to your code and your deployments.

## Key Takeaways

- Server-side flag SDKs evaluate locally from a cached ruleset, adding microseconds of latency; client-side SDKs depend on a network fetch, which introduces latency, flicker, and a dependency on flag service availability at page load.

- Targeting rules are evaluated top-to-bottom with first-match-wins semantics — the order of rules is logic, not presentation, and reordering them changes behavior.

- Percentage rollouts use deterministic hashing of the flag key and user identifier, making assignments sticky without per-user storage and ensuring that increasing a rollout percentage never removes users from the existing cohort.

- The flag key is included in the hash input specifically to prevent different flags from assigning the same users to the same cohorts, which would make experiments and rollouts statistically correlated.

- With N active boolean flags, your application has 2^N possible behavioral states, and flag interaction bugs exist in combinations that no individual flag test will catch.

- Stale flags — flags that reached 100% and were never removed — are the highest-risk flags in your inventory because disabling them during incident response affects features users have depended on for months.

- Flag changes are production changes; if your flag dashboard allows changes without the same approval, audit, and rollback controls you require for deployments, your operational controls have a gap.

- Debugging user-reported issues requires knowing the flag state evaluated for that user at request time — if you aren't logging flag evaluations per-request, you are missing a dimension of observability that you will eventually need.

# Discussion

## Why This Conversation Is Happening

Feature flags are usually introduced as a safe way to ship: deploy code early, turn it on later, roll out gradually, and turn it off if something goes wrong. That promise is real, but it hides an important fact: once you adopt flags, you have added another production system that changes application behavior at runtime. If you treat flags as “just booleans,” you miss the mechanics that actually decide who sees what, when changes take effect, and what happens when the flag service is stale, slow, or misconfigured.

That gap shows up in very concrete failures. A rule reorder silently changes which users get a feature. A client-side flag fetch arrives late, so the UI renders one version and then flips to another. Two harmless-looking flags interact and break a flow for a small cohort no one explicitly tested. During an incident, someone disables an old flag they think is unused and accidentally turns off a feature that has effectively become part of the product. These are not “feature flag problems” in the abstract; they are consequences of not understanding the runtime system behind the toggle.

---

## What You Need To Know First

**1. Caching**  
A cache is a local copy of data kept so you do not have to fetch it from the original source every time. In feature flags, server-side SDKs usually keep a local cached copy of flag rules in memory. That matters because most flag checks in backend code are not network calls; they are local evaluations against cached configuration. The catch is that cached data can become stale.

**2. Eventual consistency**  
Eventual consistency means different parts of a distributed system may temporarily disagree, but they are expected to converge later. When you change a flag in a dashboard, not every service instance sees that change at the same instant. Some update immediately, some after a polling interval, and some may keep using old data if disconnected. So “I flipped the flag” does not mean “the whole system changed at once.”

**3. Deterministic hashing**  
A hash function turns an input into a repeatable numeric output. Deterministic means the same input always gives the same result. Flag systems use this to assign users to rollout buckets: if a given user hashes into bucket 34, they stay in bucket 34 every time. That is what makes percentage rollouts stable instead of random on each request.

**4. Evaluation context**  
The evaluation context is just the set of attributes you provide when asking for a flag value: user ID, country, account tier, device type, and so on. The flag system can only make decisions based on what is in that context. If an attribute is missing, unstable, or wrong, the flag may evaluate differently than you expect.

---

## The Key Ideas, Connected

**A feature flag check looks simple in code, but it is really a runtime decision made by a separate system.**  
`is_enabled("new-checkout-flow", user_context)` looks like a local boolean function, which encourages people to think of it as a normal conditional. But the call is really asking a rules engine, “given this flag definition and this context, which variant should this user get?” That matters because the behavior now depends not just on source code, but on external configuration, update propagation, and evaluation rules.

**Because the decision engine is external, how the SDK gets flag data determines latency and failure behavior.**  
On the server side, the common pattern is: download flag definitions, cache them locally, and evaluate in-process. That keeps runtime checks fast. On the client side, you usually cannot expose the full ruleset, so the client fetches evaluated results or context-specific flag data over the network. That means backend flag checks are usually cheap local reads, while frontend checks often depend on initialization timing and network success. Once you see that difference, the next issue becomes obvious: these systems will not all have the same view of flag state at the same time.

**Since SDKs rely on cached or fetched state, flag changes propagate with delay rather than atomically.**  
A server SDK may update through streaming or polling; a client SDK may fetch once and then cache locally. So when a flag changes, one instance may apply the new rules immediately while another continues using old ones. This is not a bug in the implementation; it is a consequence of designing the system to keep working even if the flag service is unavailable. The system chooses availability over instant global agreement. Once you accept that, you can understand a key operational truth: a flag is not just on or off globally; it exists in a period of rollout and propagation across your fleet.

**What gets evaluated during that propagation window is not just a toggle, but an ordered ruleset.**  
A flag definition usually contains an enable/disable state, a list of targeting rules, and a default fallback. The important part is that rules are checked in order, and the first match wins. That means rule ordering is not presentation; it is executable logic. A specific allowlist rule placed above a broad regional rollout behaves differently from the same two rules in reverse order. This leads directly to the next idea: if order and context determine outcomes, then a flag is behaving more like code than like static config.

**Because rules are ordered and context-dependent, flags are business logic expressed as data.**  
They encode decisions like “internal testers first,” “premium users in Canada next,” “everyone else off.” That logic lives outside the application codebase, but it still controls application behavior. Bugs can therefore exist entirely in the flag configuration: wrong ordering, missing conditions, overly broad matches, bad defaults. And because the decision depends on the evaluation context, understanding what happened for a user means reconstructing both the rules and the attributes supplied at evaluation time. Once flags are understood as logic, percentage rollouts stop looking like magic and start looking like another rule type that needs a precise mechanism.

**Percentage rollouts work by deterministic bucketing, not fresh randomness.**  
If “20% of users get the new feature” were implemented by random choice on every request, users would bounce between experiences. Instead, the system hashes stable inputs such as the flag key and user ID into a bucket, then compares that bucket to a threshold. If your bucket is 34, you are out at 20% and in at 50%. Because the bucket does not change, the user experience stays sticky. This mechanism explains why percentage increases are monotonic: raising the threshold adds new users without removing old ones.

**The hash includes the flag key so different flags do not accidentally choose the same users.**  
If bucketing were based only on user ID, the same users would land in the “on” cohort for every 20% rollout. That would correlate experiments and make rollout effects hard to interpret. Including the flag key changes the hash input for each flag, so each flag produces a different cohort. This sounds like a detail, but it reveals something bigger: once you have many flags, each one creates its own axis of behavioral variation.

**Many flags create a combinatorial configuration surface, and that is where interaction bugs come from.**  
One flag doubles the number of possible application states. Fifteen flags create thousands of theoretical combinations. Most are never tested directly, yet real users can land in some of them because each flag is evaluated independently. That is why two individually safe rollouts can fail together: one assumption from flag A collides with one assumption from flag B in a small overlapping cohort. The mechanism is not mysterious complexity; it is simple multiplication of runtime branches across the system.

**Because active flags multiply states, leaving old flags around is not harmless clutter.**  
A stale flag still represents a live branch in your production behavior, even if everyone “knows” it should always be on. It adds cognitive load, preserves dead code paths, expands the possible state space, and creates a dangerous control surface: someone can still toggle it. The older and more normalized that flag becomes, the more damage an accidental change can cause, because the product has come to depend on the “temporary” branch being permanently enabled.

**That is why flag management is an operational discipline, not just a coding convenience.**  
You need ownership, expiration, flag type, removal expectations, and controls on who can change what. A release flag should age out quickly; a true kill switch may intentionally remain. Without lifecycle discipline, your flag inventory becomes an unreviewed production control plane full of hidden branches. And once flags are part of production control, the next consequence follows naturally: observability and change governance must include flag state, not just deployed code.

**If flags alter runtime behavior outside deployments, debugging and change control must account for them explicitly.**  
When a user reports a bug, “what version was deployed?” is no longer enough. You also need “which flag rules were active for this user on this request?” Without that, you are debugging an incomplete execution path. Similarly, if engineers can change flag behavior instantly through a dashboard, then that dashboard is effectively a deployment mechanism. Treating it with weaker approval, audit, and rollback controls than code deploys leaves a real operational gap.

---

## Handles and Anchors

**1. “A feature flag is not an if-statement. It is a distributed rules engine hiding behind an if-statement.”**  
Use this when you need to reset your own thinking or explain the idea quickly to someone else. It captures the core shift from syntax to mechanics.

**2. Think of server-side flags like a local map with periodic updates, not live turn-by-turn directions.**  
Each service instance has its own copy of the rules and may be reading a slightly different version for a while. That makes it easy to remember why propagation is delayed and why “I changed the flag” does not mean “everyone sees the change now.”

**3. Ask this question of any flag system: “What exact inputs determine this user’s result, and can I reconstruct them later?”**  
If you cannot answer that, you probably do not really understand how the flag behaves in production, and you will struggle to debug rollout issues.

---

## What This Changes When You Build

**An engineer who understands this will design server-side and client-side flag use differently because the runtime costs are different.**  
The aware engineer knows a backend flag check is usually a local cache lookup, while a frontend flag may depend on an initialization fetch. So they will avoid putting client-side flags in places where a delayed fetch causes visible flicker or layout shifts, or they will add SSR/loading strategies deliberately. The unaware engineer assumes all flag checks are equally cheap and ends up with UI flashes and inconsistent first-load behavior.

**An engineer who understands this will treat rule order as executable logic because first-match-wins semantics make reordering behavior-changing.**  
They will review targeting changes the way they review code logic, asking which cohorts are shadowed by earlier rules and what the fallback really catches. The unaware engineer treats rules as a list that can be tidied for readability, and accidentally changes who gets the feature.

**An engineer who understands this will choose and validate stable identifiers for rollouts because stickiness depends on identifier stability.**  
They will ask, “what identifier exists at this point in the flow?” and “does it persist across sessions or pre-login states?” If not, they will expect rebucketing and inconsistent experiences. The unaware engineer uses whatever identifier is handy, then gets mysterious reports that users seem to move in and out of the experiment.

**An engineer who understands this will test around interacting user-facing surfaces, not just individual flags in isolation, because failures often live in intersections.**  
They will explicitly identify flags that can combine on the same page or workflow and test those combinations, especially around shared assumptions and data contracts. The unaware engineer flips one flag on and off in tests, declares coverage adequate, and misses the 3% cohort where two rollouts collide.

**An engineer who understands this will manage stale flags as operational risk because old release flags remain live control points.**  
They will add owners, expiration dates, and removal work to normal delivery practice, and they will distinguish permanent kill switches from temporary rollout flags. The unaware engineer leaves flags at 100% forever, slowly building a hidden inventory of branches that can still be toggled during an incident.

**An engineer who understands this will include flag state in observability because deployed code alone no longer explains runtime behavior.**  
They will log evaluated flag values or make them reconstructable per request, especially for high-risk flows. The unaware engineer debugs only from version numbers and request traces, then cannot explain why a user hit a code path no one can reproduce locally.

---
