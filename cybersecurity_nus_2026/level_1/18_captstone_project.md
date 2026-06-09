## Metadata
- **Date:** 18-05-2026
- **Source:** 18_captstone_project.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# The Capstone: Thinking Like a Defender Who Has Done the Attack

The capstone is the moment the programme stops teaching you cybersecurity in pieces and asks whether you can hold the whole thing in your head at once. On the surface it looks like a lab exercise — stand up a Windows Server 2022 Domain Controller, point a Kali box at it, run some enumeration tools, write it up. That framing is misleading. The lab is the easy part. The hard part is that the assignment is simultaneously testing five different professional postures, and the grade reflects how well you can move between them in a single document.

Read the rubric carefully and a structure emerges. Ten points for building the lab. Fifteen for running the tools. Fifteen for using AI well, ten more for critiquing what AI gave you. Fifteen for documenting what you found, ten for proposing fixes, ten for tying findings back to confidentiality, integrity, and availability and translating them into cloud equivalents. Five for an executive summary, ten for overall structure. Notice what dominates: only twenty-five points reward technical execution. The other seventy-five reward judgment — about AI, about defence, about communication, about how a finding in an on-prem AD lab maps to an Azure AD tenant. The capstone is a writing assignment with a lab attached, not a lab assignment with a report attached.

The mental model that makes this manageable is a five-step loop: build the system, break the system, analyse the system, improve the system, reflect ethically. Each step produces artefacts the next step consumes. The build phase produces a domain you actually understand the topology of, which is what makes the enumeration outputs interpretable rather than mysterious. The enumeration phase produces logs and screenshots, which is what makes the AI analysis meaningful — you can only critique ChatGPT's interpretation if you have the raw output to compare against. The vulnerability documentation produces a finding list, which is what the mitigation section answers and what the CIA reflection generalises from. Skip a step or do it carelessly and the downstream sections lose their grip; the report starts to read like assertions rather than analysis.

The technical spine is straightforward and worth internalising as a sequence rather than a checklist. You build an isolated two-VM lab — host-only networking, never bridged — install AD DS on the Windows server, promote it to a domain controller, create a forest like mydomain.local, add a test user, and confirm SMB and DNS are running. From Kali you then work outward through the protocols a domain controller exposes: Nmap for OS and service discovery on port 445, enum4linux for authenticated SMB enumeration that pulls domain SIDs and password policy, Metasploit modules for SMB shares and GPP credentials in SYSVOL and Kerberos username validation, ADExplorer for LDAP browsing, PSTools for process and session data. Each tool is asking a slightly different question of the same machine, and the point of using several is triangulation — you want findings that show up consistently across tools, and you want to notice when they don't.

AI is the axis where most of the marks live and most of the mistakes happen. The assignment wants you to use ChatGPT to generate commands, interpret output, and suggest attack paths — and then it wants you to push back. This is not theatre. AI tools genuinely hallucinate CVEs, overstate severity on benign findings, miss context that a human reading the same scan would catch, and occasionally suggest commands that overreach the scope of the engagement. The thirty points across "integration of AI" and "critical evaluation of AI" are really one combined grade for AI literacy: can you use the tool to move faster and can you tell when it is wrong? The way to earn those points is to document the prompt, paste the response, and then write a sentence or two on what you accepted, what you corrected, and why. Vague reflection ("AI was helpful but had limitations") earns nothing. Specific correction ("ChatGPT flagged MS08-067 based on the SMB banner, but this is a 2022 server and the CVE applies to pre-Vista systems — false positive") earns full marks.

The CIA and cloud reflection is where the report stops being a lab writeup and becomes evidence that you understand the discipline. Every finding has to be translated twice: once into the CIA triad (an exposed SMB share is a confidentiality issue; weak Kerberos pre-auth threatens integrity of authentication; misconfigured replication threatens availability), and once into the cloud (group policy becomes Azure AD Conditional Access; admin group membership becomes RBAC; standing admin rights become Privileged Identity Management). This is the part of the assignment that connects the on-prem lab to the world the reader will actually work in, where most identity infrastructure is hybrid or fully cloud. Skip this section and you cap your grade somewhere in the seventies regardless of how clean the lab was.

The executive summary at the end is worth only five points but it is the part a reader notices first, and it is the easiest place to give away the impression that you understand your own work. Write it for a CEO who does not know what LDAP is. State what you found, why it matters in business terms, what it would cost to fix, and what the risk is if it isn't fixed. No tool names, no command output, no acronyms you haven't expanded. If your executive summary still reads like the technical body, you are not yet thinking like the defender the capstone is trying to produce — you are still the analyst who ran the tools.

The capstone, in the end, is asking a single question across nine rubric criteria: can you attack ethically, defend intelligently, govern responsibly, use AI critically, and communicate professionally, in one document, about one machine? That is the job. The lab is just the pretext.

