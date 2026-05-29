## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers, when asked about Layer 4 versus Layer 7 load balancing, will give you the textbook distinction: Layer 4 routes based on IP and port, Layer 7 routes based on HTTP attributes like path and headers. That description is accurate and almost completely useless for making real decisions. The actual difference between these two approaches is not about what information they route on — it is about what the load balancer *becomes* when it operates at each layer. At Layer 4, the load balancer is a traffic director that points connections somewhere and steps aside. At Layer 7, it is a full participant in every conversation — terminating connections, parsing protocols, and making decisions on a fundamentally different unit of work. That distinction changes everything: the resource profile, the failure modes, the observability you get, and the kinds of problems you can solve. Understanding the routing criteria is Level 1. Understanding the connection model is what lets you actually reason about which one to use and why.

## How Layer 4 Actually Handles Traffic

A Layer 4 load balancer makes its routing decision on the first packet of a TCP connection — typically the SYN packet. It looks at source IP, destination IP, source port, destination port, and protocol. From those five fields, it picks a backend, and every subsequent packet belonging to that connection goes to the same backend.

The critical detail is what happens to the packets after that decision. Most Layer 4 load balancers use **destination NAT (DNAT)**: they rewrite the destination IP address of incoming packets to the chosen backend's IP, and rewrite the source IP on return packets so the client never knows the backend exists. Some use **Direct Server Return (DSR)**, where the load balancer only touches inbound traffic and the backend responds directly to the client, bypassing the load balancer entirely on the return path. Either way, the load balancer does not terminate the TCP connection. The TCP handshake completes between the client and the backend (with the load balancer rewriting addresses in transit). The load balancer never holds connection state in the way a proxy does — it holds a flow mapping table, but not socket buffers.

This is why Layer 4 load balancers are fast. They can be implemented in the kernel's network stack, in eBPF, or even in hardware. They do not need to buffer data, parse payloads, or manage TLS state. A single machine running an L4 load balancer can handle millions of concurrent connections with minimal CPU and memory overhead.

But the cost of not terminating the connection is that the load balancer is *blind to the conversation*. It cannot see HTTP headers. It cannot see URL paths. It cannot see cookies. It cannot distinguish between ten HTTP requests multiplexed over one HTTP/2 connection — all of them go to the same backend because they share one TCP connection. The routing decision is **per-connection**, and once made, it is permanent for the lifetime of that connection.

## How Layer 7 Actually Handles Traffic

A Layer 7 load balancer does something fundamentally different: it **terminates the client's TCP connection**. The client completes its TCP handshake with the load balancer, not with the backend. If the traffic is HTTPS, the load balancer also terminates TLS — it holds the certificate, performs the handshake, and decrypts the traffic. At this point, the load balancer can read the plaintext HTTP request.

Once it has parsed the request — method, path, Host header, cookies, any header you care about — it opens a *second* connection to a backend and forwards the request. The client has one connection to the load balancer; the backend has a separate connection from the load balancer. **Two TCP connections, one request.** The load balancer is a proxy in the true sense: it receives, interprets, and retransmits.

This proxy model means the unit of routing is the **request**, not the connection. Ten HTTP requests arriving on one client connection can be distributed across ten different backends. This is especially significant with HTTP/2 and gRPC, where a single TCP connection carries many concurrent streams. An L4 load balancer sends all those streams to one backend. An L7 load balancer can spread them across your entire fleet.

The proxy model also gives the load balancer the ability to **modify traffic in transit**. It can inject `X-Forwarded-For` headers so backends know the client's real IP (which otherwise gets lost behind DNAT). It can rewrite paths, add authentication tokens, or strip sensitive headers. It can buffer responses and retry failed requests on a different backend — something an L4 load balancer fundamentally cannot do, because it does not understand where one request ends and another begins.

The cost is real and unavoidable: the load balancer must allocate memory for every active connection (both client-side and backend-side), parse every byte of every request, and manage TLS state for every encrypted connection. CPU and memory consumption scale with request volume and request size, not just connection count. A Layer 7 load balancer handling the same total throughput as a Layer 4 load balancer will require significantly more resources.

## Connection Pooling and Its Consequences

Because an L7 load balancer maintains separate connections to backends, it can **pool those connections**. Instead of opening a new TCP connection to a backend for every client request, it maintains a set of persistent connections and reuses them across many clients.

This matters more than it appears to. Without pooling, a service receiving 10,000 requests per second from 10,000 clients would need to manage 10,000 TCP connections. With an L7 load balancer pooling connections, the same backend might receive all that traffic over 50 persistent connections. The backend's connection management overhead drops dramatically.

