# Deep Learning & Generative AI — Level 0: Course Map

> **Intent:** To move from understanding neural networks to building, training, and deploying models that solve specific problems—and knowing which tool to reach for when.
>
> **Your angle:** You've seen the 2024 curriculum. It was a sampler platter: a bit of NLP, a bit of vision, a bit of generative AI. By 2026, that approach is outdated. Transformers have won. LLMs are now infrastructure (not research). The real questions are: When do I train from scratch vs. fine-tune a pre-trained model? When is a prompt engineer enough vs. when do I need a real model? How do I actually ship this? This map assumes you understand supervised learning and statistics. You need depth in the tools and architectural choices that matter in 2026.
> 
---

## How to use this map

This map has three levels:

- **Level 0** (you are here): the forest—which clusters matter, and in what order.
- **Level 1**: each major topic—why practitioners care, what becomes possible once you own it.
- **Level 2**: specific techniques and tools—go here when you hit the thing you need to build.

The ordering reflects dependency. Start with neural network foundations, then specialize by data modality (vision, language, multimodal). Then move to building and shipping. You do not need to master all three modalities—pick one based on your work, and use the others as reference.

```
Note: This course was completed in 2024 (Deep Learning with AI, UT Austin McCombs School of Business). The field has moved on. Rather than let these curricula fade, I've generated updated Level 0 maps reflecting what matters in 2026. Use these as starting points only. Keep the maps, not the course materials. The lecture videos and homeworks were for 2023–2024. The maps are timeless—they'll need tweaking every 18 months or so, but the structure holds.
```

---

## Topic Inventory

### Foundations: Neural Networks and Optimization

Everything that follows assumes you understand backpropagation, gradient descent, and why deep networks are hard to train.

#### L1-01 · Neural Network Architecture and Training

A neural network is a function approximator. It learns by adjusting weights to minimize a loss function via gradient descent. Sounds simple. The devil is in the details: initialization matters (random small vs. careful schemes), activation functions matter (ReLU vs. sigmoid), learning rates matter (too high = divergence, too low = glacial), and depth matters (more layers = more capacity but harder to train). In 2026, most practitioners use standard architectures (MLPs for tabular data, CNNs for vision, Transformers for sequences) rather than inventing new ones. You need to understand why these standard architectures work, how to tune them, and when they fail.

**Level 2 candidates:**
- **Activation functions and their properties** — Why ReLU dominates (sparse, efficient), what problems it has (dying ReLU), and when alternatives (GELU, Swish) matter.
- **Weight initialization and its impact on training** — Why random initialization with the wrong scale prevents learning, and what Xavier/He initialization actually do.
- **Backpropagation and computational graphs** — How gradients flow backward, why vanishing gradients plague deep networks, and what tricks (batch norm, residual connections) fix it.
- **Learning rate and optimization algorithms** — Why constant learning rate is naive, how Adam adapts per-parameter learning rates, and when SGD with momentum is better.
- **Batch normalization and layer normalization** — Why normalizing activations between layers stabilizes training, what each does differently, and the gotcha: they work differently at train vs. test time.
- **Regularization: dropout, weight decay, early stopping** — How to prevent overfitting, why dropout is a cheap ensemble, and when regularization hides a deeper problem.
- **Residual connections and skip connections** — Why ResNets enabled very deep networks, and how identity shortcuts change the optimization landscape.

---

#### L1-02 · Convolutional Neural Networks (CNNs) for Vision

