## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers encounter IaC modules as a packaging mechanism — a way to avoid repeating yourself. The Level 1 framing is accurate: modules encapsulate reusable infrastructure with defined inputs and outputs. But treating modules primarily as a DRY technique misses the actual problem they solve and leads to module designs that create more pain than they prevent. The real function of a module is not to reduce duplication. It is to create a **stable interface contract** that lets infrastructure change in one place and propagate predictably to many. The difference matters because a module designed for reuse looks fundamentally different from a module designed for evolvability — and it's evolvability that you actually need when your pager goes off at 2 AM and a security patch has to roll across every environment you operate.

## How Copy-Paste Actually Compounds

The Level 1 post established that you shouldn't define all infrastructure in one file. But the specific way that copy-paste fails is worth understanding mechanically, because it explains why teams reach for modules and what modules need to solve.

Suppose you define an EKS cluster configuration directly in your root Terraform for the dev environment — node pool sizes, networking rules, IAM roles, encryption settings. Staging needs a cluster too, so you copy the block. Production gets its own copy with different instance sizes. Three copies, all derived from the same source, all understood by the team on day one.

Six months later: dev has an experimental GPU node pool someone added. Prod has a security group rule that was patched during an incident and never backported. Staging has a modified autoscaling policy from a load test that was never reverted. The three copies have **diverged silently**, not because anyone made a bad decision, but because each environment accumulated its own local history.

Now a compliance requirement lands: all clusters must enable envelope encryption for Kubernetes secrets. This is nominally a one-line change. But you cannot apply a uniform patch because the three configurations have different shapes. Each requires its own review, its own plan output, its own risk assessment. The work is not O(1) — "change the pattern once." It's O(n) in the number of copies, with each copy carrying unique cognitive load because you must understand its local mutations before you can safely change it.

This is the compound cost. It's not the initial duplication that hurts. It's the **divergence under maintenance** that makes future changes expensive and error-prone. And the cost grows super-linearly: every additional copy is one more environment that might have drifted in ways the person making the change doesn't know about.

## The Anatomy of a Module Interface

A module in Terraform (or equivalent constructs in Pulumi, OpenTofu, CloudFormation nested stacks) has three structural components that matter: **input variables**, **managed resources**, and **output values**. Together, these form the module's interface contract.

**Input variables** are the knobs you expose to consumers. They define what can vary between uses of the module:

```hcl
variable "cluster_name" {
  type        = string
  description = "Name of the EKS cluster"
}

variable "node_instance_type" {
  type    = string
  default = "m5.large"
}

variable "enable_secret_encryption" {
  type    = bool
  default = true
}
```

**Managed resources** are the infrastructure objects the module creates and controls internally. These are implementation details — the consumer doesn't interact with them directly:

```hcl
resource "aws_eks_cluster" "this" {
  name = var.cluster_name
  # ... internal configuration the consumer doesn't control
  
  encryption_config {
    provider {
      key_arn = var.enable_secret_encryption ? aws_kms_key.eks[0].arn : null
    }
    resources = ["secrets"]
  }
}
```

**Output values** are the information the module exposes for other modules or configurations to consume:

```hcl
output "cluster_endpoint" {
  value = aws_eks_cluster.this.endpoint
}

output "cluster_security_group_id" {
  value = aws_eks_cluster.this.vpc_config[0].cluster_security_group_id
}
```

The critical design decision — the one that determines whether a module helps or hurts over time — is **where you draw the line between inputs and hardcoded internals**. Every input variable is a degree of freedom you're granting the consumer. Every hardcoded value is an opinion you're enforcing. The compliance requirement from the earlier example? If `enable_secret_encryption` is an input variable defaulting to `true`, any environment could have overridden it to `false`. If encryption is hardcoded as always-on inside the module, compliance is enforced by design with no per-environment opt-out.

This is the module designer's core tension: **flexibility versus consistency**. An overly flexible module with forty input variables has effectively moved all the complexity to the caller — you've built a configuration wrapper around a configuration language, and you haven't actually reduced anyone's cognitive load. An overly rigid module with two inputs is easy to use but gets forked the first time a team needs something slightly different, and now you're back to copy-paste divergence with extra indirection.

## How Modules Compose

