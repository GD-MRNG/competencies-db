## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams believe they have two options when a bad release hits production: roll back to the previous version, or fix the problem and ship a new version forward. They believe this is a decision they'll make in the moment, based on the severity of the issue and their best judgment under pressure. This belief is wrong in a specific and dangerous way. The choice between rollback and roll forward is not primarily a decision made during an incident. It is a consequence of architectural and operational decisions made weeks or months earlier. Teams discover this at the worst possible time — twenty minutes into an outage, when they attempt a rollback and find that it doesn't work, or decide to roll forward and realize their pipeline takes forty minutes. The gap between *having a philosophy* about bad releases and *having the mechanics in place to execute that philosophy* is where extended outages live.

The Level 1 post established the deployment strategies and introduced the expand-and-contract pattern for schema compatibility. This post is about the deeper question: what actually has to be true about your system for each strategy to work, why those preconditions are harder to maintain than they appear, and how to reason about which approach is viable in a given moment.

## What Rollback Actually Requires

Rollback sounds simple: deploy the previous version. But "deploy the previous version" is a description of what you want to happen, not a description of the mechanics. Here's what actually has to be true for a rollback to succeed.

### Artifact availability

The previous version's deployable artifact — container image, binary, package — must still exist in a registry or artifact store, tagged or referenced in a way that your deployment tooling can retrieve it without manual archaeology. This sounds trivial, but image retention policies, garbage collection on container registries, and ephemeral build outputs can quietly destroy this guarantee. If your CI pipeline builds artifacts on the fly and your previous version's branch has since been merged and deleted, you may not be able to reproduce it.

### Configuration compatibility

The previous version must be compatible with the *current* configuration and infrastructure state, not the configuration that existed when it was originally deployed. If you've rotated secrets, updated environment variables, changed service mesh routing rules, or modified infrastructure between the original deployment and now, the old artifact may not start cleanly. This is particularly insidious with infrastructure-as-code changes that are deployed independently of application code — the environment the old version expects may no longer exist.

### Data layer compatibility

This is the constraint that breaks most rollbacks. The Level 1 post covered the expand-and-contract pattern for schema migrations, but schema migrations are only the most visible form of state incompatibility. Consider what happens the moment a new version starts serving traffic: it begins writing data in formats the old version may not understand. New enum values in database columns. New fields serialized into JSON blobs. New message formats published to queues or event streams. Cache entries written with a new serialization layout. None of these require an explicit migration step — they happen as a natural consequence of the new code running.

A concrete example: your new version adds a `status` field to an order record with possible values `pending`, `confirmed`, and `waitlisted`. The old version doesn't know about `waitlisted`. You roll back. The old version reads an order with `status = waitlisted` and either crashes, silently drops it, or maps it to a default — all bad outcomes. Multiply this by every data path your application touches, and you begin to see the real surface area of the problem.

### Service compatibility in a distributed system

If you've deployed new versions of services A, B, and C together because they share a new API contract, rolling back A without rolling back B and C may create an incompatible constellation. Rolling back all three simultaneously is a coordination problem that most deployment tooling doesn't handle atomically. You end up with a period where some services are on the old version and some are on the new, which may be exactly the state that causes failures.

### The rollback window

These constraints combine to create an implicit **rollback window** — a period after deployment during which rollback is mechanically feasible. At the moment of deployment, the window is fully open: no state has been written by the new version, no downstream systems have adapted to its behavior. As time passes, state divergence accumulates, and the window closes. For a stateless API gateway, this window might be indefinite. For a service that writes to a database on every request, the window might be minutes. For a service that triggers an irreversible external side effect (sending emails, charging credit cards, publishing to a third-party API), the window is essentially zero for those specific operations.

The critical insight: **you don't choose when the rollback window closes. Your system's data flow determines it.** Teams that treat rollback as universally available are not accounting for the speed at which their system creates state that the old version cannot interpret.

## What Roll Forward Actually Requires

