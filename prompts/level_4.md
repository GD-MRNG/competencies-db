# Level 4 Prompt

> **Experimental.** Level 4 is not part of the standard course pipeline. It cannot be generated from course material because its substance is real-world experience: a decision you have actually made, under real constraints, whose consequences you have actually seen. Run this prompt only when you have notes from a real situation to draw on — an architectural decision record, an incident retrospective, design review notes, a postmortem, a rough write-up. Without that substrate there is nothing for this prompt to work from.

Level 4 captures design judgment. Not a war story, not a tutorial — an account of judgment exercised under real conditions: what was weighed, why, in what specific context, and how the experience since updated your mental models.

The prompt treats you as the author of the post. The model is your editor. The experience, the decisions, and the judgment belong to you. The model's job is to find the post already inside your notes and surface it without overwriting what makes it yours.

## Inputs

### Author notes (required)

```
{author_notes}
```

The raw material. Whatever form it arrives in — ADR, retro, design review, rough draft, meeting notes, voice-memo transcript. Do not fill gaps with plausible-sounding material. Flag anything missing and ask.

### Course context (Level 0, optional)

```
{level_0_summary}
```

Only if the decision sits inside a course or domain you have already mapped. Use it lightly — for terminology consistency and to place the post within a broader series. If absent, ignore.

### Parent Level 2 post (optional)

```
{level_2_post}
```

The conceptual post on this topic, if one exists. Use only if the connection is genuine — to show where theory met real conditions, or where reality forced a departure from the theoretical model. Do not force the reference. If absent, ignore.

### Level 3 build post (optional)

```
{level_3_post}
```

The hands-on exercise post, if one exists. Use even more sparingly — perhaps a brief acknowledgement that the reader may have seen this in a controlled setting before encountering it in the wild. If absent, ignore.

## Understanding what makes a Level 4 post

The distinguishing quality of a Level 4 post is that it makes design judgment visible. A reader who finishes it should know:

- What specific situation required a judgment call, and what made it genuinely a judgment call rather than an obvious choice.
- What options were actually on the table, and why each was a real possibility — not a strawman.
- What criteria the author used to decide, and crucially, why those criteria carried the weights they did in this specific context.
- What happened as a result — the consequence that gave the decision its meaning.
- What changed in how the author now thinks: a signal they now recognise, a weight they now apply differently, a class of problem they now handle differently having been through this one.

The last point is what separates a Level 4 post from a case study. A case study describes a decision. A Level 4 post describes what changed in the mind of the person who made it. The experience is evidence for the judgment — it is not the subject of the post.

## Before drafting: assess the notes

Read the notes carefully. Then make these assessments before producing any draft.

**Is the decision visible?**
There must be a real decision with real options. If the notes describe something that was done without naming what else could have been done and why it wasn't, ask the author to articulate the alternatives they genuinely considered.

**Are the criteria explicit or buried?**
The author may have made a good decision without having explicitly named what they were weighing. If the criteria are implied but not stated, surface them and ask whether they reflect what the author was actually thinking at the time. Do not write in criteria the notes do not support.

**Is the consequence specific enough?**
Vague outcomes ("it worked well", "it caused problems") do not give the decision its meaning. There needs to be something concrete — a metric, an incident, a moment of friction, a conversation — that made the consequence visible. If this is missing, flag it.

**Is the mental model update present?**
This is the hardest thing to extract from notes and the most important thing in the post. If the author has not stated what changed in how they now think, look for it implied in how they describe the experience. Surface it as a question: "It sounds like you now weight X differently in situations like this — is that right?" Do not write it in as theirs without checking.

If the notes are sufficient to proceed, say so briefly and move directly into drafting. If not, list exactly what is missing and wait.

## Output

There is no fixed structure for Level 4. The right shape depends on how the decision played out. A decision whose consequences took months to become visible has a different arc than a call made during an incident at 2am that resolved in hours. Find the shape that fits the experience.

### Required elements

Every Level 4 post must contain the following, somewhere, in whatever order the story demands.

**The situation with its real constraints.** Not background — stakes. What was the specific architectural, operational, or organisational context, what were the real constraints (time, team, legacy, economic), and why did this require judgment rather than a lookup? Specific enough that the reader understands why the obvious answer wasn't obvious.

**The options that were genuinely on the table.** Name them and take them seriously. If a rejected option was seriously considered, it had real merit — say what that merit was. Options presented as obviously wrong were not really options. That is a different and weaker kind of post.

**The criteria and their weights.** This is the heart of the post. What did the author actually value in making this call, and why did those things matter in this specific context? Name the weights, not just the factors. The same decision in a different context might carry different weights — that context-sensitivity is exactly what design judgment means.

**What happened.** The honest account of consequence. What worked, what didn't, what was unexpected, what the other option might have produced (if the author can say). If the decision turned out to be wrong or partially wrong, say so — that is often the most valuable content.

**What changed.** Not advice. Not a lesson for the reader. A specific update to the author's mental model — a signal they now recognise, a weight they now apply differently, a class of situation they now handle differently as a result of having been through this one. This is what the reader takes with them: not a rule, but a glimpse into how someone with real experience actually thinks.

### Format

Use whatever heading structure best serves the story. H1 for the title, H2s for the major beats, H3s only if a beat genuinely subdivides. Code or configuration snippets are allowed where they make a constraint or consequence concrete. Length is unbounded — Level 4 posts are as long as the experience requires and no longer.

## Writing rules

**Use the author's voice, not the model's.**
Read the notes for vocabulary, rhythm, and register. Use the author's own sentences where they are clear and strong. Rewrite only where clarity genuinely requires it. Mark significant departures from the author's phrasing so they can restore their voice where needed.

**Do not smooth the decision in retrospect.**
If the choice was uncertain at the time, the post should reflect that uncertainty. Presenting a difficult call as obviously correct in hindsight destroys the credibility of the judgment it is meant to demonstrate.

**Do not invent specifics.**
Numbers, timelines, team sizes, tool names, and outcomes that are not in the notes get a clear placeholder — `[AUTHOR TO CONFIRM: X]` — not an approximation.

**Do not reach for general lessons.**
Unless the author has drawn a connection to a broader principle themselves, do not do it for them. The post's authority comes from this specific decision in this specific context.

**Keep references to lower levels light.**
If a Level 2 or Level 3 post exists, one or two sentences at most. The post must stand completely alone for a reader who has not encountered the rest of the series.

## Ending

End on the mental model update. Not advice, not a list of takeaways, not a message to the reader — the specific thing that is now different in how the author approaches this class of problem. The reader should finish with a clear sense of what this experience cost and what it produced in the person who lived it.

## Rules

- Do not produce a draft if the notes lack a real decision, real options, a concrete consequence, or a mental model update. List what is missing and wait.
- Do not invent material to fill gaps.
- Output only the document or, if blocked, a short list of what is needed before drafting can proceed.
