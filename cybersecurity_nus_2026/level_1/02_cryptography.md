## Metadata
- **Date:** 18-05-2026
- **Source:** 02_cryptography.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Cryptography

Most people imagine cryptography as a contest of cleverness — a battle between someone designing a fiendishly intricate code and someone trying to crack it. That intuition is almost entirely wrong, and holding onto it will lead you to build systems that fail in predictable ways. Modern cryptography is not about cleverness. It is about economics, transparency, and a ruthless honesty about what you are actually protecting and from whom.

The first thing to internalise is that cryptography exists to serve confidentiality — keeping information readable only to those who should read it — and that it does this through one basic move: a pair of algorithms (encryption and decryption) that use a key to turn plaintext into ciphertext and back. A cryptosystem has to satisfy two requirements that pull against each other. It has to be correct, meaning the legitimate recipient can always recover the original message. And it has to be secure, meaning nobody else can. Correctness is easy. Security is the entire problem.

The history of the field is a long retreat from the dream of perfect secrecy. Classical ciphers like the Caesar shift or general substitution feel secure when you first see them — letters get scrambled, the output looks like noise — but they fail catastrophically against frequency analysis, because they preserve the statistical fingerprint of the underlying language. The letter E shows up about as often in the ciphertext as it did in the plaintext; you just have to figure out which symbol it became. The lesson here is not that those particular ciphers were bad. The lesson is that any cipher which preserves structure in its output is broken, even if you cannot immediately see how. There is exactly one cipher with mathematically perfect secrecy — the one-time pad — and it is operationally useless for almost everything, because it requires a truly random key as long as the message, never reused, somehow shared securely in advance. If you could share a key that long securely, you could just share the message. Perfect security exists. You cannot afford it.

So modern cryptography made a trade. It abandoned perfect secrecy and embraced computational security: the idea that a system is secure if breaking it would take more time, money, and computing power than the data is worth, or than the universe has existed. AES with a 128-bit key is not unbreakable in the mathematical sense the one-time pad is. It is unbreakable in the sense that brute-forcing it would outlast the heat death of the sun. That is a different kind of guarantee, and it is the only kind that scales. Once you accept this, security stops being a binary property and becomes an economic one: you are trying to make the attacker's cost exceed the defender's stake.

This is where Kerckhoffs' Principle enters, and it is the single idea from this module most worth tattooing somewhere visible. Kerckhoffs argued that a cryptosystem should remain secure even if everything about it — the algorithm, the implementation, the protocols — is public knowledge. The only thing that should need to stay secret is the key. This sounds backwards to most people. Surely hiding how the system works adds another layer of protection? In practice, it does the opposite. Secret algorithms are secret precisely because they have not been examined, and unexamined algorithms are full of mistakes their designers never noticed. Public algorithms get scrutinised by thousands of researchers over decades. AES and RSA are trusted not despite being open, but because they are open. Security through obscurity is not a layer of defence; it is a confession that you do not know whether your system is secure and would prefer not to find out.

The threat model matters as much as the algorithm, and this is where most real-world breaks actually happen. A black-box attacker only sees what goes into the system and what comes out — ciphertexts, maybe some chosen plaintexts. A grey-box attacker sees more: how long the encryption took, how much power the chip drew, electromagnetic leakage from the hardware, what happens when you physically tamper with the device. A grey-box attacker does not need to break the math. They go around it. This is why a mathematically flawless algorithm running on a poorly shielded smart card can leak its keys through the power supply, and why "the algorithm is secure" is a far weaker claim than "the implementation is secure."

The practical skill this builds is a way of looking at any system that handles sensitive information. You stop asking "is this encrypted?" and start asking sharper questions. What exactly is the plaintext I am protecting, and what is it worth? Who is the realistic adversary — a curious colleague, a competitor, a state actor — and what are their resources? Does the security rest on the secrecy of the key, or am I quietly relying on nobody figuring out where I hid things? If the algorithm and the source code leaked tomorrow, would I still be safe? And where does the key actually live, because if it lives next to the lock, it is not a lock. Cryptography is not a magic wrapper you spray on data. It is a discipline of identifying what is secret, ensuring only the key carries that secrecy, and accepting that you are buying time at a price the attacker will not pay.

## Level 2 candidates

**Kerckhoffs' Principle and the case against security by obscurity** — A deeper treatment of why open, peer-reviewed algorithms outperform proprietary ones, with the historical evidence and the structural reasons this keeps being true. Worth its own post because the principle is counterintuitive enough that most practitioners nod along and then immediately violate it in their designs.

**Classical ciphers and frequency analysis** — Substitution, shift, and other pre-modern ciphers, and the precise mechanics of how statistical attacks dismantle them. Useful as a Level 2 because working through the actual cryptanalysis is the fastest way to internalise why "preserves structure" equals "broken."

