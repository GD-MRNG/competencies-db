## Metadata
- **Date:** 11-06-2026
- **Source:** 02_the_diagnostic_method.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-02 · The Diagnostic Method

Debugging is the activity that consumes more of your career than any other, and it is the one your education most thoroughly ignored. You were taught to write code, not to figure out why code you already wrote is doing something you did not ask it to do. The result is that most engineers learn debugging the way medieval physicians learned medicine: by apprenticeship, anecdote, and a great deal of guessing. It looks improvisational from the outside, and the engineers who are good at it often describe it as intuition, which is unhelpful both to themselves and to anyone watching. It is not intuition. It is a method, and once you see the method, the people who appeared to be guessing turn out to be running a tight experimental loop in their heads.

The reframe that changes everything is old enough to feel obvious once it lands: debugging is the scientific method applied to a system you happen to control. You observe a behaviour. You form a hypothesis about what could produce it. You design the cheapest possible test that would prove that hypothesis wrong. You run the test, update your beliefs, and pick the next hypothesis. The loop is identical to the one a working scientist runs, with one enormous advantage — your system is deterministic enough (usually) that the experiments actually converge. The reason this framing matters is that it tells you what you are allowed to do. You are not allowed to change something because it might help. You are not allowed to fix a bug you cannot explain. You are allowed to form a hypothesis, test it, and act on the result.

The difference between the engineer who closes the bug in an hour and the one still flailing at hour six is almost never raw intelligence. It is that the first one is running this loop and the second one is changing things and re-running, hoping something shifts. Changing things and hoping is not debugging; it is a slot machine. It feels productive because you are typing, and it occasionally pays out, which is exactly what makes it so hard to give up. The discipline is to refuse it — to treat every change as an experiment with a prediction attached, and to be honest when the result didn't match what you expected, because that mismatch is the most valuable signal you will get all day.

The single highest-leverage move in the entire discipline is reproduction. A bug you can summon on demand is already halfway solved; a bug you cannot reproduce is not yet a bug you understand, it is a rumour. This sounds tautological until you watch how often engineers skip it — they see the stack trace, form a theory in the first thirty seconds, and start fixing, never having confirmed they can make the failure happen at will. Then they "fix" it, can't tell whether it's gone or just hiding, and ship the uncertainty to production. Reproduction is the move that converts a vague complaint into a concrete object you can interrogate. Everything that comes after — bisecting the commit range, adding instrumentation, stepping through with a debugger — depends on being able to ask the system the same question repeatedly and get the same answer. Without that, you are not doing science; you are doing astrology with logs.

Once you have reproduction, the rest of the toolkit is essentially elaboration on the same loop, optimised for different conditions. Binary search — across commits, across the call stack, across the input space — is how you halve the search space when you have no theory, and it is shockingly underused because it feels mechanical compared to "thinking hard." Stack traces and error messages are far more informative than the average engineer gives them credit for; reading them precisely, instead of skimming for the first familiar word, is the cheapest debugging skill in the field and the most commonly skipped. The choice between a debugger and instrumentation is a question about feedback latency: a debugger gives you deep inspection of a single moment, logging gives you a shallow view across many moments, and the right one depends on whether your unknown is "what is the state right here" or "how did we get into this state at all."

Then there are the bugs that break the loop itself. Races, heisenbugs, flakiness — these resist reproduction by their nature, and the naive method stalls on them because step one no longer works reliably. Understanding why they're hard is the prerequisite for the specialised tactics that catch them: stress, time dilation, deterministic replay, recorded traces. The point is not the tactics themselves but the recognition that you are now in a regime where ordinary debugging will mislead you, and the engineer who doesn't know they've crossed that line will spend a week chasing a ghost.

The last skill in the loop is the one the canon never mentions: knowing when you are lost. There is a point in every hard bug where continuing alone stops being diligence and starts being ego, and the engineer who can feel that point arriving — and rubber-duck, or escalate, or sleep on it — closes bugs that the stubborn one is still grinding on at midnight. The method is rigorous, but it is not infinite; recognising its limits is part of using it well.

What you build, over years of doing this deliberately, is a sense for which hypothesis to test next — and that sense is what looks like intuition from the outside. It isn't. It's a method, practised so often it has gone underground. Make it explicit again, and you can examine it, teach it, and get better at it on purpose.

## Level 2 candidates

**Reproduction as the First Goal** — The discipline of making the bug happen on demand before attempting to fix it, and the techniques for narrowing inputs and environments until it does. Worth a deep dive because the gap between engineers who chase reproduction first and those who skip it is the single largest predictor of who closes the hard bugs.

**Binary Search the Problem Space** — Halving the search space across commits (with `git bisect`), across the stack, and across inputs to turn an unbounded search into a logarithmic one. Worth depth because it's the most powerful generic move in debugging and the one most consistently underused in favour of "thinking harder."

**Reading a Stack Trace and an Error Message** — Extracting maximum signal from the diagnostic output the system is already handing you, including the parts most engineers' eyes slide past. Worth a deep dive because it is the highest-ratio debugging skill — almost free to acquire, and nearly always skipped.

**Instrumentation vs the Debugger** — The judgment call between stepping through with a debugger and adding logs to watch behaviour over time, framed as a question about feedback latency and what kind of unknown you're chasing. Worth depth because most engineers reach for whichever tool they're habituated to, rather than the one the problem actually calls for.

**The Hardest Bugs: Races, Heisenbugs, and Flakiness** — Why non-deterministic failures break the standard loop and what specialised tactics — stress testing, deterministic replay, recorded traces — exist for catching them. Worth a deep dive because the failure mode here isn't lack of effort; it's applying ordinary debugging in a regime where it actively misleads.

**Knowing When You're Lost** — The metacognitive skill of recognising when continuing alone has stopped being productive, and the moves (rubber-ducking, escalating, sleeping on it) that actually unstick you. Worth depth because it is almost entirely absent from formal training and is the difference between a bad afternoon and a wasted week.

---