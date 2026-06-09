## Metadata
- **Date:** 18-05-2026
- **Source:** 12_cloud_security.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Cloud Security

The instinct when you first think about cloud security is to treat it as a relocation problem: you had servers in a room, now you have servers in someone else's room, and the job is to rebuild the same fences a little further away. This is wrong in a way that quietly produces most of the breaches you read about. Moving to the cloud does not move your perimeter — it dissolves it. The walls you used to rely on were physical, the machines were yours, and the people with hands on them worked for you. None of that survives the migration. What replaces it is a stack of shared hardware, logical boundaries enforced by software, and a contract with a provider that hands you back exactly half of the security problem and tells you the rest is yours to solve.

The first mental shift is the shared responsibility model, and getting it wrong is the single most common source of cloud incidents. The provider — AWS, Azure, GCP — secures the infrastructure: the data centres, the hypervisors, the physical network, the patching of the underlying platform. You secure everything you put on top of it: your data, your access configurations, your application code, and the rules about who can touch what. The shape of that split changes depending on whether you are using IaaS (you get a virtual machine and own almost everything above the hypervisor), PaaS (the provider runs the runtime, you own the app and the data), or SaaS (the provider runs almost everything, you own the data and the access policies). The mistake is assuming the provider has done more than they have. A public S3 bucket is not the provider's fault. A leaked admin credential is not the provider's fault. Almost nothing that goes wrong in the news is the provider's fault.

The second shift is understanding what multi-tenancy actually means. Your virtual machine is sharing physical hardware with strangers. The isolation between you and them is logical — enforced by the hypervisor and the operating system — not physical. For most purposes this is fine, but "most purposes" is doing a lot of work in that sentence. Side-channel attacks like Meltdown and Spectre demonstrated that the CPU itself can be coaxed into leaking data across these logical boundaries, because the speculative execution machinery doesn't respect them the way the operating system pretends it does. There is also the more mundane "noisy neighbour" problem, where another tenant's workload degrades yours because you are competing for the same physical resources. The defensive response is to assume isolation is a probabilistic property, not a guarantee, and to encrypt data in use — via hardware enclaves like Intel SGX or ARM TrustZone — when the workload genuinely warrants it.

The third shift is that identity becomes the perimeter. In the on-premises world, getting inside the network was a meaningful step that often gave an attacker a lot for free. In the cloud, there is no inside. Every service is reachable from somewhere, every action goes through an API, and every API call is authenticated. This means Identity and Access Management — IAM — stops being a back-office concern and becomes the primary control plane for security. The principle of least privilege isn't a nice-to-have; it is the wall. If your IAM policies are loose, you have no perimeter. If a developer's credentials end up in a public GitHub repository, the attacker doesn't need to breach a firewall — they just log in. This is why MFA on every privileged account, hardware-backed where possible, is the lowest-hanging fruit in cloud security and also the one most often skipped.

Network controls still exist, but they look different. Security Groups operate at the instance level and are stateful — they remember a connection so that return traffic is allowed automatically. Network ACLs operate at the subnet level and are stateless — every packet is evaluated independently. You use them together: NACLs for broad subnet-level filtering, Security Groups for granular instance-level rules. The pattern is defence in depth applied to a network that no longer has a clean edge.

The fourth shift is that defence cannot be a phase. In on-premises operations you could plausibly run a security review before a release and call it done. In the cloud, infrastructure is code, deployments happen continuously, and the surface area changes faster than any human review process can keep up with. This is the argument for DevSecOps: security checks — code scanning, secret detection, configuration validation — get baked into the CI/CD pipeline so that every change is evaluated automatically before it ships. The complement to this is telemetry. You assume breach, because the alternative is to assume you've solved a problem nobody has solved, and you instrument everything: API calls (CloudTrail and its equivalents), network flows, system logs, all flowing into a SIEM where deviations can be detected and, increasingly, responded to automatically through SOAR playbooks. Human analysts cannot read logs at cloud scale. The only viable model is automation, with humans tuning the automation.

What this all adds up to is a different posture. Conventional security was about hardening a shell. Cloud security is about accepting that the shell is porous, that isolation is logical, that change is constant, and that the only durable defences are the ones encoded into identity, into the pipeline, and into the telemetry that watches what actually happens. The skill this builds is the ability to look at any cloud workload and ask the right four questions: who can touch this, what state is the data in when it's touched, what would I see if it went wrong, and how would I know in time to do something about it.

## Level 2 candidates

**The shared responsibility model across IaaS, PaaS, and SaaS** — Maps exactly which security obligations belong to the provider and which belong to the customer at each service tier, with worked examples. Worth a deep dive because misreading this boundary is the modal cause of cloud breaches and the answer is not intuitive — it shifts service by service.

**Multi-tenancy and side-channel attacks** — Covers how hypervisor isolation works, where it leaks (Meltdown, Spectre, and their successors), and the role of hardware enclaves like Intel SGX and ARM TrustZone in protecting data in use. Worth going deeper because this is where cloud security stops being a configuration problem and becomes a hardware problem, and the defences are non-obvious.

