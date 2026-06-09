## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams pick a merge strategy the way they pick a code formatter: someone has a preference, it gets encoded into the repository settings, and nobody revisits it. The conversation, when it happens at all, tends to center on aesthetics — "I like a clean history" or "merge commits are noisy." This framing misses the point entirely. Each merge strategy produces a fundamentally different graph structure, and that structure determines what information your history retains, what diagnostic tools remain available to you, and what operations become safe or dangerous after the fact. Choosing a merge strategy is not a style preference. It is a decision about what you will be able to learn from your repository six months from now when something is broken and you need to understand why.

The Level 1 post established that commit history is a debugging tool and that atomic commits make tools like `git bisect` effective. This post explains the mechanics that sit underneath that claim: what each strategy does to the commit graph, what exactly is preserved or destroyed, and why those structural differences matter when you need to actually use your history.

## The Graph You Are Shaping

A Git repository is a directed acyclic graph (DAG) of commit objects. Every commit stores a snapshot of the repository, a pointer to one or more parent commits, an author, a committer, a timestamp, and a message. The SHA-1 hash that identifies a commit is derived from all of this — including the parent pointer. This means two commits with identical file changes but different parents are different commits with different hashes.

When you choose a merge strategy, you are choosing how to integrate one line of commits into another. The resulting graph topology — how many parents each commit has, whether original commits are preserved or replaced, whether branch structure is visible — is the thing that varies. Everything downstream (what `git log` shows, what `git bisect` can traverse, what `git blame` reports, what `git revert` can undo) follows from that topology.

## Merge Commits: Preserving the Full Topology

A **merge commit** is a commit with two (or more) parents. When you merge a feature branch into main with a merge commit, Git creates a new commit on main whose first parent is the previous tip of main and whose second parent is the tip of the feature branch. The feature branch's commits remain exactly as they were — same hashes, same parent relationships, same authorship.

Suppose main has commits A → B → C, and your feature branch diverged at B with commits D → E. After a merge, main looks like this:

```
A → B → C → M
         \     ↗
          D → E
```

M is the merge commit. It has two parents: C and E. The commits D and E still exist with their original SHAs and their original parent pointers. The entire branch topology is recorded in the graph.

This preservation has a concrete consequence that most engineers underappreciate: `git log --first-parent main` will show you A, B, C, M — just the merge points on main, one per feature. This gives you a clean, scannable history of integrations. Meanwhile, `git log main` (without `--first-parent`) will show you every commit, including D and E, with full detail. You get both views from the same graph. The "merge commits are noisy" complaint is almost always a `git log` configuration problem, not a merge strategy problem.

Merge commits also mean that `git bisect` can traverse into the feature branch. If the regression was introduced in commit D, bisect will find it. Every atomic commit the developer made is individually testable.

The cost is real, though. The graph is more complex. Tools that render history linearly (many GUI clients, some CI dashboards) can make a merge-heavy history look tangled. And merge commits can produce confusing diffs when the merge itself resolved conflicts — the merge commit's diff shows the conflict resolution, which is new code that does not appear in any individual feature commit.

## Rebase: Rewriting Lineage

A **rebase** takes a series of commits and replays them onto a new base, producing new commits with new parent pointers and therefore new SHA hashes. The diffs are the same. The messages are the same. The authorship metadata is preserved. But they are, from Git's perspective, entirely different commits.

Starting from the same example — main at A → B → C, feature branch at B → D → E — a rebase of the feature branch onto main produces:

```
A → B → C → D' → E'
```

D' and E' have the same diffs and messages as D and E, but different SHAs because their parent pointers changed. D' points to C instead of B. The original D and E still exist in the repository's object store (until garbage collection), but nothing references them.

After rebasing, the feature branch can be fast-forward merged into main, producing a perfectly linear history with no merge commit. This is what people mean when they say rebase gives you a "clean" history.

What is actually happening is a trade: you gain linearity and lose topology. The resulting graph does not record that D' and E' were developed together as a unit, or that they were developed in parallel with C. The history looks as if the developer wrote D' and E' sequentially after C, which is not what happened.

The more important mechanical consequence is the SHA rewrite. Any system or person that referenced the original commit D by its hash — a comment in a code review, a CI build record, a link in an issue tracker, a tag — now holds a dangling reference. The commit exists in the reflog temporarily, but for practical purposes, the identity of that commit has been destroyed and replaced.

