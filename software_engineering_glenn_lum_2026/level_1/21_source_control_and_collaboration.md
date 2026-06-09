## Metadata
- **Date:** 01-01-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# 2.1 Source Control and Collaboration

Source control is foundational enough that most developers take it for granted, but there is a significant gap between using Git to save your work and using Git as a precision tool for collaborative engineering. The core idea is simple: every change to every file in your system is recorded, attributed, and reversible. But the operational implications run much deeper.

The concept of a **branching strategy** describes how a team organizes parallel work. In **trunk-based development**, developers commit to a single shared branch (the trunk or main branch) continuously, using feature flags to hide incomplete work from users. This approach keeps integration costs low because conflicts are discovered immediately rather than accumulating over time. In **GitFlow**, developers work on long-lived feature branches that are merged back to a development branch and then to a release branch on a schedule. This gives teams more isolation but creates "integration hell" when branches diverge significantly. The choice between these strategies has direct consequences for your CI pipeline: trunk-based development requires your CI to be fast and reliable enough to run on every commit, while long-lived branches shift that cost to infrequent but painful merges.

**Code review and the pull request process** is not just a quality gate; it is the primary mechanism for knowledge distribution across a team. A code review ensures that at least one other person understands every change that enters the codebase. This matters operationally because it means that when something fails at 2am, the person being paged is not the only person who knows how that system works. Good code review culture treats the review as a collaborative conversation, not a performance evaluation, and is explicit about whether feedback is blocking or advisory.

**Commit hygiene** matters more than most developers think. An "atomic commit" is a commit that makes one coherent, complete change. It passes tests. It does not mix refactoring with feature additions. It has a clear message that describes *why* the change was made, not just *what* was changed. The reason this matters operationally is that your commit history is a debugging tool. When you need to identify which change introduced a regression (using `git bisect`, for example), a history of clean, atomic commits can turn a four-hour investigation into a fifteen-minute one. A history of "WIP", "fix", and "asdasd" commits provides no leverage at all.

**The monorepo versus polyrepo decision** is an architectural choice about your source control topology that has deep implications for team workflow, CI pipeline design, and dependency management. A monorepo places all services and shared libraries in a single repository. This makes cross-cutting changes (updating a shared library that dozens of services depend on) straightforward, ensures that every change is visible and reviewable in one place, and allows a single CI system to understand the dependency graph and only rebuild what actually changed. The challenge is that this requires sophisticated build tooling to avoid running every service's tests on every commit. A polyrepo gives each service its own repository, providing clean ownership boundaries and simpler per-service CI pipelines, but making coordinated changes across services operationally painful and making it harder to maintain consistency in tooling and standards across teams.

**The "Everything as Code" principle** extends source control beyond application code. Infrastructure definitions, CI pipeline configurations, database schema migrations, environment configuration, documentation, and even security policies should all live in version control. This turns the repository into a complete, auditable record of the entire system: not just what the code does, but how it is built, where it runs, how it is secured, and how it has changed over time.

## Level 2 candidates

### 2.1 Source Control and Collaboration

**The Git Object Model: Commits, Trees, and Refs**

How Git stores content as a directed acyclic graph of immutable objects, what a commit actually contains, and how branches and tags are just pointers to commit objects. It matters because every Git behavior that seems mysterious — rebasing, cherry-picking, detached HEAD — is completely predictable once you understand the object model.

**Branching Strategies: Trunk-Based Development vs GitFlow**

The spectrum from a single shared main branch with short-lived feature branches to long-lived release branches with multiple integration points, including the effect of each on integration frequency, merge conflict rate, and CI effectiveness. It matters because the branching strategy is the single most consequential decision for how smoothly a team integrates code, and choosing the wrong one undermines CI regardless of tooling.

**Merge Strategies: Merge Commits, Rebase, and Squash**

What each merge strategy does to the commit history, what information is preserved or lost, and how the history model affects the ability to bisect bugs or understand the evolution of a codebase. It matters because history is a diagnostic and audit tool and a poorly maintained history is one that cannot be used to understand what changed and when.

**The Pull Request as a Quality Gate**

What a code review is designed to catch versus what it actually catches in practice, the difference between review as ceremony and review as a genuine quality signal, and what makes feedback effective. It matters because code review is the primary human gate in a CI workflow and teams that do it poorly generate bottlenecks without generating quality.

**Conflict Resolution: Textual vs Semantic Conflicts**

How a merge conflict arises, the difference between a conflict that Git cannot auto-resolve and one it auto-resolves incorrectly, and why semantic conflicts are the more dangerous class. It matters because undetected semantic conflicts produce bugs that tests do not catch, and understanding the difference shapes how you structure commits and review merges.

**Monorepo vs Polyrepo: Repository Structure as an Architectural Decision**

