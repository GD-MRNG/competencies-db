## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers will say they "deploy code." They'll point to a commit SHA, a branch name, or a pull request and call it "the version that's running in production." This is imprecise in a way that causes real problems. You never deploy source code. You deploy an artifact — the output of a build process that took your source code as one of its inputs. The distinction sounds pedantic until you've spent an evening debugging why "the same version" behaves differently in staging and production, only to discover that the two environments are running two different builds of the same commit, each assembled with slightly different inputs. The artifact is the unit of deployment, and understanding what that means at a mechanical level is what separates reproducible systems from systems that merely seem reproducible.

## What a Build Actually Produces

Source code is a set of human-authored instructions. It describes intent. It cannot execute on its own. Between your source code and the thing that actually runs in a compute environment, a build process performs a series of transformations.

For a compiled language like Go or Rust, the build compiles source into machine code, links in libraries, and produces a binary. For an interpreted language like Python, the build still does real work: it resolves and installs dependencies, potentially compiles C extensions, bundles everything into a distributable format like a wheel or a container image. For a JavaScript frontend, the build transpiles, bundles, tree-shakes, minifies, and produces static assets. In every case, the build takes multiple inputs and produces a single output — the **artifact**.

The artifact is a self-contained (or close to self-contained) unit that can be placed onto a target environment and executed. A Docker image. A JAR file. A statically linked binary. A `.deb` package. A ZIP archive of bundled Lambda code. The specific format varies by ecosystem, but the defining characteristic is the same: the artifact is the product of a build, not the source of one.

This matters because the build process is a function with multiple inputs, and source code is only one of them.

## The Inputs to a Build

Think of the build as a function:

```
artifact = build(source, dependencies, toolchain, environment, configuration)
```

**Source** is the code you wrote, pinned to a specific commit. **Dependencies** are the third-party libraries your code imports — their exact versions, resolved transitively. **Toolchain** is the compiler, interpreter, bundler, or build tool itself, along with its version. **Environment** is the operating system, system libraries, CPU architecture, and locale settings of the machine performing the build. **Configuration** includes build flags, environment variables, feature toggles baked in at build time, and any templated values.

Change any one of these inputs and you may get a different artifact. This is the fundamental reason why "deploy from the same commit" and "deploy the same artifact" are not equivalent statements.

Consider a concrete case. Your Node.js application is at commit `a1b2c3d`. You build it on Monday on a CI runner using Node 20.11.0 and your lockfile pins `lodash` at `4.17.21`. The build produces a Docker image. On Thursday, your CI runner fleet gets a routine update. Node is still 20.11, but the underlying `alpine` base image has been patched. You rebuild from the same commit. Your source hasn't changed. Your lockfile hasn't changed. But the resulting Docker image has different system libraries. You now have two different artifacts from the same commit, and they are not guaranteed to behave identically.

## Artifact Identity: Digests vs. Tags

The Level 1 post covered semantic versioning as a communication convention. Here we need to look at how artifacts are actually identified in practice — and why the common approach is subtly dangerous.

A **tag** is a human-readable label attached to an artifact. When you push a Docker image as `myapp:v1.2.3` or `myapp:latest`, that tag is a pointer. It is mutable. Someone (or some automation) can push a different image under the same tag, and the old image is silently dereferenced. Tags are convenient for humans. They are not reliable identifiers.

A **digest** is a cryptographic hash of the artifact's content. For a container image, it looks like `myapp@sha256:3e7a8f1b...`. It is computed from the actual bytes of the image. If a single bit changes, the digest changes. Digests are immutable by definition — they are derived from content, not assigned by convention.

This distinction has direct operational consequences. If your deployment manifests reference `myapp:v1.2.3`, and someone rebuilds and pushes a new image under that same tag, your next deployment (or your next pod restart that triggers an image pull) will silently pick up the new image. You've changed what's running in production without changing your deployment configuration. If instead your manifests reference `myapp@sha256:3e7a8f1b...`, the only way to change what's deployed is to explicitly update the digest, which shows up as a change in version control.

This is why mature deployment systems pin artifacts by digest, not by tag. Tags remain useful as human-readable references, but the digest is the source of truth for identity.

## Immutability and the Promotion Model

Once you understand that an artifact's identity is its content hash, a critical operational principle follows: **the artifact you tested must be the artifact you deploy.**

This sounds obvious, but the default behavior of many CI/CD pipelines violates it. A common pattern is to trigger a fresh build for each environment: build for staging, run tests, then build again for production. Even if the source commit is the same, you now have two different artifacts. The one running in production was never tested. You tested its sibling.

