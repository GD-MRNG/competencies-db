# Generative AI: Fundamentals to Advanced Techniques — Level 0: Course Map

> **Intent:** To develop genuine technical fluency in how modern generative AI systems are designed, trained, and deployed — not just how to use them. A practitioner with this map understands *why* RLHF works, *what* diffusion is actually doing, and *how* a RAG pipeline differs architecturally from a fine-tuned model.
>
> **Your angle:** You likely already work around AI tools and have absorbed some of the vocabulary. The risk is that surface familiarity masks conceptual gaps that matter when things break or when you need to make real architectural decisions. Treat this map as a way to find those gaps — the topics that feel familiar from the outside but hollow from the inside.

---

## How to use this map

This document is a navigation tool, not a learning resource. Each **Level 1 topic** is an entry point into a coherent area of study — something that warrants a dedicated session or set of readings. Each **Level 2 candidate** beneath it is a sub-concept that repays focused attention: a mechanism, a tradeoff, a historical decision that explains why things are the way they are.

When a Level 1 topic feels hollow — when you could not explain the *tradeoff* it represents or the *problem* it was invented to solve — that is the signal to descend to Level 2. When you could teach a Level 1 topic to a skeptical colleague, move on.

---

## Topic Inventory

---

### Group 1: Computational and Mathematical Foundations

These topics are the prerequisite layer. They are not glamorous but they are load-bearing — confusion here propagates silently into every topic that follows.

---

#### L1-01 · Python for Data and ML Work

The programme uses Python not as a language to master but as a tool for thinking in data. The gap to close is between scripting (writing Python to get things done) and idiomatic ML Python (writing code that composes cleanly with NumPy, Pandas, and framework APIs). Most practitioners underestimate this gap until they try to debug a TensorFlow computation graph.

**Level 2 candidates:**
- **Object-oriented programming in Python** — Understanding classes and instances is what separates people who can read ML framework source code from people who treat it as a black box.
- **Pandas data manipulation** — The mental model of vectorised operations over DataFrames is non-obvious and explains most performance surprises in data preprocessing.
- **Matplotlib and visualisation** — Knowing how to quickly plot a loss curve or a confusion matrix during training is a practical debugging skill, not decoration.
- **Exception handling and Python execution model** — Understanding what happens when a line fails inside a training loop explains why errors in ML code are often cryptic and why defensive coding matters.

---

#### L1-02 · Machine Learning Fundamentals

Machine learning is the conceptual substrate that everything else in this programme builds on. Before transformers, before GANs, before RLHF, there is a core set of ideas: that a model is a parameterised function, that training is optimisation over a loss surface, and that the train/validation/test split exists because of a specific failure mode called overfitting. These ideas never go away — they just get more complicated.

**Level 2 candidates:**
- **Supervised vs unsupervised learning** — The distinction is not just a taxonomy; it determines what you can learn from data without labels, and labels are expensive, which is why unsupervised pre-training became so central to modern LLMs.
- **K-means clustering** — A simple enough algorithm to understand completely, and understanding it fully (convergence, sensitivity to initialisation, the curse of dimensionality) builds the intuition needed for more complex clustering used in embedding spaces.
- **Linear regression and loss functions** — The MSE loss and its gradient are the simplest case of the idea that runs through all of deep learning; getting this right in detail pays dividends everywhere else.
- **K-nearest neighbours classification** — KNN's failure modes at scale motivate why parametric models exist — this is the historical problem that regression and neural networks were invented to solve.
- **Bias-variance tradeoff** — The organising principle behind regularisation, dropout, and model selection; missing this makes hyperparameter tuning feel arbitrary.

---

### Group 2: Neural Networks and the Deep Learning Toolkit

This group covers the core architectural ideas of deep learning — from the original perceptron through to the convolutional and recurrent models that preceded transformers. These are not obsolete; CNNs are still used in production vision systems, and understanding what they cannot do is what makes the transformer's design decisions legible.

---

#### L1-03 · Artificial Neural Networks

The ANN is where the field's conceptual vocabulary was established. Weights, activations, backpropagation, gradient descent, epochs, learning rate — all of it originates here. The reason to study ANNs carefully rather than skipping to deep learning is that the failure modes of deep models are almost always classical ANN problems at scale: vanishing gradients, overfitting, data hunger.

