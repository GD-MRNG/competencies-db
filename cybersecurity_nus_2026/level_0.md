# Cybersecurity — Integrated with AI — Level 0: Course Map

> **Intent:** To develop a durable mental model of how digital systems are attacked and defended — and to understand how AI has changed both sides of that equation. The practitioner who studies this domain can reason about threats before they materialise, design controls proportionate to actual risk, and translate technical findings into decisions that non-technical stakeholders can act on.
>
> **Your angle:** You are not here to learn that firewalls exist. You are here to rebuild your mental model from first principles — to understand *why* each layer of security was invented, what problem it failed to solve on its own, and what replaced or extended it. The historical thread matters. Most design decisions in modern security are responses to specific failures, and knowing those failures is what makes the controls feel inevitable rather than arbitrary.

---

## How to use this map

This map has two layers below it. **Level 1** is a substantive essay on each topic — the kind of treatment that gives you the reasoning, the historical context, and the "what breaks if you miss this" framing. It is not a textbook chapter; it is closer to a well-structured briefing designed to leave you with a working mental model rather than a definition. **Level 2** candidates are the sub-concepts worth drilling into once you have the Level 1 frame in place. Each is listed here with a directional description — not a definition, but a signal about what going deeper will unlock.

Descend to Level 1 when a topic is load-bearing for something you are trying to do or understand. Descend to Level 2 when a Level 1 post has raised a question you cannot answer with that frame alone — or when a specific mechanism is directly relevant to a project or incident you are working through.

---

## Topic Inventory

---

### Group I — The Security Mindset and Threat Reasoning

Before any technical control makes sense, you need the lens through which security professionals read systems. This group establishes that lens: the adversarial mindset, the vocabulary of assets and threats, and the frameworks for thinking about how attacks unfold and where defenders can intervene.

---

#### L1-01 · Introduction to Cybersecurity

Cybersecurity is not reliability engineering — it is the discipline of keeping systems working *while someone is actively trying to make them fail for their own gain*. The presence of an adversary changes everything: which controls you choose, which threats you model, which trade-offs you accept. This topic establishes the C-I-A triad (confidentiality, integrity, availability) as the three ways an adversary can hurt you; the assets-vulnerabilities-threats-controls vocabulary as the workhorse threat-modelling frame; and the weakest-link principle as the reason technical controls alone can never be sufficient. The 2024 Arup deepfake ($25M wired to a synthetic CFO) failed no firewall — it bypassed a person. Getting this framing right is the prerequisite for everything downstream.

**Level 2 candidates:**
- **The C-I-A triad in depth** — Reveals how confidentiality, integrity, and availability conflict in real designs, and why misclassifying which property a control actually protects is the root cause of many security failures.
- **Assets, vulnerabilities, threats, controls** — Unpacks the threat-modelling vocabulary into an operational method you can apply to any system — not just the sketch in Level 1.
- **The weakest-link principle and attack surface** — Explores why adversaries are economically rational, how attack surface expands with digitisation and third parties, and why the principle is easy to state but hard to operationalise.
- **Security trade-offs and Security-by-Design** — Covers the structured analysis of security against safety, usability, and cost — the conversation where security strategy actually happens, and the one most rarely taught explicitly.
- **The Mosaic Effect and inference attacks on privacy** — Reveals how combining innocuous datasets can re-identify individuals, overturning the intuition that protecting each database in isolation is sufficient.
- **Threat actors and adversary profiling** — Distinguishes external attackers, insiders, contractors, hacktivists, and state actors by motive and capability, because the profile changes which controls matter most.

---

#### L1-11 · Attacks, Malware & Mitigation

An attack is not an event — it is a chain, and defenders only need to break one link. This topic maps the attacker's playbook in sequence: passive reconnaissance, active scanning, vulnerability identification, exploitation, and persistence. It introduces the Cyber Kill Chain and MITRE ATT&CK as two complementary frameworks for reasoning about that sequence, and covers malware taxonomy (viruses, worms, trojans, ransomware) in terms of propagation mechanics rather than labels. The WannaCry case study anchors the key lesson: most successful breaches do not use novel techniques — they exploit patch latency, the operational gap between a fix being released and a fix being applied. The democratisation of state-grade tooling (EternalBlue was an NSA exploit, leaked and weaponised within months) means the baseline threat level is now extremely high for everyone.

