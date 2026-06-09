## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers interact with container orchestration as a deployment target. You write a manifest, apply it, and pods appear. When things work, the orchestrator feels like a black box you don't need to open. When things break — a pod stuck in Pending for ten minutes, a service unreachable after a node failure, containers getting OOM-killed on a node that appeared to have free memory — the black box becomes the problem. The gap between "I use Kubernetes" and "I understand what the scheduler is actually doing" is where most operational surprises live.

The Level 1 post established that orchestration manages scheduling, scaling, networking, health checking, and rollout management. This post is about the machinery underneath those words. Specifically: how does an orchestrator decide where to place a workload, what information drives that decision, what happens when reality diverges from intent, and where do the mechanics create problems that aren't obvious from the API surface?

## The Problem the Scheduler Solves

Running a container on a single host is a solved problem. You pull an image, start a process, map some ports. The difficulty begins the moment you have more workloads than one machine can handle, or the moment you need any workload to survive the failure of the machine it's running on.

At that point, you have a **cluster** — a pool of machines (nodes) available to run workloads. And you have a question that sounds simple but is computationally hard: given N workloads with different resource needs, constraints, and priorities, and M nodes with different capacities and current utilization, which workload goes where?

This is a variant of the **bin packing problem**, which is NP-hard in the general case. You can't compute the globally optimal placement in reasonable time for any non-trivial cluster. Every orchestrator uses heuristics — good-enough solutions computed fast — rather than optimal ones computed slowly. Understanding that the scheduler is making approximations, not guarantees, is the first conceptual shift that matters.

## The Reconciliation Loop

Before diving into scheduling mechanics, you need to understand the execution model that drives them. Orchestrators like Kubernetes don't operate as a sequence of imperative commands. They operate as **control loops**.

You declare a desired state: "there should be three replicas of service-A, each requesting 512Mi of memory and 250m of CPU." This declaration is written to a central data store (in Kubernetes, etcd). A set of independent controllers continuously watch for discrepancies between desired state and observed state. When a discrepancy exists, a controller takes action to close the gap.

This is not one loop. It's many. The **ReplicaSet controller** notices that three replicas are desired but only two pods exist, so it creates a third pod object. The **scheduler** notices that a pod exists with no node assignment, so it selects a node and binds the pod. The **kubelet** on that node notices a pod bound to it that isn't running, so it pulls the image and starts the container. Each controller is responsible for one narrow transition, and they operate independently and asynchronously.

This architecture has a critical implication: there is no single moment where "deployment happens." Convergence toward desired state is eventual. A pod can exist as an API object for seconds before the scheduler assigns it to a node, and more seconds pass before the kubelet starts the container, and more before health checks pass and the pod starts receiving traffic. When someone says a deployment "takes too long," the latency lives in the gaps between these independent loops, not in any single operation.

## How Scheduling Decisions Are Made

When an unscheduled pod appears, the scheduler runs a two-phase process: **filtering**, then **scoring**.

**Filtering** eliminates nodes that cannot run the pod. The reasons a node gets filtered out are concrete: it doesn't have enough allocatable CPU or memory to satisfy the pod's resource requests; it has a **taint** that the pod doesn't tolerate; it doesn't match a required **node selector** or **node affinity** rule; it would violate a **pod anti-affinity** constraint (e.g., "don't place two replicas of this service on the same node"). After filtering, you have a set of feasible nodes. If that set is empty, the pod stays in Pending — a state that means "the scheduler tried and failed to find a valid placement," not "the scheduler hasn't gotten around to it."

**Scoring** ranks the feasible nodes. Each node gets a score based on multiple weighted factors: how much the pod's resource request would balance utilization across the cluster (the **LeastRequestedPriority** or **MostRequestedPriority** strategies, depending on configuration), whether the node already has the container image cached (avoiding a pull), whether the pod has a **preferred** (soft) affinity for that node, and others. The highest-scoring node wins.

