## Metadata
- **Date:** 23-05-2026
- **Source:** 14_consistency_and_consensus.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-14 · Consistency and Consensus

Most engineers carry a binary intuition about consistency: either the database is consistent or it isn't, either you read the latest value or you read something stale. This intuition survives until the first time a production incident reveals that "consistent" was a word covering at least six different guarantees, and the one your system actually provided was not the one your application assumed. The practical work of reasoning about distributed data systems begins when you stop thinking of consistency as a property and start thinking of it as a spectrum of guarantees, each with a different price.

The price is paid in two currencies: latency and availability. Every consistency guarantee stronger than "eventually the writes will show up somewhere" requires coordination between nodes, and coordination requires network round-trips, and network round-trips fail or stall in the presence of partitions. This is not an implementation detail of any particular database — it is a structural property of distributed systems. The stronger the guarantee, the more the system must wait, refuse, or block when the network misbehaves. Engineers who understand this stop being surprised by latency spikes during failovers and start designing systems where the guarantee matches what the application actually needs.

At the top of the spectrum sits linearizability. The mental model is simple: the system behaves as if there were a single copy of the data, and operations appear to take effect atomically at some point between when they were issued and when they returned. If a write completes and then a read begins, the read sees the write — no matter which replica it hit. This is the guarantee most engineers unconsciously assume their database provides, and it is the guarantee most distributed databases do not provide by default. Linearizability is what makes leader election, uniqueness constraints, and distributed locks correct; it is also what makes them slow.

The CAP theorem is the precise statement of why you cannot have linearizability for free. Stated carelessly — "pick two of consistency, availability, partition tolerance" — it sounds like a menu. Stated precisely, it is narrower and sharper: when a network partition occurs, a system that provides linearizability must refuse to serve some requests, and a system that remains available to all requests cannot provide linearizability. Partition tolerance is not optional; partitions happen whether you tolerate them or not. The real choice is what the system does when one occurs. Most CAP debates are unproductive because the participants are arguing about the menu version. The precise version is a tool for designing how your system behaves during the failure modes it will actually encounter.

Below linearizability sits a layered hierarchy of weaker guarantees, and the names matter because each one corresponds to a specific class of anomaly that applications either tolerate or break on. Causal consistency preserves the order of operations that have a cause-and-effect relationship — your reply appears after the message it replies to — but allows concurrent operations to be observed in different orders on different replicas. Read-your-writes ensures a user sees their own updates even if other users do not yet. Monotonic reads ensures you do not see time go backwards. Each of these is weaker than linearizability, cheaper to provide, and sufficient for many applications — provided you have actually decided that they are sufficient rather than discovered after launch that they are not.

Establishing any ordering at all in a distributed system, even a weak one, is a non-trivial problem because there is no global clock. Wall-clock timestamps drift, leap, and disagree across machines by enough to invert the order of events that happened seconds apart. The mechanisms that distributed systems use to construct ordering — sequence numbers, Lamport clocks, vector clocks — are not optimisations; they are the substrate on which any consistency guarantee is built. When you read about a system providing causal consistency, somewhere underneath there is a logical clock doing the work that physical time cannot.

Consensus is the mechanism that makes the strongest guarantees achievable in practice. The consensus problem is deceptively simple to state — get a group of nodes to agree on a single value, even when some of them fail or messages are lost — and famously difficult to solve correctly. Paxos was the first algorithm to solve it; Raft was designed two decades later specifically because Paxos was so hard to understand that production implementations regularly got it wrong. Both algorithms work by electing a leader, having the leader propose values, and requiring a majority of nodes to acknowledge each proposal before it is considered committed. The majority requirement is what makes consensus work: any two majorities must overlap in at least one node, which prevents two leaders from both believing they have committed conflicting values. This is the engine inside etcd, ZooKeeper, and the coordination layer of nearly every modern distributed database.

The skill this topic builds is not memorising the hierarchy of consistency models or the mechanics of Raft. It is the ability to look at an application requirement — "users must see their own profile updates immediately" or "we cannot allow two clients to claim the same username" — and translate it into the specific consistency guarantee required, then ask whether the system you are using actually provides that guarantee, and at what cost. Most production surprises in distributed data systems come from the gap between the guarantee assumed and the guarantee provided. Closing that gap, deliberately and explicitly, is what consistency reasoning is for.

## Level 2 candidates

**Linearizability** — The strongest single-object consistency guarantee, what it actually means operationally, and the specific operations (locks, leader election, uniqueness constraints) that genuinely require it. Worth deeper treatment because most engineers conflate linearizability with serializability and with "strong consistency" generally, and untangling the three is what makes the rest of the spectrum legible.

**The CAP theorem precisely stated** — The formal statement of what is impossible under network partition, what the theorem does and does not say, and the more useful PACELC extension that accounts for latency in the non-partitioned case. Worth deeper treatment because the casual version of CAP has done more to confuse architectural conversations than to clarify them.

**Ordering guarantees** — Causality, sequence numbers, Lamport clocks, and vector clocks as the mechanisms for establishing "happened-before" without a global clock. Worth deeper treatment because these are the substrate that every consistency model above eventual is built on, and understanding them changes how you read any system that claims an ordering property.

**Consensus algorithms: Paxos and Raft** — The mechanics of how a group of nodes reaches agreement despite failures, the role of leader election and the majority quorum, and why Raft's design choices made it the dominant practical implementation. Worth deeper treatment because consensus shows up inside almost every distributed system you operate, and knowing what it costs explains a lot of operational behaviour.

