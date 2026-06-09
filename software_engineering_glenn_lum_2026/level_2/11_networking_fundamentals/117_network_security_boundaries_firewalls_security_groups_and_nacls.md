## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers treat security groups, NACLs, and firewall rules as roughly the same thing: a list that says "allow traffic on port 443" or "block everything else." When traffic flows, they move on. When traffic doesn't flow, they start toggling rules until it does. This works until it doesn't — and when it doesn't, the failure is usually invisible and confusing, because the engineer is working from a mental model where all filtering works the same way. It does not. There are two fundamentally different filtering models operating simultaneously in most cloud environments, and they behave differently in ways that matter enormously for both security posture and debugging. The distinction is not academic. It is the difference between configuring one rule and having traffic flow, versus configuring one rule and watching packets vanish into silence on the return path.

## Two Filtering Models, Not One

Every packet that moves between resources in a cloud VPC passes through at least two independent filtering layers. In AWS, these are **security groups** and **network access control lists (NACLs)**. In other cloud providers the names differ, but the architectural pattern is consistent: one layer is stateful, the other is stateless. They evaluate traffic using entirely different logic, they attach at different points in the network topology, and they make different demands on the operator. Understanding what "stateful" and "stateless" actually mean at the packet level is the single most important conceptual prerequisite for working with network security boundaries.

### Stateful Filtering: Connection Tracking

A **stateful** filter — security groups in AWS, NSGs in Azure — maintains a **connection tracking table**. When a packet arrives and matches an allow rule, the filter records the connection tuple: source IP, source port, destination IP, destination port, and protocol. From that point forward, any packet that belongs to the same connection — including return traffic flowing in the opposite direction — is automatically permitted without being evaluated against the rules again.

Here's what that means concretely. You have an EC2 instance in a security group that allows inbound TCP on port 443 from `0.0.0.0/0`. A client sends a SYN packet to your instance on port 443. The security group evaluates the inbound rules, finds a match, and allows the packet through. It also creates a tracking entry for this connection. When your instance sends back its SYN-ACK — which is now *outbound* traffic from the instance, originating from port 443 and destined for the client's ephemeral port — the security group does not evaluate the outbound rules. It recognizes this packet as return traffic for a tracked connection and passes it through automatically.

This is why, with security groups, you can configure an inbound rule for port 443 and have a working HTTPS service without touching the outbound rules. The return path is implicit. The security group is not evaluating two independent rule sets for two directions; it is tracking connections and using that state to exempt return traffic from evaluation.

The tracking table is not infinite. Entries expire after a timeout — typically around 350 seconds for established TCP connections and shorter for UDP. If a connection is idle long enough for the tracking entry to expire, subsequent packets will be evaluated against the rules as if they were new. This is why you can sometimes see long-lived idle connections break through a security group: the SG dropped the tracking entry, and there is no rule to re-admit the packet.

### Stateless Filtering: Per-Packet Evaluation

A **stateless** filter — NACLs in AWS — has no memory. It does not track connections. Every single packet, whether it is the first SYN of a new connection or the ten-thousandth data packet of an ongoing transfer, is evaluated independently against the rule set. Inbound packets are evaluated against inbound rules. Outbound packets are evaluated against outbound rules. There is no concept of "return traffic."

This has a critical practical consequence: **ephemeral ports**. When your server responds to an HTTPS request, the return packets are not sent *from* port 443 *to* port 443. They are sent from port 443 to whatever ephemeral port the client's operating system chose when it opened the connection — typically a port in the range 1024–65535 (the exact range varies by OS). In a stateful filter, this is invisible to you; connection tracking handles it. In a stateless filter, you must explicitly allow outbound traffic to those ephemeral ports, or your response packets will be silently dropped.

A concrete example: you configure a NACL to allow inbound TCP on port 443 from `0.0.0.0/0`. Traffic arrives. Your application processes it and sends a response. That response is an outbound packet from port 443 to, say, port 52344 on the client. The NACL evaluates this outbound packet against the outbound rules. If there is no outbound rule permitting TCP traffic to the ephemeral port range, the packet is dropped. The client sees a timeout. Your application logs show a successful response. Everything looks fine on the server side, and the client gets nothing.

