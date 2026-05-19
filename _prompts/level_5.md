# Level 5 Prompt

> **Experimental.** Level 5 is not part of the standard course pipeline. It is run when you are actually trying to change how others practice — a real proposal for a real team, a mentoring guide for a real person, a workshop outline for a real audience. Without an actual organisational context and audience, Level 5 has no purpose. Treat the output as a draft to argue with, not a deliverable to ship.

Level 5 is about organisational impact — the ability to change the practices of others, not just your own work. This is fundamentally different from every earlier level. You are not documenting your knowledge or recounting your experience. You are trying to move people who do not yet share your understanding, within an organisation that has its own constraints, habits, and resistance points.

Success at Level 5 is not measured by whether the artifact communicates clearly. It is measured by whether the audience actually changed their practice. That distinction shapes everything about how the artifact should be written.

The model's role is to help produce an artifact that works. It is not the strategist; it is the editor and structurer. Strategy belongs to the author, who knows the audience.

## When Level 5 shows up

- Writing a proposal or RFC for a team to adopt a new practice.
- Mentoring a developer through their first encounter with something unfamiliar.
- Facilitating a process the team hasn't run before — a blameless post-mortem, an architecture review, a chaos experiment.
- Giving a talk or running a workshop that changes how attendees actually work.
- Writing a guide that enables others to adopt something the author has learned to do well without direct support.

What these have in common is that the audience must do something differently as a result. An artifact that produces agreement but not action has not succeeded at Level 5.

## Inputs

### Practice description (required)

```
{practice_description}
```

A description of the practice, tool, or approach being introduced or advocated for. A paragraph is sufficient if it is clear.

### Organisational context (required)

```
{organizational_context}
```

A description of the team or organisation the author is trying to influence. Should include: current practices in this area, approximate technical maturity, likely sources of resistance or skepticism, any previous attempts to introduce this practice and what happened, and any constraints — time, tooling, process mandates — that shape what is actually adoptable. **This is the most important input.** An artifact written without understanding the audience's actual position will not produce adoption.

### Author experience (required)

```
{author_experience}
```

What gives the author credibility here? Their own use of the practice, a Level 4 account of a decision involving it, results they have seen, direct experience mentoring others through it. The audience will implicitly ask "why should I listen to you?" — the artifact needs to answer that question through evidence, not assertion.

### Artifact type (required)

```
{artifact_type}
```

What is being produced? Select one:

- **Team proposal / RFC** — a written case for adopting a practice, intended to persuade decision-makers and establish a concrete adoption plan.
- **Mentoring guide** — a structured walkthrough for a one-on-one or small-group setting, with checkpoints and common sticking points named.
- **Facilitation guide** — a guide for running a specific session or process with a team.
- **Talk or workshop outline** — a narrative and structural plan for a presentation or hands-on session.
- **Adoption guide** — a reference document enabling self-directed adoption without direct mentoring.

### Lower-level posts (optional)

```
{level_2_post}
```

```
{level_3_post}
```

```
{level_4_post}
```

Use only if they exist and only if they would actually serve the artifact: Level 2 to establish conceptual grounding for audiences who need it, Level 3 as an onboarding path for new adopters, Level 4 as evidence in advocacy sections. Do not force references. If absent, ignore.

## Before drafting: assess the context

Read all inputs carefully, then assess these before producing any draft.

**Is the resistance understood?**
Every attempt to change a team's practice meets resistance. It might be rational (the practice has real costs), habitual (people do it differently and see no reason to change), political (someone owns the current approach), or capacity-based (the team is too stretched to learn something new right now). If the organisational context does not name the likely resistance points specifically, ask. An artifact that does not engage with real objections will not produce adoption.

**Is the ask proportionate to where the audience actually is?**
A team that has never written a test should not be pitched on full TDD adoption in one proposal. A team already using CI should not be given a beginner's introduction to why CI matters. If the scope or starting point of the artifact does not match where the audience is, flag it.

**Is there a credible path to adoption?**
Good advocacy does not just argue for a practice — it shows how the practice gets started. If there is no concrete, low-friction first step that a skeptical team could take, the artifact will produce agreement but not change. Flag if this is absent from the inputs.

**Is the evidence sufficient for this audience?**
What does the author have that would convince a skeptical but reasonable colleague? Results, a real account, a demonstration, external evidence? If the organisational context suggests high skepticism and the evidence is thin, say so before drafting.

If the inputs are sufficient, say so briefly and proceed. If not, list what is missing and wait.

## Output

The shape of the artifact depends on `{artifact_type}`. Use the matching guidance below.

### Team Proposal / RFC

Three movements: the case for change, the plan for adoption, and the definition of success.

**The case for change** is made in terms the audience cares about — not the terms the author cares about. If the team is measured on incident frequency, lead with reliability. If they are measured on delivery speed, lead with the friction this practice removes. Do not lead with the correctness or elegance of the approach.

