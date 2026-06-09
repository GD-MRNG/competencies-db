## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers work with containers daily and understand them as "lightweight, isolated environments for running applications." That understanding is sufficient for pulling images and writing Dockerfiles, but it breaks down the moment you need to answer harder questions: Why can a process inside a container sometimes see the host's process tree? Why does a container with no memory limit set consume all available host memory and get killed? Why is a container escape a fundamentally different class of vulnerability than a VM escape? The answers live in the actual kernel mechanics underneath the container abstraction — mechanics that most practitioners have never had reason to examine. Without them, you're operating containers on faith rather than understanding, and faith is a poor foundation for security and reliability decisions.

## A Container Is a Process, Not a Machine

The single most important conceptual shift is this: a container is not a lightweight virtual machine. A VM runs a full guest operating system on emulated or virtualized hardware, with its own kernel. A container is a **regular Linux process** (or group of processes) that the host kernel has been told to lie to.

When you run `docker run nginx`, the Docker daemon asks the kernel to start a process with specific isolation constraints applied. The nginx process runs directly on the host kernel, uses the host's CPU scheduler, and makes syscalls to the same kernel as every other process on the machine. There is no guest kernel. There is no hypervisor. The "isolation" comes from the kernel selectively restricting what the process can see and how much it can consume.

Two kernel subsystems do the heavy lifting: **namespaces** control visibility (what the process can see), and **cgroups** control resources (what the process can consume). Everything else — union filesystems, capability dropping, seccomp filters — is layered on top of these two primitives.

## Namespaces: The Visibility Boundary

A **namespace** wraps a global system resource in an abstraction that makes it appear to the processes inside the namespace that they have their own isolated instance of that resource. The host kernel maintains the real, global state; namespaces provide filtered views of it.

Linux currently implements eight namespace types. The ones doing the most work in container isolation are these:

### PID Namespace

Each container gets its own PID namespace. The first process started inside the container sees itself as PID 1. It and its children see a process table that contains only processes in their namespace. From the host's perspective, these are ordinary processes with ordinary host-level PIDs — the container's PID 1 might be PID 48372 on the host. The kernel maintains a mapping between the two views.

This is why `ps aux` inside a container shows only that container's processes, while the same command on the host shows everything, including all container processes. The isolation is cosmetic from the kernel's perspective, but operationally meaningful: processes in one container cannot send signals to processes in another container by default, because they can't address them.

### Mount Namespace

Each container gets its own view of the filesystem hierarchy. When a container runtime sets up a container, it creates a new mount namespace, mounts the container image's filesystem as the root (`/`), and mounts specific paths like `/proc` and `/dev` with appropriate filtering. The container process sees its image's filesystem as the entire world.

This is where **union filesystems** (OverlayFS being the most common) enter the picture. A container image is composed of stacked read-only layers. The runtime adds a thin writable layer on top. When a process in the container reads a file, OverlayFS searches downward through the layers until it finds the file. When a process writes, the write goes to the top writable layer using a **copy-on-write** strategy — the original layer is untouched, and a modified copy is placed in the writable layer. This is how multiple containers can share the same base image layers in memory and on disk while each maintaining their own modifications. It's also why container filesystems are ephemeral by default: the writable layer is discarded when the container stops.

### Network Namespace

Each container gets its own network stack: its own interfaces, its own routing table, its own iptables rules, its own port space. This is why two containers can both bind to port 80 without conflict — they each have their own port 80 in their own network namespace.

The container runtime creates a **veth pair** — a virtual ethernet cable with one end inside the container's network namespace and the other end attached to a bridge on the host. Traffic from the container traverses this virtual link to the host bridge, where the host's network stack routes it. This is the machinery behind Docker's default bridge networking, and it's why container-to-container networking has slightly higher latency than host networking — packets cross the veth pair and the bridge, adding a few microseconds of overhead.

### UTS, IPC, and User Namespaces

The **UTS namespace** gives each container its own hostname. The **IPC namespace** isolates System V IPC resources and POSIX message queues, preventing one container from accessing another's shared memory segments. The **user namespace** is the most security-relevant of the three: it allows mapping UID 0 (root) inside the container to an unprivileged UID on the host, so a process that believes it's running as root inside the container has no root privileges if it escapes to the host.

