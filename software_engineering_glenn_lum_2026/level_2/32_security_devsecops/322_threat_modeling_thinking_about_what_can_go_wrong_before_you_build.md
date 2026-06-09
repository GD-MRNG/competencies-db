## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers encounter threat modeling as a meeting they get pulled into or a document template they're asked to fill out. They list some threats — SQL injection, DDoS, credential theft — assign some severity labels, and move on. The document gets filed. Nothing about the system's design actually changes.

This is not threat modeling. This is security Mad Libs.

Real threat modeling is a structured decomposition of your system that produces specific design decisions. It works not because it makes you think about security in general, but because it forces you to trace how data actually moves through your architecture, identify the exact boundaries where trust assumptions change, and systematically ask what can go wrong at each one. The output is not a list of fears — it is a set of architectural constraints that shape what you build. The Level 1 post covered why shifting security left matters and what kinds of tools operate at different stages. This post is about the mechanics of the thinking process itself: how you decompose a system for security analysis, how STRIDE actually works as a reasoning tool, and how identified threats become design requirements.

## The Foundation: Data Flow Diagrams and Trust Boundaries

Threat modeling does not start with thinking about attackers. It starts with understanding your own system. The primary artifact is a **data flow diagram (DFD)** — a deliberately simplified representation of your system as four types of elements: external entities (things outside your control — users, third-party APIs, external services), processes (your running code — services, functions, workers), data stores (databases, caches, file systems, message queues), and data flows (the arrows connecting them, representing data moving between components).

This is not a UML diagram and it is not an architecture diagram. A DFD is optimized for one purpose: making visible where data goes and what it crosses along the way.

The critical concept that gives a DFD its security value is the **trust boundary**. A trust boundary exists wherever data crosses between components that run at different privilege levels, are controlled by different entities, or operate in different security contexts. Between a user's browser and your API: trust boundary. Between your application code and your database: trust boundary. Between your Kubernetes pod and the host node: trust boundary. Between your internal service and a third-party payment provider's API: trust boundary.

Trust boundaries are where threats concentrate, because they are the points where assumptions change. Data arriving from a user's browser cannot be assumed to be well-formed or honest. Data leaving your network to a third-party API is leaving your confidentiality perimeter. Every trust boundary crossing is a site where the receiving component must decide what it can and cannot assume about what it just received.

### A Concrete Decomposition

Consider a standard e-commerce payment flow. The DFD looks like this, read top to bottom:

The user's browser (external entity) sends a checkout request across a trust boundary to the API Gateway (process). The API Gateway terminates TLS, validates the authentication token, and forwards the authenticated request across an internal trust boundary to the Order Service (process). The Order Service retrieves pricing data from the Product Catalog database (data store) across a trust boundary, constructs a payment request, and sends it across a trust boundary to the Payment Provider's API (external entity). The Payment Provider responds with a transaction result. The Order Service writes the completed order to the Orders Database (data store) across a final trust boundary.

Each arrow that crosses a dashed trust boundary line is a point where you will apply STRIDE. This is not incidental — it is the entire mechanism. Without the DFD, threat identification devolves into brainstorming. With it, you have a structured map that tells you exactly where to focus and ensures you do not skip anything.

## STRIDE as a Reasoning Framework

STRIDE is six categories of threats. Its value is not that it is exhaustive in an absolute sense — it is that it provides systematic coverage across the categories of security properties that matter. Without it, threat identification is biased toward whatever the participants happen to have seen recently or read about last week. STRIDE ensures you ask six distinct questions at every relevant point in the system.

Each STRIDE category maps directly to a security property it threatens and, by extension, to the category of control that mitigates it:

| Category | Threatens | Example Control Category |
|---|---|---|
| **Spoofing** | Authentication | Tokens, mutual TLS, certificates |
| **Tampering** | Integrity | Signatures, checksums, input validation |
| **Repudiation** | Non-repudiation | Audit logs, immutable event streams |
| **Information Disclosure** | Confidentiality | Encryption (transit/rest), access controls |
| **Denial of Service** | Availability | Rate limiting, circuit breakers, quotas |
| **Elevation of Privilege** | Authorization | RBAC, least-privilege, input validation |

