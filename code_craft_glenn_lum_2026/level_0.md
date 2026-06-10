# Code Craft (A Working Synthesis) — Level 0: Course Map

> **Intent:** The published canon of software craft — clean code, modularity, abstraction, testing — is decades of hard-won wisdom about a single problem: how to write code that humans can understand and safely change long after it was written. That wisdom is scattered across dozens of opinionated books that agree on the fundamentals and contradict each other loudly on the details, and a practitioner who reads them one at a time ends up cargo-culting whoever they read last. This map synthesizes the canon into the durable principles the field has genuinely converged on, and names the real disagreements honestly — so you can hold a coherent philosophy of code instead of a pile of half-remembered rules.
>
> **Your angle:** You've absorbed most of these ideas piecemeal, and you almost certainly carry scar tissue from following some rule too literally — functions kept tiny for their own sake, comments avoided on principle, coverage chased to 100%. The value here is recovering the *reasoning* beneath each principle so you know the conditions under which it holds and the conditions under which its opposite is correct. Read this to convert inherited rules into judgment — and to recognise a guru's taste when it's being sold to you as a law.

---

## How to use this map

Nearly the entire canon reduces to one claim: **the dominant cost of software is not writing it but understanding and changing it later**, so the central skill is managing complexity on behalf of future readers — most often your future self. Modularity, naming, abstraction, and tests are not separate virtues; they are all tactics serving that single goal. Hold that thesis and every technique below has an obvious *why*, and every rule has an obvious failure mode: it stops being correct the moment it stops reducing complexity.

The four tiers move from the abstract to the concrete and outward in time. **Foundations** is the lens — the war on complexity and the mindset that justifies design effort at all. **Structure** is the highest-leverage layer — how a system is decomposed and where its boundaries fall. **Surface** is the local text a human actually reads — names, functions, comments. **Time** is what keeps code alive — how it's safely changed and how you know it works.

Each **Level 1 topic** is a concept post: the synthesized principle, its history, and what it costs to ignore. Each **Level 2 candidate** is a depth post. Where the authorities genuinely disagree, a candidate is marked **The Debate** — those are not questions with a right answer but axes you learn to navigate by context. Descend only where a gap is actively costing you.

---

## Topic Inventory

---

### Tier 1 — Foundations: The War on Complexity
*The lens the whole canon is viewed through. Get this tier and the rest stops being a list of rules and becomes a single argument with many applications. Skip it and you'll collect techniques without knowing when each one turns into its own failure mode.*

---

#### L1-01 · The Nature of Complexity

**What it is and why it matters:** Brooks drew the field's deepest distinction in "No Silver Bullet" (1986): *essential* complexity is inherent in the problem, while *accidental* complexity is the mess we add ourselves — and only the second kind is ours to eliminate. Ousterhout later gave the working definition: complexity is anything that makes code hard to understand or modify, it shows up as change amplification, high cognitive load, and unknown unknowns, and it has two root causes — dependencies and obscurity. The crucial insight is that complexity is *incremental*: no single decision creates it, so no single decision feels worth resisting, and that is exactly how systems rot. This topic is the master key — every other principle on the map is a tactic for reducing one of these symptoms, and once you can name them you can evaluate any technique by asking which symptom it actually addresses.

**Level 2 candidates:**

- **L2 · Essential vs Accidental Complexity** — Brooks's 1986 distinction tells you which complexity you're obligated to fight and which you're stuck with — drilling here stops you from blaming the design for difficulty that lives in the problem itself.
- **L2 · The Three Symptoms: Change Amplification, Cognitive Load, Unknown Unknowns** — Naming how complexity actually hurts gives you a diagnostic vocabulary — the unknown-unknown (not knowing what you need to know to change something safely) is the worst and the least discussed.
- **L2 · Dependencies and Obscurity: The Two Root Causes** — Almost all complexity reduces to these two, and understanding them tells you that every technique in the canon is attacking one or the other.
- **L2 · Complexity Is Incremental** — The reason codebases degrade despite everyone's good intentions is that no single shortcut looks expensive — internalising this is what justifies a zero-tolerance posture toward small messes.
- **L2 · Why "Hard to Understand" Is the Real Metric** — Code is read far more than written, so understandability, not cleverness or brevity, is the property the whole canon optimises — this reframes what "good code" even means.

