## Metadata
- **Date:** 23-05-2026
- **Source:** 12_replication.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-12 · Replication

Replication looks like an operational concern until the day it becomes a correctness concern, and by then it is usually too late. Most engineers first meet replication as a checkbox — "we have a read replica" — and treat it as a performance feature: a way to spread read load, a way to survive a node failure. That framing is not wrong, but it hides the part that actually matters. Replication is the mechanism by which your single logical database becomes, physically, several databases that disagree with each other for windows of time you cannot fully control. Every guarantee your application thought it had about reading what it just wrote, about seeing events in order, about two users seeing the same state — all of those guarantees now depend on choices made at the replication layer.

The reason replication exists at all is that you want two things that pull in opposite directions: fault tolerance and read scalability. Fault tolerance demands that if one machine dies, another machine has the data and can take over. Read scalability demands that read traffic can be served from any of several machines rather than piling onto one. Both goals are satisfied by the same primitive — keep copies of the data on multiple machines — and both run into the same fundamental problem, which is that copies have to be kept in sync across an unreliable network with non-zero latency. Everything interesting about replication is a consequence of that fact.

There are essentially three architectural answers to "how do writes propagate to copies," and the choice between them shapes everything downstream. Single-leader replication designates one node as authoritative for writes; the leader accepts every write, then ships the changes to followers, who apply them in the same order. This is the model most relational databases default to, and it is the simplest to reason about because there is exactly one place where write ordering is decided. Multi-leader replication relaxes that constraint: writes can be accepted at multiple nodes, which then exchange their changes with each other. This is what you reach for when you have multiple datacenters or offline clients, and it pays for that flexibility with the problem of write conflicts — two leaders accepting incompatible writes to the same record at the same time. Leaderless replication, the Dynamo-style model behind Cassandra and Riak, drops the notion of a leader entirely; clients write to several nodes at once and read from several nodes at once, and consistency emerges from quorum arithmetic rather than from a coordinating authority.

The single most important concept to internalise across all three models is replication lag. When a write hits the leader and a follower is, say, two hundred milliseconds behind, your system is in a state where two clients reading from two different replicas will see two different versions of the world. Most of the time this is invisible. Some of the time it produces bugs that are nearly impossible to reproduce in development, because in development your replica is never two hundred milliseconds behind. Kleppmann's framing here is the one to carry with you: replication lag is not a performance metric. It is a window during which your system can violate guarantees that your application code is implicitly relying on, and the longer the window, the more user-visible the violations become.

Those violations have specific names because they recur in specific shapes. Reading your own writes is the anomaly where a user submits a change, the request returns success, the user refreshes — and the refresh hits a follower that has not yet received the write, so the user sees the old state and reasonably concludes the system is broken. Monotonic reads is the anomaly where a user reads a value, then reads it again, and the second read returns an older value than the first, because the second read landed on a more-lagged replica. Consistent prefix reads is the anomaly where a user observes events in an order that violates causality — they see an answer before they see the question — because different shards replicated at different speeds. Each of these has a fix, but the fix is at the application or routing layer, not at the database layer, and you can only apply the fix if you know to look for the anomaly.

Multi-leader and leaderless replication add their own characteristic problem on top: write conflicts. When two leaders accept conflicting writes, or when a quorum write race produces two divergent versions, the system has to decide what "the real value" is. The strategies range from the seductively simple but lossy (last-write-wins, which silently discards data on the basis of clock readings that may not be trustworthy) through merge functions (which require the data type to be amenable to merging) to application-level conflict resolution (which is correct but pushes complexity into your code). Choosing among these is not a database configuration decision. It is an application-level statement about what consistency means for your domain — whether two simultaneous edits to the same shopping cart should win-loss, merge, or surface to the user as a conflict to resolve.

The skill this topic builds, in the end, is the ability to look at any distributed data system and ask the right diagnostic questions before you trust it. Where is the leader, if there is one? What happens to writes during a leader failover, and how is the new leader elected? How far behind are the followers, in the worst case rather than the average case? What anomalies can application code observe as a result of that lag, and is the application defending against them or assuming they cannot happen? When two clients write to the same record at the same time, what are the rules for which write survives? These are not exotic questions. They are the questions that determine whether your system is correct in production, and the difference between engineers who configure replication and engineers who reason about it is whether they know to ask them at all.

## Level 2 candidates

**Single-leader replication** — Covers the mechanics of leader-based replication, including synchronous versus asynchronous follower configurations, leader failover protocols, and the specific ways writes can be lost during a handoff. Worth deeper treatment because "simplest" does not mean "safest" — the failover edge cases are where most production single-leader incidents actually originate.

**Replication lag and its consequences** — Covers the specific application-level anomalies that lag produces (reading your own writes, monotonic reads, consistent prefix reads) and the techniques for defending against each. Worth deeper treatment because this is where replication stops being a database concern and becomes an application architecture concern, and the techniques are not obvious until you have been bitten.

**Multi-leader replication** — Covers the topologies (circular, star, all-to-all), the use cases that justify the complexity (multi-datacenter, offline clients, collaborative editing), and the conflict-detection mechanisms that make it tractable. Worth deeper treatment because the conflict problem is the entire reason multi-leader is hard, and understanding it concretely is the prerequisite for choosing it deliberately rather than ending up in it accidentally.

**Leaderless replication** — Covers Dynamo-style replication, quorum reads and writes, the role of read repair and anti-entropy in convergence, and the specific consistency guarantees the quorum arithmetic actually delivers. Worth deeper treatment because the mental model is genuinely different from leader-based systems, and the marketing claims around "tunable consistency" hide subtleties that bite in production.

