# Cybersecurity — Integrated with AI (NUS) — Level 0: Course Map

> **Intent:** To develop the mental models, technical vocabulary, and adversarial thinking required to assess and defend real systems — not as a checklist practitioner, but as someone who understands why controls exist and what breaks when they fail.
>
> **Your angle:** You are returning to foundations with professional experience, not starting from scratch. The goal is to replace fuzzy intuitions ("we use encryption, so we're secure") with precise ones ("what exactly is this control protecting, against which adversary, at which stage of the attack chain?"). Prioritise the reasoning behind decisions over the definitions.

---

## How to use this map

This document is a navigation tool, not a study guide. It maps the territory before you enter it.

**Level 1** is the topic as covered in this course — conceptual depth, historical context, the problem the mechanism solves, and its failure modes. You have already encountered Level 1 through the course materials. Return here to locate where a topic sits relative to others.

**Level 2** is where you go to go narrower and deeper — specific algorithms, implementation details, edge cases, worked examples. Descend to Level 2 when a Level 1 concept is blocking you from reasoning clearly about a real system, or when you want to build genuine technical fluency rather than conceptual familiarity.

The map is meant to be navigated non-linearly. Use the sequencing note at the bottom to find your highest-leverage entry points.

---

## Topic Inventory

### Group I — The Adversarial Foundation

Before any mechanism makes sense, you need the lens: what cybersecurity is actually for, what it means to have an adversary, and the three primitive ways things can go wrong.

#### L1-01 · The Adversarial Mindset and Security Fundamentals

Cybersecurity begins the moment someone benefits from your system failing. This distinction from reliability engineering — intentional pressure versus random failure — changes every downstream decision. The CIA triad (confidentiality, integrity, availability) gives you a precise vocabulary for classifying failures: the Snowden disclosures are a confidentiality failure; the 2013 AP Twitter hack that wiped $136bn in market value is an integrity failure; Colonial Pipeline is an availability failure. Everything else in this field is machinery for diagnosing and preventing one of those three. The assets/vulnerabilities/threats/controls framework is the practitioner's daily tool for reasoning about cause and effect. The weakest-link principle is the single most important operational insight: your security posture is not the average of your controls, it is the minimum.

**Level 2 candidates:**
- **The CIA triad as engineering requirements** — Unpacks how each property is achieved technically and where they conflict with each other in real designs, rather than treating them as slogans.
- **Threat modelling with assets, vulnerabilities, and controls** — The formal walkthrough practitioners use daily; the Level 1 pass only sketches it.
- **The weakest-link principle and attack surface** — Why adversaries are economically rational, how attack surface expands with digitisation, and how organisations actually fail to operationalise this insight.
- **Security as trade-off and Security-by-Design** — The structured analysis of security against safety, usability, performance, and cost; where the strategy conversation actually happens.
- **Threat actor profiling** — Distinguishes external attackers, insiders, nation-states, and hacktivists by motive and capability, which drives which controls matter.
- **The Mosaic Effect and inference attacks** — How anonymised datasets combine to re-identify individuals; overturns the mental model that protecting each database in isolation is sufficient.

---

### Group II — Cryptographic Foundations

Cryptography is the mathematical layer underlying nearly every other security mechanism. This group must be understood before authentication, protocols, PKI, or secure channels make sense. The order within the group is a genuine dependency chain.

#### L1-02 · Classical and Modern Cryptography

The field is not a contest of cleverness — it is about economics, transparency, and key secrecy. The history is a long retreat from perfect secrecy (the one-time pad, which is mathematically unbreakable but operationally useless) toward computational security (hard enough to break that the attacker's cost exceeds the defender's stake). Kerckhoffs' Principle — the system must remain secure even if everything except the key is public — is the single idea most worth internalising from this cluster. Secret algorithms are trusted by those who haven't examined them; public algorithms are trusted by those who have. This principle predicts most of the cryptographic disasters you will read about: proprietary ciphers, security-by-obscurity, and "nobody will find this endpoint."

