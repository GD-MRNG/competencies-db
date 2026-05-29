## Metadata
- **Date:** 23-05-2026
- **Source:** 15_batch_and_stream_processing_at_the_data_layer.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-15 · Batch and Stream Processing at the Data Layer

Most of the data in a mature system is not written by users. It is computed. The search index is derived from the product catalogue. The analytics dashboard is derived from the event stream. The cache is derived from the database. The ML feature store is derived from a dozen upstream tables. The recommendations are derived from the features. By the time a request reaches a user-facing surface, it has typically passed through several stages of derivation, each of which had to keep itself in sync with something upstream. Understanding how that synchronisation happens is the difference between treating your data architecture as a coherent system and treating it as a pile of pipelines that mysteriously break on Tuesdays.

Kleppmann's framing for this is the idea of derived data — data that exists because it was computed from other data, rather than because a user wrote it. The source of truth is the input; everything else is a derivation that must, somehow, track changes to that input. Once you start looking for derived data you see it everywhere: every index is derived data, every cache is derived data, every replica is derived data, every materialised view is derived data, every search system, every analytics warehouse, every feature store. The architectural question is not whether you have derived data — you do — but how you keep it consistent with its source, and how stale you are willing to let it get.

There are two paradigms for answering that question, and almost every modern data architecture is some combination of them. The first is batch processing: take a snapshot of the input, run a deterministic computation over it, produce an output, repeat on a schedule. MapReduce was the canonical example, and the model has since evolved into dataflow engines like Spark and Flink, but the shape is the same — bounded inputs, deterministic transforms, outputs that supersede previous outputs. Batch processing is conceptually simple and operationally forgiving. If a job fails, you re-run it. If the logic changes, you re-run it over the historical inputs and the output corrects itself. The cost is freshness: your derived data is as old as your last batch run.

The second paradigm is stream processing: treat the input as an unbounded sequence of events, and process each one as it arrives. The output is updated incrementally rather than recomputed from scratch. The connective tissue here is the event log — most prominently Kafka, but the pattern is older — which provides a durable, ordered, replayable record of what has happened. Stream processing buys you freshness: derived data can be seconds behind the source rather than hours. The cost is that incremental computation is harder to reason about than batch computation, failure recovery is more subtle, and the operational surface area is larger.

The most architecturally important pattern in this space is change data capture. Instead of having applications write to the database and also publish events (and inevitably get the two out of sync), CDC treats the database's write-ahead log as the event stream. Every committed write becomes an event that downstream systems can subscribe to. This collapses what used to be a synchronisation problem into a pure derivation problem: the database is the source of truth, the log is the canonical record of changes, and every other data system — search indexes, caches, warehouses, feature stores — becomes a stream consumer that maintains its own materialisation. CDC is the mechanism that makes "the database is the source of truth" into an architecturally enforceable claim rather than a hopeful slogan.

Once you have both paradigms in play, you face the question of how to combine them. The historical answer was the Lambda architecture: run a batch pipeline for correctness and a stream pipeline for freshness, and reconcile the two at query time. This works but it doubles your code and creates two places where the same logic can drift apart. The Kappa architecture is the response: use the stream pipeline for everything, and handle reprocessing by replaying the log from the beginning. Kappa is conceptually cleaner; Lambda is sometimes operationally unavoidable. The choice between them is a real tradeoff, not a fashion question, and it surfaces directly in how your team will spend its time for years afterward.

The reason this layer matters so much is that it is where data freshness, consistency, and architectural complexity all collide. A product manager asking "why is the dashboard wrong" is asking a question that lives in this layer. A user seeing stale search results is experiencing this layer. An ML model trained on features that don't match production is failing in this layer. The architectural decisions you make about batch versus stream, about CDC versus dual writes, about Lambda versus Kappa, are not infrastructure choices that can be deferred to the data team — they are decisions about what your system can promise its users about how recent and how correct the information they see actually is.

The skill this topic builds is the ability to look at any data-driven feature and ask the right four questions: what is the source of truth, what is the derivation, how does the derivation stay in sync, and how stale is it allowed to get. Once those questions are explicit, the architectural choices become legible — and the production surprises stop being surprises.

## Level 2 candidates

**MapReduce and the batch processing model** — The foundational batch processing paradigm and the constraints (no shared state, deterministic outputs, bounded inputs) that define what batch can and cannot do. Worth going deeper because the limitations of MapReduce explain the design of every dataflow engine that came after it.

**Dataflow engines beyond MapReduce** — Spark, Flink, and the architectural moves (pipelining, in-memory processing, unified batch-and-stream APIs) that addressed MapReduce's performance ceiling. Worth a deep dive because the operational characteristics of these engines are dramatically different and the choice between them is a real architectural decision.

**Stream processing and messaging systems** — The distinction between traditional message queues (AMQP, JMS) and partitioned logs (Kafka), and why log-based messaging changes what consumers can do. Worth going deeper because replayability and consumer independence are the properties that make modern derived-data architectures possible.

**Change Data Capture (CDC)** — The pattern for treating a database's write-ahead log as an event stream that downstream systems consume. Worth a deep dive because CDC is the most robust mechanism for keeping derived data in sync, and the operational details (snapshot bootstrapping, schema changes, ordering guarantees) are where most CDC deployments succeed or fail.

**Combining batch and stream: Lambda and Kappa architectures** — The two strategies for systems that need both historical reprocessing and real-time updates, and the operational complexity each one trades for its consistency guarantees. Worth a deep dive because the choice shapes years of engineering effort and the tradeoffs are not obvious from the outside.

**Exactly-once semantics in stream processing** — The mechanisms (idempotent producers, transactional writes, end-to-end deduplication) that make stream processing safe in the presence of retries and failures. Worth going deeper because "exactly once" is the term most often misunderstood in this space and the actual guarantees depend on conditions that are easy to violate.

---