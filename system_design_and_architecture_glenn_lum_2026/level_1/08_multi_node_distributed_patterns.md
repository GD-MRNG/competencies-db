## Metadata
- **Date:** 23-05-2026
- **Source:** 08_multi_node_distributed_patterns.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-08 · Multi-Node Distributed Patterns

The moment your system stops fitting on one machine, a new category of problem appears — and the temptation is to treat each problem as novel, inventing bespoke solutions to scale, coordinate, and route requests across nodes. Almost none of these problems are novel. They have been encountered, named, and solved enough times that a small library of patterns covers most of what you will ever need to build. The work of multi-node design is not invention; it is recognition. Knowing the pattern library is what turns "we need to scale this" from an open-ended engineering problem into a specific decision with known costs.

The patterns in this library are not implementation details. They are structural choices about how work and state are distributed across machines, and each one corresponds to a distinct class of problem. Replicated services solve the problem of horizontal scalability for stateless work. Sharded services solve the problem of scaling state itself across machines. Scatter/gather solves the problem of computing answers that require many machines to participate in a single request. Leader election solves the problem of coordinating decisions when one node must speak for many. Each pattern is a solution to a specific problem, and each one introduces costs that the alternative patterns do not.

Replicated load-balanced services are the foundational pattern, and they are deceptively simple: run multiple identical instances of a service behind a load balancer and route requests across them. The pattern works because the service is stateless — any instance can serve any request. That word "stateless" is doing enormous work. The moment a service holds session data, in-memory caches that diverge between instances, or any per-request continuity that lives on the node, replication stops being free. You either push the state somewhere shared (which becomes its own bottleneck) or you accept session stickiness (which reintroduces the coupling that replication was supposed to eliminate). The pattern is straightforward; the prerequisite is not.

Sharded services solve a different problem: what happens when the data itself does not fit on one machine, or when a single instance cannot serve the read or write volume against it. Sharding partitions the data across instances so each one owns a subset, with a routing layer in front that knows which shard holds what. This lets you scale beyond what replication alone can achieve — replication multiplies your read capacity but every replica still holds the full dataset. Sharding multiplies your storage and write capacity by splitting the dataset itself. The cost is routing complexity and a new failure mode: the hot shard. If your partitioning scheme produces uneven load — one customer with ten times the traffic, one key range with all the activity — then one shard saturates while the others sit idle, and the system fails in a way that adding more shards does not fix.

Scatter/gather is the pattern for requests that cannot be answered by any single node. A search query that needs to consult every shard of an index, a parallel computation that needs partial results from many workers, a fan-out query that aggregates across services — all of these dispatch a request to many nodes simultaneously and combine the responses into a single answer. The pattern's power is parallelism: you turn a request that would take N units of work serially into one that takes roughly one unit of work in wall-clock time. The pattern's failure mode is the tail. Your response time is governed by the slowest responder, not the average — and at scale, something is always slow. Scatter/gather makes you intimately familiar with p99 latency, because the p99 of any individual node becomes the p50 of the aggregate.

Leader election is the pattern that emerges when a distributed system needs a single authoritative decision-maker — a node that schedules work, owns a resource, or breaks ties when others disagree. Several nodes are candidates; one of them wins; the others stand by. The interesting part is not the election. It is the failure detection. Electing a leader is mechanically straightforward when everyone is alive and reachable. The hard problem is deciding when the current leader has actually failed versus when it is merely slow or partitioned away — and getting this wrong produces either dual leadership (two nodes both believing they are in charge, both making authoritative decisions) or false failover (cycling leaders on transient blips, never making forward progress). Every leader election system you encounter is at heart a failure detector with an election protocol bolted on, and the failure detector is where the difficulty lives.

These four patterns do not exhaust the library. Functions-as-a-service is a variant on the replicated pattern that takes statelessness to its logical conclusion: no long-running instance at all, just code that materialises in response to events and disappears when done. The tradeoffs (cold start latency, vendor coupling, observability gaps) are different in kind, not degree, from the tradeoffs of long-running replicated services. And the patterns compose: a real production system is usually replicated services in front of sharded data with scatter/gather for cross-shard queries and leader election for coordination tasks, all running together. Recognising which pattern is doing which work is the first step in reading a distributed system.

The skill this topic builds is pattern recognition under pressure — the ability to look at a scaling problem and immediately see which pattern fits, what its known costs are, and what its known failure modes will be. Without this vocabulary, every distributed system is a snowflake and every problem is novel. With it, most problems are instances of a class, and the class tells you what the solution will cost before you commit to it. That is the difference between choosing an architecture and inheriting one.

## Level 2 candidates

**Replicated load-balanced services** — Covers the mechanics of horizontal scaling through stateless replication behind a load balancer, and what statelessness actually requires of a service. Worth deeper treatment because the prerequisite (genuine statelessness) is harder than it looks and most replication failures trace back to subtle state leaks.

**Session stickiness and its costs** — Covers the pattern for handling stateful sessions in a replicated environment by routing successive requests from the same client to the same instance. Worth depth because stickiness is the most common compromise made under deadline pressure and it reintroduces exactly the coupling that replication was meant to eliminate, in ways that are not visible until a node fails.

**Sharded services** — Covers partitioning data or load across instances, the routing layer that fronts the shards, and the failure modes (hot shards, rebalancing) that emerge. Worth depth because sharding decisions are difficult to reverse and the choice of partitioning key shapes every operational property of the resulting system.

**Scatter/gather** — Covers the pattern of fanning a request out to many nodes and aggregating the responses, with attention to the tail-latency problem that defines its real-world behaviour. Worth depth because the naive analysis (parallelism is fast) misses the actual failure mode (slowest node dominates), and reasoning about p99 amplification is its own discipline.