**Level 2 candidates:**
- **Kerckhoffs' Principle and the case against obscurity** — Why open, peer-reviewed algorithms consistently outperform proprietary ones; the historical evidence and the structural reasons.
- **Classical ciphers and frequency analysis** — The precise mechanics of how statistical attacks dismantle substitution ciphers; fastest way to internalise why "preserves structure = broken."
- **The one-time pad and perfect secrecy** — Information-theoretic security, why OTP achieves it, and the Venona case where reuse broke Soviet communications.
- **Computational security and key length calibration** — How hardness assumptions translate into key-length recommendations; why nominal and effective key lengths differ.
- **Adversary models: black-box, grey-box, and side-channel** — The taxonomy from ciphertext-only through timing and power attacks; where most real-world cryptographic failures actually occur.

#### L1-03 · Modern Ciphers — Stream and Block

The algorithm is rarely where systems fail; the failure is almost always in how the algorithm is used. Stream ciphers (RC4, ChaCha20) generate a pseudorandom keystream and XOR against plaintext — fast, minimal latency, but catastrophically fragile to keystream reuse. Block ciphers (AES) process fixed chunks through structured rounds — strong diffusion but sensitive to mode of operation. ECB mode is the canonical lesson: identical plaintext blocks produce identical ciphertext blocks, which is why you can still see the penguin. Authenticated encryption modes (GCM) and counter-based modes (CTR) exist because confidentiality and integrity are separate problems requiring separate machinery.

**Level 2 candidates:**
- **Stream cipher internals** — RC4, Salsa20, ChaCha20; why RC4 was deprecated while ChaCha20 thrives; what cryptographic strength means concretely.
- **Block cipher internals and AES** — Substitution-permutation networks, S-boxes, key schedules; confusion and diffusion made concrete.
- **Modes of operation** — ECB, CBC, CTR, GCM; where most real-world cryptographic failures live; when to use which.
- **IV and nonce handling** — Rules around uniqueness, length, randomness versus counter-based generation; most common operational failure in deployed systems.
- **Cryptographic agility and algorithm lifecycle** — How algorithms are standardised and deprecated (DES, RC4); designing for algorithm replacement; the post-quantum transition already underway.

#### L1-04 · Public Key Systems and Cryptographic Hash Functions

Symmetric encryption has a scaling problem: distributing shared keys requires an already-secure channel. Public key cryptography breaks the loop. Each party holds a mathematically linked pair: a public key anyone can use, a private key only you hold. Anything encrypted with the public key decrypts only with the private key (confidentiality); anything signed with the private key verifies with the public key (authenticity and non-repudiation). RSA builds this asymmetry on integer factorisation. The catch: RSA is orders of magnitude slower than AES. The solution is hybrid encryption — generate a fresh AES key, encrypt data with AES, encrypt only the AES key with RSA. This is what TLS does on every HTTPS connection. Cryptographic hash functions (SHA-256) give you integrity: the same input always produces the same fixed-length fingerprint, but a one-bit input change avalanches the output. Blockchain is hash functions plus signatures plus a tiebreaker — no magic.

**Level 2 candidates:**
- **RSA and trapdoor functions** — Prime generation, modular exponentiation, why integer factorisation is the hard problem, why post-quantum is a real concern.
- **Hash functions in depth** — Preimage resistance, collision resistance, Merkle-Damgård and sponge constructions, MACs and password-hashing schemes.
- **Hybrid encryption and the envelope pattern** — Ephemeral key generation, key wrapping, GCM; where real-world cryptographic failures happen at the seams.
- **Digital signatures and non-repudiation** — How signing differs from encryption, hash-then-sign, DSA/ECDSA/EdDSA, legal meaning of non-repudiation.
- **Key management and the private key problem** — Generation, HSMs, rotation, revocation, recovery; the gap between "we use RSA-2048" and "our keys are actually safe."
- **Post-quantum cryptography** — Why Shor's algorithm threatens RSA and ECC, lattice-based alternatives, designing for crypto-agility before the transition.

#### L1-05 · Data Origin Authentication and PKI

