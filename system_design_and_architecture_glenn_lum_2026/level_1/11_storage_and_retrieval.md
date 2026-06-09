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

### Introduction

A database feels like a black box until you understand the small number of data structures doing the actual work underneath. Every storage engine is just a set of choices about how to lay bytes down on disk and find them again — and each choice optimises for some access patterns while penalising others. The five sketches below build that mental model from the ground up, starting with the simplest possible design and adding one idea at a time. By the end, the performance characteristics of real databases — why Cassandra is fast at writes, why Postgres is predictable at reads, why you can't run analytics on your production database — should feel less like folklore and more like consequences.


### Sketch 1: The Hash Index

The simplest possible persistent store. A hash map in memory, an append-only log on disk.

```python
import csv, os

# The entire index lives in memory.
# Key → byte offset in the log file.
index = {}

def write(key, value):
    with open("log.csv", "a") as f:
        offset = f.tell()
        writer = csv.writer(f)
        writer.writerow([key, value])
    index[key] = offset          # remember where we just wrote

def read(key):
    if key not in index:
        return None
    with open("log.csv", "r") as f:
        f.seek(index[key])       # jump straight to it
        row = next(csv.reader(f))
        return row[1]

# Updates are just new appends. Old values stay on disk — wasted space.
write("name", "alice")
write("name", "bob")            # index now points to "bob", "alice" is orphaned
print(read("name"))             # → "bob"
```

**What this gets right:** Writes are just appends — the fastest thing you can do on disk. Reads are a single seek.

**The tradeoffs:**
- The entire key space must fit in RAM. The log grows forever without compaction.
- `index.keys()` gives you nothing useful about order — range queries like *"give me all keys between A and M"* are impossible.

---

### Sketch 2: Compaction (the hidden cost of append-only)

The log fills up with orphaned values. Compaction is the background job that cleans it up — but it costs I/O that competes with live traffic.

```python
def compact():
    # Read the current live value for every known key.
    live = {key: read(key) for key in index}

    # Rewrite the log from scratch with only live values.
    os.remove("log.csv")
    index.clear()
    for key, value in live.items():
        write(key, value)

write("x", "1")
write("x", "2")
write("x", "3")   # log has 3 rows; only the last matters
compact()          # log now has 1 row
```

**The tradeoff made visible:** Compaction is not free. While it runs, it reads and rewrites the entire log. In production systems this is a background thread competing with your queries for disk I/O. This tension — write fast now, pay the cost later — runs through every append-only design.

---

### Sketch 3: SSTable + LSM-Tree

Add one idea to Sketch 1: keep writes *sorted*. Writes land in a sorted in-memory buffer (the memtable). When it's full, flush it to disk as a sorted file (an SSTable). Reads check the memtable first, then each file on disk.

```python
import bisect

memtable = {}       # in-memory: absorbs all incoming writes
sstables = []       # on-disk: list of sorted [(key, value)] segments

MEMTABLE_LIMIT = 4

def write(key, value):
    memtable[key] = value
    if len(memtable) >= MEMTABLE_LIMIT:
        flush()

def flush():
    # Sort and move memtable to disk as a new SSTable segment.
    segment = sorted(memtable.items())
    sstables.append(segment)
    memtable.clear()
    print(f"Flushed segment: {segment}")

def read(key):
    if key in memtable:             # check memory first
        return memtable[key]
    for segment in reversed(sstables):   # newest segment first
        for k, v in segment:
            if k == key:
                return v
    return None

write("b", "2"); write("a", "1"); write("d", "4"); write("c", "3")
# → flushes: [('a','1'), ('b','2'), ('c','3'), ('d','4')]
print(read("a"))   # → "1"
print(read("c"))   # → "3"
```

**What this gets right:** Writes are always sequential (memtable flush → sorted append). No in-place updates anywhere. This is why LSM-tree databases advertise high write throughput.

