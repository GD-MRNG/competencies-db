## Metadata
- **Date:** 01-01-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# 1.1 Networking Fundamentals

Networking is the most common blind spot for developers moving into operational work, and it is the most consequential one. When a developer thinks about their code, they tend to think in terms of function calls, objects, and data structures. When a request fails in production, however, the failure is almost never inside the code itself; it is almost always in the path the request takes to reach the code, or the path the response takes to return from it.

You need to develop a mental model of the **request path**: the sequence of hops a user's request makes from their browser or client all the way to your application and back. That path typically looks something like this: the user's device sends a request to a **DNS resolver**, which translates a human-readable domain name into an IP address. That IP address points to a **CDN or edge node**, which may serve a cached response immediately. If not cached, the request flows through to a **load balancer**, which distributes incoming traffic across multiple instances of your service and provides health checking (removing unhealthy instances from rotation). From the load balancer, the request reaches a **reverse proxy**, which may handle TLS termination (decrypting the encrypted HTTPS traffic), route requests based on URL patterns, and forward them to the appropriate backend service. From there, the request reaches your application, which may itself make calls to a **database**, a **cache**, or another **internal service**.

Every link in this chain is a potential failure point. "The service is down" is almost never the full picture. The service may be perfectly healthy but unreachable because a firewall rule is blocking the port. The service may be receiving the request but failing because it cannot reach its database through the internal network. The service may be slow because the DNS resolution is taking too long or because TLS renegotiation is happening on every request.

The concepts you need to understand concretely are as follows. **DNS** is the system that maps domain names to IP addresses; you need to understand TTLs (how long DNS records are cached) because they affect how quickly changes propagate. **Load balancers** operate at different layers: a layer 4 load balancer routes based on IP and TCP, while a layer 7 load balancer can route based on HTTP headers, paths, or cookies, which is more powerful but more complex. **TLS** is the encryption protocol used for HTTPS; you need to understand certificate management, expiry, and renewal because an expired certificate will take down your service as completely as any code bug. **Network segmentation** is the practice of placing services in different network zones based on their sensitivity, so that a public-facing web server cannot directly connect to a production database without passing through a controlled network boundary. **Firewalls and security groups** are the rules that enforce what traffic is permitted to flow between network zones; misconfiguring them is one of the most common causes of "the service can't reach the database" failures.

The practical skill this builds is the ability to trace a failing request through the network topology and identify at which layer the failure is occurring, long before you look at application code.

## Level 2 candidates

**The OSI Model and TCP/IP Stack**

The conceptual framework that explains how data moves through layers from application to wire. It matters because every networking problem you will ever debug is a failure at a specific layer, and knowing the model tells you where to look and what questions to ask.

**IP Addressing and Subnetting (CIDR)**

How the address space is divided into networks and sub-networks using prefix notation. It matters because every cloud environment forces you to design a network topology before you deploy anything, and a wrong subnet decision is expensive to undo.

**DNS: The Resolution Chain**

How a domain name travels through recursive resolvers, root servers, and authoritative nameservers to become an IP address, and how TTL controls propagation. It matters because a misconfigured or slow DNS chain is one of the most common causes of service availability problems and deployment failures.

**TCP vs UDP: The Reliability Tradeoff**

How TCP provides ordered, acknowledged delivery through the three-way handshake and congestion control, versus UDP's stateless fire-and-forget model. It matters because the choice of transport protocol determines the failure characteristics of any service, and understanding this tradeoff is prerequisite to reasoning about timeouts, retries, and connection pooling.

**HTTP and TLS: The Application Layer in Detail**

The request-response model, how TLS adds encryption and authentication on top of TCP, and what actually happens during a TLS handshake. It matters because virtually every service interaction you will build or debug runs over HTTPS, and certificate errors, redirect chains, and header behavior are daily operational realities.

**Load Balancing: Layer 4 vs Layer 7**

The distinction between routing traffic based on connection metadata versus routing based on application-level attributes like URL path or host header, and how health checks make load balancers aware of backend state. It matters because nearly every production architecture puts a load balancer in front of services, and choosing the wrong layer or misconfiguring health checks has direct consequences for reliability.

