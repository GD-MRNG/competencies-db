## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers treat a version number like a label — a name tag that goes up by one when you ship something new. That mental model is fine until your build breaks at 2 AM because a transitive dependency four levels deep released a "patch" that changed a return type. The problem is not that semver failed. The problem is that the version number was never just a label. It is an input to an algorithm — one that your package manager runs to decide, without asking you, which exact code ends up in your build. Understanding semver means understanding that algorithm and the contract it depends on.

## What the Spec Actually Defines

The semver specification (semver.org) is short and worth reading in full, but its most important contribution is a concept most people skip past: the **public API**. Semver only has meaning relative to a declared public API surface. The MAJOR version increments when you make incompatible changes to that API. The MINOR version increments when you add functionality that is backward-compatible. The PATCH version increments when you make backward-compatible bug fixes. Without a defined API boundary, these categories are meaningless.

This matters in practice because "breaking change" is not self-evident. If a library changes the order of keys in a JSON response that was never part of its documented interface, is that breaking? According to semver, no. According to the three services that parsed that JSON positionally, absolutely. The spec puts the burden on the library author to define what the public API is and to classify changes against that boundary. This is a human judgment call, and it is where most semver problems originate.

### The 0.x Escape Hatch

The spec has a provision that is widely used and poorly understood: any version with a major version of **0** (e.g., `0.3.7`) signals that the public API is not stable. Under `0.x.y`, anything can change at any time. There are no backward-compatibility promises. The minor and patch numbers in a `0.x` version carry no semver guarantees whatsoever.

This matters because a staggering number of packages in every ecosystem live at `0.x` permanently. In npm, PyPI, and crates.io, many widely-used, production-critical libraries have never released a `1.0`. When you take a dependency on a `0.x` library, you are opting into a regime where the author has explicitly declined to make stability commitments. Package managers know this and treat `0.x` ranges differently — a point we will return to.

### Pre-release Versions and Build Metadata

The spec defines two additional segments. A **pre-release** version is denoted by a hyphen after the patch number: `2.0.0-alpha.1`, `3.1.0-rc.2`. Pre-release versions have lower precedence than the associated release — `2.0.0-alpha.1` sorts before `2.0.0`. This is how library authors publish candidate versions for testing without having them automatically pulled into consumer builds.

**Build metadata** is appended with a `+` sign: `1.0.0+build.42`. The spec is explicit that build metadata must be ignored when determining version precedence. Two versions that differ only in build metadata are equal. This segment exists purely for informational tracing; it plays no role in resolution.

## How Package Managers Resolve Versions

The version number is half the story. The other half is the **range specifier** — the syntax a consumer uses to express which versions they are willing to accept. This is where the human contract becomes a machine instruction.

### Range Specifiers Are Semver Assertions

When you write a dependency declaration, you are making an assertion about your own compatibility. Consider these npm-style specifiers:

```json
"lodash": "^4.17.0"
```

The `^` (caret) operator means: accept any version that is compatible according to semver, starting from this floor. For a version `>=1.0.0`, this means the major version is locked and the minor and patch can float. So `^4.17.0` resolves to `>=4.17.0 <5.0.0`. The caret is encoding a belief: "I depend on the public API of lodash 4, and any non-breaking release within major version 4 should work for me."

The `~` (tilde) operator is more conservative: it locks the minor version and lets only the patch float. `~4.17.0` resolves to `>=4.17.0 <4.18.0`. This encodes a narrower belief: "I trust bug fixes, but new features might affect me."

Here is the critical subtlety with `0.x` versions: `^0.2.3` does **not** resolve to `>=0.2.3 <1.0.0`. Because the spec treats `0.x` as unstable, most package managers treat the caret on a `0.x` version as pinning to the minor version: `^0.2.3` resolves to `>=0.2.3 <0.3.0`. The reasoning is that in the `0.x` regime, even minor bumps can be breaking. Different package managers handle this slightly differently — Cargo, npm, and Poetry all implement this contraction, but the exact boundary varies for `0.0.x` versions. If you depend on `0.x` libraries and do not understand this behavior, your range specifiers are not doing what you think.

