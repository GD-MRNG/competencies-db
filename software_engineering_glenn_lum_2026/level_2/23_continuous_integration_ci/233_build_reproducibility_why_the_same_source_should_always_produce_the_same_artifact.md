## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers, when they hear "reproducible build," think about pinning dependency versions. Pin your packages, lock your transitive dependencies, and you're done. This is necessary, but it addresses maybe a third of the problem. The actual challenge of build reproducibility is that a build is a function with *hundreds* of inputs, and most of them are invisible. Your source code is one input. Your dependency lockfile is another. But the compiler version, the system locale, the current timestamp, the ordering of files on disk, the contents of environment variables, the architecture of the CPU running the build — these are all inputs too. Every undeclared input is a vector for non-determinism. The question isn't whether your builds are reproducible. The question is how many of their inputs you've actually accounted for.

## The Anatomy of a Non-Deterministic Build

A build process transforms inputs into outputs. When we say a build is **reproducible**, we mean it behaves as a pure function: the same inputs always produce the same output, byte for byte. When we say a build is **hermetic**, we mean something slightly different — that the build has no ability to reach outside its declared inputs. Hermeticity is the mechanism; reproducibility is the property it produces.

The reason builds are non-reproducible in practice is that they consume **implicit inputs** — values that affect the output but are never declared in the build definition. These fall into a few distinct categories, and understanding them individually is what makes it possible to systematically eliminate them.

### Timestamps and Volatile Metadata

The most pervasive source of non-determinism is time. Many build tools embed timestamps into their output by default, and they do it in ways that aren't obvious.

When you produce a `.jar` file, you're creating a ZIP archive. ZIP entries carry modification timestamps from the files on disk. Build the same source on the same machine a minute later, and the archive is different because the `.class` files have different `mtime` values. The same applies to `.tar.gz` archives, Docker image layers, and any artifact format that preserves filesystem metadata.

Some tools embed build timestamps explicitly. Go binaries, for example, used to embed the build time and VCS metadata into the binary by default (this has improved in recent versions with `-buildvcs=false` and `-trimpath`). Java's `MANIFEST.MF` commonly includes a `Build-Time` entry. C/C++ builds that use `__DATE__` or `__TIME__` macros will produce different binaries every second.

The fix is unglamorous: you strip or normalize metadata. You set file timestamps to a fixed epoch value before archiving. You configure your tools to omit volatile fields. In Bazel, this is handled by the sandbox. In other systems, you do it yourself. The important thing to understand is that this is death by a thousand cuts — there is no single timestamp switch. You have to audit every tool in the chain for every place it captures the current time.

### Non-Deterministic Dependency Resolution

The Level 1 post covered the danger of `latest` version specifiers. The deeper problem is understanding the full chain of what a dependency manager does and where non-determinism enters.

A **manifest** (like `package.json`, `Gemfile`, or `build.gradle`) declares *intent*: what packages you need and what version ranges are acceptable. A **lockfile** (like `package-lock.json`, `Gemfile.lock`, or `gradle.lockfile`) records *reality*: the exact versions that were resolved, including every transitive dependency. Without a lockfile, running `npm install` on the same manifest a week apart can yield entirely different dependency trees because new patch versions were published in the interim.

But even lockfiles have boundaries. They typically lock the *logical* identity of packages (name and version) but not the *physical* content. If a package registry allows a maintainer to republish the same version with different contents — which some registries historically have — your lockfile doesn't protect you. This is why tools like npm added `integrity` fields: cryptographic hashes of the actual package tarballs.

Lockfiles also generally don't cover system-level or native dependencies. If your Python package depends on `libssl`, and the lockfile pins `cryptography==41.0.0`, you've pinned the Python package but not the version of OpenSSL that gets linked at build time. On one build machine you get OpenSSL 3.0, on another you get 1.1.1, and the resulting artifact behaves differently.

Then there's resolution ordering. Some dependency managers don't guarantee a deterministic resolution order when the constraint space permits multiple valid solutions. If two versions of a transitive dependency both satisfy all constraints, the resolver might pick either one depending on the order it processes the graph. Most mature tools have fixed this, but it's worth understanding why: deterministic resolution is not free, and not every solver was designed for it.

### Environment Contamination

The build machine itself is an input. This is the category most teams underestimate.

**Compiler and toolchain versions** are the obvious case. Compiling the same C code with GCC 12 and GCC 13 will produce different binaries even at the same optimization level, because the compiler's code generation changes between versions. The same source, different output, for reasons entirely outside your codebase.

