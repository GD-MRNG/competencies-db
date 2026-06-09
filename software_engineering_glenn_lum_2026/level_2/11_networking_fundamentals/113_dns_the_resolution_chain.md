## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers think of DNS as a single lookup: you ask for `api.example.com` and you get back `93.184.216.34`. A black box with a domain going in and an IP coming out. This mental model works fine right up until you're staring at an incident where half your users can reach your new service and the other half are still hitting the old IP, or where a domain you just registered returns `NXDOMAIN` for some clients but resolves perfectly from your laptop. The problem is not that DNS is complicated in the way distributed consensus is complicated. It's that DNS is a **delegation chain with caching at every layer**, and if you don't understand which layer is holding stale data or which server is authoritative for what, you cannot reason about what's happening. You can only guess and wait.

## The Query Lifecycle

When your application calls `getaddrinfo()` or your browser needs to resolve a hostname, the first thing that happens is not a network request. Your operating system checks its local DNS cache. If it finds a valid, unexpired record, the answer comes back in microseconds with no network activity at all. If it doesn't, your OS hands the query to a **stub resolver** — a deliberately simple piece of code whose only job is to forward the question to a **recursive resolver** and wait for the answer.

The stub resolver is not doing DNS resolution. It is asking someone else to do it. That someone else — the recursive resolver — is the workhorse of the entire system. This is typically a server operated by your ISP, your cloud provider, or a public service like `8.8.8.8` (Google) or `1.1.1.1` (Cloudflare). The recursive resolver is the one that actually walks the delegation chain on your behalf.

Here is what that walk looks like for a cold query — one where the recursive resolver has nothing cached — for `api.example.com`:

The recursive resolver starts by querying a **root nameserver**. There are 13 root server addresses (designated `a.root-servers.net` through `m.root-servers.net`), though behind those addresses sit hundreds of anycast instances distributed globally. The root server does not know the IP address of `api.example.com`. It doesn't even know who's responsible for `example.com`. What it knows is which nameservers are authoritative for the `.com` **top-level domain (TLD)**. It returns a **referral**: a set of NS records pointing to the `.com` TLD nameservers, along with their IP addresses.

The recursive resolver takes that referral and queries one of the `.com` TLD nameservers. That server also doesn't know the IP of `api.example.com`. But it does know which nameservers are authoritative for `example.com`. It returns another referral: NS records for `example.com`'s nameservers — something like `ns1.example.com` and `ns2.example.com` — and their corresponding IP addresses.

The recursive resolver now queries one of `example.com`'s **authoritative nameservers**. This server actually has the answer. It holds the zone file for `example.com`, and it returns an **A record** (or AAAA for IPv6) with the IP address of `api.example.com` and a **TTL** value.

The recursive resolver caches that answer, marks it with the TTL, and returns it to the stub resolver, which returns it to your application. The entire process — three to four network round trips across different servers operated by entirely different organizations — happens in tens of milliseconds for a cold lookup.

### Referrals, Not Forwarding

A critical distinction: root servers and TLD servers do not answer your query. They **refer** you to someone who might. Each step in the chain is a delegation — "I don't know, but this server is responsible for the next piece." The recursive resolver follows these referrals iteratively, one hop at a time, assembling the final answer itself.

This is why the recursive resolver is called "recursive" even though its behavior is technically iterative. From the stub resolver's perspective, it makes one request and gets back a complete answer — that's the recursion. Internally, the recursive resolver is performing an iterative walk through the delegation hierarchy.

### Glue Records and the Bootstrap Problem

There's a subtle chicken-and-egg problem in this chain. If the authoritative nameserver for `example.com` is `ns1.example.com`, how do you find the IP address of `ns1.example.com`? You'd need to query the authoritative nameserver for `example.com`, which is `ns1.example.com`, which you can't reach because you don't know its IP.

This is solved by **glue records** — A/AAAA records for nameservers that are included in the parent zone's delegation response. When the `.com` TLD server refers you to `ns1.example.com`, it also includes an additional section in the response containing `ns1.example.com → 198.51.100.1`. These glue records are maintained at the registrar level and are essential for the resolution chain to function. If your glue records point to an outdated IP, resolution for your entire domain breaks — and the error will look nothing like a "wrong IP" problem. It will look like your domain doesn't exist.

