## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers think of a merge conflict as the thing that interrupts their workflow — the moment Git stops and demands manual intervention. That framing is exactly backwards. When Git raises a textual conflict, it is doing its job correctly. It detected incompatible changes and refused to guess. The actual danger is the merge that completes without any conflict at all, producing code that compiles, passes the linter, and introduces a defect that nobody catches until production. Understanding why requires looking at what Git actually does during a merge, and more importantly, what it cannot do.

## How a Three-Way Merge Works

Git's merge operation is not a comparison between two branches. It is a comparison between three snapshots: the two branch tips and their **merge base**, the most recent common ancestor commit. This is the foundation that makes auto-resolution possible, and also the foundation that makes it dangerous.

When you run `git merge feature` from `main`, Git identifies the merge base — the commit where `feature` diverged from `main`. It then computes two diffs: one from the base to the tip of `main`, and one from the base to the tip of `feature`. The merge algorithm applies both sets of changes to the base simultaneously.

The logic is straightforward. For any given region of a file, there are four possible states: neither side changed it (keep the base version), only `main` changed it (take `main`'s version), only `feature` changed it (take `feature`'s version), or both sides changed it. That last case is a textual conflict. The first three cases are auto-resolved.

The critical detail: Git defines "region" at the level of **text lines**. It does not parse your code. It does not understand functions, classes, variable scopes, type signatures, or call graphs. It sees lines of text, groups changes into hunks, and determines whether two hunks overlap. If two changes modify different lines — even adjacent lines in the same function — Git will merge them silently. It has no mechanism to evaluate whether the combined result is logically coherent.

## Textual Conflicts: The Safe Failure Mode

A textual conflict arises when both branches modify overlapping lines in the same file relative to the merge base. Git inserts conflict markers and stops:

```
<<<<<<< HEAD
    return price * 0.85;
=======
    return price - discount;
```

The developer must choose one version, combine them, or write something new. This is the most visible form of conflict, and it is the least dangerous. It forces human review at exactly the point where the tool's ability to reason has been exhausted.

Textual conflicts are not a sign that something went wrong with your workflow. They are a signal that the merge tool correctly identified an ambiguity it could not resolve. The frequency of textual conflicts is driven by two factors: how long branches live before merging, and how concentrated changes are within the same files. Trunk-based development produces fewer textual conflicts not because it eliminates conflicting intent, but because it reduces the window of divergence during which the same lines can be modified independently.

There is one subtle class of textual conflict worth understanding: the **edit-delete conflict**. One branch modifies a region of a file; the other branch deletes the entire file (or deletes the section containing that region). Git cannot auto-resolve this because it cannot decide whether the deletion should take precedence over the edit or vice versa. These are textual conflicts that signal a potentially deep disagreement about the structure of the codebase, not just about the content of a line.

## Semantic Conflicts: The Silent Failure Mode

A **semantic conflict** occurs when Git merges two changes cleanly — no conflict markers, no human intervention — but the resulting code is incorrect. The merge succeeds textually but fails logically. This is possible because Git merges text, not meaning.

Consider a concrete scenario. Your codebase has a function:

```python
def calculate_discount(price):
    return price * 0.15  # returns absolute discount amount
```

Branch A changes the function's contract. The team decides discounts should be represented as multipliers, not absolute values:

```python
def calculate_discount(price):
    return 0.85  # returns the multiplier to apply
```

Branch A updates all existing call sites to use the new contract: `final = price * calculate_discount(price)`.

Meanwhile, Branch B — developed in parallel — adds a new checkout flow in a completely different file:

```python
final_price = item_price - calculate_discount(item_price)
```

Branch B's author wrote this against the original contract, where subtracting the return value made sense. Git merges these branches without any conflict. The changes are in different files. There are no overlapping lines. The result compiles. Branch A's tests pass because they validate the new contract. Branch B's tests pass because they were written to validate the new checkout flow in isolation. But in the merged codebase, the new checkout flow is now computing `item_price - 0.85` instead of `item_price - (item_price * 0.15)`. The customer pays $99.15 instead of $85.00. This ships.

This is not an exotic edge case. This is the ordinary consequence of two developers changing code that is related by call graph, data flow, or implicit contract — but not related by file location or line proximity.

### The Spectrum of Detectability

Not all semantic conflicts are equally invisible. They fall along a spectrum based on how far downstream the failure manifests:

**Compile-time detectable.** One branch renames a function; the other adds a call using the old name. Git merges cleanly, but the compiler catches it. In statically typed languages, a meaningful subset of semantic conflicts manifest as type errors or unresolved references after the merge. This is one of the underappreciated safety benefits of strong type systems — they act as a second layer of conflict detection after Git's textual merge. Dynamic languages lose this safety net entirely.

