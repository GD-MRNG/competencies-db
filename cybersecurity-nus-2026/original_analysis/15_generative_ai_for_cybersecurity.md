## Metadata
- **Date:** 18-05-2026
- **Source:** 15_generative_ai_for_cybersecurity.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Generative AI for Cybersecurity

The interesting thing about generative AI in security is not that it gives attackers new capabilities. It is that it collapses the time and skill required to use capabilities that already existed. A convincing phishing email, a working exploit for a known CVE, a piece of malware that mutates between scans — none of these are new. What is new is that producing them no longer requires a competent human attacker. And once you accept that, the whole shape of the defender's job changes.

The first move is to stop thinking only in terms of the CIA triad — confidentiality, integrity, availability — and start holding its inverse in your head at the same time. Attackers operate on the DAD triad: disclosure, alteration, denial. CIA is what you want to preserve; DAD is what your adversary is trying to achieve. Every control you design should be evaluated from both sides. This is not a rhetorical flourish. When you only think in CIA terms you tend to build defences around what you imagine the system should do. When you think in DAD terms you start asking how someone with no respect for your assumptions would pull the system apart. In a world where attackers can prototype attacks against your model with an LLM in an afternoon, the defender who only thinks in CIA is already behind.

The threat surface itself has changed in two directions. Malware has been getting harder to detect for years through polymorphism (code that mutates while preserving behaviour) and metamorphism (code that rewrites its entire character between generations), and signature-based scanning was already a losing game. Generative AI makes this worse, but it also democratises the lower tiers of the attack market — the script kiddie now has a research assistant, the mid-tier criminal now has a tireless social engineer, and the well-funded actor now has a force multiplier. The volume of attempts at every skill level goes up. Hyper-realistic phishing, deepfake-driven social engineering, and automated exploit generation are no longer exotic; they are the new baseline. On top of this, LLMs introduce their own attack surface — jailbreaking, where prompts manipulate a model into generating malicious code or leaking instructions it was meant to refuse, is now a category of vulnerability in its own right.

To make sense of all this, you need a stack of frameworks that fit together rather than a single one. CVE is the catalogue of specific known vulnerabilities — the records. CWE is the taxonomy of underlying weakness types — the root causes. CVSS gives you a severity score so you can triage. These feed into the MITRE ATT&CK matrix, which maps the tactics, techniques, and procedures attackers actually use across the full lifecycle of an intrusion. ATT&CK is where you stop talking about vulnerabilities in the abstract and start talking about how an adversary moves through your environment. MITRE ATLAS is the parallel matrix for attacks against AI systems themselves, which you will increasingly need as you deploy AI in your stack. The older Cyber Kill Chain still has documentary value, but it is too linear to capture how modern intrusions actually unfold. Treat ATT&CK as the working map.

On the defensive side, generative AI is genuinely useful, and the use cases are not speculative. The highest-leverage applications are the boring ones: summarising massive volumes of low-signal logs to surface indicators of compromise, translating a fresh threat intelligence report into working Snort or YARA rules in minutes rather than days, and generating synthetic datasets for rare attack patterns where you do not have enough real data to train a detector. Beyond this sit the security copilots — Crowdstrike's Charlotte AI, Palo Alto's Cortex XSIAM, GitHub Copilot in adjacent territory — which take on the repetitive analyst workload and let humans focus on judgement calls. Further out are autonomous agents that can run continuous red-team exercises against your own infrastructure, providing a feedback loop the blue team could never sustain manually.

The catch is that handing security work to LLMs introduces a problem that does not have a clean solution. Call it the Schrödinger's cat problem: an autonomous agent patching a vulnerability might introduce a new one in the process, and you may not know until something exploits it. Compounding this is the explainability gap — when a deep learning model flags something as malicious, "because the model said so" is not an answer that holds up in an incident review, a regulator's office, or a court. Guardrails on LLM inputs and outputs are necessary but not sufficient. Human oversight is non-negotiable, but human oversight also does not scale, which is precisely the problem AI was meant to solve. There is no resolution to this tension yet; there is only the discipline of designing systems that fail visibly rather than silently.