How keeping all services in a single repository versus separate repositories affects team autonomy, dependency management, build tooling complexity, and the granularity of access control. It matters because this decision is expensive to reverse and has downstream implications for CI/CD pipeline design and artifact management.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Modern software teams are rarely blocked by writing code in isolation. They are blocked by coordinating change: multiple people editing related systems, releasing under time pressure, debugging regressions, and keeping infrastructure, application logic, and delivery pipelines in sync. Source control exists to make change manageable, but the real engineering challenge is not “how do I save versions of files?” It is “how do we make constant change safe, understandable, and reversible across a team?”

When teams treat Git as a backup button instead of a collaboration system, predictable problems show up. Merges become painful because work drifted too far apart. Reviews become shallow because the change is too large to understand. Debugging takes hours because commit history is noisy and uninformative. Operational knowledge gets trapped in one person’s head. In other words: the codebase may still function, but the team’s ability to evolve it slows down.

That is why this topic matters. Source control and collaboration practices shape integration cost, incident response, release speed, and even how knowledge spreads through a team. The article is really about turning version control from passive storage into an active engineering control surface.

## What You Need To Know First

**1. Commit**

A commit is a saved snapshot of changes with an identity, timestamp, and message. The important part here is not just that it saves code, but that it creates a named point in history you can inspect, compare, revert, and reason about later.

**2. Branch**

A branch is a line of development that lets work continue separately from another line for a while. You can think of it as “a place to make changes without immediately mixing them into the main shared version.” The article assumes you understand that branches are useful, but asks you to care about *how long* they live and *when* they are merged.

**3. Continuous Integration (CI)**

CI is the automated process that checks whether changes still build, pass tests, and meet other quality checks. For this article, the key idea is that CI is what makes frequent integration safe. Without reliable CI, merging often becomes risky.

**4. Pull Request / Code Review**

A pull request is a proposed change, and code review is the team process of examining that change before it is merged. You do not need the platform details here. What matters is that review is both a correctness check and a way of making sure knowledge about the system is shared.

## The Key Ideas, Connected

**Source control is not just a history of files; it is a system for managing team change.**

The article starts from a familiar fact — Git records changes and lets you reverse them — but pushes beyond that. The real value is operational: who changed what, why it changed, how safely it can be merged, and how quickly the team can recover when something goes wrong. Once you see source control as a coordination system, the next question becomes: how should teams structure parallel work inside it?

**A branching strategy is really a strategy for controlling integration cost.**

Teams always have multiple changes happening at once, so they need a pattern for how those changes live in branches and when they come back together. The article contrasts trunk-based development with GitFlow not as a style preference but as a tradeoff in *when* pain is paid. That leads naturally to the next idea: the longer work stays apart, the more likely divergence becomes a problem.

**Trunk-based development keeps branches close to reality by integrating constantly.**

In trunk-based development, people merge into the shared main branch continuously and use feature flags to keep incomplete work hidden from users. The important meaning is not “everyone works on main” in a simplistic sense; it is “the system is brought back together so often that conflicts are found early.” That reduces the size and uncertainty of integration events. But if you merge constantly, you need something to catch breakage immediately — which is why this model depends on strong CI.

**Long-lived branches buy isolation now by increasing integration risk later.**

GitFlow and similar approaches separate work for longer periods, which can feel safer because unfinished work is isolated. But that isolation has a cost: the branch drifts away from the current state of the system, so merging later is harder technically and mentally. The article calls this “integration hell” because the eventual merge is no longer about one change — it is about untangling many changes that evolved independently. This sets up an important conclusion: your branching model and your CI design are tightly linked.

**Your CI pipeline has to match your branching strategy, because CI is how integration discipline becomes real.**

If a team practices trunk-based development, CI must be fast and trustworthy enough to run on every commit, otherwise frequent merging just means frequent breakage. If a team uses long-lived branches, they may reduce the need for constant CI on the shared branch, but they are storing up harder merge and verification work for later. So the branching choice is not just about developer preference; it changes the shape of your automation and where failure is discovered. Once changes can be merged safely, the next question is how teams make sure those changes are understood by more than one person.

**Code review is not only a gate on quality; it is a mechanism for distributing system knowledge.**

A lot of teams talk about review as defect detection: someone checks whether the code is correct. The article expands that view. Review also ensures that at least one additional person understands each change entering the codebase. That matters during incidents, maintenance, and future feature work, because the system is less likely to become “owned” by a single person. If review is about shared understanding, then the way changes are packaged starts to matter a lot.

**Small, coherent changes make review effective; messy changes turn review into guesswork.**

If one pull request mixes refactoring, bug fixes, config churn, and a new feature, the reviewer cannot tell what matters, what is risky, or what should be discussed. That is why the article emphasizes commit hygiene. For review to actually spread knowledge, the unit of change must be understandable. This leads directly to the idea of the atomic commit.

