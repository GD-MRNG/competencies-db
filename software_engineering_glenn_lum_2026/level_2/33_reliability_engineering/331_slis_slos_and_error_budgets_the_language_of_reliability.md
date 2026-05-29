## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams that adopt SLOs treat them as monitoring thresholds — a number goes red when reliability drops below a target. This misses the point entirely. An SLO that only triggers an alert is just a health check with extra steps. The actual value of the SLI/SLO/error budget framework is not that it measures reliability. You already have metrics for that. The value is that it converts reliability from a feeling into a *decision-making input* — a finite resource you can spend, track, and make policy around. The difference between "we should probably slow down on deployments" and "we have consumed 80% of our error budget with nine days remaining in the window" is the difference between a subjective argument and a quantified constraint. Understanding the mechanics of how SLIs, SLOs, and error budgets actually work — how they are defined, where they are measured, how they interact, and where they fail — is what determines whether this framework produces real engineering decisions or just produces dashboards.

## SLIs: The Ratio That Defines "Good"

An SLI is not a metric. It is a metric *expressed as a ratio*. Specifically, it is the ratio of good events to total events, measured over some time window. This distinction matters because raw metrics — request count, error count, latency — do not by themselves tell you whether your users are having a good experience. An SLI answers a specific question: of all the interactions users had with this system, what fraction were good?

**The definition of "good" is the entire design decision.** For an availability SLI, a good event might be any HTTP response that is not a 5xx. For a latency SLI, a good event might be any request that completes in under 300 milliseconds. For a correctness SLI, a good event might be any response where the returned data matches the source of truth. For a freshness SLI, a good event might be any read that returns data no more than one minute old. Each of these is a different SLI, with a different numerator, applied to the same denominator of total events.

### Where You Measure Changes What You Measure

The measurement point of your SLI is not a minor implementation detail — it fundamentally determines what your SLI captures. Consider an availability SLI for an API service. You can measure it at the load balancer, at the application server, or at the client.

If you measure at the **load balancer**, you capture failures from your application but miss failures caused by the load balancer itself, by network issues between the load balancer and the client, or by DNS resolution failures. If you measure at the **application server**, you miss everything upstream of it. If you measure at the **client** — through real-user monitoring or synthetic probes — you capture the full path that your user actually experiences, including network latency, CDN failures, and DNS problems. Client-side measurement is the most accurate representation of user experience but is also the noisiest, hardest to instrument, and most expensive to operate.

The general principle: **measure as close to the user as you can afford to maintain reliably.** For most backend services, measurement at the load balancer or API gateway is the practical sweet spot — it captures the vast majority of failures your users will see, and the data is clean and available in infrastructure you already control.

### Latency SLIs: Why Percentiles Are Non-Negotiable

Average latency is almost useless as an SLI. A service with 100ms average latency could be serving 95% of requests in 10ms and 5% in 1,900ms. The average looks fine. The experience for that 5% is catastrophic.

Latency SLIs use percentile thresholds: the fraction of requests faster than a given duration. A latency SLI might be defined as "the proportion of requests served in under 200ms" — and you would typically set separate SLOs for different percentiles. You might target 99% of requests under 200ms (your p99 latency SLO) and 99.9% under 800ms (your p999 SLO). The higher percentiles capture the tail latency that affects your worst-served users, who are often your most engaged users — the ones making the most requests.

The practical challenge is that latency distributions are almost always long-tailed, and the tail is where the interesting failures live: garbage collection pauses, cold cache misses, database lock contention, network retries. Your p50 tells you about the common case. Your p99 tells you about the failure modes.

## SLOs: The Threshold That Creates a Decision

An SLO is a target value for an SLI, applied over a specific time window. "99.9% of requests will return a non-5xx response over a rolling 30-day window." That sentence contains three components: the SLI definition (non-5xx responses), the target (99.9%), and the window (rolling 30 days). All three are load-bearing. Change any one of them and you change the operational behavior of the system.

### Why the Target Is Never 100%

This is well-trodden ground, but the *reason* matters for the mechanics that follow. A 100% SLO means zero tolerance for any failure, which means zero tolerance for any change — because any deployment, migration, or configuration change carries nonzero risk of causing a failure. A 100% target also means you are promising to be more reliable than any of your dependencies. If your cloud provider's compute SLA is 99.99%, your service cannot be 100% reliable unless you are multi-cloud with seamless failover, which introduces its own failure modes. The SLO target is the explicit, quantified answer to the question: *how much unreliability can our users tolerate before it materially harms their experience or our business?*