The correct model is **build once, promote through environments**. A single build produces a single artifact. That artifact is deployed to a test or staging environment and verified. If it passes, the *same artifact* — same bytes, same digest — is deployed to production. Nothing is rebuilt. The promotion is a metadata change (marking the artifact as "production-approved"), not a transformation.

This means that environment-specific configuration cannot be baked into the artifact at build time. If your staging artifact contains a hardcoded staging database URL, you can't promote it to production without rebuilding. This is why configuration injection at deploy time (through environment variables, mounted config files, or secrets managers) is not just a best practice but a structural requirement of the promotion model. The artifact must be environment-agnostic, or the promise of immutability breaks.

## Reproducible Builds vs. Immutable Artifacts

These two concepts are related but distinct, and conflating them causes confusion.

An **immutable artifact** means: once built, the artifact does not change. Its content hash is fixed. You store it, you reference it by that hash, and you deploy exactly those bytes. This is achievable today with any decent artifact registry and content-addressable storage. It is a property of your storage and deployment pipeline.

A **reproducible build** means: given the same inputs, the build process produces bit-for-bit identical output every time. This is a property of your build process, and it is significantly harder to achieve. Most builds are not fully reproducible. Timestamps get embedded in binaries. File system ordering varies. Compiler optimizations differ between toolchain patch versions. Docker layer caching introduces subtle variability.

Reproducible builds are valuable — they let you verify that an artifact was actually built from the source it claims to come from, which is a key supply chain security property. But they are not a prerequisite for safe deployments. What safe deployments require is immutable artifacts: build it once, verify it, and never rebuild it. Reproducible builds solve a different problem (verifiability and auditability), and pursuing perfect reproducibility can become an expensive yak-shave if you conflate it with deployment safety.

## Where This Breaks

**The "just rebuild it" reflex.** When something goes wrong in production and a team wants to "redeploy the same version," the instinct is often to re-run the CI pipeline on the same commit. If the artifact registry has been cleaned up, or if the pipeline is structured to always build fresh, this produces a new artifact. If that new artifact behaves differently — because a base image was updated, a dependency mirror returned different content, or the build environment drifted — you've introduced a variable into your incident response. You are now debugging two things: the original problem and whether the redeployment changed something. Teams that store and promote immutable artifacts can redeploy by pulling the known-good artifact from the registry. Teams that rebuild on demand cannot.

**Tag overwriting in registries.** Many container registries allow tag overwriting by default. A team tags builds as `myapp:latest` or even `myapp:v2.1.0` and pushes repeatedly. Kubernetes pulls the latest image matching the tag. Over time, the relationship between "version 2.1.0" and "what's actually running" becomes unverifiable. Registry immutability settings (available in ECR, GCR, Artifact Registry, and others) prevent tag overwriting and should be enabled for any production-facing registry.

**Enormous artifacts without layer awareness.** Container images are layered. Each instruction in a Dockerfile produces a layer, and layers are cached and shared. If you copy your entire application and its dependencies in a single layer, every build produces a full-size layer even if only one line of code changed. Understanding layer structure is not just a storage optimization — it affects pull times, startup latency, and registry egress costs. Ordering your Dockerfile so that infrequently changing layers (OS packages, dependency installation) come before frequently changing layers (application code) is a direct consequence of understanding what the artifact actually is: a stack of content-addressed layers, not a monolithic blob.

**Environment-specific artifacts.** When teams bake environment configuration into the build — API endpoints, feature flags, log levels — they end up maintaining parallel build pipelines for each environment. This multiplies build time, makes promotion impossible, and guarantees that the artifact running in production is not the one that passed staging tests. The artifact must contain the application and its dependencies. Configuration is supplied at runtime.

## The Mental Model

An artifact is a point-in-time snapshot of your application in executable form. It captures not just your source code but the fully resolved dependency tree, the compiled output, and the build toolchain's decisions — all frozen at the moment of the build. Source code tells you what you intended. The artifact is what actually runs.

The core principle that follows: **build once, deploy everywhere.** The artifact is built a single time, identified by its content hash, stored immutably, and promoted through environments unchanged. Configuration varies between environments; the artifact does not. When you need to know what's running in production, the answer is a content hash that points to exactly one set of bytes, not a commit SHA that might have produced different artifacts on different days.

If you carry one thing forward from this post, it should be the habit of thinking about deployments in terms of artifact identity rather than source identity. A commit SHA tells you what source code was written. An artifact digest tells you what is running.

## Key Takeaways

