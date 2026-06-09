## Metadata
- **Date:** 01-01-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# 3.2 Security (DevSecOps)

The traditional model of software security treated it as a final gate: you built the software, you shipped it, and then a security team audited it before (or unfortunately, after) production. This model is too slow, too late, and too disconnected from the development process to be effective. DevSecOps is the philosophy of integrating security practices directly into the development lifecycle, making security a continuous responsibility rather than a periodic event.

The **"shift left" principle** describes moving security checks earlier in the development process. The cost of remediating a security vulnerability increases dramatically the later it is found. A vulnerability found by a developer in their IDE costs minutes to fix. The same vulnerability found in a security audit after deployment costs days of engineer time, stakeholder communication, and potentially customer trust. The practical implementation of shifting left includes integrating **software composition analysis (SCA)** tools into your CI pipeline (automatically scanning your dependencies for known vulnerabilities every time you build), integrating **static application security testing (SAST)** tools that analyze your code for common vulnerability patterns (SQL injection risks, insecure deserialization, hardcoded credentials) without running the code, and educating developers on secure coding practices so that vulnerabilities are less likely to be introduced in the first place.

**Supply chain security** has become a critical concern in the current era. The attack surface of your application is not limited to the code you write; it extends to every dependency you import, every tool you use in your build process, and every artifact you pull from an external registry. Supply chain attacks work by compromising a widely-used library or build tool, inserting malicious code into it, and waiting for everyone who depends on that library to pull the update and execute the malicious code as part of their own application. Defenses include dependency pinning and lock files (preventing silent updates to newer, potentially compromised versions), cryptographic signature verification of dependencies (verifying that the artifact you downloaded matches a signature created by the author), and Software Bill of Materials (SBOM) generation (producing a machine-readable manifest of every component in your deployed artifact so that if a new vulnerability is discovered, you can immediately determine whether you are affected).

**Secret management** is the practice of handling credentials, API keys, passwords, and certificates securely. The most common failure mode is hardcoding secrets in application code or configuration files that are stored in version control. Once a secret is committed to a Git repository, it is there forever (in the history), even if you delete it from the current branch. The correct practice is to never allow secrets to touch your codebase at all. Instead, secrets are stored in a dedicated secret management service, injected into your application at runtime (as environment variables or mounted files), and rotated regularly. Access to secrets is controlled and audited: your application can only access the specific secrets it needs (least-privilege access), and every access is logged.

**The least-privilege principle** applies broadly to your operational architecture. Every service, every user, every automation job should have exactly the permissions it needs to do its job and no more. A service that needs to read from one database should not have write permissions, should not have access to other databases, and should not have administrative permissions of any kind. This principle limits the blast radius of a security breach: if an attacker compromises a service, they gain only the permissions that service held, not administrative access to your entire infrastructure.

**Runtime security** is the security layer that operates after deployment, when the code is running. Network policies define which services are allowed to communicate with which other services, preventing lateral movement in the event of a compromise (if an attacker compromises your web server, a network policy can prevent them from using it to attack your database directly). Runtime anomaly detection watches for behavior that is unusual for a given service (a web server suddenly making outbound SSH connections, a batch processing job suddenly reading files it has never accessed before) and raises alerts. **Compliance as code** is the practice of encoding regulatory or organizational security requirements as automated policy checks that run in your CI/CD pipeline and on your running infrastructure, turning security compliance from a periodic manual audit into a continuous automated verification.

## Level 2 candidates

**Shifting Security Left: From Audit to Embedded Practice**

What it means to integrate security checks into the development and CI pipeline rather than gating at the end of a release cycle, including the difference in the cost and speed of remediating a vulnerability found in development versus one found in production. It matters because the traditional security gate model creates adversarial dynamics between development and security teams and produces systems where security debt accumulates faster than it is addressed.

**Threat Modeling: Thinking About What Can Go Wrong Before You Build**

The practice of systematically identifying assets, threats, vulnerabilities, and controls before implementation using frameworks like STRIDE, and why this produces better security outcomes than reactive patching. It matters because most security vulnerabilities are not exotic — they are predictable failure modes that a structured thinking exercise would have identified, and the cost of a design-time fix is a fraction of a post-deployment one.

**The OWASP Top 10: The Recurring Vulnerability Classes**

The most common and impactful categories of web application vulnerability including injection, broken authentication, insecure deserialization, and security misconfiguration, at a conceptual level focused on why each class keeps appearing rather than how to exploit it. It matters because these vulnerability classes recur because the conditions that produce them are built into the default behaviors of frameworks and development habits, and recognizing the pattern is the first step to avoiding it.

