## Metadata
- **Date:** 01-01-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# 2.5 Continuous Delivery and Deployment (CD)

Continuous Delivery is the practice of keeping your software in a state where it can be deployed to production at any time. Continuous Deployment is the practice of automatically deploying every change that passes CI to production without human intervention. The distinction matters: Continuous Delivery requires a human decision to deploy; Continuous Deployment automates even that decision. Many organizations practice Continuous Delivery (the pipeline goes all the way to a pre-production environment automatically, and production deployment is triggered manually) because some deployment targets require a deliberate human act for regulatory or risk management reasons.

The most important conceptual refinement in this segment is the **decoupling of deployment from release**. These two acts are often conflated, but separating them is the key to making deployment genuinely low-risk. A **deployment** is the technical act of placing new code onto infrastructure. A **release** is the business act of making new functionality visible to users. By deploying code behind a **feature flag** (a configuration toggle that controls whether the code path is active), you can put new code in production while it is invisible to users. The code runs, you can observe its performance and error rates, you can run it alongside the old code path in a shadow mode, and you can release it to a small percentage of users (say, 1%) before releasing it to everyone. If problems emerge, you toggle the flag off in seconds without any deployment at all. This model changes the risk calculus of deployment fundamentally: you are no longer choosing between "deploy and risk user impact" and "don't deploy and accumulate risk in a large batch." You are continuously deploying small, dark changes and releasing them deliberately when you have sufficient confidence.

**Deployment strategies** describe the mechanics of how a new version of an artifact replaces an old version without causing downtime. In a **rolling update**, instances are updated one by one (or in small batches): some instances run the old version and some run the new version simultaneously during the rollout. This is simple and resource-efficient but means that for a period, different users may receive responses from different versions, which can cause inconsistency if the API has changed. In a **blue/green deployment**, you maintain two complete production environments ("blue" running the current version, "green" running the new version). Traffic is shifted from blue to green at the load balancer level, either all at once or gradually. Rollback is instantaneous: you redirect traffic back to blue. The cost is that you need double the infrastructure capacity during deployments. In a **canary release**, you route a small percentage of production traffic (say, 1% or 5%) to the new version and monitor its behavior. If metrics are healthy, you gradually increase the percentage. If they are not, you route the canary traffic back to the old version. This gives you the highest confidence in real-world performance but requires sophisticated traffic routing and automated metric comparison.

**Rollback strategies** are a critical operational consideration that is often neglected until an emergency. Rolling back a deployment, reverting to the previous artifact version, is not always possible. If the deployment included a database migration that added a column or changed a constraint, the previous version of the code may not be compatible with the new database schema. This is why the **expand and contract pattern** for schema changes is an operational discipline, not just a database concern. The pattern works in two phases: in the "expand" phase, you make the schema change backward-compatible (adding a new column without removing the old one), deploy the new code that can work with either schema, and verify stability. In the "contract" phase, you remove the old column once you are confident the new code is stable. This ensures that at every point in time, you can roll back the deployment without leaving the database in an incompatible state.

## Level 2 candidates

**Delivery vs Deployment: The Most Important Distinction in CD**

The specific difference between a pipeline that produces an artifact that *can* be deployed at any time (continuous delivery) versus one that deploys automatically on every successful build (continuous deployment), and why the choice between them is a business and risk management decision, not a technical one. It matters because confusion between these two concepts leads to teams building the wrong pipeline and not understanding their own release process.

**Deployment Strategies: Blue/Green, Canary, Rolling, and Recreate**

The mechanics of each strategy, what each one trades in terms of infrastructure cost, rollback speed, and blast radius of a bad deployment. It matters because the deployment strategy is the primary mechanism controlling how much production traffic is exposed to a new version at any given moment, and choosing between them requires understanding the failure modes of each.

**The Environment Pipeline: Promoting an Artifact Through Stages**

How a single artifact moves from CI through dev, staging, and production environments, what gates exist between stages, and what "environment parity" means and why its absence causes production surprises. It matters because every difference between a staging and production environment is a potential source of failures that only appear in production, and the environment pipeline is how you manage that risk.