**Level 2 candidates:**
- **The MITRE ATT&CK Framework** — Goes beyond the glossary to show how to map your own telemetry against specific adversary techniques — the working language of modern detection engineering.
- **The Cyber Kill Chain and its critiques** — The model's strengths (clarity, narrative) and weaknesses (linearity, perimeter bias) shape how organisations communicate about incidents; understanding the critique prevents you from being limited by it.
- **Vulnerability management: CVE, CWE, CVSS, and KEV** — Turns "we found a bug" into a prioritisation system — the single highest-leverage operational practice in defence.
- **Malware taxonomy and behaviour** — The functional differences between virus, worm, and trojan predict propagation patterns, dwell time, and the kind of countermeasure that will actually work.
- **Patch management as an operational discipline** — Patch latency is empirically the largest contributor to successful breaches; going deeper reveals why the gap is almost entirely a workflow problem, not a technology one.
- **MITRE ATLAS and AI-specific attack surfaces** — The frontier framework for adversarial threats against ML and generative AI systems: prompt injection, model poisoning, training data attacks.

---

### Group II — Cryptographic Foundations

Cryptography is the mechanism underneath almost every other security control: authentication, secure channels, data integrity, and non-repudiation all depend on it. This group builds the cryptographic stack from first principles — symmetric and asymmetric primitives, hash functions, key distribution — and then shows how those primitives are composed into the protocols and infrastructure that secure real communications. The ordering here reflects genuine dependency: each topic assumes the one before it.

---

#### L1-02 · Cryptography

Cryptography is not the study of secret codes — it is the study of how to formalise and achieve security properties under mathematical assumptions. This topic covers the shift from classical ciphers (substitution, transposition) to Kerckhoffs' Principle — the foundational insight that security should rest on key secrecy, not algorithm secrecy — and on to the formal definitions of what it means for a cryptosystem to be secure. These definitions were invented for a reason: without them, it is impossible to argue rigorously that a scheme is secure rather than merely unbroken so far. Everything in the applied crypto topics downstream rests on this foundation.

**Level 2 candidates:**
- **Kerckhoffs' Principle versus security by obscurity** — Reveals why the principle is counterintuitive to most engineers and why violating it remains a common design mistake in proprietary systems.
- **Shannon's information theory and perfect secrecy** — The one-time pad is provably unbreakable; understanding why illuminates both the limits of symmetric crypto and why all practical systems accept computational rather than information-theoretic security.
- **Classical ciphers and their cryptanalysis** — Caesar, Vigenère, and frequency analysis are worth understanding not for history but because the attacks they fell to — pattern leakage, statistical regularities — recur in modern failures.
- **Computational vs information-theoretic security** — The distinction between "unbreakable in principle" and "unbreakable within available compute time" is the premise on which all modern cryptographic claims rest.

---

#### L1-03 · Modern Ciphers

Stream ciphers and block ciphers are the two families of symmetric encryption used in practice, and the difference between them is not aesthetic — it determines latency, error behaviour, malleability, and the attack surface. This topic maps the mechanics of each: stream ciphers as synthetic one-time pads (fast, fragile under nonce reuse), block ciphers as structured chunk-by-chunk transformers (strong diffusion, mode-dependent security). The ECB penguin example is here not as a curiosity but as the cleanest demonstration that a strong cipher does not automatically produce a secure system — mode selection is part of the design, and getting it wrong leaves structure visible in the ciphertext even when the algorithm is running correctly.

**Level 2 candidates:**
- **Block cipher modes of operation (CBC, CTR, GCM)** — Each mode adds different properties on top of the cipher; GCM is the authenticated encryption workhorse, and going deeper reveals why confidentiality and integrity must be constructed together, not separately.
- **Nonce management and keystream reuse** — The catastrophic failure mode of stream ciphers: the constraint "never reuse a nonce" sounds simple and is routinely violated in real systems, with full confidentiality loss as the consequence.
- **Confusion, diffusion, and the avalanche effect** — Shannon's design principles in practice; connects internal cipher design to observable security properties and explains why changing one input bit should appear to change half the output.
- **Authenticated Encryption with Associated Data (AEAD)** — ChaCha20-Poly1305 and AES-GCM are the production standards; going deeper reveals why confidentiality and integrity must be constructed together rather than layered separately.
- **Cryptographic agility in system design** — Algorithms have lifespans; going deeper covers how to design systems so a cipher swap does not require a product rewrite.

