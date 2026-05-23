## Metadata
- **Date:** 18-05-2026
- **Source:** 04_entity_authentication.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Entity Authentication

Authentication is the part of security that everyone thinks they understand and almost no one models correctly. Most people picture it as a gate: you type a password, the gate opens, you're in. That picture is wrong in a way that quietly produces most of the credential breaches you read about. Authentication is not a moment. It is a lifecycle, and the gate itself is only the last stage of it. Attackers know this. They attack the stages you weren't watching.

Start with what authentication is actually trying to do. When you log into a server, the server needs to confirm you are a live, present party on the other end of this connection — not a recording, not a replayed packet, not someone who happened to find a token lying around. This is entity authentication, and it is distinct from data-origin authentication, which asks a different question: did this static artefact (an email, a signed document) come from who it claims? The two problems share machinery but solve different things. Entity authentication is about a live connection. Get that distinction wrong and you'll reach for the wrong tool.

The mental model worth carrying is that every credential has three stages, and each stage has its own attack surface. The first is bootstrapping — the moment a credential is created or a device is provisioned. This is the most underestimated stage in the entire system. It is the window where a default password sits on a router waiting to be changed, or where a setup PIN travels over an unencrypted channel, or where a factory-default IoT camera sits exposed on the public internet. The Mirai botnet did not crack anything; it logged in. It walked through the front doors of hundreds of thousands of devices using credentials the manufacturers had printed on a sticker. Bootstrapping is where trust is born, and if you don't close that window deliberately, an attacker walks through it before the legitimate user even arrives.

The second stage is storage. Once a credential exists, the system has to remember enough to verify it later, and how it remembers matters enormously. Storing passwords in cleartext is the obvious sin, but storing them as plain hashes is also broken — identical passwords produce identical hashes, which means an attacker with a stolen database can use precomputed tables to reverse common ones in bulk, and can spot which users share passwords. Salting fixes this: you mix a unique random value into each password before hashing, so two users with the password "summer2024" end up with completely different stored values, and no precomputed table helps. The 2012 LinkedIn breach is the canonical lesson here — unsalted hashes turned a database leak into a password leak. Storage is invisible to users, which is exactly why it tends to be wrong.

The third stage is presentation — the actual moment of logging in, which is what people usually mean when they say "authentication." This is where the human enters the system, and humans are exploitable in ways that cryptography cannot fix. Phishing impersonates the gate. Shoulder surfing watches the keystrokes. Skimmers overlay card readers. Keyloggers ride along on compromised hardware. Sniffers grab cleartext off the wire. The attacker does not need to break the password; they need to be there when you use it. And once you accept that the presentation stage will leak, the only durable defence is to require more than one kind of proof.

This is what multi-factor authentication actually is, and the subtlety is in the word "factor." A factor is a category of evidence: something you know (a password), something you have (a phone, a hardware token), something you are (a fingerprint, an iris), somewhere you are (GPS, network location), something you do (typing rhythm, behavioural patterns). Two passwords are not two factors — they are one factor used twice, and they fail to the same attack. Real MFA combines categories, so that compromising one does not compromise the other. A phished password plus a hardware token still leaves the attacker outside, because they would need to physically steal the token too. This is also why SMS-based one-time codes have been quietly deprecated by NIST: SIM swapping and SMS-intercepting malware turned "something you have" into "something the attacker also has," which collapses the second factor back into the first.

Each factor has its own failure mode worth respecting. Knowledge factors are phishable. Possession factors are stealable and clonable. Inherence factors — biometrics — are the most seductive and the most dangerous, because they are irrevocable. If your password leaks, you change it. If your fingerprint template leaks, you have nine more, and then you are out. Biometrics are excellent for convenience and reasonable for low-stakes presence checks, but treating them as a permanent root of identity is a bet that the storage of biometric templates will never be breached, which is a bet history suggests you will lose.

The deeper shift behind all of this is that the network perimeter is gone. When everyone worked inside an office on a corporate LAN, the network itself acted as a coarse authentication layer — being on the wire meant you belonged. Remote work, cloud services, and personal devices dissolved that assumption. The user's identity is now the perimeter, which means the integrity of authentication is no longer one control among many; it is the control. Regulators have noticed: the Monetary Authority of Singapore mandates 2FA for banking, and similar requirements are becoming standard across regulated sectors. Strong authentication is not a hardening step anymore. It is the baseline.

What you should walk away with is a habit of looking at any authentication system and asking three questions. How are credentials born, and is the bootstrapping window closed? How are they stored, and would a database leak hand the attacker the keys directly? How are they presented, and does compromising one factor compromise the whole? If you can answer those three cleanly, you understand authentication better than most of the systems you will encounter.

## Level 2 candidates

**Password storage: salting, hashing, and modern KDFs** — Covers why plain hashes fail, how salting defeats rainbow tables, and how modern key-derivation functions (bcrypt, scrypt, Argon2) add deliberate slowness to defeat offline cracking. Worth a deep dive because the implementation details determine whether a database breach becomes a password breach, and the choices are not obvious to non-specialists.