## Level 2 candidates

**Active Directory enumeration as an attack surface** — Covers what each protocol on a domain controller (SMB, LDAP, Kerberos, DNS) actually leaks under default and misconfigured states, and why AD is the highest-value target in most enterprise networks. Worth depth because the specific exposures — anonymous SMB shares, GPP cpassword in SYSVOL, Kerberos username validation, LDAP anonymous binds — each have distinct mechanics and mitigations that don't compress well into a Level 1 overview.

**Critical use of AI in security workflows** — Covers prompt design for security tasks, validation patterns for AI output, common hallucination modes (fabricated CVEs, miscontextualised advice, overreach in suggested commands), and the discipline of documenting human-in-the-loop decisions. Worth its own treatment because AI literacy in security is a distinct skill from either using AI or doing security, and the failure modes are specific enough to deserve concrete examples.

**Translating on-prem controls to cloud equivalents** — Covers the mapping between AD/GPO/file-share thinking and Azure AD/RBAC/PIM/Conditional Access thinking, including where the analogies break down. Worth depth because most working professionals operate in hybrid environments where misapplied on-prem mental models create real gaps, and the mapping is non-obvious in several places.

**Writing security findings for mixed audiences** — Covers the structural difference between a technical vulnerability writeup, a mitigation recommendation, and an executive summary, and how to produce all three from the same underlying finding without redundancy. Worth depth because this is the skill that separates analysts from leads, and it is taught almost nowhere despite being graded everywhere.

**The CIA triad as an analytical lens, not a definition** — Covers how to actively use confidentiality, integrity, and availability to classify findings, prioritise mitigations, and reason about trade-offs, rather than treating CIA as a definition to recite. Worth depth because Level 1 treatments of CIA almost always stop at the definition, and the analytical use is what makes it valuable in real assessments.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

A lot of security education is modular: one week you learn networking, another week you learn scanning, another week you learn report writing. That creates a dangerous illusion that security work happens in pieces. In practice, it does not. Real security work is nearly always a handoff problem: a technical action produces evidence, evidence needs interpretation, interpretation needs judgment, and judgment has to survive contact with both defenders and non-technical decision-makers. The capstone exists because that integration step is where many otherwise capable learners fall apart.

If you do not have a grip on this, the failure mode is not usually “you cannot run the tool.” It is “you can run the tool, but you cannot turn output into a defensible finding, cannot tell when AI is helping versus inventing, and cannot explain why any of it matters.” That is exactly the difference between performing isolated security tasks and operating like someone a team could trust with an assessment.

## What You Need To Know First

**1. Active Directory is not just a server; it is an identity system.**  
A domain controller is valuable because it answers identity questions for the rest of the environment: who are you, what groups are you in, what are you allowed to access, what policies apply to you. That means when you enumerate a domain controller, you are not just checking one machine for weaknesses; you are probing the control system that other machines trust.

**2. Enumeration is information gathering, not exploitation.**  
Enumeration means asking a system what it is willing to reveal: open ports, usernames, shares, policies, directory objects, service details. The key idea is that useful security findings often come from what a system discloses before you ever “hack” anything. If a domain leaks usernames, password policy, shares, or directory structure, that information becomes the raw material for later attack paths and for defensive remediation.

**3. The CIA triad is a way to classify impact.**  
Confidentiality is about who can see data, integrity is about who can change or impersonate trusted things, and availability is about whether systems remain usable. For this article, you do not need a textbook definition. You only need to be able to ask, for any finding: does this expose information, enable unauthorised change, or threaten service access?

**4. A rubric tells you what kind of performance is actually being tested.**  
Students often read rubrics as point distributions; experienced engineers read them as signals about what the evaluator believes the work is. If most marks are on analysis, critique, mitigation, and communication, then the assignment is not mainly testing tool operation. It is testing whether you can turn technical activity into professional judgment.

## The Key Ideas, Connected

**The capstone is testing whether you can think across the whole security workflow, not just complete a lab.**  
The article’s first important move is to reframe the assignment. On the surface, it looks like “build a domain controller and enumerate it.” But the article argues that this framing is too narrow. The real test is whether you can build, inspect, interpret, criticise, recommend, and communicate as one continuous process. That matters because once you see the assignment that way, the rubric stops looking random and starts looking coherent.

**The rubric reveals that judgment is weighted more heavily than technical execution.**  
Only a minority of the marks come from standing up the lab and running the tools. Most of the marks come from how well you use AI, critique AI, document findings, propose fixes, map to CIA and cloud controls, and communicate clearly. That tells you something fundamental: the assignment is closer to a professional assessment report than a pure technical exercise. This leads directly to the next idea, which is that you need a process that connects those non-technical deliverables back to the technical work.

