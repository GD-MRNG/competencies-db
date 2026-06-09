## Metadata
- **Date:** 23-05-2026
- **Source:** 03_modularity_and_coupling.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-03 · Modularity and Coupling

The microservices-versus-monolith debate is one of the most exhausting conversations in software, and the reason it goes nowhere is that almost nobody in it is actually arguing about the same thing. One side is talking about deployment independence. Another is talking about team autonomy. A third is talking about scalability. Underneath all of them is a single property that nobody is naming directly: how independently the parts of the system can be understood, changed, and deployed. That property is modularity, and once you have a precise vocabulary for it, the deployment-topology argument shrinks back to its actual size — a tactical question downstream of a more fundamental one.

Modularity is not a vague aspiration about "clean code" or "separation of concerns." It is a measurable structural property of a system, and the thing that erodes it is coupling. Every dependency between two parts of a system is a constraint on changing either one in isolation. The more dependencies, and the stronger they are, the more the system behaves as a single unit regardless of how many files, services, or repositories it has been split into. A codebase with one deployable artefact and clean internal boundaries is more modular than a fleet of fifty microservices that all break when one schema changes. Deployment topology is downstream of coupling, not the other way around.

The first move in thinking clearly about this is to separate the two forces that determine whether a module is well-bounded. Cohesion describes how much the things inside a module belong together — whether the module has a single reason to exist. Coupling describes how much a module depends on what is outside it. The goal is high cohesion within and low coupling without, and these forces are in tension: pushing cohesion up often means pulling related concerns into a module that previously lived elsewhere, which can increase coupling at the new boundary. Real architectural decisions are tradeoffs along this axis, not absolutes.

The deeper move — and this is where Richards and Ford add something most engineers do not have language for — is to stop treating coupling as a binary "tight or loose" judgment. Coupling has a structure. The taxonomy they borrow is connascence: a precise vocabulary for describing both the nature of a coupling (what kind of agreement two components share) and its strength (how hard it would be to change the agreement). Two components that must agree on a name are coupled differently from two components that must agree on the meaning of a value, which is different again from two components that must execute in a particular order, or within a particular timing window. Some of these couplings are cheap to maintain and safe to leave in place. Others are architectural debt the moment they appear. Without this distinction, "reduce coupling" is advice you cannot act on; with it, you can look at a system and identify which couplings are paying their rent and which are quietly accumulating cost.

This is what makes the microservices-versus-monolith debate finally legible. The question is not whether to deploy as one artefact or many. The question is where your coupling lives and what kind it is. If your coupling is mostly at the level of names and types — components calling each other through stable interfaces — a monolith with disciplined module boundaries works fine, and splitting it into services adds operational cost without buying you anything. If your coupling is at the level of meaning, timing, or shared mutable state, splitting into services does not solve the problem; it distributes it across a network and turns latent bugs into production incidents. The distributed monolith antipattern is what happens when a team performs the deployment surgery without doing the coupling analysis first. They end up with all the operational complexity of microservices and none of the independence those services were supposed to provide.

The practical consequence is that modularity is something you can measure, not just feel. You can look at a component and ask: how abstract is it (does it expose interfaces or concrete implementations)? How stable is it (how many other components depend on it)? Where does it sit in relation to what Richards and Ford call the main sequence — the line along which abstractness and stability are in healthy balance? Components that are concrete and depended-on are painful to change. Components that are abstract and depend on nothing are over-engineered scaffolding. The metrics will not make the decision for you, but they turn modularity from a judgment call into a property you can track and argue about with evidence.

Once you have this vocabulary, you start seeing it everywhere. The decision about where to draw a service boundary is a decision about which couplings to make explicit and which to leave implicit. The decision about whether to share a database between services is a decision about accepting connascence of meaning across a service boundary, which is almost always the wrong answer. The decision about whether to extract a shared library is a decision about which kind of coupling you prefer — coupling through code (which versions together) or coupling through a service contract (which evolves independently but introduces network failure modes). These are not separate decisions. They are the same decision, asked at different scales.

The skill this topic builds is the ability to read a system structurally rather than topologically. Two engineers can look at the same architecture diagram and one will see "we have eight services" while the other will see "we have eight services that all share the same user table, so we have one service wearing a costume." The second engineer is doing architecture. The first is reading a deployment manifest. Modularity and coupling are the lens that gets you to the second view — and once you have it, most of the architectural decisions you have inherited from previous teams become legible as the tradeoffs they actually were, rather than the mysteries they appeared to be.

## Level 2 candidates

**Cohesion and coupling defined** — The two forces that determine whether a module is well-bounded, and the precise definitions that turn them into analytical tools rather than slogans. Worth going deeper because the tension between them is where most module-boundary decisions actually live, and most engineers operate on intuition without a vocabulary for the tradeoff.

**Connascence** — The taxonomy that replaces "tight" and "loose" coupling with a precise spectrum: connascence of name, type, meaning, position, execution, and timing, ordered by strength and locality. Worth going deeper because this is the single most useful upgrade to most engineers' coupling vocabulary, and it makes architectural conversations dramatically more concrete.