**Environment variables** are the insidious case. Build scripts routinely inspect `PATH`, `HOME`, `LANG`, `LC_ALL`, `TZ`, and dozens of others. A build that runs under `LANG=en_US.UTF-8` may sort file listings differently than one running under `LANG=C`, and if that sort order affects which files get included in an archive first, the output changes. Locale-sensitive string comparison in build scripts is a real source of cross-machine non-determinism that is genuinely difficult to diagnose.

**Filesystem ordering** is the subtle case. When a build tool globs a directory — "compile all `.java` files in `src/`" — the order in which the filesystem returns entries is not guaranteed to be consistent across machines or even across runs on the same machine (depending on the filesystem). If that order affects the output — and it often does, because the order of class definitions in a combined output or the order of entries in an archive can change — then you've introduced non-determinism that no amount of dependency pinning will fix.

### Network Access During Builds

A build that makes network calls is non-deterministic by definition. The network is a shared mutable resource you don't control.

The most common case is downloading dependencies during the build rather than before it from a controlled cache. But there are subtler versions: build scripts that `curl` a configuration file, Dockerfile `RUN` commands that `apt-get update && apt-get install` (the contents of apt repositories change daily), builds that fetch protobuf schemas from a remote registry, or code generators that pull templates from a URL.

Any network call during a build introduces two problems. First, the content at the URL can change, so two builds from the same source produce different results. Second, the URL can become unreachable, so the build fails for reasons unrelated to your code. The combination means your build is both non-reproducible and fragile.

## How Hermetic Builds Actually Work

Hermeticity is the engineering response to all of the above. A hermetic build has exactly two properties: it uses only declared inputs, and it cannot observe the external environment.

**Bazel** achieves this through a combination of sandboxing and a content-addressable action graph. Each build action (compile this file, link these objects) runs in a sandbox where only its declared inputs are visible on the filesystem. The action cannot read `/usr/local/lib` unless it's been explicitly declared as an input. Actions are keyed by the hash of their inputs; if the inputs haven't changed, the output is reused from cache. This is why Bazel builds are reproducible and also why they're fast on incremental rebuilds — it's the same mechanism serving both purposes.

**Nix** takes a different approach: every dependency, including the compiler, the linker, the shell, and the coreutils, is stored in a content-addressed store (`/nix/store/<hash>-<name>`). A build derivation declares its complete dependency closure, and the build runs in an environment where only those store paths exist. There is no ambient `/usr/bin`. There is no system Python. If it's not in the closure, it doesn't exist.

**Docker-based builds** offer partial hermeticity. A Dockerfile pins the base image (if you use a digest rather than a tag), and the build runs inside that filesystem. But Docker builds are not hermetic by default — `RUN` instructions can access the network, and layer caching depends on instruction text rather than input content. A `COPY requirements.txt .` followed by `RUN pip install -r requirements.txt` will use the cached layer even if the *contents* of the packages at those versions have changed upstream.

The spectrum from "no reproducibility" to "bit-for-bit identical builds" looks roughly like this: unpinned dependencies with network access → pinned dependencies with lockfiles → containerized builds with pinned base images → fully sandboxed builds with content-addressed caching. Each step eliminates a class of undeclared inputs. Very few organizations reach the far end of that spectrum, and not all of them need to.

## Where Reproducibility Breaks Down in Practice

The most common failure mode isn't ignoring reproducibility — it's **believing you have it when you don't**. A team pins their npm dependencies, uses a Dockerfile, and assumes reproducibility is handled. Then six months later they rebuild an old commit to bisect a regression, and the resulting artifact behaves differently. The investigation reveals that the base Docker image was `node:18` (a floating tag that has been updated twelve times since), the `apt-get install` in the Dockerfile pulled different system library versions, and an environment variable set by the CI runner was changed during a platform migration.

This failure mode is uniquely damaging because it corrupts the debugging process. The entire point of rebuild-to-bisect is that you can trust the relationship between source code and behavior. If the build isn't reproducible, that relationship is broken, and you can spend days chasing a behavioral difference that isn't in your code at all.

The cost of hermeticity is real. Fully hermetic builds require that every tool, every library, and every system dependency is explicitly declared and versioned. This creates significant upfront configuration work and an ongoing maintenance burden. Bazel build files are verbose. Nix derivations have a steep learning curve. Vendoring all dependencies increases repository size. Sandboxed builds that can't access the network require pre-fetching every resource into a local store, which means building tooling to manage that store.