This is the single most common failure mode with NACLs, and it catches experienced engineers because it is counterintuitive if you've been working exclusively with security groups.

### Rule Evaluation: Order vs. Aggregate

The two models also differ in *how* rules are evaluated, and this difference changes what "adding a rule" means.

**Security groups** evaluate all rules as an aggregate. There are no rule numbers, no ordering, and no deny rules. Every rule is an allow rule. If any rule permits the traffic, the traffic is allowed. If no rule matches, the traffic is denied by the implicit default-deny. This means security groups are purely additive: adding a rule can only make the group *more* permissive, never less. You cannot create a security group rule that says "allow all of `10.0.0.0/16` except `10.0.0.47`." The model does not support it.

**NACLs** evaluate rules in order by rule number, lowest first. The first rule that matches determines the outcome — allow or deny — and evaluation stops. This means rule ordering is load-bearing. A deny rule at number 100 takes precedence over an allow rule at number 200, even if the allow rule is more specific. This gives NACLs more expressive power: you *can* block a specific IP within a broader allowed range. But it also means that a carelessly numbered rule can silently override rules that appear later in the list.

```
# NACL rules evaluated in order:
Rule 100: DENY  TCP  port 22  from 0.0.0.0/0
Rule 200: ALLOW TCP  port 22  from 10.0.0.0/16

# Result: ALL SSH is denied, including from 10.0.0.0/16.
# Rule 100 matches first and evaluation stops.
```

To get the intended behavior — block external SSH but allow internal — you'd need to reverse the order or renumber:

```
Rule 100: ALLOW TCP  port 22  from 10.0.0.0/16
Rule 200: DENY  TCP  port 22  from 0.0.0.0/0
```

### Where Each Layer Attaches

Security groups attach to **elastic network interfaces** (ENIs) — which in practice means they attach to individual instances, containers, Lambda functions, RDS instances, or any other resource with a network interface. A single ENI can have multiple security groups applied, and their rules are aggregated (union of all allow rules across all groups).

NACLs attach to **subnets**. Every packet entering or leaving a subnet passes through the NACL. A subnet has exactly one NACL at a time. This means NACLs operate as a perimeter control around a network segment, while security groups operate as a per-resource control.

The evaluation sequence for a packet moving between two instances in different subnets within the same VPC is: **outbound security group of the source → outbound NACL of the source subnet → inbound NACL of the destination subnet → inbound security group of the destination**. For two instances in the *same* subnet, NACLs are still evaluated if traffic crosses the subnet boundary, but the behavior depends on whether the traffic is routed through the VPC router or stays within the subnet — in AWS, even intra-subnet traffic passes through NACLs.

This layering means a packet must be permitted by *both* layers to flow. Security group allows it but NACL denies it? Blocked. NACL allows it but security group denies it? Blocked. They are independent, and the most restrictive layer wins.

### Security Group References: Filtering by Identity

One mechanism that is genuinely non-obvious and extremely powerful in practice is **security group referencing**. Instead of writing a rule that allows traffic from an IP range, you can write a rule that allows traffic from any resource that is a member of a specific security group.

```
# Instead of:
Allow TCP 5432 from 10.0.1.0/24

# You write:
Allow TCP 5432 from sg-0abc1234 (the "web-servers" security group)
```

This decouples your security rules from your IP topology. When you auto-scale your web tier and new instances launch with new IP addresses, they are automatically permitted to reach the database because they inherit the "web-servers" security group. You don't need to update any rules. The security group acts as an identity tag that the filtering layer understands natively.

This is the mechanism that makes security groups the primary tool for east-west traffic control within a VPC, and it is the main reason NACLs are often left at their permissive defaults for intra-VPC traffic. Managing IP-based NACL rules across a dynamic, auto-scaling fleet is operationally expensive and fragile. Security group references solve the same problem with zero ongoing maintenance.

## Where This Breaks

