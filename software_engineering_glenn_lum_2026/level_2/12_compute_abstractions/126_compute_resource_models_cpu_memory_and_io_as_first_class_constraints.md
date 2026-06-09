## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers treat CPU, memory, and I/O as configuration fields — numbers you plug into a deployment spec or instance type selector. You set `cpu: "500m"` and `memory: "256Mi"`, maybe because a teammate suggested those values, maybe because they were copy-pasted from a boilerplate. The workload runs. Nobody asks questions until something breaks: tail latency spikes inexplicably, a pod gets killed with no warning, or a service that handles ten requests per second falls over at twelve. When it does break, the debugging is painful precisely because the engineer never built an intuition for *which resource was the actual constraint* and *how that resource behaves when it runs out*. CPU, memory, and I/O are not interchangeable "resources" with a shared behavior model. They are fundamentally different physical constraints with different contention mechanics, different failure modes, and different observability signatures. Understanding those differences is the prerequisite for right-sizing anything.

## CPU: A Compressible, Time-Shared Resource

CPU is time. Specifically, it is access to a processor's execution cycles, shared across all processes competing for them. The key property that governs everything else: **CPU is compressible**. When a process cannot get the CPU time it wants, it does not crash. It slows down. It waits its turn. This makes CPU contention insidious — your workload degrades gradually, and the degradation shows up as latency, not errors.

On Linux, the scheduler responsible for dividing CPU time among processes is the **Completely Fair Scheduler (CFS)**. CFS assigns each process a *weight* proportional to its priority, then distributes available CPU time accordingly. When you set a CPU request in a container orchestrator, you are setting that weight. A container requesting 500 millicores gets half the scheduling weight of one requesting 1000 millicores. This matters only during contention: if the host has spare cycles, both containers can burst beyond their requested share.

CPU *limits* work differently. They impose a hard ceiling using a mechanism called **CFS bandwidth control**. The scheduler gives each cgroup a quota of microseconds per a defined period (typically 100ms). A container with a limit of 500 millicores gets 50ms of CPU time per 100ms period. If it exhausts that quota before the period ends, the scheduler **throttles** it — the container's threads are paused until the next period begins, even if the CPU is otherwise idle.

This throttling behavior is the source of a common, painful production issue. Consider a service that handles HTTP requests with a p50 latency of 5ms. Under normal load, it rarely hits its CPU limit. Under a burst, several requests arrive simultaneously, the container burns through its 50ms quota in the first 30ms of a period, and the remaining in-flight requests stall for 70ms waiting for the next period to start. The p99 latency jumps from 20ms to 90ms. From the application's perspective, nothing went wrong — no errors, no crashes. From the user's perspective, the service became unusable. The only observable signal is the throttling metric (`nr_throttled` and `throttled_time` in the cgroup's cpu.stat), which most teams do not monitor until they have already been burned by it.

A CPU-bound workload is one where adding more CPU time directly reduces execution time: mathematical computation, serialization/deserialization, compression, image processing. The defining characteristic is that the process is *runnable* — it has work to do and is just waiting for the processor. You can identify this by looking at CPU utilization relative to the limit and checking for throttling. If your container is using 95% of its CPU limit and your latency is climbing, you are CPU-bound.

## Memory: An Incompressible, Cliff-Edge Resource

Memory is space. Specifically, it is addressable bytes of RAM. The defining property: **memory is incompressible**. When a process needs more memory than is available, the system cannot simply slow it down and ask it to wait. Something must give. Either the kernel evicts pages to make room, or it kills a process to reclaim memory. There is no graceful degradation — there is a cliff.

When a process allocates memory, it is working with **virtual memory** — addresses that the kernel maps to physical RAM on demand. The actual physical memory consumed is the **resident set size (RSS)**. A process might have a virtual address space of 4GB but only 200MB resident in physical memory. What matters for resource accounting is the RSS (plus cache and other kernel-attributed memory for that cgroup), because that is what is actually occupying the finite physical resource.

In a container orchestrator, a memory *request* tells the scheduler how much memory to *guarantee* — it influences which node the container is placed on. A memory *limit* tells the kernel the absolute maximum. When a container's memory usage (as tracked by the cgroup) reaches its limit, the kernel's **OOM (Out-Of-Memory) killer** terminates a process within that cgroup. The container restarts (if your orchestrator is configured that way), users see errors, and in-flight work is lost.

This cliff-edge behavior makes memory the most dangerous resource to get wrong. Consider a Java service with a heap configured to 512MB running in a container with a 600MB memory limit. The JVM's heap is 512MB, but the JVM also needs memory for thread stacks, the metaspace (class metadata), JIT compiler buffers, native libraries, and the garbage collector itself. Total JVM memory consumption can easily reach 650MB, which exceeds the container's 600MB limit. The OOM killer fires. The container restarts. It loads state back into memory, climbs back to 650MB, and gets killed again. This crash loop is entirely predictable from the mechanics, but engineers routinely set memory limits based on heap size alone without accounting for off-heap consumption.

A memory-bound workload is one constrained by how much data it can hold resident at once: large in-memory caches, services that buffer large request/response payloads, batch jobs processing datasets that don't fit in available RAM. The symptom is not slowness (that's CPU) — it's either OOM kills or, when the system starts swapping, catastrophic latency degradation as every memory access potentially hits disk.