---

#### L1-04 · Entity Authentication

Authentication is not a gate — it is a lifecycle, and attackers attack the stages you weren't watching. This topic models the credential lifecycle in three stages — bootstrapping (where trust is born and where Mirai walked through factory-default front doors), storage (where the 2012 LinkedIn breach turned a database leak into a password leak through unsalted hashes), and presentation (where human use becomes the attack surface). It explains why multi-factor authentication only works when the factors fail *differently*, and why SMS-based OTP has been quietly deprecated by NIST: SIM swapping collapsed the second factor back into the first.

**Level 2 candidates:**
- **Password storage: salting, hashing, and modern KDFs** — The implementation details (bcrypt, scrypt, Argon2) determine whether a database breach becomes a password breach — the difference is in deliberate computational cost.
- **Multi-factor authentication design** — Goes beyond "use MFA" to why some combinations are illusory, why SMS is deprecated, and how FIDO2/WebAuthn hardware tokens change the phishing threat model fundamentally.
- **Bootstrapping and credential provisioning** — The most overlooked lifecycle stage: default passwords, factory provisioning, and credential-recovery flows are where the largest IoT compromises have originated.
- **Social engineering and the human attack surface** — Technical authentication controls can be cleanly bypassed by attacks on the person; the defences here are organisational and behavioural, not cryptographic.
- **Biometric authentication and its limits** — Biometrics are excellent for convenience and dangerous as identity roots; the irrevocability problem — you have nine more fingerprints, and then you are out — is the key tension to understand.

---

#### L1-05 · Public Key Systems and Cryptographic Hashes

Symmetric cryptography solves confidentiality but leaves a hard problem unsolved: how do you share a key with someone you have never met? Public key cryptography, introduced by Diffie and Hellman (1976) and RSA (1977), dissolves that problem by separating the encryption key from the decryption key. This topic also introduces cryptographic hash functions — the mechanism for turning variable-length input into a fixed-length fingerprint that is easy to compute and practically impossible to reverse or collide — which become the building blocks for MACs, digital signatures, and data integrity checks in every topic that follows.

**Level 2 candidates:**
- **RSA: trapdoor functions and key size selection** — Going deeper reveals why RSA security rests on the difficulty of factoring large composites, what "2048-bit key" actually means operationally, and where quantum computing threatens this assumption.
- **Elliptic curve cryptography** — ECC achieves comparable security to RSA at much smaller key sizes; drilling here explains why it has largely replaced RSA in modern TLS and why the choice of curve matters more than most engineers realise.
- **Hash function properties: preimage and collision resistance** — Each formal property protects against a different class of attack; knowing which property is absent from a given use case explains the specific failure mode.
- **Keyed hashes and HMACs** — The construction that turns a hash function into a message authentication code; going deeper reveals why using a plain hash as a MAC is broken and why the specific HMAC construction is not.
- **Post-quantum cryptography** — Shor's algorithm threatens RSA and ECC; drilling here maps the NIST PQC candidate algorithms and the urgency of cryptographic migration planning for long-lived systems.

---

#### L1-06 · Data Origin Authentication & Public Key Infrastructure

Symmetric keys prove "someone who knows the secret sent this." Digital signatures prove "the holder of this specific private key signed this, and anyone with the public key can verify it" — public verifiability without shared secrets is what makes non-repudiation and third-party trust possible. This topic covers MACs and digital signatures as the two mechanisms for proving message origin, then explains why the hardest problem in public key cryptography is not the mathematics but the binding of a key to an identity — the problem PKI was invented to solve. A CA compromise is not a local failure; it is a system-wide impersonation capability, which is why CT logs and CA accountability have become critical additions to the trust model.

