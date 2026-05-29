## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most teams adopt Infrastructure as Code believing it solves configuration drift. It does not. IaC gives you a mechanism for *detecting* drift and a mechanism for *correcting* it. But it has no ability to prevent drift from occurring. Your cloud provider does not know or care that you use Terraform, Pulumi, or CloudFormation. It exposes an API. Anyone with credentials—a developer in the console, a script in a CI pipeline, an incident responder using the CLI at 3 AM—can call that API and change your infrastructure. When they do, your IaC codebase and your actual infrastructure are no longer the same thing, and your IaC tool will not know this until someone explicitly asks it to check. Understanding exactly how that check works, what it can and cannot see, and how drift compounds when left unattended is the difference between an IaC practice that provides real control and one that provides the illusion of it.

## The Three-Way Comparison

The central mechanic behind drift detection is a **three-way comparison** between three distinct representations of your infrastructure:

**Desired state** is what your code declares. This is the `.tf` files, the Pulumi program, the CloudFormation template—whatever definition files you have committed to version control. It says: "There should be a VPC with this CIDR range, a security group with these rules, an RDS instance with this engine version."

**Stored state** is what the IaC tool believes reality looks like, based on the last time it interacted with the cloud provider. In Terraform, this is the state file. In CloudFormation, AWS maintains this internally as the stack's recorded resource states. The stored state is a snapshot—it represents reality as of the last successful apply or refresh, not reality right now.

**Actual state** is the real, current configuration of the resources as reported by the cloud provider's API. This is the ground truth.

Every plan operation involves reconciling all three. The tool cannot simply compare code to stored state, because stored state might be stale. It cannot compare code directly to actual state, because it needs stored state to know *which* real-world resources correspond to which declarations in the code. The stored state is the mapping layer: it holds the resource IDs that link a block in your code to a specific object in your cloud account.

## How a Plan Operation Actually Executes

When you run `terraform plan`, the sequence is concrete and worth understanding step by step.

First, Terraform reads your code and constructs a resource graph—the full set of resources you have declared, including their dependencies. Then it reads the state file to get the list of resources it currently tracks, along with their cloud provider resource IDs and the last-known attribute values for each.

Next comes the **refresh phase**. For every resource in the state file, Terraform makes an API call to the cloud provider: "Describe this security group. Describe this RDS instance. What are the current attributes of this S3 bucket?" The responses come back with the actual, current configuration of each resource. Terraform now holds the actual state in memory alongside the stored state.

Now Terraform performs two comparisons. It compares the refreshed actual state against the desired state declared in code. Every difference between these two becomes a line item in the plan output. If your code says the security group should allow inbound traffic on port 443 and the actual security group also allows port 22 (because someone added it through the console), the plan will show that port 22 rule being removed. If your code says the RDS instance should be `db.t3.medium` and someone scaled it up to `db.t3.large` through the console, the plan will show it being scaled back down.

The plan output is, in effect, a drift report fused with an intent report. It shows you both what has changed outside your control and what you have intentionally changed in your code, combined into a single set of proposed actions. This is powerful and dangerous in equal measure—because it does not visually distinguish between "reverting someone's emergency fix" and "applying your new feature."

### The Refresh Flag and Its Consequences

Terraform allows you to skip the refresh phase entirely with `terraform plan -refresh=false`. This compares your code against the stored state only, ignoring what has actually happened in the real world since the last apply. This is faster—significantly so when you manage thousands of resources, because it eliminates thousands of API calls—but it makes you blind to drift. Plans generated without refresh can propose changes that conflict with the current actual state of the infrastructure, and in some cases can produce destructive outcomes because the tool is operating on stale information.

## What Drift Detection Cannot See

This is where the model has a critical boundary that is easy to miss.

Your IaC tool can only detect drift on resources it tracks. If someone creates a new EC2 instance through the console, Terraform does not know about it. It is not in the state file. It will never appear in a plan. It will never be flagged. It simply exists outside the tool's field of vision.

This category of drift—**unmanaged resources**—is in many environments the more dangerous kind. Managed resources that drift will at least surface on the next plan. Unmanaged resources are invisible indefinitely. A security group created by hand, an IAM role provisioned by a one-off script, a DNS record added through the console during an incident—none of these will ever appear in a Terraform plan unless someone explicitly imports them into the state file.

