## Metadata
- **Date:** 18-05-2026
- **Source:** 08_network_security.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Web Security

The web is the most exposed surface your organisation has, and it is exposed for a structural reason that no amount of patching will fix: it was never designed to be secure. HTTP was designed to fetch documents. Cookies were bolted on to give it memory. JavaScript was bolted on to give it behaviour. Databases were bolted on to give it data. Every layer of the modern web is a feature retrofit on top of a protocol that assumed a polite, academic user. The attackers know this. The defenders are still catching up.

The cleanest way to hold web security in your head is to recognise that a web application is three things stacked on top of each other, and each of the three has its own kind of failure. There is the architecture (the LAMP stack or its equivalent — operating system, web server, database, scripting layer), there is the session (the way the application pretends to remember who you are across stateless requests), and there is the input (every byte the user sends you, all of which is hostile until proven otherwise). Almost every well-known web attack lives in exactly one of these three zones, and almost every defensive technique is a response to a specific failure within one of them.

The architecture problem is the one developers are least likely to think about and most likely to lose to. Your code may be flawless, but it runs on a Linux box you did not configure, behind an Apache server you did not tune, talking to a MySQL instance someone set up two years ago. A misconfigured server or an unpatched OS gives an attacker access that no amount of clean PHP can prevent. Defence here is not clever; it is hygienic. Patch the layers, harden the defaults, and stop assuming that "it isn't your job."

The session problem is more interesting because it is genuinely intrinsic. HTTP is stateless — every request arrives without memory of the last one — and yet users expect to log in once and stay logged in. The web's answer is the cookie: a small token the browser carries on every subsequent request that says, in effect, "this is who I am." This works, but it creates a brutal asymmetry. The cookie is a bearer credential, meaning whoever holds it is the user, full stop. An attacker who steals your session cookie does not need your password and does not need to defeat your multi-factor authentication. They simply ride the session you already authenticated. This is why modern session cookies must be marked HttpOnly (so JavaScript cannot read them), Secure (so they only travel over HTTPS), and SameSite (so other sites cannot trigger them) — three flags that cost nothing to set and are still missing from production systems every day.

The input problem is where most of the famous attacks live, and it has a single underlying cause: browsers and databases cannot tell the difference between your code and a user's text. If a user's name is rendered into a page, and that name happens to contain a `<script>` tag, the browser will execute it — that is cross-site scripting (XSS), and a stored version of it is how the Samy worm took down MySpace. If a user's input is concatenated into a database query, and that input happens to contain SQL syntax, the database will execute it — that is SQL injection, and it is how TalkTalk lost 150,000 customer records and COMELEC lost 55 million. If an attacker can trick your already-authenticated browser into submitting a request to your bank, the bank cannot tell that you did not mean to send it — that is cross-site request forgery (CSRF). All three attacks are the same mistake at different layers: trusted code and untrusted data sharing the same channel with no separator.

The defences mirror the attacks. Against SQL injection, use prepared statements — parameterised queries that send the structure of the command and the user's data to the database on separate tracks, so the data can never be interpreted as a command. Against XSS, encode all output: convert `<` to `&lt;` so the browser renders the script as harmless text instead of executing it. Against CSRF, attach an unguessable token to every state-changing request, so an attacker cannot forge a valid one from another origin. Underneath all of this sits the browser's Same-Origin Policy, which segregates data by protocol, host, and port and is the reason web security has not collapsed entirely.

The practical move, once you hold this model, is to stop reading attack lists and start reading the OWASP Top 10 — the industry's running consensus on which categories of failure are causing the most damage right now — and to use a structured threat-modelling approach like STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege) when you design something new. The frameworks matter less than the habit they enforce, which is asking, before you ship: where is the trust boundary, what crosses it, and what happens if what crosses it is hostile?

The deeper lesson is that web security is not a checklist you complete; it is a posture you adopt. The web treats every request as untrusted by default, and the application has to earn the trust back, request by request, input by input, session by session. Developers who internalise this stop writing "if (user is admin)" and start writing "prove, on this request, that this user is still the admin they were a minute ago." That shift — from authenticate-once to verify-continuously, from sanitise-sometimes to encode-always, from trust-by-default to zero-trust — is what separates a web application that survives contact with the internet from one that does not.

