## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers interact with Git as if it were a timeline. You make changes, you commit them, the log shows a sequence of events. Branches feel like parallel timelines. Merging feels like combining timelines. This metaphor works right up until it doesn't — and then everything becomes confusing at once. Why does rebasing "rewrite history" when you didn't change any files? Why does `git cherry-pick` sometimes produce a commit with a different hash even though the code diff is identical? Why does checking out a tag put you in "detached HEAD" state, and what exactly is detached about it?

The confusion is never about the commands. It is about the data model underneath. Git is not a timeline system. It is a content-addressed object store that forms a directed acyclic graph, with a thin layer of mutable pointers on top. Once you see that structure clearly, every Git behavior becomes mechanical and predictable. This post is about seeing that structure.

## The Four Object Types

Git's entire storage model is built from four kinds of objects: **blobs**, **trees**, **commits**, and **annotated tags**. Every object is immutable, identified by the SHA-1 hash of its contents, and stored in the `.git/objects` directory. That's it. There is no other storage mechanism for your repository's content.

### Blobs: Content Without Identity

A **blob** (binary large object) stores the contents of a single file. Not the filename. Not the permissions. Not the path. Just the raw bytes, prefixed with a header indicating the object type and size, then hashed.

This means if two files in your repository have identical contents — say, two different `LICENSE` files in two different directories — Git stores one blob. The hash is derived from content alone, so identical content always produces the same object. You can verify this:

```bash
echo "hello" | git hash-object --stdin
# ce013625030ba8dba906f756967f9e9ca394464a
```

Run that on any machine, any repository. Same input, same hash. This is content-addressing: the address (hash) is derived from the content itself.

### Trees: Directory Snapshots

A **tree** object represents a single directory. It contains a list of entries, where each entry has a mode (file permissions), a type (blob or tree), a hash, and a filename. A tree entry pointing to another tree is how Git represents subdirectories.

A simplified tree might look like:

```
100644 blob a1b2c3d4...  README.md
100644 blob e5f6a7b8...  main.py
040000 tree 9c8d7e6f...  src/
```

The tree does not know where it lives in the hierarchy. It does not know its own name. Its parent tree is the one that holds an entry pointing to it with a name like `src/`. This is the same principle as blobs — trees are defined entirely by their contents, so two directories with identical structures and identical files produce the same tree hash.

Here's the critical insight: a tree object is a **complete snapshot** of a directory at a point in time. Git does not store diffs between versions of files. It stores whole snapshots. When you change one file and commit, Git creates a new blob for that file, new tree objects for every directory in the path from root to that file, and reuses every other existing blob and tree object unchanged. This structural sharing is what makes snapshots storage-efficient despite being conceptually complete.

### Commits: Snapshots With Context

A **commit** object contains exactly five things:

```
tree 4b825dc642cb6eb9a060e54bf899d15643e26f72
parent 8e4f0c9d... (zero, one, or more)
author Jane Doe <jane@example.com> 1700000000 -0500
committer Jane Doe <jane@example.com> 1700000000 -0500
<blank line>
Refactor authentication middleware
```

The `tree` line points to the root tree object — the complete snapshot of the entire repository at this commit. The `parent` line points to the commit(s) that this commit was based on. The first commit in a repository has no parent. A regular commit has one parent. A merge commit has two or more.

This is the core of the model. A commit is not a diff. It is a pointer to a full snapshot (via the tree), combined with pointers to the previous state(s) (via parents), combined with metadata. The diff you see in `git log -p` or `git show` is *computed* at display time by comparing the commit's tree against its parent's tree. It is not stored.

Because a commit's hash is derived from all of its contents — the tree hash, parent hash(es), author, committer, timestamp, and message — changing any of these produces a different commit hash. This is why rebasing "changes history": it creates new commit objects with different parent pointers, which means different hashes, even if the tree snapshots are identical.

## The Directed Acyclic Graph

The parent pointers form a **directed acyclic graph (DAG)**. Each commit points backward to its parent(s). The direction is always backward in time. There are no cycles — a commit cannot be its own ancestor.

For a linear history, the graph is a simple chain:

```
A <-- B <-- C <-- D
```

Each letter is a commit. `D`'s parent is `C`, `C`'s parent is `B`, and so on. When you create a branch and make commits on it, the graph forks:

```
A <-- B <-- C <-- D       (main)
            \
             E <-- F      (feature)
```

`D` and `F` both have `C` as an ancestor. When you merge `feature` into `main`, Git creates a merge commit with two parents:

