# Mathematics for Quantum Computing — Level 0: Course Map

> **Intent:** Build the mathematical fluency needed to read Qiskit documentation, follow gate descriptions, and understand quantum circuit notation without hitting a wall. This is not a mathematics course — it is a targeted preparation for one specific downstream task.
>
> **Your angle:** You have a CS degree. You have seen linear algebra — probably in a numerical methods or ML context — and you are comfortable with vectors and matrices as computational objects. What you likely have not seen is the complex-valued, physically-motivated version of that material that quantum mechanics runs on. The goal is not to rebuild your mathematical foundations. It is to extend them in three specific directions: complex numbers, quantum-flavoured linear algebra, and the Dirac notation that quantum computing literature uses universally. Nothing here is genuinely new mathematics. Most of it is familiar structure in unfamiliar clothing.

---

## How to use this map

This map is a prerequisite layer for the Quantum Computing Level 0 map, not a standalone curriculum. Every topic here connects directly to a concept in that map — the cross-references are explicit. Work through this map first, then keep it open as a reference when the QC map surfaces a notation or operation that needs grounding.

Each **Level 1 topic** is one mathematical concept area: what it is, why quantum computing specifically needs it, and what becomes readable once you have it. Each **Level 2 candidate** is a specific technique or result worth drilling to the point of fluency.

The map is sequenced by dependency. Group 1 is genuinely foundational — do not skip it even if complex numbers feel familiar. Group 2 is the core payload. Group 3 is the notation layer that makes the core payload usable when reading circuit diagrams and algorithm descriptions.

---

## Topic Inventory

---

### Group 1 — Complex Numbers: The Foundation You Were Not Taught For This Purpose

*You have seen complex numbers. You have probably not seen them used as the fundamental data type of a physical theory. This group closes that gap — not by teaching complex numbers from scratch, but by building the specific intuitions quantum mechanics requires.*

---

#### L1-01 · Complex Numbers as Amplitudes

**What it is and why it matters:** In classical probability, the state of a system is described by real numbers between 0 and 1 that sum to 1. In quantum mechanics, the state of a system is described by complex numbers — called amplitudes — whose squared magnitudes sum to 1. This is not a generalisation for mathematical elegance: it is a physical fact, and it is the source of interference. Two amplitudes can cancel each other in a way two probabilities never can. Every quantum gate, every circuit diagram, and every Qiskit statevector output is built on this. Getting comfortable with complex numbers as the native data type of quantum states is the first prerequisite for reading anything else.

**Level 2 candidates:**

- **Rectangular and polar form** — The same complex number written as a+bi or as re^(iθ); quantum states are almost always written in polar form because the angle θ (the phase) is what interference acts on, and switching fluently between forms is a constant low-level skill in circuit analysis.
- **Complex conjugates and modulus** — The conjugate of a+bi is a−bi; the modulus |z| = √(a²+b²); quantum probabilities are computed as |amplitude|² = z·z*, and this operation appears in every measurement calculation and in the definition of inner products.
- **Euler's formula** — e^(iθ) = cos(θ) + i·sin(θ); this identity is how quantum phases are written compactly, how rotation gates are parameterised in Qiskit, and how the Bloch sphere angles map to qubit states; it appears constantly and should be automatic.
- **Phase as a physical quantity** — A global phase (multiplying the entire state by e^(iθ)) is physically unobservable; a relative phase (different phases on different components of a superposition) is observable and is what interference exploits; understanding the difference is essential for reading gate descriptions correctly.

---

#### L1-02 · Trigonometry and the Unit Circle

**What it is and why it matters:** Quantum gate operations on single qubits are rotations — rotations of a state vector on the Bloch sphere, parameterised by angles. Qiskit's rotation gates (Rx, Ry, Rz, U gate) are all expressed in terms of sin and cos of half-angles. Reading a gate matrix and knowing what it does geometrically requires being able to evaluate sin and cos at standard angles and to recognise rotation structure in a 2×2 matrix. This is not new material — it is a fluency check on material you already have.

**Level 2 candidates:**

- **Sin, cos, and the unit circle at standard angles** — Values at 0, π/6, π/4, π/3, π/2, π and their negatives; quantum gate matrices are written in terms of these values and recognising them on sight is faster than computing them each time.
- **Radians vs degrees** — Quantum mechanics and Qiskit use radians throughout; Qiskit's rotation gates take radian arguments; if your instinct is in degrees, converting it is a minor but persistent friction point worth eliminating.
- **Rotation matrices in 2D** — The 2×2 rotation matrix [[cos θ, −sin θ], [sin θ, cos θ]]; single-qubit quantum gates are 2×2 unitary matrices, and many of them are directly rotation matrices or close relatives; recognising the structure makes gate behaviour geometrically legible.