This mapping is the engine of the framework. When you identify a threat, the category immediately tells you what kind of mitigation to consider.

### Applying STRIDE to the Payment Flow

Walk the DFD's trust boundaries and apply each category. At the browser-to-API-Gateway boundary: **Spoofing** — can an attacker forge or steal a session token and submit a checkout request as another user? **Tampering** — can the request body be modified in transit (this is largely handled by TLS, but what about after TLS termination — does the API Gateway validate the integrity of the payload before forwarding it)? **Information Disclosure** — do error responses from the gateway leak internal service names, stack traces, or valid user IDs?

At the Order Service–to–Payment Provider boundary: **Spoofing** — how does the Payment Provider verify that requests are genuinely from your system and not from an attacker who has discovered the endpoint? (API keys, mutual TLS, IP allowlisting.) **Tampering** — can an attacker intercept and modify the payment amount between your service and the provider? **Repudiation** — if a payment succeeds but the user claims it didn't, do you have a signed, timestamped record from the provider that proves otherwise? **Information Disclosure** — are raw credit card numbers flowing through your system at all, or are you using tokenization to keep them off your servers entirely?

At the Order Service–to–Database boundary: **Elevation of Privilege** — if the Order Service's database credentials are compromised, can they be used to read or modify data in other databases? Does the service's database user have `DROP TABLE` permissions it never needs? **Tampering** — can a compromised Order Service modify historical order records, or are completed orders written to an append-only store?

Each of these is not a hypothetical worry — it is a specific architectural question that demands a specific design decision. That is the mechanism: STRIDE applied at trust boundaries converts a vague concern about security into a concrete engineering task.

## From Threats to Design Requirements

A real system produces dozens to hundreds of identified threats. You cannot address them all equally, and attempting to do so will either stall the project or produce uniformly shallow mitigations. Prioritization requires assessing two dimensions for each threat: how likely is it to be exploited, and how severe is the impact if it is.

A straightforward approach is a risk matrix — categorize each threat as high, medium, or low along both dimensions. A threat that is high-likelihood and high-impact (credential theft through a spoofed session at your API boundary) demands immediate mitigation. A threat that is low-likelihood and low-impact (denial of service against an internal admin tool used by three people) can be accepted.

For each prioritized threat, you choose one of four responses. **Mitigate** means implementing a control that reduces likelihood or impact — this is the most common response. **Accept** means explicitly deciding not to address a threat because the cost of mitigation exceeds the expected risk — this must be a documented, conscious decision, not a silent omission. **Transfer** means shifting the risk to another party, like using a managed service that assumes responsibility for that security boundary or purchasing insurance. **Eliminate** means removing the component or feature that creates the threat entirely — if you use tokenized payment references and never handle raw card numbers, the entire category of cardholder data exposure disappears from your threat surface.

The critical output is not the threat list itself. It is the resulting design requirements. "The Order Service database user must have only `INSERT` and `SELECT` permissions on the `orders` table." "All service-to-payment-provider communication must use mutual TLS with certificate pinning." "Checkout API responses must not include internal error details; errors must be mapped to generic client-safe codes." These statements are implementable. They go into the design document. They become acceptance criteria. They are the bridge between threat modeling and the code that gets written.

## When and Who

Threat modeling is triggered by architectural decisions, not by schedules. The right moments are: when designing a new service or system, when adding an integration with an external party, when changing how authentication or authorization works, when introducing a new data store for sensitive information, and when significantly changing a deployment topology. You do not threat model every pull request. You threat model the decisions that create or move trust boundaries.

The session requires someone who understands the system's architecture (typically the designing engineer or tech lead), and ideally someone with security expertise who can recognize non-obvious attack patterns. The security person is not there to generate a list of requirements from on high — they are there because recognizing that a particular API design enables parameter tampering that bypasses authorization checks requires specific adversarial knowledge that most application engineers have not built.