The critical detail: scheduling decisions are based on **requests**, not on actual utilization. If a node has 4 GiB of allocatable memory and pods with requests totaling 3.5 GiB are already scheduled there, the scheduler sees 512 MiB available — regardless of whether those pods are actually using 200 MiB or 3.5 GiB. This is the single most important mechanic to understand about resource management in an orchestrated cluster, and it's the one most commonly misunderstood.

## Requests, Limits, and the Overcommitment Trap

A **resource request** is a scheduling guarantee. It tells the scheduler: "this pod needs at least this much CPU and memory to be placed." The scheduler uses requests to make bin-packing decisions.

A **resource limit** is a runtime ceiling. It tells the container runtime: "if this pod tries to use more than this, throttle it (CPU) or kill it (memory)."

These are independent values. You can set a request of 256Mi of memory and a limit of 1Gi. The scheduler will place the pod on any node with 256Mi available in its accounting, but the pod can burst up to 1Gi at runtime if the memory is physically free on the node.

This gap between requests and limits is where **overcommitment** lives. If every pod on a node has a request of 256Mi but a limit of 1Gi, and every pod simultaneously bursts, the node runs out of physical memory. The kernel's OOM killer starts terminating processes. From the scheduler's perspective, the node had enough capacity. From the kernel's perspective, it didn't. The result: pods get killed on nodes that the scheduler thought were fine.

The practical failure mode looks like this: a team sets low requests to make scheduling easy (pods land quickly, bin packing is efficient) and high limits "just in case." The cluster runs well under normal load. During a traffic spike, multiple pods burst simultaneously, the node runs out of memory, and the OOM killer takes out pods semi-randomly — often including the ones handling the traffic spike. The operator sees pods restarting across the cluster and has no obvious explanation because the scheduler's resource accounting looks healthy.

The opposite failure is equally common: setting requests equal to limits (no overcommitment) on workloads that use a fraction of their requested resources. Nodes appear full to the scheduler while running at 15% actual utilization. The cluster is stable, but you're paying for four times the infrastructure you need.

## Service Discovery in a Dynamic Environment

On a single host, containers find each other by port mapping or a shared Docker network. In a cluster, the pod running your API server might be on node-7 right now and on node-12 after a reschedule. Its IP address changes every time it's re-created. Hard-coding addresses is impossible.

Orchestrators solve this with an abstraction layer between "the set of pods that implement a service" and "the network address that clients use to reach it." In Kubernetes, this is the **Service** object. A Service provides a stable virtual IP (the **ClusterIP**) and a DNS name. Behind that stable address, the Service maintains a dynamically updated list of pod IPs (**endpoints**) that match a label selector.

When a pod is created and passes its readiness checks, its IP is added to the endpoint list. When a pod is terminated or fails its readiness check, its IP is removed. Clients connect to the stable Service address and traffic is distributed across the current set of healthy pods, typically via iptables rules or IPVS on every node, updated by the **kube-proxy** component.

The non-obvious failure here is the gap between a pod starting and becoming ready. If your readiness probe is misconfigured — either too aggressive (passing before the app can handle traffic) or too slow (delaying for minutes) — the endpoint list doesn't reflect reality. Traffic arrives at pods that can't handle it, or healthy pods sit idle while the service appears degraded.

## Self-Healing: What Actually Happens During Failure

"The orchestrator restarts failed containers" is the surface description. The actual sequence during a node failure reveals more:

The kubelet on every node sends heartbeats to the control plane. When heartbeats from a node stop arriving, the **node controller** waits for a configurable timeout (the default in Kubernetes is 40 seconds of missed heartbeats before marking the node as `Unknown`, then another 5 minutes — the **pod-eviction-timeout** — before evicting pods). Only after this timeout does the control plane delete the pods assigned to the failed node, at which point the ReplicaSet controller notices replicas are missing and creates new pod objects, which the scheduler then places on surviving nodes.

The total elapsed time from node failure to replacement pods serving traffic can easily be six to seven minutes with default settings. During that window, the pods on the failed node are gone but haven't been replaced. If you had three replicas spread across three nodes and one node dies, you're running at two-thirds capacity for several minutes. If you had three replicas all on the same node — because you didn't configure anti-affinity rules and the scheduler's scoring happened to favor that placement — you're running at zero capacity.