**Level 2 candidates:**
- **Backpropagation** — The chain rule applied to a computation graph; understanding this is what separates someone who can train a model from someone who can debug why training has stalled.
- **Activation functions (ReLU, sigmoid, tanh)** — Each was invented to solve a specific problem with its predecessor; the history of activations is a history of understanding the vanishing gradient.
- **Gradient descent variants (SGD, Adam)** — Adam is almost universally used in practice, but understanding why SGD sometimes generalises better reveals something important about loss landscape geometry.
- **Overfitting, regularisation, and dropout** — The most practically consequential set of techniques in ML; dropout in particular looks strange until you understand the ensemble interpretation.

---

#### L1-04 · Deep Convolutional Neural Networks

The DCNN was the first architecture to demonstrate that raw performance on hard perceptual tasks was achievable by learning hierarchical representations from data. AlexNet in 2012 is the historical anchor: it won ImageNet by a margin that forced the field to take deep learning seriously. Understanding DCNNs explains why spatial locality and parameter sharing matter — and why they are not the right inductive bias for language.

**Level 2 candidates:**
- **Convolutional layers and receptive fields** — The core insight is that nearby pixels are correlated and share structure; following this reasoning to its limit reveals why convolutions fail on long-range dependencies.
- **Pooling and translation invariance** — Pooling is a deliberate information-discarding step; understanding what is discarded and why it helps explains a tradeoff that reappears in vision transformers.
- **Transfer learning with pre-trained CNNs** — The discovery that ImageNet features transfer to unrelated vision tasks was a paradigm shift; the same logic underlies BERT-style pre-training for language.
- **DCNN for tabular vs image data** — Applying a spatial architecture to non-spatial data is a category error that produces subtle failures; knowing when convolutions are and are not appropriate is a core modelling skill.

---

### Group 3: The Transformer Revolution

This group is the heart of the programme. The transformer (Vaswani et al., 2017) is the architectural idea that unified NLP, vision, speech, and ultimately generation. Every topic downstream — BERT, GPT, diffusion conditioning, multimodal models — is a transformer with modifications. Understanding the transformer deeply is the highest-leverage investment in this curriculum.

---

#### L1-05 · Transformer Architecture and Attention Mechanisms

The transformer was invented to solve a problem that RNNs could not: processing sequences in parallel while still modelling long-range dependencies. The solution — replacing recurrence with self-attention — turned out to be general enough to work on images, audio, protein sequences, and code. The attention mechanism is not an opaque operation; it has a clean mathematical interpretation as a learned weighted average, and getting that interpretation right is what makes everything downstream comprehensible.

**Level 2 candidates:**
- **Self-attention as query-key-value** — The QKV formulation is the mechanism; understanding it as a soft dictionary lookup (every token queries every other token and retrieves a weighted mixture of their values) is the intuition that makes attention feel principled rather than magical.
- **Multi-head attention** — Multiple attention heads allow the model to attend to different aspects of the input simultaneously; the interesting question is what different heads actually learn to attend to, which connects to interpretability.
- **Positional encoding** — Transformers have no inherent notion of order; positional encoding is the patch, and its design choices (sinusoidal vs learned vs rotary) have real consequences for handling long sequences.
- **Encoder-decoder vs encoder-only vs decoder-only** — This architectural fork produces BERT-style models (encoder-only, bidirectional), GPT-style models (decoder-only, autoregressive), and T5-style models (encoder-decoder); knowing which to reach for and why is a core design skill.
- **Feedforward sublayers** — The FFN in each transformer block is where most of the model's raw parameter count lives; recent interpretability work suggests it acts as a key-value memory, which changes how you think about what transformers store.
- **Training dynamics: data preparation and training strategies** — Curriculum learning, warmup schedules, and gradient clipping are not incidental details; they explain why large models train at all.

---

#### L1-06 · BERT and GPT: Pre-trained Language Models

BERT (Devlin et al., 2018) and GPT (Radford et al., 2018) were trained within months of each other and established the two dominant paradigms for applying transformers to language. BERT's masked language modelling objective produces rich bidirectional representations suited to understanding tasks. GPT's causal language modelling objective produces models that can generate fluently. Understanding both is necessary because the choice of pre-training objective determines almost everything about what a model is good at and what it cannot do.

