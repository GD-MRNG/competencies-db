## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers can whiteboard all four deployment strategies in under a minute. Boxes, arrows, a load balancer in the middle. The descriptions are simple enough to fit on a slide. But the moment a deployment goes wrong — a memory leak that only manifests under real load, a schema change that breaks serialization for the old version, a canary that looks healthy on latency but is silently corrupting data — the whiteboard version falls apart. The gap is not in knowing what these strategies are. It is in understanding what each strategy makes *possible* and *impossible* during the fifteen minutes between "we started the deploy" and "we're confident it's good." That intermediate state — where your system is between versions, partially old and partially new — is where deployment strategy actually matters, and it is the part most descriptions skip entirely.

## The State Between Versions

Every deployment strategy is a set of rules governing a transition between two states: the system running version N, and the system running version N+1. The differences between strategies come down to three questions about that transition. First, how many versions of the application are running simultaneously, and for how long? Second, how much production traffic is exposed to the new version at each stage? Third, when something goes wrong, what is the mechanical path back to the known-good state, and how long does that path take?

These three questions — **version coexistence**, **traffic exposure**, and **rollback mechanics** — are the axes along which every deployment strategy makes its tradeoffs. The rest of this post walks through each strategy along those axes.

## Recreate: The Only Strategy With No Coexistence

Recreate is the simplest strategy and the only one where two versions of your application never run at the same time. The process is: stop all instances of version N, then start all instances of version N+1. There is a window of downtime between those two steps. No traffic is served during the gap.

This simplicity has a real benefit that is easy to overlook. Because version N is fully stopped before version N+1 starts, you never have two versions hitting the same database, the same cache, or the same message queue simultaneously. If your deployment includes a breaking schema change — renaming a column, changing a serialization format, altering the structure of messages on a queue — Recreate is the only strategy where that change does not require backward compatibility. Every other strategy creates a window where both versions must coexist, and coexistence with a shared data layer means both versions must understand each other's data.

Rollback is a full redeployment. If version N+1 is broken, you run the same process in reverse: stop N+1, start N. That takes as long as a fresh deployment. There is no fast path.

Recreate is appropriate for batch processing systems, internal tools where brief downtime is acceptable, and any situation where the cost of maintaining backward compatibility between versions exceeds the cost of a few seconds of downtime.

## Rolling: Coexistence as the Default State

In a rolling update, instances are replaced incrementally. The orchestrator (typically Kubernetes, an ASG update policy, or a deployment coordinator) takes down a subset of version N instances and brings up version N+1 instances to replace them. This repeats until all instances are running N+1.

Two parameters control the shape of this process. In Kubernetes, they are `maxUnavailable` and `maxSurge`. **maxUnavailable** is how many old instances can be taken down before new ones are ready. **maxSurge** is how many extra instances beyond the desired count can exist during the rollout. A configuration of `maxSurge: 1, maxUnavailable: 0` means: bring up one new instance, wait until it's healthy, then take down one old instance. Repeat. This is the most conservative option — capacity never drops below the desired count — but it is the slowest rollout and requires spare capacity. A configuration of `maxSurge: 0, maxUnavailable: 1` means: kill one old instance, then start one new instance in its place. No extra infrastructure needed, but capacity temporarily drops.

The critical characteristic of rolling updates is that **both versions serve production traffic simultaneously for the entire duration of the rollout**. If you have 20 instances and replace one at a time, there is a long window where some users hit version N and some hit version N+1. You do not control which users hit which version. Load balancers distribute traffic to all healthy instances, so the split is roughly proportional to the instance count — after replacing 5 of 20, roughly 25% of traffic hits the new version.

This has direct implications. If version N+1 changes an API response format, some clients will get the old format and some will get the new format during the rollout. If version N+1 writes data in a new structure, version N instances may read that data and fail to parse it. The rolling update does not protect you from these incompatibilities — it exposes you to them for the full duration of the rollout.

