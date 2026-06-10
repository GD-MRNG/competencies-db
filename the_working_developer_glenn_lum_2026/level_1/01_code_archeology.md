## Metadata
- **Date:** 11-06-2026
- **Source:** 01_code_archeology.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-01 · Code Archaeology

The mental image most people carry of a working programmer is someone typing. The reality is someone reading. By a wide margin, the dominant activity of professional development is reconstructing what code already does and why someone wrote it that way, and the writing — when it finally happens — is a small, careful intervention into a structure you are mostly trying not to break. The trouble is that the code you read was almost never written for you. It was written by someone now gone, under constraints no longer documented, against a version of the system that no longer exists, and the comments, if any, describe an earlier intention rather than the current behaviour. You are reading the surface of a site whose original builders left no plans.

This is why the useful framing is archaeology rather than reading. An archaeologist does not stare harder at a potsherd; they know which layer to dig in, which artefacts carry information, and which questions the evidence can actually answer. Code archaeology is the same discipline applied to a system: knowing where to look first, in what order, to build an accurate working model of an unfamiliar codebase in hours rather than weeks. The skill is not patience or intelligence. It is method — and like any method, it can be learned, and its absence is visible in the people who lack it.

The evidence a codebase leaves is richer than most engineers use. There is the call graph, which tells you how the parts compose and where the load-bearing seams are. There are the data shapes — the types, the schemas, the wire formats — which constrain what the system can possibly be doing far more tightly than the procedural code that operates on them. There are the names, which are a layer of intent fossilised in the source: names that drift from their referents are themselves clues about where the design has shifted underneath. There are the tests, which encode what the author believed the code should do and which often double as the only honest specification you will find. And there is the commit history — by far the most under-used evidence in the entire codebase.

The shift that turns version history from an audit log into a reasoning tool is treating `git blame` and `git log` as answers to *why*, not just *who*. A confusing line of code, examined in isolation, looks arbitrary. The same line, traced back to the commit that introduced it, often resolves into a decision: a bug fix referencing a ticket, a workaround for a dependency that no longer behaves the same way, a defensive check added after an incident. The line stops being noise and becomes a legible response to a problem that once existed. Engineers who never reach for blame spend their days surrounded by decisions they cannot interpret; engineers who do interrogate history routinely find that the strange code is the *correct* code, and that the obvious cleanup would re-introduce a bug someone already paid to discover.

This connects to the most important reflex archaeology builds, which is restraint. Chesterton's old rule — do not remove a fence until you know why it was built — is the operating principle of safe work in an inherited system, because a codebase is almost entirely fences someone else put up. The code that looks redundant is sometimes redundant and sometimes load-bearing in a way you do not yet see, and the only way to tell is to recover the reason. Engineers who lack the archaeological reflex routinely "tidy" code that was doing real work, ship the cleanup, and discover its purpose two weeks later in an incident. The cost of investigating before changing is small; the cost of skipping it is paid in production.

The other thing archaeology gives you is a map of the terrain's hazards. Every codebase has regions that punish anyone who touches them — high churn, repeated reverts, comments that read as warnings, an unusual concentration of bug fixes per line. These are detectable from the evidence itself, before you've made the mistake of going in unprepared. The senior engineers on a team often navigate the codebase as if they had a hazard overlay; in a sense they do, accumulated by scar. Learning to read those signals from history, rather than from your own scars, is what compresses years of intuition into something a new arrival can actually acquire.

Without this skill, an engineer's relationship to an unfamiliar codebase is one of low-grade fear. Changes are gambles; cleanups are catastrophes; the rational response is to touch as little as possible, which is exactly how codebases calcify into the state where no one will work on them anymore. With the skill, the codebase becomes interrogable — a structure that will answer questions if you know how to ask them. The change you make is small because you understood the system, not because you were afraid of it. That difference, repeated across every task, is most of what separates the engineer who is productive in a new codebase within a week from the one who is still cautious six months in.

## Level 2 candidates

**Building a Mental Model Fast** — Covers the deliberate order of operations for orienting in an unfamiliar system: entry points first, then data shapes, then one core flow traced end to end. Worth depth because the *sequence* is the skill, and getting it wrong is the difference between an afternoon of orientation and a week of flailing.

**The Commit History as Evidence** — Covers using `git blame` and `git log` not as forensics but as a structured interview with past decisions, including how to follow a line through renames, moves, and rewrites. Worth depth because most engineers know these commands exist and still don't reach for them when a line confuses them — the gap is in technique and habit, not awareness.

**Tracing a Request End to End** — Covers following one real request through every layer it touches, from edge to storage and back, as the fastest path from architecture diagram to predictive model. Worth depth because the move is specific and teachable, and it converts abstract system knowledge into the kind you can actually reason from.

**Reading the Tests to Recover Intent** — Covers using the test suite as the de facto specification when documentation is absent or stale, including how to read characterisation tests, fixtures, and what isn't tested. Worth depth because tests carry intent that the production code doesn't, and most engineers read them only when they fail rather than as a source of truth about design.

**Chesterton's Fence** — Covers the discipline of recovering the reason for code before removing or restructuring it, and the specific patterns of evidence (incident references, defensive checks, oddly specific conditions) that signal a fence is load-bearing. Worth depth because the principle is easy to state and surprisingly hard to apply under deadline pressure, and the failure mode is one of the most expensive in the field.

**Identifying the Cursed Regions** — Covers detecting high-risk areas of a codebase from objective signals — churn, revert frequency, bug density, ownership gaps — before you've earned the scars yourself. Worth depth because the signals are concrete and learnable, and they convert a kind of folk knowledge into something a new arrival can acquire on day one.

---