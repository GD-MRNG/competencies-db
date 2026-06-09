## Metadata
- **Date:** 18-05-2026
- **Source:** 10_system_security_and_access_control.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# System Security and Access Control

Most security failures are not break-ins. They are mundane: someone had access they shouldn't have had, or someone with legitimate access did something they shouldn't have been able to do. The Colonial Pipeline attack that disrupted fuel supply across the eastern United States and cost over a billion dollars did not begin with a novel exploit or a zero-day vulnerability. It began with a forgotten VPN account that nobody had bothered to decommission. The attackers did not break in — they logged in. This is the territory access control governs, and it is why the discipline matters far more than its dry vocabulary suggests.

The mental model to carry is simple enough to fit on a napkin. Every security-relevant event in a system is a triple: a subject (a user, a process, anything that acts) wants to perform an operation (read, write, execute) on an object (a file, a device, a service). Sitting between the subject and the object is a reference monitor — a conceptual guard that consults a security policy and decides whether to allow the request. Everything else in this topic is a refinement of that picture: how you represent the policy, where you store it, who is allowed to change it, and how you handle the awkward cases where the rules need to bend.

The representation question matters more than it sounds, because it determines what is easy and what is hard. The most general representation is the access control matrix: a giant grid where every row is a subject, every column is an object, and every cell records what that subject can do to that object. It is conceptually pure and operationally useless — in any real system the matrix is enormous and almost entirely empty. So in practice you slice it. Slice the matrix by columns and you get access control lists: each object carries a list of who can do what to it, which is what Linux, Unix, and Windows all use. Slice it by rows and you get capabilities: each subject carries a set of tokens or keys describing what it can do, which is closer to how session tokens and OAuth scopes work. ACLs make it easy to ask "who can touch this file?" Capabilities make it easy to ask "what can this user do?" Both questions are important, and the choice of representation determines which one is cheap and which one is expensive.

Linux makes a further compression that is worth understanding because you will hit it constantly. Rather than maintain a true ACL per file, the system collapses subjects into three buckets — owner, group, others — and operations into three bits — read, write, execute. That gives you nine bits per file, which you set with chmod, written either symbolically (rwxr-x---) or as the octal numbers everyone eventually memorises (read is 4, write is 2, execute is 1, so 750 means full access for the owner, read-and-execute for the group, nothing for the world). The compression is lossy — you cannot express "Alice can read but Bob cannot" without putting them in different groups — but it is fast, simple, and good enough for most purposes. When it is not good enough, getfacl and setfacl give you a real per-user ACL on top.

This neat picture has one ugly problem: sometimes a normal user legitimately needs to do something only an administrator should be able to do. Changing your own password, for example, requires writing to /etc/shadow, which is owned by root and unreadable to everyone else. The Unix answer is the setuid bit — a special permission that says "when this program runs, it runs with the privileges of its owner, not its caller." So /usr/bin/passwd is owned by root and setuid, which lets you, an ordinary user, briefly borrow root's authority for the narrow purpose of editing your own password line. This is called controlled invocation, and it is both indispensable and dangerous. Every setuid program is a trapdoor into root, and any bug in one — a buffer overflow, a sloppy argument check, an unsanitised environment variable — becomes a privilege escalation vulnerability. The defensive posture is to keep the setuid footprint as small as possible and audit what remains.

Behind all of this sits a principle worth taking seriously: least privilege. Every subject should have exactly the permissions it needs to do its job, and no more. The reason is not philosophical neatness; it is blast radius. When something goes wrong — and something always goes wrong — the damage is bounded by what the compromised account could do. A web server that runs as root and gets popped owns the machine. A web server that runs as its own unprivileged user with read-only access to its config and write access to one log directory has a much smaller bad day. Least privilege is the difference between an incident and a catastrophe, and it is mostly free if you set it up before you need it.

