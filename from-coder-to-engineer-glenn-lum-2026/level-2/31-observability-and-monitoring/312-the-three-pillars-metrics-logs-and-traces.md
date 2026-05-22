## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams have metrics, logs, and traces. They have dashboards, they have a log aggregator, they might even have distributed tracing turned on. And when something breaks at 2 AM, they still can't figure out what happened. The reason is almost never that they're missing a pillar. It's that they don't understand the data model underneath each one — what it can and cannot represent, why it costs what it costs, and how to move between pillars during an investigation. The three pillars are not three flavors of the same thing. They are three fundamentally different data structures, optimized for fundamentally different query patterns, with fundamentally different cost profiles. Until you understand that, you'll keep collecting all three and getting the diagnostic power of one.

## The Data Models Are the Point

Each pillar exists because it represents system behavior in a way the other two structurally cannot. This isn't a matter of preference or tooling — it follows from what the underlying data looks like.

**Metrics** are pre-aggregated numerical time series. A single metric is a name, a set of label key-value pairs, and a stream of timestamped numerical values. When your application records that it handled a request in 230ms, that number doesn't get stored as an individual event. It gets folded into an aggregate: a histogram bucket is incremented, a counter ticks up, a gauge is updated. The raw event is gone. What remains is a compact summary of behavior over a time window.

This is why metrics are cheap to store and fast to query. A counter tracking HTTP requests with labels for `method`, `status`, and `endpoint` produces one time series per unique combination of those label values. Whether your service handled ten requests or ten million in the last minute, the storage cost is roughly the same — it's proportional to the number of unique label combinations, not the number of events. This property is what makes metrics viable for real-time alerting and long-term trending. It's also the source of their fundamental limitation: once you've aggregated, you cannot disaggregate. You can see that p99 latency spiked, but you cannot ask "which specific request was slow?" The individual events no longer exist in the metrics system.

**Logs** are the opposite. Each log record is a discrete, individual event with arbitrary fields. Nothing is pre-aggregated. When your service handles a request and emits a structured log line, every field you attached — user ID, request ID, duration, response code, downstream service called — is preserved as-is. This means logs can answer questions about specific events: "What happened to this particular request from this particular user at this particular time?" But it also means your storage cost scales linearly with event volume. Every request, every database query, every retry produces a record that must be ingested, indexed, and stored. A service handling 50,000 requests per second is producing 50,000 log records per second, each of which might be several hundred bytes.

This cost structure is not incidental. It's the reason log retention policies exist, the reason log sampling becomes necessary at scale, and the reason teams are perpetually fighting their log aggregation bill. The diagnostic power of logs comes precisely from their un-aggregated nature, and that nature is expensive.

**Traces** are neither aggregates nor flat event records. A trace is a **directed acyclic graph of spans**, where each span represents a unit of work and the edges represent causal relationships — "this service called that service," "this database query happened inside this request handler." The data model is inherently relational. A single trace captures the structure of a request's journey: what called what, in what order, and how long each piece took. This structural information is what neither metrics nor logs can represent. Metrics can tell you that the payment service is slow. Logs can tell you that a specific request to the payment service timed out. Only a trace can tell you that the request was slow because the payment service made a synchronous call to the fraud-detection service, which made three retries to an external API, and the third retry took four seconds.

### Cardinality: The Constraint That Governs Metrics

The single most important concept in metrics systems is **cardinality** — the number of unique time series produced by a metric. Every unique combination of label values creates a new time series, and each time series consumes memory in your metrics backend for as long as it's active.

Consider a metric like `http_request_duration_seconds` with labels `method`, `endpoint`, `status_code`, and `customer_id`. The first three labels are bounded: you have a handful of HTTP methods, a known set of endpoints, and a finite set of status codes. The product might be 5 × 30 × 5 = 750 time series. Manageable. But `customer_id` is unbounded. If you have 100,000 customers, you've just created 75 million time series. Your metrics backend will either fall over or your bill will make someone in finance ask hard questions.

This is why experienced operators are careful about which labels they attach to metrics. The rule is: **metrics labels must have low, bounded cardinality**. If you need to break down behavior by a high-cardinality dimension like user ID, request ID, or session token, that's a job for logs or traces, not metrics. Violating this rule is one of the most common ways teams accidentally take down their monitoring infrastructure — which means losing visibility precisely when they need it most.

### How Trace Context Propagation Actually Works

