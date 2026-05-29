## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams have a CI/CD pipeline. Few can point to the exact place where CI ends and CD begins. Ask where the boundary is and you'll get vague gestures toward "after the tests pass" or "when it deploys to staging." This ambiguity is not just semantic — it is architectural. The slash in "CI/CD" has collapsed two fundamentally different operations into what feels like a single flow, and that conflation is the root cause of a specific class of operational problems: rollbacks that don't work, environment configurations that drift silently, and deployments where no one can say with certainty what artifact is running or where it came from.

The Level 1 post established the principle: build once, deploy many. This post is about the machinery that makes that principle hold — what CI actually produces, where that output goes, how it gets from "verified" to "deployed," and what breaks when the boundary between those two phases is missing or misdrawn.

## What CI Actually Produces

CI's job terminates in two outputs: a **verdict** and an **artifact**.

The verdict is binary: this commit either integrates cleanly with the mainline or it does not. The test suite passes, the linter passes, the build compiles. The verdict gates whether the commit is eligible for merge. This is the part most engineers are familiar with — the green check or the red X.

The artifact is the less obvious but more important output. When CI succeeds, it should produce an **immutable, versioned object** — a Docker image, a JAR file, a compiled binary, a tarball — that is stored somewhere durable and addressable. This artifact is the thing that will eventually be deployed. Not the source code. Not a future rebuild from the same commit. This specific artifact.

The artifact must carry enough metadata to be traceable back to its origin. At minimum, that means: the commit SHA it was built from, the build ID or pipeline run that produced it, and the digest or checksum of the artifact itself. Many teams also attach the test results, the dependency manifest, and the signature of the build system. This metadata is not decorative — it is the chain of evidence that connects a running process in production back to a specific state of the source code and a specific set of verified properties.

Here's a concrete example. A CI pipeline for a Go service runs on commit `a1b2c3d`. It compiles the binary, runs unit and integration tests, builds a Docker image, and pushes it to a container registry tagged as `myservice:a1b2c3d` with a SHA256 digest of `sha256:9f3e...`. That digest is the artifact's true identity. The tag is a convenience label. From this moment forward, every environment that runs this service should run exactly `sha256:9f3e...`. Not `myservice:latest`. Not a rebuild. That specific image.

## The Artifact Registry as the Boundary

The boundary between CI and CD is not a stage in a YAML file. It is a **storage layer** — the artifact registry.

CI's responsibility ends when the artifact is written to the registry with its metadata. CD's responsibility begins when it reads from the registry to decide what to deploy and where. The registry is the handoff point. It is also the source of truth about what artifacts exist, what their provenance is, and which ones have been promoted to which environments.

This is why the registry is architecturally critical, not just operationally convenient. It decouples the build process from the deployment process in time, in tooling, and in authorization. CI can be driven by GitHub Actions while CD is driven by Argo CD. CI can run on a developer's merge event while CD runs on an operator's approval. The registry is what makes this separation possible without losing traceability.

When this boundary does not exist — when the pipeline builds and deploys in a single uninterrupted flow — CI and CD become temporally and operationally coupled. You cannot deploy without building. You cannot redeploy a previous version without re-running a previous build. You lose the ability to answer the question "what exact thing is running in production right now?" without reverse-engineering it from pipeline logs.

## The Difference Between "Passed" and "Deployable"

CI passing means one thing: the artifact meets the integration criteria defined by the test suite and build checks at the time of merge. It does not mean the artifact is ready for production. These are different assertions with different evidence.

An artifact that passes CI has been verified against unit tests, maybe integration tests, maybe a linter and a static analysis check. An artifact that is **deployable** has additionally survived a promotion process: it has been deployed to a staging or pre-production environment, it has passed acceptance tests or smoke tests that run against a realistic configuration, and it may have been reviewed by a human or approved by a policy gate.

The promotion process is a sequence of assertions, each one narrowing the gap between "this code compiles and passes isolated tests" and "this code behaves correctly in an environment that resembles production." Each assertion is applied to the **same artifact**. The artifact does not change. What changes is the set of properties that have been verified about it.

