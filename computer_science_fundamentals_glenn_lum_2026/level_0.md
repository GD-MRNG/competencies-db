# CS Fundamentals — Level 0: Course Map

> **Intent:** Build a durable floor of understanding across classical computer science — not to re-learn what you already do, but to fill the conceptual architecture that years of practical work leave patchy. The goal is principled reasoning: knowing *why* things are the way they are, not just that they work.
>
> **Your angle:** You are a practitioner with 3–5 years of industry experience returning to foundations. You think top-down and contextually. You want the map before the territory, and the historical thread before the mechanics.

---

## How to use this map

Each **Level 1 topic** below is one concept post to generate: what it is, why it matters, where it sits in the larger picture.

Each **Level 2 sub-concept** is a candidate for a depth post: mechanics, tradeoffs, where it breaks. You do not generate all of them. You descend only into the sub-concepts where deeper mastery is worth the effort.

The year groupings are a sequencing guide, not a strict order. They reflect the logical dependency chain: later topics assume earlier ones.

---

## Topic Inventory

---

### Group 1 — Year 1–2: Foundations

---

#### L1-01 · Computation Basics

**What it is and why it matters:** The philosophical and mathematical foundation of what computing even is. Before any language, any machine, any algorithm — there was a question: *what does it mean to compute something?* Turing's answer in 1936 set the outer boundary of the entire field. Everything built since is an implementation detail relative to this.

**Level 2 candidates:**

- **L2 · What is an algorithm** — A precise finite procedure for solving a problem. Predates computers by millennia (Euclid, al-Khwarizmi). Understanding this separates "code that works" from "a solution to a well-defined problem."
- **L2 · The Turing Machine** — The 1936 thought experiment that defined computability. Not a real machine — a formal model. Every computer ever built is an implementation of this idea.
- **L2 · Church-Turing Thesis** — The claim that anything computable by any means is computable by a Turing Machine. Sets the ceiling on what computers can do in principle — not in practice, but in principle.
- **L2 · Binary and information encoding** — Why computers use binary, and how all data — text, images, sound — reduces to numbers. Shannon's 1948 information theory paper is the origin. Understanding encoding is the bridge from math to machine.

---

#### L1-02 · Discrete Mathematics

**What it is and why it matters:** The mathematics that computation runs on. Continuous math (calculus) models the physical world. Discrete math models logical and structural relationships — the kind that programs, databases, and proofs are built from. If you want to read algorithm proofs or type theory, this is the prerequisite.

**Level 2 candidates:**

- **L2 · Logic and boolean algebra** — AND, OR, NOT, implication. The same logic that governs if-statements governs circuit design and formal proofs. The connection between these three domains is non-obvious and worth understanding explicitly.
- **L2 · Set theory** — The language of collections, membership, and relations. Databases, type systems, and most mathematical definitions in CS are expressed in these terms.
- **L2 · Graph theory** — Nodes and edges. Networks, dependency trees, social graphs, routing — almost every interesting real-world problem maps onto a graph. The concepts here recur constantly in applied work.
- **L2 · Proof techniques** — Induction, contradiction, direct proof. How you *know* an algorithm is correct rather than just apparently correct. Not about doing proofs — about reading them and trusting results.
- **L2 · Combinatorics** — Counting possibilities. Underlies algorithm complexity analysis and cryptography. Explains why certain problems are hard even when they look simple.

---

#### L1-03 · Programming Fundamentals

**What it is and why it matters:** The bridge between computational ideas and working machines. This is where you learn to think precisely enough that a machine can follow your reasoning — and where you see how language features map onto memory and execution. Practitioners often use these correctly without understanding what is actually happening underneath.

**Level 2 candidates:**

- **L2 · Variables, types, and memory** — What actually happens when you declare a variable. The difference between a value and a reference. Stack vs heap allocation. This is the layer where most subtle bugs live.
- **L2 · Control flow** — How a program decides what to do next. Conditionals and loops as implementations of logical propositions. Determinism and what makes a program predictable.
- **L2 · Functions and scope** — Abstraction at its most basic. Why functions are not just organisational convenience — they are how complexity is managed and how programs compose.
- **L2 · Recursion** — A function that calls itself. Unintuitive until you see it as mathematical induction in code form. Maps directly onto how trees, grammars, and many algorithms are naturally expressed.