### The Resolution Algorithm

When you run `npm install` or `pip install` or `cargo build`, the resolver must find a set of concrete versions — one per package — that satisfies every range constraint in your entire dependency tree simultaneously. This includes your direct dependencies and every transitive dependency they pull in.

The process works roughly as follows. The resolver starts with your declared dependencies and their range constraints. For each dependency, it queries the registry for all published versions that fall within the specified range. It picks a candidate (usually the highest matching version, though strategies vary). Then it examines that candidate's own declared dependencies, adds their constraints to the problem, and recurses. If at any point a constraint conflicts with an already-selected version, the resolver backtracks and tries a different candidate.

This is, in the general case, an NP-complete problem — it is equivalent to Boolean satisfiability (SAT). Modern resolvers use heuristics and caching to make it fast in practice, but the fundamental complexity means that resolution can fail in non-obvious ways, and small changes in the dependency graph can produce unexpectedly large changes in the resolved output.

### The Diamond Dependency Problem

The most common resolution pain point is the **diamond dependency**. Suppose your application depends on libraries A and B. Both A and B depend on library C, but A requires `^1.3.0` and B requires `^1.5.0`. The resolver can satisfy both: it picks C at `1.5.x` or higher (within `<2.0.0`), which falls within both ranges.

Now suppose B updates its constraint to `^2.0.0`. A still requires `^1.3.0`. The resolver cannot pick a single version of C that satisfies both constraints. In ecosystems that allow only one version of a package (Python, Go), this is a hard failure — the build does not resolve. In ecosystems that allow multiple versions of the same package (npm for Node.js), the resolver can install both C@1.x and C@2.x in different subtrees of `node_modules`. This "solves" the resolution problem but introduces a new one: if A and B pass objects from C to each other, those objects come from different versions of C and may be incompatible at runtime, producing errors that no type checker or linter will catch.

## Where Semver Breaks Down

### The Contract Is Social, Not Technical

Nothing in the publishing pipeline of any major registry verifies that a version bump correctly classifies the nature of the change. An author can ship a breaking change as a patch. They usually do not do this maliciously — they do it because determining whether a change is breaking requires understanding every way consumers use the public API, which is impossible at scale.

**Hyrum's Law** captures this precisely: with a sufficient number of users, every observable behavior of your system will be depended upon by somebody. You change the order of items in an unordered collection — technically not a public API change — and someone's test suite, or worse, their production system, breaks. Semver gives authors a framework for communicating intent, but it cannot guarantee impact.

### Wide Ranges Trade Stability for Freshness

The caret operator is the default in most ecosystems because it maximizes the chance that security patches and bug fixes flow into builds automatically. The cost is non-determinism across time: running `npm install` today and next Tuesday may produce different `node_modules` trees. Lock files exist specifically to counteract this — they freeze the resolved output. But lock files only help when they are used correctly. Libraries (as opposed to applications) typically do not publish their lock files, meaning the resolution for a library's own dependencies happens fresh at install time in the consumer's context.

This creates a category of bug that is notoriously hard to reproduce: your CI passes because the lock file is committed, but a fresh install on a new machine pulls a slightly different transitive dependency and fails. Or worse, it succeeds but behaves differently.

### Major Version Increments Create Ecosystem-Wide Friction

Bumping the major version is the correct thing to do when you make a breaking change. But it is also expensive for the entire ecosystem. Every consumer must update their code and release a new version with an updated constraint. Their consumers must then update, and so on up the graph. In practice, this means major version bumps of widely-used libraries create long periods where different parts of the ecosystem are pinned to different major versions, producing diamond dependency conflicts.

This is why many library authors avoid major version bumps for as long as possible, accumulating deprecation warnings instead of breaking changes. It is also why some ecosystems (notably Go) have adopted conventions where a major version bump results in a new import path (`github.com/user/lib/v2`), treating the new major version as an entirely separate package. This sidesteps the diamond problem but at the cost of duplicating the dependency in the graph.

## The Mental Model

A version number is a lossy compression. It takes an arbitrarily complex set of code changes and encodes them into three integers and a promise. The major number says "I changed the contract." The minor number says "I extended the contract." The patch number says "I upheld the contract more faithfully." But the accuracy of that encoding depends entirely on the author's diligence and judgment.

