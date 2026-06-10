# The Working Developer (The Unwritten Curriculum) — Level 0: Course Map

> **Intent:** The published canon of software engineering teaches the craft as it should be — clean code, deep modules, well-tested systems, reliable operations. None of it describes the actual day: arriving at a codebase you didn't write, changing it under a deadline you didn't set, and getting that change past people whose agreement you need. That layer is real, it is most of the job, and it is almost never written down — it passes between engineers as folklore, war stories, and "you'll figure it out." This curriculum makes the unwritten part of the profession explicit and navigable.
>
> **Your angle:** You already do most of this. You've absorbed it through years of shipping and the scar tissue that comes with it. The value here is not learning it for the first time — it is *naming* what you half-know so it becomes deliberate instead of instinctive. A named skill can be examined, taught, and improved; an unnamed one can only be possessed unevenly. Read this to find the instincts worth trusting, and the gaps that have been quietly costing you time for years.

---

## How to use this map

The three tiers are **concentric, not sequential** — they are rings of context around a single act, *you changing code*. Tier 1 is the innermost ring: you alone with code you did not write, where the only thing that matters is comprehension. Tier 2 is the ring around it: turning an ambiguous request into shippable work under real constraints of time, scope, and attention. Tier 3 is the outermost ring: your change has to survive other people — review, persuasion, influence, and shared failure.

Almost every real task touches all three at once. A single ticket — "checkout is occasionally slow" — begins as comprehension of a system you've never read (T1), becomes a judgment about how much to invest and what to cut to hit Friday (T2), and ends as a pull request you have to get reviewed, merged, and defended when it pages someone at 2am (T3). The thing that separates a competent coder from an engineer you can hand a vague problem to is the ability to move through all three rings without dropping any of them.

Each **Level 1 topic** is a concept post: what the skill is, why it exists, and what it costs you to lack it. Each **Level 2 candidate** is a depth post: the specific move, the tradeoff, the failure mode. Descend into Level 2 only where the gap is actively slowing you down — this is a map for finding your weak spots, not a syllabus to complete.

---

## Topic Inventory

---

### Tier 1 — The Inherited Codebase
*You, alone, with code you did not write. Most of a career is spent here, and comprehension is the prerequisite for every other skill on this map. Gaps here don't feel like "I can't code" — they feel like "I've been staring at this for three hours and I still don't know where the change goes."*

---

#### L1-01 · Code Archaeology

**What it is and why it matters:** The defining fact of professional development is that you spend far more time reading code than writing it, and most of what you read is unfamiliar, undocumented, and shaped by decisions whose reasons are long gone. Code archaeology is the craft of reconstructing a system's behaviour and intent from the evidence it leaves — the call graph, the commit history, the naming, the tests, the scars. The skill is not "read carefully"; it is knowing where to look first so you build an accurate mental model in hours instead of weeks. Treating `git blame` and the commit log as an interrogable record of *why* — not just *who* — is the move that turns a confusing line into a legible decision. Engineers without this skill rewrite things that were correct, preserve things that were accidents, and are perpetually afraid of the codebase they work in.

**Level 2 candidates:**

- **L2 · Building a Mental Model Fast** — There is an order in which to read an unfamiliar system — entry points, data shapes, the one core flow — and learning it is the difference between orienting in an afternoon and flailing for a week.
- **L2 · The Commit History as Evidence** — `git blame` and `git log` answer "why is this here?" far more reliably than the code itself — drilling here turns version history from an audit trail into a reasoning tool.
- **L2 · Tracing a Request End to End** — Following one real request through every layer it touches is the single fastest way to convert an abstract architecture diagram into a model you can actually predict from.
- **L2 · Reading the Tests to Recover Intent** — Tests encode what the author believed the code should do — when documentation is absent, the test suite is the closest thing to a specification you'll find.
- **L2 · Chesterton's Fence** — Chesterton's 1929 rule — don't remove a fence until you know why it was built — is the discipline that separates engineers who clean up safely from those who break production while "tidying."
- **L2 · Identifying the Cursed Regions** — Every codebase has areas that punish anyone who touches them — learning to detect them from history, churn, and the silence of the people who own them is a survival skill no document will give you.

