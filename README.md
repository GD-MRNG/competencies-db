# competencies-db

> A markdown-based repository for documenting and growing competencies over time.

This repo is built around the **competency system**: a layered, on-demand documentation pipeline that turns any course, book, or piece of structured learning into a depth tree of notes — generated only as far as you decide each topic deserves.

## What this repo is

When you finish a course or read a book, the conventional move is to leave with a few highlights and maybe a summary. Six months later most of it is gone. This repo is meant to replace that with a deliberate, layered set of documents where each layer represents one increment of mastery for a given topic.

You do not generate every layer for every topic. You start at the top and descend only into the topics where deeper mastery is worth the effort. Most courses terminate at Level 1 across most topics, with a few branches going deeper.

The result is a **competencies database**: a structured body of notes that shows not only what you know, but how you arrived there.

The system works for technical material (a DevOps course, a security certification, a database book) and for non-technical material (a course on negotiation, a book on systems thinking). The prompts adapt to whatever the source material actually is.

## What the competency system is

The competency system is the method this repo uses.

Each prompt is a self-contained markdown file that declares its inputs as named placeholders (`{course_input}`, `{level_2_candidate}`, etc.) and its expected output. Each level produces both a document and a structured handoff that gives direction to the next layer.

The repo is the database of competency artifacts. The competency system is the process used to create and extend them.

## The five levels

Each course folder contains documents organised across five levels of mastery. The first three are generated as you learn. The last two are written when you have real-world experience to draw on.

**Level 0 — The Map.** A compact orientation document for the course or book itself: its intent, its purpose, its objectives, and an inventory of the topics it covers. One per course.

**Level 1 — The Concept Post.** Per-topic articles that answer "what is this and why does it matter." Builds the working mental model. Most courses terminate at Level 1 across most topics.

**Level 2 — The Depth Post.** Per-sub-concept articles that go beneath the mental model and explain how the thing actually works — its mechanics, its real tradeoffs, where it breaks. Generated only for sub-concepts you decide warrant deeper treatment.

**Level 3 — The Build Post.** A short, hands-on exercise that forces you to use a sub-concept under real conditions for the first time. Scoped to roughly ten minutes by a reader with the right tools already installed.

**Level 4 — The Design Judgment Post.** *Experimental.* An account of a real decision you made under real constraints, the alternatives you weighed, what happened, and what changed in how you now think about this class of problem. **Cannot be generated from a course** — it requires real experience.

**Level 5 — The Teaching and Advocacy Artifact.** *Experimental.* An artifact aimed at changing how others practice — a proposal, a mentoring guide, a workshop outline, an adoption guide. Like Level 4, this requires real experience and an actual organisational context.

For learners, **Levels 0 through 3 are the working surface**. Levels 4 and 5 happen later, after the practice has been lived.

## How the prompts chain together

```text
Course materials
        │
        ▼
   level_0.md  ─►  Level 0 doc (course map + topic inventory)
        │
        ▼
   level_1.md  ─►  Level 1 docs, one per topic
                    (each ends with ## Level 2 candidates)
        │
        ▼  (optional, per topic worth deeper treatment)
   level_2.md  ─►  Level 2 docs, one per sub-concept
                    (ends at ## Key Takeaways)
        │
        ▼  (optional, per sub-concept worth practising)
level_3_handoff.md  ─►  Three exercise candidates with full spec
        │
        ▼
   level_3.md  ─►  Level 3 build post, one per chosen exercise

  ── Course pipeline ends here ──

  Levels 4 and 5 are experience-driven and run separately,
  not as part of the course pipeline.

   level_4.md  ─►  Level 4 doc, drafted from your own decision notes
   level_5.md  ─►  Level 5 artifact, drafted for a real audience
```

## Repo layout

The courses and books live at the first level of the repository. There is no separate central course directory.

```text
competencies-db/
  README.md
  prompts/
    level_0.md
    level_1.md
    level_2.md
    level_3_handoff.md
    level_3.md
    level_4.md
    level_5.md
  <course-name>/
    level-0.md
    level-1/
      <topic-slug>.md
    level-2/
      <topic-slug>--<sub-concept-slug>.md
    level-3/
      <topic-slug>--<sub-concept-slug>--<exercise-slug>.md
    level-4/
    level-5/
```

Filenames carry lineage. A Level 2 doc filename includes the parent Level 1 slug; a Level 3 doc includes both. Splitting any filename on the `--` separator gives you back the chain, so any leaf can be traced to its root without consulting an index.

## GitHub first, Obsidian later

This system is designed to work perfectly well as a plain Markdown repository on GitHub.

Every artifact is a normal `.md` file stored in a predictable folder structure, so the repo is already readable and navigable without any specialised tooling. You can browse course maps, concept posts, depth posts, and build posts directly in GitHub, and version control gives you a history of how your understanding evolved over time.

That is enough for the system's first mode of use: **a GitHub-native documentation tree for learning and competency growth**.