**Static and Dynamic Analysis: SAST and DAST**

How static analysis tools inspect source code without executing it to find vulnerability patterns, versus dynamic analysis tools that send crafted inputs to a running application to probe its behavior, and what each catches and misses. It matters because security scanning is often treated as a checkbox without understanding that the two approaches cover fundamentally different attack surfaces, and relying on only one produces dangerous blind spots.

**The Principle of Least Privilege: Why Permissions Should Be Minimal by Default**

The security principle that every component, service, and user should have exactly the permissions required for their function and no more, and what the blast radius of a compromise looks like under least privilege versus under ambient broad access. It matters because the most common escalation path in cloud infrastructure breaches is exploiting overpermissioned roles and service accounts, and this principle is the primary mitigation.

**Secrets and Credential Management: Injection, Rotation, and Audit**

How secrets should be stored outside of source control and environment variables, injected at runtime by a secrets management system, rotated on a schedule, and audited for access. It matters because static, long-lived credentials are the most common single point of failure in cloud security posture, and the operational model for managing them is fundamentally different from managing configuration.

**Supply Chain Security: SBOMs, Signing, and Dependency Provenance**

How software bill-of-materials documents enumerate all components in an artifact, how artifact signing provides cryptographic proof of origin, and what policies around dependency provenance mean for build systems. It matters because attackers have shifted to targeting the dependency supply chain precisely because most organizations have hardened their own code while leaving dependencies largely unchecked.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Modern software is built and shipped too quickly for security to work as a separate, end-of-process checkpoint. Teams deploy many times a day, pull in hundreds of dependencies, and rely on automated pipelines and cloud infrastructure. In that environment, a security review that happens only before release is not just inconvenient — it misses the point. By the time a problem is found, the code is already entangled with other changes, the vulnerable artifact may already be deployed, and the fix is much more expensive.

What breaks when engineers do not understand this is not only “security” in the abstract. Delivery slows down because late security findings block releases. Incident response gets harder because teams do not know what is running or what it depends on. Small mistakes — a leaked credential, an over-permissioned service, a silently updated dependency — turn into large incidents because the system was built without controls at the points where risk actually enters. DevSecOps exists because security has to keep up with how software is really made.

## What You Need To Know First

### 1. CI/CD pipeline

A CI/CD pipeline is the automated path code takes from commit to deployment. It usually runs tests, builds artifacts, and may deploy them. You need this idea because DevSecOps works by inserting security checks into that same path, so security becomes part of normal delivery rather than a separate activity.

### 2. Dependencies

Dependencies are libraries, packages, base images, and tools your software relies on instead of writing everything from scratch. They save time, but they also expand your risk surface, because a weakness in something you imported can become a weakness in your application.

### 3. Permissions and identity

Permissions define what a user, service, or job is allowed to do. Identity is how the system knows who or what is making a request. This matters because many security controls are really about constraining capability: even if something is compromised, it should not automatically gain broad access.

### 4. Runtime versus build time

Build time is when code is compiled, packaged, and prepared. Runtime is when the deployed system is actually executing. This distinction matters because some security problems can be prevented before release, while others must be detected or constrained after the system is live.

## The Key Ideas, Connected

**DevSecOps means security is built into delivery, not added after the fact.**

What this really means is that security stops being a specialized review step at the edge of the process and becomes part of how software is designed, coded, built, deployed, and operated. The point is not “developers now do everything.” The point is that the system of work is arranged so security checks happen where code and infrastructure are already changing. Once you see security as part of the delivery system, the next question becomes: where in that system do checks have the most leverage?

**The first big move is to shift security checks left, toward the moment changes are made.**

“Shift left” means finding problems earlier, when the engineer still has the code in context and the fix is small. A hardcoded secret caught in an IDE or a vulnerable package caught during a pull request is cheap and local. The same issue found after deployment becomes operational work: rollback decisions, audit trails, coordination, and possibly customer impact. This is why tools like SAST and SCA belong in development workflows and CI pipelines. Once you accept that earlier detection is cheaper, you are naturally pushed to ask: what exactly are we trying to detect early?

**A major category of risk comes from software you did not write yourself.**

The article expands the threat model from “our code might be insecure” to “our entire software supply chain can be a path for compromise.” Your application includes open-source packages, container images, build tools, registries, and transitive dependencies. If one of those is compromised, your pipeline can faithfully pull, build, and ship malicious code for you. That is why supply chain security matters: modern systems inherit risk through reuse. Once that becomes clear, the next step is to ask how you make that inherited risk visible and controllable.