---

#### L1-02 · The Diagnostic Method

**What it is and why it matters:** Debugging is the part of the job that consumes the most time and is taught the least, because it looks like improvisation when it is actually a method. The reframe that unlocks it is old — debugging is the scientific method applied to a system you control: observe, hypothesise, design the cheapest test that would falsify the hypothesis, and let the result narrow the search. Most engineers debug by guessing and changing things; the skilled ones treat each change as an experiment and refuse to fix anything they cannot first explain. The highest-leverage move in the whole discipline is reliable *reproduction* — a bug you can summon on demand is already half-solved, and a bug you cannot reproduce is not yet a bug you understand. Everything downstream — bisection, instrumentation, knowing when you're lost — is an elaboration of this loop.

**Level 2 candidates:**

- **L2 · Reproduction as the First Goal** — Before fixing anything, make it happen on demand — drilling here reveals why the engineers who chase reproduction first are the ones who close the bugs everyone else gives up on.
- **L2 · Binary Search the Problem Space** — Halving the space of possible causes — across commits with `git bisect`, across the stack, across inputs — is the move that turns a hopeless search into a bounded one.
- **L2 · Reading a Stack Trace and an Error Message** — Most error output is far more informative than people treat it as — learning to read it precisely is the cheapest debugging skill to acquire and the most commonly skipped.
- **L2 · Instrumentation vs the Debugger** — Knowing when to step through with a debugger and when to add logging and watch is a judgment about feedback speed that determines how fast you converge.
- **L2 · The Hardest Bugs: Races, Heisenbugs, and Flakiness** — Non-deterministic failures break the naive debugging loop — understanding why they resist reproduction is the prerequisite for the specialised tactics that catch them.
- **L2 · Knowing When You're Lost** — There is a point where continuing alone is ego, not diligence — recognising it, and rubber-ducking or escalating before you waste a day, is a metacognitive skill the canon never mentions.

---

#### L1-03 · Safe Change Under Uncertainty

**What it is and why it matters:** The textbook assumes you understand the code before you change it; the job rarely grants you that luxury. Michael Feathers named the problem precisely in *Working Effectively with Legacy Code* (2004): legacy code is simply code without tests, and the central difficulty is that you must change it to add the tests that would have made changing it safe. The craft is a set of techniques for making controlled changes to code you do not fully understand — finding *seams* where behaviour can be intercepted, pinning current behaviour with characterization tests before you touch anything, and changing in small reversible steps so that when something breaks you know exactly what broke it. This is what lets you move confidently through a system that no living person fully understands. Without it, every change to unfamiliar code is a gamble, and the rational response — never touching anything — is how codebases calcify.

**Level 2 candidates:**

- **L2 · Characterization Tests: Pinning Behaviour Before You Touch It** — Tests that capture what the code *currently* does, right or wrong, give you a safety net for changes you couldn't otherwise make confidently — the foundational move of legacy work.
- **L2 · Seams: Where You Can Change Behaviour Without Editing It** — Feathers' concept of a seam explains how to get untestable code under test without the rewrite that would be too risky to attempt — the technique that makes the impossible change possible.
- **L2 · Small, Reversible Steps** — Changing in increments small enough to revert cleanly is what keeps a failed change from becoming a failed afternoon — understanding why granularity buys safety reframes how you sequence any risky edit.
- **L2 · The Strangler Pattern: Replacing a System While It Runs** — Fowler's strangler approach explains how large legacy systems get replaced incrementally rather than in a doomed big-bang rewrite — the strategy behind most successful migrations you'll ever see.
- **L2 · Refactoring Under a Deadline** — The honest version of refactoring is not "leave it cleaner" but "how much can I safely improve in the time I actually have" — drilling here turns a virtue into a budgeted decision.