**Level 2 candidates:**
- **Masked language modelling (MLM)** — BERT's pre-training objective; it forces the model to develop bidirectional context, which is why BERT representations are so useful for classification but cannot generate text.
- **Causal language modelling (CLM)** — GPT's objective; the model only sees leftward context, which is a constraint that turns out to be sufficient for remarkably general capability.
- **Fine-tuning vs prompting** — Fine-tuning modifies weights; prompting modifies input; understanding the tradeoffs (data cost, generality, latency, cost) is central to deploying these models in practice.
- **BERT applications: classification, NER, QA** — The canonical downstream tasks reveal what bidirectional representations are particularly good at and where they hit limits.
- **GPT scaling behaviour** — The empirical observation that GPT-family models exhibit emergent capabilities at scale (few-shot learning, chain-of-thought reasoning) was not predicted theoretically; understanding when and why emergence happens is an open question with real practical stakes.
- **Model combinations and extensions** — RoBERTa, DistilBERT, T5, and others fix specific weaknesses in BERT or GPT; tracing these lineages is how you learn to read a new model's paper critically.

---

### Group 4: Generative Modelling

This group covers the specific architectural families used to generate new data — images, text, audio, video. Each family (VAEs, GANs, diffusion models, autoregressive LMs) represents a different mathematical formulation of the generation problem and a different set of tradeoffs between sample quality, diversity, training stability, and computational cost. Reinforcement learning for human feedback is included here because its primary application is fine-tuning generative models to align with human preferences.

---

#### L1-07 · Reinforcement Learning for Generative AI

Reinforcement learning arrived in the generative AI conversation through a specific application: RLHF, the technique used to fine-tune GPT-3 into InstructGPT (and subsequently ChatGPT) to follow instructions and refuse harmful requests. RL is a rich field in its own right, but the reason to study it here is primarily to understand how human preference data is used to shape generative model behaviour — and what the tradeoffs of that approach are.

**Level 2 candidates:**
- **Markov Decision Processes** — The formal framework for sequential decision-making; understanding MDPs is what makes RL feel principled rather than a bag of tricks.
- **Policy gradient methods (PPO)** — PPO is the specific algorithm used in most RLHF pipelines; it is complex enough that understanding it at the level of "what is being optimised and why this objective" is more valuable than implementation details.
- **Reinforcement Learning from Human Feedback (RLHF)** — The three-stage pipeline (supervised fine-tuning → reward model training → RL optimisation) is the practical technique that made ChatGPT possible; tracing each stage reveals the failure modes that motivated DPO.
- **Direct Preference Optimisation (DPO)** — DPO was published in 2023 as a simpler alternative to RLHF that achieves similar alignment without a separate reward model; understanding why it works requires understanding what RLHF's reward model was actually learning.
- **Reward hacking and alignment failure modes** — The practical limitation of RLHF is that models learn to game the reward model rather than satisfy the underlying human intent; this is the entry point into the alignment problem.

---

#### L1-08 · Variational Autoencoders and GANs

VAEs (Kingma and Welling, 2013) and GANs (Goodfellow et al., 2014) are the two foundational families of generative models for images. They are now largely superseded by diffusion models for image quality, but studying them is not historical exercise — VAEs appear inside diffusion models (Stable Diffusion uses a VAE to compress into latent space), and GANs are still used in applications where speed of sampling matters. More importantly, understanding *why* GANs are hard to train and *what* VAEs are actually approximating builds the mathematical intuition that makes diffusion models comprehensible.

**Level 2 candidates:**
- **Autoencoders and latent representations** — The concept of a bottleneck that forces the model to compress and reconstruct is the ancestor of representation learning; every generative model has some version of this.
- **VAE reparameterisation trick** — The mathematical sleight of hand that makes VAEs trainable by gradient descent; understanding it reveals the tension between reconstruction quality and latent space regularity.
- **GAN training dynamics and mode collapse** — The adversarial training loop is unstable in ways that are well-understood; mode collapse (the generator finds a small set of outputs that fool the discriminator) is the canonical failure mode and motivates many GAN variants.
- **Conditional generation** — Conditioning a GAN or VAE on a class label or text prompt is the step that makes these models useful; it also introduces a new set of tradeoffs between conditioning fidelity and sample diversity.

---

#### L1-09 · Diffusion Models

Diffusion models (Ho et al., 2020, building on earlier score matching work) are now the dominant approach for high-quality image generation. The core idea — gradually add noise to data, then train a model to reverse the process — was inspired by non-equilibrium thermodynamics and turns out to produce far more stable training than GANs. DALL-E 2, Stable Diffusion, and Midjourney all use diffusion at their core.

