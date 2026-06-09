## Metadata
- **Date:** 23-05-2026
- **Source:** 05_architectural_decision_making.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-05 · Architectural Decision-Making

The architectural debt in most systems is not bad code. It is decisions nobody can explain. Somewhere in the system's history, someone chose a message broker, a service boundary, a database, an authentication model — and then left. The decision remains, but the reasoning is gone. The next engineer to look at it cannot tell whether the choice was deliberate, accidental, or forced by a constraint that no longer exists. So they leave it alone. Then the engineer after them leaves it alone. And the system slowly calcifies around decisions that nobody understands and nobody dares to touch.

This is the problem architectural decision-making is built to solve, and it starts with a shift in how you think about decisions themselves. Most engineering decisions are reversible — you can refactor the function, rename the variable, swap the library. Architectural decisions are the ones where reversal is expensive: changing a service boundary, switching a storage engine, moving from synchronous to asynchronous communication. The cost of change is the defining property. And because the cost is high, the quality of the decision matters more, the documentation of the decision matters more, and the conditions under which you would revisit the decision matter more. Treating architectural decisions like ordinary decisions — made in a Slack thread, captured nowhere, justified by whoever was loudest in the meeting — is how you end up with the calcified system.

The discipline Richards & Ford advocate for is straightforward but not easy: when you make an architectural decision, you write it down, and you write down enough that someone who joins the team in two years can reconstruct your reasoning without finding you. The instrument for this is the Architecture Decision Record, or ADR. An ADR captures four things — the context that forced the decision, the decision itself, the alternatives that were considered, and the consequences (good and bad) that the decision is expected to produce. The format is not the point. The discipline of separating context from decision from alternatives from consequences is the point, because it forces you to make explicit the things that decisions usually leave implicit.

The piece that does the most work is the alternatives section. Most engineers, when documenting a decision, describe what they chose and why it is good. This is almost useless to a future reader, because the question they will be asking is not "is this choice good" but "is this choice still the best one given what we now know." That question can only be answered if you know what was rejected and why. An ADR that says "we chose Postgres because it fits our needs" tells the future reader nothing. An ADR that says "we considered Postgres, DynamoDB, and Cassandra; we rejected DynamoDB because we needed multi-table transactions, and we rejected Cassandra because our write volume did not justify the operational overhead, and we chose Postgres because the consistency model matched our domain" tells them everything. If write volume changes, or transaction needs change, the future reader knows immediately which decision is now suspect.

The consequences section is the other piece that earns its place. Every architectural decision costs something — that is the first law of software architecture, and pretending otherwise is how you produce decisions that cannot be defended when the costs eventually surface. Recording the consequences explicitly, including the bad ones, is what protects future engineers from believing the decision was free. It also creates the conditions under which the decision can be revisited honestly: if the recorded cost has grown beyond what was originally accepted, that is the signal that the decision needs to be reopened, not patched around.

The other instinct this discipline cultivates is knowing when to revisit a decision. Architectural decisions are not made once and locked forever — they are made under conditions, and when those conditions change, the decision should be reopened. Without ADRs, this never happens, because nobody remembers what conditions the decision was made under. With ADRs, the conditions are the first thing in the document. When you find yourself working around an old decision repeatedly, you go back to its ADR, check whether the original context still holds, and either reaffirm the decision (with a new ADR explaining why it still applies) or replace it (with an ADR explaining what changed). The system's architectural history becomes legible.

The skill this topic builds is the discipline of treating architectural decisions as artifacts in their own right — things that exist, that are owned, that can be inspected, that can be challenged, and that can be replaced with reasoning rather than guesswork. Engineers who do this produce systems that remain reasonable to work in long after they themselves have moved on. Engineers who do not produce the systems everyone else inherits and resents. The difference is not how smart the decisions were. It is whether the decisions can still be explained.

## Level 2 candidates

**Architecture Decision Records (ADRs)** — The mechanics of writing ADRs well: what to include, what to leave out, where to store them, and how to keep them alive as the system evolves rather than letting them rot. Worth a deep dive because the format is simple but the practice of writing ADRs that future engineers actually use — rather than skim and ignore — has real craft to it.

**Analyzing tradeoffs** — The framework for surfacing tradeoffs explicitly during the decision process: naming what is being gained, what is being given up, and under what conditions the tradeoff holds. Worth going deeper because most engineers can recognise tradeoffs in retrospect but struggle to make them explicit at decision time, which is when the analysis is actually useful.