---

#### L1-04 · Tooling as Instrument

**What it is and why it matters:** Every craft has tools the apprentice operates consciously and the master has stopped noticing, and software is no different — the gap between an engineer who *uses* git and one who *thinks* in it is enormous and almost entirely invisible from the outside. The point of this topic is not command memorisation; it is internalising the *models* underneath the tools so they become an extension of your hands rather than a source of friction. Git is the clearest example: once you understand it as a directed graph of immutable snapshots (Torvalds, 2005), every command stops being an incantation and merge, rebase, cherry-pick, and the life-saving reflog become obvious moves on a structure you can see. The same shift applies to the editor, the shell, and search — and increasingly to AI assistants, where the skill is not prompting but knowing precisely what to delegate and what you must still verify yourself. Fluency here doesn't make you a better engineer in theory; it gives you back hours a day and removes the friction that breaks concentration.

**Level 2 candidates:**

- **L2 · Git as a Graph, Not a Set of Commands** — Once you see commits as nodes in an immutable DAG, rebase and merge stop being scary and become obvious — the mental model that makes every git situation reasonable rather than memorised.
- **L2 · Recovering From Disaster: The Reflog** — Almost nothing in git is truly lost, and knowing the reflog exists is the difference between a panic and a thirty-second fix — the safety net that lets you experiment fearlessly.
- **L2 · The Shell and Search as a Force Multiplier** — Fluency with the terminal, pipes, and fast code search compounds across every task you do — drilling here is the highest-ratio time investment most engineers never deliberately make.
- **L2 · Editor Mastery: Navigation and Refactoring Moves** — The difference between typing code and *moving* through it — jump-to-definition, find-references, structural refactors — is a fluency that quietly determines how fast your inner loop runs.
- **L2 · Working With AI Assistants Without Outsourcing Judgment** — The new instrument on the bench rewards delegation of the mechanical and punishes delegation of the understanding — knowing which is which is the skill that separates leverage from liability.

---

### Tier 2 — The Economics of a Change
*Turning an ambiguous request into shippable work under constraints you didn't choose. This is the ring where engineering becomes a series of tradeoffs — time against correctness, scope against certainty, speed now against speed later — and where most of the decisions that actually determine whether you ship are made.*

---

#### L1-05 · Requirements Archaeology

**What it is and why it matters:** Almost no task arrives as a real specification; it arrives as a sentence, a screenshot, a Slack message, or a ticket that describes a *solution* someone already settled on rather than the *problem* they have. The skill is extracting the actual need from the stated request — and the canonical failure mode has a name, the XY problem: the user asks how to do Y because they believe Y will solve X, and you waste a day on Y when X had a simpler answer all along. Good engineers treat every requirement as a claim to be investigated, not an order to be executed, because building precisely the wrong thing is the most expensive mistake in the field and the easiest to avoid by asking one more question. This is where you decide *what to build*, and getting it wrong makes every downstream skill irrelevant. The move is to surface the real goal, the hidden constraints, and the unspoken acceptance criteria before a line of code is written.

**Level 2 candidates:**

- **L2 · The XY Problem** — When someone asks how to do Y, the highest-value question is often "what are you trying to accomplish?" — drilling here reveals how much rework comes from solving the problem you were handed instead of the one that exists.
- **L2 · Eliciting the Unspoken Acceptance Criteria** — Every request has success conditions the asker didn't state because they seemed obvious to them — finding them before you build is what prevents the "that's not what I meant" at the end.
- **L2 · Distinguishing the Need From the Proposed Solution** — Requests routinely smuggle in a solution; separating the underlying need from the suggested implementation is what frees you to find a better one.
- **L2 · Surfacing Hidden Constraints Early** — The deadline, the system that can't be touched, the stakeholder who must sign off — constraints discovered late are the ones that force rework, and asking for them up front is nearly free.
- **L2 · When to Stop Clarifying and Start Building** — There's a point where more questions are avoidance, not diligence — calibrating it is the judgment that keeps requirements work from becoming analysis paralysis.