Traces don't magically appear. They require active cooperation between every service in a request path, and understanding the mechanism matters because it's where traces most commonly break.

When a request enters your system, the first service generates a **trace ID** — a globally unique identifier for this entire request journey — and a **span ID** for its own unit of work. When that service makes an outbound call to another service, it injects both IDs (plus a new parent span ID) into the request headers. The downstream service extracts those IDs, creates its own span as a child of the parent, and does the same for any further downstream calls. This is **context propagation**, and it happens via headers in HTTP calls (typically `traceparent` in the W3C Trace Context standard), message metadata in async systems, or similar carrier mechanisms.

Every service in the chain must participate. If one service in the middle doesn't extract and propagate the context, the trace breaks — you get two disconnected fragments instead of one coherent picture. This is why instrumenting traces in a polyglot microservice architecture is genuinely hard. Every service, in every language, using every framework, must correctly handle context propagation. A single uninstrumented service creates a gap.

### Sampling: The Unavoidable Compromise in Traces

At any meaningful scale, collecting 100% of traces is economically impractical. A system handling 100,000 requests per second, where each request touches eight services, produces 800,000 spans per second. Each span carries timing data, attributes, status codes, and often log-like event annotations. The storage and processing cost is enormous.

The answer is **sampling**, and the strategy you choose has direct consequences for what you can and cannot see.

**Head-based sampling** makes the decision at the entry point: when a trace is created, you decide probabilistically (e.g., keep 1% of traces) whether to record it. This is simple and predictable in terms of cost, but it means you'll miss rare events. If an error occurs on 0.01% of requests and you're sampling at 1%, most error traces are never recorded.

**Tail-based sampling** waits until the trace is complete, examines it, and then decides whether to keep it — typically retaining all traces that contain errors or high latency while discarding routine successful traces. This is far more useful for debugging but requires a collector that can buffer complete traces before making the keep/drop decision, which adds architectural complexity and its own resource costs.

The choice between these strategies is not academic. It determines whether your tracing system will actually contain the traces you need during an incident.

## Where the Pillars Break and Where Teams Get Stuck

### The Correlation Gap

The most common failure mode isn't a missing pillar — it's three pillars that don't talk to each other. A team sees a latency spike on a metrics dashboard, switches to their log aggregator to search for errors in the affected time window, finds some timeout errors, but can't connect those errors to a specific trace showing the causal chain. They're doing archaeology across three disconnected tools.

The fix is **correlation identifiers**. Every log line should carry a trace ID. Metrics should support **exemplars** — references from an aggregate data point back to a specific trace that contributed to it. When your p99 histogram bucket shows a spike, an exemplar lets you click through to an actual trace that experienced that latency. Without these links, you have three data stores and a manual process of jumping between them with timestamps and guesswork.

Building this correlation in isn't free. It requires that your instrumentation layer — whether OpenTelemetry or something custom — consistently attaches trace and span IDs to log records, and that your metrics library supports exemplar emission. It requires that your tooling can follow those links. But without it, the promise of "three pillars" remains theoretical.

### Logs as a Crutch

Teams that haven't invested in metrics or traces tend to pour everything into logs. They log request durations (a metric), they log the call chain between services (a trace), and they also log actual event data (the thing logs are for). The result is a multi-terabyte-per-day log pipeline that is simultaneously expensive and slow to query. Asking "what is my p99 latency right now?" by scanning billions of log records is orders of magnitude slower and more expensive than reading it from a pre-aggregated time series. Using logs to reconstruct call graphs between services is possible but brittle — it requires consistent request ID propagation and careful log correlation that replicates what a tracing system does natively.

The right instinct is: if you're aggregating log data to produce a number, that should probably be a metric. If you're joining log records across services to reconstruct a request path, that should be a trace. Logs should capture what only logs can capture — the context and detail of individual events.

### Metric Averages Lie

A metric showing average latency of 150ms might mean all requests take 140-160ms, or it might mean 99% take 50ms and 1% take 10 seconds. The average hides the distribution. This is why percentile-based metrics (p50, p95, p99) exist — but percentiles have their own problem: **they cannot be aggregated across instances**. The p99 of service instance A and the p99 of service instance B cannot be averaged to produce the true p99 of the service. Histograms solve this (you can merge histogram buckets and then compute percentiles from the merged result), but only if you set your bucket boundaries appropriately before collection. The boundaries you choose determine what granularity of latency distribution you can see. This is a decision you make at instrumentation time that constrains your analysis options permanently.