Modules rarely exist in isolation. A realistic infrastructure codebase has a root configuration that wires modules together, passing outputs from one as inputs to another:

```hcl
module "network" {
  source       = "git::https://github.com/org/modules.git//network?ref=v2.1.0"
  environment  = "production"
  cidr_block   = "10.0.0.0/16"
}

module "cluster" {
  source            = "git::https://github.com/org/modules.git//eks?ref=v3.0.1"
  cluster_name      = "prod-main"
  vpc_id            = module.network.vpc_id
  subnet_ids        = module.network.private_subnet_ids
}

module "database" {
  source            = "git::https://github.com/org/modules.git//rds?ref=v1.4.0"
  subnet_ids        = module.network.database_subnet_ids
  security_group_id = module.cluster.cluster_security_group_id
}
```

This wiring creates a **dependency graph**. Terraform (and similar tools) builds a directed acyclic graph from these references and uses it to determine the order of operations: network must be created before cluster, cluster before database. The graph is implicit in the references between module outputs and inputs — you don't declare ordering, the tool infers it.

Module composition also means **nested modules** — a module can call other modules internally. Your EKS module might use a smaller IAM-role module and a security-group module under the hood. This creates layers of abstraction. Each layer hides implementation details and exposes a simpler surface.

But nesting has a cost: **debugging depth**. When `terraform plan` shows a change to `module.cluster.module.iam_role.aws_iam_role_policy_attachment.this`, you're three levels deep. Understanding why that change appeared requires traversing the module hierarchy. Deep nesting makes plan output harder to review and increases the time to understand what a change will actually do to your infrastructure.

## Versioning and Upgrade Mechanics

The `?ref=v2.1.0` in the module source is doing critical work. It pins the consumer to a specific snapshot of the module's code. This is what makes module changes safe: updating the module source doesn't affect any consumer until that consumer explicitly bumps their ref.

Module sources can resolve from several places: local file paths (no versioning — always the current code), Git repository tags, a Terraform registry with semantic versions, or artifact storage like S3. The choice determines your upgrade workflow.

With **Git tag pinning**, the upgrade process looks like this: a module maintainer merges changes and cuts a new tag. Each consuming configuration updates its `ref` parameter, runs `terraform plan` to see the impact, reviews the plan, and applies. This is deliberate and explicit — each environment upgrades independently, on its own schedule.

The practical consequence is **version sprawl**. Across fifteen environments, you might have eight different module versions in use. This is not inherently bad — it means each environment upgrades deliberately rather than being forced. But it means that if the module has a security-critical fix in v3.2.0, someone has to track which environments are still on older versions and drive those upgrades. Without tooling or process to manage this, stale versions accumulate silently.

**Breaking changes** in modules — renamed variables, removed outputs, changed resource structures — are particularly painful because they cannot be adopted incrementally. If the module renames `subnet_ids` to `private_subnet_ids`, every consumer must update their calling code at the same time they bump the version. Module maintainers who treat their interfaces as internal implementation details rather than public API contracts cause cascading work across every team that consumes their modules.

## Modules and State Entanglement

Every resource Terraform manages is tracked in the state file under a specific **address** that includes the module path: `module.network.aws_subnet.private[0]`. This address is the binding between the declared configuration and the real infrastructure object.

When you refactor modules — moving a resource from one module to another, renaming a module, splitting a large module into smaller ones — the addresses change. Terraform interprets a changed address as "destroy the old thing, create the new thing." For a subnet with running workloads, that interpretation is catastrophic.

Terraform provides `moved` blocks and the `terraform state mv` command to tell the tool "this resource didn't change, it just moved addresses." But this is manual, error-prone work that requires understanding both the old and new module structures. In a production environment, a state move operation on the wrong resource can cause real outages.

This is the hidden cost of module refactoring. The conceptual change might be clean — "let's split the networking module into separate VPC and subnet modules for better reuse." The state migration is anything but clean. It requires planning, testing against a state copy, coordination with any pipelines that might run concurrently, and often a maintenance window. This cost means module boundaries, once established with real infrastructure behind them, are **expensive to change**. Getting the boundaries roughly right early matters more than in application code, where a refactor is just a refactor.

## Tradeoffs and Failure Modes

### The God Module

