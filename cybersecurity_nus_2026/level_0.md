# Cybersecurity — Integrated with AI — Level 0: Course Map

> **Intent:** To develop a durable mental model of how digital systems are attacked and defended — and to understand how AI has changed both sides of that equation. The practitioner who studies this domain can reason about threats before they materialise, design controls proportionate to actual risk, and translate technical findings into decisions that non-technical stakeholders can act on.
>
> **Your angle:** You are not here to learn that firewalls exist. You are here to rebuild your mental model from first principles — to understand *why* each layer of security was invented, what problem it failed to solve on its own, and what replaced or extended it. The historical thread matters. Most of the design decisions in modern security are responses to specific failures, and knowing those failures is what makes the controls feel inevitable rather than arbitrary.

---

## How to use this map

This map has two layers below it. **Level 1** is a substantive essay on each topic — the kind of treatment that gives you the reasoning, the historical context, and the "what breaks if you miss this" framing. It is not a textbook chapter; it is closer to a well-structured briefing designed to leave you with a working mental model rather than a definition. **Level 2** candidates are the sub-concepts worth drilling into once you have the Level 1 frame in place. Each is listed here with a directional description — not a definition, but a signal about what going deeper will unlock.

Descend to Level 1 when a topic is load-bearing for something you are trying to do or understand. Descend to Level 2 when a Level 1 post has raised a question you cannot answer with the Level 1 frame alone — or when a specific mechanism is directly relevant to a project or incident you are working through.

---

## Topic Inventory

---

### Group I — The Security Mindset and Threat Reasoning

Before any technical control makes sense, you need the lens through which security professionals read systems. This group establishes that lens: the adversarial mindset, the vocabulary of assets and threats, and the frameworks for thinking about how attacks unfold.

---

#### L1-01 · Introduction to Cybersecurity

Cybersecurity is not reliability engineering — it is the discipline of keeping systems working *while someone is actively trying to make them fail for their own gain*. The presence of an adversary is the entire game, and every control, trade-off, and framework in the field follows from that single premise. This topic establishes the C-I-A triad (confidentiality, integrity, availability) as the three ways an adversary can hurt you; the assets-vulnerabilities-threats-controls vocabulary as the workhorse threat-modelling frame; and the weakest-link principle as the reason technical controls alone can never be enough. Getting this right is the prerequisite for everything downstream — without the adversarial mindset, you will defend the wrong layer.

**Level 2 candidates:**
- **The C-I-A triad in depth** — Drilling here reveals how confidentiality, integrity, and availability conflict in real designs, and why misclassifying which property a control actually protects is the root cause of many security failures.
- **Assets, vulnerabilities, threats, controls** — Unpacks the threat-modelling vocabulary into an operational method you can apply to any system — not just the sketch in Level 1.
- **The weakest-link principle and attack surface** — Explores why adversaries are economically rational, how attack surface expands with digitisation, and why the principle is easy to state but hard to operationalise.
- **Security trade-offs and Security-by-Design** — Covers the structured analysis of security against safety, usability, and cost — the conversation where security strategy actually happens, and the one most rarely taught.
- **The Mosaic Effect and inference attacks on privacy** — Reveals how innocuous datasets combine to re-identify individuals, overturning the intuition that protecting each database in isolation is sufficient.
- **Threat actors and adversary profiling** — Distinguishes external attackers, insiders, contractors, and state actors by motive and method, because the profile changes which controls matter.

---

#### L1-11 · Attacks, Malware & Mitigation

An attack is not an event; it is a chain — and defenders only need to break one link. This topic maps the attacker's playbook in sequence: passive reconnaissance, active scanning, vulnerability identification, exploitation, and persistence. It introduces the Cyber Kill Chain and MITRE ATT&CK as two complementary frameworks for reasoning about that sequence, and covers the malware taxonomy (viruses, worms, trojans, ransomware) in terms of propagation mechanics rather than labels. The WannaCry case study anchors the key lesson: most successful breaches do not use novel techniques — they exploit patch latency, the operational gap between a fix being released and a fix being applied.