There's also a developer experience cost. Engineers accustomed to running `pip install whatever` and having it work are now confronted with a system that refuses to build unless `whatever` has been explicitly added to a dependency declaration, fetched into the local store, and hashed. This friction is the mechanism by which hermeticity works — it forces declaration of inputs — but it's friction nonetheless, and teams will route around it if the value isn't clearly understood.

The pragmatic tradeoff is that **functional reproducibility** (same source produces an artifact that behaves identically) is achievable and almost always sufficient, while **bit-for-bit reproducibility** (same source produces a byte-identical artifact) is much harder and only necessary in specific contexts like security-sensitive supply chains where you need third parties to verify a build's integrity.

## The Model to Carry Forward

Think of a build as a function. Reproducibility is the property that this function is pure — deterministic, with no side effects, and no hidden inputs. Hermeticity is the mechanism that enforces purity by restricting what the function can observe.

Every non-reproducibility bug you'll ever encounter reduces to the same root cause: an input to the build function that wasn't declared. Timestamps are undeclared time inputs. Floating dependency tags are undeclared version inputs. Network calls are undeclared external state inputs. Environment variables are undeclared configuration inputs. Once you internalize this framing, debugging reproducibility failures becomes a systematic process of identifying which undeclared input changed, rather than a frustrating search through an opaque build system.

The decision of *how hermetic* to make your builds is a cost-benefit question, not a purity test. The right answer depends on how much you need to trust the mapping between your commits and your artifacts, and how much you can afford to invest in build infrastructure. But the mental model is always the same: enumerate your inputs, declare your inputs, eliminate the ones you haven't declared.

## Key Takeaways

- **A build is a function whose reproducibility depends on declaring all of its inputs** — not just source code and dependencies, but the compiler, system libraries, environment variables, locale, timezone, and filesystem ordering.

- **Lockfiles are necessary but not sufficient**: they pin logical package versions but typically don't pin the physical content of those packages or any native/system-level dependencies.

- **Timestamps are the most common undeclared input** and they infiltrate builds through archive metadata, build tool output, compiler macros, and manifest fields — there is no single switch to disable them all.

- **Filesystem ordering and locale settings are real sources of cross-machine non-determinism** that are difficult to diagnose because they don't appear in any dependency manifest.

- **A Docker-based build is not hermetic by default**: floating base image tags, network-accessible `RUN` instructions, and instruction-text-based layer caching all undermine reproducibility.

- **The most damaging failure mode is false confidence** — teams that believe their builds are reproducible but have undeclared inputs will discover the gap only when they need reproducibility most, typically while debugging a production regression.

- **Functional reproducibility (identical behavior) is almost always sufficient**; bit-for-bit reproducibility (identical bytes) is much harder and only required when third-party verification of build integrity is a constraint.

- **The cost of hermeticity is real and ongoing**: verbose build declarations, dependency vendoring, developer friction, and tooling to manage pre-fetched resources — but this cost is the mechanism, not a side effect.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Builds are often treated as boring plumbing until the day you need to trust one. You check out an old commit to reproduce a production bug, rebuild it, and the binary behaves differently from what originally shipped. Or CI passes on one runner and fails on another. Or two engineers build “the same” source and get different artifacts, so caches miss, signatures change, and debugging turns into guesswork. Those are not abstract quality problems; they are direct consequences of hidden build inputs.

The reason this topic matters is that modern builds do much more than compile source. They read package registries, inspect the machine they run on, embed timestamps, pick up environment variables, and inherit system tools and libraries. If you do not have a model for those hidden inputs, you can believe your build is controlled when it is only partially controlled. That false confidence is worse than knowing you have randomness, because it breaks debugging, release traceability, and supply-chain trust exactly when you most need them.

---

## What You Need To Know First

### 1. Determinism
A process is deterministic if the same inputs always produce the same outputs. For builds, that means if you run the build twice with the same declared inputs, you should get the same result. If something outside those inputs can influence the result, the build is non-deterministic.

### 2. Dependency manifests vs lockfiles
A manifest says what you want in broad terms, like “I need library X, version compatible with 2.x.” A lockfile records the exact versions that were chosen, including transitive dependencies. The important distinction is: a manifest expresses intent, while a lockfile captures one concrete resolution of that intent.

