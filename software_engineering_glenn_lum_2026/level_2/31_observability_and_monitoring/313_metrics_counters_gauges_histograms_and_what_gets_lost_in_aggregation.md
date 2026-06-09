## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers can name the metric types. Fewer can explain why the choice between them determines what questions your monitoring system is capable of answering. The real cost of misunderstanding metric mechanics is not a system that produces errors — it is a system that produces *plausible-looking data that hides real problems*. A dashboard showing 45ms average latency looks healthy. If 2% of your users are experiencing 8-second timeouts, that number is not just unhelpful — it is actively lying to you. Whether your monitoring system can even surface that problem depends entirely on how the underlying metric stores data and what happens when that data is aggregated across instances and time. That is what this post is about.

## Counters: Monotonic Accumulators

A counter is a value that only goes up. Total requests served, total bytes transferred, total errors encountered — these are all counters. The raw value of a counter is almost never what you care about. Knowing that your service has handled 14,230,891 requests since it started tells you nothing useful. What matters is the **rate of change**: how many requests per second, how many errors per minute.

This is why monitoring systems provide rate functions. In Prometheus, `rate(http_requests_total[5m])` computes the per-second average rate of increase over a five-minute window. The counter stores the cumulative total; the query layer derives the velocity.

The reason counters exist as a distinct type — rather than just recording the current rate directly as a gauge — comes down to **resilience to missed scrapes**. Prometheus pulls metrics from your application at a configured interval, typically every 15 or 30 seconds. If a scrape fails or is delayed, a gauge-based rate measurement would have a gap: you would lose whatever happened during the missed interval. A counter does not have this problem. When the next scrape succeeds, the counter's value reflects everything that happened in the interim. The rate calculation accounts for the elapsed time and produces a reasonable approximation.

Counters do reset — when a process restarts, the counter goes back to zero. Monitoring systems detect this: if the current value is lower than the previous value, it is treated as a reset rather than a massive negative rate. This works reliably in practice, but it means you should never manually decrement a counter in application code. If you need a value that goes both up and down, you need a gauge.

## Gauges: Point-in-Time Snapshots

A gauge records a value that can increase or decrease arbitrarily. CPU usage, memory consumption, queue depth, number of active connections, temperature — these are gauges. The value at the moment of collection *is* the data.

The critical limitation of a gauge is **temporal aliasing**. If your queue depth spikes to 10,000 for three seconds and then drains back to zero, but your scrape interval is 15 seconds, you may never observe the spike. The gauge only records what is true at the instant it is sampled. Everything between samples is invisible.

This matters operationally. Gauges are appropriate for values that change slowly relative to your scrape interval, or for values where the instantaneous state is inherently what you care about (current memory usage, current connection count). They are dangerous for values that spike and recover faster than your collection interval, because your monitoring system will show a flat line during an event that caused real user impact.

## Histograms: Preserving Distribution

Histograms are the most mechanically complex metric type, and the one most often misunderstood. A histogram does not store individual observations. It stores the *shape of the distribution* by counting how many observations fell into each of a set of pre-configured **buckets**.

Here is how it works concretely. Suppose you configure a histogram to track request latency with bucket boundaries at 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, and 1000ms. When a request completes in 73ms, the histogram increments the counters for every bucket whose boundary is ≥ 73ms: the 100ms bucket, the 250ms bucket, the 500ms bucket, and the 1000ms bucket all increment. This is what makes histogram buckets **cumulative** — the 250ms bucket does not mean "requests between 100ms and 250ms." It means "requests that took 250ms or less."

Alongside the buckets, the histogram maintains a `_sum` (the total of all observed values) and a `_count` (the number of observations). A single histogram with seven buckets therefore produces nine time series: one per bucket, plus sum, plus count.

### Estimating Percentiles from Buckets

To compute a percentile — say p99 — from a histogram, you find the bucket where the 99th percentile observation falls and interpolate within it. If you have 1,000 observations and need the 990th, you walk through the cumulative bucket counts until you find which bucket contains that observation, then linearly interpolate within the bucket's range.

This means **the accuracy of histogram-derived percentiles is bounded by your bucket boundaries**. If your buckets jump from 100ms to 250ms and your actual p99 is somewhere in that range, the best you get is a linear interpolation that assumes uniform distribution within the bucket. If most of your traffic clusters at 110ms with a tail at 240ms, that interpolation will be wrong. Bucket placement is an engineering decision that directly determines the precision of your percentile estimates, and getting it right requires knowing — or at least guessing well — what your distribution looks like.

### Why Histograms Are Aggregatable

