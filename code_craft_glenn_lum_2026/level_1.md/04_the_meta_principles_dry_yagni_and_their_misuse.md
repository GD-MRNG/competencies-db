## Metadata
- **Date:** 11-06-2026
- **Source:** 04_the_meta_principles_dry_yagni_and_their_misuse.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-04 · The Meta-Principles: DRY, YAGNI, and Their Misuse

The two most-quoted acronyms in software design are also the two most reliably misapplied, and the damage they do in the wrong hands is worse than the problem they were coined to solve. DRY and YAGNI are correct. They are also, in the form most developers carry them, dangerous — because each one, pushed past the conditions under which it holds, turns into the failure mode it was meant to prevent. The skill is not knowing the rules. The skill is knowing what they were actually saying, and where they stop being true.

Start with DRY. Hunt and Thomas introduced it in *The Pragmatic Programmer* in 1999, and the original formulation is precise: every piece of *knowledge* should have a single, unambiguous, authoritative representation in the system. The principle is about knowledge — design decisions, business rules, the truth of how something works — not about text. The widespread misreading collapses "knowledge" into "code that looks similar," and that one substitution is responsible for a disproportionate share of bad abstractions in modern codebases. Two functions can share most of their lines and encode entirely different decisions; merging them couples things that have no business being coupled, and the merge becomes load-bearing right around the moment the requirements diverge.

This is the failure mode Sandi Metz named in 2016 with a maxim worth memorising: the wrong abstraction is more expensive than duplication. Duplication is visible, local, and cheap to fix — when the two copies need to differ, you change one. A wrong abstraction is none of those things. It hides the duplication behind a name, accumulates parameters and flags as the cases diverge, and develops a gravitational pull that drags every new use case into its shape whether or not it fits. By the time you realise the abstraction was wrong, multiple callers depend on it, and unwinding it is a project rather than an edit. Duplication is a problem you can see; a bad abstraction is a problem that compounds.

YAGNI comes from Extreme Programming and points the other direction: don't build what you don't yet need. The reasoning is that speculative generality — code shaped around imagined future requirements — is one of the most reliable ways to add accidental complexity, because the imagined future almost never arrives in the shape you imagined, and meanwhile you've paid the cost of carrying the generality through every change in between. Most "flexibility" added on speculation turns out to be flexibility in the wrong dimension. YAGNI says: wait until you actually know.

But YAGNI taken as a literal rule produces its own pathology. Pushed to the extreme, it becomes an excuse to ignore obvious near-term needs, to skip cheap provisions that would have cost almost nothing to include, and to treat any consideration of the future as over-engineering. There is a real difference between speculative generality (building a plugin architecture for a system that has one user) and basic foresight (using a configuration value instead of a hardcoded one when you already know it'll be different in production). YAGNI was meant to kill the first, not the second. The rule, applied without judgment, can't tell them apart.

The synthesis the field has been converging on — sometimes packaged as "avoid hasty abstractions," or AHA — resolves both failure modes with one observation: duplication is cheap to fix, and bad abstractions are not, so the asymmetry of cost should bias you toward waiting. The practical form is the rule of three: don't extract an abstraction the first time you see a pattern, don't extract it the second time, and even on the third occurrence consider carefully whether it's really one pattern or three things that happen to look alike right now. By the third occurrence you have evidence — three real use cases — about what the abstraction actually needs to be. Before that, you're guessing, and you're guessing under the same conditions YAGNI warns against on the feature side.

The deeper point underneath both principles is that they're aimed at the same enemy: complexity added on speculation. DRY misused adds it through premature abstraction; YAGNI misused fails to prevent it through premature flexibility. Both, applied with judgment, push you toward code that responds to evidence rather than imagination. Both, applied as rules, become exactly the speculative complexity they were trying to eliminate. The rules are downstream of the reasoning, and the reasoning is what survives contact with cases the original authors didn't anticipate.

What this topic actually unlocks is permission to wait. The reflex that fires when you see two similar functions — extract now, before the duplication "spreads" — is the same reflex that produces the abstractions you'll later regret. Repeating yourself for a while is not a sin. Coupling two things that shouldn't be coupled is. When you see duplication, the first question isn't "how do I remove this" but "is this the same knowledge, or two pieces of knowledge that currently look alike." If you can't answer confidently, the answer is to wait until you can.

## Level 2 candidates

**DRY Is About Knowledge, Not Text** — The principle targets duplicated *decisions*, not duplicated-looking lines, and the gap between those two readings is where most premature abstractions live. Drilling here gives you the diagnostic question — "is this the same knowledge?" — that stops you from merging two things that are identical today but will diverge tomorrow.

**The Debate: The Wrong Abstraction vs Duplication** — Metz's 2016 argument that premature abstraction is costlier than repetition directly tensions the DRY reflex, and the asymmetry of fix-costs is the heart of it. Understanding the case in full is what converts "wait before extracting" from a slogan into a rule you can defend under pressure to consolidate.

**YAGNI vs Speculative Generality** — Building for imagined future needs is one of the most common ways to add accidental complexity, but YAGNI taken literally ignores cheap, obvious provisions that cost nothing to include. The skill is calibration — distinguishing speculative flexibility from basic foresight — and that distinction is worth a post on its own.

**The Rule of Three** — Waiting until you've seen a pattern three times before abstracting it is the canon's practical answer to "when is duplication actually a problem." It deserves its own treatment because the heuristic looks arbitrary until you understand what the third occurrence actually gives you that the first two don't: evidence about what varies.

**AHA: Avoiding Hasty Abstractions** — The modern synthesis prefers a little duplication now over the wrong abstraction forever, and it reframes the whole DRY-vs-WET argument around the asymmetry of fix-costs. Drilling here gives you the reasoned default that resolves the debate in practice and tells you what to do at the moment of decision.

---