Roll forward means shipping a new version that fixes the problem introduced by the bad release. It sounds aggressive — you're deploying *more* code into an already-broken production environment — but it has one enormous structural advantage: it moves the system forward through a state that is compatible with the data already written. You don't have to reconcile old code with new data. You reconcile new code with new data, which is the direction the system was already heading.

But roll forward has its own hard requirements.

### Pipeline speed

Roll forward is bounded by your deployment pipeline's end-to-end time. If your CI/CD pipeline takes forty-five minutes from merge to production, then roll forward means forty-five minutes of continued impact (plus diagnosis time, plus fix authoring time). For teams with slow pipelines, roll forward is not a realistic incident response strategy — it's a strategy for non-urgent fixes. The teams that practice roll forward successfully typically have pipelines under ten minutes, and many have invested in **fast-path pipelines** — stripped-down build and deploy paths that skip non-essential validation steps for emergency fixes.

### Diagnosis under pressure

Roll forward requires you to understand the problem well enough to fix it while users are being affected. This is a fundamentally different cognitive challenge than rollback, which requires only the recognition that *something is wrong*. Roll forward demands root-cause identification (or at least sufficient understanding to write a correct fix) under time pressure, with incomplete information, often while also managing incident communication. The fix must be correct on the first attempt, because a second roll-forward iteration doubles the total time to resolution.

### Cultural and procedural permission

Many organizations have change approval processes, code review requirements, or deployment freezes that make shipping code during an incident procedurally difficult. If your roll-forward fix requires two approvals and a Jira ticket before it can merge, the organizational mechanics work against you. Teams that rely on roll forward need explicit **break-glass procedures** — documented, pre-approved paths for emergency deployments that bypass normal gates while maintaining an audit trail.

### Feature flags as a zero-deployment roll forward

The fastest possible roll forward isn't a deployment at all — it's a feature flag toggle. If the problematic code path was deployed behind a flag, you can disable it in seconds without touching the deployment pipeline. This is why the deployment-release decoupling described in the Level 1 post is not just a nice practice for gradual rollouts — it is an incident response mechanism. A feature flag turns a "roll forward" from a twenty-minute operation into a five-second operation. But this only works if the flag was in place *before* the problem surfaced. You cannot retroactively add a feature flag to code that's already broken in production.

## How Deployment Strategy Constrains Your Options

The deployment strategy you chose for the release directly determines the mechanics of both rollback and roll forward.

**Blue/green** gives you the fastest pure rollback: shift traffic back to the blue environment at the load balancer. But this only works if you haven't decommissioned or re-provisioned blue. Many teams tear down the idle environment after a stabilization period to save infrastructure cost. If the problem surfaces after that teardown, the "instant rollback" no longer exists. Blue/green also doesn't undo state changes — any writes to shared datastores during the green deployment's active period persist.

**Canary** gives you rollback for the canary population by routing their traffic back to the stable version. The blast radius is already limited, which buys you diagnostic time. But the canary's requests have already created state. If 2% of your traffic hit the new version and wrote data in a new format, you have 2% of your data in a state the old version may mishandle. Whether this matters depends entirely on what your service does with that data.

**Rolling updates** give you rollback, but it's another rolling update in reverse — it takes approximately the same amount of time as the original deployment. During the rollback, you again have a mixed fleet of old and new versions, which is exactly the condition that may have caused the problem in the first place.

## Tradeoffs and Failure Modes

The most common failure mode is **the assumed rollback**. A team deploys with the implicit assumption that they can roll back if anything goes wrong. They don't verify that the previous artifact exists, don't check schema compatibility, don't think about messages already published in a new format. Forty minutes into an incident, they attempt the rollback and discover it fails, or worse — it appears to succeed but introduces a second class of errors because the old code misinterprets the new data. They've now burned forty minutes and need to start the roll-forward process from scratch.

The second failure mode is **roll forward under panic**. A team decides to fix forward, writes a patch quickly under pressure, and ships it. The patch fixes the immediate symptom but introduces a subtle second bug. Now they're on their third version in an hour, the system's state is a product of all three, and reasoning about behavior becomes nearly impossible. Each successive emergency deployment layers more uncertainty.