Address resistance directly and without condescension. If there is a credible objection, name it and respond to it honestly. If the practice has real costs, acknowledge them and show why the tradeoff is worth it in this specific context. Objections that are dismissed do not go away — they resurface in the review meeting.

**The adoption plan** is specific: what changes first, who is responsible, what the timeline looks like, and what the minimum viable version of the practice looks like. The minimum viable version matters — it is the difference between a proposal that gets approved and stalls, and one that produces a visible first win within a week of approval.

**Success** is defined in terms that can be pointed at, not felt.

### Mentoring Guide

Structure around what the person being mentored will encounter, in the order they will encounter it — not the logical order of the topic, but the experiential order of a first attempt.

Every section names what the mentee is likely to do wrong or find confusing at this stage, and what to do when that happens. The value of a mentoring guide over documentation is that it anticipates the human experience of learning, not just the technical content.

Include explicit checkpoints: moments where the mentor should pause and verify understanding before moving on. Name what the mentee should be able to say or do at each checkpoint to confirm they are ready to continue.

Write the guide so that a mentor who is competent but not expert in the practice can use it. The author may not always be the one delivering it.

### Facilitation Guide

Structure as a session plan: any pre-work required, an opening, the body of the session broken into phases with approximate timing, and a close.

Every phase names its purpose, the specific facilitator moves that serve that purpose, and what to do if the session is going off-track in the ways that are common for this type of session. Facilitation guides fail when they script what should happen but give the facilitator nothing to work with when something else does.

Include explicit guidance on the dynamics specific to this process. A blameless post-mortem guide needs to address what to do when conversation starts attributing blame. An architecture review guide needs to address what to do when one voice dominates. The dynamics specific to this session type matter more than general facilitation principles.

### Talk or Workshop Outline

Structure as a narrative arc, not a list of topics. An audience experiences a talk as a journey through time — they need to be oriented, moved, and landed. A list of bullets per slide is not a talk outline.

Name the state the author wants the audience in at each stage. The opening should create enough recognition that the audience believes this talk is for them. The middle should shift something — a belief, a mental model, or an awareness of a problem they had not fully seen. The end should give them something specific to do, not just something to think about.

For workshops, interleave the narrative arc with the exercises and name what each exercise is meant to produce experientially, not just what participants will do.

### Adoption Guide

Structure as a sequence of stages, each representing a distinct capability level. A reader at stage one should be able to identify themselves clearly, know exactly what to do to reach stage two, and have enough scaffolding to do it without direct support.

Assume the reader is motivated but time-constrained and skeptical of perfection. Each stage should be achievable in a single working session or sprint. The first stage should produce something tangible within hours.

Include explicit markers of "good enough for now" at each stage. A guide that implies the reader must meet a high standard of correctness before proceeding will stop most readers at stage one.

## Writing rules

**Write for the audience, not the author.**
The author already believes in the practice. Every sentence should be evaluated against the question: does this move a skeptical but reasonable colleague toward adoption? If it does not, it is probably for the author's benefit, not the audience's.

**Do not condescend.**
The audience is not failing to adopt this practice because they are less capable than the author. They are failing because they have other priorities, different mental models, and rational uncertainty about whether the change is worth the cost. Treat that as a legitimate position to be engaged, not overcome.

**Make the first step easy enough to be undeniable.**
Whatever the artifact type, there must be a first action the audience can take that is low enough in cost that declining it would feel unreasonable. Advocacy that asks for full commitment upfront rarely produces full commitment. Advocacy that produces a small win produces the conditions for the next step.

**Use the author's experience as evidence, not authority.**
"I've done this and it works" is a starting point, not an argument. Show what happened, what changed, what the audience would be able to point at if they did the same. Let the experience do the work of evidence.

**Anticipate the second objection.**
Most objections have a follow-up. Address both. "This seems like a lot of work" is the first. "But our codebase is different" is the second, and it arrives after the first has been answered. The artifact that only addresses the first produces a conversation. The one that addresses both produces a decision.

## Ending

Every artifact type ends differently, but all of them end with action.

A proposal ends with a specific, named ask — a decision, an approval, a pilot commitment. A mentoring guide ends with what the mentee does next on their own. A facilitation guide ends with the output of the session and how it gets used after the room clears. A talk ends with one concrete thing to do before the audience leaves. An adoption guide ends with a clear picture of what the practice looks like when it is fully embedded — so the reader knows what they are building toward.

Do not end with reflection. End with motion.

## Rules

- Do not produce a draft if the resistance, the ask proportionality, the adoption path, or the evidence is missing from the inputs. List what is missing and wait.
- Do not invent organisational details to fill gaps in the context.
- Output only the document or, if blocked, a short list of what is needed before drafting can proceed.
