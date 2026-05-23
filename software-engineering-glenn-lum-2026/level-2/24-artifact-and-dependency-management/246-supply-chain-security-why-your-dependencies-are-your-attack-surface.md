## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers, when they hear "supply chain security," think about running a vulnerability scanner in CI. That is the equivalent of checking whether your front door lock has a known defect while leaving every window open. Vulnerability scanning catches *known* problems in *known* dependencies. The supply chain attacks that made headlines — SolarWinds, event-stream, ua-parser-js, Codecov — were not known vulnerabilities at the time of exploitation. They were trusted code that became malicious, or trusted infrastructure that was silently compromised. The scanner had nothing to match against because no advisory existed yet.

The Level 1 post covered *what* these mitigations are: vulnerability scanning, integrity verification, artifact provenance. This post is about *how* each of those mechanisms actually works, what they can and cannot prove, and where the gaps between them create real exposure.

## How Your Dependency Graph Becomes a Trust Graph

When your application declares a dependency, your package manager resolves that dependency, then resolves *its* dependencies, recursively, until the entire tree is complete. A moderately complex Node.js application routinely pulls in 800 to 1,500 transitive packages. A Java application using Spring Boot can easily exceed 200 transitive JARs. You probably reviewed the five or ten libraries you chose directly. You almost certainly did not review the hundreds of packages those libraries pulled in.

Each node in that dependency tree represents a piece of code that will execute with the full privileges of your application. If your web server depends on a logging library that depends on a string formatting utility maintained by a single developer with a Gmail account and no two-factor authentication enabled — that developer's account security is now part of your application's security posture. The dependency graph is a trust graph, and you are trusting every node in it.

### The Ways That Trust Gets Exploited

Supply chain attacks are not a single technique. They are a category, and the attack vectors are mechanically distinct.

**Typosquatting** exploits the moment a developer types a package name. An attacker publishes `lodsah` or `reqeusts` to a public registry, containing malicious code. If a developer miskeys the name in their manifest file or install command, the malicious package installs and runs. Registries have started adding detection for this, but coverage is inconsistent and reactive.

**Dependency confusion** exploits how package managers resolve names when both a private registry and a public registry are configured. If your company has an internal package called `auth-utils` and an attacker publishes `auth-utils` on the public npm or PyPI registry with a higher version number, many package manager configurations will prefer the public, higher-versioned package. The attacker's code now runs in your build. This is not a misconfiguration — it is the *default behavior* of several package managers when scoping and priority rules are not explicitly set.

**Maintainer takeover** is the attack class that caused the event-stream incident. A legitimate, widely-used package is maintained by someone who has lost interest. An attacker offers to take over maintenance, is given publish rights, and pushes a new version containing malicious code. Every downstream consumer who runs `npm update` or whose version range accepts the new release inherits the payload. The package remains legitimate in every metadata sense — same name, same registry, valid signature if the new maintainer signs it.

**Build infrastructure compromise** is what happened with SolarWinds and Codecov. The source code of the target project is never modified. Instead, the attacker compromises the build system or CI pipeline so that the artifact produced differs from what the source code specifies. The resulting binary or container image contains malicious code, but anyone reviewing the source repository sees nothing wrong. This is the hardest class to detect because it breaks the assumption that the artifact is a faithful representation of the source.

## What Software Composition Analysis Tools Actually Do

An **SCA tool** performs a specific sequence of operations, and understanding that sequence reveals both its power and its limits.

First, the tool constructs your dependency graph. It does this by parsing your manifest files (`package.json`, `pom.xml`, `go.mod`, `requirements.txt`) and, critically, your lock files. The lock file is where the exact resolved versions live. Without a lock file, the tool either performs its own resolution (which may not match your build) or works only with declared ranges, which is significantly less precise.

Second, the tool identifies each component using a standard naming scheme. The two dominant ones are **CPE** (Common Platform Enumeration), used by the National Vulnerability Database, and **PURL** (Package URL), which is more granular and maps cleanly to package manager ecosystems. A PURL looks like `pkg:npm/lodash@4.17.20` — it encodes the ecosystem, package name, and exact version in a single identifier. The quality of this identification step matters enormously. If the tool misidentifies a component or fails to map it to the correct CPE, the vulnerability lookup produces false negatives.

Third, the tool queries one or more vulnerability databases. The NIST National Vulnerability Database (NVD) is the canonical source, but its coverage lags — sometimes by days, sometimes by weeks after a vulnerability is disclosed. The GitHub Advisory Database (GHSA) and the OSV (Open Source Vulnerabilities) database often have faster coverage for ecosystem-specific issues. A good SCA tool queries multiple databases and cross-references results.