There is a second blind spot. Some resource attributes are not returned by cloud provider APIs, or are returned inconsistently. Terraform's AWS provider, for example, cannot detect drift on certain nested block configurations within some resources because the AWS API does not round-trip those values reliably. The provider's documentation sometimes notes these cases; often it does not. The practical consequence is that drift detection coverage is not uniform—some attributes are tightly tracked, others are effectively invisible.

A third blind spot: resources with **lifecycle rules** that tell the tool to ignore certain changes. In Terraform, you might write:

```hcl
lifecycle {
  ignore_changes = [tags]
}
```

This is an intentional instruction to skip drift detection on that attribute. Teams use this as a workaround when external systems (auto-scaling policies, automated tagging tools) legitimately modify attributes that the IaC tool should not fight over. But it is also a common escape hatch that quietly expands the surface area of undetected drift. Every `ignore_changes` directive is a declaration that your code is not the source of truth for that attribute.

## How Drift Enters the System

Drift has a small number of entry paths, and understanding them concretely matters because each one requires a different organizational response.

**Console access during incidents** is the most common and most sympathetic. A production database is overloaded. An engineer scales up the instance class through the AWS console because it is the fastest path to resolution. The incident is resolved. The IaC code is not updated. The next `terraform plan` will propose scaling the instance back down, which is now the wrong thing to do.

**Parallel automation** is subtler. A security team runs a Lambda function that updates security group rules based on threat intelligence feeds. A compliance tool modifies S3 bucket policies. An auto-remediation system changes IAM policies in response to audit findings. All of these are making legitimate changes through the same cloud APIs, and all of them create drift relative to the IaC codebase.

**Partial adoption** is the most structural. Most organizations do not go from zero to 100% IaC coverage overnight. During the transition—which can last years—some resources are managed by code and some are not. The boundary between managed and unmanaged is often unclear, and resources frequently fall through the gap. Someone modifies a resource they believe is manually managed but which is actually tracked in a Terraform state file, or vice versa.

**Import failures** are the quiet variant. A team imports existing infrastructure into Terraform management but misses resources or gets attribute mappings wrong. The state file says one thing, reality says another, and nobody notices until a plan produces a surprising destructive action.

## The Accumulation Problem

The single most damaging property of drift is that it compounds. One drifted attribute is easy to reconcile. Fifty drifted attributes across twenty resources, accumulated over six months of console changes and emergency fixes, produces a plan output so large and so uncertain that no one is willing to approve it. The team cannot distinguish between safe corrections and destructive reversions. At this point, the IaC codebase has effectively lost its authority. Teams stop running plan. They stop applying. They start making more changes through the console because the IaC pathway feels broken. This is the drift spiral, and it is the primary way IaC adoptions fail in practice.

The insidious aspect is that the spiral is invisible until it is advanced. Every individual unreconciled change feels low-risk. The plan output grows by one or two lines each time. Nobody looks at it for a few weeks. Then someone runs a plan and gets 40 changes, half of which they do not recognize, and the trust is gone.

## Detection Is Not Remediation

Detecting that drift has occurred and deciding what to do about it are fundamentally different problems.

When a plan reveals drift, you have two directions. You can **reconcile forward**: apply the plan, which reverts reality to match your code. Or you can **reconcile backward**: update your code (and potentially your state) to match reality. The correct choice depends entirely on whether the drift represents an unauthorized deviation or a legitimate change that your code should incorporate.

Terraform provides `terraform apply -refresh-only`, which updates the state file to match current reality without making any infrastructure changes. This is "accept reality as the new baseline." But it leaves your code out of sync with the updated state—so the *next* plan will now try to revert reality back to what the code says, unless you also update the code. The full reconciliation path for legitimate drift is: refresh the state, update the code to match, and then confirm that the plan is clean.

For unauthorized drift, the path is simpler in theory but harder in practice: apply the plan and revert the change. The difficulty is in knowing whether the revert is safe. If someone widened a CIDR range on a security group to fix connectivity during an incident and you revert it, you may re-break production.

## Continuous Detection vs. Incidental Discovery

Most teams only discover drift when someone happens to run a plan. If nobody runs a plan for three weeks, drift accumulates undetected for three weeks. This is a design-level gap in how most teams use IaC tools.

**Continuous drift detection** means running a plan on a schedule—typically in CI—and alerting when the plan output is non-empty. The plan is never applied automatically; it is purely a detection mechanism. This turns drift from something you discover accidentally into something you detect systematically, while the scope is still small enough to reason about.

The cost is real: scheduled plans at scale hit cloud provider APIs heavily. Rate limiting, API costs, and execution time all become factors. For large estates, teams often run continuous detection on a per-workspace or per-module rotation rather than all at once.

