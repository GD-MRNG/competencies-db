## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers treat the plan step as a preflight check — a gate that answers "is this going to work?" That framing misses the point. The plan step does not tell you whether an operation will succeed. It tells you what the operation intends to do, and there is an enormous difference between those two things. A plan can show a clean, valid set of changes that will still destroy your production database if you didn't realize a rename forces a resource replacement. The plan was accurate. The operator's reading of it was not. Understanding the mechanics of how a plan is generated — what inputs it reads, what comparisons it makes, what its output actually encodes — is what turns the plan step from a rubber stamp into the primary risk management tool for infrastructure changes.

## The Three Inputs to a Plan

A plan is a diff, but it is not a simple two-way diff between "old config" and "new config" the way a `git diff` works. It is a **three-way reconciliation** between three distinct sources of truth:

**The desired state** is what your configuration files declare. This is the set of `.tf` files (in Terraform's case), the CloudFormation template, the Pulumi program — whatever declarative definition you have written. It represents what you want the infrastructure to look like.

**The state file** is the IaC tool's last known record of what it believes the infrastructure looks like. The Level 1 post covered state management. What matters here is that the state file is not a live view. It is a snapshot from the last time the tool successfully applied changes or explicitly refreshed. It can be stale.

**The real infrastructure** is what actually exists in the target environment right now. The plan step queries the cloud provider APIs (or whatever backend manages the resources) to determine the current state of each resource the tool is tracking.

The plan algorithm works roughly like this: first, refresh the state file by reading the real infrastructure. Then, compare the refreshed state to the desired state declared in configuration. For every resource, determine what action (if any) is needed to move from current to desired. The output is the set of those actions.

This three-way model is why a plan can surface changes you did not make. If someone manually modified a security group rule through the AWS console, the refresh step will detect the discrepancy between the state file and reality, and the plan will show a change to bring that resource back in line with your declared configuration. You changed nothing in your config. The plan still shows a diff. This is not a bug — it is the tool doing exactly what it should: resolving drift.

## The Refresh Step and Why It Costs Money

The refresh is the most mechanically expensive part of a plan. For every resource tracked in your state file, the tool makes an API call to the cloud provider to read the resource's current attributes. If your state file tracks 500 resources, that is at minimum 500 API calls before the diff computation even starts.

This has practical consequences. Plans against large state files are slow — sometimes minutes. They can hit API rate limits, especially in AWS accounts that are already under heavy automation load. And because the refresh reads every tracked resource, it can fail if a resource has been deleted outside of the tool's knowledge, or if the credentials being used lack read permissions on a resource that was provisioned by a different role.

Terraform exposes a `-refresh=false` flag that skips this step and plans against the stale state file. This is faster but dangerous: you are now computing a diff against what the tool last saw, not what actually exists. If someone manually deleted a resource, the plan will not know. If someone manually changed a resource's attributes, the plan will not account for it. The resulting apply can fail or, worse, produce unexpected results. The flag exists for speed in CI pipelines where you have high confidence nothing has changed externally, but using it as a default is trading safety for convenience.

## The Action Taxonomy: What a Plan Actually Proposes

Every resource in a plan output gets one of a small number of action designations. Understanding these is not optional — they encode the risk profile of the entire operation.

**Create** (`+`): A resource exists in configuration but not in state. The tool will provision it. Risk is generally low — you are adding something new, not touching anything existing.

**Update in-place** (`~`): A resource exists in both configuration and state, but some attributes differ. The tool will modify the existing resource. Risk depends entirely on what is being changed. Updating a tag is trivial. Updating a security group's ingress rules is operationally significant. The plan output shows which specific attributes are changing, and reading those attributes is where the real risk assessment happens.

**Destroy** (`-`): A resource exists in state but not in configuration. The tool will delete it. This is where blast radius becomes real. Deleting a resource might seem contained, but if other resources depend on it — instances in a subnet, records in a DNS zone — the cascading effects can be severe.

**Replace** (destroy then create, or create then delete): This is the action that catches people off guard. Some attribute changes on some resource types cannot be applied in-place. The cloud provider's API does not support modifying that attribute on a live resource. The only path is to destroy the existing resource and create a new one with the updated attributes. In Terraform's plan output, this shows as a resource being both destroyed and created, often annotated with `# forces replacement` next to the specific attribute that triggered it.

Replace is where the most dangerous plan misreadings happen. An engineer changes an EC2 instance's AMI ID, expecting an in-place update. The plan shows a replacement. If the engineer does not read the plan carefully, they approve what is functionally a full instance teardown and rebuild — losing any ephemeral state, changing the private IP, disrupting active connections. The plan told them exactly what would happen. They just did not parse the output.

```
# aws_db_instance.main must be replaced
-/+ resource "aws_db_instance" "main" {
      ~ engine_version = "14.7" -> "15.3" # forces replacement
      ~ id             = "mydb-abc123" -> (known after apply)
        name           = "production"
        # ... other attributes unchanged
    }
```

That `-/+` prefix is the signal. The `# forces replacement` annotation tells you which attribute caused it. For a database, this means the existing instance is destroyed and a new one is created. If you are not restoring from a snapshot in the new configuration, your data is gone.

## The Dependency Graph and Change Cascades

Resources in an IaC configuration are not isolated. They form a **dependency graph** — the VPC must exist before the subnet, the subnet before the instance, the instance before the DNS record pointing to it. The plan respects this graph when computing the order of operations.

This matters for risk assessment because a single change to a foundational resource can cascade. If the plan shows that a VPC is being replaced, every resource that depends on that VPC is also being replaced: subnets, route tables, security groups, instances, load balancers, NAT gateways. The plan will show all of these changes, but if you are scanning quickly, you might see the VPC replacement and miss that it implies rebuilding your entire network stack.

The dependency graph also determines parallelism during apply. Resources with no dependency relationship to each other can be created or modified concurrently. This means that a plan with 30 resource changes might execute much faster than you expect, but it also means failures can be partial — the apply might succeed on some branches of the graph and fail on others, leaving your infrastructure in a state that matches neither the old configuration nor the new one.

## Reading a Plan for Risk

A plan output is not a checklist to approve. It is a risk assessment document. The skill of reading a plan is pattern-matching for signals of high blast radius:

**Resource count.** A plan that touches 3 resources is categorically different from one that touches 150. If you expected a small change and the plan shows dozens of modifications, something is wrong — either your change has unexpected dependencies, or drift has accumulated.

**Replaces and destroys on stateful resources.** Any replacement of a database, a persistent volume, or a storage bucket should trigger deep review. These are resources where destruction means data loss.

**Changes to identity-bearing attributes.** If the plan modifies a resource's name, ARN, or unique identifier, downstream resources that reference that identity may break — even ones not managed by the same IaC configuration.

**The `(known after apply)` marker.** Some attribute values cannot be computed until the resource actually exists — like an IP address assigned by the cloud provider. When the plan shows this marker on an attribute that other resources reference, it means the plan is making assumptions about the apply-time resolution. Most of the time this is fine. When it is not fine, you will not know until apply.

## Where Plan Fails to Protect You

The plan step has real limits, and overconfidence in it causes real incidents.

**The time-of-check to time-of-use gap.** A plan is computed at a point in time. Between the moment you run `plan` and the moment you run `apply`, the real infrastructure can change. Another engineer applies their own changes. An autoscaler adds instances. A cloud provider modifies a resource's attributes as part of maintenance. The apply operates on the assumption that the world still looks like it did during the plan. If it doesn't, the apply can fail partway through or produce unexpected results. Terraform partially mitigates this by re-reading resource state during apply, but it does not re-run the full plan — it will attempt the planned actions even if the preconditions have shifted.

**Provider-level validation gaps.** The plan computes a diff based on the resource schema known to the provider plugin. It does not execute the cloud API call. This means it cannot catch errors that only the API would catch: invalid parameter combinations, quota limits, permission denials on specific operations, or regional service availability. You can get a perfectly clean plan and have the apply fail on the first resource because your account hit its VPC limit.

**Cross-state blind spots.** Most real infrastructure is split across multiple state files (by team, by environment, by service). A plan only considers the resources in its own state. If your change modifies a shared resource — say, a DNS zone entry that another team's service also depends on — the plan has no mechanism to warn you about the cross-boundary impact. The blast radius extends beyond what the plan can see.

**The false confidence loop.** The most insidious failure mode is cultural. Teams that have run plan-and-apply hundreds of times without incident start reviewing plans less carefully. The plan becomes a formality — glance at the resource count, approve. This is when the dangerous change gets through. Plan review is a skill that degrades without deliberate practice, and the consequences of a missed signal are asymmetric: you review a hundred plans correctly and nothing happens, you miss one and an outage occurs.

## The Mental Model

Think of the plan step as a structured, machine-generated risk disclosure — not a guarantee. It tells you the tool's intent: what it will try to create, modify, destroy, and replace, based on the three-way diff between your configuration, its last known state, and the live infrastructure. It is comprehensive within its scope and blind outside of it.

The critical conceptual shift is understanding that the plan is not asking you "should I proceed?" It is telling you "here is what I will do" and asking you "is this what you meant?" Answering that question correctly requires understanding the action taxonomy, recognizing which resources are stateful, knowing which attribute changes force replacements, and being alert to unexpectedly large diffs that signal drift or dependency cascades. The plan cannot protect you from changes you approve without understanding.

## Key Takeaways

- A plan is a three-way diff between your declared configuration, the tool's recorded state, and the live infrastructure — not a two-way diff between old and new config.

- The refresh step queries every tracked resource via API before computing the diff, which is why plans on large state files are slow and why skipping refresh trades safety for speed.

- Replace actions (destroy-then-create) are the highest-risk operations in a plan because they can cause data loss on stateful resources, and they are triggered by attribute changes that cannot be applied in-place.

- Changes to foundational resources cascade through the dependency graph — a single VPC replacement can imply the destruction and recreation of every resource inside it.

- The plan cannot catch errors that only the cloud API would surface at apply time: quota limits, permission denials, invalid parameter combinations, and service availability constraints.

- A clean plan does not guarantee a clean apply because the infrastructure can change between plan and apply (the time-of-check to time-of-use gap).

- Plans are scoped to a single state file and cannot warn you about cross-boundary impacts on resources managed in separate states.

- The most common plan-related incident is not a tool failure — it is an engineer approving a plan they did not read carefully enough, particularly one containing unexpected replacements of stateful resources.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Infrastructure-as-code plans are often treated like a green-light screen: if the plan runs and the output looks vaguely reasonable, people assume the change is safe. That habit breaks down the moment the plan includes something you did not realize the tool meant by “change.” A rename can mean delete-and-recreate. A small config edit can imply replacing a database. A drifted resource can show up in the plan even though nobody touched the code. If you do not understand how the plan was produced, you cannot tell the difference between “expected change” and “silent outage in preview.”

The concrete failure mode is not that the tool lies. It is that the tool tells the truth in a format the operator misreads. Engineers approve plans that destroy stateful resources, miss cascade effects through dependencies, or trust a clean plan as proof that apply will succeed. That leads to data loss, partial applies, broken references, and production changes whose blast radius was visible in the plan output but not recognized.

---

## What You Need To Know First

**1. Declarative infrastructure**  
In IaC tools like Terraform or CloudFormation, you usually describe the end state you want, not the exact imperative steps to get there. You say “there should be a database with these settings,” and the tool decides whether that means create, update, delete, or replace. This matters because the plan is the tool’s interpretation of your declaration, not your intention in natural language.

**2. State files**  
A state file is the tool’s stored record of the resources it manages and their last known attributes. It is not the cloud itself, and it is not always current. The plan uses state as one input, which is why stale or wrong state can lead to surprising plan output.

**3. Drift**  
Drift means the real infrastructure no longer matches what your IaC configuration says, usually because of manual changes, external automation, or cloud-side behavior. Plans surface drift because they compare declared intent to actual reality. So a plan can show changes even when your code diff is empty or tiny.

**4. Resource replacement vs in-place update**  
Some infrastructure changes can be made on a live resource; others cannot. If the provider API does not allow a field to be modified in place, the tool must destroy the old resource and create a new one. This distinction is central because “change one field” can operationally mean “tear down and rebuild the thing.”

---

## The Key Ideas, Connected

**A plan is not a success prediction; it is a statement of intended actions.**  
The first thing to fix in your mental model is what the plan is for. It does not answer “will apply succeed?” It answers “given what I can currently see, what actions will I try to take?” That difference matters because a plan can be perfectly accurate about intended destruction, replacement, or updates and still tell you nothing about quota failures, permissions errors, or race conditions at apply time. Once you see the plan as intent rather than guarantee, the next question becomes: intent based on what inputs?

**A plan is computed from three sources of truth, not just old config vs new config.**  
Most people implicitly imagine a plan as a `git diff` for infrastructure. It is not. The tool reconciles: your desired state in code, its recorded state in the state file, and the live infrastructure it reads from the provider. That is why a plan can show changes you did not type into the config. If reality drifted, the refresh step will discover that, and the diff will include actions to bring reality back to the declared state. Once you understand those three inputs, you can understand why refresh exists and why it is expensive.

**Before diffing, the tool refreshes its view of reality by reading the live infrastructure.**  
The state file is only a remembered snapshot, so the tool first asks the provider what each tracked resource looks like now. Mechanically, that means API reads for every managed resource. This is why plans get slow as the state grows, why they can hit rate limits, and why plan can fail even before diffing if credentials cannot read a resource or if a tracked object has been deleted unexpectedly. Because refresh is costly, tools let you skip it—but skipping it changes what the plan means.

**Skipping refresh makes planning faster by accepting stale assumptions.**  
With `-refresh=false`, the tool compares your desired config against its last remembered state instead of against current reality. That saves API calls, but the price is that the plan may be based on infrastructure that no longer exists or no longer matches state. So the tradeoff is not “same plan, faster”; it is “faster plan, weaker truthfulness about the world.” Once the tool has refreshed and compared desired vs current, it has to classify each resource into a type of action.

**The plan output is an action taxonomy: create, update, destroy, or replace.**  
These labels are not cosmetic. They are the operational meaning of your change. Create usually means additive, low-risk work. Update in place means mutate something existing, with risk determined by which fields change. Destroy means explicit removal. Replace is the dangerous category: the provider cannot do the change on the existing object, so the only legal move is old resource out, new resource in. This is why a harmless-looking field edit can turn into an outage. And that naturally raises the question: what determines whether the impact stays local or spreads?

**Resources are connected by dependencies, so one action can cascade into many more.**  
Infrastructure is a graph, not a pile. A subnet depends on a VPC; instances depend on the subnet; DNS records may depend on instance attributes. If a foundational resource must be replaced, every downstream resource that cannot survive that identity change may also need to change. The plan shows this, but only if you read beyond the first surprising line. The mechanism is straightforward: dependent resources reference attributes or existence of parent resources, so when the parent is recreated, those references become invalid or point somewhere new. That is why risk assessment cannot stop at “what changed?” and must ask “what depends on it?”

**Because plans encode dependency-driven actions, you read them for blast radius, not just correctness.**  
At this point the plan becomes a risk document. A small expected code change paired with a huge plan means either drift, hidden dependencies, or a mistaken assumption. Replacements and destroys on stateful resources are high-risk because deletion may mean data loss, not just recreation time. Identity-bearing fields matter because external systems may depend on names, ARNs, IDs, or addresses not visible in this state. `(known after apply)` matters because some downstream values are unresolved until creation time, so the tool is planning with placeholders rather than fixed values. Once you treat plan review as blast-radius analysis, the next important boundary is what the plan cannot know.

**A plan has scope limits, timing limits, and validation limits.**  
It can only reason about resources in its own state, using provider schemas and the world as observed at plan time. That creates three major blind spots. First, the world may change between plan and apply: another deploy, autoscaling, manual edits, provider maintenance. Second, the provider plugin can compute a diff without knowing whether the actual API call will be rejected for quota, permissions, unsupported combinations, or temporary service conditions. Third, resources outside this state file may depend on what you are changing, and the plan cannot warn you about those cross-state impacts. Once you understand those limits, the final conceptual shift becomes clear.

**The plan’s real value is as a machine-generated disclosure of consequences, not a safety guarantee.**  
The tool is saying: “Given my model of config, stored state, and current reality, here is what I will attempt.” Your job is not to ask whether the tool is confident. Your job is to verify that the consequences match what you intended and that the risks are acceptable. The reason incidents still happen is usually not that the plan failed to show the action, but that humans stopped reading it as a description of consequences and started treating it as a ceremonial checkmark.

---

## Handles and Anchors

**1. Handle: “A plan is a surgeon’s procedure list, not a prognosis.”**  
It tells you what operations will be attempted: remove, replace, modify, create. It does not promise the patient will be fine. That helps separate “intended action” from “guaranteed outcome.”

**2. Handle: “Three-way reconciliation, not code diff.”**  
If you remember only one mechanic, remember this: plan compares desired config, remembered state, and live reality. That explains drift, refresh cost, surprising diffs, and why skipping refresh changes the meaning of the output.

**3. Question to ask every plan: “Which lines here imply identity loss?”**  
Replacements, destroys, changed IDs/names/ARNs, and foundational resources are the lines that usually expand blast radius. This question forces you to look for consequences, not just counts.

---

## What This Changes When You Build

**An engineer who understands this will review plans by action type first, not by resource count alone, because a single replacement can be more dangerous than fifty tag updates.**  
The unaware engineer often scans the summary line—“12 to add, 3 to change, 1 to destroy”—and treats that as sufficient. The better approach is to immediately find destroys and replacements, especially on stateful or foundational resources, because that is where outages and data loss usually hide.

**An engineer who understands this will be cautious about `-refresh=false` in CI because they know it changes the truth basis of the plan, not just its speed.**  
The default unaware move is to disable refresh whenever plans feel slow. The consequence is approving changes against stale assumptions and discovering drift only during apply, when failures are more expensive and harder to unwind.

**An engineer who understands this will treat changes to foundational resources as graph changes, not local edits, because dependencies turn one replacement into a cascade.**  
The unaware engineer sees “replace VPC” or “replace subnet” as a single-resource event. The aware engineer expects secondary effects—instances, routes, gateways, load balancers, DNS, security relationships—and reads the full plan to map the implied rebuild.

**An engineer who understands this will separate “clean plan” from “safe deploy” because provider validation and TOCTOU gaps still exist.**  
The unaware engineer assumes plan success means apply should be routine. The aware engineer still checks quotas, permissions, maintenance windows, concurrent automation, and whether enough time has passed for the environment to diverge from the planned snapshot.

**An engineer who understands this will design state boundaries and review processes differently because plan visibility ends at the state file boundary.**  
The unaware engineer assumes the plan reveals all downstream impact. The aware engineer knows shared infrastructure, cross-team dependencies, and out-of-state consumers are invisible to the plan, so they add extra review, documentation, or architectural boundaries around shared resources rather than trusting plan output alone.

</details>
