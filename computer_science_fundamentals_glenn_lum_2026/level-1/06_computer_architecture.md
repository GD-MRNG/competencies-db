## Metadata
- **Date:** 23-05-2026
- **Source:** 06_computer_architecture.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Computer Architecture

Most performance intuition in software is folklore. Developers learn that some operations are fast and others are slow, that certain patterns scale and others don't, that some bugs only show up under load — and they accumulate rules of thumb without ever touching the layer where these rules originate. The rules are not arbitrary. They are consequences of how physical machines are built. Without that layer, you are pattern-matching on outcomes; with it, you are reasoning from causes.

Software feels abstract because the abstractions are good. You write a function, and a chain of translations — compiler, linker, loader, operating system, instruction decoder — eventually causes electrons to move through silicon in a particular pattern. The abstractions are so reliable that you can build entire careers on top of them without looking down. But the abstractions leak. They leak when a loop runs ten times slower than you expected, when a data structure that should be O(1) drags under real workloads, when a system that ran fine on your laptop falls over on production hardware. Every leak is the underlying machine asserting that it is, in fact, still there.

The mental model worth carrying is this: a computer is a physical device that executes a fixed repertoire of simple instructions, very quickly, on data it must first locate. Each part of that sentence matters. The instructions are simple — load this from memory, add these two numbers, jump to this address — and there are only so many of them. They execute very quickly, but "quickly" is relative; some take one cycle, some take hundreds, depending mostly on where the data lives. And locating the data is often the dominant cost, because the gap between "data the CPU has in hand" and "data sitting in main memory" is not small. It is roughly the difference between picking something off your desk and walking down the hall to fetch it.

The bottom of the stack is logic gates: physical circuits that implement boolean operations in hardware. AND, OR, NOT — the same operations you use in if-statements, but realised in transistors. Combine enough of them and you get arithmetic units, memory cells, and eventually a processor. This connection between discrete mathematics and physical silicon is the foundational link that holds the entire field together. Boolean algebra is not a metaphor for circuit design; it is circuit design. Understanding this once removes a layer of magic that never returns.

Above the gates sits the architectural model that almost every mainstream computer follows: program and data share the same memory, and the CPU pulls instructions from that memory one at a time, decodes them, executes them, and moves on. This is the von Neumann architecture, and it dates from 1945. The fetch-decode-execute cycle is the heartbeat of every running program you have ever written. It also explains entire categories of bugs and attacks — buffer overflows that overwrite return addresses work because instructions and data live in the same memory space, and the machine cannot tell them apart without help.

The most consequential thing to internalise is the memory hierarchy. Registers inside the CPU are essentially free to access. L1 cache is a few cycles away. L2 and L3 caches are progressively further. Main memory (RAM) is hundreds of cycles. Disk, even fast disk, is millions. Each level is orders of magnitude slower than the one above it, and the CPU spends a great deal of its design effort guessing what data you will need next so it can have it ready in a fast level when you ask. This is why traversing an array is faster than chasing pointers through a linked list with identical asymptotic complexity: the array is contiguous, so the cache prefetcher wins; the linked list scatters across memory, so every access is a gamble. Most "mysterious" performance differences in production code are this phenomenon in disguise.

Then there is the contract between software and hardware: the instruction set architecture. x86 and ARM are two different contracts, each describing a different repertoire of instructions and a different set of assumptions about how a program is laid out and executed. This is why a binary compiled for one cannot run on the other without recompilation or emulation, and why the recent shift of consumer machines from x86 to ARM is a genuine architectural transition rather than a cosmetic one. Below the instruction set is assembly language — not something you write daily, but something worth being able to read. Reading assembly is how you see what the compiler actually produced, which is often surprising and sometimes the only way to settle a performance argument.

The skill this topic builds is the ability to reason about performance from first principles rather than received wisdom. When you know the memory hierarchy, you stop being surprised by cache effects. When you know the fetch-decode-execute cycle, you stop being surprised by branch mispredictions. When you know that the CPU is a physical device executing a small repertoire of instructions on data it must locate, you stop treating performance as a mystery and start treating it as a consequence. The abstractions above this layer remain useful — that is the point of abstractions — but you can now look through them when you need to. That is the difference between a developer who guesses and one who knows.

## Level 2 candidates

**Logic gates and circuits** — How AND, OR, and NOT are physically realised in transistors and combined into arithmetic and memory units. Worth a deep dive because it is the single bridge between discrete mathematics and physical computation, and seeing it once changes how you think about every layer above.

**The von Neumann architecture** — The 1945 design where instructions and data share the same memory, and the implications of that choice. Worth deeper treatment because it explains a surprising amount of what feels accidental about modern systems, including entire classes of security vulnerabilities.

**CPU internals** — The fetch-decode-execute cycle, registers, the ALU, pipelining, branch prediction. Worth going deeper because the mechanical reality behind "your code runs" is where a lot of performance intuition is either built or remains absent.

**Memory hierarchy** — Registers through L1/L2/L3 cache through RAM through disk, and the orders-of-magnitude gaps between them. The single highest-leverage deep dive in this topic, because cache behaviour explains more real-world performance anomalies than any other single concept.

**Assembly language** — The lowest level of human-readable code and what it reveals about what compilers actually do. Worth a deeper look not as a daily skill but as a diagnostic lens — being able to read assembly is how you settle questions the higher layers cannot answer.

**Instruction set architectures** — x86 versus ARM as two different contracts between software and hardware, and what that distinction actually means. Worth depth because the industry is in the middle of a real ISA transition, and understanding the contract clarifies what is and is not portable.

---