---

#### L1-06 · Tactical vs Strategic Judgment

**What it is and why it matters:** Ousterhout draws the line between tactical programming (get this working now) and strategic programming (invest in a design that stays workable) as a principle in *A Philosophy of Software Design* — but on the job it isn't a principle, it's a decision you make a dozen times a day under pressure. The real skill is calibration: knowing *when* the quick path is correct and when it's a loan you'll repay with interest, and being honest about which one you're actually choosing. A throwaway script and a load-bearing module deserve opposite answers, and the engineer who applies strategic care to everything ships too slowly while the one who applies tactical speed to everything drowns in their own mess. This is the meta-decision that governs how you spend effort on every other task on this map. Mastery looks like deliberately choosing the quick-and-dirty path with full awareness of the cost, rather than defaulting to whichever mode is your habit.

**Level 2 candidates:**

- **L2 · Calibrating Investment to the Code's Lifespan** — The right amount of design depends on how long the code will live and how many people will touch it — drilling here replaces a moral instinct ("always do it right") with an economic one.
- **L2 · Recognising Load-Bearing Code** — Some code is structurally central and some is disposable, and treating them the same in either direction is costly — telling which is which up front is what makes the call correctly.
- **L2 · The Honest Shortcut** — Taking the quick path *knowing* it's a quick path, and leaving a marker, is professional; taking it by default and forgetting is how messes accrete silently.
- **L2 · Good Enough Is a Real Engineering Target** — "Good enough" is not a compromise of standards but a calibration of them to context — understanding this is what frees you from gold-plating work that doesn't warrant it.
- **L2 · The Compounding Cost of Defaulting to One Mode** — Always-tactical and always-strategic are both failure modes — seeing how each compounds over months explains why judgment, not a fixed policy, is the actual skill.

---

#### L1-07 · Scoping and Decomposition

**What it is and why it matters:** A large change made all at once is the riskiest object in software — it's hard to review, hard to test, hard to revert, and it blocks everyone until it lands. The skill of decomposition is cutting a big piece of work into a sequence of small, independently-shippable, individually-reversible steps, each of which leaves the system working. This is what makes feature flags, incremental migration, and continuous delivery possible at all, and it's the difference between a two-week branch that becomes a merge nightmare and a series of one-day pull requests that each land cleanly. The deeper move is learning to slice *vertically* — a thin end-to-end slice that delivers something real — rather than *horizontally* by layer, so value and feedback arrive early instead of all at the end. Engineers who can't decompose are forced into big-bang changes, and big-bang changes are where most disasters live.

**Level 2 candidates:**

- **L2 · Vertical Slices vs Horizontal Layers** — Slicing work end-to-end rather than layer-by-layer is what lets you ship and learn early — drilling here reveals why the "all the backend, then all the frontend" instinct delays feedback until it's most expensive.
- **L2 · Keeping the System Shippable at Every Step** — Decomposing so each increment leaves main releasable is the precondition for continuous delivery — understanding it explains why large dormant branches are a liability, not progress.
- **L2 · Feature Flags: Decoupling Deploy From Release** — Separating "the code is deployed" from "the feature is on" is the technique that makes shipping incomplete work safe — the move behind most modern incremental delivery.
- **L2 · The Cost of the Long-Lived Branch** — A branch that lives for weeks accumulates merge conflict, drift, and risk — seeing why explains the entire argument for small, frequent integration.
- **L2 · Sequencing for Early Risk Reduction** — Ordering the work so the riskiest, most uncertain part comes first means you learn whether your plan is doomed while it's still cheap to change.

---

#### L1-08 · Estimation and Forecasting

