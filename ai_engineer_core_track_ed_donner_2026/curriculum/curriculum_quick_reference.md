# AI Engineer Curriculum — Quick Reference

## The Three Tracks at a Glance

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CORE TRACK (Weeks 1-4)                                             │
│  ├─ Foundations: Decoupled Inference, Tokens, Transformers         │
│  ├─ Infrastructure: Local/Cloud Models, Prompting                  │
│  ├─ Orchestration: Tool Calling, RAG, Fine-Tuning                  │
│  └─ Reliability: Structured Outputs, Architecture, Observability   │
│                                                                     │
│  ↓ PREREQUISITE COMPLETE ↓                                          │
│                                                                     │
│  AGENTIC TRACK (Weeks 5-7)                                          │
│  ├─ Foundations: Thought-Action-Observation Loop                   │
│  ├─ Orchestration: Async, Multi-Agent, Self-Correction             │
│  ├─ Tools: Schemas, MCP, Granularity                               │
│  └─ Patterns: Graphs, Escalation, Observability, Prompting         │
│                                                                     │
│  ↓ PREREQUISITE COMPLETE ↓                                          │
│                                                                     │
│  PRODUCTION TRACK (Weeks 8-11)                                      │
│  ├─ Foundations: Decoupled Architecture, Secrets, Docker            │
│  ├─ Cloud: Platforms, Terraform, Databases, Networking             │
│  ├─ Reliability: Monitoring, Error Handling, Testing, Costs         │
│  └─ Scale: Multi-Agent, Distributed, Observability, Security       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Decision: Where Am I?

### "I'm brand new to AI engineering"
→ **START:** Core Track
- Mandatory foundation for everything else
- No exceptions

### "I've used ChatGPT but haven't built anything"
→ **START:** Core Track
- Using ≠ Building
- Learn the fundamentals

### "I've built something with prompts/APIs"
→ **START:** Core Track (validate first)
- Do you understand tokenization? Structured outputs? Tool calling?
- If yes to all three → Could skip to Agentic, but not recommended
- If no to any → Back to Core

### "I've built agents locally"
→ **START:** Agentic or Production (validate first)
- Validate: Do you understand loops? Multi-agent patterns? MCP?
- If yes → Can start Production
- If no → Back to Agentic

### "I have production systems running"
→ **START:** Production Track
- Your bottleneck is scale/reliability, not AI logic
- Start with L1-01 (80/20) and L1-02 (Secrets)

---

## The Mandatory Sequence

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ CORE TRACK   │  ──→ │ AGENTIC      │  ──→ │ PRODUCTION   │
│ (Essential)  │      │ TRACK        │      │ TRACK        │
│              │      │ (If building │      │ (If shipping │
│ 15 Topics    │      │ autonomous   │      │ to users)    │
│ 2-4 weeks    │      │ systems)     │      │              │
│              │      │ 15 Topics    │      │ 16 Topics    │
└──────────────┘      │ 2-3 weeks    │      │ 3-4 weeks    │
   (Do not skip)      └──────────────┘      └──────────────┘
                         (Do not skip)         (Do not skip)