User namespaces are powerful but historically underused. Many container runtimes ran containers as real root on the host for years because user namespace support was immature and introduced compatibility issues with volume mounts and certain syscalls. This is improving, and **rootless containers** — where the entire container runtime runs without host root privileges — are now viable in both Docker and Podman. But the default configuration in many production environments still maps container root to host root, which matters enormously for security.

## Cgroups: The Resource Boundary

If namespaces are about what a process can *see*, **cgroups** (control groups) are about what a process can *use*. Cgroups allow the kernel to allocate, limit, and account for CPU, memory, I/O bandwidth, and other resources on a per-process-group basis.

When a container runtime starts a container, it creates a cgroup for that container's processes and writes resource constraints into the cgroup's control files. These are literal files in a virtual filesystem (typically mounted at `/sys/fs/cgroup`).

### CPU Constraints

CPU limits in cgroups work through the **Completely Fair Scheduler (CFS) bandwidth control**. When you set a container to 0.5 CPU, the runtime translates this into a quota and period: for example, 50ms of CPU time per 100ms period. If the container's processes exhaust their 50ms quota within a period, the kernel **throttles** them — they are descheduled and cannot run until the next period begins.

This throttling is invisible from inside the container. The process doesn't receive a signal or an error. It simply stops getting scheduled. From the process's perspective, the CPU just got very slow. This is why CPU throttling can cause latency spikes that are extremely difficult to diagnose from application-level metrics alone — the application doesn't know it's being throttled, it just sees operations taking longer than expected. Tools like `cat /sys/fs/cgroup/cpu/cpu.stat` (cgroups v1) or the `nr_throttled` and `throttled_time` fields reveal what's actually happening.

### Memory Constraints

Memory limits are enforced hard. When a container's processes collectively exceed the cgroup's memory limit, the kernel invokes the **OOM killer** and terminates a process in the cgroup. There is no graceful degradation, no swap-to-disk by default, no warning. The process is killed with SIGKILL.

This creates a critical operational distinction: a container without a memory limit set can consume all available host memory, potentially starving other containers and system processes. A container with a memory limit set will be killed when it exceeds that limit. Neither failure mode is good, but only the second one is *contained* — the blast radius is limited to the offending container rather than the entire host.

A common operational mistake is setting memory limits equal to memory requests (common in Kubernetes) without understanding that this creates a system with zero headroom. A brief memory spike — a large request, a garbage collection pause, a burst of log buffering — triggers an OOM kill rather than being absorbed by available memory.

### Cgroups v1 vs. v2

Cgroups v1 uses a per-resource hierarchy — CPU, memory, and I/O each have separate directory trees, and a process can be in different groups for different resources. Cgroups v2 unifies this into a single hierarchy where each process belongs to exactly one group, and all resource controllers apply to that group. V2 also adds **Pressure Stall Information (PSI)**, which provides metrics on how much time processes spend waiting for CPU, memory, or I/O resources — a much more actionable signal than raw utilization numbers. Most modern distributions and container runtimes have migrated to v2, but v1 compatibility layers persist in many production environments.

## What `docker run` Actually Does

To make this concrete: when you execute `docker run -it --memory=512m --cpus=1 ubuntu /bin/bash`, the following sequence occurs. The Docker daemon instructs the container runtime (typically `runc`) to create a new process. Before executing `/bin/bash`, `runc` calls `clone()` with flags requesting new PID, mount, network, UTS, IPC, and user namespaces. It then sets up the mount namespace by mounting the ubuntu image's layers via OverlayFS at the container's root. It configures the network namespace by creating a veth pair and attaching one end to the Docker bridge. It creates a new cgroup, writes `512m` to the memory limit file and the appropriate CFS quota for one CPU to the CPU control files, and places the new process into that cgroup. It drops Linux capabilities the container shouldn't have, applies a default seccomp profile that blocks approximately 44 dangerous syscalls, and finally calls `exec` to replace the setup process with `/bin/bash`.

The result is a process that believes it is PID 1 on its own machine, with its own filesystem, its own network, and its own hostname. But it is one process on the host, governed by the host kernel, constrained by cgroup limits, and visible in the host's process table to anyone with access.

## The Shared Kernel Boundary and Its Consequences

The performance advantage of containers comes directly from their architecture: no hardware emulation, no second kernel, no boot sequence. A container starts in milliseconds because it's just a process fork with some namespace and cgroup setup. You can run hundreds of containers on a single host because they share the kernel and the base OS libraries (via image layer deduplication).