- Source code is an input to a build process; the artifact is its output. They are not interchangeable references to "the version" of your application.
- A build is a function of source, dependencies, toolchain, build environment, and configuration. Changing any input can change the resulting artifact, even if the source commit is the same.
- Tags are mutable pointers assigned by humans or automation. Digests are immutable identifiers derived from artifact content. Pin deployments by digest, not by tag.
- Build once, promote through environments. The artifact that passed your tests must be the artifact you deploy to production — not a fresh build from the same commit.
- Immutable artifacts and reproducible builds solve different problems. Immutable artifacts ensure deployment consistency. Reproducible builds ensure auditability. You need the first for safe deployments; the second is a harder and separate goal.
- Environment-specific configuration must be injected at deploy time, not baked into the artifact at build time. If configuration is in the artifact, promotion across environments requires a rebuild, which breaks immutability.
- Enable tag immutability in your artifact registry. Without it, the same tag can reference different artifacts over time, making it impossible to know what's actually running.
- When redeploying during an incident, pull the existing artifact from the registry — do not rebuild from source. Rebuilding introduces variables you cannot control during an outage.

# Discussion

## Why This Conversation Is Happening

A lot of deployment mistakes come from talking as if “the commit” and “the thing running” are the same object. They are not. That mismatch matters the moment you try to answer operational questions like: what exactly is in production, what did we test, and can we roll back to the known-good version? If your team only tracks source commits, those questions become surprisingly hard to answer with confidence.

What breaks in practice is reproducibility of operations. You rebuild from the same commit and assume nothing changed, but the new build pulls a patched base image, resolves dependencies slightly differently, or runs under a different toolchain. Now “the same version” behaves differently across staging and production, or across two incident redeploys. You lose the ability to reason cleanly about cause and effect.

This is why artifact identity matters. Without it, deployments become slippery: tags drift, rebuilds introduce invisible changes, and debugging gets contaminated by uncertainty about whether the software itself changed. The problem is not vocabulary precision for its own sake; the problem is being unable to say, with evidence, what bytes are actually running.

---

## What You Need To Know First

**1. Build process**  
A build is the set of steps that turns code into something runnable or deployable. Depending on the stack, that might mean compiling, bundling, linking, packaging dependencies, or assembling a container image. The important part is that a build is a transformation step between source code and execution.

**2. Dependencies and version pinning**  
Your application usually relies on third-party packages, libraries, or base images. “Pinning” means recording exact versions so the build uses the same dependency set each time, instead of “whatever is current.” This reduces one source of drift, but it does not eliminate all drift.

**3. Hashes / digests**  
A digest is a hash computed from content. You can think of it as a fingerprint of the bytes. If the content changes, the digest changes. That makes digests useful as immutable identifiers: they identify what something is, not just what someone called it.

**4. Runtime configuration**  
Some values should be supplied when the software runs, not when it is built: database URLs, API endpoints, credentials, feature flags, region-specific settings. If these are baked into the build output, then each environment needs its own separately built artifact.

---

## The Key Ideas, Connected

**1. You do not deploy source code; you deploy an artifact.**  
Source code is what humans write, but it is not usually what the runtime executes directly. Something has to happen in between: compilation, packaging, dependency installation, bundling, image creation. The result of that transformation is the artifact. That matters because the deployable unit is the output of the build, not the input. Once you accept that, the next question becomes: what determines the artifact you get?

**2. A build is a function of multiple inputs, not just the source commit.**  
The article’s formula is the key mechanic:

`artifact = build(source, dependencies, toolchain, environment, configuration)`

This means the commit SHA tells you only one part of the story. The exact dependency graph, compiler or runtime version, OS libraries, CPU architecture, locale, build flags, and embedded config can all influence the output. That is why “same commit” does not imply “same artifact.” Once you see the build as a multi-input function, it becomes obvious why rebuilding later can silently produce different results.

**3. Because builds can vary, source identity and runtime identity must be separated.**  
A commit identifies authored source at a point in version control. An artifact identifies a concrete built output. Those are related, but not interchangeable. Two builds from the same commit can produce different artifacts if any non-source input changed. So if your operational question is “what is running?”, a commit is an incomplete answer. You now need a way to identify the artifact itself, which leads directly to tags versus digests.

**4. Tags are labels; digests are identity.**  
A tag like `v1.2.3` or `latest` is a human-assigned pointer. It is convenient, but it can be moved. A digest is derived from the artifact’s content, so it changes only when the bytes change. Mechanically, this is the difference between naming by convention and naming by content. If your deployment references a tag, the meaning of that reference can change without the manifest changing. If your deployment references a digest, changing what runs requires changing the reference itself. That makes the change visible and reviewable.