Concretely, promotion often looks like this: CI produces `myservice:a1b2c3d` and writes it to the registry. A CD process picks it up and deploys it to a `dev` environment. Automated smoke tests run. If they pass, the artifact is marked as eligible for `staging`. A CD process deploys the same image to `staging`. A more comprehensive acceptance suite runs. If it passes, the artifact is marked as eligible for `production`. An operator or automated policy approves the promotion. CD deploys the same image to `production`.

At no point is the artifact rebuilt. At no point is the source code checked out again. The image digest `sha256:9f3e...` is the same in every environment. What differs is the **configuration** applied to it.

## Configuration as a Separate Channel

This is the piece most teams get wrong at the boundary: the artifact is immutable, but its behavior must vary across environments. Different database connection strings, different feature flags, different resource limits, different TLS certificates. How do you reconcile immutability with environment-specific behavior?

The answer is that **configuration is not part of the artifact**. Configuration is injected at deployment time, externally, through environment variables, mounted config files, secret managers, or a configuration service. The artifact contains the code and its dependencies. The configuration tells that code how to behave in a specific context.

This separation is what makes "build once, deploy many" mechanically possible. If database credentials were baked into the Docker image at build time, you would need a different image for every environment, which means you would need a different build, which means you are no longer deploying what you tested. The environment-specific configuration must travel through a different channel than the artifact itself.

In practice, this means your CD system needs to manage two things in concert: which artifact version to deploy, and which configuration to apply. These are often stored in different places — the artifact in a container registry, the configuration in a Git repository (in the GitOps model), a secrets manager, or a configuration management database. The CD system's job is to bind the right artifact to the right config for the right environment and apply the result.

```yaml
# GitOps-style environment config — artifact version pinned, config separate
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myservice
spec:
  template:
    spec:
      containers:
        - name: myservice
          image: registry.example.com/myservice@sha256:9f3e...
          envFrom:
            - configMapRef:
                name: myservice-staging-config
            - secretRef:
                name: myservice-staging-secrets
```

The image reference is a digest — immutable. The config and secrets are environment-specific. This is the separation in action.

## Tradeoffs and Failure Modes

### The Coupled Pipeline

The most common failure mode is a pipeline that builds and deploys in one continuous job. It usually starts innocently: the team has a single CI workflow file that compiles, tests, builds a Docker image, and then `kubectl apply`s it to a cluster. It works fine on day one.

The problems emerge over time. You cannot roll back to a previous artifact without re-running a previous pipeline. If the build tooling has changed, or a transient dependency has shifted, the "rollback" produces a different artifact than the original. You cannot deploy to a new environment without wiring it into the CI configuration, which means your deployment topology is coupled to your build system. And when the deployment fails, the pipeline failure is ambiguous — did the code fail to build, or did the cluster fail to accept the deployment? These are different categories of failure with different remediation paths, and the coupled pipeline obscures which one you're dealing with.

### The Configuration Leak

The second failure mode is configuration that bleeds into the artifact. This shows up as build-time environment variables that change per environment, config files that are copied into the Docker image during build, or feature flags that are compiled into the binary. The symptom is usually that staging works but production doesn't, even though "it's the same code." It is the same code — but it's not the same artifact, because the build baked in staging-specific configuration.

A subtler version of this leak occurs with dependency resolution at build time. If your `Dockerfile` runs `npm install` without a lockfile, or resolves `latest` tags for base images, the artifact produced today is not the artifact produced tomorrow, even from the same commit. The build process itself has become a source of configuration drift.

### The "Deploy on Green" Trap

Some teams set up their pipeline so that a green CI run on the main branch automatically triggers a production deployment. This conflates the verdict ("this code integrates correctly") with the promotion decision ("this code should serve production traffic"). It eliminates the space where acceptance testing, canary analysis, and human judgment operate.

Deploy-on-green works for small teams with high test confidence and low blast radius. It breaks when the test suite has gaps (all suites do), when production has failure modes that staging cannot reproduce, or when you need to coordinate a deployment with an external dependency like a database migration or a partner API change. The problem isn't automation — it's the elimination of the promotion boundary as a distinct, governable decision point.

## The Mental Model

CI is a factory. Its input is source code. Its outputs are a verdict and an artifact. Once the artifact leaves the factory, CI's job is done. CD is a logistics operation. Its job is to take an artifact that has already been built and move it through a series of environments, applying environment-specific configuration at each stop and verifying that the artifact behaves correctly in each context.

