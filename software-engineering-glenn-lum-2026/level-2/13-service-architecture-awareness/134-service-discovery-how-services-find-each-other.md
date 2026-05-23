## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers encounter service discovery as a configuration task. You set an environment variable, point at a hostname, maybe configure a registry URL, and move on. It works until it doesn't — and when it doesn't, it fails in ways that are baffling if you think of discovery as a lookup problem. A service that was working thirty seconds ago starts throwing connection errors. A deployment causes ten seconds of elevated 5xx rates even though every health check passes. A scaling event sends all traffic to a single new instance while the other nine sit idle.

These failures make sense once you understand that service discovery is not a lookup problem. It is a **consistency problem**. In a dynamic environment — containers being scheduled, instances scaling up and down, nodes failing — the set of network locations for any given service is constantly changing. Service discovery is the mechanism by which every client maintains a reasonably accurate view of that changing reality. The mechanics of how that view is constructed, propagated, and invalidated determine how your system behaves during the moments that matter most: deployments, scaling events, and partial failures.

## The Registration Lifecycle

Before any service can be discovered, it must be registered. This sounds simple, but the registration lifecycle has subtleties that directly affect reliability.

In **self-registration**, each service instance registers itself with a registry when it starts up and deregisters when it shuts down. The instance sends a message — typically an HTTP PUT or a gRPC call — containing its address, port, and metadata to a registry like Consul, Eureka, or etcd. The problem is obvious: what if the instance crashes without deregistering? It's now a ghost entry — clients will be routed to an address that accepts no connections.

This is why registries use **heartbeats** or **TTL-based leases**. The instance must periodically renew its registration. If it fails to renew within the TTL window, the registry removes it. Eureka defaults to a 30-second heartbeat interval with a 90-second eviction threshold. That means a crashed instance can remain in the registry for up to 90 seconds. During those 90 seconds, clients are being routed to a dead endpoint.

In **third-party registration**, something external to the service handles registration. Kubernetes does this: the kubelet and the control plane track pod lifecycle events and update the Endpoints (or EndpointSlice) objects accordingly. The service instance itself has no awareness of the registry. This eliminates the deregistration-on-crash problem because the platform detects the failure and removes the entry. But it introduces coupling to the platform — your discovery mechanism is now inseparable from your orchestrator.

The critical thing to internalize is that registration is not instantaneous and deregistration is not instantaneous. There is always a window — sometimes a few hundred milliseconds, sometimes tens of seconds — during which the registry's state does not match reality. Every design decision in service discovery is about managing the size and consequences of that window.

## How DNS-Based Discovery Actually Works

DNS is the most familiar discovery mechanism, and the most deceptive. Engineers reach for it because it feels simple: resolve a hostname, get an IP, connect. But DNS was designed for a world where IP addresses change rarely, and service discovery lives in a world where they change constantly.

When you configure a service in Kubernetes with a `ClusterIP` type, CoreDNS returns a single virtual IP. The kube-proxy (or eBPF, depending on your CNI) handles the actual routing to backend pods. The client resolves the name once, gets one IP, and doesn't need to know about individual instances. This is **server-side discovery masquerading as DNS** — the load balancing happens at the network layer, not in the DNS response.

**Headless services** (`clusterIP: None`) work differently. A DNS query returns multiple A records — one for each backing pod. The client receives the full set of IPs and must choose one. This is where DNS starts to strain.

The fundamental issue is **TTL and caching**. DNS responses include a time-to-live value that tells the resolver how long to cache the result. Set the TTL high and you get stale records when pods are rescheduled. Set it to zero and you're issuing a DNS query on every connection attempt — which works in some environments but breaks in others, because not every layer in the stack honors a zero TTL. The JVM, notoriously, caches DNS resolutions indefinitely by default in some security manager configurations. The `glibc` resolver has its own cache. Client HTTP libraries often resolve once and hold the connection. You can set your TTL to 5 seconds and still have clients hitting a dead IP because the resolution was cached three layers down the stack in something you don't control.

There's a further limitation: DNS A records return IP addresses but not port numbers. **SRV records** solve this by returning a host, port, priority, and weight, which gives the client enough information to do weighted routing. But most HTTP client libraries don't natively consume SRV records. You need either a specialized client or an intermediary that translates SRV responses into routable addresses.

DNS-based discovery works well when the set of instances changes infrequently and when the client infrastructure is well-understood enough that you can control caching behavior end to end. It becomes unreliable in highly dynamic environments where pods churn every few minutes.

## Client-Side Discovery and the Load Balancing Decision