**What it is and why it matters:** Estimation is the skill engineers most resent and most need, because the business runs on it and it is genuinely, irreducibly hard — Brooks diagnosed the core of it in *The Mythical Man-Month* (1975), and the planning fallacy that Kahneman and Tversky later named explains why we're systematically optimistic even when we know better. The honest reframe is that an estimate is a probability distribution, not a promise: "two days" really means "anywhere from one to five, most likely around two," and the professional move is to communicate the uncertainty rather than hide it behind a single confident number. The skill is decomposing work until the pieces are small enough to estimate with confidence, identifying the unknowns that dominate the variance, and resisting the pressure to convert a guess into a commitment. Getting this wrong erodes trust in both directions — sandbagging makes you slow, optimism makes you unreliable — and getting it right is most of what makes a senior engineer someone the business can plan around.

**Level 2 candidates:**

- **L2 · An Estimate Is a Distribution, Not a Number** — Communicating a range with its uncertainty rather than a single figure is more honest and more useful — drilling here reframes the entire awkward ritual of being asked "how long?"
- **L2 · The Planning Fallacy and Why We're Always Optimistic** — Kahneman and Tversky's finding that we systematically underestimate our own tasks explains why padding feels like lying but is actually correction.
- **L2 · Decompose Until the Pieces Are Estimable** — The unit you can estimate is the small, well-understood task — breaking work down until you reach it is the only reliable way to improve an estimate.
- **L2 · Naming the Unknowns That Dominate the Variance** — Most estimation error comes from a few high-uncertainty unknowns — de-risking them with a spike or prototype is worth more than refining the parts you already understand.
- **L2 · Resisting the Estimate-to-Commitment Slide** — The moment an estimate is quoted back as a deadline, something has gone wrong — understanding the conversion is what lets you push back on it without seeming evasive.

---

#### L1-09 · The Inner Loop and the Cost of Context

**What it is and why it matters:** The "inner loop" is the cycle you run thousands of times a day — change something, run it, see the result — and its latency, more than almost anything else, determines how much you actually get done. A loop measured in seconds keeps you in flow and lets you experiment freely; a loop measured in minutes turns every question into an expensive commitment and quietly destroys a day's productivity through accumulated waiting. The other half of the topic is the cost of *interruption*: context — the working model of the problem you hold in your head — is expensive to build and cheap to lose, and a single ill-timed interruption can cost far more than the minutes it occupies. Understanding this is what justifies the otherwise-invisible work of speeding up your feedback loop and defending your attention, and it explains why the most productive engineers are often the most protective of uninterrupted time. The grind no one warns you about is that the job is run in this loop, and its quality is your quality of life at work.

**Level 2 candidates:**

- **L2 · Feedback Latency Is the Hidden Tax on Everything** — Every second of inner-loop latency is paid thousands of times a day — drilling here reveals why a faster test/run cycle pays back more than almost any other tooling work.
- **L2 · Context as an Expensive, Perishable Asset** — The mental model you hold while working takes real time to rebuild after it's lost — this reframes interruptions and context-switching as the costly events they are.
- **L2 · Flow and Why It's Worth Defending** — There's a state of deep focus where the work goes several times faster, and it's fragile — learning what protects and destroys it is a productivity skill disguised as a personal preference.
- **L2 · Batching the Interrupt-Driven Work** — Reviews, messages, and small asks can be batched instead of serviced live — drilling here reveals how to keep a reactive job from fragmenting every block of focus you have.
- **L2 · The Real Cost of Multitasking** — Holding two problems at once doesn't halve your speed, it does worse — understanding the switching cost is what makes single-tasking a deliberate choice rather than a personality trait.

---

#### L1-10 · Technical Debt as a Managed Liability