---

#### L1-04 · Data Structures

**What it is and why it matters:** Algorithms need somewhere to put data. The choice of structure determines which operations are fast and which are slow — this is where most real performance decisions actually live. The structures here are not arbitrary; each one was invented to solve a specific limitation of the ones before it.

**Level 2 candidates:**

- **L2 · Arrays** — Contiguous memory, O(1) access by index. The simplest structure and the building block of most others. Understanding arrays means understanding what "contiguous" actually costs.
- **L2 · Linked lists** — Elements pointing to each other rather than sitting adjacently in memory. Efficient insertion, slow lookup. A historical workaround for fixed-size memory allocations that reveals how memory actually works.
- **L2 · Stacks and queues** — LIFO and FIFO access patterns. Ubiquitous in parsing, call stacks, scheduling, and undo systems. Deceptively simple — understanding their structure demystifies many system behaviours.
- **L2 · Hash tables** — Key-value lookup in near-constant time. How dictionaries, caches, and database indexes work under the hood. Understanding hash collisions and load factors explains the "near-constant" qualifier.
- **L2 · Trees** — Hierarchical structure. File systems, the DOM, compilers, and databases all use trees. Binary search trees enable O(log n) search — understanding why requires understanding the structure.
- **L2 · Heaps** — A tree that always keeps the smallest (or largest) element at the root. The backbone of priority queues and efficient sorting algorithms. Explains how schedulers and event loops prioritise work.
- **L2 · Graphs** — The general case of which trees are a constrained subset. Most interesting real-world structures are graphs. Recognising when a problem is a graph problem is a significant analytical skill.

---

#### L1-05 · Algorithms

**What it is and why it matters:** The vocabulary and analytical toolkit for reasoning about solutions independent of language or implementation. This is where you move from "it works" to "it works at scale, and I can prove it." Also where you develop intuition for *why* a given approach is the right one for a given shape of problem.

**Level 2 candidates:**

- **L2 · Big-O complexity** — A language for describing how an algorithm's cost grows with input size. The single most transferable analytical tool in software work. Without it, performance intuitions are guesses.
- **L2 · Sorting algorithms** — The canonical algorithmic problem. Quicksort, mergesort, heapsort each embody different tradeoffs between time, space, and stability. Understanding sorting teaches algorithm design thinking more than the sorts themselves.
- **L2 · Searching** — Linear vs binary search. Why sorted data is dramatically more powerful than unsorted data. The bridge between data structure choice and algorithm performance.
- **L2 · Divide and conquer** — Breaking a problem into smaller versions of itself, solving each, and combining results. The design pattern behind mergesort, binary search, and most tree algorithms.
- **L2 · Dynamic programming** — Storing intermediate results to avoid redundant computation. The step up from divide and conquer for problems where subproblems overlap. Recognising the pattern is the skill.
- **L2 · Greedy algorithms** — Making locally optimal choices at each step. Sometimes this gives the global optimum. Sometimes it doesn't. Knowing when to trust a greedy approach is a non-trivial judgment.
- **L2 · Graph algorithms** — BFS, DFS, Dijkstra's shortest path, minimum spanning trees. The toolkit for anything modelled as a network. These recur across routing, dependency resolution, social graphs, and more.

---

### Group 2 — Year 2–3: Core CS Theory

---

#### L1-06 · Computer Architecture

**What it is and why it matters:** Software is not abstract. It runs on physical machines with specific constraints. Understanding the hardware explains why certain software patterns exist, why certain operations are slow, and why certain optimisations work. Without this layer, performance reasoning is folklore.

**Level 2 candidates:**