**Rollback vs Roll Forward: Two Philosophies for Handling Bad Releases**

The distinction between reverting to a previous known-good version versus fixing forward by shipping a new version quickly, the conditions under which each is appropriate, and how deployment strategy choice affects which option is viable. It matters because under pressure during an incident, teams without a clear philosophy make the wrong choice and extend the duration of the failure.

**The Release as a Decoupled Event: Feature Flags and Dark Launches**

How decoupling the deployment of code from the activation of features gives teams control over the release experience independently of the deployment pipeline. It matters because this decoupling is the mechanism that makes continuous deployment safe for consumer-facing products where premature feature exposure has business consequences.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

As teams ship software more often, the deployment process itself becomes a source of risk. If every deploy is a tense, one-shot event where new code immediately hits every user, teams start batching changes together, delaying releases, and treating deployment like a dangerous ceremony. That slows delivery down and actually increases risk, because when something breaks, it is harder to tell which change caused it and harder to undo it safely.

Continuous Delivery and Deployment exist to solve that problem: how do you make change routine instead of dramatic? The answer is not just “automate more.” It is to change the shape of risk. Engineers need a way to put code into production safely, observe it under real conditions, and control user exposure separately from the act of moving bits onto servers.

If you do not have a working model of this, several things go wrong in practice. Teams confuse deployment with release, so every technical rollout becomes a business launch. They choose rollout strategies without understanding the failure modes. And they discover during an incident that “just roll it back” is not always possible, especially when the database has changed underneath them.

---

## What You Need To Know First

### 1. Production environment

A production environment is the live system real users interact with. It is different from development or staging because mistakes here affect actual customers, real data, and business operations. When this article talks about deployment risk, it means risk in that live environment.

### 2. Feature flag

A feature flag is a configuration switch that turns some behavior on or off without changing the deployed code. The important idea is that code can be present in production but inactive for users. That gives teams a control point after deployment.

### 3. Load balancer and traffic routing

A load balancer sits in front of your application instances and decides where incoming requests go. Traffic routing means controlling which requests go to which version of your service. You do not need the networking details here; just know that rollout strategies often work by changing traffic flow rather than replacing everything at once.

### 4. Database schema migration

A schema migration is a change to the structure of a database, such as adding a column, removing one, or changing constraints. These changes matter during deployment because application code and database structure must remain compatible. A code rollback is only safe if the old code can still work with the current schema.

---

## The Key Ideas, Connected

### 1. Continuous Delivery and Continuous Deployment are about keeping software always ready to ship, but they differ in who decides when production changes go live.

Continuous Delivery means the pipeline takes changes all the way to a deployable state, and a human still chooses when to push to production. Continuous Deployment goes one step further and automates that final production push whenever the pipeline passes. That distinction matters because it separates “we can deploy at any time” from “we always deploy immediately.” Once you see that difference, the next important question is why teams can safely move faster at all.

### 2. The real safety breakthrough is not just automation; it is separating deployment from release.

A deployment is the technical act of putting new code into production infrastructure. A release is the moment users are actually exposed to new behavior. Many people blur those together, but keeping them separate is what makes frequent deployment less risky. If code can be deployed without being visible, then production stops being the place where you instantly commit to full user impact. That is why feature flags matter next.

### 3. Feature flags let you deploy code without immediately releasing its behavior to users.

With a feature flag, the new code path can exist in production while remaining off for everyone, or on for only a tiny subset of cases. That means you can verify that the system starts, runs, logs correctly, and interacts with real infrastructure before making the feature broadly visible. This changes deployment from a cliff edge into a controlled ramp. Once you can keep deployed code dark, you can start asking how to expose it gradually and safely.

### 4. Gradual exposure changes the risk model from “big launch” to “measured rollout.”

Instead of deploying a large batch and hoping for the best, teams can ship small changes, observe real behavior, and increase exposure only when metrics look healthy. You are no longer forced to choose between shipping slowly for safety and shipping quickly with fear. Small, dark, reversible changes let you move often while keeping the blast radius low. From there, the next question becomes operational: by what mechanics do we replace the old version with the new one?

### 5. Deployment strategies are different ways of moving traffic from the old version to the new version without downtime.