The system works not because it is enforceable, but because package managers treat it as ground truth. Every caret, every tilde, every resolution decision is predicated on the assumption that authors classify their changes correctly. When you write `^2.4.0`, you are not just expressing a version preference — you are delegating a trust decision to every maintainer in your transitive dependency tree. Understanding this lets you reason clearly about when to trust that delegation (mature, well-maintained libraries with strong API discipline), when to constrain it (tilde ranges, exact pins), and when to verify it (lock files, CI-time dependency auditing).

## Key Takeaways

- **Semver is a protocol, not a label.** Package managers algorithmically consume version numbers to make resolution decisions — the number is a machine-readable input, not just a human-readable tag.

- **The `^` operator on `0.x` versions behaves differently than on `1.x+` versions.** Most resolvers contract the range to pin the minor version under `0.x`, because the spec treats the entire `0.x` range as unstable.

- **Dependency resolution is a constraint satisfaction problem across your entire transitive graph.** A single incompatible range constraint anywhere in that graph can break resolution, and small changes can cascade into large shifts in the resolved output.

- **Diamond dependency conflicts are the most common practical failure mode of semver.** They occur when two dependencies require incompatible version ranges of a shared transitive dependency, and they get worse with every major version bump of a widely-used library.

- **Hyrum's Law means that any observable behavior change can be breaking in practice, regardless of how the author classifies it.** Semver communicates intent, not verified impact.

- **Lock files freeze resolution output, but only for the context that generated them.** Libraries do not ship lock files, so their transitive dependencies resolve fresh in the consumer's build — a common source of "works on my machine" bugs.

- **Wide version ranges optimize for receiving patches at the cost of determinism; narrow ranges optimize for stability at the cost of missing fixes.** The right choice depends on how much you trust the upstream maintainer's semver discipline and how sensitive your system is to unexpected changes.

- **A major version bump is semantically correct for breaking changes but creates real ecosystem cost.** It forces a cascade of updates through every consumer in the dependency graph, which is why authors defer it and why some ecosystems treat new major versions as separate packages entirely.


# Discussion

## Why This Conversation Is Happening

Dependency management stops being a clerical task the moment your build output depends on code you did not choose explicitly. You declare a few direct dependencies, but your package manager pulls in dozens or hundreds of transitive ones, and version numbers determine which exact code lands in your build. If you think semver is just naming, you miss the real mechanism: version numbers and range specifiers drive an automated selection process.

When engineers do not understand that mechanism, they make confident but false assumptions. They write `^` thinking “safe updates,” then get a runtime break from a supposedly non-breaking release. They depend on `0.x` packages as if they were stable. They see a lock file and assume builds are reproducible everywhere, even when transitive resolution still changes in fresh contexts. The result is familiar: irreproducible installs, dependency conflicts, surprise breakages, and long debugging sessions caused by code nobody touched directly.

Semver matters because it is one of the main trust interfaces in modern software supply chains. If you do not understand what promises it makes, what promises it does not make, and how resolvers consume it, you are outsourcing production behavior to conventions you cannot reason about under failure.

---

## What You Need To Know First

### Dependency tree
Your application depends on packages, and those packages depend on other packages, forming a tree or graph. Your “real” software is not just your direct dependencies; it is the whole transitive set. This matters because semver and resolution operate across that full graph, not package-by-package in isolation.

### Public API
A public API is the part of a library that consumers are meant to rely on: exported functions, documented behaviors, accepted inputs, output formats, and sometimes CLI flags or wire formats. Semver only makes sense relative to this boundary. Without a defined public API, you cannot meaningfully say whether a change is breaking, additive, or just a bug fix.

### Version range
A version range is not a single version; it is a rule saying which versions are acceptable. `^1.2.3` and `~1.2.3` are examples. The package manager reads those rules and picks concrete versions that satisfy them, so the range is really an instruction to the resolver.

### Lock file
A lock file records the exact versions chosen during one successful resolution. Its purpose is to make repeated installs produce the same dependency set. It improves determinism, but only for the environment and dependency context where it was generated; it does not magically make all downstream installs identical forever.