This is also why gRPC services almost always require L7 load balancing. gRPC uses HTTP/2, which multiplexes many RPCs over a single long-lived TCP connection. If you put an L4 load balancer in front of a gRPC service, each client opens one connection, that connection gets mapped to one backend, and it stays there for the lifetime of the connection — potentially hours or days. Your load distribution degrades to essentially random, weighted by which clients happen to be most active. An L7 load balancer aware of HTTP/2 framing can distribute individual RPCs across backends regardless of which client connection they arrive on.

## How Health Checks Actually Work

A load balancer without health checks is just a traffic splitter. Health checks are what make it an *intelligent* traffic splitter — one that knows which backends can actually serve requests and which cannot.

**Active health checks** are probes the load balancer sends to each backend on a configured interval. The simplest form is a TCP connect check: the load balancer opens a TCP connection to the backend's port. If the connection succeeds, the backend is "healthy." If it fails or times out, it is "unhealthy." This tells you exactly one thing: a process is listening on that port. It tells you nothing about whether that process can serve a meaningful response.

An HTTP health check goes further: the load balancer sends an HTTP request (usually a GET to a specific path like `/healthz` or `/ready`) and checks the status code. A 200 means healthy; anything else means unhealthy. This tells you the application is running and can handle at least one request to a known endpoint. Some implementations also check the response body — useful if your health endpoint returns JSON with the status of downstream dependencies.

**Passive health checks** (sometimes called outlier detection) take a different approach: the load balancer observes real production traffic and tracks error rates per backend. If a backend starts returning 5xx responses or timing out above a threshold, the load balancer ejects it from the pool. This catches failures that active health checks miss — the backend that passes its `/healthz` check but fails on real requests due to a specific code path or data-dependent bug.

The most consequential configuration decisions are the **interval**, **threshold**, and **timeout**:

```
health_check:
  interval: 10s      # how often the LB probes
  timeout: 5s        # how long it waits for a response
  unhealthy_threshold: 3  # consecutive failures before removal
  healthy_threshold: 2    # consecutive successes before re-adding
```

With these settings, a backend that crashes takes at minimum `interval × unhealthy_threshold` = 30 seconds to be removed from the pool. During those 30 seconds, it receives traffic that fails. Make the interval too short and the thresholds too low, and a single network blip removes healthy backends, causing cascading capacity loss. This is a genuine tension, not an optimization problem with a clean answer.

### Shallow Versus Deep Health Checks

A **shallow health check** verifies the process is alive. A **deep health check** verifies the process can do useful work — it might test the database connection, check that a cache is reachable, or validate that a required configuration file is present.

Deep checks sound strictly better, but they create a coupling problem. If your health check queries the database and the database is slow for everyone, every backend fails its health check simultaneously, and the load balancer removes your entire fleet. You have converted a slow database into a complete outage. This is not hypothetical — it is one of the most common self-inflicted outages in production systems.

The practical pattern that works: use a **readiness check** that is moderately deep (tests critical dependencies) for initial registration — a backend should not receive traffic until it can actually serve — and a **liveness check** that is deliberately shallow for ongoing health monitoring. If the process is running and responsive, keep sending traffic. Let circuit breakers and retry logic in the application layer handle transient dependency failures.

## Tradeoffs and Failure Modes

**The gRPC/HTTP/2 trap.** This is the single most common operational mistake with load balancing layer choice. A team deploys a gRPC service behind a cloud provider's default L4 load balancer, observes that one backend is at 90% CPU while others idle, and spends days investigating the application before realizing the load balancer is routing all traffic from a high-volume client to one backend and never redistributing it.

**L7 as a single point of resource exhaustion.** Because an L7 load balancer terminates every connection and parses every request, a traffic spike that an L4 load balancer would handle without strain can saturate an L7 load balancer's CPU or memory. Slowloris attacks and similar slow-read techniques are specifically effective against L7 load balancers because they consume connection slots and memory buffers. If your L7 load balancer runs out of file descriptors or memory before your backends are saturated, the load balancer itself becomes the bottleneck.

**Health check–induced cascading failure.** When a shared dependency degrades, deep health checks can cause the load balancer to remove backends faster than the dependency recovers. Each removal concentrates more traffic on remaining backends, which increases their latency, which may cause them to fail their health checks too. The failure cascades until no backends remain. The root cause was not the dependency failure — it was a health check that converted a partial degradation into a total outage.