**Level 2 candidates:**
- **The MITRE ATT&CK Framework** — Goes beyond the glossary to show how to map your own telemetry against specific techniques — the working language of modern detection engineering.
- **The Cyber Kill Chain and its critiques** — The model's strengths (clarity, narrative) and weaknesses (linearity, perimeter bias) shape how organisations communicate about incidents; understanding the critique prevents you from being limited by it.
- **Vulnerability management: CVE, CWE, CVSS, and KEV** — Turns "we found a bug" into a prioritisation system — the single highest-leverage operational practice in defence.
- **Malware taxonomy and behaviour** — The functional differences between virus, worm, and trojan predict propagation patterns and the kind of countermeasure that will actually work.
- **Patch management as an operational discipline** — Patch latency is empirically the largest contributor to successful breaches; going deeper reveals why the gap is almost entirely a workflow problem, not a technology one.
- **MITRE ATLAS and AI-specific attack surfaces** — The frontier framework for adversarial threats against ML and generative AI systems — prompt injection, model poisoning, training data attacks.

---

### Group II — Cryptographic Foundations

Cryptography is the mechanism underneath almost every other security control: authentication, secure channels, data integrity, and non-repudiation all depend on it. This group builds the cryptographic stack from first principles — symmetric and asymmetric primitives, hash functions, key distribution — and then shows how those primitives are composed into the protocols and infrastructure that secure real communications.

---

#### L1-02 · Cryptography

Cryptography is not the study of secret codes — it is the study of how to formalize and achieve security properties under mathematical assumptions. This topic covers the shift from classical ciphers (substitution, transposition) to Kerckhoffs' Principle — the foundational insight that security should rest on key secrecy, not algorithm secrecy — and on to the formal definitions of cryptosystem security. It explains *why* these definitions were invented: without them, it is impossible to argue rigorously that a scheme is secure rather than merely unbroken so far.

**Level 2 candidates:**
- **Kerckhoffs' Principle versus security by obscurity** — Drilling here reveals why the principle is counterintuitive to most engineers and why violating it is still a common design mistake.
- **Shannon's information theory and perfect secrecy** — The one-time pad is provably unbreakable; understanding why illuminates both the limits of symmetric crypto and the reason all practical systems accept computational rather than information-theoretic security.
- **Classical ciphers and their cryptanalysis** — Caesar, Vigenère, and frequency analysis are worth understanding not for historical interest but because the attacks they fell to — pattern leakage, statistical regularities — recur in modern failures.
- **Computational vs information-theoretic security** — The distinction between "unbreakable in principle" and "unbreakable within available compute time" is the premise on which all modern cryptographic claims rest.

---

#### L1-03 · Modern Ciphers

Stream ciphers and block ciphers are the two families of symmetric encryption used in practice, and the difference between them is not aesthetic — it determines latency, error behaviour, malleability, and the attack surface. This topic maps the mechanics of each family: stream ciphers as synthetic one-time pads (fast, fragile under nonce reuse), block ciphers as structured chunk-by-chunk transformers (strong diffusion, mode-dependent security). The ECB penguin example is here not as a curiosity but as the cleanest demonstration that a strong cipher does not automatically produce a secure system — mode selection is part of the design.

**Level 2 candidates:**
- **Block cipher modes of operation (CBC, CTR, GCM)** — Each mode adds different properties on top of the cipher; GCM in particular is the authenticated encryption workhorse, and going deeper here reveals why "encryption" and "authentication" must be combined.
- **Nonce management and keystream reuse** — The catastrophic failure mode of stream ciphers deserves its own treatment because the constraint "never reuse a nonce" sounds simple and is routinely violated in real systems.
- **Confusion, diffusion, and the avalanche effect** — Shannon's design principles in practice: drilling here connects internal cipher design to observable security properties and explains why changing one bit of input should look like changing half the output.
- **Authenticated Encryption with Associated Data (AEAD)** — ChaCha20-Poly1305 and AES-GCM are the production standards; going deeper reveals why confidentiality and integrity must be constructed together, not separately.
- **Cryptographic agility in system design** — Algorithms age out; going deeper here covers how to design the system so a cipher swap does not require a product rewrite.