Rollback in a rolling update is mechanically identical to the original deployment: another rolling update, this time replacing N+1 instances with N instances. It takes approximately the same amount of time as the original rollout. If your rollout takes ten minutes, your rollback also takes ten minutes. There is no instant rollback in this strategy.

Health checks are the mechanism that gates progress. The orchestrator will not continue replacing instances if newly created instances fail their readiness checks. This is your safety net, but it is only as good as your health check. A health check that returns 200 from a `/health` endpoint while the application is silently writing corrupt data to the database will not stop the rollout.

## Blue/Green: Atomic Traffic Switching

Blue/green maintains two complete environments. Blue runs version N. Green is provisioned with version N+1. Once green is fully running and passing health checks, traffic is switched from blue to green at the routing layer — a load balancer rule change, a service mesh configuration update, or a DNS record swap.

The critical property is that the **traffic switch is atomic from the user's perspective**. One moment, all traffic goes to blue. The next moment, all traffic goes to green. There is no extended period of mixed-version traffic. (DNS-based switching is the exception here: DNS TTLs mean that some clients will continue resolving to blue for minutes or hours after the switch. For this reason, most production blue/green implementations use load balancer or reverse proxy switching, not DNS.)

Rollback is the strategy's strongest feature. If green is broken, you switch traffic back to blue. Blue is still running, still warm, still has its connection pools and caches populated. The rollback is as fast as the traffic switch — typically seconds, sometimes less.

But there is an important constraint that the simple description obscures: **both environments usually share a database**. You do not run two production databases. This means that even though traffic switches atomically, the data layer does not. While green is being validated before the switch, any writes green makes hit the same database blue is using. After the switch, if you roll back to blue, blue must be able to read any data green wrote during its brief time serving traffic. The schema compatibility requirement that rolling updates have for the duration of the rollout, blue/green has for the period between green going live and blue being decommissioned.

The infrastructure cost is real. During the deployment window, you are running 2x the compute capacity. If your service runs 40 instances, you need 40 more for the green environment. Some organizations keep both environments permanently, using one as a hot standby. Others spin up the green environment on demand. The cost depends on how long the second environment exists and whether your infrastructure supports rapid provisioning.

**Connection draining** is a detail that matters operationally. When traffic switches from blue to green, in-flight requests on blue instances need to complete. The load balancer must stop sending *new* requests to blue while allowing *existing* requests to finish. If your application handles long-running requests — file uploads, streaming responses, WebSocket connections — the drain timeout must account for them. A 30-second drain timeout will kill a file upload that takes 60 seconds.

## Canary: Controlled Traffic Exposure

A canary deployment routes a small, deliberate percentage of production traffic to the new version while the majority continues going to the old version. You start at a low percentage — 1%, 5%, 10% — observe the new version's behavior under real traffic, and either increase the percentage or abort.

What distinguishes canary from the other strategies is **explicit control over traffic exposure**. In a rolling update, traffic exposure to the new version is a side effect of how many instances have been replaced — you control instance count, and traffic exposure follows implicitly. In a canary, traffic exposure is the primary control. You decide exactly how much production traffic the new version sees, independent of how many instances are running it.

This control is implemented at the routing layer. A service mesh like Istio or Linkerd can split traffic by weight: 95% to the stable version's pods, 5% to the canary's pods. A load balancer with weighted target groups can do the same. The implementation matters because it determines the granularity of control. Instance-count-based splitting (run 1 canary instance alongside 19 stable instances for a roughly 5% split) is coarse and inexact. Traffic-weight-based splitting at the mesh or proxy layer is precise but requires that infrastructure to exist.

The canary's value is proportional to your ability to observe it. Sending 5% of traffic to the new version and then checking it manually an hour later captures some value. Automated metric comparison — comparing the canary's error rate, latency p99, and saturation against the stable version's baseline over the same time window — captures far more. Tools like Flagger and Argo Rollouts automate this loop: deploy canary, shift small traffic percentage, compare metrics for a defined bake time, promote or abort automatically based on thresholds. This is **progressive delivery**, and it transforms canary from a manual process into an automated feedback loop.