### The Asymmetry Between CPU and Memory Failure

This asymmetry is worth making explicit. CPU overcommitment causes degradation: things get slower. Memory overcommitment causes failure: things get killed. This means the consequences of getting your resource model wrong depend entirely on *which* resource you got wrong. Teams that set aggressive limits on CPU get latency surprises. Teams that set aggressive limits on memory get availability incidents. The operational posture should be different for each: you can afford tighter CPU limits if you accept some throttling during peaks, but memory limits need headroom because the failure mode is binary.

## I/O: The Queue You Cannot See

I/O encompasses disk reads and writes, network sends and receives, and any interaction where the process is waiting on an external system. The key property: **I/O-bound workloads are blocked, not busy**. The CPU is not doing useful work — it is waiting for data to arrive from a disk, a network socket, or a downstream service.

This creates a counterintuitive observability signature. An I/O-bound service under load can show low CPU utilization. An engineer looking at a dashboard sees CPU at 15% and concludes there is plenty of headroom. In reality, the service is saturated — every thread is blocked waiting on disk or network, and adding more CPU will not help at all. The correct diagnostic signals are **I/O wait time** (shown as `iowait` in system-level CPU breakdowns, representing time the CPU spent idle while waiting for I/O), disk latency and throughput metrics, and network socket queue depths.

Disk I/O contention manifests in two distinct ways. **Throughput-bound** workloads need to move large volumes of data — sequential reads for analytics, log shipping, large file transfers. They saturate the disk's bandwidth. **Latency-bound** workloads need many small random reads or writes — database queries hitting indexes, key-value store lookups. They saturate the disk's IOPS (I/O operations per second). An SSD might provide 500MB/s throughput and 100,000 IOPS, but a workload doing 4KB random reads will hit the IOPS ceiling long before the throughput ceiling. Choosing storage based on throughput when your workload is latency-bound is a common and expensive mistake.

Network I/O introduces another dimension: the latency and reliability of downstream dependencies. A service making synchronous calls to a database with a p99 latency of 50ms will spend the overwhelming majority of its wall-clock time waiting, regardless of how fast its CPU-bound code is. This is why architectures that involve many synchronous service-to-service calls are fundamentally I/O-bound systems, even if each individual service considers itself compute-intensive.

### Resource Interaction: When Bottlenecks Shift

In practice, workloads are rarely purely CPU-bound, memory-bound, or I/O-bound. Bottlenecks shift under load. A service at low request rates might be I/O-bound, spending most time waiting for database queries. As request rates increase, more data gets cached in memory, reducing I/O wait — but now the CPU is doing more work deserializing and processing cached results. Push further, and the growing number of in-flight requests inflates memory usage until the process approaches its memory limit. Garbage collection kicks in more frequently (a CPU cost triggered by memory pressure), stealing cycles from request processing and reintroducing CPU as the bottleneck.