---

#### L1-02 · Strategic vs Tactical Programming

**What it is and why it matters:** The canon exists to answer a sceptic's question — if the code works, why spend more on it? Ousterhout's framing of *tactical* programming (get it working now) versus *strategic* programming (invest so it stays workable) is the field's clearest answer: working code that can't be cheaply changed is a liability disguised as an asset. The argument is economic, not moral — design investment is a bet that the code will be read and modified many times, and that bet almost always pays because software lives far longer than anyone plans. The "tactical tornado" — the developer who ships features fast and leaves wreckage that quietly slows everyone else — is the canon's cautionary archetype. Understanding this is what lets you defend design time to a business in terms it accepts: not "this is cleaner," but "this is cheaper over the life of the code."

**Level 2 candidates:**

- **L2 · Working Code Isn't Enough** — The premise that "it passes the tests" is the *floor*, not the goal, is what separates the canon from hacking — drilling here reveals why functioning code can still be a net negative.
- **L2 · The Compounding of Small Investments** — A few percent of effort spent on design, paid continuously, is the mechanism by which a codebase stays workable for years — understanding the compounding explains why it can't be deferred to a later "cleanup phase."
- **L2 · The Tactical Tornado** — The fast feature-shipper who creates work for everyone downstream is a real and rewarded archetype — recognising the pattern is what lets you argue against optimising for visible speed alone.
- **L2 · The Boundary With Daily Judgment** — This is the *investment philosophy*; deciding tactical-or-strategic on a specific task under a real deadline is a separate skill — knowing the difference keeps the principle from becoming a mandate to over-engineer everything.

---

#### L1-03 · Design as a Deliberate Act

**What it is and why it matters:** A recurring claim across the canon is that design is a skill you practise, not a phase you either include or skip — and the most concrete expression is Ousterhout's "design it twice," the discipline of sketching two or three genuinely different approaches before committing to one. The reasoning is that your first idea is rarely your best, and the cost of exploring alternatives on paper is trivial against the cost of discovering the flaw after it's built. This sits inside the field's longest-running tension: up-front design versus the emergent, refactor-as-you-go design championed by XP and agile — a debate the synthesis resolves not by picking a side but by scaling design effort to the cost of being wrong. What this unlocks is the habit of treating the first solution that comes to mind as a draft, which is the single cheapest way to improve the quality of your designs.

**Level 2 candidates:**

- **L2 · Design It Twice** — Forcing yourself to produce a second, structurally different design before choosing is a near-free way to escape the local maximum of your first idea — the highest-return design habit in the canon.
- **L2 · The Debate: Up-Front vs Emergent Design** — The waterfall instinct to design fully before coding and the agile instinct to let design emerge through refactoring are both partly right — the synthesis is to match design depth to the reversibility of the decision.
- **L2 · Reversibility as the Deciding Variable** — How much to design up front depends on how expensive the decision is to undo — drilling here gives you the rule that dissolves most of the up-front-vs-emergent argument.
- **L2 · Designing at the Right Level** — Some decisions (data models, module boundaries) are costly to reverse and deserve real design; most are cheap and don't — telling them apart is what keeps "design first" from becoming paralysis.

---

#### L1-04 · The Meta-Principles: DRY, YAGNI, and Their Misuse