### The Ephemeral Port Trap

Already described above, but worth emphasizing as a failure mode: any time you tighten NACL outbound rules beyond "allow all," you risk breaking return traffic for every inbound service. This failure is silent on the server side, presents as a timeout on the client side, and does not appear in any application log. VPC Flow Logs will show the packet as `REJECT` on the outbound NACL evaluation, but only if you have flow logs enabled and know to look at the outbound direction for what appears to be an inbound connectivity problem.

### The "It Worked Yesterday" Problem

Security group connection tracking entries expire. An application that maintains a pool of long-lived database connections might work perfectly for days, then start failing after a deployment that restarts the connection pool — because the new connections are being established during a window when some other change (a modified security group rule, a briefly detached ENI) causes them to fail. Worse, if you modify a security group rule, existing tracked connections are *not* re-evaluated. The old connection continues to work under the old rule until it closes or its tracking entry expires. This means your rule change "takes effect" immediately for new connections but has no visible effect on existing ones, which makes testing changes in production misleading.

### Egress as a Blind Spot

Most engineers think about ingress: what traffic can reach my service? Egress — what traffic can leave — gets far less attention, and this creates two problems. First, the security problem: a compromised instance with unrestricted egress can exfiltrate data to any endpoint on the internet. Egress filtering is one of the most effective controls against data exfiltration and command-and-control communication. Second, the operational problem: when a service cannot reach an external API, DNS server, or package repository, the cause is often an egress rule that nobody thought to configure, because the mental model was entirely focused on "letting traffic in."

### Debugging Across Two Layers

When connectivity fails and both security groups and NACLs are in play, the debugging surface doubles. A common pattern is an engineer verifying that the security group allows the traffic, confirming it looks correct, and then spending hours reviewing application configuration — because they forgot NACLs exist. The inverse also happens: someone troubleshoots NACLs and forgets that security groups on the *destination* resource are a separate check. VPC Flow Logs help, but they report the *aggregate* verdict, not which layer caused the rejection. Isolating the layer requires methodically checking each one, or temporarily setting one layer to fully permissive to rule it out.

## The Mental Model

Think of network security boundaries as two concentric filtering systems with fundamentally different architectures. The outer layer (NACLs, or any stateless perimeter filter) is a packet-level gatekeeper: it inspects each packet in isolation, cares about both directions independently, and requires you to understand the full bidirectional flow of traffic including ephemeral ports. The inner layer (security groups, or any stateful instance-level filter) is a connection-level gatekeeper: it evaluates the first packet of a connection and then remembers it, freeing you from managing return traffic but binding you to the characteristics and limitations of connection tracking.

When traffic fails, your first question should be: which layer is rejecting it, and is the rejection happening on the forward path or the return path? Most connectivity problems that look mysterious stop being mysterious once you ask that question, because the answer forces you to reason about the specific filtering model — stateful or stateless — that applies at the point of failure.

## Key Takeaways

- **Stateful filters** (**security groups**) track connections and automatically permit return traffic; **stateless filters** (**NACLs**) evaluate every packet independently, including responses, and require explicit rules for both directions.

- With **NACLs**, forgetting to allow outbound traffic to the **ephemeral port range** (1024–65535) will silently drop your server's responses while the server itself logs no errors — the failure only manifests as a **client-side timeout**.

- **Security group rules** are unordered and purely additive (allow-only with implicit deny), while **NACL rules** are evaluated in **numeric order** with **first-match-wins** semantics, making rule numbering load-bearing.

- **Security group rule changes** apply immediately to new connections but do not re-evaluate **existing tracked connections**, which means the effect of a change may not be fully visible until old connections close or their **tracking entries** expire.

- **Security groups** attach to individual **network interfaces** (per-resource), **NACLs** attach to **subnets** (per-segment), and a packet must be permitted by both layers to flow — the **most restrictive layer** wins.

- **Security group references** allow rules based on **group membership** rather than IP addresses, making them the primary tool for **east-west traffic control** in dynamic, **auto-scaling environments** where IP-based rules are fragile.