### 3. Content hashes
A content hash is a fingerprint of bytes. If the bytes change, the hash changes. Build systems use hashes to decide whether an input or output is “the same.” This matters because version numbers alone do not guarantee identical content, but hashes do.

### 4. Sandboxing
Sandboxing means running a build step in a restricted environment where it can only see specific files, tools, and settings. The point is not security first; the point is control. If the action cannot see undeclared inputs, it cannot accidentally depend on them.

---

## The Key Ideas, Connected

### 1. A build is best understood as a function with many inputs.
The article’s core move is to stop thinking of a build as “compile the code” and start thinking of it as a function that transforms inputs into an artifact. Source code is one input, but so are compiler versions, system libraries, timestamps, locale, environment variables, file ordering, and network-fetched content. That framing matters because once you call something a function, you can ask the right question: have I actually identified all the inputs?

This leads directly to reproducibility, because reproducibility is just the statement that this function gives the same output for the same inputs. If outputs differ, either an input changed or you failed to notice one of the inputs.

### 2. Reproducibility is the property; hidden inputs are what destroy it.
A reproducible build means same inputs, same output, byte-for-byte if you are aiming for strict reproducibility. In practice, builds fail this test because they consume inputs that are real but undeclared. The article calls these implicit inputs. They are dangerous precisely because the build depends on them without making that dependence visible anywhere you manage.

Once you see that hidden inputs are the cause, the failures in later sections stop looking unrelated. Timestamps, floating package sources, locale differences, and network access are all the same class of problem: the build is observing state that is not part of the declared input set.

### 3. Time and metadata are common hidden inputs because tools capture them by default.
Many artifact formats preserve metadata from the filesystem or inject build-time information. A JAR is a ZIP file, and ZIP entries carry timestamps. Tar archives do similar things. Some compilers or build scripts write build dates directly into outputs. So even if your source and dependencies are unchanged, the clock alone can make artifacts differ.

This matters because it shows that non-determinism is often not a dramatic design mistake; it is default behavior in ordinary tools. That is why “just pin dependencies” is insufficient. Even with perfect package pinning, volatile metadata can still make outputs diverge.

### 4. Dependency pinning helps, but it only controls part of the input space.
A lockfile improves reproducibility because it turns “whatever satisfies this range today” into “these exact package versions.” That eliminates one source of drift. But lockfiles usually describe logical package identity, not every physical and environmental dependency involved in the build. If the registry allows the same version to point to different bytes, or if native libraries come from the host machine, your build can still change.

This is why integrity hashes and system dependency control matter. Once you understand the boundary of a lockfile, you see why teams get surprised: they pinned the application-level packages and assumed the problem was solved, while the actual build also depended on mutable tarballs, system OpenSSL, or host compilers.

### 5. The build environment itself is an input, even when nobody wrote it down.
Compilers differ by version. Environment variables affect scripts. Locale changes sort order. Timezone changes formatting. Filesystem directory iteration can return entries in different orders. These are all ways the machine leaks into the output. The build is not just running on a machine; it is reading from that machine as though the machine were part of the source.

This idea sets up hermeticity. If the environment is a hidden input source, then controlling builds means not merely documenting the machine but preventing the build from observing arbitrary parts of it.

### 6. Network access is just environment contamination at larger scale.
When a build can call out to the network, it depends on a mutable external system. A URL might return different bytes tomorrow. A package repository changes. A remote schema vanishes. So network access introduces both non-determinism and fragility: the same build may produce different outputs, or no output at all, for reasons unrelated to your repo.

This strengthens the case for a stricter mechanism. If undeclared inputs can come from the local machine and the wider network, then reproducibility requires actively blocking those observation paths, not just hoping they stay stable.

### 7. Hermeticity is the mechanism that blocks undeclared inputs.
The article draws an important distinction: reproducibility is the desired property, hermeticity is the enforcement mechanism. A hermetic build is one that can only use declared inputs and cannot observe the outside environment. That means no ambient system libraries, no undeclared tools from PATH, no surprise environment data, no casual network fetches.

This dependence matters mechanically: without hermeticity, reproducibility is mostly aspirational because the build still has access to hidden state. With hermeticity, undeclared inputs stop being possible, or at least become much harder. So hermeticity is not “extra purity”; it is how you make the build function actually behave like a function.

### 8. Systems like Bazel and Nix enforce hermeticity in different ways, but for the same reason.
Bazel constrains each action to declared inputs and keys actions by input content, so unchanged inputs can safely reuse cached outputs. Nix puts every dependency into a content-addressed store and constructs an environment from that exact closure, removing the ambient machine from the picture. Different implementation, same goal: if the action can only see declared, content-identified inputs, output stability becomes enforceable rather than assumed.

