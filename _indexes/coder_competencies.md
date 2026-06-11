# Coder Competencies — Top-Level Index

> Every change a developer makes lives in three **enduring contexts** — the **code** it's written in, the **practice** of producing it, and the **system** it runs in — each as true in 1995 as in 2035. A fourth map stands slightly apart: the **agent** now producing more and more of that code. It isn't a fifth context so much as the *instrument* reshaping how you apply the other three — and it depends on them, because you can only verify what you could have written and only direct what you understand.

| Map | Owns | The question it answers |
|---|---|---|
| **The Canon of Code Craft** *(synthesis)* | The code as a crafted object | *Is what I built good — understandable and changeable?* |
| **The Working Developer** *(unwritten curriculum)* | The human practice of producing change | *Can I actually get it done, here, with these people?* |
| **From Coder to Engineer** *(operations)* | The code as a running system | *Will it survive contact with production?* |
| **Agentic Coding Tools** *(the instrument)* | The agent that increasingly writes the code | *Can I trust what the agent built — and should I have delegated it?* |

## Reading order

Read inside-out — artifact, then practice, then system — then the instrument that now produces all three. They're lenses, not a strict sequence; jump freely once you're in, but this order builds each on the last.

1. **Code Craft** — start here. The most foundational, and the one you already half-know, so it consolidates scattered habits into a single lens (*complexity is the cost*) that recurs everywhere else. → entry: **L1-01, The Nature of Complexity**.
2. **The Working Developer** — next, because this is where an experienced returner's real gaps live: the tacit, situated skills no book teaches. Highest ROI of the first three. → entry: **L1-06, Tactical vs Strategic Judgment**.
3. **Software Engineering** — the broadest build-out: the full lifecycle of a running system, and what "operational seniority" actually means. → entry: **L1-11, Observability**.
4. **Agentic Coding Tools** — last *conceptually*, because directing and verifying an agent draws on all three above: you judge its output with the canon, steer it with practitioner judgment, and trust it in production with operational sense. But enter it *early* for immediate practical value, since you already use these tools daily. → entry: **L1-10, Specification and Verification** (or **L1-06/L1-07, Trust Boundaries + Blast Radius** if you want the risk basics first).

**If you read only four topics:** the four entry points above. They are the spine of each map and, between them, the shortest path to a coherent picture of the whole craft — the part you write, the way you work, the system you run, and the machine you increasingly delegate to.

---

## The ladder: engineering levels in the AI age

The maps are the curriculum. This is what they build toward — a progression from someone who can't read code to someone who builds the tools others code with. The behaviours are the visible surface; the section after this explains the engine underneath. Each level carries a pointer to the map that takes you to the *next* rung — the one whose absence is what's holding you where you are.

**Level 0 — Non-Coder**
*"What the hell is this? I don't know anything."*

- Has never touched code or an AI coding tool
- Thinks software development is someone else's job
- Wouldn't know where to even start

**↳ To climb from here:** nothing yet — open a tool, generate something, run it. The maps need output to work on.

---

**Level 1 — AI User (Vibe Coder)**
*"I typed what I wanted and it worked. Shipped."*

- Uses Claude / Cursor / ChatGPT to generate code
- Can copy-paste into a file and run it
- Has no idea what the code does, but it does the thing
- Breaks something → asks AI to fix it → repeat
- Has never read an error message properly

**↳ To climb from here:** **Agentic Coding Tools** L1-03 (the Feedback Environment) — read the error instead of just re-prompting — which opens **Code Craft** (start reading the code itself).

---

**Level 2 — AI-Assisted Builder**
*"I can guide the AI and actually tell when it's going wrong."*

- Uses coding agents (Cursor, Copilot, Claude Code) fluently
- Can write basic code themselves when needed
- Reads the generated code and roughly understands it
- Knows when the AI is hallucinating or going in circles
- Can break a problem into smaller prompts

**↳ To climb from here:** **The Working Developer** L1-02 (the Diagnostic Method) + L1-04 (Tooling/git) — the independence to debug and produce *without* the AI is the only thing that lets you truly judge it.

---

**Level 3 — Junior Engineer (AI-Native)**
*"I write some code myself, and I use AI as a power tool."*

- Writes real code from scratch when the AI isn't the right tool
- Uses agents to 10x output, not replace thinking
- Understands debugging — doesn't just re-prompt blindly
- Can spot bad AI output before it causes damage
- Knows git, basic system concepts, how things actually run

**↳ To climb from here:** **Code Craft** L1-01 (Complexity) + the Structure tier — start reviewing for *design*, not just bugs — paired with **Agentic Coding Tools** L1-10 (specs as the upstream lever on output quality).

---

**Level 4 — Mid-Level Engineer**
*"I know what I'm doing. The AI knows what I mean."*

- Uses agents strategically — knows when to trust them and when not to
- Reviews AI-generated code critically, not just vibes
- Writes clear specs and context so agents produce better output
- Debugs complex issues the AI can't solve alone
- Thinks about architecture, not just features

**↳ To climb from here:** **Software Engineering** (reliability, what-breaks-at-scale) + **Agentic Coding Tools** L1-08/L1-10 (spec gaming + verification) — the failures you now own live in production and in un-trusted agent output.

---

**Level 5 — Senior Engineer (AI Age)**
*"I'm the architect. The agents are my workforce."*