This also creates a hazard for shared branches. If another developer branched off your feature branch at commit D, and you rebase your feature branch (rewriting D to D'), their branch still points to the original D. When they try to merge or rebase onto your updated branch, Git sees divergent histories with duplicated changes. This is the origin of the well-known rule: **do not rebase commits that other people have based work on.** It is not a convention. It is a consequence of how commit identity works.

## Squash: Compressing a Branch Into a Single Commit

A **squash merge** takes all the commits on a feature branch and produces a single new commit on the target branch. That commit's diff is the cumulative diff of the entire feature branch, its message is typically a combination (or replacement) of the individual commit messages, and it has a single parent: the tip of the target branch.

From the same starting point, a squash merge produces:

```
A → B → C → S
```

S contains all the changes from D and E combined. Commits D and E are not reachable from main. The feature branch, if not deleted, still points to E, but Git has no record that S is related to D or E. There is no parent pointer connecting them.

This is the most aggressive compression of the three strategies. What is preserved: the cumulative code change, the final state. What is lost: every intermediate step, the individual commit authorship (if multiple people committed to the branch), the ability to attribute specific lines to specific commits within the feature, and — critically — **Git's awareness that this work was integrated at all**.

That last point has a subtle but real consequence. If you squash-merge a feature branch into main and then later try to merge that same feature branch (or another branch derived from it) into main again, Git does not know that the work is already present. It will attempt to apply those changes again, likely producing conflicts. This makes squash merging hazardous for workflows involving long-lived branches, release branches, or any pattern where the same line of work might be integrated into multiple targets.

## Diagnostic Consequences: Bisect, Blame, and Revert

The choice of merge strategy directly determines the resolution at which your diagnostic tools operate.

### Bisect

`git bisect` performs a binary search across commits to find the one that introduced a bug. Its effectiveness is a function of how many individually testable commits exist between "known good" and "known bad." With merge commits, bisect can traverse into feature branches and test individual commits — if the developer made atomic commits, bisect can pinpoint the exact change. With rebase, the commits are linear and bisect works the same way, testing each replayed commit. With squash, the entire feature is one commit. If a feature touched 40 files across 15 commits that were squashed, bisect can only tell you "the bug is somewhere in this 2,000-line change." You are back to manual inspection.

### Blame

`git blame` maps each line of a file to the commit that last modified it. With merge commits or rebase, blame traces through to individual commits with their original messages and authorship. With squash, every line touched by the feature is attributed to a single commit with a single author, even if multiple engineers contributed. The individual "why" behind each line change is gone.

### Revert

`git revert` creates a new commit that undoes the changes of a previous commit. Reverting a squash commit is mechanically simple — one commit, one revert. Reverting a merge commit requires you to specify which parent to follow (typically `-m 1` to revert relative to the mainline), and it has a well-known gotcha: if you revert a merge commit and later try to re-merge the same branch, Git considers those commits already integrated and will not apply them. You have to "revert the revert" first. This is not a bug; it follows directly from how Git tracks merge ancestry. But it surprises engineers regularly.

Reverting individual commits from a rebased history is straightforward, but because the commits are linear, reverting one mid-sequence commit can conflict with later commits that depend on it, whereas reverting an entire merge commit cleanly removes the whole unit of work.

## Where Teams Get Into Trouble

The most common failure mode is **squash-by-default without understanding what it destroys**. Many teams adopt squash merging because it makes the main branch history look tidy — one commit per PR, easy to scan. This works fine for small, single-commit features. It becomes a real problem when a PR contains meaningful intermediate steps. A developer who carefully structured their work into atomic commits — separating the refactor from the behavior change from the test update — watches all of that structure get collapsed into a single blob. The effort invested in commit hygiene yields zero diagnostic return.

The second failure mode is **rebasing shared branches**. A developer rebases a branch that a colleague has already pulled and branched from. The colleague's history diverges from the rewritten branch. The resulting merge conflicts are confusing because they involve changes the developer has already seen. The fix is painful and error-prone. This happens most often on teams that enforce rebase workflows without ensuring that every engineer understands the SHA-rewriting mechanic.

The third failure mode is **treating merge strategy as uniform policy when branch types differ**. A short-lived, single-purpose branch with one commit benefits from squash — nothing is lost. A long-running integration branch with a dozen carefully structured commits benefits from merge commits — everything is preserved. A solo developer's local feature branch benefits from rebase before merging — the local messy history is cleaned up and the public history stays linear. Applying one strategy to all three situations guarantees a poor fit in at least two of them.

A subtler issue is **losing the ability to understand the evolution of a design**. When a feature branch records the sequence "add interface, implement for case A, implement for case B, refactor shared logic," that sequence tells a story about how the design emerged. Squashing collapses that into "add feature X." Twelve months later, when someone is trying to understand why the abstraction boundary is where it is, the information that would explain it no longer exists.

## The Model to Carry Forward

Every merge strategy is a lossy transform applied to your commit graph. The question is never "which one produces the cleanest history" — that framing reduces a structural decision to an aesthetic one. The question is: **what information does my team need to recover from this history, and which strategy preserves it?**

Merge commits preserve everything — full topology, original commits, branch relationships — at the cost of a more complex graph. Rebase preserves individual commit detail but destroys topology, commit identity, and the evidence that work happened in parallel. Squash destroys almost everything except the cumulative result.

The right choice depends on what you are integrating. It depends on how your team works, how large your changes tend to be, and what you expect to need from your history when something goes wrong. The engineer who understands the graph mechanics can make that choice deliberately. The engineer who does not is making it by accident.

## Key Takeaways

- A merge commit creates a commit with two parents, preserving the full branch topology and every original commit hash; `git log --first-parent` gives you a clean integration-level view while the full graph retains all detail.

- Rebase replays commits onto a new base, producing new commits with new SHA hashes; any external references to the original commit hashes become dangling, and rebasing commits that others have branched from will cause divergent histories.

- Squash merge compresses an entire branch into a single new commit with no parent-pointer connection to the original branch, meaning Git has no record the integration occurred — re-merging the same branch will cause conflicts.

- `git bisect` effectiveness is directly proportional to the number of individually testable commits in your history; squash merging collapses a feature to a single commit, eliminating any ability to binary-search within it.

- `git blame` after a squash merge attributes every changed line to a single commit and a single author, destroying the per-line provenance that would otherwise explain why each change was made.

- Reverting a merge commit requires specifying a parent (`-m 1`) and creates a state where re-merging the same branch will silently skip the changes unless the revert itself is reverted first.

- The strongest workflow is not a single strategy applied uniformly but a deliberate choice per branch type: squash for trivial single-purpose branches, rebase for cleaning up local work before sharing, merge commits for preserving the structure of meaningful multi-commit features.

- History is not a log to be kept tidy; it is a diagnostic instrument whose resolution is determined by the merge strategy you choose at integration time.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Teams often talk about Git merge strategy as if it were about how pretty the history looks. But the real issue shows up later, when production is broken, a revert goes sideways, or someone needs to answer “which exact change introduced this?” At that moment, your commit history stops being decoration and becomes instrumentation. The merge strategy you chose months earlier determines how much of that instrumentation still exists.

When engineers do not understand the mechanics, they make choices that silently throw information away. Squash merging can collapse 15 useful commits into one opaque blob, so `git bisect` can no longer isolate the bug. Rebasing shared branches can rewrite commit identities other people are depending on, creating confusing divergence and duplicate-conflict situations. Using merge commits without understanding them can make reverts and later re-merges surprising. The failure mode is not “ugly history.” The failure mode is losing the ability to safely reason about what happened.

---

## What You Need To Know First

### 1. A Git commit is an object with identity, not just a patch
A commit is not “the set of file changes.” It also includes metadata like its parent commit(s), author/committer info, message, and timestamp. Git hashes all of that together to produce the commit SHA. So if the parent changes, the commit identity changes, even if the file diff looks identical.

### 2. Git history is a graph, not a list
Even though many tools display commits as a vertical timeline, Git actually stores history as a directed acyclic graph. Most commits have one parent; merge commits have multiple parents. Branches are just movable pointers into that graph. This matters because merge strategy changes the graph shape, and the graph shape determines what Git can infer later.

### 3. Fast-forward vs true merge
If branch A is simply ahead of branch B with no divergence, Git can “fast-forward” by moving the branch pointer forward—no new merge commit is needed. A true merge happens when histories diverged and Git creates a new commit tying the lines together. This distinction matters because rebase often turns a branch into something that can be fast-forwarded.

### 4. Tools like `bisect`, `blame`, and `revert` operate on commits and ancestry
These tools are not magical source-code analyzers. They use the commit graph. `git bisect` searches across commits, `git blame` attributes lines to commits, and `git revert` undoes commits relative to ancestry. If your merge strategy changes or removes commit structure, these tools lose resolution or behave differently.

---

## The Key Ideas, Connected

### 1. Merge strategy is really a decision about commit-graph structure.
The article’s core claim is that merge strategy is not an aesthetic preference; it is a choice about what graph Git will store after integration. That graph records parent relationships, branch convergence, and commit identity. Since Git’s later behavior depends on those relationships, different strategies preserve different kinds of information.

Once you see merge strategy as graph-shaping rather than history-formatting, the next question becomes: what exactly changes in the graph for each strategy?

### 2. Merge commits preserve the original commits and the fact that work happened on a branch.
A merge commit adds a new commit with two parents: one pointing to the previous tip of the target branch, and one pointing to the tip of the feature branch. Importantly, the feature branch’s commits are not rewritten. Their SHAs stay the same, their parent chain stays the same, and the graph still shows that this work developed separately and then joined main.

That matters because preserving branch topology means you retain two useful views of history at once. You can inspect the first-parent chain to see “what landed on main, feature by feature,” or inspect the full graph to see the detailed commits inside each feature. Since nothing was destroyed, tools can still traverse the feature’s internal history. That leads directly to the diagnostic advantage of merge commits.

### 3. Preserved topology means diagnostic tools retain fine-grained resolution.
Because the original commits still exist and are reachable from main, `git bisect` can test them individually. If a bug was introduced halfway through the feature branch, bisect can find that specific commit rather than merely telling you the whole feature is suspicious. `git blame` can attribute specific lines to the actual commits that changed them. You also retain evidence of grouping: these commits belonged to one branch and landed together.

But this preservation comes with a cost: the graph is more complex. A more complex graph is not just visual clutter; it means some tools and humans must handle non-linear history. That tradeoff sets up the appeal of rebase.

### 4. Rebase keeps the commit-level changes but rewrites their lineage.
Rebase takes commits and replays them onto a different parent, creating new commits with new SHAs. Even if the diffs and commit messages are unchanged, Git treats them as entirely new objects because their parent pointers changed. So rebase preserves the logical sequence of code changes, but not the original identity or topology.

This is why rebase produces a linear-looking history: the branch no longer appears to have diverged and merged; it appears to have been written directly on top of the current main branch. That linearity is what many teams call “clean.” But mechanically, the cleanliness comes from deleting evidence of the original branch shape. Once commit identity is rewritten, a new consequence appears: anything referring to the old commits is now referring to abandoned objects.

### 5. Rewriting commit identity makes rebase dangerous on shared history.
If someone else has based work on commit D, and you rebase D into D', their branch still points to old D. Git now sees two different histories containing similar or identical content but different commit identities. That is why rebasing a shared branch creates messy divergence and confusing conflict scenarios: Git is not being stubborn; it is faithfully responding to the fact that the shared commit identity was replaced.

So the usual advice “don’t rebase public history” is not etiquette. It follows directly from how Git defines a commit. Rebase is safe and useful when you are cleaning up your own local unpublished branch, because no one else depends on those commit identities. Once work is shared, the rewrite becomes externally disruptive. That makes squash the next important comparison, because squash throws away even more structure.

### 6. Squash merge preserves only the final combined diff, not the branch’s internal history.
A squash merge creates one new commit on the target branch containing the cumulative effect of all the feature branch’s changes. It does not preserve the original commits on main, and it does not create ancestry connecting that final commit to the feature branch’s internal commit chain. Git sees “here is one new commit with these changes,” not “this commit represents those prior commits being integrated.”

That makes squash the most lossy strategy. You keep the resulting code state, but lose the sequence of intermediate steps, individual authorship across those steps, and the graph-level fact that the feature branch was integrated. Because Git cannot see that ancestry relationship, future operations behave differently. This is why squash has hidden costs beyond just losing detail.

### 7. Losing ancestry changes what Git can recognize later.
Git reasons from commit ancestry, not from “these patches seem philosophically equivalent.” After a squash merge, main contains the code changes, but not the commit ancestry linking main to the feature branch. So if you later try to merge that same branch or a descendant of it, Git does not know the branch’s commits have effectively already been integrated. It may try to apply them again, often causing conflicts.

This is the subtle but important distinction: squash does not merely make history coarser; it removes information Git uses to decide whether work is already merged. Once you understand that, the article’s discussion of diagnostic tools makes more sense: each tool is only as powerful as the graph information still available.

### 8. `bisect`, `blame`, and `revert` work at the resolution your merge strategy leaves behind.
With merge commits, the graph retains both integration boundaries and per-commit detail. With rebase, you still have per-commit detail, but the original branch structure and old SHAs are gone. With squash, the whole feature may become one indivisible commit from the perspective of main.

So `git bisect` on a squashed feature cannot isolate the bad commit inside the feature; it can only land on the squashed blob. `git blame` on squashed code attributes many lines to one commit and one author, even if several people contributed distinct changes. `git revert` also changes character: reverting a squash is simple because there is one commit, but you lose the ability to target smaller constituent steps. Reverting merge commits is more subtle because merge ancestry matters, and future re-merges are affected by that ancestry.

Once tools behave differently because of graph shape, a final conclusion follows: there is no universally correct merge strategy.

### 9. The right merge strategy depends on what information you need your history to preserve.
If a branch contains one trivial change, squashing may lose almost nothing and keep main easy to scan. If a branch contains meaningful intermediate commits—refactor, behavior change, tests, follow-up fix—squashing destroys diagnostic value. If a developer wants to clean up their own local branch before publishing, rebase can be excellent. If a team needs full recoverability of how a feature evolved and landed, merge commits preserve that structure.

So the real decision is not “Which history looks nicest?” It is “Which information am I willing to throw away, and which future operations do I need to remain safe and informative?” That is the working model the article is trying to build.

---

## Handles and Anchors

### 1. Think of merge strategies as image compression levels for history
Merge commit is like lossless storage: you keep the full structure and can zoom in later. Rebase is like restructuring the folders while keeping the files: the contents are there, but original location and identity changed. Squash is like exporting everything into one PDF: easy to pass around, hard to inspect in detail later.

### 2. Ask: “What will Git still be able to prove after this merge?”
Not “what will the log look like,” but “will Git still know these commits were integrated, who changed which line, and which exact commit introduced the bug?” That question forces you to think in terms of retained information rather than aesthetics.

### 3. One-sentence core tension
A merge strategy trades simplicity now against recoverability later.

---

## What This Changes When You Build

### 1. An engineer who understands this will choose merge strategy by branch type, because different branches carry different amounts of information worth preserving.
A short-lived branch with one meaningful commit can be squashed with little loss. A multi-commit feature branch with carefully separated refactors and behavior changes should usually not be squashed, because that destroys the very structure that makes later debugging possible. The unaware engineer applies one repository-wide default everywhere and silently gets bad fits for non-trivial work.

### 2. An engineer who understands this will avoid rebasing branches others may already depend on, because rebase rewrites commit identity rather than merely tidying history.
They will happily rebase their own unpublished local work, but once a branch is shared, they will treat the existing SHAs as part of a social and technical contract. The unaware engineer thinks “same code, so no real harm,” then causes teammates to deal with duplicated commits, divergence, and confusing conflicts produced by rewritten ancestry.

### 3. An engineer who understands this will invest in atomic commits only when the integration strategy will preserve their value, because atomicity only helps if those commits survive onto useful history.
If the team squash-merges every PR, the practical diagnostic benefit of making 12 carefully structured commits may be lost on main. That may still be acceptable for review, but it changes what history can do later. The unaware engineer hears “make atomic commits for bisectability” while the team’s squash policy removes that bisectability at integration time.

### 4. An engineer who understands this will interpret revert workflows more cautiously, because merge ancestry affects what can be re-merged later.
When reverting a merge commit, they know Git will continue to remember the original branch as merged, which means re-merging the same branch later will not simply replay the changes. They will plan for revert-the-revert or branch recreation as needed. The unaware engineer expects revert to “reset history” and is surprised when later merge behavior does not match that mental model.

### 5. An engineer who understands this will configure history views instead of discarding information for readability, because readability and preservation are not the same problem.
They will use tools like `git log --first-parent` to get a clean integration view while still keeping full topology in the repository. The unaware engineer often chooses squash or forced-linear history mainly to make default log output look cleaner, sacrificing future diagnostic capability to solve what was really a tooling/view problem.

---

</details>