- **L2 · Logic gates and circuits** — AND, OR, NOT implemented in transistors. How boolean algebra becomes physical reality. The connection between the math (discrete logic) and the machine (silicon) is the foundational link in the entire stack.
- **L2 · The von Neumann architecture** — The 1945 design where program and data share the same memory space. Every mainstream computer still follows this model. Understanding it explains why certain classes of bugs and attacks exist.
- **L2 · CPU internals** — Fetch, decode, execute cycle. Registers, the ALU, the clock. What actually happens when your code runs — the mechanical reality behind the abstraction.
- **L2 · Memory hierarchy** — Registers → L1/L2/L3 cache → RAM → disk. Each level is orders of magnitude slower than the one above. Cache behaviour explains many real-world performance anomalies that appear mysterious otherwise.
- **L2 · Assembly language** — The lowest level of human-readable code. Reading assembly demystifies what compilers produce and what the CPU actually sees. Not a skill to use daily — a lens to see through abstractions.
- **L2 · Instruction set architectures** — x86 vs ARM and what that distinction means. The contract between software and hardware. Explains why binaries are not portable across hardware families without recompilation.

---

#### L1-07 · Operating Systems

**What it is and why it matters:** The OS is the intermediary between your code and the hardware. Its design explains why concurrency is hard, why processes are isolated from each other, why system calls are expensive, and why file I/O behaves the way it does. Most performance and reliability decisions in application software trace back to OS behaviour.

**Level 2 candidates:**

- **L2 · Processes and threads** — A process is a running program with its own memory space. A thread is a unit of execution within a process that shares that memory. The origin of most concurrency complexity.
- **L2 · Scheduling** — How the OS decides which process or thread runs next. Round-robin, priority queues, real-time scheduling. Explains latency behaviour under load and why some systems feel unresponsive.
- **L2 · Memory management** — Virtual memory, paging, segmentation. How the OS gives every process the illusion of owning all available memory. The mechanism that makes process isolation possible.
- **L2 · File systems** — How data is organised and persisted on disk. Inodes, directories, journaling. Why file operations have the performance characteristics they do — and why they sometimes don't.
- **L2 · System calls** — The boundary between user code and kernel code. Every network request, file read, and thread spawn crosses this boundary. The cost of crossing it explains many architectural decisions in high-performance systems.
- **L2 · Concurrency primitives** — Mutexes, semaphores, condition variables. The tools for coordinating threads — and the source of deadlocks and race conditions. Understanding the primitives is the prerequisite for reasoning about concurrent correctness.

---

#### L1-08 · Networking

**What it is and why it matters:** Modern software is distributed by default. Understanding the network stack explains latency, explains why protocols are designed the way they are, and explains the failure modes that distributed systems are built to tolerate. Much of what feels like magic in web infrastructure is just layered protocol design.

**Level 2 candidates:**

- **L2 · The OSI and TCP/IP models** — Layered abstractions from physical signals up through application data. Each layer only communicates with the layers immediately adjacent to it. The model is a design principle as much as a description.
- **L2 · IP addressing and routing** — How packets find their way across the internet. BGP, subnets, and why the internet has no central authority or single point of control.
- **L2 · TCP vs UDP** — Reliability and ordering vs speed and simplicity. TCP guarantees delivery at the cost of overhead. UDP is fast and unreliable. The choice shapes every protocol built on top.
- **L2 · DNS** — How domain names resolve to IP addresses. A distributed hierarchical database that underpins the entire internet. Its failure modes are some of the most impactful in infrastructure.
- **L2 · HTTP** — The application protocol the web runs on. Request-response, statelessness, versioning (HTTP/1.1 → 2 → 3). Understanding HTTP explains why REST is designed the way it is.
- **L2 · TLS and encryption in transit** — How secure connections are established. The handshake, certificates, certificate authorities. Why HTTPS is not just HTTP with a cosmetic change.

---

#### L1-09 · Databases

**What it is and why it matters:** Almost all software is ultimately about persisting and retrieving data. The relational model and its alternatives represent decades of accumulated thinking about how to do this correctly and efficiently. Most database misuse in practice traces to not understanding the model underneath the tool.

**Level 2 candidates:**

