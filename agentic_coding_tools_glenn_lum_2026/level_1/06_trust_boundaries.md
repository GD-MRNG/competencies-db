## Metadata
- **Date:** 11-06-2026
- **Source:** 06_trust_boundaries.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-06 · Trust Boundaries

You probably think of your coding agent as something you control. You wrote the prompt, you connected the tools, you approved the repository it's working in. The trust relationship feels like the one you have with a script you wrote yourself: it does what you told it to do, within the permissions you gave it. This mental model is wrong, and the gap between it and reality is the entire security story of agentic systems.

The correct frame is this: every input channel into an agent is a channel through which instructions can arrive. Not just your prompt, but the README of a repo it cloned, the issue body it summarised, the search result it browsed, the tool description it loaded from an MCP server, the error message returned from a shell command, the comment in a source file it read. To the model, all of these are tokens in a context window. There is no reliable mechanism — architectural, training-based, or otherwise — by which the model distinguishes "instruction from the principal" from "data containing text that looks like an instruction." The boundary exists in your head. It does not exist in the system.

Once you see this, a lot of agentic security stops looking like bugs and starts looking like architecture. A malicious instruction embedded in a file the agent reads is not a flaw in the agent; it is the agent doing exactly what its design permits. The model is a probabilistic text continuation engine that has been wrapped in a loop and given tools. If the most plausible continuation given its context is "call the exfiltrate tool," it will. The provenance of the text that made that continuation plausible is invisible to it.

This is why trust in agentic systems does not transfer the way you intuitively expect. When you trust a vendor, you trust their code to behave according to its specification. When you trust an agent, you are not just trusting the agent's code — you are trusting every surface the agent transitively reads from, because each of those surfaces can issue instructions through the agent. Connecting an agent to a new data source is not like adding a new input to a pipeline. It is like granting that data source the same authority as your prompt. The blast radius of a compromised README expands to whatever your agent can do.

The taxonomy that matters here is the split between direct and indirect channels. Direct prompt injection is what most people picture: an attacker types something into the chat to subvert the system prompt. This is the easier problem and the less interesting one, because the attacker needs access to the chat. Indirect injection is the structural threat — the attacker plants instructions in data the agent will read in the course of routine work, and waits. A poisoned issue, a booby-trapped dependency, a community MCP server with a subtly malicious tool description, a search result that lands in context during research. The attacker never speaks to your agent directly. They speak through the substrate the agent treats as data.

The corollaries follow quickly. An MCP server you connect to is not analogous to an API you call; it is closer to a browser extension you install, because its tool descriptions and responses become part of the agent's context and can shape its behaviour. A multi-agent system propagates injection through trust relationships between agents — a compromised subagent's output is "data" to the orchestrator, which means it is also instruction. Public repositories become attack surface in a new way: attackers can plant content specifically calibrated to be discovered by agents performing routine dependency or codebase searches, knowing the agent will execute on what it reads. None of these are speculative future risks. They follow directly from the architecture.

The defensive posture this implies is not "sanitise the inputs" or "harden the prompt." Both of those treat trust as something you can patch into the system after the fact. You cannot. The model has no input-sanitisation layer that's stronger than its own pattern-matching, and adversarial text routinely defeats prompt-level defenses because the defense and the attack live in the same medium. The actual defenses are architectural: limit what the agent can do (so an injection's blast radius is bounded), control what the agent can read (so adversaries can't reach it cheaply), and treat every new input surface as a privilege escalation decision rather than a convenience. The question is never "do I trust this data source." It is always "what can this data source make my agent do, and am I willing to grant it that authority."

The skill this topic builds is the habit of asking, before connecting any new surface to your agent, whether you are prepared for the contents of that surface to issue commands on your behalf. That reframing — from input as data to input as instruction — is the whole concept. Once it's installed, the rest of agentic security becomes a series of consequences rather than a list of rules to memorise.

## Level 2 candidates

**Prompt injection (direct vs. indirect)** — Covers the mechanics of how injected instructions propagate through the context window, with particular focus on the indirect case where instructions arrive through data the agent reads as part of its normal work. Worth deeper treatment because the defenses for direct and indirect injection are structurally different, and indirect injection is where most realistic attacks land but where developer intuition is weakest.

**MCP server trust** — Covers the actual risk surface of connecting to a community-published MCP server, including how tool descriptions enter the model's decision-making and what an adversarial server can do to a session. Worth deeper treatment because MCP adoption is accelerating and most users treat servers as "tools you call" rather than "code that shapes what your agent decides to do."

**Cross-agent propagation** — Covers how a successful injection in one agent spreads to co-running agents through inter-agent message passing, where one agent's output becomes another's trusted input. Worth deeper treatment because multi-agent architectures invert the usual trust model — your orchestrator is now downstream of an attacker-controlled subagent — and the patterns to contain this don't show up in single-agent threat modelling.

**Supply chain injection** — Covers how attackers seed public repositories, package descriptions, and documentation with content designed to be ingested by agents performing routine searches, and what makes this category distinct from classical software supply chain attacks. Worth deeper treatment because the attack assumes an agent in the loop and exploits agentic behaviours (summarisation, autonomous tool use) that have no analogue in non-agentic dependency management.

**Trust boundary modelling in practice** — Covers how to actually enumerate the input surfaces of a working agent setup and classify each by the authority an injection through it would carry. Worth deeper treatment because the abstract principle is easy to agree with but the concrete inventory — for a real repo, with real tools and MCP servers connected — is what converts the principle into a configuration decision.

---