The hard problem in cryptography is not the math — the math has been solved. The hard problem is trust: when a server sends you a public key claiming to be your bank, why should you believe it? MACs (Message Authentication Codes) provide symmetric authentication — fast, suited for high-volume bilateral traffic, but neither party can prove to a third party who sent the message. Digital signatures provide asymmetric authentication — slower, but binding and publicly verifiable; what holds up in court. PKI is the bureaucratic infrastructure that binds public keys to identities: Certification Authorities examine identity claims and issue signed certificates; chains of trust route up to a small set of root CAs pre-installed in your browser. The 2011 Comodo breach (fraudulent certificates issued for Google, Yahoo, and others accepted by every browser) is the canonical failure mode. Most PKI failures in practice are not cryptographic — they are operational: expired certificates, bad renewal processes, smart cards that stop working during critical trading.

**Level 2 candidates:**
- **MACs vs digital signatures in depth** — HMAC mechanics, RSA-PSS/ECDSA/EdDSA; how non-repudiation is formally argued; key distribution and post-quantum concerns.
- **X.509 certificates and chain validation** — What is inside a certificate, how chain validation walks from leaf to root, name constraints and extended key usages.
- **Certificate revocation: CRLs, OCSP, and stapling** — Why CRLs scale badly, OCSP privacy and availability problems, stapling; where PKI consistently fails in practice.
- **The CA trust model and Certificate Transparency** — How root CAs are admitted to browser trust stores, what CT logs added after Comodo and DigiNotar, how the ecosystem handles CA misbehaviour.
- **PKI lifecycle management** — Tiered hierarchies, HSM-backed storage, ACME/Let's Encrypt, automated issuance; where enterprise PKI projects actually live or die.
- **Freshness, uniqueness, and the limits of PKI** — Replay attacks, nonces, timestamps; why signatures don't prove freshness and what distributed ledgers add.

---

### Group III — Applied Security Domains

With the cryptographic foundation in place, this group applies it to the actual systems where most security work happens: protocols, networks, the web, host operating systems, and the adversarial techniques used to attack them.

#### L1-06 · Protocol Security

Even when individual primitives (ciphers, hashes, signatures) are sound, their composition can fail. Protocol security asks: how do you combine the pieces into an authenticated key exchange that establishes a secure channel between parties who have never met before? The canonical failures — replay attacks, man-in-the-middle attacks, downgrade attacks — all come from incorrect assumptions about the protocol environment. TLS is the worked example that ties together everything in Group II: certificate validation for identity, key exchange for a shared session key, symmetric encryption for bulk data, and MACs for integrity.

**Level 2 candidates:**
- **TLS handshake in detail** — Certificate validation, key exchange mechanisms (ECDHE), cipher suite negotiation, session resumption.
- **Authenticated key exchange protocols** — Diffie-Hellman, forward secrecy, and why the session key must not be derivable from the long-term private key.
- **Protocol failure modes** — Replay, MITM, downgrade, oracle attacks; why correct primitives in incorrect composition still fail.
- **SSH and other secure channel protocols** — How host key verification works, known-hosts files, common misconfigurations.

#### L1-07 · Network Security

The TCP/IP stack was designed for connectivity, not adversaries. ARP, DNS, and IP all accept claims at face value — which is why network attacks mostly look like forging labels rather than breaking encryption. The Sea Turtle campaign (2019) hijacked national-level DNS traffic across forty-plus countries without breaking any cryptography. Nmap and Wireshark are the dual-use tools that define the network security discipline: the same scan that maps an attacker's target maps the defender's perimeter. The perimeter firewall (default-deny, specific-allow, DMZ for public-facing services) is the classical control; Zero Trust Network Architecture (verify every request regardless of origin, grant least privilege, assume breach) is the contemporary response to the dissolution of "inside" as a meaningful security category.

