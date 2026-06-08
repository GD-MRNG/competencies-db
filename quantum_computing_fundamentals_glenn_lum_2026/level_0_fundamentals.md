# Quantum Computing — Level 0: Course Map

> **Intent:** Build enough understanding of quantum mechanics, quantum circuits, and quantum algorithm structure to write, run, and reason about real quantum programs in Qiskit — and to know *why* the code does what it does, not just how to copy it.
>
> **Your angle:** You have a CS degree. You know what a computation model is, what complexity classes mean, and how classical gates compose into algorithms. You do not need quantum mechanics explained from scratch — you need it explained in terms of what it changes about computation. The math will stretch you, but nothing here requires more than linear algebra you already know in principle. The goal is fluency, not mastery.

---

## How to use this map

Each **Level 1 topic** is one concept node: what it is, why it matters, and where it sits relative to what comes before and after. Each **Level 2 candidate** is a target for a depth post — the mechanics, the tradeoffs, the point where things get interesting or break.

This map is ordered by dependency, not difficulty. Work through Group 1 before touching Qiskit. Group 2 gives you the physical intuition that makes circuits readable rather than magic. Group 3 is where you write code. Group 4 is what you need to understand why your circuits behave strangely on real hardware.

The map does not include open research frontiers. Those are for a different reader. This map ends where practical fluency begins.

---

## Topic Inventory

---

### Group 1 — Reframing What You Know

*These topics do not introduce new material from scratch — they show you where your existing CS knowledge stops applying and what replaces it. Work through all of these before Group 2.*

---

#### L1-01 · The Computational Model Shift

**What it is and why it matters:** Your CS education begins with the Turing machine — a model of computation that abstracts away the physical substrate entirely. Quantum computing breaks that abstraction. The physics is not implementation detail; it is the mechanism. A qubit is not a fast bit. A quantum circuit is not a faster boolean circuit. Understanding this distinction early prevents the most persistent beginner misconception: that quantum computers are generically faster, when in fact they are faster at a specific structural class of problems for specific physical reasons. This is the conceptual hinge everything else turns on.

**Level 2 candidates:**

