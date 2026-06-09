## Metadata
- **Date:** 23-05-2026
- **Source:** 10_foundations_of_data_systems.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-10 · Foundations of Data Systems

Most engineers learn to talk about data systems through the vocabulary of vendors. A database is "fast." A queue is "reliable." A cache is "scalable." These words feel like properties of the software, but they aren't — they are claims, and most of them collapse the moment you ask what they actually mean under load, under failure, or three years into a system's life. Kleppmann's opening move is to take the three words that get used most loosely — reliable, scalable, maintainable — and turn them into engineering properties with definitions you can argue about, measure, and trade off against each other.

Start with reliability. A reliable system is not one that doesn't fail; it is one that continues to work correctly when things go wrong. The distinction matters because failure is not optional. Hardware fails, software has bugs, networks partition, and humans make mistakes — and any definition of reliability that depends on these things not happening is a definition that will be falsified in production. The useful framing is fault tolerance: the system is designed so that specific anticipated faults do not become user-visible failures. A fault is a component deviating from its spec. A failure is the system as a whole stopping doing what users need. Reliability engineering is the discipline of preventing the first from becoming the second — and the cost of that prevention is paid in complexity, redundancy, and operational overhead that has to be justified by the consequences of failure.

Scalability is the property that gets talked about most and understood least. It is not a synonym for "fast" or "big." Scalability is the question of what your strategy is when load increases — and to answer it, you have to first say precisely what load means for your system. Load parameters are workload-specific: requests per second, ratio of reads to writes, number of simultaneous users, hit rate on a cache. Twitter's load is dominated by the fan-out of a single tweet to millions of timelines; a payments system's load is dominated by transactional throughput at peak hours; an analytics warehouse's load is dominated by the size of the scans, not the rate of them. The right load parameters are the ones that capture what actually constrains your system, not the ones that are easy to measure.

Once load is defined, performance under load is the next question — and this is where averages start to lie. The mean response time tells you almost nothing about what users actually experience. What matters is the distribution: the median tells you the typical case, but the high percentiles (p95, p99, p999) tell you what your worst-served users see, and those users are disproportionately your most engaged ones, since heavier users make more requests. Tail latency is not a corner case; it is the experience of the people who use your system most. Designing for percentiles rather than averages is one of the small mental shifts that separates engineers who reason about systems from engineers who report on them.

Maintainability is the property engineers most often dismiss as soft and most often pay for hardest. The majority of the cost of software is not in its initial development but in its ongoing maintenance — fixing bugs, adapting to new requirements, paying down technical debt, onboarding new engineers, migrating off deprecated dependencies. A system that is hard to maintain extracts that cost from every team that touches it, forever. Kleppmann decomposes maintainability into three sub-properties that make it concrete: operability (can the operations team keep the system running smoothly), simplicity (can a new engineer understand the system without losing their mind), and evolvability (can the system be changed as requirements change). None of these are accidental. They are designed in or designed out at the architectural level, and bolting them on later is harder than building them in from the start.

The reason to put all three together is that they are in tension. Reliability often demands redundancy and complexity, which work against simplicity. Scalability often demands distribution, which makes both reliability (more components, more failure modes) and maintainability (more operational surface area) harder. Maintainability sometimes demands choosing a less performant solution because the more performant one is harder to understand. There is no architecture that maximises all three; there are only architectures that have made specific tradeoffs explicit and architectures that have made them by accident. The first move in designing a data system that holds up in production is to surface these tradeoffs deliberately — to say what your reliability target is, what load you are designing for, what maintainability you are willing to sacrifice — rather than letting them be settled by whoever wrote the first prototype.

The skill this topic builds is the ability to read a data system claim and translate it into the underlying engineering question. "This database is highly available" becomes: against what faults, with what recovery time, at what consistency cost? "This system scales to a million users" becomes: along what load parameter, with what response time at what percentile? "This service is easy to maintain" becomes: operable by whom, simple to whom, evolvable in what direction? Once you can do this translation reflexively, every conversation about data systems becomes more useful — because the words stop being marketing and start being specifications you can hold a system to.

## Level 2 candidates

**Reliability, scalability, maintainability defined** — The precise engineering definitions of the three properties and the distinction between faults and failures, hardware vs. software vs. human error, and the specific sub-properties (operability, simplicity, evolvability) that make maintainability concrete. Worth going deeper because each of these terms hides a lot of structure that determines what design choices actually mean in practice.

**Describing load and performance** — The tools for quantifying system behaviour: load parameters, throughput, response time distributions, percentiles, and the relationship between load and latency under saturation. Worth going deeper because most engineers reason about performance using averages, and percentile thinking changes both what you measure and what you optimise.

**Approaches to coping with load** — Vertical vs. horizontal scaling, stateless vs. stateful services, and the architectural patterns that follow from each — and why "scaling" is not one decision but a family of decisions with different costs. Worth going deeper because the choice of scaling strategy constrains the rest of the architecture in ways that are expensive to reverse.

**Data models and query languages** — How the choice of data model (relational, document, graph) shapes what queries are natural and what queries are painful. Worth going deeper because this is the decision that determines the access patterns your system can serve efficiently, and it is hard to undo once data has accumulated.

**Encoding and data evolution** — How data serialised today must be readable by code written tomorrow — forward and backward compatibility, schema evolution, and the encoding formats that handle this well or badly. Worth going deeper because schema evolution is a problem that looks small until you are mid-migration on a system with five years of data and three live consumers.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Reliability: a fault is local; a failure is user-visible

