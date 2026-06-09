## Metadata
- **Date:** 04-06-2026
- **Source:** 08_network_security.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Network Security

Cryptography is the part of security that gets the elegant lectures. It has the prime numbers, the famous names, the satisfying sense that mathematics is doing the work. Network security is what you actually deal with when something goes wrong. It is the discipline of admitting that even a perfectly encrypted message has to travel across an infrastructure built in the 1970s by people who assumed everyone on the network was trustworthy — and then figuring out what to do about that.

The premise you have to internalise first is that the Internet's plumbing was not designed to be secure. TCP/IP was designed to be functional, modular, and resilient against equipment failure. It was not designed against adversaries. Every protocol you rely on every day — DNS to find a server, ARP to find a machine on your local network, IP to route packets, even the three-way handshake that starts a TCP connection — assumes the other party is telling the truth about who they are. Security on top of this stack is an addition, not a foundation. This is sometimes called architectural debt, and it is the thing that explains why network security is structured the way it is: defensively, in layers, with the assumption that any single control will eventually be bypassed.

The mental model that makes the rest tractable is the layered stack — OSI's seven layers in theory, TCP/IP's five in practice — combined with the idea of encapsulation. A piece of data starts as an application payload, then each layer beneath it wraps the payload in its own header before handing it down. The headers are metadata: source and destination addresses, ports, sequence numbers, checksums. When you understand this, you understand that an attacker has a separate attack surface at every layer, and each surface looks different. At Layer 1, an adversary can physically sniff cables or wireless signals. At Layer 2, they can lie about MAC addresses. At Layer 3, they can spoof source IPs. At Layer 4, they can exhaust connection tables or race legitimate replies. At Layer 7, they can phish, inject, or impersonate. The reason security people draw the stack on a whiteboard so often is that the stack is the map. A vulnerability you cannot place on the map is a vulnerability you cannot reason about.

Name resolution is where the trust problem becomes most painful, because name resolution is what turns human-readable intent into network reality. When you type a domain into a browser, DNS translates it into an IP address, and your packets go wherever that address points. DNS in its original form has no authentication — a client that asks "where is this domain?" will trust the first plausible-looking answer that arrives. That race condition is the entire basis of DNS hijacking. The Sea Turtle campaign in 2019 used this against more than forty countries, redirecting national-level traffic through attacker-controlled servers and silently sitting in the middle of supposedly secure connections. ARP, which resolves IPs to MAC addresses on a local network, has the same problem at smaller scale. DNSSEC exists to fix some of this; adoption is patchy. Until that changes, you should assume that name resolution is a soft target.

Availability is the other thing cryptography cannot help you with. A denial-of-service attack does not need to break your encryption — it just needs to drown your servers in traffic, or exhaust some finite resource like connection slots, until legitimate users cannot get through. Mirai and the botnet generation that followed it demonstrated that you can rent attack volume that exceeds the capacity of most organisations to absorb. Encryption protects confidentiality and, with the right constructions, integrity. It does nothing for the third leg of the CIA triad. Network-level defences — rate limiting, filtering, upstream scrubbing, and the architectural decisions that come before any of those — are where availability is won or lost.

The practical toolkit splits neatly into two: tools for seeing what is on the network, and tools for controlling what passes through it. Wireshark lets you capture and dissect actual packets, watching the headers and payloads of real conversations and reconstructing what happened during an incident. Nmap maps a network from the outside, telling you which hosts are reachable, which ports they have open, and often which software versions are listening. Both tools are described as double-edged because attackers use them for reconnaissance and defenders use them for hardening, and the techniques are identical. If you do not run Nmap against your own perimeter regularly, someone else will run it for you, and they will not send you the report. Visibility is a prerequisite for defence; you cannot protect what you cannot see.

On the control side, the dominant constructs are firewalls and network segmentation. A firewall enforces a policy about what traffic is allowed to cross a boundary. The discipline behind a good firewall ruleset is deceptively simple: rules are evaluated in order, you write the most specific allow rules first, and you end with a catch-all deny. This is the default-deny stance, and it inverts the naive instinct to block known-bad things; instead, you permit only known-good things, and everything else is rejected. Segmentation extends this idea architecturally. Public-facing servers — web, mail, anything the Internet must reach — sit in a demilitarised zone between two firewalls, isolated from the internal network so that a compromise of a public service does not give an attacker free movement inside. Next-generation firewalls add application awareness and inspection, but the underlying philosophy is the same: explicit policy, enforced at boundaries.

