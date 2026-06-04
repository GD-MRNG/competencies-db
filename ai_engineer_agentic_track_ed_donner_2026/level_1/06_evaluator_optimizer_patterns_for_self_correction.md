## Metadata
- **Date:** 05-06-2026
- **Source:** 06_evaluator_optimizer_patterns_for_self_correction.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-06 · Evaluator-Optimizer Patterns for Self-Correction

A single-pass agent is a confident liar. It will pick the wrong tool, misread a result, or chase a dead end, and it will present the outcome with the same calm authority it would use for a correct answer. The model has no built-in mechanism for noticing that it was wrong, because from inside a single forward pass there is no "wrong" — there is only the next most likely token. If you want reliability, you have to build the noticing from the outside.

That is what evaluator-optimizer patterns do. You take the output of one reasoning step and feed it to a second step whose only job is to judge: is this good enough, and if not, what is wrong with it? If the judgment is negative, a third step — the optimizer — revises the output in light of the critique, and the cycle repeats until the evaluator approves or you run out of patience. The pattern is structurally simple and it maps onto something the model is actually good at: criticising work it didn't have to produce under pressure. Generating an answer and evaluating an answer are different cognitive tasks, and models tend to do the second one better when it's framed cleanly.

The mental shift is to stop thinking of the model as a function that returns an answer and start thinking of it as a participant in a quality process. In single-pass mode, you are betting everything on one roll of the dice. In an evaluator-optimizer loop, you are running a small adversarial system where one role produces and another role challenges, and the output you ship is whatever survives the challenge. This is the same logic as code review, peer review in science, or a second opinion in medicine — domains where humans long ago accepted that the original author is the wrong person to certify their own work.

The roles can be played by the same model with different prompts, by different models entirely, or by a hybrid where a frontier model evaluates the output of a cheaper worker. Each arrangement trades off cost and rigour. Same-model self-critique is the cheapest and surprisingly effective; the model can often spot issues in its own output that it didn't account for during generation, because the evaluation prompt frames the task differently and activates different patterns. Cross-model evaluation is more expensive but catches blind spots that a single model would share with itself. The right choice depends on how much you're willing to spend per decision and how independent you need the judgement to be.

The hard part is not the loop. The hard part is defining what "good" means precisely enough that the evaluator can judge it consistently. Vague criteria — "is this answer helpful?" — produce vague evaluations, and the loop degenerates into the evaluator approving anything that looks plausible. Sharp criteria — "does this output cite at least two sources, address the user's specific question about pricing, and avoid making claims about the product roadmap?" — give the evaluator something to actually check. The discipline of writing good evaluation criteria forces you to articulate what you wanted in the first place, which often reveals that you didn't know.

You also have to decide when to stop. Evaluator-optimizer loops can run forever if the optimizer keeps producing outputs the evaluator keeps rejecting, and every iteration costs tokens, latency, and money. You need a maximum iteration count, an escalation path for when the loop fails to converge (often: hand it to a human), and ideally some signal that progress is being made — if iteration five is no better than iteration two, more iterations probably won't help. A close cousin of this pattern is confidence scoring with rejection sampling: instead of a separate evaluator, the model emits a confidence score with its answer, and low confidence triggers a regeneration or escalation. Cheaper, less rigorous, often good enough.

The cost of all this is real. You are doing at least twice the work for every answer, often more, and latency multiplies with iterations. This is why the pattern is reserved for tasks where correctness matters more than throughput: financial calculations, medical or legal summaries, decisions that touch external systems irreversibly, anything where a confidently wrong answer carries a higher cost than a slow correct one. For low-stakes chat, the overhead isn't worth it. For an agent that is about to issue a refund or send an email to a customer, it almost always is.

The skill this builds is treating reliability as something you architect rather than something you hope for. Once you internalise that any single model output is a draft and that quality comes from structured criticism rather than from picking a better model, you start designing systems where reasoning is checked by reasoning. That is the difference between an agent that works in a demo and an agent you would trust to run unattended.

## Level 2 candidates

**Evaluation Criteria and Success Metrics** — Covers how to define what "good" means for an agent's output in terms the evaluator can actually apply, including the difference between binary checks, rubric scoring, and reference-based grading. Worth a deeper dive because the quality of your evaluator ceiling is set entirely here — a sloppy rubric produces a sloppy loop no matter how many iterations you run.

**The Evaluator-Optimizer Loop Mechanics** — Covers the concrete control flow: how the evaluator's critique is passed to the optimizer, how revision context accumulates across iterations, and how to detect non-convergence. Worth a deeper dive because the naive implementation has subtle failure modes (the optimizer ignoring the critique, the evaluator drifting in standards, context bloat across iterations) that only show up under load.

**Confidence Scoring and Rejection Sampling** — Covers the lighter-weight alternative where the model self-reports confidence and you regenerate or escalate when it dips, rather than running a separate evaluator pass. Worth a deeper dive because the calibration of self-reported confidence is its own problem — models are often confidently wrong and uncertainly right — and the techniques for making confidence scores actually useful are non-obvious.

**Prompting for Self-Critique** — Covers the prompts and framings that elicit useful criticism from a model evaluating its own output, including techniques like "what could be wrong with this," "what edge cases were missed," and adversarial role-play. Worth a deeper dive because the gap between a self-critique prompt that catches real issues and one that produces sycophantic agreement is large and not intuitive.

**Ensemble and Voting Patterns** — Covers running the same task multiple times with varied prompts, temperatures, or models and selecting or aggregating the best output. Worth a deeper dive because it's a different reliability strategy than evaluator-optimizer — parallel rather than sequential — with different cost, latency, and failure characteristics, and the aggregation logic (voting, weighted ensemble, judge model) is where most of the design work lives.

**Cross-Model Evaluation Strategies** — Covers when to use the same model for generation and evaluation versus different models, and how to think about evaluator independence. Worth a deeper dive because shared blind spots between generator and evaluator can silently undermine the entire pattern, and the choice has real cost implications when frontier models are involved on both sides.

---