Deriving that number is not a pure engineering exercise. It requires understanding your users' actual tolerance — which is shaped by their alternatives, their expectations, and the criticality of the interaction. A payment processing API and an internal dashboard for viewing weekly reports have radically different user tolerance profiles, and their SLOs should reflect that.

### Rolling Windows vs. Calendar Windows

A **rolling window** (e.g., the trailing 30 days) means the error budget is continuously recalculated. A bad day that consumed significant budget three weeks ago will eventually "roll off" as time passes, naturally restoring budget. A **calendar window** (e.g., each calendar month) resets the budget at a fixed boundary — the first of the month, the start of the quarter.

The behavioral difference is significant. Calendar windows create a perverse incentive: if you've already blown your budget mid-month, there is no additional cost to further unreliability until the reset. Conversely, if you've been perfectly reliable for 28 days, you have a large unspent budget that vanishes in three days regardless. Rolling windows avoid both of these problems by making budget a continuous function. Most mature implementations use rolling windows.

## Error Budgets: The Currency of the Framework

The error budget is the gap between perfection and your SLO target, applied to your actual traffic volume. If your SLO is 99.9% availability over 30 days, your error budget is 0.1% of all requests in that window. If you serve 10 million requests per day, your 30-day error budget is 300,000 failed requests — or equivalently, roughly 43 minutes of total downtime.

This is not a monitoring number. This is an **allocation**. You are explicitly deciding that 0.1% unreliability is acceptable, and you are assigning that unreliability a concrete magnitude that everyone — product managers, engineers, leadership — can see and reason about.

### Burn Rate: The Speed of Consumption

The raw error budget remaining tells you how much budget is left. The **burn rate** tells you how fast you are consuming it, and this is the operationally useful signal.

A burn rate of 1x means you are consuming budget at exactly the rate that would exhaust it precisely at the end of the window. A burn rate of 10x means you will exhaust your 30-day budget in 3 days at the current rate. A burn rate of 0.5x means you are consuming budget slower than your allocation — you are "under budget."

Burn rate is what connects error budgets to alerting. Rather than alerting when the error rate exceeds a fixed threshold, you alert when the burn rate exceeds a multiple that implies the budget will be exhausted before the window ends. This is fundamentally different from threshold-based alerting because it is *contextual*: a 0.5% error rate that lasts for two minutes might be noise, but a 0.5% error rate that has persisted for six hours is a serious budget burn. Burn rate captures duration and magnitude together.

Practical implementations use **multi-window, multi-burn-rate alerts**. A fast burn (e.g., 14x over the last five minutes, confirmed by a 1-hour lookback) triggers a page — something is actively broken. A slow burn (e.g., 2x over the last six hours, confirmed by a 3-day lookback) triggers a ticket — something is degraded and needs investigation, but not at 3 AM. This structure dramatically reduces false positives compared to static error rate thresholds.

### When the Budget Runs Out

The error budget only has teeth if exhausting it triggers a concrete policy response. This is where the framework transitions from measurement to governance. Common policies when the error budget is exhausted include: freezing feature deployments until the budget recovers, redirecting engineering effort from feature work to reliability work, requiring all changes to go through additional review or canary stages, or escalating to leadership for a risk-acceptance decision.

The specific policy matters less than its existence and enforcement. An error budget with no exhaustion policy is just a metric. An error budget with an enforced exhaustion policy is a governance mechanism that automatically balances velocity and stability without requiring any individual to make a judgment call about whether "now is a good time to slow down."

## Where This Framework Breaks

### Measuring the Wrong Thing

The most common failure mode is SLIs that track system health rather than user experience. CPU utilization, memory pressure, queue depth — these are useful operational signals, but they are not SLIs. A service can be at 95% CPU and serving every request correctly in under 100ms. A service can be at 10% CPU and returning stale data to every user. If your SLIs are disconnected from what users actually experience, your SLOs will be green while your users are suffering, and your error budget will be meaningless.

### SLOs That Nobody Enforces

Many teams set SLOs, build dashboards, and then treat budget exhaustion as informational rather than prescriptive. When the budget runs out, nothing changes — deployments continue, priorities don't shift, and the SLO becomes a number that reflects past reliability but doesn't shape future behavior. This is the most common way the framework dies in practice. It requires organizational commitment to a policy, and that policy will, at some point, require telling a product team that their feature launch is delayed because the error budget is exhausted. If leadership overrides that decision every time, the framework is decoration.