**What it is and why it matters:** A handful of acronyms carry most of the canon's everyday weight — DRY (don't repeat yourself, from *The Pragmatic Programmer*, 1999) and YAGNI (you aren't gonna need it, from XP) — and both are correct, widely taught, and routinely over-applied into their own failure modes. DRY is really about not duplicating *knowledge*, but it gets applied to any code that merely *looks* similar, producing premature abstractions that couple unrelated things — which is why Sandi Metz's counter-maxim that the wrong abstraction is more expensive than duplication (2016) is the necessary corrective. YAGNI rightly fights speculative generality, but pushed too far it becomes an excuse to ignore obvious near-term needs. The synthesis the field has settled toward — sometimes called "avoid hasty abstractions" — is that duplication is cheap to fix and bad abstractions are not, so you wait for the pattern to prove itself (the rule of three) before extracting it.

**Level 2 candidates:**

- **L2 · DRY Is About Knowledge, Not Text** — The principle targets duplicated *decisions*, not duplicated-looking lines — drilling here stops you from merging two things that are identical today but will diverge tomorrow.
- **L2 · The Debate: The Wrong Abstraction vs Duplication** — Metz's argument that premature abstraction is costlier than repetition directly tensions the DRY reflex — understanding it is what makes you wait before extracting.
- **L2 · YAGNI vs Speculative Generality** — Building for imagined future needs is one of the most common ways to add accidental complexity — but YAGNI taken literally ignores cheap, obvious provisions, so the skill is calibration, not dogma.
- **L2 · The Rule of Three** — Waiting until you've seen a pattern three times before abstracting it is the canon's practical answer to "when is duplication actually a problem" — the heuristic that operationalises the whole debate.
- **L2 · AHA: Avoiding Hasty Abstractions** — The modern synthesis prefers a little duplication now over the wrong abstraction forever — drilling here gives you the reasoned default that resolves DRY-vs-WET in practice.

---

### Tier 2 — Structure: Decomposition and Abstraction
*The highest-leverage tier. Where you draw boundaries determines more about a system's complexity than anything you do inside them. This is the macro layer — the architecture of a module — and the place where one good decision pays off for years and one bad one taxes every future change.*

---

#### L1-05 · Modularity, Coupling, and Cohesion

**What it is and why it matters:** The structured-design tradition of the 1970s (Constantine, Yourdon) gave the field its most durable structural vocabulary — *coupling*, how much modules depend on each other, and *cohesion*, how single-purpose each module is — and the consensus that has never been overturned is: minimise coupling, maximise cohesion. The reasoning ties straight back to complexity: coupling is dependency made concrete, so loosely coupled modules can be understood and changed in isolation, which is the entire point of breaking a system into modules at all. Cohesion is the other half — a module that does one thing well has an obvious place for every change, while a grab-bag module forces you to understand everything to change anything. This is the structural foundation the rest of the tier builds on, and most architectural smells you'll ever meet are a coupling or cohesion problem wearing a costume.

**Level 2 candidates:**

- **L2 · Coupling as Dependency Made Visible** — Every coupling is a reason two pieces of code must be understood together — drilling here reframes "reduce coupling" from a slogan into the direct mechanism for isolating change.
- **L2 · Cohesion and the One-Thing Module** — A module with a single clear responsibility gives every change an obvious home — understanding cohesion explains why "utils" and "helpers" modules become dumping grounds that resist all reasoning.
- **L2 · The Debate: When to Split and When to Merge** — Ousterhout warns that over-splitting creates as much complexity as under-splitting; code that's always changed together often belongs together — this tensions the reflex to decompose everything.
- **L2 · Temporal and Logical Coupling** — Some dependencies aren't in the code but in the requirement that things change at the same time — recognising hidden coupling is what explains changes that mysteriously break distant code.
- **L2 · Connascence: A Finer Vocabulary for Coupling** — The connascence taxonomy grades coupling by how strongly and remotely two things are bound — drilling here gives you a sharper tool than the binary "coupled or not."

---

#### L1-06 · Information Hiding and Deep Modules

**What it is and why it matters:** Parnas's 1972 paper on decomposing systems into modules is arguably the single most important document in the canon, and its thesis is counterintuitive: you should decompose a system not by the *steps* it performs but by the *design decisions* each module hides from the rest. A module's value is the knowledge it keeps to itself, because hidden decisions can change without anyone else caring — that is what decoupling actually buys you. Ousterhout's "deep module" is the modern restatement: the best modules present a simple interface over a complex implementation, maximising the functionality hidden behind the smallest possible surface. The failure mode is *information leakage* — a design decision that shows up in multiple modules, so changing it means changing all of them — and learning to spot it is what tells you a boundary is in the wrong place. This is the criterion for *where* to cut, and it's the idea most likely to upgrade your structural judgment in one sitting.

**Level 2 candidates:**

- **L2 · Parnas's Criterion: Hide the Decisions Likely to Change** — Decomposing around what varies, not around the processing sequence, is the original and still-best rule for placing module boundaries — drilling here is the highest-value structural idea in the canon.
- **L2 · Deep vs Shallow Modules** — A deep module hides a lot behind a little interface; a shallow one's interface is nearly as complex as its implementation and barely earns its existence — understanding depth is how you judge whether a class is pulling its weight.
- **L2 · Information Leakage** — When one design decision is reflected in several modules, you've leaked — spotting leakage is the diagnostic that tells you a boundary is drawn in the wrong place.
- **L2 · Interface vs Implementation Complexity** — The cost of a module is its interface (paid by every caller); the benefit is the implementation it hides — this ratio is the lens that makes "is this abstraction worth it?" answerable.
- **L2 · Pass-Through Methods and Other Shallow Smells** — A method that does nothing but forward to another adds interface without hiding anything — recognising these reveals decomposition that's adding complexity while pretending to reduce it.

---

#### L1-07 · Abstraction and Leaky Boundaries

**What it is and why it matters:** An abstraction is a deliberately simplified view that omits detail so you can reason about something without holding all of it in your head — it is the fundamental tool the entire canon relies on, and also the one that never fully works. Spolsky's Law of Leaky Abstractions (2002) names the permanent catch: every abstraction leaks the details it was meant to hide at some point, usually under performance pressure or failure, which is why you can never fully escape the layer beneath. Ousterhout's "different layer, different abstraction" adds the design rule — each layer of a system should offer a genuinely different view, and when adjacent layers look the same you have a layer that isn't earning its place. The payoff of this topic is calibration: knowing that abstractions are both indispensable and imperfect stops you from either trusting them blindly or abandoning them for fear of leaks.

**Level 2 candidates:**

- **L2 · The Law of Leaky Abstractions** — Spolsky's 2002 observation that abstractions always eventually leak explains why you still need to understand the layer below the one you're using — drilling here inoculates you against trusting a boundary completely.
- **L2 · Different Layer, Different Abstraction** — When two adjacent layers expose the same concepts, one of them is redundant — understanding this is how you detect a layer that adds indirection without adding value.
- **L2 · The Cost of an Abstraction** — Each abstraction has a cost (a thing to learn, a place to look) that must be repaid by what it hides — this is what separates clarifying abstractions from indirection for its own sake.
- **L2 · Pull Complexity Downward** — Ousterhout's principle that a module should absorb complexity rather than pushing it onto its callers explains why a slightly harder implementation is worth a much simpler interface.
- **L2 · Abstraction vs Indirection** — Adding a layer isn't the same as adding an abstraction; indirection that doesn't simplify just adds hops — drilling here is what keeps "add a layer" from being a reflex.

---

#### L1-08 · Interfaces, Contracts, and Defining Errors Away

**What it is and why it matters:** An interface is a promise, and Meyer's Design by Contract (Eiffel, 1986) made the promise formal: a method's preconditions, postconditions, and invariants are a contract between caller and implementation that says exactly who is responsible for what. The canon's design advice converges here — Ousterhout's "general-purpose modules are deeper" argues that an interface designed for a slightly broader use than today's specific need is usually simpler and more reusable, because special-casing leaks the caller's situation into the module. The most provocative idea in this space is "define errors out of existence" — redesigning an interface so that the error condition simply cannot arise (an operation that's harmlessly idempotent, a value that's never null) rather than forcing every caller to handle it. This sits in genuine tension with defensive programming and exception-heavy styles, and the synthesis is that the best error handling is the error you designed away, with explicit handling as the fallback for the ones you can't.

**Level 2 candidates:**

- **L2 · Design by Contract** — Meyer's preconditions/postconditions/invariants make the caller-implementer responsibility split explicit — drilling here turns vague interface "expectations" into a checkable contract.
- **L2 · General-Purpose vs Special-Purpose Interfaces** — An interface shaped to one caller's exact need tends to be shallow and leaky; a slightly more general one is often simpler — understanding why reframes "build only what you need today."
- **L2 · The Debate: Define Errors Out of Existence vs Defensive Programming** — Eliminating error conditions by design versus checking for them everywhere are opposing philosophies — the synthesis is to design the common errors away and explicitly handle the rest.
- **L2 · Exceptions vs Error Values vs Result Types** — How a language and team represent failure shapes how robust calling code is — drilling here explains why the same logic feels safe in one error model and fragile in another.
- **L2 · Making Misuse Hard** — The strongest interfaces make the wrong call impossible to write, not merely documented as wrong — this is the "hard to misuse" principle that connects contracts to real-world robustness.

---

### Tier 3 — Surface: Code a Human Can Read
*The local text, line by line, that a reader actually parses. This is the tier where the canon's authors fight the loudest — function size and comments are where Clean Code and A Philosophy of Software Design openly disagree — so it's where synthesis matters most and where inherited rules do the most quiet damage.*

---

#### L1-09 · Naming

**What it is and why it matters:** "There are only two hard things in computer science: cache invalidation and naming things" (Phil Karlton) is a joke that the canon takes entirely seriously, because a name is the highest-frequency, lowest-effort design decision you make — every reader pays for a bad one, repeatedly. A good name is compression: it carries the design intent so the reader doesn't have to reconstruct it from the code, which means naming is really a test of whether *you* understand the thing you're naming. This is one of the rare topics where the canon is in near-total agreement — Ousterhout, Martin, and the broader tradition all treat precise, consistent naming as foundational rather than cosmetic. What it unlocks is disproportionate: improving the names in a confusing piece of code often clarifies it more than any restructuring, because it removes the obscurity that was half the complexity to begin with.

**Level 2 candidates:**

- **L2 · A Name as Compressed Intent** — A precise name transmits what something is *for* without the reader decoding the implementation — drilling here reveals why a vague name is a tax paid on every single read.
- **L2 · Naming as a Test of Understanding** — Struggling to name something cleanly is usually a sign the concept itself is muddled — the difficulty is diagnostic, pointing at a design problem behind the naming problem.
- **L2 · Consistency in Naming** — The same concept under one name everywhere lets readers predict and search; synonyms for one idea force them to verify each is really the same — small discipline, large compounding payoff.
- **L2 · Length, Scope, and Precision** — How descriptive a name should be scales with how far it's used from where it's defined — understanding this resolves the "short vs descriptive names" argument by context rather than by rule.
- **L2 · The Magic Number Problem** — A hardcoded literal is an unnamed concept; giving it a name turns an inexplicable value into a documented decision — the cheapest readability win available.

---

#### L1-10 · Functions, Size, and the Clean Code Debate

**What it is and why it matters:** This is the canon's most famous open disagreement, and navigating it is worth more than accepting either side. Martin's *Clean Code* (2008) argues functions should be very small and do exactly one thing, pushing "extract till you drop" — and for a generation this hardened into a rule that small is automatically better. Ousterhout's direct, documented critique is that excessive decomposition produces *shallow* methods, multiplies interfaces, and creates "conjoined" functions you can't understand without flipping between several — so chopping a function up can *increase* complexity even as it lowers line counts. The synthesis is that line count was always the wrong metric: the real variables are depth and cohesion, and you split a function when the pieces are genuinely independent and the interface between them is simpler than the code it hides — not because a function crossed an arbitrary length. Internalising this frees you from a rule that, applied mechanically, has degraded a great deal of otherwise-good code.

**Level 2 candidates:**

- **L2 · The Debate: "Extract Till You Drop" vs Deep Methods** — Martin's small-functions doctrine and Ousterhout's warning against shallow over-decomposition are directly opposed — understanding both is what stops you from splitting code that was clearer whole.
- **L2 · Why Line Count Is the Wrong Metric** — Brevity measures nothing about understandability; a long cohesive function can be clearer than five fragments — drilling here replaces a number with a judgment.
- **L2 · Conjoined Methods** — When you can't understand one function without reading another it calls, the split didn't reduce complexity, it relocated it — recognising this is the test for a bad extraction.
- **L2 · "Do One Thing" — At Which Level of Abstraction?** — The do-one-thing rule is true but underspecified, since "one thing" depends on the layer — clarifying this is what makes the principle usable instead of a license to over-split.
- **L2 · When Extraction Genuinely Pays** — Splitting earns its keep when the extracted piece is reusable, independently testable, or hides real complexity behind a simpler name — naming the actual criteria turns extraction from a reflex into a decision.

---

#### L1-11 · Comments

**What it is and why it matters:** Comments are the canon's other great schism, and the disagreement is sharper than it first appears. One camp — much of the agile folk tradition, and parts of *Clean Code* — treats comments as a failure, a sign you couldn't make the code self-explanatory, and pushes "self-documenting code." Ousterhout takes the opposite, strong position: comments capture exactly what code *cannot* — the *why*, the rationale, the non-obvious constraint, the design intent — and he goes further, advocating "write the comments first" as a design tool that exposes a muddled interface before you implement it. The synthesis dissolves most of the fight by distinguishing *kinds* of comments: a comment that restates what the code plainly does is indeed noise, but a comment that records intent, rationale, or a non-obvious gotcha is information that exists nowhere else and is lost forever if not written. What this unlocks is treating comments as design artifacts rather than apologies — and knowing which comments to delete and which are load-bearing.

**Level 2 candidates:**

- **L2 · The Debate: Self-Documenting Code vs Comments as Essential** — The "good code needs no comments" position and Ousterhout's "comments capture what code can't" position are both defensible about *different* comments — separating them ends the argument.
- **L2 · Comments Should Say What the Code Cannot** — The why, the rationale, the rejected alternative, the non-obvious constraint — these live nowhere in the code itself — drilling here is the rule that tells a useless comment from an irreplaceable one.
- **L2 · Write the Comments First** — Drafting the interface comment before the implementation surfaces a confused design while it's still cheap to fix — a design technique disguised as a documentation habit.
- **L2 · Why Comments Rot, and What to Do About It** — Comments drift from code because nothing enforces their truth — understanding the failure mode tells you to comment the stable *why* rather than the volatile *how*.
- **L2 · Documenting the Interface vs the Implementation** — Interface comments serve callers and should hide internals; implementation comments serve maintainers — confusing the two is why some comments leak detail they should hide.

---

#### L1-12 · Consistency and Obviousness

**What it is and why it matters:** Consistency is the principle nearly every author agrees compounds, because it lets a reader predict — once a convention holds everywhere, the reader stops re-deriving it and the codebase becomes legible by pattern rather than by inspection. Ousterhout frames the destination as code that is *obvious*: code where the reader's first guess about what it does is correct, requiring little effort and producing no surprises. The deep and slightly uncomfortable implication is that a consistent-but-imperfect convention often beats a locally-superior inconsistency, because the cost of a reader hitting an exception usually exceeds the benefit of the local optimisation. This connects to the principle of least surprise — code that behaves as it looks like it should — and it's the quiet reason that style guides, linters, and "matching the surrounding code" are worth more than they appear. What it unlocks is the discipline to suppress a clever local improvement in service of a predictable whole.

**Level 2 candidates:**

- **L2 · Consistency Lets Readers Predict** — A reliable convention means the reader infers instead of verifying — drilling here explains why consistency reduces cognitive load even when the convention itself is imperfect.
- **L2 · Code Should Be Obvious** — The target is code whose first reading is the correct reading — understanding obviousness as the goal reframes "clever" code as a defect, since cleverness is surprise.
- **L2 · The Principle of Least Surprise** — Code that does what it looks like it does is safer than code that's technically correct but unexpected — this is why a misleadingly-named or side-effecting function is a bug waiting to happen.
- **L2 · When Consistency Should Lose** — Matching surrounding code stops being right when the surrounding pattern is actively harmful — knowing when to break consistency deliberately is what keeps it from ossifying into "we've always done it wrong."
- **L2 · Conventions, Linters, and Mechanised Agreement** — Automating style removes a whole category of argument and review noise — drilling here reveals why offloading consistency to tools frees human attention for design.

---

### Tier 4 — Time: Evolution and Confidence
*Code is never finished — it is read, changed, and depended on for years, and it has to keep working through all of it. This tier covers how you safely improve a design over time and how you earn confidence that it's correct. It also holds the canon's most tribal debate: how to test.*

---

#### L1-13 · Refactoring and Code Smells

**What it is and why it matters:** Refactoring got its rigour from Opdyke's 1992 thesis and its popular form from Fowler's *Refactoring* (1999), and the precise definition is the whole point: a *behaviour-preserving* transformation of internal structure, made in small steps, backed by tests so you can prove behaviour didn't change. This is what separates disciplined refactoring from "rewriting and hoping" — the safety net of tests is what lets you improve a design continuously instead of in terrifying big-bang rewrites. Beck and Fowler's other gift was *code smells* — a shared vocabulary (long method, feature envy, shotgun surgery, primitive obsession) for the intuition that "something is wrong here" but you can't yet say what — which turns a vague unease into a named, discussable, fixable thing. The synthesis with the rest of the canon is clean: smells are symptoms of the complexity from Tier 1, and refactorings are the named moves that drain it back out, applied via the rule of three and the boy scout rule (leave it cleaner than you found it).

**Level 2 candidates:**

- **L2 · Refactoring as Behaviour-Preserving Change** — The discipline is changing structure *without* changing behaviour, in steps small enough to verify — drilling here is what separates safe refactoring from the rewrite-and-pray that gets refactoring blamed for breakage.
- **L2 · Code Smells as a Shared Vocabulary** — Named smells turn "this feels wrong" into a specific, communicable diagnosis — understanding the catalogue is what lets a team discuss design problems precisely instead of by taste.
- **L2 · Tests as the Refactoring Safety Net** — You can only refactor fearlessly what you can prove still works — this is the dependency that ties this topic to testing and explains why untested code resists improvement.
- **L2 · The Boy Scout Rule and Opportunistic Cleanup** — Improving the small area you touch on every change is how design debt gets paid down without a dedicated project — drilling here reveals the only cleanup strategy that reliably survives contact with deadlines.
- **L2 · When NOT to Refactor** — Refactoring stable, rarely-touched, working code is often net-negative risk — knowing when to leave code alone is as much a part of the skill as knowing when to improve it.

---

#### L1-14 · Testing: The Four Pillars and What Makes a Test Valuable

**What it is and why it matters:** Most testing advice is folklore until you have a frame for judging a test's *value*, and Khorikov's four pillars are the field's best synthesis of one: a good test maximises protection against regressions, resistance to refactoring, and fast feedback — while staying maintainable — and the crucial insight is that these are in tension, so no test maxes all of them and every test is a tradeoff. The most under-appreciated pillar is *resistance to refactoring*: a test that breaks every time you change implementation details (without any behaviour changing) is worse than no test, because it punishes exactly the improvement you want to make. This is why the durable rule is *test behaviour, not implementation* — couple your tests to what the code does, observable from outside, not to how it does it. The test pyramid (Cohn) sits on top as the allocation strategy — many fast unit tests, fewer slow integration tests — and the whole topic is what turns a test suite from a maintenance burden into the safety net that makes Tier 3 and refactoring possible at all.

**Level 2 candidates:**

- **L2 · The Four Pillars and Their Tradeoff** — Protection, refactoring-resistance, fast feedback, and maintainability can't all be maximised at once — internalising the tradeoff is what lets you judge any test instead of chasing coverage.
- **L2 · Resistance to Refactoring: The Forgotten Pillar** — A test that fails when you change implementation but not behaviour is actively harmful — drilling here explains why over-specified tests make codebases *harder* to change.
- **L2 · Test Behaviour, Not Implementation** — Coupling tests to observable behaviour rather than internal structure is the single principle that produces tests worth keeping — understanding it dissolves most "our tests are too brittle" complaints.
- **L2 · The Test Pyramid and Where Coverage Pays** — Cohn's pyramid allocates many cheap unit tests under fewer expensive integration tests — drilling here reveals why "100% coverage" is the wrong target and what to aim for instead.
- **L2 · Mocks, Stubs, and Over-Mocking** — Test doubles are necessary for isolation and toxic in excess, coupling tests to call structure — understanding when a mock helps versus when it freezes your design is core to non-fragile testing.

---

#### L1-15 · TDD and the Schools of Testing

**What it is and why it matters:** Test-driven development (Beck, *Test-Driven Development by Example*, 2003) is the canon's most evangelised and most contested practice — the red-green-refactor loop, writing the failing test first as a design pressure, not merely a verification step. The genuine fork beneath it is the two *schools*, named by Fowler: the Classical (or Detroit) school tests through real collaborators and asserts on resulting state, while the London (or mockist) school isolates each unit with mocks and asserts on interactions — and they produce meaningfully different designs and different test fragility profiles. The synthesis Khorikov argues is that the Classical default produces tests with better refactoring-resistance, with mocking reserved for genuine out-of-process dependencies — which connects this topic straight back to the four pillars. And the field has openly litigated TDD itself: the 2014 "Is TDD Dead?" exchange between Heinemeier Hansson, Beck, and Fowler is the honest record of practitioners disagreeing about when the discipline helps and when it harms. What this unlocks is a *reasoned* testing posture instead of a tribal one — the ability to say why you test the way you do.

**Level 2 candidates:**

- **L2 · Red-Green-Refactor as Design Pressure** — Writing the test first forces you to use your own interface before it exists, exposing awkward designs early — drilling here reframes TDD as a design technique rather than just a testing one.
- **L2 · The Debate: Classical vs London (Mockist) Schools** — Testing through real collaborators versus isolating with mocks yields different designs and different fragility — understanding both is what lets you choose a style deliberately instead of inheriting one.
- **L2 · Why the Mockist Style Tends Toward Fragility** — Asserting on interactions couples tests to *how* code works, hurting refactoring-resistance — this connects the school debate directly to the four-pillars tradeoff.
- **L2 · The Debate: "Is TDD Dead?"** — The 2014 Hansson–Beck–Fowler exchange is the field reasoning openly about TDD's limits — drilling here gives you a balanced view of where test-first genuinely pays and where it doesn't.
- **L2 · Mock Only Out-of-Process Dependencies** — Reserving mocks for things crossing a process boundary (databases, network) rather than for internal collaborators is the synthesis rule that keeps isolation from creating brittle tests.

---

## Sequencing note

The tiers are ordered by leverage and dependency, and the order is deliberate. **Tier 1 is the spine of the whole synthesis** — without the complexity lens, the rest is a pile of rules with no way to adjudicate between them, and the single highest-value entry on the entire map is **L1-01 (The Nature of Complexity)**, because it converts every other topic from "a thing an author told me to do" into "a tactic against a named problem I can now recognise." For someone returning to foundations with the canon already absorbed piecemeal, that reframe is the one that makes everything else cohere.

**Tier 2 is where structural judgment is won**, and within it **L1-06 (Information Hiding and Deep Modules)** is the highest-leverage single idea in the field — Parnas's criterion for *where to draw boundaries* will upgrade your designs more than any local technique, and it's the one most practitioners have never read in the original. Approach Tier 2 before Tier 3: structure dominates surface, and clean names on a badly-decomposed module are lipstick.

**Tier 3 is where your scar tissue most likely lives.** If you learned the canon through *Clean Code*, the two highest-value topics for you are **L1-10 (Functions and the Clean Code Debate)** and **L1-11 (Comments)** — not to learn them, but to *un-learn the rules as rules* and recover the reasoning, because these are exactly the principles that do damage when applied mechanically. Reading the two sides of each debate side by side is the fastest way to turn an inherited habit back into a judgment.

**Tier 4 depends on everything before it** — refactoring needs tests, tests need structure worth testing, and the testing debates only make sense once you hold the four pillars. Within it, **L1-14 (What Makes a Test Valuable)** is the prerequisite for everything else; the TDD school wars in L1-15 are unresolvable noise until you have the pillars to judge them by.

For your profile specifically, the two entries that will compound the most are **L1-01** (the unifying lens) and **L1-10** (the clearest place to feel the canon disagree and to replace a rule with reasoning). Start at the top for coherence; jump to the Tier 3 debates if what you most want is to stop second-guessing habits you absorbed years ago.

---