**Level 2 candidates:**
- **MAC vs digital signature: choosing for the use case** — The choice between symmetric and asymmetric authentication has concrete consequences for who can verify, who can dispute, and what happens when the shared secret leaks.
- **Certificate lifecycle management** — Issuance, renewal, revocation (OCSP, CRL), and the operational reality that most PKI failures in production are procedural, not mathematical.
- **Certificate Transparency and CA accountability** — A practical response to the structural weakness of hierarchical trust; drilling here explains how an append-only public log of certificates makes CA misbehaviour detectable after the fact.
- **Hash-then-sign and signing large documents** — The engineering pattern that makes asymmetric signing practical at production scale, and why signing raw document bytes is never the right implementation choice.
- **Replay attacks and freshness mechanisms** — A valid signature is still a valid signature tomorrow; going deeper covers timestamps, nonces, and sequence numbers as the constructions that add temporal binding to signed artefacts.

---

#### L1-07 · Protocol Security

Cryptographic primitives are not protocols. AES does not protect your session; RSA does not authenticate your user. What protects you is the choreography — who sends what, in what order, how each party verifies the other. Get the choreography wrong and the strongest cipher is decorative. The adversary is not trying to break the encryption; they are trying to break the *conversation* — replaying yesterday's valid proof today, sitting in the middle translating faithfully while reading everything, or waiting until the handshake completes and hijacking the session that follows. This topic covers the three properties that separate a real protocol from a toy (freshness, proof-of-knowledge, mutual authentication), why authentication must produce a bound session key to be meaningful, and why logical flaws now dominate over brute force as keys get longer.

**Level 2 candidates:**
- **Challenge-response and the design of freshness** — Covers how nonces and time-bound tokens enforce session uniqueness, and the failure modes when challenges are too small, too predictable, or reused — where a large fraction of real-world protocol breaks live.
- **Authenticated key exchange and session binding** — The integration of authentication with key exchange (Diffie-Hellman variants) to produce a session key bound to verified identity; this is where forward secrecy, key confirmation, and downgrade resistance all live.
- **Man-in-the-middle attacks and mutual authentication** — The canonical protocol-level attack; understanding it concretely changes how you read every handshake, and why certificates and PKI exist as the closure.
- **Logical flaws in protocol design (XOR and algebraic manipulation)** — The class of attacks where primitives are sound but protocol structure lets an adversary derive valid responses without the key — the modern attack surface as brute force becomes prohibitively expensive.
- **Lightweight protocols for RFID and IoT** — The trade-offs forced by resource-constrained devices, and the systemic risk of deploying weakened protocols at the scale of billions of devices.
- **Token-based API security: OAuth 2.0, JWT, PKCE** — The dominant protocol family for contemporary web and mobile applications; going deeper reveals the specific failure modes — token leakage, scope misuse, redirect-flow abuse — that replace the cipher-level attacks of earlier generations.
- **Zero-knowledge proofs** — Proving an attribute without revealing the underlying data; represents a genuine shift in how verification can work — verification without collection — and the conceptual machinery is unfamiliar enough to deserve its own treatment.

---

### Group III — Applied Security Domains

With cryptographic and threat-reasoning foundations in place, this group covers the concrete attack surfaces practitioners encounter: the network stack, web applications, host systems, and the cloud. Each topic follows the same pattern — understand how the infrastructure was built to trust, understand how attackers exploit that trust, then understand what controls exist and why they are structured as they are.

---

#### L1-08 · Network Security

The Internet's plumbing was designed for connectivity, not adversaries. TCP/IP assumes the other party is telling the truth about who they are — and DNS, ARP, IP routing, and the TCP handshake all take claims at face value. Security on top of this stack is an addition, not a foundation. This topic maps the layered stack as the framework for locating attack classes: MAC spoofing at Layer 2, IP spoofing at Layer 3, connection exhaustion at Layer 4, impersonation at Layer 7. It covers DNS hijacking (Sea Turtle 2019: 40+ countries' national traffic redirected before any encrypted connection started), why DoS is the one attack category that cryptography cannot touch, and the practical toolkit — Wireshark for visibility, Nmap for reconnaissance — before covering the controls (firewalls, DMZs, Zero Trust) that emerged as the perimeter dissolved.