## Where Threat Modeling Breaks Down

**The ritual failure mode.** Organizations adopt threat modeling, create templates with pre-populated threat categories, and mandate that every project fill one out. Engineers treat it as a compliance exercise. They write "SQL injection" in the threats column without examining whether their system uses SQL at all. They write "DDoS" without identifying which specific component lacks rate limiting. The output is a document that provides false confidence — it looks like security was considered, but no actual reasoning about the system's specific architecture occurred. If your threat model does not reference specific components and specific data flows in your system, it is not a threat model.

**Scope explosion.** A system of any real complexity can generate a threat surface that is unmanageable in a single analysis. Teams that try to model their entire microservices architecture in one session produce an overwhelming list that never gets prioritized and never results in action. Effective threat modeling is scoped tightly: one flow, one subsystem, one significant change. The payment processing flow is a scope. "Our platform" is not.

**Model decay.** A threat model captures your architecture at a specific point in time. When the architecture changes — a new service is added, a data flow is rerouted, a new external integration is introduced — the threat model becomes stale. Mitigations designed for the original architecture may not cover the current one. A trust boundary that didn't exist when the model was built now exists unexamined. This means threat modeling is not a one-time design phase artifact. It requires revisiting when the architecture it describes changes.

**The expertise ceiling.** STRIDE provides structure, but structure alone does not produce insight. Asking "can an entity gain elevated privileges here?" is useful only if you can recognize the mechanisms by which privilege escalation actually happens — insecure direct object references, JWT algorithm confusion, path traversal, deserialization attacks. Purely engineering-driven threat modeling without adversarial security knowledge catches the obvious architectural issues but misses the subtle implementation-level threats that experienced attackers exploit. This is not a reason to skip threat modeling — catching the obvious architectural issues is enormously valuable. But it is a reason to involve security expertise when it is available and to invest in adversarial thinking skills across the engineering team over time.

**Completeness is not the goal.** No threat model will ever identify every possible threat. Novel techniques, creative adversaries, and implementation bugs that only manifest under specific conditions will always produce surprises. Threat modeling addresses the structural, predictable threats that emerge from your architecture — the ones that are visible in the data flows and trust boundaries. The remaining tail risk is handled by the defense-in-depth mechanisms covered in the Level 1 post: runtime monitoring, anomaly detection, network policies, and incident response.

## The Model to Carry Forward

Threat modeling is architecture review through an adversarial lens, made systematic by two structural tools: the DFD tells you where to look, and STRIDE tells you what to ask. The output is not awareness — it is design requirements that exist at specific points in your system for specific, articulable reasons.

The conceptual shift that matters: security controls are not features you bolt onto a system after designing it. They are constraints that emerge from the architecture itself, discoverable through structured analysis. Mutual TLS between services, input validation at API boundaries, rate limiting at entry points, audit logging for sensitive operations — these are not items from a generic security checklist. They are responses to specific threats at specific trust boundaries in your specific system. When you understand why a control needs to exist at a particular point, you implement it correctly. When you are just following a checklist, you implement it superficially and miss the cases the checklist didn't enumerate.

This is what makes building with confidence possible. When you sit down to implement security controls, you are not guessing at what matters — you are executing design decisions that trace back to a structured analysis of how your system actually works.

## Key Takeaways

- Threat modeling is not brainstorming about what might go wrong — it is a structured decomposition of your system's data flows and trust boundaries, with systematic threat enumeration at each crossing point.

- Trust boundaries — where data moves between components at different privilege levels or controlled by different entities — are where threats concentrate and where your analysis should focus.

- STRIDE provides six categories of threats (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), each mapping to a specific security property and a specific category of mitigation, which is what makes it a reasoning tool rather than just a mnemonic.

- The output of a threat model is not a document or a risk register — it is a set of concrete, implementable design requirements tied to specific components and data flows in your system.

