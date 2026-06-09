## Metadata
- **Date:** 23-05-2026
- **Source:** 04_architectural_styles.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-04 · Architecture Styles

Most engineers who have worked inside a system for any length of time can tell you what it does, but struggle to tell you what it is. They can describe the services, the queues, the database, the deployment pipeline — but if you ask them what shape the system has, the answer comes out as a list of components rather than a structural claim. This is the gap that architecture styles fill. A style is not a label you apply after the fact; it is a structural commitment that determines what the system is good at, what it is bad at, and what kinds of changes it will resist.

An architecture style is a named, reusable structural pattern with known characteristics, known tradeoffs, and a known domain of applicability. The three clauses each carry weight. Named, because shared vocabulary is what makes architectural conversations possible — when two engineers say "event-driven," they should be reaching for the same mental model. Known characteristics, because every style has a profile of what it is structurally good at: layered architectures are simple, microservices are deployable, space-based architectures are extreme-scale. Known tradeoffs, because every characteristic comes at a cost — layered architectures scale poorly, microservices are operationally complex, event-driven systems are hard to reason about. Known domain of applicability, because no style is universally correct; each fits some problems and actively misfits others.

The catalogue Richards & Ford build is not a menu. The mistake engineers make when they first encounter the styles — layered, pipeline, microkernel, service-based, event-driven, space-based, microservices, modular monolith — is to treat them as options to choose from at the start of a greenfield project. That framing misses the point. The catalogue is primarily a vocabulary for recognising what a system already is. Most of the systems you will work on were not designed; they accreted. They started as one style, drifted toward another, and now exhibit characteristics of both without the discipline of either. The first job of the catalogue is to let you name what you are looking at so you can reason about whether it is the right thing to be.

The styles divide along two axes that are worth holding in your head. The first axis is monolithic versus distributed: does the system run as a single deployment unit, or as multiple units coordinating across a network? Layered, pipeline, microkernel, and modular monolith are monolithic. Service-based, event-driven, space-based, and microservices are distributed. The second axis is technically partitioned versus domain partitioned: are the boundaries inside the system drawn by technical role (presentation, business logic, persistence) or by business domain (orders, inventory, payments)? Layered architecture is the canonical technically partitioned style; microservices are the canonical domain partitioned one. These two axes will not tell you which style you have, but they will narrow the field quickly when you are reading an unfamiliar system.

The reason this matters in practice is that structural problems are visible in the style long before they are visible in the code. If a team is complaining that every change requires touching three layers and coordinating two deployments, you do not need to read the code to know they are in a layered architecture being asked to do domain-partitioned work. If a team is complaining that they cannot trace a request through their system without piecing together logs from seven services, you do not need to read the code to know they are in an event-driven architecture without the observability investment that style demands. The style predicts the pain. Once you can read the style, you can predict the pain — and more importantly, you can tell whether the pain is essential to the style (and therefore the price of admission) or accidental (and therefore fixable without restructuring).

The other reason styles matter is that they make the cost of change legible. Every style has a set of changes it absorbs cheaply and a set it resists violently. A modular monolith absorbs changes within a module cheaply and resists changes that cut across modules. Microservices absorb independent service changes cheaply and resist changes that require coordinated updates across services. Event-driven systems absorb new consumers cheaply and resist changes to event schemas. The style is, in effect, a prediction about which future changes will be easy and which will be expensive. Choosing a style is choosing which future you are betting on.

The skill this topic builds is the ability to read a system structurally rather than componentially. Given an unfamiliar codebase, deployment topology, and team structure, you should be able to name the dominant style within an hour, identify where the system has drifted from it, and predict the three or four classes of change that will be most painful. That diagnostic capability is the foundation for everything else: it is what lets you ask whether the style fits the characteristics the system actually needs, whether the operational complexity is justified, whether the team is fighting the architecture or working with it. Without it, every architectural conversation is about components. With it, the conversation is about structure — which is where the leverage actually lives.

## Level 2 candidates

**Styles vs. patterns** — The distinction between an architecture style (a system-level structural choice) and a design pattern (a local solution to a recurring problem). Worth a deep dive because conflating the two is one of the most common sources of confused architectural conversations, and untangling it sharpens the rest of the vocabulary.

**Layered architecture** — The default style most systems start in: simple, technically partitioned, and quietly limiting. Worth deeper treatment because understanding precisely why it scales poorly and deploys awkwardly is what explains the migration pressure that pushes teams toward other styles, often before they need to go.

**Event-driven architecture** — Asynchronous, decoupled, high-scalability, and the hardest style to reason about. Worth a Level 2 because its failure modes — eventual consistency, lost events, ordering problems, debugging opacity — are the prerequisite knowledge for using it without quietly building a system nobody can operate.

**Microservices architecture** — The style most often adopted without understanding what it actually costs. Worth a deep dive because the gap between the marketing characteristics (deployability, scalability, team autonomy) and the operational reality (network complexity, distributed data, observability burden) is where most failed microservices migrations live.

**Modular monolith** — The style that combines the deployment simplicity of a monolith with the modularity discipline of microservices. Worth deeper treatment because it reframes the microservices decision: the question stops being "monolith or microservices" and becomes "is the operational complexity of distribution justified by what modularity alone cannot give you."

