## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers, when asked about idempotency in infrastructure, will say something like "it means you can run it twice and nothing bad happens." That sentence is correct the way saying "airplanes fly because of their wings" is correct — true, not useful, and dangerously incomplete when you need to debug why something went wrong at altitude. The real question is not *whether* an operation is idempotent. It is *what specific mechanism makes it idempotent*, which operations quietly violate that mechanism even inside tools that claim to provide it, and what actually happens to your infrastructure when idempotency breaks halfway through an apply. That is where the failures live, and it is where most practitioners have a gap.

## The Mathematical Property and the Operational Reality

Idempotency has a precise mathematical definition: an operation *f* is idempotent if applying it twice produces the same result as applying it once. Formally, *f(f(x)) = f(x)*. Setting a value to 5 is idempotent — do it ten times and you still have 5. Incrementing a value by 1 is not — do it ten times and you have shifted by 10.

This is useful as a foundation, but infrastructure operations are not pure functions. They execute against remote systems with latency, partial failure, concurrent actors, and side effects. The property you actually need is not the mathematical one. It is the operational one: **re-applying the same infrastructure definition to the same environment must converge to the same end state regardless of how many times you apply it, and without creating duplicate resources, corrupted configurations, or unintended side effects.** That is a much harder property to guarantee, and understanding how tools attempt to guarantee it — and where they fail — is the substance of this post.

## The Read-Diff-Apply Loop

Declarative IaC tools achieve idempotency through a single core mechanism. Every tool in this category — Terraform, Pulumi, CloudFormation, Crossplane — implements some version of the same loop:

**Read** the current state of the infrastructure. This might come from the state file, from a live API query to the cloud provider, or both. The tool needs to know what exists right now.

**Diff** the current state against the desired state declared in your configuration files. For every resource, the tool asks: does this resource exist? If it exists, do its attributes match what the configuration says they should be? If it does not exist, it needs to be created.

**Apply** only the changes necessary to close the gap. If a resource exists and matches, the tool does nothing — this is the **no-op** path, and it is where idempotency lives. If a resource exists but its attributes differ, the tool updates it in place or destroys and recreates it. If a resource does not exist, the tool creates it.

This loop is why running `terraform apply` twice in a row with no configuration changes produces no infrastructure changes on the second run. The read phase finds everything already matches, the diff is empty, and there is nothing to apply. That is not magic. That is the direct mechanical consequence of comparing desired state to current state and only acting on the delta.

The critical insight: **idempotency in declarative IaC is not a property of the apply step. It is a property of the entire loop.** If the read is wrong, or the diff is wrong, or the apply has side effects the tool does not track, idempotency breaks — even though the tool is still "declarative."

## What the State File Actually Does for Idempotency

The Level 1 post covered state management from an operational perspective. Here is why the state file is specifically load-bearing for idempotency.

When Terraform creates an AWS EC2 instance, the cloud provider returns an instance ID — say, `i-0a1b2c3d4e5f`. Terraform writes that ID into the state file, binding the logical resource in your configuration (`aws_instance.web`) to the physical resource in the real world (`i-0a1b2c3d4e5f`). On the next apply, Terraform does not ask AWS "is there an instance that matches this configuration?" It asks "what is the current state of `i-0a1b2c3d4e5f`?" and compares the answer to your configuration.

This binding is what prevents duplicate resource creation. Without it, the tool has no way to distinguish between "this resource does not exist yet and needs to be created" and "this resource exists but I have lost track of it." Lose the state file, and your next apply will attempt to create every resource from scratch — colliding with the existing infrastructure, creating duplicates, or failing on uniqueness constraints depending on the resource type and provider.

This also explains why **importing** existing infrastructure into state is not just an operational convenience — it is a prerequisite for idempotent management of resources that were created outside the tool. Until a resource is tracked in state, the tool cannot perform the read-diff-apply loop against it.

## Why Specific Operations Are Not Naturally Idempotent

Not all infrastructure operations fit cleanly into the declarative convergence model. Understanding which ones resist idempotency and why is essential.