## The Mental Model

Your IaC codebase is not a control plane. It is a *declaration of intent* paired with a *detection system*. The detection system only works when you run it, only covers resources you have explicitly brought under management, and only examines attributes the cloud provider API reliably exposes. Everything outside that envelope—unmanaged resources, ignored attributes, the time between plan runs—is a detection gap.

Drift is not a bug in IaC. It is an inherent property of any system where the managed infrastructure has an API that accepts changes from sources other than the IaC tool. Which is every system. The question is never "how do we prevent drift?" but "how do we detect drift early, keep the blast radius small, and maintain the discipline to reconcile it before it compounds?"

The teams that succeed with IaC long-term are not the ones that never experience drift. They are the ones that treat a non-empty plan as an operational signal with the same urgency as a monitoring alert—something to be investigated and resolved, not something to be deferred.

## Key Takeaways

- **Drift detection is a three-way comparison** between desired state (code), stored state (state file), and actual state (cloud API)—the stored state provides the mapping between code declarations and real-world resource IDs.

- **IaC tools can only detect drift on resources they track.** Resources created outside the tool are invisible to it indefinitely, making unmanaged resources a more dangerous form of drift than modified managed ones.

- **The plan output merges drift correction and intentional changes into a single list.** There is no built-in distinction between reverting unauthorized changes and applying your new code, which is why accumulated drift makes plans unreadable and unapprovable.

- **Every `ignore_changes` directive, every `-refresh=false` flag, and every skipped plan run is a deliberate expansion of your detection gap.** These are sometimes necessary, but they should be tracked as accepted risk, not treated as routine.

- **Drift compounds.** One drifted attribute is trivially fixable. Fifty drifted attributes across months of accumulated changes produce a plan that no one will approve, and this is how IaC adoptions lose authority and collapse.

- **Reconciliation has two directions—revert reality to match code, or update code to match reality—and choosing wrong can cause outages.** There is no safe default; every drifted attribute requires a judgment call about whether the real-world state or the declared state is correct.

- **Continuous drift detection (scheduled plan runs with alerting) converts drift from an incidental discovery into a systematic operational signal**, and is the single highest-leverage practice for preventing drift accumulation.

- **Your IaC codebase is authoritative only to the extent that you enforce the discipline to keep it so.** The tool provides detection. The authority comes from organizational practice.


# Discussion

## Why This Conversation Is Happening

Teams often adopt Infrastructure as Code with an implicit promise in mind: “once infra is in code, the code is the truth.” The real system is less comforting. Your cloud account is still just an API surface. Anyone or anything with credentials can change it directly. That means the live infrastructure can drift away from the code at any time, and your IaC tool does not stop that from happening.

What breaks when engineers miss this is not just neatness or process hygiene. Emergency console edits get silently reverted later. Plans become full of changes nobody recognizes. Resources created outside IaC run for months without anyone noticing. Eventually the plan output becomes so noisy and uncertain that nobody trusts it enough to apply it. At that point, IaC has stopped being a control mechanism and has become a stale document.

So this topic matters because drift is how IaC loses authority in real teams. If you do not understand how drift is detected, what the tool can actually see, and where its blind spots are, you will mistake “we have Terraform” for “our infrastructure is under control,” and those are not the same thing.

---

## What You Need To Know First

**1. Infrastructure as Code state**
IaC tools usually keep some record of what resources they believe they manage. In Terraform this is the state file. It contains resource identities and last-known attributes. The important thing is: this is not the infrastructure itself, and it is not guaranteed to be current. It is just the tool’s memory of reality from the last time it checked or applied.

**2. Cloud provider APIs**
AWS, Azure, and GCP expose APIs for creating, reading, updating, and deleting resources. The console, CLI, SDKs, Terraform, incident scripts, and internal automation all use those same APIs underneath. So from the cloud provider’s point of view, Terraform is not special; it is just one more API client among many.

**3. Terraform plan/apply as separate steps**
A plan is not a change. It is a proposed set of actions based on comparing what exists to what your code says should exist. Apply is the step that actually calls the provider APIs and makes the changes. This matters because drift detection mostly happens during planning, not magically in the background.

**4. Managed vs unmanaged resources**
A managed resource is one your IaC tool knows about and tracks in state. An unmanaged resource exists in the account but is not tracked by the tool. The distinction matters because IaC can only reason about what it knows exists. If a resource is unmanaged, it may be completely invisible to drift detection.

---

## The Key Ideas, Connected