**Level 2 candidates:**
- **The OSI and TCP/IP layered model with encapsulation** — The organising framework for every other network security topic; fluency here turns vague threats into precisely located ones.
- **DNS and name resolution attacks** — How DNS resolution works, why it lacks authentication by default, the race-condition mechanics of spoofing and hijacking, and what DNSSEC and DoH change — and why adoption has lagged despite well-understood attacks.
- **Denial-of-service and distributed denial-of-service attacks** — Volumetric vs protocol-exhaustion vs application-layer attacks, botnet economics (Mirai), and the layered mitigations — the category that cryptography explicitly cannot address.
- **Wireshark and packet analysis** — Capture mechanics, filtering, and the workflow of reconstructing an incident from packets; packet-level fluency is the difference between guessing what happened and knowing.
- **Nmap and network reconnaissance** — Host discovery, port scanning techniques, service and version fingerprinting; reconnaissance is the first phase of every serious attack, and understanding it offensively is the only way to defend the perimeter intelligently.
- **Firewalls, DMZs, and ruleset design** — Packet filters vs stateful inspection vs application proxies, default-deny discipline, rule ordering, and the two-firewall DMZ architecture; most real-world firewall failures are failures of ruleset hygiene, not technology.
- **Zero Trust Network Architecture** — The move away from perimeter-based trust toward per-request continuous verification; the dominant architectural shift in the field and the direct consequence of everything this topic covers.

---

#### L1-09 · Web Security

Web security is not application security in general — it is the specific set of vulnerabilities that arise from browsers, HTTP, and the trust model of the web. This topic covers the four major classes: UI-based attacks (clickjacking), XSS (injecting scripts into pages trusted by users), CSRF (exploiting ambient browser credentials to forge requests), and SQL injection (breaking the structural separation between query and data). Each vulnerability exists because a parser or browser does not care about your intentions once it starts interpreting text. The defensive answer is always structural — parameterised queries, output encoding, SameSite cookies — not input filtering, because any filter that depends on maintaining a list of "bad patterns" will eventually be bypassed.

**Level 2 candidates:**
- **The same-origin policy and CORS** — The foundational browser trust mechanism; CORS misconfigurations are a consistent source of data exposure in production APIs and the failure mode is non-obvious.
- **XSS in depth: stored, reflected, DOM-based** — Each type exploits the same root cause through a different injection path; the defensive techniques differ enough that conflating them produces gaps.
- **SQL injection and parameterised queries** — The canonical code-versus-data confusion; going deeper reveals why ORMs do not automatically protect you and where developers still get this wrong in practice.
- **CSRF and SameSite cookies** — The attack exploits the fact that browsers send cookies automatically; going deeper covers the three SameSite values and what each one actually buys in terms of defence.
- **Session management and token security** — Session tokens are credentials; the security of everything post-login depends entirely on how they are issued, stored, rotated, and invalidated.
- **Content Security Policy and the browser as a security boundary** — CSP is a defence-in-depth mechanism against XSS; drilling here reveals what it can and cannot prevent and why misconfigured CSPs are near-universal in production.

---

#### L1-10 · System Security and Access Control

Most security failures are not break-ins — they are mundane: someone had access they should not have had, or someone with legitimate access did something they should not have been able to do. The Colonial Pipeline attack began with a forgotten VPN account nobody decommissioned. The attackers logged in. This topic provides the formal model for reasoning about these failures: every security-relevant event is a subject–operation–object triple, mediated by a reference monitor consulting a policy. It covers how that policy is represented (ACL vs capabilities vs RBAC), how Linux implements it (the nine permission bits, setuid, sudo), and how least privilege translates from a slogan into an engineering discipline that bounds blast radius. Zero Trust is the modern reframing: stop treating network location as evidence of identity and apply access decisions at every layer.

**Level 2 candidates:**
- **Access control representations (ACM, ACL, capabilities)** — The choice between object-centric and subject-centric representations ripples through auditing, revocation, delegation, and how OAuth scopes and Kerberos tickets actually work under the hood.
- **Linux/Unix permissions in practice** — Owner/group/other, octal chmod, ACL extensions, and the corner cases (sticky bit, umask, directory execute semantics) — where the actual configuration mistakes happen.
- **Controlled invocation and privilege escalation** — Setuid, sudo, and the broader pattern of elevated-privilege execution; every setuid binary is a potential privilege escalation vector, which connects access control directly to exploit development.
- **DAC vs MAC vs RBAC** — The three major policy models have deep consequences for compliance, scalability, and how human error propagates; the choice is an organisational decision with structural implications.
- **The principle of least privilege as a design discipline** — Not a slogan but a working method: how to scope service accounts, design permission boundaries, handle break-glass scenarios, and reason about blast radius in API design and incident response.

