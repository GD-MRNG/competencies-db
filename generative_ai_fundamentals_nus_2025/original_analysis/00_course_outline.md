# Generative AI: Fundamentals to Advanced Techniques — Level 0 Orientation Document

## Summary

This programme is an end-to-end technical education in Generative AI, offered by the NUS School of Computing (SoC) in collaboration with Emeritus. It is designed to take learners from foundational programming and machine learning concepts all the way through to state-of-the-art generative techniques including diffusion models, large language models, and multi-agent systems. The course runs for 14 weeks online, with live faculty sessions supplementing self-paced pre-recorded content, and culminates in a capstone project.

The programme addresses a clear professional need: Generative AI is reshaping every industry, and practitioners who lack technical fluency in its underlying methods risk being left behind. It is aimed primarily at early-to-mid-level professionals seeking to enter or pivot into the AI field, and at mid-level professionals who already work adjacent to AI and want a rigorous technical grounding in how modern generative systems are actually built. The course is not a business overview — it is a hands-on technical deep dive requiring programming experience as a prerequisite.

By the end of the programme, learners are expected to be able to write Python code for machine learning tasks, build and train neural networks using TensorFlow and Keras, understand and work with Transformer architectures including BERT and GPT, implement generative models such as VAEs, GANs, and diffusion models, and deploy retrieval-augmented generation (RAG) pipelines and multi-agent systems using frameworks like LangChain. The programme also addresses AI ethics and societal impact.

The course blends theory with practice throughout. Tool-based learning is a stated design principle, and learners gain hands-on exposure to a wide ecosystem of industry tools including Keras, Hugging Face, LangChain, Kaggle, Runway, and others. Assignments are graded by industry practitioners, and a progressive capstone project runs through the programme to give learners an applied, real-world deliverable.

Credentials awarded are a verified digital certificate from the NUS School of Computing. The programme is not eligible for SkillsFuture Credit (SFC) and is delivered through Emeritus's learning platform, with 12 months of post-completion access to materials.

---

## Topics

**Overview of Python** — Covers Python fundamentals including data types, variables, operators, control flow constructs, object-oriented programming, and key libraries (Pandas, Matplotlib). Serves as the programming foundation for the rest of the course.

**Machine Learning Fundamentals** — Introduces core ML concepts and learning paradigms: unsupervised learning (clustering, correlation analysis), supervised learning (regression, classification, KNN), and an introduction to artificial neural networks.

**Deep Learning Fundamentals and GenAI Introduction** — Reviews ANNs and introduces deep convolutional neural networks (DCNNs) for both tabular and image data. Provides a first look at Generative AI and Transformers as a bridge to subsequent modules.

**Transformer Architecture and Attention Mechanisms** — Explains the Transformer architecture in detail, covering encoder-decoder structure, embedding layers, self-attention, multi-head attention, feedforward networks, and training strategies. Also surveys applications in NLP and computer vision and recent architectural innovations.

**Transformer-Based Models: BERT and GPT** — Studies the two dominant families of pre-trained language models. Covers each model's architecture, pre-training and fine-tuning procedures, application case studies, implementation best practices, and performance optimisation.

**Reinforcement Learning for Generative AI** — Introduces reinforcement learning from first principles (Markov Decision Processes, Bellman equations, Q-learning, policy gradients) through to its application in fine-tuning language models, including Reinforcement Learning from Human Feedback (RLHF) and Direct Preference Optimisation (DPO), with a ChatGPT case study.

**Early Image Generation Models: VAEs and GANs** — Covers the mechanics and training of Variational Autoencoders and Generative Adversarial Networks as foundational image generation approaches, including their practical application to image synthesis tasks.

**Image Generation Using Diffusion Models** — Explains diffusion processes, diffusion model architecture, training and sampling procedures, and performance optimisation. Surveys current applications of diffusion models in generative image tasks.

**Transformers for Vision: ViT and CLIP** — Introduces Vision Transformers (ViT) and Contrastive Language-Image Pre-Training (CLIP), explaining how Transformer architectures are adapted for computer vision tasks.