**Anti-patterns in architectural decisions** — The recurring failure modes of architectural decision-making — covering your assets, email-driven architecture, decision by committee, decision by avoidance — and the structural reasons each one produces the systems nobody understands. Worth a separate post because recognising the anti-pattern in your own organisation is often the prerequisite for adopting the discipline at all.

**Fitness functions** — Automated checks that verify architectural characteristics are maintained as the system evolves, turning architectural intent into a continuous constraint rather than a decision documented once and forgotten. Worth deeper treatment because it is the bridge between decision-making (a one-time act) and architectural integrity (an ongoing property), and it changes how you think about what an ADR is actually for.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Ordinary decision vs architectural decision = cost of reversal

```python
# Cheap to change later: ordinary code decision
def price_label(amount):
    return f"${amount:.2f}"   # easy to reformat later


# Expensive to change later: architectural decision
# Order service writes directly into the same database schema as Billing.
def create_order(db, order):
    db.execute("INSERT INTO billing.orders ...")  # shared schema boundary

# Later "small" change request:
# "Split Billing into its own service"
#
# This now implies:
# - moving data ownership
# - changing APIs
# - changing deployments
# - changing failure modes
# - migrating old data
#
# Same codebase, but not the same kind of decision.
```

The point: architectural decisions are the ones where undoing them is expensive, not merely annoying.

---

### 2) Undocumented architecture becomes "do not touch"

```text
# What a future engineer sees

system/
  payment_service.py
  auth_gateway.py
  kafka_consumer.py
  postgres/
  redis/
  legacy_sync_api_client.py

Question: Why Kafka?
Answer in code: none

Question: Why sync client instead of async events?
Answer in code: none

Question: Why Redis for sessions?
Answer in code: none

Resulting team behavior:
if nobody knows why it exists:
    leave_it_alone()
```

If the reasoning is gone, people cannot tell whether a choice was deliberate, temporary, or obsolete. So the safest move becomes inaction.

---

### 3) Minimal ADR: context, decision, alternatives, consequences

```md
# ADR-007: Use PostgreSQL for order storage

## Context
- Orders need multi-step updates:
  create order + reserve inventory + record payment status
- We need strong consistency for these operations
- Team has PostgreSQL operational experience

## Decision
Use PostgreSQL as the primary order database.

## Alternatives considered
- DynamoDB
  - Rejected: transaction model is a worse fit for our multi-record workflow
- Cassandra
  - Rejected: high write scale benefits do not justify current operational cost

## Consequences
- Good: simpler transactional logic
- Good: lower operational risk for current team
- Bad: harder horizontal scaling than some distributed stores
- Bad: future migration cost if write volume grows sharply
```

The format is simple; the value is that it separates forces that are usually blurred together.

---

### 4) Bad ADR vs useful ADR

```md
# Bad
We chose PostgreSQL because it fits our needs.
```

```md
# Useful
We chose PostgreSQL.

Alternatives:
- DynamoDB: rejected because we need multi-record transactional consistency
- Cassandra: rejected because our current scale does not justify its ops overhead

Revisit if:
- write throughput grows beyond single-cluster comfort
- transaction requirements weaken
```

The second version helps with the future question: "Is this still the best choice under current conditions?"

---

### 5) Consequences are part of the decision, not an afterthought

```yaml
decision: "Use synchronous HTTP calls between services"

good:
  - simple request/response flow
  - easy to debug with logs

bad:
  - caller latency now depends on callee latency
  - failures can cascade across services
  - retries/idempotency become required
  - difficult to support offline processing later
```

If the bad consequences are not written down, future engineers may treat the decision as if it were free and "solve" the costs with endless patches.

---

### 6) Revisit decisions when conditions change

```python
adr = {
    "decision": "Use PostgreSQL",
    "context": {
        "needs_transactions": True,
        "write_volume": "moderate",
    }
}

current_system = {
    "needs_transactions": False,
    "write_volume": "very_high",
}

def should_revisit(adr, current):
    return adr["context"] != current

if should_revisit(adr, current_system):
    print("Open new ADR: original conditions no longer hold")
else:
    print("Decision still fits")
```

An ADR is not a permanent lock. It records the conditions under which a choice made sense, so you can detect when those conditions stop being true.

---

## Key Ideas

Architectural decision-making is about treating expensive-to-reverse choices as first-class artifacts instead of tribal knowledge. The sketches show the progression: some decisions are costly because they shape boundaries and failure modes; when their reasoning is lost, teams freeze and preserve them by default; an ADR makes the decision legible by recording context, alternatives, and consequences; the alternatives section is what lets future engineers judge whether the choice still fits; the consequences section makes the cost explicit; and once the original conditions change, the right move is not blind loyalty to the old choice but a new decision with new reasoning.

</details>