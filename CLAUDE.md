# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Personal knowledge infrastructure. The goal is a durable floor of understanding across domains that matter — not mastery of everything, but structure that survives breaks, shifts, and disruptions. The level of document that can honestly be written for a topic is a signal of where the author actually stands. Structure outlasts detail: when specifics fade, the map remains and enables rapid reconstruction. The level system prevents conflating "filed it" with "know it."

Each course or book lives in its own top-level folder. Prompts that generate documents live in `_prompts/`. There is no build system, no test suite, and no executable code — the "pipeline" is a human (or LLM) substituting `{placeholders}` in prompt files and saving the output as markdown.

## The five levels

Every course folder is organised across five levels:

| Level | File location | Purpose |
|---|---|---|
| 0 | `<course>/level-0.md` | Course map — one file per course |
| 1 | `<course>/level-1/<topic-slug>.md` | Concept post — one per topic |
| 2 | `<course>/level-2/<topic-slug>--<sub-concept-slug>.md` | Depth post — selected sub-concepts only |
| 3 | `<course>/level-3/<topic-slug>--<sub-concept-slug>--<exercise-slug>.md` | Build post — hands-on exercise |
| 4 | `<course>/level-4/` | Design judgment — requires real experience, not generated from courses |
| 5 | `<course>/level-5/` | Teaching artifact — requires real audience |

Levels 4 and 5 are not part of the course pipeline; they are written from real-world experience.

## Naming conventions

- **Course folders:** kebab-case, descriptive (`devops-fundamentals`, not `course-1`)
- **Topic slugs:** kebab-case from the topic's most distinctive nouns (`dns-resolution-chain`)
- **Level 2+ filenames:** parent slug(s) joined with `--` separator (`topic--sub-concept--exercise`)
- **Level 1 filenames:** two conventions exist depending on source structure. Sequential modules use a two-digit prefix with underscores (`01_introduction.md`, `02_cryptography.md`). Module-and-topic encoded courses use a four-digit prefix with a hyphen separator (`11-networking-fundamentals.md` = module 1, topic 1; `21-source-control.md` = module 2, topic 1). Follow whichever convention the course folder already uses.

## How the prompt pipeline chains

```
{course_input}
      │
      ▼
_prompts/level_0.md  →  <course>/level-0.md
      │
      ▼
_prompts/level_1.md (+ level-0 + module content)  →  <course>/level-1/<slug>.md
      │
      ▼  (for sub-concepts worth depth)
_prompts/level_2.md  →  <course>/level-2/<slug>--<sub-slug>.md
      │
      ▼  (for sub-concepts to practise)
_prompts/level_3_handoff.md  →  exercise proposals (appended to level-2 or saved alongside)
      │
      ▼
_prompts/level_3.md  →  <course>/level-3/<slug>--<sub-slug>--<exercise-slug>.md
```

Each Level 1 doc ends with a `## Level 2 candidates` section — that section is the handoff to the next layer and must not be omitted.

## Adding a new course

```bash
mkdir -p <course-name>/level-1 <course-name>/level-2 <course-name>/level-3
```

Then run `_prompts/level_0.md` with the course materials to generate `<course-name>/level-0.md`.

## Prompt inputs

Each prompt declares named `{placeholder}` variables. The standard variables are:

| Prompt | Inputs |
|---|---|
| `level_0.md` | `{course_input}` |
| `level_1.md` | `{level_0_summary}`, `{module_content}` |
| `level_2.md` | `{level_0_summary}`, `{level_1_post}`, `{level_2_candidate}` |
| `level_3_handoff.md` | `{level_2_post}` |
| `level_3.md` | `{level_0_summary}`, `{level_2_post}`, `{exercise_description}` |
| `level_4.md` | `{author_notes}` (required); `{level_0_summary}`, `{level_2_post}`, `{level_3_post}` (optional) |
| `level_5.md` | `{practice_description}`, `{organizational_context}`, `{author_experience}`, `{artifact_type}` (all required); `{level_2_post}`, `{level_3_post}`, `{level_4_post}` (optional) |
| `learning_companion.md` | `{content}` (a Level 1 article) |
| `structural_companion_engineer.md` | `{content}` (a Level 1 article, engineering audience) |
| `structural_companion_analyst.md` | `{content}` (a Level 1 article, analyst audience) |
| `structural_companion_civilisation.md` | `{content}` (any historical or civilisational content) |

The structural companion prompts share a common five-section pedagogy. See `_prompts/docs/structural_companion_prompts.md` for the overarching pattern and guidance on creating new variants.

## Content rules to preserve

- Level 1 posts: flowing prose only — no subheadings, no bullet points, no code blocks, no bolded terms inside prose. 600–1500 words.
- Do not invent content. If something is inferred from inputs, mark it `(inferred)`.
- Each Level 1 post must end with a `## Level 2 candidates` section listing 3–7 sub-concepts.
- Level 2 filenames encode lineage: splitting on `--` gives back the full parent chain.