**Test-detectable.** The merged code compiles but produces wrong results that an existing integration test catches. This requires that your test suite exercises the specific interaction created by the merge — not just the behavior of each branch in isolation. Most test suites do not have this property, because tests are typically written to validate the change being made, not to validate the interaction between that change and an unknown concurrent change.

**Silently incorrect.** The merged code compiles, passes all tests, and produces subtly wrong behavior in production. The discount example above falls here if the test suite only validates the checkout flow with mocked discount values. These are the conflicts that produce the bugs you spend days tracking down, because nothing in the commit history or the merge record suggests anything went wrong.

### Why Semantic Conflicts Happen in Different Files

The most counterintuitive property of semantic conflicts is that they almost always involve changes in different files or in well-separated regions of the same file. This is precisely why Git cannot detect them — Git's auto-resolution works perfectly when changes don't overlap textually.

The root cause is that **code has coupling that text does not**. A function's callers are semantically coupled to its contract, but textually they exist in completely different locations. A configuration value is semantically coupled to every code path that reads it, but those code paths may be spread across dozens of files. When one branch changes the source of that coupling (the function contract, the config schema, the database column meaning) and another branch adds or modifies a consumer of it, Git sees two non-overlapping text changes and combines them without hesitation.

## Where This Breaks in Practice

### The Clean Merge Trap

Teams that judge merge safety by the absence of textual conflicts are operating with a false signal. A merge that completes cleanly provides zero information about semantic correctness. The confidence should come not from Git's merge result, but from what runs after it: the CI pipeline on the merged commit, the integration test suite, the type checker. Teams that skip post-merge validation because "there were no conflicts" are relying on a text tool to guarantee program correctness.

### Long-Lived Branches Amplify Semantic Risk Non-Linearly

The Level 1 post described how long-lived branches create "integration hell." The specific mechanism worth understanding is that semantic conflict risk grows non-linearly with branch lifetime. A branch that lives for two days overlaps with whatever else was merged in those two days. A branch that lives for two weeks overlaps with everything merged in two weeks — but the number of potential semantic interactions between your changes and all of those merged changes grows combinatorially, not linearly. Every new function you add can conflict with every contract change that landed on `main`. Every contract change you make can conflict with every new consumer added on `main`. This is why the pain of long-lived branches feels disproportionate to their length.

### The Test Gap

The standard advice for catching semantic conflicts is "write good tests." This is correct but insufficient. The specific gap is that branch-level testing validates each branch's changes against the codebase as it existed when the branch was created. It does not validate those changes against the concurrent changes landing from other branches.

Only tests that run against the **post-merge commit** can catch semantic conflicts, and only if those tests exercise the specific interaction that was broken. This is why CI pipelines that run the full test suite on every merge to `main` are not optional overhead — they are the primary detection mechanism for the class of bugs that Git is structurally incapable of preventing. And even then, the detection is only as good as the coverage of cross-cutting interactions, which is almost always the weakest part of any test suite.

### Refactoring as a Semantic Conflict Generator

Large refactors — renaming a widely-used function, changing a shared data structure's shape, modifying a return type's semantics — are disproportionate generators of semantic conflicts. The refactor changes a contract that many consumers depend on, and if any other branch is concurrently adding or modifying a consumer of that contract, a semantic conflict is nearly guaranteed. This is one reason atomic, well-communicated refactoring that lands quickly on the trunk is less risky than a refactoring branch that lives for a week. The faster the contract change lands, the smaller the window for concurrent work to be written against the old contract.

## The Model to Carry Forward

Git is a text merge tool. It guarantees textual consistency — that the bytes in the merged file represent a coherent combination of both sides' textual changes. It provides zero guarantees about semantic consistency — that the merged program does what either author intended.

This means there are two entirely separate categories of merge risk, and they require different defenses. Textual conflicts are handled by Git itself — they force human resolution and are therefore self-limiting. Semantic conflicts pass through Git undetected and must be caught by everything downstream: compilers, type checkers, test suites running on the post-merge commit, integration environments, and ultimately code review of the merge itself. The most important conceptual shift is this: a clean merge is not a safe merge. It is an unvalidated merge. Safety comes from what you build after the merge tool finishes.

## Key Takeaways