The modern reframing of all this is zero trust, which is less a technology than an admission. The old model assumed that once you were inside the network perimeter — past the firewall, on the corporate LAN, through the VPN — you were trusted. The Snowden disclosures, the Colonial Pipeline breach, and a thousand smaller incidents made it clear that this assumption is false: insiders go bad, credentials get stolen, legacy access points get forgotten, and "inside" is a meaningless concept when half your workforce is remote and your infrastructure lives in someone else's data centre. Zero trust replaces the perimeter with three working assumptions — always verify, grant least privilege, assume breach — and applies them at every layer rather than once at the gate. In practice this looks like short-lived credentials instead of permanent ones, continuous re-authentication instead of single sign-on for life, and policies expressed in terms of identity and context rather than network location.

What you should walk away with is not a list of commands but a way of looking at systems. When you see a security incident, ask: which subject, which operation, which object, and why did the reference monitor say yes? When you design a system, ask: what is the smallest set of permissions this component needs, and what happens when it is compromised? Most of the access control you will ever configure is a variation on chmod and group membership. Most of the access control you will ever debug is a variation on someone having more privilege than they needed at the moment something went wrong.

## Level 2 candidates

**Access control representations (ACM, ACL, capabilities)** — Covers the three canonical ways to encode a security policy and the operational tradeoffs between object-centric and subject-centric views. Worth a deeper treatment because the choice ripples through auditing, revocation, delegation, and how systems like OAuth, Kerberos, and Linux file permissions actually work under the hood.

**Linux/Unix permissions in practice** — Covers the owner/group/other model, octal vs symbolic chmod, ACL extensions via getfacl/setfacl, and the "everything is a file" philosophy that makes these permissions apply uniformly to devices and pipes. Worth going deeper because this is the access control system most practitioners will actually touch, and the corner cases (sticky bit, directory execute semantics, umask) are where mistakes happen.

**Controlled invocation and privilege escalation** — Covers setuid, setgid, sudo, and the broader pattern of letting unprivileged subjects briefly act with elevated authority. Worth a deep dive because this is where access control meets exploit development — every setuid binary is a potential privilege escalation vector, and understanding the attack surface is essential for both defenders and ethical hackers.

**DAC vs MAC vs RBAC** — Covers the three major policy models: discretionary (owner decides), mandatory (system decides based on labels), and role-based (permissions attach to roles, not users). Worth its own post because the choice of model is an organisational decision with deep consequences for compliance, scalability, and how human error propagates.

**Zero Trust Architecture** — Covers the shift from perimeter-based defence to continuous verification, including the always-verify / least-privilege / assume-breach pillars and how they translate into concrete controls like short-lived tokens, device posture checks, and identity-aware proxies. Worth deeper exploration because it is the dominant enterprise security paradigm of the next decade and connects access control to identity, networking, and cloud architecture.

**The principle of least privilege as a design discipline** — Covers least privilege not as a slogan but as a working method: how to scope service accounts, design permission boundaries, handle break-glass scenarios, and reason about blast radius. Worth its own treatment because it generalises beyond access control into a broader engineering posture that applies to API design, secret management, and incident response.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Access control exists because most real security failures are not dramatic hacks against exotic bugs. They are ordinary systems doing exactly what they were allowed to do for the wrong person, at the wrong time, or with too much authority. A forgotten account, an over-privileged service, a token that lives too long, a helper program that quietly runs as root — these are the conditions that turn routine mistakes into serious incidents.

If you do not have a clear model of access control, security work becomes vague very quickly. You can see that “something had too much access,” but you cannot say what kind of thing, access to what, under whose rules, or how to narrow it safely. That matters because engineering decisions about file permissions, service accounts, admin tools, tokens, and network trust all depend on the same underlying structure. If that structure is fuzzy, you end up patching symptoms instead of designing boundaries.

---

## What You Need To Know First

**1. Subjects, objects, and operations**  
In access control, you can reduce almost every question to: who is trying to do what to which thing? The “who” is the subject, which might be a human user, a process, or a service. The “what” is the operation, like read, write, execute, delete, or connect. The “which thing” is the object, such as a file, database row, API endpoint, or device. This framing matters because it turns security from a vague property into a specific request that can be checked.