**Multimodal Models: Text-to-Image (DALL-E and Stable Diffusion)** — Covers the fundamentals of multi-modal AI, text-to-image generation architectures, API integration, prompt engineering for image generation, fine-tuning for specialised tasks, and ethical considerations around model limitations.

**Generative AI Applications I: LLMs and RAG** — Introduces LangChain as a framework for building conversational AI, covers the implementation of chains, and provides a thorough treatment of Retrieval-Augmented Generation (RAG) including vector embeddings and document integration for performance optimisation.

**Generative AI Applications II: Multi-Agents** — Explores multi-agent system design, communication protocols, coordination strategies, and multi-agent reinforcement learning. Covers LLMs as autonomous agents capable of task planning and execution, along with current challenges and future directions.

---

## Metadata
- **Date:** 24-05-2026
- **Source:** 00_course_outline.txt
- **Model:** gemini-3.5-flash
- **Prompt:** cognitive-assets/prompts/knowledge_extraction_and_mapping.txt

## LLM Processed Content

## 1. Analytical Summary

The provided curriculum document outlines a pedagogical architecture designed to transition learners from foundational programming to state-of-the-art generative AI engineering. The central thesis of this curriculum is that true competency in generative AI cannot be achieved through high-level business overviews or simple API consumption; instead, it requires a rigorous, bottom-up reconstruction of the mathematical and structural paradigms underlying modern models. By structuring the educational journey from basic Python and classical machine learning up to multi-agent systems, the curriculum asserts that advanced generative techniques are logical evolutions of foundational deep learning principles rather than isolated phenomena.

This curriculum directly responds to a critical gap in the professional landscape: the prevalence of "wrapper-level" developers who can call APIs but lack the deep technical fluency to optimize, fine-tune, or architect custom AI systems. To resolve this, the course structure is divided into three progressive phases: foundational mechanics (Python, machine learning, and basic neural networks), core architectural paradigms (Transformers, attention mechanisms, and reinforcement learning), and advanced generative applications (diffusion, multimodal systems, retrieval-augmented generation, and autonomous multi-agent frameworks). This progression ensures that when students encounter complex systems, they understand the underlying vector spaces, attention matrices, and probabilistic distributions driving them.

The strength of this curriculum lies in its uncompromising technical depth and its logical, highly structured sequence, which avoids the common pitfall of teaching tools without their theoretical underpinnings. However, the curriculum relies on the heavy assumption that a diverse cohort of early-to-mid-level professionals can successfully digest highly complex mathematical and architectural concepts—ranging from Bellman equations and Markov Decision Processes to diffusion sampling and contrastive learning—within a compressed 14-week timeframe. Furthermore, while it promises hands-on mastery, the sheer breadth of topics covered suggests that several advanced areas, such as multi-agent reinforcement learning and custom transformer training, may lean more toward conceptual exposure than deep, production-grade engineering competency.

## 2. Concept Inventory

*   **Supervised Learning**
    *   *What it explains*: How models learn mapping functions from labeled training data to make predictions or classifications on unseen data.
    *   *Connects to*: Unsupervised Learning, Artificial Neural Networks.
*   **Unsupervised Learning**
    *   *What it explains*: How models discover hidden patterns, structures, or groupings in unlabeled data.
    *   *Connects to*: Supervised Learning, Variational Autoencoders.
*   **Artificial Neural Networks (ANNs)**
    *   *What it explains*: How interconnected nodes (neurons) can approximate complex non-linear functions through backpropagation.
    *   *Connects to*: Deep Convolutional Neural Networks, Transformer Architecture.
*   **Deep Convolutional Neural Networks (DCNNs)**
    *   *What it explains*: How spatial hierarchies of features can be automatically and adaptively learned from grid-structured data like images.
    *   *Connects to*: Artificial Neural Networks, Vision Transformers.