But sharing the kernel is also the fundamental security limitation. Every container on a host makes syscalls to the same kernel. A kernel vulnerability is a vulnerability for every container on that host. A **container escape** — where a process breaks out of its namespace constraints and gains access to the host — is a kernel-level exploit. This is categorically different from a VM escape, which requires breaking through a hypervisor that provides hardware-level isolation.

This is why defense in depth matters for containers: seccomp profiles restrict which syscalls a container can make, capability dropping removes dangerous Linux capabilities like `CAP_SYS_ADMIN`, and AppArmor or SELinux profiles constrain file and network access patterns. Each layer reduces the attack surface independently. In practice, many production deployments run with default seccomp profiles and no mandatory access control, which means they're relying entirely on namespace isolation — the thinnest layer.

Another consequence of the shared kernel: `/proc` and `/sys` inside a container expose host-level information by default. Files like `/proc/meminfo` report the *host's* total memory, not the cgroup's limit. An application that reads available memory from `/proc/meminfo` to size its heap or thread pool will make decisions based on the host's 64GB of RAM, not the 512MB the container is actually allowed to use. This is the source of a large category of OOM kills in containerized Java, Python, and Node.js applications. The **LXCFS** project and runtime-level patches address this by intercepting reads to these files and returning cgroup-aware values, but it's not universal.

## The Mental Model

Think of a container as a process in a box. The box has tinted windows (namespaces) that control what the process can see — its own PID tree, its own filesystem, its own network stack. The box has a meter (cgroups) that enforces a strict budget on CPU time, memory, and I/O. But the floor of the box is the host kernel. Every container on the machine stands on the same floor. The box is strong enough to isolate well-behaved processes from each other, and with proper hardening (seccomp, capability dropping, user namespaces), it can resist many deliberate escape attempts. But it is not a separate machine. The isolation is constructed from policies enforced by a shared kernel, not from physical or virtual hardware boundaries.

This is the reasoning framework you need before building anything on containers: the speed and density come from the shared kernel, and so do the security constraints. Every operational decision — whether to run as root, whether to set resource limits, whether to apply seccomp profiles, whether to use a VM-level isolation boundary like Firecracker or gVisor for untrusted workloads — follows from understanding where the box is strong and where the floor is exposed.

## Key Takeaways

- A container is a regular Linux process with namespace and cgroup constraints applied by the host kernel; there is no guest kernel, no hypervisor, and no hardware emulation.
- Namespaces control visibility — what a process can see (its own PID tree, filesystem, network stack, hostname) — while cgroups control resources — what a process can consume (CPU time, memory, I/O bandwidth).
- CPU throttling is invisible to the throttled process; it manifests as unexplained latency spikes that are only visible through cgroup-level metrics like `nr_throttled` and `throttled_time`.
- A container without explicit memory limits can consume all host memory; a container with memory limits is OOM-killed without warning when it exceeds them. Neither is safe by default — both require deliberate configuration.
- `/proc/meminfo` and similar files inside a container report host-level values, not cgroup limits, which causes applications to over-allocate memory and get OOM-killed.
- The shared kernel is both the source of containers' performance advantage and their fundamental security boundary — a kernel exploit compromises every container on the host.
- Running containers as root inside the container typically means root on the host unless user namespaces are explicitly configured; most production defaults still map container root to host root.
- For workloads running untrusted code, namespace isolation alone is insufficient — VM-level isolation (Firecracker, gVisor) or aggressive seccomp and capability restriction is necessary to compensate for the shared-kernel attack surface.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Containers are easy to use at the surface and easy to misunderstand underneath. That mismatch becomes expensive the moment something abnormal happens. An app gets OOM-killed even though it “only used a little memory.” A service shows random latency spikes even though CPU utilization looks fine. A supposedly isolated process can still leak host information through `/proc`, or a “root in the container” process turns out to be much closer to real host root than the team assumed. These are not edge cases; they are normal consequences of how containers actually work.

The reason this topic matters is that containers are often treated like tiny VMs, and that mental model is wrong in ways that affect security, debugging, and capacity planning. If you think a container is a machine, you will ask the wrong questions and trust the wrong boundaries. If you understand that it is a host process with kernel-enforced visibility and resource constraints, a lot of confusing behavior stops being confusing and starts becoming predictable.

---

## What You Need To Know First

### Processes and the kernel

A process is a running program. The kernel is the part of the operating system that schedules processes, manages memory, handles filesystems, and services syscalls. The important prerequisite here is: processes do not directly control hardware or core OS resources; they ask the kernel to do things for them. Containers matter because they are still just processes talking to the host kernel.

