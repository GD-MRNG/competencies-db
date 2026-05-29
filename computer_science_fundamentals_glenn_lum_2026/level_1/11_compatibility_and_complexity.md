## Metadata
- **Date:** 23-05-2026
- **Source:** 11_computability_and_complexity.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Computability and Complexity

Most of the time, when something is hard in software, it is hard because you have not yet found the right approach. You have not picked the right data structure, you have not seen the right paper, you have not had the right idea. The implicit assumption underneath this — the assumption almost every working programmer carries — is that for any well-posed problem there exists, somewhere, an efficient algorithm waiting to be discovered. Computability and complexity is the branch of computer science that tells you this assumption is wrong. Some problems have no algorithm at all. Others have one, but no efficient one, and probably never will. Knowing how to recognise these cases is what separates a practitioner who keeps trying from one who knows when to stop.

The field splits cleanly along two axes. Computability asks what is solvable in principle, given infinite time and memory. Complexity asks what is solvable in practice, given the resources we actually have. Computability is the older question — Turing settled its outer boundaries in 1936 — and its central result is that the boundary exists at all. There are well-defined problems, statable in a few sentences, for which no algorithm can ever exist. The halting problem is the canonical one: no program can correctly determine, for every possible input program, whether that program eventually finishes or runs forever. This is not a statement about current technology or human cleverness. It is a mathematical impossibility, proved by contradiction, as solid as the irrationality of the square root of two.

Once you accept that there are problems no algorithm can solve, the next question naturally follows. Of the problems that *can* be solved, which can be solved quickly? This is where complexity theory takes over, and where the working practitioner spends most of their useful time. The headline categories are P and NP. P is the class of problems solvable in polynomial time — the time required grows as some power of the input size. These are the problems we consider tractable. NP is the class of problems whose solutions can be *verified* in polynomial time, even if finding them might take much longer. Sudoku is the intuition pump here: checking that a completed grid is correct is fast, but finding the completion from a sparse starting position can be brutally slow.

The question of whether P equals NP — whether every problem we can verify quickly we can also solve quickly — is the largest open problem in theoretical computer science, and most researchers believe the answer is no. What makes this practically relevant is the existence of NP-complete problems: a class of problems that are, in a precise mathematical sense, the hardest problems in NP. They are all equivalent in difficulty. A polynomial-time algorithm for any one of them would yield polynomial-time algorithms for all of them, and would prove P equals NP. None has been found in over fifty years of trying. This is not for lack of effort or talent.

The practical consequence is what matters. Many problems you encounter in real work — scheduling, routing, packing, constraint satisfaction, certain graph problems — are NP-complete or NP-hard. When you recognise one in the wild, you know something important: you should stop trying to find a perfect efficient algorithm. There almost certainly isn't one. The right move is to accept the constraint and pivot. You can solve smaller instances exactly. You can use approximation algorithms that give provably-close-to-optimal answers. You can use heuristics that work well in practice without guarantees. You can restrict the problem to a special case that *is* tractable. What you should not do is keep believing the next clever idea will crack it open.

The technique that makes all of this rigorous is reduction. To prove a new problem is at least as hard as a known hard one, you show that any instance of the known problem can be transformed into an instance of the new one. If you could solve the new problem efficiently, you could solve the old one efficiently — so the new one must be at least as hard. Reductions are how the entire complexity hierarchy is built. They are also a deeply useful intellectual habit even outside formal proofs: the question "is this problem really new, or is it a familiar problem in disguise?" is one of the most productive questions you can ask when you are stuck.

The skill this topic builds is not the ability to do complexity proofs. It is the ability to look at a problem and ask three questions that most practitioners never ask. Is this problem solvable at all? Is it solvable efficiently? And if not, what is the shape of the compromise I should be making? These are the questions that turn algorithm design from a search for cleverness into a search for the right kind of acceptance. The deepest payoff of complexity theory is the permission it grants you to stop looking — and the framework it gives you for what to do instead.

## Level 2 candidates

**Decidability and the halting problem** — Covers the mathematical proof that some problems admit no algorithm at any cost, with the halting problem as the load-bearing example. Worth deeper treatment because the proof technique (diagonalisation) is itself a powerful tool, and because decidability boundaries show up in surprisingly practical places — type checking, program analysis, formal verification.

**Complexity classes (P, NP, and beyond)** — The formal definitions of P and NP, what polynomial-time actually means, and the broader hierarchy (PSPACE, EXPTIME, co-NP). Worth depth because the precise definitions matter — the difference between "hard in theory" and "hard in practice" lives in the details, and the hierarchy beyond P and NP is where many real systems problems actually sit.

**NP-completeness in practice** — How to recognise NP-complete problems in real engineering work, the catalogue of canonical ones (SAT, TSP, knapsack, graph colouring), and the standard responses (approximation, heuristics, restriction, exact solvers). Worth depth because this is the most directly applicable part of complexity theory for working practitioners.

**Reductions as a proof technique** — The mechanics of polynomial-time reductions, Karp vs Cook reductions, and how Cook-Levin established SAT as the first NP-complete problem. Worth depth because reductions are both the foundational proof tool of complexity theory and a transferable analytical habit for recognising disguised problems in everyday work.

---