**Multi-factor authentication design** — Goes beyond "use MFA" into how factors actually combine, why some combinations are illusory (password + security question), why SMS is deprecated, and how hardware tokens like FIDO2/WebAuthn change the threat model. Worth deeper treatment because most MFA failures are not absence of MFA but bad MFA design.

**Bootstrapping and credential provisioning** — Covers the lifecycle vulnerability around credential creation: default passwords, initial-setup channels, factory provisioning of IoT devices, and credential-recovery flows. Worth its own treatment because it is the most overlooked stage and the source of some of the largest attacks (Mirai, IoT botnets) in recent history.

**Biometric authentication and its limits** — Covers how biometric templates are extracted, stored, and matched; the difference between local (Secure Enclave) and server-side biometric storage; and the irrevocability problem. Worth depth because biometrics are increasingly the default on consumer devices and the trade-offs are widely misunderstood.

**Social engineering and the human attack surface** — Covers phishing, pretexting, shoulder surfing, and the design of security questions and recovery flows that resist public-data research. Worth depth because technical authentication controls can be cleanly bypassed by attacks on the human, and the defences are organisational and behavioural rather than cryptographic.

**Physical and side-channel attacks on authentication** — Covers ATM skimming, magnetic stripe cloning, keyloggers, KeySweeper-style hardware sniffers, and the broader cyber-physical gap. Worth a deeper look because it grounds the abstract idea of "presentation-stage attacks" in concrete hardware reality and matters increasingly as IoT and physical access systems proliferate.

---

# Discussion

## Why This Conversation Is Happening

Authentication systems usually fail long before the login form appears. Engineers often think of authentication as a single check at the edge of a system — compare password, issue session, move on. But the real problem is broader: credentials have to be created, stored, and used, and each of those stages gives attackers a different place to win. If you only defend the final login step, you can still lose the system through default credentials, a leaked hash database, or a phished user.

That matters because modern systems increasingly treat identity as the main control plane. The old comfort of “inside the network equals trusted” has eroded with cloud services, remote access, SaaS, mobile devices, and APIs. In practice, if authentication is weak, everything built on top of it — authorization, audit, compliance, customer trust — becomes fragile. So the engineering problem is not “how do we check a password,” but “how do we preserve trust across the full credential lifecycle?”

## What You Need To Know First

**1. Threat model**  
A threat model is just a clear statement of who might attack the system, what they can realistically do, and where they are likely to attack. For authentication, this matters because the defence against a database thief is different from the defence against a phishing attacker or someone with physical access to a device. If you do not name the attacker, you will accidentally design for the wrong failure mode.

**2. Hashing**  
A hash function takes input data and turns it into a fixed-size output that is easy to compute but hard to reverse directly. For passwords, the idea is that the server should store a derived value, not the password itself. That only helps if the hashing approach is designed for passwords; otherwise an attacker who steals the database can still guess likely passwords offline at high speed.

**3. Replay vs live presence**  
A replay attack happens when an attacker reuses a captured credential or message instead of knowing the secret themselves. So one core job of entity authentication is not merely checking “does this look valid,” but checking “is there a live, legitimate party on the other side right now?” This is what separates authenticating an active session from verifying a static signed file.

**4. Authentication factor**  
A factor is a category of proof, not just an extra prompt. “Something you know” and “something you have” are different factors; two passwords are not. This prerequisite matters because a lot of systems look stronger by adding steps, while still depending on the same underlying weakness.

## The Key Ideas, Connected

**Authentication is not a moment; it is a lifecycle.**  
The article is trying to replace the “login gate” mental model with a broader one. Authentication does include the moment a user signs in, but the trust involved in that moment depends on earlier choices: how the credential came into existence and how it has been protected since. Once you accept that, you stop asking only “is the login flow secure?” and start asking where trust first appears and where it can leak before login ever happens. That leads directly to the distinction between different kinds of authentication problems.

**Entity authentication is about a live party, not just a valid-looking artefact.**  
The system is not only asking “does this credential match?” It is asking “am I dealing with the real participant in this interaction right now?” That is different from data-origin authentication, where you verify that a document, signature, or message came from some claimed source. The distinction matters because tools that prove authorship of a static artefact do not automatically prove live presence in an ongoing exchange. Once you see authentication as a live-session problem, you can see why attackers target the full credential lifecycle instead of only cryptographic validity.

**The credential lifecycle has three stages: bootstrapping, storage, and presentation.**  
This is the article’s main organizing idea. A credential is born somehow, remembered somehow, and later presented somehow. Each stage is a separate attack surface. That framing is powerful because it gives you a repeatable way to inspect real systems: how was the credential created, what is retained, and what happens when the user actually uses it? The first stage in that chain is bootstrapping, and the article argues it is the most neglected.