What this all adds up to is a shift in what a cybersecurity professional actually does. The job used to be heavily weighted toward execution — running scans, writing rules, triaging alerts, investigating incidents by hand. That work is increasingly done by AI systems, faster and at higher volume than any human can match. The role that survives, and the one worth building toward, is the governor: the person who decides what the AI is allowed to do, validates what it has done, designs the guardrails it operates within, and takes responsibility when it gets something wrong. The technical depth still matters — you cannot govern systems you do not understand — but the leverage is in oversight, policy, and judgement. The regulatory frame for this work is already forming around the EU AI Act and the NIST AI Risk Management Framework, and anyone serious about security leadership needs to be reading both.

The skill this topic builds, then, is not a tool or a technique. It is a stance. You learn to hold offence and defence in the same field of view, to map any threat through the CVE-CWE-CVSS-ATT&CK chain almost reflexively, and to evaluate every proposed AI defence against the question of what happens when it is wrong. The arms race is not optional and it is not slowing down. The defenders who matter in five years will be the ones who learned to govern AI rather than compete with it.

## Level 2 candidates

**The DAD triad as an evaluation lens** — Covers how to systematically apply disclosure, alteration, and denial as adversarial counterparts to CIA when reviewing a system or control. Worth deeper treatment because it is a transferable analytic habit, not just a definition, and the move from knowing the triad to using it well is non-trivial.

**The CVE / CWE / CVSS / ATT&CK stack** — Covers how the four frameworks fit together, what each one is actually for, and how to traverse them when responding to a real vulnerability. Worth a deep dive because most practitioners use these in isolation and miss the leverage that comes from treating them as one integrated workflow, including the role of NVD and EPSS in prioritisation.

**MITRE ATLAS and securing AI systems themselves** — Covers the adversarial threat landscape specific to machine learning models, including model evasion, data poisoning, and prompt-level attacks. Worth going deeper as ATLAS is still unfamiliar to most security teams and will become essential as AI components proliferate inside production stacks.

**LLM jailbreaking and guardrail design** — Covers the techniques used to bypass model safety instructions and the input/output filtering patterns that defend against them. Worth a deep dive because this is a fast-moving subfield with real engineering content — system prompts, output classifiers, adversarial testing — that a Level 1 framing can only gesture at.

**Polymorphic and metamorphic malware** — Covers how modern malware mutates to evade signature-based detection and what behavioural and ML-based detection approaches actually look like in response. Worth deeper coverage because the cat-and-mouse dynamic has specific technical content that rewards a closer look, particularly around how generative models change the economics of producing variants.

**GenAI-driven SOC operations and copilots** — Covers the concrete defensive workflows — log summarisation, automated rule generation, synthetic data, copilot-assisted triage — and the tooling that supports them. Worth going deeper because the gap between "we should use AI in the SOC" and a working integration is substantial, and the design choices around human-in-the-loop matter enormously.

**The governance, ethics, and liability gap** — Covers the EU AI Act, NIST AI RMF, the explainability problem, and the open question of who is responsible when an autonomous defender causes harm. Worth a deeper treatment because this is where security leadership careers will be made or broken over the next several years, and the regulatory landscape is concrete enough now to study seriously.

---

# Discussion

## Why This Conversation Is Happening

For a long time, cybersecurity had a useful friction built into it: many attacks were possible in theory, but expensive in skill, time, or coordination. That friction protected defenders more than people liked to admit. Generative AI reduces that friction. It does not magically invent new categories of attack so much as make existing ones cheaper, faster, and available to less capable attackers. When that happens, the defender is no longer dealing with a few skilled adversaries; they are dealing with many more attempts, produced at higher speed, with less warning.

That changes what breaks in practice. Phishing gets more convincing at scale. Malware variants multiply faster than signature rules can keep up. Vulnerabilities that were once "known but not yet operationalised" get turned into working attack paths much more quickly. And when defenders add AI into their own stack, they inherit a second problem: the defence system itself becomes something that can be manipulated, misled, or trusted too far. If you do not have a clean mental model here, you will make two common mistakes: underestimating how AI changes attacker economics, and overestimating how safely AI can be dropped into defensive workflows.

---

## What You Need To Know First

**1. The CIA triad**  
CIA stands for confidentiality, integrity, and availability. It is the classic way defenders describe what security is supposed to preserve: keep data secret from the wrong people, keep systems and data correct, and keep services usable. You do not need more than that here; just hold onto the idea that CIA describes the system from the defender's point of view.