*   **Self-Attention Mechanism**
    *   *What it explains*: How a model dynamically weights the importance of different parts of an input sequence relative to a specific token, regardless of their distance from one another.
    *   *Connects to*: Transformer Architecture, Multi-Head Attention.
*   **Multi-Head Attention**
    *   *What it explains*: How a model can simultaneously attend to information from different representation subspaces at different positions, enhancing representation capacity.
    *   *Connects to*: Self-Attention Mechanism, Transformer Architecture.
*   **Encoder-Decoder Structure**
    *   *What it explains*: How an input sequence can be compressed into a latent representation and then reconstructed or translated into a target sequence.
    *   *Connects to*: Transformer Architecture, Variational Autoencoders.
*   **Pre-training and Fine-tuning**
    *   *What it explains*: How a model can first learn general representations on a massive dataset before being adapted to specific downstream tasks with limited data.
    *   *Connects to*: Transformer Architecture, Reinforcement Learning from Human Feedback.
*   **Markov Decision Processes (MDP)**
    *   *What it explains*: How decision-making environments can be mathematically formalized where outcomes are partly random and partly under the control of a decision-making agent.
    *   *Connects to*: Reinforcement Learning, Bellman Equations.
*   **Bellman Equations**
    *   *What it explains*: How the value of a decision state can be broken down into the immediate reward plus the discounted value of future states.
    *   *Connects to*: Markov Decision Processes, Reinforcement Learning.
*   **Reinforcement Learning (RL)**
    *   *What it explains*: How an autonomous agent learns to make decisions by performing actions and receiving rewards or penalties within an environment.
    *   *Connects to*: Markov Decision Processes, Reinforcement Learning from Human Feedback.
*   **Reinforcement Learning from Human Feedback (RLHF)**
    *   *What it explains*: How generative models can be aligned with human preferences, safety guidelines, and intent using a reward model trained on human evaluations.
    *   *Connects to*: Reinforcement Learning, Direct Preference Optimisation.
*   **Direct Preference Optimisation (DPO)**
    *   *What it explains*: How language models can be directly optimized for human preferences without training an explicit reward model or using complex reinforcement learning loops.
    *   *Connects to*: Reinforcement Learning from Human Feedback, Pre-training and Fine-tuning.
*   **Variational Autoencoders (VAEs)**
    *   *What it explains*: How high-dimensional data can be mapped to a continuous, probabilistic latent space to generate new, similar data points.
    *   *Connects to*: Unsupervised Learning, Encoder-Decoder Structure.
*   **Generative Adversarial Networks (GANs)**
    *   *What it explains*: How realistic data can be generated through a zero-sum game between a generator network and a discriminator network.
    *   *Connects to*: Variational Autoencoders, Diffusion Processes.
*   **Diffusion Processes**
    *   *What it explains*: How data can be generated by systematically reversing a gradual noise-addition process.
    *   *Connects to*: Generative Adversarial Networks, Multimodal AI.
*   **Contrastive Learning**
    *   *What it explains*: How models learn to align representations of different modalities (e.g., text and images) by bringing positive pairs closer and pushing negative pairs apart in a shared vector space.
    *   *Connects to*: Multimodal AI, Vector Embeddings.
*   **Multimodal AI**
    *   *What it explains*: How systems process, align, and generate information across multiple distinct modalities, such as text, images, and audio.
    *   *Connects to*: Contrastive Learning, Diffusion Processes.
*   **Retrieval-Augmented Generation (RAG)**
    *   *What it explains*: How generative models can access external, dynamic knowledge bases to improve factual accuracy and reduce hallucinations without retraining.
    *   *Connects to*: Vector Embeddings, Transformer Architecture.
*   **Vector Embeddings**
    *   *What it explains*: How discrete semantic concepts (words, images, documents) can be represented as continuous, low-dimensional vectors in a geometric space where distance correlates with semantic similarity.
    *   *Connects to*: Retrieval-Augmented Generation, Contrastive Learning.
*   **Multi-Agent Systems**
    *   *What it explains*: How multiple autonomous computational entities can interact, communicate, and coordinate to solve complex tasks that exceed the capabilities of a single agent.
    *   *Connects to*: Autonomous Agents, Reinforcement Learning.