**Bootstrapping is where trust is created, so failure here poisons everything after it.**  
If a device ships with a known default password, or onboarding happens over an insecure channel, then the attacker may gain access before the legitimate user has even established control. Nothing about later login checks can repair that original mistake, because the system’s root trust was already claimed by the wrong party. This is why incidents like large IoT compromises often involve “logging in” rather than “breaking crypto.” Once a credential exists, though, a new problem appears: the system has to remember enough to verify it later.

**Storage determines whether a database leak becomes a credential leak.**  
The server cannot usually keep secrets in plain form without creating catastrophic risk, so it stores a derived representation. But the article pushes one level deeper: even “hashed” is not automatically safe. If two identical passwords produce identical stored outputs, attackers gain leverage at scale — they can use precomputed tables and identify password reuse patterns. Salting works by making each stored password-derived value unique even when users choose the same password. That means storage is not just a hygiene detail; it changes the economics of offline attack. Still, even perfectly stored passwords have to be used somewhere, which opens the next stage.

**Presentation is where human use becomes an attack surface.**  
When a person types a password, taps approval on a phone, inserts a card, or scans a fingerprint, that interaction can be observed, intercepted, or imitated. Phishing pages can mimic the real login page. Keyloggers can capture secrets at entry. Sniffers can catch secrets sent improperly over the network. So the article’s point is not that presentation is flawed because users are careless; it is that use itself creates exposure. If one exposed act of use is enough to compromise the whole account, then the system is brittle. That is what motivates multi-factor authentication.

**Multi-factor authentication only helps when the proofs come from different categories of evidence.**  
The important word is “factor,” not “multiple.” Asking for two passwords or a password plus a security question may feel layered, but both are still “something you know,” so one style of attack can often defeat both. Real MFA tries to make the attacker solve different problems: maybe phish a password and physically possess a token, or know a secret and also pass a biometric check. This shifts authentication from “one secret must remain hidden forever” to “the attacker must compromise independent kinds of evidence at the same time.” But that only works if you respect the weaknesses of each factor.

**Every factor fails differently, so MFA design is about combining failure modes, not collecting gadgets.**  
Passwords are guessable and phishable. Tokens can be stolen, cloned, or socially bypassed in recovery flows. Biometrics are convenient but cannot be rotated like passwords if their templates leak. SMS looks like possession, but in practice it can be undermined by SIM swaps or malware, so it may not provide the independence you hoped for. This is the deeper engineering lesson: authentication strength comes from how the factors fail in combination, not from how impressive each factor sounds in isolation. Once identity becomes the main perimeter, these design choices stop being optional hardening.

**In modern systems, identity is the perimeter.**  
When users, services, and devices operate across cloud networks, home networks, mobile environments, and third-party platforms, “being on the trusted network” no longer proves much. So authentication is no longer one control among many surrounding a strong perimeter; it is itself the central boundary. That is why the article ends with three diagnostic questions — how credentials are born, stored, and presented. Those questions are practical because they map directly onto where modern systems actually fail.

## Handles and Anchors

**1. Think of authentication as a supply chain, not a checkpoint.**  
A secure checkpoint at the end does not help if the goods were poisoned at the factory, swapped in the warehouse, or stolen in transit. Bootstrapping, storage, and presentation are those stages. The login prompt is just the final inspection point.

**2. “Multiple steps” is not the same as “multiple factors.”**  
If two proofs can be defeated by the same attack, they are functionally one weakness wearing two labels. Good MFA works when breaking one proof does not give you the other.

**3. The core tension is: authentication must be usable by legitimate humans and hard to reuse by illegitimate ones.**  
That is why presentation-stage attacks are so important. The same moment that lets a real user prove identity is often the moment an attacker tries to capture, relay, or imitate that proof.

## What This Changes When You Build

**An engineer who understands this will approach device onboarding differently because the first claimant to a credential often becomes the trusted one.**  
That changes decisions around factory defaults, enrollment links, setup PIN delivery, first-login enforcement, and whether a device can operate before secure provisioning is complete.

**An engineer who understands this will approach password storage differently because the breach to plan for is database theft, not only online guessing.**  
That leads to design choices like per-user salts, modern password KDFs, and explicit review of what an attacker can do offline with stolen credential material.

**An engineer who understands this will approach login UX differently because the act of entering a secret is itself an attack surface.**  
That affects whether secrets are ever transmitted in reusable form, how phishing-resistant the flow is, whether prompts are bindable to the real origin, and whether recovery paths quietly undercut the main authentication design.

**An engineer who understands this will choose MFA combinations differently because factor independence matters more than factor count.**  
They will ask whether the second factor is truly a different category of evidence, whether it can be socially subverted, and whether compromise of one channel meaningfully helps with the other.

**An engineer who understands this will evaluate biometrics differently because convenience and revocability trade against each other.**  
That changes where biometric templates are stored, whether biometrics are used as a local unlock versus a remote identity root, and how the system recovers when a biometric signal is spoofed or exposed.