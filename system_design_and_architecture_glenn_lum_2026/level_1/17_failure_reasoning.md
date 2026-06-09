## Metadata
- **Date:** 23-05-2026
- **Source:** 17_failure_reasoning.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-17 · Failure Reasoning

The instinct most engineers develop early is to reason about systems in terms of what they do when they work. You design the happy path, write tests for a few obvious error cases, and trust that the rest will be caught in code review or staging. This is the wrong starting point for any system above a certain size. Above that threshold — somewhere around the point where your system has more than one process, more than one machine, or more than one team touching it — the interesting design question is not what the system does when it works. It is what the system does when it fails, because it will, and the shape of that failure is determined by decisions you made long before the failure occurred.

Failure reasoning is the discipline of thinking about failure modes as a first-class design input rather than a post-hoc concern. It treats the question "how does this break?" as equal in weight to "how does this work?" — and in distributed systems, often more important, because the ways a system can break vastly outnumber the ways it can succeed. The goal is not to prevent all failures (you can't) or to enumerate every possible one (you can't do that either). The goal is to design systems where failures are contained rather than cascading, detectable rather than silent, and recoverable rather than terminal. Each of those three properties is a distinct design choice, and each has costs.

The mental model worth carrying is that every system has a failure surface — the set of components, links, and interactions that can fail — and a failure topology — the way failures propagate when they do. A monolith on a single machine has a small failure surface and a trivial failure topology: when the machine dies, the system dies, and the failure is total but contained. A microservices system has a vastly larger failure surface (every service, every network link, every dependency between them) and a complex failure topology, where a single slow downstream service can starve thread pools upstream and bring down components that have no logical relationship to the original fault. The architectural choice between these two is, among other things, a choice about which failure topology you want to manage. Engineers who skip this analysis tend to discover their failure topology in production, one outage at a time.

The hardest failures to reason about are the partial ones. A machine that is fully dead is easy: it stops responding, your health check fails, your load balancer routes around it. A machine that is half-dead — accepting connections but not processing them, returning stale data, responding slowly enough to consume your retry budget without actually serving requests — is the failure mode that takes systems down. Burns' distributed patterns spend much of their complexity budget on this problem; Kleppmann's data layer treatment is largely a catalogue of partial-failure modes (replication lag, split brain, lost writes during failover) that look like working systems until they don't. The discipline here is to assume that any component can fail in any of the ways short of clean death, and to design boundaries that contain that ambiguity rather than propagate it.

Three properties matter most for designing failure-aware systems. Containment is whether a failure stays where it happens or spreads — and the architectural mechanisms that produce containment (bulkheads, circuit breakers, timeouts, failure domains) are all about deliberately introducing seams where failures can stop. Detection is whether you can tell that a failure has occurred — and the harder problem is detecting partial failures and silent corruption, where the system continues to operate but produces wrong answers. Recovery is whether the system can return to a correct state after the failure, which depends on properties like idempotency, durability of state, and the ability to replay or reconstruct work. Each of these properties is built into the system or it isn't; none of them can be retrofitted cheaply once the architecture is fixed.

The reason failure reasoning runs across all three of the foundational books is that failure manifests at every layer simultaneously. Richards & Ford's fitness functions are how you encode failure-relevant invariants as continuous architectural constraints — preventing the slow erosion that turns a graceful system into a brittle one. Burns' patterns are largely structural answers to specific distributed failure modes — leader election exists because coordinator failure is a problem, sidecars exist partly because cross-cutting failure handling needs to be modular. Kleppmann's data layer is where the most subtle failures live: clock skew producing ordering anomalies, replication lag producing stale reads, isolation level violations producing write skew that survives every test until the day it doesn't. Reasoning about failure means moving fluently across these layers, because the symptom often appears in one layer and the root cause sits in another.

The skill this topic builds is the ability to look at a design and ask, before anything else, "what happens when this fails?" — and to keep asking it for every component, every link, every assumption. Strong systems thinking is not the absence of failures from your designs; it is the presence of explicit, defensible answers to that question for every part of the system. Engineers who have this skill produce systems that degrade gracefully under conditions they never anticipated. Engineers who don't produce systems that work beautifully in the demo and fail spectacularly under load. The difference is not in talent. It is in which question they ask first.

## Level 2 candidates

**Partial failure and cascading failure** — The failure modes unique to distributed systems, where a subset of components fails and the failure propagates to components that were functioning correctly. Worth depth because the mechanisms by which partial failures cascade (thread pool exhaustion, retry storms, timeout misalignment) are non-obvious and the mitigations (bulkheads, circuit breakers, backpressure) are specific patterns that need to be understood individually.

**Failure domain analysis** — The practice of mapping which components fail together and using that map to make architectural decisions about coupling, redundancy, and isolation. Worth depth because failure domain thinking is the bridge between abstract architectural choices and concrete reliability outcomes — and because most engineers have never been taught to draw the map explicitly.

**The trouble with distributed clocks** — Why time is unreliable in distributed systems and the specific correctness problems that arise when systems assume clocks are synchronised, including ordering anomalies, stale reads, and lease expiration races. Worth depth because clock-related failures are among the most counterintuitive in production and the standard mitigations (logical clocks, hybrid clocks, monotonic clocks) require their own conceptual model.