This dynamic shifting is why static resource allocation based on a single load test at a single traffic level is unreliable. The resource profile of a workload at 30% capacity is often qualitatively different from its profile at 85% capacity.

## Where Resource Models Break in Practice

**The overcommitment trap.** Orchestrators allow you to request fewer resources than the node actually has — this is overcommitment, and it's how you get utilization above 50%. But overcommitment works only when not all workloads peak simultaneously. If they do, CPU-bound workloads all throttle at once (correlated latency spikes across services), and memory-bound workloads trigger cascading OOM kills. Cluster-level resource utilization metrics look healthy right up until this correlated peak, which is why per-pod and per-container metrics are essential.

**Confusing limits with right-sizing.** Setting a CPU limit of 2 cores does not mean the workload *needs* 2 cores. It means it is *allowed* 2 cores. Without profiling under realistic load, limits are guesses. The common failure pattern is setting limits generously during initial deployment ("give it plenty of room"), never revisiting them, and then paying 3x in compute costs because every instance of the service reserves resources it never uses. On the other end, setting limits too tight based on average usage rather than peak usage produces intermittent failures that are difficult to reproduce in testing because test environments rarely replicate production traffic patterns.

**Ignoring I/O in capacity planning.** Most resource discussions focus exclusively on CPU and memory because those are the resources container orchestrators expose as first-class scheduling constraints. I/O is often unmanaged — there are no default request/limit fields for disk IOPS or network bandwidth in a standard pod spec. This does not mean I/O contention does not exist. It means it is invisible to the scheduler. Two pods on the same node competing for the same underlying disk can starve each other in ways that the orchestrator's resource model cannot detect or prevent.