This also explains why reproducibility and cache efficiency often come together. If the system can precisely identify the complete input set, it can both guarantee correctness and know when previous outputs are safe to reuse.

### 9. Docker gives some control, but not hermeticity by default.
Docker helps because it packages a filesystem view and can pin a base image. But unless you pin by digest, block network access, and control package installation carefully, the container still sees mutable upstream state. `apt-get update` today is not `apt-get update` next month. Docker layer caching also works from instruction text and prior layers, not from a full semantic model of all fetched content.

This matters because many teams stop here. They containerize a build and mentally mark the problem solved. The article is warning that containers reduce some environmental variation, but they do not automatically eliminate hidden inputs.

### 10. The most damaging failure mode is false confidence.
The article argues that the worst case is not “we know our build is loose”; it is “we think our build is reproducible when it is not.” That belief corrupts debugging. If you rebuild an old commit to bisect behavior, you assume artifact differences come from source changes. But if the build itself drifted, the investigation starts from a false premise.

That leads to the practical endpoint: reproducibility is not an ideological goal, it is about how much you can trust the mapping from commit to artifact. Once you see that, the cost-benefit tradeoff makes sense. Not every team needs byte-identical builds, but every team benefits from knowing which inputs they control and which they are still leaving ambient.

### 11. The useful mental model is: every reproducibility bug is an undeclared input.
This is the unifying model the article wants you to keep. Instead of memorizing a catalog of weird build bugs, treat them all as one pattern. A timestamp is undeclared time. A floating Docker tag is undeclared image content. `PATH` is undeclared tool selection. `curl` in a build script is undeclared remote state.

That model is powerful because it gives you a debugging method. When a build differs unexpectedly, ask: what input changed that we failed to declare or isolate? That question turns a vague, frustrating problem into a systematic search.

---

## Handles and Anchors

### 1. “A build is a lab experiment, not a recipe.”
A recipe assumes the kitchen is mostly stable. A lab experiment assumes tiny environmental differences can change the result, so you control and record everything that matters. Reproducible builds are the lab mindset applied to software artifacts.

### 2. “Reproducibility is what you want; hermeticity is how you stop cheating.”
You can claim a build is reproducible, but if it can still read random host state or hit the network, it is effectively cheating. Hermeticity is how you force the build to show all the inputs it depends on.

### 3. Ask this question of any build system:
“What can this build observe that is not explicitly declared?”
If you can answer: the system clock, `/usr/bin`, CI environment variables, package registries, remote URLs, floating image tags — you have found your reproducibility risks.

---

## What This Changes When You Build

### 1. An engineer who understands this will treat build debugging as input debugging.
Instead of comparing only source diffs, they will compare toolchain versions, environment variables, image digests, lockfiles, timestamps, and network-fetched resources, because they know behavior can change without source changes. The unaware engineer defaults to “the code must be different,” and can lose days chasing a regression introduced by environment drift.

### 2. An engineer who understands this will pin more than package versions.
They will pin compiler versions, base images by digest, system packages, and where possible the hashes of fetched artifacts, because they know lockfiles only cover part of the dependency story. The unaware engineer pins `package-lock.json`, leaves `FROM node:18`, runs `apt-get install`, and inherits silent drift from upstream images and repositories.

### 3. An engineer who understands this will remove or normalize volatile metadata in artifacts.
They will audit archive creation, build manifests, compiler flags, and macros like `__DATE__` and `__TIME__`, because they know time leaks into outputs through many small defaults. The unaware engineer assumes “nothing changed” and is confused when two builds differ only because file mtimes or build timestamps were embedded.

### 4. An engineer who understands this will be suspicious of ambient machine state.
They will explicitly set locale, timezone, PATH, and relevant environment variables, and they will sort file lists before consuming them, because they know the host environment is a real input channel. The unaware engineer inherits whatever the CI runner or developer laptop provides, and gets flaky, hard-to-reproduce cross-machine build behavior.

### 5. An engineer who understands this will see network access during builds as a design choice, not a convenience.
They will prefetch dependencies into controlled caches or artifact stores and make build steps consume those declared resources, because they know every live fetch trades reproducibility for convenience. The unaware engineer writes build steps that download data at execution time, then discovers later that rebuilds depend on third-party uptime and mutable remote content.

</details>