**An atomic commit is one complete thought captured in a form you can trust.**

An atomic commit makes one coherent change, passes tests, and does not bundle unrelated work together. The message should explain why the change exists, not just mechanically describe the edit. In practice, this means a future engineer can inspect that commit and understand its purpose quickly. That matters because history is not just for archaeology — it is used actively in debugging. Which brings us to the next step.

**Clean history turns version control into a debugging tool, not just a storage log.**

When a regression appears, tools like `git bisect` help narrow down the change that introduced it. But that only works well if each commit is meaningful and self-contained. If the history is full of vague “WIP” commits or mixed changes, the search may still find a commit, but that commit tells you little. So commit hygiene is really about preserving diagnostic leverage. Once you see the repository as an operational tool, the article broadens the scope from individual commits to repository structure itself.

**Repository topology changes how teams coordinate architecture-level change.**

The monorepo versus polyrepo discussion is about more than folder layout. It asks: where does the boundary of coordination live? In a monorepo, many services and shared libraries live together, so cross-cutting changes are easier to make and easier to review in one place. In a polyrepo, each service has clearer ownership and simpler local workflows, but coordinated changes across services become harder. This means repository structure affects not only code organization but also CI design, dependency management, and team interaction patterns.

**A monorepo centralizes visibility and coordination, but demands smarter tooling.**

Because everything lives together, a monorepo can support dependency-aware builds and make large coordinated changes straightforward. But without sophisticated tooling, every commit risks triggering too much work. The key idea is that monorepos shift complexity away from cross-repository coordination and into build/test infrastructure. That naturally contrasts with polyrepos.

**A polyrepo simplifies local ownership, but pushes coordination costs to the edges.**

Separate repositories make it easier to assign responsibility and run per-service pipelines. But if one shared library changes and many services must update, the work becomes fragmented across repositories and teams. So polyrepos reduce some forms of complexity by increasing others. At this point, the article makes its broadest move: if the repository is such a powerful coordination mechanism, why limit it to application code?

**“Everything as Code” means version control should describe the whole operating system of the team, not just the app.**

Infrastructure definitions, CI configuration, schema migrations, docs, environment config, and security policies all affect how the system behaves in production. If they live outside version control, important parts of reality become invisible, hard to audit, and easy to drift. Putting them in the repository makes change reviewable, attributable, and reproducible. This is the article’s endpoint: source control becomes the authoritative record of both the software and the conditions under which that software is built, deployed, and operated.

## Handles and Anchors

**1. Branching strategy is “when do we pay the integration bill?”**

That is the simplest way to hold trunk-based development versus long-lived branches in your head. Trunk-based pays continuously in small amounts. Long-lived branching defers payment, but the final bill is larger and more chaotic.

**2. Good commit history is a lab notebook, not a scratch pad.**

A scratch pad is full of partial thoughts that made sense only while you were writing them. A lab notebook records what changed and why in a way someone else can follow later. If your commit history reads like notes to your future self during panic, it will fail when your future teammate needs it most.

**3. Code review is team memory being written in real time.**

Do not think of review only as inspection. Think of it as the mechanism by which the codebase stops being private knowledge. If a change is merged without shared understanding, the team has gained code but not capability.

## What This Changes When You Build

- **An engineer who understands this will choose branch lifetime deliberately, because branch duration is really a decision about where integration pain shows up.**
    
    They will not say “we use GitFlow” or “we use trunk-based” as a cultural default. They will ask whether their CI is fast enough for constant integration, whether feature flags are available, and whether the team can tolerate late-stage merge complexity.
    
- **An engineer who understands this will keep pull requests smaller, because review quality collapses when a reviewer has to evaluate too many different kinds of change at once.**
    
    They will separate refactoring from feature work, avoid giant “everything touched” PRs, and optimize for a reviewer being able to answer: what changed, why, and what risk did this introduce?
    
- **An engineer who understands this will write atomic commits, because they know commit history is part of the production debugging toolkit.**
    
    When making changes, they will ask: if this causes a regression next week, will this commit help us isolate and explain it? That changes how they stage files, how often they commit, and how carefully they write commit messages.
    
- **An engineer who understands this will evaluate monorepo versus polyrepo based on coordination patterns, not ideology.**
    
    If the organization makes frequent cross-service changes or relies heavily on shared libraries, they will recognize the value of a monorepo plus dependency-aware CI. If services are truly independent and ownership clarity matters more, they may prefer polyrepos and accept the coordination overhead.
    
- **An engineer who understands this will put infrastructure, pipeline config, migrations, and security-relevant settings under version control, because unmanaged operational state creates invisible system behavior.**
    
    They will treat “how the system runs” as part of the system itself, which changes how deployments are reviewed, how incidents are investigated, and how environments are reproduced.

</details>