**The one-time pad and the limits of perfect secrecy** — What perfect secrecy actually means information-theoretically, why OTP achieves it, and the operational reasons it cannot be generalised — including the Venona case where reuse of supposedly one-time keys broke Soviet communications. Worth a deep dive because it sharpens the distinction between mathematical and practical security.

**Computational security and key length calibration** — How "hardness assumptions" translate into key length recommendations, why nominal and effective key lengths differ (e.g. RSA-2048 giving roughly 112 bits of effective security), and how to reason about future-proofing against rising compute. Worth going deeper because most key-length decisions in practice are made by copying defaults without understanding the underlying budget.

**Adversary models: black-box, grey-box, and side-channel attacks** — The taxonomy of attacker capabilities, from ciphertext-only through chosen-plaintext to timing, power, and electromagnetic side-channels. Worth a separate post because side-channel attacks are where most real-world cryptographic failures actually occur, and they are almost invisible if you only think about the math.

**The Alice and Bob threat-modelling vocabulary** — The standardised cast (Alice, Bob, Eve, Mallory, and the broader family) and how to use them to make protocol assumptions explicit. Worth its own treatment because the vocabulary is a working tool for designing protocols, not just pedagogical scaffolding.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Cryptography shows up in engineering whenever data has to remain protected while moving through systems you do not fully trust: networks, browsers, phones, cloud services, smart cards, backups, and APIs. The hard part is that many systems look secure from the outside. Data is "encrypted," the output looks scrambled, and a team feels done. But that surface impression is exactly how weak systems survive until someone with patience, money, or better access breaks them.

What forces this topic into engineering reality is that security failures usually do not come from movie-style codebreaking. They come from simpler mistakes: preserving structure that leaks information, relying on hidden design instead of strong keys, or protecting the algorithm while leaving the key or implementation exposed. If you do not have a clear model of what cryptography is buying you, you end up treating it like a magic coating rather than a tool with very specific limits.

This matters because cryptography is one of the few engineering domains where being slightly wrong often means being completely broken. A system can be correct enough to work in testing and still fail as a security system. So the point of this conversation is not to help you admire cryptography. It is to help you think like someone who can use it without lying to themselves about what it does.

## What You Need To Know First

**1. Plaintext, ciphertext, and key**  
Plaintext is the original readable data. Ciphertext is the scrambled output after encryption. The key is the secret input that controls the scrambling and unscrambling. If you remember only one thing, remember this: in modern cryptography, the key is supposed to be the secret, not the whole design.

**2. Algorithm versus implementation**  
An algorithm is the mathematical procedure: for example, how AES transforms data. An implementation is the actual code or hardware that runs it. This distinction matters because an algorithm can be sound while the implementation leaks secrets through bugs, timing differences, power use, or bad key handling.

**3. Information leakage through structure**  
A system leaks structure when patterns in the input still show up in the output in some usable way. You do not need the original message to be visible for this to be dangerous. If repeated inputs, statistical patterns, or predictable relationships survive encryption, an attacker can often use those traces to recover information.

**4. Threat model**  
A threat model is a concrete description of who the attacker is and what they can do. Can they only observe messages on the wire? Can they choose inputs? Can they measure timing or touch the device? Cryptography is never "secure" in the abstract. It is only secure relative to a particular attacker model.

## The Key Ideas, Connected

**Cryptography exists to keep readable information limited to the people who should have it.**  
At the center, cryptography is not a puzzle contest. It is a mechanism for controlling who can recover meaning from data. Encryption transforms readable data into unreadable-looking data, and decryption reverses that transformation for someone who has the right key. That framing matters because it shifts your attention away from "is this clever?" and toward "who can read what, under what conditions?" Once you see that, you can separate the easy part from the hard part.

**Correctness is necessary, but security is the actual problem.**  
A cryptosystem has to let the legitimate recipient recover the message, otherwise it is useless. But making something that decrypts properly for the intended user is not that hard. The real challenge is making sure nobody else can do the same. This matters because many weak systems feel successful in development: messages encrypt, decrypt, and round-trip correctly. But that only proves the system works for friends, not that it resists enemies. That leads directly to why older ciphers failed.

**A cipher that preserves useful structure is broken, even if the output looks scrambled.**  
Classical ciphers taught this the hard way. They often changed symbols but preserved the statistical shape of the underlying language. If common letters stay common, then the ciphertext still carries the fingerprint of the plaintext. An attacker does not need to guess the whole message at once; they can exploit the structure piece by piece. The important lesson is bigger than "Caesar shift is weak." It is that apparent disorder is not enough. If meaningful patterns survive, the cipher is leaking. Once you grasp that, you can understand why perfect secrecy is so rare.

