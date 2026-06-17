# Terminals, Shells & the OS Underneath — Level 0: Course Map

> **Intent:** "The terminal" is not one thing — it's at minimum three separate programs (a terminal emulator, a shell, and the OS kernel underneath both) that have been visually fused into a single black rectangle for fifty years. A practitioner studies this not to learn more commands, but to dissolve that fusion: once you can see which of the three layers is responsible for a given behavior, things that look like inconsistent magic — why `cd` can't be a normal program, why a pipe between two commands runs them *simultaneously*, why closing a window can silently kill a long-running job, why the same command behaves differently on Linux vs macOS vs Windows — become predictable consequences of a small, stable set of mechanisms.
>
> **Your angle:** You already know how to *operate* a terminal; what's missing is the causal model underneath the commands you've memorized. Because you work across Linux, macOS, and Windows, the highest-leverage move is to learn the layered architecture first — terminal emulator → shell → OS/kernel — as a structure that's *substantially the same shape* on all three, then treat OS-specific differences (and Windows' genuinely different lineage) as variations on that shape rather than three unrelated systems to memorize separately. Once the layers are distinct in your head, "memorizing lines" turns into "deriving lines," because most commands are just a thin, guessable syntax over one of a handful of underlying OS mechanisms.

---

## How to use this map

This is Level 0: a map of the domain, not a tutorial. Each Level 1 topic is a node worth a few hours to a few days of focused attention. The "Level 2 candidates" under each one preview what you'd find if you descended further, so you can judge relevance before opening them.

Descend into a Level 1 topic when a real moment of confusion traces back to it — or proactively, following the Sequencing Note below, when a topic is foundational enough that understanding it in advance will collapse several future confusions at once. A Level 2 descent should produce a focused explainer or hands-on exercise on just that sub-concept, not a re-tour of the whole parent topic.

---

## Topic Inventory

### Group 1: The Three Layers (what you're actually looking at)

#### L1-01 · The Terminal Emulator
The thing you open and see — Terminal.app, Windows Terminal, iTerm2, GNOME Terminal, Alacritty — is just a program that draws text and forwards your keystrokes; it has no idea what `ls` or `git` mean and never executes a command itself. This layer exists because, decades ago, "terminals" were literal physical devices (teletypes, then video terminals like the DEC VT100) wired to a remote computer, and when personal computers no longer had real terminals attached, software had to *emulate* one — hence "terminal emulator," a name that's a historical fossil still describing exactly what the program does. Understanding that this layer is "just a text-rendering and input-forwarding program" is what explains why terminal emulators can have wildly different fonts, color schemes, and tab features, while the commands you type inside them behave identically: the emulator isn't involved in running anything, it's just the window.

**Level 2 candidates:**
- **Physical teletypes and the VT100 legacy** — explains why so much terminal behavior (escape codes, 80-column assumptions, "TTY" terminology) traces back to hardware that hasn't existed in production for decades.
- **Pseudo-terminals (PTYs)** — explains the kernel-level trick that lets a software emulator pretend to be a real hardware terminal, which is the actual mechanism that connects layer 1 to layer 2.
- **Escape sequences and ANSI codes** — explains how colored text, cursor movement, and progress bars work: the shell isn't drawing pixels, it's sending special byte sequences the emulator interprets as drawing instructions.
- **Why copy-paste, scrollback, and fonts differ across emulators** — explains why these are emulator features, not shell or OS features, and why changing emulators changes none of your actual command behavior.
- **Multiplexers (tmux, screen)** — explains how a session can survive the emulator window closing, by inserting another layer that detaches the running programs from any single terminal window.

#### L1-02 · The Shell
The shell — bash, zsh, fish, PowerShell — is the actual program that reads what you type, interprets it as a command, and asks the OS to do something. This is the layer most "command memorization" actually lives in, and it's also where most of the *inconsistency* you've felt comes from: bash, zsh, and PowerShell are genuinely different programs with different syntax, different scripting languages, and different philosophies (Unix shells assume "everything is text"; PowerShell, designed decades later, assumes "everything is a structured object"), even though they're all sitting in the same architectural slot. Once the shell is its own distinct layer in your head, "why does this work in bash but not PowerShell" stops being a mystery and becomes an expected consequence of using two different programs that happen to look similar.