## Level 2 candidates

**SQL Injection and Prepared Statements** — Covers how injection actually works at the query-parser level, the difference between escaping and parameterisation, and why ORMs do not automatically protect you. Worth deeper treatment because the gap between "I know what SQLi is" and "I can audit a codebase for it" is wide, and the failure modes (second-order injection, stored procedures, dynamic table names) are not obvious from the basic definition.

**Cross-Site Scripting (XSS) and Output Encoding** — Covers the three flavours (reflected, stored, DOM-based), the contexts in which encoding rules differ (HTML body, attribute, JavaScript, URL), and why Content Security Policy exists. Worth going deeper because correct XSS defence is context-sensitive in a way most developers underestimate, and getting it wrong silently fails.

**Session Management and Cookie Security** — Covers session lifecycle, the HttpOnly/Secure/SameSite flags in detail, token rotation, session fixation, and the rise of "pass-the-cookie" attacks that bypass MFA. Worth depth because session theft is now the dominant credential attack and the defences are subtle.

**Cross-Site Request Forgery (CSRF) and the Same-Origin Policy** — Covers how browsers decide what counts as a same origin, how CSRF tokens are generated and validated, and how SameSite cookies have changed the threat landscape. Worth depth because the SOP has many edge cases (CORS, postMessage, subdomain trust) that are routinely misunderstood.

**The OWASP Top 10 and Threat Modelling Frameworks** — Covers the current OWASP categories, how to read them as a prioritisation tool rather than a checklist, and how STRIDE and PASTA structure proactive threat analysis. Worth depth because these are the lingua franca of professional security work and the difference between using them well and using them ritualistically is significant.

**HTTPS, TLS, and the Untrusted Network** — Covers why HTTPS is non-optional, what TLS actually guarantees (and what it does not), certificate validation, and the "malicious cafe owner" threat model that makes the network itself an attacker. Worth depth because the assumptions HTTPS makes are routinely violated in practice and developers need to know where the guarantees end.

---

# Discussion

## Why This Conversation Is Happening

Web security exists because the web stack keeps accepting input from places you do not control and then doing powerful things with it: rendering it in a browser, executing it in an app, using it in a database query, or attaching it to an authenticated user session. That combination is what makes the web so useful, and also what makes it so fragile. The problem is not just “bugs happen.” The problem is that the web is built out of layers that were not originally designed with hostile traffic in mind, so security failures tend to emerge at the joins between those layers.

When engineers do not have a clear model of this, they defend the wrong thing. They focus on application code but ignore server misconfiguration. They implement login correctly but treat the session cookie casually. They validate some inputs but miss the deeper rule that code and data must stay separated. The result is that systems which look fine in happy-path testing fail immediately when exposed to real traffic from attackers.

This topic matters because web security is not a specialist concern sitting off to the side of normal engineering. It changes how you design request flows, how you store trust, how you move data across layers, and how you think about “user input.” If you do not have that model, security feels like an endless list of attacks. If you do have it, the attack list collapses into a small number of recurring engineering mistakes.

## What You Need To Know First

**HTTP is stateless.**  
HTTP treats each request as independent. If your browser loads a page, then clicks a button, the server does not automatically “remember” that those two requests came from the same person. Any sense of continuity — being logged in, having a cart, keeping preferences — has to be added on top.

**A cookie is usually how the web fakes memory.**  
A cookie is a small piece of data the browser stores and sends back with later requests. In practice, a session cookie often acts like “proof” that the server already authenticated you. That means the cookie is valuable: if someone else can use it, they can often act as you.

**Browsers and databases parse structure, not intent.**  
A browser does not know whether some text “was meant to be content” if it looks like HTML or JavaScript. A database does not know whether some string “was meant to be a name” if it looks like SQL syntax. These systems follow syntax rules, not developer intention, which is why mixing untrusted input into commands is dangerous.

**A trust boundary is any point where outside data enters a more trusted system.**  
When a browser sends a form, when an API accepts JSON, when a service reads headers, when an app uses a cookie to identify a user — each of these is a trust boundary. The basic security question is always: what crossed the boundary, and how do we stop it from being treated as more trustworthy than it is?