This is why **pod disruption budgets**, **topology spread constraints**, and **anti-affinity rules** exist. They aren't advanced features for edge cases. They're the mechanisms that make self-healing actually work at the level most people assume it already works at by default.

## The Tradeoffs That Bite

The scheduler's design optimizes for generality — it handles stateless web servers, batch jobs, stateful databases, GPU workloads, and daemon processes through the same machinery. This generality has costs.

**Rescheduling doesn't mean zero-downtime.** Moving a workload from a failed node to a healthy one takes time. For stateless services behind a load balancer, this may be transparent. For a stateful workload with a persistent volume, the volume must be detached from the dead node and reattached to the new one — a process that can take minutes, especially in cloud environments where volume attachment is an API call with its own latency and failure modes.

**The scheduler is not aware of your application's behavior.** It knows about resource requests, labels, taints, and topology. It doesn't know that your service has a three-minute warmup period, or that two of your services compete for the same shared lock, or that scheduling a batch job next to a latency-sensitive service will cause cache eviction that degrades both. Everything the scheduler doesn't know has to be expressed through its constraint language (affinities, tolerations, topology constraints), or it won't be considered.

**Cluster autoscaling adds another feedback loop.** If no node has capacity for a pending pod, a cluster autoscaler can provision a new node. But provisioning a cloud VM takes one to five minutes. During that time, the pod is Pending, the scheduler is waiting, and the application is under-provisioned. The autoscaler's decision is also based on the same request-based accounting — it responds to scheduling failures, not to actual resource pressure. If your requests are artificially low, the autoscaler won't trigger even as nodes buckle under real load.

## The Mental Model

An orchestrator is a set of independent control loops driving observed state toward declared state. The scheduler is the loop that solves the placement problem, and it does so using a constraint-satisfaction approach: filter nodes that violate hard constraints, score the rest, pick the winner. Every scheduling decision is based on the resource model you declared (requests and limits), not the resources your application actually consumes.

This means the quality of your scheduling outcomes is a direct function of the accuracy of your resource declarations and the specificity of your placement constraints. The orchestrator will faithfully execute a bad declaration — placing all replicas on one node, overcommitting memory, or leaving pods Pending because requests don't match reality. The machinery is precise. The inputs are your responsibility.

When you look at a cluster and see pods in unexpected states — Pending, OOMKilled, CrashLoopBackOff on a node that looks underutilized — don't start with the application. Start with the scheduling model. Ask: what did the scheduler see when it made this decision? What did the resource accounting say? What constraints were in play? That's the reasoning path the mechanics support, and it resolves the majority of operational surprises.

## Key Takeaways

- **The scheduler solves a bin-packing problem using heuristics, not optimal solutions.** Placement decisions are good-enough approximations made quickly, which means edge cases in packing efficiency are expected, not bugs.

- **Scheduling decisions are based on resource requests, not actual utilization.** A node that appears idle to monitoring tools can appear full to the scheduler, and vice versa. Misaligned requests are the root cause of most scheduling surprises.

- **Requests and limits serve different purposes and are set independently.** Requests are for scheduling (where does the pod land). Limits are for runtime enforcement (what happens when the pod exceeds expectations). Setting them incorrectly in either direction — too low or too high — creates real operational problems.

- **Self-healing is not instant.** Default timeouts mean that recovery from a node failure takes minutes, not seconds. The gap between failure and recovery must be accounted for in your availability design through replica counts, anti-affinity rules, and pod disruption budgets.

- **Service discovery depends on the accuracy of readiness probes.** A stable Service IP is only useful if the endpoint list behind it reflects which pods can actually handle traffic. Misconfigured readiness probes are one of the most common causes of intermittent service errors in orchestrated environments.

- **Convergence toward desired state is eventual and multi-step.** No single controller handles a deployment end-to-end. Multiple independent loops act in sequence, and the total time from declaration to running workload is the sum of their individual latencies.