**Level 2 candidates:**
- **REPL loop (read–eval–print)** — explains the shell's actual job in one sentence: read a line, figure out what program(s) it names, run them, print the result, repeat — which is the loop every other shell concept attaches to.
- **Built-ins vs external commands** — explains why `cd`, `export`, and `alias` can't be separate programs (a separate process can't change *your* shell's directory or environment) while `ls` and `grep` can be and are.
- **Shell scripting as a real programming language** — explains why `.sh` files have variables, loops, and conditionals: the shell is an interpreter, and the interactive prompt is just that same interpreter running one line at a time.
- **PowerShell's object pipeline vs Unix's text pipeline** — explains the deepest cross-platform divergence in this entire map: why piping in PowerShell passes structured .NET objects while Unix pipes pass raw bytes, and why that makes naive command translation between them misleading.
- **Shell configuration files (`.bashrc`, `.zshrc`, profile scripts)** — explains why a command works in one terminal tab but not another, or after a reboot but not before: these files run at specific lifecycle moments (login vs interactive) that determine what's actually loaded.
- **Why there are so many shells** — explains the lineage (sh → csh → bash → zsh → fish) as a history of incremental feature wars, not arbitrary proliferation.

#### L1-03 · The Operating System / Kernel
Beneath the shell is the actual OS kernel — the thing that owns the hardware, schedules what runs when, and enforces every permission boundary. The shell doesn't "run" your programs in any deep sense; it asks the kernel to do it, via system calls, and the kernel is the only thing actually capable of creating a process, opening a file, or allocating memory. This is the layer where the real cross-platform divergence lives: Linux and macOS both descend from Unix and share a kernel-level vocabulary (processes, file descriptors, permissions, signals), while Windows' kernel has a genuinely different lineage and a different native vocabulary — which is *why* so many commands and concepts don't map 1:1, no matter how good the translation layer (WSL, Cygwin, PowerShell) gets.

**Level 2 candidates:**
- **System calls** — explains the actual boundary between "asking" and "doing": every shell command that touches a file, starts a program, or reads input is, underneath, a request across this boundary.
- **The Unix lineage (Linux & macOS) vs Windows NT lineage** — explains why Linux and macOS commands feel like dialects of the same language while Windows feels foreign, and why that's a real historical fact (Unix, 1969; Windows NT, designed independently in the early 1990s) rather than a stylistic accident.
- **The kernel as the only thing with hardware access** — explains why "permission denied" exists at all: the kernel is the sole gatekeeper, and everything above it (your shell, your terminal, your programs) must ask.
- **WSL and POSIX-compatibility layers** — explains what's actually happening when Windows runs "Linux" commands: either a real Linux kernel running alongside (WSL2) or a translation layer reimplementing Unix calls on top of Windows (older Cygwin/WSL1 approach), and why the distinction matters for performance and edge cases.
- **The filesystem as a kernel-managed abstraction** — explains why "a file" looks the same from any program, even though the actual bytes might be on an SSD, a network share, or not really "a file" at all (like `/proc` on Linux).

---

### Group 2: Processes (what "running a program" actually means)

#### L1-04 · Processes, PIDs, and the Process Tree
A "process" is the OS's bookkeeping object for a running program — memory, open files, and execution state, all tracked under a single number (the PID). Every command you run spawns at least one process, and the shell itself is a process too, which is the detail that explains the entire parent-child structure of everything happening on your machine at any moment: your terminal emulator is a process, running a shell process, running whatever command process you just typed, in a strict tree. This is the concept that makes `ps`, Task Manager, Activity Monitor, and `top` all legible as three different windows onto the exact same underlying structure, and explains why killing a parent process can take its children down with it.

