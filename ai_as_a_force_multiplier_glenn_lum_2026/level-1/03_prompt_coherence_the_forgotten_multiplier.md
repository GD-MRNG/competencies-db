## Metadata
- **Date:** 24-05-2026
- **Source:** 03_prompt_coherence_the_forgotten_multiplier.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-03 · Prompt Coherence: The Forgotten Multiplier

Most people think prompting is something you do to AI. It isn't. Prompting is something AI does to you — it forces you to articulate what you actually want, in enough detail that a system with no context about your life, your work, or your taste can produce something usable. The reason most AI output disappoints isn't that the model is weak. It's that the prompt was vague, and vague prompts surface vague thinking. If you can't describe the output you want, you don't yet know what you want. The model is just the mirror that makes this obvious.

This is the reframe: prompt coherence is not a trick layer between you and the AI. It is the single largest controllable variable in the quality of what you get back. The same model, given a sloppy prompt and a clear one, will produce outputs that differ by an order of magnitude in usefulness. No model upgrade, no plugin, no new technique closes that gap. The gap is yours. And the discipline of closing it — being precise about intent, context, and constraints — is the same discipline that makes you a better thinker independent of AI. This is why prompt coherence is the highest-leverage skill in the entire stack: it compounds with every other thing you do.

The mental model worth holding is that a prompt does three jobs at once. It sets intent (what you want produced and why), it supplies context (what the model needs to know to produce it for your specific situation), and it imposes structure (the shape, format, and constraints of the output). Most prompts fail because they only do the first one. "Write me a launch email" is pure intent — no context about the audience, the product, the tone you've used before, the action you want the reader to take, or the format you need. The model fills the gaps with statistical averages, which is exactly why the output feels generic. It is generic. You asked for the average.

Context is where most of the real work happens, and it's the part people skip because it feels like overhead. Adding three sentences about your audience, two examples of writing you've done before, and one line about what you're trying to avoid will change the output more than any clever phrasing of the request itself. But context has a ceiling — at some point you're burying the actual ask under so much background that the model loses the thread. The skill is calibration: enough context that the model can produce something specific to you, not so much that the signal drowns. You learn this by feel, by watching where outputs go wrong and asking whether the failure was a missing constraint or an over-specified one.

Structural constraints are the most underused lever. Asking for a numbered list, a JSON object, a table with specific columns, or a response that follows a specific template will radically improve reliability — not because the format itself is magic, but because structure forces the model to commit to discrete claims rather than hide behind narrative coherence. A paragraph can sound right while being wrong. A table cell either has the right value or it doesn't. The cost is that you lose some flexibility and some of the model's ability to surprise you. The trade is almost always worth it for any output you're going to act on.

Examples deserve their own mention because they're often more powerful than instructions. If you can show the model two or three examples of what good output looks like — your previous work, a reference style, a worked sample — you'll get closer to what you want than any amount of describing it in the abstract. This is because models are pattern matchers by nature, and a concrete pattern is unambiguous in a way that adjectives never are. "Write in a punchy, direct voice" is a request the model will interpret loosely. Three paragraphs of your actual punchy, direct writing is a target it can hit. When you find yourself struggling to describe what you want, stop describing and start showing.

There's a question that comes up about whether to ask the model to "think step by step" or show its reasoning. Sometimes this helps, particularly for analytical tasks where the intermediate steps catch errors the final answer would have hidden. Sometimes it produces fluent-sounding reasoning that's actually post-hoc rationalization for an answer the model would have given anyway. The honest answer is that it depends on the task, and the only way to know is to test both versions and compare. Treat any prompting heuristic — including this one — as a hypothesis, not a rule.

The trap to avoid is treating prompting as a collection of incantations to be memorized. The people who write the best prompts aren't the ones who learned a framework; they're the ones who developed the habit of asking, before they hit send, "Have I been clear about what I want, what context matters, and what shape the output should take?" That question is the entire skill. Everything else is variation. Build that habit and you'll outperform people using more sophisticated tools, because they're typing fast and you're thinking first. The forgotten multiplier isn't in the model. It's in the moment before you talk to it.

## Level 2 candidates

**Context layers in prompts** — How much background to include, how to layer it (role, situation, examples, constraints), and how models behave differently as context accumulates. Worth deeper treatment because calibration is the single biggest determinant of output quality and it cannot be reduced to a rule of thumb.

**Framing effects** — Why the same request phrased three different ways produces vastly different output, and how to test framings systematically rather than randomly. Deserves its own treatment because most users blame the model for what is actually a framing problem, and learning to debug framing is a teachable empirical skill.

**Structured output formats** — When and why to demand JSON, tables, schemas, or templates instead of natural language, and the trade-offs you accept in flexibility. Worth depth because the reliability gain is large but the failure modes (over-constraint, broken outputs, brittleness) are non-obvious until you've experienced them.

**Example-driven prompting (few-shot)** — How to use examples to teach style, format, or judgment, and why showing usually beats telling. Worth a deeper post because the technique is consistently underused and the practical question of "which examples, in what order, with how much variation" has real depth.

**The role of "thinking" in prompts** — When asking a model to reason aloud genuinely improves output versus when it produces hallucinated justifications. Deserves its own treatment because the conventional wisdom (always ask for reasoning) is wrong often enough to matter, and the conditions for each case are learnable.

**Prompt iteration and versioning** — How to refine prompts systematically over time, save what works, and avoid relitigating the same setup every session. Worth depth because most users redo prompt work constantly without realizing they're rebuilding the same scaffolding, and a small amount of discipline here compounds enormously.

---