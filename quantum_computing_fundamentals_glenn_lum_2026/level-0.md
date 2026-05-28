# Quantum Computing Fundamentals — Level 0: Course Map

> **Intent:** Understand quantum computing as a principled extension of classical 
> computation — not as an exotic curiosity, but as a different computational 
> model with specific theoretical advantages, hard physical constraints, and 
> a maturing but incomplete engineering reality. The goal is to reason clearly 
> about what quantum computers can do, why, and what it costs.
>
> **Your angle:** You have the CS foundations map. That map ends at classical 
> computation. This map begins at the boundary — where classical assumptions 
> break down and quantum mechanics becomes the operating principle. You are not 
> learning physics from scratch; you are extending a computational model you 
> already understand deeply.

---

## How to use this map

Each **Level 1 topic** is one concept post: what it is, why it matters, where 
it sits in the larger picture. Each **Level 2 sub-concept** is a candidate for 
a depth post: mechanics, tradeoffs, where it breaks.

The bridge group below is the mandatory entry layer — it reframes concepts from 
your CS map in quantum terms. Do not skip it even if the labels look familiar. 
The meaning of "computation," "information," and "complexity" is genuinely 
different here.

---

## Topic Inventory

---

### Group 1 — The Bridge: Where Classical CS Meets Quantum

*These topics do not repeat your CS foundations — they reframe them. Each one 
takes a node from the existing map and shows what changes when the physical 
substrate is quantum mechanical.*

---

#### L1-01 · The Computational Model Shift

**What it is and why it matters:** Your CS map begins with Turing (L1-01) — a 
model of computation that abstracts away the physical substrate entirely. Quantum 
computing breaks that abstraction. The computational model is no longer substrate-
independent: the physics of quantum mechanics is not a detail but the mechanism. 
Understanding the quantum circuit model — the analogue of the Turing machine for 
quantum computation — requires first understanding why the classical model is 
insufficient and what specific physical properties enable something different. 
This is the conceptual hinge the entire domain turns on.

**Level 2 candidates:**

- **L2 · Classical vs quantum bits** — Where a classical bit is a committed value, 
  a qubit is a superposition of both until measured; understanding this distinction 
  clarifies why quantum computers are not simply faster classical ones.
- **L2 · The quantum circuit model** — The quantum analogue of boolean circuits 
  (your L1-06 logic gates), where operations are reversible unitary transformations 
  rather than irreversible logic gates; reversibility is not a design choice but a 
  physical necessity.