- Designs systems and delegates implementation to agents
- Writes minimal code — spends time on decisions, not syntax
- Knows the limits of current AI tools better than most
- Can take an agent-written codebase and reason about it deeply
- Thinks about what breaks at scale, what agents miss

**↳ To climb from here:** **Agentic Coding Tools** L1-12 (multi-agent / pipelines) + **The Working Developer** L1-13 (Organizational Navigation) — stop optimising your own output, start shaping how a team-plus-agents produces.

---

**Level 6 — Staff / Principal (AI-Native)**
*"I build the workflows other engineers use to ship 10x faster."*

- Designs agent pipelines, not just features
- Shapes how a team or company uses AI coding tools
- Thinks about quality, security, maintainability in an AI-generated codebase
- Sees what's coming next in tooling before it arrives

**↳ To climb from here:** beyond the product layer into the model layer — you understand the tools deeply enough that their limits look like problems, not walls. (You're now applying all four maps at the level of the *system*, not your own output.)

---

**Level 7 — Legend**
*"I'm building the agents you're coding with."*

- Contributes to or builds AI coding tools themselves
- Understands the model layer, not just the product layer
- Has opinions on where this is all going — and they're usually right

**↳ The ceiling:** the four maps now describe the tools *you* build. You work one layer beneath them, at the model layer they all sit on top of.


## Beneath the levels: what changes, and why

The checklist describes *behaviours*. This section describes the engine underneath them — what actually moves as you climb, what forces each jump, and why the ladder has the shape it now does.

**Start here:** the levels do not measure what you can *build*. In an AI-native world, building — generation — is cheap and getting cheaper, equally available to a Level 1 vibe coder and a Level 7 legend. What the levels measure is what you can *verify*: the range of ways the generated thing can be wrong that you are able to detect, and therefore be accountable for. Every rung up is an expansion of your verification frontier. This is the durable mechanism, and it follows from the one condition that reshaped the whole ladder: when generation becomes nearly free, value migrates to verification and specification — the two things a machine cannot take responsibility for. The old bottleneck was your fingers; the new one is your judgment.

### Four things rise together

- **The bottleneck migrates outward** — from *generation* (L1: can I get anything that works?) to *comprehension* (L2–3: do I understand what came out?) to *verification and judgment* (L4–5: is it right, and is it even the right thing?) to *leverage design* (L6–7: do the conditions I've built make others produce good work?). You always work on whatever has just become scarce.
- **The unit you own expands** — line → feature → component → system → workflow → tooling. Seniority is partly just the size of the thing whose quality is your fault.
- **The failure you're preventing moves further into the future** — "does it run now?" → "is it correct?" → "will this design survive change?" → "will it hold at scale?" → "will the *process* still produce good code in a year?" Junior work is judged against the present; senior work against time.
- **Your relationship to the AI changes** — oracle (trust blindly) → tool (wield) → workforce (direct and review) → substrate (build). The vibe coder obeys the model; the legend builds it.

### The jumps that matter (and the condition that forces each)

Growth isn't smooth — it's a few genuine phase transitions, each usually triggered by a specific kind of pain.

- **L1 → L2 · the comprehension threshold.** You start *reading* the output. *Forced by:* shipping something you didn't understand and watching it break in a way re-prompting couldn't fix — the first time the black box bit you.
- **L2 → L3 · the independence threshold.** You can produce without the AI, which is the only reason you can judge it. *Forced by:* hitting problems the AI couldn't solve, and discovering that what you can't do yourself, you can't supervise.
- **L3 → L4 · the judgment threshold.** You stop thinking in features and start thinking in structure; review stops being vibes. *Forced by:* owning code long enough to feel the cost of bad design — the one-hour change that took a day because the system fought you.
- **L4 → L5 · the delegation threshold.** You shift from doing to deciding-and-delegating: minimal code, maximal judgment. *Forced by:* agents getting good enough that your typing stopped being the constraint — so the constraint became how precisely you specify intent and how well you verify results, and you reorganised your work around those two.
- **L5 → L6 · the leverage threshold.** You stop optimising your own output and start designing the conditions under which a whole team-plus-agents produces. *Forced by:* seeing that individual output doesn't scale and that the bottleneck had moved off any person onto the *system* — the pipeline, the standards, the feedback environment.
- **L6 → L7 · the substrate threshold.** You move from using the tools to building them, product layer to model layer. *Forced by:* understanding the tools deeply enough that their limits stop looking like walls and start looking like problems.

### So what *is* seniority now?

Not output — agents flattened that. It is the product of three things: how much wrongness you can foresee and verify, how large a system you can hold responsibility for, and how far ahead the failures you reason about lie. The deep irony of the era is that AI raised the *floor* (anyone can ship) while raising the *value of judgment* at the same time — because someone still has to be accountable for what ships, accountability requires verification, and verification requires exactly the expertise AI appears to make unnecessary. The single sentence the whole ladder reduces to: **you can only safely delegate what you could have caught being wrong.**

Which is why the maps above aren't made obsolete by agents — they're what *set your level among them*. The Canon raises the kinds of design failure you can see; the Working Developer raises the judgment you delegate with; Operations raises the failures-at-scale you can foresee; the Agentic map names the bottleneck all of it now serves. Climbing this ladder is, concretely, raising your verification ceiling — and those four maps are the curriculum for doing it.

---