## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers treat an artifact registry the way they treat an S3 bucket: you push a thing in, you pull the thing out, and the interesting work happens elsewhere. This mental model is comfortable, and it works right up until the moment it doesn't — when a deployment that passed staging behaves differently in production, when a rollback pulls an artifact that isn't what you expected, or when a registry outage takes down your entire deployment pipeline because nothing was designed to tolerate it. The registry is not passive storage. It is a system with specific semantics — content addressing, mutable references, layered deduplication, distribution protocols — and those semantics directly determine whether your CI/CD pipeline is reliable or merely appears to be.

## What a Registry Actually Stores

A registry stores artifacts, but "artifact" is a more structured concept than "file." The mechanics differ by ecosystem, but the most instructive example is the OCI (Open Container Initiative) model used by container registries, because it makes the internal structure explicit. Other registries — npm, Maven, PyPI — follow similar principles with different implementation details.

In an OCI-compliant registry, what you think of as "an image" is actually three distinct things: **blobs**, **manifests**, and **tags**.

**Blobs** are the actual content — compressed filesystem layers, configuration data. Each blob is stored and addressed by its cryptographic digest, typically a SHA-256 hash. A blob with digest `sha256:a3ed95c...` is always and forever that exact sequence of bytes. If a single bit changes, the digest changes. This is content-addressable storage: the address *is* the content's identity.

A **manifest** is a JSON document that describes an artifact by listing the digests of its constituent blobs and their media types. The manifest itself also has a digest. When you "pull an image," you are first retrieving a manifest, and then using the blob digests within it to pull the actual data. For multi-platform images, there is an additional layer: an **index** (or manifest list) that maps platform/architecture combinations to individual manifests.

A **tag** is a human-readable name — `v1.4.2`, `latest`, `staging-verified` — that points to a manifest digest. This is the critical detail: **tags are mutable pointers to immutable content**. The tag `v1.4.2` points to a specific manifest digest right now, but someone with write access can re-push a different image under the same tag, and the pointer silently changes. The digest never lies. The tag can.

Package registries work on a similar conceptual model even when the implementation differs. An npm package at version `1.2.3` is a tarball with an integrity hash. A Maven artifact has coordinates (group, artifact, version) and a checksum. The fundamental pattern is the same: immutable content identified by hash, with human-friendly identifiers layered on top.

## How a Pull Actually Resolves

When a deployment system or container runtime requests an artifact, the resolution process follows a specific sequence that matters for understanding failure modes.

Given a reference like `registry.example.com/myapp:v1.4.2`, the client first resolves the tag. It issues an HTTP GET to the registry's API — for OCI registries, this is `GET /v2/myapp/manifests/v1.4.2`. The registry returns the manifest along with its content digest in a header. The client now has a complete description of what the artifact contains.

