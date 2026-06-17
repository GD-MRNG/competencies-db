# Git — Level 0: Course Map

> **Intent:** Git is the substrate almost every modern engineering workflow sits on top of — branching strategy, CI/CD, code review, release management, even how teams structure collaboration are all downstream of decisions baked into Git's design in 2005. A practitioner studies this not to memorize commands but to stop being surprised: every confusing Git moment ("detached HEAD", a force-push wiping history, a merge conflict that won't resolve) is actually a direct, deterministic consequence of a small set of underlying ideas. Once those ideas click, the command-line interface — which is widely considered a leaky, inconsistent abstraction over a clean internal model — becomes legible instead of arbitrary.
>
> **Your angle:** You're not learning Git from zero — you're replacing a copy-paste relationship with a causal one. The fastest path for you is to skip the command-by-command tour and go straight to the internal data model (how Git actually stores and identifies things), because nearly every "why does this command do *that*" moment resolves instantly once you can see what's happening to the underlying object graph. Treat the CLI as a thin, sometimes badly-designed window onto that model — your goal is to be able to predict what the window will show, not memorize what to type.

---

## How to use this map

This is Level 0: a map of the domain, not a tutorial. Each Level 1 topic below is a node you could spend a few hours to a few days on. The "Level 2 candidates" under each one are the sub-concepts you'd hit if you descended further — they're listed so you can see what's *inside* a topic before deciding whether to open it.

Descend into a Level 1 topic when you hit it in real work and the one-paragraph explanation here isn't enough to resolve your confusion — or when the Sequencing Note below tells you it's a high-leverage one to study proactively rather than reactively. A Level 2 descent means generating a focused explainer or doing hands-on exercises for just that sub-concept, not the whole parent topic. You don't need to clear a group before moving to the next one; dependency arrows matter more than group boundaries.

---

## Topic Inventory

### Group 1: The Object Model (what Git actually *is*)

#### L1-01 · Content-Addressable Storage & the Object Database
Git's core trick, inherited conceptually from systems like the Plan 9 file system and content-addressable storage research from the 1990s, is that *everything* — file contents, directory structures, commits — is stored as an immutable object, named by the SHA-1 (now transitioning to SHA-256) hash of its own content. This single decision is why Git "just works" for huge, distributed history: there's no central authority assigning IDs, because the content assigns its own ID. Once this lands, commands that look like magic — `git cat-file`, why two identical files in different commits take zero extra space, why a SHA never changes once committed — become obvious restatements of the same fact. This is the one concept worth understanding before any other, because almost every other Level 1 topic is really just "a particular way of navigating or mutating this object graph."

**Level 2 candidates:**
- **Blobs** — explains why Git tracks content, not files or filenames, which is the reason renames are "detected" heuristically rather than recorded.
- **Trees** — shows how directory structure is itself a hashed, versioned object, which is what lets `git diff` distinguish a content change from a structural one.
- **Commits** — reveals that a commit is just a pointer to one tree plus pointers to parent commit(s), which is the entire reason history is a graph and not a list.
- **The `.git/objects` directory** — gives you the ability to literally read your repository's history with no Git commands at all, which deflates "Git internals" from mysterious to mechanical.
- **SHA-1 vs SHA-256 transition** — explains why some tooling cares about hash collisions and why "the hash *is* the content" has real security implications, not just identity ones.
- **Loose objects vs packfiles** — answers why a fresh clone is small but a long-lived repo's `.git` folder can balloon, and what `git gc` is actually doing.

#### L1-02 · Refs: Branches, Tags, and HEAD
A "branch" in Git is not a structure that contains commits — it's a 41-byte text file containing a single SHA, living in `.git/refs/heads/`. This is the most load-bearing simplification in the entire system: branches are *cheap* (instant to create, trivial to delete) specifically because a branch is a name, not a copy. Tags are the same idea frozen in place rather than moving forward with each commit. HEAD is a ref to a ref — it's what makes "where am I right now" a well-defined question. Understanding this turns "detached HEAD state," one of the most disorienting messages in Git, into something predictable rather than alarming: it's just HEAD pointing directly at a commit instead of at a branch.

