## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers who use Terraform, CloudFormation, or Pulumi can articulate the declarative-imperative distinction. Declarative means you describe the desired end state; imperative means you describe the steps. That definition is correct and almost entirely insufficient. It tells you the shape of the idea but nothing about the machinery that makes it work. And the machinery is where every real problem lives.

The practical question is not "what is declarative infrastructure?" It is: what does a declarative tool actually *do* when you hand it a configuration and run apply? What computational model makes idempotency fall out as a structural property rather than something you have to hand-implement? What makes drift detection mechanically possible? And what exactly breaks when you — knowingly or not — violate that model?

These are the questions that determine whether you use declarative tools effectively or whether you fight them for years while producing the exact brittleness IaC was supposed to eliminate.

## The Reconciliation Engine

A declarative infrastructure tool is, at its core, a **reconciliation engine**. It takes two representations of the world — what you said you want, and what currently exists — and computes the minimal set of operations needed to transform the latter into the former. That computation is the entire value proposition. Everything else is ergonomics.

But the actual mechanics involve not two, but three distinct representations of state, and understanding their interplay is what separates a working mental model from a broken one.

### Three States, Not Two

When you run `terraform plan`, the tool is working with three inputs:

**Desired state** is what your `.tf` files declare. This is the configuration you wrote: the resources, their attributes, their relationships. It is the source of truth for intent.

**Recorded state** is the state file — the tool's internal record of what it believes currently exists in the real world, including resource IDs, computed attributes, and metadata from the last successful apply. The Level 1 post covered why this file must be stored centrally and locked during operations. What it didn't cover is *why the file exists at all*.

**Actual state** is what really exists in the target environment right now — the actual cloud resources, their actual attributes, their actual configurations as reported by provider APIs.

The reconciliation process works in a specific sequence. First, the tool **refreshes**: it queries the real infrastructure through provider APIs and updates the recorded state to reflect the actual state. Then, it **diffs**: it compares the desired state against the now-refreshed recorded state and produces a set of planned operations — create, update, or destroy — for each resource where the two diverge. Then, on apply, it **executes** those operations in dependency order and **records** the results back into the state file.

This three-way model exists because of a problem that seems simple until you actually think about it: the tool needs to know what it is *responsible for*. If your configuration declares one EC2 instance and there are fourteen instances in the AWS account, the tool cannot simply look at the desired state and the actual state and figure out what to do. It needs to know: which of those fourteen instances did *I* create? Which one is mine to manage? The state file answers that question. It is the tool's memory of what it has previously provisioned and what it is therefore responsible for tracking, updating, and destroying.

Without the state file, a declarative tool would have no way to distinguish "this resource should exist because I declared it and already created it" from "this resource should be created because I declared it and it doesn't exist yet." It would also have no way to handle destruction — if you remove a resource from your configuration, the tool needs the state file to know that a real resource in the world corresponds to that now-absent declaration and should be destroyed.

### The Dependency Graph

Declarative configurations specify *what* should exist, not the order in which things should be created. But order matters — you cannot create a subnet before the VPC it belongs to. Declarative tools resolve this through a **directed acyclic graph** (DAG) of dependencies.