---

#### L1-04 · Entity Authentication

Authentication is not a gate — it is a lifecycle, and attackers attack the stages you weren't watching. This topic models the credential lifecycle in three stages — bootstrapping (where trust is born), storage (where a breach can silently become a password leak), and presentation (where human use is the attack surface) — and explains why multi-factor authentication only works when the factors fail differently. The Mirai botnet logged in through factory-default credentials; the LinkedIn breach turned database theft into password theft through unsalted hashes; these cases make the lifecycle model concrete rather than abstract.

**Level 2 candidates:**
- **Password storage: salting, hashing, and modern KDFs** — The implementation details (bcrypt, scrypt, Argon2) determine whether a database breach becomes a password breach — and the difference is in deliberate computational cost.
- **Multi-factor authentication design** — Goes beyond "use MFA" to why some combinations are illusory, why SMS has been deprecated by NIST, and how hardware tokens (FIDO2/WebAuthn) change the phishing threat model.
- **Bootstrapping and credential provisioning** — The most overlooked stage: default passwords, factory provisioning, and credential-recovery flows are where the largest IoT compromises have started.
- **Social engineering and the human attack surface** — Technical authentication controls can be cleanly bypassed by attacks on the person; the defences here are organisational and behavioural, not cryptographic.
- **Biometric authentication and its limits** — Biometrics are excellent for convenience and dangerous as identity roots; the irrevocability problem is the key tension.

---

#### L1-05 · Public Key Systems and Cryptographic Hashes

Symmetric cryptography solves confidentiality but leaves a hard problem unsolved: how do you share a key with someone you've never met? Public key cryptography, introduced independently by Diffie and Hellman (1976) and Rivest, Shamir, and Adleman (1977), dissolves that problem by separating the encryption key from the decryption key. This topic also introduces cryptographic hash functions as the mechanism for turning variable-length input into a fixed-length fingerprint that is easy to compute and practically impossible to reverse or collide — the building block for MACs, digital signatures, and data integrity checks.

**Level 2 candidates:**
- **RSA: trapdoor functions and key size selection** — Going deeper reveals why RSA security rests on the difficulty of factoring large composites, what "2048-bit key" actually means, and where quantum computing threatens this assumption.
- **Elliptic curve cryptography** — ECC achieves comparable security to RSA at much smaller key sizes; drilling here explains why it has largely replaced RSA in modern TLS and why the curve choice matters more than most engineers realise.
- **Hash function properties: preimage resistance, collision resistance** — The formal security properties are not just definitions — each one protects against a different class of attack, and knowing which property is missing from a given use explains the specific failure.
- **Keyed hashes and HMACs** — The construction that turns a hash function into a message authentication code; going deeper reveals why using a plain hash for a MAC is broken and why the specific HMAC construction is not.
- **Post-quantum cryptography** — Shor's algorithm threatens RSA and ECC; drilling here maps the NIST PQC candidate algorithms and the urgency of cryptographic migration planning.

---

#### L1-06 · Data Origin Authentication & Public Key Infrastructure

Symmetric keys prove "someone who knows the secret sent this." Digital signatures prove "the holder of this specific private key signed this, and anyone can verify it." That asymmetry — public verifiability without shared secrets — is what makes non-repudiation and third-party trust possible. This topic covers MACs and digital signatures as the two mechanisms for proving message origin, then explains why the hardest problem in public key cryptography is not the math but the binding of a key to an identity — the problem PKI exists to solve. A CA compromise is not a local failure; it is a system-wide impersonation capability.