**Resource creation with server-generated values.** When you create a resource, the provider often generates values that become part of the resource's identity: randomly assigned IPs, auto-generated names, UUIDs. If the creation succeeds but the state file write fails (network error, process killed, state lock timeout), you have a resource that exists in the real world but is not tracked. The next apply sees the resource as missing from state and attempts to create it again. This is the **orphaned resource** problem, and it is the most common way idempotency breaks in practice.

**Operations with external side effects.** Consider a Terraform resource that provisions an AWS RDS database. The database creation itself is idempotent through the state-tracking mechanism. But if your configuration also uses a `provisioner` block to run a SQL script that seeds initial data, that script runs every time the resource is created. If the resource gets tainted and recreated, the script runs again. If the script is not itself idempotent (e.g., it uses `INSERT` rather than `INSERT ... ON CONFLICT DO NOTHING`), your second apply corrupts your data. The IaC tool's idempotency does not extend to the code it shells out to.

**Append-only or cumulative operations.** Some cloud resources have attributes that accumulate rather than converge. Adding an inline IAM policy statement, appending a CIDR block to a security group rule list, or adding a tag — if the tool models these as "add this item" rather than "ensure this exact set exists," repeated application grows the list. Most mature providers model these correctly as the full desired set, but edge cases exist, particularly with less-maintained providers or modules that use imperative escape hatches.

**`null_resource` and local-exec provisioners.** These are explicit escape hatches from the declarative model. A `null_resource` with a `local-exec` provisioner runs an arbitrary shell command. The tool has no way to determine whether the effect of that command already exists. It runs it every time (or when triggered). Idempotency of these operations is entirely your responsibility.

```hcl
resource "null_resource" "run_migration" {
  triggers = {
    schema_version = var.schema_version
  }
  provisioner "local-exec" {
    command = "python run_migrations.py --version ${var.schema_version}"
  }
}
```

If `run_migrations.py` is not itself idempotent, this resource is a landmine in your pipeline. The IaC tool has no opinion about what that script does. It runs it when the trigger changes. Everything beyond that is on you.

## The Partial Apply Problem

Idempotency is often discussed as if applies are atomic — they either fully succeed or fully fail. They are not. A `terraform apply` that provisions fifteen resources might succeed on the first twelve and fail on the thirteenth. You now have a partially applied state. The state file reflects the twelve resources that were created. Your configuration declares fifteen.

The next apply picks up from where it failed: it sees the twelve resources exist and match (no-op), and attempts to create the remaining three. **This is idempotency working correctly under partial failure** — and it is one of the most practically important properties of the state-tracking model. The tool does not re-create the first twelve resources. It converges toward the full desired state.

But this only works because the state file was updated incrementally as each resource was created. If the state file update fails (the state backend is unavailable, the lock is broken), you get a divergence between the state file and reality. The tool thinks the resource does not exist; the cloud provider knows it does. Now your next apply will either fail with a conflict or, worse, create a duplicate.

This is why state locking is not an operational nicety. **State locking is a correctness requirement for idempotency.** Without it, two concurrent applies can each read the same initial state, each decide to create the same resource, and produce duplicates that neither state file knows about.

## Idempotency at the Pipeline Level

Individual resource-level idempotency is necessary but not sufficient. In a real IaC pipeline, you often have multiple stages: perhaps one that provisions networking, another that provisions compute, another that configures DNS. Each stage might be idempotent in isolation, but the pipeline as a whole has ordering dependencies.

If stage two fails and you re-run the entire pipeline, stage one runs again. If stage one is truly idempotent, this is a no-op and the pipeline proceeds to retry stage two. If stage one has any non-idempotent side effects — say, it rotates an API key as part of its apply — then re-running the pipeline from the top invalidates the work that stage two partially completed in its first attempt. You now have infrastructure that references a key that no longer exists.

**Pipeline-level idempotency requires that every stage is idempotent, and that the side effects of each stage do not invalidate the completed work of downstream stages on re-execution.** This is a design constraint that must be intentional. It does not emerge automatically from using declarative tools.

## Where Drift Breaks the Contract

Idempotency assumes that the tool's model of reality is accurate. Configuration drift — changes made outside the tool — breaks this assumption. If someone manually changes a security group rule through the AWS console, the state file still reflects the old rule. On the next apply, the tool's diff will detect the discrepancy and attempt to revert the manual change back to the declared state. This is actually idempotency working as intended — the system converges to the declared state.