The artifact registry sits between them. It is the loading dock — the place where CI drops off what it produced and CD picks up what it needs. The registry is the single source of truth about what has been built, what has been tested, and what is eligible for deployment to which environment.

If you can draw a clean line in your system at the registry — CI writes to it, CD reads from it, nothing crosses that line in both directions — you have a pipeline that supports independent rollbacks, reproducible deployments, and clear operational boundaries. If you cannot draw that line, every deployment carries implicit uncertainty about what was actually built, what was actually tested, and whether the thing running in production is the thing you think it is.

## Key Takeaways

- **CI produces two things: a verdict (pass/fail) and an artifact (the immutable, versioned object that will be deployed).** The artifact is the more important output.

- **The boundary between CI and CD is the artifact registry.** CI writes to it; CD reads from it. If your pipeline does not have this boundary, your build process and deployment process are coupled in ways that will eventually cause operational pain.

- **"CI passed" and "this artifact is deployable" are different assertions.** Promotion is the process of applying progressively more rigorous verification to the same artifact across environments, not rebuilding the artifact for each one.

- **Configuration must travel through a separate channel from the artifact.** If environment-specific values are baked into the build, you do not have an immutable artifact — you have a different artifact for every environment, and you are deploying untested builds.

- **A pipeline that builds and deploys in one continuous job cannot roll back cleanly**, because rollback requires deploying a previous artifact, not re-running a previous build.

- **Artifact identity is a digest, not a tag.** Tags like `latest` or `v1.2.3` are mutable labels. The SHA256 digest is the only reliable way to guarantee that the artifact running in production is the one that was tested.

- **Deploy-on-green eliminates the promotion boundary.** This is a deliberate tradeoff, not a best practice. It works when blast radius is small and test confidence is high. It fails when either condition is not met.

- **If you cannot answer "what exact artifact is running in production right now?" from the registry alone, your CI/CD boundary is missing or broken.**

# Discussion

## Why This Conversation Is Happening

A lot of teams say they have “CI/CD,” but in practice they have one long automation script that builds, tests, and deploys in a blur. That works until you need to answer operational questions under pressure: What exactly is running in production? Can we roll back right now? Did staging and production run the same thing? If the answer depends on reading old pipeline logs, re-running a build, or trusting a mutable tag like `latest`, the system is already more fragile than it looks.

The reason this matters is that build systems and deployment systems solve different problems, and when you blur them together, you inherit specific failure modes. Rollbacks silently produce new binaries instead of redeploying old ones. Environment-specific settings get baked into images, so “the same code” behaves differently across environments. A pipeline failure tells you only “something went wrong,” not whether the code failed verification or the cluster rejected a deploy. These are not naming issues; they are mechanical issues that affect reliability, traceability, and incident response.

This topic exists because once software is deployed repeatedly across multiple environments, you need a trustworthy handoff between “we built and verified something” and “we chose to run that thing here.” Without that handoff, you lose control over artifact identity, promotion, and rollback — exactly the things you need most when production is on fire.

---

## What You Need To Know First

### 1. Artifact
An artifact is the built output of your code: a Docker image, binary, JAR, tarball, and so on. It is not the source repository and not the idea of “version 1.2”; it is the concrete thing produced by a specific build. The article assumes that deployment should happen from this built object, not by rebuilding from source every time.

### 2. Immutable vs mutable identity
Immutable means “this exact thing cannot change”; mutable means “this label can point to different things over time.” A SHA256 digest is immutable: it identifies one exact image. A tag like `latest` or even `v1.2.3` is mutable: someone can retag it later. You need this distinction to understand why the article insists that the digest, not the tag, is the artifact’s real identity.

### 3. Environment-specific configuration
The same application often needs different values in different places: database URLs, secrets, feature flags, resource limits, certificates. Configuration is those varying inputs. The key prerequisite is that code can stay the same while configuration changes at deploy time; if config is baked into the build, you no longer have one artifact moving through environments.

### 4. Promotion
Promotion means taking the same built artifact and advancing it from one environment to another as it earns more trust. For example: build once, deploy to dev, then staging, then production. Promotion is not “rebuild with production settings”; it is “apply more evidence and then deploy the same artifact again.”

---

## The Key Ideas, Connected