## How TTL Actually Works

TTL is an integer in a DNS response, expressed in seconds, that says: "you may cache this answer for this many seconds." When a recursive resolver caches a record with a TTL of 3600, it starts a countdown. After 3600 seconds, the record is evicted, and the next query for that name triggers a fresh walk through the delegation chain (or at least a query to the authoritative server, since the resolver likely still has the TLD and root referrals cached).

The important thing to understand is that TTL is **per-cache, per-record, and starts at cache insertion time**. There is no global clock. There is no coordination between resolvers. If Cloudflare's resolver caches your record at 14:00:00 and Google's resolver caches it at 14:02:30, those two caches will expire at different times. This is why the notion of DNS "propagation" is misleading — nothing is propagating. Independent caches are expiring at independent times, and when they do, they independently discover whatever the current authoritative answer is.

### TTL Does Not Mean What You Think During Migrations

Suppose your A record for `api.example.com` has a TTL of 86400 (24 hours) and points to `93.184.216.34`. You update it to point to `198.51.100.10`. The new TTL you set on the new record is irrelevant for the next 24 hours. Every recursive resolver that cached the old record will continue serving `93.184.216.34` until its local countdown expires. The TTL on your new record only governs how long the new answer gets cached after a resolver fetches it.

This is why the standard practice for DNS migrations is to **lower the TTL well in advance**. If you know you're going to change an IP address on Thursday, drop the TTL to 300 (five minutes) on Monday or Tuesday. By Thursday, all caches will have either expired their old long-TTL records and fetched the short-TTL version, or they'll expire within a few minutes. After the migration stabilizes, raise the TTL back up to reduce query load on your authoritative servers.

### Negative Caching

When a recursive resolver queries a name that doesn't exist, the authoritative server returns an **NXDOMAIN** response. This response is also cached, governed by the **SOA record's minimum TTL field** (sometimes called the negative TTL). If your SOA has a minimum TTL of 3600 and someone queries `typo.example.com` before you've created that record, resolvers will cache the "this doesn't exist" answer for up to an hour. If you create the record during that hour, those resolvers won't see it until the negative cache expires.

This bites hardest during initial service deployments. You set up a new subdomain, test it immediately from a machine that already queried it (and got NXDOMAIN), and conclude the DNS is broken. It isn't. Your resolver cached the negative response.

## Caching Beyond the Resolver