The client then walks the manifest's blob list and issues a GET for each blob it doesn't already have locally. This is where **deduplication** pays off. Container images are built in layers, and many images share base layers. If your local cache (or the registry's storage) already has a blob matching a given digest, it doesn't need to transfer it again. A 500MB image might only require 12MB of actual network transfer if the base layers are already cached.

This is also why **pull-through caches** and **registry mirrors** work. A pull-through cache sits between your infrastructure and an upstream registry. The first pull fetches from upstream and caches locally. Subsequent pulls serve from cache. Because content is addressed by digest, the cache can verify integrity without trusting the upstream — if the bytes don't hash to the expected digest, the pull fails. This is not just a performance optimization. It is a reliability boundary. When Docker Hub has a rate limit incident or a public registry goes down, your pull-through cache is the difference between "deploy continues" and "deploy blocked."

## Public Registries vs. Private Registries

The distinction between public and private registries is not just about access control. It is about trust boundaries, availability guarantees, and operational control.

A **public registry** (Docker Hub, npm's public registry, Maven Central) is a shared commons. You consume artifacts you did not build, from maintainers you do not control, on infrastructure you do not operate. The trust model is: you trust that the registry's integrity mechanisms (signatures, checksums) are intact, and you trust that the package maintainer hasn't published something malicious. The availability model is: you hope it's up when you need it.

A **private registry** (Artifactory, Nexus, AWS ECR, Google Artifact Registry, GitHub Packages) is infrastructure you operate or delegate to a cloud provider. It stores artifacts you built, and optionally proxies or mirrors artifacts from public registries. The trust model shifts — you control who can push, and you can enforce policies like vulnerability scanning gates before an artifact becomes pullable. The availability model becomes your responsibility.

The practical pattern most production systems use is a **private registry that proxies public registries**. This gives you a single pull endpoint for both your own artifacts and third-party dependencies, with the private registry acting as a cache and policy enforcement point. Your build system references `registry.internal/dockerhub-proxy/node:20-alpine` instead of `docker.io/node:20-alpine`. This insulates your builds from upstream availability issues, gives you a point to inject scanning policies, and provides an audit log of every artifact that enters your environment.

This proxy pattern also addresses a subtle operational risk. If your CI pipeline pulls a base image directly from a public registry at build time, and that base image tag gets updated between two builds, your "same source code" can produce different artifacts. Proxying through a private registry with tag immutability enforced — or better, pinning to a digest — closes this gap.

## Promotion: Moving Artifacts, Not Rebuilding Them

Promotion is the concept that most directly separates mature deployment pipelines from fragile ones. The principle is simple: **an artifact that passes testing in one environment should be the exact artifact deployed to the next environment, with zero modification**. In practice, implementing this correctly requires understanding registry mechanics.

The naive approach is to rebuild for each environment. Your CI pipeline builds from source, runs tests, and pushes to a dev registry. When you want to deploy to staging, you run the pipeline again and push to a staging registry. This is wrong for a specific reason: the artifact deployed to staging is not the artifact you tested. It was built from the same source (probably), but the build may not be reproducible — a transitive dependency may have updated, a build tool may have changed, a layer cache may have been invalidated. The only way to guarantee you are deploying what you tested is to deploy the same bytes, verified by digest.

Promotion in registry terms typically follows one of two patterns.

**Tag-based promotion** means adding tags to an existing manifest. After an artifact at `myapp@sha256:abc123` passes staging tests, you add the tag `production-approved` to that same digest. The content doesn't move. The bytes don't change. A new pointer is added to the same immutable content. This is cheap and fast, but it requires your registry to be accessible from all environments, and it means your staging and production infrastructure pull from the same registry instance.

**Copy-based promotion** means copying the artifact from one registry or repository to another. After staging validation, you copy `staging-registry.example.com/myapp@sha256:abc123` to `production-registry.example.com/myapp@sha256:abc123`. The digest is preserved across the copy, so you can verify that the production artifact is byte-identical to what was tested. This is necessary when environments are network-isolated (common in regulated industries or multi-cloud setups), but it introduces a copy step that must be managed, and you need tooling to verify digest consistency post-copy.

In both cases, the digest is the anchor. Configuration that varies between environments — database connection strings, feature flags, resource limits — lives outside the artifact, in environment-specific configuration that is injected at deploy time. The artifact is the constant. The configuration is the variable.

## Where Registries Break and Where Misunderstanding Costs You

**Tag mutability is the most common source of deployment non-determinism.** If your Kubernetes manifests reference `myapp:latest` or even `myapp:v1.4.2` by tag, and someone pushes a new image under that tag, your next pod restart pulls a different artifact than the one currently running. This is not a hypothetical — it is the default behavior. The fix is to reference artifacts by digest in deployment manifests (`myapp@sha256:abc123`), but this trades human readability for determinism. Most teams use a hybrid: tags for human communication, digests in deployment automation.

**Registry availability is a deployment dependency you may not have accounted for.** If your container runtime's image pull policy is `Always` (the Kubernetes default for the `latest` tag), every pod restart requires a registry round-trip. A registry outage means pods cannot start. Even with `IfNotPresent`, a node that hasn't cached the image yet — say, a new node added by autoscaling — will fail to pull. Pre-pulling images to nodes, using DaemonSets for critical images, or running a registry mirror per cluster are mitigations, each with operational cost.

**Garbage collection in content-addressable registries is non-trivial.** Because blobs are shared across manifests (via deduplication), you cannot delete a blob just because one manifest no longer references it — another manifest might. Registry garbage collection is a mark-and-sweep process: mark all blobs referenced by any current manifest, sweep everything else. Running this on a large registry with millions of layers is expensive and typically requires downtime or a read-only window in older implementations. If you never run garbage collection, storage costs grow without bound. If you run it incorrectly, you can delete blobs still in use by manifests, corrupting those artifacts.

**Promotion without environment-specific config separation leads to config leaking into artifacts.** If your artifact contains staging database credentials baked into a config file, promoting that artifact to production doesn't just fail — it connects your production system to your staging database. Promotion only works when the artifact is genuinely environment-agnostic, which requires disciplined separation of build-time concerns (code, dependencies, compiled output) from deploy-time concerns (configuration, secrets, resource allocation).

## The Model to Carry Forward

A registry is a content-addressed store with a mutable naming layer on top. The immutable layer — digests — gives you identity, integrity, and reproducibility. The mutable layer — tags — gives you human usability and workflow semantics like promotion. Every reliability property of your deployment pipeline depends on which layer you anchor to, and when.

The registry sits at the boundary between build and deploy. Everything before it (source, compilation, testing) produces an artifact. Everything after it (deployment, rollback, scaling) consumes one. The integrity of that boundary — the guarantee that what you tested is what you deploy — depends on treating the registry not as a file dump but as a system whose semantics you understand and deliberately use. Promotion is the practice that makes this real: one artifact, built once, verified progressively, deployed everywhere. The digest is the proof.

## Key Takeaways

- **Tags are mutable pointers; digests are immutable identifiers.** Referencing an artifact by tag in deployment automation introduces non-determinism. Reference by digest when determinism matters.

- **A container image is not a single file — it is a manifest pointing to content-addressed blobs.** Understanding this structure is necessary to reason about layer caching, deduplication, and garbage collection.

- **Promotion means moving (or retagging) a tested artifact to the next environment without rebuilding it.** If you rebuild for each environment, you are not deploying what you tested, regardless of whether the source code is the same.

- **Private registries that proxy public registries give you a cache, an availability buffer, and a policy enforcement point** — solving three problems at once.

- **Registry availability is a hidden deployment dependency.** If the registry is unreachable and the image is not locally cached, pods cannot start. Design for this, especially in autoscaling scenarios.

- **Garbage collection in content-addressable registries is a mark-and-sweep operation** that requires care. Mismanaging it either wastes storage or corrupts artifacts.

- **Promotion only works when artifacts are environment-agnostic.** Configuration that varies between environments must be injected at deploy time, not baked in at build time.

- **The digest is the single most reliable identifier in the entire pipeline.** It is the only mechanism that guarantees the bytes you deploy are the bytes you tested. Treat it as the source of truth.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Artifact registries become important the moment you need deployments to be repeatable, explainable, and survivable under failure. If your team thinks of the registry as “just storage,” you end up making dangerous assumptions: that `myapp:v1.4.2` always means the same bytes, that rebuilding from the same source is equivalent to reusing the same artifact, or that a deployment can proceed even if the registry is flaky. Those assumptions hold until they suddenly do not.

What actually breaks is concrete. A rollback fetches a tag that was silently repointed. A node added by autoscaling cannot start pods because the registry is unavailable. Two builds from the same commit produce different outputs because a base image or dependency tag moved underneath you. Storage costs explode because garbage collection was never designed into the operating model. These are not “best practice” issues; they are failures caused by misunderstanding what the registry is doing mechanically.

---

## What You Need To Know First

### 1. Cryptographic digests / hashes
A digest is a fingerprint of some bytes, usually produced by a hash like SHA-256. If the bytes change, the digest changes. That gives you a way to talk about exact content, not just a name someone attached to it. For this article, the important property is: a digest identifies one exact blob or manifest, and you can verify that what you received matches what you expected.

### 2. Immutable vs. mutable identifiers
An immutable identifier always refers to the same thing. A mutable identifier can be updated to point somewhere else. In registry terms, a digest is immutable identity, while a tag is a mutable label. If you keep that distinction clear, most of the article’s reliability arguments make sense.

### 3. CI/CD pipeline boundary
A CI/CD pipeline has a build side and a deploy side. The build side turns source code into an artifact; the deploy side takes an artifact and runs it somewhere. The registry sits between those two halves. The key question is whether the deploy side is consuming the exact thing the build side tested, or just something with a similar name.

### 4. Layered artifacts and caching
Container images are usually built from layers, not as one monolithic file. If two images share the same base layers, those layers can be reused instead of downloaded again. This matters because registries are not only naming systems; they also exploit shared content for performance and storage efficiency.

---

## The Key Ideas, Connected

### 1. A registry does not just store files; it stores structured artifacts with identity semantics.
What this means is that the registry understands more than “blob in, blob out.” In OCI-style registries, the stored object has internal structure: content blobs, manifests that describe how those blobs fit together, and tags that give humans friendly names. That structure is why the registry can support integrity checks, deduplication, caching, promotion, and policy enforcement.

Once you see that the artifact is structured, the next question becomes: which part of that structure is the stable truth, and which part is just a convenient label?

### 2. The stable truth is the digest, because content is addressed by hash.
A blob addressed by digest is tied to exact bytes. A manifest also has a digest, so the whole image description can be pinned immutably too. That gives you a strong anchor: if two systems refer to the same digest, they mean the same content.

This matters because humans rarely use digests directly. We prefer names like `latest` or `v1.4.2`. So once immutable identity exists, registries add a more usable naming layer on top of it—and that creates the core tradeoff.

### 3. Tags are useful because they are human-friendly, but dangerous because they are mutable pointers.
A tag is not the artifact itself. It is a reference that currently points to a manifest digest. That means tags are workflow tools, not truth. They let teams say “deploy the staging-approved build” or “pull version 1.4.2” without memorizing hashes. But because the pointer can change, the same tag can resolve to different content at different times.

That mutability is exactly why deployment systems become non-deterministic when they rely on tags alone. If the pointer moves, your deployment changes without your source code changing. That leads directly to needing to understand how pulls actually resolve.

### 4. Pulling an artifact is a resolution process: first resolve the name, then fetch the referenced content.
When a client pulls `myapp:v1.4.2`, it does not fetch a single opaque file. It first asks the registry what manifest that tag points to. Then it reads the manifest and fetches the needed blobs by digest. This is the actual mechanical path from a human-readable reference to concrete bytes on disk.

That resolution path explains several behaviors that otherwise look accidental. It explains why tag changes alter future pulls. It explains why clients can reuse existing layers if they already have matching digests. And it explains why caches and mirrors are possible: once content is identified by digest, intermediaries can store and verify it safely.

### 5. Content addressing makes deduplication, local caching, and pull-through caches work.
Because layers are named by digest, identical layers across many images collapse to the same stored object. A runtime or registry can say, “I already have blob `sha256:...`; I do not need to transfer it again.” That is why large images can pull surprisingly fast when base layers are already present.

This is not only about speed. It creates a reliability tool. A pull-through cache or private proxy can keep local copies of upstream artifacts, reducing dependency on public registries. Since the cached content can be validated against its digest, the cache does not have to blindly trust what it serves. Once registries are part of your delivery path, that availability boundary becomes operationally significant.

### 6. Registry choice is really about trust and availability boundaries, not just public vs. private access.
A public registry means you depend on someone else’s infrastructure, publishing workflow, and uptime. A private registry means you control—or delegate control over—who can push, what policies apply, and how available the service is to your own systems. The important shift is that the registry becomes part of your supply chain and deployment control plane, not just a download endpoint.

That is why many mature setups use a private registry to proxy public ones. The proxy gives one internal source of truth, one cache, one audit point, and one place to enforce policy. Once you adopt that model, the next issue is not just “where do artifacts live?” but “how do artifacts move through environments without changing?”

### 7. Promotion exists because rebuilding is not the same as reusing the same artifact.
If you rebuild for staging and rebuild again for production, you have created two different opportunities for drift: dependency versions may change, build tools may change, caches may differ, and upstream tags may move. Even if the source commit is identical, the produced bytes may not be. So “same code” is not strong enough if you care about deploying what you tested.

That is why promotion means carrying forward the already-built artifact. The mechanism can be retagging the same digest or copying the same digest to another registry. In both cases, the digest is the evidence that the promoted object is the tested one. Once promotion becomes the goal, another constraint appears: the artifact itself cannot contain environment-specific state.

### 8. Promotion only works if the artifact is environment-agnostic and configuration is injected later.
If your image contains staging credentials, then promoting that exact image to production is wrong by construction. The whole promise of promotion is “same artifact, different environment-specific config.” So code and dependencies belong in the artifact, while secrets, endpoints, resource settings, and flags belong outside it at deploy time.

This separation is what lets one digest move cleanly from dev to staging to production. It also makes rollbacks meaningful: you are rolling back to known bytes, while environment-specific configuration stays under separate control. With that model in place, the common failure modes become easier to explain.

### 9. Most operational problems come from anchoring to the mutable layer when you needed the immutable one.
Tag-based deployment references create surprise changes. Registry outages break pod starts because image pulls require registry access. Garbage collection becomes tricky because shared blobs cannot be deleted by simple file cleanup; you must trace which manifests still reference them. All of these behaviors follow directly from the registry’s mechanics: content-addressed storage plus a mutable naming layer plus shared references.

So the working model to keep is: the digest layer gives identity and reproducibility; the tag layer gives usability and workflow semantics. Reliable systems deliberately choose which layer to rely on for each job. Human communication can use tags. Automation that needs determinism should anchor to digests.

---

## Handles and Anchors

### 1. Think of tags as symlinks and digests as inode-level identity.
A filename or symlink is convenient for humans, but it can be repointed. The underlying inode-like object is the actual thing. In registries, the tag is the repointable name; the digest is the thing with stable identity.

### 2. One sentence to keep: “Tags tell you what people call it; digests tell you what it is.”
This is the core distinction behind most of the article. If you remember only one line, remember that one.

### 3. Ask this question of any deployment system:
“When this system says it is deploying version X, is that a mutable name or an immutable byte identity?”
If the answer is “a mutable name,” you have found a source of drift, rollback confusion, and hard-to-explain production differences.

---

## What This Changes When You Build

### 1. An engineer who understands this will reference artifacts by digest in deployment automation because tags do not guarantee byte identity.
The unaware default is to put `myapp:v1.4.2` or `myapp:latest` into Kubernetes manifests or deployment scripts and assume that label is stable enough. The consequence is that restarts, rollouts, or new nodes may pull different bytes than the ones originally tested. The aware engineer may still use tags for release workflow, but resolves them to digests before deployment.

### 2. An engineer who understands this will promote a tested artifact forward rather than rebuild it for each environment because rebuilds reintroduce drift.
The unaware default is “same source, same result,” so they rerun the pipeline for staging and production. The consequence is subtle non-reproducibility: different base image, dependency, or toolchain state can produce a different artifact. The aware engineer treats the registry as the handoff point and moves the exact same digest through environments.

### 3. An engineer who understands this will separate environment configuration from the artifact because promotion only works when the artifact stays constant.
The unaware default is to bake environment details into files during build time, especially for convenience in CI. The consequence is either rebuilding per environment or, worse, deploying production with staging settings embedded. The aware engineer keeps config and secrets outside the image and injects them at deploy time.

### 4. An engineer who understands this will design for registry unavailability because image pulls are a runtime dependency, not just a build-time dependency.
The unaware default is to notice the registry only when CI pushes images. The consequence appears later: node replacement, autoscaling, or pod restart fails during a registry outage. The aware engineer changes cluster design decisions—using mirrors, pre-pulls, local caches, or controlled pull policies—because they recognize that startup path depends on registry reachability.

### 5. An engineer who understands this will treat registry cleanup as graph management, not file deletion, because blobs are shared across artifacts.
The unaware default is to think old tags can be deleted and storage will naturally shrink. The consequence is either unbounded storage growth or accidental corruption if cleanup is too aggressive. The aware engineer plans retention and garbage collection around manifest-to-blob references, knowing shared layers make deletion non-local.

---

</details>
