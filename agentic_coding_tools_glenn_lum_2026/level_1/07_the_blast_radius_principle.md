## Metadata
- **Date:** 11-06-2026
- **Source:** 07_the_blast_radius_principle.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-07 · The Blast Radius Principle

The most consequential misconfiguration in production agentic workflows is not a prompt mistake or a model choice. It is the quiet decision, made implicitly the first time you wired the agent up, to treat "the agent has access" as a single trust level. Once that flattening is in place, every action the agent takes — reading a file, editing a file, committing, pushing, deploying, calling a paid external API — sits at the same level of authority. The agent's own confidence becomes the only gate. That is the configuration most teams are running today, and it is wrong in a way that only reveals itself when something irreversible has already happened.

The reframe is to stop thinking about agent permissions in terms of capability ("can the agent do X?") and start thinking in terms of reversibility ("if the agent does X wrong, what does it cost to undo?"). Agent actions exist on a spectrum, and the spectrum is steep. Editing a file in a working tree is almost free to reverse — git will tell you exactly what changed and let you discard it in a keystroke. A local commit is slightly costlier but still contained. A push to a shared branch starts to involve other people's mental models. A deployment touches running systems and possibly users. An external API call — sending an email, charging a card, posting to a webhook, mutating a third-party database — has crossed a boundary you cannot cross back over. The same agent, executing the same loop, with the same expressed confidence, is doing categorically different things at each of these points.

This is why calibrating oversight to the agent's confidence is a category error. The agent does not know the blast radius of its actions; it knows the syntax of the tool call. Its confidence is calibrated against the local task ("did this change accomplish what I was asked?") and not against the question that actually matters to you ("if this is wrong, what does my Tuesday look like?"). Confidence is the wrong axis. Reversibility is the right one. Oversight should be a function of how hard it would be to undo the action if it turned out to be wrong, full stop — independent of how sure the agent sounds, independent of how well the previous ten actions went, independent of whether the task is "almost done."

Once you adopt this lens, the practical work becomes building a reversibility taxonomy for your own environment. The categories generalise — local edits, version-controlled changes, shared-state changes, externally-visible changes, irreversible external effects — but the thresholds don't. A push to main means something different in a solo project than in a regulated production system. A deployment to staging is reversible in some setups and effectively permanent in others. A database migration is in a class of its own. The work is to look at every action surface your agent touches and place it on the spectrum honestly, with particular attention to the actions that look cheap but aren't: a `rm -rf` in the wrong directory, a force push, a Stripe API call in live mode, an email send to a real list.

From there, permission scoping stops being an operational chore and becomes a structural risk decision. The default impulse — grant the agent broad access because narrowing it is annoying — is the impulse that flattens the spectrum back to a single trust level. The discipline is to grant the minimum permission that lets the task succeed, and to recognise that "convenient" and "safe" are pulling in opposite directions every time. An agent that can read your codebase but not push to it is a different product than one that can do both, and the difference is not friction; it is the size of the worst plausible mistake.

The other half of the work is human-in-the-loop checkpoint design. The trap on this side is the opposite of the first one: if you require synchronous human review for every action, you destroy the autonomy that made the agent worth using. The discipline is to identify the specific action types whose blast radius warrants synchronous review — typically the irreversible external effects and the shared-state mutations — and let the rest run. Async audit (logs, diffs, traces you can review after the fact) is sufficient for reversible actions. Synchronous review is reserved for the actions where "after the fact" is too late. Get this split right and you preserve most of the speed while removing most of the risk; get it wrong in either direction and you either crawl or get burned.

The skill this topic builds is the habit of asking, before you grant any agent any permission, what the worst plausible outcome of that permission is and how long it would take to recover from it. That question is cheap to ask and expensive to skip. The agent will not ask it for you. Its confidence is not calibrated to your blast radius; only you are.

## Level 2 candidates

**Reversibility taxonomy** — A practical framework for classifying every action surface in your environment by undo cost, from local file edits through to irreversible external API calls. Worth deeper treatment because the spectrum generalises but the thresholds are environment-specific, and most teams have never sat down and explicitly placed their actual tool surface on it.

**Minimal permission scoping** — The structural discipline of granting agents the narrowest access that lets the task succeed, and recognising convenience-driven permission grants as risk decisions rather than operational ones. Deserves depth because it intersects with concrete mechanisms (sandboxing, credential scoping, read-only mounts, network egress controls) that have real engineering tradeoffs.

**Human-in-the-loop checkpoints** — How to identify which specific action types warrant synchronous review versus async audit, without collapsing the autonomy that makes agents useful in the first place. Worth a separate treatment because the design space is non-obvious — checkpoint placement, batching, approval UX, and fallback behaviour all matter — and getting it wrong in either direction (too many checkpoints or too few) defeats the purpose.

**Irreversibility in practice** — The category of actions that look cheap but aren't: force pushes, destructive shell commands, live-mode payment APIs, production database writes, outbound communications to real recipients. Worth its own pass because these are the actions where the gap between perceived and actual blast radius is widest, and they're disproportionately where catastrophic agent failures happen.

**Blast radius across multi-agent systems** — How reversibility reasoning compounds when multiple agents share permissions or when one agent's output becomes another's input. Connects to L1-12 but warrants its own treatment because the failure mode — an action that looks reversible in isolation becoming irreversible through propagation — is specific to coordinated systems.

---