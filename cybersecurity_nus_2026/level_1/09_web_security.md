## Metadata
- **Date:** 18-05-2026
- **Source:** 09_web_security.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Web Security

Web applications are the most exposed surface your organisation operates, and they are exposed in a way that is structurally different from almost any other system you run. A database has a perimeter. An internal service has a perimeter. A web application, by definition, does not — its job is to take input from anyone in the world, hand that input to a backend, and return something useful. Every defence you build sits on top of that fundamental concession. This is why web security is not a checklist of patches but a way of thinking about what happens when untrusted input meets a system that was designed, mostly, to be helpful.

The first thing to internalise is that the web is built on a stateless protocol. HTTP has no memory. Each request arrives as if for the first time, which means every notion of "logged in," "shopping cart," or "admin user" is a fiction the application maintains on top of the protocol — usually through cookies or session tokens. This matters because the entire concept of identity on the web reduces to a string the browser sends along with each request. Steal that string and you are the user. You did not need their password. You did not need to defeat their multi-factor authentication. You needed a cookie. Once you see this clearly, a large fraction of modern attacks stop looking like separate phenomena and start looking like variations on a theme: get the token, ride the session, act as someone else.

The second thing to internalise is that the stack is wider than the code you wrote. A typical web application — the canonical example is the LAMP stack of Linux, Apache, MySQL, and PHP — runs across an operating system, a web server, a database, and an application layer, plus whatever JavaScript executes in the browser on the client side. An attacker does not care which layer they break. They care that one of them is breakable. A perfectly written application running on an unpatched server is compromised. A hardened server running careless SQL is compromised. Web security is layered or it is nothing, and the layers do not protect each other automatically.

The major attacks all share a common root cause: the system cannot tell the difference between code and data. SQL injection works because user input gets concatenated into a database query, and the database has no way to know that the string `' OR 1=1 --` was supposed to be a username rather than part of the query syntax. Cross-site scripting works because user input gets reflected into an HTML page, and the browser has no way to know that the `<script>` tag came from an attacker rather than from the developer. The fix in both cases is structural rather than cosmetic. Prepared statements separate query structure from query parameters at the protocol level, so input cannot become code no matter what it contains. HTML entity encoding converts the dangerous characters into their inert visual equivalents before they reach the browser's parser. Filtering input by looking for "bad words" is the wrong mental model; the right one is architectural separation between the channel that carries instructions and the channel that carries data.

Cross-site request forgery is a different beast and worth understanding on its own terms. CSRF does not steal anything. It exploits the fact that your browser automatically attaches your cookies to any request going to a site you are logged into, including requests triggered by a different site you happened to visit. If you are logged into your bank in one tab and you load a malicious page in another, that page can cause your browser to issue a transfer request that your bank will happily authenticate, because your cookie came along for the ride. The defence — anti-CSRF tokens — works by demanding a piece of information that the attacker's site cannot know and cannot guess, attached to every state-changing request. The browser's same-origin policy helps here too, by preventing scripts on one origin from reading responses from another, but same-origin protection is a fence, not a wall, and configuration mistakes routinely punch holes in it.

The threat model you bring to all of this matters more than any individual mitigation. The useful framing is to assume the network is hostile, the user's input is hostile, and any third-party script you load is potentially hostile. Frameworks like STRIDE — spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege — give you a structured way to walk through an application and ask where each category of failure could occur. The OWASP Top 10 gives you the empirical version: here are the categories of mistake that actually cause breaches in the wild, ranked by frequency and impact. Use the first to think systematically and the second to check your work against reality.

The breaches that make the news — TalkTalk losing 150,000 customer records to a SQL injection in 2015, the Philippines' COMELEC losing 55 million voter records the next year, Marriott losing hundreds of millions of guest records in 2018 — are not exotic. They are the boring attacks executed against real systems that did not implement the boring defences. This is the uncomfortable truth at the centre of the discipline: most web breaches do not happen because attackers were clever. They happen because somebody concatenated a string into a SQL query, or forgot to set a cookie flag, or trusted a piece of input they should not have trusted. Web security as a working competency is mostly the discipline of not doing those things, consistently, across every endpoint, forever. The mental model that makes this sustainable is simple — never trust input, never store identity in a token you have not protected, never let the same code path carry both instructions and data — and the rest is engineering.

