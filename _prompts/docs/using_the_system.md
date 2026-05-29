# Using the Competency System

## Why this system exists

This is personal knowledge infrastructure. The goal is not mastery of everything — it is a durable floor of understanding across the domains that matter, so that after any break, any shift, any disruption, you are never starting from zero. You always have structure to return to, entry points to re-engage from, and principles to reason with.

Return to this file when you come back to the system. The documents are the material. This is the reason they exist.

## Why systematising compounds knowledge

Structure does two things that raw notes cannot.

**It forces honest encoding.** When you have to place something in a map — decide what group it belongs to, what depends on it, what it unlocks — you discover whether you actually understood it or just recognised it. Recognition feels like knowledge but evaporates under pressure. Placement requires understanding.

**It creates re-entry points.** Knowledge decays with disuse, but not evenly. Detail fades first; structure fades last. If you documented the structure, you can reconstruct the detail from it far faster than learning from scratch. The map survives even when the specifics have gone quiet.

The compounding is specifically about connections. An isolated fact has value proportional to itself. A fact connected to five others has value proportional to all five — because recalling it recalls the others, and any of the five can retrieve it. The more connections exist, the more the network self-reinforces. That is the non-linear growth.

A useful analogy: a list of addresses has information; a city has infrastructure. You can navigate a city, find shortcuts, notice when something is missing. This system is infrastructure, not a list.

**What the level system adds on top** is honest depth signalling. A Level 1 doc means you can describe it. A Level 3 doc means you have built with it. The system prevents conflating "filed it" with "know it" — which is where most knowledge management breaks down.

## The course pipeline, step by step

When you finish a course, book, or other piece of structured learning material:

1. **Create the course folder.** At the repo root, create `<course-name>/`. Inside, create `level-1/`, `level-2/`, `level-3/` subfolders. Skip the deeper ones until you need them.

2. **Generate Level 0.** Feed whatever you have on hand — course description, syllabus, table of contents, blurb, your own notes — into `prompts/level_0.md` as `{course_input}`. Save the output as `<course-name>/level-0.md`. The output's Topic Inventory is your worklist for Level 1.

3. **Generate Level 1 docs, one topic at a time.** For each topic in the inventory, gather the corresponding chapter or module text. Run `prompts/level_1.md` with `{level_0_summary}` and `{module_content}`. Save as `<course-name>/level-1/<topic-slug>.md`. Each Level 1 doc ends with a `## Level 2 candidates` section — that's your worklist for descent.

4. **Stop here for most topics.** Level 1 is enough for most learners on most topics. There is no obligation to descend further.

5. **Generate Level 2 docs for the sub-concepts that warrant depth.** Pick a candidate from the parent Level 1 handoff list. Run `prompts/level_2.md` with `{level_0_summary}`, `{level_1_post}`, and `{level_2_candidate}`. Save as `<course-name>/level-2/<topic-slug>--<sub-concept-slug>.md`.

6. **Generate the Level 3 handoff for sub-concepts you want to practise.** Run `prompts/level_3_handoff.md` with `{level_2_post}`. The output is a Stage 1 analysis followed by either three exercise proposals or three Alternative Practice Proposals, depending on whether the material is hands-on or conceptual. Append it to the Level 2 file or save it alongside — your call.

7. **Generate Level 3 build posts.** Pick one of the three proposals. Run `prompts/level_3.md` with `{level_0_summary}`, `{level_2_post}`, and `{exercise_description}`. Save as `<course-name>/level-3/<topic-slug>--<sub-concept-slug>--<exercise-slug>.md`.

The course pipeline ends here. Levels 4 and 5 are not run from course material.

## Levels 4 and 5

Levels 4 and 5 are deliberately not part of the course pipeline.

**Level 4 (design judgment)** is written from real decisions you have made under real constraints. The Level 4 prompt treats you as the author and itself as an editor. Without your notes from an actual experience — an architectural decision record, an incident retrospective, design review notes, a postmortem, a rough write-up — there is nothing to edit.

**Level 5 (teaching and advocacy)** is written when you are actually trying to change how others practice. A proposal for a real team. A mentoring guide for a real person. A workshop outline for a real audience. Without that organisational context, Level 5 has no audience and no purpose.

Both prompts are experimental. They work best with substantive real input and a willingness to iterate. Treat the output as a draft to argue with, not a deliverable to ship.

If you have not yet encountered a real failure, decision, or advocacy moment in a topic, that is useful self-assessment information: you are not yet at Level 4 or 5 for that topic, and the doc should wait until you are.

## Non-technical material

The prompts are written so the model adapts to the actual material rather than assuming everything is technical. A book on negotiation, a course on systems thinking, a workshop on facilitation — all of them produce useful output through the same pipeline.

The structural sections stay constant; the surface choices shift based on what the source material actually is.

The Level 3 handoff has a built-in fork for this. If the material does not naturally support hands-on exercises at the ten-minute scale, it produces three Alternative Practice Proposals instead — for example:

- a structured reflection against a system you already work on
- an annotated evaluation of a real artefact using the article's framework
- a decision audit applying the article's criteria to a past choice
- a comparative analysis using the article's concepts as the evaluative lens

## Running prompts

To run a prompt by hand: substitute the `{placeholders}` with your actual content, paste the result into a long-context model, and save the response to the right file location.

For repeated use, a small Python script that reads the prompt file, substitutes variables, calls a model, and writes the output to a slugged path is straightforward. The system assumes such an orchestrator exists but does not require one.

## Self-assessment

The five levels map directly onto a 1–5 mastery scale:

- **1.** Heard the term, can't explain it. *(No doc yet.)*
- **2.** Can describe it superficially. *(Level 1 written.)*
- **3.** Have built or used it in practice. *(Level 3 done.)*
- **4.** Have debugged real failures and made tradeoffs. *(Level 4 written from real notes.)*
- **5.** Can teach it and design systems around it. *(Level 5 artifact landed in a real audience.)*

The level of doc you can honestly write for a topic is a strong signal of where you actually sit on that scale.

## What this system is not

Not a second brain. Not a note-taking system. Not a substitute for experience.
It is infrastructure — built during the calm, so the storm has less power to disorient you.