**Measuring modularity** — Abstractness, instability, and the distance from the main sequence — the metrics that turn modularity from a judgment call into a quantifiable property. Worth going deeper because the metrics expose structural problems that are invisible to code review, and they give you something to track over time as the system evolves.

**From modules to components** — How logical modules become deployable components, and why that mapping is itself an architectural decision rather than a mechanical translation. Worth going deeper because this is the layer at which the microservices-versus-monolith decision actually gets made, and most teams conflate the logical and physical decompositions to their cost.

**Component coupling patterns** — Acyclic dependencies, stable dependencies, stable abstractions: the principles that keep a component graph from becoming a tangled graph. Worth going deeper because these principles operate at the level above individual modules and govern the long-term health of the system as it grows, and most teams discover them only after violating them.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### Sketch 1 — One deployable can still be modular; many deployables can still be one system

```python
# Monolith with clear internal boundaries

class Pricing:
    def total(self, items): return sum(items)

class Checkout:
    def __init__(self, pricing): self.pricing = pricing
    def place_order(self, items): return self.pricing.total(items)

# Only dependency: Checkout -> Pricing interface/behavior
checkout = Checkout(Pricing())
print(checkout.place_order([10, 20]))
```

```python
# "Microservices" with hidden shared coupling

# service_a.py
# reads users.status directly from shared database

# service_b.py
# writes users.status = "ACTIVE"

# later: service_b changes meaning
# users.status = 1   # same column, new encoding

# service_a did not change deployment-wise,
# but it is still broken logically.
```

Same deployment unit does not imply bad modularity. Separate services do not imply independence. The real question is: if one part changes, what else must change with it?

---

### Sketch 2 — Cohesion: put together what changes for the same reason

```python
# Low cohesion: one class has unrelated reasons to change

class UserManager:
    def save_user(self, user): ...
    def send_welcome_email(self, user): ...
    def generate_monthly_report(self): ...
```

```python
# Higher cohesion: each module has one job

class UserRepository:
    def save_user(self, user): ...

class WelcomeMailer:
    def send(self, user): ...

class ReportGenerator:
    def monthly(self): ...
```

The second version is easier to understand because each piece has a single reason to exist. Cost: more parts, more boundaries, and sometimes more wiring.

---

### Sketch 3 — Coupling: the boundary matters more than the file count

```python
# Tighter coupling: depends on concrete internals

class MySQLUserRepository:
    def insert_row(self, name): ...

class UserService:
    def __init__(self):
        self.repo = MySQLUserRepository()   # hard-coded concrete dependency

    def register(self, name):
        self.repo.insert_row(name)
```

```python
# Looser coupling: depends on an abstract behavior

class UserRepository:
    def save(self, name): ...

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, name):
        self.repo.save(name)
```

In the first version, changing storage tends to ripple into `UserService`. In the second, the service mostly cares that "something can save users." Cost: abstraction can be overdone if there is only one implementation and no real variation pressure.

---

### Sketch 4 — Coupling has kinds: name is cheaper than meaning

```python
# Connascence of name: both sides must agree on the field name "email"

payload = {"email": "a@example.com"}

def handle_signup(data):
    return data["email"]
```

If one side renames `"email"` to `"user_email"`, the other breaks. Annoying, but usually easy to find and fix.

```python
# Connascence of meaning: both sides must agree on what "status" means

# producer
payload = {"status": 1}   # 1 means ACTIVE ... maybe

# consumer
def can_login(data):
    return data["status"] == 1   # assumes same meaning
```

This is stronger coupling. The field name can stay the same while the system still breaks because the meaning changed. These bugs are harder: the code runs, but does the wrong thing.

---

### Sketch 5 — Distributed systems often add timing coupling, not remove coupling

```python
# In-process call: simple execution coupling
inventory.reserve(item)
payment.charge(card)
shipping.create_label(order)
```

```python
# Split into services: now timing matters too

POST /inventory/reserve
POST /payment/charge
POST /shipping/create_label

# New failure mode:
# inventory succeeds
# payment times out
# shipping never runs
# system now needs retries / compensation
```

Breaking code into services did not remove the workflow coupling. It changed its kind. What was once ordinary call-order dependency is now call-order plus network failure plus timeout behavior. Cost: operational complexity.

---

### Sketch 6 — Shared database across services = one system with costume changes

```sql
-- "user-service" owns this table
CREATE TABLE users (
  id INT PRIMARY KEY,
  status VARCHAR(20)
);
```

```python
# billing-service
# reads users.status directly

def can_invoice(user_row):
    return user_row["status"] == "ACTIVE"
```

```python
# user-service decides to normalize values
UPDATE users SET status = 'A' WHERE status = 'ACTIVE';
```

`billing-service` is now broken even though no API contract changed. The services were coupled through shared storage and shared meaning. This is why "separate repos + separate deploys" can still behave like one application.

---

## Key Ideas

Modularity is about change independence, not packaging. The sketches show that good boundaries come from high cohesion inside modules and low coupling across them, but "low coupling" needs precision: some dependencies are just agreements on names, while others are deeper agreements on meaning, order, or timing. Those stronger forms of coupling are what make systems hard to change safely. Splitting a system into services does not automatically improve modularity; if the parts still share database schemas, meanings, or workflow timing, you have only moved the coupling around and often made it more expensive to manage.

</details>