But it is only safe if the declared state is actually correct. If the manual change was a critical hotfix for an active incident, reverting it automatically could re-open the vulnerability. The tool is not wrong — it is doing exactly what it was designed to do. The failure is in the process that allowed a change to be made outside the tool without updating the configuration. This is a human-systems problem that the tool's idempotency guarantee actively surfaces rather than hides.

## The Mental Model

Idempotency in infrastructure is not a feature you get for free by choosing a declarative tool. It is the emergent property of a correctly functioning read-diff-apply loop. The loop requires three things to hold: the tool must accurately know current state (the read), it must correctly compute the difference against desired state (the diff), and the operations it executes must not produce effects outside what the tool tracks (the apply). When any of these break — lost state, concurrent modification, untracked side effects, imperative escape hatches — idempotency degrades.

The practical question to carry into every IaC design decision is not "is this tool idempotent?" but "**does every operation in this pipeline preserve the read-diff-apply loop?**" Any provisioner, any external script, any manual change, any untracked side effect is a place where the loop can break. Idempotency is not binary. It is the degree to which your entire system — tool, configuration, pipeline, and operational discipline — maintains the integrity of that loop.

## Key Takeaways

- Idempotency in IaC is mechanically produced by the read-diff-apply loop: read current state, diff against desired state, apply only the delta — which makes a second apply a no-op when nothing has changed.

- The state file is the binding between logical resources in your configuration and physical resources in the real world; losing it breaks the tool's ability to distinguish "needs to be created" from "already exists," which directly breaks idempotency.

- State locking is not an operational convenience — it is a correctness requirement, because concurrent applies against the same state can produce duplicate resources that neither run tracks.

- Provisioners, `local-exec` blocks, and arbitrary scripts are escape hatches from the declarative model, and their idempotency is entirely your responsibility — the tool cannot verify or enforce it.

- Partial applies are the normal failure mode in infrastructure operations; idempotency means the next apply picks up where the last one failed, but only if the state file accurately reflects what was actually created.

- Pipeline-level idempotency requires more than idempotent stages — it requires that re-running an earlier stage does not invalidate the completed work of later stages through side effects like key rotation or credential regeneration.

- Configuration drift does not break idempotency — it triggers convergence back to declared state, which is only safe if the declared state is actually the correct state, making out-of-band changes a process problem that the tool will faithfully enforce.

- The right question is never "is this tool idempotent?" but "does every operation in this pipeline preserve the integrity of the read-diff-apply loop?"

# Discussion

## Why This Conversation Is Happening

Infrastructure changes rarely happen in a clean, single-shot world. Applies get interrupted, networks flap, pipelines retry, humans click in cloud consoles, and scripts run twice because a job was re-queued. If your mental model of idempotency is only "safe to run again," you will miss the exact places where that safety depends on state tracking, locking, and the absence of hidden side effects. Then the failures look mysterious: duplicate resources, orphaned instances, reverted hotfixes, or a pipeline that becomes less reliable every time it retries.

What breaks in practice is not usually the happy path. It is the recovery path. A resource gets created but not recorded in state. Two applies run at once and both think they should create the same thing. A provisioner seeds data twice because a resource was recreated. A manual emergency fix is silently undone on the next apply. These are not edge-case trivia; they are the normal ways infrastructure systems fail under real operational pressure.

So this topic matters because idempotency is the property that makes retries, partial failure recovery, and repeated pipeline execution survivable. If you do not understand the mechanism that produces it, you cannot tell when you still have it and when you have already stepped outside it.

---

## What You Need To Know First

### 1. Declarative vs imperative infrastructure
A declarative tool says what end state you want: "there should be one database with these settings." An imperative tool says the steps to perform: "create database, then set parameter X, then attach policy Y." Idempotency is easier in declarative systems because the tool can compare desired state to current state and decide whether anything needs doing. In imperative systems, repeating the same steps may repeat the side effects too.

### 2. State in IaC
State is the tool's record of what real-world resources correspond to the things named in your configuration. If your config says `aws_instance.web`, the state file tells the tool which actual EC2 instance that means. Without that mapping, the tool cannot reliably tell "this already exists" from "I need to create it."