**IAM as the new perimeter** — Covers least privilege, role-based and attribute-based access control, MFA strategies (including FIDO hardware keys), and the failure modes of cloud identity systems. Worth a Level 2 because IAM is simultaneously the most important and most commonly mis-configured cloud security control, and the design space is large.

**Network controls in the cloud: Security Groups vs NACLs** — Covers stateful instance-level filtering, stateless subnet-level filtering, and how to compose them for defence in depth. Worth deeper treatment because the stateful/stateless distinction has subtle operational consequences that bite teams who haven't thought through them.

**DevSecOps and shift-left security** — Covers integration of security scanning into CI/CD pipelines, secret detection, infrastructure-as-code validation, and the cultural shift from gate-based to continuous security. Worth a Level 2 because the tooling is concrete (SonarQube, Snyk, policy-as-code) and the workflow design has real depth.

**Telemetry, SIEM, and SOAR** — Covers the logging surface in a cloud environment (CloudTrail and equivalents), aggregation into SIEMs, and automated response via SOAR playbooks. Worth going deeper because "assume breach" is only meaningful if you can operationalise detection and response, and the architecture for doing so at cloud scale is its own discipline.

**Data sovereignty, compliance, and systemic risk** — Covers the tension between regulatory requirements (GDPR, HIPAA, MAS) that pin data to geographies and the disaster-recovery model that depends on geographic diversity, plus the systemic risk created by hyperscaler concentration. Worth a Level 2 because the trade-offs are strategic rather than technical and shape architecture decisions that are expensive to reverse.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

A lot of security intuition was built in a world where systems had a location, a boundary, and a relatively stable shape. You could picture the network, put controls at the edge, and treat "inside" and "outside" as meaningful categories. Cloud systems break that mental model. Resources appear and disappear continuously, access happens through APIs rather than cable-connected machines, and the infrastructure itself belongs to someone else. If you keep using the old model, you will protect the wrong things.

That is why cloud breaches so often look embarrassingly simple in hindsight. Not because cloud security is trivial, but because teams often defend infrastructure ownership while the real risk sits in identity, configuration, and automation. The practical failure mode is not usually "the cloud provider got hacked." It is "we misunderstood which part was ours to secure," or "we left too much access in place," or "we had no way to detect bad behavior quickly enough."

So this topic matters because cloud security is not just traditional security with new tooling. It requires a different operating model. If you do not internalize that shift, you can spend heavily on protection and still leave the most dangerous paths wide open.

## What You Need To Know First

**Virtualization**  
A cloud "server" is usually not a whole physical machine. It is a virtual machine, meaning software slices one physical computer into multiple isolated environments that behave like separate computers. This matters because many security assumptions in the cloud depend on trusting that software-based isolation is strong enough.

**Service models: IaaS, PaaS, SaaS**  
These describe how much of the stack the provider runs for you. In IaaS, you get basic infrastructure and manage most things above it. In PaaS, the provider also manages the runtime platform. In SaaS, the provider manages almost the whole application, and you mostly control data and user access. You need this because the security boundary moves depending on the model.

**Identity and Access Management (IAM)**  
IAM is the system that decides which users, services, or applications can do which actions on which resources. In cloud systems, this is not an administrative afterthought; it is often the main gatekeeper between a safe system and a compromised one.

**CI/CD and infrastructure as code**  
CI/CD means software changes are built, tested, and deployed automatically and frequently. Infrastructure as code means your cloud resources are defined in files and created by automation, not by clicking around manually. These matter because cloud environments change too fast for occasional manual security review to be enough.

## The Key Ideas, Connected

**Cloud security is not a relocation problem; it is a model change.**  
The article starts by trying to break a very natural instinct: "we moved our servers elsewhere, so now we just need equivalent protections in the new place." What actually changes is deeper than location. You no longer control the hardware, the physical access, or the clean network edge in the same way. That means the old picture of a defended castle no longer tells you where the real risks are. Once that old picture is gone, the next question becomes: if the provider owns part of the stack, what exactly is still yours to secure?

**The shared responsibility model tells you where provider security ends and your security begins.**  
This is the first core boundary to understand. The provider secures the underlying cloud infrastructure, but you secure what you deploy, configure, and permit on top of it. That sounds simple until you notice that the line moves across IaaS, PaaS, and SaaS. In IaaS, you own much more of the stack. In SaaS, you own much less operational infrastructure, but you still own critical things like data handling and access control. This matters because many teams accidentally outsource responsibility in their heads before they have actually outsourced it in reality. Once you understand that the provider does not absorb your mistakes, the next issue is whether the environment you are building on is truly isolated from everyone else using it.

**Cloud isolation is real, but it is logical rather than absolute.**  
Your workload is usually sharing physical hardware with other tenants. The separation is enforced by software and platform controls, not by dedicated physical ownership. Most of the time that is good enough, but the article wants you to stop thinking of isolation as a perfect wall. Side-channel attacks show that lower-level hardware behavior can sometimes leak information across boundaries that look secure at the operating-system level. Even without exotic attacks, shared resources can create performance interference through noisy neighbors. This leads to a more mature stance: isolation is something you evaluate and strengthen, not something you treat as magically guaranteed. Once the perimeter is no longer physical and the hardware boundary is not absolute, you need a new place to anchor your security model.