**Level 2 candidates:**
- **The TCP/IP stack and encapsulation** — Which class of attack lives at which layer; MAC spoofing, IP spoofing, TCP hijacking, application-layer injection.
- **DNS attacks and DNSSEC** — Cache poisoning, race-condition spoofing, hijacking campaigns; DNSSEC, DoH, DoT; why adoption has lagged.
- **Firewalls, DMZ, and rule design** — Packet filters vs stateful inspection vs application proxies; two-firewall DMZ construction; rule ordering and stateful tracking mechanics.
- **Zero Trust Network Architecture** — Per-request verification, microsegmentation, continuous authorisation; what it actually requires in practice.
- **DDoS and volumetric attacks** — Volumetric vs protocol vs application-layer attacks; Mirai botnet economics; defences that actually work.
- **Wireshark and Nmap in depth** — Capture filters, TCP stream reconstruction, scan types, OS fingerprinting; the gap between running the tool and using it well.

#### L1-08 · Web Security

The web is the most exposed surface your organisation has, and it is exposed for a structural reason: HTTP was designed to fetch documents. Everything else — cookies for memory, JavaScript for behaviour, databases for data — was retrofitted onto a stateless protocol that assumed a polite academic user. The dominant web attacks all share a single root cause: the receiving system cannot distinguish code from data. SQL injection sends user input to the database parser as if it were query syntax. XSS sends attacker-controlled content to the browser parser as if it were page logic. The fixes are structural — prepared statements, output encoding — not cosmetic (blacklists fail). CSRF exploits the browser's automatic credential forwarding; anti-CSRF tokens fix it by requiring proof of intentional request origin. The OWASP Top 10 is the empirical consensus on which categories are causing actual breaches; STRIDE is the structured lens for finding them before they ship.

**Level 2 candidates:**
- **SQL injection and prepared statements** — How injection works at the query-parser level; blind and time-based variants; why ORMs don't automatically protect you.
- **XSS and output encoding** — Reflected, stored, and DOM-based variants; encoding rules that differ by context (HTML body, attribute, JavaScript, URL); Content Security Policy.
- **Session management and cookie security** — Session lifecycle, HttpOnly/Secure/SameSite flags, token rotation, session fixation, pass-the-cookie attacks that bypass MFA.
- **CSRF and the Same-Origin Policy** — Precise SOP rules, anti-CSRF token mechanics, SameSite cookies; the subtle cross-origin exceptions that create bypasses.
- **Threat modelling with STRIDE and OWASP** — Structured frameworks for finding threats before code is written; STRIDE's six categories; OWASP ASVS as a standards reference.
- **HTTPS and TLS for web security** — What TLS guarantees and what it does not; the "malicious cafe owner" threat model; where the guarantees end.

#### L1-09 · System Security and Access Control

Most security failures are not break-ins — they are mundane: someone had access they shouldn't have had. Colonial Pipeline began with a forgotten VPN account. Every security-relevant event reduces to a triple: subject (user, process) wants to perform an operation (read, write, execute) on an object (file, device, service). The reference monitor decides. The access control matrix is the general model; ACLs (per-object lists) and capabilities (per-subject tokens) are practical slices of it. Linux collapses this into nine permission bits per file — useful, lossy, and the system most practitioners will actually configure. Setuid is controlled invocation: a normal user temporarily borrows root's authority for a narrow task; every setuid binary is a trapdoor into root, and bugs in setuid programs are privilege escalation vulnerabilities. Least privilege is blast-radius engineering: it doesn't prevent compromise, it limits its consequences.

**Level 2 candidates:**
- **Access control representations: ACM, ACL, capabilities** — Operational tradeoffs between object-centric and subject-centric views; how OAuth, Kerberos, and Linux permissions work under the hood.
- **Linux/Unix permissions in practice** — Owner/group/other model, octal chmod, ACL extensions, the "everything is a file" philosophy; where mistakes happen.
- **Controlled invocation and privilege escalation** — Setuid, setgid, sudo, and the attack surface they create; the bridge from access control to exploit development.
- **DAC vs MAC vs RBAC** — Policy model choice as an organisational decision with compliance, scalability, and error-propagation consequences.
- **The principle of least privilege as a design discipline** — Scoping service accounts, designing permission boundaries, break-glass scenarios, reasoning about blast radius.

#### L1-10 · Attacks, Malware, and Mitigation