*   **Autonomous Agents**
    *   *What it explains*: How a language model can use reasoning, planning, and tool execution to autonomously complete open-ended goals.
    *   *Connects to*: Multi-Agent Systems, Retrieval-Augmented Generation.
*   **Multi-Agent Reinforcement Learning** *(surface-level)*
    *   *What it explains*: How multiple learning agents can simultaneously optimize their policies in a shared, dynamic environment.
    *   *Connects to*: Multi-Agent Systems, Reinforcement Learning.

## 3. Principles & Abstractions

*   **Representation via Latent Vector Spaces**
    *   *Principle*: Complex, high-dimensional real-world data (text, images, audio) can be mapped into continuous, lower-dimensional vector spaces where geometric proximity corresponds to semantic similarity.
    *   *Structural Importance*: This principle is the foundation of modern AI representation. Without it, models cannot perform semantic search, align different modalities (like text and images), or compress data for generation. It makes the mathematical manipulation of meaning predictable and computable.
*   **Attention-Driven Contextualization**
    *   *Principle*: The meaning of any individual element in a sequence is dynamic and defined entirely by its relationship to all other elements in its context, calculated via parallelized weighting mechanisms.
    *   *Structural Importance*: This principle replaces sequential processing with parallelized, global context calculation. Without it, long-range dependencies break, training cannot scale to massive datasets, and modern large language models become computationally intractable.
*   **Alignment via Preference Optimization**
    *   *Principle*: Raw statistical next-token prediction models must be explicitly steered using human preference feedback loops to ensure utility, safety, and instruction-following behavior.
    *   *Structural Importance*: This principle bridges the gap between raw pattern matching and functional, safe utility. Without it, generative models remain unpredictable, prone to hallucination, and unsafe for public or enterprise deployment.
*   **Iterative Refinement over Single-Step Generation**
    *   *Principle*: High-fidelity generation of complex data (such as images or multi-step plans) is best achieved through iterative, step-by-step denoising or reasoning processes rather than single-pass predictions.
    *   *Structural Importance*: This principle underpins both diffusion models (which generate images by gradually removing noise) and autonomous agents (which plan and execute iteratively). Without it, generative outputs suffer from low fidelity, lack of structural coherence, and high error rates.
*   **Modular Orchestration and Externalization**
    *   *Principle*: The capabilities of generative models are exponentially multiplied when they are decoupled from static weights and allowed to interact with external tools, databases, and other specialized models.
    *   *Structural Importance*: This principle governs RAG and multi-agent architectures. It solves the fundamental limitation of static model knowledge, making systems dynamic, verifiable, and capable of executing complex, real-world workflows.

## 4. Key Takeaways & Learning Points

1.  **Shift from API Consumption to Architectural Engineering**: Practitioners must move beyond treating generative models as black-box APIs and instead master the underlying mechanics (attention, embeddings, fine-tuning) to diagnose failures, optimize performance, and build custom solutions.
2.  **Prioritize Retrieval over Retraining for Dynamic Knowledge**: When building enterprise applications, use Retrieval-Augmented Generation (RAG) to ground models in dynamic, domain-specific data rather than attempting to bake that knowledge directly into model weights via expensive pre-training or fine-tuning.
3.  **Design for Iterative Alignment, Not Just Raw Capability**: Building a useful AI system requires continuous alignment strategies (like RLHF or DPO) to shape model behavior, meaning developers must design evaluation and feedback loops into their deployment pipelines from day one.
4.  **Deconstruct Complex Tasks into Multi-Agent Workflows**: Instead of forcing a single, massive prompt or model to handle an entire complex workflow, decompose the problem into a network of specialized, autonomous agents with clear communication protocols and defined boundaries.
5.  **Evaluate Generative Models through a Probabilistic Lens**: Because generative architectures (VAEs, GANs, Diffusion, LLMs) operate on probabilistic distributions rather than deterministic rules, testing and validation must shift from binary assertions to statistical evaluation frameworks.

