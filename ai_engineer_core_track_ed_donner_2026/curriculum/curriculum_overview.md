# AI Engineer Full Curriculum — Overview and Learning Path

This document provides a master view of the complete AI Engineer curriculum and how to navigate it.

---

## The Three Tracks

The AI Engineer curriculum consists of three sequential tracks, each building on the previous one. **You must complete them in order.**

### Track 1: Core Track (15 topics)
**What:** Understanding AI as a decoupled service, managing context, and building reliable single-shot and multi-turn systems.

**Why:** Every AI system depends on understanding how models work, how to prompt them reliably, and how to integrate them with real data.

**Duration:** 2-4 weeks of focused learning.

**Key Outcomes:**
- Call models locally and via APIs reliably
- Manage context and tokens strategically
- Wire models to data via tool calling and RAG
- Enforce reliability through structured outputs
- Understand tradeoffs (cost, latency, accuracy)

**Essential Topics (Don't Skip):**
- L1-01: Decoupled Inference — The foundation of all AI engineering
- L1-02: Tokenization — Understanding economic and architectural constraints
- L1-08: Tool Calling — How to wire models to real data
- L1-11: Structured Outputs — How to enforce reliability

### Track 2: Agentic Track (15 topics)
**What:** Building autonomous systems where the model decides what to do next, managing loops, and orchestrating multiple agents.

**Why:** Once you can call a model reliably, the next frontier is making models reason dynamically. This unlocks autonomous agents that can solve multi-step problems.

**Duration:** 2-3 weeks of focused learning (after Core).

**Prerequisites:** Must complete Core Track, especially L1-08 (Tool Calling) and L1-11 (Structured Outputs).

**Key Outcomes:**
- Master the Thought-Action-Observation loop
- Build multi-agent systems that specialize and parallelize
- Implement self-correction and error recovery
- Design tool ecosystems using MCP
- Add safety via escalation and approval workflows

**Essential Topics (Don't Skip):**
- L1-01: The Agentic Loop — The core pattern of all autonomous systems
- L1-02: Workflows vs. Agents — Understanding when to use each
- L1-05: Multi-Agent Teams — Scaling beyond a single agent
- L1-08: Tool Definition — Getting schemas right so tools work reliably

### Track 3: Production Track (16 topics)
**What:** Taking working AI systems and making them reliable, observable, scalable, and secure for real users.

**Why:** An agent that works on your laptop is worthless. This track teaches you to deploy, monitor, scale, and harden systems for production.

**Duration:** 3-4 weeks of focused learning (after Core and Agentic).

**Prerequisites:** Must complete Core and Agentic tracks completely. You need working AI logic before worrying about infrastructure.

**Key Outcomes:**
- Deploy AI systems to production (Docker, Cloud)
- Manage secrets, IAM, and security properly
- Monitor systems and respond to issues
- Scale to thousands of concurrent users
- Implement observability and cost management

**Essential Topics (Don't Skip):**
- L1-01: 80/20 Rule — Understanding that 80% of production is infrastructure
- L1-02: Secrets Management — Critical security from day one
- L1-03: Containerization (Docker) — The standard way to deploy
- L1-09: Observability — You can't manage what you can't measure

---

## Complete Learning Path

### Fast Track (New to AI Engineering)
**Total time: 6-12 weeks**

1. **Core Track (2-4 weeks)**
   - Complete all 15 topics
   - Build a working prototype (API call → prompt → structured output)
   - Understand tradeoffs (local vs. cloud, cost vs. reasoning, latency vs. accuracy)

2. **Agentic Track (2-3 weeks)**
   - Master L1-01 (The Loop) in raw Python
   - Build a multi-agent system with tool calling
   - Implement observability and error handling

3. **Production Track (2-3 weeks)**
   - Deploy your agent to AWS/cloud
   - Add monitoring and alerting
   - Harden for reliability

**Outcome:** A production-ready agent serving real users.

---

### Specialist Paths Within the Curriculum

**Path A: "I need a RAG system for document Q&A"**
- Core Track: L1-01 → L1-05 → L1-09 (RAG)
- Build and validate retrieval quality
- Production Track: L1-01 → L1-06 → L1-09 (observability)
- Ship with monitoring

**Path B: "I need multi-agent reasoning (e.g., financial analysis)"**
- Core Track: L1-01 → L1-05 → L1-06 (Prompting) → L1-08 (Tools)
- Agentic Track: L1-01 (Loop) → L1-03 (Model Choice) → L1-05 (Teams)
- Production Track: L1-01 → L1-13 (Multi-Agent) → L1-14 (Job Queues)
- Ship with Terraform-managed infrastructure

**Path C: "I need a chatbot for internal tools"**
- Core Track: L1-01 → L1-05 → L1-06 (Prompting)
- Agentic Track: L1-01 (Loop) — optional, depends on complexity
- Production Track: L1-01 → L1-05 (Vercel PaaS) → L1-09 (basic observability)
- Ship quickly with minimal infrastructure

**Path D: "I need an agent that browses the web and takes actions"**
- Core Track: All 15 topics (especially L1-08 Tool Calling)
- Agentic Track: All 15 topics (especially L1-09 MCP for browser tools)
- Production Track: L1-01 → L1-03 (Docker) → L1-05 (AWS App Runner) → L1-14 (containers vs. Lambda)
- Ship with proper sandboxing and limits

---

## What NOT to Do

### ❌ Mistake 1: Skip Core Track
**Why this fails:**
- You'll misunderstand context windows and build systems that break under user input
- You won't understand tokenization and costs will spiral
- You'll try to use tool calling without understanding schemas, creating infinite loops
- You'll expect features that are mathematically impossible with stateless models

**Cost of skipping:** 2-4 weeks of wasted debugging and 100+ hours of frustration.

### ❌ Mistake 2: Start with Production
**Why this fails:**
- You'll spend weeks on Terraform and Docker, then realize your AI logic is broken
- You'll optimize infrastructure that doesn't matter because your bottleneck is model accuracy
- You'll build complex systems that fail in ways you can't understand without knowing how agents work
- You'll ship non-functional code to production

**Cost of skipping:** 1-3 months of misdirected effort.

### ❌ Mistake 3: Skip Agentic Track if you need autonomous systems
**Why this fails:**
- You'll try to build agents without understanding loops, getting stuck in infinite recursion
- You'll make tool calling decisions without understanding tradeoffs, shipping unreliable systems
- You'll over-engineer multi-agent architectures because you don't understand when they're needed
- You'll spend weeks debugging agent behavior that would take minutes if you understood the patterns

**Cost of skipping:** 4-8 weeks of debugging and redesign.

### ❌ Mistake 4: Rush Production before systems are stable
**Why this fails:**
- You'll deploy systems to production that aren't ready, causing customer-facing outages
- You'll optimize costs for systems that are broken, missing the real bottleneck
- You'll have no observability into why systems fail, leading to 3 AM pages
- You'll have to refactor the entire system after launch because you didn't plan for scale

**Cost of rushing:** 2-4 weeks of firefighting and rewrites post-launch.

---

## Decision Trees: Which Track to Start With

### "I'm brand new to AI engineering"
→ Start with **Core Track**
- You need foundations before anything else
- Everything you build later depends on this
- No shortcuts available

### "I'm a traditional software engineer new to AI"
→ Start with **Core Track**
- You know how to build systems, but not how models work
- Core teaches the mental models that are different from traditional software
- Agentic patterns will feel natural once you understand Core

### "I have used ChatGPT and want to build my own systems"
→ Start with **Core Track**
- Using an AI as a consumer ≠ building AI systems
- Core teaches the fundamentals you're missing
- At least 2-4 weeks before moving forward

### "I've built with LLMs before (prompting, basic API calls)"
→ Consider **Agentic Track** (but validate Core knowledge first)
- You understand L1-01 (Decoupled Inference)
- You probably understand L1-05 (API-Based Inference)
- **But test yourself:** Can you explain L1-08 (Tool Calling) and L1-11 (Structured Outputs) in detail?
- If not, go back to Core and strengthen those topics

### "I have built working agents and want to deploy them"
→ Go straight to **Production Track**
- You've completed Core and Agentic implicitly
- Your bottleneck is infrastructure and scale, not AI logic
- Start with L1-01 and L1-02, then focus on your specific needs

---

## Checkpoints: Self-Assessment

### "Am I ready for Agentic Track?"

✅ You're ready if you can answer "yes" to:
- [ ] Can you explain why models are stateless and why this matters?
- [ ] Can you write code that calls an LLM and gets structured JSON back?
- [ ] Can you design a tool schema (function name, parameters, return type) that an LLM could use reliably?
- [ ] Do you understand the difference between context size, token count, and cost?
- [ ] Have you built something that calls an LLM and integrates the output into an application?

❌ You're not ready if:
- [ ] You think you can skip Core because you "understand prompting"
- [ ] You've only used ChatGPT, not built anything
- [ ] You don't understand token counting or context windows

**If not ready:** Go back to Core Track. Invest the time now.

### "Am I ready for Production Track?"

✅ You're ready if you can answer "yes" to:
- [ ] Can you explain the Thought-Action-Observation loop in detail?
- [ ] Have you built a system with multiple agents or a complex workflow?
- [ ] Do you understand when to use workflows vs. agentic loops?
- [ ] Can you design a multi-agent architecture for a complex problem?
- [ ] Have you dealt with observability and debugging in agents?

❌ You're not ready if:
- [ ] You've only written single-prompt code
- [ ] You don't understand agentic loops
- [ ] You think "just Docker it" is a production strategy

**If not ready:** Complete Agentic Track. You'll waste time in Production if you skip this.

---

## How Tracks Interconnect

### Core Topics Used in Agentic

| Core Topic | How It's Used in Agentic |
|-----------|--------------------------|
| L1-01 (Decoupled Inference) | Understanding that tool calls are just text generation |
| L1-02 (Tokenization) | Managing token budgets in long agent loops |
| L1-08 (Tool Calling) | The foundation of Agentic L1-01 (The Loop) |
| L1-11 (Structured Outputs) | Ensuring tool calls are valid JSON reliably |
| L1-14 (Architecture) | Designing where logic lives (model vs. code) |
| L1-15 (Observability) | Debugging agent behavior |

### Core + Agentic Topics Used in Production

| Topic | How It's Used in Production |
|-------|----------------------------|
| Core L1-01 + Agentic L1-01 | Understanding bottlenecks and where to optimize |
| Core L1-02 + Agentic Loops | Token budgeting and cost management (Prod L1-12) |
| Agentic L1-04 + Prod L1-04 | Async execution at scale (FastAPI + concurrent agents) |
| Agentic L1-05 + Prod L1-13 | Multi-agent architecture in production |
| Core L1-15 + Agentic L1-13 + Prod L1-09 | Observability throughout the stack |

---

## Time Investment vs. ROI

| Track | Time | ROI | When It Pays Off |
|-------|------|-----|------------------|
| **Core** | 2-4 weeks | 100x | Within 2 weeks (fundamental errors caught) |
| **Agentic** | 2-3 weeks | 10x | Within 1 week (autonomous systems work, don't loop forever) |
| **Production** | 3-4 weeks | 50x | Within 1 month (systems scale, you sleep at night) |

**Total investment:** 7-11 weeks
**Break-even:** First working product shipped without major rewrites

---

## Common Pitfalls by Track

### Core Track Pitfalls
- **Skipping L1-02 (Tokenization):** You'll build systems that break unexpectedly when users ask longer questions
- **Not mastering L1-01 (Statelessness):** You'll expect features the system can't possibly have
- **Avoiding L1-11 (Structured Outputs):** Your systems will crash on malformed JSON in production

### Agentic Track Pitfalls
- **Not starting with L1-01 (the loop in raw Python):** You'll over-complicate with frameworks before understanding the basics
- **Underestimating L1-02 (Workflows vs. Agents):** You'll build autonomous systems that should be workflows, wasting cost and latency
- **Skipping L1-08 (Tool Definition):** Your tools will be unreliable, causing infinite loops

### Production Track Pitfalls
- **Skipping L1-02 (Secrets Management):** You'll leak API keys and get pwned
- **Starting with Kubernetes before understanding L1-05 (Cloud Choice):** You'll over-engineer for your current scale
- **Deferring L1-09 (Observability):** You'll ship systems you can't understand when they fail

---

## The Mentor's Final Advice

1. **Do not skip tracks.** The curriculum is sequential for a reason. Every hour you invest in Core saves 10 hours in Agentic and 100 hours in Production.

2. **Build something at the end of each track.** Don't just read. Write code. Deploy it. Feel what breaks and why. This is where real learning happens.

3. **Master the patterns, not the tools.** FastAPI, Vercel, Terraform—these change. The patterns (decoupled architecture, the control loop, observability) don't. Learn the patterns deeply.

4. **Understand tradeoffs, not absolutes.** "Should I use Kubernetes?" depends on your scale, not on being "right." Understand what each choice trades off.

5. **Invest in observability early.** You cannot manage what you cannot measure. Add logging and tracing from day one, not after production fires.

6. **The 80/20 rule is real.** In AI engineering, 20% is the model and 80% is the infrastructure. Accept this. Don't spend 3 weeks optimizing prompts when you should spend 1 day on secrets management.

---

## Next Steps

1. **Assess yourself:** Use the checkpoints above. Where are you?
2. **Pick your starting track:** Almost certainly Core (unless you've already built multiple working LLM systems)
3. **Set a goal:** "I will complete Core Track in 4 weeks" or "I will deploy one system using this curriculum"
4. **Work through sequentially:** Don't jump around. Each topic depends on the previous ones
5. **Build and ship:** At the end of each track, deploy something real. Don't just read

---

## FAQ

**Q: Can I learn all three tracks simultaneously?**
A: No. Your brain needs to integrate each layer before the next makes sense. Core → Agentic → Production, in order.

**Q: I'm running a startup and need to hire. Which track should I require candidates to know?**
A: Depends on the role. Backend AI engineers: Core + Production. Autonomous agents: Core + Agentic. Everyone: Core.

**Q: I've done some of these topics. Can I test out?**
A: Use the checkpoints. If you can't answer the "ready" questions with confidence, you have gaps. Fill them.

**Q: How long until I can ship a production system?**
A: 7-11 weeks if you're new. 4-6 weeks if you have relevant background. But rushing = technical debt = costs later.

**Q: What if I focus on just one track?**
A: You'll be incomplete. Core alone = prototype. Core + Agentic = research/demo. Core + Agentic + Production = real product.

---

## You Are Here

You're reading this because you want to build real AI systems, not play with ChatGPT. Good news: this curriculum works. It's designed for people like you—professionals with technical background who want to master a new domain.

Bad news: it takes time. 7-11 weeks of focused learning. But it's non-negotiable. Every shortcut you try to take will cost you more time later.

So: Pick a starting point, commit to 8-10 weeks, and work through sequentially. By the end, you'll have built systems that work, that scale, that make money.

Let's go.