## Metadata
- **Date:** 11-06-2026
- **Source:** 03_design_as_a_deliberate_act.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-03 · Design as a Deliberate Act

The most expensive bug in your codebase right now is almost certainly not a bug. It is a design decision someone made in the first ten minutes of thinking about a problem, committed to without examining alternatives, and built on top of for two years. The code works. It passes its tests. And every change to it costs three times what it should, because the shape was wrong from the start and nobody noticed in time to do anything cheap about it. This is the failure mode the canon's design literature exists to prevent, and it is not prevented by working harder or knowing more patterns. It is prevented by treating design as a thing you deliberately do, not a thing that happens to you while you type.

The premise underneath the entire topic is uncomfortable: your first idea is rarely your best one. Not because you are inexperienced, but because the first solution that comes to mind is, by construction, the one most strongly suggested by the problem as you currently understand it — which is to say, the one shaped by your current blind spots. Treating that first idea as a draft rather than a destination is the single cheapest improvement available to your design quality, and most working programmers don't do it, because they have no concrete practice that forces them to.

Ousterhout's "design it twice" is exactly that practice. Before committing to an approach, sketch two or three genuinely different ones — not minor variations of the same shape, but structurally different decompositions, different places to draw the boundaries, different things to hide. The cost is small: paper, a whiteboard, an hour. The return is that you discover the weaknesses of your first instinct by comparison rather than by production incident. You also discover, often, that the second design borrows something the first didn't have, and the synthesis is better than either alone. The discipline is mechanical; the payoff is judgment.

This sits inside the field's longest-running argument, which you should understand even though it doesn't have a clean winner. On one side is the tradition of up-front design — work the problem out before you build, because rework is expensive and structure is hard to change once code exists. On the other is the emergent-design tradition from XP and agile — accept that you don't yet know enough to design correctly, build the simplest thing that works, and refactor the design out of the code as understanding grows. Both camps are right about something real, and both, applied dogmatically, produce recognisable disasters: paralytic over-design that ships nothing, or a tangle of accumulated short-term decisions that nobody can untangle.

The synthesis is not a compromise but a reframing: scale your design effort to the reversibility of the decision. Decisions that are cheap to change later — the body of a function, a local variable name, an internal data structure used in one place — deserve almost no up-front design, because the cost of getting them wrong is the cost of fixing them, which is small. Decisions that are expensive to change later — a public API consumed by other teams, a database schema with millions of rows, the boundary between two major subsystems — deserve real design effort, because the cost of getting them wrong is the cost of fixing them plus the cost of every workaround built on top of them in the meantime. The argument between up-front and emergent collapses once you stop pretending all decisions have the same blast radius.

This means the skill is not "design more" or "design less." It is recognising, as you work, which decisions you are about to make and how reversible each one is — and spending design effort proportionally. This is harder than either dogma, because the answer changes by the hour. Some days you are choosing variable names; some days you are choosing module boundaries that will outlive you in this codebase. The same engineer should treat those decisions completely differently, and most of the damage done by inherited rules ("always design first," "always let it emerge") is the damage of applying one posture to both kinds of decision.

What this topic unlocks, then, is small and large at once. The small thing is the habit of pausing before you commit to your first idea long enough to imagine a structurally different one — even if you end up choosing the first. The large thing is calibration: knowing that design is not a phase you skip or include, but a continuous allocation of attention against the reversibility of what you're about to do. Once you hold that, the entire up-front-vs-emergent debate stops being a question you have to answer and becomes a dial you turn, by the decision, with reasons.

The practical test is whether you can defend your design effort in both directions. Can you explain why you spent two days sketching three approaches to a module boundary? (Because reversing it later costs weeks.) Can you explain why you didn't sketch anything before writing this function? (Because rewriting it tomorrow costs ten minutes.) When you can answer both questions in the same vocabulary, you have replaced a rule with a judgment — which is the entire point.

## Level 2 candidates

**Design It Twice** — The concrete practice of producing two or three structurally different designs before choosing one, and what makes a "genuinely different" alternative versus a cosmetic variation. Worth a deep dive because the technique sounds trivial and is in fact the highest-return design habit in the canon — the gap between knowing about it and actually doing it consistently is where most of the value lives.

**The Debate: Up-Front vs Emergent Design** — The full history of the disagreement between the design-first tradition and the XP/agile emergent-design tradition, what each camp gets right, and the failure modes of each taken to its extreme. Worth depth because most practitioners have absorbed one side as default without ever seeing the other argued in good faith, and the argument itself contains the reasoning that makes the synthesis make sense.

**Reversibility as the Deciding Variable** — The principle that design effort should scale to how expensive a decision is to undo, and how to actually estimate reversibility in practice. Worth depth because this is the rule that dissolves most of the up-front-vs-emergent argument, and applying it well requires concrete heuristics for recognising which decisions are which — heuristics that take time to develop.

**Designing at the Right Level** — Which categories of decision (data models, public interfaces, module boundaries, persistence schemas) genuinely warrant up-front design, and which categories almost never do. Worth depth because "design first" without this distinction collapses into either paralysis or selective application, and the catalogue of high-leverage decisions is concrete enough to teach directly.

---