### 3. Drift
Drift means the real infrastructure changed without the configuration changing—usually because someone edited something manually or another system touched it. Once drift exists, the tool's stored view and reality are no longer aligned. The next apply will try to reconcile them.

### 4. Side effects
A side effect is any effect beyond the narrow resource change the tool is tracking. Creating a database is one thing; running a script that inserts rows into it is another. IaC tools can often track the first kind well, but they usually cannot see or reason about the second kind.

---

## The Key Ideas, Connected

### Idempotency in infrastructure is not just a definition; it is an operational guarantee about convergence.
The mathematical definition—doing something twice has the same result as doing it once—is the right starting point, but infrastructure is not a pure math function. Real applies touch remote APIs, depend on network calls, and can succeed only partly. So the useful version of idempotency is: if you apply the same desired definition again, the system should move toward the same intended end state without duplicating or corrupting things.

That broader meaning immediately creates a question: what mechanism actually makes repeated applies converge instead of repeat work? That leads to the core loop.

### Declarative IaC tools create idempotency through a read-diff-apply loop.
The tool first reads what it believes exists, then computes the difference between current and desired state, then applies only the required changes. If the diff is empty, the tool does nothing. That no-op path is the practical expression of idempotency.

This matters because it shows idempotency is not located in "apply" alone. Apply is only safe because read correctly identified reality and diff correctly computed the gap. If either of those is wrong, apply can confidently do the wrong thing. That is why the next idea—the role of state—is load-bearing.

### State is the binding that lets the tool know which real resource it is managing.
A config name like `aws_instance.web` is only a logical label. The state file ties that label to a specific physical object, such as a concrete EC2 instance ID. On a later run, the tool does not search the cloud for "something kind of like my web server"; it asks about that exact known resource and compares it to the declared configuration.

That binding is what prevents duplicate creation. If the tool loses the mapping, it cannot distinguish "resource missing from state because it doesn't exist" from "resource missing from state because I lost my record." Once you see that, you can understand why import matters and why state loss is not just inconvenient—it directly breaks idempotent management.

### Idempotency depends on tracked identity, so anything created outside state is unmanaged until imported.
If a resource exists but is not in state, the tool cannot include it correctly in the read-diff-apply loop. It has no identity link to read from. That means repeated applies are no longer converging against the real thing you care about; they are operating against an incomplete model.

This leads to a deeper point: some operations are hard to fit into this model even when you are using a declarative tool, because not all effects have a stable, tracked identity.

### Some infrastructure operations are not naturally idempotent because their effects are cumulative, hidden, or only partially tracked.
A create call may succeed in the provider but fail before the tool records the returned ID. A script may mutate a database in ways the tool cannot observe. A command may append to a list rather than enforce an exact set. In all of these cases, repeating the operation is not "compare and no-op"; it is "do another side effect."

The orphaned resource example is especially important mechanically: if the provider created the resource but the state write failed, the next apply sees absence in state, not existence in reality, and attempts another creation. The failure comes from the loop being broken between apply and state persistence. Once you understand that, partial applies make more sense.

### Partial applies are normal, and idempotency is what makes recovery possible.
Infrastructure runs are usually not atomic. One run may create some resources successfully, fail later, and stop. If state was updated as those successful resources were created, the next run can read that partial progress, diff against the remaining desired state, and continue from where it left off.

So partial failure is not the opposite of idempotency; it is one of the main situations where idempotency proves its value. But that only holds if the state accurately reflects what succeeded. If state persistence is broken, recovery turns into duplicate creation or conflict. That is why locking becomes necessary, not optional.

### State locking is required because concurrent applies can invalidate the read step.
If two runs start from the same old state at the same time, each may conclude that a resource does not yet exist and each may try to create it. This is not a bug in the apply step alone; it is a race caused by both runs reading an outdated snapshot and diffing from it independently.

Locking preserves the integrity of the loop by ensuring only one writer is making decisions from a given state view at a time. Without that serialization, the system no longer has a single coherent read-diff-apply cycle. Once you accept that, you can extend the idea beyond one tool invocation to the whole delivery pipeline.