What comes back is a list of known CVEs mapped to specific package versions. This is where most teams stop, and where the meaningful limitations begin.

### The Reachability Problem

A CVE in a dependency means a vulnerability exists in that package's code. It does not mean your application is exploitable. If the vulnerable function is in a code path your application never invokes — because you use a different subset of the library's API — the vulnerability exists in your dependency tree but is not reachable from your application. Advanced SCA tools attempt **reachability analysis**: they trace call graphs from your application code into the dependency to determine whether the vulnerable code path is actually exercised. This is computationally expensive, language-dependent, and imperfect (dynamic dispatch, reflection, and runtime code generation all confound static analysis). But even imperfect reachability analysis dramatically reduces false positives. Without it, teams drown in alerts for vulnerabilities that do not affect them, which leads to alert fatigue, which leads to real vulnerabilities being ignored.

### The Temporal Gap

SCA tools match against *known* vulnerabilities. Between the moment an attacker introduces malicious code and the moment that code is identified and cataloged as a CVE, the SCA tool reports nothing. For the event-stream attack, the malicious code was present for over two months before discovery. For less prominent packages, it can be much longer. SCA is a retrospective control. It catches yesterday's compromises, not today's.

## What SBOMs Contain and What They Enable

A **Software Bill of Materials** is a structured inventory of every component in an artifact. The two dominant formats are **SPDX** (maintained by the Linux Foundation) and **CycloneDX** (maintained by OWASP). Both are machine-readable (JSON, XML, or tag-value). They record package names, versions, supplier information, license data, and relationships between components (this package depends on that package).

SBOMs can be generated in several ways, and the method determines accuracy. **Build-time generation** instruments the build process itself and captures exactly what the build tool resolved. This is the most accurate method. **Manifest parsing** reads lock files and dependency declarations after the fact — accurate for declared dependencies but may miss vendored code, copy-pasted files, or statically linked C libraries that do not appear in a manifest. **Binary analysis** examines a compiled artifact and attempts to identify embedded components by matching code patterns or metadata — useful for compiled languages but inherently less precise.

The value of an SBOM is not in its generation. It is in what happens downstream. With a machine-readable inventory of every component in every deployed artifact, you can answer questions that are otherwise nearly impossible at scale: "Are we running any version of `log4j` anywhere?" becomes a database query instead of a multi-day firefight. When a new critical CVE drops, you can correlate it against every SBOM in your fleet and know within minutes which services are affected. This was the operational crisis that Log4Shell exposed — most organizations had no fast way to answer that question.

SBOMs also enable **policy enforcement at ingestion boundaries**. An artifact registry can reject any artifact whose SBOM contains a component with a critical unpatched CVE, a component with a disallowed license, or a component without a minimum provenance attestation. This shifts enforcement from "someone should check this" to "the system will not permit this."

## What Signing and Provenance Actually Prove

Code signing uses asymmetric cryptography to bind an identity to an artifact. When a maintainer signs a package, they produce a signature that proves two things: the artifact was signed by the holder of that private key, and the artifact has not been modified since signing. This is **integrity** and **attribution**, not safety. A maintainer who has been socially engineered, or whose account has been taken over, will produce validly signed malicious artifacts.

**Sigstore**, the signing framework that has become the emerging standard for open-source ecosystems, addresses one of the historical barriers to signing: key management. Traditional signing requires developers to generate, store, and rotate long-lived private keys, which most do not do. Sigstore's **keyless signing** model uses short-lived certificates tied to an identity provider (like GitHub OIDC). The developer authenticates through their existing identity, receives a temporary certificate, signs the artifact, and the signing event is recorded in a tamper-evident transparency log called **Rekor**. There is no long-lived key to steal. Verification checks the transparency log to confirm the signature was valid at the time of signing.

