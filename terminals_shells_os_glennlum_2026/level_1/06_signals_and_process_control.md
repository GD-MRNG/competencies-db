## Metadata
- **Date:** 25-06-2026
- **Source:** 06_signals_and_process_control.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-06 · Signals and Process Control

Ctrl+C is not a keystroke that the program receives. This is the single fact that, once it lands, rearranges everything you thought you knew about interrupting, killing, and quitting programs from the terminal. When you press Ctrl+C, no character is typed into the running program's input. Instead, the kernel notices the keystroke, looks up which process is currently in the foreground of your terminal, and delivers a small, numbered message to it — a signal — saying, in effect, "you've been asked to stop." Whether the program actually stops is a separate question entirely, and the answer is up to the program.

This is what signals are: the operating system's mechanism for interrupting a running process asynchronously, from the outside, while it's in the middle of doing something else. They are not function calls, not input, not messages on a queue the program chose to listen on. They arrive whenever the kernel decides to deliver them, and the running program's normal flow of execution is suspended so the signal can be handled. Every signal has a number and a name (SIGINT, SIGTERM, SIGKILL, SIGHUP, and so on), and each one carries a default behavior the kernel will apply if the program hasn't said otherwise — usually "terminate," sometimes "ignore," sometimes "stop." The program, however, can override almost all of these defaults by installing a signal handler: a small piece of code that runs when that specific signal arrives, deciding what to do instead of dying.

Almost everything else about process control follows from this. Ctrl+C sends SIGINT (interrupt). The `kill` command, despite its name, doesn't kill anything — it sends a signal, and the default signal it sends is SIGTERM (terminate), which is a polite request: "please shut down, at your convenience." A well-behaved program receiving SIGTERM will catch it, flush its buffers, close its files, perhaps tell its children to wind down, and then exit cleanly. This is the entire basis of graceful shutdown in servers, databases, and containers — when Kubernetes or systemd stops a service, it sends SIGTERM first, waits, and only escalates if the process refuses to leave.

The escalation is SIGKILL, conventionally invoked as `kill -9`. SIGKILL is the one signal a program cannot catch, cannot ignore, and cannot handle. The kernel doesn't even deliver it to the program in the usual sense; it simply removes the process from existence. This is why `kill -9` always works, and also why it is the wrong tool in almost every case where SIGTERM would have sufficed — the program gets no chance to clean up, save state, or release resources. Reaching for `-9` first is the process-control equivalent of unplugging the machine to close a document.

Once you have this model, several pieces of terminal behavior that looked like quirks become predictable. Ctrl+C doing nothing isn't a bug; it's a program that has installed a SIGINT handler and chosen to ignore or repurpose the signal — common in shells themselves (which need Ctrl+C to interrupt the running command, not exit the shell) and in programs that need to confirm exits or finish a critical section first. A long-running script that won't die to repeated Ctrl+C presses, but does die to `kill` from another terminal, is telling you the same thing from the other side: it's handling SIGINT but not SIGTERM. A program that survives even `kill` and requires `kill -9` is one whose SIGTERM handler is stuck, blocked, or buggy — it intended to be polite, but it's wedged.

Ctrl+C, Ctrl+Z, and Ctrl+D, which look like a family, are actually three completely different mechanisms hiding under similar keystrokes. Ctrl+C sends SIGINT, asking the process to stop. Ctrl+Z sends SIGTSTP, asking the kernel to suspend the process — freeze it in place, return you to the shell prompt, leave it parked for later resumption with `fg` or `bg`. Ctrl+D isn't a signal at all; it's an end-of-file marker on standard input, which most programs interpret as "no more input is coming" and respond to by exiting. Three near-identical keystrokes, three entirely different layers of the system being poked.

There is one more piece of this worth keeping in your model from the start: this whole framework is a Unix framework. Linux and macOS share it almost exactly. Windows, with its independent NT lineage, historically used a different mechanism (console control events) for the same kinds of interruptions, and its native model for stopping processes doesn't map one-to-one onto POSIX signals — which is why cross-platform tools, container runtimes, and language runtimes often have to do real work to make "Ctrl+C does the right thing" behave consistently everywhere.

The practical skill this topic builds is the ability to stop reading "kill" as "destroy" and start reading it as "send a signal" — at which point `kill -TERM`, `kill -HUP`, `kill -9`, and Ctrl+C all line up as the same verb with different arguments, aimed at the same small, well-defined kernel mechanism. The question stops being "how do I make this program die" and becomes "which signal do I send, and is the program set up to handle it?" That's the shift.

## Level 2 candidates

**SIGINT, SIGTERM, SIGKILL** — Covers the concrete differences between the three most common signals: what each one means by default, which can be caught or ignored, and the conventional escalation path from polite request to unstoppable termination. Worth going deeper because the contrast between SIGTERM (catchable, the basis of graceful shutdown) and SIGKILL (uncatchable, the nuclear option) is the single most operationally relevant distinction in this entire topic, and it's the one engineers most often get wrong by reaching for `-9` reflexively.

**Signal handlers** — Covers how a program installs code to run when a specific signal arrives, and the constraints on what that code can safely do (signals interrupt arbitrary execution, so handlers must be reentrant-safe). Worth going deeper because this is the mechanism behind every "graceful shutdown" implementation in real systems — web servers draining connections, databases flushing writes, containers responding to orchestrator stop commands — and writing one correctly is subtler than it looks.

**Ctrl+C vs Ctrl+Z vs Ctrl+D** — Covers three visually similar keystrokes that touch three entirely different mechanisms: signal delivery (SIGINT), process suspension (SIGTSTP), and end-of-input marking (EOF on stdin). Worth going deeper because conflating these is one of the most common sources of terminal confusion, and separating them cleanly also pulls in job control (`fg`, `bg`, `jobs`) as a natural extension.

**Windows' different signal model** — Covers how Windows console applications historically handled interruption through console control events rather than POSIX signals, and how modern cross-platform runtimes paper over the difference. Worth going deeper because this is one of the genuine cross-platform seams where the Unix model and the NT model don't align, and understanding the actual mechanism explains why "Ctrl+C handling" behaves subtly differently in Node, Python, or .NET programs depending on the host OS.

**SIGHUP and the controlling terminal** — Covers the signal sent to processes when their controlling terminal goes away, which is the actual mechanism behind "closing my SSH session killed my long-running job." Worth going deeper because it's the direct bridge from this topic to L1-10 (remote sessions) and explains why `nohup`, `disown`, and terminal multiplexers exist as solutions to one specific signal-delivery problem.

---

## Original Content

#### L1-06 · Signals and Process Control
Signals are the OS's mechanism for interrupting a running process asynchronously — Ctrl+C doesn't "type" anything into the program, it asks the kernel to deliver a specific signal (SIGINT) to the foreground process, which by default terminates it but which a program can choose to intercept and handle differently. This is the concept that explains why Ctrl+C sometimes does nothing (the program is ignoring or has overridden that signal), why `kill` doesn't necessarily mean "force quit" (it's "send a signal," and the default signal is a polite request, not a command), and why some processes need `kill -9` specifically to actually die.