In client-side discovery, the client queries a service registry (or watches it for changes), receives the full set of healthy instances, and decides which one to call. The load balancing logic lives in the client process.

This is what gRPC does natively. A gRPC channel is configured with a **resolver** that returns a list of backend addresses and a **load balancing policy** that selects among them. The default policy is `pick_first` — try the first address that works and stick with it. This is a common source of confusion: engineers deploy five instances of a service, configure gRPC, and find that all traffic goes to a single instance. The fix is switching to `round_robin` or a custom policy, but the failure reveals a deeper truth — client-side discovery means the client must understand load balancing, and the default behavior might not be what you expect.

The mechanics of client-side balancing interact with **connection pooling** in ways that matter. HTTP/1.1 clients typically open multiple short-lived connections, so round-robin across resolved IPs works naturally. HTTP/2 and gRPC multiplex many requests over a single long-lived connection. If the client opens one connection to one backend and multiplexes everything over it, load balancing at the connection level is meaningless — you need request-level balancing, which requires the client to maintain connections to multiple backends and distribute requests across them.

The advantage of client-side discovery is latency and control. There's no intermediary proxy adding a network hop. The client can implement sophisticated balancing strategies — least-outstanding-requests, consistent hashing for cache affinity, locality-aware routing. The cost is that every client language and framework needs a correct implementation. If your system has services in Go, Java, and Python, you need three working discovery and load balancing implementations, and they all need to handle edge cases like instance removal, connection draining, and retry behavior consistently.

## Server-Side Discovery and the Proxy Tradeoff

Server-side discovery puts a load balancer or reverse proxy between the client and the service instances. The client sends traffic to a single stable endpoint — a virtual IP, a DNS name pointing to a load balancer — and the proxy routes to an available backend.

This is the model behind Kubernetes `ClusterIP` services, AWS ALB target groups, and traditional HAProxy/NGINX setups. The client doesn't need to know about the registry. It doesn't need load balancing logic. It just connects to one address.

The proxy now owns two responsibilities: maintaining an up-to-date view of healthy backends, and distributing traffic across them. The propagation delay here is between the registry and the proxy's backend pool. When a new instance registers, there's a window before the proxy adds it. When an instance fails, there's a window before the proxy removes it. These windows are typically shorter than DNS TTLs because the proxy can watch the registry for changes rather than polling, but they still exist.

The operational cost is the proxy itself. It's an additional piece of infrastructure that needs to be deployed, monitored, and scaled. It adds a network hop — typically sub-millisecond within a data center, but it shows up under high throughput. And it's a chokepoint: if the proxy fails, all traffic to that service fails. You mitigate this with redundancy, but now you're running highly available proxies in front of every service, which is essentially what a service mesh does.

## Service Mesh: Discovery as Infrastructure

A service mesh moves discovery, load balancing, retries, and observability out of the application entirely and into a **sidecar proxy** — a process (typically Envoy) that runs alongside every service instance.

The mechanics work like this: outbound traffic from your application is intercepted by the sidecar (using iptables rules or eBPF) before it leaves the pod. The sidecar resolves the destination service name against its local configuration, which was pushed to it by the mesh's **control plane** (Istio's istiod, Linkerd's destination service). The control plane watches the service registry — usually the Kubernetes API — and pushes endpoint updates to all sidecars via a protocol like **xDS** (Envoy's discovery service API). The sidecar then routes the request to a specific backend instance, applying load balancing, retries, and timeouts as configured.

This is client-side discovery, architecturally. The balancing decision happens at the caller's side. But the implementation lives outside the application code, in the sidecar. Your Go service and your Python service get identical discovery and balancing behavior without either of them containing a single line of discovery logic.

The cost is real. Every pod now runs an additional process consuming CPU and memory. The sidecar adds latency to every request — typically 1–3ms per hop, but in a request that traverses six services, that's 12–36ms added. Debugging becomes harder because the network path is no longer direct; you're reasoning about application behavior and proxy behavior simultaneously. And the control plane is a critical dependency — if it can't push updates, sidecars operate on stale configuration.

## Where Discovery Breaks

The most common production failure in service discovery is **stale routing during deployment**. An old instance is being terminated, but the registry hasn't propagated the removal yet, and clients are still sending traffic to it. The connection is refused or times out. This is the staleness window made visible. The mitigation is **connection draining**: the instance stops accepting new connections, finishes in-flight requests, then shuts down, and you configure the deregistration delay to exceed the propagation delay. If the drain period is shorter than the time it takes for all clients to learn the instance is gone, you'll drop requests.

