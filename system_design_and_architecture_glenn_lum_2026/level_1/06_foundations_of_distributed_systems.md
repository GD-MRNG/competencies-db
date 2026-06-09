## Metadata
- **Date:** 23-05-2026
- **Source:** 06_foundations_of_distributed_systems.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-06 · Foundations of Distributed Systems

The fallacies of distributed computing are usually presented as a list of mistakes — the network is reliable, latency is zero, bandwidth is infinite, and so on — as if memorising them were the lesson. It isn't. The fallacies only become useful once you can see what they are fallacies *about*. Underneath each one is an invariant property of distributed systems that the developer's mental model has quietly ignored, and the fallacy is what happens when production forces that property back into view. This topic is about those underlying invariants — the ones that hold whether you are building microservices, a database cluster, a message queue, or a system you have not yet imagined.

The frame to start with is this: the moment a function call crosses a process boundary onto a network, it stops being a function call and becomes something else. It looks the same in your code — you invoke a method, you get a result — but the semantics have changed completely. The call can take milliseconds or minutes. It can succeed, fail, or do something worse than either, which is to succeed on the remote side and fail on the way back so that you cannot tell which happened. It can be retried and produce the same effect twice. The network in between is not a wire; it is a system of its own with its own queues, congestion, partitions, and failure modes. Every concept in this foundation layer is a consequence of taking that gap seriously.

The first invariant is that distributed components communicate through contracts, not through code. An API is a promise about what messages a service will accept, what messages it will return, and what those messages mean — and the only thing holding two services together is the durability of that promise. RPCs make this contract feel like a local function call, which is both their virtue and their hazard. The virtue is that you can compose distributed systems with familiar syntax. The hazard is that the syntax hides the things that make a remote call fundamentally different from a local one: latency, partial failure, and versioning. A local function either runs or it doesn't. A remote call has a third state — unknown — and the entire structure of reliability semantics is built on top of that third state.

Reliability semantics formalise what you can promise about messages crossing a network. There are exactly three options, and they are not interchangeable. At-most-once means a message will be delivered zero or one times — you might lose it, but you will never see it twice. At-least-once means a message will be delivered one or more times — you will not lose it, but you might see duplicates. Exactly-once means a message will be delivered exactly once, which is what everyone wants and what no system can fully provide for free; achieving it always requires some combination of deduplication, idempotency, or coordination, and the cost of that machinery is one of the most consequential design decisions you make. Most production systems pick at-least-once and pay for exactly-once semantics through application-level idempotency.

Idempotency is the property that makes at-least-once delivery survivable. An operation is idempotent if applying it more than once produces the same result as applying it once — but this is not a property of the operation in isolation. It is a property of the operation combined with the state it acts on. A "set the balance to 100" call is idempotent. A "deduct 10 from the balance" call is not, unless you give it an identifier and track which deductions have already been applied. This distinction matters because almost every retry-safe design depends on getting it right, and the bug pattern of "we retried a non-idempotent operation and double-charged the customer" is one of the most common production incidents in distributed systems.

Latency is the constraint that ties all of this together, and it deserves to be treated as a design constraint rather than a performance metric. Latency in a single process is measured in nanoseconds. Latency across a datacenter network is measured in tens of microseconds to single-digit milliseconds. Latency across the public internet is measured in tens to hundreds of milliseconds and is unpredictable. When you decompose a system into services, every boundary you draw is a place where requests cross a network, and the cumulative latency of those crossings shapes every architectural choice that follows: how chatty your services can be, where you must cache, where you must batch, where you must go asynchronous, and where you cannot decompose at all. A microservice architecture that ignores latency becomes a distributed monolith that is slower than the monolith it replaced.

The skill this topic builds is the ability to read any distributed system — yours or someone else's — and identify which of these invariants it is leaning on, which it is ignoring, and where the production surprises will come from. When a colleague proposes a new service boundary, you will hear the latency cost. When someone says "we'll just retry on failure," you will ask what makes the operation idempotent. When a vendor claims exactly-once delivery, you will know what they are quietly assuming about your application. The fallacies of distributed computing are not a list of mistakes to memorise; they are a list of invariants you have learned to never assume away.

## Level 2 candidates

**The fallacies of distributed computing** — The eight assumptions engineers routinely make about networks that are false, walked through one by one with the production failure mode each one produces. Worth deeper treatment because each fallacy is a self-contained reasoning trap that recurs in different disguises across architectural styles.

**APIs and RPCs** — The contract that distributed components communicate through, including RPC semantics, failure modes, and versioning practice. Worth deeper treatment because reasoning about service boundaries depends on understanding what a remote call actually costs and how the contract evolves over time without breaking the systems on either side of it.

**Reliability and delivery semantics** — At-most-once, at-least-once, exactly-once: the three guarantees, what each one actually costs to implement, and how exactly-once is constructed from at-least-once plus idempotency. Worth deeper treatment because the choice between them is a recurring architectural decision that surfaces in queues, message brokers, RPC frameworks, and stream processors.