**Distributed transactions and two-phase commit** — The protocol for atomicity across multiple nodes, its specific failure modes (coordinator crash, indefinite blocking), and why most modern distributed systems route around it rather than rely on it. Worth deeper treatment because the gap between "we need a distributed transaction" and "we should actually use one" is where many architectural mistakes live.

**Weaker consistency models in practice** — Causal consistency, read-your-writes, monotonic reads, and consistent prefix reads as the practical guarantees that real applications usually need. Worth deeper treatment because these are the models most production systems actually provide, and matching them to application requirements is where consistency reasoning earns its keep.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) “Consistent” is not one thing

```python
# One write, then one read. What can the app safely assume?

write(user="u1", field="name", value="Ada")   # returns OK

# Different guarantees imply different promises:

read("u1.name")

# Linearizable:
#   must return "Ada"

# Read-your-writes:
#   if the SAME user/session reads, must return "Ada"
#   another client may still see old value

# Eventual consistency:
#   may return old value now, but should converge to "Ada" later
```

Same API, different guarantees. Most bugs happen when the app assumes the first and the database only provides the third.

---

### 2) Linearizability: “as if there were one copy”

```python
# Two replicas, but clients want single-copy behavior.

# Time -->
# client A                    replica 1 / replica 2                 client B
#
# write(x=1) -----------------------------------------------------> returns OK
#                                                         read(x) ---------> ?

# Linearizable system:
#   if read starts AFTER write completed, read must see x=1

# Non-linearizable but replicated:
#   write reaches replica 1, not replica 2 yet
#   client B reads replica 2 and sees old x=0
```

Why this matters:

```python
# uniqueness check needs linearizability

if not username_exists("ada"):
    create_username("ada")

# If two replicas answer "doesn't exist" at the same time,
# two clients can both create "ada".
```

Linearizability prevents that class of race, but it needs coordination, which adds latency and can block during failures.

---

### 3) CAP, precisely: partition forces a choice

```python
# Node A and Node B are replicas.
# A network partition disconnects them.

# Client 1 can reach only A
# Client 2 can reach only B

# Client 1:
write(balance=100)  # at A

# Client 2:
read(balance)       # at B
```

Two possible behaviors:

```text
Option 1: Stay available
- A accepts write
- B answers read
- B may return stale data
=> available, but not linearizable

Option 2: Preserve linearizability
- A or B refuse/block some requests until coordination is possible
=> linearizable, but not fully available during partition
```

Partition tolerance is not optional; the network already broke. The real choice is what your system does next.

---

### 4) Weaker guarantees are often enough

```python
# Read-your-writes

session = connect()

session.write("profile.bio", "Hello")
print(session.read("profile.bio"))   # must be "Hello"

other_user = connect()
print(other_user.read("profile.bio"))  # may still be old
```

```python
# Monotonic reads: don't go backwards

# First read from a fresh replica:
v1 = read("post.likes")   # 10

# Later read from a stale replica:
v2 = read("post.likes")   # 8   <-- bad if monotonic reads promised
```

```python
# Causal consistency: reply must not appear before original message

post("msg1", "I got the job")
post("reply-to-msg1", "Congrats!")

# Allowed under causal consistency:
#   everyone may see the two messages later
# Not allowed:
#   seeing "Congrats!" before seeing "I got the job"
```

These are cheaper than linearizability because they preserve less order.

---

### 5) No global clock: ordering needs logical clocks

```python
# Physical clocks can lie about order.

# machine A clock: 12:00:05
# machine B clock: 12:00:03   (skewed backward)

A: send("update")
B: receive("update")

# Wall-clock timestamps might record:
#   receive at 12:00:03
#   send    at 12:00:05
# which falsely suggests receive happened before send
```

Lamport clock sketch:

```python
# each node keeps an integer clock

# on local event: clock += 1
# on send: attach clock
# on receive(msg_clock): clock = max(clock, msg_clock) + 1
```

Example:

```python
A.clock = 0
A.clock += 1              # event: prepare update, A=1
send(msg, ts=A.clock)     # send ts=1

B.clock = 0
recv_ts = 1
B.clock = max(0, 1) + 1   # B=2
# Now B's receive is correctly ordered after A's send
```

Logical clocks do not give real time. They give enough order to talk about causality.

---

### 6) Consensus: majority overlap is the safety trick

```python
# 3-node cluster: N1, N2, N3
# A value is committed only after a majority accepts it.

majority = 2
```

Leader proposes:

```python
proposal = "x=1"

acks = [N1.accept(proposal), N2.accept(proposal), N3.timeout()]
# 2 accepts => committed
```

Why conflicting commits are prevented:

```text
Possible majorities in 3 nodes:
- {N1, N2}
- {N1, N3}
- {N2, N3}

Any two majorities share at least one node.
That shared node cannot honestly accept two different committed values
for the same log position.
```

Cost shown directly in the protocol:

```python
# write latency includes waiting for quorum
propose()
wait_for_majority()   # extra network round-trip(s)
commit()
```

Consensus is what makes leader election, metadata stores, and replicated logs safe — and what makes them slower when the network is unhealthy.

---

## Key Ideas

The useful mental shift is to stop asking “is the system consistent?” and start asking “what exact ordering or visibility guarantee do I need, and what coordination cost does that imply?” Linearizability gives single-copy behavior but must coordinate and may refuse requests during partitions. Weaker guarantees like read-your-writes, monotonic reads, and causal consistency preserve only the order many applications actually need, so they are cheaper. Because distributed systems have no trustworthy global clock, ordering must be constructed with logical mechanisms. And when you need the strongest guarantees across replicas, consensus works by quorum overlap: safety comes from majority agreement, while latency and reduced availability during failures are the price.

</details>