The second failure mode is **discovery during partition**. If the registry is split-brained — part of the cluster thinks an instance is healthy and part doesn't — different clients get different answers. Consul and etcd are CP systems (they sacrifice availability for consistency), so during a partition the registry may refuse to answer queries rather than return stale data. Eureka is AP (it sacrifices consistency for availability), so it will continue serving registrations that may be outdated. Neither is wrong. The choice determines whether your failure mode is "no discovery results" or "possibly stale discovery results," and your system needs to handle whichever one you've chosen.

The third failure mode is **health check mismatch**. The registry says the instance is healthy because it responded to a TCP check. But the instance is in a state where it accepts connections and then hangs — it's wedged on a downstream dependency, or it's in a garbage collection pause, or it's returned to service before its caches are warm. This is the gap between **liveness** (the process is running) and **readiness** (the process can serve traffic correctly). If your health check doesn't test what your clients actually need, your discovery mechanism will cheerfully route traffic to instances that can't handle it.

## The Mental Model

Service discovery is a distributed cache coherence problem. Every consumer of a service holds a local view of where that service's instances are. That view was accurate at some point in the past. The discovery mechanism determines how that view is updated, how much lag exists between reality and each client's understanding of reality, and what happens when the view is wrong.

The three approaches — DNS, client-side registry, service mesh — are not a progression from primitive to advanced. They are different answers to the same question: who is responsible for maintaining that view, and what is the acceptable staleness? DNS pushes it to the network's caching layer with coarse-grained TTLs. Client-side discovery pushes it to the application with fine-grained watches. Service mesh pushes it to infrastructure with proxy-level interception. Each shifts complexity to a different layer. None eliminates it.

The capability you should have after reading this post is the ability to look at any discovery configuration and answer: how long after an instance dies could a client still try to reach it? If you can answer that question for your system, you understand your discovery model. If you can't, you have a latent incident waiting for the right scaling event.

## Key Takeaways

- Service discovery is a consistency problem, not a lookup problem — every mechanism has a staleness window between reality and what clients believe, and the size of that window determines your failure behavior during deployments and scaling events.

- DNS-based discovery is limited by TTL caching at multiple layers (OS, language runtime, client library), and setting a low TTL does not guarantee clients will re-resolve promptly — you must understand every cache in the resolution path.

- Self-registration requires heartbeat-based eviction to handle crashes, which means a dead instance can remain discoverable for the duration of the eviction timeout — typically 30 to 90 seconds in default configurations.

- Client-side discovery gives you control over load balancing strategy but requires a correct implementation in every language and framework your system uses, and interacts with connection pooling in ways that can silently defeat round-robin balancing (especially with HTTP/2 and gRPC).

- Server-side discovery simplifies clients but introduces a proxy as a dependency that must be independently scaled, monitored, and made highly available.

- A service mesh is architecturally client-side discovery relocated to a sidecar proxy — it standardizes behavior across languages but adds per-request latency, per-pod resource overhead, and a critical dependency on the control plane.

- Connection draining during shutdown must exceed the discovery propagation delay; if instances terminate before all clients have learned they're gone, you will drop requests on every deployment.

- Your health check defines what "discoverable" means — if the check only verifies liveness (process is running) rather than readiness (process can serve correctly), discovery will route traffic to instances that accept connections but cannot handle requests.

# Discussion

## Why This Conversation Is Happening

Service discovery becomes visible when systems stop being static. In a simple setup, a service lives at one hostname or one IP for a long time, and “finding it” really does look like a lookup. But modern systems constantly change underneath you: containers restart, pods get rescheduled, autoscaling adds and removes instances, nodes fail, deployments replace one fleet with another. The real problem is no longer “what is the address?” but “how quickly does everyone learn that the address set has changed?”

If you miss that, production failures look random. A service instance dies, but clients keep calling it because some cache still thinks it exists. A rollout starts cleanly, but requests fail during termination because removal from discovery lags behind process shutdown. A scaling event adds new capacity, but traffic stays pinned to old connections or one lucky instance because discovery and balancing are happening at different layers than you assumed.

So the practical reason to care is this: service discovery determines how wrong your system is allowed to be about reality, for how long, and who pays when that wrongness shows up. If you cannot describe that lag, you cannot reason clearly about deployments, failover, or traffic distribution.

---

## What You Need To Know First

**1. Load balancing**  
Load balancing is just the act of choosing which backend instance should handle a request when multiple healthy instances exist. That choice can happen in the client, in a proxy, or somewhere in the network. The important part here is that “discovering instances” and “choosing among them” are related but separate jobs.

