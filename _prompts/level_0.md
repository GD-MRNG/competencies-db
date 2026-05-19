# Level 0 Prompt

Generate a Level 0 orientation document for a course or book. This document is the top-level reference for a competency system — it captures what the course is and what it covers, and is fed in as context when generating deeper articles.

## Input

```
{course_input}
```

The input may be a course description, syllabus, table of contents, book blurb, stated objectives, personal notes, or any combination of these. It may be partial or rough.

## Output

A markdown document with two sections.

### Summary

A short prose summary (three to six paragraphs) covering:

- the course's **intent** — what it is fundamentally about
- its **purpose** — why someone would take it; the problem it addresses
- its **objectives** — what a learner should come away knowing or being able to do

### Topics

A list of the topics the course covers, each with a one-to-two-sentence description. Use the granularity of the source — modules, chapters, or sections. Format each entry as:

**Topic name** — one or two sentences on what the topic covers.

## Rules

- Do not invent content. If something is inferred rather than stated in the input, mark it "(inferred)".
- Do not assume the course is technical; adapt to the actual material.
- Output only the document — no preamble, no commentary.
