## Metadata
- **Date:** 23-05-2026
- **Source:** 01_what_architecture_actually_is.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-01 · What Architecture Actually Is

Ask ten engineers what software architecture is and you will get two answers, repeated. One group will point at a diagram — boxes, arrows, the thing that lives in Confluence and gets updated twice a year. The other group will point at a person — the architect, the staff engineer, whoever happens to make the calls when a decision feels too big for a sprint planning meeting. Both answers are wrong in the same way: they describe the artefacts and rituals around architecture without saying what the thing actually is. And until you can say what it actually is, you cannot tell which of your decisions are architectural and which are not — which means you cannot tell which decisions deserve the scrutiny they need.

The more precise definition, the one this entire curriculum stands on, has three parts. Architecture is the structure of a system, plus the characteristics it must exhibit, plus the decisions that are hard to reverse. The structure is the part most engineers already recognise — components, their relationships, the shape of how the system is composed. The characteristics are the properties the system must have beyond doing what it functionally does — how fast, how reliable, how scalable, how secure, how easy to change. But the third clause is the one doing the real work, and it is the one most working definitions miss.

The decisions that are hard to reverse. That is the load-bearing phrase, and once you internalise it, a lot of confusion drops away. Architectural decisions are not architectural because they are big, or because they are made by senior people, or because they appear on a diagram. They are architectural because the cost of changing them later is high — high enough that you have to live with the consequences for a long time, high enough that getting them wrong shapes the work of every engineer who comes after you. Choice of database engine is usually architectural. Choice of variable name is not. Choice of whether services communicate synchronously or asynchronously is architectural. Choice of which logging library to use is usually not. The test is not size; it is reversibility.

This reframe is what separates architectural thinking from design thinking. Design decisions are the ones you can change cheaply — refactor the function, swap the implementation, rename the field. Architectural decisions are the ones that calcify the moment you ship them. A monolith you can split into services later is a different beast from a fleet of services you have to merge back together; both are possible, but the second is a multi-quarter project and the first is an afternoon of cargo-culted YAML. The asymmetry of cost is the architectural property. And once you are looking for that asymmetry, you start to see it everywhere — in your data model, in your service boundaries, in your deployment topology, in the contracts your APIs expose to clients you cannot control.

The reason this matters for you, as someone who already operates systems, is that architectural decisions are usually invisible until they hurt. Nobody tells you at the time that the choice of message broker is going to constrain your retry semantics for the next four years. Nobody tells you that picking a relational schema with deeply nested joins is going to make your eventual move to a read replica into a six-month project. The decisions get made, the system ships, the team moves on, and the cost of reversal accumulates silently. By the time the cost becomes visible — usually as a migration that nobody can scope, or a refactor that nobody dares to start — the original reasoning is gone, the original decision-makers are gone, and what remains is a structure that nobody chose and nobody owns. This is where most architectural debt actually comes from. Not from bad decisions, but from undocumented decisions whose original justifications evaporated.

Treating architecture as the set of high-cost-of-change decisions reorients how you behave at the moment those decisions are being made. You start to notice them. You start to ask, before the decision ships, what it would cost to undo. You start to write down why, because you know the why is what future engineers will need when they inherit the consequences. You start to distinguish between the decisions that deserve a meeting and a written record and the decisions that can be made in a pull request comment. This discrimination — between the reversible and the irreversible — is the core architectural skill, and it is the one that everything else in this curriculum builds on.

The practical takeaway is small but radical. When you look at a system, do not ask "what is the architecture" as if architecture were a document. Ask: which decisions baked into this system are now expensive to change? Those decisions, collectively, are the architecture. Some of them were made deliberately. Most of them were made by accident, by default, or by someone who did not realise they were making an architectural decision at all. The discipline you are building is the ability to tell the difference — and, going forward, to make those decisions on purpose.

## Level 2 candidates

**Architecture vs. design** — The boundary between architectural decisions and design decisions, framed not by scale but by reversibility. Worth deeper treatment because the line is genuinely fuzzy in practice and the diagnostic of "what does it cost to undo" needs concrete examples to become a usable instinct.

**The laws of software architecture** — Richards & Ford's two operating laws: everything is a tradeoff, and why is more important than how. Worth its own post because internalising these as working principles rather than slogans reshapes how you run architectural conversations and how you read other people's decisions.

**The role of the architect** — What the responsibilities of architectural thinking actually are, independent of job title or org chart position. Worth deeper treatment because the cultural assumption that architecture is a role rather than a practice is one of the main reasons engineers in operational positions fail to apply it to their own decisions.

**Architecture and DevOps intersection** — The specific places where architectural choices constrain or enable operational practice — deployment, observability, reliability, recoverability. Worth its own post because the link between structural decisions and operational outcomes is where architectural quality becomes legible to engineers who already live in the operational layer.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Architecture is not the diagram; it is the costly commitment inside the code

