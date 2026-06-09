## Metadata
- **Date:** 23-05-2026
- **Source:** 13_partitioning_transactions.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-13 · Partitioning and Transactions

Partitioning and transactions look like separate topics until you watch a system grow. A database that fits on one machine has neither problem: there is nothing to split, and the machine itself is the boundary inside which atomicity and isolation are cheap. The moment you outgrow that machine — because the data no longer fits, or the write rate no longer fits, or the read rate no longer fits — you reach for partitioning. And the moment you partition, you have created exactly the problem that transactions exist to solve: operations that must succeed or fail together now span machines that fail independently. This is why these two topics belong in the same conversation. Partitioning is what you do to scale. Transactions are what you owe the system afterwards.

Partitioning, in its essential form, is the decision that each piece of data lives on exactly one node (or one small set of nodes, if you also replicate). The work of the system is then to route each request to the node that owns the relevant data. The two dominant strategies — range partitioning and hash partitioning — express a tradeoff that you cannot escape: range partitioning keeps related keys close together, which makes range queries cheap and hot spots easy to create; hash partitioning spreads load evenly, which makes hot spots rare and range queries impossible without scattering across every node. There is no neutral choice here. You are picking which access pattern your system will be good at and which it will be bad at, and the choice cascades through every secondary index, every rebalancing decision, and every query you will ever write against the system.

Secondary indexes are where partitioning stops being elegant. A primary key partitions cleanly because the partition function is the routing function — the system knows which node to ask. A secondary index has no such alignment: the values you want to look up are scattered across whatever partitioning scheme the primary key chose. You get two options, and both are bad. Local indexes (one index per partition) make writes cheap but force every query to fan out to every partition. Global indexes (one index across partitions) make queries cheap but force every write to update an index that lives on a different node — which is itself a distributed transaction, and now you see the problem returning.

Rebalancing is the operational face of partitioning, and it is where naive solutions punish you most visibly. The obvious approach — hash the key modulo N, where N is the number of nodes — works exactly until you add or remove a node, at which point nearly every key changes its partition assignment and the entire dataset moves across the network. Real systems use schemes (consistent hashing, fixed number of partitions, dynamic partitioning) that bound how much data has to move when the cluster changes shape. The lesson is structural: rebalancing strategy is not a deployment detail you defer to the database; it is a property of the partitioning scheme you chose, and you inherited its costs the moment you chose it.

Transactions are what makes a database feel like a place where invariants hold. ACID — atomicity, consistency, isolation, durability — is the standard shorthand, but the shorthand has been so abused as a marketing term that it tells you almost nothing about what guarantees a given system actually offers. Atomicity means a transaction either fully happens or fully doesn't, even under crash. Durability means committed data survives crashes. Consistency, in the ACID sense, is mostly an application-level property the database helps you maintain. Isolation is where the real complexity lives, because it is the property that governs what concurrent transactions can see of each other — and almost every database in production runs at an isolation level weaker than full serializability, whether you noticed or not.

Isolation levels form a spectrum, and each level on that spectrum is defined by which concurrency anomalies it prevents and which it permits. Read committed prevents dirty reads but allows non-repeatable reads. Snapshot isolation (often marketed as "repeatable read") prevents most read anomalies by giving each transaction a consistent point-in-time view, but it permits write skew — two transactions that each read a consistent snapshot, each make a decision based on that snapshot, and together violate an invariant that neither alone would have violated. Serializability is the only level at which concurrent transactions are guaranteed to behave as if they had run one after another. Every weaker level is a performance optimisation that you, the application author, are choosing to pay for in correctness — even if nobody told you that's what you were doing.

Achieving serializability has historically been expensive, which is why most databases default to weaker levels. The three implementation strategies — literal serial execution (one transaction at a time, viable only because main memory got large enough), two-phase locking (the traditional approach, with its associated lock contention and deadlock cost), and serializable snapshot isolation (the modern optimistic approach that detects conflicts at commit time) — each make different tradeoffs between throughput, latency, and tail behaviour under contention. None of them is free, and none of them survives the move from a single node to multiple nodes without becoming dramatically harder.