- **The scheduler can only optimize for what it's told.** Application-level concerns — warmup time, cache locality, resource contention patterns — must be expressed as scheduling constraints (affinities, tolerations, topology spread) or they will be invisible to placement decisions.

- **Overcommitment is a deliberate tradeoff, not a default you can ignore.** The gap between requests and limits determines how much risk you're carrying. Clusters that look efficient on paper can be fragile under load if overcommitment isn't managed intentionally.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Kubernetes often feels simple right up until the moment it doesn’t. You declare a pod, apply YAML, and something starts running somewhere. That surface experience hides the real mechanics: placement is approximate, recovery is delayed, networking depends on health signals, and resource accounting is based on what you declared, not what is physically happening right now. When those mechanics stay invisible, operational failures look random.

That is why engineers get surprised by things like pods stuck in `Pending` even though nodes “look empty,” services failing after a node dies even though replicas exist, or pods getting OOM-killed on nodes with apparently low average memory usage. These are not weird edge cases. They are normal outcomes of how the orchestrator works. If you do not understand what the scheduler sees, what each controller is responsible for, and where the delays live, you end up debugging symptoms while missing the actual cause.

The practical cost is real: underused clusters that are expensive, overloaded clusters that are fragile, rollout delays that are blamed on the app, and self-healing assumptions that collapse during failures. This topic matters because the orchestrator is not magic infrastructure around your system. It is part of your system.

---

## What You Need To Know First

**1. Pods, nodes, and clusters**  
A **pod** is the unit Kubernetes schedules and runs. A **node** is a machine that can host pods. A **cluster** is the set of nodes plus the control plane coordinating them. If you hold that in your head, then “scheduling” just means deciding which node should run a given pod.

**2. Desired state vs observed state**  
Kubernetes is built around the idea that you declare what you want — for example, “three replicas should exist” — and the system keeps checking reality to see whether that is true. If reality differs, some component tries to push it back toward what was declared. This matters because Kubernetes is not executing one command from start to finish; it is repeatedly correcting drift.

**3. Resource requests and limits**  
A **request** is what a pod asks the scheduler to reserve for placement. A **limit** is the maximum the runtime will let the container consume before throttling or killing it. The important minimum understanding is: requests affect where the pod can land; limits affect what happens after it starts.

**4. Readiness vs process running**  
A container process being started does not mean it is ready to serve traffic. Kubernetes uses **readiness probes** to decide whether a pod should receive requests through a Service. This matters because networking in Kubernetes is built around “which pods are currently considered ready,” not merely “which pods exist.”

---

## The Key Ideas, Connected

**1. Kubernetes works as a set of control loops, not as one deployment command.**  
What this means is that no single component takes your deployment from YAML all the way to healthy traffic-serving containers in one continuous action. Instead, one controller notices missing replicas and creates pod objects, the scheduler notices unscheduled pods and assigns nodes, and the kubelet on each node notices assigned pods and starts containers. Each step is separate, owned by a different loop, and happens asynchronously.

That matters because it explains why deployment and recovery are inherently incremental and delayed. If the system is made of independent loops, then latency appears in the handoff between loops. That naturally leads to the next idea: the scheduler is only one stage in convergence, but it is the stage that decides placement.

**2. The scheduler’s job is to choose a node for an unscheduled pod under constraints.**  
This sounds straightforward, but it is hard because the scheduler is choosing from many nodes with different capacities, workloads, and rules. It is solving a placement problem: which node can run this pod without violating declared constraints, and which of the valid choices is best enough?

Because that problem is computationally hard in the general case, the scheduler does not search for the perfect placement. It uses heuristics. Once you accept that, the next idea follows: scheduling is a fast approximation process, not a global optimization engine.

**3. Scheduling is heuristic bin-packing, so it aims for good-enough decisions made quickly.**  
The scheduler is effectively packing workloads into machines, like fitting differently shaped items into bins. The “best” arrangement across a whole cluster is too expensive to compute exactly, so Kubernetes uses practical rules to make a decent choice quickly.

