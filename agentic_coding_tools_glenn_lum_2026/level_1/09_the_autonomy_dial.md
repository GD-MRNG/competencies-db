## Metadata
- **Date:** 11-06-2026
- **Source:** 09_the_autonomy_dial.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-09 · The Autonomy Dial

The most expensive mistake you can make with a coding agent is treating its autonomy level as a property of the tool rather than a setting you choose. Every agent on the market — from the most cautious IDE assistant to the most aggressive background worker — exposes a dial. The dial runs from line-by-line suggestion, where you accept or reject every token, through chunk-level review, through supervised task execution, all the way to multi-hour unsupervised runs that branch, commit, and report back. Pretending the dial doesn't exist, or leaving it at whatever the vendor shipped, is how teams end up either bottlenecked on trivial approvals or surprised by what got merged overnight.

The reason this matters is that the right setting is not a property of the tool, the model, or your seniority. It is a property of the task in front of you, and it shifts hour by hour. A senior engineer working on a well-tested utility library at 10am should probably be running with high autonomy. The same engineer at 4pm, touching authentication code in a service whose tests are flaky, should be back near the manual end of the dial. The tool hasn't changed. The model hasn't changed. What changed is the three things that actually determine where the dial belongs.

The first is reversibility. Some agent actions are cheap to undo — an edit to a file you haven't committed, a scratch branch, a dev-environment experiment. Others are not — a force-push, a database migration, a deployment, an external API call that charged a customer or sent an email. The dial should be calibrated to the worst irreversible action the agent can take in the current session, not the average one. This is the same lesson as the blast radius principle, applied to the autonomy axis: a single irreversible action in an otherwise reversible workflow drags the appropriate autonomy level down to match it.

The second is specification quality. An agent operating with high autonomy on an underspecified prompt does not refuse and ask questions; it fills in the gaps from its priors and produces something plausible. The output will compile, the tests it writes will pass, and the result will look like work. Whether it solves your actual problem is a different question, and one you will only discover later — often much later, because plausible-but-wrong is harder to catch than obviously broken. The rule is uncomfortable but reliable: the vaguer your spec, the lower the dial belongs. High autonomy amplifies whatever is in the prompt, including the gaps.

The third is your current capacity to verify the output. Verification is not free, and it is not constant. If you have good tests, clear acceptance criteria, and the time to actually run and read the result, you can absorb a larger volume of agent output safely. If you don't — if the test suite is thin, if you're context-switching, if you're tired — then high autonomy just means more code arriving faster than you can confirm it is correct. The dial should be set to the rate at which you can actually verify, not the rate at which the agent can produce. Mismatching these is how you end up nominally shipping fast and actually accumulating debt you cannot see.

The failure mode worth naming is autonomy creep. It rarely happens as a deliberate decision. It happens because a workflow that was working at one setting gets nudged upward — you skip a confirmation here, enable an auto-approve flag there, add a tool to the allowlist because the prompts were getting tedious — and each individual step is reasonable. What's missing is a corresponding increase in oversight: better tests, tighter scoping, audit review. Six weeks later the agent has permissions you wouldn't have granted on day one, and nobody made the decision to grant them. Detecting this requires looking at the actual configuration periodically, not at the workflow as you remember setting it up.

The skill this topic builds is the habit of asking, before each significant agent task, where the dial belongs for this specific piece of work. Not where it usually sits, not where the tool defaults, not where it was for the last task. The question is: how reversible is what I'm about to let the agent do, how precisely have I specified what I want, and how much output can I actually verify in the time I have? The answer determines the setting. Get into the habit of moving the dial down deliberately when any of those three weakens, and back up when they strengthen, and most of the "the agent did something I didn't want" failure mode evaporates — because you stopped delegating decisions you weren't in a position to verify.

## Level 2 candidates

**Task delegability criteria** — A structured framework for classifying tasks by the three factors that determine appropriate autonomy: reversibility, specification clarity, and verifiability. Worth a deep dive because the intuitive judgment most engineers use ("does this feel safe to delegate?") collapses under load and on unfamiliar codebases, and an explicit checklist holds up where intuition does not.

**Prompt specificity vs. output quality** — How underspecification interacts with autonomy to produce plausible-but-misaligned output, and the practical techniques for tightening a spec to the point where higher autonomy is actually safe. Worth deeper treatment because this is the lever most engineers underuse — they reach for better models or more retries when the cheaper fix is upstream in the prompt.

**Autonomy creep** — The mechanisms by which permissions and trust expand silently across a workflow's lifetime, the leading indicators that it is happening, and the audit practices that catch it before something goes wrong. Worth going deeper because this is a process and configuration problem more than a technical one, and the countermeasures are organisational habits that don't fit inside a single prompt or session.

**Calibrating the dial to team context, not just task context** — How team size, on-call rotation, review capacity, and codebase maturity shift where the appropriate default sits, independent of the individual task. Worth its own treatment because most autonomy advice is written for individuals and breaks down when multiple engineers share a repo with shared agent configuration.

---