### Goodhart's Law in Action

Once an SLI becomes a target, teams optimize for it — sometimes at the expense of the user experience it was supposed to represent. A team measured on availability SLI might add aggressive retries that keep the success ratio high but double the latency for failed-then-retried requests. A team measured on latency SLI might return fast, empty responses rather than waiting for slow backends to provide complete data. The SLI looks healthy. The user experience degrades. This is why mature implementations use multiple SLIs per service — availability *and* latency *and* correctness — to make it difficult to game one dimension without visibly degrading another.

### The Coverage Gap

SLOs only cover the interactions you instrument. If your SLI is defined at the API gateway, you have no coverage for failures that prevent requests from reaching the gateway — DNS outages, certificate expiration, network partitions between users and your edge. These are often the most impactful incidents (total outage, affecting all users) and the ones your SLO-based alerting is blind to. Synthetic monitoring — external probes that simulate real user interactions — fills this gap and should be considered a complement to, not a replacement for, event-based SLIs.

## The Mental Model

Think of the SLI/SLO/error budget system as a closed-loop control mechanism. The SLI is the sensor — it continuously measures the user-facing output of your system. The SLO is the setpoint — the threshold that defines acceptable. The error budget is the control signal — it translates the difference between actual and target into a quantified resource that drives action. When budget is ample, the system permits higher velocity: more deployments, more experiments, more risk. When budget is thin, the system constrains velocity: slower rollouts, more review, reliability-focused work. The output is not a dashboard. The output is an engineering decision — deploy or don't deploy, invest in features or invest in reliability — made against a quantified constraint rather than a subjective feeling.

What makes this framework powerful is not its precision — the specific numbers are always somewhat arbitrary. What makes it powerful is that it forces reliability to be *negotiated and explicit*. The moment you write down "99.9% over 30 days," you have committed to a definition of good enough, and every minute of downtime, every elevated error rate, every slow response is now countable against a finite budget that everyone in the organization can see. Reliability stops being the thing that one team argues about in incident reviews and becomes the quantified constraint that shapes how the whole organization ships software.

## Key Takeaways

- An SLI is not a metric — it is the ratio of good events to total events, where the definition of "good" is the design decision that determines whether the SLI actually reflects user experience.

- Where you measure your SLI (client, load balancer, application) determines what failures it can see; measure as close to the user as you can reliably maintain.

- Average latency conceals tail behavior; latency SLIs must use percentile thresholds (p99, p999) to capture the experience of your worst-served users.

- Rolling time windows are generally superior to calendar windows because they avoid the perverse incentive of budget resets and budget-expiration waste.

- Burn rate — not raw budget remaining — is the operationally useful signal, because it captures both the magnitude and duration of an issue and enables tiered alerting (page for fast burns, ticket for slow burns).

- An error budget without an enforced exhaustion policy is just a metric; the framework only produces decisions if exceeding the budget triggers concrete, pre-agreed consequences.

- Multiple SLIs per service (availability, latency, correctness) guard against Goodhart's Law — optimizing one dimension at the expense of others becomes visible.

- SLO-based alerting has a coverage gap for failures that prevent requests from reaching your instrumentation; synthetic monitoring from external vantage points is the necessary complement.

# Discussion

## Why This Conversation Is Happening

Reliability is easy to talk about badly. Teams often say things like “the service seems stable” or “we should probably be more careful with deploys,” but those are judgment calls, not operating rules. When reliability is handled as a feeling, every release becomes a negotiation: product wants to ship, engineering is nervous, and nobody has a shared way to decide whether the system can absorb more risk. The result is usually one of two bad defaults: either teams move too cautiously and slow down unnecessarily, or they keep shipping through visible degradation until users force the issue.

What breaks in practice is not just uptime — it is decision quality. Alerts fire on thresholds that do not map to user pain. Dashboards are green while users are failing at the edge. Teams burn time arguing about whether an incident was “bad enough” to halt launches. And when reliability targets exist but have no policy attached, they become retrospective scorecards rather than something that changes behavior. The SLI/SLO/error budget framework exists to turn reliability into something operational: measurable in a user-relevant way, bounded over time, and tied to specific actions when the system is spending too much reliability.

---

## What You Need To Know First

**1. Metrics vs. user experience signals**  
A metric is just a measurement: error count, latency, CPU usage, request volume. Useful, but incomplete. To reason about reliability, you need a measurement that says something about whether users actually got acceptable service. The article’s core move is to distinguish raw internal measurements from signals that represent “how often did the user get what they needed?”