```python
# A payment service depends on a database.

def charge_card(db, user_id, amount):
    db.write({"user": user_id, "amount": amount})   # may throw
    return "charged"

# Fault: the DB process crashes.
# Failure: users cannot complete payment.

# A more reliable version does not prevent faults.
# It stops one fault from immediately becoming a user-visible failure.

def charge_card_with_retry(primary_db, replica_db, user_id, amount):
    event = {"user": user_id, "amount": amount}

    try:
        primary_db.write(event)
        return "charged"
    except DatabaseDown:
        replica_db.write(event)   # fallback path
        return "charged"

# Tradeoff:
# + tolerates one anticipated fault
# - more complexity
# - may create consistency problems if primary and replica diverge
# - only reliable against faults you designed for
```

The key move is: reliability is not “nothing breaks,” but “the system still does the right thing when something breaks.”

---

### 2) Reliability depends on what “correctly” means

```python
# Two systems both "stay up" during an outage.
# Only one preserves the required correctness.

inventory = {"book": 1}

def reserve_book_naive():
    # If two requests run at the same time, both may see 1.
    if inventory["book"] > 0:
        inventory["book"] -= 1
        return "reserved"
    return "sold out"

# Better pseudocode:
#
# BEGIN TRANSACTION
#   SELECT stock WHERE item='book'
#   IF stock > 0:
#       UPDATE stock = stock - 1
#       COMMIT
#       return "reserved"
#   ELSE:
#       ROLLBACK
#       return "sold out"

# Tradeoff:
# + prevents overselling
# - coordination adds latency and limits throughput
```

A system that returns answers quickly but violates an important invariant is not “reliable” in the way users care about.

---

### 3) Scalability starts by naming the load parameter

```python
# Same endpoint count, very different load.

# System A: chat app
requests_per_second = 5_000
payload_bytes = 200

# System B: analytics API
requests_per_second = 50
payload_bytes = 50_000_000

# If you only report "RPS", A looks harder.
# If network or scan size is the bottleneck, B may be harder.

def load_signature(rps, bytes_per_request):
    return {
        "rps": rps,
        "mb_per_sec": rps * bytes_per_request / 1_000_000
    }

print(load_signature(5_000, 200))         # {'rps': 5000, 'mb_per_sec': 1.0}
print(load_signature(50, 50_000_000))     # {'rps': 50, 'mb_per_sec': 2500.0}
```

“Scales to a million users” is not meaningful until you say what kind of work those users create.

---

### 4) Averages hide pain; percentiles reveal it

```python
latencies_ms = [20, 22, 19, 21, 20, 18, 500, 900]

mean = sum(latencies_ms) / len(latencies_ms)  # 190.0 ms

sorted_lat = sorted(latencies_ms)
p50 = sorted_lat[ len(sorted_lat) // 2 ]      # 21 ms
p95 = sorted_lat[-1]                          # rough sketch: 900 ms

print("mean:", mean)
print("p50 :", p50)
print("p95 :", p95)
```

Possible output:

```text
mean: 190.0
p50 : 21
p95 : 900
```

If you only report the mean, the system sounds “190 ms fast.” But most requests are ~20 ms, and some users experience ~900 ms. Tail latency is where “the system feels bad” lives.

---

### 5) Scaling out improves one bottleneck by introducing others

```python
# Before: one server, simple but limited
counter = 0

def increment_single_node():
    global counter
    counter += 1
    return counter

# After: two shards, more capacity, more complexity
shard_a = 0
shard_b = 0

def increment_sharded(user_id):
    global shard_a, shard_b
    if user_id % 2 == 0:
        shard_a += 1
        return shard_a
    else:
        shard_b += 1
        return shard_b

def total_count():
    return shard_a + shard_b
```

What changed?

- `increment_single_node()` is simple, but all writes hit one machine.
- `increment_sharded()` spreads load.
- But now:
  - there is no single global sequence
  - rebalancing shards is hard
  - queries like “top 100 across all shards” require coordination

Horizontal scaling is not “same system, just more machines.” It changes the shape of the problem.

---

### 6) Maintainability: the shorter clever version can be the worse system

```python
# Hard to understand/change
def price(o):
    return sum(i["p"]*i["q"] for i in o if i["t"]!="gift") * (0.9 if len(o)>10 else 1)

# Easier to operate and evolve
def subtotal(items):
    return sum(item["price"] * item["qty"] for item in items)

def billable_items(items):
    return [item for item in items if item["type"] != "gift"]

def discount_rate(items):
    return 0.9 if len(items) > 10 else 1.0

def price_clear(order_items):
    items = billable_items(order_items)
    return subtotal(items) * discount_rate(order_items)
```

The second version is not “better” because it is longer. It is better because future engineers can change discount rules, debug billing issues, and add logging without decoding a compressed expression first.

Maintainability becomes concrete when you ask:
- Can someone operate this?
- Can someone understand this?
- Can someone change this safely?

---

## Key Ideas

The sketches show that “reliable,” “scalable,” and “maintainable” are not vendor adjectives but design choices you can test against concrete situations. Reliability means faults happen but do not necessarily become user-visible failures, and that only matters relative to a correctness rule worth protecting. Scalability begins with identifying the actual load parameter, not repeating generic claims about traffic, and performance must be judged by distributions, especially tail latency, not averages. Finally, every attempt to improve capacity or resilience tends to add complexity, which is why maintainability matters: if a system cannot be understood, operated, and evolved, its future cost will dominate its present speed.

</details>