Defence is best built by understanding the attack chain, not by cataloguing assets. An attack is a sequence: reconnaissance (passive OSINT, WHOIS, Shodan), active scanning (Nmap, vulnerability scanners, CVE/CVSS databases), exploitation (Metasploit industrialises known CVE-to-payload matching), and persistence (the overlooked stage — malware planted so patching the original hole doesn't evict the attacker). WannaCry is the canonical lesson: Microsoft had patched EternalBlue two months before the attack; the vulnerability was patch latency, not the cryptography. MITRE ATT&CK is the working operational framework (real adversary TTPs, matrix-structured); the Cyber Kill Chain is the narrative framework (linear, useful for executive communication); MITRE ATLAS extends both to attacks against AI systems.

**Level 2 candidates:**
- **MITRE ATT&CK in depth** — Mapping telemetry against specific techniques rather than treating it as a glossary; how to use it for detection engineering.
- **The Cyber Kill Chain and its critiques** — Strengths (clarity, narrative) and weaknesses (linearity, perimeter bias); why critique enables better use.
- **Vulnerability management: CVE, CWE, CVSS, KEV** — How the ecosystem turns "we found a bug" into "we know priority and exploitation status"; what each acronym actually tells you.
- **Malware taxonomy and behaviour** — Viruses, worms, trojans, ransomware, and wipers as distinct propagation patterns driving different defensive strategies.
- **Patch management as an operational discipline** — Patch latency as an operational metric; organisational and technical practices that determine remediation speed.
- **MITRE ATLAS and AI-specific attack surfaces** — Prompt injection, model evasion, training data poisoning; the framework for the next decade of incidents.

---

### Group IV — Contemporary and Emerging Domains

These topics sit at the frontier of the discipline. Cloud security is already mainstream practice; AI in cybersecurity is the fastest-moving area in both attack and defence; governance and quantum are the long-horizon topics that most practitioners underinvest in until they become urgent.

#### L1-11 · Cloud Security

Moving to the cloud does not move your perimeter — it dissolves it. The shared responsibility model is the first mental shift: the provider secures the infrastructure (data centres, hypervisors, physical network); you secure everything you deploy on top (data, IAM configurations, application code). Most cloud breaches are the customer's fault — a public S3 bucket, a leaked admin credential, an over-privileged service account. Multi-tenancy means your workload shares physical hardware with strangers; logical isolation via hypervisor is strong but not absolute (Meltdown, Spectre). IAM becomes the perimeter: if IAM policies are loose, there is no perimeter. DevSecOps and SIEM/SOAR are not optional hardening — they are required because cloud infrastructure changes faster than any human review cycle can track.

**Level 2 candidates:**
- **Shared responsibility across IaaS, PaaS, SaaS** — Exactly which obligations belong to provider vs customer at each tier, with worked examples.
- **Multi-tenancy and side-channel attacks** — Hypervisor isolation mechanics; Meltdown/Spectre; hardware enclaves (Intel SGX, ARM TrustZone).
- **IAM as the new perimeter** — Least privilege, RBAC, MFA strategies, FIDO hardware keys, failure modes of cloud identity systems.
- **DevSecOps and shift-left security** — CI/CD pipeline integration of scanning, secret detection, infrastructure-as-code validation; the cultural shift.
- **Telemetry, SIEM, and SOAR** — Cloud audit logging (CloudTrail), aggregation and detection, automated response playbooks; the architecture for detection at cloud scale.
- **Data sovereignty, compliance, and systemic risk** — GDPR, HIPAA, MAS; geographic data pinning vs disaster recovery; hyperscaler concentration risk.

#### L1-12 · AI in Cybersecurity

AI in security is not fashionable — it is a response to a mismatch. The volume of traffic, the pace of attacker iteration, and the novelty of threats all exceed what human-authored rule sets can handle. The enabling shift was hardware: GPUs repurposed from pixel rendering turned out to map almost perfectly onto the matrix operations underlying neural networks. Traditional ML (supervised learning on labelled data) handles known categories precisely but cannot see what it has never been named. Unsupervised learning (anomaly detection on unlabelled data) is the only approach that meaningfully addresses zero-days. Deep learning adds temporal awareness: RNNs and LSTMs carry state forward, so a model can connect Monday's scan to next month's exfiltration — the attack that is invisible to any point-in-time classifier. False positives and false negatives have different price tags in security; tuning a model is a business risk decision, not a technical one.

**Level 2 candidates:**
- **Supervised vs unsupervised learning in security** — Practical tradeoffs, labelling pipeline design, how teams convert anomaly flags into training data.
- **False positives, false negatives, and F-1 score as business strategy** — How error tradeoffs map onto business risk and customer experience; the metric becoming a board-level concern.
- **Feature engineering from network traffic** — How raw PCAPs become numeric features; where domain expertise compounds over identical algorithms.
- **Recurrent architectures for sequence-aware detection** — RNNs, LSTMs, context windows applied to network traffic; the shift from event classification to campaign detection.
- **Explainable AI in SIEM (AMIDES pattern)** — How deep learning outputs are attributed back to interpretable rules; the adoption pivot in operational security.
- **Data preprocessing for security ML** — Normalisation, class imbalance, concept drift, adversarial contamination; where most implementations fail silently.

#### L1-13 · Generative AI and Cybersecurity

Generative AI changes the economics of attack more than it changes the categories. A convincing phishing email, a working exploit for a known CVE, a mutating malware variant — none of these are new. What is new is that producing them no longer requires a competent attacker. The defender's response requires both the CVE/CWE/CVSS/ATT&CK/ATLAS stack (to reason from specific vulnerability to adversary behaviour to priority) and new AI-native defences (GenAI for log summarisation, rule generation, synthetic training data, autonomous red-teaming). The unresolved tension: AI can act faster than humans, but AI acting autonomously introduces unverifiable mistakes. The governance layer — EU AI Act, NIST AI RMF, explainability requirements — is where security leadership careers will be made or broken over the next decade.

**Level 2 candidates:**
- **The CVE/CWE/CVSS/ATT&CK/ATLAS stack as integrated workflow** — Traversing from specific flaw to root cause to priority to adversary behaviour; the leverage that comes from treating them as one chain.
- **LLM jailbreaking and guardrail design** — Techniques for bypassing model safety instructions; input/output filtering; adversarial testing; system prompt hardening.
- **Polymorphic and metamorphic malware** — How malware mutates to evade signatures; what behavioural and ML-based detection looks like in response; how GenAI changes the economics.
- **GenAI-driven SOC operations** — Log summarisation, automated rule generation, synthetic data, copilot-assisted triage; the gap between "use AI in the SOC" and a working integration.
- **MITRE ATLAS in depth** — Adversarial threats specific to ML systems; model evasion, data poisoning, prompt injection; the framework practitioners increasingly need.
- **AI governance, ethics, and liability** — EU AI Act, NIST AI RMF, explainability obligations, accountability when autonomous defenders cause harm.

#### L1-14 · Ethical Hacking

The line between a hacker and a security professional is a piece of paper. Every technique — Nmap scanning, Metasploit payloads, password cracking — is identical on both sides of the authorisation boundary; what separates them is a signed Rules of Engagement document. Ethical hacking is paying someone to bring the attacker's methodology to bear on your systems before an attacker does. The workflow is a funnel: passive OSINT → active scanning → version detection (the hinge — VSFTPD 2.3.4, not "an FTP server") → exploitation via Metasploit → post-exploitation (privilege escalation, lateral movement) → reporting with CVSS scores. Reverse shells are preferred over bind shells because the target initiates the outbound connection, bypassing inbound firewall rules. The deliverable is not the breach; it is the prioritised list of paths to fix.

**Level 2 candidates:**
- **Nmap and active network scanning in depth** — SYN, connect, UDP, idle scans; service version detection; NSE scripting; what each scan type puts on the wire.
- **Metasploit and exploitation workflows** — Module structure, payload selection (bind vs reverse, staged vs stageless), Meterpreter post-exploitation.
- **Privilege escalation techniques** — Password cracking with John the Ripper/Hashcat; buffer overflow mechanics; misconfiguration-based escalation paths.
- **Rules of Engagement and the legal framework** — Scope definition, authorisation documents, Singapore's Computer Misuse Act; the legal exposure of getting this wrong.
- **Reporting, CVSS, and remediation translation** — Scoring, prioritisation, and communicating to non-technical stakeholders; the report as the actual product.
- **The attack lifecycle and cyber kill chain (applied)** — Each stage's tooling, detection signatures, and where defenders can most cheaply break the chain.

#### L1-15 · Ethics, Governance, and the Future of Cybersecurity

Security has stopped being a function and started being a posture. A function is something a team performs; a posture is something the entire organisation maintains. Strategic alignment means security goals are written in the language of business outcomes. The CISO shapes strategy; the board holds accountability — the right design, because accountability inside the security team is accountability nobody else feels. RACI (Responsible, Accountable, Consulted, Informed) is the antidote to "I thought someone else had that." The three lines of defence keep operations, oversight, and audit independent. Ethics in the profession sits on four pillars — confidentiality, integrity, objectivity, due care — because the same skills that defend a system compromise one. Vulnerability disclosure is the canonical ethics test: Google Project Zero's 90-day window is the de facto industry clock. The two long-horizon threats worth taking seriously now: generative AI compressing attacker cycles to machine speed, and quantum computing threatening the cryptographic substrate (Shor's algorithm breaks RSA and ECC; "harvest now, decrypt later" means data intercepted today is at risk the moment a capable quantum computer exists).