**2. Time windows**  
Most reliability claims are not about a single instant; they are about performance over some span of time. “99.9% over 30 days” means small failures may be acceptable, but only up to a limit within that window. The choice of window matters because it changes how quickly past failures stop affecting current decisions.

**3. Percentiles**  
A percentile tells you how the worst part of a distribution behaves. If p99 latency is 200ms, that means 99% of requests are faster than 200ms and 1% are slower. This matters because averages hide tails. In systems work, the tail often contains the real failure modes users notice.

**4. Feedback control as a mental model**  
A control system measures some output, compares it to a target, and adjusts behavior based on the gap. You do not need formal control theory here — just the idea that measurement is only useful if it feeds action. That is the shape of the SLI/SLO/error budget system: measure, compare to target, change operating behavior.

---

## The Key Ideas, Connected

**1. An SLI is a ratio of acceptable outcomes, not just any metric.**  
The important distinction is that an SLI answers: “Out of all the things users tried to do, how many were good?” That ratio structure matters because reliability is about the fraction of interactions that met a standard, not about isolated raw counts. Ten errors means something very different in a thousand requests than in a hundred million requests. Once you define reliability as a ratio, you are forced to define what counts as “good,” which leads directly to the next idea.

**2. The definition of “good” is the real design decision in an SLI.**  
A request can be “good” because it returned without a 5xx, or because it finished under 300ms, or because it returned correct and fresh data. Those are different user promises. This is why an SLI is not mechanically extracted from existing telemetry; it is chosen. If you choose badly, you can measure the system accurately and still learn the wrong thing. That makes measurement location important, because even a good definition of “good” can become misleading if you observe it from the wrong place.

**3. Where you measure the SLI determines which failures are visible.**  
If you measure at the app server, you only see what reaches the app server. If DNS is broken, the user cannot connect, but your app-side SLI may still look perfect because no bad requests arrived there to be counted. If you measure at the load balancer, you see more of the path, but still not everything the user experiences. If you measure at the client, you capture the real path but inherit more noise and operational complexity. The mechanism here is simple: an instrument can only observe failures downstream of where it sits. That is why “measure close to the user” is not a slogan; it follows from what failures each vantage point can and cannot see. Once you have a visible ratio measured from some vantage point, you can set a target on it.

**4. An SLO is an SLI plus a target plus a time window.**  
An SLO is not just “99.9%.” It is a specific promise about a specific user-relevant ratio over a specific span of time. Remove the window, and you cannot say when the promise has been kept or broken. Remove the SLI definition, and you do not know what is being promised. Remove the target, and there is nothing to compare performance against. This combination is what turns measurement into a standard. That standard cannot be 100% in realistic systems, which brings in the next idea.

**5. The target is below 100% because change and dependencies introduce unavoidable risk.**  
A 100% target means any failure is unacceptable, which effectively means no risk-taking is acceptable. But deployments, migrations, dependency outages, retries, failovers, and configuration changes all carry nonzero failure probability. Also, your service cannot usually be more reliable than the chain it depends on without substantial extra architecture. So the SLO target is really an explicit answer to: “How much unreliability is acceptable before users or the business are materially harmed?” Once you accept less than perfection, you have created a gap between perfect service and acceptable service. That gap is the error budget.

**6. The error budget is the allowed amount of unreliability implied by the SLO.**  
If your target is 99.9%, the missing 0.1% is not an accident — it is the amount of failure you are allowing yourself. This is the conceptual shift the article cares about most. Instead of treating failure as something vaguely bad, you treat a bounded amount of it as spendable. The budget is finite and depletes as bad events accumulate. That makes reliability legible as a resource, but a raw amount remaining is still not enough to operate on moment to moment. You also need to know the speed of consumption.

**7. Burn rate tells you whether the current failure pattern is dangerous.**  
A remaining budget number is static: it says how much room you have left. Burn rate is dynamic: it says how quickly you are eating that room. The mechanism is what makes it useful: the same instantaneous error rate means different things depending on how long it persists. A brief spike may be irrelevant; a sustained smaller issue may exhaust the whole window. Burn rate combines severity and duration into one operational signal. That is why it works better for alerting than fixed thresholds — it asks not just “is the error rate elevated?” but “at this pace, are we on track to run out of tolerated unreliability too soon?” Once alerting is based on budget consumption, the framework is ready to drive behavior.