- Every identified threat gets one of four responses: mitigate, accept, transfer, or eliminate — and "accept" must be an explicit, documented decision, not a silent omission.

- Threat modeling should be scoped to a specific flow, subsystem, or architectural change — attempting to model an entire system at once produces analysis that is too broad to act on.

- Threat models decay when the architecture they describe changes; they must be revisited when new services, data flows, or trust boundaries are introduced.

- STRIDE provides structure but not adversarial insight — involving someone with security expertise significantly improves the quality of identified threats beyond what application engineers will find on their own.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Security work often fails not because engineers have never heard of common attacks, but because they cannot map those attacks onto their own system. They know words like “SQL injection” or “credential theft,” but when asked where their architecture actually changes trust, what assumptions a service is making about incoming data, or which component is responsible for enforcing a control, they do not have a clear answer. The result is security theater: a checklist gets completed, a threat model document exists, but the system design stays the same.

What breaks in practice is concrete. An API trusts fields from the browser that should have been derived server-side. A backend service has broader database permissions than it needs, so one compromised credential becomes a much larger incident. A new third-party integration quietly creates a new path for sensitive data to leave the system, but nobody recognizes it as a new trust boundary. Without a working threat model, teams discover these problems after an incident, during an audit, or when the system is already expensive to change.

Threat modeling exists because architecture creates predictable security consequences. If you can see where data flows and where trust changes, you can often catch the structural problems early enough to make cheap design decisions instead of expensive repairs.

---

## What You Need To Know First

**1. Data flow**  
A data flow is just the path data takes through a system: who sends it, which component receives it, where it is stored, and where it goes next. For this article, the important thing is not protocol detail but visibility: you need to be able to say “this request starts in the browser, passes through the gateway, reaches this service, then gets written to this database.”

**2. Authentication vs authorization**  
Authentication answers “who are you?” Authorization answers “what are you allowed to do?” These get mixed up constantly. A user can be successfully authenticated and still be allowed to do too much. That distinction matters because different threat categories target different security properties.

**3. Security boundary / trust boundary**  
A trust boundary is a place where one component has to stop assuming the world is safe and decide what it can trust about incoming data. Usually this happens when data comes from a different actor, privilege level, runtime, network zone, or external service. The key idea is simple: crossing a boundary means assumptions must be re-checked.

**4. Security controls**  
A security control is a mechanism you add to reduce a threat: token validation, rate limiting, encryption, least-privilege permissions, audit logging, and so on. You do not need a taxonomy here. Just hold the idea that controls are not abstract “security things”; they are specific mechanisms attached to specific parts of a system.

---

## The Key Ideas, Connected

**Threat modeling starts by understanding your system, not by brainstorming attacks.**  
The article’s first important move is to reject the usual “let’s list bad things” approach. If you begin with attacker ideas in the abstract, you mostly get whatever people remember from recent incidents or security training. That produces generic threats, not system-specific insight. So the process starts with a model of your own architecture: what components exist, what data moves between them, and where it crosses from one context into another.

That is why the next idea matters: to reason about threats, you need a representation of the system that makes those crossings visible.

**A data flow diagram is useful because it shows where data goes and what it crosses.**  
A DFD is not trying to capture every implementation detail. It strips the system down to a few element types: outside actors, processes, storage, and the flows between them. That simplification is what makes it usable. You are not optimizing for documentation completeness; you are optimizing for being able to inspect how data moves.

Once you have that picture, one feature of it becomes the main object of analysis: the trust boundary. Without the DFD, trust boundaries are easy to miss because they are buried inside architecture diagrams, deployment details, or service descriptions.

**Trust boundaries are where security questions become necessary, because assumptions change there.**  
A trust boundary is not magical; it is just the point where a receiving component can no longer safely inherit the assumptions of the sender. Data from a browser is not trustworthy in the same way as data from an internal service you operate. Data leaving your infrastructure for a third-party provider is no longer under your confidentiality controls. A service talking to a database with privileged credentials is crossing into a different security context.

