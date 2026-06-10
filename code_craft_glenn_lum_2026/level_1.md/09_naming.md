## Metadata
- **Date:** 11-06-2026
- **Source:** 09_naming.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-09 · Naming

The single highest-frequency design decision you make in a codebase is what to call things. Every identifier you choose will be read hundreds or thousands of times by people — including you, six months from now — who do not have your context, did not sit through your meeting, and cannot ask you what you meant. The cost of a bad name is not paid once when you type it; it is paid every time someone parses it, doubts it, or has to read the implementation to find out what it actually does. This is why the field's running joke — that the only hard problems are cache invalidation and naming things — is told by people who are not actually joking.

The mental model worth holding is that a name is compression. The thing being named has a purpose, a shape, a set of constraints, and a role in the design; the name is the smallest possible artifact that carries enough of that to let a reader skip reading the implementation. When the compression works, the name does the explaining and the code can get on with doing. When it fails, the reader has to decompress by hand — open the function, trace the variable, search for callers — and the name has shifted its work onto every future reader instead of bearing it itself. A good name is information transfer; a bad name is information theft, taken from everyone who will ever read past it.

This reframes naming as a test of your own understanding. If you cannot name a function cleanly, the usual reason is not that you lack vocabulary; it is that the thing you are trying to name is not actually one thing, or its responsibility is muddled, or it is doing work that belongs somewhere else. The struggle to name is diagnostic — it is the design pushing back on you and telling you that the concept beneath the name has not yet been clarified. Practitioners who treat naming as a final cosmetic pass miss this signal entirely; the people who treat it as a design activity find their structural problems early, while they are still cheap to fix. You don't write a clean name on a confused thing. You discover, by trying, that the thing is confused.

The canon is in unusually broad agreement here. Ousterhout, Martin, and the wider tradition disagree loudly about function size and about comments, but on naming they converge: precise, consistent names are foundational, not decorative, and the discipline of choosing them well is what keeps a codebase legible at scale. The agreement makes sense once you see naming through the complexity lens — obscurity is one of the two root causes of complexity, and a vague name is obscurity in its purest form, a small fog deposited at the exact point a reader is trying to see. You cannot reduce coupling by renaming, but you can dissolve a striking amount of cognitive load, because much of what felt like complexity was actually just identifiers refusing to tell you what they were.

The components of a good name are worth naming themselves. Precision is the first: a name should describe what the thing is for, not merely the category it belongs to — `expiry` beats `date`, `pendingInvoices` beats `items`, and a name that could plausibly describe three different variables in the same scope is failing its job. Consistency is the second, and it compounds harder than it looks: when the same concept wears the same name everywhere, readers stop verifying and start predicting, and the codebase becomes navigable by pattern instead of by inspection. Synonyms are the silent enemy here — `user`, `account`, `customer` scattered across a system for what is actually one concept will tax every reader who has to confirm, each time, that these three things really are the same. The third component is calibrating length to scope: a loop counter living for three lines does not need to be `currentIterationIndex`, but a function parameter used across forty lines of logic absolutely earns its descriptive name. Distance from definition is what determines how much context a name has to carry on its own.

The smallest, cheapest naming win is also the most overlooked: turning literals into named constants. A bare `86400` in a calculation is a concept the author understood and the reader has to reverse-engineer; `secondsPerDay` is the same value with the decision attached. The same logic applies to magic strings, status codes, and threshold values — every unnamed literal is a piece of design intent that exists in the author's head and nowhere in the code. Naming it is not adding a constant; it is recording a decision that was previously invisible.

What this unlocks, when you take it seriously, is disproportionate. Renaming is among the safest changes you can make, and it routinely clarifies confusing code more than restructuring does, because so much of what reads as complexity is just obscurity wearing a costume. A confused module with good names becomes a module whose problems you can see; a clear module with bad names looks like a confused one. Treat naming as a first-class design activity — not the polish you do at the end, but the pressure you apply early to find out whether you actually understand what you are building. The codebases that stay legible for years are not the ones with the cleverest abstractions. They are the ones where almost every name means exactly what it says.

## Level 2 candidates

**A Name as Compressed Intent** — Covers the mechanism by which a precise name transmits design intent without the reader decoding the implementation, and why a vague name is a tax paid on every read. Worth depth because it reframes naming from cosmetic concern to information-theoretic one and makes the cost of bad names quantifiable.

**Naming as a Test of Understanding** — Covers the diagnostic use of naming difficulty: when you cannot name something cleanly, the concept itself is usually muddled. Worth depth because it converts naming from a writing task into a design technique, with implications for when to stop and rethink rather than push through.

**Consistency in Naming** — Covers the compounding payoff of using one name per concept across a codebase, and the specific damage done by synonyms for the same idea. Worth depth because the discipline is unglamorous but produces outsized legibility gains and connects directly to the broader principle of consistency in Tier 3.

**Length, Scope, and Precision** — Covers the rule that descriptiveness should scale with distance from definition, resolving the perennial "short vs descriptive names" argument by context. Worth depth because the rule dissolves a debate that otherwise gets re-litigated by taste.

**The Magic Number Problem** — Covers why hardcoded literals are unnamed concepts, and how naming them records design decisions that previously lived only in the author's head. Worth depth because it is the cheapest readability intervention in the canon and a clean illustration of naming-as-decision-recording.

---