### Syscalls

A syscall is how a process asks the kernel to perform privileged work, like opening a file, allocating memory, creating a socket, or starting another process. You do not need to know the syscall list in detail. What matters is that a containerized process makes syscalls to the same kernel as every other process on the host, which is why the shared-kernel boundary is so important.

### Virtual machines vs. OS-level isolation

A virtual machine gets virtual hardware and usually runs its own kernel. OS-level isolation does not create a second kernel; it isolates ordinary processes inside one kernel. That distinction is the heart of the article. VMs isolate by putting a boundary below the guest OS; containers isolate by having the host kernel present different views and enforce limits.

### Copy-on-write

Copy-on-write means shared data is reused until someone tries to modify it; only then is a private copy created. In container filesystems, many containers can share image layers read-only, and writes go into a separate writable layer. This explains both efficiency and ephemerality: sharing is cheap, but default container-local writes disappear when that writable layer is discarded.

---

## The Key Ideas, Connected

### A container is a process with constraints, not a machine.

What this means in practice is that when you start a container, you are not booting an OS. You are starting a normal Linux process and asking the kernel to apply isolation and resource rules around it. The containerized process uses the host scheduler, the host memory manager, and the host syscall interface.

That matters because once you stop imagining a container as a mini-server, the rest of the mechanics become clearer. If it is “just a process,” then isolation has to come from specific kernel features. That is what leads directly to namespaces and cgroups.

### Namespaces isolate what the process can see.

A namespace changes the process’s view of some global resource. The kernel still has one real underlying system state, but it presents a filtered or remapped version to the process. The process experiences that filtered view as “my own machine,” even though the host has not actually created a separate machine.

This is why a process in a PID namespace can think it is PID 1, why a process in a mount namespace sees a different root filesystem, and why a process in a network namespace can have its own interfaces and port bindings. The process is not in another world; it is seeing a curated slice of the same world. Once you understand that visibility is being rewritten, the next question becomes: even if the process sees its own world, what stops it from consuming all shared resources? That is where cgroups enter.

### Cgroups isolate what the process can use.

If namespaces answer “what can this process observe and address?”, cgroups answer “how much CPU, memory, or I/O may this process group consume?” The kernel groups processes together and enforces resource policies on the group. This is not advisory bookkeeping; it is active enforcement.

That distinction matters because visibility isolation alone would still let one container monopolize the host. A process that cannot see other workloads can still use all memory or all CPU unless something separately limits consumption. So once namespaces hide the rest of the world, cgroups become necessary to stop one isolated workload from ruining the machine for all the others.

### PID, mount, and network namespaces create the “feels like my own system” illusion.

PID namespaces make a process see only a limited process tree. Mount namespaces make a process see its own filesystem layout. Network namespaces make it see its own network interfaces, routes, and port space. Together, these produce most of what people informally mean by “the container.”

The important mechanical point is that each of these is a different kind of lie the kernel tells. The process tree is remapped, not duplicated. The filesystem root is switched, not physically separate. The network stack is isolated through namespace plumbing, not because the host disappeared. Because each piece is implemented separately, each can also fail, be shared intentionally, or be configured differently. That is why “container isolation” is not one switch; it is a bundle of kernel features assembled together.

### The filesystem illusion depends on layered images and copy-on-write.

A container image is built from read-only layers. At runtime, the container gets a thin writable layer on top. Reads walk down through layers until the file is found; writes copy the file into the writable layer and modify that copy. This means many containers can share the same lower layers efficiently.

That directly explains a behavior many people memorize without understanding: container filesystems are ephemeral by default. The writable layer is runtime state, not part of the underlying image. Remove the container, and that top layer goes away. So the filesystem model is not just about packaging; it changes persistence behavior. Once you see that, volume mounts stop looking like a convenience feature and start looking like the mechanism for keeping data outside the disposable writable layer.

### Network isolation works because the runtime wires a separate network namespace back to the host.

A container can bind to port 80 at the same time as another container because each has its own network namespace. But the packets still need to get somewhere, so the runtime creates a virtual link, usually a veth pair, connecting the container-side interface to host-side networking, often through a bridge.

This explains both flexibility and overhead. You get isolated port spaces and routable connectivity because the host is doing virtual network plumbing for each container. But packets are not magically teleporting; they are traversing extra virtual hops. That is why bridge networking has a small latency cost compared with host networking. The overhead is not mysterious; it comes from the added path through virtual interfaces and the bridge.