Which is where partitioning and transactions collide. A transaction that touches data on a single partition is, mechanically, a single-node transaction with whatever guarantees the local engine offers. A transaction that touches data on multiple partitions is a distributed transaction, and distributed transactions are the hardest correctness problem in data systems engineering — coordinator failures, blocking participants, and the impossibility of distinguishing a slow node from a failed one. The skill this topic builds is not memorising isolation levels or partition strategies. It is recognising that every time you decompose data across nodes for scale, you are making a future decision about which invariants you will defend with distributed transactions, which you will defend with application-level reasoning, and which you will quietly let go of. Most production data systems are running on the third option without anyone having decided.

## Level 2 candidates

**Partitioning strategies** — Range partitioning vs. hash partitioning, and the hybrid schemes that try to capture properties of both. Worth deeper treatment because the choice shapes query performance, hot spot behaviour, and rebalancing cost simultaneously, and the interactions are not obvious until you've seen them fail.

**Secondary indexes and partitioning** — The two approaches (local/document-partitioned indexes and global/term-partitioned indexes) and the asymmetric costs each imposes on reads and writes. Worth deeper treatment because secondary index design is where most teams discover their partitioning scheme was wrong, and the failure mode is performance collapse rather than incorrectness.

**Rebalancing partitions** — Why mod-N hashing is catastrophic, and how consistent hashing, fixed-partition schemes, and dynamic partitioning bound the cost of cluster changes. Worth deeper treatment because the differences between schemes only become visible during operational events, and that is the worst time to be learning them.

**ACID properties in depth** — The precise meaning of each letter, and the gap between what ACID guarantees and what databases marketed as "ACID compliant" actually deliver. Worth deeper treatment because the term has been so diluted that engineers routinely assume guarantees their database does not offer.

**Isolation levels** — The full spectrum from read uncommitted to serializable, and the specific anomalies (dirty reads, non-repeatable reads, phantom reads, write skew, lost updates) that each level permits or prevents. Worth deeper treatment because choosing an isolation level is an application correctness decision disguised as a configuration setting, and most engineers have never seen the disguise removed.

**Serializability implementations** — Two-phase locking, serial execution, and serializable snapshot isolation as three architecturally distinct ways to reach the same correctness guarantee. Worth deeper treatment because the choice of implementation determines the system's behaviour under contention — which is to say, its behaviour at exactly the moments that matter most.

**Distributed transactions and two-phase commit** — The protocol for atomicity across partitions, and the failure modes (coordinator crash, indefinite blocking, the heuristic decisions that violate atomicity) that make it fragile in practice. Worth deeper treatment because this is the point where partitioning and transactions actually collide, and the alternatives (sagas, compensation, accepting weaker guarantees) are architectural decisions that deserve their own analysis.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Partitioning picks your pain: range vs hash

```python
# Same keys, two partitioning strategies.

keys = [1001, 1002, 1003, 9001]

def range_partition(user_id):
    if user_id < 5000:
        return "node_A"
    return "node_B"

def hash_partition(user_id):
    return ["node_A", "node_B"][hash(user_id) % 2]

for k in keys:
    print(k, "range->", range_partition(k), "hash->", hash_partition(k))
```

What this makes visible:

- **Range partitioning** keeps nearby keys together.
  - Query like `WHERE user_id BETWEEN 1000 AND 1999` can hit one node.
  - But if new users mostly get increasing IDs, one node becomes hot.
- **Hash partitioning** spreads load more evenly.
  - But `BETWEEN 1000 AND 1999` now likely needs **both nodes**.

The partition function is not just storage layout. It decides which queries are cheap and which become scatter-gather operations.

---

### 2) Secondary indexes stop routing from being easy

```sql
-- Table is partitioned by primary key: user_id
CREATE TABLE orders (
  order_id   BIGINT PRIMARY KEY,
  user_id    BIGINT,
  status     TEXT
);

-- Query we want:
SELECT * FROM orders WHERE status = 'PENDING';
```

```text
Case A: local secondary index on each partition
-----------------------------------------------
node_1 has index(status)
node_2 has index(status)
node_3 has index(status)

To answer status='PENDING':
  ask node_1
  ask node_2
  ask node_3
  merge results

Cheap writes, expensive reads (fan-out).
```

