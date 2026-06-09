## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers frame this as a simple binary: pin your dependencies for safety, or use ranges for convenience. That framing is wrong, and it leads to policies that feel rigorous but quietly rot. The real question is not *whether* to pin or use ranges — it is understanding what your package manager actually does when it encounters either strategy, how version resolution compounds across a dependency graph, and why the cost of both approaches is invisible until it becomes an emergency. The mechanics underneath this decision are what determine whether your system is reproducible, updatable, or slowly becoming neither.

## What Version Resolution Actually Does

When you declare a dependency, you are not selecting a version. You are expressing a **constraint**. Your package manager collects constraints from every package in your dependency tree and feeds them into a **resolver** — an algorithm that finds a set of concrete versions satisfying all constraints simultaneously, or fails if no such set exists.

Consider a `package.json` with:

```json
{
  "dependencies": {
    "library-a": "^2.3.0",
    "library-b": "^1.1.0"
  }
}
```

This looks like two decisions, but it is the start of a constraint satisfaction problem. `library-a@2.5.1` might depend on `shared-util@^3.2.0`, while `library-b@1.4.0` might depend on `shared-util@^3.0.0`. The resolver must find a single version of `shared-util` that satisfies both ranges. If `library-a` updates to require `shared-util@^4.0.0` while `library-b` still requires `^3.0.0`, no solution exists. Your build breaks — not because of anything you changed, but because of an incompatibility between your transitive dependencies.

This is the first non-obvious mechanic: **your dependency policy governs your direct dependencies, but the resolver operates on the entire graph.** You control perhaps ten to thirty direct dependencies. The resolved tree might contain hundreds or thousands of packages. The constraints those transitive packages declare are outside your control, and the resolver must satisfy all of them simultaneously.

Different ecosystems handle resolution differently. npm installs a tree structure where multiple versions of the same package can coexist (library-a gets its `shared-util@4.1.0` and library-b gets its `shared-util@3.8.0`). pip, by contrast, installs into a flat namespace — only one version of any package can exist, so conflicts are hard failures. Go modules use **minimum version selection**, always choosing the lowest version that satisfies all constraints, which inverts the usual "give me the latest compatible version" behavior. These are not implementation details you can ignore. They determine what "using a range" actually means in your ecosystem.

## The Manifest vs. the Lock File

Two files govern your dependencies, and confusing their roles is the root of most reproducibility problems.

The **manifest** (`package.json`, `Pipfile`, `Cargo.toml`, `go.mod`) declares your intent: which packages you want and what version constraints you accept. The **lock file** (`package-lock.json`, `Pipfile.lock`, `Cargo.lock`, `go.sum`) records the output of resolution: the exact version of every package — direct and transitive — that the resolver selected.

When you run `npm install` on a project with no lock file, the resolver reads the manifest, solves the constraint problem against the current state of the registry, and writes both a `node_modules` directory and a lock file. When you run `npm install` with a lock file present, the resolver skips the solving step entirely and installs exactly what the lock file specifies — *unless* the manifest has changed in a way that invalidates the lock file.

This means that the lock file is the actual source of reproducibility, not the manifest. A manifest with `"lodash": "^4.17.0"` is compatible with hundreds of resolved versions. The lock file picks one. If your CI pipeline regenerates the lock file from scratch on every build instead of consuming the committed lock file, you have ranges with extra steps — not pinning.

Here is the subtlety that catches people: **the manifest governs what the resolver is allowed to choose, the lock file records what it chose, and the distinction between "pinning" and "ranges" lives in the manifest.** When someone says they "pin dependencies," they usually mean one of two things, and the difference matters enormously. They might mean they use exact versions in the manifest (`"lodash": "4.17.21"`), which constrains the resolver to a single choice for that direct dependency. Or they might mean they commit a lock file, which freezes the entire resolved tree regardless of what the manifest says. These are different strategies with different update behaviors.

## Direct Dependencies vs. Transitive Dependencies