## The Model to Carry Forward

Think of the three pillars as three projections of the same underlying reality — the stream of everything happening in your system. Metrics are the statistical projection: they discard individual identity in exchange for cheap, fast, aggregable summaries. Logs are the event projection: they preserve individual identity and context at the cost of volume and query expense. Traces are the structural projection: they capture causal relationships between units of work at the cost of propagation complexity and sampling tradeoffs.

No single projection can reconstruct the full picture. A metric tells you something is wrong. A log tells you what happened in one place. A trace tells you why it happened across places. The skill isn't choosing the right pillar — it's knowing which projection answers the question you're currently asking and being able to pivot between them using correlation identifiers when the first projection isn't enough. If your pillars aren't linked, you have three separate tools. If they are, you have one observability system with three lenses.

## Key Takeaways

- **Metrics are pre-aggregated by design.** Their cost scales with the number of unique label combinations (cardinality), not with request volume, which is why they're cheap — and why they can never answer questions about individual events.

- **Cardinality is the single most important constraint in metrics systems.** Adding a high-cardinality label like user ID or request ID to a metric can produce millions of time series and destabilize your monitoring infrastructure.

- **Logs preserve individual event identity, and that's both their power and their cost.** Storage scales linearly with event volume, which is why log retention, sampling, and careful selection of what to log are operational necessities, not optimizations.

- **A trace is a graph of causally related spans, not a flat list.** Its unique value is representing the structure of a request's journey — what called what, in what order, and where time was spent — which neither metrics nor logs can capture.

- **Trace context propagation requires every service in the request path to participate.** A single uninstrumented service breaks the trace into disconnected fragments, which is why full-stack instrumentation is a prerequisite, not an enhancement.

- **Tail-based sampling retains interesting traces (errors, high latency) at the cost of architectural complexity; head-based sampling is simple but randomly discards the traces you most need during incidents.**

- **The three pillars only function as a system when they are linked by correlation identifiers** — trace IDs in log records, exemplars in metrics — allowing you to pivot from an aggregate anomaly to a specific event to a causal chain without manual timestamp matching.

- **If you're aggregating logs to produce a number, you need a metric. If you're joining logs across services to reconstruct a call path, you need a trace.** Misusing one pillar as a substitute for another produces worse results at higher cost.


# Discussion

## Why This Conversation Is Happening

A lot of teams think they “have observability” because they’ve deployed the standard tooling set: metrics backend, log aggregator, tracing system, dashboards. Then an incident happens and they discover they still cannot answer basic questions fast enough: What is broken? Which requests are affected? Where in the call chain is the time going? They have data, but not a model of what that data actually represents.

What usually goes wrong is not lack of collection, but mismatch between question and data model. Teams ask metrics to explain a single bad request, ask logs to provide cheap real-time fleet-wide signals, or expect traces to be complete when context propagation or sampling broke them. The result is slow incident response, expensive storage, misleading dashboards, and blind spots exactly where engineers expected clarity.

If you do not understand the mechanics underneath metrics, logs, and traces, you inherit bad defaults without noticing: high-cardinality metrics that blow up the backend, massive log volumes doing the job of metrics, traces that look “enabled” but are fragmented and missing the requests you care about. The practical problem is not terminology. It is that the wrong representation gives you the wrong answers.

---

## What You Need To Know First

**Aggregation**  
Aggregation means combining many raw events into a summary. Instead of storing “request A took 230ms” and “request B took 410ms,” you might store bucket counts or totals that summarize many requests over time. Aggregation is what makes metrics cheap and fast, but it also destroys detail. Once data has been folded into a summary, you cannot recover the original events from it.

**Labels / dimensions**  
A label is a key-value tag attached to telemetry, like `method=GET` or `status=500`. Labels let you break data down by category. In metrics systems, every unique combination of label values creates a separate time series, so labels are useful but also dangerous when they have too many possible values.

**Distributed request flow**  
In a microservice system, one user request often becomes many internal operations: service A calls service B, which calls a database and service C, which calls an external API, and so on. Understanding system behavior means understanding not just isolated events, but how one unit of work triggers others across boundaries.

**Percentiles vs averages**  
An average gives you one central value, but it can hide outliers. Percentiles answer questions like “how slow are the slowest 1% of requests?” For latency, this matters because users often feel tail behavior, not the average. The article assumes you already care about that distinction because it changes what metrics need to capture.

---

## The Key Ideas, Connected

