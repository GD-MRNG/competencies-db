# AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents

## Summary

This course is an eight-week, hands-on engineering programme designed to take Python-proficient developers through the full spectrum of modern LLM engineering — from foundational inference and API use, through open-source model deployment, retrieval-augmented generation, and fine-tuning, to production deployment with agentic capabilities. It is structured around eight real-world projects of increasing complexity, with the philosophy that practical building is the fastest and most durable path to expertise.

The course addresses the needs of developers, data scientists, and technically minded professionals who want to work seriously with large language models but lack a structured path from first principles to production-grade engineering. It assumes Python familiarity but requires no advanced mathematics, making it accessible to a broad technical audience without sacrificing depth. The target learner is someone who wants to be genuinely competitive in the AI engineering job market or capable of building commercially meaningful AI products.

By completing the course, a learner should be able to build and deploy full LLM-powered applications using both frontier and open-source models; evaluate and select among the leading models for specific tasks; implement RAG pipelines with vector embeddings and datastores; fine-tune models using both frontier APIs and QLoRA techniques on open-source models; and integrate agents into production systems with polished user interfaces. The capstone — a three-part price prediction and autonomous deal-spotting system — ties all of these capabilities together into a single deployable product.

The eight-week structure is deliberately progressive. The first two weeks establish inference and API fluency with frontier models. Weeks three and four expand into open-source models and LLM selection judgement. Week five introduces RAG. Weeks six and seven shift from inference to training, covering both frontier fine-tuning and advanced QLoRA techniques on open-source models. Week eight closes the loop with production deployment and agentisation. Each week culminates in a project that demonstrates the week's techniques in a commercially meaningful context.

The course sits at the intersection of the AI Leader and Agentic Track courses in the same programme family — it assumes more technical depth than the leadership briefing and covers more foundational LLM engineering than the agent-focused track, making it the natural core curriculum for someone building end-to-end AI engineering competence.

---

## Topics

**Transformer Fundamentals** — Introduces the architectural foundations of large language models, providing enough conceptual grounding to reason about model behaviour and selection without requiring mathematical depth.

**Frontier Model Landscape** — Surveys the leading frontier models (including GPT-4o, Claude, Gemini, and others), covering their relative strengths, cost-performance trade-offs, and how to select the right model for a given business task.

**Frontier APIs & Prompt Engineering** — Covers how to interact with frontier model APIs, structure effective prompts, and build basic generative AI workflows that produce formatted, business-ready outputs.

**Project 1 — AI Brochure Generator** — Builds a web-scraping generative AI product that navigates company websites intelligently and produces formatted sales brochures, introducing multi-step LLM workflows and real-world data ingestion.

**Multimodal Inputs & Function Calling** — Explores how frontier models handle text, images, and audio as inputs, and how function calling enables agents to take actions beyond text generation.

**Project 2 — Multimodal Airline Customer Support Agent** — Constructs a customer support chatbot with a polished UI that handles text, image, and audio interactions, demonstrating multimodal function-calling in a production-like setting.

**Open-Source Models with HuggingFace** — Introduces the HuggingFace ecosystem for accessing and running open-source models locally or in the cloud, covering ten common generative AI use cases from translation to image generation.

**Project 3 — Meeting Minutes Generator** — Builds an audio-to-text pipeline that produces structured meeting minutes and action items, using both open-source and closed-source models to compare outputs and trade-offs.

**LLM Selection & Evaluation** — Develops a framework for comparing and selecting among frontier and open-source models based on task requirements, covering ten frontier and ten open-source models in depth.

**Code Generation with LLMs** — Applies LLMs to software engineering tasks, using models to translate and optimise code across languages; demonstrates the practical ceiling of LLM-assisted code generation.

**Project 4 — Python-to-C++ Code Optimiser** — Builds a tool that translates Python code to optimised C++, achieving performance improvements of over 60,000x, illustrating LLMs as a force multiplier for software engineering.

**Retrieval-Augmented Generation (RAG)** — Provides a thorough grounding in RAG architecture, covering vector embeddings, similarity search, and integration with popular open-source vector datastores to improve model accuracy on domain-specific tasks.

**Project 5 — AI Knowledge Worker** — Constructs a full RAG-powered knowledge worker that can answer any question about a company based on its shared drive, mirroring the design of real enterprise AI products.

**Frontier Model Fine-Tuning** — Covers the transition from inference to training, explaining how to fine-tune a frontier model via API on a labelled dataset to solve a specific business problem.

**Project 6 — Price Prediction with Frontier Models (Capstone Part A)** — The first part of the three-part capstone: builds a system that predicts product prices from short text descriptions using frontier model fine-tuning.

**QLoRA & Advanced Fine-Tuning** — Introduces parameter-efficient fine-tuning techniques, specifically QLoRA, enabling learners to train open-source models on consumer-grade hardware to outperform frontier models on narrow tasks.

**Project 7 — Fine-Tuned Open-Source Price Predictor (Capstone Part B)** — Continues the capstone by fine-tuning an open-source model using QLoRA to compete with and match frontier model performance on the price prediction task, at a fraction of the cost.

**Production Deployment with Agents** — Covers deploying LLM applications to production with polished Gradio-based UIs, integrating agents to extend model capabilities, and structuring an end-to-end productionised system.

**Project 8 — Autonomous Deal-Spotting Agent System (Capstone Part C)** — Completes the capstone with a multi-agent system that autonomously compares predicted and actual prices to identify bargains and notifies the user, bringing together fine-tuning, inference, RAG, and agentic orchestration in a single deployed product.