Pinning your direct dependencies does not pin your transitive dependencies. If your manifest says `"express": "4.18.2"` (exact), you have locked the version of Express. But Express depends on dozens of packages, each with their own declared ranges. The first time you resolve — or any time you delete your lock file and re-resolve — the transitive tree beneath Express can change.

This is where the two strategies interact. If you pin direct dependencies in the manifest *and* commit the lock file, you get full reproducibility. If you pin direct dependencies in the manifest but do not commit the lock file (common in library development, where lock files are often gitignored), you have controlled only the surface. The packages three levels deep in your tree can still shift between builds.

Conversely, if you use ranges in the manifest but commit the lock file, you get reproducibility that is easy to update — running `npm update` or equivalent will re-resolve within the constraints and write a new lock file that you can review, test, and commit. This is the strategy most ecosystem maintainers recommend, and it is the one most teams think they are following. The gap between thinking you follow it and actually following it is where breakage lives.

## How Freshness Decays

A fully pinned, locked dependency tree is a snapshot. On day one, that snapshot is current — every package is at or near its latest version, all known vulnerabilities are patched. Over time, the snapshot ages. New vulnerabilities are discovered. New versions are released. Some of those new versions contain security fixes. Some contain breaking changes.

The cost of updating is roughly proportional to how far behind you are. Updating one package from `3.2.1` to `3.2.4` is almost always trivial. Updating from `3.2.1` to `3.9.0` might require adjusting to new behaviors. Updating from `3.2.1` to `5.0.0` might require rewriting integration code. And because dependencies constrain each other, updating one package deep in the tree can force cascading updates to packages that depend on it.

This creates the **update cliff** — the phenomenon where a team pins everything, ignores updates for months, then faces a security advisory that forces an update. The vulnerable package is three major versions behind. Updating it breaks compatibility with two other packages that also need to be updated. Those updates surface new deprecation warnings in your code. What should have been a patch-level bump becomes a multi-day project.

The update cliff is the primary failure mode of aggressive pinning, and it is invisible until you hit it. Nothing in your CI pipeline warns you that your dependency tree is gradually becoming unmaintainable. Everything is green. Builds are reproducible. And the cost of your next update is growing every day.

## The Failure Modes That Actually Happen

**Phantom breakage from ranges without lock files.** A team uses ranges in their manifest, does not commit the lock file, and runs `pip install -r requirements.txt` (with `>=` style ranges) in CI. Monday's build works. Tuesday's build fails. Nothing in the repository changed. A transitive dependency released a minor version that changed behavior in a way semantic versioning says should not happen — but did. The team spends hours bisecting their own code before realizing the problem is external. This is the most common argument for pinning, and it is valid.

**Vulnerability accumulation from pinning without update discipline.** A team pins every dependency and commits the lock file. Six months later, a CVE is published against a transitive dependency four levels deep. The fix requires updating the transitive dependency, which requires updating its parent, which requires updating a direct dependency across a major version boundary. The team patches the vulnerability manually (if they can), forks the dependency (if they are desperate), or accepts the risk (if they do not understand it).

**Lock file drift in monorepos and multi-service setups.** Service A and Service B share a library. Each has its own lock file. Service A updates the library; Service B does not. The shared library now behaves differently in each service. Integration tests pass in isolation. Production breaks at the boundary. The lock files are individually correct and collectively inconsistent.

**False reproducibility from misunderstanding lock file scope.** A team commits their lock file but runs `npm ci` on some pipelines and `npm install` on others. `npm ci` faithfully installs from the lock file. `npm install` may update it. The artifact built by the "install" pipeline subtly differs from the one tested by the "ci" pipeline. The build is reproducible in theory and non-deterministic in practice.

## The Policy Space Between the Extremes

The practical solution is neither "pin everything" nor "range everything." It is a combination: use ranges in the manifest for direct dependencies (typically caret or tilde ranges that allow patch and minor updates), commit the lock file for reproducibility, and run automated update tooling (Dependabot, Renovate, or equivalent) on a cadence that keeps the update delta small.