This is why threats “concentrate” at trust boundaries. The risk is not the arrow on the diagram by itself; the risk is that the receiving side may trust something it should have verified, expose something it should have concealed, or allow something it should have constrained. Once you accept that trust changes at these points, you need a systematic way to ask what can go wrong at each one.

**STRIDE matters because it gives you complete-enough coverage at each boundary instead of relying on memory.**  
STRIDE is useful less as a mnemonic and more as a forcing function. At each trust boundary, it makes you ask six different kinds of questions: could someone fake identity, alter data, deny having acted, learn something they should not, exhaust the system, or gain permissions they should not have? The point is not that STRIDE perfectly captures all security reality. The point is that it prevents threat identification from collapsing into “what attacks do we happen to remember?”

The reason the framework works mechanically is that each category lines up with a security property. Spoofing attacks authentication. Tampering attacks integrity. Information disclosure attacks confidentiality. Elevation of privilege attacks authorization. That mapping matters because once you classify a threat, you immediately have a direction for mitigation. So the process does not stop at naming threats; it naturally pulls you toward control categories.

**Applying STRIDE at specific trust boundaries converts vague security concern into concrete architectural questions.**  
This is the operational heart of the article. At the browser-to-API boundary, “spoofing” is not just a word; it becomes “how does the gateway know this token really belongs to this user?” At the service-to-payment-provider boundary, “information disclosure” becomes “are we sending raw card data at all, or did we design the flow to avoid handling it?” At the service-to-database boundary, “elevation of privilege” becomes “what exact permissions does this database identity have?”

That shift is important: the threat model becomes useful only when each threat is attached to a component, a flow, and an assumption. Otherwise you just have category labels. Once attached, threats stop being abstract fears and become design questions that require design answers.

**Because real systems generate many threats, you need prioritization, not equal treatment.**  
As soon as you apply this method seriously, you get a long list. That is a sign the process is working, not failing. But if every identified threat gets the same attention, the team either freezes or implements shallow defenses everywhere. So the next step is risk evaluation: how likely is exploitation, and how bad is the impact if it happens?

This leads directly to response selection. Prioritization is what makes it possible to act instead of just document.

**Each threat needs an explicit response: mitigate, accept, transfer, or eliminate.**  
This is where threat modeling becomes decision-making rather than analysis for its own sake. Some threats deserve technical controls. Some are consciously tolerated because the mitigation cost is not worth it. Some are shifted to managed providers or contractual arrangements. Some disappear because you redesign the system so the risky condition no longer exists.

“Eliminate” is especially important because it shows that architecture can remove whole classes of problems. If your system never handles raw card numbers, you have not merely reduced that risk; you have removed an entire exposure surface. That is a stronger outcome than adding controls around a dangerous flow you chose to keep.

**The real output of threat modeling is design requirements, not the threat list.**  
This is the article’s main practical claim. A threat list by itself does not change a system. What changes a system is a requirement like “this service account may only read these tables,” or “all traffic to the payment provider must use mutual TLS,” or “client-visible errors must be generic and not leak internal details.” Those are buildable, testable, reviewable constraints.

This is why the earlier steps matter. DFD gives you the structure. Trust boundaries tell you where assumptions change. STRIDE tells you what to ask. Risk treatment tells you what deserves action. All of that exists so you can produce design constraints that influence implementation.

**Threat modeling should be triggered by architectural change, because trust boundaries move when the design moves.**  
If the mechanism is “analyze trust boundaries in a specific architecture,” then the right time to do it is when the architecture is being created or changed. A new service, a new external integration, a new authentication scheme, a new data store, or a new deployment topology can all create new boundaries or alter old assumptions. That is why threat modeling is not a per-PR exercise and also not a once-per-project exercise. It belongs at moments where the structure of trust is changing.

This also explains model decay. A threat model describes a system as it existed when you drew it. If the architecture changes, the model can quietly stop corresponding to reality.