- A textual conflict means Git detected overlapping changes to the same lines and refused to guess — this is the merge tool working correctly, not a failure of your workflow.
- Git's three-way merge compares both branch tips against their common ancestor; it auto-resolves when changes affect different text regions, regardless of whether those regions are semantically related.
- Semantic conflicts occur when Git merges cleanly but the combined code is logically incorrect — these are more dangerous than textual conflicts precisely because no tool flags them at merge time.
- Statically typed languages provide a partial safety net against semantic conflicts by catching type errors and unresolved references in the post-merge compile step; dynamic languages offer no equivalent automatic detection.
- Tests written to validate a single branch's changes do not protect against semantic conflicts — only tests run on the post-merge result that exercise cross-cutting interactions can catch them.
- Semantic conflict risk grows non-linearly with branch lifetime because the number of potential interactions between your changes and concurrent changes is combinatorial.
- Large refactors that change widely-used contracts are disproportionate sources of semantic conflicts and should land on the trunk as quickly as possible to minimize the window of divergence.
- A merge that completes without conflict markers provides no information about semantic correctness — post-merge CI, not merge cleanliness, is your actual safety signal.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Many engineers learn to fear the red, noisy kind of merge problem: Git stops, shows conflict markers, and forces a decision. But that visible interruption is usually the safer case. The more expensive failures are the quiet ones: the merge succeeds, CI is weak or skipped, the code still runs, and a contract mismatch or broken assumption leaks into production. Those bugs are hard to trace because the merge itself looked normal.

If you do not have a clear model of what Git is actually checking during a merge, you will treat “merged cleanly” as evidence of safety when it is not. That leads teams to trust the wrong signal, underestimate long-lived branch risk, and miss why post-merge validation exists at all. In practice, this shows up as regressions after refactors, features that worked on each branch but break together, and production defects that seem to come from nowhere because no explicit merge conflict ever appeared.

## What You Need To Know First

**1. A Git commit is a snapshot, not a list of edits.**  
Git stores the state of the project at a point in time. When you merge, Git is comparing snapshots and inferring changes between them. That matters because merge behavior is based on differences between versions of files, not on your intent while editing them.

**2. A branch is just a line of commits that diverged from another line.**  
When two branches split, each can evolve independently. The longer they stay apart, the more each branch accumulates changes made without knowledge of the other. Merging is the act of reconciling those two histories back into one codebase.

**3. A function or interface has a contract.**  
A contract is the behavior other code relies on: what a function returns, what arguments it expects, what a config field means, what shape some data has. Code in different places can be tightly connected through that contract even if the text is far apart.

**4. CI, compilers, type checkers, and tests are different kinds of validation.**  
Git answers a narrow question: can these text changes be combined? A compiler checks whether the combined program is structurally valid. A type checker catches some interface mismatches. Tests check behavior for the cases they cover. These are separate layers, and they catch different failure modes.

## The Key Ideas, Connected

**Git does not merge “two branches”; it merges two branch tips relative to a shared base.**  
The core mechanism is a three-way merge. Git looks at the most recent common ancestor of the branches, then asks: what changed from that base to branch A, and what changed from that base to branch B? It then tries to apply both sets of changes to the base result. This matters because merge behavior depends on how each branch changed relative to the shared starting point, not just on how the two branch tips differ from each other.

**Because Git works from diffs against the base, it can auto-resolve many cases without asking a human.**  
If only one branch changed a given region, Git can safely take that change. If neither changed it, Git keeps the base version. The only time Git must stop is when both branches changed the same region and Git cannot choose one without discarding the other. That is what creates the familiar textual conflict. This leads directly to the next idea: what counts as “the same region” is much narrower than many engineers assume.

**Git’s notion of conflict is textual, not semantic.**  
Git operates on lines and hunks of text. It does not know that two files participate in the same workflow, that one function calls another, or that a return value changed meaning. So when we say Git found no conflict, we mean only that the two sets of text edits did not overlap in a way the merge algorithm considers ambiguous. Once you see that, an important consequence follows: a clean merge says nothing about whether the combined program still makes sense.

**Textual conflicts are the safe failure mode because Git is refusing to guess when line-level edits overlap.**  
When Git inserts conflict markers, it is signaling the boundary of its competence. It found overlapping edits and stopped before silently choosing a result. That is annoying for flow, but good for correctness, because a human is forced to inspect the code at the exact point where automatic line-based merging became unreliable. This sets up the contrast with the more dangerous case: problems Git cannot even see.

**Semantic conflicts happen when the text merges cleanly but the meaning of the program breaks.**  
Suppose one branch changes what a function returns, and another branch adds a new caller written against the old behavior. The edits may be in different files, so Git merges them happily. But the caller is now using the function under the wrong assumptions. The breakage comes from a mismatch in meaning, not an overlap in lines. This is why semantic conflicts are often silent: the merge tool never had enough information to flag them.