**Level 2 candidates:**
- **Forward and reverse diffusion processes** — The mathematical formulation of "destroy information gradually, then learn to restore it" is what separates diffusion from VAEs and GANs; the forward process is a fixed Markov chain, and the reverse is learned.
- **U-Net architecture for denoising** — The specific neural network used to predict noise at each step; the U-Net's skip connections are critical and explain why spatial structure is preserved through generation.
- **Classifier-free guidance** — The technique that allows a single model to operate with or without a conditioning signal at inference time; it is what makes prompt-following controllable without a separate classifier.
- **Latent diffusion (LDM)** — Running diffusion in the compressed latent space of a VAE rather than in pixel space is what made high-resolution diffusion tractable; this is the architecture of Stable Diffusion.
- **Sampling methods (DDPM vs DDIM)** — DDPM requires hundreds of denoising steps; DDIM reduces this to tens via a deterministic process; the tradeoff between speed and sample diversity is practically important.

---

### Group 5: Applied Generative AI Systems

This group covers how generative models are combined, conditioned, and deployed to solve real problems. The architectural ideas are largely from Groups 3 and 4; what is new here is the system-level thinking — how models are connected, how prompts are engineered, how retrieval augments generation, and how multiple agents coordinate.

---

#### L1-10 · Vision Transformers and CLIP

The Vision Transformer (Dosovitskiy et al., 2020) demonstrated that the transformer architecture works for images with minimal modification, by treating an image as a sequence of patches. CLIP (Radford et al., 2021) went further by training a joint image-text embedding space using contrastive learning on 400 million image-caption pairs. CLIP is now the conditioning backbone for most text-to-image systems — understanding it is required to understand why DALL-E and Stable Diffusion can follow text prompts at all.

**Level 2 candidates:**
- **Patch embedding in ViT** — The conversion of an image into a sequence of flattened patch vectors is the key design choice; its implications for computational cost and inductive bias relative to CNNs are the reason ViT requires more data to train.
- **Contrastive learning objective** — CLIP's training signal comes from making paired image-text embeddings similar and unpaired ones dissimilar; understanding this objective explains why CLIP generalises to zero-shot classification.
- **CLIP as a text encoder for diffusion** — How the text prompt enters a Stable Diffusion pipeline, why CLIP's text encoder shapes generation, and where CLIP's vocabulary gaps create failure modes.
- **Zero-shot transfer from CLIP** — The ability to use CLIP for tasks it was not explicitly trained on (classification, retrieval, generation conditioning) is the paradigm that later generalised to GPT-style models; it is the empirical foundation of the "foundation model" concept.

---

#### L1-11 · Text-to-Image Generation: DALL-E and Stable Diffusion

DALL-E (OpenAI, 2021) and Stable Diffusion (Rombach et al., 2022) are the two most influential text-to-image systems and represent different architectural philosophies: DALL-E leans on autoregressive generation, Stable Diffusion on latent diffusion with open weights. Studying both together clarifies the design choices rather than making them seem arbitrary. Prompt engineering for image generation is a genuine skill with a body of empirical findings.

**Level 2 candidates:**
- **DALL-E's autoregressive image generation** — Treating image tokens like language tokens and generating them sequentially is the approach; its advantage is architectural simplicity, its disadvantage is sampling speed and resolution.
- **Stable Diffusion's architecture in full** — Text encoder (CLIP) → latent diffusion backbone (U-Net with cross-attention) → VAE decoder; tracing data through this pipeline once is the single most clarifying exercise for understanding modern image generation.
- **Prompt engineering for image generation** — The empirical regularities of what prompts produce what results are a practical craft; understanding *why* certain prompt structures work (e.g. style modifiers, aspect ratios, negative prompts) requires understanding how the conditioning enters the model.
- **Fine-tuning: DreamBooth and LoRA** — Methods for personalising diffusion models to generate specific subjects or styles; understanding them requires understanding what fine-tuning actually modifies about a pre-trained model's weights.
- **Ethical considerations and misuse vectors** — The specific ways text-to-image systems can produce harmful content, and why technical mitigations (NSFW filters, training data curation) are partial solutions, not complete ones.

---

#### L1-12 · LLMs in Applications: LangChain and RAG