**2. Authentication vs authorisation**  
Authentication answers “who are you?” Authorisation answers “now that I know who you are, what are you allowed to do?” People often blur these together, but the article is mainly about the second one. A system can authenticate someone perfectly and still be insecure if it authorises too much.

**3. Privilege**  
Privilege just means authority inside a system. Root has a lot of it. A normal user has less. A service account may have a very specific slice of it. The important thing is that privilege is not binary; it comes in scopes and levels. That is why the article keeps returning to the idea of narrowing what an account or program can do.

**4. Policy vs mechanism**  
A policy is the rule: “only these users may edit this file” or “this service may read but not write.” A mechanism is how the system enforces that rule: file permission bits, ACLs, tokens, roles, or a reference monitor. This distinction helps because many engineering arguments are really about mechanism choice, even when the real goal is to express a policy.

---

## The Key Ideas, Connected

**1. Every access-control decision can be seen as a subject trying to perform an operation on an object.**  
This is the core simplification that makes the rest manageable. Instead of treating security as an enormous cloud of settings and exceptions, you reduce each event to a basic request: some actor wants to do some action to some resource. That gives you a stable mental unit for reasoning. Once you have that unit, you can ask the next necessary question: who decides whether the request should succeed?

**2. A reference monitor is the conceptual guard that checks each request against policy.**  
The reference monitor is not mainly about one specific product or command. It is the idea that there must be some trusted point that stands between the subject and the object and says yes or no. If you miss this idea, permissions feel like labels attached to files; if you get it, you see a live decision process. That naturally leads to the next issue: if decisions are being made, how are the rules represented so the system can consult them?

**3. The access control matrix is the cleanest general model for representing those rules.**  
The matrix says: list subjects as rows, objects as columns, and permissions in the cells. It is useful because it shows the full policy in one abstract picture. But it is mostly a thinking tool, not a practical storage format, because real systems have too many subjects and objects, and most possible relationships are empty. That practical problem forces the next step: instead of storing the whole matrix, systems store a useful slice of it.

**4. ACLs and capabilities are two different ways of slicing the same underlying matrix.**  
An ACL is the object-centric slice: each object stores who can do what to it. A capability system is the subject-centric slice: each subject carries the permissions or tokens describing what it can do. This is an important connection, because ACLs and capabilities are not unrelated ideas; they are two views of the same policy space. Once you see that, the tradeoff becomes clearer: ACLs make it easy to inspect an object’s allowed users, while capabilities make it easy to inspect a subject’s allowed actions. That leads directly to why real operating systems often use simplified forms rather than full generality.

**5. Linux file permissions are a compressed, simplified access-control scheme built for speed and usability.**  
Linux does not keep a rich per-user policy for every file by default. It compresses the problem into three subject classes — owner, group, others — and three operations — read, write, execute. That is why `chmod 750` works: it is a compact encoding of a policy, not magic syntax. The reason this matters is that you can now see both the strength and the limitation of the model. It is simple and fast, but it cannot express every policy you might want. That is why richer ACLs exist as an extension rather than the default.

**6. Simpler permission systems leave awkward cases where legitimate work still requires higher privilege.**  
Sooner or later, a normal user needs to trigger an action that touches a protected resource. Changing your password is the classic example: you should be allowed to change your own password, but you should not get broad write access to sensitive system files. This tension creates the need for controlled elevation rather than blanket privilege. And that leads to one of the most important and dangerous mechanisms in Unix-like systems.

**7. Setuid is a way to borrow the owner’s privilege for a narrow, controlled action.**  
A setuid program runs with the privilege of its owner, often root, instead of the user who launched it. The intended purpose is narrow delegation: let an unprivileged user perform one carefully designed administrative task without becoming an administrator generally. This is powerful because it solves a real systems problem cleanly. But it also creates a dangerous fact: if the privileged program is flawed, the attacker may inherit far more than intended. That is why understanding controlled invocation naturally pushes you toward the broader design principle behind safer systems.