---

### Group 2 — Linear Algebra: The Quantum-Specific Extension

*You know vectors and matrices as computational objects. Quantum mechanics uses them as the mathematical language of physical states and operations. This group covers the specific extensions — complex inner products, unitary matrices, tensor products — that your prior linear algebra likely did not include.*

---

#### L1-03 · Vectors and Vector Spaces Over the Complex Numbers

**What it is and why it matters:** A quantum state is a vector in a complex vector space. A single qubit's state is a 2-dimensional complex vector; an n-qubit state is a 2ⁿ-dimensional complex vector. The structure you know from real vector spaces — linear combinations, basis vectors, span — carries over directly, but with complex scalars. The specific vector space quantum mechanics uses is called a Hilbert space, which adds an inner product. Most of what you need is standard linear algebra extended to complex entries; the Hilbert space terminology is largely a label for this extension, not new mathematics.

**Level 2 candidates:**

- **Complex vector arithmetic** — Addition and scalar multiplication with complex scalars; the mechanics are identical to real vectors with complex entries; fluency here means not slowing down when a vector has i in its components.
- **Basis vectors and the computational basis** — In quantum computing the standard basis for a single qubit is |0⟩ = [1, 0]ᵀ and |1⟩ = [0, 1]ᵀ; any qubit state is a linear combination of these; recognising the computational basis as an ordinary orthonormal basis removes the mystery from the notation.
- **Linear combinations and superposition** — A superposition state is exactly a linear combination of basis vectors with complex coefficients (amplitudes); there is no new mathematics here, only a physical interpretation layered onto the algebra you already know.
- **Span and dimension** — An n-qubit system lives in a 2ⁿ-dimensional complex vector space; the exponential growth of the state space with qubit count is a fact about vector space dimension, not a mystery, and it is the direct mathematical explanation for why quantum systems are hard to simulate classically.

---

#### L1-04 · Inner Products and Orthogonality

**What it is and why it matters:** The inner product is what connects the abstract vector space to physical measurement. In quantum mechanics, the probability of measuring a particular outcome is the squared magnitude of the inner product between the current state and the measurement basis vector. The inner product also defines orthogonality — orthogonal states are perfectly distinguishable, which is why quantum measurement outcomes correspond to orthogonal basis vectors. Getting the inner product right in the complex case — where conjugation is required — is a small but consequential correction to the real-valued version you likely learned.

**Level 2 candidates:**

- **The complex inner product** — For complex vectors, the inner product ⟨u, v⟩ conjugates the first argument: ⟨u, v⟩ = u*ᵀ · v; omitting the conjugate gives wrong answers for complex states and is the most common error when extending real linear algebra to quantum mechanics.
- **Norm and normalisation** — A quantum state vector must have norm 1 (probabilities must sum to 1); ‖v‖ = √⟨v,v⟩; normalisation is a constant operation in quantum state preparation and in verifying that a gate preserves valid states.
- **Orthogonality and distinguishable states** — Two quantum states are perfectly distinguishable if and only if they are orthogonal; the computational basis states |0⟩ and |1⟩ are orthogonal, and measurement in the computational basis is projection onto these orthogonal vectors.
- **Projection** — The projection of a state onto a basis vector gives the amplitude for that measurement outcome; the probability of that outcome is the squared magnitude of the projection; understanding projection makes measurement calculations mechanical rather than mysterious.

---

#### L1-05 · Matrices as Linear Maps and Quantum Gates

**What it is and why it matters:** Quantum gates are matrices — specifically, square matrices acting on state vectors. Every gate in Qiskit has an underlying matrix, and reading that matrix tells you exactly what the gate does to any input state. The connection between a matrix and its action as a linear map is the core of this topic. If you have used matrices mainly as data structures (storing weights, representing graphs), this is the conceptual shift: a quantum gate matrix is a function, and multiplying it by a state vector is evaluating that function on the state.

**Level 2 candidates:**