### 1. CI does not just give you a pass/fail result; it should also produce the deployable artifact.
The familiar output of CI is the green checkmark: tests passed, lint passed, build succeeded. But the more important output is the actual thing those checks were performed on — the built artifact. If CI only tells you “this commit passed” without preserving the exact built output, then deployment later depends on rebuilding, and that rebuild may not produce the same result.

That matters because deployment needs something concrete to move around. CD cannot reliably deploy “a commit” or “whatever source was on main at that time”; it needs a stable object. Once you accept that CI must produce and preserve that object, the next question becomes: where does that object live so CD can use it later?

### 2. The real boundary between CI and CD is the artifact registry.
The article’s main structural claim is that the handoff is not a stage label in a YAML pipeline. It is a storage boundary: CI writes the artifact to a durable registry, and CD reads it from there. That registry is what separates “building and verifying” from “choosing where to run.”

This separation matters because it breaks coupling. If deployment can only happen inside the same pipeline run that built the image, then building and deploying are one operation in practice, even if you call them different stages. But once the artifact is stored durably, CD can happen later, with different tooling, different permissions, and different approval logic. That makes rollback and promotion possible as independent actions. Once the registry becomes the boundary, artifact identity and traceability become critical, which leads to the next idea.

### 3. The artifact has to be traceable and identified immutably.
If CI writes an artifact into a registry, you need to know exactly what that artifact is and where it came from. That means metadata: commit SHA, build ID, digest, maybe test results and signatures. The digest matters most because it is the immutable identity of the artifact.

This is the mechanism that makes traceability real instead of aspirational. If production is running `sha256:9f3e...`, you can ask: which commit produced this, which pipeline built it, and which checks were run against it? If instead production is running `myservice:latest`, you have only a mutable label, not a trustworthy answer. Once artifact identity is stable, you can start making stronger claims about moving that same artifact through environments rather than rebuilding it each time.

### 4. “CI passed” and “this is deployable to production” are different claims.
A passing CI run tells you that the artifact met a certain set of integration checks at build time. That is useful, but limited. It does not prove the artifact behaves correctly with production-like config, production infrastructure, external dependencies, real traffic patterns, or operational constraints.

So another stage of decision-making becomes necessary: promotion. Promotion exists because the evidence required for “mergeable” is weaker than the evidence required for “safe to run in production.” Once you separate these claims, CD is no longer just “automatically deploy what CI built”; it becomes the process of applying further checks and approvals to the same artifact as it moves through environments. That “same artifact” part is essential, which is why the next idea exists.

### 5. Promotion only means something if the artifact stays the same across environments.
If you build once for dev, rebuild for staging, and rebuild again for prod, you are not promoting one artifact — you are testing one thing and deploying another. That destroys the chain of evidence. The whole point of promotion is that confidence accumulates around a fixed object.

Mechanically, that means the binary or image must not change between environments. The digest in dev should be the digest in staging and the digest in prod. If it changes, any claim like “it passed staging” applies only to the staging-built artifact, not the production one. But environments do need to differ somehow, so the system needs another channel for those differences. That requirement leads directly to configuration separation.

### 6. Environment differences must come from configuration, not from rebuilding the artifact.
Applications behave differently in dev, staging, and production because the context changes: database endpoints, secrets, feature flags, CPU limits, certificates, and so on. If you tried to encode those differences by changing the artifact itself, you would need a separate build per environment. That would violate build-once-deploy-many.

So configuration has to be injected externally at deploy time. The artifact carries code and dependencies; configuration tells that code which environment it is in and what resources to use there. This is the only way to have one immutable artifact and still get environment-specific behavior. Once you see config as a separate channel, CD’s job becomes clearer: it is binding one artifact identity to the right environment-specific configuration. That also explains a major class of failure.

### 7. When configuration leaks into the build, you no longer have one tested artifact.
A team may think they are deploying the same service everywhere because the source code is the same. But if they bake different env vars, config files, dependency versions, or base-image resolutions into each build, then each environment is running a different artifact. The build has become environment-sensitive.

This is why the failure mode is so deceptive. Engineers say, “it worked in staging, but failed in prod even though it was the same code.” The mechanism is that it was not the same artifact. The configuration leak broke immutability. Once you understand that, the article’s criticism of coupled pipelines becomes easier to see: if building and deploying are one uninterrupted flow, you make these leaks and couplings much easier to create and much harder to detect.