Obsidian is a natural future extension, not a requirement. Because the repository is plain Markdown, the whole repo could later be opened as an Obsidian vault for richer navigation, search, cross-linking, and personal knowledge management. But none of that is necessary to make the system useful now.

For the current version, the design assumption is simple: **if it works cleanly as files in a GitHub repo, it is sufficient**.

## How to use it for learning

When you finish a course, book, or other piece of structured learning material:

1. **Create the course folder.** At the repo root, create `<course-name>/`. Inside, create `level-1/`, `level-2/`, `level-3/` subfolders. Skip the deeper ones until you need them.

2. **Generate Level 0.** Feed whatever you have on hand — course description, syllabus, table of contents, blurb, your own notes — into `prompts/level_0.md` as `{course_input}`. Save the output as `<course-name>/level-0.md`. The output's Topic Inventory is your worklist for Level 1.

3. **Generate Level 1 docs, one topic at a time.** For each topic in the inventory, gather the corresponding chapter or module text. Run `prompts/level_1.md` with `{level_0_summary}` and `{module_content}`. Save as `<course-name>/level-1/<topic-slug>.md`. Each Level 1 doc ends with a `## Level 2 candidates` section — that's your worklist for descent.

4. **Stop here for most topics.** Level 1 is enough for most learners on most topics. There is no obligation to descend further.

5. **Generate Level 2 docs for the sub-concepts that warrant depth.** Pick a candidate from the parent Level 1 handoff list. Run `prompts/level_2.md` with `{level_0_summary}`, `{level_1_post}`, and `{level_2_candidate}`. Save as `<course-name>/level-2/<topic-slug>--<sub-concept-slug>.md`.

6. **Generate the Level 3 handoff for sub-concepts you want to practise.** Run `prompts/level_3_handoff.md` with `{level_2_post}`. The output is a Stage 1 analysis followed by either three exercise proposals or three Alternative Practice Proposals, depending on whether the material is hands-on or conceptual. Append it to the Level 2 file or save it alongside — your call.

7. **Generate Level 3 build posts.** Pick one of the three proposals. Run `prompts/level_3.md` with `{level_0_summary}`, `{level_2_post}`, and `{exercise_description}`. Save as `<course-name>/level-3/<topic-slug>--<sub-concept-slug>--<exercise-slug>.md`.

That is the course pipeline. **Levels 4 and 5 are not run from course material** — see below.

## Adding a new course or book

The minimum steps to start a new course folder:

```bash
mkdir -p <course-name>/level-1 <course-name>/level-2 <course-name>/level-3
```

Then run the Level 0 prompt as described above. Everything else flows from there.

A few naming conventions that pay off later:

- **Course folder names.** Kebab-case, descriptive enough to be unambiguous a year from now (`devops-fundamentals`, not `course-1`).
- **Topic slugs.** Kebab-case, taken from the most distinctive nouns of the topic (`networking-fundamentals`, `dns-resolution-chain`).
- **Lineage separator.** Use `--` between segments in filenames at Level 2 and below.

Examples:

```text
devops-fundamentals/level-0.md
devops-fundamentals/level-1/networking-fundamentals.md
devops-fundamentals/level-2/networking-fundamentals--dns-resolution-chain.md
devops-fundamentals/level-3/networking-fundamentals--dns-resolution-chain--watch-time-wait.md
```

## Non-technical material

The prompts are written so the model adapts to the actual material rather than assuming everything is technical. A book on negotiation, a course on systems thinking, a workshop on facilitation — all of them produce useful output through the same pipeline.

The structural sections stay constant; the surface choices shift based on what the source material actually is.

The Level 3 handoff has a built-in fork for this. If the material does not naturally support hands-on exercises at the ten-minute scale, it produces three Alternative Practice Proposals instead — for example:

- a structured reflection against a system you already work on
- an annotated evaluation of a real artefact using the article's framework
- a decision audit applying the article's criteria to a past choice
- a comparative analysis using the article's concepts as the evaluative lens

## A note on Levels 4 and 5

Levels 4 and 5 are deliberately **not** part of the course pipeline.

Level 4 (design judgment) is written from real decisions you have made under real constraints. The Level 4 prompt treats you as the author and itself as an editor. Without your notes from an actual experience — an architectural decision record, a postmortem, a design review, or a rough write-up — there is nothing to edit.

Level 5 (teaching and advocacy) is written when you are actually trying to change how others practice. A proposal for a real team. A mentoring guide for a real person. A workshop outline for a real audience. Without that organisational context, Level 5 has no audience and no purpose.

Both prompts are experimental. They work best with substantive real input and a willingness to iterate. Treat the output as a draft to argue with, not a deliverable to ship.

If you have not yet encountered a real failure, decision, or advocacy moment in a topic, that is useful self-assessment information: you are not yet at Level 4 or 5 for that topic, and the doc should wait until you are.

## Working with the prompts

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

## Licensing

No license has been assigned to this repository at this time. The contents are published for viewing and reference only unless explicit permission is given otherwise.