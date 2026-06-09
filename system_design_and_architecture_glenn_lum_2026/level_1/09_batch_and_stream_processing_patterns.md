## Metadata
- **Date:** 23-05-2026
- **Source:** 09_batch_and_stream_processing_patterns.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-09 · Batch and Stream Processing Patterns

Most of the architectural vocabulary you absorb early in your career is shaped around the request-response model: a client calls, a server answers, and the latency budget for the whole exchange is measured in milliseconds. That model is so dominant it becomes invisible, and the invisibility is the problem. A large fraction of what production systems actually do is not request-response at all. It is work that runs on a schedule, work that fans out across hundreds of workers, work that flows through multi-stage pipelines where each stage hands off to the next. When you treat these as exotic edge cases rather than as a first-class category of computation with its own pattern library, you end up reinventing — badly — patterns that have well-understood shapes and well-understood failure modes.

The mental shift Burns asks you to make is to stop thinking of asynchronous processing as "the thing we do when synchronous didn't work" and start thinking of it as a distinct architectural mode with its own structural primitives. In request-response, the unit of reasoning is the call. In batch and stream processing, the unit of reasoning is the pipeline: a graph of stages through which work flows, where the interesting questions are about how work is divided, how stages coordinate, and what happens when a stage fails partway through. The patterns in this topic are the named, reusable shapes that pipeline graphs take.

The first primitive is the work queue. You have a large pool of discrete units of work — image thumbnails to generate, emails to send, records to process — and a pool of workers that can each handle one unit at a time. The queue is the connective tissue that decouples the producers from the consumers, lets you scale the worker pool independently of the work source, and absorbs bursts. This is the foundation of essentially every background processing system you have ever encountered, and it is also the source of most of the operational pain those systems generate. The pain is not accidental: a queue introduces an asynchronous boundary, and asynchronous boundaries force you to confront delivery semantics. Most queue systems give you at-least-once delivery, which means workers must be idempotent, which means the operation each worker performs has to be designed for the possibility of being executed twice. The work queue pattern is simple to draw and structurally demanding to operate.

The second primitive is event-driven batch processing — pipelines built by composing small, single-purpose stages. The stages have names that describe what they do to the stream of events flowing through them: a copier duplicates events into multiple downstream branches, a filter drops events that do not match a predicate, a splitter breaks one event into many, a merger combines multiple inputs into one. Each stage does one thing, and the pipeline's behaviour is the composition of its stages. This is the pattern that makes data pipelines modular: you can rearrange the stages, insert new ones, swap implementations, without rewriting the system. It is also the pattern that, when ignored, produces the monolithic ETL script — thousands of lines of procedural code that nobody dares to modify because the stages are not separable.

The third primitive is coordinated batch processing, which exists because some computations cannot be expressed as a stream of independent stages. Some require synchronisation: a reduce step that must wait for all map outputs before it can run, an image processing pipeline where the second pass needs the complete result of the first, a multi-phase computation where stage N+1 cannot begin until stage N has fully completed. The coordination introduces a barrier, and the barrier introduces a class of problems — stragglers, partial failures, restart semantics — that work queues and event-driven pipelines do not have to deal with. This is where batch processing earns its reputation for operational complexity, and it is also where the most architecturally interesting choices get made.

The thread that runs through all three primitives is that the structural choice you make at the pattern level dictates the failure modes you will spend your operational life dealing with. Work queues give you simplicity at the cost of duplicate-execution risk. Event-driven pipelines give you modularity at the cost of debugging difficulty when an event takes a wrong turn three stages downstream of where the bug actually is. Coordinated pipelines give you the ability to express computations the other two cannot, at the cost of synchronisation logic that must handle every variation of partial failure. None of the patterns are free, and none of them are wrong — they each match a different shape of problem.

There is also a more recent shift that sits underneath all of this: the move from point-to-point queues to partitioned logs as the connective tissue between stages. Kafka is the canonical example, but the architectural significance is broader than any one product. A traditional queue is a delivery mechanism — once the message is consumed, it is gone. A partitioned log is a durable, replayable, ordered record that multiple independent consumers can read at their own pace. That single change — making the substrate replayable — collapses a class of problems that batch and stream architectures have historically had to solve in application code. Reprocessing becomes possible. New consumers can be added without coordinating with existing ones. The boundary between batch and stream blurs, because both are now reading from the same kind of substrate.

What this topic builds is the ability to look at a piece of asynchronous infrastructure — a Sidekiq cluster, an Airflow DAG, a Spark job, a Kafka consumer group — and recognise which of these patterns it is implementing, what failure modes that pattern carries, and what alternatives existed when it was designed. Most asynchronous systems in production were not chosen so much as accumulated; making the patterns explicit is what lets you reason about whether the accumulation matches the work the system is actually doing.

## Level 2 candidates

**Work queue systems** — The pattern for distributing discrete units of work across a pool of workers, including the queue, the worker pool, and the delivery semantics that connect them. Worth deeper treatment because at-least-once delivery and the idempotency requirements it imposes are where most production incidents in background processing systems originate.

**Event-driven batch processing** — Composing pipelines from named single-purpose stages — copier, filter, splitter, merger — and the discipline of keeping each stage independently reasonable. Worth a deeper post because the stage taxonomy is more precise than most engineers realise, and using the names correctly is what keeps pipelines modular rather than monolithic.

**Coordinated batch processing** — Multi-stage computations with synchronisation barriers, where later stages depend on the completion of earlier ones. Worth going deeper on because the failure modes — stragglers, partial completion, restart semantics — are qualitatively different from the uncoordinated cases and need their own framework.