**2. Vulnerability vs weakness vs attack technique**  
These terms are easy to blur together. A **vulnerability** is a specific flaw in a specific product or system. A **weakness** is the underlying class of mistake that made that flaw possible, like bad input validation. An **attack technique** is how an attacker actually behaves to exploit weaknesses and move through an environment. This distinction matters because the article is arguing that good security work connects all three, rather than treating each as a separate world.

**3. Signature-based detection**  
A signature is a known pattern used to spot known malicious software or behaviour. It works well when attackers reuse the same code or indicators. It works poorly when malware keeps changing its appearance while keeping the same purpose. You only need that much to follow why AI-amplified mutation creates pressure on older defensive methods.

**4. Human-in-the-loop**  
This means an automated system can assist or act, but a human still reviews, approves, or oversees important decisions. In this article, that idea matters because AI can increase defensive speed, but the cost of letting it act alone is that it may make harmful changes or produce conclusions nobody can properly justify afterward.

---

## The Key Ideas, Connected

**1. Generative AI changes cybersecurity mainly by compressing the cost of attack work.**  
The central claim is not "AI creates science-fiction attacks." It is "AI makes existing attacks easier to produce." A good phishing email, exploit adaptation, malware variation, and social-engineering prep all existed before. What changes is who can do them, how fast, and how often. That matters because defence is shaped not just by what is possible, but by how cheaply attackers can repeat it. Once attack capability becomes cheaper, you need a more adversarial way of thinking about systems, which leads to the next idea.

**2. Defenders need to think in both CIA and DAD at the same time.**  
CIA says what you want to protect: confidentiality, integrity, availability. DAD — disclosure, alteration, denial — says what the attacker is trying to cause. That shift sounds small, but it changes how you inspect a system. Instead of asking only "how do we preserve intended behaviour?", you also ask "how would someone force disclosure, alter outcomes, or deny service if they did not care about our design assumptions?" The point is to evaluate controls from both sides of the contest. Once you start doing that, you can see more clearly why the threat surface is expanding, not just intensifying.

**3. The threat surface is expanding in two directions: more AI-enabled attacks, and new attacks against AI systems.**  
On one side, AI amplifies familiar attacker activity: phishing becomes more scalable, exploit generation faster, and malware variation easier to produce. On the other side, the AI systems themselves become targets. If you deploy LLMs or other models, attackers can try to jailbreak them, manipulate their inputs, or get them to produce unsafe outputs. So AI is not just an accelerant poured onto the old security problem; it also adds a new layer of systems that require defence. Once the problem gets that broad, one security framework is no longer enough, which leads to the need for a stack.

**4. Security teams need a connected stack of frameworks, not isolated labels.**  
The article names CVE, CWE, CVSS, ATT&CK, and ATLAS because each answers a different question. CVE tells you **what specific flaw** is known. CWE tells you **what kind of engineering mistake** sits underneath it. CVSS tells you **how severe** it appears for triage. ATT&CK tells you **how an attacker would actually use techniques** across an intrusion. ATLAS extends that idea to attacks on AI systems. The important move is to stop treating these as vocabulary words and start treating them as a path of reasoning: from concrete flaw, to root cause, to prioritisation, to adversary behaviour. Once you have that map, defensive AI becomes easier to place in real workflows rather than as a vague promise.

**5. The strongest defensive uses of generative AI are practical workflow accelerators.**  
The article is deliberately unsentimental here. The highest-value uses are not magical autonomous defenders; they are tasks that consume analyst time and benefit from speed: summarising noisy logs, converting threat intel into detection rules, generating synthetic data where real attack samples are scarce, and helping analysts triage repetitive work. This is important because it grounds AI's value in operational bottlenecks, not hype. But the moment AI starts acting inside defensive workflows, a new problem appears: the system helping you can also make mistakes that create risk.

**6. AI-assisted defence creates an unresolved trust problem.**  
If an AI system patches, blocks, rewrites, or escalates, it can be wrong in ways that are hard to inspect. It might close one hole and open another. It might flag something malicious without a reason a human can defend. That is the article's deeper tension: AI is attractive precisely because humans do not scale, but handing more control to AI introduces actions whose safety and explainability are uncertain. There is no neat solution offered here. Instead, the operating principle is to design systems whose failures are visible, reviewable, and interruptible. That unresolved tension then changes the human role in security itself.