**The three pillars are different data structures, not three interchangeable views of the same data.**  
Metrics, logs, and traces exist because each preserves a different aspect of system behavior and throws away different information. That means each is good at different questions by construction, not by tooling preference. Once you see them as different data models, the rest of the tradeoffs make sense: cost, speed, failure modes, and query style all follow from what the system chooses to store.

**Metrics store pre-aggregated numerical summaries over time.**  
A metric is not a list of request events. It is a compact rolling summary: counters go up, gauges change, histogram buckets are incremented. The key consequence is that storage cost depends mostly on how many distinct time series you have, not how many raw events occurred. That is why metrics stay cheap even at high request rates and are suitable for alerting and dashboards. But the mechanism that makes them cheap is exactly what removes per-event identity. Since the raw events are never kept, metrics can tell you that latency got worse but can never tell you which exact request was slow. That limitation leads directly to the next idea: the central operational constraint in metrics is not event volume, but series explosion.

**In metrics systems, cardinality is the governing constraint because every unique label combination becomes a separate time series.**  
If you add labels with a small bounded set of values, you create a manageable number of series. If you add something unbounded like `user_id` or `request_id`, the number of time series multiplies dramatically. The backend must track each active series in memory and storage, so high cardinality can overload the monitoring system itself. This is why experienced engineers treat label choice as architecture, not decoration. Once you understand that metrics are compressed summaries indexed by label combinations, it becomes obvious why they cannot safely carry highly specific identifiers. Those detailed, high-cardinality facts need a different representation: logs or traces.

**Logs preserve individual events and their full attached context.**  
A log record keeps the event as an event: this request, this user, this downstream target, this error, this duration. That is why logs can answer highly specific forensic questions that metrics fundamentally cannot. But logs do this by storing each event separately, so cost scales with event volume. More requests means more records to ingest, index, and retain. This is not a tooling flaw; it is the direct price of preserving identity and detail. Because logs preserve arbitrary event context but not causal structure across services by default, they solve a different problem than metrics and expose the need for a representation that captures relationships, not just records.

**Traces capture causality and structure by representing work as a graph of related spans.**  
A trace is not just “logs with IDs” and not “metrics for a request.” It is a graph showing how one request moved through the system: which operation called which, what happened in parallel, and where time accumulated. That graph structure is the unique thing traces preserve. Metrics lose identity; logs preserve identity but flatten events unless you reconstruct relationships yourself. Traces explicitly encode the parent-child relationships, which is what lets you answer “why was this request slow?” in a cross-service sense. But because traces depend on linked spans from multiple services, they are only as complete as the context propagation that creates those links.

**Trace context propagation is the mechanism that turns isolated spans into one coherent trace.**  
When an incoming request starts a trace, the service creates identifiers for the overall request and for its own unit of work, then sends that context on downstream calls. Each downstream service must extract that context, create its own child span, and continue forwarding it. If any service fails to do that, the graph breaks into disconnected pieces. This means tracing quality is not just about “tracing turned on”; it depends on consistent participation across every hop. In polyglot systems, this is often where reality diverges from intent. And once you realize traces require cooperation everywhere, the next problem appears: even if propagation works, keeping every trace can be too expensive.

**Tracing at scale requires sampling, which means accepting intentional incompleteness.**  
A high-throughput system generates too many spans to retain all of them economically. Sampling is how you cap cost, but the way you sample determines what kinds of debugging are possible. Head-based sampling decides early and is operationally simple, but it randomly discards many traces before you know whether they were interesting. Tail-based sampling waits to see the outcome and can keep error or high-latency traces, but that requires buffering and more collector-side complexity. This is a direct tradeoff between cost predictability and diagnostic usefulness. Once traces are sampled and metrics are aggregated, you now have multiple incomplete projections of reality. To investigate effectively, you need a way to move between them.

**The main practical failure mode is not missing telemetry, but uncorrelated telemetry.**  
A team notices a latency spike in metrics, searches logs around that time, maybe opens traces, and still spends too long manually lining things up. That happens because the three data stores are not linked. Without shared identifiers, engineers are doing timestamp archaeology instead of investigation. Correlation identifiers solve this by letting a metric point to an example trace, and logs carry the trace ID that ties a local event back to the broader request path. The mechanism matters: the identifiers must be attached at instrumentation time and supported by the tooling path end to end. Otherwise the pillars remain separate systems.

