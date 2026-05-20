# competencies-db

> A markdown-based repository for documenting and growing competencies over time.

## What this is

When you finish a course or read a book, the conventional move is to leave with a few highlights and maybe a summary. Six months later most of it is gone. This repo replaces that with a layered set of documents where each layer represents one increment of mastery for a given topic.

You do not generate every layer for every topic. You start at the top and descend only into the topics where deeper mastery is worth the effort. The result is a structured body of notes that shows not only what you know, but how you arrived there.

The system works for technical material (a DevOps course, a security certification, a database book) and non-technical material (a course on negotiation, a book on systems thinking).

## How it works

Each course or book lives in its own top-level folder. Every folder is organised across five levels:

| Level | Purpose |
|---|---|
| 0 | Course map — intent, objectives, topic inventory |
| 1 | Concept post — what it is and why it matters, one per topic |
| 2 | Depth post — mechanics, tradeoffs, where it breaks, one per sub-concept |
| 3 | Build post — a short hands-on exercise (~10 minutes) |
| 4 | Design judgment — a real decision under real constraints *(from experience, not courses)* |
| 5 | Teaching artifact — a proposal, guide, or workshop for a real audience *(from experience)* |

A prompt file in `_prompts/` drives each level. Each prompt declares its inputs as named `{placeholders}`. The pipeline chains naturally: each level's output contains a handoff section that gives direction to the next.

```
Course materials → level_0.md → level_1.md → level_2.md → level_3_handoff.md → level_3.md
```

Levels 4 and 5 run separately from real-world experience, not course material.

## How to use it

**Start a new course:**

```bash
mkdir -p <course-name>/level-1 <course-name>/level-2 <course-name>/level-3
```

Then feed your course materials into `_prompts/level_0.md` and save the output as `<course-name>/level-0.md`. The Topic Inventory in that output is your worklist for Level 1.

**Generate Level 1 docs** one topic at a time using `_prompts/level_1.md`. Each output ends with a `## Level 2 candidates` section — your worklist for descent.

**Stop at Level 1 for most topics.** Descend to Level 2 and 3 only for sub-concepts where deeper mastery is worth the effort.

For full step-by-step instructions, see [`_prompts/docs/using-the-system.md`](_prompts/docs/using-the-system.md).

## Repo layout

```
competencies-db/
  _prompts/          # prompt files (level_0.md … level_5.md, learning_companion.md, etc.)
    docs/            # design notes for the prompts
  <course-name>/
    level-0.md
    level-1/
    level-2/
    level-3/
    level-4/
    level-5/
```

Filenames carry lineage. A Level 2 filename includes the parent Level 1 slug; a Level 3 filename includes both. Splitting any filename on `--` gives back the full parent chain.

## Licensing

No license has been assigned to this repository at this time. The contents are published for viewing and reference only unless explicit permission is given otherwise.
