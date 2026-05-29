## Metadata
- **Date:** 23-05-2026
- **Source:** 14_security.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-14 · Security

Most developers learn security as a list of things to do: hash your passwords, sanitise your inputs, rotate your keys, add the security headers. This produces a particular kind of engineer — one who can pass an audit but cannot tell you why the controls exist, and who treats every new vulnerability as a surprise rather than as the predictable consequence of a design choice. The fundamentals of security are not a checklist. They are a way of thinking about systems that, once internalised, makes most of the checklist obvious and the rest negotiable.

The core reframe is this: security is not a feature you add to a system, it is a property that emerges from how the system is designed. You cannot bolt it on at the end any more than you can bolt on correctness or performance. Every system makes assumptions — about who is calling it, what shape the input will take, what the network looks like, who can read which file. An attack is what happens when one of those assumptions turns out to be wrong, and an attacker has noticed before you have. This is why the same vulnerabilities keep appearing under different names across decades: the underlying class of mistake is a category of assumption, not a specific bug.

Once you see security this way, the field organises itself into a small number of pillars. The first is cryptography, the mathematical machinery that lets two parties communicate or verify each other without trusting the medium between them. Symmetric encryption (one shared key), asymmetric encryption (a public key paired with a private one), hashing (one-way functions that fingerprint data), digital signatures, and key exchange protocols are the primitives. Almost every higher-level security construct — TLS, password storage, JWTs, signed cookies, blockchain — is a recombination of these few primitives. Understanding them at the primitive level means you can read a new protocol and predict its failure modes without waiting for a CVE to tell you.

The second pillar is the distinction between authentication and authorisation, which sound similar enough that practitioners conflate them and pay for it. Authentication answers "who are you?" — proving identity, usually via something you know, have, or are. Authorisation answers "what are you allowed to do?" — granting permissions to an already-identified actor. The mechanics that implement these (sessions, tokens, OAuth flows, JWTs, RBAC, capability systems) are where the majority of real-world web vulnerabilities are introduced, almost always because someone treated a successful authentication as an answer to an authorisation question. The user proved they were logged in; nobody checked whether the logged-in user was supposed to access that record.

The third pillar is the catalogue of vulnerability classes themselves. SQL injection, cross-site scripting, buffer overflows, cross-site request forgery, deserialisation attacks, path traversal, server-side request forgery — these read like a list of unrelated tricks, but each one is a single underlying mistake repeated in different contexts. SQL injection happens because user input was treated as code rather than data. XSS happens for the same reason, in a different language. Buffer overflows happen because input size was assumed rather than checked. CSRF happens because the server trusted that any authenticated request reflected the user's intent. The patches for each are specific; the lesson is general. Trust boundaries exist whether you draw them or not, and any input that crosses one without being explicitly validated is a vulnerability waiting to be named.

The fourth pillar is threat modelling, which is the discipline of asking these questions before writing the code rather than after the breach. Who would want to attack this system? What do they want — data, money, disruption, leverage? What capabilities do they plausibly have? Where are the boundaries between trusted and untrusted, and what crosses them? Threat modelling is unfashionable because it does not produce code, but it is the activity that determines whether the code you do write is defending against the actual threats or against an imagined ideal. A system that is well-defended against the wrong threats is just an expensive theatre.

What pulls these pillars together is a posture, more than a technique. The secure mindset assumes that every input is hostile until proven otherwise, that every component will eventually be compromised, and that the system should fail in ways that limit damage rather than ways that maximise it. Defence in depth — layered controls, so that no single failure is catastrophic — falls naturally out of this posture, as does the principle of least privilege, where every component gets exactly the access it needs and no more. These are not rules to memorise. They are what you do automatically once you stop thinking of security as a feature.

The practical skill this topic builds is the ability to look at a system — your own, or a third party's, or one you are evaluating — and see its trust boundaries, its assumptions about input, and the gap between what it authenticates and what it authorises. With that lens, vulnerabilities stop appearing as surprises and start appearing as design questions. You will not need to memorise every new attack. You will recognise it as a member of a class you already understand.

## Level 2 candidates

**Cryptography** — Covers the primitives (symmetric and asymmetric encryption, hashing, signatures, key exchange) and how they compose into real protocols. Worth depth because almost every higher-level security construct is a recombination of these primitives, and reasoning about new protocols requires fluency at this layer.

**Authentication and authorisation** — Covers identity proofing versus permission granting, and the mechanisms that implement each (sessions, tokens, OAuth, JWTs, RBAC). Worth depth because the conflation of these two concepts is where the largest share of real-world application vulnerabilities are introduced.

**Common vulnerability classes** — Covers SQL injection, XSS, CSRF, buffer overflows, deserialisation attacks, and the rest, as instances of a small number of underlying assumption violations. Worth depth because seeing the class behind the specific attack is what makes the knowledge durable across the constant churn of new named vulnerabilities.

**Threat modelling** — Covers the structured practice of identifying assets, attackers, capabilities, and trust boundaries before writing code. Worth depth because it is the activity that determines whether the rest of your security work is defending against actual threats or imagined ones, and it is rarely taught as a discipline rather than as a vague recommendation.

---