**2. Health checks: liveness vs readiness**  
A liveness check asks, “Is the process alive?” A readiness check asks, “Should this instance receive traffic right now?” An app can be alive but not ready: maybe it is starting up, warming caches, stuck on a dependency, or draining before shutdown. Discovery is only as good as the signal it uses to decide who is eligible.

**3. Caching and TTL**  
A cache keeps old answers so you do not have to ask again every time. TTL, or time-to-live, is how long a cached answer may be reused before it should be refreshed. In service discovery, caching improves performance but creates staleness: clients may keep using a once-correct answer after reality has changed.

**4. Long-lived vs short-lived connections**  
Some clients open a connection, use it briefly, and reconnect often. Others open one connection and send many requests over it for a long time, like HTTP/2 and gRPC often do. This matters because even if discovery learns about new backends, a client with one long-lived connection may keep sending everything to the same place.

---

## The Key Ideas, Connected

**Service discovery is fundamentally a consistency problem, not a lookup problem.**  
The central point is that the set of valid endpoints for a service is changing over time, while each client only sees a local copy of that information. The question is not simply “where is service A?” but “how fresh is the client’s view of where service A is?” Once you frame it this way, the important variables become update delay, cache invalidation, health signal quality, and what happens while views disagree.

**Because reality changes continuously, registration and deregistration are never perfectly in sync with it.**  
Before anyone can discover an instance, some system must add it to a registry or routing table. Before traffic stops going to a dead or terminating instance, some system must remove it. Those changes take time. In self-registration, the instance announces itself and later renews its lease or heartbeat; if it crashes, the registry only notices after the lease expires. In third-party registration, the platform observes lifecycle changes and updates discovery on the instance’s behalf. Either way, there is always a gap between “what is true” and “what discovery currently believes.” That gap is the staleness window, and every other design choice is really about where that window comes from and how large it gets.

**Once you accept that stale information is unavoidable, the main design question becomes who holds the stale view.**  
Different discovery systems place the stale state in different layers. DNS places it in resolvers and caches. Client-side discovery places it in each application process. Server-side discovery places it in proxies or load balancers. Service mesh places it in sidecars managed by infrastructure. This matters because each layer has different update mechanics, observability, failure modes, and operational costs.

**DNS-based discovery works by returning names or IPs, but its behavior is dominated by caching rather than by the DNS query itself.**  
DNS feels simple because the interface is simple: ask for a name, get an address. But in dynamic systems, the hard part is not producing the answer once; it is making sure old answers stop being used quickly enough. TTL is supposed to control this, but there are multiple caches in the path: OS resolver behavior, runtime behavior, client library behavior, and connection reuse. So a low TTL does not guarantee fast convergence to reality. That means DNS is often acceptable when endpoint sets change slowly or when you tightly control the whole resolution path, but it becomes fragile when instances churn quickly and different clients cache differently.

**That DNS limitation leads directly to client-side discovery: if DNS caches are too blunt, let the client hold the backend list directly and update it more precisely.**  
In client-side discovery, the client talks to a registry or receives watched updates and gets the current set of healthy instances. This avoids some of DNS’s coarse cache behavior and gives the caller more immediate control. But once the client has the full backend list, it also inherits the responsibility of choosing among them. Discovery and load balancing become one combined concern inside the client.

**When load balancing moves into the client, connection behavior becomes part of the discovery story.**  
This is a subtle but important mechanical point. If a client has a list of five healthy backends but opens one long-lived HTTP/2 or gRPC connection to the first one and sends everything over that connection, then “having five backends” does not produce balanced traffic. The registry may be correct, but the actual request distribution is still skewed because balancing happened only once, at connection establishment. That is why default policies like gRPC’s `pick_first` can surprise engineers: the discovery data is fine, but the selection strategy and connection model defeat the intended distribution.

**Because client-side discovery requires each application stack to implement these mechanics correctly, many systems push the problem into a proxy instead.**  
Server-side discovery says: let clients talk to one stable endpoint, and let a dedicated intermediary maintain the backend pool and choose targets. This simplifies application code because clients no longer need resolver logic, balancing policy, or registry watches. The proxy can often react quickly to changes because it watches the registry directly. But this simplification is not free; it moves complexity into a new component that must stay available, keep its backend view fresh, and handle all traffic without becoming a bottleneck or single point of failure.