**8. The framework only works if exhausting the budget changes what the organization is allowed to do.**  
Without an attached policy, an error budget is just a descriptive number. The mechanical point is important: the budget is supposed to close a loop. If the budget gets low or reaches zero, deploy policy, review rigor, rollout speed, or engineering priorities should change. Otherwise, no control action occurs and the system is open-loop — it observes reliability but does not regulate behavior with it. This is why teams with dashboards but no enforcement get very little value. But even with enforcement, the framework can still fail if the measured signal does not match actual user value.

**9. The framework breaks when the SLI is gameable, incomplete, or disconnected from user experience.**  
If you measure CPU, you are not measuring user experience at all. If you measure only availability, teams can preserve the success ratio while harming latency or correctness. If you measure only at the gateway, outages before the gateway remain invisible. These are not edge cases; they come directly from how targets shape behavior. Once a number becomes a target, teams optimize for it. That is Goodhart’s Law in system form. The response is not to abandon SLOs, but to design them more carefully: use multiple SLIs for different dimensions of user experience and complement internal event-based measurement with synthetic checks that cover blind spots.

**10. The full system is a control loop for balancing velocity against reliability.**  
Now the earlier pieces fit together. The SLI is the sensor. The SLO is the acceptable operating point. The error budget is the allowed deviation. Burn rate is the “how urgently is this drifting?” signal. Policies tied to exhaustion are the actuator that changes engineering behavior. This is why the article says the output is not a dashboard but a decision. The framework’s purpose is to help an organization decide when it can safely move fast and when reliability debt has become too expensive to keep spending.

---

## Handles and Anchors

**1. Reliability budget is like financial budget, not a smoke alarm.**  
A smoke alarm only tells you something is wrong right now. A budget tells you how much capacity you have left to spend and whether your current spending rate is sustainable. That is the jump from threshold monitoring to error budgets.

**2. Ask: “What user failure can this measurement not see?”**  
This is a strong test for whether an SLI is well designed. If a DNS outage, stale response, or slow tail request can badly hurt users while your SLI stays green, your measurement point or “good event” definition is wrong or incomplete.

**3. Core tension: “How much failure are we willing to spend in exchange for shipping faster?”**  
That sentence captures why SLOs are governance, not just observability. The framework exists because reliability and delivery speed compete, and teams need an explicit rule for trading one against the other.

---

## What This Changes When You Build

**1. An engineer who understands this will define service objectives from user interactions, not infrastructure symptoms, because only user-facing ratios can support meaningful reliability policy.**  
The unaware default is to pick whatever is easy to graph — CPU, memory, queue depth, generic error count. That produces attractive dashboards but weak decisions, because the team is managing machine stress rather than user harm.

**2. An engineer who understands this will choose instrumentation points deliberately because where the SLI is measured determines what classes of incidents count against reliability.**  
The unaware default is to measure wherever telemetry already exists, often deep inside the service. The consequence is blind spots: edge failures, DNS problems, TLS expiry, CDN issues, and network path failures can produce severe outages that do not show up in the SLO.

**3. An engineer who understands this will use latency thresholds and percentiles instead of averages because tail behavior is where meaningful user pain and system pathologies often show up.**  
The unaware default is average latency, because it is simple and familiar. The consequence is that a minority of very bad experiences disappear inside a healthy-looking mean, especially during lock contention, cache misses, GC pauses, or retry storms.

**4. An engineer who understands this will build burn-rate-based alerting with different urgency tiers because operational response should depend on how quickly the budget is being consumed, not merely on whether a raw error threshold was crossed.**  
The unaware default is a static alert like “page if errors exceed 1%.” That tends to create either noisy pages for harmless spikes or silence during long, slow degradations that are quietly draining the month’s reliability.

**5. An engineer who understands this will attach explicit release and prioritization policies to budget exhaustion because the framework only changes outcomes when low reliability constrains future risk-taking.**  
The unaware default is to publish SLOs without enforcement. The consequence is organizational theater: reliability is measured, reviewed, and discussed, but feature delivery continues unchanged, so the supposed tradeoff between velocity and stability never actually gets managed.

**6. An engineer who understands this will often define multiple SLIs for one service because optimizing one dimension alone can degrade another while keeping the target green.**  
The unaware default is a single easy metric, usually availability. The consequence is metric gaming by accident or necessity: fast but empty responses, successful retries that are painfully slow, or technically served but stale data.

---