Convolution is not magic—it is weight sharing. A learned filter slides across an image, producing a feature map. Stack many filters, and you extract hierarchies of features: edges → textures → shapes → objects. CNNs exploit two properties of images: locality (nearby pixels matter more than distant ones) and translation invariance (a cat looks like a cat whether it's on the left or right). In 2026, you rarely train a CNN from scratch on real data. Transfer learning (Section L1-05) is the default. But you need to understand what a CNN learns at each layer, why pooling and striding matter, and how to interpret failures.

**Level 2 candidates:**
- **Convolution, padding, and strides** — How a filter produces a feature map, what padding does (preserve size vs. lose information), and how stride trades off resolution for speed.
- **Pooling and downsampling** — Why max pooling (robustness to small shifts) often works better than average pooling, and what information you discard.
- **Standard architectures: VGG, ResNet, EfficientNet** — What each architecture prioritizes (VGG: simplicity, ResNet: depth, EfficientNet: efficiency), and when to use each.
- **Visualizing learned features** — How to interpret what each layer learns (early layers detect edges, later layers detect objects), and how to spot when a network is relying on shortcuts.
- **Data augmentation for vision** — Why rotating, cropping, and color-jittering during training improve robustness, and when augmentation is essential (small datasets) vs. optional.
- **Common failure modes** — When CNNs hallucinate objects that aren't there, when they overfit to spurious correlations, and how to debug.

---

#### L1-03 · Recurrent and Sequential Models: LSTM and GRU

Sequences are different. A sequence has order: "the cat sat on the mat" is not the same as "the mat on sat cat the." RNNs process sequences one element at a time, maintaining hidden state that encodes what they've seen so far. LSTMs (Long Short-Term Memory) are RNNs that remember long-range dependencies by learning what to forget. In 2026, pure RNNs are largely obsolete—Transformers (L1-04) handle sequences better. But you need to understand LSTMs because they still appear in older codebases, and the intuition (learning what to remember) is useful. More importantly, you need to recognize when a problem is sequential and needs a sequential model.

**Level 2 candidates:**
- **RNN fundamentals: unrolling and backprop through time** — How an RNN is applied to each timestep, how gradients flow backward through time, and why this is expensive and unstable.
- **Vanishing gradients in RNNs** — Why gradients shrink as they propagate backward through many timesteps, causing RNNs to forget distant context.
- **LSTM cells and gates** — How a forget gate, input gate, and output gate let an LSTM choose what to remember, and why this solves vanishing gradients.
- **GRU: a simpler alternative** — How GRUs reduce the LSTM cell to fewer gates, and why the trade-off (simpler but slightly less expressive) often doesn't matter.
- **Sequence-to-sequence models** — How an encoder RNN reads a sequence, and a decoder RNN writes a sequence, enabling machine translation and summarization.
- **Bidirectional RNNs** — Why processing a sequence forward and backward (reading the whole context before predicting each output) improves accuracy.
- **Common pitfalls: packed sequences, variable length input** — How to handle sequences of different lengths efficiently, and what breaks if you don't.

---

### Language Models: From Embeddings to Transformers

These topics are about how neural networks learn and use language. This is where generative AI lives.

#### L1-04 · Transformers and Attention Mechanisms

Attention is a mechanism that lets a model focus on relevant parts of its input. "What should I pay attention to?" In the sentence "The bank executive washed his hands," the word "his" should attend to "executive," not "bank" or "hands." Attention allows a model to compute similarity between every pair of positions in a sequence, then use those similarities to weight what information to combine. Transformers are stacks of attention layers—no recurrence, just attention. This architecture is parallelizable (good for GPUs), can learn long-range dependencies easily, and has become the foundation of all modern language models. You do not need to implement Transformers from scratch, but you need to understand why they work, what self-attention computes, and how to use pre-trained Transformers.

**Level 2 candidates:**
- **Self-attention: keys, queries, values** — How an input is projected into three representations, similarity is computed between queries and keys, and the result is a weighted sum of values.
- **Multi-head attention** — Why using multiple attention heads in parallel, each learning different patterns, improves expressivity.
- **Positional encodings** — How Transformers encode position (Transformers have no inherent sense of "first," "second," "third"), and why sinusoidal encodings work.
- **Scaled dot-product attention and softmax** — What scaling by √d does (prevents saturation), and how softmax converts similarities to weights.
- **Cross-attention vs. self-attention** — When a model attends to itself vs. when it attends to external context (e.g., an image in vision-language models).
- **Causal masking and autoregressive generation** — How to prevent a language model from "cheating" by looking at future tokens during training, and how this enables one-token-at-a-time generation.
- **Transformer efficiency and variants** — Why full attention is O(n²) (a problem for long documents), and what sparse or linear attention variants trade off.

---

#### L1-05 · Pre-Trained Models and Transfer Learning

Training a language model from scratch is expensive (billions of tokens, months of compute). In 2026, you do not train from scratch. You use a pre-trained model (BERT, GPT-2, LLaMA, etc.) and either: (1) fine-tune it on your task (if you have labeled data), or (2) prompt it directly (if you don't). Transfer learning in language is about moving from generic understanding (learned on Wikipedia and Common Crawl) to specific understanding (your domain, your task). This shift from "train a model for my problem" to "adapt a pre-trained model to my problem" is the biggest change in 2026.

**Level 2 candidates:**
- **Pre-training objectives: MLM, CLM, contrastive** — What "masked language modeling" (BERT) teaches a model (bidirectional context), what "causal language modeling" (GPT) teaches it (predicting the next token), and how contrastive objectives (SimCLR) teach similarity.
- **Fine-tuning strategies and overfitting** — How to adapt a pre-trained model to your task without overfitting (early stopping, learning rate schedules, adapter layers).
- **Adapter modules and parameter-efficient fine-tuning** — Why freezing most of a pre-trained model's weights and training small "adapters" is often better than fine-tuning everything.
- **LoRA and other low-rank adaptation** — How LoRA reduces trainable parameters 100x by learning low-rank updates instead of full weight matrices.
- **Knowledge distillation** — How to compress a large pre-trained model into a smaller one by training the smaller model to mimic the larger one's outputs.
- **Domain-specific vs. task-specific fine-tuning** — When to fine-tune on domain data first (medical texts for medical NLP) before fine-tuning on your specific task.

---

#### L1-06 · Large Language Models (LLMs) and Prompting

Large language models (GPT-4, Claude, LLaMA, Gemini) are Transformers trained on trillions of tokens. They can do things no amount of fine-tuning would teach them: reasoning, few-shot learning, translation, code generation. In 2026, you do not need to understand how GPT-4 works internally—you need to understand how to use it. Prompting is an engineering discipline: how to phrase a question so an LLM answers correctly, how to structure few-shot examples, how to chain LLMs together for complex tasks. This is not magic. It is specification and iteration.

**Level 2 candidates:**
- **Prompt engineering: clarity, examples, constraints** — How to write prompts that produce correct outputs (be specific about format, provide examples, set constraints).
- **Few-shot prompting and in-context learning** — How an LLM can learn to solve a task from a handful of examples in the prompt (not retraining, not fine-tuning—just prompt examples).
- **Chain-of-thought prompting** — Why asking an LLM to "think step by step" often produces better answers than asking for the final answer directly.
- **Prompt templates and retrieval-augmented generation (RAG)** — How to build systems that retrieve relevant documents and pass them to an LLM (so it answers based on your data, not its training data).
- **Structured outputs and parsing** — How to prompt an LLM to return JSON or other structured formats, and how to handle parsing failures gracefully.
- **Hallucinations and factuality** — How LLMs confidently produce false information, why RAG helps, and what other techniques (self-critique, retrieval, verification) mitigate this.
- **Cost and latency optimization** — When to use a large model (accurate but slow and expensive), when to use a smaller model (fast and cheap but less capable), and when to distill or cache.

---

#### L1-07 · Natural Language Processing (NLP) Tasks and Fine-Tuning

Beyond LLMs, there is a range of NLP tasks: classification (sentiment, topic, intent), sequence labeling (named entity recognition, part-of-speech tagging), generation (summarization, translation), and retrieval (information retrieval, semantic search). Some are best solved with fine-tuned models (classification on your data), some with prompting (zero-shot classification with an LLM), some with classical methods (token-level operations). Understanding the landscape of NLP tasks and their solutions is essential.

**Level 2 candidates:**
- **Text classification and sentiment analysis** — How to frame classification as a fine-tuning task, what metrics matter (accuracy? F1? weighted precision?), and when LLM prompting is better than fine-tuning.
- **Named entity recognition (NER) and sequence labeling** — How to fine-tune a model to label tokens rather than whole documents, and why entity recognition is harder than it seems (boundary detection, ambiguity).
- **Semantic similarity and embedding-based retrieval** — How to fine-tune a model to produce useful embeddings (dense vectors that encode meaning), and how to use cosine similarity for retrieval.
- **Abstractive summarization and paraphrasing** — How generation tasks require a different fine-tuning setup (encoder-decoder or decoder-only), and why BLEU and ROUGE scores are imperfect.
- **Machine translation and multilingual models** — How translation differs from other tasks (no single correct answer), and why multilingual pre-trained models (mBERT, XLM-RoBERTa) are useful.
- **Information extraction and relation extraction** — How to extract structured data from unstructured text, and when rule-based methods (regex, pattern matching) complement neural approaches.

---

### Vision and Multimodal: Beyond Text

#### L1-08 · Image Processing and CNN Fundamentals

Images are high-dimensional data: a 1000×1000 RGB image is 3 million numbers. Classical machine learning (logistic regression, random forests) fails because they don't respect the spatial structure of images. CNNs work because they exploit locality and weight sharing. Before using a CNN, you need to understand what an image is, how to preprocess it, and what an augmented dataset looks like. This is foundational.

**Level 2 candidates:**
- **Pixel representation and color spaces** — What RGB, HSV, and grayscale represent, and why converting between color spaces sometimes helps (e.g., HSV for lighting invariance).
- **Image preprocessing: normalization and resizing** — Why subtracting the training set mean and dividing by standard deviation helps training, and what resizing does (and when it hurts).
- **Data augmentation for images** — Why rotating, flipping, cropping, and color-jittering during training improve robustness without collecting more data.
- **Imbalanced datasets in vision** — How image datasets often have class imbalance (1000 images of cats, 10 of platypuses), and why weighted losses or resampling help.
- **Common preprocessing pitfalls** — When normalization is wrong (different per-channel vs. per-image), when augmentation is too aggressive, when resizing introduces artifacts.

---

#### L1-09 · Transfer Learning in Vision: Pre-trained Architectures

Training a CNN on ImageNet from scratch would take weeks on modern hardware. Instead, you use a model pre-trained on ImageNet (or another large dataset), then fine-tune on your task. In 2026, this is the default. ImageNet pre-trained weights are a commodity. You need to know what architectures are available (ResNet, EfficientNet, Vision Transformers), how to fine-tune them, and when a pre-trained model is overkill (fine-grained visual tasks need more data than ImageNet provides).

**Level 2 candidates:**
- **ImageNet pre-trained weights and their utility** — What ImageNet features actually capture, and why they transfer well to unrelated visual tasks.
- **Common architectures: ResNet, DenseNet, EfficientNet** — The trade-offs each makes (ResNet: simple, ResNets: feature reuse, EfficientNet: efficiency across scales), and when to use each.
- **Vision Transformers (ViTs)** — How Transformers (not convolutions) can process images by treating them as sequences of patches, and why they're becoming competitive with CNNs.
- **Fine-tuning strategies: frozen backbone vs. end-to-end** — When to freeze the pre-trained weights and train only the classifier head (small datasets), when to fine-tune all weights (large datasets).
- **Domain shift and when transfer learning fails** — When a pre-trained model doesn't help (medical imaging, satellite imagery), and what to do (domain-specific pre-training, more labeled data).

---

#### L1-10 · Multimodal Models: Vision and Language Together

A model that understands both images and text can answer questions about images ("what is in this picture?"), generate captions, and retrieve images from text descriptions. In 2026, multimodal models (CLIP, GPT-4V, Gemini) are mainstream. They learn a shared embedding space where images and text descriptions cluster together. This is a shift from separate vision and language models to unified models that reason across modalities.

**Level 2 candidates:**
- **Contrastive learning and embedding spaces** — How CLIP learns to pull image-text pairs together and push unrelated pairs apart, without labeled data.
- **Vision-language models: architecture and training** — How a visual encoder and language model are connected (adding a projection layer between them), and how they're trained together.
- **Image captioning and visual question answering** — How to fine-tune a multimodal model to generate descriptions or answer questions about images.
- **Retrieval with multimodal embeddings** — How to index images and text in a shared embedding space, enabling both "find images like this text" and "find text like this image."
- **Hallucinations in multimodal models** — How vision-language models sometimes invent objects or attributes, and why having both modalities doesn't prevent it.

---

### Building and Shipping: From Model to System

#### L1-11 · Model Deployment and Serving

A model that works in a notebook is not useful. Deployment means: (1) choosing a serving environment (API, batch, edge), (2) optimizing for latency and throughput, (3) handling versioning and updates, and (4) monitoring in production. This is where most real-world AI fails. A model that returns predictions is not a deployed model. A model that returns correct predictions, quickly, reliably, and maintains accuracy over time is deployed.

**Level 2 candidates:**
- **Inference optimization: quantization and pruning** — How to reduce model size (quantization: 32-bit floats to 8-bit integers) and speed (pruning: removing unimportant weights) with minimal accuracy loss.
- **Batch vs. online serving** — When to score data on a schedule (batch, cheaper, higher latency), when to score on-demand (online, more expensive, low latency).
- **Model serving frameworks: TensorFlow Serving, Triton, KServe** — How to expose a model as an API that handles batching, versioning, and scaling.
- **API design and latency budgets** — How to structure a prediction API (what inputs, what outputs, what error handling), and what "fast enough" means (100ms? 1s?).
- **Model versioning and A/B testing** — How to deploy two models side-by-side, routing traffic to each, measuring which performs better.
- **Containerization with Docker** — How to package a model and its dependencies so it runs the same on your laptop, in CI/CD, and in production.
- **Edge deployment: TensorFlow Lite, ONNX, CoreML** — How to run models on phones and devices where you can't call a server (offline, low latency, low power).

---

#### L1-12 · Generative Model Applications: RAG, Fine-tuning, and Agents

Generative models (LLMs, image generators) are tools. The art is knowing which tool to reach for. Do you need to retrieve facts from your data? Use RAG. Do you need the model to learn your domain's language? Fine-tune. Do you need the model to accomplish multi-step tasks? Use agents (systems that plan, act, observe, and iterate). In 2026, these patterns are standard.

**Level 2 candidates:**
- **Retrieval-Augmented Generation (RAG)** — How to build systems that retrieve relevant documents from your database and pass them to an LLM, so it answers about your data.
- **RAG implementation: embedding models, vector databases, ranking** — How to index documents into vectors (using an embedding model), retrieve top-k documents, rerank them, and pass them to the LLM.
- **Fine-tuning vs. RAG: when to use each** — When fine-tuning is better (you want the model to learn your domain's reasoning, you have labeled examples), when RAG is better (you want factuality, your data changes).
- **Agents and agentic workflows** — How to build systems where an LLM decides what tools to use (calculator, web search, database), executes those tools, and iterates (ReAct pattern).
- **Function calling and tool use** — How to prompt an LLM to call functions (structured outputs with the function name and arguments), and how to route its decisions to real tools.
- **Long-context windows and retrieval tradeoffs** — Whether to stuff all context into a single long prompt (simpler, more expensive) vs. retrieve selectively (cheaper, requires good ranking).
- **Evaluation of generative outputs** — How to measure if an LLM-generated response is good (BLEU? Human rating? Does it solve the task?), and why automatic metrics are often insufficient.

---

#### L1-13 · Monitoring and Debugging Deep Learning Systems

Production models degrade. Data distribution shifts, users change behavior, and bugs hide in preprocessing. In 2026, monitoring is not optional. You need to know when to retrain, when to investigate, and what actually broke. Debugging a neural network is harder than debugging classical software—the failure modes are subtle (slightly wrong preprocessing, a shifted feature distribution) and hard to localize.

**Level 2 candidates:**
- **Data quality and drift detection** — How to monitor that incoming data still matches training data (same distribution, no missing values, no obvious outliers), and what to do when it doesn't.
- **Model prediction drift** — When a model's predictions change over time (not due to new data, but due to subtle shifts), and why this signals a problem.
- **Concept drift** — When the underlying relationship between features and targets changes (e.g., user preferences shift), and why retraining is the only fix.
- **Logging and instrumentation** — What to log (inputs, predictions, latency, errors), how to store it (databases, data warehouses), and how to query it fast.
- **Automated retraining** — When to retrain (on schedule? on drift? on error rate?), how to validate new models before deployment, and how to rollback if needed.
- **Debugging inference failures** — How to reproduce a bad prediction (requires logging inputs), and what to check (data preprocessing, feature engineering, model weights).

---

## Sequencing Note

**Start here (refresher):**

1. **L1-01 (Neural Network Fundamentals)** — If you remember this, skim it. If not, spend a week understanding backprop, gradient descent, and why deep networks are hard to train. This is your foundation.

2. **L1-04 (Transformers and Attention)** — Transformers have won. Understand attention (keys, queries, values) and why self-attention is powerful. Skip the math details, focus on intuition.

3. **L1-05 (Transfer Learning)** — The revolution of 2026: you don't train from scratch, you fine-tune pre-trained models. This is now the default everywhere.

**Then specialize by data type:**

4. **If your work is mostly text/language:**
   - L1-06 (LLMs and Prompting) — How to use GPT-4, Claude, etc. in production.
   - L1-07 (NLP Tasks) — When to fine-tune vs. prompt, classification, extraction, generation.
   - L1-12 (RAG and Agents) — How to ground LLMs in your data and build multi-step systems.

5. **If your work is mostly images:**
   - L1-08 (Image Processing) — Preprocessing, augmentation, common gotchas.
   - L1-09 (Vision Transfer Learning) — Fine-tuning ImageNet pre-trained models.
   - L1-10 (Multimodal) — Only if your task involves both images and text.

6. **If your work involves both:**
   - L1-10 (Multimodal Models) — CLIP, GPT-4V, and similar.

**Always doing:**

7. **L1-11 (Deployment)** — As soon as you have a model that works, move to deployment. This is where real value lives.

8. **L1-12 (RAG, Fine-tuning, Agents)** — Pick the pattern that matches your problem.

9. **L1-13 (Monitoring)** — Deploy monitoring alongside your model. The two are inseparable.

---

**Highest-leverage path for re-entry:** Neural Network Fundamentals → Transformers → Transfer Learning → (Specialize: LLMs+RAG OR Vision+Transfer) → Deployment → Monitoring. Skip the 2024 curriculum's survey approach. Go deep on what your work actually requires.

**What changed from 2024:**
- **Transformers are not optional** — They're the foundation of everything now (vision, language, multimodal).
- **LLMs and prompting are now core** — Not a research topic, but a production tool you use every day.
- **Transfer learning is the default** — Not an optimization, but the baseline. Training from scratch is rare.
- **Multimodal is mainstream** — Vision and language together is no longer niche.
- **Deployment and monitoring are not afterthoughts** — They are as important as the model.