**Byzantine faults** — Failures where components behave incorrectly rather than simply stopping, and the class of systems where tolerating byzantine faults is a design requirement rather than an exotic concern. Worth depth because the boundary between "we trust our components" and "we don't" is an architectural decision with major cost implications, and the assumption is rarely made explicit.

**Designing for recoverability** — The architectural properties — idempotency, exactly-once semantics, durable state, replayable inputs — that make a system recoverable after failure rather than merely resilient while running. Worth depth because recoverability is a composite property built from several distinct mechanisms, each with its own cost, and the difference between a system that can recover and one that cannot is usually invisible until the failure that demands it.

**Detection and observability for failure** — The mechanisms by which failures become visible to operators and to the system itself, and why detecting partial failure is fundamentally harder than detecting clean failure. Worth depth because detection design is often treated as an operational concern rather than an architectural one, and the resulting blind spots are where the worst outages happen.

---


<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Happy-path thinking misses the real design question

```python
# "Works when everything works"
def place_order(user_id, item_id):
    reserve_inventory(item_id)     # service A
    charge_card(user_id)           # service B
    create_shipment(user_id)       # service C
    return "ok"
```

```python
# Same flow, but now ask: what happens when each step fails?
def place_order(user_id, item_id):
    reserve_inventory(item_id)     # what if this succeeds...
    charge_card(user_id)           # ...but this times out after charging?
    create_shipment(user_id)       # what if this fails after payment?
    return "ok"
```

The second version looks identical, but it exposes the real problem: success is one path; failure is many. Failure reasoning starts by treating each call as “may succeed, fail, or half-fail.”

---

### 2) Partial failure is worse than clean failure

```python
# Clean failure: fast, obvious
def call_service():
    raise ConnectionError("host down")
```

```python
# Partial failure: accepts work, but never finishes in time
import time

def call_service():
    time.sleep(30)   # looks alive, behaves dead
    return "ok"
```

```python
# Caller behavior changes completely depending on which failure it sees
def handle_request():
    try:
        result = call_service()
        return result
    except ConnectionError:
        return "fallback"
```

A clean crash triggers the `except`. A slow, half-dead dependency does not. It just ties up the caller until resources run out. In distributed systems, “slow” is often more dangerous than “down.”

---

### 3) Cascading failure often starts with retries

```python
# Bad: retries multiply load on an already struggling dependency
def fetch_profile(user_id):
    for _ in range(3):          # retry 3 times
        return downstream(user_id)
```

```python
# Service A handles one request by calling B
def handle_request(user_id):
    return fetch_profile(user_id)
```

If 100 incoming requests hit `handle_request()` and `downstream()` is slow, A may generate up to 300 downstream calls. The retry meant to improve reliability can become a retry storm.

A more honest version:

```python
def fetch_profile(user_id):
    try:
        return downstream(user_id, timeout=0.2)
    except TimeoutError:
        return "stale-profile"   # degraded result
```

Tradeoff: fewer retries reduces load and limits spread, but may return lower-quality results more often.

---

### 4) Containment requires explicit boundaries

```python
# Before: one shared worker pool handles everything
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(max_workers=10)

pool.submit(handle_payment, order)
pool.submit(send_email, order)
pool.submit(generate_report, order)
```

If `generate_report` hangs, it can consume the same workers needed for payments.

```python
# After: bulkheads isolate failure domains
payment_pool = ThreadPoolExecutor(max_workers=5)
email_pool   = ThreadPoolExecutor(max_workers=2)
report_pool  = ThreadPoolExecutor(max_workers=3)

payment_pool.submit(handle_payment, order)
email_pool.submit(send_email, order)
report_pool.submit(generate_report, order)
```

Now report failures hurt reports first. Cost: isolation reduces sharing efficiency; an idle pool cannot automatically lend capacity to a busy one.

---

### 5) Detection must distinguish “wrong” from “dead”

```python
# Naive health check
def health():
    return "OK"
```

A service can return `"OK"` while serving stale or corrupted data.

```python
# Better: probe a failure-relevant invariant
last_replicated_offset = 100
primary_offset = 125

def health():
    lag = primary_offset - last_replicated_offset
    if lag > 10:
        return "DEGRADED"   # alive, but unsafe for fresh reads
    return "OK"
```

This is failure reasoning in observability form: don’t ask only “is the process running?” Ask “is it still meeting the assumptions other components rely on?”

---

### 6) Recovery depends on idempotency

```python
# Dangerous: retry can double-charge
balance = 0

def charge(amount):
    global balance
    balance += amount
```

```python
charge(50)   # succeeds, but response is lost
charge(50)   # client retries
print(balance)   # 100
```

```python
# Safer: same operation ID can be replayed without applying twice
balance = 0
seen = set()

def charge(op_id, amount):
    global balance
    if op_id in seen:
        return
    seen.add(op_id)
    balance += amount
```

```python
charge("txn-123", 50)   # succeeds, response lost
charge("txn-123", 50)   # retry
print(balance)          # 50
```

Cost: you must store operation IDs somewhere durable enough to survive the failures you care about.

---

## Key Ideas

Failure reasoning means designing around the shape of failure, not just the shape of success. The sketches show that distributed systems break in partial, ambiguous ways; that retries and shared resources can spread one fault into many; that containment only happens when you introduce explicit boundaries; that detection must check meaningful invariants rather than mere liveness; and that recovery depends on properties like idempotency that must be designed in early. A system is not “reliable” because it avoids failure, but because its failures are limited, visible, and recoverable.

</details>