A failure mode specific to canary deployments is **insufficient traffic volume**. If your service handles 100 requests per minute and you send 1% to the canary, the canary receives one request per minute. You cannot draw statistically meaningful conclusions about error rates or latency distributions from one request per minute over a ten-minute bake time. For low-traffic services, canary percentages must be higher, or bake times must be longer, or both. The alternative is that the canary phase gives you false confidence — the metrics looked fine, but the sample size was meaningless.

Rollback is fast for the traffic that was going to the canary: you set the canary weight to 0%, and all traffic returns to the stable version. The blast radius of a bad canary is explicitly bounded by the traffic percentage. A canary at 2% that serves errors for five minutes affects 2% of your traffic for five minutes. The same bad version deployed via a rolling update with no canary phase would affect an increasing percentage of traffic over the entire rollout window.

## Where These Strategies Break

**The shared data layer is the universal complication.** Every strategy except Recreate involves two versions of your application running simultaneously for some period. If both versions read and write to the same database, cache, or message queue, the data they produce and consume must be mutually intelligible. A rolling update with a migration that renames a column from `user_name` to `username` will cause the still-running old instances to throw errors the moment the migration executes. Blue/green does not save you — green's migration changes the schema that blue is still reading. Canary does not save you either. The expand-and-contract pattern described in the Level 1 post is not optional for these strategies; it is a structural requirement.

**Rollback speed is not the same as recovery speed.** Blue/green gives you instant rollback, but if the bad version wrote corrupt data to the database during the minutes it served traffic, rolling back the code does not roll back the data. You are now running the old code against a database that contains data the old code may not expect. Rollback restores the code path, not the system state. Data remediation is a separate, often manual, process.

**Health checks gate rollouts but do not validate correctness.** A rolling update or canary that checks `/health` and gets a 200 will proceed even if the application is returning wrong results, charging incorrect amounts, or silently dropping events. The sophistication of your deployment safety is capped by the sophistication of your observability. A canary with automated metric comparison against error rates, business metrics, and latency distributions is fundamentally safer than a canary that only checks health endpoints, which is in turn fundamentally safer than a rolling update with no canary phase at all.

**Long rollout times create extended vulnerability windows.** A rolling update across 200 instances, one at a time, with a 30-second readiness check per instance, takes 100 minutes. For those 100 minutes, your system is in a mixed-version state. Any version incompatibility bug has 100 minutes to cause damage before the rollout completes. Increasing `maxSurge` shortens the rollout but increases the resource cost. This is a direct, linear tradeoff.

## The Model to Carry Forward

The deployment strategy you choose determines three things: how long two versions of your code coexist in production, how much traffic the new version receives before you have confidence in it, and how fast you can get back to the last known-good state when confidence fails. These three properties — coexistence duration, traffic exposure curve, and rollback latency — are the complete framework for reasoning about any deployment strategy, including hybrid ones you construct yourself.

Recreate eliminates coexistence entirely at the cost of downtime. Rolling updates spread coexistence across the full rollout window with traffic exposure that grows as instances are replaced. Blue/green minimizes the coexistence window and gives instant rollback but requires double the infrastructure and does not solve data-layer compatibility. Canary gives you explicit control over traffic exposure and bounds the blast radius of failures but demands real observability to justify its complexity.

No strategy eliminates risk. Each one moves risk to a different place. Your job is to know where each strategy puts the risk and decide which location you can best tolerate and monitor.

## Key Takeaways

- Every deployment strategy except Recreate runs two versions simultaneously, which means every deployment involving a shared database, cache, or message queue requires backward-compatible data changes — not as a best practice, but as a correctness requirement.

- Rolling updates offer no explicit control over traffic exposure; the percentage of traffic hitting the new version is a function of how many instances have been replaced, and you cannot target it precisely.

- Blue/green rollback is instant for traffic routing but does not undo any data written by the bad version — rollback restores the code path, not the system state.