**The tradeoffs:**
- A read for a missing key must scan *every* SSTable. As segments accumulate, reads get slower. (Real systems use Bloom filters to skip segments cheaply.)
- Segments pile up on disk. Compaction must merge them — same I/O tension as Sketch 2, now at larger scale. This is called *write amplification*.

---

### Sketch 4: B-Tree

Instead of an append-only log, data lives in fixed-size pages organised as a sorted tree. Writes find the right page and modify it in place.

```python
class BTreeNode:
    def __init__(self):
        self.keys   = []
        self.values = []
        self.children = []

    def is_leaf(self):
        return len(self.children) == 0

def read(node, key):
    for i, k in enumerate(node.keys):
        if key == k:
            return node.values[i]         # found it on this page
        if key < k:
            if node.is_leaf(): return None
            return read(node.children[i], key)   # go left
    if node.is_leaf(): return None
    return read(node.children[-1], key)          # go right

def write(node, key, value):
    i = 0
    while i < len(node.keys) and key > node.keys[i]:
        i += 1
    if i < len(node.keys) and node.keys[i] == key:
        node.values[i] = value            # update in place
        return
    if node.is_leaf():
        node.keys.insert(i, key)          # insert in sorted order
        node.values.insert(i, value)
    else:
        write(node.children[i], key, value)

root = BTreeNode()
write(root, "b", "2"); write(root, "a", "1"); write(root, "d", "4"); write(root, "c", "3")
print(read(root, "c"))   # → "3"
print(read(root, "z"))   # → None
```

**What this gets right:** Reads are predictable — traverse the tree, find the page, done. Range queries work naturally because keys are sorted within pages. There's no compaction background job.

**The tradeoffs:**
- Writes are random I/O — you have to find the right page, then modify it. Much more expensive than an append.
- Page splits (when a page is full) are complex and must be crash-safe. Real B-trees use a write-ahead log (WAL) to survive a crash mid-split — adding more write overhead.

---

### Sketch 5: Row vs Column Storage

Same data, two layouts. The layout alone determines whether analytical queries are fast or catastrophically slow.

```python
# Three records: id, age, country
rows = [
    {"id": 1, "age": 28, "country": "SG"},
    {"id": 2, "age": 34, "country": "MY"},
    {"id": 3, "age": 22, "country": "SG"},
]

# ROW store: each record is stored together.
row_store = rows   # → [{id,age,country}, {id,age,country}, ...]

# COLUMN store: each field is stored together.
col_store = {
    "id":      [r["id"]      for r in rows],
    "age":     [r["age"]     for r in rows],
    "country": [r["country"] for r in rows],
}

# OLTP query: fetch one full record. Row store wins.
def get_record_row(id):
    return next(r for r in row_store if r["id"] == id)   # one read, all fields

def get_record_col(id):
    i = col_store["id"].index(id)
    return {k: col_store[k][i] for k in col_store}       # must touch every column

# OLAP query: aggregate one column. Column store wins.
def avg_age_col():
    return sum(col_store["age"]) / len(col_store["age"]) # touches only "age"

def avg_age_row():
    return sum(r["age"] for r in row_store) / len(row_store)  # reads every field of every row
```

**What this makes visible:**
- `avg_age_col()` reads one array. `avg_age_row()` reads every field of every row to get to `age`.
- At millions of rows, that's the difference between microseconds and seconds.
- Column storage also compresses aggressively — `["SG", "MY", "SG", "SG", "SG"]` becomes trivial to encode. Row storage can't do this because adjacent bytes belong to different fields.

**The fundamental mismatch:** A column store makes single-row writes painful — inserting one record means appending to *every* column array. This is why you can't use an analytical database as your application database, and why trying produces exactly the kind of performance problems that look like tuning issues but are actually the wrong architecture.

---

These five sketches cover the full arc of the document — from the simplest possible design to the architectural split that explains why OLTP and OLAP databases exist as separate categories.

</details>