**Level 2 candidates:**
- **`fork` and `exec` (Unix) vs `CreateProcess` (Windows)** — explains the actual mechanism of "running a program": Unix clones the current process then replaces its memory with the new program, a two-step model with real historical reasons, while Windows does it in one step — which is why some cross-platform tools behave subtly differently under the hood.
- **Parent/child process relationships** — explains orphaned and zombie processes, and why a crashed parent can leave children running with nothing managing them.
- **Foreground vs background jobs (`&`, `fg`, `bg`)** — explains what's actually happening when you background a job: the shell stops waiting for that child process to finish before giving you the prompt back.
- **Environment variables and inheritance** — explains why a child process sees the variables you `export`ed but not ones you merely set, because inheritance happens at process-creation time via a copied environment block.
- **Process states (running, sleeping, stopped, zombie)** — explains the cryptic single-letter codes in `ps`/`top` output as a real, small state machine, not noise.

#### L1-05 · Standard Streams and Redirection
Every process is handed three open "files" the instant it starts — standard input, standard output, standard error — and almost everything that looks like terminal magic (`>`, `<`, `2>`, `|`) is just the shell rewiring which actual file or process is sitting on the other end of one of those three streams before the program even starts. This is arguably the single highest-leverage concept in the entire map for someone who feels like the terminal is a black box, because once you see redirection as "the shell plugs a different file/process into slot 0, 1, or 2," the entire family of `>`, `>>`, `<`, `2>`, `2>&1`, and `|` syntax becomes derivable from one idea instead of five memorized symbols.

**Level 2 candidates:**
- **stdin/stdout/stderr as numbered file descriptors (0, 1, 2)** — explains the exact thing redirection syntax is manipulating, and why `2>` specifically means "redirect stream number 2."
- **Pipes (`|`) as simultaneous process connection** — explains why `cmd1 | cmd2` runs both commands *at the same time*, streaming output to input, rather than running one fully before the other starts.
- **Output vs append redirection (`>` vs `>>`)** — explains the easily-forgotten but consequential difference between overwriting and appending, and why one has destroyed someone's file at some point in every engineer's career.
- **Redirecting stderr separately from stdout** — explains why some error messages "don't show up" in a redirected log file: they were never going to stream 1 in the first place.
- **Here-documents and here-strings** — explains a less common but useful pattern for feeding multi-line input to a command without a separate file.

#### L1-06 · Signals and Process Control
Signals are the OS's mechanism for interrupting a running process asynchronously — Ctrl+C doesn't "type" anything into the program, it asks the kernel to deliver a specific signal (SIGINT) to the foreground process, which by default terminates it but which a program can choose to intercept and handle differently. This is the concept that explains why Ctrl+C sometimes does nothing (the program is ignoring or has overridden that signal), why `kill` doesn't necessarily mean "force quit" (it's "send a signal," and the default signal is a polite request, not a command), and why some processes need `kill -9` specifically to actually die.

**Level 2 candidates:**
- **SIGINT, SIGTERM, SIGKILL** — explains the actual difference between Ctrl+C, a polite `kill`, and an unstoppable `kill -9`, and why only one of the three can't be intercepted or ignored by the target process.
- **Signal handlers** — explains how well-behaved programs catch SIGTERM to clean up before exiting, which is the entire basis of "graceful shutdown" in servers and containers.
- **Ctrl+C vs Ctrl+Z vs Ctrl+D** — explains three visually similar keystrokes as three completely different mechanisms: interrupt, suspend-to-background, and end-of-input.
- **Windows' different signal model** — explains why Windows console applications historically handled interruption differently (console control events rather than POSIX signals), and why this is one of the genuine cross-platform seams.

---

### Group 3: The Filesystem and Permissions (what the OS is actually protecting)

#### L1-07 · The Filesystem Hierarchy and Paths
What looks like "folders and files" is a tree-shaped namespace the kernel exposes uniformly, and the differences you've felt between operating systems here are real but narrower than they look: Linux and macOS share a single-rooted tree (`/`) where even other disks get *mounted into* that one tree, while Windows uses a separate-letter-per-drive model (`C:`, `D:`) for historical reasons dating to DOS. Understanding paths as "instructions for walking this tree" — rather than memorizing specific path strings — is what makes absolute vs relative paths, `..`, `~`, and environment-variable-based paths (`$PATH`, `%PATH%`) click as one coherent idea instead of separate syntax to memorize per OS.