**In the cloud, identity becomes the perimeter.**  
If every important action happens through an authenticated API, then access control is no longer just one control among many. It becomes the main way the system decides what is allowed. In older environments, getting onto the internal network often gave an attacker a strong starting position. In cloud environments, possession of valid credentials and permissions is often the attack path itself. That is why least privilege matters so much: it is not bureaucratic neatness, it is structural defense. If identities are over-permitted, the system is effectively open in the places that matter most. Once you accept that identity is central, you can see network controls differently too: still useful, but no longer the singular outer wall.

**Network controls still matter, but now they support identity-centered security instead of replacing it.**  
The article uses Security Groups and NACLs to show that cloud networking still has filtering layers, just not in the same old perimeter-centric shape. Security Groups are stateful and attached more closely to instances. NACLs are stateless and operate at the subnet level. The important point is not memorizing their definitions; it is understanding that cloud defense becomes layered and compositional. You build broad constraints in one place and more specific constraints in another. But even that is not enough on its own, because cloud systems change too quickly for static controls and occasional review to keep up.

**Because cloud environments change continuously, security has to be built into the delivery process.**  
If infrastructure is created from code and deployments happen constantly, then security cannot sit at the end as a human checkpoint. By the time someone manually reviews a system, the system may already have changed several times. That is the case for DevSecOps: security checks need to run automatically inside the same machinery that builds and ships software. Secret scanning, configuration validation, dependency checking, and policy enforcement all move earlier and become continuous. This naturally creates the next requirement: if systems are changing automatically at scale, you also need automated ways to observe what they are doing after deployment.

**Telemetry turns "assume breach" from a slogan into an operating model.**  
The article argues that at cloud scale, detection cannot depend on people manually reading logs. You need broad instrumentation of API calls, network activity, and system events, and you need those signals aggregated somewhere they can be analyzed. SIEM and SOAR are the operational consequence of that need: one centralizes and correlates signals; the other automates response workflows. The deeper point is that cloud security is not just about preventing every bad action in advance. It is also about making sure bad actions become visible quickly enough to contain. That leads to the article's final posture shift.

**Cloud security is really a practice of encoding trust boundaries into access, automation, and visibility.**  
All the earlier ideas connect here. Shared responsibility tells you what you own. Multi-tenancy tells you not to over-trust isolation. IAM tells you where the real gatekeeping happens. Network controls add layered containment. DevSecOps makes protection continuous. Telemetry makes detection and response possible. Together they replace the old goal of building a hard shell. The new goal is to design systems where permissions are narrow, change is checked automatically, and abnormal behavior is visible fast enough to matter.

## Handles and Anchors

**Handle 1: The cloud is not a castle; it is an airport.**  
In a castle model, thick walls matter most. In an airport model, identity checks, controlled zones, and surveillance matter most. Lots of people share the same physical structure, and the key question is not "are they inside the building?" but "what are they allowed to access, and how quickly will we notice if they go somewhere they should not?"

**Handle 2: Shared responsibility means "managed" does not mean "safe by default."**  
A useful sentence to remember is: *the provider secures the platform; you secure your use of the platform.* That one line prevents a lot of bad assumptions.

**Handle 3: In the cloud, permissions are architecture.**  
Do not think of IAM as paperwork. Think of it as part of the system design itself. If compute, storage, and deployment pipelines can all be driven through APIs, then permission structure is as fundamental as network topology used to be.

## What This Changes When You Build

**An engineer who understands this will treat service selection as a security design choice, because moving from IaaS to PaaS to SaaS changes which controls must be owned and operated internally.**  
That affects procurement, architecture reviews, and staffing. A team choosing IaaS is not just choosing flexibility; it is accepting a larger operational security surface.

**An engineer who understands this will design IAM early and explicitly, because over-broad permissions in the cloud create direct compromise paths without needing a traditional network breach.**  
That changes how roles are defined, how machine identities are issued, how temporary credentials are preferred over static ones, and how privileged access is reviewed.

**An engineer who understands this will be more deliberate about where sensitive workloads run, because multi-tenancy risk is usually acceptable but not always negligible.**  
That changes decisions about workload placement, use of confidential computing or enclaves, tenant isolation requirements, and whether certain data should be processed only under stronger hardware-backed protections.

**An engineer who understands this will build security checks into delivery pipelines, because manual review cannot keep pace with cloud infrastructure that is created and modified continuously.**  
That changes how pull requests are validated, how secrets are prevented from entering repositories, how infrastructure templates are policy-checked before deployment, and how failed security gates block release automatically.

**An engineer who understands this will invest in logs and detection as part of the product environment, because prevention failures are inevitable and response speed depends on visibility.**  
That changes whether audit logging is enabled by default, whether logs are centralized and retained correctly, whether detection rules exist for dangerous API actions, and whether common incidents have automated containment playbooks ready to run.

</details>