This is the property that makes histograms fundamentally more useful than the alternative. Because each bucket is a counter, you can **sum histogram buckets across instances** and get a mathematically valid result. If instance A's 100ms bucket has counted 4,500 observations and instance B's 100ms bucket has counted 3,200, the combined 100ms bucket is 7,700. You can then compute percentiles from the aggregated buckets, and the result represents the actual distribution of latency across your entire fleet.

This is not true of pre-computed percentiles. Which brings us to summaries.

## Summaries: Accurate but Isolated

A **summary** computes percentiles client-side, inside your application process. Instead of maintaining bucket counts, the application maintains a sliding window of observations and calculates precise quantiles (p50, p95, p99, etc.) directly. The results are more accurate than histogram estimates for a single process — there is no bucket granularity problem.

The tradeoff is fatal for most production use cases: **summary quantiles cannot be aggregated across instances**. You cannot take the p99 from instance A and the p99 from instance B and combine them into a fleet-wide p99. Not by averaging. Not by taking the max. Not by any mathematical operation. The information required to reconstruct the combined distribution has been discarded during the quantile computation.

This is not a minor inconvenience. Any service running more than one instance — which is effectively every production service — needs fleet-wide percentiles to understand user experience. Summaries cannot provide them.

## What Aggregation Actually Destroys

The aggregation problem is the core of why metric type selection matters, so it is worth walking through a concrete example.

Suppose you have two instances of an API service behind a load balancer. Instance A handles 10,000 requests in a five-minute window, with a p99 of 55ms. Instance B handles 200 requests in the same window, with a p99 of 1,200ms — it is hitting a degraded downstream dependency.

If you average the two p99 values, you get 627ms. If you weight by request volume, you get approximately 78ms. Neither number is the actual p99 across all 10,200 requests. The real p99 is probably close to 55ms, because instance A's volume dominates the distribution and only the slowest two requests across the combined set determine the 99th percentile. But it could also be higher if instance B's slow requests are slow enough to push into the top 1% of the combined population.

The point is not that the math is complicated. The point is that **no operation on pre-computed percentiles can recover the information needed to compute the correct combined percentile**. The distribution has already been collapsed into a single number per instance. The shape is gone.

Histograms avoid this because the bucket counts *are* the distribution, at the resolution of the bucket boundaries. Sum the buckets, and you have the combined distribution. Compute the percentile from that, and you have the right answer (within bucket-resolution error).

This is why the Level 1 post's observation that "average latency hides the experience of slow users" is not just a caveat — it is a structural property of the metric type. An average (mean) is computed from sum and count. It is perfectly aggregatable — you can combine averages correctly using weighted means. But it tells you nothing about the tail. A service with a mean latency of 40ms could have a p99 of 60ms or a p99 of 15,000ms. The average cannot distinguish between these two very different realities.

## The Cardinality Tax

Histograms solve the aggregation problem, but they impose a real cost: **cardinality multiplication**. Every unique combination of labels on a metric produces a separate time series. A counter with labels for `method`, `path`, and `status_code` might produce a few hundred time series. A histogram with the same labels and ten buckets produces twelve time series (ten buckets plus sum and count) for every label combination — so a few hundred becomes a few thousand.

In monitoring systems like Prometheus, cardinality is the primary scaling constraint. High-cardinality metrics — metrics with many distinct label combinations — consume memory, slow queries, and can destabilize the monitoring system itself. An engineer who adds a `user_id` label to a histogram has just created a time series explosion that may take down the monitoring infrastructure before it ever provides useful data.

The practical discipline is: use histograms for metrics where you need distributional information (latency is the canonical example), and use counters or gauges for everything else. Do not histogram metrics where the mean is genuinely sufficient. And ruthlessly control label cardinality on histograms — every label you add multiplies the cost by the number of distinct values that label takes.

### Bucket Boundaries as a Commitment

Choosing histogram bucket boundaries is a decision you make at instrumentation time that constrains your analytical precision permanently (or until you re-deploy with new boundaries and lose continuity with historical data). Buckets that are too coarse give you poor percentile estimates. Buckets that are too fine waste cardinality on resolution you do not need.