**Level 2 candidates:**
- **MAC vs digital signature: choosing for the use case** — The choice between symmetric and asymmetric authentication has concrete consequences for who can verify, who can dispute, and what happens when the shared secret leaks.
- **Certificate lifecycle management** — Issuance, renewal, revocation (OCSP, CRL), and the operational reality that most PKI failures are not mathematical but procedural.
- **Certificate Transparency and CA accountability** — A practical response to the structural weakness of hierarchical trust; drilling here explains how the public append-only log of certificates makes CA misbehaviour detectable.
- **Hash-then-sign and signing large documents** — The engineering pattern that makes asymmetric signing practical at production scale, and why signing raw document bytes is never the right choice.
- **Replay attacks and freshness mechanisms** — A valid signature is still a valid signature tomorrow; going deeper covers timestamps, nonces, and sequence numbers as the constructions that add temporal binding.

---

#### L1-07 · Protocol Security

Cryptographic primitives are not protocols. TLS, SSH, and Kerberos are protocols that compose those primitives — key exchange, authentication, and authenticated encryption — into a sequence that resists not just eavesdropping but active manipulation. This topic covers strong authentication protocols, key exchange (Diffie-Hellman and its variants), and authenticated key exchange as the components that produce a secure channel. The design decisions here — why forward secrecy was added to TLS, why handshake authentication matters — reflect lessons learned from real breaks of earlier, weaker protocols.

**Level 2 candidates:**
- **TLS 1.3 and the evolution of the handshake** — Each version of TLS removed a category of known attack; tracing that evolution reveals exactly what was broken in TLS 1.0–1.2 and why the current design is structured as it is.
- **Forward secrecy and ephemeral key exchange** — Prevents a future private key compromise from decrypting past sessions; drilling here explains why this property was retrofitted rather than designed in from the start.
- **Kerberos and ticket-based authentication** — The dominant enterprise authentication protocol; going deeper reveals how the ticket-granting architecture works, where Kerberoasting attacks operate, and why it connects directly to Active Directory security.
- **Common protocol attacks: downgrade, MITM, replay** — The classes of attack that protocol design specifically defends against; understanding each one explains a structural choice in every modern secure protocol.
- **SSH and secure remote access** — Worth depth because SSH is ubiquitous and its security depends on key management practices that are poorly understood — trust-on-first-use, host key pinning, agent forwarding risks.

---

### Group III — Applied Security Domains

With the cryptographic and threat-reasoning foundations in place, this group covers the concrete attack surfaces that practitioners encounter: the network stack, web applications, host systems, and the cloud. Each topic follows the same pattern — understand how the infrastructure was built to trust, then understand how attackers exploit that trust, then understand what controls exist and why they are structured as they are.

---

#### L1-08 · Network Security

Encryption is not network security. Cryptography secures the payload; it does almost nothing to secure the conversation itself — who you're talking to, whether the address you looked up is genuine, whether the message arrives at all. The TCP/IP stack was built for connectivity, not adversaries, and every protocol you rely on — ARP, DNS, IP routing — takes claims at face value. This topic maps the layers of the stack, the attack class native to each layer (MAC spoofing, IP spoofing, DNS poisoning, DDoS), and the controls (firewalls, DMZs, zero trust architecture) that emerged in response. The Sea Turtle DNS hijacking campaign of 2019 is the cleanest case study: the HTTPS was fine; the address book was poisoned before the connection started.