**Supply chain defense is about making inputs explicit, stable, and verifiable.**

Dependency pinning and lock files make versions predictable instead of allowing silent drift. Signature verification helps answer, “Did this artifact really come from who I think it came from, and was it altered?” SBOMs answer a different question: “What is actually inside what I shipped?” These controls do not eliminate dependency risk, but they turn it from an invisible moving target into something you can inspect, reason about, and respond to. And once you start thinking in terms of controlling sensitive inputs, credentials become impossible to ignore.

**Secrets are dangerous because they grant access directly, and version control preserves mistakes permanently.**

A secret is not just data; it is capability. If an API key or password is committed to a repository, the problem is not solved by deleting it from the latest file, because the history still contains it and copies may already exist elsewhere. So secret management is not merely “store secrets more carefully.” It is a design rule: secrets should be kept outside the codebase, delivered to applications only when needed, and rotated so exposure does not remain valuable forever. Once you treat secrets as runtime-delivered capabilities, the broader security pattern becomes clearer: every capability should be deliberately constrained.

**That broader pattern is the principle of least privilege.**

Least privilege means each user, service, or automation job gets only the permissions required for its job and nothing extra. This matters because compromise is never fully preventable; what you can control is how far compromise can spread. If a service only has read access to one database, then taking over that service does not automatically grant write access, admin access, or access to unrelated systems. In other words, least privilege turns security architecture into blast-radius management. And once you focus on blast radius, you are led to think not just about permissions, but about what happens after deployment if something still goes wrong.

**That is where runtime security comes in: some defenses must operate on live systems, not just source code.**

Static checks can catch known bad patterns before release, but they cannot fully predict real behavior in production. Runtime controls limit or observe what running services are allowed to do. Network policies prevent unexpected service-to-service communication and make lateral movement harder. Anomaly detection looks for behavior that does not match the service’s normal role. These controls assume that some issues will escape earlier stages, so the running system needs guardrails and sensors. Once security is happening continuously in production too, compliance also starts to look different.

**Compliance as code turns policy from a periodic audit artifact into an automated engineering constraint.**

Instead of treating regulatory or organizational requirements as paperwork checked by humans every few months, compliance as code expresses those requirements as machine-enforced rules in pipelines and infrastructure. That means the same system that checks tests or deployment manifests can also check whether encryption is enabled, whether public exposure is blocked, or whether approved configurations are being used. This idea follows naturally from the rest of DevSecOps: if security is continuous, then governance has to become continuous too. The full chain is: integrate security into delivery, move checks earlier where possible, control the software you ingest, protect the capabilities you issue, limit blast radius when compromise happens, and enforce policies continuously across build and runtime.

## Handles and Anchors

### 1. Security is not a fence at the end; it is guardrails along the road.

A fence at the end only tells you that you crashed. Guardrails along the road keep small mistakes from turning into disasters while you are still moving. That is the core mental model of DevSecOps: security belongs throughout the path from commit to production.

### 2. Every dependency and every secret is borrowed power.

A dependency is code you are trusting to act inside your system. A secret is authority you are handing to a process. Thinking of both as borrowed power helps explain why they need control, verification, and visibility rather than convenience-driven handling.

### 3. The goal is not “prevent every breach”; the goal is “make compromise small, visible, and recoverable.”

This is the tension that ties the whole topic together. Shift-left practices try to prevent issues early. Least privilege and network policy try to make escapes smaller. Runtime monitoring and compliance automation try to make problems visible quickly and keep systems within acceptable bounds.

## What This Changes When You Build

- An engineer who understands this will put security checks inside the normal CI path rather than relying on a separate review stage, because the cheapest fix is the one made while the change is still small and local.
- An engineer who understands this will treat dependency upgrades as controlled changes with pinning, lock files, and provenance checks, because “we imported it from a trusted registry” is not the same as “we know exactly what we are running.”
- An engineer who understands this will design applications so secrets are injected at runtime from a secret manager rather than stored in config files or repositories, because once credentials enter source control the exposure is durable and cleanup becomes much harder than replacement.
- An engineer who understands this will scope service accounts, IAM roles, and database permissions narrowly from the start, because permission design is really incident containment design: the rights you grant during calm conditions define the attacker’s reach during a breach.
- An engineer who understands this will add runtime controls such as service-to-service network restrictions and anomaly detection, because pre-deployment scanning cannot prove that a live system will only behave in expected ways once it is under real traffic and real operational conditions.

</details>