- **Egress rules** are the most common blind spot: unrestricted egress is both a security liability (**data exfiltration**) and an operational debugging gap (**outbound connectivity failures** that nobody thought to check).

- When debugging connectivity failures across both layers, **VPC Flow Logs** report the **aggregate verdict** but not which layer caused the rejection — **isolating the responsible layer** requires methodical per-layer verification.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

A lot of cloud network debugging goes wrong because engineers compress different mechanisms into one vague category: “firewall rules.” That mental shortcut is cheap when things are working, but expensive when they are not. You open port 443, the app still times out, and now you are changing rules by trial and error because you do not know whether the problem is on the way in, the way out, or only on return traffic.

The practical failures are specific and ugly. A server receives a request, processes it successfully, and sends a response — but the client never gets it because a stateless filter dropped the return packet on an ephemeral port. A rule change appears to work in testing but not for existing sessions because a stateful filter is still honoring old tracked connections. An engineer checks the instance-level rules, sees they allow traffic, and loses hours in app logs because the subnet-level filter was the real blocker.

If you do not hold the difference between stateful and stateless filtering as a real mechanism, cloud networking feels arbitrary. If you do hold it, a lot of “mysterious” connectivity failures become predictable: you know where to look, what kind of mistake is even possible, and what sort of fix will actually work.

---

## What You Need To Know First

**1. TCP connections and bidirectional traffic**  
Most application traffic is not one-way. A client opens a connection to a server by sending packets to the server’s listening port, and the server replies back to the client. Even if you think of the service as “inbound on 443,” the actual exchange is bidirectional: request packets go one direction, response packets go the other. Any filter that treats directions separately can break one half while leaving the other half intact.

**2. Ports and ephemeral ports**  
A server usually listens on a known port like 80, 443, or 5432. A client, when it initiates a connection, uses a temporary source port chosen by its OS. That temporary source port is called an ephemeral port. So a reply from the server usually does not go back to port 443 on the client; it goes to some high-numbered client port. This matters because stateless filters need explicit permission for that return traffic.

**3. Network interfaces and subnets**  
A network interface belongs to a specific resource: an instance, database, container host, and so on. A subnet is a network segment that contains many resources. A filter attached to an interface acts close to one resource; a filter attached to a subnet acts around everything in that segment. That attachment point determines both what the filter protects and how broadly a mistake can break traffic.

**4. Default deny**  
These systems usually work from “allow what is explicitly permitted; deny everything else.” That means missing a necessary rule is enough to break traffic. You do not need a special deny statement to cause failure — absence of allowance is already a block.

---

## The Key Ideas, Connected

**There are two different filtering models in cloud networks, not one.**  
The article’s core point is that security groups and NACLs are not two versions of the same thing. They solve related problems using different mechanics. If you flatten them into “lists of allowed ports,” you miss the behavior that actually decides whether packets flow. That matters because the first big distinction — stateful versus stateless — changes what counts as a complete rule set. Once you see that, the rest of the differences start to make sense instead of feeling arbitrary.

**A stateful filter remembers allowed connections and uses that memory to permit return traffic.**  
A stateful filter does not just inspect a packet in isolation. When the first packet of a new connection is allowed, the filter records enough information to recognize later packets from that same connection. That record is the connection tracking state. Because of that stored state, reply packets do not need to independently match a separate opposite-direction rule. This is why allowing inbound HTTPS on a security group is often enough for a functioning service: the incoming packet creates tracked state, and the outgoing reply is recognized as part of that same conversation. That memory is exactly what stateless filters do not have, which is why the next idea becomes necessary.

**A stateless filter has no memory, so every packet must be valid on its own.**  
A stateless filter evaluates each packet as if it has never seen anything before. It does not know whether a packet is opening a connection, continuing one, or returning from one. That means the return packet from your server is not “obviously okay” just because the request packet was allowed earlier. It must separately match outbound rules. This changes the operator’s job: you are no longer permitting a connection, you are permitting both directions of a packet flow. Once you reason at packet level instead of connection level, ephemeral ports stop being a detail and become operationally important.