That has an important consequence: strange-looking placements are not always bugs. Sometimes they are just the output of local heuristics operating under the inputs you provided. If the scheduler is making approximate decisions, then what information it uses becomes critically important. That leads directly to how it decides.

**4. The scheduler decides in two steps: filter out impossible nodes, then score the remaining ones.**  
First, it removes nodes that violate hard constraints: not enough requested CPU or memory available, missing required labels, conflicting anti-affinity, taints the pod does not tolerate, and so on. If every node gets filtered out, the pod remains `Pending`. In that case, `Pending` means “no valid placement exists under current rules,” not “Kubernetes is slow.”

Then the scheduler scores the feasible nodes. It prefers some placements over others based on weighted factors such as balance, preferences, and image locality. This explains why pods can land in ways that are valid but not what you intuitively expected: many placements are legal, and the scheduler chooses the top-scoring one according to its rules.

Once you understand filtering and scoring, the next question is: what data are these decisions based on? That is where many misunderstandings begin.

**5. The scheduler reasons from declared resource requests, not from live actual usage.**  
This is the article’s central mechanic. If pods on a node have requested 3.5 GiB out of 4 GiB allocatable memory, the scheduler sees only 0.5 GiB left, even if the processes are currently using much less. The scheduler is not making placement decisions from your dashboards showing low real-time utilization; it is making decisions from the reservation model you declared.

This explains a common surprise: a node can appear mostly idle in monitoring and still be unavailable for new scheduling. The reverse can also happen: a node can look schedulable because requests are low while being dangerous in reality because actual consumption can spike. That naturally leads to the distinction between requests and limits.

**6. Requests and limits describe two different phases of the pod’s life: placement and runtime.**  
A request is for admission to a node. A limit is for enforcement once the pod is running. If you request 256Mi and limit at 1Gi, the scheduler only reserves 256Mi in its accounting, but the running container may consume much more if memory is physically available.

That separation is powerful because it allows overcommitment, but it is also risky. The scheduler can honestly think a node is safe based on requests, while the kernel later discovers that real memory demand exceeds physical capacity. That mechanism produces the next failure mode.

**7. Overcommitment is the gap where scheduler logic and runtime reality can diverge.**  
If many pods ask for small requests but are allowed large limits, the cluster can be packed tightly. This improves utilization in calm conditions. But if several pods burst together, the node can run out of physical memory. At that point, the scheduler is no longer the active decider; the Linux kernel is, and it uses the OOM killer to terminate processes.

So when pods get OOM-killed on a node the scheduler considered healthy, that is not contradictory. The scheduler answered, “Can this pod be placed based on declared minimum needs?” The kernel later answered, “Can all these processes fit in actual memory right now?” Those are different questions. Once you see that mismatch, you can understand why “the scheduler said yes” does not guarantee runtime safety.

With placement understood, the next issue is how clients find pods in a system where placements can change constantly.

**8. Services exist because pod identities are unstable, but the traffic path depends on readiness.**  
Pods can move, be recreated, or get new IPs, so clients cannot safely connect to them directly by fixed address. Kubernetes solves this with a Service: a stable virtual address that points to whichever pod IPs currently match the selector and are considered ready.

The key mechanic is that the endpoint list behind the Service changes as pods enter or leave readiness. So service discovery is not just naming; it is health-gated routing. That is why readiness probes matter so much. If readiness says “healthy” too early, traffic reaches pods that cannot really handle it. If readiness says “not ready” for too long, healthy capacity stays unused. Understanding Services therefore requires understanding that traffic eligibility is controlled by readiness state, not simply by process existence.

That same “eventual convergence” model also explains self-healing during failure.

**9. Self-healing is real, but it is delayed because failure detection and replacement are separate steps.**  
When a node dies, Kubernetes does not instantly know it. The control plane waits for missed heartbeats, marks the node unhealthy, then after another timeout evicts the pods from that node. Only then do higher-level controllers create replacement pods, which then still need to be scheduled and started.