**IaC does not prevent drift; it only lets you detect and correct it later.**

That means the existence of code does not block out-of-band changes. A developer can change a security group in the console, a script can alter an IAM policy, or an incident responder can resize a database at 3 AM. Those changes succeed because the cloud provider accepts API calls from any authorized client, not just your IaC tool.

Once you accept that drift can happen at any time, the next question becomes: how does the IaC tool even know drift exists?

**Drift detection works by comparing three different representations of infrastructure.**

The three are: desired state in code, stored state in the tool, and actual state in the cloud provider. Desired state is your intent. Actual state is reality. Stored state is the bridge between them: it tells the tool which real resource corresponds to which declaration in code.

That mapping role is crucial. Without stored state, the tool would have trouble answering basic questions like “which actual AWS security group is this `aws_security_group.web` block supposed to refer to?” So once you understand the three-way model, you can understand why planning is not just “compare code to cloud.”

**The stored state exists because code alone is not enough to identify real resources.**

A code block describes a resource shape, but the live cloud object has provider-specific IDs and metadata. The stored state holds those IDs. That is how the tool knows which objects to query during refresh and which objects it intends to update during apply.

Because the stored state is only a snapshot from some earlier interaction, it may be stale. That makes the next step necessary: the tool has to refresh its understanding of reality before it can produce a trustworthy plan.

**A normal plan includes a refresh phase so the tool can replace stale assumptions with current reality.**

In Terraform, planning starts by reading code and state, then asking the provider API for the current attributes of every tracked resource. This is the refresh phase. After that, Terraform has the actual current values in memory and can compare those values against the code.

This matters because without refresh, the tool would be planning against its old memory, not against the system as it exists now. And that leads directly to the next idea.

**Skipping refresh makes plans faster by accepting stale knowledge, which means you can become blind to drift.**

`terraform plan -refresh=false` compares code only against stored state. That saves API calls, which can be a big performance win in large estates. But the cost is that the tool stops checking whether reality has changed since the last apply or refresh.

Mechanically, this means the plan can be wrong in a very specific way: it can propose actions based on outdated assumptions about the current resource shape. So speed is bought by widening your detection gap. Once you see that, you can also see that drift detection quality depends on what the tool is actually able to inspect.

**Drift detection only covers resources and attributes the tool can see.**

If a resource is not in state, the tool does not know to ask the provider about it. No state entry means no refresh call, no comparison, and no plan output mentioning it. That is why a manually created EC2 instance can sit in your account forever without appearing in Terraform.

Even for managed resources, coverage is uneven. The tool depends on what the provider API returns. If an API omits or inconsistently reports some nested setting, the IaC tool cannot reliably compare it. So “managed” does not always mean “fully observable.”

That boundary matters because it explains why some forms of drift are visible and others are silently absent.

**Unmanaged resources and ignored attributes are not edge cases; they are explicit blind spots.**

An unmanaged resource is invisible because the tool has no mapping to it. An ignored attribute is invisible because you told the tool not to care about it. For example, `ignore_changes = [tags]` is effectively a contract that says: changes to tags may happen outside code, and this tool should not report or reconcile them.

This is sometimes the right choice. External autoscaling systems, policy remediators, and tagging tools may need to mutate infrastructure independently. But the mechanism is important: every ignore rule narrows the set of things for which your code is authoritative. Once enough of those exceptions accumulate, your “source of truth” becomes partial rather than total.

That leads naturally to where drift comes from in practice.

**Drift enters through ordinary operational paths, not just mistakes.**

Console edits during incidents are the obvious case: someone makes a fast production fix and forgets to codify it. Parallel automation is subtler: another sanctioned system also edits infrastructure through the same APIs. Partial adoption creates ambiguity about what is managed by code and what is not. Bad imports create mismatches from the beginning.

The common mechanism across all of these is the same: real infrastructure is being modified by actors other than the IaC workflow, while the code and state are not being updated in sync. Once that happens repeatedly, the problem changes shape.

**The most dangerous property of drift is that it accumulates until plans stop being trustworthy.**

One drifted security group rule is usually easy to interpret. Fifty differences across many resources are not. The plan output becomes a mixed bundle of intended changes, unintended drift corrections, and maybe reversions of legitimate emergency fixes. Because the tool does not label which is which, the human reviewer has to reconstruct that context manually.

At small scale, that is manageable. At larger scale, it becomes cognitively expensive and risky. Teams start postponing applies because they cannot confidently predict the outcome. Then they make more direct console changes because the IaC path feels blocked. This is the drift spiral: drift reduces trust, reduced trust reduces IaC usage, reduced IaC usage creates more drift.