This combination gives you reproducible builds (from the lock file), controlled flexibility (from the ranges), and small update increments (from the automation). The lock file is the artifact of truth. The ranges define the search space for updates. The automation ensures the search space is explored regularly rather than in a panic.

The key nuance: this only works if your CI pipeline installs from the lock file in all paths, if the update PRs are actually reviewed and merged, and if your test suite is comprehensive enough to catch behavioral changes in dependencies. Automated update tooling that produces PRs nobody merges is the same as not having it.

## The Mental Model

Think of your dependency tree as a snapshot of the ecosystem at a point in time. The manifest is a set of constraints that defines a *region* of valid snapshots. The lock file is a specific point within that region. Pinning narrows the region; ranges widen it. But the region only matters at resolution time — the moment the resolver runs and selects a concrete point.

Reproducibility comes from controlling when and how that resolution happens. If you re-resolve on every build, you are at the mercy of the ecosystem's rate of change. If you never re-resolve, you are at the mercy of the ecosystem's vulnerability disclosure rate. The engineering task is not choosing one extreme but choosing the resolution cadence — how often you take a new snapshot, and how much of the tree you allow to change when you do.

The tradeoff is not pinning vs. ranges. It is **resolution frequency vs. update cost per resolution.** Resolve often and each update is small. Resolve rarely and each update is large. The right frequency depends on your risk tolerance, your test coverage, and your team's capacity to review dependency changes — not on a universal best practice.

## Key Takeaways

- Version resolution is a constraint satisfaction problem across your entire dependency graph, not a lookup against a flat list of packages you declared.
- The manifest expresses constraints; the lock file records the resolved result. Reproducibility comes from the lock file, not from pinning versions in the manifest.
- Pinning direct dependencies does not pin transitive dependencies — only a committed lock file freezes the full tree.
- The cost of updating a dependency is roughly proportional to how far behind you are, which means deferred updates compound into increasingly expensive and risky changes.
- Automated update tooling (Dependabot, Renovate) works only if the PRs it produces are actually merged on a regular cadence and validated by meaningful tests.
- Different ecosystems resolve differently: npm allows duplicate versions in a tree, pip requires a flat namespace, Go uses minimum version selection. Your pinning strategy must account for your resolver's behavior.
- The most common reproducibility failure is not choosing the wrong policy but applying the right policy inconsistently — mixing `install` and `ci` commands, regenerating lock files in some pipelines, or gitignoring lock files in applications.
- The real tradeoff is resolution frequency vs. update cost per resolution: resolve often and each change is small, resolve rarely and each change is a project.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Dependency policy often gets discussed as if it were just style: “do we pin versions or use ranges?” But production systems do not experience that choice as style. They experience it as builds that suddenly stop working, security fixes that turn into emergency migrations, and services that behave differently even though “nothing changed in our code.” The pain comes from misunderstanding what the package manager is actually doing underneath your manifest.

When engineers do not have a working model of resolution, they usually make one of two bad assumptions. Either they think exact versions in the manifest guarantee reproducibility, when transitive dependencies can still drift, or they think a committed lock file solves everything, while some pipelines quietly re-resolve anyway. That is how teams end up debugging phantom breakages caused by dependency churn, or discovering too late that their “safe” pinned tree has fossilized into a costly update cliff.

---

## What You Need To Know First

**1. Dependency graph**  
Your app depends on packages, and those packages depend on other packages, and so on. That creates a graph or tree of dependencies. The packages you list yourself are **direct dependencies**; the ones pulled in underneath are **transitive dependencies**. Most of the packages that actually get installed are transitive, not direct.

**2. Version constraints**  
A version string in a manifest is usually not “install exactly this” but “anything in this allowed range.” For example, `^2.3.0` usually means “2.x versions at or above 2.3.0, but not 3.0.0.” Exact versions and ranges are both forms of constraints; they just leave different amounts of choice to the resolver.

