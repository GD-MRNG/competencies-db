## Metadata
- **Date:** 11-06-2026
- **Source:** 06_information_hiding_and_deep_modules.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-06 · Information Hiding and Deep Modules

The instinct most developers have when decomposing a system is to break it into the steps it performs: parse, validate, transform, persist, render. This feels natural — it mirrors the order things happen — and it is almost always wrong. The single most important paper in the canon, Parnas's 1972 "On the Criteria To Be Used in Decomposing Systems Into Modules," argues that decomposing by processing sequence produces modules that all need to know each other's business, and that the right criterion is something else entirely: each module should hide a design decision from the rest of the system. The module's job is not to perform a step. Its job is to keep a secret.

That reframing is the whole game. If a module hides a decision — the on-disk format, the choice of data structure, the network protocol, the caching policy — then that decision can change without anyone outside the module noticing. That is what decoupling actually buys you, and it is the only thing it buys you. Modules that share knowledge of a decision are coupled to that decision whether or not they call each other directly; modules that each hide their own decisions can evolve independently because there is nothing outside them to break. Coupling is not really about who calls whom. It is about who has to know what.

Ousterhout's modern restatement of this idea is the deep module: a module whose interface is much simpler than its implementation. A deep module hides a lot behind a little. The Unix file system is the textbook case — open, read, write, close — four operations that conceal block allocation, directory structures, permissions, caching, journaling, and device drivers. The interface is small enough to memorise; the implementation is a career. That ratio between interface cost and implementation hidden is the metric you want, and it is the lens through which you can finally answer the otherwise-unanswerable question of whether a given class is pulling its weight.

The opposite — a shallow module — is the one whose interface is nearly as complex as its implementation. A class with fifteen public methods, each a thin wrapper over a single field access, is shallow; a function that exists only to forward its arguments to another function is shallow; a layer of "managers" and "helpers" that each expose most of what they wrap is shallow. Shallow modules are the costume in which over-decomposition arrives, and they are dangerous precisely because they look like good design — small classes, single responsibilities, lots of boundaries — while paying interface costs that nothing on the other side repays. Every public method is a promise to every caller. If the method hides nothing, the promise is pure overhead.

The failure mode that tells you a boundary is in the wrong place is information leakage: when a single design decision is reflected in two or more modules, so changing it forces you to change all of them in lockstep. The classic tell is opening one file to make a change and finding yourself opening three more to keep them consistent — the decision you thought lived in one place actually lives spread across a seam. Leakage is sneakier than coupling-by-call, because the leaking modules may never reference each other directly; they merely happen to encode the same assumption about the format, the order, the units, the protocol. When you see this, the answer is rarely to add another layer. It is to redraw the boundary so the leaking decision lives behind exactly one of them.

The practical consequence is a shift in how you decide where to cut. Decomposition by steps asks "what does this system do, in order?" and produces modules that are each a stage in a pipeline, all sharing the data shapes that flow between them. Decomposition by hidden decisions asks "what is likely to change, and which module should absorb that change so no one else feels it?" — and produces modules organised around volatility rather than sequence. The data format goes behind one module. The wire protocol goes behind another. The retry policy goes behind a third. The pipeline still exists, but it is now a thin coordinator over modules that each protect their own secret, and a change to any one secret is a change to one file.

This is the criterion for where to draw a line, and it is also the criterion for whether a line you've already drawn deserves to stay. A module that hides little is a module that taxes every caller for nothing, and the honest move is usually to inline it and redraw the boundary somewhere it can actually keep a secret. The skill this topic builds, more than any other in the structural tier, is the ability to look at a proposed boundary and ask the only question that matters: what does this hide, and is what it hides worth what its interface costs? Most of the design judgment in software collapses into that one trade.

## Level 2 candidates

**Parnas's Criterion: Hide the Decisions Likely to Change** — Drilling into the original 1972 argument and the worked example (the KWIC index) that makes it concrete, including how Parnas chose what counted as a "design decision likely to change." Worth depth because the paper's reasoning, read directly, reframes decomposition more thoroughly than any restatement of it.

**Deep vs Shallow Modules** — A deeper look at the interface-to-implementation ratio as a working metric, with concrete examples of deep modules (Unix files, garbage collectors) and shallow ones (anaemic getters/setters, manager classes). Worth its own post because applying the depth lens to real code is a learnable skill that requires practice on cases.

**Information Leakage** — How to spot leakage in code you didn't write: the multi-file change, the duplicated assumption, the parallel switch statement. Worth depth because leakage is the diagnostic that translates the abstract "wrong boundary" intuition into a specific, fixable observation.

**Interface vs Implementation Complexity** — The economic framing of a module — interface as cost paid by every caller, implementation as the complexity hidden in return — and how the ratio drives the "is this abstraction worth it?" decision. Worth depth because it gives you a defensible answer to a question most teams resolve by taste.

**Pass-Through Methods and Other Shallow Smells** — A catalogue of the specific patterns (pass-through methods, thin wrappers, parallel class hierarchies that mirror the thing they wrap) that signal decomposition adding interface without hiding anything. Worth depth because the smells are concrete enough to teach and the corrective moves are specific.

**Decomposing by Decisions vs Decomposing by Steps** — A direct comparison of the two decomposition strategies on the same problem, showing how the resulting module graphs differ and why one absorbs change better. Worth depth because seeing both applied to one example is the fastest way to internalise the difference Parnas was actually pointing at.

---