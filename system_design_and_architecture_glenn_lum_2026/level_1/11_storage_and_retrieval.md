## Metadata
- **Date:** 23-05-2026
- **Source:** 11_storage_and_retrieval.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-11 · Storage and Retrieval

Most engineers treat the choice of database as a question of features: does it support JSON, does it have full-text search, does it scale horizontally, does the team already know it. This is the wrong layer to be reasoning at. Underneath every database is a small number of data structures doing the actual work of putting bytes on disk and finding them again, and those data structures are the thing that determines whether your workload will be fast or slow, whether your writes will keep up with your reads, and whether the system will degrade predictably or fall off a cliff under load. The features are downstream of the storage engine. The storage engine is the architecture.

The mental model worth building is this: a storage engine is a set of choices about how data is laid out on disk and how it is found again, and every choice optimises for some access patterns at the expense of others. There is no neutral storage engine. A database that is fast at writes is fast at writes because it has accepted a cost somewhere else — usually read amplification, or space amplification, or background work that competes with foreground queries. A database that is fast at range queries pays for that with a more expensive write path. The job is not to find the storage engine without tradeoffs; it is to understand which tradeoffs the engine has made and whether those match the workload you are putting on it.

The simplest persistent index is the hash index: a hash map from key to file offset, kept in memory, pointing into an append-only log on disk. Writes are an append (cheap) and a hash table update (cheap). Reads are a hash lookup followed by a single disk seek (cheap). It is genuinely fast, and it is the conceptual ancestor of more sophisticated designs. But the constraints are severe — the entire key space must fit in memory, range queries are impossible because hash buckets are unordered, and the log has to be compacted in the background to reclaim space from overwritten keys. Hash indexes survive in narrow niches (Bitcask, some caching layers) and as a teaching example. Their real value is showing you the shape of the design space.

The two designs that dominate real-world storage engines extend the basic idea in opposite directions. SSTables and LSM-trees take the append-only log and add sortedness — writes go into an in-memory sorted structure (a memtable), which is periodically flushed to disk as a sorted file, and these sorted files are merged in the background through a process called compaction. This makes writes extremely fast (sequential disk writes, no in-place updates) and supports range queries (the files are sorted), but reads may have to check multiple files before finding a key, and compaction consumes I/O that competes with the foreground workload. This is the architecture behind Cassandra, RocksDB, LevelDB, and ScyllaDB — and the reason those databases make the write-throughput claims they do.

B-trees take the opposite path. Data lives in fixed-size pages on disk, organised as a balanced tree, and writes happen by locating the right page and modifying it in place. Reads are predictable — a small number of page traversals to find any key. Range queries are efficient because the tree is ordered. But writes are more expensive than in an LSM-tree (random I/O, page splits, write-ahead logging to survive crashes mid-write), and the data structure is more complex. This is the architecture behind PostgreSQL, MySQL/InnoDB, SQL Server, and most of the relational databases you have ever used. It is not an accident that the read-optimised path and the relational model have converged on each other for forty years.