**Level 2 candidates:**
- **The TCP/IP stack and encapsulation** — Placing an attack at the right layer (ARP vs DNS vs TCP vs application) is the prerequisite for every other network security topic; most learners cannot do this reliably.
- **DNS attacks and DNSSEC** — Cache poisoning, race-condition spoofing, and why adoption of DNSSEC and DoH has lagged despite well-understood attack paths.
- **Firewalls, DMZ, and rule design** — Packet filter vs stateful inspection vs application proxy; default-deny discipline; the two-firewall DMZ sandwich — misconfiguration here is one of the most common real-world breach causes.
- **Zero Trust Network Architecture** — The shift from perimeter defence to per-request verification; worth depth because the term is marketing-saturated and the actual architecture requirements are poorly understood.
- **Denial of Service and DDoS** — The one attack category that cryptography and authentication cannot touch; drilling here covers why Mirai worked and what defences actually exist.
- **Nmap and Wireshark for network analysis** — The dual-use toolkit; skilled use produces very different intelligence from surface-level use, and the difference is worth a dedicated treatment.

---

#### L1-09 · Web Security

Web security is not application security in general — it is the specific set of vulnerabilities that arise from browsers, HTTP, and the trust model of the web. This topic covers the four major classes: UI-based attacks (clickjacking), XSS (injecting scripts into pages trusted by users), CSRF (exploiting ambient browser credentials to forge requests), and SQL injection (breaking the structural separation between query and data). Each vulnerability exists because a parser or a browser does not care about your intentions once it starts interpreting text — which is why the defensive answer is always structural (parameterised queries, output encoding, SameSite cookies) rather than input filtering.

**Level 2 candidates:**
- **The same-origin policy and CORS** — The foundational browser trust mechanism; going deeper reveals why misconfigurations in CORS are a consistent source of data exposure in production APIs.
- **XSS in depth: stored, reflected, DOM-based** — Each type exploits the same root cause through a different injection path; the defensive techniques differ enough to warrant a separate treatment.
- **SQL injection and parameterised queries** — The canonical code-versus-data confusion; drilling here reveals why ORMs do not automatically protect you and where developers still get this wrong.
- **CSRF and SameSite cookies** — The attack exploits the fact that browsers send cookies automatically; going deeper covers the three SameSite values and what each one actually buys you.
- **Session management and token security** — Session tokens are credentials; the security of the session depends entirely on how they are issued, stored, rotated, and invalidated.
- **Content Security Policy and the browser as a security boundary** — CSP is a defence-in-depth mechanism against XSS; drilling here reveals what it can and cannot prevent and why misconfigured CSPs are near-universal.

---

#### L1-10 · System Security and Access Control

Most security failures are not break-ins — they are mundane: someone had access they should not have had, or someone with legitimate access did something they should not have been able to do. The Colonial Pipeline attack began with a forgotten VPN account nobody had decommissioned. This topic provides the formal model for reasoning about these failures: every security-relevant event is a subject–operation–object triple, mediated by a reference monitor consulting a policy. It covers how that policy is represented (ACL vs capabilities vs RBAC), how Linux implements it (the nine permission bits, setuid, sudo), and how the principle of least privilege translates from a slogan into an engineering discipline that bounds blast radius.

**Level 2 candidates:**
- **Access control representations (ACM, ACL, capabilities)** — The choice between object-centric and subject-centric representations ripples through auditing, revocation, delegation, and how OAuth scopes work.
- **Linux/Unix permissions in practice** — Owner/group/other, octal chmod, ACL extensions, the corner cases (sticky bit, umask, directory execute semantics) — where the actual mistakes happen.
- **Controlled invocation and privilege escalation** — Setuid, sudo, and the broader pattern of elevated-privilege execution — every setuid binary is a potential privilege escalation vector, which connects access control directly to exploit development.
- **DAC vs MAC vs RBAC** — The three major policy models have deep consequences for compliance, scalability, and how human error propagates; the choice is an organisational decision, not just a technical one.
- **The principle of least privilege as a design discipline** — Not a slogan but a working method: how to scope service accounts, design permission boundaries, and reason about blast radius in API design, secret management, and incident response.

---

#### L1-12 · Cloud Security