**Leader election and ownership** — Covers the protocols for selecting a single authoritative node and, more importantly, the failure detection that determines when a new election is needed. Worth depth because the election itself is the easy part and most production incidents around leader election are failure-detection problems wearing election-protocol clothing.

**Functions and event-driven processing (FaaS)** — Covers the pattern of replacing long-running services with stateless functions triggered by events, and the operational characteristics (cold starts, vendor lock-in, observability) it produces. Worth depth because FaaS is often adopted for reasons that do not match its actual tradeoff profile, and recognising when those tradeoffs are and are not justified is a distinct skill.

---


<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Replication works only when any node can handle any request

```python
# Two identical service instances behind a load balancer.
instances = ["app-1", "app-2"]

def load_balancer(request_id):
    return instances[request_id % 2]   # pretend round-robin

def handle_request(instance, request):
    # OK: everything needed is in the request or shared DB
    return f"{instance} served user={request['user_id']}"

for req_id, req in enumerate([{"user_id": 10}, {"user_id": 11}, {"user_id": 12}]):
    node = load_balancer(req_id)
    print(handle_request(node, req))
```

If requests are truly self-contained, replication is easy: add more identical nodes and spread traffic across them.

---

### 2) A tiny bit of hidden state breaks “any node can serve any request”

```python
# Bad: session state stored in process memory.
sessions = {
    "app-1": {},
    "app-2": {},
}

def login(instance, user_id):
    sessions[instance]["current_user"] = user_id

def get_profile(instance):
    return sessions[instance].get("current_user", "NOT LOGGED IN")

login("app-1", 42)

print(get_profile("app-1"))  # 42
print(get_profile("app-2"))  # NOT LOGGED IN
```

Same service code, but now requests are not interchangeable across nodes. Replication stops being “free” the moment important state lives inside one process.

---

### 3) Session stickiness is a workaround, not a cure

```python
# Route a given client to the same node every time.
sticky_table = {"client-A": "app-1"}

def route(client_id):
    return sticky_table[client_id]

# Works while app-1 is healthy.
print(route("client-A"))  # app-1

# But if app-1 dies, the "session" dies with it.
alive = {"app-1": False, "app-2": True}

node = route("client-A")
if not alive[node]:
    print("client-A lost session; must log in again")
```

Stickiness preserves stateful behavior by reintroducing coupling to one machine. You get fewer immediate code changes, but weaker failover and uneven load.

---

### 4) Sharding scales state by splitting ownership

```python
# Each shard owns part of the dataset.
shards = {
    0: {},
    1: {},
}

def shard_for(user_id):
    return user_id % 2

def put_user(user_id, name):
    shards[shard_for(user_id)][user_id] = name

def get_user(user_id):
    return shards[shard_for(user_id)][user_id]

put_user(10, "Ana")   # shard 0
put_user(11, "Ben")   # shard 1

print(shards)         # data is split, not copied
print(get_user(10))   # routed to the right shard
```

Replication gives many copies of the same data. Sharding gives different nodes different pieces of the data, which increases storage and write capacity.

---

### 5) Sharding introduces the hot-shard problem

```python
# Bad shard key: all traffic for one "big customer" lands on one shard.
def shard_for(customer_id):
    return customer_id % 2

traffic = [1000, 2, 3, 4]   # customer 0 is huge
load = {0: 0, 1: 0}

for customer_id, requests in enumerate(traffic):
    load[shard_for(customer_id)] += requests

print(load)   # {0: 1003, 1: 6}
```

Adding shards does not help if the partitioning rule concentrates most activity on one shard. The problem is not shard count; it is shard-key choice.

---

### 6) Scatter/gather is fast on average, but limited by the slowest responder

```python
# Query all shards, then combine partial answers.
shard_times_ms = [8, 9, 120]   # one slow shard

def scatter_gather(times):
    parallel_wall_clock = max(times)   # must wait for all
    return parallel_wall_clock

print(scatter_gather(shard_times_ms))  # 120 ms
```

The work happened in parallel, but the user still waits for the slowest shard. In scatter/gather systems, tail latency dominates.

---

### 7) Leader election is easy when failure is obvious; hard when it is ambiguous

```text
Nodes: A, B, C
Current leader: A

Every 1s:
  followers expect heartbeat from leader

Rule:
  if no heartbeat for 3s:
      start election
      highest node id wins

Case 1: A crashed
  B and C stop hearing heartbeats
  election happens
  C becomes leader
  -> fine

Case 2: A is slow or partitioned
  B and C do not hear A
  A still thinks "I am leader"
  B/C elect C
  -> now A and C may both act as leader
```

The hard part is not choosing a winner. The hard part is deciding whether the old leader is truly dead or merely unreachable.

---

### 8) These patterns usually compose, not compete

```text
Client
  -> load balancer
      -> replicated API nodes           # stateless request handling
          -> router
              -> sharded database       # split state across machines

Search request:
  API node
    -> scatter to all shards
    -> gather partial results

Background scheduler:
  many candidates
    -> one elected leader runs the job
```

Real systems rarely use just one pattern. The useful skill is recognizing which part of the system is using which pattern, and why.

## Key Ideas

Multi-node design gets simpler when you stop treating every scaling problem as unique and instead recognize the small set of patterns involved. Replication handles stateless work, but hidden per-node state breaks its promise; stickiness patches that breakage by tying users back to individual machines. Sharding scales the data itself, but makes routing and load distribution critical, because a bad shard key creates hot spots. Scatter/gather gives parallelism, but latency is set by the slowest participant. Leader election provides single-node authority, but its real difficulty is failure detection under ambiguity. In practice, production systems combine these patterns, so the main skill is identifying which pattern fits each problem and what cost comes with it.

</details>