```

---

## Critical Topics (Don't Skip)

### From Core Track
- **L1-01:** Decoupled Inference — Everything depends on this
- **L1-02:** Tokenization — Understand economic constraints
- **L1-08:** Tool Calling — How to wire models to data
- **L1-11:** Structured Outputs — How to enforce reliability

### From Agentic Track  
- **L1-01:** The Loop — The core pattern
- **L1-02:** Workflows vs. Agents — Knowing which to use
- **L1-08:** Tool Definition — Getting schemas right

### From Production Track
- **L1-01:** 80/20 Rule — Understand infrastructure load
- **L1-02:** Secrets Management — Critical security
- **L1-03:** Docker — Standard deployment
- **L1-09:** Observability — Can't manage what you don't measure

---

## What Happens If You Skip

| If You Skip | What Breaks | Cost |
|---|---|---|
| **Core L1-02 (Tokens)** | Systems break under longer user input | 1-2 weeks debugging |
| **Core L1-08 (Tools)** | Can't wire models to data; infinite loops | 2-3 weeks redesign |
| **Core L1-11 (Structured)** | Production systems crash on malformed JSON | 1 week firefighting |
| **Entire Core → Agentic** | Agent behavior unpredictable; loops endlessly | 4-8 weeks of debugging |
| **Entire Core+Agentic → Prod** | Ship broken systems; 3 AM pages; rewrites | 2-4 weeks post-launch |
| **Core L1-02 → Production** | Leak API keys; get hacked | Catastrophic |

**Pattern:** Every week you skip costs you 4-8 weeks later. Don't do it.

---

## Checkpoints: Am I Ready?

### Ready for Agentic Track?
Answer **yes** to ALL:
- [ ] What is statelessness and why does it matter?
- [ ] How do I call an LLM and get structured JSON back?
- [ ] How do I design a tool schema an LLM can use?
- [ ] What is context size vs. token count vs. cost?
- [ ] Have I built something that calls an LLM?

**If not:** Go back to Core. Seriously.

### Ready for Production Track?
Answer **yes** to ALL:
- [ ] Can I explain the Thought-Action-Observation loop?
- [ ] Have I built multi-agent or complex agent systems?
- [ ] When do I use workflows vs. agents?
- [ ] Can I design a multi-agent architecture?
- [ ] Have I debugged agent behavior?

**If not:** Complete Agentic. You'll waste time otherwise.

---

## Time Estimates

| Track | Duration | Prerequisites | Next |
|-------|----------|---|---|
| **Core** | 2-4 weeks | None | Agentic Track |
| **Agentic** | 2-3 weeks | Core ✓ | Production Track |
| **Production** | 3-4 weeks | Core ✓ + Agentic ✓ | Ship! |
| **Total** | 7-11 weeks | Sequential | Real system in production |

---

## Common Mistakes (And Their Costs)

### ❌ "I'll skip Core and learn on the job"
Cost: 8-16 weeks of debugging

### ❌ "I'll build an agent without understanding loops"
Cost: 4-8 weeks of weird behavior

### ❌ "I'll deploy to production before hardening"
Cost: 2-4 weeks of 3 AM pages

### ❌ "I'll over-engineer multi-agent before understanding single-agent"
Cost: 3-6 weeks of refactoring

### ❌ "I'll use a framework without understanding the underlying pattern"
Cost: Forever being helpless when it breaks

---

## Entry Points by Problem

### "I need a RAG system"
Core: L1-01 → L1-05 → L1-09 → Ship
(Optional: Agentic if you want agents querying docs)

### "I need a chatbot"
Core: L1-01 → L1-05 → L1-06 → Ship on Vercel
(Skip Agentic unless you need tool calling)

### "I need autonomous agents"
Core (all) → Agentic (all) → Production (L1-01, L1-09, L1-13) → Ship

### "I need to scale to 10K+ users"
Core (all) → Agentic (optional) → Production (all) → Ship

### "I need enterprise compliance"
Core (all) → Agentic (if agents) → Production (esp. L1-02, L1-16) → Ship

---

## File Structure

```
/outputs/
├── ai-engineer-curriculum-overview.md          ← START HERE
├── ai-engineer-core-track_level-0.md           ← Track 1
├── ai-engineer-agentic-track_level-0.md        ← Track 2
├── ai-engineer-production-track_level-0.md     ← Track 3
├── curriculum-integration-summary.md           ← Integration guide
└── curriculum-quick-reference.md               ← THIS FILE
```

---

## Next Steps

1. **Read:** Curriculum Overview (20 min)
2. **Assess:** Where are you? (5 min)
3. **Commit:** "I will complete Core Track in 4 weeks" (1 min)
4. **Start:** First topic in your track
5. **Build:** Something real at the end of each track
6. **Ship:** Production Track → Real users

---

## The One Rule

**DO NOT SKIP AHEAD.**

Each track depends on the previous one. Skipping saves 1-2 weeks and costs 4-8 weeks later.

The curriculum works. Trust it.

---

## FAQ

**Q: Can I skip topics?**
A: Only if you can explain them fluently and implement them from scratch. Most people can't; don't assume you're the exception.

**Q: How long can I take?**
A: 7-11 weeks is the healthy pace. Take 6 months and you'll forget what you learned. Rush it in 3 weeks and you'll miss the patterns.

**Q: I'm experienced; can I just do Production?**
A: Not unless you've built working LLM systems before. If you haven't, Core is mandatory.

**Q: What if I need this for work right now?**
A: You still need Core. An extra 4 weeks now beats 4 months of firefighting later.

---

**Created:** June 4, 2026  
**Version:** 1.0  
**Last Updated:** Today