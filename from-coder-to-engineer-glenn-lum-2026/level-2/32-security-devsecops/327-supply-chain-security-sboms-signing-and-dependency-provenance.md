## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams that adopt SBOMs, artifact signing, and provenance checks treat them as compliance checkboxes — generate a document, slap a signature on an image, reference a SLSA level in a slide deck. The artifacts get produced but never consumed. The signatures exist but nothing verifies them in the critical path. The provenance attestations sit in a registry, unqueried. This is not supply chain security. It is supply chain theater. The gap between having these artifacts and actually using them to make trust decisions is where every real supply chain attack finds its opening. To close that gap, you need to understand what each mechanism actually proves, how it proves it, and where the proof falls apart.

## What an SBOM Actually Contains and How It Gets Built

An SBOM is not a dependency list. Your `package-lock.json` or `go.sum` is a dependency list. An SBOM is a structured, standardized document that describes every component in a built artifact — direct dependencies, transitive dependencies, the compiler or runtime used, embedded libraries, vendored code, even operating system packages in a container image — along with metadata about each component's origin, version, and licensing.

Two formats dominate: **SPDX** (an ISO standard, originating from the Linux Foundation) and **CycloneDX** (from OWASP). They encode similar information differently. SPDX models components and relationships as a graph with explicit relationship types (`DEPENDS_ON`, `BUILD_TOOL_OF`, `CONTAINED_BY`). CycloneDX uses a more hierarchical component inventory model with explicit vulnerability and service extensions. Neither is strictly superior; SPDX has deeper roots in license compliance, CycloneDX in security-oriented tooling. The choice matters less than consistency — pick one and make sure your entire toolchain can produce and consume it.

The critical question is *when* the SBOM is generated, because this determines its accuracy.

**Source-level analysis** inspects manifest files (`pom.xml`, `requirements.txt`, `Cargo.toml`) and produces an SBOM from declared dependencies. This is fast and cheap but misses everything the build process introduces: dependencies resolved at build time, C libraries linked during compilation, packages pulled into a container base image. It also trusts the manifest, which may not reflect what actually gets built.

**Build-time generation** hooks into the actual build process — the resolver, the compiler, the linker — and records what was actually consumed. Tools like Syft operating on a built container image, or build systems that emit provenance during the build, produce SBOMs that reflect the real artifact. This is more accurate but requires integration with your build pipeline and introduces a dependency on the SBOM tooling itself.

**Binary analysis** reverse-engineers components from a compiled artifact by scanning for known library signatures, version strings, and file hashes. This is the most honest — it looks at what you actually ship — but it is the least complete. Statically linked libraries, minified JavaScript, and vendored Go modules can all evade detection.

Each component in the SBOM needs a stable, unambiguous identifier. This is where **Package URL (purl)** comes in — a standardized format like `pkg:npm/%40angular/core@16.2.0` that uniquely identifies a package across ecosystems. Without stable identifiers, correlating SBOM entries against vulnerability databases (which track CVEs by package identifier) becomes string-matching guesswork. The identifier scheme is not a cosmetic detail; it is what makes an SBOM queryable rather than merely readable.

## How Artifact Signing Actually Works

Signing a software artifact is cryptographically straightforward in principle: hash the artifact, encrypt the hash with a private key, distribute the public key so consumers can verify. In practice, the entire difficulty lives in key management and trust establishment.

**Traditional signing** uses long-lived key pairs. You generate a GPG or PGP key, guard the private key, publish the public key, and sign every release. The consumer imports your public key and verifies signatures before using your artifact. This works, but it creates brutal operational problems. The private key becomes a high-value target that must be secured indefinitely. If it is compromised, every artifact ever signed with it becomes suspect. Key rotation requires coordinating with every consumer. Key distribution itself is a trust problem — how does a consumer know the public key they fetched is actually yours?

**Sigstore** was created to solve these problems, and its architecture is worth understanding because it reframes signing around short-lived identity rather than long-lived keys.

Sigstore has three components. **Fulcio** is a certificate authority that issues short-lived signing certificates. Instead of managing your own key pair, you authenticate via an OIDC identity provider (your GitHub identity, your Google Workspace account, a Kubernetes service account). Fulcio verifies your identity, generates an ephemeral key pair, binds the public key to your verified identity in a short-lived certificate (typically valid for 10 minutes), and returns it. You sign your artifact with the ephemeral private key, then the private key is discarded.

