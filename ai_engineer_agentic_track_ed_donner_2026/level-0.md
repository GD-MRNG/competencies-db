# AI Engineer Agentic Track: The Complete Agent & MCP Course

## Summary

This course is an intensive, hands-on six-week programme designed to take learners from foundational agent concepts through to the confident design, construction, and deployment of autonomous AI agents using the major professional frameworks. It is positioned as a practical engineering curriculum — structured around building eight real-world projects — rather than a conceptual survey. The central thesis is that agentic AI represents a watershed moment in 2026, and practical expertise in this space opens significant career and commercial opportunities.

The course addresses a skills gap for developers and technically inclined learners who understand that AI agents matter but have not yet built fluency with the frameworks, design patterns, and deployment practices that production-grade agentic systems require. While it is best suited to those with some Python and LLM experience, foundational self-study labs are included to accommodate learners coming from less technical backgrounds.

By the end of the programme, a learner should be able to design and implement multi-agent systems using OpenAI Agents SDK, CrewAI, LangGraph, and AutoGen; apply core agentic design patterns including orchestration, tool use, guardrails, memory, and feedback loops; and integrate Model Context Protocol (MCP) servers to connect agents to external data sources and tools at scale. The capstone project — a four-agent autonomous trading floor powered by six MCP servers and 44 tools — is intended to demonstrate mastery across all of these dimensions.

The course is structured as a progressive six-week journey. Each week introduces a new framework or capability layer, building on prior weeks, and is delivered at a daily cadence with short, focused video sessions. Projects grow in complexity across the six weeks, from a personal career chatbot in week one to fully distributed, autonomous multi-agent systems in weeks five and six.

The programme also treats framework selection as a genuine design decision, dedicating attention to comparing the strengths and trade-offs of each framework rather than prescribing a single approach. Learners are expected to emerge with the judgement to choose the right tool for a given problem, not just the ability to use any one of them.

---

## Topics

**Agentic AI Foundations & Design Patterns** — Establishes core concepts including LLM autonomy, tool integration, multi-step workflows, and the five essential design patterns for building robust agentic systems; introduces the distinction between agent and workflow architectures.

**Environment Setup & Tooling** — Covers development environment configuration across Mac and Windows, including Cursor IDE, UV package manager, GitHub, and API key setup; introduces the range of frontier and open-source model API options available to learners.

**Multi-LLM Orchestration** — Explores how to combine and compare multiple LLMs — including GPT-4o, Claude, Gemini, and DeepSeek — within a single pipeline, using one model to evaluate or route the outputs of another.

**Function Calling & Tool Use** — Explains how LLMs invoke external functions, how tool call responses are processed, and how to build assistants that handle unknown questions gracefully through structured tool integration.

**Project 1 — Career Digital Twin** — A complete end-to-end project building and deploying a personal agent chatbot that represents the learner to potential employers, covering the full cycle from agent loop construction to deployment on HuggingFace Spaces via Gradio.

**OpenAI Agents SDK** — Covers the SDK's core abstractions (Agent, Runner, Trace), asynchronous Python patterns, concurrent execution with asyncio, guardrails, structured outputs with Pydantic, and hierarchical agent composition using handoffs and agents-as-tools.

**Project 2 — SDR Sales Agent** — Builds a business-ready sales development agent that crafts and sends professional emails using SendGrid, demonstrating real-world agentic automation for commercial outreach.

**Project 3 — Deep Research Agent** — Constructs a multi-agent research pipeline that conducts parallel web searches, synthesises findings, and presents results through a Gradio UI; covers planning agents, structured outputs, and async task management at scale.

**CrewAI Framework** — Introduces the CrewAI framework for building collaborative agent teams, covering agents, tasks, processing modes, LightLLM integration, memory with vector and SQL storage, and custom tool development including Google Search integration.

**Project 4 — Stock Picker Agent** — A CrewAI project that automates financial research across multiple agents, demonstrating how to build investment-focused agentic workflows with structured Pydantic outputs and push notifications.

**Project 5 — Four-Agent Engineering Team** — Deploys a software engineering team of four agents using CrewAI and Coder Agents running in Docker, capable of managing, building, and testing software applications autonomously.

**LangGraph Framework** — Covers graph-based agent architecture in depth, including state management, nodes, edges, conditional routing, checkpointing with SQLite, tool nodes, LangSmith integration, and feedback loops with worker-evaluator patterns.

**Project 6 — Browser Sidekick Agent** — Builds a personal browser automation agent using LangGraph, Playwright, and Gradio, replicating core functionality of OpenAI's Operator agent for in-browser task assistance.

**AutoGen Framework** — Introduces Microsoft AutoGen (v0.5.1), covering AgentChat for high-level multi-agent collaboration, multimodal features, structured outputs, and AutoGen Core for distributed agent communication using message handlers, gRPC runtime, and cross-process agent registration.

**Project 7 — Agent Creator Agent** — An AutoGen-powered meta-agent that autonomously writes, configures, and launches new agents, demonstrating recursive agentic capability and the outer limits of autonomous system design.

**Model Context Protocol (MCP)** — Provides a comprehensive introduction to MCP as a standardisation layer for agent-tool connectivity, covering the host-client-server architecture, existing MCP marketplaces, security considerations, and how to build and wire custom MCP servers with business logic.

**Project 8 — Autonomous Trading Floor (Capstone)** — The course capstone: four autonomous agents making live trading decisions, powered by six MCP servers (including Brave Search and Polygon for market data) and 44 tools, with a full UI for monitoring activity and portfolio management.

**Framework Selection & Agent Engineering Principles** — Closes the course with a comparative evaluation of all four frameworks (OpenAI SDK, CrewAI, LangGraph, AutoGen) and ten synthesised lessons for building production-grade agent solutions, guiding learners toward sound architectural judgement.