**The L4 observability gap.** Because L4 load balancers do not parse HTTP, they cannot emit per-request metrics like latency histograms, status code distributions, or error rates. You get connection-level metrics: new connections per second, active connections, bytes transferred. If you need the load balancer to be a point of observability (and in many architectures, it is the *only* convenient point of observability for inter-service traffic), L4 gives you almost nothing to work with.

**Connection draining at L4.** When a backend is being removed — due to a failing health check, a deploy, or a scale-down event — the load balancer should stop sending *new* work to it while allowing *existing* work to complete. At L7, this is straightforward: stop routing new requests, wait for in-flight requests to finish. At L4, the load balancer does not know when the current "request" on a connection is finished because it does not understand the protocol. It can only wait for the TCP connection to close, which for long-lived connections might be never. The result is either prematurely killing connections (causing errors) or waiting indefinitely (stalling deploys).

## The Mental Model

The distinction that matters is not "what fields can the load balancer read." It is **whether the load balancer owns the connection or just directs it**. An L4 load balancer maps flows to backends and gets out of the way — its resource cost is trivial, its routing is coarse, and its understanding of application state is zero. An L7 load balancer is a proxy that breaks every connection into two halves and actively participates in the conversation — it costs more, understands more, and can do more.

This means the decision is not really "L4 or L7." It is: does your architecture need the load balancer to understand the application protocol? If you are routing raw TCP connections, doing TLS passthrough, or handling protocols the load balancer does not speak, L4 is not the compromise — it is the correct choice. If you need path-based routing, per-request distribution, gRPC-aware balancing, or request-level retries, L7 is not a luxury — it is a requirement. And health checks are not a checkbox; they are a contract between the load balancer and your backends about what "able to serve" means, and getting that contract wrong is more dangerous than having no health checks at all.

## Key Takeaways

- Layer 4 load balancers route per-connection, not per-request — once a TCP connection is mapped to a backend, every byte on that connection goes to the same place, which makes them a poor fit for multiplexed protocols like HTTP/2 and gRPC.

- Layer 7 load balancers terminate the client's TCP (and TLS) connection and create a separate connection to the backend, making them full proxies with significantly higher resource requirements but the ability to make per-request routing decisions.

- Connection pooling at Layer 7 dramatically reduces the connection management burden on backends, which can matter as much as the routing flexibility in high-throughput architectures.

- Active health checks have an unavoidable detection delay of at least `interval × unhealthy_threshold` — during which the failed backend still receives and drops traffic — and tuning this tradeoff is a judgment call, not an optimization.

- Deep health checks that test downstream dependencies can convert a partial dependency degradation into a total outage by simultaneously removing all backends from the load balancer pool.

- Use moderately deep readiness checks to gate initial traffic to a new backend, and deliberately shallow liveness checks for ongoing health monitoring to avoid cascading ejection.

- If you need per-request observability (latency, status codes, error rates) at the load balancer layer, Layer 4 cannot provide it — you will need either Layer 7 or a separate instrumentation strategy.

- The load balancing layer decision is not a preference — it is determined by whether your architecture requires the load balancer to understand the application protocol, and getting this wrong produces failures that are obvious in retrospect but difficult to diagnose in the moment.

# Discussion

## Why This Conversation Is Happening

Load balancers sit in the path of production traffic, so when you misunderstand what kind of load balancer you are using, you do not get a small theoretical mistake — you get very concrete operational failures. A team puts gRPC behind an L4 balancer and one backend ends up overloaded while the rest sit mostly idle. Another team chooses L7 for convenience, then discovers the load balancer itself becomes the bottleneck during a traffic spike because it is terminating TLS and buffering requests for everyone. These are not edge cases; they fall directly out of how the two models work.

The reason this topic matters is that "L4 vs L7" is often taught as a routing-criteria distinction, which is true but misses the operational heart of the decision. The real question is whether your load balancer is merely steering packets or actually acting as a proxy. If you do not hold that model clearly, you will make bad choices around protocol support, health checks, observability, scaling, draining, and failure handling — and those choices usually fail under pressure, not in a clean test environment.

Health checks make this even more consequential. Engineers often treat them as harmless safety features, but they are really a control loop that decides who receives production traffic. Misconfigure them and the load balancer can amplify a partial failure into a total outage by removing healthy-enough backends faster than the system can recover.

## What You Need To Know First

**TCP connection**  
A TCP connection is a long-lived conversation between two endpoints, not a single request. Once established, many bytes can flow over it in both directions until one side closes it. This matters because an L4 load balancer makes a decision for the whole connection, while an L7 load balancer can make decisions for individual requests carried inside that connection.