**8. Least privilege is the discipline of giving each subject only the authority it actually needs.**  
Least privilege is not moral advice; it is damage control. If a program, user, or token is compromised, the scope of the incident is limited by the permissions already attached to it. This idea unifies everything that came before: file permissions, setuid minimisation, scoped tokens, service accounts, and role design are all attempts to reduce unnecessary authority. Once you see access control this way, the next modern shift makes sense: systems stopped assuming that being “inside” a network was enough to deserve broad trust.

**9. Zero trust applies access-control thinking continuously instead of once at the perimeter.**  
The old perimeter model assumed that passing the outer boundary meant you were trustworthy enough. Zero trust treats that assumption as unsafe. Identity, device state, session age, and context matter every time, not just at login or network entry. This is not a replacement for access control; it is access control made more explicit and less naive. It takes the same core ideas — verify the subject, evaluate the requested operation, minimise privilege, assume compromise is possible — and applies them everywhere, continuously.

**10. The real takeaway is a way of diagnosing and designing systems, not a list of security commands.**  
When something goes wrong, you can ask: which subject performed which operation on which object, and why was that allowed? When you build something, you can ask: what is the minimum authority this component needs, and what can happen if it is compromised? That is the full chain of the article: from single access requests, to decision points, to policy representation, to practical permission systems, to controlled elevation, to least privilege, to modern trust models.

---

## Handles and Anchors

**1. Think of access control as a customs checkpoint, not a wall.**  
A wall only tries to keep outsiders out. A checkpoint examines each crossing: who are you, what are you carrying, where are you going, and are you allowed through? That is closer to how real access control works. The important action is in the decision at the crossing, not in the mere existence of a boundary.

**2. ACLs answer “who can touch this thing?” while capabilities answer “what can this actor touch?”**  
That one sentence is a strong mental handle because it lets you orient yourself quickly whenever you see a permissions system. If the system stores rules near the resource, think object-first. If it hands around tokens or scopes, think subject-first.

**3. Least privilege is blast-radius engineering.**  
That phrase captures the point cleanly. You are not trying to predict every failure. You are trying to make sure that when failure happens, the damaged component cannot take everything else down with it.

---

## What This Changes When You Build

**An engineer who understands this will design service accounts differently because they will ask for the minimum operations on the minimum resources, not “whatever makes the app work.”**  
That changes how you provision database credentials, cloud IAM roles, CI tokens, and background jobs. Instead of one broad account shared across components, you create narrower identities tied to actual tasks.

**An engineer who understands this will debug permission failures faster because they will frame the problem as subject, operation, object, and policy decision.**  
Instead of staring at a generic “permission denied” and guessing, they will ask: which process or user made the request, what exact action was attempted, what resource was targeted, and which rule blocked it? That tends to reveal whether the issue is ownership, group membership, missing execute permission on a directory, token scope, or a higher-level policy mismatch.

**An engineer who understands this will treat privileged helper programs with far more caution because controlled invocation is a legitimate design pattern and a privilege-escalation surface at the same time.**  
That changes code review and operational posture. A small root-owned utility, a `sudo` rule, or a setuid binary is no longer “just a convenience”; it becomes a narrowly bounded trust transfer that must be audited like an attack surface.

**An engineer who understands this will make different choices about token lifetime and session design because access is not a one-time gate.**  
They will prefer short-lived credentials, scoped tokens, and revalidation for sensitive operations. The reason is that stolen credentials are much less useful when they expire quickly and carry limited authority.

**An engineer who understands this will structure systems to fail smaller because they will assume compromise and design around containment.**  
That affects container users, filesystem mounts, network segmentation, secret distribution, and writable paths. If a web process only needs read access to configuration and write access to one upload directory, then giving it broader filesystem rights is no longer a harmless default — it is an unnecessary expansion of blast radius.

</details>