**Level 2 candidates:**
- **Branches as movable pointers** — explains why `git branch` is instant while "branching" in older VCSs (like CVS or SVN, which copied directory trees) was expensive, and why deleting a branch never deletes commits by itself.
- **HEAD and the reflog** — unlocks recovery from almost any local mistake, because the reflog is a private journal of everywhere HEAD has pointed, even commits no branch currently references.
- **Detached HEAD** — resolves why checking out a specific commit (not a branch) puts you in a state where new commits can be silently orphaned if you're not paying attention.
- **Tags: lightweight vs annotated** — explains why release tooling and `git describe` prefer annotated tags, which are full objects with metadata, not just a name.
- **Tracking branches and remotes/origin refs** — explains what `origin/main` actually is (a cached pointer, not a live connection) and why it can silently go stale.
- **The symbolic ref mechanism** — shows how HEAD pointing to `refs/heads/main` rather than a SHA is what makes "switching branches" mean something different from "checking out a commit."

#### L1-03 · The Three Trees: Working Directory, Index, and HEAD
Most day-to-day Git confusion — "why do I have to `add` before I `commit`," "why did `git diff` show nothing," "what does staged even mean" — comes from not tracking that Git maintains three distinct snapshots of your project at all times: the working directory (your actual files), the index/staging area (a proposed next commit), and HEAD (the last commit). This three-tree model exists because Linus Torvalds, designing Git in 2005 after the BitKeeper licensing dispute forced the kernel project to build its own VCS in days, wanted commit construction to be a deliberate, inspectable act rather than an automatic snapshot of whatever's on disk — a deliberate rejection of how older systems worked. Once you can name, for any Git command, *which two trees it's comparing or moving between*, the entire command surface stops looking arbitrary.

**Level 2 candidates:**
- **The staging area / index** — explains why you can commit only *part* of your changes, and why `git status` shows two separate "changes" sections.
- **`git add` as a tree operation** — reframes "adding a file" as "copying a blob's hash into the index," which is why adding a file twice with different content just updates one entry.
- **`git diff` vs `git diff --staged`** — resolves the single most common "why is this showing nothing" confusion by mapping each command to a specific pair of trees being compared.
- **`git checkout` / `git restore` semantics** — explains why this one command historically did wildly different things depending on arguments, and why newer Git split it into `restore` and `switch`.
- **Partial staging (`git add -p`)** — unlocks committing cleanly-scoped changes even when you edited multiple concerns in one sitting, by staging at the hunk level rather than the file level.

---

### Group 2: History as a Graph (how change accumulates and diverges)

#### L1-04 · Commits as a Directed Acyclic Graph
Once you know a commit just points to its parent(s), "history" stops being a timeline and becomes a graph — specifically a DAG, since a commit can have multiple parents (merges) but you can never travel forward in time into a cycle. This is the conceptual leap that explains why Git branching is fundamentally different from, and more powerful than, the linear history models of older systems: divergence and reconvergence are first-class, not edge cases bolted on. Most "advanced" Git operations — rebasing, cherry-picking, bisecting — are really just different ways of walking, rewriting, or searching this graph. Seeing history this way is also what makes tools like `git log --graph` legible instead of decorative ASCII art.

**Level 2 candidates:**
- **Parent pointers and multi-parent (merge) commits** — explains why a merge commit "remembers" both lines of history, which is the mechanism `git log --first-parent` exploits to hide noise.
- **Ancestry and reachability (`git log A..B`)** — unlocks precise questions like "what's in this branch that isn't in main yet," which is the basis of every PR diff view.
- **Common ancestors (merge base)** — explains what Git is actually computing before it attempts a merge or rebase, and why an unexpected merge base produces a baffling diff.
- **`git bisect`** — shows how treating history as a searchable graph turns "which of these 200 commits broke this" into a binary search instead of a guessing game.
- **Fast-forward vs non-fast-forward** — explains why some merges produce no merge commit at all, and why `--no-ff` exists as an explicit override.

#### L1-05 · Merging
A merge is Git's answer to "two lines of history diverged from a common point and need to become one again" — and the algorithm (three-way merge, comparing both branch tips against their common ancestor) was itself an evolution from earlier two-way diff/patch tooling that couldn't distinguish "you changed this" from "I changed this" cleanly. Understanding the three-way merge is what makes conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) interpretable as "here's what changed on each side since the common ancestor" rather than inscrutable noise. This is also where team workflow decisions (merge commits vs squash vs rebase-and-merge) actually originate — they're different philosophies about whether the DAG should preserve literal history or a cleaned-up narrative of it.