## The Key Ideas, Connected

**A web application is easiest to understand as three security zones: architecture, session, and input.**  
This is a simplifying model, but it is a useful one because it groups failures by where they happen. Some attacks happen because the underlying stack is weak or misconfigured. Some happen because the app has to remember users across stateless requests. Others happen because untrusted input gets interpreted as commands. Once you see those zones, attack categories stop feeling random, which sets up the first zone: architecture.

**The architecture layer can lose the whole game before your application logic even matters.**  
Your code runs inside an operating system, behind a web server, connected to a database, often with framework and runtime dependencies in between. If one of those layers is unpatched, overexposed, or badly configured, an attacker may not need an application bug at all. That leads to an important shift: security is not only about writing correct business logic; it is also about hardening the environment that business logic depends on. Once you accept that the platform itself can fail, the next question becomes how the app manages user identity across requests.

**The session layer exists because users expect continuity on top of a stateless protocol.**  
HTTP does not preserve identity from one request to the next, so applications create sessions to simulate continuity. Usually that means the browser sends a session cookie with each request, and the server maps that token to an authenticated user. This is convenient, but it creates a sharp security property: the token itself becomes the thing that proves identity. That naturally leads to the next idea.

**A session cookie is often a bearer credential, so possession is enough.**  
“Bearer credential” means the system treats whoever presents it as the legitimate user. The server usually does not ask, “Did the real user intend this request right now?” It asks, “Did this request arrive with the valid session token?” That is why stolen cookies are so dangerous: they bypass the need to re-enter a password or repeat MFA if the session is already established. Once you see how much power sits in the cookie, the purpose of flags like `HttpOnly`, `Secure`, and `SameSite` becomes much clearer.

**Cookie security flags are cheap ways to reduce how easily sessions are stolen or misused.**  
`HttpOnly` helps by preventing JavaScript from reading the cookie directly, which limits some session theft paths after XSS. `Secure` restricts the cookie to HTTPS, reducing exposure over insecure transport. `SameSite` limits when the browser will attach the cookie to cross-site requests, which helps against CSRF-style abuse. These do not “solve sessions,” but they narrow the easiest attack paths. That brings us to the third zone, where many famous web attacks live: input.

**Input becomes dangerous when untrusted data can be interpreted as code or commands.**  
The underlying mistake is not “users send weird strings.” The mistake is that the application allows those strings to enter places where the receiving system has executable syntax. If the browser interprets user-controlled content as script, you get XSS. If the database interprets user-controlled content as SQL, you get SQL injection. If the server accepts a forged browser request because it only sees a valid session, you get CSRF. These are different manifestations of the same deeper failure: trusted instructions and untrusted data are sharing a channel without a reliable separator.

**XSS happens when the browser is allowed to treat user-controlled content as active page logic.**  
If attacker-controlled input lands in a page in the wrong way, the browser may execute it as script instead of displaying it as text. That matters not just because scripts run, but because they run in the security context of your site: they may read page data, act as the user, or exploit the session indirectly. Seeing XSS this way makes the defense intuitive: do not let arbitrary input become executable page structure. That leads directly to output encoding.

**Output encoding works by forcing the browser to treat input as text, not markup or script.**  
When you encode special characters before rendering untrusted content, the browser displays them literally instead of interpreting them as instructions. The key idea is that the defense happens at output, in the context where interpretation would occur. You are not asking whether the input “looks safe in general”; you are making it non-executable for the specific place it is being rendered. The same separation principle appears again in databases, which leads to SQL injection.

**SQL injection happens when user input is merged into a query as if it were part of the query’s structure.**  
If you build SQL by concatenating strings, the database parser receives one mixed stream containing both command structure and untrusted data. If the input contains SQL syntax, the parser has no way to know it was “just data” in your mind. It sees a legal query and executes it. Once you understand that the parser is the real audience, the correct defense becomes obvious.

**Prepared statements solve SQL injection by sending command structure and data separately.**  
Instead of constructing one big SQL string, parameterized queries define the query shape first and bind user values separately. That means the database knows which parts are instructions and which parts are values, so the values cannot change the meaning of the command. This is stronger than hoping correct escaping was applied everywhere, because it preserves the code/data boundary structurally. That same “prove intent, do not assume it” logic appears in CSRF.