Once drift is detected, the next problem is not technical comparison but judgment.

**Detection and remediation are different problems because a difference does not tell you which side is correct.**

If the live database size differs from code, you still have to answer: was the console change an unauthorized deviation that should be reverted, or was it a legitimate production fix that the code should adopt? The plan only shows mismatch; it does not tell you intent.

That is why reconciliation has two directions. You can push reality back toward code, or you can update code and state to accept reality as the new baseline. Neither is automatically safe. Reverting a valid incident change can break production; accepting an unauthorized change can normalize bad config.

Because this judgment is easier when the change set is small and recent, the next idea follows directly.

**Continuous drift detection is valuable because it turns a growing unknown into a small, fresh operational signal.**

If drift is only discovered when a human happens to run plan, then the detection interval is random and often long. During that gap, more changes can pile up. Scheduled plans shrink the time between drift entering the system and drift becoming visible.

The mechanism here is simple: shorter detection intervals mean fewer unknown changes per investigation. That keeps plans understandable, keeps reconciliation decisions local and timely, and prevents the trust collapse that comes from giant surprise diffs.

All of this supports the article’s core mental model.

**Your IaC system is not a control plane; it is a declaration of intent plus a periodically run comparison mechanism.**

It does not continuously enforce. It does not automatically know about every resource. It does not prevent others from changing infrastructure. Its authority comes from practice: keeping resources under management, running detection often, and reconciling drift before it compounds.

Once you hold that model, the rest of the article makes sense. Drift is not an exception to IaC. It is the normal consequence of managing infrastructure in an environment where multiple actors can mutate the same system.

---

## Handles and Anchors

**1. “Terraform is not a lock; it is a ledger plus an inspection.”**  
A lock prevents change. Terraform does not. It records what it thinks exists and, when asked, inspects reality to find differences. If you remember that, you will stop expecting prevention from a tool that only offers comparison and correction.

**2. Think of drift detection like reconciling accounting books against a bank account.**  
Your code is what you intended to spend. Your state file is your last recorded balance. The cloud provider is the bank statement. If someone made transactions outside your bookkeeping, your books are wrong until you reconcile. And if you skip reconciliation for months, the problem becomes much harder to untangle.

**3. Ask this question of any IaC setup: “What can change this infrastructure without this tool noticing immediately?”**  
That question reveals the real detection gaps: console access, other automation, unmanaged resources, ignored attributes, infrequent plans, skipped refresh. It is a practical way to test whether IaC is actually authoritative or only aspirational.

---

## What This Changes When You Build

**An engineer who understands this will treat scheduled plan runs as an operational control, not a convenience, because drift gets harder to reason about as detection latency increases.**  
The unaware engineer runs plan only when they are already making a change. That means drift is discovered late, bundled together with new work, and harder to review safely.

**An engineer who understands this will be cautious with `-refresh=false` because they know they are trading correctness for speed, not just skipping a harmless extra step.**  
The unaware engineer reaches for it when plans are slow and assumes the output is still a trustworthy view of reality. In practice they are now planning against stale memory, which can produce misleading or dangerous change proposals.

**An engineer who understands this will inventory unmanaged resources and import or explicitly exclude them, because invisible infrastructure is more dangerous than visible drift.**  
The unaware engineer assumes “if Terraform doesn’t mention it, it probably doesn’t matter.” The consequence is orphaned infrastructure, hidden security exposure, and systems that exist outside any review or reconciliation process.

**An engineer who understands this will review every `ignore_changes` as a governance decision, because it defines where code stops being authoritative.**  
The unaware engineer uses ignore rules as a quick way to silence noisy diffs. The result is that the team gradually teaches the tool not to report meaningful changes, widening the gap between declared and actual state.

**An engineer who understands this will separate “difference detected” from “safe to apply,” because plan output merges intentional changes with drift correction.**  
The unaware engineer treats a non-empty plan as a straightforward to-do list. The better approach is to ask, for each drifted item: who changed this, why, and should code or reality win? That is how you avoid reverting valid emergency changes or legitimizing bad manual edits.

**An engineer who understands this will design incident processes that include post-incident codification, because emergency fixes made outside IaC are not complete until the code reflects them.**  
The unaware engineer considers the incident over once production is stable. The consequence is that the next apply may undo the fix, or the drift may sit around and contribute to a larger future reconciliation mess.