**Perfect secrecy exists, but it is operationally too expensive for general use.**  
The one-time pad is the benchmark case: if used correctly, it gives mathematically perfect secrecy. But the cost is severe. You need a truly random key as long as the message, you must share it securely in advance, and you must never reuse it. That means the thing you need to manage securely is almost as large and awkward as the message itself. So the field learned a hard constraint: perfect secrecy is possible in theory, but not scalable for most real systems. That forces a different kind of bargain.

**Modern cryptography replaces perfect secrecy with computational security.**  
Instead of asking for "impossible to break," modern systems aim for "too expensive to break." A scheme is considered secure if the time, compute, and money required to defeat it are beyond what an attacker can realistically spend. This is the major conceptual shift in the article. Security becomes an economic claim, not an absolute one. You are not proving that attack is impossible; you are pricing attack out of reach. Once security is economic, another question becomes central: what exactly has to stay secret for this pricing model to hold?

**A good cryptosystem depends on secret keys, not secret design.**  
This is Kerckhoffs' Principle. You should assume the attacker knows the algorithm, the protocol, and ideally even the source code. If the system only stays secure while its design remains hidden, then it is fragile by construction. Hidden designs do not get enough scrutiny, and undiscovered flaws are not the same as strength. Open, reviewed systems earn trust because many capable people have tried to break them. Once you accept this principle, you stop treating obscurity as protection and start isolating secrecy to the key itself. But that still does not finish the job, because the key lives inside a real system.

**The attacker model must include the implementation, not just the math.**  
An algorithm can be mathematically sound and still fail in practice if the implementation leaks information. A black-box attacker only sees inputs and outputs. A grey-box attacker may observe timing, power draw, electromagnetic leakage, or effects of physical tampering. In that world, the attacker does not need to defeat the theory of the cipher; they only need to learn enough from the way your system runs it. This is why "we use a strong algorithm" is not the same as "we built a secure system." And that leads to the final engineering habit the article is trying to build.

**Real cryptographic thinking starts with sharper questions, not stronger slogans.**  
Once you internalise the earlier ideas, your behavior changes. You stop asking "is this encrypted?" as if that settles anything. You ask what data is being protected, what adversary is realistic, what value the data has, where the key lives, whether the system still stands if the design becomes public, and whether the implementation leaks around the math. That is the chain the article builds: from basic encryption, to the failure of structure-preserving ciphers, to the impracticality of perfect secrecy, to computational security, to Kerckhoffs' Principle, to threat models and side channels, and finally to a more honest engineering mindset.

## Handles and Anchors

**1. "Cryptography is not a magic shield; it is a cost engine."**  
This is a strong anchor for the move from perfect secrecy to computational security. You are not making attack impossible. You are making it uneconomical. If someone can steal \$10 million by spending \$10,000 to attack you, your cryptography is weak no matter how elegant the math is.

**2. "The key is the secret; everything else should survive daylight."**  
This is the cleanest way to remember Kerckhoffs' Principle. If revealing the algorithm, protocol, or source code would collapse your security story, then the system was never strong. The only secrecy you should be depending on is the key.

**3. Think of implementation leaks like soundproofing around a vault door.**  
You can install a perfect vault door, but if the hinges squeal in a recognizable pattern every time the combination wheel moves, information is escaping around the mechanism. Side-channel attacks work like that. They do not smash the vault; they listen to the building.

## What This Changes When You Build

**An engineer who understands this will approach algorithm selection differently because proven public designs are safer than proprietary ones that nobody has stress-tested.**  
Instead of asking whether an in-house scheme feels unique, they will ask whether it has survived broad public analysis. They will prefer standard, well-reviewed primitives over custom encryption, because novelty increases the chance of hidden structural weaknesses.

**An engineer who understands this will approach key management differently because the security of the system collapses if the key is stored next to the thing it protects.**  
They will spend more design energy on where keys are generated, stored, rotated, and exposed than on cosmetic details of the encryption step itself. They will recognize that poor key custody can nullify a strong algorithm.

**An engineer who understands this will approach requirements gathering differently because "encrypted" is not a sufficient security specification.**  
They will ask what data needs protection, from which attackers, with what expected attacker resources, and at which points in the system lifecycle. That changes architecture discussions: for example, whether encryption at rest is enough, whether data must be protected in transit, or whether endpoint compromise makes the whole question different.

**An engineer who understands this will approach implementation review differently because side-channel and leakage risks are part of the design, not postscript concerns.**  
They will care about timing behavior, hardware exposure, debug interfaces, shared environments, and physical access assumptions. In practice, that means cryptographic review extends beyond API correctness into runtime behavior and deployment conditions.

**An engineer who understands this will approach system trust differently because they know secrecy of design is not a durable control.**  
If a teammate says "it is safe because nobody knows how we encoded it," they will treat that as a warning sign. They will design as though attackers can inspect binaries, reverse engineer clients, read documentation, and observe traffic. That mindset usually leads to more robust systems long before any attack occurs.

</details>