The third failure mode is **the philosophical mismatch**. The team has a roll-forward culture but a rollback-speed pipeline — or a rollback assumption but a schema migration strategy that closes the rollback window on every deploy. The philosophy and the mechanics are misaligned, and the team doesn't discover this until the incident that reveals the gap.

A real scenario that illustrates the compounding problem: a team deploys a new version that introduces a background job processing orders into a new fulfillment workflow. The job runs for ten minutes before monitoring catches elevated error rates. By that time, three thousand orders have been processed through the new (buggy) workflow. Rolling back the code doesn't un-process those orders. Rolling forward with a fix addresses new orders but not the three thousand already affected. The actual recovery requires a data remediation script that someone has to write from scratch during the incident — a third category of work that neither "rollback" nor "roll forward" addresses. This is why the most prepared teams think not just about code versioning but about **data remediation runbooks** for their critical paths.

## The Mental Model

The choice between rollback and roll forward is not a runtime decision — it is a property of your system's architecture, your pipeline's speed, and your data model's compatibility guarantees. During an incident, you are not choosing a strategy. You are discovering which strategies are available to you based on decisions already made.

The single most important variable is **state**. Stateless operations can be rolled back trivially. The moment a new version writes state — to a database, a queue, a cache, an external system — rollback becomes a state reconciliation problem, not a deployment problem. The question to ask about any system is not "can we roll back?" but "how fast does our rollback window close, and what do we do after it's closed?"

Teams that handle bad releases well don't commit to one philosophy. They maintain the ability to do both, they know the constraints that determine which is viable in a given moment, and they've pre-decided the criteria before the incident starts.

## Key Takeaways

- **Rollback is not "deploy the previous version."** It is a claim that the previous version is compatible with the current state of your data, configuration, infrastructure, and dependent services. That claim must be verified, not assumed.

- **Every system has an implicit rollback window that begins closing the moment a new version serves traffic.** The speed at which it closes is determined by how quickly the new version creates state the old version cannot interpret.

- **Roll forward is bounded by pipeline speed plus diagnosis time.** If that total exceeds your tolerance for user impact, roll forward is not a viable incident response strategy — it's a cleanup strategy.

- **Feature flags are the fastest roll-forward mechanism because they require no deployment.** But they only work for problems in code paths that were flagged before the incident. They are a preparedness tool, not a reactive one.

- **Deployment strategy determines rollback mechanics, not just deployment mechanics.** Blue/green gives instant traffic rollback but doesn't undo state. Canary limits blast radius but still creates divergent state. Rolling updates roll back at the same speed they roll out.

- **The most dangerous failure mode is the assumed rollback** — the team that discovers mid-incident that the rollback they planned on is not mechanically possible, and has to switch strategies after already burning time.

- **Neither rollback nor roll forward addresses data already corrupted or state already changed by the bad version.** The third, often-forgotten category of incident work is data remediation, and it should be planned for explicitly on critical paths.

- **The decision between rollback and roll forward should be pre-decided based on system properties, not made under pressure during an incident.** Document which paths are rollback-safe, which require roll forward, and what the criteria are for choosing — before you need to choose.

# Discussion

## Why This Conversation Is Happening

When a release goes bad, teams often talk as if they have a clean emergency choice: “we’ll just roll back” or “we’ll fix it and roll forward.” In practice, that choice is often already constrained by the system itself. If the new version has written data the old version cannot read, rollback is no longer a simple deployment action. If the delivery pipeline takes forty minutes, roll forward may be too slow to stop user harm. The incident does not create these constraints; it reveals them.

What breaks when engineers miss this is not just speed, but recovery itself. A rollback can fail because the old artifact is gone, because configuration drift makes it unstartable, or because shared data has already changed shape. A rushed roll forward can compound the outage by adding another hurried patch to an already unstable system. And in many real incidents, neither option repairs the damage already done to state: orders have been misprocessed, emails sent, charges submitted, events published. If you do not understand the mechanics behind rollback and roll forward, you discover your real options only after production is already on fire.

## What You Need To Know First