The most common failure pattern is a single module that manages an entire environment — networking, compute, databases, DNS, monitoring — all in one. It starts as a convenience: "everything for a service in one module call." But it becomes unmaintainable because any change to any component requires understanding the whole module. It cannot be reused partially. Teams that need "just the networking part" either use the whole thing (pulling in resources they don't want) or fork it (back to copy-paste). The fix is decomposition into single-responsibility modules, but see the state entanglement section above for why that fix is expensive after the fact.

### The Inner Platform

The opposite failure: a module so parameterized that it reproduces the full surface area of the underlying provider. Every resource argument is exposed as a variable, often with `any` types. The module adds no opinions, enforces no standards, and provides no simplification. It's a pass-through layer that adds indirection without adding value. A good module **makes decisions** so its consumers don't have to. If your module's variable count approaches the argument count of the underlying resources, you haven't written a module — you've written a wrapper.

### Premature Abstraction

You extract a module from a single use case, design its interface around that one context, then discover it doesn't generalize to the second use case. But the first team already depends on it in production. Now you're maintaining a module whose interface you want to change but can't, and building a second module that's almost-but-not-quite the same. The standard guidance — wait until you have two or three concrete uses before extracting a module — applies to infrastructure just as it applies to application code, perhaps more so, because the state entanglement makes interface changes costlier.

### Version Drift as Silent Risk

When no one owns the process of tracking module versions across consumers, environments quietly fall behind. The module gets improved, security patches land, but production stays pinned to a version from nine months ago. This isn't visible in any dashboard. It surfaces only when someone tries to make a change and discovers their environment is too far behind to upgrade cleanly, or when an audit reveals that a vulnerability fixed months ago was never rolled out.

## The Mental Model

A module is not a function. It is closer to a **versioned API with state**. Its inputs are the API's parameters. Its outputs are the API's response. Its managed resources are side effects that persist in the real world and are tracked in the state file. Its version tag is the contract that consumers depend on.

This framing changes how you design modules. You think about backward compatibility. You think about what constitutes a breaking change. You think about how many consumers will need to coordinate when the interface evolves. You think about the blast radius of a change — not just "what does this module do?" but "who calls this module, and what are they pinned to?"

The decision of what to put in a module is not "what code is repeated?" It is "what infrastructure should change together, be versioned together, and be constrained together?" That question — what changes together — is the right starting point for every module boundary you draw.

## Key Takeaways

- Copy-paste in infrastructure doesn't fail at creation time — it fails during maintenance, when each copy has silently diverged and a uniform change becomes O(n) work with per-copy risk assessment.

- A module's interface is defined by three components: input variables (what varies), managed resources (what's hidden), and output values (what's shared). The ratio of inputs to hardcoded internals determines whether the module enforces consistency or just relocates complexity.

- Module composition creates an implicit dependency graph. Terraform infers ordering from output-to-input references between modules, and deep nesting increases the cost of reviewing plan output.

- Version pinning makes module upgrades explicit and controlled, but creates a version sprawl management problem that requires active tracking to prevent silent drift across environments.

- Refactoring module boundaries after infrastructure exists requires state migration — not just code changes — making early module boundary decisions disproportionately sticky compared to application code refactoring.

- The "god module" (everything in one) and the "inner platform" (every knob exposed) are opposite failure modes that both result from not deciding what opinions the module should enforce.

- Wait for two or three concrete use cases before extracting a module. Premature abstraction in infrastructure is more costly than in application code because interface changes cascade through state and consumers simultaneously.

- The right question for module boundaries is not "what code is duplicated?" but "what infrastructure should change together, be versioned together, and be constrained together?"

# Discussion

## Why This Conversation Is Happening

Teams usually discover the real value of IaC modules during maintenance, not during initial setup. Copy-pasting Terraform works fine on day one: dev, staging, and prod all come up, and everyone feels productive. The trouble starts months later, when each copy has been edited under different pressures — an incident hotfix in prod, a test change in staging, an experiment in dev. Now a “simple global change” is no longer one change. It is many slightly different changes, each with its own review risk.

That becomes dangerous when the change is urgent or mandatory. A security control, compliance requirement, provider deprecation, or cost fix has to roll out everywhere, but your infrastructure no longer has one shape. Engineers have to rediscover local differences before they can act safely. That slows response time, increases the chance of missing an environment, and turns infrastructure maintenance into archaeology.

Modules exist to control that maintenance problem. If you only think of them as a DRY feature, you will likely design them to reduce typing rather than to preserve a stable contract across time. That usually produces modules that are too loose, too rigid, or too entangled to evolve safely.

---

## What You Need To Know First

### Terraform state
Terraform keeps a record of what real infrastructure objects it believes it manages. That record is the state file. It maps your configuration to actual cloud resources, and Terraform uses it to decide whether to create, change, or destroy something. If a resource’s identity in configuration changes, Terraform may think the old object should be destroyed and a new one created unless you explicitly tell it the resource was only moved.

### Inputs, outputs, and encapsulation
A module has things callers are allowed to provide, and things it gives back. Inputs are the allowed variations; outputs are the pieces other code can depend on. Everything else inside the module is internal implementation. The key idea is that consumers should depend on the interface, not the internals, so the internals can change without forcing every caller to change too.

### Dependency graph
Terraform builds an execution order by following references. If one module takes another module’s output as an input, Terraform infers that the second depends on the first. You usually do not hand-write the order; the tool derives it from the data flow. This matters because module composition is not just organization — it affects how changes propagate and in what order infrastructure is created or updated.

### Version pinning
When you reference a module at a specific tag or version, you are saying “use exactly this snapshot.” That protects consumers from unreviewed changes. But it also means upgrades do not happen automatically; someone has to choose to move each consumer to a newer version and verify the impact.

---

## The Key Ideas, Connected

### A module’s real job is to create a stable interface for infrastructure that must evolve.
The article’s core claim is that modules are not mainly about avoiding repeated code. They are about making change manageable. In infrastructure, the expensive part is rarely initial creation; it is the repeated need to modify many similar systems over time. A stable interface lets you improve, patch, or constrain the implementation in one place while giving many consumers a predictable way to adopt that change.

That immediately explains why copy-paste is the real enemy. If there is no shared interface, there is no single place where change can be introduced and propagated deliberately.

### Copy-paste hurts because duplicates do not stay identical; they accumulate separate histories.
Three copied environment configs start the same, but each one gets changed in response to local needs. Those changes are usually reasonable in isolation. The problem is that the copies stop being instances of one pattern and become three unrelated configurations that merely share ancestry. The maintenance cost then becomes proportional to the number of copies, plus the effort of understanding how each one has drifted.

Once you see divergence as the mechanism, modules make more sense. A module is a way to keep many consumers tied to one maintained implementation while still allowing a controlled set of differences.

### That means the important part of a module is its interface: what varies, what is fixed, and what is exposed.
A module has inputs, internal resources, and outputs. Inputs define the sanctioned variation between uses. Internal resources are the implementation choices the module owns. Outputs define what downstream consumers may rely on. Together, those three parts form a contract.

This leads directly to the hardest design decision: where to draw the boundary between caller control and module opinion. If too much is an input, consumers can all drift in behavior even though they “use the same module.” If too little is an input, consumers will fork or bypass the module as soon as reality differs from the designer’s assumptions.

### The central tension in module design is flexibility versus consistency.
Every input variable is permission for callers to differ. Every hardcoded internal is a rule the module enforces. If secret encryption is an optional boolean input, then some environments may disable it. If it is always on inside the module, then the module enforces compliance by construction.

This is not just a style choice. It determines whether the module actually reduces future change cost. Too-flexible modules push complexity outward: callers must still understand and choose many low-level settings. Too-rigid modules fail to survive real usage and get forked, recreating the same divergence problem modules were supposed to solve.

### Once modules are used together, they form a dependency graph rather than isolated building blocks.
Real systems are built by wiring modules together: network feeds cluster, cluster feeds database, and so on. Outputs from one module become inputs to another. Terraform uses those references to infer order. So module design is not only about reuse; it also shapes the graph of dependencies and therefore the operational behavior of planning and applying changes.

And once composition exists, abstraction depth becomes a tradeoff. Nesting modules can simplify the caller’s view, but it can also make plan output harder to interpret because the actual changed resource may be buried several layers down.

### Because modules are consumed by many callers, versioning becomes part of the design, not an afterthought.
A pinned module version means consumers are protected from surprise changes. That is good because infrastructure changes are consequential and deserve explicit review. But pinning also means each consumer upgrades on its own timeline. Over time, different environments end up on different module versions.

That creates a new maintenance problem: version sprawl. The same mechanism that makes upgrades safe also makes stale consumers easy to ignore. So a module interface must be treated like a public API. Breaking changes are painful because every caller must coordinate code changes with the version bump.

### Modules are harder to refactor than application helpers because state ties structure to real infrastructure.
In application code, moving a function is often just code motion. In Terraform, moving a resource between modules changes its address in state. Terraform may interpret that as “old thing gone, new thing needed,” which can trigger destructive actions. Preventing that requires explicit state migration or moved declarations.

This is why module boundaries become sticky. Refactoring a bad boundary later is not just a readability improvement; it is a migration of Terraform’s identity mapping for real infrastructure. That cost makes early boundary decisions much more consequential than many engineers expect.

### So the right module boundary is defined by what should change together, be versioned together, and be constrained together.
If you organize modules around “what code is duplicated,” you risk making abstraction choices based on syntax rather than operational behavior. A better question is: which infrastructure pieces should share one contract and one upgrade path? Things that should evolve together belong behind the same module interface. Things that need independent lifecycles or independent policies likely should not.

That framing also clarifies the common failure modes. A god module groups too much under one contract, forcing unrelated things to change together. An over-parameterized wrapper groups too little under one opinion, exposing everything and enforcing nothing. Good module design sits between those extremes.

---

## Handles and Anchors

### 1. “A module is a versioned API with side effects.”
This is probably the best single mental model. Inputs are API parameters, outputs are the response, the internals are implementation, and the side effects are real cloud resources that persist in the world. That is why backward compatibility, versioning, and upgrade coordination matter so much more than “did we avoid repetition?”

### 2. “Copy-paste fails in maintenance, not creation.”
If you need a quick explanation for a colleague: duplication is not expensive when you create it; it becomes expensive when each copy lives a different life and you later need one safe change everywhere. That sentence gets you to the real reason modules exist.

### 3. Ask: “What should change together?”
When looking at a possible module, use this test. If these resources need the same policy decisions, the same upgrade cadence, and the same interface contract, grouping them may make sense. If not, the boundary is probably wrong. This question is more reliable than “what looks reusable?”

---

## What This Changes When You Build

### An engineer who understands this will extract modules later and with more evidence, because the real cost is locking in a public contract plus state structure.
The unaware engineer often pulls a module out after the first duplicated block because it “feels cleaner.” That usually bakes one use case’s assumptions into an interface that later proves wrong. The aware engineer waits until there are multiple concrete consumers and uses those cases to discover which variations are truly needed.

### An engineer who understands this will design fewer, more meaningful inputs, because every exposed variable is a place where consumers can diverge.
The unaware engineer often exposes every provider argument “for flexibility.” The result is a wrapper that adds indirection but does not enforce standards. The aware engineer asks which choices must remain caller-controlled and which should be fixed inside the module to guarantee consistency, security, or operability.

### An engineer who understands this will treat module versioning as an operational process, not just a source syntax detail, because pinning prevents surprise but creates drift.
The default failure is to pin versions and then never build inventory or upgrade discipline around them. Environments quietly age. The aware engineer sets up a way to see which consumers are on which versions and treats security or breaking upgrades as work that must be actively driven.

### An engineer who understands this will be cautious about deep nesting, because abstraction depth increases debugging and review cost.
The default move is to keep decomposing for elegance until plan output becomes unreadable and diagnosing a change requires traversing several layers of modules. The aware engineer still composes modules, but watches whether the abstraction is actually reducing caller complexity or just hiding behavior behind longer addresses.

### An engineer who understands this will treat module refactors as infrastructure migrations, because changing structure can change state addresses and trigger destructive plans.
The unaware engineer sees “split this big module into two” as a code cleanup task. The aware engineer immediately asks: what resource addresses will change, how will state be migrated, what happens if a pipeline runs mid-migration, and which resources are too dangerous to move casually? That shift in mindset prevents outages caused by innocent-looking reorganizations.