- **L2 · The relational model** — Codd's 1970 paper. Tables, rows, columns, keys, and the mathematical foundations in set theory and predicate logic. The model is why SQL is declarative — you describe *what*, not *how*.
- **L2 · SQL** — The language of relational databases. Selecting, filtering, joining, aggregating. Understanding query composition rather than just syntax.
- **L2 · Normalisation** — Organising data to eliminate redundancy and prevent update anomalies. 1NF through 3NF. The theory behind why badly designed schemas cause cascading problems.
- **L2 · Indexing** — How databases find rows efficiently. B-trees under the hood. Why the right index transforms a slow query — and why too many indexes harm write performance.
- **L2 · Transactions and ACID** — Atomicity, Consistency, Isolation, Durability. The guarantees a database makes when operations fail mid-way. The foundation of data integrity reasoning.
- **L2 · Query planning** — How the database decides *how* to execute your SQL. Statistics, cost estimation, join strategies. The bridge between writing SQL and writing *fast* SQL.
- **L2 · NoSQL and alternatives** — Document stores, key-value stores, graph databases, column stores. Not replacements for relational — different tradeoffs for different data shapes and access patterns.

---

#### L1-10 · Programming Languages Theory

**What it is and why it matters:** You have used many languages. This is where you understand why they exist, why they differ, and what the design choices actually mean. Languages are not arbitrary — they embed assumptions about what kinds of correctness matter and what kinds of errors are possible.

**Level 2 candidates:**

- **L2 · Syntax and grammars** — How languages are formally defined. Context-free grammars, BNF notation. Why some constructs are syntactically impossible — and why that is a deliberate design choice, not a limitation.
- **L2 · Parsing** — How source code becomes a tree the compiler can reason about. Lexing, tokenising, abstract syntax trees. The mechanics behind every language toolchain.
- **L2 · Type systems** — Static vs dynamic, strong vs weak, structural vs nominal. Types are proofs about program behaviour made at compile time. The tradeoffs explain most serious language design debates.
- **L2 · Compilers vs interpreters** — How source code becomes executable. The compilation pipeline: parse → analyse → optimise → generate. Where the performance of a language is actually decided.
- **L2 · Memory models** — Stack allocation, heap allocation, garbage collection, manual management, ownership (Rust). Each language makes a deliberate choice here with real performance and safety implications.
- **L2 · Functional vs imperative paradigms** — Two fundamentally different ways of expressing computation. Imperative describes *how*; functional describes *what*. Most modern languages borrow from both — understanding each in its pure form clarifies the borrowing.

---

#### L1-11 · Computability and Complexity

**What it is and why it matters:** The deepest theoretical layer. Establishes what computers can and cannot do in principle, and what they can do but not efficiently. Knowing this tells you when to stop looking for a perfect algorithm — and when the problem itself is the reason.

**Level 2 candidates:**

- **L2 · Decidability** — Some problems have no algorithmic solution at all. The halting problem is the canonical example: no program can correctly determine whether every arbitrary program eventually halts. This is a hard mathematical result, not a limitation of current technology.
- **L2 · Complexity classes** — P (solvable in polynomial time), NP (verifiable in polynomial time), and the relationship between them. The P vs NP question is the largest open problem in theoretical CS.
- **L2 · NP-completeness** — A class of problems where a solution to any one of them would solve all of them. Recognising NP-complete problems in the wild tells you when to stop searching for an efficient exact algorithm and start looking at approximations.
- **L2 · Reductions** — Transforming one problem into another to prove hardness. How we establish that a new problem is at least as hard as a known hard problem. The core proof technique in complexity theory.

---

### Group 3 — Year 3–4: Applied and Specialised

---

#### L1-12 · Software Engineering

**What it is and why it matters:** The gap between code that works and software that can be maintained, extended, and reasoned about by a team over years. This domain formalises the hard-won lessons of the industry — most of them discovered by experiencing the consequences of ignoring them.

**Level 2 candidates:**

- **L2 · Design patterns** — Recurring solutions to recurring problems. Gang of Four patterns (factory, observer, strategy, etc.) are a shared vocabulary for design decisions — knowing them lets you name what you're doing and communicate it.
- **L2 · SOLID principles** — Five principles for object-oriented design that make systems easier to change. Each one exists because a specific category of design mistake kept recurring across codebases at scale.
- **L2 · Version control internals** — What Git is actually doing beneath the commands. DAGs of commits, how branching and merging work structurally. Demystifies the tool most developers use daily without fully understanding.
- **L2 · Testing theory** — Unit, integration, end-to-end. TDD as a design discipline rather than just a verification tool. What coverage actually measures — and what it does not.
- **L2 · System design** — How to reason about large systems before building them. Scalability, reliability, and the tradeoffs between them. The discipline behind architectural decision-making.