The boundary itself, though, is dissolving. Remote work, BYOD, cloud services, and the routine hijackability of DNS all mean that "inside the network" is no longer a meaningful security claim. The response is Zero Trust: stop treating network location as evidence of trustworthiness and start authenticating every request, every time, regardless of where it comes from. This is the direction the field is moving, and it is a direct consequence of the points above. If your protocols cannot be trusted, your perimeter is porous, and your visibility is partial, then trust has to be earned per-request rather than granted per-network. That is the shift you are training your instincts for.

## Level 2 candidates

**The OSI and TCP/IP layered model with encapsulation** — Covers how each layer wraps the payload below it in headers and how attacks map cleanly to specific layers. Worth a deep dive because the layered model is the organising framework for every other network security topic, and a fluent grasp of it turns vague threats into precisely located ones.

**DNS and name resolution attacks** — Covers how DNS resolution works, why it lacks authentication by default, the race-condition mechanics of DNS spoofing and hijacking, and what DNSSEC and DoH change. Worth going deeper because DNS is both the most fragile and most consequential piece of Internet infrastructure most people never think about, and the Sea Turtle case study rewards detailed examination.

**Denial-of-service and distributed denial-of-service attacks** — Covers volumetric attacks, protocol-exhaustion attacks, botnet architecture (Mirai and successors), and the layered mitigations from rate limiting to upstream scrubbing. Worth a deep dive because DoS is the category of attack that cryptography explicitly cannot address, which makes it conceptually distinct from most other security topics.

**Wireshark and packet analysis** — Covers capture mechanics, promiscuous mode, filtering and dissection, and the workflow of reconstructing an incident from packets. Worth going deeper because packet-level fluency is the difference between guessing what happened and knowing, and the skill compounds across every other network topic.

**Nmap and network reconnaissance** — Covers host discovery, port scanning techniques, service and version fingerprinting, and how the same tool serves attackers and defenders. Worth a deep dive because reconnaissance is the first phase of every serious attack, and understanding it from the offensive side is the only way to defend the perimeter intelligently.

**Firewalls, DMZs, and ruleset design** — Covers packet filters versus stateful inspection versus application proxies, NIST classifications, the default-deny discipline, rule ordering, and the two-firewall DMZ architecture. Worth going deeper because firewall design is where network security policy becomes concrete, and most real-world firewall failures are failures of ruleset hygiene rather than technology.

**Zero Trust Network Architecture** — Covers the move away from perimeter-based trust, the principles of continuous verification, and how ZTNA interacts with endpoint security and identity. Worth a deep dive because Zero Trust is the dominant architectural shift in the field right now and reframes most of the assumptions the older topics rest on.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Network security matters because the network itself is not naturally trustworthy. Most of the systems your software depends on to send, receive, and route traffic were designed to make communication possible, not to prove that every participant is honest. That means a system can be "working as designed" and still be easy to misdirect, impersonate, overwhelm, or observe. If you do not hold that model clearly, you will keep assuming that successful delivery implies safe delivery, when in fact those are different things.

What goes wrong in practice is rarely exotic. Traffic gets redirected because a resolver accepts a forged answer. A public-facing service gets overwhelmed even though its encryption is fine. An exposed port stays open because nobody mapped the perimeter from the outside. A compromised web server becomes a stepping stone into internal systems because the network was laid out for convenience rather than containment. Engineers who do not understand the mechanics of the network tend to trust boundaries, names, and locations more than they should — and those are exactly the things attackers learn to exploit first.

---

## What You Need To Know First

### Packets, headers, and payloads

Network communication happens by breaking data into packets. Each packet carries the actual content being sent, called the payload, plus metadata in headers, such as source and destination addresses, ports, and sequencing information. This matters because many network attacks do not target the content directly; they target the metadata that tells the network where traffic should go and how it should be treated.

### The layered model

Networks are usually understood as a stack of layers. Higher layers deal with application behavior, while lower layers deal with transport, addressing, and physical transmission. Each layer adds its own information and depends on the layer below. You do not need to memorise every layer to follow this article; you just need the mental model that different kinds of trust assumptions and different kinds of attacks live at different layers.