---

## The Key Ideas, Connected

### Semver is not just a label; it is input to a resolver.
A version number matters because package managers use it to decide what code to install.

If version numbers were only human-readable tags, mistakes would be mostly social. But they are consumed by tooling. The resolver compares available versions against constraints and picks concrete packages for your build. That means semver affects behavior mechanically: the numbers influence installation outcome, not just communication.

Once you see version numbers as machine input, the next question becomes: input to what contract? That leads directly to the public API, because semver categories only make sense if there is a defined boundary for what counts as compatibility.

### Semver only has meaning relative to a public API.
“Major,” “minor,” and “patch” describe changes to a declared interface, not changes to code in general.

A breaking change is not “anything different in the repo.” It is a change that invalidates assumptions consumers are supposed to be allowed to make. A minor release adds new compatible behavior. A patch fixes behavior without invalidating existing use. If the author has not defined what users are allowed to rely on, these categories become fuzzy and inconsistent.

That fuzziness matters because package managers act as though the classification is meaningful. So the next step is understanding the exact promises semver encodes when the API is considered stable—and what changes when it is not.

### `1.x+` semver encodes stability promises, but `0.x` explicitly does not.
A package in `0.x` is saying “do not assume stable compatibility guarantees yet.”

For `1.2.3`, semver says patch bumps preserve compatibility, minor bumps add compatible functionality, and major bumps can break consumers. But `0.2.3` is different: the spec treats the API as unstable, so even small-looking bumps may contain breaking changes. This is not just a cultural vibe; package managers usually narrow their interpretation of version ranges under `0.x` because they assume less compatibility.

That creates the need to understand range specifiers, because the same symbol like `^` means “trust semver compatibility” — and that trust is reduced under `0.x`.

### A version range is a compatibility claim you make to the resolver.
When you write `^4.17.0`, you are saying “any semver-compatible release in this line should work for me.”

This is easy to miss. A dependency declaration is not only a request for some package; it is an assertion about what future versions your code can tolerate. `^4.17.0` usually means “anything from 4.17.0 up to but not including 5.0.0.” `~4.17.0` means “stay within 4.17.x.” Those are different risk postures. The wider the range, the more future change you are permitting without review.

Under `0.x`, the same claim becomes weaker because the package itself has declined to promise stability. So `^0.2.3` is commonly treated more like “stay within 0.2.x,” not “anything until 1.0.” That leads to the next key idea: these range rules do not apply one package at a time. They are solved across the whole graph simultaneously.

### Dependency resolution is a constraint-solving problem over the entire graph.
The resolver must find one concrete set of package versions that satisfies all declared ranges at once.

Your app may allow one version of package C, dependency A may allow another range for C, and dependency B may allow yet another. The resolver walks the graph, gathers constraints, chooses candidate versions, and backtracks when choices conflict. This is why a tiny change in one dependency can alter the final resolved tree much more than you expect: the solver is searching for a globally valid combination, not making isolated local choices.

Once version selection is understood as a graph-wide constraint problem, the most common practical failure mode becomes easier to see: multiple parts of the graph wanting incompatible versions of the same package.

### Diamond dependencies are where semver pain becomes visible.
A diamond dependency happens when two dependencies both rely on the same transitive package but require incompatible version ranges.

If A and B both depend on C, and their allowed ranges overlap, the resolver can pick one C version that satisfies both. If A needs C `^1.x` and B needs C `^2.x`, that overlap disappears. In ecosystems that require a single version, resolution fails. In ecosystems that allow duplicates, both may be installed separately—but then values crossing those boundaries can be incompatible at runtime.

The mechanism is important: the break is not random. It comes from the resolver trying to satisfy two contradictory compatibility claims. And that exposes the deeper weakness beneath the whole system: semver works only if the compatibility claims are accurate.

### Semver is a social contract enforced by trust, not by verification.
Nothing automatically proves that a patch release is truly non-breaking.