**Deployable artifact**  
This is the thing you actually ship: a container image, binary, package, or build output. “Going back to the previous version” only works if that exact artifact still exists somewhere retrievable and your tooling knows how to deploy it. If your system rebuilds from source instead of storing artifacts, reproducing “the old version” may not be reliable.

**Stateful vs stateless behavior**  
A stateless component can handle a request without leaving behind meaningful memory of it. A stateful component changes something persistent: database rows, queue messages, cache entries, files, external side effects. This matters because rollback is easy when nothing durable changed; once the new version has changed state, rollback becomes a compatibility problem.

**Backward and forward compatibility**  
Backward compatibility means newer producers or formats do not break older consumers. Forward compatibility means older producers do not break newer consumers. For this article, the key idea is simple: can old code still function correctly when it encounters data, messages, or configuration produced by new code? If not, rollback has a short life.

**Deployment strategy**  
This is the way new code reaches production: blue/green, canary, rolling update, and so on. These strategies are not just release mechanics; they determine what rollback physically looks like. For example, blue/green can switch traffic fast, while rolling updates reverse more slowly and may leave a mixed-version fleet during recovery.

## The Key Ideas, Connected

**The choice between rollback and roll forward is mostly decided before the incident starts.**  
It feels like an operational judgment call made under pressure, but the article’s point is that your architecture, pipeline, and compatibility rules have already limited what is possible. During the incident, you are usually not inventing a strategy; you are discovering which strategies remain mechanically viable. That leads directly to the next idea: if rollback is not guaranteed, what does it actually require?

**Rollback requires much more than “the old code still exists.”**  
To roll back successfully, you need the prior artifact available, deployable, and compatible with the environment as it exists now. Not the environment from last week, but current secrets, infrastructure, routing, and service dependencies. This matters because teams often reduce rollback to version selection, when in reality it is a claim about compatibility across several layers. Once you see rollback as a compatibility claim, the next question becomes obvious: compatible with what?

**The hardest rollback constraint is compatibility with state created by the new version.**  
The moment new code serves traffic, it may write data the old code does not understand. That can be explicit schema changes, but more often it is ordinary runtime behavior: new enum values, new JSON fields, changed message shapes, new cache formats, altered workflow states. The mechanism is simple: the new code starts producing outputs according to its own assumptions, and the old code later has to consume those outputs using older assumptions. If those assumptions differ, rollback can fail or silently corrupt behavior. That dependence on changing state leads to the next idea.

**Because state accumulates over time, every deployment has a rollback window.**  
At deployment time, rollback is easiest because little or no new-version state exists yet. As requests flow through the system, more state diverges from what the old version expects, so rollback becomes less safe or impossible. The window closes quickly for systems that write on nearly every request, and almost immediately for irreversible side effects like payment captures or outbound emails. This is not a policy choice; it is produced by the system’s data flow. Once rollback becomes time-sensitive, the alternative strategy matters more.

**Roll forward works with the new state instead of trying to escape it.**  
That is its structural advantage. If the new version has already written data in a new shape, a corrected newer version can usually be written to understand that shape, because it is moving in the same direction as the system’s current state. Rollback asks old code to interpret new reality; roll forward asks newer code to repair and continue from new reality. But that advantage creates a new dependency: if fixing forward is your plan, you must be able to ship a fix fast enough to matter.

**Roll forward is limited by diagnosis time plus pipeline time.**  
Even if roll forward is architecturally safer, it may be operationally useless if your pipeline is slow or your incident process blocks emergency changes. The mechanism here is straightforward: users continue experiencing the issue until you understand it, implement a fix, validate it enough to trust it, and get it into production. If that path takes too long, roll forward becomes more like delayed cleanup than active incident response. This leads to a sharper version of preparedness.

**Feature flags are powerful because they turn some roll-forwards into configuration changes instead of deployments.**  
If the bad behavior sits behind a pre-existing flag, you can disable it immediately without rebuilding or redeploying. That shrinks recovery from minutes to seconds. But the dependence is strict: flags only help if they were designed in before the problem occurred. You cannot use a flag as an emergency escape hatch for code that was never made switchable. This generalizes into a larger point about deployment design.