**Conflict resolution strategies** — Covers last-write-wins and its hidden costs, CRDTs and merge-based approaches, version vectors for detecting concurrent writes, and application-level resolution patterns. Worth deeper treatment because conflict resolution is where the database hands the consistency problem back to your application, and the choice of strategy is effectively a product decision dressed as a configuration option.

**Replication and consensus** — Covers the relationship between replication protocols and consensus algorithms (Raft, Paxos), and why strong replication guarantees ultimately reduce to a consensus problem. Worth deeper treatment because it is the bridge from this topic to L1-14, and the connection is what makes the CAP-theorem tradeoffs feel inevitable rather than arbitrary.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Single-leader replication: one place decides write order

```text
# Client wants to update account balance.

Client -> Leader:  UPDATE accounts SET balance = 80 WHERE id = 1;
Leader:            apply locally
Leader -> Follower: "UPDATE accounts SET balance = 80 WHERE id = 1;"
Follower:          apply later

# Important property:
# all writes are ordered at the leader

Write order at leader:
1. balance = 100 -> 80
2. balance = 80  -> 60

Followers replay in that same order.
```

The simplification is the benefit: there is exactly one node that decides write order.  
The cost is also visible: followers are always catching up to a past decision.

---

### 2) Replication lag: a successful write does not mean every replica agrees yet

```python
leader = {"title": "old"}
follower = {"title": "old"}

def write_to_leader(new_title):
    leader["title"] = new_title
    return "200 OK"

def replicate_later():
    follower["title"] = leader["title"]

print(write_to_leader("new"))     # user sees success
print(follower["title"])          # old  <- stale read from replica
replicate_later()
print(follower["title"])          # new
```

This is the core replication fact: after a write succeeds, replicas may still disagree for some window of time.  
That window is replication lag, and it creates correctness problems, not just slower dashboards.

---

### 3) Read-your-own-writes: route some reads to the leader

```python
# bad: write to leader, then read from any replica

write_to_leader("new profile name")
read_from = follower
print(read_from["title"])   # maybe stale

# better: after a user writes, pin that user's reads to leader for a while

recently_wrote = True

def read_profile():
    if recently_wrote:
        return leader["title"]    # read your own write
    return follower["title"]
```

This fixes one specific anomaly: a user should not save and then immediately see old data.  
The cost is reduced read scaling for those sessions, because some reads must go back to the leader.

---

### 4) Monotonic reads: always using “any replica” can move time backwards

```python
replica_a = {"msg_count": 5}  # less lagged
replica_b = {"msg_count": 3}  # more lagged

def random_replica():
    # imagine a load balancer
    return replica_a, replica_b

# first request
seen1 = replica_a["msg_count"]   # 5

# second request, same user, different replica
seen2 = replica_b["msg_count"]   # 3  <- older than before
```

A user has now observed time going backwards.  
Typical fix: keep one user tied to one replica, or track a minimum version and reject older reads.

---

### 5) Multi-leader replication: availability goes up, conflicts appear

```python
# Two datacenters, both accept writes.

leader_us = {"email": "a@example.com"}
leader_eu = {"email": "a@example.com"}

# same user edited in two places before replication finished
leader_us["email"] = "alice@us.example"
leader_eu["email"] = "alice@eu.example"

# later, replication exchanges updates
incoming_from_us = leader_us["email"]
incoming_from_eu = leader_eu["email"]

# conflict: which value is correct?
```

Single-leader avoids this by choosing one writer.  
Multi-leader gains flexibility for multi-region/offline use, but now “what is the truth?” becomes an application decision.

---

### 6) Conflict resolution: last-write-wins is simple and lossy

```python
# two conflicting writes with timestamps from different machines
write1 = {"value": "alice@us.example", "ts": 105}
write2 = {"value": "alice@eu.example", "ts": 110}

def last_write_wins(a, b):
    return a if a["ts"] > b["ts"] else b

winner = last_write_wins(write1, write2)
print(winner["value"])   # alice@eu.example

# simple, but one write disappears
```

If clocks are wrong, the “winner” may not even be the truly later write.  
The code is small because the policy is crude: it resolves conflicts by discarding one side.

---

### 7) Leaderless replication: consistency comes from quorum arithmetic, not a leader

```text
# 3 replicas: R1, R2, R3
# write quorum W=2, read quorum R=2

Client write x=7:
  send to R1, R2, R3
  success after any 2 acknowledge

Example:
  R1 = 7
  R2 = 7
  R3 = old value   # missed the write

Client read x:
  read from any 2 replicas
  values returned: [7, old]

Client picks newest version -> 7
```

The attraction is no single leader bottleneck.  
The cost is that reads and writes are now more complicated: clients or coordinators must compare versions, repair stale replicas, and reason about partial success.

---

## Key Ideas

Replication means one logical database becomes several physical copies that can temporarily disagree. Single-leader replication is easiest to reason about because one node defines write order, but lag makes follower reads stale. That lag creates concrete anomalies such as not reading your own writes and seeing older data on a later read, which applications must defend against through routing or session policies. If you allow writes in multiple places, conflicts become unavoidable, and “resolution” is really a business rule about which data may be lost or merged. Leaderless systems remove the leader but replace it with quorum math and version reconciliation, so the central question never goes away: when replicas disagree, what does your application consider correct?

</details>