Registries do not inspect the meaning of a code change and verify that the version bump was correct. Authors make judgment calls. Sometimes they are careful and right; sometimes they overlook an observable behavior consumers depend on. That is where Hyrum’s Law matters: if behavior can be observed, some users will rely on it, whether or not the author intended it as public API.

So even when the resolver behaves perfectly, the inputs it consumes may still be wrong. That leads to the operational tradeoff engineers actually live with: do you allow fresh compatible versions to flow in automatically, or do you freeze exact results?

### Wide ranges optimize for freshness; locks optimize for determinism.
Allowing floating versions gets you newer fixes automatically, while lock files preserve the exact set that worked before.

If you use wide ranges like caret dependencies, a fresh install next week may resolve to different versions than a fresh install today. That can bring in security fixes and bug fixes without manual intervention, but it also means your build output changes over time. Lock files counter this by recording exact chosen versions, making repeated installs deterministic.

But lock files do not remove semver dynamics everywhere. They mainly freeze one resolution result for one project context. Libraries often do not pass that frozen world on to consumers, so their dependencies can still resolve differently downstream. That is why “it passed in CI” and “it failed on a fresh machine” can both be true without contradiction.

Once you understand that, the final mental model becomes clear: semver is a compression of change into a promise the tooling treats as truth.

### A version number is compressed change plus a promise.
Semver reduces many code changes into a short signal that package managers trust when making installation decisions.

Major means “the contract changed incompatibly.” Minor means “the contract expanded compatibly.” Patch means “the contract was preserved while behavior was corrected.” But that encoding is lossy because real software behavior is richer than three integers. The package manager cannot inspect intent; it only sees the numbers and the ranges.

That is why semver understanding is really trust management. Every version range says how much you are willing to trust upstream maintainers, across your whole transitive graph, to classify changes correctly and preserve the behaviors your system depends on.

---

## Handles and Anchors

### 1. Semver is a traffic signal for a robot, not a label for a human.
The important question is not “what does this version call itself?” but “what will the package manager do when it sees this version?” That framing keeps attention on resolution behavior, not naming.

### 2. A dependency range is a delegated trust decision.
When you write `^2.4.0`, you are saying: “I permit future releases from maintainers I may never meet to enter my build without review, as long as they label them non-breaking.” That sentence captures the real risk.

### 3. Ask: “What behavior am I trusting, and who said it was stable?”
This is a useful test for any dependency. If the relied-on behavior is undocumented, or the package is still `0.x`, or the maintainer has weak release discipline, then a wide range means more risk than you may think.

---

## What This Changes When You Build

- An engineer who understands this will choose dependency ranges differently because range syntax is a risk policy, not just convenience. They may use `^` for mature libraries with strong API discipline, `~` for dependencies with shakier release history, and exact pins for brittle infrastructure code. The unaware engineer inherits the ecosystem default, often caret ranges everywhere, and then acts surprised when “non-breaking” upstream changes alter production behavior.

- An engineer who understands this will treat `0.x` dependencies as unstable by default because semver promises are intentionally weaker there. They will review upgrades more carefully, avoid broad assumptions about compatibility, and check how their package manager interprets `^0.x`. The unaware engineer sees `^0.2.3` and assumes it behaves like `^2.3.0`, then misreads what updates are actually allowed.

- An engineer who understands this will debug dependency issues at the graph level because failures often come from transitive constraints, not the package they just changed. When a build suddenly breaks, they inspect the lock diff, resolved tree, and shared transitive dependencies. The unaware engineer keeps staring at direct dependencies and misses that a package four levels down changed under a permissive range.

- An engineer who understands this will distinguish application dependency management from library dependency management because lock files help them differently. For an application, committing and controlling the lock file can make builds reproducible. For a library, consumers re-resolve transitive dependencies in their own environment, so compatibility has to survive fresh resolution. The unaware engineer assumes “it works in my repo with my lock file” proves the library is broadly safe to publish.

- An engineer who understands this will see major version bumps as ecosystem events, not just local housekeeping, because a major bump can create widespread diamond conflicts and delayed adoption across downstream users. They will plan migrations, compatibility windows, and deprecation paths accordingly. The unaware engineer ships a clean semver-major release and is confused when the ecosystem fragments around old and new majors for months or years.
