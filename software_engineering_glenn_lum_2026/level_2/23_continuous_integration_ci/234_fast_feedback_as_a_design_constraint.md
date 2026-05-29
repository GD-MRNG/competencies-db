## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams treat pipeline speed as a performance problem. The pipeline gets slow, someone files a ticket, an engineer spends a sprint shaving off minutes, and the team moves on until it gets slow again. This framing is wrong. Pipeline execution time is not a performance metric to be optimized after the fact — it is a design constraint that should shape how you structure your pipeline from the start. The difference matters because a performance problem invites incremental fixes, while a design constraint demands upfront decisions about what runs, when, and why. Teams that treat speed as an afterthought end up with pipelines that technically work but behaviorally fail: they produce correct results too late to change how developers work, which quietly undoes the integration frequency that CI exists to enable.

## The Behavioral Threshold Effect

Pipeline duration doesn't degrade developer productivity linearly. It crosses thresholds that change behavior in qualitative ways.

A pipeline that completes in **under five minutes** is synchronous feedback. Developers push and wait. They stay in the mental context of the change they just made. When the result comes back — pass or fail — they act on it immediately. This is the equivalent of a compiler error: fast enough to be part of the development loop itself.

Between **five and ten minutes**, most developers will glance at something else — read a message, review a pull request — but they can return to their original context without significant cost. The feedback is still close enough to feel connected to the work.

Beyond **ten minutes**, a meaningful context switch happens. The developer picks up a different task. Cognitive research on task-switching consistently finds that returning to a complex mental context — remembering what you were testing, why you structured the change that way, what edge cases you were thinking about — takes fifteen to twenty-five minutes of reloading time. A pipeline that takes fifteen minutes to fail doesn't cost the developer fifteen minutes. It costs fifteen minutes of wait plus fifteen or more minutes of context reconstruction. The effective cost is thirty minutes, and the developer may not return to the failure immediately because they're now mid-thought on something else.

Beyond **thirty minutes**, developers stop waiting entirely. They push and move on with their day. Failure notifications arrive as interrupts into unrelated work. The mental model of the original change has decayed. And critically, developers begin to adapt: they start batching changes to avoid paying the feedback cost multiple times. Instead of four small pushes per day, they make one or two larger ones. This is the exact behavioral regression that CI was designed to prevent. The pipeline is technically running continuous integration. The developer is not practicing it.

The threshold that matters is not a precise minute count — it depends on team norms and individual tolerance — but the structural consequence is reliable: **slow pipelines cause batching, batching reduces integration frequency, and reduced integration frequency reintroduces merge conflicts and integration failures at a rate proportional to the batch size.**

## Stage Ordering as an Optimization Problem

The Level 1 post established that you should run cheap checks before expensive ones. The deeper question is: what does "cheap" actually mean, and how do you decide the order when stages have different failure rates, different execution times, and dependencies between them?

Each stage in your pipeline has two relevant properties: its **execution time** and its **probability of catching a defect** on any given run. A linting stage might take ten seconds and flag problems in twelve percent of pushes. A unit test suite might take ninety seconds and catch failures in twenty percent of pushes. An integration test suite might take eight minutes and catch failures in three percent of pushes.

The optimal ordering for independent stages — those with no dependency relationship — is to sort by failure probability divided by execution time, descending. This is the "bang for the buck" metric: which stage gives you the highest chance of a failure signal per second of execution? A stage that fails twelve percent of the time in ten seconds (0.012 per second) should run before a stage that fails twenty percent of the time in ninety seconds (0.0022 per second), even though the second stage has a higher absolute failure rate.

This is analogous to weighted shortest job first scheduling, and the intuition is the same: you want to minimize the expected time a developer waits before getting an actionable signal. Every second the pipeline spends running a stage that will pass is a second of wasted wall-clock time when a later stage would have caught the problem faster.

In practice, stages are not all independent. Compilation must precede unit tests. Unit tests should generally precede integration tests, not because of a technical dependency, but because debugging an integration test failure when unit tests are also broken is a diagnostic nightmare — you end up chasing symptoms of a root cause that a unit test would have localized in seconds. So the ordering is constrained by a directed acyclic graph of dependencies and diagnostic value, and you optimize within those constraints.