**Ephemeral ports are the practical trap created by stateless filtering.**  
When a client connects to server port 443, the return packet does not go to client port 443. It goes to the client’s temporary source port — some high-numbered ephemeral port. In a stateful filter, that complexity is hidden by connection tracking. In a stateless filter, it is your responsibility to allow it. That is why a NACL with “allow inbound 443” can still break HTTPS: the request enters, but the response packet gets evaluated outbound and dropped because the destination is an ephemeral client port that your rules did not allow. This is not a corner case; it is the normal shape of client-server traffic. Once you understand that stateless filters force you to model both directions explicitly, the next question is how they decide which rule applies.

**Stateful and stateless filters also differ in rule evaluation semantics.**  
Security groups are additive allow-lists. There is no ordered rule processing and no explicit deny rule; if any rule allows the traffic, it passes. That means adding a security group rule can only increase access. NACLs work differently: rules are numbered, checked in order, and the first match wins, whether it is allow or deny. That gives NACLs more expressive power — they can carve out exceptions inside broader ranges — but it also makes rule order load-bearing. The mechanism matters: in an ordered system, a broad deny early in the list can silently override a more specific allow later. Once you see that these layers think differently about traffic, it becomes important to know where they sit in the network.

**The attachment point of each filter tells you what scope it controls.**  
Security groups attach to network interfaces, so they act as per-resource controls. NACLs attach to subnets, so they act as per-segment controls. This is why security groups are usually the precise tool for controlling which workloads can talk to which other workloads, while NACLs are broader perimeter controls around a subnet. The placement also explains why both can affect the same packet without being redundant: one check happens at the resource boundary, another at the subnet boundary. Because they are independent checks, a packet must survive both.

**Traffic only flows if every layer on the path permits it.**  
These filters are not alternatives where one substitutes for the other. They stack. A packet can be allowed by the source security group, then dropped by the source subnet’s outbound NACL. Or pass both source-side checks, then get dropped by the destination subnet’s inbound NACL. Or reach the destination and fail at the destination security group. Mechanically, each layer gets a chance to reject the traffic, so the effective policy is the intersection of all allowed paths. This is why debugging has to be path-based: not “is port 443 open?” but “which check on which direction rejected which packet?” That same layering also explains why security groups gained an especially useful feature for dynamic environments.

**Security group references let you authorize by identity instead of IP address.**  
Because security groups are attached to resources, they can be used as identities inside the filtering system: “allow traffic from members of this group” rather than “allow traffic from this CIDR block.” That is powerful because cloud fleets change IPs constantly. In auto-scaling systems, IP-based authorization becomes fragile and high-maintenance; group-based authorization stays aligned with intent. The mechanism here is not just convenience. The filter understands resource membership directly, so the policy follows the workload even as the network coordinates change. That makes security groups the natural tool for east-west traffic between dynamic services, while NACLs remain coarse subnet controls.

**Statefulness creates its own operational edge cases.**  
Connection tracking makes normal service setup easier because it handles return traffic automatically, but the cost is that the filter’s behavior now depends on stored state with a lifetime. Existing tracked connections may continue to work even after you tighten a security group rule, because those sessions are not re-evaluated packet-by-packet. Idle connections may fail later when tracking entries expire and new packets are treated as fresh traffic. So statefulness removes one class of manual rule burden but introduces timing-dependent behavior. That leads directly to a major debugging lesson: you must ask not just “what do the rules say now?” but also “is this traffic using old tracked state or being evaluated as new?”

**The right debugging question is: which layer rejected which direction of traffic?**  
Once all the above is in place, the mystery drains away. A timeout on an apparently inbound service may actually be an outbound return-path rejection at a stateless layer. A rule change that seems ineffective may be hidden by surviving tracked connections at a stateful layer. A flow log showing rejection tells you traffic was blocked somewhere, but not automatically whether the subnet filter or the resource filter was responsible. So the useful mental model is directional and layered: forward path vs return path, stateful vs stateless, subnet boundary vs resource boundary. That is the model that lets you reason instead of poke at rules blindly.

