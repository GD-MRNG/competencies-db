## Metadata
- **Date:** 01-01-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# 2.4 Artifact and Dependency Management

Once CI produces a verified artifact, that artifact needs a home. An **artifact registry** (also called a container registry or package registry depending on the artifact type) is the storage system for your built, versioned artifacts. The registry provides versioning (so you can identify exactly which version of the artifact is running where), promotion tracking (tagging an artifact as "staging-verified" before it is allowed into production), retention policies (cleaning up old artifacts to manage storage costs), and access control (preventing unauthorized parties from pulling or pushing artifacts).

**Semantic versioning** is the convention by which artifacts are numbered in a way that communicates the nature of the change. A version number of the form `MAJOR.MINOR.PATCH` communicates whether a change is a breaking change (major), a backward-compatible addition (minor), or a backward-compatible fix (patch). Understanding semantic versioning is important for dependency management because it tells you how risky it is to update a dependency. Upgrading from `2.3.1` to `2.3.2` should be safe. Upgrading from `2.3.1` to `3.0.0` may require significant code changes on your part.

**Dependency pinning and lock files** are the practices that make your dependency tree explicit and reproducible. When you declare a dependency as `"requests": "^2.28.0"`, you are saying "any version from 2.28.0 up to but not including 3.0.0 is acceptable." This means your build might use `2.28.0` today and `2.31.1` tomorrow if the library author releases an update, and those two versions may behave differently. A lock file (like `package-lock.json` in Node or `Pipfile.lock` in Python) records the exact version of every dependency (including transitive dependencies, the dependencies of your dependencies) that was used in a specific build. When a lock file is committed to version control, your build tool will always use exactly those versions, making the build reproducible across machines and over time.

**Supply chain security** has moved from an academic concern to a practical operational requirement. The 2020s saw a series of high-profile supply chain attacks in which malicious code was introduced into widely-used open-source libraries and executed in the applications of everyone who depended on them. Your application's attack surface is not limited to the code you write; it includes every library you import, and the libraries those libraries import. The mitigations for this include vulnerability scanning (automated tools that compare your dependency versions against databases of known vulnerabilities), integrity verification (checking that the dependency you download matches a known cryptographic hash), and artifact provenance (establishing a verifiable chain of custody from source code to deployed artifact). These practices belong in your CI pipeline so that every build is automatically checked against known vulnerabilities, and every dependency is verified against its expected signature.

## Level 2 candidates

**What an Artifact Is: The Unit of Deployment**

The distinction between source code as human-authored instructions and a built artifact as the executable product of a deterministic build process, and why the artifact rather than the source is the thing you deploy. It matters because treating source code and artifacts as interchangeable leads to non-reproducible deployments where "deploying the same version" means something ambiguous.

**Semantic Versioning: What a Version Number Communicates**

The major.minor.patch convention, what each segment signals about the nature of a change, and how package managers use this to resolve dependency graphs. It matters because version numbers are a contract between a library author and their consumers, and breaking the convention creates unexpected upgrade failures downstream.

**Dependency Graphs and Transitive Dependencies**

How a dependency's dependencies become your dependencies, why a small change to a shared library can have a blast radius across many services, and how dependency resolution algorithms handle conflicting version requirements. It matters because most security vulnerabilities in production applications arrive through transitive dependencies, not direct ones, and understanding the graph is prerequisite to managing it.

**Artifact Registries: Storage, Distribution, and Promotion**

What a registry stores, how artifact discovery works, the difference between a public registry and a private one, and how registry design supports the concept of promoting an artifact through environments rather than rebuilding it. It matters because the registry is the handoff point between CI and CD, and how you version and organize artifacts in the registry determines how reliably you can deploy and roll back.

**Dependency Pinning vs Version Ranges: The Reproducibility Tradeoff**

The tradeoff between pinning exact dependency versions for reproducibility versus using version ranges that automatically receive security patches and minor improvements. It matters because both extremes are dangerous — unpinned dependencies cause sudden breakage, and pinned dependencies accumulate unpatched vulnerabilities — and the right policy depends on understanding the tradeoff.

**Supply Chain Security: Why Your Dependencies Are Your Attack Surface**