Large language models have a fundamental limitation: they cannot access information beyond their training data, and their parametric knowledge cannot be updated cheaply. Retrieval-Augmented Generation (Lewis et al., 2020) addresses this by giving the model access to a retrieved context at inference time. LangChain is the most widely used framework for building LLM-powered applications that incorporate retrieval, memory, tool use, and chaining. This combination — a capable LLM plus a retrieval system — is the dominant architectural pattern for practical LLM deployment in 2024.

**Level 2 candidates:**
- **RAG architecture: retriever + reader** — The two-component design separates finding relevant information from using it; understanding each component's failure modes is necessary to diagnose why a RAG pipeline gives wrong answers.
- **Vector embeddings and similarity search** — The conversion of text into dense vectors and retrieval by cosine similarity is the mechanism; the choice of embedding model determines what semantic relationships are captured.
- **Vector databases (FAISS, Pinecone, Chroma)** — Approximate nearest-neighbour indices make similarity search tractable at scale; understanding the speed/recall tradeoff is essential for production decisions.
- **LangChain chains and agents** — The abstraction of "a chain of LLM calls with optional tool use" is what LangChain formalises; understanding what chains add over raw API calls reveals both the power and the debugging overhead.
- **Context window management** — LLMs have fixed context limits; strategies for fitting retrieved documents, conversation history, and instructions into context are practical engineering problems with real accuracy consequences.

---

#### L1-13 · Multi-Agent Systems with LLMs

A single LLM call is a tool. A network of LLM agents that decompose tasks, specialise, communicate, and check each other's work is a system — and a different set of design problems. Multi-agent LLM systems (AutoGPT, CrewAI, and similar frameworks, 2023-2024) represent an early but rapidly developing area where coordination failures, prompt injection, and error propagation are the primary engineering concerns rather than model capability per se.

**Level 2 candidates:**
- **Task decomposition and planning** — The strategy of breaking a complex task into sub-tasks and assigning them to specialised agents; the failure mode is that planning and execution errors compound, and the success condition (verifiable completion) is often ill-defined.
- **Agent communication protocols** — How agents pass messages, share state, and coordinate; the design choices here determine whether multi-agent systems are robust or brittle.
- **Multi-agent reinforcement learning (MARL)** — The formal framework for agents that learn to cooperate or compete; it is theoretically deep and practically relevant to understanding how emergent coordination behaviours arise.
- **LLMs as planners vs executors** — The architectural question of whether an LLM should plan and delegate or plan and execute is a live research question; the tradeoffs involve latency, error propagation, and oversight.
- **Security and prompt injection in agentic systems** — When an LLM agent can take actions in the world, adversarial inputs in the environment (malicious web pages, documents) can hijack its behaviour; this is the primary safety concern unique to agentic deployments.

---

## Sequencing Note

The dependency chain is genuine and should be respected. Group 1 (Python, ML fundamentals) is the prerequisite for everything else — not because the later topics require Python fluency, but because the ML mental model (loss function, optimisation, generalisation) is the vocabulary used in every subsequent discussion. Skipping it produces practitioners who can use models but cannot reason about why they fail.

Group 2 (neural networks, DCNNs) is the bridge from classical ML to deep learning. For a practitioner who has worked with ML but not deep learning, this is often where the most significant conceptual gaps live — particularly around backpropagation and why deep networks are hard to train.

Group 3 (transformers) is the highest-leverage group in the curriculum. Everything in Groups 4 and 5 either *is* a transformer with modifications or *uses* a transformer as a component. The single highest-leverage entry point for a practitioner returning to foundations is **L1-05** (attention mechanisms) — getting this right unlocks the rest. If time is constrained, L1-05 and L1-06 (BERT/GPT) should be prioritised before anything in Groups 4 or 5.

Group 4 (generative modelling) has internal dependencies: VAEs/GANs (L1-08) before diffusion (L1-09), since latent diffusion uses a VAE. RLHF (L1-07) can be studied in parallel with the image generation sequence, as it depends on the transformer foundations (Group 3) but not on image generation specifically.

Group 5 (applied systems) is the least foundationally dependent and the most practically oriented. L1-12 (RAG) and L1-13 (multi-agent) can be approached once Group 3 is solid. L1-10 (ViT/CLIP) and L1-11 (DALL-E/Stable Diffusion) require Group 4 as well.