---

## Handles and Anchors

**1. Stateful filtering is “approve the conversation,” stateless filtering is “inspect every sentence.”**  
If a stateful filter approves the start of a conversation, it remembers that approval and lets the back-and-forth continue. A stateless filter does not remember anything; every sentence has to be acceptable on its own. That is why return traffic is automatic in one model and manual in the other.

**2. Security groups protect doors; NACLs protect the fence line.**  
A security group sits on the resource’s interface, so think of it as the rule at each building door. A NACL sits on the subnet, so think of it as the rule at the perimeter of the property. To reach the building, you have to get through both the fence and the door.

**3. Ask this debugging question: “If this packet is a response, what exact rule allows it back?”**  
That question forces you to surface whether you are relying on connection tracking or whether a stateless layer needs an explicit opposite-direction rule. It is a quick test for whether your mental model is connection-based or packet-based.

---

## What This Changes When You Build

**An engineer who understands this will design NACL rules as bidirectional packet policies, not service-port checklists, because return traffic in a stateless layer is a separate rule problem.**  
The unaware engineer writes “allow inbound 443” and assumes HTTPS is handled. The aware engineer also checks the outbound path for client ephemeral ports, and does the equivalent reasoning for any other protocol. The consequence is fewer silent timeout failures where the server looks healthy and only clients see breakage.

**An engineer who understands this will treat security group changes with caution during live testing because existing tracked connections may hide the effect of the change.**  
The unaware engineer tightens a rule, sees an existing session still working, and concludes the rule is wrong or AWS is inconsistent. The aware engineer knows old connections may continue under existing tracking state and tests with new connections or after connection turnover. That prevents false conclusions during production changes.

**An engineer who understands this will choose security groups for service-to-service authorization in dynamic environments because group identity survives IP churn.**  
The unaware engineer encodes east-west policy with CIDRs and inherits ongoing maintenance every time auto-scaling, failover, or redeployment shifts addresses. The aware engineer uses security group references where possible, so “web can talk to db” stays true even as individual instance IPs change. The outcome is lower policy drift and fewer accidental outages during scaling events.

**An engineer who understands this will debug connectivity by tracing the packet path layer by layer because a packet must be permitted at every checkpoint.**  
The unaware engineer checks one layer, sees an allow rule, and then jumps into application debugging. The aware engineer verifies source SG, source subnet NACL, destination subnet NACL, and destination SG, while keeping forward and return directions separate. That shortens incidents because the search matches the actual decision path.

**An engineer who understands this will pay deliberate attention to egress controls because outbound traffic is both a security boundary and a common operational dependency.**  
The unaware engineer inherits permissive outbound rules and only thinks about ingress. The aware engineer asks which destinations a workload really needs — DNS, package repos, external APIs, control planes — and constrains or documents those paths intentionally. That improves both security posture against exfiltration and reliability when diagnosing “service cannot reach X” failures.

</details>


<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) Stateful filtering: one allowed packet creates a remembered flow
```text
# Security-group-like logic

state_table = set()

on_packet(packet):
  flow = (src_ip, src_port, dst_ip, dst_port, proto)
  reverse_flow = (dst_ip, dst_port, src_ip, src_port, proto)

  if reverse_flow in state_table:
    ALLOW   # return traffic for an already-allowed connection

  elif packet.direction == INBOUND and rule_allows(packet):
    state_table.add(flow)
    ALLOW   # first packet admitted, flow is now tracked

  else:
    DENY
```

```text
# Consequence:
# Allow inbound TCP dst_port=443
# No explicit outbound rule needed for the response packet.
#
# Cost:
# The behavior depends on remembered state, not just current rules.
# Existing tracked connections can keep working after a rule change.
```

---

### 2) Stateless filtering: every packet must match on its own
```text
# NACL-like logic

on_packet(packet):
  if packet.direction == INBOUND:
    return first_matching_inbound_rule(packet) or DENY
  else:
    return first_matching_outbound_rule(packet) or DENY
```