**Semantic conflicts exist because code is coupled by behavior, not by file position.**  
A function and its callers are related through call graphs and contracts. A config schema and the code that reads it are related through shared interpretation. A database field and the business logic using it are related through meaning. Those relationships are real in the running system, but invisible to a text merge algorithm. Therefore two changes can be strongly connected in the program while being far apart in the source tree. Once you understand that, it becomes clear why many of the worst merge bugs involve different files, not the same lines.

**Whether a semantic conflict is caught depends on what validation runs after the merge.**  
Some semantic conflicts become compile errors: a renamed function, a changed type, a removed field. Statically typed languages catch more of these because the type system turns some meaning changes into structural failures. Other semantic conflicts only show up in tests, and only if the tests exercise the exact cross-branch interaction that broke. And some pass everything and fail only in production. This means the real safety system is downstream of Git: compiler, type checker, integration tests, runtime observation.

**That is why a clean merge is not a safe merge; it is merely an unresolved merge that produced text successfully.**  
If Git only guarantees textual consistency, then the absence of conflict markers is not evidence of semantic correctness. The merge result still needs to be validated as a program. This shifts where confidence should come from: not from “Git accepted it,” but from “the merged commit was built, checked, and exercised.” That naturally leads to why branch lifetime matters so much.

**Long-lived branches increase semantic conflict risk because they increase the number of unseen interactions.**  
A short-lived branch only has to reconcile with a small amount of concurrent change. A long-lived branch must reconcile with everything that landed while it was away. More importantly, the number of possible interactions between your branch’s contract changes, new consumers, refactors, and other teams’ changes grows quickly as the divergence window expands. The pain feels disproportionate because it is: each additional day can add many new possible combinations, not just one more change to read through.

**Refactors are especially risky because they change shared contracts many parts of the system depend on.**  
If a refactor changes the meaning of a function, renames widely used symbols, or reshapes shared data, it creates many opportunities for other in-flight work to be written against the old world. Git will not connect those consumers to the changed contract unless they touch the same lines. So large refactors on long-lived branches are strong generators of semantic conflict. The practical consequence is that refactors are safer when landed quickly and centrally, with as little divergence window as possible.

## Handles and Anchors

**1. Git is a text traffic cop, not a program reasoner.**  
It can tell when two cars are trying to occupy the same lane at the same spot. It cannot tell whether both cars are driving toward a bridge that is out. “No collision at the intersection” is not the same as “the trip is safe.”

**2. A clean merge means “the edits fit together on the page,” not “the behaviors fit together in the system.”**  
If you remember one sentence, remember that one. It captures the core mismatch between what Git validates and what engineers often assume it validates.

**3. Ask this question after any merge-sensitive change: “What else depends on the meaning of this, even if it lives somewhere else?”**  
That question pulls your attention away from file locality and toward contracts, callers, schema consumers, and hidden coupling—the places semantic conflicts actually come from.

## What This Changes When You Build

**An engineer who understands this will treat post-merge CI as the real safety check, because Git only proves textual mergeability.**  
The unaware engineer sees “merged cleanly” and may skip or weaken validation, especially for low-drama changes. The consequence is that semantic conflicts survive until staging or production. The aware engineer insists on building and testing the merged commit itself, not just the branch in isolation.

**An engineer who understands this will prefer shorter-lived branches because branch lifetime increases the number of unseen semantic interactions.**  
The unaware engineer thinks long-lived branches are mainly a convenience tradeoff with an occasional painful rebase. The aware engineer sees them as semantic risk multipliers: every extra day increases the chance that some contract, schema, or shared assumption changed elsewhere.

**An engineer who understands this will be cautious with refactors that change contracts, because the danger is in downstream consumers Git cannot see.**  
The default move is to perform a broad refactor on an isolated branch for days, then merge when “everything on the branch passes.” The consequence is a high chance of silently breaking concurrent work written against the old contract. The better approach is to land contract changes quickly, stage compatibility where possible, and communicate the migration window clearly.

**An engineer who understands this will design tests around interactions, not only around individual changes.**  
The unaware engineer writes tests that prove “my branch works against the world as I branched from.” That misses cross-branch combinations. The aware engineer asks: what existing callers, flows, integrations, or assumptions could this change invalidate after merge? That leads to more integration tests and fewer mocks around the exact seams where semantic conflicts tend to hide.

**An engineer who understands this will read “no conflict” as absence of one class of problem, not as evidence that no problem exists.**  
The default interpretation of a smooth merge is confidence. The better interpretation is narrower: Git found no overlapping line edits requiring human arbitration. That mental shift changes review behavior, release confidence, and how teams talk about merge risk.

</details>
