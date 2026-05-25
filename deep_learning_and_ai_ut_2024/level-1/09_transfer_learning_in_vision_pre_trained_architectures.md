## Metadata
- **Date:** 26-05-2026
- **Source:** 09_transfer_learning_in_vision_pre_trained_architectures.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-09 · Transfer Learning in Vision: Pre-trained Architectures

The single most important fact about computer vision in 2026 is that you almost certainly will not train a model from scratch. The interesting question is not "how do I design a CNN for my problem?" — it is "which pre-trained model do I start from, and how much of it do I touch?" If you internalize this shift, half the decisions about a vision project make themselves. If you don't, you will burn weeks training a model that a fine-tuned ResNet would have beaten in an afternoon.

The reason transfer learning works is mundane and worth saying out loud. A network trained on ImageNet has seen roughly a million images across a thousand categories. In learning to tell a beagle from a basset hound, it had to learn edges, then textures, then parts, then objects — a hierarchy of visual primitives that is not specific to dogs. Those early and middle layers are doing generic visual work. When you point that network at your problem — defects on a circuit board, species of plankton, retail products on a shelf — the lower layers already know what an edge is. You are not teaching vision from zero; you are reusing vision and teaching specificity. This is why ImageNet weights are a commodity. They are the visual equivalent of a standard library.

The architectures you will encounter form a small, well-worn menu. ResNet is the workhorse: a residual network whose skip connections made it possible to train very deep models without the gradient pathologies that plagued earlier architectures. It is simple, well-understood, and a sensible default when you have no opinion. EfficientNet is what you reach for when you care about the trade-off between accuracy and compute — it scales depth, width, and input resolution together in a principled way, and it tends to give you more accuracy per FLOP than ResNet at a comparable size. DenseNet, with its feature reuse via concatenation rather than addition, is the third commonly seen CNN family. None of these are wrong choices; the differences mostly matter at the margins.

The bigger architectural shift is the Vision Transformer. ViTs treat an image as a sequence of patches and apply the same self-attention machinery that powers language models. They were initially data-hungry — pure ViTs underperform CNNs when pre-trained only on ImageNet — but with larger pre-training datasets they match or exceed CNN performance, and they share an architectural lineage with the rest of modern deep learning. In 2026, ViTs are competitive defaults, especially when you have access to large pre-trained checkpoints. The practical implication is that "the pre-trained vision model" is no longer synonymous with "a CNN."

The strategic choice you actually have to make is not which architecture, but how much of it to fine-tune. There are two ends of a spectrum and the answer is almost always somewhere on it. At one end, you freeze the entire pre-trained backbone and train only a new classifier head on top. This treats the pre-trained model as a fixed feature extractor and is the right move when your dataset is small — a few hundred to a few thousand labeled examples. You are not going to teach a 25-million-parameter network anything useful with a thousand images; you will only overfit it. At the other end, you fine-tune everything end-to-end, usually with a small learning rate so you do not destroy the pre-trained weights you are trying to leverage. This works when you have enough labeled data to support it — tens of thousands of examples and up. Most real projects sit in between: freeze the early layers (the generic edge and texture detectors), fine-tune the later ones (the more task-specific feature combinations), and train the head from scratch.

The case where transfer learning quietly fails is the case where ImageNet is not actually relevant to your problem. ImageNet is photographs of natural objects, mostly centered, mostly well-lit. If your problem is medical imaging, satellite imagery, microscopy, document scans, or industrial inspection, the visual primitives you need are different — different textures, different scales, different color statistics, different notions of what "an object" even means. A pre-trained ResNet still helps a little (edges are edges), but the gain is much smaller, and you may need domain-specific pre-training, far more labeled data, or self-supervised pre-training on your own unlabeled data to get acceptable performance. Recognizing this case early saves you from the frustration of fine-tuning that mysteriously refuses to converge to anything good. The other failure mode is fine-grained classification — telling apart bird species, plant varieties, or specific product SKUs — where ImageNet's category structure is too coarse to have taught useful discriminative features, and you simply need more data.

The skill this topic builds is a kind of triage. Given a vision problem, you should be able to answer in a few minutes: what pre-trained checkpoint do I start from, how much data do I have, how much of the network do I unfreeze, and is my domain close enough to ImageNet that this will work at all? Get those four answers right and the rest is mostly engineering. Get them wrong and no amount of clever architecture will save you.

## Level 2 candidates

**ImageNet pre-trained weights and their utility** — What ImageNet features actually capture at each layer of the network, and why they transfer well to visual tasks that have nothing to do with the original thousand categories. Worth a deep dive because the intuition for what transfers and what doesn't is the foundation for every fine-tuning decision you'll make.

**Common architectures: ResNet, DenseNet, EfficientNet** — The specific design choices each family makes — residual addition versus dense concatenation, compound scaling versus uniform depth — and the practical trade-offs in accuracy, parameter count, and inference speed. Worth deeper treatment because choosing among them is a recurring decision and the differences are non-obvious without seeing the architectures side by side.

**Vision Transformers (ViTs)** — How patch embeddings, positional encodings, and self-attention combine to process images without convolutions, and the data and compute regimes in which ViTs outperform CNNs. Worth its own post because the mechanics differ enough from CNNs that the analogies break, and ViTs are the architectural direction the field is heading.

**Fine-tuning strategies: frozen backbone vs. end-to-end** — The full spectrum of options between "train the head only" and "fine-tune everything," including layer-wise learning rate schedules, gradual unfreezing, and discriminative fine-tuning. Worth deeper coverage because this is the decision that most directly determines whether your fine-tuning run produces a useful model or an overfitted one.

**Domain shift and when transfer learning fails** — The specific domains where ImageNet pre-training doesn't transfer well (medical, satellite, microscopy, fine-grained classification) and the alternatives: domain-specific pre-training, self-supervised pre-training on unlabeled in-domain data, and synthetic data. Worth a deep dive because recognizing this case is what separates practitioners who ship from practitioners who spend a quarter wondering why their loss isn't going down.

---

## Original Content

#### L1-09 · Transfer Learning in Vision: Pre-trained Architectures

Training a CNN on ImageNet from scratch would take weeks on modern hardware. Instead, you use a model pre-trained on ImageNet (or another large dataset), then fine-tune on your task. In 2026, this is the default. ImageNet pre-trained weights are a commodity. You need to know what architectures are available (ResNet, EfficientNet, Vision Transformers), how to fine-tune them, and when a pre-trained model is overkill (fine-grained visual tasks need more data than ImageNet provides).