**Level 2 candidates:**
- **Absolute vs relative paths** — explains why the same command can succeed or fail purely based on your current working directory, which is itself just a piece of state every process carries.
- **The single-root tree (Unix) vs drive letters (Windows)** — explains the most visible cross-platform filesystem difference, and the historical reason (DOS's FAT filesystem design) Windows still carries it forward.
- **Mounting** — explains how Unix-like systems make an entirely separate disk, network share, or even virtual device appear as just another directory in the one tree, which is the same mechanism WSL uses to expose Windows drives inside Linux.
- **`$PATH` / `%PATH%` and command resolution** — explains exactly how the shell decides what program `git` or `python` even refers to, and why "command not found" is really "not found in any directory listed here."
- **Special/virtual filesystems (`/proc`, `/dev`)** — explains how Unix-like systems expose live kernel state (running processes, hardware devices) *as if* they were ordinary files, which is a deliberate, elegant design choice rather than a quirk.

#### L1-08 · Permissions and Ownership
Every file and process exists under a permission model that determines who can read, write, or execute it — and this is the layer responsible for "permission denied," `sudo`, and why some commands need elevation while others don't. Unix-style permissions (owner/group/other, read/write/execute) are a relatively simple, decades-old model that Linux and macOS share almost exactly; Windows' permission model (ACLs — access control lists) is more granular and was designed independently, which is the real reason permission errors and `sudo`-equivalents (`runas`, UAC prompts) feel unfamiliar when you cross between the two worlds.

**Level 2 candidates:**
- **Owner/group/other and read/write/execute bits** — explains the `rwxr-xr-x`-style strings you've seen and ignored, and what each position actually controls.
- **`chmod` and `chown`** — explains how to deliberately change the permission state you can currently only read, turning permissions from a wall into a tool.
- **`sudo` and privilege elevation** — explains what's actually happening when you elevate: you're not bypassing permissions, you're temporarily running as a different, more privileged user (root).
- **Windows ACLs and UAC** — explains the more granular but differently-shaped Windows model, and why "Run as Administrator" is a conceptual cousin of `sudo`, not the same mechanism.
- **Executable permission vs file type** — explains why a `.sh` file with the wrong permission bit fails to run even though "it's clearly a script," a classic confusion rooted in Unix not caring about file extensions at all.

---

### Group 4: Putting It Together (the parts that make it feel less like a black box)

#### L1-09 · Environment and Configuration
"Why does this work on my machine but not yours" and "why did this work yesterday but not today" overwhelmingly trace back to environment state — variables, `$PATH` entries, shell configuration files — that's invisible unless you go looking for it. This topic is really the practical synthesis of L1-02 (shell) and L1-04 (processes): environment variables are inherited at process-creation time, set by configuration files that run at specific, orderable moments, which is why two terminal tabs, a script run directly, and the same script run via cron can all see different environments despite "the same machine."

**Level 2 candidates:**
- **Variable scope and inheritance** — explains why setting a variable in one terminal tab doesn't affect another, since each shell process has its own copy, inherited only downward to children.
- **Login shells vs interactive non-login shells** — explains why `.bash_profile`/`.bashrc` (or their zsh equivalents) load in some contexts and not others, which is the direct cause of "it works when I open a new terminal but not in this script."
- **`$PATH` ordering and shadowing** — explains why you sometimes run "the wrong" version of a tool (an old Python, a different git) purely because of directory order in `$PATH`.
- **Cross-platform environment differences** — explains why a script with hardcoded environment assumptions breaks the instant it crosses from macOS/Linux to Windows or vice versa.
- **Dotfiles as portable configuration** — explains why engineers version-control their shell configs, treating environment setup as code rather than one-off manual tweaks.

#### L1-10 · Terminal Multiplexing, Remote Sessions, and SSH
Once you understand that the terminal emulator, shell, and OS are separable layers, remote work stops being mysterious: SSH connects your local terminal emulator to a *shell running on a different machine's kernel entirely*, with your local emulator doing nothing but display and input-forwarding the whole time. This is the topic that finally explains why closing your laptop can kill a remote session (the local emulator/connection died, taking the remote shell's controlling terminal with it) and why tools like `tmux`/`screen` or `nohup` exist specifically to detach a running process from that fragile connection.