When you write something like this:

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "web" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}
```

The reference `aws_vpc.main.id` in the subnet resource creates an implicit dependency edge. The tool builds a graph of all such edges across your entire configuration, then performs a topological sort to determine the creation order. Resources without dependencies on each other can be created in parallel. Destruction follows the reverse order — the subnet must be destroyed before the VPC.

This graph is not incidental to the declarative model; it is essential to it. An imperative script encodes ordering in the sequence of its lines. A declarative configuration *cannot* encode ordering that way — it has no sequential execution model. The graph is the mechanism that replaces it. When you see `terraform plan` output showing "14 to add, 3 to change, 2 to destroy," the tool has already solved the graph and determined a valid execution order for all nineteen operations.

### How Idempotency Emerges

The Level 1 post defined idempotency as "producing the same result when applied multiple times." At the mechanical level, idempotency is not a feature the tool implements per-resource. It is a structural consequence of the diff-based model.

An imperative script says: "create a server." Run it again, and it creates another server, because the script has no concept of existing state — it just executes instructions. A declarative tool says: "a server with these properties should exist." On the first run, the diff shows "server does not exist → create." On the second run, the refresh finds the server, the diff shows "server exists and matches desired state → no operation." On the third run, the same. The idempotent behavior emerges from the fact that the tool computes a delta each time rather than executing a fixed sequence. When the delta is zero, the tool does nothing.

This also means idempotency can *break* at the provider level. If a cloud provider's API reports a resource attribute differently each time it's queried — a timestamp that updates, an ordering of tags that isn't stable — the tool will see a diff where none meaningfully exists, and it will propose an update on every run. This is a common source of "phantom diffs" in Terraform plans and is not a bug in the model but a friction point between the model's assumptions and the real behavior of provider APIs.

### Drift Detection as a Consequence

Drift detection is often presented as a feature. It is more accurate to call it a byproduct. The refresh step — where the tool queries actual infrastructure and compares it to recorded and desired state — inherently detects drift. If someone manually changed a security group rule, the refresh will pick it up, and the plan will propose reverting it.

But drift detection has real mechanical limitations. It only happens when you run the tool. Between runs, drift accumulates silently. Some tools offer scheduled drift detection (CloudFormation's drift detection feature, for example), but this is polling, not real-time monitoring. Kubernetes takes a fundamentally different approach: its controllers run a **continuous reconciliation loop**, constantly comparing desired state (the manifests in etcd) to actual state (the cluster) and converging. This is the difference between **one-shot convergence** (Terraform: run, converge, stop) and **continuous convergence** (Kubernetes: converge forever). Both are declarative, but they have radically different operational characteristics around drift.

There is also the question of *what* is checked. Not every attribute of every resource is compared during refresh. Computed attributes that the user didn't set may or may not be tracked. Some resources have attributes that change frequently for legitimate reasons — an auto-scaling group's current instance count, for example — and treating that as "drift" would be counterproductive. Declarative tools handle this through a combination of attribute-level configuration (marking attributes as ignored), provider-level logic, and lifecycle rules. This complexity is invisible when things work and extremely visible when they don't.

## Where the Model Breaks: Tradeoffs and Failure Modes

### Using Declarative Tools Imperatively

This is the most common and most damaging failure mode, and it is exactly what the Level 1 post warned about. It happens when engineers treat a declarative tool as a script runner rather than a reconciliation engine.

**Targeted applies** are the most frequent symptom. `terraform apply -target=aws_instance.web` tells Terraform to only apply changes to one resource, skipping the rest of the graph. This is sometimes necessary for emergency fixes, but used routinely, it produces state files that diverge from both the configuration and reality. The state file now reflects a partial apply — some resources are up to date, others are not — and subsequent full plans become unpredictable.

**Manual changes followed by plan/apply** is the other common pattern. An engineer modifies a resource through the console — adds a tag, changes a security group rule — then runs `terraform plan`. The tool sees the drift and proposes reverting the manual change. If the engineer doesn't understand why, they might run `terraform apply` and blow away a critical production fix, or they might add `-target` to avoid the revert, compounding the problem.

**Imperative escape hatches** are the subtler form. Terraform's `null_resource` with a `local-exec` provisioner, or `provisioner "remote-exec"` blocks, are imperative code embedded inside a declarative framework. They run shell commands on create or destroy. They have no drift detection, no diff, no reconciliation. They execute every time the resource is tainted or recreated, and they do whatever the script says regardless of current state. Leaning on these mechanisms means you have opted out of the declarative model for that piece of infrastructure while still appearing to use it — which is worse than writing a standalone script, because at least a standalone script doesn't give the illusion of declarative management.

### The State File as a Single Point of Failure

The reconciliation model requires the state file. If the state file is lost, corrupted, or significantly out of sync with reality, the tool cannot function. It does not know what it owns. `terraform plan` against a fresh state file will propose creating every resource from scratch, which means duplicating everything that already exists. Recovering from state file loss on a large infrastructure is a manual, resource-by-resource `terraform import` operation that can take days. Teams that don't take state file durability seriously — encrypted, versioned, backed up, access-controlled — are operating without a safety net and will eventually find out.

### The Expressiveness Ceiling

Declarative models are powerful when the desired state can be expressed as a static graph of resources with fixed attributes. They strain when the desired state depends on runtime conditions, complex conditional logic, or multi-phase orchestration. "Create this resource, wait for it to become healthy, then use its output to configure these other resources" is straightforward. "If this resource fails to create, fall back to a different configuration in a different region" is not something declarative models handle natively. This is where teams either layer imperative orchestration on top (CI/CD pipelines wrapping Terraform runs with conditional logic) or accept that some infrastructure workflows will live outside the declarative model.

## The Mental Model to Carry Forward

A declarative infrastructure tool is a **diff engine operating over a dependency graph against a three-state data model**. The three states are desired (your configuration), recorded (the state file), and actual (reality). The tool refreshes actual state, diffs it against desired state, computes a plan that respects the dependency graph, and applies the minimum operations needed to converge. Idempotency and drift detection are not features bolted on — they are structural consequences of this computational model.

Every time you do something that bypasses or corrupts one of these three inputs — editing infrastructure manually, running targeted applies routinely, relying on imperative provisioners, losing the state file — you are degrading the model's ability to reconcile. The tool does not become less useful incrementally. It degrades in a step function: the reconciliation model works until it doesn't, and when it doesn't, you are back to the manual archaeology that IaC was supposed to eliminate, except now you also have a state file that's lying to you.

The question to ask of any infrastructure operation is: *does this preserve the reconciliation model, or does it break it?* If you can answer that, you can use any declarative IaC tool — Terraform, CloudFormation, Pulumi, Crossplane — and understand not just what it does, but why.

## Key Takeaways

- A declarative IaC tool operates on three representations of state — desired (configuration), recorded (state file), and actual (real infrastructure) — and reconciliation depends on all three being accurate.
- The state file exists to track what the tool is responsible for; without it, the tool cannot distinguish between resources it should manage and resources it should ignore.
- Idempotency is not a per-resource feature but a structural property of the diff-based reconciliation model: when desired state equals actual state, the computed delta is empty, so nothing happens.
- Drift detection is a byproduct of the refresh step, not a separate feature — it only occurs when the tool runs and is subject to attribute-level granularity limits.
- One-shot convergence (Terraform) and continuous convergence (Kubernetes controllers) are both declarative but have fundamentally different drift characteristics: one detects drift on demand, the other remediates it continuously.
- Using `terraform apply -target`, making manual infrastructure changes, or relying on imperative provisioners all break the reconciliation model in ways that compound over time and produce state files that diverge from reality.
- State file loss on a large infrastructure is a multi-day recovery event; treating the state file with anything less than the same durability guarantees as a production database is an operational risk.
- The declarative model has an expressiveness ceiling — complex conditional logic, fallback strategies, and multi-phase orchestration typically require imperative orchestration layered on top, and recognizing where that boundary is prevents misuse of the declarative layer.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Teams adopt Terraform, CloudFormation, or Pulumi because handwritten infrastructure scripts and console clicks become unreliable fast. The same script run twice creates duplicates. A manual hotfix in the cloud console gets silently overwritten later. A resource is deleted from code, but nobody can tell whether the tool will remove the real thing, recreate it, or ignore it. The promise of declarative IaC is that the tool can reason about the gap between “what we want” and “what exists” and close that gap safely.

That promise only holds if you understand the machinery underneath. If you treat a declarative tool like a fancy shell script, you create the exact failures IaC was meant to prevent: plans that constantly show weird diffs, targeted applies that leave state half-updated, manual production changes that get reverted by surprise, and state loss that turns a normal deploy into days of resource import and cleanup.

The practical reason to care is simple: these tools are not just “config-driven provisioning.” They are reconciliation systems. If you don’t hold that model, your day-to-day actions will accidentally break the assumptions the tool relies on, and once those assumptions break, the tool stops being predictable.

---

## What You Need To Know First

**1. Desired state vs actual state**  
Desired state is the configuration you wrote: “there should be one VPC, two subnets, this security group, this instance.” Actual state is what really exists in AWS, Azure, or wherever right now. Declarative systems work by comparing those two and trying to make reality match the declaration.

**2. Resource identity**  
A resource is not just “an EC2 instance” in the abstract; it is a specific real object with an ID assigned by the provider. The tool needs a stable way to know which real object corresponds to which thing in your config. Without that mapping, it cannot tell whether something should be updated, created, or destroyed.

**3. Dependency graphs**  
Some infrastructure can only be created after other infrastructure exists. A subnet depends on a VPC; an instance may depend on a subnet and security group. Declarative tools represent these relationships as a graph, then compute an order that respects those dependencies.

**4. Idempotency**  
An operation is idempotent if running it again produces the same end result instead of repeating side effects. In infrastructure, that usually means “run apply again and it should do nothing if the world already matches the config.” The article’s key point is that declarative tools get this from their model, not from manually coding “if exists, skip.”

---

## The Key Ideas, Connected

**A declarative IaC tool is fundamentally a reconciliation engine.**  
That means its real job is not “run provisioning commands.” Its job is: look at what you want, look at what exists, compute the difference, then perform the minimum operations needed to close that difference. This is the core behavior that makes declarative IaC different from a script. A script executes instructions because you told it to; a reconciliation engine decides what actions are necessary based on the current gap.  
Once you see the tool this way, the next question becomes: what information does it need in order to reconcile correctly?

**To reconcile correctly, the tool needs three states, not just desired and actual.**  
At first glance, you might think desired state and actual state are enough. But they are not, because the tool also needs memory: what resources it previously created and therefore owns. That is the recorded state, typically the Terraform state file. Desired state tells the tool your intent. Actual state tells it what the provider says exists. Recorded state tells it which real resources correspond to which declarations in your config.  
This extra state becomes necessary because real environments contain many things the tool did not create. Without recorded state, the tool cannot answer basic ownership questions like “which of these fourteen instances is the one my config refers to?” That ownership problem is why the state file exists at all.

**The state file is the tool’s memory of responsibility.**  
This is the mechanical reason state matters so much. It is not just a cache for performance. It is the mapping between abstract declarations and concrete cloud objects. If a resource disappears from configuration, the tool uses recorded state to know that there is a corresponding real object to destroy. If a resource remains in configuration, the tool uses recorded state to know which existing object to inspect and update.  
Once the tool has desired, recorded, and actual state, it can perform a specific sequence: refresh actual into recorded, diff desired against that refreshed view, then plan changes. That sequence leads directly to the next key mechanism: execution order.

**Because declarative config does not specify step-by-step order, the tool must derive order from a dependency graph.**  
In an imperative script, the order is the script itself: line 1, then line 2, then line 3. In a declarative config, resources are declarations, not steps. So the tool needs another way to know that a subnet must wait for a VPC. It gets that from references and explicit dependency metadata, which form a directed acyclic graph.  
The graph is what turns “what should exist” into “what can be created now, what must wait, and what can run in parallel.” Without the graph, the tool would know *what* needs to change but not *in what safe order* to apply those changes.

**The diff plus graph model is what makes idempotency emerge naturally.**  
An imperative command like “create server” has the same instruction every run, so if you run it twice, it may create two servers unless you manually guard against that. A declarative engine does something different each run: it recalculates the delta between desired and current reality. On the first run, the delta may be “server missing, create it.” On the second run, after refresh, the delta may be empty. If the delta is empty, there is nothing to execute.  
So idempotency is not magic and not a special flag on the resource. It falls out of the fact that the tool recomputes desired-vs-current each time instead of replaying a fixed command list. That also explains why idempotency can fail in practice: if the provider reports unstable values, the diff is never truly empty.

**Phantom diffs happen when the model expects stable comparisons but the provider API does not provide them.**  
If an attribute changes representation every time it is read—a timestamp, a reordered list, a computed field that flips around—the tool sees “difference” even if nothing meaningful changed. It then plans an update every run. The engine is still doing the correct thing according to its model; the problem is that the underlying inputs are noisy.  
This matters because it shows that reconciliation depends on trustworthy observation of actual state. Once the tool can refresh and compare actual state, another behavior appears automatically: drift detection.

**Drift detection is a consequence of refresh, not a separate superpower.**  
When the tool asks the provider for current resource attributes during refresh, it is already checking whether reality still matches the last known and desired state. If someone changed a security group manually in the console, that divergence appears during refresh and then shows up in the plan. So drift detection is just reconciliation noticing that actual state no longer aligns with intent.  
That also exposes its limits: the tool only detects drift when it runs, and only for attributes it knows how to track and compare. This is why Terraform’s drift behavior feels very different from Kubernetes.

**One-shot reconciliation and continuous reconciliation are the same idea run on different schedules.**  
Terraform typically reconciles when a human or pipeline runs plan/apply: observe, compute delta, act, stop. Kubernetes controllers run that loop continuously: observe, compute delta, act, repeat forever. Mechanically they are both declarative systems, but operationally they behave differently because one polls on demand and the other keeps watching and correcting.  
This difference matters because it shapes how drift accumulates. In one-shot systems, drift can sit unnoticed between runs. In continuous systems, drift is often short-lived because the controller tries to correct it quickly.

**The model breaks when you bypass one of its inputs or its execution rules.**  
Manual console changes alter actual state outside the tool. Targeted applies intentionally execute only part of the graph. Imperative provisioners perform side effects that are not represented in diff/reconcile terms. Losing the state file destroys recorded state entirely. In each case, the tool’s picture of the world becomes incomplete or misleading.  
That is why these are not just “bad practices” in a moral sense. They are specific ways of violating the reconciliation model. If the model needs accurate desired, recorded, and actual state plus graph-based execution, then anything that corrupts those pieces reduces correctness.

**The state file is therefore a hard operational dependency, not a convenience artifact.**  
If recorded state is gone, the tool loses its memory of ownership. It may propose creating resources that already exist because it no longer knows it created them before. Recovery then becomes manual mapping: importing real resources back into state one by one.  
This follows directly from the earlier mechanics. If recorded state is one of the three required inputs, then durability of the state file is as important as durability of any other critical system record.

**Declarative IaC also has an expressiveness ceiling because reconciliation works best on stable desired end states, not dynamic control flow.**  
The model is excellent at “these resources should exist with these relationships.” It is weaker at workflows like “try region A, and if that fails, switch to region B,” or “wait for a health signal, then choose one of two branches.” Those are control-flow problems, not just end-state descriptions.  
That is why teams often layer pipelines or orchestration around Terraform instead of forcing all logic into it. Once your problem stops looking like a graph of desired resources and starts looking like branching runtime behavior, you are moving beyond what declarative reconciliation naturally expresses.

---

## Handles and Anchors

**1. Think: “map, memory, reality.”**  
- Map = desired state in code  
- Memory = recorded state in the state file  
- Reality = actual cloud resources  
A declarative tool works only when it can compare all three. If one is wrong, the plan becomes untrustworthy.

**2. A declarative tool is more thermostat than script.**  
A script says, “turn heater on now.” A thermostat says, “target is 21°C; check current temperature and act only if needed.” That is reconciliation. The action is derived from the gap, not hardcoded as a fixed sequence.

**3. Ask this question of any IaC workflow: “Does this preserve the tool’s ability to reconcile?”**  
If the answer is no—manual changes, partial applies, hidden side effects, lost state—you are stepping outside the model. That single question is a good quick test for whether an operational shortcut is safe or corrosive.

---

## What This Changes When You Build

**An engineer who understands this will treat the state file like critical production data because it is the tool’s ownership record.**  
The unaware engineer often treats state as an implementation detail: maybe local on a laptop, maybe poorly backed up, maybe without locking. The consequence is that a lost or corrupted state file turns normal infrastructure management into manual reconstruction and risky duplicate creation.

**An engineer who understands this will be cautious with manual console changes because they know those changes create drift the tool will later try to reconcile away.**  
The unaware engineer makes a quick production fix in the console and assumes Terraform will “pick it up” harmlessly. The consequence is often the opposite: the next apply reverts the emergency fix because desired state never changed.

**An engineer who understands this will avoid routine targeted applies because they know the graph is part of correctness, not just convenience.**  
The unaware engineer uses `-target` as a normal workflow shortcut to “just update this one thing.” The consequence is partial convergence: some nodes in the graph move forward while others remain stale, making future plans harder to reason about and sometimes surprising.

**An engineer who understands this will be suspicious of imperative escape hatches inside declarative configs because those side effects are outside the diff model.**  
The unaware engineer uses `local-exec`, `remote-exec`, or similar hooks as an easy way to “finish the job.” The consequence is infrastructure behavior the tool cannot truly observe, diff, or repair later, which means drift and repeatability problems are now hidden inside something that only looks declarative.

**An engineer who understands this will separate declarative resource management from imperative orchestration when the workflow requires branching or fallback logic.**  
The unaware engineer tries to force complex runtime decision-making into Terraform itself. The consequence is awkward, fragile configs that fight the tool’s model. The better approach is often: let Terraform reconcile resource graphs, and let CI/CD or another orchestrator handle conditional control flow around it.

---

</details>