### Identity versus location

On a network, "where traffic came from" is not the same as "who should be trusted." IP addresses, MAC addresses, and domain names are routing and lookup mechanisms, not proof of identity on their own. This distinction becomes important because much of classic networking behaves as if location or naming is good enough evidence, while modern security increasingly assumes it is not.

### Basic security goals: confidentiality, integrity, availability

Security is often framed as protecting confidentiality, integrity, and availability. Confidentiality means keeping data secret, integrity means preventing or detecting unauthorised changes, and availability means keeping systems reachable and usable. This article leans on the fact that some controls, especially cryptography, help strongly with the first two but do not solve the third.

---

## The Key Ideas, Connected

### The Internet’s core protocols were built for reliable communication, not hostile environments.

The article starts here because this is the root condition that makes the rest of network security necessary. TCP/IP was designed to move packets between machines and recover from failures in links or hardware. It was not built around the assumption that participants would lie. So when a protocol accepts information like an address, a name, or a reply, it often does so because the system needs to keep moving, not because that information has been strongly verified.

Once you see that, network security stops looking like a neat built-in property and starts looking like a set of compensating controls layered onto a system that was permissive by default. That directly leads to the next idea: if trust is weak at the foundation, you need a way to locate where the weakness appears.

### The layered stack is the map of the attack surface.

The reason engineers keep returning to OSI or TCP/IP diagrams is not academic habit; it is because the layers tell you what kind of thing can be attacked and how. Each layer wraps the one above it with its own headers and behaviors. That means each layer exposes different assumptions: physical access at the bottom, local identity at Layer 2, routing identity at Layer 3, connection state at Layer 4, and human or application logic at the top.

This matters mechanically because attackers do not attack "the network" in the abstract. They exploit a specific trust assumption in a specific layer. If you cannot place a problem on the stack, you cannot tell what data is being trusted, what component enforces it, or what mitigation would actually help. And once you start looking at those trust assumptions, name resolution becomes one of the clearest examples of the problem.

### DNS and ARP show what happens when the network accepts plausible answers without strong authentication.

DNS turns a human-meaningful name into an IP address, and ARP turns a local IP address into a MAC address. Both are translation systems that help traffic reach the intended destination. But in their basic forms, both were designed for environments where answers were assumed to be honest enough. If a client asks a question and accepts the first plausible answer, then an attacker does not need to break encryption to win; they only need to answer faster or insert themselves into the conversation.

That is why name resolution is such a soft target. It sits early in the chain of communication and determines where traffic goes before higher-level protections have much chance to help. If you can poison the answer to "where is this service?", you can redirect traffic, impersonate infrastructure, or insert a man-in-the-middle position. This leads naturally to the next idea: even if you protect the correctness or secrecy of communication, you still have to deal with whether communication can happen at all.

### Cryptography does not solve availability.

Encryption can keep content secret and signatures can help verify integrity, but neither prevents an attacker from exhausting bandwidth, CPU, memory, or connection state. A denial-of-service attack works by consuming finite resources until legitimate users cannot be served. That mechanism is important: the attacker is not required to understand your data, only your bottlenecks.

This is why availability lives differently from confidentiality and integrity in network security. You cannot "encrypt your way out" of a volumetric flood or a connection-exhaustion attack. The system has to absorb, reject, rate-limit, or divert abusive traffic before scarce resources are consumed. Once that becomes clear, another requirement follows: you need visibility into what traffic exists and control over what traffic is allowed.

### Network defence depends on both visibility and policy enforcement.

You cannot secure traffic you cannot observe. Tools like Wireshark and Nmap matter because they reveal different sides of network reality. Wireshark lets you inspect actual packet flows and reconstruct what happened on the wire. Nmap lets you see your exposed surface from the outside: which hosts respond, which ports are open, and what services appear to be there. The same mechanics serve attackers and defenders because reconnaissance is morally neutral; it is simply the act of learning what the network exposes.

But seeing is not enough. Once you know what traffic exists and what surfaces are exposed, you need a way to decide what should be permitted. That is where firewalls and segmentation come in, as concrete expressions of policy.

### Firewalls and segmentation turn security intent into enforced boundaries.