```
A <-- B <-- C <-- D <-- G  (main)
            \          /
             E <-- F
```

`G` points to both `D` and `F` as parents. Its tree is the merged snapshot. The entire history of your repository is this graph of commit objects, stored as immutable content-addressed objects in `.git/objects`.

The DAG structure is why Git can answer questions like "what is the common ancestor of these two branches?" efficiently. It walks the graph backward from both commits until it finds where the paths converge. This operation — finding the **merge base** — is what drives both `git merge` and `git rebase`.

## Refs: The Mutable Layer

Everything described so far is immutable. Once an object is written, it never changes. So how does Git know what `main` is? How does it know where you are in the graph?

**Refs** (references) are the answer, and they are shockingly simple. A ref is a file that contains a 40-character commit hash. That's all.

```bash
cat .git/refs/heads/main
# 9f4d3b2a1e8c7f6d5a4b3c2d1e0f9a8b7c6d5e4f
```

A branch is a ref that lives in `.git/refs/heads/`. A tag (a lightweight tag, specifically) is a ref in `.git/refs/tags/`. When you "create a branch," Git creates a 41-byte file. When you commit on a branch, Git moves that file's contents to point to the new commit. That is the entire mechanism.

**HEAD** is a special ref stored in `.git/HEAD`. Usually, it contains a symbolic reference to a branch:

```
ref: refs/heads/main
```

This means "I am currently on the `main` branch." When you make a commit, Git creates the new commit object, then updates the ref that HEAD points to so it contains the new commit's hash.

**Detached HEAD** state occurs when `.git/HEAD` contains a raw commit hash instead of a symbolic reference:

```
9f4d3b2a1e8c7f6d5a4b3c2d1e0f9a8b7c6d5e4f
```

You are no longer "on" any branch. If you make commits in this state, they are perfectly valid commit objects in the graph, but no branch ref is being updated to track them. Once you check out a branch, there is no named pointer leading to those commits. They become **unreachable** — still in the object store but not discoverable by walking from any ref. Eventually, `git gc` will delete them.

**Annotated tags** differ from lightweight tags. A lightweight tag is just a ref pointing to a commit. An annotated tag is a ref pointing to a **tag object**, which in turn points to a commit and also stores a tagger, date, and message. This is why annotated tags are preferred for releases — they carry their own metadata and are themselves content-addressed objects.

## How Operations Map to the Object Model

With this model in hand, Git operations become mechanical:

`git commit` creates a new blob for each changed file, creates new tree objects for affected directories (reusing unchanged subtrees), creates a commit object pointing to the new root tree and the current HEAD commit as parent, then updates the current branch ref to point to the new commit.

`git branch feature` creates a new file at `.git/refs/heads/feature` containing the same commit hash as the current HEAD. No objects are created. No copies are made. It is a 41-byte file creation.

`git merge feature` (assuming a non-fast-forward) finds the merge base of the current branch and `feature`, computes a three-way merge of the trees, creates a new commit with two parents and the merged tree, and advances the current branch ref.