A concrete example of what good ordering looks like in a typical pipeline:

```
Stage 1: Syntax check / lint          (~10s,  high failure rate)
Stage 2: Compile / build              (~30-90s, medium failure rate)
Stage 3: Unit tests                   (~1-3min, medium-high failure rate)
Stage 4: Integration / contract tests (~5-10min, low failure rate)
Stage 5: End-to-end / acceptance tests (~10-20min, very low failure rate)
```

Each stage gates the next. A syntax error is caught in ten seconds, not after a ten-minute integration suite has also run and failed for a different reason. The developer gets a single, clear signal rather than a wall of failures across multiple stages.

## The Critical Path Under Parallelism

Parallelism is the standard tool for reducing wall-clock time, but it has a mechanical constraint that teams frequently misunderstand. When you parallelize stages, the total pipeline duration is determined by the **critical path**: the longest sequential chain of dependent stages from start to finish.

Consider a pipeline with two parallel branches. Branch A runs lint, compile, and unit tests in sequence: 10 seconds + 60 seconds + 120 seconds = 190 seconds. Branch B runs integration test environment setup and integration tests in sequence: 45 seconds + 480 seconds = 525 seconds. The pipeline's wall-clock time is 525 seconds — the length of Branch B — regardless of how fast Branch A is. You could reduce unit test time to zero and the pipeline still takes 525 seconds.

This means that optimizing anything that is not on the critical path has zero effect on pipeline duration. Teams that spend weeks parallelizing and speeding up unit test shards while their integration test suite is a single sequential bottleneck are not making the pipeline faster. They're making a non-bottleneck more efficient, which is definitionally waste.

Identify the critical path first. Optimize there. Then re-evaluate, because shortening the critical path may shift it to a different branch.

### Parallelism within a stage

Splitting a test suite into parallel shards is effective but has mechanical overhead. Each shard needs a compute environment provisioned, dependencies installed, and test context established. If shard setup takes sixty seconds and the shard itself runs for thirty seconds, you've made the pipeline slower by parallelizing, not faster. The crossover point where parallelism helps depends on the ratio of setup time to execution time. For test suites, this means parallelism pays off primarily when the test execution time significantly exceeds the environment setup time — which is why container image caching and pre-warmed build environments matter so much. They compress setup time, shifting the ratio in favor of parallelism.

## Time-to-Signal Is Not Pipeline Duration

A subtlety that most pipeline dashboards obscure: the metric that affects developer behavior is **time from push to actionable signal**, not pipeline execution duration. These are different numbers.

If a developer pushes code and the pipeline spends eight minutes in a queue waiting for a runner, then takes seven minutes to execute, the pipeline duration is seven minutes but the feedback time is fifteen minutes. The developer experiences fifteen minutes of waiting. From a behavioral standpoint, an eight-minute queue plus a seven-minute pipeline is worse than a zero-minute queue plus a twelve-minute pipeline, even though the latter has a longer execution time.

Queue depth is governed by utilization. When your CI runner pool is at eighty percent utilization, queue times are noticeable. At ninety percent, they grow sharply. At ninety-five percent, they become the dominant contributor to feedback time. This follows directly from queuing theory: wait time grows non-linearly as utilization approaches capacity. Teams that carefully optimize pipeline execution while running a perpetually saturated runner pool are solving the wrong problem.

The other hidden contributor to time-to-signal is **failure readability**. A test that fails with `AssertionError: expected true, got false` and no additional context forces the developer to clone the build environment, reproduce the failure, and read the test source to understand what was being asserted. That investigation might take ten minutes. A test that fails with `User creation should return 409 when email already exists: expected status 409 but received 500; response body: {"error": "unique constraint violation on users.email"}` is actionable immediately. The effective feedback time includes the time the developer spends interpreting the failure. Writing better assertion messages is a pipeline speed optimization, even though it doesn't change execution time by a single millisecond.

## Tradeoffs and Failure Modes

### Fast but hollow