**3. Semantic versioning**  
Many ecosystems assume versions are structured as `major.minor.patch`. The rough convention is: patch = bug fixes, minor = backward-compatible features, major = breaking changes. This convention helps package managers decide what counts as “compatible,” but it is only a convention. Real packages sometimes violate it, which is why “allowed by semver” does not always mean “safe in practice.”

**4. Lock file**  
A lock file records the exact versions that were selected for a dependency tree at one point in time. Think of it as the frozen output of dependency resolution. If the manifest says what you are willing to accept, the lock file says what you actually got.

---

## The Key Ideas, Connected

**1. Declaring a dependency is expressing a constraint, not choosing a concrete package version.**  
When you write `"library-a": "^2.3.0"`, you have not picked one version; you have given the package manager a permitted range. Even `"2.3.0"` is still just one constraint among many, because the full install also has to satisfy everything that `library-a` depends on. So the moment you declare dependencies, you are not building a list—you are defining a search space.

That matters because the next step is not “download these versions,” but “find a set of versions that all fit together.”

**2. The resolver solves that constraint problem across the entire dependency graph.**  
The package manager gathers constraints from your direct dependencies and all the transitive ones beneath them. Then it tries to choose concrete versions that satisfy all of them simultaneously. If two packages need incompatible versions of the same shared dependency, resolution either fails or works around it according to the ecosystem’s rules.

This is why your dependency policy has effects beyond the few lines in your manifest. You directly control a small surface area, but the resolver is operating over a much larger graph. Once you see that, it becomes obvious why “I only changed one package” can still produce a large or surprising tree change.

**3. What “using ranges” means depends on how your ecosystem resolves conflicts.**  
In npm-style tree installs, different branches can sometimes keep different versions of the same package. In pip’s flat environment, only one version can exist, so conflicts are stricter. In Go’s minimum version selection, resolution prefers the lowest version satisfying constraints rather than the newest compatible one.

This leads directly to an important practical point: a dependency policy is not portable across ecosystems. “Use ranges” in npm does not behave like “use ranges” in pip. So if you do not know your resolver’s conflict model, you do not actually know the consequences of your manifest choices.

**4. The manifest and the lock file do different jobs.**  
The manifest declares intent: what packages you want and what version space is acceptable. The lock file records a specific resolved result: every exact direct and transitive version that the resolver selected. The manifest defines the allowable region; the lock file marks one exact point inside it.

This distinction matters because engineers often assign reproducibility to the wrong file. The manifest may limit what can happen, but the lock file captures what did happen. That is what the next idea depends on.

**5. Reproducibility comes from the lock file, not from version ranges or exact pins in the manifest alone.**  
If two builds consume the same lock file, they install the same resolved tree. If two builds independently resolve from the same manifest without a shared lock file, they may get different answers because the registry has changed, transitive packages have released updates, or metadata has shifted. Exact versions in the manifest only lock your direct dependency choices; they do not freeze the entire transitive world beneath them.

That is why “we pinned our dependencies” is often a false sense of safety. The real question is: did you freeze the resolved graph, and do all build paths actually use that frozen graph?

**6. Pinning direct dependencies does not pin transitive dependencies.**  
Suppose you specify `express: "4.18.2"` exactly. That guarantees the version of Express itself. But Express still depends on many other packages using its own ranges. Without a lock file, a fresh resolution can produce a different set of transitive versions under the same exact Express version. So you have stabilized the top layer while leaving the rest of the graph free to move.

Once you understand that, the false binary starts to collapse. Exact versions in the manifest and committed lock files are not substitutes; they control different layers of the problem.

**7. A locked dependency tree is reproducible, but it naturally gets older over time.**  
The lock file gives you a snapshot of the ecosystem at the moment resolution ran. That is valuable because builds become deterministic. But snapshots age. New releases appear, vulnerabilities are disclosed, and compatibility expectations drift. The lock file protects you from surprise today by preserving yesterday.

That creates the next tradeoff: the thing that gives stability now also creates distance from the current ecosystem later.