```text
Case B: global secondary index
------------------------------
global_index[status='PENDING'] -> [order_id 7, order_id 22, ...]

To answer status='PENDING':
  ask global index
  route to owning partitions for matching rows

Cheap reads, but every write must update:
  - the row's home partition
  - the global index, which may live elsewhere

Now one logical write touches multiple nodes.
```

Primary-key routing is simple because partitioning tells you where the row lives. Secondary indexes break that alignment.

---

### 3) Naive rebalancing: mod-N hashing moves almost everything

```python
keys = [10, 11, 12, 13, 14, 15]

def mod_n_partition(key, n):
    return key % n

before = {k: mod_n_partition(k, 3) for k in keys}
after  = {k: mod_n_partition(k, 4) for k in keys}

for k in keys:
    print(f"key={k}: before={before[k]} after={after[k]}")
```

Typical outcome: many keys change partitions when node count changes from 3 to 4.

That means:

- adding one node can force **massive data movement**
- cache locality disappears
- rebalancing becomes a cluster-wide event

A better scheme is usually:

```text
partition = hash(key) % 1024    # fixed logical partitions
node = assignment_table[partition]
```

Now adding a node mostly means reassigning some of the **1024 logical partitions**, not remapping every key in the database.

---

### 4) Read committed prevents dirty reads, but not changing answers

```sql
-- Initial row:
-- accounts(id=1, balance=100)

-- Transaction T1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- sees 100

-- Transaction T2
BEGIN;
UPDATE accounts SET balance = 50 WHERE id = 1;
COMMIT;

-- Back to T1, same transaction:
SELECT balance FROM accounts WHERE id = 1;  -- now sees 50
COMMIT;
```

At **read committed**:

- T1 does **not** see uncommitted data from T2
- but T1 can get **different answers** from the same query in one transaction

So "I wrapped it in a transaction" does **not** automatically mean "my reads are stable."

---

### 5) Snapshot isolation can still violate invariants: write skew

```sql
-- Rule: at least one doctor must remain on call.
-- Initial state:
-- doctors(name, on_call)
-- ('A', true), ('B', true)
```

```sql
-- Transaction T1
BEGIN;
SELECT COUNT(*) FROM doctors WHERE on_call = true;  -- 2
-- "Safe for A to go off call"
UPDATE doctors SET on_call = false WHERE name = 'A';
COMMIT;
```

```sql
-- Concurrent Transaction T2
BEGIN;
SELECT COUNT(*) FROM doctors WHERE on_call = true;  -- 2
-- "Safe for B to go off call"
UPDATE doctors SET on_call = false WHERE name = 'B';
COMMIT;
```

Final state:

```sql
SELECT * FROM doctors;
-- ('A', false), ('B', false)
```

Each transaction saw a consistent snapshot. Each changed a different row. Together they broke the rule.

That is the important lesson: **consistent snapshot** is weaker than **serializable correctness**.

---

### 6) Once a transaction spans partitions, atomicity needs coordination

```text
Goal: transfer $10 from account A on node_1 to account B on node_2

Without coordination:
  1. debit A on node_1   ✔
  2. network failure
  3. credit B on node_2  ✘

Money vanished.
```

Minimal two-phase commit pseudocode:

```text
coordinator:
  send PREPARE to node_1, node_2
  if all vote YES:
      send COMMIT
  else:
      send ABORT

participant (each node):
  on PREPARE:
    check constraints
    write "prepared" to durable log
    reply YES or NO

  on COMMIT:
    finalize changes

  on ABORT:
    discard changes
```

This fixes the "half-committed transfer" problem, but introduces distributed failure modes:

- if the **coordinator crashes** after participants prepare, they may block
- if a node is slow, others cannot tell whether it is slow or dead
- latency increases because commit now requires cross-node coordination

Partitioning scales the system by splitting data. Distributed transactions are the bill you pay when one invariant still spans the split.

---

## Key Ideas

Partitioning and transactions are linked because partitioning turns one machine's simple atomic updates into cross-node coordination problems. The sketches show the chain: partition strategy decides which requests are local and which scatter; secondary indexes break clean routing; naive rebalancing can make cluster changes painfully expensive; weaker isolation levels allow surprising anomalies even on one node; and once one transaction touches multiple partitions, atomicity requires protocols like two-phase commit, with real operational costs. The core skill is not memorizing terms, but recognizing which invariants remain local to a partition and which ones force you into distributed correctness.

</details>