**7. The security professional's role is shifting from primary operator to governor.**  
If AI takes more of the scanning, summarising, drafting, and first-pass investigation work, the lasting human leverage moves upward. The valuable person is not just the one who can execute tasks manually, but the one who decides what the AI may do, what evidence is required before action, where guardrails sit, when escalation is mandatory, and who owns the consequences of failure. "Governor" is a useful word because it implies oversight with technical understanding. You still need the depth to judge the system; you just apply that depth through policy, validation, and control design more than through raw manual throughput. That is why the article ends by calling this a stance rather than a tool.

**8. The lasting skill is learning to reason about AI security as an adversarial control problem.**  
The article's endpoint is that you should hold offence and defence together, move fluidly through the vulnerability-to-technique stack, and judge AI systems by what happens when they are wrong. That is more durable than any one tool. Tools will change. Vendors will change. But the engineer who can ask "what attacker capability got cheaper?", "what failure mode did this automation introduce?", and "how do we keep wrong actions observable and governable?" will keep making good decisions as the landscape shifts.

---

## Handles and Anchors

**1. Generative AI is not a new weapon so much as a power tool.**  
A power tool does not invent carpentry; it lets more people cut faster, with less effort. That is the right mental model here. AI does not have to invent unprecedented attacks to matter. It only has to let attackers do familiar things at much higher speed and volume.

**2. CIA is the building owner's view; DAD is the burglar's view.**  
The owner thinks: keep the valuables private, keep the structure intact, keep the doors working. The burglar thinks: expose what should be hidden, change what matters, stop normal use. Looking through both views at once is what turns security from checklist thinking into adversarial reasoning.

**3. AI in security is a very fast junior operator with uncertain judgement.**  
It can read more, draft more, and respond more quickly than a person. But it may also make a confident mistake, and its reasoning may be hard to defend afterward. That single image captures why AI is useful and why guardrails and oversight remain central.

---

## What This Changes When You Build

**An engineer who understands this will evaluate controls from the attacker's objective, not just the system's intended behaviour, because preserving CIA is only half the story.**  
In practice, that changes design reviews and threat modelling. Instead of stopping at "does this control protect data?", they will also ask "how could this be used to force disclosure, alteration, or denial?" That produces different questions around logging, privilege boundaries, prompt handling, fallback paths, and abuse cases.

**An engineer who understands this will prioritise detection approaches differently because high-variance AI-assisted attacks erode the value of static signatures alone.**  
They will still use signatures where appropriate, but they will put more weight on behavioural detection, anomaly correlation, layered telemetry, and rapid rule iteration. The reason is simple: if attackers can generate endless superficial variants, appearance becomes a weaker signal than behaviour and sequence.

**An engineer who understands this will connect CVE, CWE, CVSS, and ATT&CK during incident response because a flaw is not the same thing as its exploit path or business priority.**  
That changes how they triage a new issue. They will ask: what is the exact vulnerability, what weakness produced it, how urgent is it, and what techniques would an adversary use to operationalise it in our environment? That leads to better patch order, better compensating controls, and fewer cases where teams fix the headline issue but miss the realistic attack chain.

**An engineer who understands this will introduce AI into SOC workflows first at low-risk, high-volume bottlenecks because the main value is throughput, while the main danger is unreviewed action.**  
So they are more likely to start with log summarisation, draft rule creation, analyst assistance, and evidence condensation than with fully autonomous remediation. The reason is that these uses capture speed gains while containing the blast radius of model mistakes.

**An engineer who understands this will design AI-enabled security systems to fail visibly because hidden failure is more dangerous than slow failure.**  
That means approval gates for sensitive actions, audit trails for model outputs, replayable evidence, rollback paths for automated changes, and clear escalation triggers when confidence is low or consequences are high. They build for inspection, not just automation, because the core question is not whether the model can act, but what happens when it acts wrongly.

**An engineer who understands this will treat security leadership as a governance problem as much as a technical one because somebody must define the operating boundary for AI systems.**  
That changes day-to-day work around policy, access control, model permissions, documentation, accountability, and regulatory readiness. The engineer is no longer just choosing tools; they are deciding which decisions may be delegated, under what evidence standard, with what human override, and with whose responsibility attached.