**Threat modeling fails when it becomes ritual, too broad, stale, or disconnected from expertise.**  
The article names several breakdowns, and they all follow from losing contact with the underlying mechanism. Ritual failure happens when teams fill in template threats without tying them to actual flows and components. Scope explosion happens when the model is so broad that the team cannot turn findings into decisions. Model decay happens when the DFD and trust boundaries no longer match the live system. The expertise ceiling appears because the framework can force the question, but someone still has to recognize subtle attack patterns in the answer.

That last point is worth holding clearly: structure helps you ask better questions, but it does not guarantee you will notice every exploit path. Threat modeling improves systematic coverage of architectural risk; it does not replace security expertise or runtime defenses.

**The deeper shift is that security controls are consequences of architecture, not decorations added afterward.**  
This is the unifying idea the article wants the reader to leave with. If a control is there for a real reason, you can point to the trust boundary and threat that made it necessary. If you cannot, there is a good chance you are either applying generic checklist security or missing the actual place the control belongs. Understanding the architecture-security connection is what turns security from paperwork into engineering.

---

## Handles and Anchors

**1. “DFD tells you where to look; STRIDE tells you what to ask.”**  
If you remember only one sentence, remember this one. The diagram locates the important crossings. STRIDE prevents you from asking only the questions you already know to ask.

**2. Trust boundaries are customs checkpoints, not roads.**  
The road is just movement. The checkpoint is where someone inspects what is coming through, decides what is allowed, and applies rules because the thing arriving came from somewhere with different assumptions. Threat modeling focuses on the checkpoints.

**3. Ask of any new design: “What data crosses from one trust context into another, and what must the receiver verify before acting on it?”**  
That question is usable in design reviews, architecture docs, and implementation discussions. If you can answer it clearly, you are already doing the core move of threat modeling.

---

## What This Changes When You Build

**An engineer who understands this will approach architecture diagrams differently because they are looking for trust changes, not just service relationships.**  
The unaware engineer draws boxes and arrows to explain system structure and call patterns. The aware engineer asks which arrows cross privilege, ownership, or security-context boundaries and marks those explicitly. That changes what gets discussed in design review: not just “service A calls service B,” but “what is service B allowed to assume about this input, and what must it verify?”

**An engineer who understands this will design APIs differently because client input is treated as a boundary crossing, not as application state.**  
The unaware engineer often trusts values that came from the browser because they arrived through an authenticated session: price, user ID, role hints, resource identifiers. The aware engineer distinguishes authenticated caller from trustworthy payload and designs the API so sensitive values are derived server-side or revalidated. That reduces parameter tampering and authorization bypasses that otherwise look like “normal requests.”

**An engineer who understands this will scope permissions more narrowly because service-to-database communication is recognized as a privilege boundary.**  
The unaware engineer provisions one broad database user because it is fast and operationally simple. The aware engineer asks what the service actually needs to do at that boundary and constrains credentials accordingly: maybe read-only on one table, maybe insert-only for append records, definitely no unused administrative privileges. The practical outcome is that a compromised service account turns into a contained incident instead of full data compromise.

**An engineer who understands this will evaluate third-party integrations differently because adding an external dependency also adds a new trust boundary and data exposure path.**  
The unaware engineer sees a payment provider, analytics SDK, or webhook consumer mainly as a feature integration. The aware engineer asks what data leaves the system, how the third party authenticates requests, what comes back that must be validated, and whether the architecture can avoid sending sensitive data at all. That often leads to tokenization, narrower payloads, signature verification, or refusing an integration pattern that was convenient but unsafe.

**An engineer who understands this will treat threat model outputs as implementation constraints because otherwise the exercise has no effect on the built system.**  
The unaware engineer leaves the threat model in a document repository and assumes “security was considered.” The aware engineer turns findings into requirements that appear in tickets, acceptance criteria, test plans, and config review: exact auth mechanisms, exact logging expectations, exact error-handling rules, exact rate limits, exact permission scopes. That is the difference between analysis that influences code and analysis that becomes compliance evidence.

</details>
