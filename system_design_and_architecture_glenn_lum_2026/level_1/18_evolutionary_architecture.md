## Metadata
- **Date:** 23-05-2026
- **Source:** 18_evolutionary_architecture.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-18 · Evolutionary Architecture

The instinct most engineers carry into architecture work is that a good system is one that is correct today. The instinct evolutionary architecture asks you to develop is different and slightly uncomfortable: a good system is one that can be wrong today and corrected tomorrow without a rewrite. Those two goals pull in opposite directions more often than people admit. The decisions that make a system maximally correct for its current requirements — tight schemas, sharp service boundaries drawn around today's domain model, optimised data representations — are frequently the same decisions that make it expensive to change when the requirements move. And the requirements always move.

The naive response to this is to over-engineer for the future: add abstraction layers, generalise data models, build extension points for capabilities nobody has asked for. This is the failure mode evolutionary architecture is specifically designed to avoid. Speculative flexibility is not the same as evolvability. A system loaded with unused abstractions is harder to change, not easier, because every abstraction is a decision the next engineer must understand and respect. Evolutionary architecture is the opposite discipline: building the simplest system that solves today's problem while preserving the seams along which it will need to be cut tomorrow. It is closer to a gardening practice than a construction one — you are not trying to predict the final shape of the system, you are trying to keep it prunable.

The mental model that makes this concrete is the distinction between decisions that constrain the system's current behaviour and decisions that constrain the system's ability to be changed. A choice of database affects performance today; a choice of how data is encoded affects whether next year's deployment can read last year's records. A service boundary affects how the team works today; the contract at that boundary affects whether either side can be rewritten without coordinating with the other. Evolutionary architecture is the practice of recognising the second category and treating it with more care than the first, because the cost of being wrong is paid not at decision time but every time the system needs to change.

Three mechanisms recur across the literature, and they are worth holding together as a set rather than treating as separate practices. The first is fitness functions — automated, executable checks that verify the system continues to exhibit the architectural characteristics you decided it should have. If modularity matters, you write a test that fails when a forbidden dependency appears. If a service must respond within 200ms at the 99th percentile, you write a check that fails when it doesn't. Fitness functions turn architectural intent from a document people stop reading into a constraint the build pipeline enforces. They are how you prevent the slow drift between what the architecture is supposed to be and what it has actually become.