## Level 2 candidates

**SQL Injection and Prepared Statements** — Covers how SQL injection actually works at the query-parsing level, the spectrum from classic injection to blind and time-based variants, and why parameterised queries fix it structurally rather than cosmetically. Worth a deep dive because the mechanics of the database protocol — and the specific reason concatenation is unsafe while parameter binding is safe — reward technical depth that a Level 1 post cannot give.

**Cross-Site Scripting (XSS)** — Covers the three flavours (reflected, stored, DOM-based), how each delivers attacker-controlled JavaScript into a victim's browser context, and the defence stack from output encoding to Content Security Policy. Worth going deeper because the DOM-based variant in particular requires understanding how the browser's parser and JavaScript runtime interact, which is non-obvious and frequently mishandled.

**Cross-Site Request Forgery and the Same-Origin Policy** — Covers the browser security model that makes CSRF possible, the precise rules of same-origin (protocol, host, port), and the defence mechanisms including anti-CSRF tokens and SameSite cookies. Worth a deep dive because the browser's security boundaries are subtle, full of historical exceptions, and the source of many real-world bypasses.

**Sessions, Cookies, and Token Security** — Covers how stateless HTTP is turned into a stateful application via session tokens, the cookie attributes that protect them (HttpOnly, Secure, SameSite, expiry), and modern attacks like session fixation and pass-the-cookie that bypass MFA. Worth depth because session management sits at the centre of nearly every authenticated web application and the failure modes are operationally severe.

**Threat Modelling with STRIDE and OWASP** — Covers structured frameworks for reasoning about application threats before code is written, including STRIDE's six categories, PASTA's risk-centric process, and the OWASP Top 10 and ASVS as practical reference standards. Worth a Level 2 because applied threat modelling is a methodology, not a fact, and it benefits from worked examples on a real architecture.

**The Web Application Stack and Its Attack Surface** — Covers the LAMP-style architecture in detail, what each layer does, where vulnerabilities concentrate at each layer, and how attacks chain across layers. Worth going deeper because most developers know their layer well and the others poorly, and the cross-layer view is where defence-in-depth actually lives.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Web applications are unusual systems because they are built to accept input from strangers. That is not an edge case; it is the job. A web app has to take data from browsers it does not control, over networks it does not trust, and turn that into useful actions inside systems that do matter: databases, payment flows, admin panels, internal APIs. That is why web security feels different from securing an internal service. Exposure is not accidental. Exposure is the product.

When engineers do not have a clear mental model of this, they reach for shallow fixes. They look for “bad inputs,” patch individual bugs, or assume the framework is handling it somewhere. But most serious web failures come from misunderstanding a few structural facts: HTTP is stateless, identity is usually represented by bearer tokens like cookies, and many attacks work by smuggling untrusted data into places where the system expects instructions. If you do not see those patterns, attacks look like a random catalogue. If you do, they collapse into a small number of repeatable engineering problems.

The practical consequence is that security stops being a bolt-on concern and becomes a design discipline. The engineer who understands web security does not just know names like SQL injection or CSRF; they can look at a request path and ask, “Where is trust being assumed here, and what actually enforces it?”

## What You Need To Know First

**HTTP is stateless.**  
HTTP does not remember previous requests. Every request arrives on its own, with no built-in memory of who the user is or what they were doing before. So when a site seems to “remember” that you are logged in or that your cart has three items, that memory is being recreated by the application using things like cookies, session IDs, or tokens.

**A browser automatically does some things on the user’s behalf.**  
Browsers attach cookies to matching requests, render HTML, execute JavaScript, and enforce rules like the same-origin policy. This matters because many web attacks are really attacks on browser behaviour: the attacker is not breaking crypto, they are getting the browser to send something, render something, or trust something in a dangerous context.