---

#### L1-12 · Cloud Security

Moving to the cloud does not relocate your perimeter — it dissolves it. The shared responsibility model is the single most important mental shift: the provider secures the underlying infrastructure; you secure everything you deploy on top of it. The line moves with the service model — you own far more in IaaS than in SaaS — and getting the boundary wrong is the most common source of cloud incidents. Public S3 bucket, leaked admin credential, over-broad IAM role: these are not provider failures. This topic also covers why identity becomes the new perimeter when everything happens through authenticated APIs, why logical multi-tenant isolation is real but not absolute (Meltdown, Spectre), and why security must move into the CI/CD pipeline when infrastructure is created from code and changes continuously.

**Level 2 candidates:**
- **Shared responsibility model across IaaS/PaaS/SaaS** — The boundary moves with the service model; going deeper makes explicit what is yours to secure in each tier and where teams most commonly misplace responsibility.
- **Cloud IAM and least-privilege access** — In cloud environments, possession of valid credentials is often the attack path itself; covers role design, machine identities, temporary credentials, and privilege review as structural defence.
- **DevSecOps: security in the CI/CD pipeline** — Secret scanning, infrastructure policy-as-code, and dependency checking; going deeper covers the specific integrations that make security continuous rather than a post-deployment checkpoint.
- **Multi-tenancy, side-channel attacks, and confidential computing** — Meltdown and Spectre demonstrated that CPU-level behaviour can leak across logical isolation boundaries; covers hardware enclaves (SGX, TrustZone) for workloads that require stronger guarantees.
- **SIEM, SOAR, and detection at cloud scale** — At cloud scale, detection cannot depend on people reading logs; going deeper covers how to design telemetry, correlation, and automated response as infrastructure requirements rather than operational afterthoughts.

---

### Group IV — Contemporary Threats and Professional Practice

The final group covers the domains that complete the practitioner picture: AI as both attacker and defender tool, offensive techniques a defender must understand, and the governance frameworks that translate technical security into organisational accountability. This group cannot be understood without Groups II and III in place — it builds on the controls and vulnerabilities covered there.

---

#### L1-13 & L1-14 · AI in Cybersecurity

For most of cybersecurity's history, defence was a rule-writing exercise. That model broke when attacks scaled beyond any human's ability to characterise them fast enough. This topic covers why AI became unavoidable in security (volume-and-velocity), how supervised and unsupervised ML differ in what data they require and what questions they can answer, and why deep learning specifically matters for network defence: sequence-aware detection using LSTMs can see multi-stage campaigns that play out over weeks, where each individual event looks unremarkable in isolation. The operational consequence is a shift from analyst-as-craftsperson to analyst-as-model-overseer. The arms race is real: the same pattern-recognition tools are available to attackers.

**Level 2 candidates:**
- **Supervised vs unsupervised detection: choosing the right frame** — The data labelling question is upstream of every algorithm choice; getting it wrong produces a confidently wrong model.
- **Feature engineering for security data** — Two teams using the same algorithm get very different outcomes depending on how they represent network behaviour numerically — this is where most implementations fail silently.
- **Precision, recall, and the cost of each error type** — Model tuning in security is a cost dial, not a truth dial: false positives and false negatives have different business owners and different costs, and threshold choice is ultimately a business decision.
- **Recurrent architectures for sequence-aware detection** — LSTMs and context windows are what let a model connect today's packet to yesterday's probe — the crux of why deep learning matters for APT detection that traditional ML cannot see.
- **Explainable AI in SIEM (the AMIDES pattern)** — Explainability is the pivot point determining whether AI gets adopted in real security operations or stays in research; analysts will not act on verdicts they cannot interrogate.
- **AI-driven penetration testing and continuous red teaming** — The shift from quarterly human red teams to 24/7 autonomous agents inverts the economics of offensive security and previews the attacker-side use of the same techniques.

---

#### L1-15 · Generative AI for Cybersecurity