### 8. A coupled build-and-deploy pipeline removes important operational capabilities.
When one workflow builds and immediately deploys, you lose the clean handoff. You cannot redeploy an old known-good artifact without rerunning old build logic. If dependencies or tooling changed since then, the “same” build may now produce something different. You also mix two distinct failure domains: build failures and deployment failures.

That coupling is not just inconvenient; it changes what operations are possible. Rollback becomes “rebuild an old commit and hope,” not “redeploy a known artifact.” Deploying to a new environment means editing build logic. Investigating incidents means piecing together what happened from pipeline history rather than asking the registry. This also explains why “deploy on green” is a deliberate tradeoff rather than an automatic best practice.

### 9. Deploy-on-green collapses verification and promotion into one decision.
If every green CI run on main goes straight to production, then you have chosen to treat “passed integration checks” as sufficient evidence for “should receive production traffic.” Sometimes that is acceptable — small systems, excellent tests, low blast radius. But it is still a choice to remove the promotion boundary.

The reason this is risky is that production readiness often depends on more than CI can know: rollout timing, partner dependencies, migration sequencing, canary results, human review, or environment-specific smoke tests. If you eliminate the boundary, you eliminate the place where those judgments can happen. This brings the whole model together: CI builds and verifies an artifact, the registry preserves and identifies it, CD promotes that same artifact through environments with separate configuration, and operational safety depends on keeping those boundaries real.

---

## Handles and Anchors

### 1. Factory and logistics
CI is a factory: it manufactures a specific item and stamps it with identity and quality checks. CD is logistics: it moves that already-manufactured item to different destinations. If the warehouse cannot tell you exactly which package was shipped, the problem is not shipping speed — it is loss of control over inventory.

### 2. “Test the object, then move the object.”
This is the core sentence. Not: test the code, then rebuild it elsewhere. Not: test a commit, then hope a later build matches. Test the object, then move the object. If the object changes, your evidence no longer applies.

### 3. Diagnostic question
Ask of any pipeline: “Can I tell, from the registry alone, exactly what artifact is running in production and redeploy it without rebuilding?” If the answer is no, the CI/CD boundary is either missing or too weak to trust under pressure.

---

## What This Changes When You Build

### 1. An engineer who understands this will pin deployments by digest, not by tag, because tags are labels and digests are identity.
The unaware engineer writes `image: myservice:latest` or `:main` because it is convenient and human-readable. The consequence is that nobody can prove which image actually ran when that tag was resolved. The aware engineer treats tags as pointers for people and digests as the contract for systems.

### 2. An engineer who understands this will design CI to publish artifacts into a registry and stop there, because deployment needs a durable handoff point.
The default inherited design is a single workflow that builds, tests, and deploys in sequence. That feels simpler initially, but it couples rollback, promotion, and deployment topology to the build system. The aware engineer creates a point where CI finishes after producing a traceable artifact, allowing CD to operate later and independently.

### 3. An engineer who understands this will treat rollback as redeploying a previous artifact, not rebuilding an old commit, because reproducibility matters most during incidents.
The unaware engineer reaches for “rerun the old pipeline” or “checkout the old SHA and rebuild.” That can silently produce a different result if dependencies, base images, or tooling changed. The aware engineer keeps prior artifacts available and rollback-ready in the registry, so rollback is selecting an old digest, not rerunning history.

### 4. An engineer who understands this will keep configuration outside the artifact, because per-environment rebuilds destroy the meaning of promotion.
The default mistake is to inject env-specific files or variables during image build, often because it seems easier at first. That produces different images for dev, staging, and prod, even if the codebase is the same. The aware engineer separates code from runtime configuration, so the same artifact can be promoted while only config changes per environment.

### 5. An engineer who understands this will create a distinct promotion step between “passed CI” and “goes to production,” because those are different assertions backed by different evidence.
The unaware engineer often lets a green build auto-deploy everywhere by default, inheriting the assumption that integration checks equal production readiness. The aware engineer decides explicitly whether that tradeoff is acceptable for this system’s blast radius, test confidence, and operational constraints, and introduces staging checks, approvals, or canary gates when it is not.