- **L2 · Why reversibility matters** — Classical computation destroys information 
  (Landauer's principle, 1961); quantum gates must be reversible, which constrains 
  circuit design in ways that have no classical parallel and explain why certain 
  classical algorithms cannot be directly ported.
- **L2 · Measurement and collapse** — The act of reading a quantum state destroys 
  the superposition; understanding when and how to measure is where quantum algorithm 
  design differs most sharply from classical programming.
- **L2 · The extended Church-Turing thesis** — The original thesis (your L1-01) 
  claims all physical computation is classically simulable; quantum computing challenges 
  this, and understanding the challenge is the theoretical argument for why quantum 
  computing matters at all.

---

#### L1-02 · Quantum Complexity Theory

**What it is and why it matters:** Your CS map covers P and NP (L1-11). Quantum 
computing adds new complexity classes that sit in a different relationship to those 
classical ones — and the resulting picture is the honest answer to the question 
"what can quantum computers actually do that classical computers cannot?" This is 
not a peripheral theory topic; it is the principled framing for every claimed 
quantum advantage. Without it, quantum speedup claims are folklore.

**Level 2 candidates:**

- **L2 · BQP (bounded-error quantum polynomial time)** — The quantum analogue of P; 
  the class of problems a quantum computer can solve efficiently, and understanding 
  where it sits relative to P and NP is the core open question in quantum complexity.
- **L2 · QMA (quantum Merlin-Arthur)** — The quantum analogue of NP; problems whose 
  solutions can be verified efficiently by a quantum computer, revealing that quantum 
  verification is itself a richer problem class than classical verification.
- **L2 · Oracle separations** — The method used to prove Grover's and Shor's give 
  genuine quantum speedups; understanding oracles explains why "quantum beats classical 
  on this benchmark" does not always translate to real-world advantage.
- **L2 · Quantum supremacy vs quantum advantage** — The distinction between 
  demonstrating that a quantum device can do something a classical one cannot (supremacy, 
  2019 Google experiment) and demonstrating it can solve a practically useful problem 
  faster (advantage, still largely unproven); the confusion between these two claims 
  drives most quantum hype.

---

#### L1-03 · The Mathematics of Quantum States

**What it is and why it matters:** Your CS map covers linear algebra for ML 
(L1-13) — vectors, matrices, transformations. Quantum computing uses the same 
mathematics but in a specific way: quantum states are unit vectors in complex 
Hilbert spaces, and quantum operations are unitary matrices acting on those 
spaces. The notation (Dirac's bra-ket, 1939) is unfamiliar but the underlying 
structure is not new to you. This topic closes the gap between the linear algebra 
you already know and the specific formalism quantum mechanics requires.

**Level 2 candidates:**

- **L2 · Complex vector spaces and Hilbert spaces** — Why quantum amplitudes are 
  complex numbers rather than real probabilities, and what inner products in complex 
  space reveal about quantum state similarity and orthogonality.
- **L2 · Dirac notation (bra-ket)** — The |ψ⟩ notation is not arbitrary; it separates 
  state vectors from their duals in a way that makes quantum operations cleaner to 
  express than matrix notation, and fluency with it is the prerequisite for reading 
  any quantum algorithm literature.
- **L2 · Unitary matrices and why gates must be unitary** — Unitarity preserves the 
  total probability of all outcomes summing to 1; understanding this constraint explains 
  why quantum gate sets look the way they do and why not every matrix is a valid 
  quantum operation.
- **L2 · Tensor products and multi-qubit systems** — When you combine two qubits, 
  the combined state space grows exponentially (2^n dimensions for n qubits); the 
  tensor product is the mathematical operation that explains both quantum parallelism 
  and why classical simulation of quantum systems is hard.
- **L2 · Eigenvalues and quantum measurement** — Measuring a quantum system returns 
  an eigenvalue of the measurement operator; the eigenvalue structure of Hermitian 
  matrices is what connects the abstract linear algebra to observable physical outcomes.

---

### Group 2 — Core Quantum Mechanics for Computation

*The physical principles that create computational power. Not physics for its own 
sake — physics read through the lens of what it enables algorithmically.*

---

#### L1-04 · Superposition and Interference

**What it is and why it matters:** Superposition is the most cited quantum property 
but the most frequently misunderstood. It does not mean "tries all paths simultaneously" 
in any operationally useful sense — a measurement on a superposed state gives one 
outcome. What matters computationally is interference: the ability to make probability 
amplitudes add constructively for correct answers and destructively for wrong ones. 
Every quantum algorithm is, at its core, an interference pattern. Understanding 
superposition without interference is understanding half the story.

**Level 2 candidates:**

- **L2 · Probability amplitudes vs classical probabilities** — Amplitudes can be 
  negative or complex and can cancel; classical probabilities cannot, and this 
  cancellation is the mechanism that makes quantum computation more than randomised 
  classical computation.
- **L2 · The Bloch sphere** — A geometric representation of a single qubit's state 
  as a point on a unit sphere; it makes quantum gate operations (rotations) visually 
  intuitive and reveals why a qubit has continuously many possible states despite 
  producing only a binary measurement.
- **L2 · Interference in algorithm design** — Grover's and the Deutsch-Jozsa algorithm 
  are both interference patterns amplifying correct outputs; understanding interference 
  as a design tool rather than a side effect is the shift from circuit-writing to 
  algorithm design thinking.
- **L2 · The double-slit analogy and its limits** — The double-slit experiment is 
  the standard introduction to quantum interference, but its limits as an analogy 
  for quantum computation are as important as its usefulness; knowing where it breaks 
  down prevents persistent misconceptions.

---

#### L1-05 · Entanglement

**What it is and why it matters:** Entanglement is the property that makes quantum 
states of multiple qubits inseparable — the state of the whole cannot be written 
as a product of the states of the parts. Bell's 1964 theorem proved this is a 
genuine physical phenomenon, not a classical correlation. Computationally, 
entanglement is what creates the exponential state space that quantum computers 
exploit and what makes quantum teleportation and superdense coding possible. 
It is also the resource that quantum error correction depends on.

**Level 2 candidates:**

- **L2 · Bell states** — The four maximally entangled two-qubit states; they are 
  the building blocks of teleportation, superdense coding, and many quantum protocols, 
  and understanding them concretely grounds the abstract definition of entanglement.
- **L2 · Bell's theorem and no local hidden variables** — Bell's 1964 proof that 
  entanglement cannot be explained by pre-agreed classical correlations; the CHSH 
  inequality is the experimental test, and its violation establishes that quantum 
  mechanics is genuinely non-classical, not just an unfamiliar classical model.
- **L2 · Entanglement as a computational resource** — Entanglement is consumed 
  in quantum protocols the way classical resources (memory, bandwidth) are consumed; 
  thinking of it as a resource with a cost rather than a magical property reframes 
  its role in algorithm design.
- **L2 · Quantum teleportation** — Not science-fiction teleportation but the exact 
  transfer of a quantum state using entanglement and classical communication; 
  understanding it concretely demonstrates that entanglement enables communication 
  of quantum information without transmitting the qubit itself.
- **L2 · Entanglement entropy** — A measure of how entangled a state is; high 
  entanglement entropy is what makes quantum systems hard to simulate classically, 
  which is both why quantum computers are powerful and why building them is difficult.

---

#### L1-06 · Quantum Gates and Circuit Design

**What it is and why it matters:** Quantum gates are the operational vocabulary 
of quantum circuits — the quantum analogue of your L1-06 logic gates, but with 
two crucial differences: they are reversible and they act on complex amplitudes. 
The standard gate set (Hadamard, CNOT, T gate, phase gates) was not chosen 
arbitrarily — these specific gates are universal, meaning any quantum computation 
can be expressed in terms of them. Understanding the gate set is the bridge from 
quantum mechanics to quantum programming.

**Level 2 candidates:**

- **L2 · The Hadamard gate** — The gate that creates superposition from a basis 
  state; it is to quantum computing what NOT is to classical, and understanding 
  its matrix form connects the linear algebra to the physical operation.
- **L2 · Pauli gates (X, Y, Z)** — The quantum analogues of classical bit flip 
  and phase operations; their commutation and anti-commutation relations underlie 
  much of quantum error correction theory.
- **L2 · The CNOT gate and two-qubit entanglement** — The controlled-NOT gate 
  is the two-qubit gate that creates entanglement from separable states; along 
  with single-qubit gates, it forms a universal gate set — the quantum equivalent 
  of NAND universality.
- **L2 · Universality and gate sets** — Just as NAND alone suffices for all 
  classical computation (your L1-06), a specific set of quantum gates suffices 
  for all quantum computation; understanding which sets are universal and why 
  explains quantum compiler design.
- **L2 · Circuit depth and gate count** — The resources of a quantum computation 
  are measured in gate count and circuit depth, not clock cycles; understanding 
  these metrics is prerequisite for comparing quantum algorithm efficiency.
- **L2 · The Toffoli gate** — A three-qubit gate that is classically universal; 
  it bridges quantum and classical gate theory and is used in quantum arithmetic 
  circuits within larger algorithms like Shor's.

---

### Group 3 — Quantum Algorithms

*The reason quantum computers are interesting. Each algorithm here represents 
a proven quantum advantage — and each has a specific structural reason why 
a quantum computer can solve it faster than any known classical method.*

---

#### L1-07 · Query Algorithms and Quantum Speedup

**What it is and why it matters:** The first quantum algorithms — Deutsch (1985), 
Deutsch-Jozsa (1992), Bernstein-Vazirani (1993) — were not practical but 
conceptually decisive. They proved that a quantum computer can answer certain 
questions about a function in fewer queries than any classical computer, 
regardless of how clever the classical algorithm is. This established that 
quantum speedup is real and structural, not a hardware speed advantage. They 
are the entry point for understanding what "quantum advantage" actually means 
formally.

**Level 2 candidates:**

- **L2 · The oracle model** — Query algorithms access their input through an oracle 
  (a black-box function); the oracle model isolates the quantum advantage to query 
  complexity alone, which is why these algorithms prove something precise about 
  quantum vs classical computation.
- **L2 · Deutsch's algorithm** — The first quantum algorithm to demonstrate quantum 
  speedup (1985), solving a trivial problem but proving the principle; understanding 
  it concretely reveals the interference mechanism that all subsequent algorithms 
  exploit.
- **L2 · Bernstein-Vazirani** — Finds a hidden string in one query where classical 
  algorithms need n; the gap scales linearly, and the algorithm structure directly 
  prepares you for Grover's.
- **L2 · Simon's algorithm** — Simon's 1994 algorithm provided the first exponential 
  quantum speedup and directly inspired Shor's; it is the conceptual bridge between 
  simple query algorithms and the harder number-theoretic results.

---

#### L1-08 · Grover's Search Algorithm

**What it is and why it matters:** Grover's algorithm (1996) is the canonical 
demonstration of quantum speedup on an unstructured problem. It searches an 
unsorted database of N items in O(√N) operations where classical search requires 
O(N). The speedup is quadratic rather than exponential — but it applies to any 
problem reducible to search, which is an enormous class. Understanding Grover's 
means understanding amplitude amplification, the general technique underlying 
the algorithm, which recurs as a subroutine in more advanced quantum algorithms.

**Level 2 candidates:**

- **L2 · Amplitude amplification** — The general mechanism behind Grover's: 
  iteratively rotating the quantum state toward the target by a small angle; 
  understanding the geometry of this rotation (the Grover iteration as a 2D 
  rotation) makes the O(√N) bound intuitive rather than magical.
- **L2 · The diffusion operator** — The inversion-about-the-mean step that 
  amplifies the target amplitude; it is a specific interference operation 
  whose structure reveals why Grover's uses exactly π/(4·arcsin(1/√N)) iterations.
- **L2 · Optimality of Grover's** — Bennett's 1997 proof that no quantum algorithm 
  can search faster than O(√N) establishes that Grover's is optimal; this bound 
  also explains why quantum computers cannot break symmetric encryption (AES) — 
  they halve the key strength but do not break it.
- **L2 · Applications beyond search** — Grover's as a subroutine in quantum 
  collision finding, minimum finding, and satisfiability; the pattern of using 
  amplitude amplification within larger algorithms is the key transferable skill.

---

#### L1-09 · Shor's Factoring Algorithm

**What it is and why it matters:** Shor's algorithm (1994) is the most consequential 
quantum algorithm known. It factors large integers in polynomial time where the 
best classical algorithm requires sub-exponential time — and RSA encryption, which 
secures most of the internet, depends on factoring being classically hard. (Your CS 
map covers RSA in L1-14 cryptography.) The algorithm is a case study in quantum 
algorithm design: the factoring problem is reduced to period-finding, which is then 
solved using the Quantum Fourier Transform. Each reduction is elegant and instructive.

**Level 2 candidates:**

- **L2 · Reduction of factoring to period-finding** — Shor's insight was that 
  factoring N reduces to finding the period of the function f(x) = a^x mod N; 
  understanding this reduction is a number theory problem as much as a quantum 
  one, and it separates Shor's classical pre/post-processing from its quantum core.
- **L2 · The Quantum Fourier Transform (QFT)** — The quantum analogue of the 
  discrete Fourier transform, computed in O(n²) quantum gates vs O(n 2^n) classical 
  operations; it is the engine of Shor's and appears in virtually every advanced 
  quantum algorithm as a subroutine.
- **L2 · Quantum Phase Estimation** — The algorithm that extracts eigenvalues 
  of unitary operators using the QFT; Shor's period-finding step is an instance 
  of phase estimation, and phase estimation itself appears in quantum chemistry 
  and quantum machine learning algorithms.
- **L2 · Post-quantum cryptography** — Because Shor's breaks RSA and elliptic 
  curve cryptography, NIST began a standardisation process in 2016; the 2024 
  finalised standards (CRYSTALS-Kyber, CRYSTALS-Dilithium) are the response, 
  and understanding Shor's explains both why the migration is urgent and what 
  "quantum-resistant" actually means.
- **L2 · Current hardware requirements vs current hardware reality** — Shor's 
  requires millions of logical qubits with error correction to break RSA-2048; 
  current devices have hundreds to thousands of noisy physical qubits; the gap 
  explains why RSA is not yet broken despite Shor's algorithm existing for 30 years.

---

### Group 4 — Quantum Hardware and the Engineering Reality

*The physical constraints that separate quantum theory from quantum practice. 
This group explains why quantum computers are hard to build and what the 
current frontier actually looks like.*

---

#### L1-10 · Qubits: Physical Implementations

**What it is and why it matters:** The qubit is an abstraction — the physical 
systems used to implement it vary enormously and have radically different 
properties. Superconducting qubits (IBM, Google), trapped ions (IonQ, Quantinuum), 
photonic qubits, and topological qubits (Microsoft's approach) are not equivalent 
implementations of the same thing — they embody different tradeoffs in coherence 
time, gate fidelity, connectivity, and scalability. Understanding the hardware 
landscape explains why quantum computers look the way they do and why certain 
algorithms are harder to run than their theoretical gate counts suggest.

**Level 2 candidates:**

- **L2 · Superconducting qubits** — The dominant commercial platform (IBM, Google); 
  operate at millikelvin temperatures, fast gates but short coherence times; 
  understanding their physical basis explains the connectivity constraints that 
  make CNOT gates between non-adjacent qubits expensive.
- **L2 · Trapped ion qubits** — Use individual atoms as qubits; slower gates but 
  longer coherence times and all-to-all connectivity; the comparison with 
  superconducting approaches illustrates the coherence-speed tradeoff that shapes 
  real circuit design.
- **L2 · Gate fidelity and error rates** — Every gate operation on real hardware 
  introduces error; fidelity (the probability a gate does what it should) is the 
  central metric that determines what circuits are executable today.
- **L2 · Connectivity graphs** — Real quantum devices have limited qubit-to-qubit 
  connections; an algorithm designed for all-to-all connectivity must be compiled 
  to the device's topology using SWAP gates, each of which adds error; the 
  compilation problem is one of the active research areas in quantum software.

---

#### L1-11 · Decoherence and Noise

**What it is and why it matters:** Quantum states are extraordinarily fragile. 
Any interaction with the environment collapses the superposition — this is 
decoherence, and it is the fundamental engineering challenge of quantum computing. 
The coherence time of a qubit (how long it holds its quantum state before 
decoherence) is the clock the entire computation must finish within. Understanding 
decoherence is what separates an honest assessment of quantum hardware from the 
marketing claims — and it is what makes error correction not an optional enhancement 
but an existential requirement for large-scale quantum computing.

**Level 2 candidates:**

- **L2 · The Lindblad master equation** — The mathematical framework for describing 
  open quantum systems evolving in the presence of noise; you do not need to solve 
  it, but knowing it exists frames decoherence as a quantitative engineering 
  parameter, not just a vague limitation.
- **L2 · Bit flip vs phase flip errors** — Quantum errors come in two orthogonal 
  types that have no classical analogue for phase flips; the structure of quantum 
  error correction codes is determined by the need to correct both simultaneously.
- **L2 · The threshold theorem** — If physical gate error rates are below a certain 
  threshold (~1%), quantum error correction can in principle make computation 
  arbitrarily reliable; the threshold theorem is the theoretical guarantee that 
  fault-tolerant quantum computing is possible in principle.
- **L2 · NISQ (Noisy Intermediate-Scale Quantum)** — Preskill's 2018 framing 
  of where quantum hardware currently sits: devices with 50–1000 qubits and no 
  error correction, useful for research but not fault-tolerant; understanding 
  NISQ defines what is and is not achievable with today's hardware.

---

#### L1-12 · Quantum Error Correction

**What it is and why it matters:** Classical error correction (parity bits, 
checksums) cannot be directly applied to quantum states — you cannot copy a 
qubit (no-cloning theorem) and measuring it to check for errors destroys the 
state. Quantum error correction (Shor's code, 1995; Steane code, 1996; the 
surface code) encodes one logical qubit in many physical qubits in a way that 
allows errors to be detected without measuring the logical state. This is the 
most mathematically demanding and practically consequential area in quantum 
engineering, and it is what separates NISQ devices from the fault-tolerant 
quantum computers that would run Shor's algorithm.

**Level 2 candidates:**

- **L2 · The no-cloning theorem** — A quantum state cannot be copied exactly; 
  the proof is a two-line linear algebra result, and the implication for error 
  correction, cryptography, and the fundamental limits of quantum information 
  is profound.
- **L2 · Stabiliser codes** — The framework (Gottesman, 1997) in which most 
  practical quantum error correcting codes are described; stabilisers are operators 
  whose eigenvalue tells you about an error without revealing the logical state, 
  which is the key conceptual step in quantum error correction.
- **L2 · The surface code** — The leading candidate for practical error correction 
  in superconducting quantum computers; it tolerates local errors with a threshold 
  around 1% and its structure — qubits on a 2D grid — matches naturally to 
  superconducting hardware topology.
- **L2 · Logical vs physical qubits and overhead** — A single logical (error-
  corrected) qubit requires hundreds to thousands of physical qubits; this overhead 
  is the direct explanation for why breaking RSA requires millions of physical qubits 
  despite the algorithm needing ~4000 logical qubits.
- **L2 · Fault-tolerant gate sets** — Not all quantum gates are compatible with 
  error correction; the Clifford + T gate set is the standard fault-tolerant 
  basis, and the T gate is the expensive one, which reshapes how fault-tolerant 
  circuits are designed and costed.

### Group 5 — Open Frontiers: What the Field Does Not Yet Know

*Quantum computing is not a mature field with settled answers awaiting 
implementation. Several of its most important questions are genuinely 
unresolved — some theoretically, some empirically, some both. This group 
maps the boundary between what is known and what is not, so the rest of 
the map can be read as a snapshot rather than a conclusion.*

---

#### L1-13 · Open Problems in Quantum Complexity

**What it is and why it matters:** The theoretical foundations of quantum 
computing rest on complexity questions that are as open as P vs NP — and 
some are directly connected to it. The relationship between BQP (what 
quantum computers can solve efficiently) and the classical complexity 
hierarchy is not fully understood. Whether quantum computers can solve 
NP-complete problems efficiently is almost certainly no, but it has not 
been proved. These are not engineering gaps — they are mathematical 
unknowns that would reshape the field if resolved either way.

**Level 2 candidates:**

- **L2 · Is BQP inside NP?** — The leading conjecture is that quantum 
  computers cannot solve NP-complete problems efficiently, but no proof 
  exists; if BQP ⊄ NP were proved, it would establish a formal separation 
  between quantum and classical computation more decisive than anything 
  currently known.
- **L2 · QPCP conjecture** — The quantum analogue of the PCP theorem; 
  whether quantum proofs can be checked locally is unresolved and its 
  resolution would have deep implications for quantum cryptography and 
  Hamiltonian complexity.
- **L2 · The quantum PCP vs NLTS gap** — Anshu, Breuckmann, and Nirkhe's 
  2022 proof of the NLTS (No Low-Energy Trivial States) theorem was a major 
  step toward the quantum PCP conjecture but did not resolve it; the gap 
  between what was proved and what is conjectured illustrates how incremental 
  progress looks in this area.
- **L2 · Dequantisation** — Tang's 2018 result showed that a famous quantum 
  machine learning algorithm (recommendation systems) could be matched by a 
  classical randomised algorithm; "dequantisation" is now an active research 
  programme asking which claimed quantum advantages survive scrutiny, and its 
  results have already shrunk the list.

---

#### L1-14 · The Quantum Advantage Question

**What it is and why it matters:** Whether quantum computers provide practical 
advantage on real problems — not contrived oracle problems — is still largely 
open. Google's 2019 "quantum supremacy" claim and IBM's near-simultaneous 
classical rebuttal illustrated that the frontier is contested, not settled. 
The field is currently in a period where claimed advantages are being published, 
challenged, and refined on timescales of months. For a practitioner, knowing 
how to read these claims — what they prove, what they assume, and what the 
classical counterargument is — is more durable than knowing any specific result.

**Level 2 candidates:**

- **L2 · Sampling problems and classical simulability** — The 2019 Google 
  supremacy experiment was a sampling task chosen because it is hard to simulate 
  classically; subsequent work by researchers at Alibaba and others showed improved 
  classical simulation, narrowing the gap; the episode illustrates that "hard to 
  simulate classically" is a moving target as classical algorithms improve.
- **L2 · Variational quantum algorithms (VQAs) and NISQ utility** — VQAs like 
  QAOA and VQE are the main candidates for near-term quantum advantage; whether 
  they will outperform classical optimisation methods on practical problem sizes 
  is an open empirical question, and several 2023–2024 results suggest classical 
  tensor network methods may match them at current circuit depths.
- **L2 · Quantum advantage in quantum chemistry** — The simulation of molecular 
  electronic structure is the most credible near-term application; the crossover 
  point at which a quantum computer outperforms classical chemistry codes is 
  estimated to require ~1000 logical qubits, which is likely a decade away at 
  current hardware trajectories.
- **L2 · The fault-tolerance timeline** — Major hardware roadmaps (IBM's, Google's, 
  Microsoft's) project fault-tolerant devices in the 2030s; these timelines have 
  slipped before and rest on achieving error rates and qubit counts not yet 
  demonstrated at scale; treating any specific date as reliable is unwarranted.

---

#### L1-15 · Open Problems in Quantum Error Correction

**What it is and why it matters:** Error correction is the gating problem for 
practical quantum computing, and several of its most important questions are 
unresolved. The threshold theorem proves fault tolerance is possible in principle, 
but the practical overhead — how many physical qubits per logical qubit at 
achievable error rates — is still being actively reduced by research. New 
codes are being discovered. The tradeoffs between code distance, gate overhead, 
and hardware topology are not fully characterised. This is the area of the field 
where theoretical progress most directly translates to a hardware milestone.

**Level 2 candidates:**

- **L2 · Good quantum LDPC codes** — Panteleev and Kalachev's 2022 construction 
  of asymptotically good quantum low-density parity-check codes was a decade-scale 
  open problem; it suggests that the physical qubit overhead for fault tolerance 
  may eventually be much lower than surface code estimates, but practical 
  implementations at scale have not been demonstrated.
- **L2 · Magic state distillation overhead** — The T gate (required for universal 
  fault-tolerant computation) cannot be implemented directly from the Clifford 
  group and requires "magic state distillation," a costly procedure; reducing 
  this overhead is one of the most active areas in fault-tolerant circuit design.
- **L2 · Biased noise and hardware-tailored codes** — Real hardware noise is 
  not symmetric (phase errors often dominate bit errors in superconducting qubits); 
  codes tailored to biased noise channels can achieve lower overhead, but the 
  optimal code for each hardware platform is an active research question.
- **L2 · Bosonic codes** — An alternative approach encoding a logical qubit 
  in the infinite-dimensional state space of a harmonic oscillator (cat codes, 
  GKP codes); Amazon's and Yale's hardware programs are pursuing this direction, 
  and whether it will achieve lower overhead than qubit-based codes at scale 
  is unresolved.

---

#### L1-16 · Quantum Algorithms: The Unsolved Discovery Problem

**What it is and why it matters:** The algorithm landscape is surprisingly sparse. 
Most known quantum algorithms either descend from QFT (Shor's, phase estimation) 
or amplitude amplification (Grover's). Whether there are fundamentally different 
algorithmic techniques — quantum algorithms with structures we have not yet 
discovered — is genuinely unknown. The field has been searching since the 1990s 
and the list of proven exponential speedups on practically relevant problems 
remains short. This is the honest picture of where quantum algorithms research 
stands, and it contextualises both the excitement and the caution warranted by 
the field's current state.

**Level 2 candidates:**

- **L2 · The algorithm zoo** — The Quantum Algorithm Zoo (maintained by Stephen 
  Jordan at NIST) is the canonical catalogue of known quantum algorithms and their 
  speedups; surveying it reveals both the breadth and the sparsity of the landscape 
  — many algorithms solve contrived or narrow problems.
- **L2 · Quantum walks** — A quantum analogue of random walks that produces 
  quadratic speedups on certain graph problems; it is the third major algorithmic 
  technique after QFT-based and amplitude amplification approaches, and whether 
  it leads to further discoveries is an open research question.
- **L2 · HHL and quantum linear systems** — Harrow, Hassidim, Lloyd's 2009 
  algorithm provides exponential speedup for solving linear systems under specific 
  conditions; subsequent work showed those conditions are more restrictive than 
  initially understood, and it became a case study in how quantum algorithm 
  advantages can be partially dequantised.
- **L2 · Quantum machine learning: promise vs evidence** — The early 2010s wave 
  of quantum ML algorithms (quantum PCA, quantum SVM) claimed exponential speedups; 
  most have since been shown to require quantum RAM (which does not exist at scale) 
  or have classical analogues; the gap between the claims in papers and the 
  achievable practical advantage is one of the most contested areas of current 
  research.

---

## Sequencing note

The dependency chain runs in group order. Group 1 (the bridge) is mandatory 
first — not because the material is hardest but because it reframes what you 
already know. Without L1-02 (complexity theory), you will misread every 
quantum speedup claim you encounter. Without L1-03 (the mathematics), Group 
2 will feel like vocabulary without grammar.

Within Group 2, L1-04 (superposition/interference) and L1-05 (entanglement) 
are genuinely parallel and can be read in either order. L1-06 (gates) depends 
on both. Group 3 can be approached selectively: L1-07 (query algorithms) is 
the conceptual foundation for understanding what a speedup proof means; 
L1-08 (Grover's) is the most accessible algorithm to fully understand before 
tackling L1-09 (Shor's), which has the highest mathematical demand of any 
topic in the map.

Group 4 can be read at any point after Group 2 — it is largely independent 
of the algorithm content and is the practical counterweight to the theoretical 
Groups 2 and 3. For someone who has run circuits on IBM hardware (as the Packt 
course provides), reading Group 4 after Group 3 will reframe that hands-on 
experience with the principled understanding it was missing.

Group 5 sits outside the dependency chain — it can be read at any point 
after Group 1, and benefits from being revisited after Groups 3 and 4 
when the theoretical and hardware context is in place. Its purpose is 
not to be learned but to be known: the map should be read as a live 
document, and Group 5 is where that liveness is most concentrated. 
The open problems here will have developments on 6–18 month timescales — 
tracking them is part of maintaining the map, not completing it.