**Service mesh is the same architectural idea as client-side discovery, but moved out of application code and into per-service infrastructure.**  
A mesh sidecar sits next to the application and makes outbound routing decisions locally, using endpoint state pushed from a control plane. So architecturally it behaves like client-side discovery: the caller side chooses the backend. Operationally, though, it feels like infrastructure: app teams do not write discovery code in every language. This solves consistency of implementation across stacks, but it introduces per-hop latency, sidecar resource cost, and a new dependency on the control plane’s ability to distribute fresh config.

**No matter which model you choose, the real failures show up when stale views intersect with lifecycle events.**  
During deployment, an instance may stop being a valid target before every client has learned that fact. During scale-up, new instances may exist before traffic reaches them. During network partition, different observers may disagree on which instances are alive. During partial degradation, a health check may say “healthy” even though the instance cannot serve useful work. These are not separate concerns from service discovery; they are what service discovery looks like when its consistency model is stressed.

**That is why health check quality and shutdown behavior are part of discovery mechanics, not add-ons.**  
If discoverability is based on a TCP connect check, the system may route to instances that accept connections but hang on real requests. If shutdown happens faster than deregistration propagation, clients will continue sending traffic into disappearing instances. So readiness checks and connection draining are how you shape the cost of stale information. You cannot remove staleness, but you can make sure that while stale entries still exist, those instances fail gracefully or stop accepting new work safely.

**The practical mental model is that service discovery is distributed cache coherence for endpoint lists.**  
Every consumer has a view of “where this service lives.” That view was correct at some earlier moment. The implementation choice determines how updates propagate, how much lag exists, and whether the system prefers stale answers, no answers, or proxy-mediated answers during trouble. Once you hold that model, the key operational question becomes obvious: after an instance dies or begins shutdown, how long can some caller still try to use it? If you can answer that, you understand your discovery system mechanically rather than cosmetically.

---

## Handles and Anchors

**1. “Service discovery is not answering ‘where is it?’; it is answering ‘how stale is my answer?’”**  
Use this as the core reframing. If someone describes discovery only in terms of hostnames, registries, or DNS records, ask about staleness windows and update propagation. That usually reveals the real behavior.

**2. Think of it like distributed cache invalidation for backend addresses.**  
Every client, proxy, or sidecar is holding a cached view of healthy endpoints. All the classic cache questions apply: who populates it, how long it lives, how it gets invalidated, and what happens while old data is still in use.

**3. Diagnostic question: “After an instance dies, who can still believe it exists, and for how long?”**  
This is a powerful test for any system. The answer forces you to inspect heartbeats, TTLs, DNS caches, proxy watch delays, connection reuse, health check semantics, and draining behavior. If nobody on the team can answer it, the system is relying on hidden defaults.

---

## What This Changes When You Build

**An engineer who understands this will approach deployments differently because shutdown timing must be aligned with discovery propagation.**  
The default unaware behavior is to terminate old instances as soon as the orchestrator says replacement instances are up. That often causes brief 5xx spikes because some callers still route to instances that are already exiting. The aware engineer adds readiness-off-first behavior, connection draining, and termination grace periods longer than the maximum propagation delay.

**An engineer who understands this will evaluate DNS-based discovery by tracing every cache layer, not by trusting the configured TTL.**  
The unaware engineer sees `TTL=5s` and assumes clients will stop using old addresses within five seconds. The aware engineer checks runtime DNS caching, OS resolver behavior, library behavior, connection pooling, and whether clients re-resolve on reconnect. This changes whether DNS is considered viable at all for a highly dynamic service.

**An engineer who understands this will treat client-side discovery as a load-balancing implementation choice, not just a registry integration.**  
The unaware engineer enables a registry-backed client and assumes traffic will naturally spread. The aware engineer asks what balancing policy is used, whether connections are long-lived, whether request-level balancing exists, and how instance removal affects open connections. This is the difference between “we have five replicas” and “one replica receives 95% of traffic.”

**An engineer who understands this will design health checks around traffic safety, not process existence.**  
The unaware engineer exposes a simple liveness endpoint or TCP port check and assumes discoverability is handled. The aware engineer asks what conditions actually make an instance safe to receive requests: dependency availability, startup completion, cache warmup, graceful drain state, overload state. That changes which instances enter or remain in the discovery set.

**An engineer who understands this will choose between client-side, server-side, and mesh-based discovery by asking where they want the complexity to live.**  
The unaware engineer often inherits whichever mechanism the platform makes easiest and treats it as neutral. The aware engineer recognizes the trade: client libraries give control but require per-language correctness; proxies simplify clients but add infrastructure and hops; meshes standardize behavior but add latency, resource overhead, and control-plane dependency. That leads to deliberate architecture instead of accidental complexity placement.

---