Generative AI introduces both new attack surfaces and new defensive capabilities simultaneously. On the attack side: high-volume personalised phishing at near-zero marginal cost, synthetic media for social engineering (the 2024 Arup deepfake, $25M wired to a synthetic CFO), and accelerated vulnerability discovery. On the defensive side: natural-language interfaces to SIEM systems, automated code review, and security report generation. The unstable part is that the same model capabilities that make LLMs useful for defenders make them useful for attackers — and the adversarial surface of the models themselves (prompt injection, training data poisoning) is largely uncharted territory that existing security frameworks were not designed to cover.

**Level 2 candidates:**
- **Prompt injection and AI-native attack vectors** — The attack category with no analogue in traditional security; structural defences are fundamentally different from input filtering, and going deeper reveals why input-based mitigations are weak by design.
- **Deepfakes and synthetic media in social engineering** — The Arup case is the template; going deeper covers detection methods, organisational policies (callback verification for large transfers), and the limits of technical countermeasures.
- **LLM-assisted red teaming and vulnerability discovery** — AI can enumerate attack paths faster than humans; going deeper covers both the offensive capability and how defenders can use the same tools to find their own weaknesses first.
- **Responsible disclosure and AI security governance** — The policy frameworks that manage vulnerability research in a world where AI accelerates both discovery and exploitation.

---

#### L1-16 · Ethical Hacking