### CPU limits do not slow the process in a graceful, visible way; they cause scheduling throttling.

When you set a CPU limit, the kernel gives the cgroup a budget within a period. If the processes in that cgroup spend the budget early, the kernel stops scheduling them until the next period. The process is not told “you hit your limit.” It just stops getting CPU time for a while.

This produces a very specific failure mode: latency spikes that are hard to explain from inside the application. The app sees slower request handling, longer queue times, or timer weirdness, but no explicit error. That behavior follows directly from the mechanism. The kernel is not reducing instruction speed; it is intermittently refusing to run the process. Once you understand that, you know why app-level metrics can miss the cause and why cgroup throttling counters are the right place to look.

### Memory limits are enforced by killing, not by graceful slowdown.

Memory cgroups are harsher. If the container exceeds its limit, the kernel does not politely backpressure the process into using less memory. It invokes the OOM killer and terminates a process in the cgroup. If no limit is set, the process can compete for host memory until the whole system is under pressure.

This creates the central operational tradeoff: without a limit, one container can damage the whole node; with a tight limit, the container may die during ordinary spikes. The mechanism matters because it explains why “just set the limit equal to expected usage” often fails. Real workloads burst. Garbage-collected runtimes overshoot. Buffers grow temporarily. A hard ceiling means normal transients can become kills. So the right question is not “should I set limits?” but “what failure mode am I choosing, and what headroom do I need?”

### The container experience is shaped by what the kernel virtualizes incompletely.

Some files and interfaces inside containers still reflect host reality rather than cgroup-scoped reality. A classic example is `/proc/meminfo`, which may show host memory, not the container’s actual memory limit. An application that sizes itself based on that value can over-allocate and then get OOM-killed by the cgroup.

This is a good example of why the “kernel is lying” model is more accurate than “the container is a machine” model. The lie is selective, not perfect. Some things are namespaced cleanly; some are not; some need runtime patches or userspace shims to look container-aware. Once you understand that, strange application behavior inside containers stops looking random. It often comes from software reading host-shaped signals while living under container-shaped limits.

### The shared kernel is both the performance advantage and the security boundary.

Containers start quickly and run densely because there is no guest kernel to boot and no hypervisor translating hardware isolation into a second OS instance. They are cheap because the host kernel is shared. But that same fact means the kernel is the real trust boundary. If a process escapes namespace or capability constraints through a kernel bug, it is escaping into the host.

That is why a container escape is not just “like a VM escape but lighter.” It is a different class of risk. A VM has a stronger boundary because the guest kernel is not the host kernel. A container relies on policy enforcement within one kernel. Once that is true, extra hardening layers become necessary, which leads to the final idea.

### Security around containers is defense in depth because namespaces alone are not enough.

If all containers share one kernel, then reducing what syscalls they can make, what privileges they hold, and what files or devices they can access materially reduces blast radius. Seccomp narrows the syscall surface. Capability dropping removes broad powers like `CAP_SYS_ADMIN`. User namespaces can map container root to an unprivileged host user. AppArmor or SELinux can further constrain behavior.

These are not optional decorations on top of “real” container isolation. They compensate for the thinness of the shared-kernel boundary. An engineer who understands the mechanics sees default container isolation as a starting point, not a complete trust model. And from there the broader design decision becomes legible: for trusted internal workloads, ordinary containers may be enough; for untrusted code, you often want a stronger isolation layer such as microVMs or sandboxed runtimes.

---

## Handles and Anchors

### 1. “A container is a process in a box, standing on the host kernel floor.”

The walls of the box are namespaces and cgroups. They limit what the process can see and use. But the floor is shared. If the floor cracks, every box is affected. This is a good anchor for remembering both the convenience and the risk.

### 2. “Namespaces answer ‘what world do I appear to live in?’ Cgroups answer ‘what budget am I allowed to burn?’”

That one sentence separates the two most important primitives cleanly. If you are debugging weird visibility, think namespaces. If you are debugging starvation, throttling, or OOMs, think cgroups.

### 3. Ask: “Is this isolation implemented by a separate kernel, or by one kernel presenting filtered views and enforcing quotas?”

That question quickly tells you whether you are dealing with VM-style isolation or container-style isolation. It also forces you to locate the real trust boundary before making security assumptions.

---