This means “Kubernetes reschedules failed workloads” is true but incomplete. The full truth is: Kubernetes notices the failure after a delay, then begins replacement through the same controller chain as any other reconciliation event. That is why node failure recovery often takes minutes. If your availability model assumes immediate replacement, your design is wrong for the actual machinery.

And that leads to the final idea: if the system only knows what you declare, then reliability depends on how well you encode your real needs.

**10. The orchestrator can only optimize for the constraints and signals you give it.**  
The scheduler does not know your app warms up for three minutes, that replicas should never share a node, or that one workload interferes with another unless you express those facts through requests, affinities, topology spread, probes, budgets, and similar mechanisms. The orchestrator is precise about declared state, not about implied intent.

So the final mental model is this: Kubernetes is a set of independent loops reconciling declared state toward reality, and the scheduler is one of those loops making approximate placement decisions from your declarations. If the declarations are inaccurate, incomplete, or overly simplistic, the system will still behave correctly relative to them — and operationally badly relative to what you actually wanted.

---

## Handles and Anchors

**1. Think of the scheduler as booking based on reservation forms, not on people’s actual behavior.**  
A hotel assigns rooms from reservations, not by predicting who will spend most of the day outside. If every guest reserves a huge suite, the hotel looks full even if many rooms are mostly empty. If every guest reserves a tiny room but secretly brings five extra people, the building becomes overloaded at night. Kubernetes works similarly with requests and limits.

**2. “Kubernetes does not do deployment; it does convergence.”**  
That sentence captures a lot. It reminds you there is no single action called “deploy” inside the system. There are many controllers each moving the world one step closer to the declared state. Delays and odd intermediate states make more sense once you think in convergence instead of command execution.

**3. Ask this question when something looks wrong: “What did the scheduler believe at decision time?”**  
Not “what does my dashboard show now?” and not “what did I mean?” but “what inputs did the scheduler actually have?” That question cuts through many mysteries: `Pending` pods, bad placement, missed autoscaling, and OOMs on apparently healthy nodes.

---

## What This Changes When You Build

**1. An engineer who understands this will size resource requests from observed behavior, not from guesswork, because requests control placement and autoscaling decisions.**  
The unaware engineer often sets requests very low to make scheduling easy or copies arbitrary defaults from another service. The consequence is fragile overcommitment, missing autoscaler reactions, and runtime failures that appear unrelated to scheduling. The informed engineer treats requests as cluster-shaping inputs and revisits them using actual usage distributions.

**2. An engineer who understands this will separate “can start” from “can serve” when configuring readiness, because Services route only to pods considered ready.**  
The default mistake is to use a shallow readiness check that passes as soon as the process is alive, or to make the check so conservative that usable pods stay out of rotation too long. The consequence is intermittent 5xxs during startup or unnecessary capacity loss during deploys. The informed engineer designs readiness around the real moment the application can safely accept production traffic.

**3. An engineer who understands this will design replica placement explicitly, because self-healing is slow and default scheduling does not guarantee fault isolation.**  
The unaware engineer assumes that “three replicas” implies resilience. It does not if all three can land on one node or one zone. The consequence is that a single infrastructure failure can remove all capacity at once, and replacement may take minutes. The informed engineer uses anti-affinity, topology spread constraints, and disruption budgets so replica count translates into actual availability.

**4. An engineer who understands this will debug `Pending`, `OOMKilled`, and post-failure outages by inspecting scheduling inputs and controller timing, because these states are produced by specific mechanisms.**  
The unaware engineer starts at the application logs and treats the orchestrator as an opaque backdrop. That often leads to long debugging sessions focused on the wrong layer. The informed engineer checks events, requests, node allocatable capacity, affinity rules, taints, readiness state, and failure-detection timeouts first, because those are the mechanics most likely to explain the symptom.

**5. An engineer who understands this will treat overcommitment as an explicit risk decision, because efficiency and safety are being traded against each other.**  
The unaware engineer inherits whatever ratio emerges from ad hoc requests and limits. The consequence is either expensive underutilization or clusters that fail under burst load. The informed engineer decides where bursting is acceptable, where requests should match limits, and which workloads are allowed to compete for spare capacity.

---

</details>