**Rekor** is an immutable transparency log. After signing, the signature and the signing certificate are recorded in Rekor. This log is append-only and publicly auditable. It serves the same role as Certificate Transparency logs in the TLS ecosystem: even if a certificate was mis-issued, the public record makes it detectable.

**Cosign** is the client tool that orchestrates this. When you run `cosign sign`, it handles the OIDC flow, gets the Fulcio certificate, signs the artifact, and records the entry in Rekor. When a consumer runs `cosign verify`, it checks the signature against the certificate, checks the certificate against Fulcio's root of trust, and checks that the signing event exists in Rekor's transparency log.

The verification step is doing something subtle: it is not just checking that the artifact was not tampered with. It is checking *who signed it* (the OIDC identity bound to the certificate), *when they signed it* (the Rekor timestamp, which must fall within the certificate's validity window), and *whether that signing event was publicly recorded* (the transparency log entry). This is a fundamentally stronger statement than "someone with access to a particular private key signed this."

For container images specifically, signatures and attestations are stored as OCI artifacts in the same registry as the image itself, referenced by digest. This means your verification policy can be enforced at the admission control layer — a Kubernetes admission controller like Sigstore's Policy Controller or Kyverno can reject any image that lacks a valid signature from an expected identity before it ever runs in your cluster.

## Provenance Attestations and What They Prove

Signing tells you *who* produced an artifact. Provenance tells you *how* it was produced. These are different questions, and conflating them is a common mistake.

A **provenance attestation** is a signed statement describing the build process that created an artifact. The **SLSA framework** (Supply-chain Levels for Software Artifacts) defines increasingly rigorous levels of provenance:

At SLSA Build L1, the provenance simply documents the build process — which build system, which entry point, which inputs. At L2, the provenance is generated by a hosted build service (not the developer's laptop) and the provenance document is authenticated. At L3, the build service is hardened — the build runs in an isolated, ephemeral environment, and the provenance cannot be forged by the build's own tenants.

The concrete output is an **in-toto attestation** — a JSON document following the in-toto attestation framework, signed by the build system, that specifies the artifact's digest, the source repository and commit, the build configuration used, and the builder identity. Here is a simplified provenance predicate:

```json
{
  "buildType": "https://github.com/slsa-framework/slsa-github-generator/generic@v1",
  "builder": {
    "id": "https://github.com/slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@refs/tags/v1.9.0"
  },
  "invocation": {
    "configSource": {
      "uri": "git+https://github.com/my-org/my-repo@refs/tags/v2.1.0",
      "digest": { "sha1": "abc123..." },
      "entryPoint": ".github/workflows/release.yml"
    }
  },
  "materials": [
    {
      "uri": "pkg:npm/lodash@4.17.21",
      "digest": { "sha256": "def456..." }
    }
  ]
}
```

What this proves, when verified, is that a specific build system processed a specific source commit using a specific workflow and produced the artifact you are about to deploy. A policy engine can then enforce rules like: "only deploy artifacts built by our CI system from our main branch, built using our approved workflow file." This is a much stronger guarantee than signature alone, because it closes the gap between "a trusted identity signed this" and "this was built in a process we control."

GitHub Actions, for instance, can generate SLSA L3 provenance using the `slsa-github-generator` reusable workflows. The provenance is generated by an isolated builder workflow that the calling workflow cannot tamper with, and it is signed using Sigstore's keyless signing bound to the workflow's identity.

## Where This Breaks Down

**SBOMs without consumption infrastructure are inert.** The most common failure mode is generating SBOMs because a regulation or customer contract requires it, then storing them in a bucket where nothing reads them. An SBOM only creates value when it is ingested by a system that can correlate its contents against a continuously updated vulnerability database and alert when a newly disclosed CVE matches a component you ship. Without that pipeline — SBOM generation, storage, ingestion, correlation, alerting — the SBOM is a PDF you hand to an auditor.

**Signing without verification policy is security decoration.** If nothing in your deployment path rejects unsigned or incorrectly signed artifacts, signatures are cosmetic. The verification must be enforced — typically at the admission controller in Kubernetes, or at the deployment step in your CD pipeline — and it must be enforced as a hard gate, not a warning. The number of organizations that sign every image and verify none of them is disturbingly high.

**Provenance verification is only as strong as your trust in the build system.** SLSA L3 requires that the build environment is hardened and that the provenance cannot be forged by the build's tenants. But if your build system is self-hosted and an attacker gains access to the build infrastructure itself, they can forge provenance attestations. The trust boundary is the build system. If you do not control that boundary — or if you do but have not hardened it — your provenance guarantees are weaker than they appear.

**Transitive dependency opacity remains largely unsolved.** Your SBOM can enumerate that you depend on `libfoo@1.2.3`, and your signature can prove that `libfoo@1.2.3` was built by its maintainer. But unless `libfoo` itself has an SBOM and provenance attestation for *its* dependencies, you have a one-layer-deep view into a dependency tree that may be thirty layers deep. The chain of trust needs to be recursive, and the ecosystem tooling for recursive SBOM and provenance verification is still immature.

**The operational cost is real.** Maintaining SBOM generation across every build pipeline, keeping signing infrastructure operational, managing verification policies, updating vulnerability correlation databases, and responding to the alerts they generate all require dedicated effort. For small teams, the overhead may exceed the security value until dependency scale makes the risk concrete.

## The Model to Carry Forward

Think of supply chain security as three distinct questions about every artifact you run in production: *what is in it* (SBOM), *who produced it* (signing), and *how was it produced* (provenance). Each question has a different mechanism, a different verification path, and a different failure mode. None of them substitute for the others.

The underlying principle is that trust must be *verifiable and automated*. A human reviewing a dependency list is not supply chain security. A policy engine that rejects an image because its provenance attestation does not match your build policy, before the image ever reaches a node — that is supply chain security. The shift is from trust-by-default to trust-by-evidence, where every artifact must present cryptographically verifiable evidence of its composition, origin, and build process, and that evidence is checked in the critical deployment path with no human in the loop.

## Key Takeaways

- An SBOM is only useful when paired with a consumption pipeline that correlates its contents against vulnerability databases and triggers alerts on match — generating it without ingesting it is compliance theater.
- Build-time SBOM generation is more accurate than source-level analysis because it captures what was actually resolved and linked, not just what was declared in a manifest.
- Sigstore's keyless signing model eliminates long-lived key management by binding ephemeral signing certificates to verified OIDC identities and recording signing events in an immutable transparency log.
- Artifact signing proves who produced an artifact; provenance attestations prove how it was produced — these answer different questions and enforce different policies.
- SLSA provenance levels are only meaningful when the build system itself is a hardened trust boundary; self-hosted CI without isolation gives you provenance documents without provenance guarantees.
- Verification must be enforced as a hard gate in the deployment path (admission controller, CD pipeline step), not as an optional check or logged warning.
- Transitive dependency chains are the weakest link: your supply chain visibility extends only as far as your dependencies themselves publish SBOMs and provenance, which today is rarely more than one level deep.
- Package URL (purl) identifiers are what make SBOMs queryable against vulnerability databases — without stable, cross-ecosystem identifiers, correlation degrades to unreliable string matching.

# Discussion

## Why This Conversation Is Happening

Modern software is assembled from layers you did not write: packages, container base images, compilers, build actions, vendored code, transitive dependencies. That means an attacker does not need to break into your production cluster directly if they can poison something upstream and let your normal build and deploy process carry it the rest of the way. When teams only talk about “supply chain security” in terms of documents and signatures they produced, they often miss the operational question that matters: what in the pipeline actually refuses bad artifacts?

Without a working model here, teams create evidence but not enforcement. They generate SBOMs that nobody queries, sign images that nobody verifies, and attach provenance that no policy engine reads. In that state, a vulnerable library stays unnoticed until exploitation, a malicious image signed from the wrong identity still deploys, or a release built from an untrusted workflow is treated the same as one built from hardened CI. The failure mode is not “we lacked a security artifact.” The failure mode is “we had no mechanism turning that artifact into a trust decision.”

The topic matters because these mechanisms answer different questions, and if you confuse them you leave gaps. Knowing what is inside an artifact does not tell you who produced it. Knowing who signed it does not tell you whether it came from your approved build path. If you do not separate those questions, you will think you have coverage while an attack walks through the unanswered one.

---

## What You Need To Know First

**1. Hashes and digital signatures**  
A hash is a fingerprint of data: if the file changes, the hash changes. A digital signature uses a private key to sign that fingerprint so that anyone with the public key can verify two things: the content has not changed, and the signer possessed the private key. That is the base mechanism behind artifact signing.

**2. CI/CD pipelines and build systems**  
A build system is the thing that turns source code plus inputs into an artifact: binary, package, image, release bundle. CI/CD pipelines automate that process. This matters because many supply-chain claims are really claims about the build environment: what inputs it used, what workflow ran, and whether that environment can be trusted not to forge results.

**3. Container images and OCI registries**  
A container image is a packaged filesystem plus metadata, usually stored in a registry. OCI is the common format and distribution model many tools build around. Signatures and attestations can be stored next to the image in the same registry and linked to the image by digest, which is why registries become the place where these trust artifacts live.

**4. Dependency graphs and transitive dependencies**  
Your code depends on packages directly, and those packages depend on others. Those indirect dependencies are transitive dependencies. Supply-chain security gets tricky because the real software you ship includes the whole graph, not just the top-level packages you intentionally chose.

---

## The Key Ideas, Connected

**1. Supply chain security is really three separate questions about an artifact: what is in it, who produced it, and how it was produced.**  
The article’s core model is that SBOMs, signatures, and provenance are not interchangeable controls. They cover different uncertainty. An SBOM describes composition. A signature binds an artifact to an identity. Provenance describes the build process that created it. You need this separation first because the rest of the mechanics only make sense if you stop expecting one artifact to answer all three questions.

That separation immediately creates a practical requirement: each question needs its own evidence and its own verification path. Once you see that, it becomes obvious why “we sign our images” does not answer “what vulnerable libraries are inside them,” and “we generated an SBOM” does not answer “did this come from our approved CI.” That leads directly to understanding SBOMs more precisely.

**2. An SBOM is a standardized inventory of the components actually present in a built artifact, not just a list of declared dependencies.**  
A dependency file like `package-lock.json` or `go.sum` reflects what your source says it wants or resolved during package management. An SBOM aims to describe the contents of the final thing you ship: packages, embedded libraries, OS packages, runtimes, build tools, vendored code, and more. The reason standard formats matter is that machines need a predictable structure to query and compare across tools.

This matters because vulnerability matching is not done against “whatever developers wrote in a manifest.” It is done against identified components in shipped artifacts. If your goal is to ask “are we running something affected by this new CVE?”, the quality of that answer depends on whether the SBOM reflects reality. That requirement forces the next idea: when and how you generate the SBOM changes what it can truthfully claim.

**3. The timing of SBOM generation determines whether it describes declared intent, observed build inputs, or detectable shipped contents.**  
Source-level generation is fast because it reads manifests, but it only sees what was declared. Build-time generation sees what the resolver, compiler, linker, and image builder actually used. Binary analysis sees what ended up in the final artifact but can miss things that are hard to detect from compiled output. These are not just implementation choices; they are different observation points on the lifecycle of software.

Mechanically, each point has blind spots because each sees a different slice of reality. Source analysis misses what the build introduced. Binary analysis misses what cannot be inferred from bytes alone. Build-time generation often gives the strongest practical view because it watches the actual assembly process. Once you understand that, another requirement appears: if the SBOM is going to drive automation, its component names must be stable enough for other systems to match reliably.

**4. Stable identifiers like purl are what make an SBOM machine-actionable instead of merely human-readable.**  
If one tool says “lodash,” another says “npm lodash,” and a vulnerability database stores “pkg:npm/lodash@4.17.21,” correlation becomes brittle guesswork. Package URL gives a standard way to identify packages across ecosystems. That lets scanners and policy systems join SBOM entries to vulnerability records reliably.

This is a deeper point than formatting. Queryability is the whole value proposition if you want automation. Without stable identifiers, the SBOM cannot consistently answer “does this artifact contain component X?” And once the SBOM becomes machine-actionable, you hit the operational truth the article stresses: the document by itself still does nothing unless some system consumes it.

**5. SBOMs create security value only when they are consumed by a pipeline that continuously correlates them against vulnerability intelligence.**  
An SBOM sitting in storage is inert. The useful system is: generate SBOM, store it where it can be found, ingest it into a service, correlate components against updated CVE data, and alert or gate when there is a match. The mechanism is important: vulnerabilities are often discovered after deployment, so the pipeline must re-check old artifacts against newly updated vulnerability data.

That is why “we generated the SBOM during build” is not the finish line. The artifact answers “what is in this image,” but only a consuming system turns that into “this image now contains a newly disclosed vulnerable library.” Once you see that gap between evidence and decision, the same pattern becomes easier to understand for signing.

**6. Artifact signing proves that a particular identity signed a specific artifact digest, but the hard problem is establishing and operating trust in that identity.**  
At the cryptographic level, signing is simple: hash the artifact and sign the hash. But a verifier has to know which public key or trust root to believe, whether the key was compromised, how it rotates, and whether the key really belongs to the claimed producer. Traditional long-lived keys push all that pain onto key storage, distribution, and lifecycle management.

That is why the industry moved toward systems like Sigstore. The problem was never “we lacked a mathematical way to sign files.” The problem was “operating long-lived trust anchors safely at scale is hard.” Once that becomes the bottleneck, a different model becomes attractive: bind signatures to short-lived verified identity instead of persistent private keys.

**7. Sigstore replaces long-lived signing keys with short-lived certificates tied to an authenticated identity and recorded in a transparency log.**  
With Sigstore, Fulcio issues a short-lived certificate after the signer authenticates through an identity provider such as GitHub OIDC. An ephemeral key signs the artifact, and Rekor records the event in an append-only log. Cosign handles the workflow. Verification therefore checks more than file integrity: it checks that a trusted identity signed it, that the certificate was valid at the signing time, and that the event was publicly logged.

This is stronger operationally because it changes the trust statement. Instead of “someone in possession of private key K signed this,” you get something closer to “this GitHub workflow identity signed this at this time, and the event is publicly visible.” That extra context makes policy possible. If identity becomes meaningful, then deployment systems can enforce “only artifacts signed by identities we expect.” That naturally leads to where signing is useful in practice.

**8. Signing only matters when verification is enforced in the deployment path as a hard gate.**  
If a cluster, deploy job, or registry allows unsigned or wrongly signed artifacts through anyway, signatures are decoration. The mechanism of enforcement is usually an admission controller or a CD policy step that verifies signature properties before the artifact can run. This is where the abstract trust evidence becomes an actual operational control.

This idea mirrors the SBOM point: generated evidence without consumption is theater. But it also reveals a limit of signing. Even if you can prove the right identity signed the image, you still do not know whether that image was built through the approved process. A developer or attacker with signing ability might sign something produced outside your controlled pipeline. That is why provenance exists.

**9. Provenance attestations answer a different question: not who signed the artifact, but what build system, inputs, and workflow produced it.**  
A provenance attestation is a signed statement about the build event. It names things like source repository, commit, builder identity, workflow entry point, and materials used. In the SLSA model, the rigor of this claim depends on how trustworthy the build service is. The point is to bridge the gap between artifact and build process.

Mechanically, this lets a verifier test process-level rules. Not just “is this image signed by our org?” but “was this image built by our hardened CI, from our repository, from the expected branch or tag, using the approved workflow?” Signing alone cannot answer those because signatures bind identity to artifact, not workflow to artifact. Once process becomes the thing you care about, provenance has to come from a build system the build itself cannot tamper with.

**10. Provenance is only as trustworthy as the build system that emits it, which makes the build environment the real trust boundary.**  
A provenance document can look perfectly complete and still be weak if the builder is weak. If attackers can compromise the CI system or forge attestations inside a self-hosted environment without isolation, the document stops being strong evidence. SLSA levels matter precisely because they describe how hard it is for a tenant or attacker to fake the build record.

This is the article’s most important “don’t stop at the label” point. A provenance file is not a guarantee by itself; it is a claim backed by the security properties of the builder. That same realism exposes the remaining weak spot in the wider ecosystem: even if your own artifact has good evidence, your view usually stops quickly as you look down the dependency tree.

**11. Supply-chain trust is only one layer deep unless your dependencies also publish verifiable metadata, and today that recursive chain is incomplete.**  
Your SBOM can name `libfoo`. A signature can say `libfoo` came from its maintainer. But unless `libfoo` also has its own SBOM and provenance, you cannot see or verify the full nested chain beneath it. The trust graph does not recurse automatically. It depends on downstream ecosystems publishing compatible metadata and tooling being able to traverse it.

This matters because it explains why supply-chain security is valuable but not absolute. These mechanisms reduce uncertainty; they do not eliminate it. That leads to the final operational conclusion: the point is not to collect more documents, but to automate trust decisions from the evidence you do have.

**12. The real shift is from trust-by-default to trust-by-evidence enforced automatically.**  
The article keeps returning to the same pattern: evidence is only useful when policy consumes it in the critical path. SBOMs feed vulnerability correlation. Signatures feed identity checks. Provenance feeds build-policy enforcement. Humans can inspect these artifacts, but the scalable security property comes from systems refusing deployment when evidence is missing or does not satisfy policy.

That is the chain’s endpoint because all previous ideas feed this one. Standardized component inventory makes automated vulnerability checks possible. Identity-bound signatures make automated producer checks possible. Build attestations make automated process checks possible. The engineering move is to wire those checks into build and deploy gates so artifacts are trusted only when they present verifiable evidence.

---

## Handles and Anchors

**1. Three questions, three artifacts:**  
Ask of every artifact: **What is in it? Who produced it? How was it produced?**  
If you remember only this, you can reconstruct the whole topic: SBOM answers the first, signature the second, provenance the third.

**2. A badge, an ingredient label, and a manufacturing record:**  
An SBOM is the ingredient label. A signature is the badge of the person who handed it to you. Provenance is the factory production record showing which line made it from which inputs. You would not use one of those as a substitute for the others in food safety; same here.

**3. “Evidence that is not enforced is paperwork.”**  
This captures the central operational tension. Teams think producing the artifact means they have the control. They do not. The control appears only when some system reads that evidence and blocks or alerts on it.

---

## What This Changes When You Build

**1. An engineer who understands this will choose SBOM generation points based on the question they need answered, because source manifests and shipped artifacts expose different truths.**  
The unaware engineer defaults to “scan `package.json` or `requirements.txt` and call it done.” That misses build-introduced dependencies, base-image packages, linked system libraries, and vendored content. The aware engineer asks: do I need a fast declared-dependency view, or do I need a representation of what we actually ship? That usually pushes them toward build-time or image-level SBOM generation for deployable artifacts.

**2. An engineer who understands this will design an SBOM consumption pipeline, not just an SBOM generation step, because vulnerabilities are discovered after artifacts are built.**  
The default behavior is to archive the SBOM for audits and never revisit it. The consequence is that newly disclosed CVEs affecting already deployed images stay invisible unless some manual scan happens later. The aware engineer sets up storage, ingestion, correlation against updated vulnerability feeds, and alerting keyed to deployed artifact digests.

**3. An engineer who understands this will enforce signature verification in admission or deployment policy, because an unchecked signature does not change runtime risk.**  
The unaware engineer signs everything in CI and assumes that improved security posture follows automatically. But if Kubernetes, the CD job, or the release promotion step never rejects bad signatures, an attacker can still deploy unsigned or wrongly signed artifacts. The aware engineer makes verification a gate: only images signed by expected identities, under expected trust roots, are allowed through.

**4. An engineer who understands this will treat signing policy and provenance policy as separate controls, because identity approval and build-path approval are different decisions.**  
The default mistake is to say “it was signed by our GitHub org, so it is trusted.” That still permits artifacts built from the wrong workflow, wrong branch, wrong repository, or a less controlled path. The aware engineer writes provenance-aware policies such as “must be built by this reusable workflow from this repository on this ref pattern,” instead of relying on signer identity alone.

**5. An engineer who understands this will evaluate the build system as a security boundary, because provenance strength collapses if the builder can be tampered with.**  
The unaware engineer sees “SLSA L3 provenance generated” and treats the label as portable truth. The aware engineer asks harder questions: Is the builder isolated? Ephemeral? Can tenants alter the provenance generation path? Who controls the signing identity for attestations? This changes platform choices, especially around self-hosted CI, because the value of provenance is directly tied to how hard it is to forge inside your build environment.

**6. An engineer who understands this will scope promises carefully around dependency depth, because ecosystem trust usually stops after the first layer.**  
The default assumption is “we have supply-chain visibility now.” In practice, you usually have strong visibility into your artifact and weak visibility into your dependencies’ dependencies. The aware engineer treats recursive trust as partial, prioritizes critical dependencies, and does not overstate the assurance level to the rest of the organization.

---