A rollout strategy is the operational pattern for how both versions coexist during changeover. This is not just implementation detail; it determines what kinds of failures are likely, how much infrastructure you need, and how easy rollback will be. The article then introduces the three common patterns because each one makes a different tradeoff.

### 6. A rolling update trades simplicity and efficiency for a period of mixed-version behavior.

In a rolling update, you replace instances gradually, so some requests hit old code while others hit new code during the rollout. This is operationally straightforward and does not require doubling your whole environment. But it means the system is temporarily heterogeneous. If the old and new versions are not compatible with each other or with shared data formats, users may see inconsistent behavior. Once you recognize that mixed versions are the main risk here, you can see why some teams prefer stronger isolation.

### 7. Blue/green deployment trades extra infrastructure cost for cleaner cutover and faster rollback.

In blue/green, you keep two full environments: one serving traffic now, one holding the new version. Then you switch traffic from one to the other. This avoids the mixed-instance state of rolling updates and makes rollback very fast, because you can redirect traffic back to the old environment. The tradeoff is cost and operational overhead: during deployment you are effectively running both worlds. If you want even more confidence from real user behavior before full cutover, you move toward canarying.

### 8. A canary release trades routing complexity for the best real-world signal before full rollout.

With a canary, only a small percentage of real production traffic goes to the new version at first. If latency, error rates, and other metrics stay healthy, you increase the percentage gradually. This gives you feedback from actual users and actual workloads, not just test environments. But it depends on fine-grained traffic control and good automated monitoring, because the whole point is to detect subtle regressions before they affect everyone. Once you start relying on gradual rollout, rollback becomes the next serious concern.

### 9. Rollback is only easy if the old version is still compatible with the world the new version changed.

People often talk as if rollback simply means “redeploy the previous artifact.” That works only when the surrounding system still matches the assumptions of the old code. Database migrations are the classic place where this breaks down: if the new deployment changed the schema in a way the old code cannot understand, then rolling back the app may not restore the system safely. That is why deployment strategy must connect to schema change strategy.

### 10. The expand-and-contract pattern makes schema changes compatible with safe rollback.

In the expand phase, you introduce the new schema in a backward-compatible way, such as adding a new column while keeping the old one. Then you deploy code that can handle both shapes. Only after the new path is proven stable do you enter the contract phase and remove the old structure. The core idea is that every intermediate state must be safe for both forward movement and backward movement. That closes the loop on the article’s main theme: low-risk delivery is not one trick, but a chain of compatible practices that make change observable, gradual, and reversible.

---

## Handles and Anchors

### 1. Deployment is moving the furniture in; release is opening the room to guests.

You can set up a new room in a hotel before letting guests enter it. In the same way, you can put code into production before letting users experience it. That one distinction explains why feature flags reduce risk so much.

### 2. The core tradeoff is: the more gradually you expose change, the more control you gain, but the more operational machinery you need.

Rolling updates need less machinery but give less isolation. Blue/green gives cleaner switching but costs more. Canary gives the best live signal but requires sophisticated routing and monitoring. This is a useful sentence to keep in your head when comparing strategies.

### 3. “Can I roll back?” really means “Is the old code still compatible with the current reality?”

That reality includes the database schema, traffic routing, and any shared state. This handle helps prevent the common mistake of treating rollback as just a deployment button rather than a compatibility question.

---

## What This Changes When You Build

- An engineer who understands this will separate deployment workflows from release decisions because putting code in production and exposing it to users are different control points with different risks.
- An engineer who understands this will introduce feature flags for risky or user-visible changes because flags allow production validation and fast disablement without requiring a fresh deployment during an incident.
- An engineer who understands this will choose rollout strategy based on system compatibility constraints because mixed-version operation in a rolling update is acceptable only when old and new versions can safely coexist.
- An engineer who understands this will invest in canary metrics and traffic controls for high-risk services because a small slice of real production traffic reveals failure modes that staging and synthetic tests often miss.
- An engineer who understands this will design database migrations in expand-and-contract phases because rollback safety depends on keeping old and new application versions compatible with the schema throughout the transition.

</details>