**Choosing the right style** — The framework for mapping characteristic requirements to style candidates. Worth a Level 2 because the actual practice — surfacing the non-negotiable characteristics, eliminating styles that cannot deliver them, and choosing among what remains — is a repeatable discipline rather than the intuitive judgment most engineers treat it as.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### Sketch 1 — A style is a structural claim, not a component list

```text
System A
- web/
- service/
- db/
- queue/

This is only a parts list.
It tells us what exists, not what shape the system has.
```

```text
System B: Layered monolith
request
  -> controller layer
  -> business layer
  -> persistence layer
  -> database

Structural claim:
- single deployment unit
- boundaries drawn by technical role
- changes often flow through multiple layers
```

```text
System C: Microservices
client
  -> order-service -> order-db
  -> payment-service -> payment-db

Structural claim:
- multiple deployment units
- boundaries drawn by business domain
- coordination happens over the network
```

Same kinds of components can appear in all three.  
The style is the rule for how they are arranged and how change flows.

---

### Sketch 2 — Two fast classification axes: monolith/distributed and technical/domain boundaries

```python
def classify(deployments, boundaries):
    if deployments == 1 and boundaries == "technical":
        return "likely layered monolith"
    if deployments > 1 and boundaries == "domain":
        return "likely microservices"
    if deployments == 1 and boundaries == "domain":
        return "likely modular monolith"
    if deployments > 1 and boundaries == "technical":
        return "likely service-based or mixed style"
```

```python
print(classify(1, "technical"))  # layered monolith
print(classify(12, "domain"))    # microservices
print(classify(1, "domain"))     # modular monolith
```

This does **not** identify every style exactly.  
It is a narrowing tool: first ask “how many deployment units?”, then ask “what are the boundaries for?”

---

### Sketch 3 — Style predicts which changes are cheap and which are expensive

#### Layered architecture: easy technical separation, expensive feature changes

```python
# To add "discount codes" in a layered system:

# presentation.py
def apply_discount_endpoint(req):
    return service.apply_discount(req.code, req.cart)

# service.py
def apply_discount(code, cart):
    discount = repo.find_discount(code)
    return total(cart) - discount.amount

# repository.py
def find_discount(code):
    return db.query("select amount from discounts where code=?", code)
```

A single feature crosses controller → service → repository.  
That is normal in a layered system.

Cost profile:
- cheap: replacing logic inside one layer
- expensive: end-to-end feature work that touches many layers

#### Microservices: easy independent service change, expensive coordinated change

```text
Change request: rename event field "customer_id" -> "user_id"

order-service publishes:   { "user_id": 42 }   # changed
billing-service expects:   { "customer_id": 42 }  # not changed yet

Result:
- publisher deploys fine
- consumer breaks at runtime
```

Cost profile:
- cheap: changing one service internally
- expensive: changes that require coordination across services or schemas

---

### Sketch 4 — Recognize architecture pain from the structure before reading code

```text
Symptom:
"Every small change needs edits in controller, service, repository,
plus a full-app deployment."

Likely structure:
layered monolith

Likely reason:
the system is partitioned by technical role, so one business change
cuts across multiple layers.
```

```text
Symptom:
"We cannot follow one customer action without checking logs from
five services and a message broker."

Likely structure:
distributed, probably event-driven or microservices

Likely reason:
the request path crosses process boundaries, so observability is now
part of the architecture, not an optional tool.
```

The point is diagnostic:  
you can often predict the pain from the shape of the system alone.

---

### Sketch 5 — Drift: systems often become hybrids without the discipline of either style

#### Started as a clean layered monolith

```text
app/
  controllers/
  services/
  repositories/
```

#### Then "just one extraction"

```text
app/
  controllers/
  services/
  repositories/
invoice-service/   # separate deploy now
```

#### Then cross-boundary shortcuts appear

```python
# monolith service calling remote service directly
def checkout(order):
    save_order(order)                 # local DB
    http.post("http://invoice/create", order)  # remote call
    send_confirmation(order)
```

Now the system has mixed assumptions:
- some calls are in-process, some are over network
- some failures are exceptions, some are timeouts
- developers may still think “it’s basically a monolith”

That mismatch is architectural drift.  
Naming it matters because operating a hybrid requires different discipline than pretending it is one clean style.

---

### Sketch 6 — Choosing a style means choosing which future changes you want to be cheap

| Likely future change | Style that tends to absorb it cheaply | What becomes expensive instead |
|---|---|---|
| Add new business modules inside one deployable app | Modular monolith | Cross-module coupling |
| Deploy one business capability independently | Microservices | Cross-service coordination |
| Add new consumers of existing business events | Event-driven | Event schema evolution, debugging |
| Keep implementation simple for a small team | Layered monolith | Growth in scale and cross-layer change |

A style is a bet:
```text
"We expect these kinds of changes often,
so we accept the costs required to make them cheap."
```

If the predicted future is wrong, the architecture will feel hostile.

---

## Key Ideas

Architecture styles are useful because they let you describe a system by structure rather than by inventory. The important questions are not “does it have services and a database?” but “is it one deployment or many?” and “are boundaries technical or domain-based?” Once you can answer those, you can usually predict where change will be easy, where it will hurt, and what kinds of complaints the team will have before opening the code. That is why style matters: it makes tradeoffs legible, exposes drift when a system becomes a messy hybrid, and turns architecture from vague opinion into a concrete claim about which future changes the system is designed to absorb.

</details>