Moving to the cloud does not relocate your perimeter — it dissolves it. The most important mental shift is the shared responsibility model: the provider secures the underlying infrastructure; you secure everything you put on top of it. Getting this boundary wrong is the single most common source of cloud incidents. Public S3 bucket, leaked admin credential, over-broad IAM role — these are not provider failures. This topic covers multi-tenancy and its limits, why identity becomes the new perimeter in cloud environments, how network controls (Security Groups, NACLs) shift from primary defence to supporting layer, and why security must move into the CI/CD pipeline when infrastructure is created from code and changes continuously.

**Level 2 candidates:**
- **Shared responsibility model across IaaS/PaaS/SaaS** — The boundary moves with the service model; going deeper makes explicit what is yours to secure in each tier and where teams most commonly misplace responsibility.
- **Cloud IAM and least-privilege access** — In cloud environments, possession of valid credentials is often the attack path itself; drilling here covers role design, machine identities, temporary credentials, and privilege review.
- **DevSecOps: security in the CI/CD pipeline** — Secret scanning, infrastructure policy-as-code, and dependency checking — going deeper covers the specific integrations that make security continuous rather than a post-deployment checkpoint.
- **Multi-tenancy, side-channel attacks, and confidential computing** — Meltdown and Spectre demonstrated that CPU-level behaviour can leak across logical isolation boundaries; drilling here covers hardware enclaves (SGX, TrustZone) for workloads that require stronger guarantees.
- **SIEM, SOAR, and detection at cloud scale** — At cloud scale, detection cannot depend on people reading logs; going deeper covers how to design telemetry, correlation, and automated response as infrastructure requirements.

---

### Group IV — Contemporary Threats and Professional Practice

The final group covers the domains that complete the practitioner picture: AI as both attacker and defender tool, the offensive techniques a defender must understand, and the governance frameworks that translate technical security into organisational accountability. This group cannot be understood without Group II and III in place — it builds on the controls and vulnerabilities covered there.

---

#### L1-13 & L1-14 · AI in Cybersecurity

For most of cybersecurity's history, defence was a rule-writing exercise. That model broke when attacks scaled beyond any human's ability to characterise them fast enough. This pair of topics covers why AI became unavoidable in security (the volume-and-velocity problem), how supervised and unsupervised ML are used for threat detection (known-bad classification vs anomaly detection), why deep learning specifically matters for network defence (sequence-aware detection that can see multi-stage campaigns rather than isolated events), and what the operational consequences are — the shift from analyst-as-craftsperson to analyst-as-model-overseer. The arms race is real: the same pattern-recognition tools are available to attackers.

**Level 2 candidates:**
- **Supervised vs unsupervised detection: choosing the right frame** — The data labelling question is upstream of every algorithm choice; getting it wrong produces a confidently wrong model.
- **Feature engineering for security data** — Two teams using the same algorithm get very different outcomes depending on how they represent network behaviour numerically — this is where most implementations fail silently.
- **Precision, recall, and the cost of each error type** — Model tuning in security is a cost dial, not a truth dial: false positives have different business owners than false negatives, and the tradeoff is ultimately a business decision.
- **Recurrent architectures for sequence-aware detection** — LSTMs and their context windows are what let a model connect today's packet to yesterday's probe — the crux of why deep learning matters for APT detection.
- **Explainable AI in SIEM (the AMIDES pattern)** — Explainability is the pivot point determining whether AI gets adopted in real security operations or stays in research; analysts will not trust verdicts they cannot interrogate.
- **AI-driven penetration testing and continuous red teaming** — The shift from quarterly human red teams to 24/7 autonomous agents inverts the economics of offensive security and previews the attacker-side use of the same techniques.

---

#### L1-15 · Generative AI for Cybersecurity