**Idempotency in distributed systems** — The property that makes retry-safe design possible, with attention to the fact that idempotency is a property of the operation-plus-state combination rather than the operation alone. Worth deeper treatment because the practical patterns for making operations idempotent (idempotency keys, conditional writes, dedup tables) each have failure modes that are not obvious until you have seen them break.

**Latency as a first-class constraint** — Why latency in distributed systems is a design constraint that shapes service decomposition, communication patterns, and where you can and cannot draw service boundaries. Worth deeper treatment because the difference between thinking of latency as a metric to optimise and thinking of it as a constraint to design around changes how you read every architectural decision.

---


<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) A remote call has an extra outcome: **unknown**

```python
# Local call: usually "returned" or "raised".
def local_divide(a, b):
    return a / b

# Remote call: "returned", "failed", or "unknown".
def charge_customer():
    send_request("POST /charge", {"amount": 100})

    if timeout_waiting_for_response():
        raise Exception("UNKNOWN: server may have charged, reply may be lost")
    return "charged"
```

```python
# Why retrying is dangerous:
try:
    charge_customer()
except Exception as e:
    if "UNKNOWN" in str(e):
        charge_customer()   # maybe first one already succeeded -> double charge
```

A network call is not just a slower function call. The caller can lose the response after the server already did the work.

---

### 2) Distributed components depend on **contracts**, not shared code

```python
# Client assumes this contract:
# request:  {"user_id": 7}
# response: {"name": "Ana"}

# Server v1
def get_user_v1(request):
    return {"name": "Ana"}

# Server v2 - breaking change
def get_user_v2(request):
    return {"full_name": "Ana"}   # renamed field
```

```python
# Client code
user = rpc_call("get_user", {"user_id": 7})
print(user["name"])   # works with v1, breaks with v2
```

The client and server are coupled by message shape and meaning. They do not share memory or execution; they survive only if the contract stays compatible.

---

### 3) Delivery semantics are a **tradeoff table**, not interchangeable features

| Semantics      | What you get        | What you pay |
|----------------|---------------------|--------------|
| At-most-once   | 0 or 1 deliveries   | messages can be lost |
| At-least-once  | 1 or more deliveries| duplicates happen |
| Exactly-once   | "once" effect       | needs dedup/idempotency/coordination |

```text
send(message):
  if no retry:
    at-most-once
  if retry until ack:
    at-least-once
  if retry + dedup/applied-once tracking:
    "exactly-once effect"
```

"Exactly once" is not a free transport property. It is built with extra state and coordination somewhere.

---

### 4) Idempotency is about **operation + state**

```python
balance = 100

def deduct_10():
    global balance
    balance -= 10

deduct_10()
deduct_10()
print(balance)   # 80  -> duplicate changed result
```

```python
balance = 100
seen = set()

def deduct_10_once(request_id):
    global balance
    if request_id in seen:
        return
    balance -= 10
    seen.add(request_id)

deduct_10_once("req-123")
deduct_10_once("req-123")
print(balance)   # 90 -> duplicate suppressed
```

`deduct_10` is not idempotent. `deduct_10_once(request_id)` becomes idempotent because the system remembers whether that logical action already happened.

---

### 5) Retries are safe only when paired with idempotency

```python
def send_with_retry(op):
    for _ in range(3):
        try:
            return op()
        except TimeoutError:
            pass
    raise Exception("gave up")
```

```python
# Unsafe: duplicate side effects possible
send_with_retry(lambda: rpc_call("deduct_balance", {"amount": 10}))

# Safer: caller supplies an idempotency key
send_with_retry(lambda: rpc_call(
    "deduct_balance",
    {"amount": 10, "request_id": "req-123"}
))
```

```python
# Server-side pseudocode
if request_id already processed:
    return previous_result
apply deduction
store request_id as processed
return success
```

Retries solve temporary failure, but they turn one uncertain action into possibly many deliveries. Idempotency is what makes that survivable.

---

### 6) Latency changes architecture, not just speed

```python
# Chatty design: 5 network round trips
user    = rpc("user-service")
orders  = rpc("order-service")
cart    = rpc("cart-service")
prefs   = rpc("prefs-service")
offers  = rpc("offer-service")
page = render(user, orders, cart, prefs, offers)
```

```python
# If each call takes ~50ms:
# total network wait ~= 250ms before rendering
```

```python
# Less chatty: one aggregated call
page_data = rpc("profile-page-service")
page = render(page_data)
```

Or:

```python
# Parallel helps, but does not make latency zero
user, orders, cart, prefs, offers = parallel_rpc([...])
# total wait is now roughly the slowest call, plus coordination cost
```

Every service boundary adds network latency. Too many fine-grained calls can turn a clean design into a slow distributed monolith.

---

## Key Ideas

Distributed systems become easier to reason about once you stop pretending remote calls are local calls with worse performance. The sketches show the core shift: network communication adds an **unknown** outcome, services depend on **message contracts** rather than shared code, delivery guarantees are explicit **tradeoffs**, retries require **idempotent effects** to avoid duplicate work, and latency constrains how finely you can split a system. Most real systems survive by accepting at-least-once delivery and then designing operations so duplicates are harmless.

</details>