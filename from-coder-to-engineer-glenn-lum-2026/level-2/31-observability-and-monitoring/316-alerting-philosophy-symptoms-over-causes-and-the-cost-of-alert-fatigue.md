## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams don't have an alerting problem. They have a classification problem they've never examined. They've instrumented dozens of system internals — CPU usage, memory pressure, disk I/O, thread pool sizes, queue depths — set thresholds on each one, and wired every threshold breach to a page. The system dutifully fires alerts. Engineers dutifully investigate. Most of the time, nothing is actually wrong — users are unaffected, the spike was transient, the system self-corrected. The engineer marks the alert as resolved and goes back to what they were doing. This cycle repeats hundreds of times. And then one night, a real outage begins, the pager fires, and the on-call engineer glances at their phone, assumes it's another false alarm, and rolls over. The alerting system didn't fail. The engineer didn't fail. The *design* of the alerting system made this outcome inevitable.

Understanding why requires looking at the actual mechanics: what makes symptom-based alerting structurally different from cause-based alerting, how alert fatigue develops as a learned behavior, and what a well-designed alerting system actually computes.

## The Asymmetry Between Causes and Symptoms

The fundamental argument for symptom-based alerting is not a preference. It is a structural property of complex systems.

**Symptoms are finite and stable.** For any given service, the ways users experience failure are constrained: requests return errors, requests take too long, requests return wrong data. These categories don't change when you refactor your infrastructure, swap databases, or add a new dependency. The user-visible failure modes of your checkout service are roughly the same whether it runs on bare metal or Kubernetes.

**Causes are infinite and unpredictable.** A service can fail because of a memory leak, a connection pool exhaustion, a kernel bug, a misconfigured load balancer, a slow downstream dependency, a poison-pill message in a queue, a clock skew between nodes, a certificate expiration, a DNS resolution failure, or a cascading retry storm triggered by a deploy two services away. You cannot enumerate all the causes in advance. Every cause-based alert you write covers a failure mode you've already imagined. The outage that actually takes you down is usually one you haven't.

This creates an asymmetry that no amount of alert tuning can fix. A symptom-based alert on "error rate > 1% for 5 minutes" catches *every* cause that produces user-facing errors, including causes you've never seen before. A cause-based alert on "CPU > 90%" catches only the subset of problems that manifest as high CPU, and it also fires for the many situations where high CPU is completely benign — a batch job running on schedule, a JVM garbage collection cycle, a burst of legitimate traffic.

Consider a concrete scenario. Your payment service starts returning HTTP 500s to 3% of requests. The root cause is that a downstream fraud-detection service deployed a change that causes it to timeout on certain request patterns. If you have a symptom-based alert on payment service error rate, you are paged immediately. If you are relying on cause-based alerts, you need to have predicted this specific failure mode in advance and built an alert for it. You probably didn't, because the failure is in a dependency's behavior, not in any of your own system's internal metrics. Your CPU is fine. Your memory is fine. Your connection pools are fine. Your database is fine. You are just returning errors.

## Every Alert Is a Classifier