The most common failure mode of treating speed as a design constraint is gutting the pipeline to hit a time target. A team decides the pipeline should take five minutes, looks at a fifteen-minute pipeline, and cuts the integration tests. The pipeline is now fast and untrustworthy. Failures that integration tests would have caught now surface in staging or production, and the team learns that pipeline green doesn't mean the code works. Once that trust erodes, the pipeline becomes a bureaucratic checkbox rather than a safety mechanism.

The correct response to a pipeline that can't be made fast enough is not to remove stages but to restructure what runs when. Move expensive tests to a post-merge pipeline that runs against the main branch asynchronously. Keep the pre-merge pipeline fast and focused on the highest-probability failures. This creates a two-tier system: fast pre-merge feedback that catches most problems, and thorough post-merge validation that catches the rest before deployment. The tradeoff is that some failures are caught after merge rather than before, which means you need a mechanism (automated revert, deploy gates) to handle post-merge failures. This is a real cost, and you should acknowledge it rather than pretend the slow tests don't matter.

### Flaky tests as feedback poison

A flaky test — one that fails intermittently for reasons unrelated to the code change — destroys feedback loops disproportionately to its frequency. If you have two thousand tests and each has a 0.1% flake rate per run, the probability that at least one flaky test fails on any given pipeline run is `1 - 0.999^2000 ≈ 86%`. Eighty-six percent of your pipeline runs will contain a spurious failure. Developers will learn to re-run failures reflexively rather than investigating them. When a real failure occurs, it will be re-run too, caught on the second attempt only by luck if the flaky test happens to pass, and otherwise dismissed as "probably flaky." The signal-to-noise ratio collapses, and the pipeline becomes a slot machine rather than a diagnostic tool.

### The infrastructure cost of parallelism

Running stages in parallel requires proportionally more compute. A pipeline that runs ten test shards concurrently needs ten runners. At scale — hundreds of developers pushing multiple times per day — CI infrastructure becomes a significant budget line. There is a direct tradeoff between feedback speed and infrastructure cost, and the economically correct answer depends on engineer salaries, team size, and deployment frequency. For most teams, the cost of developer time lost to slow feedback exceeds the cost of additional CI runners by an order of magnitude, but this is an argument that must be made with numbers specific to your organization, not assumed.

## The Mental Model

Think of your pipeline as a **time budget**, not a sequence of tasks. Set the budget first — five minutes, eight minutes, whatever your team's behavioral threshold is — and then make design decisions about what fits. What runs pre-merge versus post-merge? What runs in parallel versus sequentially? What tests get written at which level of the test pyramid? These are all consequences of the time budget, not independent decisions.

The deeper shift is recognizing that **pipeline speed is not an engineering convenience — it is a direct input to integration frequency**, and integration frequency is the entire point of continuous integration. A team with a thirty-minute pipeline that pushes twice a day is doing automated building, not continuous integration. The speed of the feedback loop determines whether CI is a practice or just a tool.

## Key Takeaways

- Pipeline execution time is a design constraint that should be set before stages are defined, not a metric to be optimized after the pipeline is already slow.
- Developer behavior changes qualitatively at threshold points: under five minutes, feedback is synchronous; over ten, context-switching begins; over thirty, batching replaces frequent integration.
- Optimal stage ordering minimizes expected time to failure signal by running stages with the highest failure probability per unit time first, subject to dependency constraints.
- Parallelism only helps if it shortens the critical path; optimizing stages that are not on the critical path has zero effect on total pipeline duration.
- Time-to-signal includes queue wait time and failure interpretation time, not just pipeline execution duration — optimizing execution while ignoring queue depth solves the wrong problem.
- Moving expensive tests to a post-merge pipeline is a legitimate design choice, but it requires compensating mechanisms like automated reverts or deploy gates to maintain safety.
- Flaky tests degrade feedback loops non-linearly: even a 0.1% per-test flake rate across a large suite means most pipeline runs contain a spurious failure, training developers to ignore real ones.
- The economic argument for faster pipelines is almost always favorable — developer time lost to slow feedback typically exceeds additional infrastructure cost by an order of magnitude — but it must be made with your organization's specific numbers.

# Discussion

## Why This Conversation Is Happening