**Level 2 candidates:**
- **SSH as a remote shell, not a remote desktop** — explains exactly what crosses the network (keystrokes and text output) versus what doesn't (no GUI, no filesystem access unless separately configured).
- **Controlling terminals and session death** — explains why a disconnected SSH session can kill every process that was depending on it, tying directly back to signals (L1-06) and process trees (L1-04).
- **`nohup` and `disown`** — explains the specific mechanisms for telling a process "don't die just because my terminal did," as a lighter alternative to a full multiplexer.
- **Persistent sessions via tmux/screen** — revisits L1-01's multiplexer concept specifically in the remote-work context, where it solves a real, recurring problem rather than being a nice-to-have.

#### L1-11 · Where the Three Platforms Actually Diverge
This topic exists to consolidate every cross-platform seam mentioned piecemeal above into one deliberate comparison, because the goal of this whole map is to stop you from treating Linux, macOS, and Windows as three unrelated skill sets. The honest answer is that Linux and macOS diverge from Windows far more than they diverge from each other — both being Unix descendants sharing kernel vocabulary, permission models, and shell lineage — while Windows' differences are real, structural, and rooted in an entirely separate 1990s design lineage (NT), not a deficiency or a stylistic choice.

**Level 2 candidates:**
- **Shared Unix ancestry of Linux and macOS** — explains why so much of this map "just works" identically on both, down to shell choice and permission bits.
- **Windows NT's independent lineage** — explains why Windows isn't "Unix done differently" but a genuinely separate design tradition, which reframes its differences as foreign rather than wrong.
- **PowerShell's object-oriented pipeline as a deliberate alternative philosophy** — revisits L1-02's deepest point specifically as a designed response to Unix's text-pipe model's limitations, not an accident of history.
- **WSL as a deliberate bridge, not a true merge** — explains what WSL actually buys you (a real or near-real Linux kernel environment) versus what it doesn't (it's still a guest inside a fundamentally Windows NT host).
- **Why "it works in bash" doesn't mean "it works in PowerShell"** — ties the whole comparison back to something you've certainly experienced directly, now explainable in terms of every layer above.

---

## Sequencing note

The dependency shape here is a deliberate "three layers, then two cross-cutting mechanisms" structure. **Group 1 (L1-01 → L1-02 → L1-03) is the true prerequisite for everything else**, because its entire purpose is to pull apart a thing your brain has been treating as one black box into three distinct programs with three distinct responsibilities. Skipping straight to processes or permissions without first installing that three-layer separation means you'll keep attributing one layer's behavior to another — which is exactly the pattern that produces "I don't understand why this works" even when you can recite the command.

Once Group 1 is in place, **Group 2 (processes, streams, signals) and Group 3 (filesystem, permissions) are siblings, not a strict chain** — both depend on L1-03 (the kernel) but not meaningfully on each other, so you can tackle whichever one is biting you more in real work first. That said, **L1-05 (standard streams and redirection) is the single highest-leverage topic in the entire map for someone describing your exact symptom** ("memorizing lines, want to stop"): an enormous fraction of shell syntax you've memorized as separate symbols (`>`, `>>`, `<`, `|`, `2>&1`) collapses into one idea — rewiring numbered file descriptors — the moment this topic lands, so it's worth pulling forward even ahead of some of Group 2.

Group 4 is explicitly the synthesis layer: **L1-09 (environment) is what most directly resolves "why did this work yesterday/elsewhere and not now,"** and depends on having both the shell (L1-02) and process (L1-04) layers in place first. L1-10 (remote sessions) is a satisfying but optional payoff topic — it doesn't unlock anything else, but it's where the layered model you've built finally explains something that felt genuinely magical (a closed laptop killing a remote job) in one clean causal chain. **L1-11 should be read last, deliberately** — it's designed as a capstone that re-collects every small cross-platform aside scattered through the earlier topics into one explicit comparison, which only lands once the individual pieces it's referencing are already familiar.

**Highest-leverage entry point for you specifically:** L1-01 → L1-02 → L1-03 to install the three-layer separation, then immediately to L1-05 (streams/redirection) before anything else in Groups 2–3, since that's the fastest route from "memorizing lines" to "deriving lines" given what you've described. Save L1-11 for the end as a deliberate, satisfying close, once Linux, macOS, and Windows have stopped being three separate memorized rulebooks and started being one model with a few well-understood seams.