- **Matrix-vector multiplication as state transformation** — Applying a quantum gate to a qubit state is matrix-vector multiplication; if you can multiply a 2×2 complex matrix by a 2×1 complex vector, you can compute the output of any single-qubit gate.
- **Matrix multiplication as gate composition** — Applying two gates in sequence is multiplying their matrices; gate circuit diagrams read left-to-right but matrix multiplication applies right-to-left; getting this order right is the difference between correct and wrong circuit analysis.
- **The identity matrix and do-nothing gates** — The identity matrix I leaves the state unchanged; it appears explicitly in multi-qubit tensor products when a gate acts on one qubit but not another, and recognising it prevents confusion when reading circuit matrix representations.
- **Eigenvalues and eigenvectors** — An eigenvector of a matrix is unchanged in direction by that matrix; quantum measurement operators have eigenvectors corresponding to definite measurement outcomes; you need this concept to understand why measuring in different bases gives different results.
- **The determinant and invertibility** — A matrix is invertible if and only if its determinant is non-zero; quantum gates are always invertible (unitary implies invertible), which is the mathematical expression of reversible computation; checking invertibility via the determinant is a useful sanity check.

---

#### L1-06 · Unitary Matrices

**What it is and why it matters:** Every quantum gate is a unitary matrix. Unitary matrices are the complex analogue of rotation matrices: they preserve the norm of any vector they act on, which is the mathematical requirement that quantum gates preserve the total probability of all outcomes summing to 1. The defining property — U†U = I, where U† is the conjugate transpose — is the single constraint that determines which matrices are valid quantum gates and which are not. Every gate you use in Qiskit satisfies this, and knowing what it means lets you verify gate properties and understand why certain operations are forbidden.

**Level 2 candidates:**

- **The conjugate transpose (Hermitian adjoint)** — The conjugate transpose U† is obtained by transposing the matrix and conjugating every entry; for a quantum gate U, applying U† reverses the gate — it is the inverse operation; this is the mathematical basis for uncomputation in quantum circuits.
- **Unitarity condition U†U = I** — A matrix is unitary if and only if its conjugate transpose is also its inverse; this is the constraint that makes a matrix a valid quantum gate; verifying it for the Hadamard and Pauli matrices is a useful exercise that builds intuition for the gate set.
- **Norm preservation** — A unitary matrix preserves the norm of any vector: ‖Uv‖ = ‖v‖; since quantum states must have norm 1, norm preservation is exactly the constraint that quantum gates must satisfy to map valid states to valid states.
- **Unitary matrices as generalisations of rotations** — Real orthogonal matrices (rotations and reflections) are the real special case of unitary matrices; every quantum gate is a rotation or reflection of the state vector in complex space; this geometric picture is what the Bloch sphere visualises for single qubits.
- **The Pauli matrices as a basis** — The four matrices I, X, Y, Z (the Paulis) form a basis for all 2×2 Hermitian matrices, and any 2×2 unitary can be expressed in terms of them; they appear constantly in gate descriptions, error models, and Hamiltonian representations in Qiskit.

---

#### L1-07 · Hermitian Matrices and Observables

**What it is and why it matters:** Measurement in quantum mechanics is represented by Hermitian matrices — matrices that equal their own conjugate transpose (H = H†). The eigenvalues of a Hermitian matrix are always real, which is why measurement outcomes are real numbers. The eigenvectors form an orthonormal basis, which is why measurement always produces one definite outcome from a set of orthogonal possibilities. You do not need to work with Hermitian matrices routinely for circuit-level Qiskit work, but you need the concept to understand why quantum measurement is structured the way it is and to read any documentation that discusses observables or expectation values.

**Level 2 candidates:**

- **The Hermitian condition H = H†** — A Hermitian matrix equals its conjugate transpose; the diagonal entries are always real; the off-diagonal entries come in conjugate pairs; checking this condition is quick and worth doing when an unfamiliar operator appears.
- **Real eigenvalues of Hermitian matrices** — Hermitian matrices always have real eigenvalues; this is why measurement outcomes (which correspond to eigenvalues) are real numbers despite the state vector being complex; the proof is a one-line inner product argument.
- **Orthogonal eigenvectors and measurement bases** — The eigenvectors of a Hermitian matrix corresponding to distinct eigenvalues are orthogonal; measurement in the computational basis corresponds to the eigenvectors of the Pauli Z matrix; changing measurement basis is changing which Hermitian matrix you are diagonalising.
- **Expectation values** — The expectation value ⟨ψ|H|ψ⟩ is the average measurement outcome over many repetitions; expectation values appear throughout VQE documentation and Qiskit's observable framework; computing one requires the inner product and matrix-vector multiplication you already have.

---

#### L1-08 · Tensor Products

**What it is and why it matters:** The tensor product is the mathematical operation that combines two quantum systems into one larger system. A single qubit lives in a 2-dimensional space; two qubits together live in a 4-dimensional space constructed as the tensor product of two 2-dimensional spaces; n qubits live in a 2ⁿ-dimensional space. This exponential growth is both why quantum computers are powerful (the state space is enormous) and why they are hard to simulate classically (you cannot store 2ⁿ amplitudes efficiently for large n). Every multi-qubit circuit in Qiskit is operating on tensor product spaces, and every multi-qubit gate matrix is constructed using tensor products.