CI pipelines exist to change developer behavior: integrate small changes frequently, find problems quickly, and fix them while the change is still fresh in the author's head. When the pipeline is slow, that behavior breaks. Developers stop waiting for feedback, pick up other work, and come back later with half the context gone. A failure that should have taken two minutes to fix now costs a context switch, reconstruction time, and often a delayed response.

That delay creates second-order failures. People start batching changes so they do not "pay the pipeline cost" multiple times per day. Bigger batches mean harder code review, more painful merges, and failures that are harder to localize because many things changed at once. The pipeline may still be technically running on every push, but functionally it is no longer supporting continuous integration.

The article matters because teams often misclassify this as a mere speed problem: "make it faster later." But once a pipeline is built without a time budget, you usually end up with the wrong work in the wrong place, poor stage ordering, expensive bottlenecks, and feedback that arrives too late to influence behavior. The system still computes results correctly; it just computes them too late to be useful.

---

## What You Need To Know First

### 1. Continuous Integration (CI)
CI is the practice of merging and validating small changes frequently rather than letting lots of work pile up. The point is not just to run tests automatically; it is to catch integration problems while changes are still small and understandable. If developers start batching work into big pushes, the "continuous" part is gone even if the tooling still runs.

### 2. Dependency vs independence between stages
Some pipeline steps must happen before others. You cannot run unit tests before the code builds, and you usually should not trust integration test results if basic correctness checks have already failed. Other stages are independent and could run in either order or in parallel. This matters because optimization is only possible where ordering is flexible.

### 3. Parallelism and the critical path
Parallelism means running multiple pieces of work at the same time. But total elapsed time is not the sum of everything; it is controlled by the longest chain of dependent work. That longest chain is the critical path. If you speed up something outside that path, total pipeline time does not change.

### 4. Queueing in shared systems
If your CI system has limited runners, jobs may wait before they start. As utilization gets high, wait times can rise sharply rather than gradually. So "how long the pipeline takes to execute" and "how long the developer waits for feedback" are different things. The second one is what people feel.

---

## The Key Ideas, Connected

### 1. Pipeline speed is a design constraint, not a cleanup task.
The main point is that acceptable feedback time has to be decided before you design the pipeline, because that budget determines what kind of pipeline you can afford to build. If you wait until the pipeline is already fifteen or thirty minutes long, you are usually limited to local optimizations: shave a few seconds here, parallelize a bit there. But the bigger decisions — which tests run pre-merge, which run after merge, how stages are grouped, how much setup cost each stage carries — have already been made.

That leads directly to the next idea, because the reason speed must be designed in up front is not aesthetic. It is about how humans behave when feedback arrives at different times.

### 2. Feedback time changes developer behavior at thresholds, not smoothly.
A one-minute increase from three to four minutes barely changes workflow. A one-minute increase from nine to ten can push someone from "I am still in this change" to "I have moved on." The article's thresholds matter because they mark changes in behavior: under about five minutes, feedback is part of the same mental loop; beyond ten, context switching starts; beyond thirty, people stop treating the pipeline as something to wait on at all.

The mechanism is cognitive, not just temporal. Once a developer has switched tasks, the cost is no longer "pipeline time"; it is pipeline time plus the cost of reloading the original problem into working memory. That is why a fifteen-minute failure can act more like a thirty-minute interruption.

Once you understand that slow feedback changes behavior, the next idea becomes necessary: if time is behavior-shaping, then stage ordering is not arbitrary. It directly affects when useful failure signals arrive.

### 3. Stage ordering should minimize expected time to useful failure.
Each stage has at least two important properties: how long it takes, and how often it catches something wrong. A fast stage that often fails is disproportionately valuable because it can stop the pipeline early and give the developer a useful answer quickly. That is why "failure probability divided by execution time" is a useful ordering heuristic for independent stages: it estimates signal per second.

The deeper mechanism is expected wasted time. If you run a slow, low-yield stage before a fast, high-yield stage, then on every run where the later stage would have failed, you forced the developer to wait through work that did not improve the decision. You spent wall-clock time proving something less informative before checking something more informative.

But that ordering logic immediately runs into a real constraint: not all stages are reorderable. Some are technically dependent, and some are ordered for diagnostic clarity even if they could technically run elsewhere. That is why the pipeline becomes a constrained optimization problem rather than a simple sort.