**Using one pillar as a substitute for another creates both cost and clarity problems.**  
If you scan logs to compute latency numbers, you are paying event-level storage and query cost for a question that metrics answer naturally. If you reconstruct call chains by joining logs with request IDs, you are manually rebuilding something traces are designed to represent. This misuse happens when teams focus on “we have data” rather than “what representation fits this question?” The right mental move is to start from the question: aggregate fleet behavior suggests metrics; event-specific local detail suggests logs; cross-service causal structure suggests traces. That leads to the final model.

**The three pillars are three projections of one underlying stream of system activity, each preserving different information and discarding different information.**  
Metrics preserve aggregate shape and discard identity. Logs preserve event identity and local context but do not natively encode system-wide causality. Traces preserve causal structure across components but often via partial collection and fragile propagation. No one projection can reconstruct the others after the fact because the discarded information is truly gone. That is why observability is not about picking the “best” pillar. It is about knowing which lens fits the current question and designing the system so you can pivot between lenses when one stops being sufficient.

---

## Handles and Anchors

**1. Three cameras pointed at the same traffic intersection.**  
Metrics are the traffic counter: 400 cars per minute, average speed, congestion level. Logs are the police notebook: this specific car ran the light at 2:03 PM. Traces are the route map of one car through multiple intersections. Same reality, different captured information. You cannot reconstruct a single car’s route from the counter, and you cannot cheaply measure total traffic by reading every notebook entry.

**2. “Cheap means compressed; detailed means expensive.”**  
This sentence captures a lot. Metrics are cheap because they compress events into summaries. Logs are detailed because they keep events, and that costs money. Traces keep structure, which costs coordination and often sampling. If a system is both cheap and detailed, ask what information it is silently discarding.

**3. Ask: what question am I actually asking?**  
- “Is the fleet unhealthy right now?” → metric question.  
- “What happened to this exact request?” → log question.  
- “Why did this request become slow across services?” → trace question.  
This is a practical diagnostic handle you can use in real incidents and in design reviews.

---

## What This Changes When You Build

**An engineer who understands this will choose metric labels differently because every extra label combination creates real backend series cost.**  
The unaware engineer often adds labels like `user_id`, `session_id`, or `request_id` because they sound useful for slicing dashboards later. The consequence is a cardinality explosion that makes the metrics system slow, expensive, or unstable. The informed engineer restricts metric labels to bounded dimensions and routes high-cardinality detail into logs or traces instead.

**An engineer who understands this will instrument latency with histograms rather than relying on averages or precomputed per-instance percentiles because only histograms can be merged correctly across instances.**  
The unaware engineer sees a nice p99 on each pod or an average latency graph and assumes they can roll those up for the service. The consequence is misleading fleet-level latency visibility, especially in tail behavior. The informed engineer chooses histogram buckets deliberately at instrumentation time, knowing that bucket design constrains future analysis.

**An engineer who understands this will treat trace propagation as a cross-service integration requirement, not a library checkbox, because one non-participating hop breaks the causal graph.**  
The unaware engineer enables tracing in a few services and assumes traces are “on.” During an incident they discover fragmented traces and missing links right where the problem sits. The informed engineer verifies propagation through HTTP headers, async message metadata, gateways, and background workers, and tests for broken context paths explicitly.

**An engineer who understands this will choose a sampling strategy based on incident questions, not just cost targets, because sampling determines which failures are visible later.**  
The unaware engineer picks a low head-sampling rate to control spend and later finds that rare but important error traces are absent. The informed engineer asks whether the system must reliably retain slow/error traces and, if so, accepts the collector complexity of tail-based sampling or some hybrid policy.

**An engineer who understands this will add correlation identifiers across pillars because investigation speed depends on pivoting between representations without manual matching.**  
The unaware engineer leaves logs, metrics, and traces as separate tools and relies on timestamps and guesswork during incidents. The consequence is slow diagnosis and fragile human correlation. The informed engineer ensures logs carry trace IDs, metrics emit exemplars where possible, and tooling supports click-through from anomaly to trace to local event detail.

**An engineer who understands this will stop using logs as the default sink for every observability need because logs are the most expensive place to do metric or trace work badly.**  
The unaware engineer logs durations, aggregates them later, and stitches request IDs together to infer system paths. The consequence is huge log bills and slow queries for routine operational questions. The informed engineer keeps logs for event context, emits metrics for summaries, and uses traces for cross-service structure, reducing both cost and cognitive friction during debugging.
