## Metadata
- **Date:** 25-06-2026
- **Source:** 09_collaborative_workflows.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-09 · Collaboration Workflows

Most arguments about Git workflows are not really about Git. When two engineers disagree about whether the team should rebase or merge, whether feature branches should live for a day or a sprint, or whether Gitflow is "right" for the project, they almost never reach resolution — and the reason is that they're not actually arguing about the same thing. One person is talking about how the commit graph should look. The other is talking about how often the team should be able to ship. A third, listening in, is thinking about how code review fits into their CI pipeline. All three are using the vocabulary of Git, but the disagreement lives somewhere else entirely.

The clarifying move is to notice that Git itself has no opinion about any of this. Git gives you a small set of primitives — cheap branches, three-way merges, rebases that replay commits onto new bases, remotes that are just other repositories — and it stops there. It does not know what a "feature" is. It does not know what "main" means or that it should be protected. It does not know about pull requests; those are a GitHub invention layered on top. Every "workflow" you've ever heard named is a convention built on these primitives by humans who needed to coordinate with other humans, and the convention encodes a specific bet about how the team wants to release software, review code, and recover from mistakes.

Once you see this, the named workflows stop being competing religions and start being legible as different points on a tradeoff surface. Feature branching — the baseline almost everything else extends — bets that work should be isolated until it's ready, and that integration is a deliberate event. Trunk-based development bets the opposite: that long-lived branches are themselves the problem, that integration should happen constantly (often many times a day), and that the way you protect unfinished work from users is feature flags in the code, not isolation in the version control system. These aren't different uses of Git; they're different theories of how a team should coordinate, with Git as the substrate underneath.

Gitflow, popularised by Vincent Driessen in 2010, is the most instructive example because its decline tells you something. It prescribes a heavyweight set of long-lived branches — develop, release, hotfix, feature, master — each with strict rules about what merges where. It made sense for a world of quarterly, packaged releases where a "release" was a discrete, ceremonial event. As release cadence sped up toward continuous deployment, the overhead of maintaining all those branches stopped paying for itself, and most teams quietly migrated to something simpler. The workflow didn't become wrong; the underlying release model it was designed for became rare. That's the pattern you should be watching for whenever a workflow gets debated: what release cadence and review philosophy does it actually assume, and does that match what your team is doing?

Pull requests deserve a specific callout, because they are probably the single biggest source of confusion about what "Git" is. A pull request is not a Git concept. It is a feature of GitHub, GitLab, Bitbucket, and similar platforms — a structured UI for proposing changes, gathering review comments, running CI, and gating a merge. Underneath, the Git operations the platform invokes when you click "merge" are exactly the same primitives you could run from the command line: a fast-forward, a merge commit, a squash, or a rebase-and-merge. This matters because the platform's UI hides those choices behind a button, and teams routinely adopt a "merge strategy" without realising they've made a permanent decision about what their commit graph will look like. The platform is opinionated. Git isn't.

The same separation applies to monorepo versus polyrepo decisions, which often get framed as a workflow choice but are really an organisational one. The repository structure changes which Git features stop being optional — at sufficient scale, sparse checkout and partial clone go from curiosities to load-bearing — but the question of whether to have one repo or many is driven by how the org wants to share code, coordinate releases, and define ownership. Git will accommodate either; it just won't tell you which to pick.

The practical skill this builds is the ability to walk into a Git workflow disagreement and translate it back to the actual question underneath. When someone insists on squash merges, ask what they want the history to look like and why — usually it's about making `main` bisectable, or about hiding messy work-in-progress commits from reviewers, both legitimate goals you can now evaluate directly. When someone advocates for trunk-based development, ask about their release cadence and their feature-flag infrastructure, because trunk-based without flags is just chaos. When someone wants Gitflow, ask whether their release model actually looks like the one Gitflow was built for. The point isn't to win the argument; it's to stop having an argument about Git when the disagreement is somewhere else.

The deeper payoff is that you stop treating your current team's workflow as how Git works. It isn't. It's how your team has decided to coordinate, encoded in Git commands. When you join a new team with different conventions, you'll be able to learn their workflow as a set of social choices with stated tradeoffs, not as a new dialect of a tool you thought you already knew.

## Level 2 candidates

**Feature branching** — Covers the baseline isolation pattern: develop a unit of work on a branch, integrate it deliberately via merge or PR. Worth a deeper look because nearly every other workflow is a variation on or reaction to this default, and the specific decisions inside it (branch lifetime, naming, integration cadence) shape everything downstream.

**Trunk-based development** — Covers the high-velocity alternative where branches stay extremely short-lived or don't exist at all, with feature flags handling the isolation that branches would otherwise provide. Worth descending into because the model only works if you understand the supporting infrastructure (flags, CI, fast rollback) it implicitly requires.

**Gitflow and its decline** — Covers Driessen's 2010 model in concrete detail: the develop/release/hotfix/feature branch structure and the rules connecting them. Worth a deeper look as a historical artifact that explains why so many teams still have leftover branch conventions whose original justification is gone.

**Pull/merge requests as a platform feature** — Covers what GitHub, GitLab, and Bitbucket actually do when you click "merge," and how their merge-strategy options map onto raw Git operations. Worth descending into because the platform UI obscures real choices about your commit graph, and most teams adopt defaults without realising they've made a permanent decision.

**Monorepo vs polyrepo implications** — Covers how repository scale and structure change which Git features become mandatory rather than optional, and how the choice interacts with code-sharing, release coordination, and ownership models. Worth a deeper look because the tradeoffs are organisational as much as technical, and the Git-side consequences (sparse checkout, partial clone, submodules) only become legible once you've seen the org-side drivers.

---

## Original Content

#### L1-09 · Collaboration Workflows
The actual day-to-day shape of "how a team uses Git" — feature branches, pull/merge requests, trunk-based development, Gitflow — isn't dictated by Git itself; Git only provides the primitives (cheap branches, merges, rebases). The workflow layer is a social and process decision built on top, and most of the friction engineers feel in "Git workflow" disagreements is really a disagreement about release cadence, code review philosophy, or CI design wearing Git's clothing. Seeing this separation clearly is what lets you evaluate a team's chosen workflow on its actual merits instead of treating it as Git's mandate.