How a compromised or malicious package in the dependency graph becomes an attack vector, what software composition analysis tools do, and what SBOMs and signing provide. It matters because the majority of high-profile supply chain attacks in recent years have exploited dependency relationships rather than the target's own code, and this risk is invisible without deliberate management.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Modern software is rarely “just your code.” What actually runs in production is a built artifact, assembled from your source code, your direct dependencies, your transitive dependencies, your build tooling, and whatever exact versions happened to be resolved at build time. If you cannot name and control that artifact precisely, you lose the ability to answer basic operational questions like: *What is running? Where did it come from? Can we rebuild it? Can we trust it?*

Without a solid grip on registries, versioning, lock files, and supply chain controls, teams run into very practical failures. A deployment works in staging but not production because a dependency shifted underneath the build. A rollback fails because nobody knows which image was actually deployed. A critical vulnerability is announced and the team cannot quickly tell whether they are affected. These are not documentation problems; they are control problems.

This topic exists because CI by itself is not enough. Building and testing software proves something *once*. Engineering teams also need a durable system for storing that result, identifying it unambiguously, reproducing it later, and verifying that nothing unsafe entered the build along the way.

---

## What You Need To Know First

### 1. Build artifact

A build artifact is the output of your build process: a container image, package, binary, JAR, wheel, or similar deliverable. It is the thing you actually deploy or publish. The important idea is that production does not run your Git repository directly; it runs an artifact produced from it.

### 2. Dependency tree

A dependency tree is the full set of external code your application relies on, including both the libraries you directly choose and the libraries *they* rely on. Those indirect ones are called transitive dependencies. This matters because your software behavior and risk profile depend on the whole tree, not just the top-level packages you remember adding.

### 3. Reproducible build

A reproducible build is a build that produces the same resolved inputs every time you run it under the same conditions. In this article’s context, the key idea is not bit-for-bit theory; it is practical repeatability: if two engineers or two CI runs build the same commit, they should resolve the same dependency versions and produce the same intended artifact.

### 4. Cryptographic hash and signature

A cryptographic hash is a fingerprint of a file; if the file changes, the fingerprint changes. A signature uses cryptography to let you verify who produced something and whether it was altered. You do not need the math here — just the engineering use: hashes help confirm *this file is exactly the one expected*, and signatures help support *this file came from who it claims to come from*.

---

## The Key Ideas, Connected

### 1. Once CI builds something trustworthy, you need a system to store and identify that exact thing.

CI can compile, test, and verify your code, but those checks are only useful if the resulting output is preserved as a first-class object. That is the role of an artifact registry: it is the controlled home for built outputs. Instead of rebuilding ad hoc or passing files around informally, you store the exact artifact that passed CI so later environments can pull the same object. That naturally leads to the next question: if many artifacts are stored there, how do you tell them apart safely?

### 2. A registry is valuable because it gives artifacts identity, history, and control.

An artifact registry is not just a bucket of files. It adds versioning, tags, promotion states, retention rules, and permissions. That means you can distinguish artifact A from artifact B, track which one was approved for staging or production, clean up old versions, and restrict who can publish or consume them. Once artifacts have durable identity, the next issue is how that identity communicates change to humans and systems.

### 3. Semantic versioning is a language for signaling how risky a change probably is.

A version like 2.3.1 is not just a label; under semantic versioning it carries meaning. PATCH suggests a backward-compatible fix, MINOR suggests a backward-compatible addition, and MAJOR warns of breaking changes. This helps engineers reason about upgrades without reading every line of source code first. But semantic versioning only helps if you are choosing versions intentionally. That leads to the next problem: what happens when your build accepts a *range* instead of a specific version?

### 4. Version ranges create flexibility, but they also make builds drift over time.

If you declare a dependency as allowing any compatible version, the build tool may resolve a different version next week than it did today. Nothing in your own repository changed, but your build result did. That can be convenient for automatically picking up fixes, yet it also means “same source code” no longer guarantees “same behavior.” Once you see that instability, the need for lock files becomes obvious.

### 5. Lock files turn an allowed dependency range into an exact dependency snapshot.

