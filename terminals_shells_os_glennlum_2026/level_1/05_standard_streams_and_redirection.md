## Metadata
- **Date:** 25-06-2026
- **Source:** 05_standard_streams_and_redirection.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-05 · Standard Streams and Redirection

There is a particular flavor of terminal frustration that comes from staring at a line like `command 2>&1 | tee log.txt` and feeling that you are looking at a small piece of cipher. You know it works. You can copy it. You may even have written variations of it. But the symbols feel arbitrary — five or six distinct pieces of syntax that you have memorized individually, each with its own rule about what goes on which side of what arrow. This is the wrong number of ideas to be holding. The actual number is one.

Every process the operating system creates is handed three open connections the instant it starts running, before a single line of its own code executes. These connections are called standard input, standard output, and standard error, and the kernel refers to them internally by the numbers 0, 1, and 2. A process reads from stream 0 when it wants input, writes its normal results to stream 1, and writes its complaints — error messages, warnings, diagnostics — to stream 2. That separation is deliberate: it exists precisely so you can capture a program's real output without also capturing its grumbling, or vice versa. From the program's perspective, these three streams are just there, the way a newborn human has lungs already attached to air; the program does not open them, request them, or even know where they go.

This is the crucial move: the program does not know where they go. By default, when you run a command interactively, all three streams happen to be connected to your terminal — input comes from your keyboard, output and errors both appear on your screen. But the program has no idea that this is the case. It is writing to slot 1 and slot 2, and slot 1 and slot 2 happen, at this moment, to point at your terminal. They could just as easily point somewhere else, and the program would never notice the difference.

The shell is what controls where those slots point. Every piece of redirection syntax you have ever seen is the shell, before launching your command, reaching in and rewiring one of those three numbered slots to point at something other than the terminal. That is the entire idea. When you write `command > file.txt`, the shell is saying: before you start this command, take slot 1 and point it at this file instead of the screen. The command runs identically to how it always runs — it writes to slot 1 — except now slot 1 happens to be a file. When you write `command < input.txt`, the shell points slot 0 at a file instead of the keyboard. When you write `command 2> errors.log`, the shell points slot 2, specifically, at a file, leaving slot 1 alone — which is why "the errors went to the file but the normal output still printed to my screen" is exactly the behavior you should expect, not a quirk.

Once you see this, the rest of the family falls out of it. The double-arrow `>>` is the same rewiring, except the file is opened in append mode instead of overwrite mode — same idea, one flag different, and the reason a misplaced single `>` has destroyed someone's carefully accumulated log file at least once in every engineer's career. The construction `2>&1` looks cryptic until you read it as "point slot 2 at whatever slot 1 is currently pointing at," at which point it is just slot-rewiring with a slightly more verbose target. There is no special "merge errors into output" feature in the shell; there is just the same rewiring operation, applied between two slots instead of between a slot and a file.

The pipe is the same idea taken one step further, and it is the most quietly powerful version. When you write `cmd1 | cmd2`, the shell starts both commands at the same time, and rewires cmd1's slot 1 to feed directly into cmd2's slot 0. There is no temporary file in between, no "first one finishes, then the other starts" — they run concurrently, with cmd1's output streaming into cmd2's input as it is produced. This is why piping the output of a slow-running command into `grep` shows you matches as they arrive, rather than after the slow command completes: there is nothing buffering the whole thing, just two processes wired together at their stream endpoints, running side by side.

The practical consequence is that you stop memorizing redirection syntax and start deriving it. You no longer need to remember whether `2>` means "redirect errors" or "append errors" or "merge errors" — you just need to remember that 2 is the error stream's number, `>` is rewire-to-file, `>>` is rewire-to-file-in-append-mode, and `&` in this context means "rewire to another slot rather than to a file." Every combination you will ever need is built from those pieces. The next time you see something like `command > out.log 2>&1 < input.txt`, you should be able to read it left-to-right as three independent rewirings of three independent slots, performed by the shell before the command ever runs — and the command itself, sitting at the center of all of this, simply doing what it always does: reading from 0, writing to 1, complaining to 2, blissfully unaware that any of this happened.

## Level 2 candidates

**stdin/stdout/stderr as numbered file descriptors (0, 1, 2)** — Covers the precise mechanism by which the kernel tracks open files and streams per process, and what a file descriptor actually is at the OS level. Worth deepening because it connects redirection to a broader kernel concept (the per-process file descriptor table) that also underlies sockets, pipes, and how programs like `lsof` work.

**Pipes as simultaneous process connection** — Covers the fact that `cmd1 | cmd2` runs both processes concurrently with a kernel-managed buffer between them, not sequentially. Worth deepening because the "concurrent, streaming" nature has real consequences — backpressure, broken-pipe errors, why `head` on a huge stream finishes instantly — that the Level 1 framing only gestures at.

**Output vs append redirection (`>` vs `>>`)** — Covers the difference between truncate-on-open and append-on-open semantics for redirected files. Worth deepening mostly as a focused cautionary explainer with concrete failure modes, since the asymmetry between the two is small in syntax and large in consequence.

**Redirecting stderr separately from stdout** — Covers the practical patterns for capturing errors to one place, output to another, or merging them, including the order-sensitivity of constructions like `> out 2>&1` versus `2>&1 > out`. Worth deepening because the ordering trap genuinely surprises people who think they understand redirection, and the explanation requires thinking carefully about when each rewiring happens.

**Here-documents and here-strings** — Covers the `<<` and `<<<` syntax for feeding inline multi-line or single-line input to a command's stdin without a separate file. Worth deepening as a self-contained pattern that is useful, somewhat less commonly understood, and a natural extension of the "slot 0 can be rewired to anything" idea into "anything" including a literal block of text in your script.

---

## Original Content

#### L1-05 · Standard Streams and Redirection
Every process is handed three open "files" the instant it starts — standard input, standard output, standard error — and almost everything that looks like terminal magic (`>`, `<`, `2>`, `|`) is just the shell rewiring which actual file or process is sitting on the other end of one of those three streams before the program even starts. This is arguably the single highest-leverage concept in the entire map for someone who feels like the terminal is a black box, because once you see redirection as "the shell plugs a different file/process into slot 0, 1, or 2," the entire family of `>`, `>>`, `<`, `2>`, `2>&1`, and `|` syntax becomes derivable from one idea instead of five memorized symbols.