**What it is and why it matters:** Ward Cunningham coined "technical debt" in 1992 to make a *financial* argument to non-engineers — and the metaphor is routinely misused, because Cunningham's point was not "messy code is debt" but "shipping before you fully understand the domain is a loan you take on deliberately and repay by refactoring as you learn." Reclaiming the real meaning matters, because it reframes debt from a moral failing into an instrument: sometimes the right move is to borrow against the future to ship now, *provided you track the loan and intend to service it*. The skill is distinguishing deliberate, prudent debt from the reckless, inadvertent kind; making the debt visible so it can be prioritised against features; and articulating its cost in terms the business can weigh rather than as engineers' aesthetic complaints. This is what lets you argue for paying it down without sounding like you're asking permission to gold-plate. Mismanaged debt is how systems slow to a crawl while everyone is working as hard as ever.

**Level 2 candidates:**

- **L2 · Cunningham's Original Meaning vs the Common Misuse** — The metaphor was about shipping to learn, not about sloppy code — recovering the original framing changes when taking on debt is wise rather than lazy.
- **L2 · Deliberate vs Inadvertent, Prudent vs Reckless** — Fowler's quadrant separates the debt worth taking from the debt that just happens — drilling here gives you the vocabulary to defend a shortcut or condemn one.
- **L2 · Making Debt Visible** — Debt that lives only in engineers' heads can never be prioritised — the practices that surface it (tracking, naming, mapping it to slowed delivery) are what get it onto the actual roadmap.
- **L2 · Pricing Debt in the Business's Terms** — "This is ugly" loses every argument; "this adds two days to every change in this area" wins — translating debt into delivery cost is the skill that gets paydown funded.
- **L2 · Interest vs Principal: When Paydown Is Worth It** — Debt in stable, rarely-touched code costs little while debt in hot paths compounds — understanding the distinction is what directs cleanup to where it actually pays.

---

### Tier 3 — The Social System
*Your change is not done when it works; it is done when other people have accepted it. This ring is where engineering stops being a solitary act — review, persuasion, influence, and shared failure — and it is the layer most invisible to those who learned the craft alone.*

---

#### L1-11 · Code Review as Negotiation

**What it is and why it matters:** Code review is presented as a quality gate, but most of what makes it hard is social, not technical — it's the recurring point where your work meets someone else's judgment, and where ego, taste, and power quietly shape outcomes that are dressed up as objective. The skill has two faces. As an *author*, you learn to make a change easy to review — small, well-described, with the reasoning made explicit — because a reviewer's willingness to engage degrades sharply with size, and an unreviewable PR is a stalled one. As a *reviewer*, you learn to separate the changes that matter from personal preference, to phrase feedback so it improves the code without bruising the author, and to know when "different from how I'd do it" is not a valid objection. Done well, review is how a team's standards propagate and how trust is built; done badly, it's where resentment accumulates and good changes go to die.

**Level 2 candidates:**

- **L2 · Authoring a Reviewable Change** — Small diffs, a description that explains *why*, and pre-empted questions get reviewed faster and better — drilling here reveals how much review latency is actually caused by the author.
- **L2 · Separating Substance From Preference** — The hardest reviewer skill is letting go of "I'd have done it differently" when the difference doesn't matter — it's what keeps review from becoming a tax on everyone's style.
- **L2 · Feedback That Improves Code Without Bruising People** — How a comment is phrased determines whether it's acted on or resented — the wording moves (questions over commands, reasons over edicts) are a learnable craft.
- **L2 · Receiving Criticism on Your Own Code** — Decoupling your work from your worth is what lets you extract the value from harsh feedback instead of defending against it — a skill that pays off far beyond review.
- **L2 · Getting a Stalled Review Unstuck** — A PR sitting for days is a social problem, not a technical one — knowing how to nudge, escalate, or split it without becoming annoying is what keeps your work flowing.
- **L2 · Nitpicks, Blocking, and the Power Dynamics of Approval** — Who can block a merge and over what is a quiet power structure — seeing it clearly is what lets you navigate a reviewer holding your change hostage over trivia.

---

#### L1-12 · The Written Record