**The assignment becomes manageable when you treat it as a loop of dependent stages.**  
The five-step loop in the article — build, break, analyse, improve, reflect ethically — is really a dependency map. Each stage creates the evidence needed for the next one. If you build the lab carefully, you understand what you are looking at during enumeration. If you enumerate carefully, you have outputs that can be checked against AI interpretations. If you analyse carefully, you can write findings that support concrete mitigations. If you propose mitigations clearly, you can then discuss impact through CIA and cloud equivalents. The reason this matters is that weak work early on does not stay local; it degrades every later section.

**The technical work matters most as a source of interpretable evidence.**  
The article deliberately lowers the drama around the tooling. Nmap, enum4linux, Metasploit modules, ADExplorer, and PSTools are presented less as heroic hacker instruments and more as different ways of asking the domain controller what it exposes. That is a useful mental shift. The point of multiple tools is triangulation: one tool may suggest something, but confidence grows when several independent views line up. Once you see the technical spine this way, you can understand why the next stage — AI use — is not about outsourcing thought.

**AI is being assessed as a force multiplier that still requires human verification.**  
The article treats AI use and AI critique as one combined competency: can you accelerate your work with the tool, and can you catch it when it is wrong? This is a very security-specific form of literacy. A model might generate a plausible command, misread a banner, hallucinate a CVE, or recommend something outside scope. The assignment rewards you not for saying “I used AI,” but for showing a traceable decision process: here is the prompt, here is the response, here is what I accepted, here is what I rejected, and here is why. That naturally leads to the next layer, because once you have trustworthy findings, you still need to express why they matter.

**A finding is incomplete until you translate it into impact and into the environment people actually operate.**  
This is why the CIA and cloud-mapping section matters so much. A raw observation like “SMB share exposed” is not yet a professional result. It becomes one when you can say what kind of harm it enables and how the same control problem appears in a hybrid or cloud setting. The article’s deeper point is that security understanding is not tied to one platform. If you really understand the issue, you can map it from on-prem AD concepts to Azure AD, RBAC, Conditional Access, or PIM without losing the underlying logic.

**The final proof of understanding is whether you can change register for different audiences.**  
The executive summary is the sharpest test of this. It asks whether you can leave tool-centric language behind and explain the same work in business terms: what was found, why it matters, what should be done, and what happens if nothing changes. This is not separate from the technical work; it is the final expression of it. The chain ends here because the whole article is building to one conclusion: the capstone is really asking whether you can act like a defender who understands attack mechanics, not merely like a student who completed security tasks.

## Handles and Anchors

**1. Think of the capstone as a supply chain of evidence.**  
The lab setup manufactures the environment. Enumeration produces raw materials. Analysis refines them into findings. Mitigation turns findings into action. The executive summary packages the result for decision-makers. If one stage is weak, the whole chain downstream degrades.

**2. The tools are not the product; the judgment is the product.**  
A scan result, screenshot, or AI response is intermediate output. The thing being graded — and the thing that matters in real work — is whether you can decide what is true, what matters, and what should happen next.

**3. “Can you attack ethically, defend intelligently, and explain clearly — all from the same evidence?”**  
That sentence captures the core tension of the assignment. You are being asked to inhabit offensive and defensive viewpoints at once, while also proving you can communicate across technical and non-technical audiences.

## What This Changes When You Build

**An engineer who understands this will build the lab more deliberately because later interpretation depends on knowing exactly what was configured.**  
They will record topology, host-only isolation, domain name, users created, services enabled, and any deviations from defaults. Without that, later enumeration output becomes ambiguous, and they cannot confidently separate expected exposure from misconfiguration.

**An engineer who understands this will treat enumeration as hypothesis gathering rather than screenshot collection because the goal is corroborated findings, not tool coverage.**  
Instead of running every tool once and pasting results, they will compare outputs across protocols and tools: does the SMB view match LDAP objects, do Kerberos observations fit known users, do shares exposed by one tool appear in another? This reduces shallow reporting and improves confidence in findings.

**An engineer who understands this will use AI with an audit trail because the marks — and the real risk — sit in validation, not convenience.**  
They will preserve prompts, responses, and raw command output, then explicitly note where AI helped, where it overreached, and how they corrected it. That changes the report from “AI-assisted” in name only to a documented human-in-the-loop workflow.

**An engineer who understands this will write findings in a three-layer form because each later section needs a different view of the same issue.**  
They will describe the technical observation, explain the security impact, and attach a mitigation that answers that specific risk. That makes it much easier to later map the same finding to CIA categories and to cloud equivalents without inventing new reasoning at the end.

**An engineer who understands this will draft the executive summary as a translation exercise, not a shortened technical section, because decision-makers do not act on protocol names; they act on business risk and remediation cost.**  
So they will remove tool names, expand acronyms, focus on consequences, and state what should be fixed first. That produces a report that could plausibly be read by both a technical reviewer and a manager, which is exactly the professional posture the capstone is trying to develop.

</details>