It helps to think about each alert rule as a binary classifier. It makes a decision every evaluation cycle: fire or don't fire. Like any classifier, it has four outcomes: true positives (alert fires, real problem exists), false positives (alert fires, no real problem), true negatives (alert doesn't fire, nothing is wrong), and false negatives (alert doesn't fire, but something is actually wrong).

The quality of an alerting system depends on two properties: **precision** (what fraction of fired alerts correspond to real problems) and **recall** (what fraction of real problems generate an alert). Cause-based alerts tend to have poor precision, because many causes occur without producing user-visible problems. CPU spikes, memory pressure, elevated disk I/O — these are often transient, self-correcting, or simply normal operating behavior under load. A cause-based alert fires whenever the metric crosses a threshold, regardless of whether any user is affected.

This matters because of the **base rate problem**. If 90% of CPU spikes are benign, then even a perfectly calibrated CPU threshold will page you nine times for every one time the spike actually matters. The on-call engineer doesn't experience "this alert has 10% precision." They experience "this alert is almost always wrong." The rational behavioral response to an alert that is almost always wrong is to stop treating it as urgent.

Symptom-based alerts are not immune to false positives, but they have a structural advantage: they are measuring the thing you actually care about. An alert that says "5% of user requests are failing" can be wrong (a measurement artifact, a monitoring pipeline delay), but it cannot be *irrelevant*. The base rate of "user-facing error rate breaches threshold and it doesn't matter" is much lower than the base rate of "CPU crosses 90% and it doesn't matter."

## The Mechanics of Alert Fatigue

Alert fatigue is not merely "too many alerts." It is a specific learned behavior that develops through a well-understood psychological mechanism, and once it takes hold, it is remarkably difficult to reverse.

Every time an alert fires and the engineer investigates and finds nothing actionable, a small amount of trust in the alerting system is destroyed. Every time an alert fires and the engineer finds a real problem, trust is reinforced. The problem is that this process is **asymmetric**: trust erodes faster than it builds. One week of false alarms does more damage than one month of accurate alerts can repair. This is not a character flaw in engineers. It is the same cognitive mechanism that makes people stop listening to car alarms.

The behavioral progression is predictable. First, the engineer starts taking longer to respond to pages, because experience has taught them the alert is probably not real. Then they start glancing at the alert details and making a snap judgment about whether to investigate, based on pattern recognition rather than actual diagnosis. Then they start silencing certain alerts entirely. Then new engineers join the on-call rotation and are told by their peers which alerts to ignore. At this point, the alerting system is not just failing — it is *actively harmful*, because it provides the organizational illusion of monitoring coverage while delivering none.

The critical insight is that **alert fatigue is a property of the system, not the individual.** You cannot fix it by hiring more disciplined engineers or by writing better runbooks. If the alert system has a high false positive rate, the humans in the loop will adapt to that rate. The only fix is to change the signal-to-noise ratio of the alerts themselves.

## Burn Rate: How Symptom-Based Alerting Actually Works

Naive symptom-based alerting — "page me when the error rate exceeds X%" — is better than cause-based alerting but still has problems. A brief spike that lasts 30 seconds and affects a handful of requests probably isn't worth a page. A slow elevation in error rate from 0.1% to 0.5% over several days might be eating through your error budget without ever crossing a threshold that feels acute.

The mechanism that solves both problems is **burn rate alerting**, tied directly to your SLO. The concept: instead of alerting on the raw metric value, you alert on the *rate at which you are consuming your error budget*.

Here is how the math works. Suppose your SLO is 99.9% availability over a 30-day window. That gives you an error budget of 0.1% — roughly 43 minutes of total downtime, or equivalently, 0.1% of requests can fail. A **burn rate of 1** means you are consuming your error budget at exactly the sustainable pace — you will use 100% of it by the end of the 30-day window. A burn rate of 14 means you are consuming budget 14 times faster than sustainable — at this rate, you will exhaust your entire monthly budget in about two days.

A well-designed alerting system uses **multiple burn rates with multiple time windows**. The fast-burn alert catches acute incidents: a burn rate of 14x sustained over 5 minutes, confirmed by a 1-hour window. This fires for sudden outages — your service starts returning 50% errors and you need to act now. The slow-burn alert catches chronic degradation: a burn rate of 3x sustained over a 6-hour window. This catches the scenario where your error rate has crept up slightly, not enough to feel urgent in any given minute, but enough to exhaust your error budget well before the end of the month.

In practice, a burn rate alerting rule looks something like this:

```
# Fast burn: exhausts 30-day budget in ~2 days
alert: HighErrorBudgetBurn_Fast
expr: |
  (1 - (rate(http_requests_total{code!~"5.."}[5m]) 
  / rate(http_requests_total[5m]))) > (14 * 0.001)
for: 2m
```

```
# Slow burn: exhausts 30-day budget in ~10 days
alert: HighErrorBudgetBurn_Slow
expr: |
  (1 - (rate(http_requests_total{code!~"5.."}[6h]) 
  / rate(http_requests_total[6h]))) > (3 * 0.001)
for: 30m
```

The fast-burn alert pages the on-call engineer. The slow-burn alert creates a ticket. This distinction — **page for acute, ticket for chronic** — is itself a critical design choice. Not every problem that needs fixing needs to wake someone up.

## Where Cause-Based Alerts Belong

Symptom-based alerting does not make cause-based monitoring irrelevant. It changes its role. Causes become your **diagnostic layer**, not your **notification layer**.

When a symptom-based alert fires — error rate is elevated — the engineer needs to diagnose *why*. This is where dashboards showing CPU, memory, connection pools, queue depths, and downstream latency become essential. They are investigative tools, not alerting triggers.

There is one legitimate exception: **predictive resource exhaustion**. A disk filling up at a rate that will hit 100% in four hours is not yet causing user-visible symptoms, but it will. A TLS certificate expiring in 72 hours is not yet causing errors, but it will. These are not truly "cause" alerts — they are alerts on *imminent future symptoms*. The distinction matters: they are justified not because they represent internal state you should care about, but because they represent inevitable user impact you can still prevent. Even these should typically generate tickets, not pages, unless the time-to-impact is measured in minutes.

## Tradeoffs and Failure Modes

**Detection latency.** Symptom-based alerting is structurally slower than cause-based alerting. A cause-based alert on connection pool exhaustion fires the moment connections are exhausted. A symptom-based alert fires only after that exhaustion has produced enough errors, for long enough, to cross your threshold. If your burn-rate window is 5 minutes, you will not be paged until users have been experiencing errors for 5 minutes. For most services, this tradeoff is correct — the cost of five minutes of degradation is far lower than the cost of an on-call rotation that doesn't trust its pager. For systems with extremely tight latency requirements (payment processing, real-time bidding), you may need to accept some well-chosen cause-based alerts alongside your symptom-based ones, understanding that you are trading higher noise for faster detection.

**The debugging gap.** A symptom-based alert tells you *that* users are affected but not *why*. This is a feature, not a bug — it separates detection from diagnosis — but it requires investment. If your dashboards, logs, and traces are not good enough to support rapid diagnosis once you've been paged, you will feel pressure to add cause-based alerts "just so we know what's wrong faster." This is a trap. The correct response is to improve your observability tooling, not to degrade your alerting system.

**The quiet system.** Teams migrating from cause-based to symptom-based alerting often experience anxiety when their pagers go quiet. They were accustomed to receiving several alerts per week — each one felt like proof that the monitoring system was working. A well-tuned symptom-based system might page once a month. This silence feels like something is broken. It isn't. But the psychological transition is real, and teams that don't expect it sometimes regress by adding cause-based alerts back "just in case."

**Organizational contagion.** Alert fatigue is not contained to the individual who experiences it. It propagates through on-call rotations via institutional knowledge. Senior engineers tell junior engineers which alerts are noise. Runbooks accumulate notes like "this usually resolves on its own — wait 10 minutes before investigating." Dashboards are built that filter out entire categories of alerts. Once this culture takes root, restoring trust in the alerting system requires not just fixing the alerts themselves but actively unwinding the institutional muscle memory built around ignoring them. This is significantly harder than getting it right the first time.

## The Mental Model

An alerting system is a communication channel between your infrastructure and your engineers. Like any communication channel, it has a credibility budget. Every false positive spends credibility. Every true positive that leads to meaningful action earns it back — but slower than it was spent. The system fails not when it stops sending signals, but when the humans on the other end stop believing them.

Your alerting layer should be a thin, high-trust surface that answers one question: *are users being harmed right now, or are they about to be?* Everything else — what's causing it, which component is misbehaving, what the internal metrics look like — belongs in your diagnostic layer, accessible on demand, not pushed to your pager.

The shift from cause-based to symptom-based alerting is not a tuning change. It is a structural decision about what your alerting system is *for*. It is for protecting users, not for narrating system internals.

## Key Takeaways

- **Symptoms are finite; causes are infinite.** A symptom-based alert on error rate or latency catches every failure mode that affects users, including ones you haven't imagined. A cause-based alert only catches the specific failure you predicted.

- **Every alert is a binary classifier, and precision matters more than coverage.** A pager that fires ten times with nine false positives doesn't have a "tuning" problem — it has a structural problem that trains engineers to ignore it.

- **Alert fatigue is a system property, not an individual discipline problem.** You cannot solve it with better runbooks or more diligent engineers. You solve it by changing the false positive rate of the alerts themselves.

- **Burn rate alerting is the mechanical link between SLOs and your pager.** Instead of alerting on raw metric thresholds, alert on the rate at which you are consuming your error budget, using fast-burn windows for acute incidents and slow-burn windows for chronic degradation.

- **Page for acute, ticket for chronic.** Not every problem that needs attention needs to wake someone up. Fast budget burn gets a page. Slow budget burn gets a ticket. Predictive resource exhaustion (disk, certificates) gets a ticket unless impact is imminent.

- **Cause-based metrics are diagnostic tools, not alerting triggers.** CPU, memory, connection pools, and queue depths are essential for investigating *why* an alert fired. They should live on dashboards and in runbooks, not on your pager.

- **The silence of a well-tuned alerting system is a feature, not a sign of failure.** Teams accustomed to noisy pagers often mistake quiet for broken. A system that pages once a month and is right every time is vastly superior to one that pages daily and is wrong 90% of the time.

- **Alert fatigue propagates culturally and is harder to reverse than to prevent.** Once an on-call rotation develops the institutional habit of ignoring pages, restoring trust requires changing both the alerts and the organizational muscle memory built around dismissing them.

# Discussion

## Why This Conversation Is Happening

Many teams think their monitoring is mature because they collect lots of metrics and have lots of alerts. But the real failure often shows up later: the pager goes off, the engineer assumes it is another noisy internal threshold crossing, and a real user-facing outage gets ignored or handled late. What breaks is not just incident response speed. Trust in the alerting system itself decays.

The core problem is that teams often page on internal system conditions rather than on actual user harm. That creates a stream of alerts for CPU spikes, queue growth, memory pressure, or transient dependency issues that may never affect users at all. Over time, engineers learn that the pager is usually describing system activity, not urgent action. Once that learning sets in, the alert channel stops working as an emergency channel.

So this topic matters because alerting is not just about detecting bad states. It is about deciding what deserves to interrupt a human. If you get that classification wrong, you do not merely create noise — you train your organization to miss the alerts that actually matter.

---

## What You Need To Know First

**Service Level Objective (SLO)**  
An SLO is a target for user-visible service quality over a period of time, like “99.9% of requests succeed over 30 days” or “99% of requests complete under 300ms.” It is not about internal component health. It is a statement about what users experience.

**Error budget**  
If your SLO is 99.9%, then the remaining 0.1% is the error budget: the amount of failure you can “spend” within that window before you miss the target. This gives you a concrete way to reason about whether current degradation is acceptable, urgent, or unsustainable.

**Symptoms vs causes**  
A symptom is what users experience: errors, high latency, wrong results. A cause is one possible reason that symptom happened: CPU saturation, database locks, certificate expiry, connection pool exhaustion. Many different causes can produce the same symptom.

**Precision and recall for alerts**  
Treat an alert like a yes/no detector. Precision means “when it fires, how often is there really a meaningful problem?” Recall means “when a meaningful problem exists, how often does it fire?” For pager alerts, low precision is especially damaging because false alarms train people not to trust the signal.

---

## The Key Ideas, Connected

**An alerting system is not mainly a metric collection system; it is a decision system about when to interrupt humans.**  
The important design question is not “what can we measure?” but “what conditions justify waking someone up?” Teams often slide from one to the other without noticing. They instrument internal metrics, add thresholds, and page on threshold breaches because the data is available. But availability of a metric does not mean that metric is a good trigger for human action. Once you see alerting as a human-interruption system, you immediately care about signal quality, not metric quantity. That leads to the next idea: what kind of signals are structurally better?

**Symptoms are better paging signals than causes because symptoms are stable while causes are open-ended.**  
Users only experience a limited set of failures: the system is down, slow, or incorrect. But the reasons behind those failures are effectively unbounded. New dependencies, new deploy patterns, obscure interactions, partial downstream failures, timing issues, and environment-specific bugs can all create harm. If you alert on causes, you only catch the causes you predicted in advance. If you alert on symptoms, you catch any cause that produces user-visible damage, including causes nobody imagined. That is why symptom-based alerting has broader coverage with fewer rules. But broad coverage alone is not enough; we also need to understand why cause-based alerts feel so noisy in practice.

**Every alert behaves like a binary classifier, and noisy cause-based alerts usually have poor precision.**  
On every evaluation cycle, an alert rule decides: fire or do not fire. That makes it a classifier. The key practical issue is precision: when the alert fires, does it usually correspond to a real problem worth action? Cause-based thresholds often fail here because internal conditions frequently occur without user impact. CPU can spike during healthy load. Queue depth can rise briefly and drain normally. Memory pressure can resolve after GC. The alert fires because the threshold was crossed, not because the user is being harmed. So the engineer’s lived experience becomes “this page is usually irrelevant.” Once that happens, the statistical property of low precision turns into a behavioral property: distrust. That is the mechanism behind alert fatigue.

**Alert fatigue is learned behavior produced by repeated false positives, not a vague morale problem.**  
If engineers repeatedly investigate alerts and find nothing actionable, they adapt rationally. They delay response. They pattern-match instead of investigating. They mute recurring alerts. They teach others which alerts are noise. This is not laziness; it is the system training its operators. The asymmetry matters: a few false alarms can destroy trust faster than a few accurate alerts can rebuild it. So the true failure mode of noisy alerts is not inconvenience. It is that your emergency communication channel loses credibility. Once that is clear, the design goal sharpens: alerts must be tied to conditions that are both meaningful and scarce enough to preserve trust. That is where SLOs and burn rate come in.

**Burn rate turns symptom-based alerting from a crude threshold into a measure of how fast you are consuming tolerated failure.**  
A raw symptom threshold like “page when errors exceed 1%” is better than paging on CPU, but still blunt. A brief spike may not matter. A small persistent degradation may matter a lot. Burn rate solves this by measuring current failure relative to the allowed failure in your SLO. If your service has a 0.1% error budget and you are currently failing requests at 1.4%, you are burning the budget 14 times faster than sustainable. That is useful because it connects current symptoms to business significance over time. You are no longer asking only “is error rate above some number?” You are asking “at this pace, how quickly are we consuming our allowed unreliability?” That makes the next design move possible: using different windows for different operational purposes.

**Multiple burn-rate windows separate acute incidents from chronic degradation.**  
A short window catches sharp failures quickly: a sudden outage or steep spike in errors. A longer window catches slow leaks that do not look dramatic minute-to-minute but still threaten the SLO over days. The mechanism matters here: short windows are sensitive but noisy; long windows are stable but slower. Combining them gives you coverage of both “the building is on fire now” and “we are steadily bleeding reliability.” This is why good alerting systems often use a fast-burn page and a slow-burn ticket. Once you understand this split, the next question becomes: if symptoms drive paging, what happens to all those internal metrics?

**Internal metrics do not go away; they move from the notification layer to the diagnostic layer.**  
CPU, memory, queue depth, thread pools, downstream latency, and similar signals are still valuable. But their value is usually explanatory, not interrupt-worthy. Once a symptom-based alert tells you users are being harmed, those metrics help answer why. That separation is important because it preserves pager trust while still giving engineers the observability they need to debug quickly. If you mix those roles, your diagnostics become your pager, and your pager becomes noisy. The article’s exception makes sense in this framework too: some internal-looking signals really represent unavoidable future symptoms.

**The main exception is predictive exhaustion: conditions that have not hurt users yet but are on a reliable path to doing so soon.**  
A disk filling to 100%, a certificate nearing expiry, or a quota that will be hit in a known time window can justify alerting before user-visible symptoms appear. But the reason is not “internal metrics matter after all.” The reason is that these metrics are acting as forecasts of imminent user harm. The system is effectively saying: “No users are broken yet, but unless someone acts, users will be broken soon.” That still fits the same philosophy: alert on user impact, present or imminent. And it also supports the page-versus-ticket distinction. If impact is hours away, create planned work. If impact is minutes away, escalate.

**Symptom-based alerting has tradeoffs, and the main one is detection latency in exchange for trust.**  
Because symptom alerts wait for user-visible degradation to appear and persist, they may fire later than a well-chosen cause alert. That is a real cost. In very tight systems, a few minutes may matter enough that some low-noise cause-based pages are justified. But the article’s point is that this should be a deliberate trade, not the default. Most teams accidentally optimize for earliest possible detection of anything unusual, and in doing so they destroy the trustworthiness of the pager. The better framing is: the pager is a scarce, credibility-limited channel, so only high-confidence, user-relevant signals belong there.

**The final mental model is that alerts spend credibility, and credibility is the real scarce resource.**  
Every false positive spends some of the operator’s willingness to believe the next page. Every irrelevant page teaches “this channel exaggerates.” A good alerting system therefore computes more than breach/no-breach. It computes whether the condition represents user harm severe enough, sustained enough, or imminent enough to justify consuming human attention. That is the structural shift: from “tell me when internals look odd” to “tell me when users are being harmed, or are about to be harmed.”

---

## Handles and Anchors

**1. Pager = fire alarm, dashboard = instrument panel.**  
A fire alarm should mean “leave now,” not “something somewhere changed a bit.” The dashboard is where you inspect temperature, airflow, and wiring after the alarm. If you wire the fire alarm to every unusual sensor fluctuation, people stop treating it like a fire alarm.

**2. Symptoms are the destination; causes are the roads.**  
Many roads can lead to the same destination. If your job is to know whether you have arrived at “users are failing,” checking the destination is more reliable than trying to enumerate every possible road that might get you there.

**3. Ask this question of any alert: “If this fires at 3am, what user harm is likely happening right now?”**  
If the answer is vague, speculative, or “none necessarily,” it probably should not page. That one question is often enough to distinguish notification signals from diagnostic signals.

---

## What This Changes When You Build

**An engineer who understands this will design paging rules around user-visible SLO indicators rather than around infrastructure thresholds, because symptoms generalize across unknown causes while thresholds only cover imagined ones.**  
The unaware engineer pages on CPU, memory, queue depth, and dependency internals by default because those are easy to measure. The result is wide alert coverage on paper but poor real coverage of novel incidents.

**An engineer who understands this will evaluate alerts in terms of precision and operator trust, not just whether the alert “caught something once,” because repeated false positives train humans to ignore the channel.**  
The unaware engineer keeps noisy alerts because they occasionally correlate with real issues. That preserves theoretical signal but destroys practical response behavior.

**An engineer who understands this will tie alert thresholds to error-budget burn rather than arbitrary percentages, because urgency depends on how fast reliability is being consumed over time, not on a raw metric crossing a standalone line.**  
The unaware engineer picks thresholds like “1% errors for 5 minutes” without connecting them to the service’s reliability target. That causes overpaging for harmless bursts and underreacting to slow sustained degradation.

**An engineer who understands this will separate page-worthy alerts from ticket-worthy alerts, because acute fast-burn failures and slow-burn maintenance risks require different response modes.**  
The unaware engineer often routes everything important to the pager. The consequence is that urgent incidents and scheduled remediation compete in the same channel, raising noise and reducing urgency clarity.

**An engineer who understands this will invest more in dashboards, logs, and traces after moving to symptom-based paging, because once the page says “users are impacted,” fast diagnosis depends on strong observability rather than on pre-baked cause alerts.**  
The unaware engineer feels the loss of cause-based pages as loss of information and adds more alert rules to compensate. That makes the pager narrate internals instead of preserving it as a high-trust trigger.

---