## What This Changes When You Build

### An engineer who understands this will set memory limits with headroom, not just equal to expected steady-state usage, because cgroup memory enforcement ends in OOM kills rather than graceful slowdown.

The unaware default is to set a limit that matches nominal usage or to copy a platform default without thinking. The consequence is a service that dies during brief but ordinary spikes. A more informed approach is to decide how much burst the workload needs, test under pressure, and treat the limit as a kill threshold, not a planning estimate.

### An engineer who understands this will debug latency spikes by checking cgroup throttling metrics, not just application response times and host CPU averages, because CPU limits manifest as descheduling rather than explicit errors.

The unaware default is to conclude “the app is slow” or “the node is underutilized, so CPU is not the issue.” The consequence is long debugging cycles chasing database calls, GC pauses, or network ghosts while the real issue is quota exhaustion. Knowing the mechanism changes where you look first.

### An engineer who understands this will be cautious about software that auto-sizes itself from `/proc` or host-visible system information, because the process may observe host capacity while being constrained by cgroups.

The unaware default is to trust runtime auto-tuning. The consequence is heap sizing, worker counts, or buffer allocation tuned for the host instead of the container, followed by OOM kills or aggressive memory pressure. The informed engineer explicitly sets container-aware runtime flags or validates that the runtime is cgroup-aware.

### An engineer who understands this will treat “root in the container” as a security-sensitive choice, because without user namespaces it often maps to real host-root privilege at the kernel boundary.

The unaware default is to accept root inside the container as harmless because “it’s isolated anyway.” The consequence is a much more dangerous posture if a breakout or misconfiguration occurs. The informed engineer prefers non-root images, user namespace remapping, rootless runtimes where possible, and deliberate capability minimization.

### An engineer who understands this will choose stronger isolation for untrusted workloads, because containers gain speed by sharing the kernel and therefore do not provide the same trust boundary as VMs.

The unaware default is to standardize on plain containers for everything. The consequence is inheriting shared-kernel risk in places where the workload should never have had that much proximity to the host. The informed engineer asks whether the code is trusted; if not, they consider microVMs, gVisor-like sandboxes, or more aggressive syscall and capability restrictions.

---

</details>


<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) A container is a process with extra kernel rules, not a tiny VM

```sh
# Host shell
sleep 1000 &
HOST_PID=$!
echo "host pid = $HOST_PID"

# "Container-like" process: same kernel, just a new PID namespace view
unshare --pid --fork --mount-proc sh -c '
  echo "inside namespace, I am PID $$"
  ps -o pid,ppid,comm
  sleep 1000
'
```

What this shows:
- `sleep` on the host and `sleep` “inside the container” are both ordinary host processes.
- Inside the new PID namespace, the shell thinks it has a tiny private process tree.
- There is still only one kernel scheduling both processes.

Cost/tradeoff:
- Fast startup comes from “just start a process”.
- The same fact means both processes trust the same host kernel.

---

### 2) Namespaces isolate what a process can see

```sh
# Host sees the real process tree
ps -o pid,comm | head

# New PID namespace: filtered process view
unshare --pid --fork --mount-proc sh -c '
  echo "--- inside PID namespace ---"
  ps -o pid,comm
'
```

```sh
# New UTS namespace: private hostname
hostname
unshare --uts sh -c '
  hostname container-demo
  echo "inside hostname = $(hostname)"
'
echo "host hostname = $(hostname)"
```

What this shows:
- PID namespace: same machine, different visible process table.
- UTS namespace: same kernel, different hostname.

Cost/tradeoff:
- Isolation is “kernel presents a filtered view,” not “new machine exists.”
- If you share a namespace intentionally, the isolation disappears for that resource.

---

### 3) Mount namespaces + copy-on-write create the container filesystem illusion

```sh
# Pseudocode: what runtime storage looks like

image_layers = [
  "layer A: /bin/sh",
  "layer B: /etc/app.conf = version=1",
]

writable_layer = {}

read("/etc/app.conf"):
  if "/etc/app.conf" in writable_layer:
    return writable_layer["/etc/app.conf"]
  else:
    return topmost_match_in(image_layers, "/etc/app.conf")

write("/etc/app.conf", "version=2"):
  # copy-on-write: don't mutate image layer
  writable_layer["/etc/app.conf"] = "version=2"

delete_container():
  writable_layer = {}   # container-local changes vanish
```