The default bucket boundaries in most client libraries (Prometheus's defaults are 5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s, 10s) are reasonable starting points for HTTP request latency. They are terrible for a batch job that runs for minutes, or for an in-memory cache lookup that completes in microseconds. Matching bucket boundaries to the expected distribution of the thing you are measuring is not optional — it is a correctness concern.

## The Mental Model

Think of metric type selection as choosing what questions you are *permitted* to answer later. A counter lets you answer questions about rate and total volume. A gauge lets you answer questions about instantaneous state. A histogram lets you answer questions about distribution — but only at the resolution you chose when you configured the buckets, and only if you pay the cardinality cost.

The deepest insight is about what aggregation preserves and what it destroys. Counters and gauges aggregate naturally — sums of counters are valid counters, and averages of gauges are (often) meaningful. Histogram buckets aggregate naturally because they are counters. Pre-computed percentiles and pre-computed averages do not aggregate into valid percentiles — the distributional information has been irreversibly discarded. Every time you see a dashboard showing an averaged percentile across instances, you are looking at a number that is not mathematically what it claims to be.

This is why the choice of metric type is not a cosmetic or stylistic decision. It determines, at instrumentation time, whether your monitoring system will be able to tell you the truth during an incident — or whether it will show you a reassuring number while your users suffer.

## Key Takeaways

- **Counters only go up**, and you almost always care about their rate of change, not their raw value. Their monotonic property makes them resilient to missed scrapes in a way that gauges are not.

- **Gauges capture instantaneous state** and are subject to temporal aliasing: events that spike and recover between scrape intervals are invisible to gauge-based metrics.

- **Histogram buckets are cumulative counters**, not bins. A histogram with *n* buckets produces *n* + 2 time series per unique label combination (buckets plus sum plus count), which makes cardinality control critical.

- **Histogram bucket boundaries determine the precision of your percentile estimates.** Default boundaries are only appropriate for the distribution they were designed for. Mismatched boundaries produce percentile estimates that can be significantly wrong.

- **Pre-computed percentiles (summaries) cannot be aggregated across instances.** No mathematical operation on per-instance p99 values produces a valid fleet-wide p99. Histograms can be aggregated because their buckets are counters.

- **Averaging a percentile across instances produces a number that is not a percentile.** It looks like one, it sits on a dashboard like one, but it has no valid statistical meaning and will mislead you during incidents where load is unevenly distributed.

- **Averages (means) aggregate correctly but hide distributional shape.** A mean latency of 40ms is consistent with both a tight distribution around 40ms and a bimodal distribution where most requests take 5ms and a significant minority take 500ms. Only percentiles (or histograms) can distinguish these cases.

- **Cardinality is the primary cost of histograms.** Every label you add to a histogram multiplies its storage and query cost by the number of distinct values that label takes. High-cardinality labels on histograms are the most common way engineers accidentally destabilize their monitoring infrastructure.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Monitoring fails in a particularly dangerous way: it often fails by showing numbers that look reasonable. That is worse than no data, because it gives you false confidence. If you record latency in a way that only preserves averages, your dashboard can say “45ms” while a meaningful slice of users is timing out. If you record percentiles in a way that cannot be combined across instances, your fleet-wide dashboard can show a mathematically meaningless p99 and still look polished and authoritative.

The engineering problem here is that metric types are not just storage formats; they determine what truth survives collection and aggregation. Once data has been collapsed the wrong way, you cannot recover what was lost later in a query. That means incidents become harder to diagnose, regressions hide in the tail, and scaling the monitoring system itself becomes painful because the “fix” for better visibility often multiplies cardinality until Prometheus struggles or falls over.

If you do not have a working model of these mechanics, you inherit defaults without realizing it: gauges for things that should be counters, summaries for fleet metrics, histograms with bad buckets, labels that explode time series count. The result is a monitoring system that answers easy questions and fails on the ones you actually need during an outage.

---

## What You Need To Know First

### 1. Scraping
In systems like Prometheus, the monitoring system usually does not receive every event directly. Instead, it periodically asks each service for its current metric values — for example every 15 seconds. That means your monitoring data is a sequence of samples, not a perfect recording of everything that happened between them.

### 2. Time series and labels
A metric is not just one line on a graph. Every unique label combination becomes its own time series. So `http_requests_total{method="GET",status="200"}` and `http_requests_total{method="POST",status="500"}` are different series. This matters because storage and query cost scale with the number of series, not just the number of metric names.

### 3. Aggregation
Aggregation means combining data across time or across instances. Summing request counts across pods is aggregation. Computing fleet-wide latency from all instances is aggregation too. The crucial question is: does the metric type preserve enough information for that aggregation to still mean what you think it means?

### 4. Percentiles
A percentile tells you where a given fraction of observations fall. p99 latency means 99% of requests were at or below that latency, and 1% were slower. Percentiles are useful because they describe tail behavior, which averages hide. But they are only valid if computed from the underlying distribution, not from already-computed per-instance percentile values.

---

## The Key Ideas, Connected

### 1. Metric type selection is really a choice about what questions you will be able to answer later.
The article’s core point is that metric types are not cosmetic categories. They are different ways of preserving or discarding information. A counter preserves cumulative change, a gauge preserves a snapshot, a histogram preserves an approximate distribution, and a summary preserves per-process quantiles. Once you choose one, that choice limits what later queries can reconstruct.

That leads directly to counters, because counters are the simplest example of preserving data in a way that remains useful after imperfect collection.

### 2. A counter stores cumulative totals so that rates can be reconstructed even when scrapes are imperfect.
A counter only goes up: total requests, total errors, total bytes. The raw number is rarely useful by itself, because “14 million requests since startup” does not tell you what is happening now. What you usually want is the slope: requests per second, errors per minute.

The reason this works well is mechanical. If Prometheus misses one scrape, the next scrape still contains the total accumulated work. Since the total did not forget the missed interval, the query layer can estimate the average rate over time. That makes counters resilient to collection gaps in a way a directly-recorded “current requests/sec” gauge would not be. This naturally brings us to gauges, which behave differently because they do not accumulate history.

### 3. A gauge stores only the value at the instant of observation, so anything between scrapes can disappear.
A gauge can move up or down freely: memory usage, queue depth, active connections. Unlike counters, the sampled value is the data. There is no preserved cumulative history between samples.

The failure mode follows from that. If a queue spikes for 3 seconds and your scrape interval is 15 seconds, that spike may never be observed. Nothing in the gauge encodes “something bad happened between these two samples.” This is temporal aliasing: the system changed faster than your sampling could see. Once you understand that some metric types preserve missed intervals and others do not, histograms make more sense: they are built to preserve more structure than a single point value.

### 4. A histogram preserves an approximate distribution by turning observations into bucket counters.
A histogram does not keep each request latency individually. Instead, it counts how many requests were at or below each bucket boundary. If a request takes 73ms, every bucket with boundary greater than or equal to 73ms increments. That is why the buckets are cumulative.

This matters because bucket counts are counters. They inherit the good aggregation properties of counters: they can be summed across instances and across time windows in mathematically valid ways. Histograms also expose `_sum` and `_count`, which let you compute means, but the more important feature is that they preserve enough distribution shape to estimate percentiles later. That leads to the next crucial idea: percentile estimation depends on bucket design.

### 5. Histogram percentiles are only as accurate as the bucket boundaries allow.
When you compute p99 from histogram buckets, you are not reading an exact stored p99. You are finding the bucket where the 99th percentile lands and estimating its position within that bucket. If the relevant bucket spans 100ms to 250ms, your answer cannot be more precise than the assumptions you make inside that range.

So the approximation error is not some incidental implementation detail. It is a direct consequence of how much resolution your buckets preserve. Wide buckets throw away detail; narrow buckets preserve more but cost more series. Once that is clear, the value of histograms becomes sharper: despite approximation error, they preserve something summaries do not preserve at all — aggregatability.

### 6. Histograms are useful at fleet level because bucket counts can be added together without breaking their meaning.
If instance A saw 4,500 requests under 100ms and instance B saw 3,200 requests under 100ms, the combined fleet saw 7,700 requests under 100ms. That statement remains true after summation because bucket counts are counts. You are combining compatible pieces of the same distribution representation.

This is the key mechanical reason histograms work for multi-instance systems. You can sum all buckets from all instances, then compute p99 from the combined result, and that percentile corresponds to the fleet’s request population. That naturally sets up the contrast with summaries, which compute percentiles too early.

### 7. A summary gives precise per-process quantiles by discarding the very information needed for fleet-wide aggregation.
A summary computes quantiles inside the application process over a sliding window. For one instance, that can be more accurate than histogram estimation because it does not rely on coarse buckets.

But that precision comes from collapsing the observation stream into a few outputs like p50, p95, and p99. Once that collapse happens, the underlying distribution shape is gone. You no longer know how many requests were around each latency band; you only know a few cut points. That is why per-instance summaries cannot be combined into a valid global percentile. The issue is not lack of a clever formula. The information required has been thrown away.

### 8. The real distinction between metric types is what aggregation preserves and what it destroys.
This is the deepest connective idea in the article. Counters preserve additive totals, so rates can be derived and instances can be summed. Gauges preserve instantaneous state, but not what happened between samples. Histograms preserve an approximate distribution, so percentiles can be estimated after aggregation. Summaries preserve local quantiles, but destroy the distribution needed for global quantiles.

Once you see metric types through that lens, common monitoring mistakes become obvious. Averaging per-instance p99 values is wrong not because it is “bad practice,” but because percentiles are not additive and the per-instance distributions are already gone. The same reasoning explains why averages are safe to aggregate yet often operationally misleading.

### 9. Means aggregate correctly, but they hide tail behavior because they collapse the distribution too aggressively.
If you know sum and count, you can compute a correct mean for one instance or many. Weighted averaging works because means derive from additive quantities. So from a pure math perspective, averages aggregate nicely.

But they answer a weaker question. A mean tells you central tendency, not spread or tail pain. A service where almost everyone sees 40ms and another where most users see 5ms while a minority see 8-second stalls can share the same average. So “correctly aggregatable” does not mean “operationally sufficient.” This is why engineers reach for histograms specifically for latency and similar metrics where the tail matters.

### 10. Histograms solve the visibility problem by paying with cardinality.
Every histogram bucket is its own time series, plus `_sum` and `_count`. Add labels and you multiply all of those series across each label combination. That means histograms are not free visibility; they are visibility bought with storage, memory, and query cost.

This tradeoff is not accidental. To preserve enough structure for later percentile estimation and aggregation, the system must store more pieces. If you then add a high-cardinality label like `user_id`, you multiply that cost catastrophically. So the final practical insight follows: bucket choices and label choices are not tuning details; they are part of the correctness and survivability of your monitoring design.

### 11. Bucket boundaries are an instrumentation-time commitment about the precision you will have later.
Because percentiles are estimated from bucket counts, your bucket layout defines the resolution of your future questions. If your latency buckets are shaped for HTTP requests but you apply them to microsecond cache lookups or multi-minute batch jobs, the resulting percentiles will be too coarse to trust or too expensive to justify.

You cannot fully repair that later in query logic. The monitoring system can only answer with the detail you chose to preserve at instrumentation time. That closes the chain back to the first idea: metric design is deciding, in advance, what truths your system will still be able to tell you during an incident.

---

## Handles and Anchors

### 1. “Metric types are compression formats for reality.”
Each metric type keeps some information and throws some away. Counter: keeps cumulative total. Gauge: keeps current snapshot. Histogram: keeps approximate shape. Summary: keeps local quantiles. If you remember them as compression formats, the right question becomes: “What information will I regret losing later?”

### 2. “Can I add these across machines and still mean the same thing?”
This is a strong test question. Request counts: yes. Histogram buckets: yes. Per-instance p99s: no. If the answer is no, then a fleet-wide dashboard built from that value is probably lying or at least claiming more than the math supports.

### 3. Histograms are like a vote tally by range, not a list of every vote.
You do not know every individual latency, but you know how many fell under 10ms, 25ms, 50ms, and so on. Because counts from different polling stations can be added, you can reconstruct the overall shape well enough to answer percentile questions. Summaries are like each station reporting only “our 99th-percentile voter wait time,” which sounds useful but cannot be combined into a national p99.

---

## What This Changes When You Build

### 1. An engineer who understands this will instrument request volume and errors as counters, not gauges, because missed scrapes do not erase cumulative work.
The unaware engineer often records “current requests/sec” or similar instantaneous rates directly. That inherits sampling gaps: if scrapes fail, the system loses what happened during the gap. With counters, the total survives and rate can be derived later with acceptable accuracy.

### 2. An engineer who understands this will treat gauges with suspicion for short-lived spikes because a flat graph may only mean “we did not sample at the right instant.”
The unaware engineer sees a smooth queue-depth graph and concludes the queue never spiked. The informed engineer asks whether the queue can fill and drain faster than the scrape interval. If yes, they may add counters for enqueues/dequeues, shorten the scrape interval, or instrument the event differently.

### 3. An engineer who understands this will choose histograms for latency they need to reason about across a fleet, because summaries cannot produce a valid global percentile.
The unaware engineer may expose per-pod p99 latency and then average it in Grafana, producing a number that looks legitimate. The informed engineer knows that this dashboard is mathematically invalid, and instead instruments latency with histogram buckets so the fleet-wide distribution can be reconstructed.

### 4. An engineer who understands this will design histogram buckets around the expected latency range, because bucket layout directly sets percentile precision.
The unaware engineer accepts library defaults everywhere. That can make sub-millisecond systems look artificially coarse or long-running jobs collapse into top buckets with no useful discrimination. The informed engineer asks: “Where are the operational thresholds? Where do I need detail?” and places buckets accordingly.

### 5. An engineer who understands this will be much stricter about labels on histograms than on simple counters, because every extra label multiplies every bucket series.
The unaware engineer may add `endpoint`, `tenant_id`, or worse `user_id` to a latency histogram to make dashboards “more detailed,” and then discover memory blowups, slow queries, and an overloaded Prometheus. The informed engineer keeps high-cardinality dimensions out of histograms, or moves that analysis to logs/traces where per-entity detail is a better fit.

---

</details>