**Level 2 candidates:**

- **The Kronecker product** — The tensor product of two matrices is computed via the Kronecker product: replace each entry a_ij of the first matrix with a_ij times the entire second matrix; this is the concrete computation behind every two-qubit gate matrix and behind Qiskit's internal state representations.
- **Separable vs entangled states** — A two-qubit state is separable if it can be written as the tensor product of two single-qubit states; if it cannot, it is entangled; testing separability is a direct application of tensor product structure and makes the definition of entanglement precise.
- **Tensor products of gates** — Applying gate A to qubit 1 and gate B to qubit 2 simultaneously corresponds to the tensor product A⊗B acting on the combined state; this is how single-qubit gates on individual qubits are represented in the full multi-qubit circuit matrix.
- **Identity padding** — When a gate acts on one qubit of a multi-qubit system and leaves the others unchanged, the gate matrix is tensored with identity matrices for the unused qubits; this is a constant pattern in multi-qubit circuit matrices and understanding it makes those matrices readable.
- **State space scaling** — Each additional qubit doubles the dimension of the state space; the state of 10 qubits requires 2¹⁰ = 1024 complex amplitudes; 50 qubits require over 10¹⁵; this is the mathematical fact behind why classical simulation of quantum computers is hard beyond ~50 qubits.

---

### Group 3 — Dirac Notation: Reading the Language of Quantum Computing

*All quantum computing literature — Qiskit documentation, textbooks, papers — uses Dirac (bra-ket) notation. It is not new mathematics: it is a compact, consistent notation for the inner product and linear algebra you have just covered. This group makes it automatic.*

---

#### L1-09 · Kets, Bras, and the Bra-Ket Inner Product

**What it is and why it matters:** Dirac notation, introduced by Paul Dirac in 1939, is the universal language of quantum mechanics and quantum computing literature. A ket |ψ⟩ is a column vector (a quantum state). A bra ⟨ψ| is its conjugate transpose — a row vector. The inner product ⟨φ|ψ⟩ is bra times ket, giving a complex number. This is all it is: a compact notation for operations you already know. The payoff is that Qiskit documentation, circuit diagrams, and algorithm descriptions all use this notation without explanation. Fluency with it means being able to read them without translation overhead.

**Level 2 candidates:**

- **Ket |ψ⟩ as a column vector** — Every quantum state is a ket; |0⟩ = [1, 0]ᵀ, |1⟩ = [0, 1]ᵀ are the computational basis kets; any superposition is a linear combination α|0⟩ + β|1⟩ = [α, β]ᵀ; fluency means not needing to mentally translate back to matrix notation.
- **Bra ⟨ψ| as the conjugate transpose** — The bra ⟨ψ| = (|ψ⟩)† is the row vector obtained by transposing and conjugating; it is not a different object from the ket, just the same state in dual form; the inner product ⟨φ|ψ⟩ is then standard row-times-column matrix multiplication.
- **Inner product ⟨φ|ψ⟩ and its interpretation** — The inner product of two states is a complex number; its squared magnitude |⟨φ|ψ⟩|² is the probability of measuring state |φ⟩ when the system is in state |ψ⟩; this is the fundamental measurement rule in Dirac notation.
- **Orthonormality of basis states** — ⟨0|0⟩ = 1, ⟨1|1⟩ = 1, ⟨0|1⟩ = 0; these three facts are used constantly in quantum calculation; they follow directly from the inner product definition but are worth knowing as immediate reflexes.

---

#### L1-10 · Operators, Outer Products, and Matrix Representation

**What it is and why it matters:** In Dirac notation, a quantum gate applied to a state is written as U|ψ⟩ — the operator (matrix) acting on the ket (vector). The outer product |φ⟩⟨ψ| is the complementary operation: bra times ket gives a scalar, ket times bra gives a matrix. Projection operators, measurement operators, and many gate constructions are written as outer products. Being able to read and construct these representations is what lets you follow derivations in Qiskit's algorithm documentation and understand how measurement projectors are built.

**Level 2 candidates:**