### Pipeline-level idempotency is harder because stages can interfere through side effects.
A networking stage, compute stage, and DNS stage may each be individually rerunnable, but the pipeline is only rerunnable if repeating an earlier stage does not invalidate later work. For example, if a retry of stage one rotates credentials, stage two's previously completed work may now point at expired secrets.

This shows that idempotency is compositional only under conditions. The parts must each be rerunnable, and their side effects must not break each other across retries. That same theme appears again with drift.

### Drift does not break idempotency; it changes what the system converges toward.
If someone manually changes a resource, the next apply detects that reality differs from the declared state and pushes reality back toward the declaration. Mechanically, the loop is still working: read found a difference, diff identified it, apply reconciled it.

The danger is social, not algorithmic. If the manual change was the right emergency fix and the declaration is now stale, the tool will faithfully restore the wrong thing. So idempotency is not the same as correctness of intent. It guarantees consistent convergence to the declared state, not that the declared state is wise. That is the final mental model.

### Idempotency is an emergent property of the whole system preserving the read-diff-apply loop.
You do not "have idempotency" just because your tool advertises it. You have it to the extent that the tool can accurately read current state, compute the right diff, and apply changes without important untracked side effects. Lose state, allow concurrent writers, add imperative scripts, or tolerate unmanaged drift, and you have weakened the loop.

So the practical question is not "is Terraform idempotent?" or "is this tool declarative?" The practical question is: for this specific operation and this specific pipeline, does the system still preserve a trustworthy read-diff-apply cycle?

---

## Handles and Anchors

### 1. Think of state as the claim ticket at a coat check
Your configuration says "I own a coat." The state file is the ticket that tells the system which exact coat is yours. Lose the ticket, and the attendant cannot safely match you to the existing coat; they may hand you a new one, reject you, or create a mess. Idempotency depends on having that ticket.

### 2. Core sentence: idempotency lives in the no-op
The important question is not whether a tool can create resources. Many things can do that. The question is whether, after reading reality, it can correctly decide to do nothing when nothing needs changing.

### 3. Diagnostic question for any new mechanism
Ask: "If this step runs again after partial failure, how does it know what it already did?"  
If the answer is "it checks tracked state and compares against desired state," you may still be inside the safe model. If the answer is "it just reruns the command" or "it probably won't happen," you have found an idempotency risk.

---

## What This Changes When You Build

### 1. An engineer who understands this will treat state storage and locking as correctness infrastructure, not admin overhead.
They will choose a remote backend with locking, durability, and team-safe access because concurrent applies and lost state are direct idempotency failures. The unaware engineer often treats local state or weakly managed shared state as acceptable "until later," and inherits race conditions, duplicate creation, and painful recovery when a run dies mid-apply.

### 2. An engineer who understands this will be suspicious of provisioners, `local-exec`, and out-of-band scripts because the tool cannot diff their effects.
They will either avoid these escape hatches, make the scripts explicitly rerunnable, or isolate them behind systems that have their own convergence model. The unaware engineer often assumes "it's in Terraform, so it's idempotent," and discovers only during retries that a migration ran twice, seed data duplicated, or a shell command produced cumulative changes.

### 3. An engineer who understands this will design retries around partial success rather than assuming all-or-nothing execution.
They will expect some resources to be created before failure and will verify that successful creations are recorded durably before re-running. The unaware engineer often assumes failure means "nothing happened," reruns blindly, and is surprised by conflicts, duplicates, or strange provider errors caused by real infrastructure existing outside trusted state.

### 4. An engineer who understands this will model resources as exact desired sets rather than additive commands whenever possible.
For things like security rules, tags, policy statements, and memberships, they will prefer "ensure this full set exists" over "append this one more item." The unaware engineer often inherits additive patterns from scripts or weak modules, which makes repeated runs grow state instead of converge.

### 5. An engineer who understands this will treat manual fixes and pipeline stage side effects as design inputs, not exceptions.
They will ask how emergency changes are folded back into config, and whether rerunning an earlier stage invalidates outputs used later. The unaware engineer often assumes stage-level idempotency is enough, then finds that retries rotate keys, replace credentials, or revert hotfixes in ways that make the overall pipeline non-idempotent even though each step looked fine in isolation.