`git rebase main` (from a feature branch) finds the merge base, takes each commit unique to the feature branch, and **replays** each one on top of `main`. "Replays" means computing the diff each commit introduced against its parent, applying that diff to the new base, and creating a **new commit object** with a new parent (the previous replayed commit or `main`'s tip) and a new tree. The new commits have different hashes. The old commits still exist in the object store but are no longer reachable from any branch ref.

`git cherry-pick abc123` does exactly what rebase does for a single commit: computes the diff that `abc123` introduced relative to its parent, applies it to the current HEAD, and creates a new commit. The new commit has a different hash because it has a different parent and likely a different tree, even though the diff is semantically identical.

## Where the Model Bites You

### The Rebase-and-Force-Push Problem

When you rebase commits that have already been pushed to a shared branch, you create new commit objects and need to force-push (`git push --force`) to overwrite the remote ref. Anyone who had the old commits checked out now has a local history that diverges from the remote — not because of content differences but because the commit objects themselves are different. Their `git pull` will try to merge two histories that share identical code changes but have different graph structures. This is the root cause of every "rebase vs. merge" team conflict, and it is entirely predictable from the object model: rebase creates new objects, and sharing objects that others have already based work on creates divergence.

### Unreachable Objects and the Illusion of Deletion

Engineers sometimes believe that `git reset --hard` or a force-push deletes commits. It does not. It moves a pointer. The commit objects remain in the object store. The **reflog** (`.git/logs/`) records every ref update, which means `git reflog` will show you the "deleted" commits for at least 90 days by default. This is your safety net — but it is a local safety net. The reflog exists only in the repository where the operation happened. A force-push to a remote does not preserve the remote's reflog for you.

### Large Files and the Snapshot Model

Because Git stores blobs of full file content (not diffs), committing a 100MB binary file means that object exists in your repository forever, even if you delete the file in the next commit. The old blob is still referenced by the old commit's tree. This is why Git repositories grow permanently when large binaries are committed, and why tools like Git LFS exist — they replace the blob with a small pointer file and store the actual content externally.

## The Model You Should Carry

Git is two layers. The bottom layer is an immutable, content-addressed object store where blobs, trees, commits, and tags are identified by hashes and linked into a directed acyclic graph. This layer only grows; nothing in it changes. The top layer is a set of mutable pointers — branches, tags, HEAD — that give human-readable names to specific points in the graph.

Every Git operation is either creating new objects in the bottom layer, moving pointers in the top layer, or both. When you internalize this, you stop thinking about Git as a timeline with magical commands and start thinking about it as a graph with named positions. Rebase does not "rewrite history" — it writes *new* history (new commit objects) and moves a pointer to it. Reset does not "delete commits" — it moves a pointer backward. A branch is not a container for your work — it is a pointer that advances as you add commits.

This two-layer model is the conceptual foundation for everything that follows: interactive rebase, the reflog, recovery workflows, the mechanics of merge conflicts, and the design of Git-based deployment pipelines. If you can reason about objects and refs, you can reason about any Git operation from first principles.

## Key Takeaways

- Git stores snapshots, not diffs — each commit points to a tree that represents the complete state of the repository, and diffs are computed at display time by comparing trees.
- Every object (blob, tree, commit, tag) is immutable and identified by the SHA-1 hash of its contents, which means identical content always produces the same hash regardless of when or where it is created.
- A branch is a 41-byte file containing a commit hash — creating a branch creates no copies, allocates no storage beyond the pointer, and costs nothing.
- Detached HEAD means `.git/HEAD` contains a raw commit hash instead of a symbolic reference to a branch, so new commits have no branch ref tracking them and will become unreachable when you switch away.
- Rebase creates entirely new commit objects with new hashes because the parent pointers change — this is why rebasing shared commits causes divergence for anyone else working from those commits.
- `git reset --hard` and force-push do not delete commits; they move pointers, and the unreachable objects remain in the object store until garbage collection runs (at least 90 days by default via the reflog).
- Git's snapshot model means large binary files permanently inflate repository size even if deleted in subsequent commits, because the blob remains referenced by the old commit's tree.
- Every Git operation reduces to creating immutable objects, moving mutable pointers, or both — if you can identify which, the operation's behavior becomes fully predictable.


# Discussion

## Why This Conversation Is Happening

Git feels simple when you stay on the happy path: commit, branch, merge, push. The trouble starts when the visible behavior stops matching the timeline story people carry in their heads. A rebase seems to "change the past" even when the code looks the same. A cherry-pick creates a "different" commit from the one you copied. A reset appears to delete work, except sometimes you can still recover it. If your model is "Git stores a sequence of changes over time," these behaviors look arbitrary.

That confusion turns into real engineering mistakes. People force-push rebased branches without understanding why teammates now see divergent history. They panic after a detached-HEAD commit because they think the work is gone. They commit large binaries, delete them later, and are surprised the repo stays huge. In each case, the command is not the real problem; the missing piece is the storage model underneath. Without that model, Git remains a bag of memorized rituals, and rituals break under pressure.

## What You Need To Know First

### 1. Hashes as content-derived IDs

A hash is a fixed-size identifier computed from data. For this article, the important part is not the math; it is the behavior: same content gives the same hash, different content gives a different hash. Git uses that property to name objects by what they contain, not by where they were created or when.

### 2. A directory tree as a nested structure

A filesystem is not just "files"; it is directories containing files and other directories. If you picture the repository as one root folder with nested subfolders beneath it, you're ready for Git trees. Git needs a way to represent both file contents and the folder structure that arranges them.

### 3. Pointers or references

A pointer is just a name that tells you where to look. In Git, names like `main`, `feature`, and `HEAD` are references to commits. The key idea is that the named thing and the object it points to are separate: the object can stay unchanged while the pointer moves.

### 4. Parent-child relationships in a graph

A graph is just nodes connected by links. In Git, commits are nodes, and each commit links back to its parent commit or commits. You do not need graph theory here; you just need to be comfortable with "this commit came from that earlier one" and with the fact that one commit can have two parents after a merge.

## The Key Ideas, Connected

### Git is not fundamentally a timeline; it is an object store with pointers.

When people say "Git history," they often imagine a logbook of changes over time. That is useful for reading, but it is not how Git stores data. Git stores objects identified by content-derived hashes, and then keeps a small mutable naming layer on top. This matters because most "weird" Git behavior comes from the difference between immutable stored objects and movable names. Once you accept that storage and naming are separate, the next question becomes: what exactly is being stored?

### Git stores four object types, and each one has a specific job.

The article names blobs, trees, commits, and annotated tags. You can think of them as progressively richer layers of meaning. A blob is raw file content. A tree organizes blobs and subtrees into a directory snapshot. A commit points to one root tree and to earlier commit(s), adding metadata like author and message. An annotated tag adds human-facing release metadata around another object. This layering matters because it shows that Git does not start from "changes"; it starts from content and structure. That leads directly to the first surprising object type: the blob.

### A blob stores file contents only, not filename or path.

This is easy to miss because humans think in files-with-names. Git splits that apart. The bytes of the file live in a blob; the name and location live elsewhere. That is why two files with identical contents can share one blob object: if the bytes are the same, the blob is the same. Once content is separated from naming, Git needs another object to describe where that content sits in the repository structure. That is what trees do.

### A tree stores one directory snapshot by naming blobs and subtrees.

A tree is Git's representation of a directory at one moment. It says, in effect, "this directory contains an entry called `README.md` pointing to this blob, and an entry called `src` pointing to this subtree." The tree does not know its own parent directory; it only knows the entries inside it. This means repository structure is built by nesting trees. The important mechanical consequence is that if one file changes, Git does not rebuild everything. It creates a new blob for that file and new trees only along the path back up to the root, while reusing all unchanged objects. That reuse is what makes snapshots practical instead of wasteful. Once you have a complete root tree for the repository, you have enough to describe the full project state at one point in time. The next step is to attach context to that snapshot, which is what commits do.

### A commit is a snapshot plus ancestry, not a stored diff.

This is the central idea. A commit points to the root tree for the entire repository, and it points to parent commit(s). So a commit says both "here is the full project state now" and "here is where I came from." The diff you see in Git commands is computed later by comparing this commit's tree to its parent's tree. Git did not store "change lines 10-15"; it stored the full snapshot and enough ancestry to compare snapshots. This explains several behaviors at once. If the commit includes parent pointers and metadata in its contents, then changing the parent changes the commit object itself. That is exactly why rebase creates new commits.

### Because commit identity includes parent pointers and metadata, "same change" can still mean "different commit."

A commit hash is derived from all the commit's contents: tree, parent(s), author/committer info, timestamps, message. So if you take the same conceptual code change and place it on top of a different parent, you get a different commit object and therefore a different hash. Cherry-pick does this for one commit. Rebase does it for a sequence of commits. The code delta may look equivalent, but the object identity is different because the ancestry is different. Once commits point backward to parent commits, all commits together form a graph.

### Commit parent links form a directed acyclic graph.

Each commit points to earlier commit(s), so the arrows always go backward. Because a commit cannot point to itself through some loop, the structure is acyclic. In normal development, this graph often looks like a line with occasional branches and merges, which is why the timeline metaphor feels close enough at first. But the graph model is more accurate: branching is just two refs pointing into different paths through the same commit graph, and merging is one new commit with two parents. This graph structure is what allows Git to find common ancestors and perform merges or rebases mechanically. But the graph alone still does not explain how `main` or `HEAD` knows where you are. For that, Git adds a mutable naming layer.

### Refs are the mutable names that point into the immutable graph.

Everything below this layer is immutable: blobs, trees, commits, tag objects. Refs are the movable labels. A branch is just a ref whose contents are a commit hash. Creating a branch does not copy commits; it creates another name pointing to an existing commit. Making a new commit while on that branch creates a new commit object, then moves the branch ref forward to point to it. This is a huge simplification: Git is mostly "write new immutable objects, then move a pointer." Once you understand refs this way, `HEAD` becomes easier to reason about.

### HEAD usually points to a branch name, and detached HEAD means it points directly to a commit.

When `HEAD` is attached, it does not name a commit directly; it names a branch ref like `refs/heads/main`. Then new commits move that branch. In detached HEAD state, `HEAD` contains a raw commit hash instead. New commits still work, but no branch ref moves with them. So the commits exist, but nothing with a stable human name points to them after you switch away. That is why detached-HEAD work feels precarious: not because the commits are invalid, but because they are easy to make unreachable. Once you understand unreachable commits as "objects with no refs leading to them," recovery and deletion start to make sense too.

### Many Git operations are just combinations of object creation and ref movement.

This is the payoff. `git commit` creates blobs/trees/commit, then advances the current branch ref. `git branch` creates a new ref and no new objects. `git reset --hard` usually moves a ref and updates the working tree; it does not delete commit objects. `git merge` creates a new commit with two parents and advances the current branch ref. `git rebase` creates new commit objects replayed onto a different base, then moves the branch ref to the new chain. `git cherry-pick` does the same replay idea for one commit. Once you can classify an operation as "create objects," "move pointers," or both, its behavior stops being mysterious. That also explains the failure modes the article calls out.

### The painful Git surprises are direct consequences of the model, not special cases.

Rebasing shared commits hurts because rebasing does not "clean up labels"; it creates new commit objects with different identities. If others built work on the old objects, your force-push moves the shared branch ref to a different path in the graph, and now their local refs and the remote ref disagree. Large-file problems happen because blobs store whole file contents, and old commits still reference old blobs. Reset does not truly erase work because moving refs does not remove objects immediately; unreachable objects can still be found through reflog until garbage collection eventually prunes them. These are not random gotchas. They fall straight out of immutable objects plus mutable refs.

## Handles and Anchors

### 1. "Git is a warehouse plus labels."

The warehouse contains sealed boxes you never edit in place: blobs, trees, commits, tags. The labels on shelves are refs like `main` and `HEAD`. Most Git commands either put new sealed boxes into the warehouse or move labels to point at different boxes. If you remember that, rebasing and resetting become much easier to reason about.

### 2. "A commit is a photo of the whole repo, with arrows to its parent photos."

Do not picture a commit as "the patch." Picture it as a complete snapshot of the repository plus a link backward. The patch view is something Git computes by comparing two photos. This single shift explains why merges, rebases, and cherry-picks behave the way they do.

### 3. Ask: "Did this command create new objects, move refs, or both?"

This is a practical diagnostic question. If you ask it before running a Git command, you can often predict the outcome. Rebase? Both. Branch? Move/create refs only. Commit? Both. Reset? Mostly ref movement. That question turns Git from folklore into mechanics.

## What This Changes When You Build

### An engineer who understands this will approach rebasing shared branches differently because rebase creates new commit objects, not just a prettier view of the same history.

The unaware engineer sees rebase as cosmetic cleanup and force-pushes casually. The consequence is that teammates now have local branches built on old commit IDs, so pulls and merges become confusing even when the code changes are "the same." The aware engineer distinguishes between private history, where rebasing is low-risk, and shared history, where rebasing changes object identity for everyone downstream.

### An engineer who understands this will treat branch creation as cheap and disposable because a branch is only a ref, not a copy of the repository.

The unaware engineer may avoid branches out of fear that they are heavy or duplicative, or may speak as if work "lives inside" a branch. The aware engineer knows a branch is just a movable name pointing at a commit, so creating short-lived feature branches, safety branches before dangerous operations, or recovery branches from detached HEAD is nearly free.

### An engineer who understands this will recover from "lost" work by looking for moved pointers rather than assuming data was deleted.

The default panic response after `reset --hard`, bad rebase, or accidental checkout is "my commits are gone." The aware engineer knows commit objects often still exist and starts with reflog or old refs, because the likely event was pointer movement, not immediate destruction. That changes incidents from data-loss emergencies into recoverable bookkeeping problems.

### An engineer who understands this will make different repository hygiene decisions around binaries because old blobs remain part of reachable history.

The unaware engineer thinks deleting a large file in the next commit removes the cost. It does not; the earlier commit still points to the large blob. The aware engineer keeps large binaries out of normal Git history in the first place, uses Git LFS or artifact storage, and treats "accidentally committed giant file" as a history-rewrite problem rather than a normal delete.

### An engineer who understands this will reason about detached HEAD correctly because the risk is not invalid commits but unnamed commits.

The default misunderstanding is "detached HEAD means commits won't work" or "Git is in a broken state." The aware engineer knows commits made there are real commit objects; the issue is only that no branch ref advances with them. So if the work matters, they create a branch or tag before moving away. That small action turns potentially unreachable work into named, durable history.