- Canary deployments are only as valuable as the metrics you compare; a canary with no automated metric analysis and insufficient traffic volume provides false confidence, not safety.

- Rollback in a rolling update is itself another rolling update, meaning it takes approximately the same time as the original deployment — there is no fast rollback path.

- The blast radius of a bad deployment is determined by how much traffic the new version receives before the problem is detected; canary bounds this explicitly, rolling update bounds it implicitly by rollout speed, and blue/green has no partial exposure (it is all or nothing).

- DNS-based traffic switching in blue/green deployments is not atomic due to TTL caching; production implementations should use load balancer or proxy-level switching for reliable cutover and rollback.

- The safety ceiling of any deployment strategy is set by your observability, not by the strategy itself — a health check that returns 200 while the application serves incorrect results will not prevent a bad rollout from completing.

# Discussion

## Why This Conversation Is Happening

Deployment strategy sounds like a release-process choice, but it is really a failure-shaping choice. The hard part is not “how do I get new code into production.” The hard part is “what exactly happens while production is between versions, and what happens if the new version is wrong.” If you do not have a concrete model of that transition period, you make deployments that look safe on diagrams but fail in real systems.

What actually goes wrong is very mechanical. Old and new versions may both talk to the same database and disagree about schema or data format. A rollout may appear healthy because `/health` returns 200 while the app is silently corrupting data. A rollback may be “fast” for traffic routing but useless for undoing writes already made by the bad version. Engineers who only know the names — rolling, blue/green, canary, recreate — often miss that each strategy changes three real things: how long versions coexist, how much traffic the new code sees, and how long it takes to retreat.

If you do not understand those mechanics, you inherit hidden choices. You accidentally accept long mixed-version windows, uncontrolled exposure, or slow rollback paths without meaning to. Then when a deploy fails, the surprise is not that the code had a bug; the surprise is where the system allowed that bug to spread.

## What You Need To Know First

**Load balancer / traffic router**  
This is the component that decides which app instance receives a request. It can send traffic to any instance it considers healthy, and in some systems it can send weighted percentages to different versions. You need this idea because deployment strategies are mostly about changing where traffic goes over time.

**Readiness / health checks**  
A health check is how the platform decides whether a new instance is safe to receive traffic. A readiness check usually means “this instance is prepared to serve requests now.” The important limit is that health checks only prove what they test. If they only test “process is up,” they do not prove the app is correct.

**Shared data layer**  
This means multiple app versions use the same database, cache, or queue during deployment. That shared layer is where many deployment problems come from, because even if traffic routing is elegant, both versions still need to read and write data the other can understand.

**Backward compatibility in data changes**  
A change is backward-compatible when old and new versions can both operate correctly during the transition. For example, adding a new nullable column is usually easier than renaming an existing one immediately. You need this because every strategy except recreate usually creates a period where both versions exist at once.

## The Key Ideas, Connected

**A deployment strategy is really a way of controlling the transition between version N and version N+1.**  
The article’s main move is to stop treating strategies as labels and start treating them as transition mechanics. A deployment is not just “before” and “after.” There is an in-between state where production may contain both versions, partial traffic shifts, and possible retreat paths. That in-between state is where the strategy matters, so the next step is to describe the dimensions that define it.

**Those transition mechanics can be understood on three axes: version coexistence, traffic exposure, and rollback mechanics.**  
Version coexistence asks whether old and new run at the same time, and for how long. Traffic exposure asks how much real production traffic hits the new version at each moment. Rollback mechanics ask what you physically do to return to safety, and how long that takes. These axes matter because every named strategy is just a different combination of those three properties. Once you see that, you can analyze each strategy without memorizing four separate stories.

**Recreate is the only strategy that removes coexistence entirely, and that changes the compatibility requirement.**  
In recreate, you stop all old instances and then start all new ones. Because there is never a moment when both versions are active together, you avoid mixed-version interaction with shared systems. That means breaking schema or serialization changes can work here in a way they cannot safely work in rolling, blue/green, or canary. But removing coexistence creates downtime, and rollback is slow because recovery is just another full redeploy in reverse. So recreate trades availability for simplicity and compatibility freedom. That naturally sets up the next strategy, where you keep availability by allowing coexistence.