A lock file records the precise versions selected for all dependencies, including transitive ones. So while your manifest may say “versions in this range are acceptable,” the lock file says “this build used exactly these versions.” Committing that lock file means other developers, CI agents, and future rebuilds can resolve the same dependency tree. That is how dependency management moves from approximate to reproducible. And once you can reproduce the tree, you can inspect and secure it more systematically.

### 6. Reproducibility matters not just for debugging, but for trust.

If you cannot reproduce what was built, you cannot confidently investigate failures, compare environments, or prove what code went into production. Reproducibility is therefore an operational control, not just a convenience. It gives you a stable target for testing, rollback, and auditing. But even a perfectly reproducible build can still reproduce something malicious or vulnerable, which brings in supply chain security.

### 7. Your software supply chain includes every external component that enters the build, not just the code your team wrote.

Applications inherit risk from third-party libraries, transitive dependencies, downloaded packages, base images, and build-time tooling. That means an attacker does not need to compromise your repository directly; compromising something you consume may be enough. Once engineers recognize that the dependency tree is part of the attack surface, they need controls that check both *known risk* and *artifact authenticity*.

### 8. Supply chain defenses answer three different questions: is it known-bad, is it the expected file, and can we prove where it came from?

Vulnerability scanning checks dependency versions against databases of known issues. Integrity verification checks that downloaded content matches an expected hash, helping detect tampering or substitution. Provenance goes one step further by establishing a verifiable chain from source to build to artifact, so you can show how the deployed output was produced. These are complementary, not interchangeable. A package can be authentic and still vulnerable; it can be non-vulnerable in the database and still be tampered with. That is why the final idea is about automation.

### 9. These controls belong in CI because trust must be enforced automatically, not remembered manually.

If version locking, scanning, signature checking, and provenance generation are optional side activities, they will be skipped under delivery pressure. Putting them in CI makes them part of the contract of every build. The result is a pipeline where the artifact is built, dependencies are resolved predictably, risks are checked, and the final output is stored in a controlled registry with enough metadata to deploy it confidently later. That is the full chain the article is trying to get you to see.

---

## Handles and Anchors

### 1. The registry is a warehouse with labeled, sealed boxes.

CI is the factory. The artifact registry is the warehouse. Semantic versions are the labels, promotion tags are the “approved for store shelves” stickers, lock files are the packing lists, and signatures are the tamper-evident seals. If the boxes are unlabeled, swapped, or unsealed, you stop trusting distribution even if the factory worked perfectly.

### 2. A dependency range is a recipe; a lock file is the exact grocery receipt.

A recipe might say “use cheddar cheese,” which leaves room for variation. A grocery receipt says exactly which brand and package you bought that day. Dependency declarations describe acceptable inputs; lock files record the exact ones actually used. If you want the meal to come out the same tomorrow, the receipt matters.

### 3. The core tension is: flexibility speeds updates, exactness preserves control.

Allowing version ranges makes it easier to pick up improvements automatically. Pinning and locking make it easier to reproduce, debug, and trust builds. Good engineering is not choosing one forever; it is knowing when you want movement and when you need stability.

---

## What This Changes When You Build

- An engineer who understands this will treat the built artifact as the deployable unit, not the source branch, because production reliability depends on promoting the *same verified output* through environments rather than rebuilding differently each time.
- An engineer who understands this will be careful about using broad dependency ranges in production systems because range-based resolution can change build behavior without any source-code diff in the application repository.
- An engineer who understands this will commit and maintain lock files because debugging, rollback, and incident response are dramatically easier when the exact dependency tree of a release is knowable and reproducible.
- An engineer who understands this will separate “version intent” from “resolved version state” because the manifest expresses compatibility policy, while the lock file captures the concrete dependency set that was actually tested.
- An engineer who understands this will design CI to fail builds on security policy violations because vulnerability scanning, integrity checks, and provenance are only reliable controls when they are automatic gates rather than best-effort manual checks.
- An engineer who understands this will use registry tags and promotion markers carefully because labeling an artifact as staging-approved or production-approved creates an auditable release path and reduces the risk of deploying an unverified build.
- An engineer who understands this will respond to security advisories differently because they can ask precise questions such as “Which deployed artifacts include the affected dependency version?” instead of starting from a vague search through repositories and build logs.

</details>