**Provenance attestations** go further than signing. A provenance record answers: where was this artifact built, from what source, by what build system, with what parameters? The **SLSA framework** (Supply-chain Levels for Software Artifacts) defines increasing levels of build integrity. At SLSA Level 1, the build process documents provenance. At Level 2, provenance is generated by a hosted build service (not the developer's laptop). At Level 3, the build service is hardened and the provenance is non-falsifiable — the builder itself signs the attestation, and the builder's identity is independently verifiable. What this means concretely: at SLSA Level 3, even if an attacker compromises a maintainer's GitHub account, they cannot produce an artifact with valid provenance unless they also compromise the build service itself. The SolarWinds-class attack — compromising the build system — is precisely what SLSA Level 3 and above are designed to make detectable.

Provenance does not prove the source code is benign. It proves the artifact was built from *this specific source* by *this specific builder*. If the source itself is malicious (as in the event-stream attack), the provenance will be valid and the artifact will still be malicious. This is a feature, not a bug — it means provenance is the right tool for detecting build tampering, but you need other controls (code review, maintainer vetting, behavioral analysis) for detecting malicious source.

## Where This Breaks in Practice

**Alert fatigue is the dominant failure mode of SCA adoption.** A mature application with hundreds of transitive dependencies will produce dozens to hundreds of CVE findings on first scan. Many are in transitive dependencies the team did not choose and cannot easily replace. Many are not reachable. Without triage tooling, severity context, and reachability data, teams either ignore the results entirely or spend engineering cycles on changes that do not actually reduce risk.

**SBOMs that are generated but never consumed provide zero security value.** The executive mandate to "produce SBOMs" has outpaced the tooling and processes to use them. If no system is querying your SBOMs when new CVEs are published, if no policy engine is evaluating them at deployment gates, they are compliance artifacts, not security controls.

**Dependency pinning without update discipline creates a different risk.** Pinning every dependency to an exact version prevents surprise changes but also prevents automatic security patches. If your lock file is committed and never updated, you are frozen on a dependency tree that accumulates known vulnerabilities over time. The tradeoff is explicit: pinning gives you reproducibility and control, but it makes you responsible for actively monitoring and applying updates. Tools like Dependabot and Renovate automate the update proposal, but someone still has to review and merge.

**Signing without verification is security theater.** Many package registries now support signatures. Very few consumers verify them. If your `pip install` or `docker pull` does not check signatures against a trust policy, the presence of signatures in the ecosystem provides you no protection. Verification must be configured, enforced, and maintained — including decisions about which signing identities you trust, which is a policy problem more than a technical one.

## The Model to Carry Forward

Your dependency graph is an implicit trust delegation. Every edge in that graph is a decision — mostly made by someone else — to execute code from a source you have not audited, maintained by people you have not vetted, built by systems you do not control. SCA, SBOMs, and signing are three tools that answer three different questions. SCA asks: "Is any component in this graph known to be vulnerable?" SBOMs ask: "What exactly is in this artifact, and can I query that inventory at scale?" Signing and provenance ask: "Can I verify who built this artifact, from what source, and that it has not been tampered with?"

None of them answer the question "Is this code safe?" That question has no single tooling solution. What these mechanisms provide, together, is *evidence layering* — each one closes a category of attack that the others leave open. A mature supply chain security posture is not about choosing between them. It is about understanding which threat each one addresses, deploying them in the right order, and building the operational processes to act on what they tell you.

## Key Takeaways

- Your application's dependency graph is a trust graph — every transitive dependency is code that runs with your application's full privileges, maintained by people and systems outside your control.

- Supply chain attacks are not a single technique; typosquatting, dependency confusion, maintainer takeover, and build infrastructure compromise are mechanically distinct vectors that require different mitigations.

- SCA tools match your resolved dependency versions against vulnerability databases, but they only catch *known* vulnerabilities — the window between compromise and discovery is the attacker's advantage.

- Reachability analysis — determining whether your application actually invokes the vulnerable code path — is the difference between actionable SCA results and alert noise that gets ignored.

- SBOMs are only a security control if something downstream consumes them; an SBOM that is generated for compliance but never queried during incident response or policy enforcement provides no protection.

- Code signing proves integrity and attribution, not safety — a compromised maintainer will produce validly signed malicious artifacts, which is why provenance attestations (who built it, from what source, on what infrastructure) add a necessary additional layer.

- Dependency pinning trades the risk of unexpected changes for the risk of stale dependencies accumulating unpatched vulnerabilities; pinning without an active update process is not a security posture, it is a deferred liability.

- SCA, SBOMs, and signing each close a different category of supply chain risk — no single tool covers the full attack surface, and mature supply chain security requires all three working together with operational processes behind them.

# Discussion

## Why This Conversation Is Happening

Modern software is mostly assembled, not written from scratch. A team may choose a handful of direct dependencies, but the build pulls in hundreds more transitively, and every one of those packages can execute in the context of the application. That means your system's security is partly determined by maintainers, registries, CI systems, and release processes you do not control. If you treat "dependency management" as just a package-install convenience problem, you miss the fact that it is also a trust delegation problem.

What breaks in practice is not only "we shipped a vulnerable library." More often, teams get blindsided by cases their existing controls were never designed to catch: a malicious package with no CVE yet, a public package overriding a private one during resolution, a signed artifact built from a compromised pipeline, or a flood of scanner findings so noisy that engineers start ignoring them. The result is either silent compromise or defensive paralysis: you are either exposed without knowing it, or buried in signals you cannot act on.

The point of understanding this topic is not to memorize acronyms like SCA, SBOM, Sigstore, or SLSA. It is to know what each mechanism actually proves, what it does not prove, and which class of failure appears when you rely on one tool to do another tool's job.

---

## What You Need To Know First

**1. Dependency resolution**  
When you add a package, your package manager does not stop there. It also fetches that package's dependencies, then their dependencies, until it has a full tree. The important part is that your application ends up running code you never explicitly selected. That is why a "dependency graph" becomes a security topic: the graph determines what code lands in your build.

**2. Lock files vs version ranges**  
A manifest often says something like "accept any 1.x version," but the lock file records the exact version that was actually resolved at build time. This matters because security tooling needs to know what you really built with, not the broad range you said you were willing to accept. Without a lock file, different machines can resolve different versions, and your scanner may inspect something different from what production runs.

**3. Known vulnerability databases**  
Databases like NVD, GHSA, and OSV record publicly identified vulnerabilities and the package versions they affect. A scanner compares your dependencies against those records. The key limitation: if a compromise has not yet been discovered and published, there is nothing for the scanner to match. That is why scanners are useful but inherently backward-looking.

**4. Digital signatures in plain terms**  
A signature lets a producer prove "this artifact came from whoever controls this signing identity, and it has not changed since they signed it." That tells you about integrity and origin, not whether the code is good. A malicious or compromised maintainer can still sign bad code, and the signature will verify correctly.

---

## The Key Ideas, Connected

**1. Your dependency graph is really a trust graph.**  
The article's starting point is that dependencies are not just reusable code units; they are trust relationships. If a package is present in your resolved tree, its code can run inside your application or build process. That means you are indirectly trusting the package maintainer, the account security around publication, the registry serving it, and the build path that produced it.  
This matters because once you see dependencies as trust delegation, the next question becomes: how exactly does that trust get abused?

**2. Supply chain attacks are a category of trust abuse, not one single attack pattern.**  
Typosquatting, dependency confusion, maintainer takeover, and build-system compromise all attack different points in the chain. Typosquatting exploits human input. Dependency confusion exploits name resolution rules. Maintainer takeover exploits project governance and publish rights. Build compromise exploits the gap between source and artifact.  
This distinction matters because different attacks violate trust in different ways. Once you know the attack points are mechanically different, you can see why a single defensive tool cannot cover them all.

**3. SCA tools answer a narrow question: "Do any of my known components match known vulnerabilities?"**  
An SCA tool first identifies what components are in your build, usually from manifests and lock files. Then it normalizes those components into identifiers like PURLs or CPEs. Then it checks vulnerability databases for published advisories affecting those versions.  
That sequence explains both why SCA is valuable and why it misses things. It is good at matching known-bad versions, but it depends completely on correct component identification and on a vulnerability already existing in a database. Once you understand that, the next limitation becomes obvious: even a correct match may still not mean your app is actually exploitable.

**4. A vulnerable dependency is not the same thing as a reachable exploit path.**  
If a package contains vulnerable code but your application never calls that part of the package, the code is present but not reachable from your usage. Reachability analysis tries to answer this by tracing whether your application can flow into the vulnerable function or code path.  
This matters operationally because without reachability, SCA produces many findings that are technically true but practically irrelevant. Too many such findings create alert fatigue. And once teams are fatigued, the scanner stops functioning as a real control because engineers learn to dismiss its output.

**5. Even perfect SCA has a time blind spot: it only sees yesterday's known problems.**  
A scanner cannot flag malicious code that has not yet been recognized as malicious and recorded somewhere. In a maintainer takeover or newly introduced backdoor, the package may look normal to the scanner for days or months.  
This is the key reason SCA is only one layer. Once you understand that vulnerability matching cannot tell you everything, you need another mechanism that answers a different question: not "is this known vulnerable?" but "what exactly is inside this artifact?"

**6. An SBOM is an inventory, not a verdict.**  
An SBOM records the components present in an artifact: package names, versions, relationships, suppliers, and similar metadata. Its purpose is not to declare an artifact safe. Its purpose is to make the artifact inspectable and queryable later.  
That distinction is crucial. The value of an SBOM shows up downstream: when a new CVE appears, you can search your fleet and identify affected artifacts quickly. So the next idea follows naturally: the usefulness of an SBOM depends less on generating it and more on whether some system actually consumes it.

**7. SBOMs only matter when connected to decisions or incident response.**  
If you produce SBOMs and store them somewhere no process reads, they are documentation, not defense. They become security controls only when they drive actions: rejecting an artifact, flagging affected services during a new CVE, enforcing policy on licenses or provenance, or answering "where are we running this component?" quickly.  
Once you see SBOMs as inventory that supports policy and response, you can ask another missing question: even if I know what is in the artifact, how do I know the artifact I received is genuinely what the producer intended to release?

**8. Signing proves integrity and attribution, not safety.**  
A valid signature tells you the artifact has not been altered since signing and that it is associated with a signing identity. That protects against tampering in transit or substitution by an unrelated actor. But it does not tell you that the code is non-malicious. If a trusted maintainer signs a bad release, the signature still verifies.  
This is why signing is necessary but insufficient. It secures the chain between signer and consumer, but not the quality or intent of what was signed. That naturally leads to provenance, which asks a more detailed question than simple origin.

**9. Provenance asks how the artifact was produced, not just who signed it.**  
A provenance attestation ties an artifact to a specific source, builder, and build context. Instead of merely saying "Alice signed this tarball," provenance says "this artifact was built from commit X, by builder Y, under process Z." Frameworks like SLSA increase confidence by moving build generation away from a developer laptop and into hardened, attestable build systems.  
This matters because build compromise attacks work by changing the artifact without changing the visible source. Provenance is designed to detect exactly that kind of break in faithfulness between source and artifact. But it still does not prove the source itself is benign.

**10. No single mechanism answers "is this code safe?" because each one closes a different gap.**  
SCA covers known vulnerabilities. SBOMs make contents queryable. Signing proves integrity and identity. Provenance proves build lineage. None of them can independently guarantee safety because the attack surface spans different trust boundaries: package names, version resolution, maintainer control, build systems, and source intent.  
That is the article's real model: supply chain security is evidence layering. You do not pick one "best" control. You combine controls so that one tool's blind spot is covered by another tool's evidence.

---

## Handles and Anchors

**1. "Dependencies are outsourced code execution."**  
If you remember one sentence, use this one. Adding a dependency is not just importing functionality; it is authorizing outside code to run in your environment. That framing makes the security stakes intuitive.

**2. A simple question map:**  
- SCA: "Is anything here known-bad?"  
- SBOM: "What exactly is here?"  
- Signing/provenance: "Where did this come from, and how was it built?"  
If you can ask these three questions separately, you are much less likely to expect one tool to answer all of them.

**3. Think of it like airport security with different checkpoints.**  
An ID check proves who you are. A baggage scan shows what you are carrying. A sealed chain-of-custody tag shows whether the bag was tampered with. None of those proves the traveler is harmless by itself. Software supply chain controls work the same way: each check establishes a different kind of evidence.

---

## What This Changes When You Build

**1. An engineer who understands this will treat lock files as security-critical build inputs, not disposable generated files, because the lock file defines the exact dependency set being trusted.**  
The unaware default is to let dependency resolution vary across machines or environments, then scan against approximate versions. The consequence is drift: the thing you scanned may not be the thing you deployed.

**2. An engineer who understands this will evaluate scanner output through reachability, exploitability, and ownership context, because raw CVE counts are a poor guide to actual risk.**  
The unaware default is either "fix everything immediately" or "ignore the scanner because it always screams." Both fail. The first burns time on low-value work; the second normalizes ignoring real exposures.

**3. An engineer who understands this will set explicit package source and namespace rules, especially for private packages, because dependency confusion is often enabled by default resolution behavior rather than an obvious mistake.**  
The unaware default is to assume the package manager will "do the sensible thing." The consequence is that public packages can win resolution unexpectedly and execute attacker-controlled code in your build.

**4. An engineer who understands this will build a process around SBOM consumption, not just SBOM generation, because inventory only changes outcomes when it is queried at the moment a new issue appears or enforced at a deployment boundary.**  
The unaware default is to produce SBOMs for compliance and store them as artifacts no one uses. The consequence is that when the next Log4Shell-style event happens, the team still cannot answer "where are we affected?" quickly.

**5. An engineer who understands this will enforce signature and provenance verification in artifact intake paths, because unsigned-or-unverified artifacts erase the value of producers doing the right thing upstream.**  
The unaware default is to say "the ecosystem supports signing now, so we are covered." The consequence is security theater: protections exist in theory, but no policy actually blocks an untrusted or unverifiable artifact from entering the build or runtime path.