The second mechanism is schema and data evolution. This is the part of evolutionary architecture that lives in the data layer, and it is the part most often underestimated. Code can be redeployed in minutes; data accumulated over years cannot. The moment a system has writers and readers that deploy independently — which is almost any system worth talking about — schemas must support backward compatibility (new code can read old data) and forward compatibility (old code can read new data, ignoring fields it doesn't understand). The serialisation format is not a detail; it is the contract that determines whether the system can evolve at all. Choosing JSON without a schema, or Protobuf with disciplined field numbering, or Avro with a schema registry, is an architectural decision about how change will propagate through the system over time.

The third mechanism is incremental migration, and the canonical pattern is the strangler fig — wrapping a legacy system with a routing layer that gradually redirects traffic to its replacement, piece by piece, until the original can be removed. This works because it creates a seam: a place where the old system and the new system meet, where they can coexist, and where the cutover happens gradually rather than as a single high-stakes event. The principle generalises. Whenever you face a change too large to make atomically, the architectural move is to find or create a seam — an interface, a routing point, a feature flag, a versioned API — and then perform the change incrementally across that seam. Big-bang rewrites fail not because rewrites are bad but because they refuse the incremental discipline that makes change survivable.

Underneath all of this is a structural truth that Conway's Law makes explicit: systems come to mirror the communication structures of the organisations that build them. This means evolutionary architecture is not purely a technical discipline. If teams cannot change without coordinating with five other teams, the architecture cannot evolve faster than that coordination allows, regardless of how many fitness functions you write. The team topology is itself an architectural decision, and reorganising the teams is sometimes the most effective architectural change available. The corollary is that an architecture that fights the organisation will always lose; the architectures that evolve well are the ones whose seams align with the team boundaries, so that each team can evolve its piece without negotiating with the others.

The skill this topic builds is the ability to distinguish, at decision time, between optimising for correctness now and optimising for changeability later — and to make the call consciously rather than by default. Most architectural debt does not come from decisions that were wrong when made; it comes from decisions that were correct for the system as it existed but that closed off paths the system later needed to take. Evolutionary architecture is the practice of keeping those paths open without paying for ones you'll never use. It is what makes the difference between a system that ages into something maintainable and a system that ages into something nobody is willing to touch.

## Level 2 candidates

**Fitness functions as architectural tests** — Automated checks that verify architectural characteristics — modularity rules, performance budgets, dependency constraints — are maintained as the system evolves. Worth a deep dive because the practice of writing fitness functions is non-obvious: knowing which characteristics are testable, how to express them as executable checks, and how to integrate them into the build pipeline is the operational mechanism that makes evolutionary architecture real rather than aspirational.

**Schema evolution and backward compatibility** — The specific techniques — additive changes, optional fields, version negotiation, schema registries — that allow data formats to change without breaking existing readers or writers. Worth deeper treatment because the failure modes here are subtle and expensive: a single non-additive schema change can break replication, invalidate historical data, or force coordinated deployments across systems that were supposed to be independent.

**The strangler fig pattern** — The migration strategy for incrementally replacing a legacy system by routing traffic through a façade that gradually redirects to the replacement. Worth depth because the pattern's success depends on details most descriptions skip: where the seam is placed, how state is migrated alongside behaviour, and how to know when the legacy can finally be retired versus when the migration has stalled into permanent coexistence.

**Technical debt as architectural erosion** — The process by which small local decisions accumulate into structural degradation, and the practices that make the accumulation visible rather than silent. Worth a deeper post because the framing of debt as erosion (rather than as a backlog of cleanup tasks) changes how teams reason about prioritisation and changes which interventions actually slow the decay.

**Team topology and architecture** — Conway's Law, its inverse, and the practical implications of organising teams to match the architecture you want rather than the architecture you have. Worth depth because this is the architectural lever most engineers don't recognise as architectural — and the one that most often determines whether technical evolutionary practices actually result in systems that evolve.

---


<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Correct today vs changeable tomorrow

```python
# BEFORE: maximally correct for today's rule
def shipping_cost(order):
    if order.country == "US":
        return 5
    raise ValueError("Only US shipping supported")

# Works perfectly... until "support Canada" arrives.
# Change now means editing core logic and redeploying.


# AFTER: still simple, but with a seam where change is likely
RATES = {
    "US": 5,
    # "CA": 8 can be added later
}

def shipping_cost(order):
    try:
        return RATES[order.country]
    except KeyError:
        raise ValueError(f"Unsupported country: {order.country}")
```

The second version is not “future-proof”; it just keeps one likely axis of change isolated. The cost is a tiny bit more indirection now.

---

### 2) Speculative flexibility is not evolvability

```python
# BAD: generic abstraction invented before any real need
class AbstractShippingStrategyFactoryProvider:
    def get_factory(self):
        raise NotImplementedError

class ShippingContextManager:
    def __init__(self, provider):
        self.provider = provider

# Nothing here solves a real current problem.
# Every future change must first understand the abstraction.


# BETTER: simple code + one obvious seam
def shipping_cost(order):
    if order.country == "US":
        return 5
    if order.country == "CA":
        return 8
    raise ValueError("Unsupported")
```

Evolutionary architecture is not “add lots of extension points.” It is “keep the likely cut line visible.” The cost of over-abstraction is cognitive load and slower change.

---

### 3) Fitness functions make architecture executable

```python
# Goal: "billing must not depend on web"
# Instead of writing this in a wiki, enforce it.

FORBIDDEN = [("billing", "web")]

imports = {
    "billing": ["db", "email"],
    "web": ["billing"],   # OK: web can call billing
    "reporting": ["db"],
}

def test_architecture_dependencies():
    for module, deps in imports.items():
        for forbidden_source, forbidden_target in FORBIDDEN:
            if module == forbidden_source and forbidden_target in deps:
                raise AssertionError(
                    f"{forbidden_source} must not depend on {forbidden_target}"
                )

test_architecture_dependencies()
```

Now imagine someone changes `imports["billing"] = ["db", "web"]`: the build fails.  
This does not guarantee good architecture; it only guards one chosen property. The cost is maintenance: stale fitness functions become noise.

---

### 4) Schema evolution: additive changes survive independent deployment

```python
# v1 event written last month
event_v1 = {
    "id": 101,
    "total": 49.99
}

# v2 writer adds a field
event_v2 = {
    "id": 102,
    "total": 79.99,
    "currency": "USD"   # additive change
}

# old reader
def read_v1(event):
    return f"order={event['id']} total={event['total']}"

print(read_v1(event_v1))  # works
print(read_v1(event_v2))  # also works: ignores unknown field


# dangerous non-additive change
bad_event = {
    "id": 103,
    "amount": 79.99   # renamed from total
}

print(read_v1(bad_event))  # KeyError: coordinated deploy now required
```

Add fields; don’t casually rename or delete them. Data outlives code. The cost is carrying old fields and compatibility rules longer than feels clean.

---

### 5) Incremental migration needs a seam

```python
# Router in front of old and new implementations

def legacy_get_user(user_id):
    return {"source": "legacy", "name": "Alice"}

def new_get_user(user_id):
    return {"source": "new", "name": "Alice"}

USE_NEW_FOR = {42, 43}

def get_user(user_id):
    if user_id in USE_NEW_FOR:
        return new_get_user(user_id)
    return legacy_get_user(user_id)

print(get_user(10))  # legacy
print(get_user(42))  # new
```

This is the strangler fig in miniature: create a routing point, move traffic gradually, expand the set, then delete the legacy path. The hard part is not the `if`; it is keeping old and new behavior/data compatible during the migration.

---

### 6) Team boundaries can help or block evolution

```text
Architecture wanted:
- Team A owns checkout
- Team B owns catalog

Good seam:
checkout -> catalog API

Bad seam:
checkout code imports catalog tables directly
checkout code also writes inventory records
catalog code calls checkout internals
```

```python
# Good: one contract between teams
def get_product(product_id): ...
def place_order(cart): ...
```

```python
# Bad: changes now require cross-team coordination everywhere
SELECT * FROM catalog_products;      # Team A reads Team B's tables directly
UPDATE inventory SET stock = ...;    # Team A writes Team B's data
```

If team boundaries and system seams align, each team can change its part more independently. If they do not, the architecture may look modular in diagrams but behave like a monolith in practice.

---

## Key Ideas

Evolutionary architecture is not about predicting the future; it is about preserving cheap ways to respond when the future arrives. The sketches show the pattern repeatedly: keep likely change points isolated, avoid speculative abstraction, turn architectural intent into executable checks, treat data formats as long-lived contracts, make large changes incremental by introducing a seam, and align those seams with team boundaries so independent change is actually possible. The tradeoff is constant: a little more discipline and compatibility work now, in exchange for avoiding rewrites and coordinated breakage later.

</details>