**Level 2 candidates:**
- **Security governance frameworks and RACI** — NIST and COBIT as reference frameworks; the policy/standard/guideline/procedure hierarchy; how RACI assigns ownership in practice.
- **The three lines of defence model** — Why the model is widely cited and widely misimplemented; what each line actually does.
- **Professional code of ethics and vulnerability disclosure** — The four pillars, the legal landscape post-Morris Worm, the mechanics of responsible disclosure.
- **Defence in depth across network, cloud, and IoT** — DMZ architectures, IDS/IPS, SIEM, hardware roots of trust (PUFs, Secure Enclave).
- **The quantum threat and post-quantum cryptography** — Shor's and Grover's algorithms; harvest-now-decrypt-later risk; the NIST PQC migration path.
- **Secure hardware as a root of trust** — PUFs, Apple Secure Enclave, ARM TrustZone; hardware as the last defensible boundary as software exploitation gets automated.

---

## Sequencing Note

The curriculum is structured as a genuine dependency chain, not an arbitrary sequence, and the dependencies are real.

**The hard floor:** L1-01 (adversarial mindset) → L1-02 (cryptography foundations) → L1-04 (public key and hash) → L1-05 (PKI and data origin authentication). Nothing in the Applied or Contemporary groups makes full sense without these. If you feel uncertainty in any applied topic, trace it back — it almost always resolves to a fuzzy concept in Group II.

**For a practitioner returning to fill gaps:** The highest-leverage entry points are L1-01 (to get the adversarial lens precise), L1-09 (access control — most breaches are mundane failures here), and L1-10 (attacks and mitigation — understanding the chain is what makes defensive architecture feel like a response to something real rather than a compliance list). From those three, the rest of the map falls into place.

**For someone building toward AI-era security roles:** L1-12 and L1-13 are the fastest-moving areas, but they depend on L1-10 (attack chain) and L1-11 (cloud) for the operational context that gives AI techniques their meaning. Read them together.

**The most underinvested topics for professionals with a technical background:** L1-05 (PKI — the operational failure modes are almost universally underestimated), L1-15 (governance — the skill that determines whether technical work has organisational consequence), and the quantum/PQC thread in L1-15 (decisions being made today in system design will outlive current cryptographic assumptions).

**The capstone's implicit claim:** You can only think at the level of a defender-who-has-done-the-attack when you can hold the adversarial mindset (L1-01), the cryptographic substrate (L1-02 through L1-05), the applied attack surfaces (L1-06 through L1-10), and the governance context (L1-15) simultaneously — and translate findings across all three into language a board can act on.