**Level 2 candidates:**
- **Three-way merge algorithm** — explains exactly why conflicts happen on overlapping line ranges and not just identical lines, and why the same change merges cleanly in one context but conflicts in another.
- **Conflict markers and resolution** — turns conflict-resolution from trial-and-error into a deliberate act once you know which section corresponds to which branch and the ancestor.
- **Merge commits and the second parent** — explains why `git log` on a merged branch shows commits "out of order" chronologically, and what `--first-parent` is filtering out.
- **Merge strategies (recursive, ort, octopus)** — explains why some merges silently behave differently across Git versions, and when you'd intentionally merge more than two branches at once.
- **Squash merging** — unlocks why some teams have linear `main` history with no merge commits at all, trading granular history for a clean narrative.

#### L1-06 · Rebasing
Rebasing answers a different question than merging: instead of "combine these two histories," it asks "replay my changes as if I'd started from a more current point." Mechanically, this means Git takes each of your commits, computes its diff, and reapplies that diff on top of a new base — which is why rebase can hit the *same* conflicts a merge would, but resolves them one commit at a time rather than once in aggregate. This is the topic most likely to cause real damage if misunderstood, because rebasing rewrites commit SHAs (a "new" commit is created even if the content is identical), which is catastrophic on shared/pushed history and the direct cause of the "never rebase public branches" rule you've probably heard without understanding why.

**Level 2 candidates:**
- **Rebase as "replay," not "move"** — explains why rebased commits get new SHAs even with identical content, which is the root cause of every "rebase broke the shared branch" incident.
- **Interactive rebase (`-i`)** — unlocks rewriting your own commit history before sharing it: squashing, reordering, splitting, or editing commit messages as a deliberate narrative act.
- **`--onto`** — explains how to move a branch to a different base entirely, useful when a dependency branch gets merged or abandoned out from under you.
- **Rebase vs merge as a team policy decision** — explains the actual tradeoff (linear, readable history vs preserved-but-messy literal history) underneath the "rebase vs merge" debates you've likely seen argued without resolution.
- **Why you never rebase a shared/public branch** — the cost side of the previous candidate: rewritten history diverges from what collaborators have, forcing force-pushes that can silently discard their work.

#### L1-07 · Cherry-picking and Selective History Application
Cherry-pick is the single-commit version of rebase's "replay" idea: take one commit's diff and reapply it elsewhere, independent of its original ancestry. It exists because real engineering work doesn't always move in clean, mergeable branches — sometimes you need exactly one fix from a branch without its other nine commits, classically for hotfix backports to a release branch. Once you see this as "diff extraction and reapplication," it stops feeling like a special case and becomes a tool you reach for deliberately, with a clear sense of when it'll apply cleanly and when it'll conflict.

**Level 2 candidates:**
- **Cherry-pick as targeted diff replay** — explains why a cherry-picked commit gets a new SHA, same as a rebase, and why that's not a bug.
- **Cherry-pick conflicts** — shows that conflicts here come from the same three-way-merge logic as a real merge, just scoped to one commit's diff.
- **Backporting to release branches** — the classic real-world use case, and why teams without it resort to manually re-typing fixes across branches.
- **`-x` and tracking provenance** — explains how to leave a trail back to the original commit, useful when auditing where a fix actually came from.

---

### Group 3: Working With Others (the distributed model)

#### L1-08 · Distributed Architecture: Remotes and the Clone Model
Git was built, from day one, on the assumption that every clone is a complete, independent repository with full history — not a thin client talking to a central server, which is how CVS and Subversion worked. This is *the* design decision that makes offline commits, fast local operations, and the entire GitHub/GitLab pull-request model possible: "the remote" is just another repository that happens to be conventionally treated as authoritative, not a different kind of thing. Once this lands, `git fetch` vs `git pull`, "tracking branches," and why your local `main` can drift from `origin/main` all become consequences of "you have two full copies of history that occasionally need to be reconciled," not arbitrary command behavior.

**Level 2 candidates:**
- **Remotes as named repository URLs** — explains why you can have multiple remotes (`origin`, `upstream`) and what's actually being stored when you `git remote add`.
- **`fetch` vs `pull`** — resolves the most common entry-level confusion by separating "download new objects and update remote-tracking refs" from "fetch, then also merge/rebase into my current branch."
- **Push, and why it can be rejected** — explains the non-fast-forward rejection as a safety mechanism, not an arbitrary error, protecting against silently discarding others' commits.
- **Force-push and its dangers** — explains exactly what's being overwritten on the remote, and why `--force-with-lease` exists as a safer middle ground.
- **Shallow clones and partial clones** — explains why large monorepos use `--depth` or partial clone, trading full history for faster checkout.