**What it is and why it matters:** Software organisations run on writing far more than newcomers expect — the decisions that shape systems are made in design docs, RFCs, tickets, and PR descriptions, and an engineer who can't write clearly is locked out of the room where those decisions happen. The shift to remote and asynchronous work has only sharpened this: when you can't tap someone on the shoulder, the quality of your writing *is* the quality of your collaboration. The deeper point is that a design doc is not documentation, it's *persuasion* — its job is to surface a decision early, expose it to challenge while changing it is still cheap, and build the alignment that prevents the expensive argument after the code is written. Writing also serves your future self: the comment that explains *why*, the postmortem that captures the lesson, and the decision record that outlives the people who made it are how knowledge survives the engineer who held it. Strong writing is a force multiplier precisely because it scales to readers you'll never meet and times you won't be present.

**Level 2 candidates:**

- **L2 · The Design Doc as Persuasion, Not Documentation** — A design doc exists to get a decision challenged while it's still cheap to change — understanding its real job changes what you put in it and when you write it.
- **L2 · The Async Message That Doesn't Need a Follow-Up** — A message that anticipates the obvious questions and states the ask clearly saves a whole round-trip — a high-leverage skill in any distributed team.
- **L2 · Decision Records: Capturing Why, Not Just What** — The reasoning behind a decision is the part lost first and missed most — recording it is what stops teams re-litigating settled questions every year.
- **L2 · Comments That Explain Intent** — The valuable comment captures the *why* the code can't — drilling here connects to the canon's rule that comments should say what isn't obvious from the code itself.
- **L2 · Writing to Be Skimmed** — Busy readers scan; structuring a document so the key point survives skimming is what determines whether it's actually read — a craft distinct from writing to be read in full.

---

#### L1-13 · Organizational Navigation

**What it is and why it matters:** Conway observed in 1968 that a system's structure mirrors the communication structure of the organisation that built it — which means the org chart is not a backdrop to your technical work, it's a force that shapes the code itself, and learning to read it is an engineering skill. This is the topic most absent from any curriculum because it's the most political: how technical decisions actually get made (rarely by the best argument alone), how to build the influence that lets you drive a change you can't simply mandate, and how to disagree-and-commit when a decision goes against you without either caving or sulking. It includes the unglamorous, decisive skill of *managing up* — making your work legible to the people who allocate your time and rewards, because work that isn't visible is work that didn't happen as far as the org is concerned. None of this is cynicism; it's recognising that engineering happens inside a human system with its own physics, and effectiveness requires reading that system as carefully as you read code. The engineers who ignore this layer wonder why their good ideas never go anywhere.

**Level 2 candidates:**

- **L2 · Conway's Law: The Org Chart Is in Your Codebase** — Conway's 1968 observation explains why your system's seams fall along team boundaries — it lets you predict architecture from org structure and sometimes change one by changing the other.
- **L2 · How Decisions Actually Get Made** — The best technical argument doesn't automatically win; trust, timing, and who's in the room do — seeing this is the difference between being right and being effective.
- **L2 · Building Influence Without Authority** — Most of what you'll want to change, you can't order — getting there through credibility and alliance is what separates engineers who shape direction from those who only execute it.
- **L2 · Disagree and Commit** — Backing a decision you argued against, fully rather than grudgingly, is what keeps teams moving — it's what lets you lose an argument without losing standing.
- **L2 · Managing Up and Making Work Visible** — Work your manager can't see is work that didn't happen, organisationally — drilling here reveals why legibility, not just output, determines how your effort is rewarded.
- **L2 · Picking Battles** — Influence is a budget you spend, not a constant — knowing which hills are worth it keeps you from being the person who objects to everything and is heard on nothing.

---

#### L1-14 · Incident Response and Shared Failure