Generative AI introduces both new attack surfaces and new defensive capabilities — simultaneously. On the attack side, it enables high-volume, personalised phishing at near-zero marginal cost; synthetic media for social engineering (the 2024 Arup deepfake: $25M wired to a synthetic CFO); and accelerated vulnerability discovery. On the defensive side, it enables natural-language interfaces to SIEM systems, automated code review, and security report generation. The unstable part is that the same model capabilities that make LLMs useful for defenders make them useful for attackers, and the adversarial surface of the models themselves — prompt injection, training data poisoning — is largely uncharted.

**Level 2 candidates:**
- **Prompt injection and AI-native attack vectors** — The category of attack that has no analogue in traditional security; drilling here reveals why input-based defences against prompt injection are fundamentally weak and what structural alternatives exist.
- **Deepfakes and synthetic media in social engineering** — The Arup case is the template; going deeper covers detection methods, organisational policies (callback verification), and the limits of technical countermeasures.
- **LLM-assisted red teaming and vulnerability discovery** — AI can enumerate attack paths faster than humans; going deeper covers both the offensive capability and how defenders can use the same tools to find their own weaknesses first.
- **Responsible disclosure and AI security governance** — The policy frameworks that manage vulnerability research in a world where AI accelerates both discovery and exploitation.

---

#### L1-16 · Ethical Hacking