#### L1-09 · Collaboration Workflows
The actual day-to-day shape of "how a team uses Git" — feature branches, pull/merge requests, trunk-based development, Gitflow — isn't dictated by Git itself; Git only provides the primitives (cheap branches, merges, rebases). The workflow layer is a social and process decision built on top, and most of the friction engineers feel in "Git workflow" disagreements is really a disagreement about release cadence, code review philosophy, or CI design wearing Git's clothing. Seeing this separation clearly is what lets you evaluate a team's chosen workflow on its actual merits instead of treating it as Git's mandate.

**Level 2 candidates:**
- **Feature branching** — explains the basic isolation pattern almost everything else builds on: develop in isolation, integrate deliberately.
- **Trunk-based development** — explains why some high-velocity teams avoid long-lived branches almost entirely, leaning on feature flags instead of branch isolation.
- **Gitflow and its decline** — explains the once-popular heavyweight branching model (Vincent Driessen, 2010) and why most teams have since moved to simpler models as release cadence sped up.
- **Pull/merge requests as a review gate** — explains that PRs are a platform feature (GitHub/GitLab/Bitbucket), not a Git concept, which is why the underlying Git operations differ from what the platform UI implies.
- **Monorepo vs polyrepo implications** — explains how repository scale changes which Git features (sparse checkout, partial clone) stop being optional.

#### L1-10 · Submodules and Subtrees
When one repository needs to depend on another repository's history rather than just its latest snapshot (vendoring a library, sharing code across projects without a package manager), Git offers two distinct, both somewhat clunky, solutions. Submodules store a *pointer* to a specific commit in another repo, which is precise but famously easy to get into a confusing detached state with. Subtrees instead merge another repo's history directly into yours, trading precision for simplicity. Knowing both exist — and why neither feels as smooth as the rest of Git — saves you from reaching for ad hoc copy-paste vendoring or fighting a submodule for hours without understanding what state it's actually in.

**Level 2 candidates:**
- **Submodules as commit pointers** — explains why a submodule directory in `git status` often shows as "modified" with no visible diff: the pointer commit changed.
- **Detached HEAD inside submodules** — explains why naive `cd` and `git pull` inside a submodule frequently leaves it in a state that doesn't get committed correctly.
- **Subtree merge** — explains the alternative model where dependency history is folded directly into your repo, avoiding the "extra clone" mental overhead of submodules.
- **When to avoid both** — explains why many teams prefer package managers or monorepos specifically to avoid this entire problem space.

---

### Group 4: Recovery, Inspection, and Maintenance

#### L1-11 · Undoing Things: Reset, Revert, and Checkout
This is the topic most directly tied to the panic-and-copy-paste cycle, because Git has *three* commands that all sound like "undo" but operate on completely different trees and have completely different safety properties. `reset` moves where a branch ref points (and optionally rewinds the index/working directory with it) — it rewrites history. `revert` creates a *new* commit that undoes a previous one's changes — it adds to history rather than rewriting it, which is why it's the only one of the three that's safe on shared branches. `checkout`/`restore` discard local changes by overwriting the working directory from another tree. Knowing which of the three trees from L1-03 each command touches is what turns "which undo command do I need" from guesswork into a lookup.

**Level 2 candidates:**
- **`git reset --soft/--mixed/--hard`** — explains exactly how far back each variant unwinds (commit ref only, ref + index, or ref + index + working directory), which is the single most useful table to memorize in all of Git.
- **`git revert`** — explains why this is the *only* safe "undo" for commits already pushed and shared, since it adds history instead of erasing it.
- **`git restore` (working tree vs staged)** — explains the modern split of the old overloaded `checkout` command into separate, less dangerous operations.
- **Recovering "lost" commits via reflog** — explains why almost nothing in local Git history is ever truly gone for ~90 days, even after a hard reset, as long as you know to look in the reflog.
- **`git clean`** — explains the one genuinely destructive, unrecoverable operation (removing untracked files) and why it's separated from the rest of "undo" by design.

#### L1-12 · Inspecting History
Most of the anxiety around Git comes from not being able to *see* what's actually happening before you act — these are the read-only tools that let you build confidence before committing to a destructive operation. `git log` with the right flags turns the abstract DAG from L1-04 into something visible; `git blame` and `git show` let you attribute and inspect specific changes; `git diff` variants let you compare any two trees, not just the three default ones. Treat this entire group as the "look before you leap" toolkit that should precede most of Group 4's other topics in practice.

