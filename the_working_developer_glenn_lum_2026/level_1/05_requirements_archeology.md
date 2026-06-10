## Metadata
- **Date:** 11-06-2026
- **Source:** 05_requirements_archeology.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-05 · Requirements Archaeology

The most expensive bug in software is the one where the code works exactly as written and solves the wrong problem. It ships, it passes review, it survives production — and then someone uses it and says "no, that's not what I needed." Every hour that went into it is gone, and the cost compounds because now you have to undo it before you can do the right thing. This failure mode is invisible in any framing of engineering that starts with "given a specification." The job almost never starts with a specification.

What it starts with is a sentence in Slack, a screenshot with an arrow, a ticket someone wrote in two minutes between meetings, or a conversation that ended with "you know what I mean." None of these are requirements. They are *artifacts* of someone else's thinking — usually thinking that has already jumped past the problem and landed on a solution. The ticket says "add a dropdown to the settings page" when what the user actually needs is to stop being interrupted by a notification they can't currently turn off. The dropdown is a guess at the answer. Build the dropdown and you've solved nothing; you've just added surface area to a product that already has too much.

This is the XY problem, and it has a name because it is the canonical failure of this whole layer. Someone wants X, decides Y will get them X, and asks you about Y. You answer the question about Y — competently, even elegantly — and a day later discover that Y was never going to solve X, or that X had a one-line answer that didn't involve Y at all. The move that prevents this is almost embarrassingly simple: before you start working on Y, ask what they're actually trying to accomplish. Most of the time the asker will tell you, and half the time the answer rearranges the problem entirely. The cost of asking is one message. The cost of not asking is the work.

The mental model worth holding is that a request is a claim, not an instruction. Someone is claiming that a particular change will produce a particular outcome they want, and your job before building is to investigate whether the claim is true. This sounds like insubordination if you frame it as "questioning the request"; it stops sounding that way when you frame it as "making sure we don't waste a week." Treating requirements as claims rather than orders is what separates an engineer who delivers value from one who delivers tickets. The output of the investigation is not a different ticket — it's a shared understanding of the underlying need, which is the only thing you can actually build against.

Three things need to surface before code is written, and none of them are usually in the ticket. The first is the real goal — what does success look like for the person asking, in terms that don't reference the proposed implementation? The second is the hidden constraints: the deadline that wasn't mentioned, the system that can't be touched because someone else is mid-migration, the stakeholder whose sign-off will be needed at the end. Constraints are nearly free to ask about up front and brutally expensive to discover late, because late constraints force rework. The third is the acceptance criteria the asker didn't state because they seemed too obvious to mention — the edge cases they assume you'll handle, the performance they assume you'll preserve, the existing behaviour they assume you won't break. "That's not what I meant" at the end of a project almost always traces to acceptance criteria that lived in the asker's head and never made it into yours.

The other side of this skill is knowing when to stop. There is a point past which more questions are no longer diligence — they are avoidance, or they are signalling, or they are an attempt to push the discomfort of starting onto someone else. Calibrating that point is its own judgment, and it tilts with the size of the work: a one-hour fix doesn't deserve a thirty-minute requirements interview, and a two-week project absolutely does. The heuristic that holds is to ask until you can describe the problem back in your own words and have the asker agree, and then start. Past that, you're stalling.

What this skill builds, when you practise it, is a habit of treating the front of every task as a small piece of investigative work in its own right. Not analysis paralysis, not committee-by-clarification, but a deliberate ten or thirty or sixty minutes spent making sure the thing you're about to spend days building is the thing that will actually solve the problem. Every other skill on this map — scoping, estimating, designing, reviewing, shipping — operates on whatever requirement you accept at this stage. Get this stage wrong and the rest of your craft is in service of the wrong target. Get it right and most of the work that follows becomes straightforward, because you know what you're aiming at.

The engineers who do this well don't look like they're doing anything special. They ask one or two questions that reframe the request, they confirm a constraint nobody mentioned, they write back a one-paragraph summary of what they understood and ask for corrections — and then they go build. The engineers who don't do it well are usually working harder, building more, and shipping things that get sent back. The difference between them is not effort. It's the willingness to spend ten minutes interrogating the request before treating it as work.

## Level 2 candidates

**The XY Problem** — The pattern where someone asks for help with their attempted solution rather than the underlying problem, and the question ("what are you actually trying to accomplish?") that defuses it. Worth deeper treatment because the pattern shows up in dozens of disguises and recognising each variant takes practice beyond just knowing the name.

**Eliciting the Unspoken Acceptance Criteria** — The success conditions an asker doesn't state because they feel obvious to them, and the techniques for surfacing them before you build rather than after. Deserves depth because the specific moves — example-driven elicitation, edge-case probing, "what would make this a failure" — are learnable craft, not just awareness.

**Distinguishing the Need From the Proposed Solution** — The skill of separating "what they want to happen" from "how they've suggested doing it," even when the request is phrased entirely as the latter. Worth its own post because the linguistic and conversational moves for doing this without sounding like you're rejecting the request are subtle.

**Surfacing Hidden Constraints Early** — The deadline, the off-limits system, the required sign-off, the political third rail — constraints that exist but weren't mentioned, and the up-front questions that flush them out. Deserves depth because the catalogue of constraint types and the questions that find each one is genuinely useful reference material.

**When to Stop Clarifying and Start Building** — The judgment about when further questions stop being diligence and start being avoidance, and how that judgment scales with the size and reversibility of the work. Worth deeper treatment because miscalibrating in either direction has costs, and the heuristics for finding the right point are non-obvious.

---