**Code and data are not the same thing, even if they are both strings.**  
A username, a SQL fragment, and a `<script>` tag can all be represented as text, but systems should not treat them interchangeably. Security problems often begin when untrusted data is inserted into a context where the receiver interprets it as instructions. You do not solve that by “spotting dangerous strings” reliably; you solve it by keeping instruction channels and data channels separate.

**Authentication and authorisation are different.**  
Authentication answers “who are you?” Authorisation answers “what are you allowed to do?” A session cookie may authenticate a request as coming from Alice, but the application still has to decide whether Alice is allowed to read this record, trigger this action, or access this admin route. Many web systems fail because they prove identity and then assume permission.

## The Key Ideas, Connected

**Web security begins with the fact that a web application is designed to accept untrusted input.**  
That is the starting condition, not an exception. A web app cannot avoid hostile input by closing itself off, because its purpose is to receive requests from the outside world. So the core problem is never “how do we stop all bad input from arriving?” The core problem is “how do we handle untrusted input safely at every boundary?” Once you see that, the next idea matters: the web has very little built-in notion of trusted identity.

**HTTP itself does not know who a user is, so applications simulate identity on top of it.**  
Because HTTP is stateless, the application has to invent continuity. It does that with cookies, session IDs, bearer tokens, and similar mechanisms. “Logged in” is not a property of the protocol; it is a state the application reconstructs on each request from a token the browser presents. That leads directly to a harsh but useful conclusion: if an attacker gets the token, they often get the user.

**In practice, web identity often collapses to possession of a token.**  
If the server treats a cookie or session token as proof of identity, then stealing or replaying that token can be enough to act as the victim. The attacker may not need the password, and they may not need to defeat MFA at the moment of use, because the authenticated session already exists. This is why cookie handling, session storage, expiry, and flags like `HttpOnly`, `Secure`, and `SameSite` are not implementation trivia. They are part of the identity system. Once you understand that sessions are fragile trust objects, you can widen the view from “the app” to “the whole stack that handles them.”

**The attack surface is the whole web stack, not just the application code you wrote.**  
A request passes through many layers: browser, client-side JavaScript, network edge, web server, application runtime, database, operating system, and often third-party services. An attacker only needs one weak point that leads to leverage. That means a secure ORM does not save you from a vulnerable server configuration, and a patched server does not save you from reflected user input that becomes executable script in a browser. This is why web security has to be layered. But layered defence only helps if you understand the common failure pattern connecting these attacks.

**Many major web vulnerabilities happen when a system confuses data with instructions.**  
This is the deep structural pattern behind several attack classes. In SQL injection, user input is placed into a SQL statement in a way that lets the database parse the input as part of the query itself. In cross-site scripting, user input reaches the browser in a context where the browser parses it as HTML or JavaScript instead of inert text. In both cases, the receiving system is not “fooled” by clever wording; it is simply doing what its parser is designed to do with mixed instruction/data input. That naturally raises the next question: what kind of defence actually fixes that?

**The strongest defences are structural: separate code from data before parsing happens.**  
Prepared statements work because the SQL structure is defined first and user values are bound as parameters, so the database never has to guess whether the input is syntax. Output encoding works because dangerous characters are transformed before the browser interprets the content, so the data is rendered as text instead of executed as markup or script. This is a very important shift in mindset. Blacklists and ad hoc filtering try to recognise dangerous payloads after the fact. Structural defences make the ambiguity impossible in the first place. But not every attack works by turning data into code.

**CSRF works even when the attacker cannot read your site, because it abuses the browser’s automatic credential sending.**  
Cross-site request forgery is different from injection. The attacker does not need to steal the cookie or inject code into the target site. They just need the victim’s browser to send a request to the target while the browser automatically includes the victim’s existing cookies. If the site accepts “valid cookie present” as enough proof for a state-changing action, the forged request may succeed. This leads to the need for a second proof: something the attacker’s site cannot provide.