A firewall is not just a box that "blocks bad traffic." It is a place where you encode decisions about which communications are allowed to cross a boundary. The key discipline is default deny: allow only what is specifically needed, and reject everything else. Mechanically, this works because network traffic is regular enough to match against addresses, ports, protocols, states, or even application-level characteristics.

Segmentation takes that same logic and applies it to architecture rather than just packet filtering. Instead of assuming all internal systems can trust one another, you divide the network so that compromise in one zone does not automatically become compromise everywhere. A DMZ is a classic example: public-facing services are reachable from the internet, but they are separated from the more trusted internal environment. This leads to the final idea because modern systems increasingly make even these boundaries less reliable than they once seemed.

### The old idea of a trustworthy “inside” network no longer holds, so trust shifts from location to continuous verification.

If users work remotely, devices are unmanaged, services live in the cloud, and infrastructure depends on weakly trusted protocols, then network position is a poor proxy for legitimacy. Being "on the corporate network" does not tell you enough about whether a request should be allowed. Zero Trust is the response to that reality: trust is not granted because of location; it is established per request through identity, context, and policy.

This is not a fashionable add-on to perimeter security so much as a consequence of everything before it. If foundational protocols are weakly authenticated, if boundaries are porous, and if compromise can move laterally when trust is inherited too freely, then each access decision has to stand on its own. Zero Trust is what you get when you take the mechanics seriously instead of preserving the old mental shortcut that inside means safe.

---

## Handles and Anchors

### 1. The network is a delivery system, not a truth machine.

A useful way to hold this topic is: the original network stack is good at moving packets, not proving honesty. If you remember that, many security behaviors make immediate sense. DNS, ARP, source addresses, and even connection setup become things to verify or constrain, not things to accept at face value.

### 2. Every layer has its own lie.

Use this as a diagnostic handle. At the physical layer, someone can observe or interfere with the medium. At the local network layer, someone can lie about hardware identity. At the routing layer, they can lie about source or destination. At the transport layer, they can abuse state or connection setup. At the application layer, they can impersonate a service or user. That framing helps you ask not just "what is vulnerable?" but "what assumption is being exploited, and at what layer?"

### 3. Default trust expands blast radius; explicit trust shrinks it.

This captures the design tension. Whenever the system implicitly trusts names, locations, or broad internal reachability, compromise spreads more easily. Whenever trust is explicit, narrow, and continuously checked, failures are contained better. You can use this sentence to explain firewalls, segmentation, and Zero Trust in one line.

---

## What This Changes When You Build

### An engineer who understands this will treat network names and addresses as inputs to validate, not ground truth, because DNS, ARP, and source identity mechanisms can be manipulated.

The unaware engineer tends to inherit the assumption that if a service resolves correctly and packets arrive from an expected address, communication is probably legitimate. The more aware engineer asks what authenticates that mapping, what happens if the mapping is poisoned, and where additional verification belongs.

### An engineer who understands this will design controls per layer instead of looking for a single “secure network” solution, because attacks target different headers, assumptions, and resources at different layers.

The unaware engineer often reaches for one dominant control, such as TLS, and assumes the problem is mostly solved. The informed engineer knows TLS protects only part of the chain, so they think separately about name resolution, connection exhaustion, exposed ports, lateral movement, and application impersonation.

### An engineer who understands this will scan and observe their own environment regularly, because exposure is often created by drift rather than deliberate design.

The default failure mode in real systems is inherited exposure: a port left open, a service version forgotten, a route added for expedience, a packet pattern nobody noticed. An engineer with a working model of network security uses tools like packet capture and external scanning not as occasional audits but as routine ways to compare intended architecture with actual behavior.

### An engineer who understands this will use default-deny and segmentation earlier in system design, because containment is far easier to build in than to retrofit after compromise paths exist.

The unaware engineer often starts from permissive connectivity and adds exceptions later when something bad happens. That creates broad east-west movement and makes public-service compromise far more costly. The aware engineer starts by asking which communications are truly necessary, then allows only those, reducing the number of paths an attacker can use.

### An engineer who understands this will stop using network location as a shortcut for trust, because modern environments make “inside” too weak a security boundary to carry much meaning.

The default inherited assumption is that internal traffic is lower risk and deserves broader access. In practice, that assumption breaks under remote work, cloud systems, contractor devices, and post-compromise lateral movement. An engineer who understands this designs access around identity, context, and narrowly scoped policy checks rather than subnet membership alone.

</details>