**Rolling updates keep the service available by replacing instances gradually, which makes coexistence the default state.**  
Instead of stopping everything, rolling updates swap instances in batches or one by one. That preserves service continuity, but now old and new versions serve real traffic at the same time for the full rollout duration. This is not a side detail; it is the defining mechanic. Because the load balancer sends requests to all healthy instances, some users hit old code and some hit new code, often with no explicit control over which. That means compatibility problems are no longer hypothetical edge cases — they are guaranteed to matter if your versions disagree about data formats, API responses, or queue messages. Once you accept that coexistence is long-lived, rollback also becomes slow, because rollback is just another rolling replacement.

**In rolling updates, traffic exposure is implicit, not directly controlled.**  
If 5 of 20 instances have been updated, roughly 25% of traffic lands on the new version. The exposure curve follows instance replacement progress. That means your blast radius is shaped by rollout speed and batch size, not by an explicit traffic policy. This leads to two consequences. First, rollout tuning parameters like `maxSurge` and `maxUnavailable` are not just performance knobs; they directly shape how long you live in a mixed-version world and how much traffic sees the new code. Second, because exposure is indirect, rolling updates are weaker when you want careful experimental release behavior. That gap leads to blue/green and canary, which control the transition more explicitly.

**Blue/green separates “new version is running” from “new version receives traffic,” allowing an atomic traffic switch.**  
Here you stand up a full green environment with N+1 while blue continues serving N. That means validation of the new environment can happen before the cutover. Then traffic switching happens at the routing layer in one step: all traffic goes from blue to green. From the user’s perspective, there is no long mixed-traffic period like there is in rolling. This gives the strategy its major strength: rollback is just switching traffic back, which is fast because the old environment is still alive and warm. But atomic traffic switching does not mean atomic system switching, because the database is usually still shared.

**Blue/green avoids mixed traffic for the app tier, but not mixed compatibility requirements for the data tier.**  
This is one of the most important corrections to the simplified mental model. People often think blue/green avoids compatibility problems because traffic only points to one environment at a time. But both environments usually depend on the same persistent state. If green writes data blue cannot read, then switching back to blue may fail even though the rollback itself is fast. So blue/green improves rollback latency at the routing layer, but it does not remove the need for backward-compatible data evolution. That observation makes a broader point: rollback speed and recovery speed are not the same thing.

**Fast rollback of traffic does not mean restoration of system state.**  
If bad code wrote corrupt records, charged users incorrectly, or emitted broken events, switching traffic back only stops further damage through that code path. It does not erase the damage already written into shared systems. This is why the article distinguishes code rollback from full recovery. Once you understand that, you stop over-crediting deployment strategies for solving problems they do not solve. That opens the door to canary, whose goal is not instant rollback alone but limiting how much bad traffic ever reaches the new version before you decide.

**Canary makes traffic exposure the primary control surface.**  
Unlike rolling updates, where exposure follows instance replacement, canary starts with a small chosen percentage of production traffic sent to the new version. The key idea is control: 1%, 5%, 10% are deliberate exposure limits, not side effects. This lets you bound blast radius explicitly. If the canary is bad, only the canary share was affected before you cut it off. Mechanically, this depends on routing infrastructure that can split traffic by weight, not just by whichever instances happen to exist.

**The value of canary depends on observability, because controlled exposure only helps if you can detect badness within that exposure.**  
A canary is not magic. Sending 5% of traffic to the new version is only useful if you have a way to compare its behavior against the stable version and decide whether to continue. If your checks only say “instance is alive,” then a canary can happily continue while producing wrong business outcomes. If your metrics are strong — error rates, latency tails, resource saturation, business counters — then canary becomes a real feedback loop. This is why progressive delivery matters: it automates the observe-decide-promote/abort cycle. But this introduces another constraint: enough traffic must reach the canary to make the observations meaningful.