**CSRF defences add proof of request origin or user intent beyond ambient cookies.**  
Anti-CSRF tokens work because they require a value tied to the user’s session and page state, not just a cookie the browser sends automatically. `SameSite` cookie settings can also reduce when cookies are attached cross-site. The same-origin policy helps limit what one site’s scripts can read from another origin, but it does not stop all cross-origin request sending, and configuration mistakes can weaken it further. So now the pattern is broader: web security is not just about hostile inputs, but about hostile assumptions in the browser-server trust relationship.

**Because these failures repeat in different forms, engineers need a threat model, not just a bag of mitigations.**  
If you only memorise named attacks, you end up reacting case by case. A threat model gives you a way to inspect a system systematically. STRIDE asks what could be spoofed, tampered with, denied, disclosed, or escalated. OWASP gives you a reality check from common breach patterns. Together they help you move from “I know these attack names” to “I can walk a design and spot where trust is being assumed, where identity can be replayed, where data may become code, and where one layer is relying on another layer to save it.” That is the connective tissue of the whole topic.

**The practical lesson is that most web security failures are ordinary engineering failures under hostile conditions.**  
The famous incidents are not memorable because the attacks were magical. They are memorable because ordinary mistakes met internet-scale exposure. A concatenated SQL string, an over-trusted cookie, an unencoded output path, an over-permissive cross-origin configuration — these are small local decisions with large external consequences. So the working competency is not “be paranoid about everything in the abstract.” It is “design every boundary so that untrusted input stays data, identity tokens are treated as sensitive credentials, and no single layer is assumed to make the rest safe.”

## Handles and Anchors

**1. A web app is a helpful machine taking requests from strangers.**  
That is the core tension. The system is supposed to be responsive and useful, but it must do that without trusting the party making the request. If you keep this in your head, many security practices stop feeling like bureaucracy and start feeling like the minimum needed to operate safely.

**2. A session cookie is closer to a hotel keycard than to a password.**  
The server often does not care who physically holds it; possession is what matters. If someone copies the keycard, they may be able to open the door without knowing the guest’s name or how they checked in. This is a strong anchor for understanding session theft, pass-the-cookie attacks, and why cookie protection matters so much.

**3. Never let the parser guess whether a string is data or instructions.**  
This is the shortest useful sentence for injection-class problems. If the database, browser, shell, or template engine has to interpret mixed content and infer intent, you are already in danger. Good defences remove the guesswork structurally.

## What This Changes When You Build

**An engineer who understands this will design request handling around trust boundaries, not just feature flow, because every external input is adversarial by default.**  
That changes how they review endpoints, form handlers, query parameters, headers, file uploads, and webhook payloads. They do not ask only “does this work?” They ask “what is trusted here, why is it trusted, and what enforces that trust?”

**An engineer who understands this will treat session tokens as credentials in their own right, because possession of the token often is the authentication event in practice.**  
That changes decisions around cookie flags, token storage, rotation after login or privilege change, session expiry, logout invalidation, and exposure to client-side JavaScript. It also changes incident response: suspicious token leakage is treated like account compromise, not just a logging issue.

**An engineer who understands this will prefer structural separation mechanisms over input filtering, because parsers do not care about your intention after they start interpreting text.**  
That means using parameterised queries instead of concatenated SQL, context-appropriate output encoding instead of “sanitising strings” generically, safe templating defaults, and APIs that preserve the distinction between code and data. They will be suspicious of any fix that depends on maintaining a list of “bad patterns.”

**An engineer who understands this will design state-changing routes to require more than ambient browser credentials, because browsers send cookies automatically and attackers can exploit that behaviour.**  
That changes how they implement forms, API mutations, and sensitive account actions. They add CSRF protections, use `SameSite` deliberately, and distinguish between requests that merely read state and requests that change it. They also stop assuming “the user is authenticated” means “this request was intentionally initiated from our app.”

**An engineer who understands this will review the full path of a request across layers, because compromise usually follows the weakest layer, not the one they personally own.**  
That changes deployment and architecture decisions: patch cadence, reverse-proxy configuration, TLS termination, database permissions, third-party script inclusion, CSP policy, and logging. They stop saying “the app is secure” as if the runtime, web server, browser context, and dependencies are outside the problem.

</details>