**8. Update cost grows with the amount of time since the last meaningful resolution.**  
If you update regularly, each re-resolution usually changes a small number of packages by a small amount. Those changes are easier to review, test, and understand. If you defer updates for months, the resolver may need to jump across many package releases and major-version boundaries. Dependencies may force one another forward, so one required fix can cascade into several coordinated upgrades.

This is the mechanism behind the “update cliff.” The cliff is not magic; it is accumulated version distance plus graph coupling. Small missed updates compound until one security advisory or build failure forces you to pay all the deferred integration cost at once.

**9. The practical tradeoff is not pinning versus ranges; it is when and how often you re-resolve.**  
If you re-resolve constantly without controlling the result, you risk phantom breakage from ecosystem churn. If you never re-resolve, you accumulate stale dependencies and expensive updates. The actual engineering decision is cadence: how frequently you take a new snapshot, how much change you allow each time, and whether your process catches breakage before production.

That is why the common practical pattern is: ranges in the manifest, committed lock file, and regular automated update PRs. The ranges define what movement is allowed, the lock file freezes a tested snapshot, and the update cadence keeps the jump size small.

**10. Dependency policy only works if your tooling and pipelines apply it consistently.**  
A correct-looking policy can still fail in practice if some jobs use the lock file and others regenerate it, if one team commits lock files and another ignores them, or if update PRs are generated but never merged. In that case, the written policy says “reproducible and maintainable,” but the actual system says “partially deterministic and slowly decaying.”

So the final lesson is that dependency management is operational, not just declarative. Your real policy is the combination of manifest rules, resolver behavior, lock-file handling, CI commands, and update cadence.

---

## Handles and Anchors

**1. The manifest is a menu; the lock file is the receipt.**  
The menu says what choices are allowed. The receipt records exactly what was chosen that time. If you want the same meal again, the receipt is what matters.

**2. A lock file is a snapshot, and snapshots age.**  
A snapshot gives clarity and repeatability, but it is frozen in time. The longer you wait to take the next one, the bigger the difference becomes.

**3. Ask this question of any system: “When does resolution happen, and who controls that moment?”**  
That question exposes most dependency problems. If resolution happens implicitly during every build, you are exposed to ecosystem churn. If it happens only during deliberate updates, you control change but must maintain update discipline.

---

## What This Changes When You Build

**An engineer who understands this will treat the lock file as a production artifact, not as generated noise, because reproducibility depends on the resolved graph, not just on direct dependency declarations.**  
The unaware engineer often commits `package.json` changes casually while allowing CI or local installs to rewrite the lock file inconsistently, or ignores the lock file entirely. The consequence is “works on my machine” builds that differ across environments for reasons hidden in transitive dependencies.

**An engineer who understands this will choose install commands differently because `install from lock` and `resolve then install` are materially different operations.**  
For example, they will prefer `npm ci` in CI when the goal is reproducible builds, because it consumes the lock file rather than opportunistically updating it. The unaware engineer mixes `npm install` and `npm ci` across pipelines and quietly ends up testing one tree while deploying another.

**An engineer who understands this will not mistake exact direct versions for full dependency control, because transitive dependencies can still drift without a committed lock file.**  
So when building an application, they will commit and enforce the lock file rather than assuming manifest pinning is sufficient. The unaware engineer pins top-level versions, skips lock discipline, and is surprised when a clean install changes behavior.

**An engineer who understands this will design dependency update work as a recurring maintenance loop, not a rare cleanup task, because update cost compounds with age.**  
They are more likely to enable Renovate or Dependabot, review small dependency PRs weekly, and keep tests strong enough to validate those changes. The unaware engineer lets updates pile up because nothing is visibly broken, then hits a CVE or ecosystem change that turns routine maintenance into a risky migration project.

**An engineer who understands this will adapt policy to the ecosystem’s resolver behavior because conflict handling differs across package managers.**  
In npm they may accept some duplicate transitive versions as normal; in pip they will be more cautious because a single-version environment means conflicts fail hard. The unaware engineer ports a dependency strategy from one ecosystem to another and gets surprising failures because the underlying resolution mechanics are different, even if the vocabulary sounds the same.

</details>