You cannot reliably defend what you have not tried to break. Ethical hacking is the practice of simulating adversarial pressure under explicit authorisation and defined scope — not to demonstrate that the tester is clever, but to produce prioritised remediation guidance that changes what gets fixed. This topic covers the structured engagement funnel (reconnaissance → scanning → exploitation → post-exploitation → reporting), the legal framework that separates a penetration test from a criminal offence (Singapore's Computer Misuse Act; scope documents as the condition that makes the work possible), and the offensive toolchain (Nmap, Metasploit, privilege escalation, session hijacking). Lateral movement is the practical argument against perimeter-only security: a single compromised edge device that can reach internal resources exposes that "inside the network" has been silently equated with "trusted."

**Level 2 candidates:**
- **The attack lifecycle and cyber kill chain** — Each stage has distinct tooling, distinct detection signatures, and distinct mitigation strategies; understanding the full chain lets defenders break it at the cheapest point rather than the most obvious one.
- **The Metasploit framework and exploitation workflows** — How modular exploitation frameworks industrialise known attack paths; understanding the module structure teaches how vulnerability research becomes reusable, repeatable tooling.
- **Privilege escalation techniques** — Password cracking, buffer overflow mechanics, and misconfiguration-based escalation paths; where most real breaches actually progress, and the underlying mechanics are foundational rather than tool-specific.
- **Rules of engagement and the legal framework** — Scope definition, authorisation documents, and the relevant legislation; the legal exposure for getting this wrong is severe, and the documentation practices are non-obvious to people from a purely technical background.
- **Reporting, CVSS, and remediation translation** — The report is the actual product of an ethical hacking engagement; translating a technical exploit into a business-relevant risk statement is what separates competent testers from valuable ones.

---

#### L1-17 · Ethics, Governance and the Future of Cybersecurity

Technical controls fail. When they do, governance frameworks, professional obligations, and legal structures are the remaining accountability layer. This topic covers the security principles that predate and outlive specific controls (defence-in-depth, fail-safe defaults, separation of privilege), the governance standards that operationalise them (ISO 27001, NIST CSF, Singapore's Cybersecurity Act 2018, MAS TRM guidelines), and the professional ethics obligations that define what a practitioner is accountable for. It also surveys emerging threats — AI-enabled attacks, IoT proliferation, and quantum computing's implications for current cryptographic infrastructure — and explains why the discipline is not converging toward a fixed endpoint but is structurally defined by the adversary's ability to evolve faster than any fixed rulebook.

**Level 2 candidates:**
- **Security principles as design heuristics** — Fail-safe defaults, least privilege, separation of privilege, and complete mediation are not slogans; going deeper reveals how they translate into concrete architectural decisions and where violations lead.
- **ISO 27001 and the ISMS** — The dominant organisational security management framework; going deeper covers what certification actually requires and where it creates real accountability versus paper compliance.
- **Singapore's Cybersecurity Act and MAS TRM** — The regulatory framework most directly relevant to this learner profile; covers reporting obligations, critical information infrastructure designations, and sector-specific requirements for financial services.
- **IoT security as a systemic problem** — Billions of devices, long lifespans, no patching culture, persistent exposure; drilling here covers policy and technical approaches that do not rely on expecting manufacturers to act voluntarily.
- **Post-quantum cryptography and migration planning** — The timeline and urgency for organisations to audit cryptographic dependencies and plan migration to PQC algorithms before quantum hardware matures.

---

#### L1-18 · Capstone: Thinking Like a Defender Who Has Done the Attack

The capstone integrates the programme's threads through a controlled ethical hacking engagement against an Active Directory lab environment. Its value as a study topic is not the technical execution — it is the integration: can you attack, interpret, govern, use AI critically, and communicate professionally in one continuous workflow? This topic covers how to approach the exercise as a supply chain of evidence (lab setup → enumeration → analysis → mitigation → executive communication), why AI use must be documentable and critiqueable (the marks sit in validation, not convenience), how to map findings between on-premises controls and their cloud equivalents, and what an executive summary actually requires — register shift, not just length reduction.

**Level 2 candidates:**
- **Active Directory enumeration as an attack surface** — What each protocol on a domain controller (SMB, LDAP, Kerberos, DNS) leaks under default and misconfigured states, and why AD is the highest-value target in most enterprise networks.
- **Critical use of AI in security workflows** — Prompt design, validation patterns, common hallucination modes (fabricated CVEs, miscontextualised advice), and the discipline of documenting human-in-the-loop decisions with enough specificity to be auditable.
- **Translating on-prem controls to cloud equivalents** — The mapping between AD/GPO and Azure AD/RBAC/PIM/Conditional Access, including where the analogies break down — essential for hybrid environments.
- **Writing security findings for mixed audiences** — The structural difference between a technical vulnerability writeup, a mitigation recommendation, and an executive summary, and how to produce all three from the same underlying finding without redundancy.
- **The CIA triad as an analytical lens, not a definition** — How to actively use C-I-A to classify findings and prioritise mitigations, rather than treating it as a definition to recite at the start of a report.

---

## Sequencing note

The domain has genuine dependency structure, and respecting it pays off significantly.

**Cryptography (L1-02 through L1-06) must precede protocol and network security.** L1-07 Protocol Security, L1-08 Network Security, and L1-09 Web Security all reference encryption, hashes, MACs, and certificates without re-explaining them. If you skip the cryptographic stack, the controls in Group III will feel like arbitrary rules rather than solutions to specific problems.

**L1-07 Protocol Security sits between crypto and networks by design.** It is the topic that explains why strong cryptographic primitives are not sufficient — the choreography of who sends what, when, and how each party verifies the other is a separate problem from the cipher. Read it after L1-05 and L1-06, before L1-08.

**The threat framing (L1-01, L1-11) should be visited first and revisited after Group III.** L1-01 establishes the adversarial lens; L1-11 operationalises the attacker's perspective through the kill chain. Re-reading L1-11 after you understand network and web attack surfaces will make ATT&CK feel concrete rather than abstract.

**Access control (L1-10) is the pivot between Group II and Group IV.** It draws on cryptographic concepts (keys, tokens, hashes) and is itself the foundation for cloud security, ethical hacking, and governance. If you are going to invest deeply in one Group III topic before tackling Group IV, make it this one.

**The AI topics (L1-13/14, L1-15) assume Group III is in place.** The value of AI-based detection only becomes clear once you understand what traditional signature-based detection does and where it breaks down. Approaching the AI topics without that context produces a surface-level understanding of algorithms without an understanding of why the architectural shift matters.

**The highest-leverage entry points for a practitioner returning to foundations** are: L1-01 (reset the adversarial lens), L1-04 (authentication, because identity is now the perimeter in cloud and remote-work environments), L1-10 (access control, because most real failures live here), and L1-08 (network security, because the original trust assumptions of TCP/IP are still exploited daily). If you want to add a single AI dimension quickly, L1-13/14 pairs naturally with L1-08 — anomaly detection and traditional network monitoring are strongest when understood together.

The capstone (L1-18) is best approached after completing L1-16 and L1-10, since it presupposes both the ethical hacking workflow and a working model of Active Directory access control. It also rewards having completed L1-13/14 first, since critical AI evaluation is a graded dimension with significant weight.