**5. Once artifact identity is content-based, safe deployment means deploying the exact tested artifact.**  
If a digest identifies one exact set of bytes, then “the artifact we tested” is a concrete thing, not an abstract version label. From there, the next principle follows almost automatically: the thing promoted to production should be the same digest that passed staging or tests. If you rebuild for production, you have broken that chain. Even if the source commit matches, the output might not. So the tested object and the deployed object diverge.

**6. This creates the build-once, promote-through-environments model.**  
To preserve identity, you build once, store the artifact, test that artifact, and then promote that same artifact to later environments. Promotion is not another build step; it is a decision about where to deploy an already-built object. This model exists because repeated building reintroduces variation. If deployment safety means “production runs the tested bytes,” then rebuilding per environment defeats that safety property.

**7. Build-once promotion only works if environment-specific values are not baked into the artifact.**  
This is an important dependency. If the artifact contains a staging DB URL or staging-only flags, you cannot promote it unchanged to production. You are forced to rebuild. So the promotion model requires environment-agnostic artifacts and runtime configuration injection. In other words: immutability of the artifact pushes configuration out of the build and into deployment/runtime mechanisms.

**8. Immutable artifacts and reproducible builds are different guarantees.**  
An immutable artifact means that after creation, those exact bytes are stored and deployed unchanged. A reproducible build means rerunning the build with the same inputs produces the same bytes again. The first is about deployment consistency; the second is about rebuild verifiability. This distinction matters because teams often chase reproducibility when their immediate operational need is simply to stop rebuilding during promotion or incident response. You need immutability to know what you are running. You need reproducibility to prove a rebuild would match.

**9. Most real failure modes come from violating artifact identity without noticing.**  
“Redeploy the same version” often means “rerun CI on the same commit,” which is not the same thing at all. Tag overwrites let the label stay stable while the content changes underneath. Environment-specific builds multiply artifacts and make staging validation less meaningful. Poor container layer structure inflates artifact size and slows pulls because the artifact is actually a stack of content-addressed layers, not one opaque blob. These failures are all expressions of the same underlying mistake: treating deployment as if the source version alone determines what runs.

**10. The right mental model is: source expresses intent, artifact is the executable snapshot.**  
Source tells you what developers wrote. The artifact captures what the build system actually resolved, compiled, bundled, and packaged at one moment in time. Operationally, the artifact is the thing you can store, hash, promote, redeploy, and audit. Once you internalize that, “what’s running?” stops being answered with a branch or commit and starts being answered with an artifact digest.

---

## Handles and Anchors

**1. Handle: “A commit is a recipe; an artifact is the meal.”**  
The recipe describes what should be made. But the actual meal depends on ingredients, kitchen tools, substitutions, and preparation. Two cooks can use the same recipe and produce different dishes. In the same way, two builds from the same commit can produce different artifacts.

**2. Handle: “Tags are nicknames; digests are fingerprints.”**  
A nickname can be reused or reassigned. A fingerprint is tied to the thing itself. If you want operational certainty, use the fingerprint.

**3. Question to ask of any deployment system:**  
“When we say ‘deploy the same version,’ do we mean reusing the exact same artifact bytes, or rebuilding from the same source?”  
If the answer is the second one, the system is less stable than it sounds.

---

## What This Changes When You Build

**1. An engineer who understands this will treat the artifact registry as part of the release system, because the deployable unit must be stored and reused, not regenerated.**  
The unaware default is to let CI build on demand whenever a deployment happens. The consequence is that rollback and incident redeploys become fresh builds, which introduces new variables exactly when you need stability.

**2. An engineer who understands this will pin deployments by digest, not by mutable tags, because “same tag” does not guarantee “same bytes.”**  
The unaware default is to deploy `:latest` or even a semantic version tag and assume that label is stable enough. The consequence is silent drift: pod restarts or later deploys may pull different content without any config diff showing why.

**3. An engineer who understands this will design pipelines around build-once promotion, because test results only transfer if the exact artifact transfers.**  
The unaware default is separate staging and production builds from the same commit. The consequence is false confidence: staging validated one artifact, production runs another.

**4. An engineer who understands this will move environment-specific configuration to runtime injection, because baked-in config prevents artifact promotion across environments.**  
The unaware default is compiling endpoints, flags, or credentials directly into the artifact for each environment. The consequence is multiple environment-specific artifacts, slower pipelines, and no clean path to immutable promotion.

**5. An engineer who understands this will care about Dockerfile layer ordering and artifact composition, because the artifact is a structured object whose layout affects operational cost and speed.**  
The unaware default is writing a Dockerfile that copies everything early and rebuilds large layers constantly. The consequence is larger pushes and pulls, worse cache reuse, slower deploys, and higher registry/network costs.

---