## 5. Notable References

### Works & Models
*   **BERT**: Cited as a dominant family of pre-trained language models to study encoder-based architectures, pre-training, and fine-tuning procedures.
*   **GPT**: Cited as a dominant family of pre-trained language models to study decoder-based architectures and autoregressive generation.
*   **DALL-E**: Cited as a primary text-to-image multimodal architecture used to study image generation and prompt engineering.
*   **Stable Diffusion**: Cited as a primary text-to-image multimodal architecture used to study diffusion processes and fine-tuning for specialized tasks.
*   **CLIP**: Cited to explain how Transformer architectures are adapted for computer vision and cross-modal alignment.
*   **Vision Transformers (ViT)**: Cited to demonstrate how self-attention mechanisms can be applied directly to image patches for computer vision tasks.

### Tools & Frameworks
*   **TensorFlow & Keras**: Cited as the primary deep learning frameworks used to teach learners how to build and train neural networks.
*   **Hugging Face**: Cited as the industry-standard ecosystem utilized for accessing, training, and deploying pre-trained transformer models.
*   **LangChain**: Cited as the core orchestration framework used to teach learners how to build conversational AI, chains, and RAG pipelines.
*   **Runway**: Cited as an industry tool used to provide hands-on exposure to generative media and image/video synthesis.
*   **Kaggle**: Cited as an industry platform used within the course for hands-on machine learning practice and competitive learning.

### Organisations
*   **NUS School of Computing (SoC)**: Cited as the academic institution designing, delivering, and certifying the technical curriculum.
*   **Emeritus**: Cited as the collaborative digital learning platform partner responsible for hosting and delivering the course.

### Events & Dates
*   **14-week online course duration**: Cited to define the temporal scope and intensity of the technical training program.
*   **12 months of post-completion access**: Cited to specify the duration of ongoing learning support and resource availability for graduates.

## 6. Coverage & Gaps

### What the Source Covers Well
The curriculum provides an exceptionally comprehensive, end-to-end technical roadmap. It covers the mathematical and structural evolution of deep learning, starting from basic Python and classical machine learning, moving through deep neural networks, and culminating in advanced transformer architectures, reinforcement learning (RLHF/DPO), and multi-agent systems. The inclusion of both text (LLMs, RAG) and vision (VAEs, GANs, Diffusion, ViT, CLIP) domains is highly robust.

### What is Surface-Level or Underexplained
Several highly complex topics are compressed into single-week modules, suggesting they are treated at a surface level. Specifically, **multi-agent reinforcement learning** is a notoriously difficult academic field that cannot be mastered in a sub-module. Similarly, **performance optimization** for both transformers and diffusion models is mentioned but likely lacks the depth required for production-level infrastructure engineering (e.g., quantization, distributed training, hardware acceleration).

### What is Absent
The document is virtually silent on the operational and infrastructure side of generative AI, commonly known as **LLMOps** or **FMOps**. There is no mention of model serving infrastructure (e.g., vLLM, Triton Inference Server), vector database selection and scaling (e.g., Pinecone, Milvus, Qdrant), or continuous monitoring for drift and evaluation (e.g., Ragas, TruLens). Additionally, while "AI ethics" is mentioned, there is no discussion of the legal and copyright frameworks currently challenging generative AI training data practices, which is a critical gap for enterprise practitioners.

### Perspective or Bias
The curriculum exhibits an academic-technical bias, originating from a top-tier university (NUS). It assumes that the optimal path to utilizing generative AI is to understand its low-level mathematical and architectural foundations (e.g., writing neural networks from scratch in TensorFlow/Keras). A critic or industry pragmatist might argue that this bottom-up approach is inefficient for most professionals, who would benefit far more from a top-down focus on system design, API orchestration, prompt engineering, and business integration, rather than learning how to implement VAEs or write Bellman equations from scratch.

## Source

https://nus.comp.emeritus.org/generative-ai-fundamentals-to-advanced-techniques-programme