Cutting across this distinction is another one that matters at least as much: transactional versus analytical workloads. OLTP systems serve many small queries, each touching a few rows, with strict latency requirements — the kind of work an application server generates. OLAP systems serve few large queries, each scanning millions or billions of rows, aggregating across columns — the kind of work a dashboard or a data scientist generates. The same row-oriented storage that makes OLTP fast (a row's fields are stored together, so fetching a row is one sequential read) makes OLAP catastrophically slow (computing the average of one column means reading every other column too). Column-oriented storage flips the layout — values from the same column are stored together — which makes analytical scans dramatically faster and enables aggressive compression, but makes writing or updating a single row painful. This is why analytical databases (Redshift, BigQuery, ClickHouse, Snowflake) exist as a separate category from transactional ones, and why trying to use one for the other's workload produces the kind of performance problems that look like configuration issues but are actually architectural mismatches.

What this layer gives you is the ability to read database performance claims as the consequences of design choices rather than as marketing. When a vendor says "10x faster writes," you can ask what they did to the read path. When a system slows down after running for weeks, you can suspect compaction or vacuuming and know where to look. When someone proposes putting analytical queries on the production OLTP database, you can name the specific reason that will fail rather than gesturing at "it'll be slow." Storage engines are the layer where database selection stops being folklore and starts being engineering.

## Level 2 candidates

**Hash indexes** — Covers the mechanics of in-memory hash maps over append-only logs, including segmentation, compaction, and crash recovery. Worth deeper treatment because the constraints (memory-bound key space, no range queries, compaction overhead) are instructive about the general shape of every storage engine's tradeoff surface, even though hash indexes themselves are rarely the right choice.

**SSTables and LSM-trees** — Covers the write path through memtables, the structure of sorted string tables, and the compaction strategies (size-tiered vs. leveled) that determine read amplification and space amplification behaviour. Worth deeper treatment because LSM-trees power most of the write-optimised databases in production today, and their failure modes (write stalls, compaction backlog, tombstone accumulation) are not intuitive without understanding the mechanism.

**B-trees** — Covers page structure, splits and merges, write-ahead logging, and the concurrency control mechanisms that make B-trees safe under concurrent access. Worth deeper treatment because B-trees are the storage layer of nearly every relational database, and understanding how they handle crash safety and concurrent writes is the prerequisite for reasoning about transaction performance and replication lag at the storage level.

**OLTP vs OLAP** — Covers the workload distinction between transactional and analytical systems, including query patterns, latency requirements, and why the same database optimised for one will fail at the other. Worth deeper treatment because the mismatch between workload and storage engine is one of the most common sources of unexplained performance problems in production data systems, and naming it precisely is the first step to fixing it.

**Column-oriented storage** — Covers the columnar data layout, compression techniques (run-length encoding, bitmap indexes), and vectorised execution that make analytical queries fast. Worth deeper treatment because columnar storage is the architecture behind every modern analytical database, and understanding why it is incompatible with transactional workloads (despite appearing to store the same data) clarifies when a separate analytical system is required rather than optional.

---

<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### Sketch 1: Hash index = fast append, no ordering

```python
# key -> latest value
log = []          # on disk: append-only
index = {}        # in memory: key -> position in log

def put(key, value):
    log.append((key, value))          # cheap append
    index[key] = len(log) - 1         # cheap hash update

def get(key):
    pos = index.get(key)
    return None if pos is None else log[pos][1]

put("user:1", "Alice")
put("user:1", "Bob")   # update = append again; old value still exists
print(get("user:1"))   # Bob

print(log)
# [('user:1', 'Alice'), ('user:1', 'Bob')]
# Fast writes, but stale bytes accumulate.
```

This makes one tradeoff obvious: writes are cheap because nothing is updated in place. But the hash table is unordered, so queries like “all keys from `user:100` to `user:200`” have no efficient path.

---

### Sketch 2: Append-only needs compaction

```python
log = [("x", "1"), ("x", "2"), ("y", "9"), ("x", "3")]
index = {"x": 3, "y": 2}

def compact(log):
    latest = {}
    for i, (k, v) in enumerate(log):
        latest[k] = v                 # keep only newest value per key
    return list(latest.items())       # rewritten log

print("before:", log)
print("after: ", compact(log))
# before: [('x','1'), ('x','2'), ('y','9'), ('x','3')]
# after:  [('x','3'), ('y','9')]
```

Compaction recovers space, but it is extra background work: read old data, rewrite live data, compete with foreground traffic. “Fast writes” often means “pay later.”

---

### Sketch 3: LSM idea = buffer writes, flush sorted files

```python
memtable = {}     # in memory
sstables = []     # on disk, each sorted by key

def put(key, value):
    memtable[key] = value

def flush():
    global memtable
    sstables.append(sorted(memtable.items()))   # write one sorted segment
    memtable = {}

def get(key):
    if key in memtable:
        return memtable[key]
    for table in reversed(sstables):            # newest file first
        for k, v in table:
            if k == key:
                return v
    return None

put("b", 2); put("a", 1); flush()
put("c", 3); flush()

print(sstables)
# [[('a', 1), ('b', 2)], [('c', 3)]]
print(get("a"))  # 1
```

Sorted files buy you range queries and cheap sequential writes. The cost is visible in `get`: reads may need to check several files. Real LSM systems add Bloom filters and compaction because too many SSTables make reads and storage worse.

---

### Sketch 4: B-tree idea = ordered pages, update in place

```python
# One "page" kept sorted.
page = [("a", 1), ("c", 3), ("d", 4)]

def get(key):
    for k, v in page:          # real B-trees do this across tree pages
        if k == key:
            return v
        if k > key:
            return None
    return None

def put(key, value):
    for i, (k, _) in enumerate(page):
        if k == key:
            page[i] = (key, value)     # overwrite in place
            return
        if k > key:
            page.insert(i, (key, value))
            return
    page.append((key, value))

print(get("c"))   # 3
put("b", 2)
print(page)       # [('a',1), ('b',2), ('c',3), ('d',4)]
```

This tiny page sketch shows the core B-tree property: data stays ordered where it lives. Reads and range scans are predictable. The cost is that writes are not simple appends anymore—they must find and modify the right page, and full pages force splits. Real systems add a WAL because crashes during page updates must be recoverable.

---

### Sketch 5: Same rows, two layouts, opposite strengths

```python
rows = [
    {"id": 1, "age": 28, "country": "SG"},
    {"id": 2, "age": 34, "country": "MY"},
    {"id": 3, "age": 22, "country": "SG"},
]

row_store = rows

column_store = {
    "id":      [1, 2, 3],
    "age":     [28, 34, 22],
    "country": ["SG", "MY", "SG"],
}

def fetch_user_row(id):
    return next(r for r in row_store if r["id"] == id)

def avg_age_col():
    return sum(column_store["age"]) / len(column_store["age"])

print(fetch_user_row(2))  # touches one row, gets all fields
print(avg_age_col())      # touches one column, skips the rest
```

The storage layout determines the workload it likes. Row layout is good for OLTP: “get me user 2.” Column layout is good for OLAP: “average age over 100M users.” Using one for the other is not a tuning mistake; it is an architectural mismatch.

---

### Sketch 6: Read vendor claims as tradeoffs

| Claim | Likely storage choice | Cost moved where? |
|---|---|---|
| “Very fast writes” | Append-only / LSM | Compaction, read amplification |
| “Predictable point reads” | B-tree | More expensive writes, page management |
| “Fast range scans” | Ordered structure | Writes must preserve order |
| “Fast analytics” | Column store | Painful row updates/inserts |
| “Simple key lookup only” | Hash index | No efficient range queries |

This is the practical skill: translate performance claims into storage-engine consequences.

## Key Ideas

Storage engines are not interchangeable boxes with different feature checklists; they are different answers to two questions: how do we write bytes, and how do we find them again? Hash indexes optimise for simple key lookups with cheap appends, LSM-trees extend that idea into sorted immutable files with compaction-heavy write optimisation, B-trees keep data ordered in place for predictable reads and range scans, and row versus column layout determines whether the system fits transactional or analytical work. Once you can see those few underlying structures, database behavior stops looking mysterious: every speedup is bought by a cost somewhere else.

</details>