## Metadata
- **Date:** 26-05-2026
- **Source:** 01_neural_network_architecture_and_training.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-01 · Neural Network Architecture and Training

The most common mistake in deep learning is treating a neural network like a black box you train. You feed it data, it spits out predictions, and when something goes wrong you reach for more data or a bigger model. That instinct is wrong, and it is expensive. A neural network is not a black box — it is a stack of simple operations whose behaviour during training is governed by a small number of design choices that interact in unforgiving ways. Understanding those choices is the difference between a model that converges in an afternoon and one that wastes a week of GPU time and still doesn't learn.

Start with the mental model. A neural network is a function approximator: a parameterised function that maps inputs to outputs, where the parameters (weights) are learned from data. The learning procedure is gradient descent on a loss function. You compute how wrong the network is, compute how each weight contributed to that wrongness (via backpropagation), and nudge each weight in the direction that reduces the error. Repeat across millions of examples. That is the entire game. Everything else — every architectural choice, every hyperparameter, every clever trick — exists to make that loop work in practice, because in practice it is fragile.

The fragility comes from depth. A single-layer network is mostly well-behaved; you can train it with naive choices and it will probably converge. A fifty-layer network is a different animal. Gradients have to flow backward through every layer, and small numerical issues compound. Activations can saturate, gradients can vanish or explode, and the optimisation landscape gets pathological. Most of what you need to know about training deep networks is really about controlling these compounding effects.

Four design choices dominate. Initialisation sets the starting point: weights that are too small produce vanishing gradients (the network learns nothing), weights that are too large produce explosions (the network diverges). Modern initialisation schemes (Xavier, He) scale the initial weights based on layer width, which is unglamorous but essential. Activation functions determine what each neuron computes; ReLU dominates because it is cheap and doesn't saturate for positive inputs, but it has its own pathology (dying neurons whose gradients are permanently zero), which is why alternatives like GELU show up in Transformers. Learning rate controls how big each gradient step is — too high and you bounce around or diverge, too low and training takes forever. This is the single hyperparameter most worth tuning, and modern optimisers like Adam adapt it per-parameter so you don't have to be perfect. Depth gives the network capacity to represent complex functions, but each additional layer makes optimisation harder; tricks like batch normalisation and residual connections exist precisely to make deep networks trainable at all.

In 2026, you almost never invent a new architecture. The field has converged on a small set of standard ones, each matched to a data type. For tabular data, a multi-layer perceptron — fully connected layers stacked on top of each other — is usually enough, and gradient-boosted trees are often better. For images, convolutional networks dominate because they exploit locality and translation invariance. For sequences (text, audio, time series), Transformers have replaced almost everything else. The reason these architectures won is not aesthetic; it is that their inductive biases match the structure of their data, which means they learn more from less. You should pick the standard architecture that matches your data and spend your effort on tuning it, not on trying to reinvent it.

The real skill is recognising failure modes. A loss that doesn't decrease usually means the learning rate is wrong or the initialisation is broken. A loss that decreases on training data but not validation data means you are overfitting and need regularisation (dropout, weight decay, early stopping) or more data. A loss that decreases briefly then explodes is gradient instability — try gradient clipping, lower the learning rate, or add normalisation. A model that trains fine but performs terribly on real inputs is usually a data problem, not a model problem. None of these are diagnosed by staring at the architecture; they are diagnosed by reading the training curves and knowing what each shape implies.

The practical consequence is that you should treat training a neural network as an engineering discipline with known failure modes, not as alchemy. The hyperparameters that matter most — learning rate, batch size, initialisation scheme, regularisation strength — are well-understood. The architectures that work — MLPs, CNNs, Transformers — are well-documented. What separates practitioners who ship from those who don't is not knowledge of obscure tricks; it is the discipline to debug systematically, to recognise the signature of each failure mode, and to know when to reach for a standard fix rather than invent a new one. Everything else in this course assumes you have this foundation.

## Level 2 candidates

**Activation functions and their properties** — Covers why ReLU dominates (sparse, efficient, no saturation for positive inputs), what dying ReLU is, and when alternatives like GELU and Swish are worth using. Worth a deep dive because the choice of activation interacts subtly with initialisation and normalisation, and the wrong choice silently degrades training.

**Weight initialization and its impact on training** — Covers why random initialisation with the wrong scale prevents learning and what Xavier and He initialisation actually compute. Worth deeper treatment because the math is short, the intuition is powerful, and getting it wrong is one of the most common silent failures in custom architectures.

**Backpropagation and computational graphs** — Covers how gradients flow backward through a network, why vanishing and exploding gradients happen, and what residual connections and batch normalisation do to the gradient flow. Worth depth because every debugging skill in deep learning rests on understanding what the gradient is actually doing.

**Learning rate and optimization algorithms** — Covers why a constant learning rate is naive, how Adam adapts per-parameter learning rates, when SGD with momentum is preferable, and how learning rate schedules (warmup, cosine decay) work. Worth depth because the learning rate is the single most consequential hyperparameter, and the differences between optimisers actually matter at scale.

**Batch normalization and layer normalization** — Covers why normalising activations between layers stabilises training, the mechanical difference between batch and layer norm, and the train/test gotcha (batch norm uses running statistics at inference). Worth depth because layer norm is everywhere in Transformers, batch norm has subtle pitfalls, and most practitioners use them without understanding what they do.

**Regularization: dropout, weight decay, early stopping** — Covers the three standard techniques for preventing overfitting, why dropout acts like a cheap ensemble, and when regularisation is masking a deeper data problem. Worth depth because regularisation choices interact with model capacity and dataset size in non-obvious ways.

**Residual connections and skip connections** — Covers why ResNets enabled training of very deep networks and how identity shortcuts change the optimisation landscape (gradients can flow directly back to early layers). Worth depth because skip connections are now standard in nearly every deep architecture, including Transformers, and the intuition for why they work is non-obvious.

---

## Original Content

#### L1-01 · Neural Network Architecture and Training

A neural network is a function approximator. It learns by adjusting weights to minimize a loss function via gradient descent. Sounds simple. The devil is in the details: initialization matters (random small vs. careful schemes), activation functions matter (ReLU vs. sigmoid), learning rates matter (too high = divergence, too low = glacial), and depth matters (more layers = more capacity but harder to train). In 2026, most practitioners use standard architectures (MLPs for tabular data, CNNs for vision, Transformers for sequences) rather than inventing new ones. You need to understand why these standard architectures work, how to tune them, and when they fail.