The recursive resolver is the most important cache in the chain, but it is not the only one. Your operating system maintains a DNS cache (visible on macOS with `sudo dscacheutil -flushcache`, on Linux it depends on whether `systemd-resolved` or `nscd` is running). Your browser maintains its own DNS cache (Chrome's is viewable at `chrome://net-internals/#dns`). Some application runtimes cache DNS results internally — the JVM, notoriously, caches DNS lookups indefinitely by default when a security manager is installed, controlled by `networkaddress.cache.ttl` in `java.security`.

Each of these caches operates independently with its own expiry logic. When you're debugging a resolution issue, you have to think about which cache you're actually testing. Running `dig @8.8.8.8 api.example.com` bypasses your OS cache and your browser cache — it queries Google's recursive resolver directly. Running `nslookup api.example.com` uses your OS's configured resolver. Curling the endpoint uses whatever your OS and potentially your runtime decide. These can all return different answers at the same point in time, and that's not a bug — it's the system working as designed.

## Tradeoffs and Failure Modes

### The TTL Tension

Low TTLs give you fast failover and migration agility. High TTLs reduce query volume against your authoritative servers and improve resolution latency for end users (cached answers are fast). There is no universally correct value. A TTL of 300 seconds is common for records that might change during incident response. A TTL of 86400 is reasonable for records that almost never change, like MX records. The cost of a low TTL is real: more queries hit your authoritative nameservers, more cold lookups add latency for users, and if your authoritative servers become unreachable, caches drain within minutes and your domain effectively vanishes. With a high TTL, an authoritative outage is invisible for hours because the world is still serving cached answers.

### Resolver Misbehavior

Not all recursive resolvers honor TTL faithfully. Some ISP resolvers impose a minimum TTL floor — even if you set a TTL of 60, they'll cache for 300. Some impose a maximum cap. Some enterprise resolvers serve stale records beyond their TTL if the authoritative server is unreachable (this is actually codified in RFC 8767 as "serve-stale"). You cannot assume that your TTL will be respected exactly. You can only set it and understand that it's a request, not a command.

### The Authoritative/Recursive Misconfiguration

One of the more insidious DNS failures happens when a server is configured to be both authoritative and recursive. It answers authoritatively for some zones and recursively for everything else. This creates cache poisoning vulnerabilities and unpredictable behavior. If you're running your own DNS infrastructure, your authoritative servers and your recursive resolvers should be separate systems with separate roles.

### CNAME Chains and Hidden Latency

A CNAME record doesn't resolve to an IP — it resolves to another domain name, which itself needs to be resolved. If `api.example.com` is a CNAME to `loadbalancer.cdn.example.net`, the resolver now has to resolve `loadbalancer.cdn.example.net` separately, potentially walking a different branch of the delegation tree. Stacking CNAMEs (a CNAME that points to another CNAME) multiplies this cost. Each link adds a potential cache miss and additional round trips. In latency-sensitive paths, an unnecessary CNAME chain is measurable overhead.

## The Mental Model

DNS is not a lookup. It is a hierarchical delegation system with independent caches at every layer. When you query a domain, you're walking a tree from the root to the specific zone that holds the answer, with each node in the tree only knowing the identity of the next node down. Every answer in this system has a shelf life (TTL), and that shelf life is enforced independently by every cache that holds a copy.

The practical consequence is that DNS changes are not atomic and not instant. They are **eventually consistent** across an unknowable number of independent caches, each running its own expiry clock. When you change a DNS record, you haven't changed what the world sees — you've changed what the world will *eventually* see, governed by TTLs you set in the past. Reasoning about DNS correctly means reasoning about cache state across time, not about the current value of a record.

## Key Takeaways

- DNS resolution is a delegation chain: stub resolver → recursive resolver → root server → TLD server → authoritative nameserver, with each step returning a referral to the next authority, not the final answer.

- The recursive resolver does all the real work. Your application's stub resolver just asks the recursive resolver and waits.

- TTL governs how long each independent cache holds a record. There is no coordination between caches — "DNS propagation" is actually independent caches expiring at different times.

- When preparing for a DNS migration, lower the TTL days in advance. The TTL on your *new* record doesn't help flush the *old* record from caches.

- Negative responses (NXDOMAIN) are cached too, governed by the SOA record's minimum TTL. Querying a name before the record exists will cause it to appear missing even after you create it.

- Multiple layers cache DNS results independently: browser, OS, application runtime (especially the JVM), and recursive resolver. When debugging, know which cache you're actually testing.

- Low TTLs buy agility but cost resilience: if your authoritative servers go down, low-TTL caches drain fast and your domain disappears. High TTLs are a buffer against authoritative outages.

- Not all resolvers honor your TTL. ISP resolvers may impose floors or caps, and some will serve stale records beyond TTL expiry. Your TTL is a request, not a guarantee.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

DNS only feels simple when nothing is changing. In steady state, “name in, IP out” is good enough to build features and move on. But production systems are full of change: cutovers, failovers, new subdomains, provider migrations, CDN onboarding, certificate validation, traffic steering. The moment a DNS answer differs depending on who asks, from where, and when, the black-box model stops being useful.

What breaks without a real model is not just troubleshooting speed — it is decision quality. You lower a TTL too late and your migration drags for a day. You test a new record from the wrong layer and conclude the change failed. You see NXDOMAIN from one client and a valid answer from another and treat it like randomness instead of cached state. DNS incidents often feel mysterious not because the system is unknowable, but because engineers are reasoning about it as a single lookup when it is actually a delegated, cached, time-dependent process.

If you hold the right problem in your head, the topic becomes much clearer: **when a hostname resolves, who is answering, who is merely referring you onward, and which caches are still holding an older view of reality?** That is the practical question the article is trying to equip you to answer.

## What You Need To Know First

### 1. Caching

A cache is just a temporary saved copy of an answer so you do not have to ask again every time. The important part here is that caches make systems faster, but they also mean different places can hold different answers for a while. For DNS, that is the whole game: the “current” answer on the authoritative server and the answer some resolver is still serving may not match yet.

### 2. Authority vs. possession

In distributed systems, the machine that has a copy of data is not always the machine allowed to define the truth. In DNS, an authoritative nameserver is the server that is allowed to say what records exist for a zone. A recursive resolver may have a cached copy of that answer, but it is not the source of truth; it is a temporary holder of previously fetched truth.

### 3. Hierarchy / delegation

Delegation means responsibility is handed down layer by layer. A higher layer does not need to know every final answer; it only needs to know who is responsible for the next layer. DNS is built exactly this way: root knows about TLDs, TLDs know about domains, domains know about their own records. If you miss this, the resolution path feels arbitrary; once you see it, the chain becomes predictable.

### 4. TTL as expiration, not synchronization

TTL is not a broadcast signal telling the internet to update. It is an expiration timer attached to a cached answer. Each cache starts that timer when it stores the answer. That means two resolvers can legitimately disagree for a period of time even if both are behaving correctly.

## The Key Ideas, Connected

### 1. DNS resolution is not one lookup; it is a chain of responsibility.

What this means is that when your app asks for `api.example.com`, the system is not consulting one global directory. It is moving through a hierarchy of actors, each of which knows only part of the path. This matters because failure or staleness can happen at different points in the chain, so “DNS is wrong” is too vague to be useful. Once you accept that DNS is a chain, the next question becomes: who actually walks that chain?

### 2. Your machine usually does not perform the real resolution work itself.

The OS or application typically uses a stub resolver, which is intentionally simple. Its job is mostly to ask a recursive resolver, “please go find the answer for me.” This is an important demotion of the client’s role: the client is usually not discovering root servers or TLD servers itself. That pushes the real work onto the recursive resolver, which is why understanding DNS means understanding what the recursive resolver does next.

### 3. The recursive resolver follows referrals, one layer at a time.

The recursive resolver starts high in the hierarchy and works downward. It asks the root, which points to `.com`; it asks `.com`, which points to the nameservers for `example.com`; then it asks the authoritative server for `example.com`, which can finally answer for `api.example.com`. The crucial idea here is that the earlier servers are not forwarding your query to the next hop for you. They are saying, in effect, “I am not the one who knows, but this is who you should ask next.” That leads to the distinction the article emphasizes: DNS is built on referrals and delegation, not magical end-to-end lookup.

### 4. Only the authoritative server defines the answer; the others help you reach it.

The root and TLD servers are like signposts, not encyclopedias. The authoritative nameserver is the server that owns the zone data and can say “the A record is this” or “that name does not exist.” This matters because when debugging, you need to separate “where truth lives” from “where a cached copy was served.” Once that distinction is clear, caching stops looking like a side detail and becomes central to understanding why answers differ over time.

### 5. Caching exists at multiple layers, and each layer has its own timer.

The recursive resolver caches. Your OS may cache. Your browser may cache. Your runtime may cache. Each layer can return an answer without asking the next layer if its cached copy is still considered valid. This means a DNS lookup is not always a network event at all. It also means that two tests run from different tools may be probing different caches rather than the same underlying truth. Once you see multiple independent caches, TTL becomes much more concrete.

### 6. TTL controls how long a cache may reuse an answer, but only from the moment that cache stored it.

This is the article’s key correction to the sloppy idea of “propagation.” TTL does not create a coordinated global switchover. It creates many local expiration deadlines. Resolver A may refresh at 2:00 PM; Resolver B may refresh at 2:07 PM. During that window, both can honestly return different answers. That naturally leads to the migration lesson: if old answers are already cached, changing the record now does not erase those old cached copies.

### 7. DNS changes are governed by past TTL decisions, not just present record values.

This is why lowering TTL at the time of the migration is too late. If resolvers cached the old answer yesterday with a 24-hour TTL, they are allowed to keep serving it until that timer expires, no matter what new TTL you put on the replacement record today. So operationally, DNS asks you to think ahead in time: if you want a fast cutover on Thursday, you need to make caches short-lived before Thursday. That same time-based reasoning also explains why even “nonexistent” answers can linger.

### 8. Negative answers are cached too.

If a resolver asks for a name before it exists and gets NXDOMAIN, that “does not exist” result can be cached just like a positive A record. So you can create the record afterward and still observe failures from some clients until that negative cache expires. This is a perfect example of why DNS problems often feel like contradictions: the authoritative state has changed, but some caches are still faithfully serving an older conclusion. Once you accept that, debugging becomes a matter of identifying which layer still holds the stale state.

### 9. Some DNS failures are really bootstrap or configuration failures, not “wrong answer” failures.

Glue records are the classic case. If the parent zone delegates to nameservers inside the child zone, the parent must also provide their IP addresses so resolvers can reach them. If that glue is wrong, the resolver may be unable to reach the authoritative server at all. The symptom is not usually “I got the old IP”; it is more like “the domain cannot be resolved.” This broadens the mental model further: DNS can fail because the answer is stale, because the answer is cached negatively, or because the chain itself cannot be traversed.

### 10. The practical mental model is “delegation tree plus independent caches over time.”

That is the connected picture the whole article is building toward. DNS is hierarchical, so answers are discovered by walking down delegated authority. DNS is cached, so what any client sees depends on which copy it is hitting and when that copy expires. Put those together and you get the operational truth: DNS is not atomic, not globally synchronized, and not instantly reversible. Engineering decisions around DNS are therefore decisions about cache behavior over time, not just record contents in a zone file.

## Handles and Anchors

### 1. DNS is a receptionist chain, not a phone book.

If you ask one receptionist for a person in a large organization, they may not know the person’s number — but they know which department to transfer you to. That department may transfer you again until you finally reach the team that owns the person you want. Root and TLD servers work like that: they do not know the final answer; they know who is responsible next.

### 2. TTL is a food expiration label, not a recall notice.

When you change a DNS record, you are not recalling every old copy from every cache. You are waiting for each cache’s existing copy to expire. Some fridges get stocked at different times, so they discard the old item at different times. That is why “propagation” is a misleading word: nothing is being pushed outward in lockstep.

### 3. The core tension is: agility vs. insulation.

Low TTL means you can change direction quickly, but you are also forcing the world to come back and ask more often. High TTL means the world can keep operating longer on cached answers, but it also means your changes take longer to show up. That one sentence explains most of the operational tradeoff.

## What This Changes When You Build

- An engineer who understands this will plan DNS cutovers days ahead, not minutes ahead, because the real constraint is the TTL already attached to cached old answers, not the new record they are about to publish.
- An engineer who understands this will test DNS changes with multiple methods on purpose — authoritative queries, direct queries to specific recursive resolvers, and application-level tests — because each method exercises a different cache layer and answers different debugging questions.
- An engineer who understands this will treat NXDOMAIN during rollout as a cache-state hypothesis before treating it as a provisioning failure, because a previously cached negative response can survive after the record has been created.
- An engineer who understands this will keep latency-sensitive hostnames free of unnecessary CNAME hops, because every alias can turn one logical lookup into additional delegated resolution work and extra cache-miss round trips.
- An engineer who understands this will choose TTLs based on failure posture, not habit: low TTL for records that may need rapid failover, higher TTL for stable records where insulating users from authoritative outages matters more than fast change.
- An engineer who understands this will separate authoritative and recursive DNS roles in infrastructure design, because mixing them blurs trust boundaries, creates confusing behavior, and increases the blast radius of misconfiguration.
- An engineer who understands this will verify glue and delegation any time nameserver records change, because some of the nastiest DNS failures are not bad endpoint records but broken reachability to the servers that are supposed to answer authoritatively.

</details>