```text
# Example flow for HTTPS:
# client 1.2.3.4:52344  -> server 10.0.0.10:443   # inbound request
# server 10.0.0.10:443  -> client 1.2.3.4:52344   # outbound response
#
# If rules are only:
#   inbound:  ALLOW tcp dst_port=443
#   outbound: ALLOW tcp dst_port=443
#
# Then the response is DROPPED.
# Why? Its destination port is 52344, not 443.
```

```text
# Cost:
# You must model both directions explicitly.
# "Open 443" is not enough in a stateless layer.
```

---

### 3) The ephemeral-port trap, shown as the minimal fix
```yaml
# Broken NACL
inbound:
  - allow: tcp dst_port=443 src=0.0.0.0/0
outbound:
  - deny: all
```

```yaml
# Working NACL for public HTTPS server
inbound:
  - allow: tcp dst_port=443 src=0.0.0.0/0

outbound:
  - allow: tcp dst_port=1024-65535 dst=0.0.0.0/0   # client ephemeral ports
  - deny: all
```

```text
# Cost:
# This is broader than many people expect.
# Tightening stateless egress safely requires knowing real client/server flows.
```

---

### 4) Rule evaluation is different: additive vs first-match-wins

**Security group style**
```text
rules = [
  allow tcp from 10.0.0.0/16 to port 22,
  allow tcp from 0.0.0.0/0   to port 443,
]

# Evaluation:
# if ANY allow rule matches -> ALLOW
# else -> DENY

# Adding a rule can only increase access.
# There is no "deny this one IP inside the allowed range".
```

**NACL style**
```text
100 DENY  tcp from 0.0.0.0/0   to port 22
200 ALLOW tcp from 10.0.0.0/16 to port 22
```

```text
# Result: all SSH is denied.
# Rule 100 matches first; rule 200 is never reached.
```

```text
# Cost:
# NACLs are more expressive, but numbering is part of the policy.
# A badly ordered rule silently overrides later intent.
```

---

### 5) The same packet is checked at different attachment points
```text
Packet path: instance A -> instance B

A's security group     : per-interface check
A subnet's NACL        : per-subnet check
B subnet's NACL        : per-subnet check
B's security group     : per-interface check
```

```text
# Minimal truth table

A-SG   A-NACL  B-NACL  B-SG   Result
allow  allow   allow   allow  PASS
allow  deny    allow   allow  DROP
allow  allow   deny    allow  DROP
allow  allow   allow   deny   DROP
```

```text
# Cost:
# "The rule looks right" is never enough.
# Traffic must survive every layer on the path.
```

---

### 6) Security group references: policy by identity, not IP
```yaml
# Fragile: tied to network coordinates
db_sg:
  inbound:
    - allow: tcp port=5432 from=10.0.1.0/24
```

```yaml
# Durable: tied to workload identity
db_sg:
  inbound:
    - allow: tcp port=5432 from_security_group=web_sg
```

```text
# Effect:
# New web instances can get new IPs and still reach the DB,
# as long as they join web_sg.

# Cost:
# This works well for resource-to-resource policy,
# but not for arbitrary external clients on the internet.
```

---

### 7) Stateful changes can look inconsistent because old flows survive
```text
t0: SG inbound allows tcp:5432 from app_sg
t1: app opens DB connection -> flow is tracked
t2: SG rule is removed
t3: existing DB connection still works
t4: app reconnects
t5: new connection fails
```

```text
# Minimal lesson:
# Current rules explain new flows.
# Existing tracked state can explain old flows.

# Cost:
# Testing a security group change against an already-open session is misleading.
```

## Key Ideas

Cloud packet filtering is not one mechanism with different names; it is usually two different models stacked together. The sketches show the practical consequences of that split: stateful filters admit a connection and remember it, while stateless filters judge every packet independently, which makes ephemeral ports part of the policy whether you want them or not. They also show that rule syntax is not the whole story: evaluation semantics matter, attachment points matter, and tracked state can make rule changes appear inconsistent. If you keep one debugging question in mind, it should be: which layer rejected which direction of traffic?

</details>