**A canary with too little traffic can produce false confidence instead of safety.**  
If 1% of your traffic means one request per minute, then your “experiment” may be statistically useless. Low traffic means slow learning, weak signal, and a serious risk of promoting bad code because nothing obvious happened in a tiny sample. So canary is not automatically safer; its safety depends on sample size, bake time, and measurement quality. This reinforces the article’s broader claim that a strategy’s safety ceiling is set by observability and system mechanics, not by the name of the strategy.

**Across all strategies except recreate, the shared data layer is the universal complication.**  
This is the deepest unifying mechanism. If old and new versions coexist against shared storage or messaging, they must be able to understand each other’s outputs. That is why expand-and-contract migrations are a correctness requirement, not just a style preference. Renaming a column in one move breaks old readers the moment the schema changes. The exact routing strategy changes how traffic moves and how quickly you can back out, but it does not remove the coexistence problem at the data layer.

**So the real model is: each strategy moves risk, rather than eliminating it.**  
Recreate moves risk into downtime. Rolling moves risk into long coexistence windows and slow rollback. Blue/green moves risk into infrastructure cost and shared-data rollback limits. Canary moves risk into observability quality and statistical validity. This is the model to carry forward: ask where coexistence lives, how exposure grows, and how retreat actually works. Once you do that, deployment strategies stop being names on a slide and become operational tradeoffs you can reason about.

## Handles and Anchors

**1. “Deployment strategy is risk routing.”**  
Not “how do I ship code,” but “where does the risk go during transition?” Downtime, mixed-version compatibility, all-at-once cutover, or controlled partial exposure. If you can say where the risk sits, you understand the strategy.

**2. Think of the database as the part that does not switch cleanly.**  
Traffic can switch instantly. Containers can be replaced gradually. But shared data persists across all of it. If you remember only one failure source, remember this: the data layer is where old and new versions are forced to coexist even when your app routing looks neat.

**3. Ask this question of any rollout plan: “While old and new both exist, what must both versions successfully understand?”**  
That question immediately exposes hidden schema, cache, serialization, and queue compatibility assumptions. It is a practical test for whether the strategy’s transition state is actually safe.

## What This Changes When You Build

**An engineer who understands this will approach schema changes differently because deployment strategy does not protect shared data compatibility.**  
The aware engineer uses additive, backward-compatible migrations first, then code rollout, then cleanup later. The unaware engineer renames columns or changes message formats in one step because “we’re doing blue/green” or “Kubernetes will roll it safely,” and old instances fail as soon as they encounter new data.

**An engineer who understands this will treat rollback planning as a separate design problem from code deployment because code rollback does not restore data state.**  
They ask, “If this version writes bad data for three minutes, what is the remediation path?” The unaware engineer assumes blue/green means safe rollback and discovers too late that the old version cannot cope with records written by the new one.

**An engineer who understands this will configure rolling updates based on coexistence risk, not just cluster convenience, because rollout duration is exposure duration.**  
They see `maxSurge` and `maxUnavailable` as knobs that shape how long mixed-version behavior exists and how much capacity cushion they have. The unaware engineer leaves defaults in place, creating unnecessarily long rollouts and extended vulnerability windows.

**An engineer who understands this will invest in health signals that measure correctness, not just liveness, because rollout gates only stop on what they can detect.**  
They add canary analysis on error rates, latency distributions, and business metrics like failed checkouts or malformed writes. The unaware engineer relies on `/health == 200` and is surprised when a rollout completes successfully while serving wrong results.

**An engineer who understands this will choose canary only when they can support meaningful observation, because partial traffic without signal is theater.**  
They check whether the service has enough traffic volume, whether weighted routing exists, and whether they can compare stable versus canary behavior over a valid bake time. The unaware engineer copies canary from a high-traffic service to a low-traffic internal API and gains false confidence from meaningless sample sizes.