**Network Security Boundaries: Firewalls, Security Groups, and NACLs**

How traffic filtering works at stateful versus stateless layers and how ingress and egress rules define what is permitted across network boundaries. It matters because cloud infrastructure requires you to explicitly open every communication path, and understanding the filtering model is essential to both security and debugging connectivity failures.

**NAT and Private Networking**

How private RFC-1918 address space is translated to a public routable address for outbound traffic, and why services in private subnets require a gateway to reach the internet. It matters because most production infrastructure places workloads in private networks for security, and understanding NAT explains why outbound connections behave differently from inbound ones and where routing failures originate.

---

# Discussion

## Why This Conversation Is Happening

When software leaves your laptop and starts serving real users, it stops living in a neat world of direct function calls. A user request has to cross a chain of systems before your code ever sees it: DNS, edge caches, load balancers, proxies, firewalls, internal networks, and only then your application. If you do not have a mental model of that path, production failures look random. You see “timeout,” “502,” or “can’t connect,” but you cannot tell whether the problem is your code, the network, or something in between.

This matters because many operational failures are not application bugs at all. The app may be healthy, but traffic may be routed to the wrong place, blocked by policy, slowed by repeated handshakes, or still pointing at an old IP because DNS has not updated everywhere yet. Without networking fundamentals, engineers often debug the wrong layer first, which turns a fixable outage into a long and confusing incident.

The real payoff of understanding this topic is speed and precision under pressure. Instead of asking “is the service down?”, you start asking “where along the request path is it failing?” That shift is what makes production systems feel diagnosable rather than mysterious.

## What You Need To Know First

### 1. IP address

An IP address is the network location of a machine or service. If a domain name is the label humans use, the IP address is what the network actually uses to deliver traffic. You do not need deep routing theory here; you just need to know that traffic ultimately has to be sent to a concrete address.

### 2. HTTP request and response

A request is a client asking for something; a response is the server replying. In development, this can feel like “the browser calls my app.” In production, that request may pass through several systems before the app handles it, and each of those systems can inspect, forward, cache, reject, or reshape the traffic.

### 3. Ports

A port is a numbered entry point on a machine for a particular kind of service. Two machines being reachable on the network is not enough; the correct port must also be open and allowed. This is why “the server is up” and “the application is reachable” are different claims.

### 4. Caching

Caching means storing a previous result so it can be reused instead of recomputed or refetched. In networking, this shows up in places like DNS and CDNs. The useful idea is simple: caches make things faster, but they also make changes take time to show up everywhere.

## The Key Ideas, Connected

**A production request follows a path, not a jump.**

What this means is that a user does not connect “straight to your app” in the way developers often imagine. The request moves hop by hop through multiple systems, each with a distinct job. That matters because once you accept that there is a path, you can stop treating failures as one undifferentiated event. And that leads directly to the next idea: you need to know what those hops actually do.

**Each hop in the path exists to solve a specific problem.**

DNS translates a human-friendly name into an IP address. A CDN or edge node may answer the request from cache to reduce latency and offload origin traffic. A load balancer spreads traffic across multiple service instances and avoids sending traffic to unhealthy ones. A reverse proxy can terminate TLS, inspect HTTP details, and route traffic to the right backend. Your application then does its work, often by making further calls to databases, caches, or internal services. Once you see that each layer has a job, you can also see that each layer can fail in a different way, which is the next step.

**A failed request does not mean the application is broken.**

“The service is down” is often an overly compressed description. A request can fail because the name resolved to the wrong address, because a cache is stale, because the load balancer thinks all targets are unhealthy, because TLS is broken, because a firewall blocks the port, or because the app cannot reach something it depends on. This is the core operational shift: the symptom appears at the user boundary, but the cause may live anywhere along the chain. Once you accept that, you need a way to distinguish one kind of failure from another, which is why the article introduces the key networking concepts concretely.

**DNS matters because name changes do not become true everywhere at once.**

DNS maps names to IPs, but the important operational idea is TTL: how long resolvers and clients may keep using a cached answer. If you change where a service points, some parts of the world may still use the old destination until that cache expires. That means a rollout or failover can appear partially broken even when your new target is healthy. Understanding DNS introduces a broader lesson: some network layers remember past decisions, so changes propagate over time rather than instantly. From there, the next concept is about what happens after traffic finds the right destination.