You cannot defend what you cannot break. Ethical hacking is the practice of simulating adversarial pressure under authorisation and scope — not to demonstrate that the tester is clever, but to produce prioritised remediation guidance. This topic covers the structured engagement funnel (reconnaissance → scanning → exploitation → post-exploitation → reporting), the legal framework that separates white from black hat (Singapore's Computer Misuse Act; the difference between a penetration test contract and a criminal offence), and the offensive toolchain (Nmap, Metasploit, privilege escalation, session hijacking). Lateral movement is the practical argument against perimeter-only security: a single compromised edge device that can reach internal resources reveals that "inside the network" has been silently equated with "trusted."

**Level 2 candidates:**
- **The attack lifecycle and cyber kill chain** — Each stage has distinct tooling, distinct detection signatures, and distinct mitigation strategies; understanding the full chain is what lets defenders break it at the cheapest point.
- **The Metasploit framework and exploitation workflows** — How modular exploitation frameworks industrialise known attack paths; understanding the module structure teaches how vulnerability research becomes reusable tooling.
- **Privilege escalation techniques** — Password cracking, buffer overflow mechanics, and misconfiguration-based escalation — where most real breaches actually progress, and the underlying mechanics are foundational rather than tool-specific.
- **Rules of engagement and the legal framework** — Scope definition, authorisation documents, and the relevant legislation; the legal exposure for getting this wrong is severe and the documentation practices are non-obvious.
- **Reporting, CVSS, and remediation translation** — The report is the actual product of an ethical hacking engagement; translating a technical exploit into a business-relevant risk statement is what separates competent testers from valuable ones.

---

#### L1-17 · Ethics, Governance and the Future of Cybersecurity

Technical controls fail. When they do, governance frameworks, codes of conduct, and legal obligations are the remaining structure. This topic covers the security principles that predate and outlive specific controls (defence-in-depth, fail-safe defaults, separation of privilege), the governance standards that operationalise them at an organisational level (ISO 27001, NIST CSF, Singapore's Cybersecurity Act 2018, MAS TRM guidelines), and the professional ethics obligations that define what a practitioner is accountable for. It also surveys emerging threats — AI-enabled attacks, IoT proliferation, quantum computing's implications for current cryptographic infrastructure — and explains why the discipline is not converging toward a fixed endpoint.

**Level 2 candidates:**
- **Security principles as design heuristics** — Fail-safe defaults, least privilege, separation of privilege, and complete mediation are not slogans; drilling here reveals how they translate into concrete architectural decisions and where violations lead.
- **ISO 27001 and the ISMS** — The dominant organisational security management framework; going deeper covers what certification actually requires and where it creates accountability.
- **Singapore's Cybersecurity Act and MAS TRM** — The regulatory framework most relevant to this learner profile; going deeper covers reporting obligations, critical information infrastructure designations, and sector-specific requirements.
- **IoT security as a systemic problem** — Billions of devices with long lifespans, no patching culture, and persistent exposure; drilling here covers the policy and technical approaches that do not rely on expecting manufacturers to act voluntarily.
- **Post-quantum cryptography and migration planning** — The timeline and urgency for organisations to audit cryptographic dependencies and plan migration to PQC algorithms before quantum hardware matures.

---

#### L1-18 · Capstone: Thinking Like a Defender Who Has Done the Attack

The capstone integrates the programme's threads through a controlled ethical hacking engagement against an Active Directory lab environment. Its value as a study topic is not the technical execution — it is the integration: can you attack, interpret, govern, use AI critically, and communicate professionally in one continuous process? This topic covers how to approach the capstone as a supply chain of evidence (lab setup → enumeration → analysis → mitigation → reflection), why AI use must be documentable and critiqueable rather than opaque, how to map findings across on-premises controls and their cloud equivalents, and what an executive summary actually requires in terms of register shift and information selection.

**Level 2 candidates:**
- **Active Directory enumeration as an attack surface** — What each protocol on a domain controller (SMB, LDAP, Kerberos, DNS) leaks under default and misconfigured states, and why AD is the highest-value target in most enterprise networks.
- **Critical use of AI in security workflows** — Prompt design, validation patterns, common hallucination modes (fabricated CVEs, miscontextualised advice), and the discipline of documenting human-in-the-loop decisions.
- **Translating on-prem controls to cloud equivalents** — The mapping between AD/GPO and Azure AD/RBAC/PIM/Conditional Access, including where the analogies break down — essential for hybrid environments.
- **Writing security findings for mixed audiences** — The structural difference between a technical vulnerability writeup, a mitigation recommendation, and an executive summary, and how to produce all three from the same finding.
- **The CIA triad as an analytical lens, not a definition** — How to actively use C-I-A to classify findings and prioritise mitigations, rather than treating it as a definition to recite.

---

## Sequencing note

The domain has a genuine dependency structure, and respecting it pays off.

**Cryptography (L1-02 through L1-07) must precede the network and web topics.** Network security, web security, and protocol security all reference encryption, MACs, and certificates without re-explaining them. If you skip the cryptographic stack, the controls in Group III will feel like arbitrary rules rather than solutions to specific problems.

**The threat framing (L1-01, L1-11) should be visited first and revisited after Group III.** L1-01 establishes the lens; L1-11 operationalises it for the attacker's perspective. Re-reading L1-11 after you understand the network and web attack surfaces will make the kill chain and ATT&CK matrix feel concrete rather than abstract.

**Access control (L1-10) is the pivot point between Group II and Group III.** It draws on cryptographic concepts (keys, tokens, hashes) and is itself the foundation for cloud security, ethical hacking, and governance. If you are going to invest in one topic from Group III before tackling Group IV, make it this one.

**The AI topics (L1-13/14, L1-15) assume Group III is in place.** The value of AI-based detection only becomes clear when you understand what traditional signature-based detection does and where it breaks down. Approaching the AI topics cold produces a surface-level understanding of algorithms without an understanding of why the architectural shift matters.

**The highest-leverage entry points for a practitioner returning to foundations** are L1-01 (to reset the adversarial lens), then L1-04 (authentication, because identity is now the perimeter), then L1-10 (access control, because most real failures live here), then L1-08 (network security, because the original assumptions of the TCP/IP stack are still exploited daily). If you want to add a single AI dimension quickly, L1-13/14 pairs well with L1-08 — anomaly detection and traditional network monitoring are strongest when read together.

The capstone (L1-18) is best approached after L1-16 and L1-10, because it presupposes both the ethical hacking workflow and a working model of access control and Active Directory. It also rewards having done L1-13/14 first, since AI critical evaluation is a graded dimension.

## Source

https://nus.comp.emeritus.org/cybersecurity