What this shows:
- Reads can come from shared image layers.
- Writes go to a private top layer.
- Deleting the container deletes that writable layer, so “local filesystem changes” are ephemeral.

Cost/tradeoff:
- Efficient sharing and fast startup.
- But persistence is not automatic; you need a volume if the data must survive.

---

### 4) Network namespaces isolate port space, not networking work

```sh
# Two processes can both "own port 80" if they are in different network namespaces.

# namespace A
ip netns add nsA
ip netns exec nsA sh -c '
  ip link set lo up
  nc -l -p 80 >/dev/null
' &

# namespace B
ip netns add nsB
ip netns exec nsB sh -c '
  ip link set lo up
  nc -l -p 80 >/dev/null
' &
```

Both listeners succeed because:
- `nsA` has its own network stack.
- `nsB` has its own network stack.

But this is not free:
```text
container process
  -> veth
  -> host bridge / routing / NAT
  -> network
```

Cost/tradeoff:
- Great isolation and flexible wiring.
- Slight overhead and more moving parts than host networking.

---

### 5) Cgroups limit what a process can use: CPU limits throttle, they do not error

```sh
# Pseudocode for CFS quota behavior

period = 100ms
quota  = 50ms   # "0.5 CPU"

loop forever:
  run_tasks_until_cpu_time_used(quota)
  throttle_until_next_period()
```

Application view:

```python
# app.py
while True:
    handle_request()   # no exception says "you were throttled"
```

Kernel/accounting view:

```text
cpu.stat:
  nr_periods     1000
  nr_throttled    420
  throttled_usec  9000000
```

What this shows:
- The process is not told “CPU limit exceeded.”
- It just stops getting scheduled until the next period.
- From inside the app, it looks like random slowness.

Cost/tradeoff:
- CPU limits protect neighbors.
- But they can create latency spikes that app metrics alone won’t explain.

---

### 6) Memory limits are hard ceilings; no limit risks the host, tight limits kill the container

Before: no memory limit

```python
# alloc.py
chunks = []
while True:
    chunks.append(bytearray(100 * 1024 * 1024))  # +100 MB forever
```

Effect:
```text
No cgroup memory limit:
  process keeps growing
  host memory pressure rises
  eventually host-wide OOM risk
```

After: cgroup memory limit = 512 MB

```text
Same program, but inside a 512 MB memory cgroup:

usage: 100 MB -> 200 MB -> 300 MB -> 400 MB -> 500 MB -> 600 MB
result: kernel sends SIGKILL to a process in the cgroup
```

And the subtle trap:

```sh
# Inside container
cat /proc/meminfo | head -n 1
# MemTotal: 67108864 kB   <-- host memory, maybe 64 GB

# But cgroup limit might actually be:
cat /sys/fs/cgroup/memory.max
# 536870912               <-- 512 MB
```

What this shows:
- No limit: one container can hurt the whole node.
- Hard limit: the container dies when it crosses the line.
- Apps that size themselves from `/proc/meminfo` may over-allocate and get OOM-killed.

Cost/tradeoff:
- Limits contain blast radius.
- But limits need headroom, because memory enforcement is abrupt.

---

### 7) “Root in the container” may still be dangerously close to root on the host

Without user namespaces:

```text
container UID 0  -> host UID 0
```

With user namespaces:

```text
container UID 0  -> host UID 100000
```

Pseudocode:

```sh
# unsafe mental model
if inside_container and uid == 0:
  assume("basically harmless root")
# false

# safer model
if uid == 0:
  ask("root where?")
  # root in container namespace?
  # or real host root mapping?
```

What this shows:
- “Root” is only safe-ish if mapped to an unprivileged host identity.
- Without user namespaces, a breakout has much worse consequences.

Cost/tradeoff:
- User namespaces improve security.
- But they can complicate mounts, permissions, and older tooling.

---

## Key Ideas

A container is best understood as a normal Linux process wrapped in two main kinds of kernel policy: namespaces change its view of the world, and cgroups limit its budget. That combination creates the “feels like my own machine” experience without actually creating a machine. The sketches also show why this is powerful and dangerous at the same time: startup is cheap because there is no guest kernel, but the shared host kernel becomes the true trust boundary; filesystem writes are cheap because of copy-on-write, but ephemeral; CPU limits protect neighbors, but show up as invisible throttling; memory limits contain damage, but fail by killing; and “root in the container” is only meaningfully safer if user namespaces break the mapping to host root.

</details>