**Deployment strategy shapes recovery mechanics, not just release mechanics.**  
Blue/green enables very fast traffic reversal if the old environment is still intact, but that does not erase database writes or external side effects. Canary limits how much traffic sees the bad code, buying time and reducing impact, but the canary slice can still create incompatible state. Rolling updates can reverse, but reversal takes time and may preserve the same mixed-version condition that caused problems. So deployment strategy is not just about “how to release safely”; it also determines “what kind of failure state you can get out of quickly.”

**Neither rollback nor roll forward repairs already-damaged state.**  
This is where many teams get surprised. If a buggy job processed three thousand orders incorrectly, rolling back only stops more bad processing; rolling forward only fixes future processing. The already-processed orders remain wrong. That is a different class of work: remediation. The mechanism is that code deployment controls future behavior, while persistent state stores the past effects of prior behavior. Once you separate those two, the article’s main model becomes clear.

**State is the variable that turns deployment problems into recovery problems.**  
As long as a release has not changed durable state, rollback can look like simple version management. Once state changes, recovery is about compatibility and reconciliation. That is why the right question is not “do we prefer rollback or roll forward?” but “how quickly does this system create irreversible or incompatible state, and what prepared path do we have once that starts happening?” That question ties together artifact retention, schema design, feature flags, pipeline speed, and remediation planning into one operational model.

## Handles and Anchors

**Handle 1: Rollback is not a button; it is a compatibility claim.**  
If you remember one sentence, make it this one. Saying “we can roll back” really means “the old version can still operate correctly against today’s data, config, dependencies, and side effects.” That is a much stronger statement than most teams realize.

**Handle 2: New code starts painting the world in its own colors.**  
The moment a release handles traffic, it changes records, emits messages, fills caches, and triggers workflows according to its own model of reality. Rolling back means asking old code to walk into that repainted world and still behave correctly. Sometimes it can. Often it cannot.

**Handle 3: Ask, “How fast does our rollback window close?”**  
This is a practical diagnostic question for any system. If the answer is “after a few writes,” “after a queue message,” or “immediately after we call an external API,” then rollback is much less available than your team may assume. If the answer is “this service is mostly stateless,” rollback may genuinely be easy.

## What This Changes When You Build

**An engineer who understands this will treat artifact retention as an incident-response dependency, not a housekeeping detail, because a missing prior artifact turns rollback from a plan into a fiction.**  
The unaware engineer inherits default registry retention or rebuild-from-source behavior and assumes “previous version” is always recoverable. They discover during an outage that the exact old deployable no longer exists or cannot be reproduced reliably.

**An engineer who understands this will design schema and message changes for compatibility over time, because rollback safety is mostly about whether old code can survive new state.**  
The unaware engineer adds enum values, changes event formats, or updates cache serialization in ways that seem harmless in isolated code review. The consequence is that the rollback window closes almost immediately after deployment.

**An engineer who understands this will evaluate deployment strategies partly by their recovery behavior, because blue/green, canary, and rolling update fail in different ways once bad code has touched state.**  
The unaware engineer chooses a strategy based only on rollout convenience or infrastructure cost. Then they are surprised that tearing down blue removes instant rollback, that canary still polluted shared data, or that rolling back a rolling update recreates mixed-version incompatibilities.

**An engineer who understands this will invest in pipeline speed and break-glass procedures if the team expects to roll forward during incidents, because a theoretically safe roll forward is useless if it takes too long to execute.**  
The unaware engineer says “we’re a roll-forward team” while living with long CI, mandatory approvals, and no emergency path. During an outage, that philosophy collapses into delay.

**An engineer who understands this will plan remediation for critical state transitions, because code recovery and state recovery are separate jobs.**  
The unaware engineer thinks only in terms of “revert” or “fix.” When bad code has already sent emails, charged cards, or advanced workflows, they must invent cleanup scripts and operational procedures in the middle of the incident, when time and confidence are lowest.