**CSRF happens when a server trusts an authenticated browser request without proving the user intentionally initiated it.**  
Browsers automatically attach relevant cookies to requests, including ones triggered from another site in some cases. So if a user is logged in and visits a malicious page, that page may cause the browser to send a valid-looking request to the target site. From the server’s point of view, the session is real — but the user’s intent is missing. This shows that authentication alone is not enough for sensitive actions, which leads to anti-CSRF mechanisms.

**CSRF tokens add proof that the request came from the legitimate application flow, not just from a browser carrying the cookie.**  
A synchronizer token or equivalent anti-CSRF value is hard for an attacker’s site to guess or supply correctly. So even if the browser sends the session cookie, the forged request still fails without the additional token. The important idea is that the server stops treating “valid session present” as sufficient evidence for state-changing requests. This sits on top of an even broader browser rule that quietly supports much of web security.

**The Same-Origin Policy is a baseline browser containment rule, not a complete security system.**  
It restricts how documents and scripts from one origin can interact with data from another origin. Without it, the web would be dramatically less defensible. But it is only a baseline: applications still need encoding, parameterization, CSRF protections, and session controls. Understanding SOP this way prevents a common mistake, which is assuming the browser will “just block bad cross-site behavior” for you. That leads to the practical mindset shift the article is driving toward.

**The real lesson is to think in trust boundaries and continuous verification, not isolated attack names.**  
OWASP Top 10 and STRIDE are useful not because they give you a checklist to memorize, but because they train you to ask structured questions: what is trusted here, what is untrusted, what crosses the boundary, and how could that crossing be abused? Once you adopt that posture, security stops being something you bolt on after features are built. It becomes a property of how requests, sessions, and data flows are designed from the start.

## Handles and Anchors

**1. Think of the web app as a building with three doors: infrastructure, identity, and content.**  
One door is the building itself: server, OS, database, runtime. One door is identity: how the app keeps recognizing you. One door is content: everything users send in. Most attacks are just different ways of getting through one of those doors.

**2. The core failure is “the system cannot tell instructions from input.”**  
If you remember one sentence, make it this one. XSS, SQL injection, and a surprising amount of adjacent web security pain reduce to the same pattern: untrusted data reached a place where it could be interpreted as something authoritative.

**3. A session cookie is closer to a badge than a password.**  
A password proves you know something. A badge proves you are already admitted. If someone steals the badge, the guard often lets them through without asking how they got it. That is the right mental model for why cookie theft is so serious and why session protections matter.

## What This Changes When You Build

**An engineer who understands this will approach deployment differently because application correctness does not compensate for platform weakness.**  
They will care about patch cadence, exposed services, database network reachability, framework/runtime versions, default server configuration, and secret handling as first-class parts of application security, not “ops details” outside the app boundary.

**An engineer who understands this will approach authentication flows differently because logging in securely is not the same as maintaining a secure session.**  
They will pay attention to session rotation after login, cookie flags, idle and absolute timeouts, re-authentication for sensitive actions, and what happens if a session token is copied rather than guessed.

**An engineer who understands this will approach data handling differently because the question is not “did we validate input?” but “where could this value be interpreted?”**  
They will inspect every sink: SQL queries, HTML rendering, template interpolation, JavaScript contexts, headers, redirects, file paths, and shell commands. The implementation habit changes from generic sanitization to context-specific defenses like prepared statements and output encoding.

**An engineer who understands this will approach browser-to-server actions differently because a valid session does not prove user intent.**  
They will distinguish read actions from state-changing actions, add CSRF protections where needed, evaluate `SameSite` behavior intentionally, and avoid designing endpoints that can perform sensitive work on the basis of ambient cookies alone.

**An engineer who understands this will approach design reviews differently because they can ask better security questions earlier.**  
Instead of asking “are we protected against XSS and SQLi?”, they will ask “where are the trust boundaries, what parser or interpreter consumes this data next, what credential is actually authorizing this request, and what happens if an attacker controls this field, header, or browser context?” That changes outcomes because it catches structural failures before they become bugs in production.