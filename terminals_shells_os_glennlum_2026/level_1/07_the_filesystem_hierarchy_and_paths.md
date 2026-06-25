## Metadata
- **Date:** 25-06-2026
- **Source:** 07_the_filesystem_hierarchy_and_paths.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-07 · The Filesystem Hierarchy and Paths

The fastest way to stop memorizing paths is to stop thinking about paths at all and start thinking about the tree they describe. What your operating system calls "folders and files" is a single tree-shaped namespace — a hierarchy of named nodes — that the kernel exposes to every program that asks. A path is not a thing in itself; it is an instruction for walking that tree from some starting point to some destination. Once you internalize that, most of the syntax you've been memorizing per-OS (`..`, `~`, `/`, `C:\`, `$PATH`, `%PATH%`) collapses into variations on one idea: where do I start, and which branches do I take from there.

The tree is kernel-managed, not shell-managed, and that detail matters more than it sounds. Your shell does not own the filesystem; it just hands path strings to the kernel and the kernel does the walking. This is why the same tree looks identical from your shell, your editor, your text-mode `ls`, and your graphical file browser — they're all asking the same authority the same questions. It's also why a "file" doesn't have to be a real blob of bytes on a disk to behave like one: as long as the kernel agrees to answer questions about a name in the tree, every program above sees a file. Linux's `/proc` and `/dev` are the cleanest example — running processes and hardware devices appear as ordinary-looking files because the kernel decided to expose them that way.

The most visible cross-platform difference here is also the narrowest. Linux and macOS share a single-rooted tree: there is exactly one root, written `/`, and everything else — every disk, every USB stick, every network share — gets mounted into that one tree as a subdirectory. A second hard drive isn't a separate world; it's a branch you reach by walking through, say, `/mnt/data` or `/Volumes/Backup`. Windows, by contrast, gives each drive its own root letter (`C:\`, `D:\`, `E:\`), a model it inherited from DOS, which inherited it from the assumption that you'd be swapping floppy disks. The two models look very different on the surface, but the underlying idea — a tree you walk — is the same; Windows just has a small forest of trees instead of one.

Paths come in two flavors, and the distinction is the single most useful thing to get right. An absolute path starts at the root (`/etc/hosts`, `C:\Windows\System32`) and gives complete walking instructions from a fixed, universal starting point — it means the same thing no matter where you are. A relative path (`config.json`, `../src/main.py`) starts wherever you currently are and walks from there. "Wherever you are" is a real piece of state called the current working directory, and every process carries its own. This is why the same command can succeed in one terminal tab and fail in another: not because the command is broken, but because the two shells are standing in different places in the tree, and the relative path means different things from each spot. `..` means "up one level" and `~` means "your home directory" — both are just shorthand expansions the shell performs before handing the result to the kernel.

`$PATH` (and Windows' `%PATH%`) is the same idea applied to one specific question: when you type `git` or `python`, which file in the tree do you actually mean? The shell doesn't guess. It walks a list of directories — the ones named in `$PATH`, in order — and runs the first matching executable it finds. "Command not found" is not a deep error; it is literally "I walked every directory on this list and none of them contained a file by that name." This is also why two machines with "the same" tools installed can run different versions: the directories are listed in a different order, and whichever one comes first wins.

The practical skill this topic builds is small but high-leverage: when something involving a path breaks, you stop staring at the string and start asking three questions instead. Where am I starting from — an absolute root, or the current directory of this particular process? What branches am I being told to walk, and do they exist? And if this is a command lookup rather than a file lookup, which list of directories is being searched, and in what order? Almost every "file not found," "command not found," and "wrong version" error is one of those three questions with an unexpected answer. The path itself is rarely the mystery; the tree, and your position in it, almost always is.

## Level 2 candidates

**Absolute vs relative paths** — Covers the mechanical difference between paths that start at the root and paths that start at the current working directory, and the per-process state that makes relative paths context-dependent. Worth a deeper pass because "current working directory" being a property each process carries independently is the root cause of a whole category of "works here, breaks there" bugs that don't look like path bugs on the surface.

**The single-root tree (Unix) vs drive letters (Windows)** — Covers the historical reason Windows still uses `C:`/`D:` (DOS and FAT lineage) while Unix-derived systems mount everything into one tree. Worth going deeper on because the mounting model is not just a stylistic choice — it's the same mechanism that makes WSL, network shares, and removable media all look like ordinary directories, which is conceptually richer than the surface comparison suggests.

**Mounting** — Covers the mechanism by which a separate disk, partition, network share, or virtual device gets attached as a subdirectory of the existing tree. Worth a Level 2 because mounting is what makes the single-root model work in practice, and understanding it is what makes things like `/mnt/c` in WSL or macOS's `/Volumes` stop looking like quirks.

**`$PATH` / `%PATH%` and command resolution** — Covers exactly how the shell turns a bare command name like `git` into a specific executable file by walking a list of directories in order. Worth deeper treatment because `$PATH` ordering is the actual cause of an enormous number of "wrong version" problems that get misdiagnosed as installation issues, and the resolution algorithm is simpler than its consequences make it look.

**Special and virtual filesystems (`/proc`, `/dev`)** — Covers how Unix-like systems expose live kernel state — running processes, hardware devices, kernel parameters — through the same path-and-file interface as ordinary data. Worth descending into because it's the cleanest example of "a file is whatever the kernel says it is," which reframes the filesystem from a storage abstraction into a general-purpose namespace and pays off in understanding tools like `lsof`, `/sys`, and container internals.

---

## Original Content

#### L1-07 · The Filesystem Hierarchy and Paths
What looks like "folders and files" is a tree-shaped namespace the kernel exposes uniformly, and the differences you've felt between operating systems here are real but narrower than they look: Linux and macOS share a single-rooted tree (`/`) where even other disks get *mounted into* that one tree, while Windows uses a separate-letter-per-drive model (`C:`, `D:`) for historical reasons dating to DOS. Understanding paths as "instructions for walking this tree" — rather than memorizing specific path strings — is what makes absolute vs relative paths, `..`, `~`, and environment-variable-based paths (`$PATH`, `%PATH%`) click as one coherent idea instead of separate syntax to memorize per OS.