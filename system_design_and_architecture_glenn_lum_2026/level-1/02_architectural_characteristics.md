## Metadata
- **Date:** 23-05-2026
- **Source:** 02_architectural_characteristics.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-02 · Architectural Characteristics

Every system you have ever worked on optimised for something. The question is whether anyone decided what that something was, or whether it emerged by accident from a thousand local decisions made under deadline pressure. This is the gap that architectural characteristics are meant to close: they are the explicit articulation of what a system must do beyond delivering its features. And the discipline of naming them — before choosing a style, before drawing a diagram, before writing code — is what separates architecture done by intent from architecture done by default.

The framing matters because functional requirements are seductive. They are concrete, they are testable, they are what the business asks for, and they are what gets you paid. But functional requirements describe what the system does, not how it must do it. Two systems can implement identical features and still be radically different architectures because one was built to handle ten thousand concurrent users and the other was built to be deployed by a single developer in under a minute. The features tell you nothing about that. The characteristics do.

Richards & Ford organise these characteristics into three families, and the taxonomy is worth holding in your head because each family fails differently when neglected. Operational characteristics — performance, scalability, availability, reliability — govern how the system behaves under load and under failure. These are the ones that wake you up at three in the morning. They are the most visible because their failure is loud: pages don't load, requests time out, the dashboard goes red. Most engineers can name these without prompting because the production environment punishes their absence relentlessly.

Structural characteristics — modularity, deployability, testability, maintainability — govern how the system can be changed. These are the ones that fail quietly. A system with poor modularity does not page anyone; it just makes every feature take twice as long as the last one, until eventually nobody can explain why a small change requires three weeks of work. Structural characteristics are systematically underweighted in early architectural decisions because their costs accrue over years rather than seconds, and the engineers paying those costs are often not the ones who made the original decisions. This is also why retrofitting them is so expensive: you are paying compound interest on a debt nobody recorded.

Cross-cutting characteristics — security, observability, agility — apply across the entire system rather than to specific components. They are the ones that cannot be added later, or rather, can only be added later at extraordinary cost. A system that was not designed to be observable does not become observable by adding a logging library; it requires you to revisit every component boundary and every error path. A system that was not designed with security as a structural concern accumulates vulnerabilities that no audit can fully surface. The defining property of cross-cutting characteristics is that they must be designed in, because their absence is a property of the whole, not of any single part.

The real discipline is not knowing the categories — it is forcing prioritisation. Every project stakeholder, asked which characteristics matter, will answer "all of them." This is the answer you must refuse to accept. A system that tries to optimise for everything optimises for nothing, because the characteristics are in genuine tension with each other. High availability fights consistency. Performance fights modularity. Security fights agility. Scalability fights simplicity. These tensions are not failures of imagination that a clever architect can resolve; they are structural properties of the design space. Pretending otherwise is how you end up with a system that is moderately bad at everything because nobody was willing to say which two or three things it had to be good at.

The deeper observation is that some characteristics are composites — they are emergent properties of other characteristics in combination. Agility, for example, is not a thing you build directly; it is what you get when deployability, testability, and modularity are all sufficiently strong. This matters because optimising for the composite is different from optimising for the parts. You cannot make a system more agile by holding a meeting about agility. You make it more agile by improving the underlying characteristics that compose into it — and you have to know which ones those are.

The practical skill this topic builds is the habit of asking, before any architectural conversation: which characteristics is this system actually being designed for, and which are we willing to compromise? If you cannot answer that question, you are not yet having an architectural conversation — you are having a feature conversation with architectural vocabulary. The characteristics are how you make the implicit explicit, how you turn taste into argument, and how you give future engineers — including your future self — a chance to understand why the system is the way it is.

## Level 2 candidates

**Operational characteristics** — Scalability, availability, performance, and reliability as the characteristics that govern behaviour under load and under failure. Worth deeper exploration because these are in constant tension with each other, and understanding the precise nature of those tensions (why availability and consistency trade against each other, why performance and scalability are not the same thing) is the foundation for almost every distributed systems decision.

**Structural characteristics** — Modularity, deployability, testability, and maintainability as the characteristics that govern how easily a system can be changed. Worth deeper exploration because these are systematically underweighted in early decisions, and understanding why — and how to argue for them against the gravitational pull of feature work — is its own discipline.

**Cross-cutting characteristics** — Security, observability, and agility as characteristics that apply across the system rather than to specific components. Worth deeper exploration because the "designed in, not bolted on" claim has concrete implications for how you structure component boundaries, error paths, and instrumentation from day one.

**Identifying and prioritising characteristics** — The practical method for surfacing implicit requirements from stakeholders and forcing explicit prioritisation. Worth deeper exploration because this is where the theory meets the conference room: how do you actually run the conversation that gets a stakeholder to admit which three characteristics they cannot compromise on?

**Composite characteristics** — How individual characteristics combine into emergent properties like agility, and why optimising for the composite differs from optimising for the parts. Worth deeper exploration because the composite framing changes how you diagnose problems — when a team complains about agility, the answer lives in the underlying characteristics, not in the composite itself.

---