**Level 2 candidates:**
- **`git log` flags (`--oneline`, `--graph`, `--stat`, `--all`)** — unlocks actually seeing the branch structure instead of guessing at it from memory.
- **`git show`** — explains how to inspect any single object (commit, tree, blob) directly, collapsing "what even is this SHA" into one command.
- **`git blame`** — explains line-level provenance, and why it's often more useful for "what was this person trying to solve" than literal authorship.
- **`git diff` between arbitrary refs** — generalizes the three-tree comparisons from L1-03 to comparing *any* two commits, branches, or tags.
- **`git log -S` / pickaxe search** — unlocks searching history by *content change* rather than commit message, useful when you remember a removed line but not when.

#### L1-13 · Repository Maintenance and Internals Hygiene
This is the "why is my repo slow / huge / weird" topic — what Git is doing in the background to keep the object database efficient, and what happens when that maintenance is skipped or interrupted. Packfiles, garbage collection, and the various integrity-check tools exist because a naive one-loose-file-per-object model (L1-01) doesn't scale to years of history without compaction. This topic matters less for daily workflow and more for the moments your repo behaves strangely and you need to understand what state the object database itself is actually in.

**Level 2 candidates:**
- **Packfiles and `git gc`** — explains how thousands of loose objects get compressed into a handful of efficient packfiles, and why a repo's `.git` size can drop dramatically after gc.
- **`git fsck`** — explains how to verify the integrity of the object database itself, useful when something seems corrupted rather than merely confusing.
- **Dangling commits and pruning** — explains what "dangling" actually means (a real object with no ref pointing to it) and why pruning is the operation that finally makes a reflog-recoverable commit truly unrecoverable.
- **`.gitignore` and why it only affects untracked files** — explains the common confusion of adding a pattern to `.gitignore` and having it do nothing, because the file was already tracked before the ignore rule existed.
- **Git hooks** — explains the extension points (pre-commit, pre-push, etc.) that let teams enforce policy automatically, and why hooks aren't versioned/shared by default the way the rest of the repo is.

---

## Sequencing note

The dependency chain here is steep at the bottom and flattens out fast. **L1-01 (object model) and L1-02 (refs) are true prerequisites for everything else** — every other topic in this map is, underneath, a statement about objects and refs, so skipping them means every later topic gets explained in terms you haven't actually internalized. L1-03 (the three trees) is the next non-negotiable step, because it's the direct cause of the staging-area confusion that drives most day-to-day copy-paste behavior — and notably, you can fully understand L1-01 through L1-03 without ever touching a remote or another collaborator, which makes them ideal to nail down in isolation before workflow complexity enters.

From there, **Group 2 (history as a graph) branches into two paths that depend on Group 1 but not on each other**: L1-04 → L1-05/L1-06/L1-07 (merge, rebase, cherry-pick) is the "changing history" path, while jumping ahead to L1-12 (inspecting history) is the "observing history" path — and given your stated experience (currently copy-pasting without a model), **L1-12 is worth pulling forward out of its group position**, because the ability to actually *see* the DAG before you act on it will make L1-05/06/07 dramatically less anxiety-inducing when you get there. Group 3 (collaboration) depends on Group 1 and L1-08 specifically, but L1-09 (workflows) is mostly social convention layered on top — low conceptual depth, high practical relevance, safe to skim early and return to only when your team's specific workflow demands it. L1-10 (submodules) is a dead-end branch in the dependency graph — almost nothing else depends on it, and it's only worth descending into if you actually encounter a submodule in the wild.

**Highest-leverage entry point for you specifically:** start at L1-01, move directly through L1-02 and L1-03, then detour into L1-12 (inspecting history) before touching L1-05/06/07. This ordering directly targets the copy-paste-without-understanding pattern: it front-loads the exact conceptual primitives that make every confusing command legible, and it gives you a *safe, read-only* toolkit (L1-12) to build confidence with before you're voluntarily running history-rewriting commands. L1-11 (undo operations) should be your second priority after that detour — not because it's conceptually prerequisite to anything, but because being fluent in "how do I get out of this" is what actually lets you stop reaching for an agent out of fear of irreversible mistakes, which is the real goal underneath this whole map.