### 4. Dependencies and diagnostic value constrain the "best" order.
Compile before unit tests is a hard dependency. Unit tests before integration tests is often a soft dependency: integration tests might technically run, but the resulting failures are harder to interpret if basic correctness is already broken. So the pipeline is not just trying to fail fast; it is trying to fail clearly.

That matters because the goal is actionable signal, not just early red status. A giant wall of downstream failures from one root cause is slower for humans than one early localized failure. This is the bridge to the next concept: even when you use parallelism to reduce elapsed time, what matters is still whether the resulting structure shortens the path to actionable signal.

### 5. Parallelism only helps if it shortens the critical path.
Teams often hear "parallelize more" and assume any concurrent work makes the pipeline faster. But wall-clock duration is determined by the longest dependent chain. If one branch still takes nine minutes, making another branch go from three minutes to one minute changes nothing about total completion time.

The mechanism is simple: the pipeline cannot finish until all required branches finish, so the slowest required branch dominates. That is the critical path. Optimization effort outside it improves resource usage or local efficiency, but not elapsed feedback time.

This leads to an important refinement: even inside a stage, parallelism is not free. If spinning up each shard has substantial setup cost, splitting work can actually increase time instead of reducing it.

### 6. Parallelism has overhead, so there is a crossover point where it becomes worth doing.
Every parallel shard needs environment setup, dependency installation, and orchestration. If that fixed overhead is large relative to the actual test runtime, you have multiplied setup cost more than you have reduced execution time. The result is a slower pipeline with more infrastructure usage.

So the benefit of parallelism depends on ratio, not ideology: large chunks of expensive work are good candidates; tiny chunks with heavy setup overhead are not. That is why things like image caching and pre-warmed environments matter so much — they reduce fixed setup cost and make parallel execution actually pay off.

Once you see the mechanics of execution time, the article adds a corrective: even total execution time is still not the whole thing the developer experiences.

### 7. Time-to-signal is broader than execution duration.
The developer does not care when the job starts running internally; they care when they get a useful answer. If the job waits eight minutes in queue and runs for seven, the experienced delay is fifteen. Likewise, if the test output is cryptic and takes ten minutes to decode, then the effective feedback loop includes that interpretation time too.

This matters because many dashboards foreground the wrong metric. They show "pipeline duration" while hiding queue delay and readability cost. A team can proudly reduce runtime from eight minutes to six while still giving developers fifteen-minute feedback because the runner pool is saturated or the failures are opaque.

That naturally leads to another failure mode: if the signals that do arrive are untrustworthy, then even fast feedback stops functioning as feedback.

### 8. Flaky tests poison the feedback loop because false failures train the wrong behavior.
A flaky test does more damage than its per-test failure rate suggests because many low-probability flakes aggregate across a large suite. With enough tests, "at least one spurious failure" becomes common. Developers adapt rationally: rerun first, investigate later, maybe never. That adaptation is deadly because it treats real and fake failures the same way.

The key mechanism is signal-to-noise collapse. Once the pipeline produces too many false alarms, the human system around it stops trusting red as meaningful. The pipeline still emits signals, but they no longer drive action reliably.

At that point, a team might be tempted to cut expensive or noisy stages just to recover speed and trust. That creates the next tradeoff.

### 9. A fast pipeline that stops checking important things is not actually a good pipeline.
If you remove slow integration checks just to hit a five-minute budget, you may improve latency while destroying confidence. Then "green" no longer means "safe enough to proceed." The pipeline becomes fast but hollow: good at returning quickly, bad at catching important classes of failure.

So the real design move is not always "make every important check fit pre-merge." Sometimes it is "split validation into tiers." Keep pre-merge focused on the fastest, highest-yield checks that preserve developer flow; move slower, lower-frequency, but still valuable checks to post-merge validation. But that only works if you add compensating controls such as deploy gates or automatic reverts, because now some failures are intentionally allowed to be discovered later.

This yields the final mental model: the pipeline is best understood as a budgeted system for delivering useful feedback quickly enough to preserve continuous integration behavior.