**Kafka as a pipeline primitive** — How partitioned logs replace point-to-point queues as the substrate of distributed batch and stream systems. Worth deeper treatment because the shift from delivery-based to log-based messaging is one of the more consequential architectural moves of the last decade, and its implications for replayability, consumer independence, and the batch/stream boundary deserve to be made explicit.

**Delivery semantics in asynchronous systems** — At-most-once, at-least-once, and exactly-once, and what each one actually costs to achieve in a real pipeline. Worth a deeper post because these semantics are usually treated as configuration rather than as architectural decisions, and the gap between what people assume their system delivers and what it actually delivers is where silent data corruption lives.

---


<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Work queue: producers and workers are decoupled

```python
# producer.py
queue = []

def enqueue(job):
    queue.append(job)

enqueue({"type": "send_email", "to": "a@example.com"})
enqueue({"type": "send_email", "to": "b@example.com"})
```

```python
# worker.py
def handle(job):
    print("doing", job)

while queue:
    job = queue.pop(0)   # take next job
    handle(job)
```

What this makes visible:
- The producer does not do the work itself.
- Workers can scale separately from producers.
- The queue absorbs bursts.

What it hides, and therefore what becomes the real problem:
- What if the worker crashes after starting the job?
- How do we know whether the job is finished?
- Can the same job run twice?

---

### 2) At-least-once delivery means workers must be idempotent

```python
sent_emails = set()

def send_email(job):
    recipient = job["to"]

    # idempotency guard: safe if job is delivered twice
    if recipient in sent_emails:
        return "already sent"

    print("sending email to", recipient)
    sent_emails.add(recipient)
    return "sent"
```

Counter-example:

```python
total_charged = 0

def charge_card(job):
    global total_charged
    total_charged += job["amount"]   # BAD: duplicate delivery charges twice
```

Safer shape:

```python
processed_payments = set()
total_charged = 0

def charge_card(job):
    global total_charged
    payment_id = job["payment_id"]

    if payment_id in processed_payments:
        return "already charged"

    total_charged += job["amount"]
    processed_payments.add(payment_id)
```

The core idea:
- In many queue systems, “maybe twice” is normal.
- So the worker logic must be safe to repeat.

---

### 3) Event-driven pipeline: each stage does one thing

```python
events = [
    {"user": "u1", "active": True,  "items": ["a", "b"]},
    {"user": "u2", "active": False, "items": ["c"]},
]

def filter_active(events):
    return [e for e in events if e["active"]]

def split_items(events):
    out = []
    for e in events:
        for item in e["items"]:
            out.append({"user": e["user"], "item": item})
    return out

def enrich(events):
    return [{**e, "source": "batch-2026-05-23"} for e in events]

result = enrich(split_items(filter_active(events)))
print(result)
# [{'user': 'u1', 'item': 'a', 'source': 'batch-2026-05-23'},
#  {'user': 'u1', 'item': 'b', 'source': 'batch-2026-05-23'}]
```

Why this matters:
- `filter_active` filters.
- `split_items` splits one event into many.
- `enrich` adds data.
- Small stages are easier to reorder, test, and replace.

The cost:
- When output is wrong, the bug may be several stages upstream.

---

### 4) Monolithic ETL vs composable stages

Before: one large script, mixed responsibilities

```python
def process(events):
    out = []
    for e in events:
        if e["active"]:                 # filter
            for item in e["items"]:     # split
                out.append({            # enrich
                    "user": e["user"],
                    "item": item,
                    "source": "batch-2026-05-23"
                })
    return out
```

After: same logic, but separable

```python
def process(events):
    return enrich(split_items(filter_active(events)))
```

The point is not fewer lines.
The point is named boundaries:
- you can insert a new stage,
- swap one stage,
- test one stage,
- reason about one failure at a time.

---

### 5) Coordinated batch processing: barriers change the failure mode

Some jobs cannot stream straight through. A later phase must wait for all earlier work.

```python
# Phase 1: map
inputs = [1, 2, 3, 4]
partials = []

for x in inputs:
    partials.append(x * 10)   # imagine many workers

# Barrier: reduce cannot start until all partials exist
if len(partials) == len(inputs):
    total = sum(partials)
    print(total)  # 100
```

Failure case:

```python
inputs = [1, 2, 3, 4]
partials = [10, 20, 30]   # one worker never finished

if len(partials) == len(inputs):
    print(sum(partials))
else:
    print("wait / retry / mark failed")
```

New problems introduced by the barrier:
- One slow worker delays everyone else.
- Partial completion must be tracked.
- Restarting must avoid losing completed work or counting it twice.

---

### 6) Queue vs partitioned log: consume-and-delete vs replay

Traditional queue mental model:

```text
enqueue A
worker reads A
A is gone
```

Partitioned log mental model:

```python
log = ["A", "B", "C"]

consumer1_offset = 0
consumer2_offset = 0

# consumer1 reads A, B
consumer1_offset = 2

# consumer2 is independent, reads only A
consumer2_offset = 1

# log still contains A, B, C
# consumers track position, not message deletion
```

What changes:
- New consumers can start later and replay old data.
- Reprocessing becomes possible.
- Multiple consumers can read the same history independently.

The cost:
- You now manage offsets and retention.
- “Who has processed what?” moves from queue deletion to consumer state.

## Key Ideas

Batch and stream systems are easier to understand when you stop treating them like slower request-response systems and instead model them as pipelines with explicit structure. A work queue solves decoupling and scaling, but forces you to design for duplicate delivery. Event-driven pipelines stay manageable when each stage has one job and a clear name; otherwise they collapse into fragile ETL blobs. Coordinated batch jobs add barriers, which make some computations possible but introduce stragglers, partial completion, and restart complexity. Finally, replacing point-to-point queues with replayable logs changes the substrate itself: messages are no longer “used up,” so reprocessing and independent consumers become first-class patterns.

</details>