**The GC death spiral.** In garbage-collected languages (Java, Go, C#), memory pressure triggers garbage collection, which consumes CPU. If the container has tight CPU limits, GC pauses become longer because the collector is throttled. Longer pauses mean more objects accumulate, increasing memory pressure further. This feedback loop between memory and CPU constraints produces symptoms (high latency, eventual OOM kill) that are nearly impossible to diagnose if you are looking at each resource in isolation.

## The Model to Carry Forward

Every compute workload is bounded by some resource at any given moment. The resource it's bounded by determines how it degrades, how you diagnose it, and how you fix it. CPU contention slows you down. Memory exhaustion kills you. I/O contention blocks you. These are not three flavors of the same problem — they are three different problems with different observability signals, different failure modes, and different remediation strategies.

The mental model is this: before you can right-size a workload, you must first identify which resource is the binding constraint under realistic load. Before you can interpret a performance problem, you must know whether the process is *running and throttled* (CPU), *running and about to be killed* (memory), or *idle and waiting* (I/O). The resource model is not a configuration exercise. It is a diagnostic framework. Every decision you make about instance types, container limits, autoscaling thresholds, and storage tiers is downstream of this understanding.

## Key Takeaways

- **CPU is compressible; memory is not.** CPU contention causes gradual latency degradation through throttling. Memory contention causes hard failures through OOM kills. Your tolerance for tight limits should reflect this asymmetry.
- **CPU throttling is invisible unless you monitor it explicitly.** CFS bandwidth control can pause your container's threads even when the host CPU is idle, and the only evidence is in cgroup-level throttling counters that most default dashboards do not surface.
- **Memory limits must account for total process memory, not just application-level allocation.** JVM off-heap memory, thread stacks, native libraries, and memory-mapped files all count against the cgroup limit.
- **Low CPU utilization does not mean the workload has headroom.** An I/O-bound service waiting on disk or network will show idle CPU while being completely saturated. Diagnose with I/O wait time and queue depths, not CPU percentage.
- **Bottlenecks shift under load.** A workload that is I/O-bound at low traffic can become CPU-bound or memory-bound at high traffic. Static resource allocation based on a single traffic level will be wrong at other levels.
- **Container orchestrators do not manage I/O contention by default.** Disk IOPS and network bandwidth are not first-class scheduling constraints in most platforms, which means I/O-bound workloads can suffer noisy-neighbor effects the scheduler cannot see or prevent.
- **The GC death spiral is a cross-resource failure mode.** Memory pressure increases garbage collection, which consumes CPU; CPU throttling slows garbage collection, which increases memory pressure. Diagnosing this requires looking at CPU and memory together.
- **Resource configuration is not a one-time decision.** Traffic patterns change, code changes, and dependency performance changes. Resource profiles must be observed continuously, not set at deploy time and forgotten.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

A lot of production performance work goes wrong because engineers talk about “resources” as if CPU, memory, and I/O are interchangeable knobs. They are not. When you run out of CPU, your service usually gets slower. When you run out of memory, something gets killed. When you are blocked on I/O, the CPU may look mostly idle even though the system is already saturated. If you do not distinguish those cases, you end up applying the wrong fix: adding CPU to a service that is waiting on the network, tightening memory limits until pods crash-loop, or chasing “high latency” without noticing the real cause is CPU throttling.

This matters because modern infrastructure makes it easy to set numbers without understanding mechanics. A Kubernetes request or limit looks like a harmless config field, but those numbers directly shape scheduler behavior, kernel enforcement, and failure modes. The result is a common pattern: systems look fine under average load, then fail under bursts in ways that feel mysterious only because the underlying resource model was never made explicit.

The practical cost is real: tail latency spikes with no errors, OOM kills that wipe in-flight work, noisy-neighbor effects on shared disks, and expensive overprovisioning because nobody knows which constraint is actually binding. If you can tell whether a process is running but starved, occupying memory dangerously, or blocked on an external dependency, debugging and capacity planning become much more concrete.

## What You Need To Know First

**1. The operating system scheduler**  
The OS cannot run every runnable process at once on a finite number of CPU cores, so it takes turns. The scheduler decides who gets CPU time and for how long. That means “having CPU” really means “being allowed to run now.” If many processes want CPU at once, some wait.

**2. Containers and cgroups**  
A container is not a separate machine; it is a process isolated and constrained by kernel features. Cgroups are the mechanism Linux uses to track and limit a group of processes. CPU limits, memory limits, and the counters that show throttling or memory usage are enforced at this level.

**3. Requests vs limits in orchestrators**  
A request is mainly a scheduling hint: “place me on a node that can reasonably fit this.” A limit is an enforcement boundary: “do not let me go past this.” Those are different jobs. Confusing them leads to bad mental models, especially when a workload can burst above its request but is hard-stopped at its limit.

**4. Throughput, latency, and saturation**  
Throughput is how much work gets done per unit time. Latency is how long one unit of work takes. Saturation means a resource is fully occupied, so extra work starts queueing or failing. A system can have acceptable average latency while its p99 gets terrible, which often happens when a resource is near saturation and bursts push requests into queues or throttling windows.

## The Key Ideas, Connected

**1. CPU, memory, and I/O are different constraints with different behaviors when they get tight.**  
The article’s core point is that these are not three versions of the same shortage. They produce different symptoms because the underlying mechanics are different. CPU is about time on a processor, memory is about finite space in RAM, and I/O is about waiting for something outside the CPU to deliver data. Once you accept that the resource types behave differently, it follows that “resource tuning” cannot be one generic activity. You need a separate mental model for each one.

**2. CPU is a time-shared resource, so contention usually means slowdown rather than immediate failure.**  
A process that wants CPU can often just wait a little longer for its turn. The work is still possible; it is delayed. That is why CPU is called compressible in the article: when demand exceeds supply, execution stretches out in time instead of crashing on the spot. This explains why CPU problems often show up first as increased latency, especially at the tail, not as explicit application errors.  
Because CPU is time-shared, the next question becomes: who decides how that time is divided?

**3. On Linux, CPU sharing and limiting happen through scheduler weights and quotas, and those are different mechanisms.**  
A CPU request affects relative share during contention: if two containers compete, the one with the larger request gets more scheduling weight. But a CPU limit is not just a lower weight; it is a quota enforced over a time window. That distinction matters. A request says “my fair share when crowded.” A limit says “you may not exceed this ceiling, even if spare CPU exists.”  
Once you see that, the article’s warning about throttling makes sense: the scheduler can pause your workload because it used up its quota for the current period, not because the machine is globally out of CPU.

**4. CPU throttling creates latency spikes because runnable work is forcibly paused mid-burst.**  
This is the mechanism behind the “mysterious” p99 jump. If several requests arrive together, the container may burn through its CPU quota quickly. After that, its threads are paused until the next quota period begins. The important detail is that these requests are not blocked on a database or sleeping by choice—they are ready to run but forbidden from doing so. That is why the service appears healthy at the application level while users experience slowness.  
This leads to an important diagnostic distinction: if the process has work to do and latency rises while CPU is near its limit or throttling counters rise, the bottleneck is CPU.

**5. Memory is different because it is not time-shared in the same forgiving way; it is finite occupancy.**  
RAM is not something your process can usually “use half as fast.” If the bytes you need are not available, the system must reclaim space somehow. That is why memory is called incompressible in the article. The kernel may reclaim cache, swap, or ultimately kill a process, but there is no equivalent of “just wait your turn” that preserves behavior gracefully.  
This is why the next idea is a cliff: once memory accounting reaches the enforced boundary, the system has to take destructive action.

**6. Memory limits fail by hard enforcement, typically via OOM kills, not gradual degradation.**  
A memory limit on a container is an absolute boundary. If the cgroup exceeds it, the kernel selects a victim and kills it. From the application’s point of view, this is abrupt. In-flight requests vanish, warm state is lost, and the service may restart repeatedly. That is a totally different failure shape than CPU contention.  
The mechanism also explains why engineers get surprised when they size memory from only one application-visible pool, like the JVM heap. The kernel accounts total memory use in the cgroup, not just the heap you configured. So thread stacks, native allocations, runtime metadata, page cache effects, and other off-heap memory still count. If your mental model is “heap size equals memory usage,” you will set limits too low and create predictable OOM events.

**7. The asymmetry between CPU and memory means you should treat their limits differently.**  
Because CPU pressure usually degrades and memory pressure often kills, the cost of being wrong is not symmetric. Tight CPU limits may be acceptable if your system can tolerate latency degradation during spikes. Tight memory limits are riskier because they turn estimation error into immediate availability incidents.  
Once that asymmetry is clear, it becomes easier to see why “right-sizing” is not just minimizing unused capacity. The acceptable safety margin depends on the failure mode of the resource.

**8. I/O-bound systems are constrained not by doing work on the CPU, but by waiting for external operations to complete.**  
This is the third major category. A thread can be alive, requests can be piling up, and users can be waiting—while CPU usage stays low. That happens because the bottleneck is outside the processor: disk, network, downstream services, sockets, or storage devices. In this state the process is often blocked, not runnable.  
This matters because low CPU is easy to misread as spare capacity. But if all workers are waiting on slow I/O, adding more CPU changes nothing. The system is saturated in a place your usual CPU dashboard does not reveal.

**9. I/O saturation often hides in queues, latencies, and wait times rather than obvious CPU or memory metrics.**  
If a disk can only serve so many IOPS, or a downstream service has a 50ms p99, requests accumulate in queues. The process spends wall-clock time waiting for reads, writes, or responses. That is why the article emphasizes iowait, disk latency, throughput, IOPS, and socket or network queue depth. These metrics expose where time is actually going.  
This also explains the distinction between throughput-bound and latency-bound disk workloads: large sequential transfers stress bandwidth, while many tiny random operations stress operation count. Same broad resource category, different inner mechanism.

**10. Real systems shift bottlenecks as load changes, so a single resource classification is often temporary.**  
A service might start out I/O-bound because every request hits a database. With more traffic, cache hit rates improve, reducing I/O wait. Now the CPU spends more time parsing, serializing, and executing application logic, so CPU becomes the bottleneck. Push further and the number of in-flight requests or cached objects raises memory pressure, which introduces GC costs or OOM risk.  
This is why static sizing from one benchmark is unreliable: the system’s dominant constraint can move as the workload shape changes. The bottleneck is not a permanent label on the service; it is a state produced by current demand and current architecture.

**11. Cross-resource interactions create failure modes that are invisible if you inspect each resource in isolation.**  
The GC death spiral is the clearest example. Memory pressure causes more garbage collection. Garbage collection uses CPU. Tight CPU limits throttle the collector, so memory is freed more slowly. That increases memory pressure further, which causes more GC. The visible symptom might be latency first and OOM later, but the mechanism is a loop between memory and CPU.  
This idea generalizes: one constrained resource can transform demand on another. That means diagnosis has to trace causal links, not just spot a high metric.

**12. The practical model is: identify the binding resource under realistic load, then reason from its mechanics to its failure mode and fix.**  
That is the article’s endpoint. Before choosing instance sizes, setting limits, or interpreting latency spikes, ask: is the process runnable and waiting for CPU, occupying dangerous amounts of memory, or blocked on I/O? The answer tells you what metrics matter, what failure to expect, and what interventions are plausible.  
Without that model, engineers tune configs by folklore. With it, resource settings become hypotheses about system behavior that can be tested against the right signals.

## Handles and Anchors

**1. CPU, memory, and I/O fail like traffic, storage, and delivery.**  
CPU is like lane access on a highway: if too many cars want in, traffic slows.  
Memory is like parking spaces: when they are full, incoming cars cannot just “go slower”; something must be turned away or removed.  
I/O is like waiting for shipments: your workers may be standing around ready, but work cannot continue until the truck arrives.

**2. Ask: “Is the process busy, full, or waiting?”**  
Busy = CPU-bound.  
Full = memory-bound.  
Waiting = I/O-bound.  
That question is simple enough to use in live debugging and strong enough to steer you toward the right metrics.

**3. One-sentence tension:**  
“CPU pressure stretches time, memory pressure hits a wall, and I/O pressure hides in queues.”

## What This Changes When You Build

**1. An engineer who understands this will set CPU limits more cautiously because a CPU limit is not just a budget, it is a throttle.**  
The unaware engineer sees `limit: 500m` as “half a core should be enough on average.” In reality, under bursty concurrency that limit can create artificial pauses that blow up p99 latency even if average CPU usage looks fine. The aware engineer checks throttling metrics, tests burst behavior, and may avoid strict CPU limits on latency-sensitive services.

**2. An engineer who understands this will size memory from total process footprint, not just application-configured heap or cache size, because the kernel kills based on cgroup usage, not language-level abstractions.**  
The unaware engineer says, “Java heap is 512MB, so a 600MB limit is safe.” The consequence is a restart loop when metaspace, thread stacks, native buffers, and GC overhead push real usage above the limit. The aware engineer measures RSS and runtime-specific overhead, leaves headroom, and treats memory limits as safety-critical boundaries.

**3. An engineer who understands this will not treat low CPU utilization as proof of headroom because blocked systems can be saturated while mostly idle on the CPU.**  
The unaware engineer sees 15% CPU and reaches for a bigger instance only when traffic grows. Meanwhile request latency keeps rising because threads are stuck on disk or downstream calls. The aware engineer looks at dependency latency, queue depth, I/O wait, connection pools, and storage characteristics before deciding where capacity is actually constrained.

**4. An engineer who understands this will test systems across multiple load levels because the bottleneck can move as traffic changes.**  
The unaware engineer runs one load test at a moderate rate, declares the service “CPU-light,” and sizes it accordingly. In production, higher concurrency changes cache behavior, memory footprint, and GC frequency, and the failure mode looks unrelated to the original test. The aware engineer expects phase changes: low-load bottlenecks and high-load bottlenecks may be different problems.

**5. An engineer who understands this will treat right-sizing as ongoing observation rather than one-time configuration because resource behavior depends on workload shape, code changes, and neighbor contention.**  
The unaware engineer inherits old requests and limits forever, paying for idle reservation or suffering intermittent failures during peaks. The aware engineer revisits resource settings with real production telemetry, separates scheduling needs from enforcement needs, and recognizes that shared-node I/O contention may require architectural or placement changes, not just new CPU and memory numbers.

---

</details>
