## Metadata
- **Date:** 11-06-2026
- **Source:** 04_the_context_window_as_a_contract.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-04 · The Context Window as a Contract

The first instinct when an agent does something baffling — invents a function that doesn't exist, edits a file in a directory it was never shown, confidently references a config key that's just wrong — is to reach for the model. Wrong model, bad model, hallucinating model. Almost always, the actual fault is upstream of the model entirely. The agent acted on what it had. What it had was incomplete. The gap got filled with something that sounded right.

The mental shift worth making is to stop thinking of context as input and start thinking of it as a contract. Everything inside the context window is, for the duration of this turn, the agent's entire universe: the codebase it believes exists, the conventions it believes you follow, the task it believes you asked for, the tools it believes are available, the history it believes happened. Anything outside the window does not exist from the agent's perspective. There is no background knowledge it can quietly consult, no "and obviously you also meant" it can fall back on. There are only two things: what's in the window, and the model's priors about what code like this usually looks like. When the first runs out, the second takes over — silently, fluently, and without raising an error.

This is the property that makes context failures so dangerous. A missing import throws an exception. A missing piece of context produces a paragraph of plausible reasoning and a diff that looks like it was written by someone who knows what they're doing. The agent does not say "I don't know what your auth middleware looks like, so I'm guessing." It guesses, and the guess is shaped by every similar codebase the model has ever seen. You get the median of the internet's opinion about what your code probably does, presented in your project's voice. Confabulation, not error. The worst kind of failure mode, because it survives a casual review.

Once you see context as a contract, the practical questions reorder themselves. The question stops being "is the model good enough" and becomes "what does the agent actually have in the window right now, and what is it being forced to invent to fill the gaps." That reframing changes how you set up projects, how you write prompts, and how you read failures. A test the agent broke in a strange way is rarely a model problem; it's usually a context problem — the agent didn't have the file that explained why the test was structured that way, so it pattern-matched to a more common shape and rewrote it to fit.

Several distinct failure modes live inside this single concept, and they're worth naming because they don't all look the same in practice. Context can degrade over a long session even before the hard token limit — output quality erodes as relevant information gets buried under accumulated turns, and the degradation is gradual enough to be invisible until something snaps. Context can be augmented through retrieval, which extends the window's reach but introduces a seam between what was authoritatively given and what was fetched on the fly, and the agent treats both with the same confidence regardless of source. Context can be made persistent through instruction files — the AGENTS.md, CLAUDE.md, .cursorrules surface that most engineers underuse — which is the highest-leverage place to encode the conventions and constraints you'd otherwise have to repeat every session. And context can be poisoned: hostile or noisy content in a retrieved file can redirect behaviour without any visible signal, because from inside the window there is no distinction between instructions you wrote and instructions that arrived in data.

The skill this topic builds is reading agent failures correctly. When something goes wrong, the first question is no longer "was the model confused" but "what was in the window, what was missing, and what did the model fill the gap with." That question is almost always answerable, and it usually points to a fix that's structural — a file added to the persistent context, a clearer specification, a smaller and more focused scope — rather than a fix that's prompt-level. Engineers who internalise this stop trying to out-prompt confabulation and start engineering the contract instead.

The practical takeaway is that context is the most controllable variable in the system and the one most engineers treat as background. You don't pick the model's weights. You don't rewrite the scaffold. But you do, every single turn, decide what the agent gets to see — and that decision determines whether it's reasoning about your codebase or about a plausible-looking average of every codebase. Treat the window as a specification you're authoring, not a buffer you're filling, and the entire failure surface contracts.

## Level 2 candidates

**Context rot** — How agent output quality degrades over long sessions before the hard context limit is reached, as relevant information gets buried, displaced, or de-weighted under accumulated turns. Worth a deep dive because the degradation is gradual and invisible, and the practical mitigations (session resets, summarisation, scope narrowing) are not obvious from the Level 1 framing.

**Retrieval-augmented context** — What RAG actually adds to a coding agent, what it cannot substitute for, and where the seam between retrieved content and authoritatively-provided content creates trust problems. Worth going deeper because retrieval is increasingly the default mechanism for extending context, and the failure modes — stale embeddings, wrong-chunk retrieval, retrieved-as-authoritative confusion — have specific shapes worth recognising.

**Instruction files as the persistent context surface** — Why AGENTS.md, CLAUDE.md, and .cursorrules are the highest-leverage configuration surface in most agentic workflows, what belongs in them versus what belongs in a per-session prompt, and why a cross-tool standard is converging. Worth its own treatment because the practice of authoring these well is genuinely a craft, and most engineers underuse it by an order of magnitude.

**Context poisoning** — How malicious or noisy content embedded in retrieved files, dependencies, or repository data can redirect agent behaviour without triggering any visible error, because the agent has no mechanism to distinguish data from instruction. Worth deeper coverage because it sits at the intersection of context and trust boundaries, and the defenses are architectural rather than prompt-level.

**Confabulation diagnostics** — How to read an agent's output for signs that it filled a context gap with priors rather than with grounded information, and the specific tells (overly-conventional structure, references to things you never specified, suspiciously generic naming) that distinguish guessed-from-priors from given-by-context. Worth a deep dive because this is the diagnostic skill that the Level 1 framing implies but doesn't teach in detail.

---