**Load balancers decide where traffic goes, and the layer they operate at changes what decisions they can make.**

A layer 4 load balancer works with lower-level connection information like IP and TCP. A layer 7 load balancer understands HTTP details such as paths, headers, or cookies, which lets it do smarter routing. The tradeoff is capability versus complexity. If you route by URL path or need sticky behavior based on application-level data, layer 7 can help; if you only need simpler connection distribution, layer 4 may be enough. This matters because “traffic reached the service boundary” still does not mean it reached the correct backend in the correct way. That naturally leads to TLS and reverse proxies, which often sit at that boundary.

**TLS protects traffic, but it also introduces operational state that must be managed.**

TLS is what makes HTTPS encrypted, but in practice you must manage certificates: obtaining them, renewing them, and ensuring they are valid and not expired. If certificate handling fails, users experience your service as down even if the application is perfectly healthy. TLS also often gets terminated at a reverse proxy or load balancer, meaning the encryption concerns may live outside the app process itself. This reinforces the central pattern: user-visible availability depends on more than application code. Once traffic is decrypted and routed, though, there is still another concern: not every part of your system should be able to talk to every other part.

**Network segmentation exists to limit what can talk to what.**

Instead of placing all services on one flat network, engineers create zones and boundaries. Public-facing systems may accept internet traffic, while sensitive systems like production databases sit behind tighter controls. The point is not just organization; it is risk reduction. If a public server is compromised, segmentation helps prevent direct movement to the most sensitive resources. But a boundary only matters if something enforces it, which leads to firewalls and security groups.

**Firewalls and security groups turn intended boundaries into actual allowed or denied traffic.**

These rules specify which sources can connect to which destinations on which ports. They are one of the most common causes of operational confusion because everything may look healthy in isolation: the app is running, the database is running, yet the app still cannot connect. The missing piece is that reachability is policy-controlled. This connects back to the earlier idea that “up” and “reachable” are different states. Once you understand that, the final practical conclusion follows.

**The real skill is tracing the request until you find the layer where reality diverges from expectation.**

You do not begin by reading application code. You begin by asking: did DNS resolve correctly? Did the request hit the edge? Did the load balancer have healthy targets? Did TLS succeed? Did the proxy forward it? Could the app reach its dependencies? This is the working internal model the article is trying to build. Networking fundamentals are not a bag of terms; they are the map that lets you localize failure.

## Handles and Anchors

### 1. Think of a request like a traveler changing vehicles

A traveler may take a taxi to a station, a train to a city, a shuttle to a building, and an elevator to an office. If they never arrive, “the office is broken” is a bad diagnosis. The problem may be the ticket, the station, the route, the gate, or the final door. A network request works the same way: each hop hands it off to the next.

### 2. “Healthy” is not the same as “reachable”

This is the sentence to keep. A service can be running perfectly and still be unavailable to users because traffic cannot find it, is not allowed to reach it, or fails before it gets there.

### 3. Networking is about narrowing the gap between where traffic should go and where it actually goes

That is the operational tension underneath the whole topic. Configuration says one thing, caches remember another, policies allow some paths and deny others, and failures happen where those differ.

## What This Changes When You Build

- An engineer who understands this will investigate an outage by walking the request path layer by layer because a user-facing error often originates before the application ever receives the request.
- An engineer who understands this will plan DNS changes differently because TTL means cutovers, failovers, and rollbacks do not propagate instantly, so “we changed it” does not mean “everyone sees the change now.”
- An engineer who understands this will choose load-balancing behavior more deliberately because routing at layer 7 enables path- or header-based decisions, while layer 4 keeps the system simpler when application-aware routing is unnecessary.
- An engineer who understands this will treat certificate renewal and expiry monitoring as core availability work because an expired TLS certificate can create a total outage even when every service process is healthy.
- An engineer who understands this will debug service-to-database failures by checking network policy and segmentation early because “connection refused” or “timeout” often comes from firewall or security-group rules, not from a broken database engine.