---

#### L1-13 · Machine Learning and AI

**What it is and why it matters:** Has gone from a specialisation to a near-core competency in the last decade. Understanding the fundamentals separates principled use from cargo-culting — and contextualises the current AI moment within a longer historical arc of advances and setbacks.

**Level 2 candidates:**

- **L2 · Linear algebra foundations** — Vectors, matrices, transformations. The mathematical substrate that neural networks operate on. Without this, the mechanics of ML are a black box.
- **L2 · Statistics and probability** — Distributions, Bayes' theorem, expectation, variance. ML is applied statistics. Without this, you are tuning hyperparameters without understanding what they are doing.
- **L2 · Gradient descent** — The optimisation algorithm that trains neural networks. Understanding it explains why training is slow, why it sometimes fails, and what learning rate actually controls.
- **L2 · Neural network architecture** — Layers, weights, activation functions, forward and backward passes. How a network learns a representation of data from examples.
- **L2 · The historical arc** — Perceptrons in the 1950s, the AI winters of the 1970s and 1980s, the deep learning renaissance after 2012. Understanding why progress stalled and then restarted contextualises the current moment rather than making it feel unprecedented.

---

#### L1-14 · Security

**What it is and why it matters:** Security is not a feature to add — it is a property of how systems are designed. The fundamentals explain why attacks work, which lets you understand what design choices prevent them rather than treating security as a checklist of patches.

**Level 2 candidates:**

- **L2 · Cryptography** — Symmetric vs asymmetric encryption, hashing, digital signatures, key exchange. The mathematical tools that make secure communication possible. Understanding these demystifies most security protocols.
- **L2 · Authentication and authorisation** — Proving identity vs granting permissions. Sessions, tokens, OAuth, JWTs. The distinction is where most security vulnerabilities are introduced.
- **L2 · Common vulnerability classes** — SQL injection, XSS, buffer overflows, CSRF. Each one is a violation of a specific assumption about input boundaries or trust. Understanding the class is more durable than knowing the patch.
- **L2 · Threat modelling** — Reasoning about what an attacker wants, what capabilities they have, and where the system's assumptions are weakest before writing any code.

---

#### L1-15 · Distributed Systems

**What it is and why it matters:** Cloud infrastructure is the default deployment environment. The theoretical foundations of distributed systems explain why they behave unexpectedly — and what guarantees are actually achievable when you cannot rely on a single machine or a synchronised clock.

**Level 2 candidates:**

- **L2 · The CAP theorem** — In a distributed system you can guarantee at most two of: Consistency, Availability, Partition tolerance. The theorem forces explicit tradeoff decisions rather than letting you pretend all three are possible.
- **L2 · Consensus algorithms** — How distributed nodes agree on a value despite failures. Paxos, Raft. The problem that makes distributed systems fundamentally harder than single-machine systems — and why most distributed databases are really consensus problems in disguise.
- **L2 · Eventual consistency** — A weaker consistency model that enables higher availability. Understanding it explains why distributed databases behave differently from relational ones — and when that difference matters.
- **L2 · Clock synchronisation** — There is no global clock in a distributed system. Lamport clocks and vector clocks establish causal ordering without requiring synchronised time. Explains why "what happened first" is a hard question across machines.
- **L2 · Failure modes** — Networks partition, nodes crash, messages arrive out of order or are duplicated. Distributed systems theory is largely the study of how to build reliable systems from unreliable components. Understanding failure modes is the prerequisite for building tolerant ones.

---

## Sequencing note

The dependency chain runs roughly as written. Discrete Mathematics underlies Algorithms and Programming Languages Theory. Computer Architecture underlies Operating Systems. Operating Systems underlies Networking and Distributed Systems. Databases sits relatively independently after the relational model is understood.

For a practitioner returning to foundations, the highest-leverage starting points are typically: **Algorithms** (closes the most gaps in existing intuition), **Operating Systems** (explains the most previously-mysterious behaviour), and **Computability and Complexity** (provides the deepest theoretical grounding for reasoning about what is and is not solvable).