### 10. The right mental model is a time budget that shapes system design.
Instead of asking, "What stages should we include, and then how do we speed them up?", ask, "What is our acceptable time-to-signal budget, and what pipeline structure can deliver the highest-value signal inside it?" That question forces explicit tradeoffs: pre-merge versus post-merge, sequential versus parallel, cheap broad checks versus expensive deep checks, more runners versus more waiting.

The reason this is the correct framing is that pipeline speed is not just an efficiency concern. It directly affects integration frequency. And integration frequency is the whole reason CI exists. Once the feedback loop gets slow enough that developers batch changes, the system is no longer producing the behavior CI was meant to enable.

---

## Handles and Anchors

### 1. Treat the pipeline like a smoke alarm, not a forensic investigation.
A smoke alarm is useful because it goes off quickly enough to change what you do now. A perfect report delivered an hour later may contain better information, but it does not serve the same function. Pre-merge CI should act like the alarm: fast enough to interrupt the bad change before the developer has mentally left the room.

### 2. Ask: "What is the first useful red I can deliver?"
This is a good design question for any pipeline. Not "what can I run earliest?" and not "what is most comprehensive?" but "what gives the developer the fastest actionable failure signal?" That question naturally surfaces ordering, readability, dependencies, and whether a stage belongs pre-merge at all.

### 3. Core tension: trust, speed, and cost pull against each other.
You want feedback that is fast enough to preserve flow, trustworthy enough to drive action, and cheap enough to operate at scale. Over-optimize one dimension and you hurt another: fast but shallow, thorough but too slow, massively parallel but too expensive. Good pipeline design is choosing where to spend that budget deliberately.

---

## What This Changes When You Build

### 1. An engineer who understands this will set a time-to-signal budget before adding stages, because the budget determines pipeline shape.
The unaware default is to keep adding checks to the pre-merge pipeline until it becomes slow, then try to optimize afterward. That usually produces a bloated pipeline where every stage argues it is important and nothing fits cleanly. The aware engineer starts with something like, "pre-merge must return a useful answer within five to eight minutes," and then decides what belongs there versus in post-merge validation.

### 2. An engineer who understands this will order checks by expected signal value, not by convention alone, because early low-cost failures save disproportionate time.
The unaware default is often historical ordering: whatever got added first runs first. That can mean expensive suites run before cheap high-yield checks. The aware engineer asks which stages fail often, which are fast, and which ones make later failures easier to diagnose. They will happily put a ten-second lint or schema validation stage ahead of a ninety-second build step if it catches common mistakes earlier.

### 3. An engineer who understands this will optimize the critical path first, because improving non-bottlenecks does not reduce total feedback time.
The unaware default is to optimize the loudest or easiest target — often the test suite a team already knows well. The aware engineer maps the dependency graph, identifies the longest required chain, and spends effort there first. If integration setup plus integration tests dominate elapsed time, shaving thirty seconds off unit tests is not a pipeline speed win.

### 4. An engineer who understands this will measure queue time and failure readability alongside execution time, because developers experience end-to-end delay, not internal runtime metrics.
The unaware default is to celebrate lower execution duration while runner queues quietly grow or failures remain opaque. The aware engineer tracks push-to-first-actionable-signal. That can lead to very practical decisions: add CI capacity instead of rewriting tests, improve assertion messages instead of only chasing milliseconds, or reduce runner saturation instead of over-sharding jobs.

### 5. An engineer who understands this will treat flaky tests as a systemic reliability issue, not as minor annoyance, because false failures retrain developer behavior.
The unaware default is to tolerate occasional flakes and rely on reruns. The consequence is that rerun becomes the normal response to red builds, which destroys trust in the pipeline. The aware engineer quarantines, fixes, or removes flakes aggressively, because they understand that the pipeline's real job is not merely to run checks but to produce signals developers believe.

### 6. An engineer who understands this will split pre-merge and post-merge validation deliberately, because not all useful checks belong in the same feedback loop.
The unaware default is binary thinking: either every check must run before merge, or slow checks get deleted. The aware engineer sees a third option: a fast, trusted pre-merge gate for high-probability and high-actionability failures, plus slower post-merge checks with rollback or deployment protection. That preserves flow without pretending deep validation is unnecessary.