```python
# Two files in the repo.

# file: user_service.py
def get_user(user_id):
    return db.fetch("SELECT * FROM users WHERE id = ?", [user_id])

# file: README.md
# "Architecture: microservices, event-driven, cloud-native"
```

```python
# What actually constrains future work is this:
import psycopg2
db = psycopg2.connect("postgres://...")

def get_user(user_id):
    return db.fetch("SELECT * FROM users WHERE id = ?", [user_id])
```

Changing the README is cheap. Changing “this system is tightly coupled to PostgreSQL access patterns and SQL semantics” may be expensive. The architectural part is the commitment that survives contact with the system.

---

### 2) Reversibility is the test: design changes are cheap, architectural changes are not

```python
# Cheap-to-reverse design decision
def total_price(items):
    return sum(item.price for item in items)

# Later: easy refactor
def total_price(items):
    subtotal = sum(item.price for item in items)
    return apply_discount(subtotal)
```

```python
# Hard-to-reverse architectural decision
# Every caller assumes synchronous request/response.
def place_order(order):
    payment = charge_card(order.card, order.amount)   # blocks
    reserve_inventory(order.items)                    # blocks
    create_shipment(order)                            # blocks
    return {"status": "confirmed"}
```

```python
# Later: changing to async messaging is not a refactor.
def place_order(order):
    publish("orders.requested", order)
    return {"status": "pending"}  # API contract changed

# Now you also need:
# - message broker
# - retries / idempotency
# - eventual consistency handling
# - new client expectations
```

Renaming or refactoring a function is design. Changing the interaction model from sync to async changes contracts, failure modes, and operations. That is architecture.

---

### 3) Structure + required characteristics + hard-to-reverse decisions

```python
# Same feature: "download report"

# Option A: simple and direct
def download_report(report_id):
    return build_report(report_id)  # takes 12 seconds
```

```python
# Option B: different structure because of a required characteristic
# Requirement: "user must get a response in under 200ms"
def request_report(report_id):
    job_id = enqueue("build-report", report_id)
    return {"job_id": job_id, "status": "processing"}
```

```python
def report_status(job_id):
    return lookup(job_id)

def download_ready_report(job_id):
    return storage.read(job_id)
```

The feature is the same. The required characteristic changed: low latency for the initial request. That forces a different structure: queue, background worker, job status, storage. If many clients depend on this workflow, undoing it later is expensive. That makes it architectural.

---

### 4) “Big” is not the same as “architectural”

| Decision | Big-looking? | Hard to reverse? | Usually architectural? |
|---|---:|---:|---:|
| Rename `user_name` to `username` inside one module | No | Low | No |
| Split one service into 12 services | Yes | High | Yes |
| Pick PostgreSQL vs DynamoDB | Maybe | High | Yes |
| Switch logging library | Maybe | Low | Usually no |
| Public API returns sync result vs async job ID | No | High | Yes |
| Reorder helper methods in a file | No | Low | No |

The useful question is not “does this look important?” but “what will it cost to undo after other code, data, and teams depend on it?”

---

### 5) Architectural debt often comes from undocumented defaults

```python
# Day 1: someone makes a "small" choice
def save_order(order):
    db.execute("""
        INSERT INTO orders (
            id, customer_id, shipping_street, shipping_city, shipping_zip,
            billing_street, billing_city, billing_zip,
            item1_sku, item1_qty, item2_sku, item2_qty, item3_sku, item3_qty
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [...])
```

```text
Six months later:
- Need variable number of items
- Need read replicas
- Need partial updates
- Need analytics on addresses and items
- Nobody knows why this shape was chosen
```

```text
Now the "small choice" is expensive because:
- application code depends on this schema
- migrations are risky
- queries are awkward
- original reasoning is gone
```

Undocumented architectural decisions become debt because future engineers inherit the cost without the context needed to judge whether the cost is worth paying.

---

### 6) A tiny ADR is often enough: record the irreversible choice and why

```md
# ADR-007: Orders use asynchronous fulfillment

## Decision
Order API returns 202 Accepted and a tracking ID.
Fulfillment happens via message queue.

## Why
- checkout must respond under 300ms
- warehouse system is unreliable
- retries must not charge customer twice

## Consequences
- clients must poll or receive webhook
- eventual consistency in order status
- queue operations become mission-critical

## Revisit when
- warehouse API becomes reliable and fast
- most clients require immediate confirmation
```

This is not documentation theater. It captures the part future engineers will need when they ask, “Why is this system shaped this way, and what breaks if we change it?”

---

## Key Ideas

Architecture is best understood as the set of decisions embedded in a system that are expensive to reverse, especially those that shape structure and determine whether required qualities like speed, reliability, or scalability are possible. The sketches show that the real architecture lives less in diagrams and more in commitments like database choice, sync vs async communication, public API contracts, and schema shape. Small code changes are design when they are cheap to undo; they become architectural when other code, teams, and operational constraints start depending on them. Because these decisions often happen quietly and early, the practical skill is to notice them at decision time, ask what reversal would cost, and write down why the tradeoff was chosen.

</details>