**What it is and why it matters:** Eventually something you shipped breaks in production, usually at the worst time, and how you and your organisation respond is a discipline in its own right — distinct from debugging because the clock is running, others are watching, and the first job is to stop the bleeding, not to understand the cause. Amazon's "you build it, you run it" (Vogels, 2006) collapsed the old wall between writing code and operating it, which means modern engineers carry the pager for their own work — and the pager is a harsh but honest teacher about the gap between "passes tests" and "survives reality." The cultural keystone is the *blameless postmortem*, developed in the SRE and Etsy traditions: human error is almost always a symptom of a system that permitted it, so a postmortem that hunts for someone to blame learns nothing and makes everyone hide the next failure. Mastering this loop — triage under pressure, mitigate before you diagnose, then extract the systemic lesson without blame — is what turns outages from trauma into the most concentrated learning available in the field. It's also where every other skill on this map is tested at once.

**Level 2 candidates:**

- **L2 · Mitigate First, Diagnose Second** — During an incident, restoring service comes before understanding the cause — this ordering is what separates an engineer who stops an outage from one who prolongs it while investigating.
- **L2 · You Build It, You Run It** — Vogels' 2006 principle put developers on the pager for their own code — understanding why closes the feedback loop that makes engineers design for operability rather than just correctness.
- **L2 · The Blameless Postmortem** — Treating human error as a symptom of system design, not a culprit to punish, is what makes people report failures honestly — the cultural precondition for actually learning from incidents.
- **L2 · Communicating During an Outage** — A clear status update to anxious stakeholders is its own skill under pressure — the engineer who communicates well during an incident is trusted with the next one.
- **L2 · Turning an Incident Into a Systemic Fix** — The lesson worth extracting is rarely "be more careful"; it's the change that makes the failure class impossible — this links incident response back to the reliability discipline.
- **L2 · The Pager as a Teacher** — Carrying on-call teaches the gap between "works in the demo" and "survives production" faster than any other experience — it reframes on-call from a burden into the field's most concentrated feedback.

---

## Sequencing note

The tiers are concentric, not sequential — every real task pulls on all three at once — but there is a practical order of acquisition, and it runs inward to outward. **Tier 1 is the floor.** You cannot scope, estimate, or review what you cannot first read and change safely, and the most common reason an experienced engineer feels slow in a new role is not weak fundamentals but un-practised code archaeology in an unfamiliar codebase. Within Tier 1, **Code Archaeology (L1-01)** is the single highest-leverage entry point for anyone joining a system they didn't build — it's the skill every other Tier 1 skill stands on, and the one most often left to chance.

Tier 2 is where the returning practitioner is most likely to find their real gaps, because these skills are invisible until you're accountable for an outcome rather than a task. Within it the dependency runs roughly **Requirements Archaeology (L1-05) → Tactical vs Strategic (L1-06) → Scoping (L1-07) → Estimation (L1-08)**: you can't estimate work you haven't scoped, can't scope work whose investment level you haven't decided, and can't decide investment for a need you haven't correctly identified. **The Inner Loop (L1-09)** and **Technical Debt (L1-10)** apply throughout and can be picked up in parallel.

Tier 3 can't be studied in the abstract — it's learned by doing, and reading about it mostly helps you notice and name what's happening while it happens to you. Of its topics, **Code Review (L1-11)** is the daily one and the right place to start, since it's the most frequent point of contact between your work and other people's judgment.

For your specific profile — experienced, returning to foundations, strong at the parts of the craft that are written down — the highest-leverage entry on the entire map is almost certainly **Tier 2**, and within it **L1-06 (Tactical vs Strategic Judgment)**. You already make this call constantly; you've just never had it named as the meta-skill that governs everything else. Bringing it from instinct into deliberate practice is the change most likely to compound, because it sits upstream of how you spend effort on every other topic here. The second-highest is **L1-13 (Organizational Navigation)** — not because it's foundational, but because it's the layer most systematically neglected by engineers who are good at the technical craft, and the one where that neglect most quietly caps a career.

---