- **Operator notation U|ψ⟩** — A gate U applied to state |ψ⟩ is written U|ψ⟩; this is matrix-vector multiplication; the notation change is cosmetic but must be automatic before circuit-level reading is fluent.
- **The outer product |φ⟩⟨ψ|** — Ket times bra is a matrix (outer product); |0⟩⟨0| = [[1,0],[0,0]] and |1⟩⟨1| = [[0,0],[0,1]] are the projection operators onto the computational basis states; they appear in measurement definitions and density matrix formalism.
- **Projectors and measurement** — Measuring in the computational basis applies projector P₀ = |0⟩⟨0| or P₁ = |1⟩⟨1|; the probability of each outcome is ⟨ψ|Pₙ|ψ⟩; this is the Dirac-notation expression of the projection operation from L1-04.
- **Completeness relation** — The projectors onto any complete orthonormal basis sum to the identity: Σᵢ |i⟩⟨i| = I; this identity is used constantly in derivations to insert a resolution of the identity, and recognising it makes multi-step quantum calculations readable.
- **Matrix elements** — The (i,j) entry of a matrix U in Dirac notation is ⟨i|U|j⟩ (bra-ket sandwiching the operator); this is how gate matrices are defined and computed in quantum mechanics derivations and is the bridge between the abstract operator and the concrete matrix.

---

#### L1-11 · Multi-Qubit Notation and Circuit Reading

**What it is and why it matters:** Multi-qubit states in Dirac notation are written as tensor products of single-qubit kets: |01⟩ = |0⟩⊗|1⟩ = [0, 1, 0, 0]ᵀ. Quantum circuit diagrams are read left-to-right, but the corresponding matrix expressions are applied right-to-left. Qubit ordering conventions differ between textbooks and Qiskit. These are notational facts, not mathematics — but getting them wrong produces incorrect calculations and incorrect Qiskit circuits. This topic exists to make those conventions explicit and automatic.

**Level 2 candidates:**

- **Multi-qubit ket notation** — |01⟩ means qubit 1 is in state |0⟩ and qubit 2 is in state |1⟩; it corresponds to the tensor product |0⟩⊗|1⟩ and maps to a specific computational basis vector in the 4-dimensional two-qubit state space; fluency means knowing which vector without computing it.
- **Circuit diagram reading order vs matrix order** — In a circuit diagram, gates applied first are drawn leftmost; in the corresponding matrix expression, they appear rightmost (applied first); this reversal is a constant source of errors and must be automatic.
- **Qiskit qubit ordering** — Qiskit orders qubits with qubit 0 as the least significant bit, which is the reverse of most textbook conventions; this affects how statevector outputs map to ket notation and is the most common source of confusion when comparing Qiskit output to textbook calculations.
- **Bell state notation** — The four Bell states (|Φ+⟩, |Φ-⟩, |Ψ+⟩, |Ψ-⟩) are the standard maximally entangled two-qubit states; recognising them in both vector and Dirac notation is a practical fluency marker, since they appear throughout quantum protocol descriptions and Qiskit examples.
- **Tensor product notation shortcuts** — |0⟩⊗n means n qubits all in state |0⟩; |+⟩ = (|0⟩+|1⟩)/√2 is standard shorthand for the uniform superposition; these compact forms appear constantly in Qiskit documentation and algorithm descriptions without further explanation.

---

## Sequencing note

Work through the groups strictly in order. Group 1 (complex numbers) is the prerequisite for everything in Group 2 — quantum states have complex amplitudes, and none of the linear algebra makes sense without that established first. L1-01 (complex numbers as amplitudes) and L1-02 (trigonometry and rotation) are both needed before L1-05 (matrices as gates), since gate matrices contain complex exponentials and trigonometric entries throughout.

Within Group 2, the dependency order is L1-03 → L1-04 → L1-05 → L1-06, then L1-07 and L1-08 in parallel. Tensor products (L1-08) require matrix fluency from L1-05 and L1-06; Hermitian matrices (L1-07) require inner products from L1-04. Both L1-07 and L1-08 feed directly into Group 3.

Group 3 requires all of Group 2. It is not additional mathematics — it is the notation layer over the mathematics you have just built. Dirac notation without the underlying linear algebra is memorisation; with it, the notation is transparent. Work through L1-09 and L1-10 before touching the Quantum Computing Level 0 map. L1-11 (multi-qubit notation and Qiskit conventions) can be read when the QC map first introduces multi-qubit circuits — it is the most Qiskit-specific topic here and is most useful with concrete circuit examples in front of you.

**Crosswalk to the Quantum Computing map:** L1-01 and L1-02 here ground QC/L1-01 (Computational Model Shift) and QC/L1-02 (Mathematics You Need). Group 2 as a whole is the prerequisite for QC/L1-05 (Gates and Circuit Design) and everything downstream of it. Group 3 is the prerequisite for reading any Qiskit documentation, circuit notation, or algorithm description in the QC map without translation overhead.