**NAT / address rewriting**  
Network Address Translation means changing packet addresses as traffic passes through a device. In load balancing, this usually means the load balancer rewrites where traffic is going so packets end up at the chosen backend, then rewrites return traffic so the client thinks it is still talking to one service address. You do not need all the variants here; just hold the idea that packets can be redirected without the client or backend seeing the full original picture.

**Proxy vs pass-through device**  
A pass-through device forwards traffic onward without becoming one endpoint of the application conversation. A proxy actually accepts the connection from the client and then creates a separate connection to the backend. That distinction is the core of this topic: L4 behaves more like traffic steering, L7 behaves like a proxy.

**HTTP/2 or gRPC multiplexing**  
HTTP/2 allows many requests or streams to share one TCP connection at the same time. gRPC usually runs on top of this. This matters because if routing happens once per TCP connection, then many logically separate requests get stuck together and all land on one backend.

## The Key Ideas, Connected

**Layer 4 load balancing routes a connection once and then sticks with that choice.**  
At L4, the load balancer looks at transport-level information like IPs, ports, and protocol when the connection starts. It picks a backend for that flow, records the mapping, and sends all packets for that connection to the same place. The important part is not just what fields it inspects; it is that the decision is made at connection start and persists for the whole life of the connection. That sets up the next idea: because it only needs to steer packets, it does not need to become part of the conversation.

**Because L4 only steers packets, it does not terminate or understand the application protocol.**  
The backend is still the real TCP endpoint from the application's point of view, even if addresses are rewritten along the way. The load balancer keeps enough state to know which packets belong to which flow, but it is not maintaining request buffers, parsing HTTP, or tracking TLS session details the way a proxy does. That is why L4 can be extremely fast and cheap per connection. But that same "step aside after choosing" behavior creates a hard limit: if you never parse the conversation, you cannot make decisions based on anything inside it.

**Once the load balancer does not understand the conversation, routing is unavoidably per-connection rather than per-request.**  
This is the mechanism behind the usual L4 limitations. If ten HTTP requests travel over one TCP connection, L4 sees one flow, not ten units of work. If one long-lived gRPC channel carries hundreds of RPCs, L4 still sees one connection and sends all of it to one backend. So the failure mode with multiplexed protocols is not accidental misbehavior; it is the natural consequence of making a one-time routing decision for a transport connection that may carry many application requests.

**Layer 7 load balancing changes the model completely by terminating the client connection.**  
An L7 load balancer is not just reading more fields. It accepts the client's TCP connection itself, often terminates TLS too, decrypts the traffic, and parses the HTTP-level request. Then it opens or reuses a separate connection to a backend and forwards the request. This means there are now two connections: client-to-LB and LB-to-backend. That split is the key mechanical difference, and it is what makes the next capability possible.

**Once the load balancer is a proxy, the unit of routing becomes the request instead of the connection.**  
Because the L7 balancer can see where one request begins and ends, it can make backend choices request by request. One client connection can send multiple requests, and the load balancer can distribute them across the fleet. With HTTP/2 and gRPC, this is especially important because many streams share one TCP connection; L7 can still spread those streams around because it understands the framing above TCP. So the move from L4 to L7 is really a move from flow distribution to work distribution.

**Being a proxy also allows the load balancer to transform and manage traffic, not just route it.**  
Once the LB is parsing requests, it can add headers, rewrite paths, remove sensitive information, and attach client identity information like `X-Forwarded-For`. It can also retry a failed request on another backend in cases where doing so is safe, because it knows what a request is and can tell whether one failed before completion. L4 cannot do this, not because the feature is missing, but because it lacks the application boundaries needed to know what should be retried or modified.

**Those extra powers come from real work, so L7 has a fundamentally heavier resource profile.**  
Terminating TCP and TLS, parsing bytes, buffering data, holding state for both sides of the proxy, and managing many open sockets all consume CPU and memory. This is not implementation sloppiness; it is the cost of participating in every conversation. So L7 solves classes of problems L4 cannot solve, but in exchange the load balancer itself becomes a meaningful compute component that can saturate, run out of memory, or exhaust file descriptors.

**Because L7 owns backend-side connections, it can pool them and change the backend’s load shape.**  
A proxy can keep a smaller set of persistent connections open to backends and reuse them across many client requests. That means backends do not need to manage one connection per client. This can materially reduce connection churn, handshake overhead, and socket pressure on backend services. This is an underappreciated effect: choosing L7 is not only about richer routing; it can also simplify backend connection management.

