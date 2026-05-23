## Metadata
- **Date:** 23-05-2026
- **Source:** 08_networking.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-08 · Networking

Networking is the most common blind spot for developers moving into operational work, and it is the most consequential one. When you think about your code, you think in terms of function calls, objects, and data structures. When a request fails in production, the failure is almost never inside the code itself; it is in the path the request takes to reach the code, or the path the response takes to return from it. The reason most developers find this domain mysterious is not that it is genuinely complicated — it is that they have never been forced to think about it as a system with its own structure, designed by people solving specific problems in a specific historical order.

The single most important idea in networking is that everything is layered. A web request does not travel from your browser to a server in one step; it travels through a stack of protocols, each of which only knows about the one immediately below and immediately above it. Your application code speaks HTTP. HTTP rides on top of TCP, which guarantees that the bytes arrive in order. TCP rides on top of IP, which figures out how to route packets across networks it has never seen before. IP rides on top of whatever physical medium is available — Ethernet, Wi-Fi, fibre. Each layer is deliberately ignorant of the others. This ignorance is the design. It is what allowed the internet to scale across hardware nobody had imagined when the protocols were written, and it is why you can replace any single layer (say, swap HTTP/1.1 for HTTP/2) without rewriting everything else.

The two reference models you will encounter are the OSI model (seven layers, more theoretical) and the TCP/IP model (four or five layers, what the internet actually runs on). Treat them as two attempts to describe the same underlying principle: separation of concerns at the protocol level. The exact layer count matters less than the habit of asking, when something breaks, which layer it broke at. A DNS failure is a different problem from a TCP connection refusing to open, which is a different problem from a TLS handshake failing, which is a different problem from a 500 response from your application. The layers are diagnostic categories as much as architectural ones.

Above the routing layer, the central design choice is between TCP and UDP. TCP gives you a reliable, ordered stream — the bytes you send arrive, and they arrive in the order you sent them, or you get told the connection failed. UDP gives you fast, unreliable, unordered datagrams — you fire packets into the network and hope. Almost everything you interact with daily (web traffic, databases, SSH) runs on TCP because correctness matters more than latency. The exceptions (DNS queries, video streaming, real-time games) run on UDP because by the time TCP has retransmitted a lost packet, the moment has passed and the data is no longer useful. This choice — reliability or speed, never both — shapes every protocol built above.

On top of TCP sits HTTP, the protocol the web runs on. HTTP is request-response and stateless: each request is independent, the server is not expected to remember the last one. Statelessness is what makes HTTP scale; it is also what forces every web application to invent its own mechanism for sessions, authentication, and state. The evolution from HTTP/1.1 (one request per connection, mostly) to HTTP/2 (multiplexed streams over one connection) to HTTP/3 (built on UDP, not TCP, to escape head-of-line blocking) is a long argument about how to keep the semantics of HTTP while fixing the performance limits of the transport beneath it. REST, GraphQL, and most of what you call "API design" are conventions layered on top of HTTP semantics.

Two pieces of infrastructure deserve naming because their failure modes are disproportionately catastrophic. The first is DNS — the system that turns names like `example.com` into IP addresses. It is a globally distributed hierarchical database with caching at every level, which means it is fast when it works and confusing when it does not. A surprising fraction of "the site is down" incidents are DNS incidents. The second is TLS, which sits between TCP and HTTP and turns plain connections into encrypted ones. The TLS handshake establishes identity (via certificates issued by trusted authorities) and negotiates the keys for the rest of the conversation. HTTPS is not a cosmetic change to HTTP; it is HTTP wrapped in a separate cryptographic protocol with its own state machine, its own failure modes, and its own latency cost.

The skill this topic builds is the ability to reason about a system you cannot see. The network is invisible by design — the whole point of layered abstraction is that you do not have to think about IP routing when you write a function call. But when something fails, the abstraction tears, and the only people who can debug it are the ones who know what is underneath. Latency, retries, timeouts, partial failures, and the seemingly random unreliability of distributed systems are all symptoms of network behaviour. Once you can name the layer where a problem lives, most of the magic disappears.

## Level 2 candidates

**The OSI and TCP/IP models** — How layered protocol design works in detail, what each layer is responsible for, and how data is encapsulated as it travels down the stack and unwrapped on the way up. Worth deeper treatment because the layered model is the conceptual scaffolding everything else hangs from, and most practitioners know it only as a list to memorise rather than as a design principle.

**IP addressing and routing** — How packets actually find their way across the internet: subnets, CIDR, routing tables, and protocols like BGP that let independent networks coordinate without a central authority. Worth deeper treatment because it explains how the internet has no owner, why outages can cascade across continents, and why network configuration is harder than it looks.

**TCP vs UDP** — The mechanics of TCP's reliability guarantees (sequencing, acknowledgements, retransmission, congestion control, flow control) versus UDP's deliberate minimalism. Worth deeper treatment because the tradeoffs are not obvious until you understand what TCP is actually doing on your behalf — and what it costs.

**DNS** — How a hierarchical, cached, distributed name resolution system works in practice: root servers, authoritative servers, resolvers, TTLs, and the specific failure modes that emerge from caching at every level. Worth deeper treatment because DNS is involved in nearly every production incident and is poorly understood relative to its impact.

**HTTP and its evolution** — Request-response semantics, statelessness, methods and status codes, and the architectural shifts from HTTP/1.1 to HTTP/2 to HTTP/3. Worth deeper treatment because most application-level performance work above the transport layer is really an argument with HTTP's design choices.

**TLS and encryption in transit** — The handshake, certificate validation, the chain of trust through certificate authorities, and how session keys are negotiated. Worth deeper treatment because TLS is the protocol most developers depend on without ever inspecting, and its failure modes (expired certs, misconfigured chains, protocol downgrades) are common and instructive.

---

## Original Content

#### L1-08 · Networking

**What it is and why it matters:** Modern software is distributed by default. Understanding the network stack explains latency, explains why protocols are designed the way they are, and explains the failure modes that distributed systems are built to tolerate. Much of what feels like magic in web infrastructure is just layered protocol design.