- **Classical vs quantum bits** — Where a classical bit is a committed value, a qubit holds a superposition of both until measured; internalising this distinction is what separates understanding quantum code from merely writing it.
- **The quantum circuit model** — The quantum analogue of boolean circuits, where operations are reversible unitary transformations rather than irreversible logic gates; reversibility is not a design choice but a physical constraint, and it changes how you think about computation structurally.
- **Why reversibility matters** — Classical computation destroys information (Landauer's principle, 1961); quantum gates must be reversible, which shapes circuit structure in ways that have no classical parallel and explain why classical algorithms cannot be directly ported.
- **Measurement and collapse** — Reading a quantum state destroys the superposition; understanding when and how to measure is where quantum algorithm design — and quantum program design — differs most sharply from classical programming.
- **The extended Church-Turing thesis** — The original thesis claims all physical computation is classically simulable; quantum computing challenges this, and the challenge is the principled answer to "why does any of this matter?"

---

#### L1-02 · The Mathematics You Actually Need

**What it is and why it matters:** Quantum mechanics runs on linear algebra — but a specific flavour of it: complex vector spaces, unitary matrices, and tensor products. If your linear algebra is rusty or real-valued only, this is the place to close the gap before touching anything else. The good news: you do not need to be fluent before starting. You need enough to read a quantum circuit description without losing the thread. The notation (Dirac's bra-ket, 1939) looks unfamiliar but is a thin layer over matrix-vector arithmetic you already know.

**Level 2 candidates:**

- **Complex amplitudes vs real probabilities** — Quantum states use complex numbers as amplitudes, not probabilities; complex amplitudes can cancel (negative interference), which is the mechanism that makes quantum algorithms work, and it has no classical analogue.
- **Dirac (bra-ket) notation** — The `|ψ⟩` notation is not arbitrary; it cleanly separates a state vector from its dual, making quantum operations easier to express than matrix notation; fluency with it is the entry fee for reading any Qiskit documentation or algorithm reference.
- **Unitary matrices and why gates must be unitary** — Unitarity preserves the constraint that all outcome probabilities sum to 1; understanding this explains why quantum gate sets look the way they do and why not every matrix is a valid quantum operation.
- **Tensor products and multi-qubit state spaces** — When you combine two qubits, the state space grows exponentially; the tensor product is the mathematical operation that explains both quantum parallelism and why simulating quantum systems classically gets hard fast.
- **The Bloch sphere** — A geometric representation of a single qubit's state as a point on a unit sphere; it makes quantum gate operations (rotations) visually intuitive and is the standard mental model used in Qiskit visualisations and documentation.

---

### Group 2 — Core Quantum Mechanics for Computation

*The physical principles that create computational power. Not physics for its own sake — each topic here is included because it directly determines how quantum circuits are structured and why they behave as they do.*

---

#### L1-03 · Superposition and Interference

**What it is and why it matters:** Superposition is the most cited quantum property and the most frequently misunderstood. It does not mean a quantum computer "tries all paths simultaneously" in any operationally useful sense — measuring a superposed qubit gives one outcome. What matters computationally is interference: the ability to make probability amplitudes reinforce for correct answers and cancel for wrong ones. Every quantum algorithm is, at its core, a carefully engineered interference pattern. Grover's algorithm, the Deutsch-Jozsa algorithm, and the QFT are all interference patterns. Understanding superposition without interference is understanding the setup without the mechanism.

**Level 2 candidates:**

- **Probability amplitudes and cancellation** — Amplitudes can be negative or complex and can cancel; this cancellation is why quantum algorithms can suppress wrong answers, and it is the physical phenomenon classical probability cannot replicate.
- **Interference as an algorithm design tool** — The Deutsch-Jozsa and Grover algorithms both work by constructing interference that amplifies the correct output; seeing this pattern concretely shifts quantum programming from circuit-copying to intentional design.
- **The Hadamard gate as an interference engine** — The Hadamard gate creates uniform superposition and, when applied twice, cancels back to the original state; its action is the simplest concrete demonstration of constructive and destructive interference in a circuit.
- **The double-slit analogy and its limits** — The standard introduction to quantum interference, but its limits as an analogy for quantum computation matter as much as its usefulness; knowing where it breaks prevents persistent misconceptions about what superposition means in a circuit.

---

#### L1-04 · Entanglement

**What it is and why it matters:** Entanglement is the property that makes multi-qubit states inseparable — the state of a two-qubit system cannot always be written as a product of two individual qubit states. Bell's 1964 theorem proved this is a genuine physical phenomenon, not a classical correlation by another name. In Qiskit, you create entanglement the moment you apply a CNOT gate to qubits in superposition. Understanding what entanglement is — and what it is not — determines whether you can reason about multi-qubit circuits or just write them.

**Level 2 candidates:**

- **Bell states** — The four maximally entangled two-qubit states; they are produced by a Hadamard followed by a CNOT, appear constantly in quantum protocols, and are the first entangled states you will create in Qiskit.
- **Entanglement vs classical correlation** — Entangled qubits are correlated in ways that classical shared randomness cannot reproduce; Bell's inequality is the test, and its violation is why entanglement is a genuine quantum resource rather than a classical effect with a new name.
- **Quantum teleportation** — Not science-fiction teleportation but the exact transfer of a quantum state using entanglement and classical communication; implementing it in Qiskit is a standard early exercise and concretely demonstrates what entanglement enables.
- **Entanglement as a computational resource** — Entanglement is consumed in quantum protocols the way classical resources (memory, bandwidth) are consumed; thinking of it as a resource with a cost rather than a property reframes how you read multi-qubit circuit design.
- **Entanglement entropy** — A measure of how entangled a state is; high entanglement entropy is what makes quantum systems hard to simulate classically, which is both why quantum computers are powerful and why running large circuits on your laptop gets intractable fast.

---

#### L1-05 · Quantum Gates and Circuit Design

**What it is and why it matters:** Quantum gates are the vocabulary of quantum circuits — the quantum analogue of logic gates, but reversible and acting on complex amplitudes. The standard gate set (Hadamard, CNOT, T gate, phase gates) was not chosen arbitrarily: these specific gates are universal, meaning any quantum computation can be expressed in terms of them. In Qiskit, every circuit you write is a sequence of these gates. Understanding the gate set is the direct prerequisite for reading, writing, and debugging quantum programs.

**Level 2 candidates:**

- **Pauli gates (X, Y, Z)** — The quantum analogues of classical bit-flip and phase operations; X is the quantum NOT gate, and the commutation relations between Paulis underlie both circuit simplification and error correction theory.
- **The Hadamard gate** — Creates superposition from a basis state and is the most-used gate in quantum algorithm design; its matrix form connects the linear algebra directly to the physical operation and it appears in virtually every non-trivial Qiskit circuit.
- **The CNOT gate and two-qubit entanglement** — The controlled-NOT gate creates entanglement from separable states when the control qubit is in superposition; along with single-qubit gates it forms a universal gate set — the quantum equivalent of NAND universality.
- **Phase gates (S, T, Rz)** — Phase gates rotate the qubit around the Z-axis of the Bloch sphere; the T gate in particular is essential for universal fault-tolerant computation and is the gate that makes Qiskit circuits expensive to run error-corrected.
- **Circuit depth and gate count** — Quantum computation resources are measured in gate count and circuit depth, not clock cycles; understanding these metrics is prerequisite for comparing algorithm efficiency and for knowing whether a circuit is runnable on today's hardware.
- **Universality and gate sets** — Just as NAND alone suffices for all classical computation, a specific minimal set of quantum gates suffices for all quantum computation; understanding which sets are universal and why explains how Qiskit compiles circuits to device-native gates.

---

### Group 3 — Quantum Algorithms

*The reason the field exists. Each algorithm here represents a proven quantum advantage with a specific structural reason for it. Working through these gives you both the circuit patterns you will reuse in Qiskit and the conceptual vocabulary for reading anything written about quantum computing.*

---

#### L1-06 · The First Proofs of Quantum Advantage

**What it is and why it matters:** The first quantum algorithms — Deutsch (1985), Deutsch-Jozsa (1992), Bernstein-Vazirani (1993) — solved toy problems but proved something precise: a quantum computer can answer certain questions about a function in fewer queries than any classical computer, regardless of classical cleverness. They are short enough to fit on a single page of circuit diagrams, implementable in Qiskit in under 20 lines, and the interference mechanism they use is the same one underlying Grover's and Shor's. These are the best entry point for understanding what a quantum speedup actually means and for writing your first non-trivial quantum circuits.

**Level 2 candidates:**

- **The oracle model** — These algorithms access their input through a black-box function (oracle); the oracle model isolates the quantum advantage to query complexity alone, which is why these proofs are precise rather than benchmark-dependent.
- **Deutsch's algorithm** — The simplest quantum algorithm to demonstrate speedup (1985): one query where classical algorithms need two; short enough to trace by hand and the interference mechanism is visible at the circuit level.
- **Deutsch-Jozsa** — Generalises Deutsch's algorithm to n-bit inputs; solves in one query what classical algorithms need 2^(n-1)+1 queries to guarantee; the circuit structure directly previews the Hadamard sandwich pattern used in Grover's.
- **Bernstein-Vazirani** — Recovers a hidden n-bit string in one query where classical algorithms need n; the circuit is almost identical to Deutsch-Jozsa and is the clearest demonstration that the Hadamard-oracle-Hadamard structure is a reusable pattern, not a one-off trick.
- **Simon's algorithm** — Provides the first exponential quantum speedup and directly inspired Shor's; it is the conceptual bridge from these toy algorithms to the number-theoretic results, and understanding it makes Shor's structure legible.

---

#### L1-07 · Grover's Search Algorithm

**What it is and why it matters:** Grover's algorithm (1996) searches an unsorted list of N items in O(√N) operations where classical search requires O(N). The quadratic speedup applies to any problem reducible to search — which is a large class — and the technique underlying it (amplitude amplification) recurs as a subroutine in more advanced algorithms. Grover's is the standard second algorithm to implement in Qiskit after the oracle-based algorithms: it is complex enough to be instructive, short enough to trace completely, and the amplitude amplification pattern it introduces is one of the two foundational algorithmic techniques in the field.

**Level 2 candidates:**

- **Amplitude amplification** — The general mechanism behind Grover's: iteratively rotating the quantum state toward the target; visualising this as a 2D rotation in the Bloch sphere makes the O(√N) iteration count intuitive rather than magical.
- **The oracle and phase kickback** — Grover's oracle marks the target state by flipping its phase; phase kickback is the technique that makes this work, and understanding it is the key to implementing custom Grover oracles in Qiskit.
- **The diffusion operator** — The inversion-about-the-mean step that amplifies the target's probability; it is a specific interference operation and understanding its structure reveals why running Grover's for too many iterations degrades rather than improves results.
- **Optimality of Grover's** — No quantum algorithm can search faster than O(√N); this bound explains why quantum computers do not break symmetric encryption (AES) — they halve the effective key strength but do not eliminate it.
- **Amplitude amplification as a subroutine** — Grover's pattern appears inside quantum minimum-finding, collision detection, and satisfiability algorithms; recognising it in other circuits is the key transferable skill from this topic.

---

#### L1-08 · The Quantum Fourier Transform and Phase Estimation

**What it is and why it matters:** The Quantum Fourier Transform (QFT) is the quantum analogue of the discrete Fourier transform, computed exponentially faster in gate count. It is the engine of Shor's algorithm and appears as a subroutine in quantum phase estimation, quantum chemistry simulations, and a range of other algorithms. Quantum Phase Estimation (QPE) uses the QFT to extract eigenvalues of unitary operators and is the foundation of the most practically important near-term quantum algorithms. Learning to implement the QFT and QPE in Qiskit is the technical inflection point where circuits become algorithms.

**Level 2 candidates:**

- **The QFT circuit structure** — The QFT decomposes into Hadamard gates and controlled phase rotations in a regular pattern; the circuit is one of the most elegant in quantum computing and understanding its structure makes it implementable rather than just copyable.
- **Quantum Phase Estimation (QPE)** — Uses the QFT to determine the phase (eigenvalue) of a unitary operator applied to an eigenvector; QPE is the core subroutine of Shor's period-finding step and of quantum chemistry energy estimation.
- **The relationship between QFT and classical FFT** — The QFT achieves O(n²) gate complexity vs O(n·2^n) for the classical FFT on the same input size; understanding the comparison is important for correctly interpreting the speedup claim.
- **Controlled-unitary operations** — QPE requires applying a unitary U raised to increasing powers (U, U², U⁴...); implementing this efficiently in Qiskit is one of the main practical challenges in QPE circuits and determines whether the algorithm is runnable on real hardware.

---

#### L1-09 · Shor's Factoring Algorithm

**What it is and why it matters:** Shor's algorithm (1994) factors large integers in polynomial time where the best classical algorithm requires sub-exponential time. RSA encryption — which secures most internet traffic — depends on factoring being classically hard. Shor's algorithm is the reason post-quantum cryptography exists and the reason governments and enterprises are investing in quantum hardware. The algorithm is instructive beyond its application: it reduces factoring to period-finding, then solves period-finding with the QFT, and each step is a clean lesson in quantum algorithm design. You will not run Shor's on real hardware at meaningful scale for years — but implementing it in Qiskit on small inputs is achievable and revealing.

**Level 2 candidates:**

- **Reduction of factoring to period-finding** — The classical insight that factoring N reduces to finding the period of f(x) = aˣ mod N; this reduction is number theory, not quantum mechanics, and separating it from the quantum core clarifies what Shor's actually contributes.
- **The QFT as the period-finding engine** — The quantum core of Shor's is using QPE to find the period of the modular exponentiation function; seeing how QFT extracts periodicity makes the speedup structural rather than mysterious.
- **Modular exponentiation circuits** — The classical subroutine that computes aˣ mod N must be implemented as a quantum circuit; it is the most gate-intensive part of Shor's and the main reason the algorithm requires error correction at scale to be useful.
- **Post-quantum cryptography** — Shor's breaks RSA and elliptic curve cryptography; NIST's 2024 post-quantum standards (CRYSTALS-Kyber, CRYSTALS-Dilithium) are the cryptographic response; understanding Shor's explains what "quantum-resistant" means and why the migration is urgent regardless of hardware timelines.
- **Current hardware gap** — Breaking RSA-2048 with Shor's requires millions of error-corrected physical qubits; today's devices have hundreds to thousands of noisy qubits; implementing Shor's in Qiskit on 3–4 bit numbers is the pedagogically useful version.

---

#### L1-10 · Variational Quantum Algorithms (VQAs)

**What it is and why it matters:** Variational algorithms — VQE (Variational Quantum Eigensolver) and QAOA (Quantum Approximate Optimisation Algorithm) — are the class of quantum algorithms designed for today's noisy, error-uncorrected hardware. They use a classical optimiser in a feedback loop with a parameterised quantum circuit, adjusting gate angles iteratively to minimise a cost function. VQAs are what most near-term Qiskit work actually looks like: they are the main candidates for practical quantum utility before fault-tolerant hardware arrives. Understanding their structure also means understanding their limitations — they are heuristic, not guaranteed to outperform classical optimisers.

**Level 2 candidates:**

- **Parameterised quantum circuits (PQCs)** — Circuits with tunable rotation angles; the parameters are optimised classically, making VQAs a hybrid quantum-classical architecture; understanding PQC structure is the prerequisite for writing any VQA in Qiskit.
- **VQE and quantum chemistry** — VQE estimates the ground state energy of a molecule by minimising the expectation value of its Hamiltonian; it is the most credible near-term application for quantum advantage and the standard example in Qiskit's chemistry tutorials.
- **QAOA and combinatorial optimisation** — QAOA applies to problems like Max-Cut and TSP variants; its circuit structure alternates between a problem Hamiltonian and a mixing Hamiltonian, and understanding this structure is the entry point for applying it to real optimisation problems.
- **The barren plateau problem** — As PQC depth and width increase, gradients become exponentially small and classical optimisers fail to improve the circuit; this is the central practical obstacle for scaling VQAs and explains why deeper is not always better.
- **NISQ utility: honest assessment** — Whether VQAs will outperform the best classical optimisation methods on practically relevant problem sizes is an open empirical question; several recent results suggest classical tensor network methods match them at current circuit depths; knowing this prevents misplaced expectations.

---

### Group 4 — Hardware Reality and Qiskit on Real Devices

*The physical constraints that explain why circuits that work in simulation misbehave on real hardware. This group reframes everything in Groups 1–3 in terms of what is actually executable today.*

---

#### L1-11 · Qubits: Physical Implementations

**What it is and why it matters:** The qubit is an abstraction — the physical systems used to implement it vary enormously and have different properties. Superconducting qubits (IBM, Google), trapped ions (IonQ, Quantinuum), photonic qubits, and neutral atoms are not equivalent hardware platforms: they differ in coherence time, gate fidelity, connectivity, and scalability in ways that directly affect which circuits you can run and how you need to compile them. IBM's hardware — the platform behind Qiskit — uses superconducting qubits, and understanding their specific constraints makes Qiskit's transpiler choices legible.

**Level 2 candidates:**

- **Superconducting qubits** — IBM and Google's platform; fast gates but short coherence times (~100 microseconds); operate at millikelvin temperatures; limited qubit-to-qubit connectivity means CNOT gates between non-adjacent qubits require SWAP insertion.
- **Trapped ion qubits** — Individual atoms used as qubits; slower gates but longer coherence times and all-to-all connectivity; the comparison with superconducting qubits illustrates the coherence-speed tradeoff that shapes every hardware choice.
- **Gate fidelity and error rates** — Every gate on real hardware introduces error; fidelity (the probability a gate performs correctly) is the central metric determining which circuits are runnable today and which are not.
- **Connectivity graphs and SWAP overhead** — Real devices have a fixed qubit topology; circuits written for all-to-all connectivity must be compiled to the device graph using SWAP gates, each of which adds error; Qiskit's transpiler handles this, but understanding it explains why transpiled circuits look different from what you wrote.
- **IBM Quantum hardware backends** — Qiskit connects to IBM's fleet of real quantum devices with different qubit counts, topologies, and calibration states; knowing how to choose a backend, read its properties, and interpret noise data is essential for running real jobs.

---

#### L1-12 · Decoherence and Noise

**What it is and why it matters:** Quantum states are fragile. Any interaction with the environment collapses the superposition — this is decoherence, and the coherence time of a qubit is the clock your entire computation must finish within. On IBM hardware, coherence times are measured in microseconds. A deep circuit that takes too long simply decoheres before it finishes. Understanding decoherence separates an honest reading of hardware specs from marketing claims — and it explains why circuit depth, not just gate count, is a hard constraint on what is runnable today.

**Level 2 candidates:**

- **T1 and T2 times** — T1 (relaxation time) and T2 (dephasing time) are the two hardware parameters that define how long a qubit holds its state; reading these from IBM's backend properties and calculating whether your circuit fits within them is a practical skill for every real job.
- **Bit flip and phase flip errors** — Quantum errors come in two orthogonal types; phase flip errors have no classical analogue, and understanding both is necessary for reading noise model documentation and for interpreting unexpected measurement results.
- **Noise models in Qiskit Aer** — Qiskit's simulator allows realistic noise models derived from actual hardware; using noise-model simulation before running on real hardware is standard practice and the main tool for debugging circuits before committing to queue time.
- **NISQ (Noisy Intermediate-Scale Quantum)** — Preskill's 2018 framing of where quantum hardware currently sits: 50–1000 qubits, no error correction, useful for research but inherently noisy; understanding NISQ defines the practical ceiling on what circuits are currently meaningful to run.

---

#### L1-13 · Quantum Error Correction: What It Is and Why It Is Not Yet Practical

**What it is and why it matters:** Classical error correction cannot be applied directly to quantum states — you cannot copy a qubit (no-cloning theorem) and measuring it to check for errors destroys the state. Quantum error correction (Shor's code, 1995; the surface code) encodes one logical qubit across many physical qubits in a way that allows errors to be detected without measuring the logical state. This is not yet practical at scale — it requires physical qubit counts and error rates not yet achieved — but understanding the principle explains why the gap between "Shor's algorithm exists" and "RSA is broken" is so large, and why fault-tolerant quantum computing is a decade-scale engineering programme.

**Level 2 candidates:**

- **The no-cloning theorem** — A quantum state cannot be copied exactly; the proof is a two-line linear algebra result, and the consequence for error correction and cryptography is profound and practical.
- **Logical vs physical qubits** — A single logical (error-corrected) qubit requires hundreds to thousands of physical qubits at current error rates; this overhead is the direct explanation for why breaking RSA requires millions of physical qubits despite Shor's needing only ~4000 logical qubits.
- **The surface code** — The leading practical error correcting code for superconducting hardware; its 2D grid structure maps naturally to IBM and Google's qubit topologies, and understanding it at a conceptual level is sufficient for interpreting hardware roadmap discussions.
- **The threshold theorem** — If physical gate error rates fall below ~1%, quantum error correction can in principle make computation arbitrarily reliable; the threshold theorem is the theoretical guarantee that fault-tolerant quantum computing is achievable, not just hoped for.
- **Clifford + T and fault-tolerant gate sets** — Not all quantum gates are compatible with error correction; the Clifford + T gate set is the standard fault-tolerant basis, and the T gate is the expensive one; this reshapes how fault-tolerant circuits are designed and explains why T gate count is a key algorithmic cost metric.

---

#### L1-14 · Quantum Complexity and Reading Speedup Claims

**What it is and why it matters:** Every claim that a quantum algorithm is faster than a classical one rests on a complexity argument. Understanding the basics — BQP (the problems quantum computers can solve efficiently), its relationship to P and NP, and the oracle model used to prove most speedup results — gives you the vocabulary to evaluate quantum hype rather than absorb it. This is not an abstract theory topic: it is the framework for reading papers, press releases, and algorithm descriptions with appropriate skepticism and appropriate excitement.

**Level 2 candidates:**

- **BQP (bounded-error quantum polynomial time)** — The quantum analogue of P; the class of problems solvable efficiently by a quantum computer; knowing where Grover's and Shor's sit in BQP, and where BQP sits relative to P and NP, is the baseline for evaluating any quantum speedup claim.
- **Quantum supremacy vs quantum advantage** — The 2019 Google experiment demonstrated a quantum device doing something classically hard (supremacy); quantum advantage means doing something practically useful faster (still largely unproven for applications); the confusion between these two drives most quantum hype.
- **Oracle speedups and their limits** — Most proven quantum speedups are in the oracle model; oracle separations do not always translate to real-world advantages; this is why "quantum beats classical on this benchmark" does not automatically mean "quantum is better in practice."
- **Dequantisation** — Tang's 2018 result showed a famous quantum ML algorithm could be matched by a classical randomised algorithm; "dequantisation" is now an active area and a useful reminder that claimed quantum advantages are not always stable.

---

## Sequencing note

Work through the groups in order. Group 1 is mandatory first — not because it is the hardest material but because it reframes assumptions you will otherwise carry in from classical programming, and those assumptions will mislead you constantly if they are not corrected early. The mathematics in L1-02 does not need to be mastered before proceeding — work through it in parallel with Group 2, returning to each concept as it appears in context.

Within Group 2, L1-03 (superposition and interference) and L1-04 (entanglement) are genuinely parallel and can be read in either order. Both are prerequisites for L1-05 (gates), which is the direct prerequisite for writing any real Qiskit circuit.

In Group 3, the intended path is L1-06 → L1-07 → L1-08 → L1-09, in that order. Shor's algorithm has the highest mathematical demand of any topic here; working through Grover's first and the QFT topic second makes Shor's structure legible rather than opaque. VQAs (L1-10) can be read after L1-07 independently of Shor's — they draw on parameterised circuits, not QFT, and are likely the first algorithms you will actually run on real hardware.

Group 4 can begin in parallel with Group 3 once you have written your first real Qiskit circuits. L1-11 (hardware implementations) and L1-12 (decoherence) are the most immediately practical and should be read before running any real device jobs. L1-13 (error correction) is conceptual background for Group 3 rather than a programming prerequisite — understand it enough to know why logical qubit counts matter; you will not implement error correction in Qiskit at this stage. L1-14 (complexity and speedup claims) is best read last, after Group 3 has given you concrete algorithms to attach the abstractions to.