**Health checks turn a load balancer from a distributor into a control system.**  
Without health checks, the load balancer just spreads traffic. With them, it continuously decides who is eligible to receive work. Active checks probe on a schedule; passive checks infer health from real traffic outcomes. The important mechanism is that these checks operate with delay and thresholds. A backend is not removed instantly when it fails; it is removed only after enough evidence accumulates. That means some bad traffic is unavoidable before detection.

**The health-check settings create a built-in tradeoff between fast detection and false ejection.**  
If checks are frequent and thresholds low, failures are detected sooner, but transient blips can cause healthy backends to be removed. If checks are conservative, healthy backends stay in rotation through minor issues, but truly dead backends continue receiving traffic longer. This is not a tuning puzzle with one best answer. It is a balance between two kinds of harm: sending traffic to broken nodes versus shrinking healthy capacity too aggressively.

**Deep health checks can create system-wide coupling that turns partial dependency trouble into full outage.**  
A shallow check asks "is this process alive and responsive?" A deep check asks "can this service do useful work right now, including its dependencies?" Deep checks seem smarter, but if every backend depends on the same database and that database slows down, then every backend may fail the same deep check together. The load balancer then removes the whole fleet, even though some requests might still have succeeded or degraded gracefully. The outage is amplified by the health policy, not just caused by the dependency problem.

**So the real design question is whether you need the load balancer to understand the protocol and own request boundaries.**  
If you need raw TCP pass-through, TLS passthrough, very high connection counts, or support for protocols the load balancer does not speak, L4 is often exactly right. If you need per-request routing, HTTP-aware behavior, request-level observability, gRPC balancing, header manipulation, or clean request draining, L7 is not optional. The layer choice is really a choice about how much application responsibility the load balancer should take on.

## Handles and Anchors

**1. Traffic cop vs interpreter**  
L4 is a traffic cop waving an entire car onto one road and then ignoring what happens inside. L7 is an interpreter sitting in every conversation, listening to each sentence and deciding what to do next. If you need decisions per sentence, a traffic cop cannot help you.

**2. Ask: "What is the unit of work my system cares about?"**  
If your system cares about TCP connections, L4 may fit. If your system cares about HTTP requests, RPCs, paths, headers, or per-request retries, you already need L7 behavior whether you say so explicitly or not.

**3. Core tension sentence**  
L4 is cheap because it stays ignorant; L7 is powerful because it stops being ignorant.  
That single sentence captures both the capability difference and the resource tradeoff.

## What This Changes When You Build

**An engineer who understands this will choose load-balancing layer based on routing unit, not feature checklist, because the real question is whether traffic should be distributed per connection or per request.**  
The unaware engineer often inherits the cloud default or chooses "simpler/faster" L4 for everything. That works until HTTP/2 or gRPC creates hot backends from long-lived client connections. The aware engineer asks early: "Will many requests share one connection, and do I need those requests spread across the fleet?"

**An engineer who understands this will capacity-plan an L7 load balancer like an active service component, because it terminates TLS, parses traffic, buffers data, and can become the bottleneck before backends do.**  
The unaware engineer treats the LB as lightweight network plumbing and scales only the application fleet. Then a surge hits, backend CPU remains available, but the proxy tier exhausts CPU, memory, or file descriptors first. The aware engineer monitors and scales the LB tier separately and includes handshake and buffering cost in performance tests.

**An engineer who understands this will design observability differently because L4 cannot provide request-level visibility.**  
The unaware engineer expects latency histograms, status code counts, or request error rates from an L4 layer and discovers too late that only connection metrics are available. The aware engineer either uses L7 where that observability is needed or deliberately builds instrumentation into the application and sidecars instead of assuming the load balancer can see requests.

**An engineer who understands this will treat health checks as failure-policy design, not boilerplate config, because interval, timeout, and thresholds determine both detection delay and the risk of false ejection.**  
The unaware engineer copies a health-check config from another service and calls it done. The aware engineer computes what those settings mean in wall-clock time, asks how many failed requests they are willing to tolerate before removal, and asks what kinds of transient issues should not cause ejection.

**An engineer who understands this will separate readiness from liveness and keep ongoing liveness checks shallow, because deep checks against shared dependencies can remove the whole fleet during partial degradation.**  
The unaware engineer makes `/healthz` verify database, cache, downstream APIs, and anything else "important," then wonders why a dependency slowdown caused every backend to disappear from rotation at once. The aware engineer uses readiness to block traffic until a node is truly able to start serving, but uses shallow ongoing checks so the load balancer does not turn dependency turbulence into a self-inflicted full outage.

