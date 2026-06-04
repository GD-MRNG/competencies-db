## Metadata
- **Date:** 05-06-2026
- **Source:** 10_model_fine_tuning_baking_behaviour_into_weights.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-10 · Model Fine-Tuning: Baking Behavior into Weights

Most engineers reach for fine-tuning at exactly the wrong moment. They have a model that's making mistakes, they've heard fine-tuning is how you "customize" a model, and they assume the path forward is to gather some examples and train. What they actually need, nine times out of ten, is a better prompt or a retrieval pipeline. Fine-tuning is not the default tool for shaping model behavior; it is a specialized, expensive, and risky one. Understanding when it's the right answer — and when it's a trap — is more valuable than knowing how to run the training loop.

The clearest way to think about fine-tuning is by contrast with retrieval. RAG is "look it up": at inference time, you fetch the relevant facts and stuff them into the context window so the model can reason over them. Fine-tuning is "remember it": you take a pre-trained model and adjust its weights using your own data, so the patterns are baked into the network itself. The first changes what the model sees. The second changes what the model *is*. These solve different problems, and confusing them is the most common mistake in this part of the stack.

What fine-tuning is genuinely good at is behavioral adaptation — style, tone, format, the shape of a response. If you want a model that always responds in your company's voice, always structures its output a particular way, or has internalized a domain's vocabulary so deeply that you don't need to re-explain it in every prompt, fine-tuning is the right tool. What it is genuinely bad at is teaching new facts that change. Bake last week's product catalog into the weights and you'll be retraining every week; put it in a vector database and you update a row.

The mechanics are conceptually simple and operationally unforgiving. You start with a pre-trained model — someone else has already spent millions of dollars teaching it language. You then run additional training cycles on your own dataset, which has to be formatted exactly the way the model expects (typically a messages list with system, user, and assistant roles). Each cycle adjusts the weights slightly to make your examples more likely. The training loop computes a loss (how wrong the model was on each example), propagates that error backward through the network, and nudges the weights. Repeat thousands of times across thousands of examples, and the model's behavior shifts.

The risk that dominates everything is overfitting. If you train for too long on too narrow a dataset, the model stops learning the *pattern* in your data and starts memorizing the specific examples. It will look phenomenal on your training set and fall apart on anything it hasn't seen. The discipline that prevents this is the holdout set: before you train, you partition your data and reserve a slice the model never sees during training. You watch validation loss (performance on the holdout set) in parallel with training loss. As long as both are dropping, you're learning. The moment validation loss starts climbing while training loss keeps falling, you've crossed into memorization. That inflection point is where the useful version of your model lives — and you need to have saved checkpoints to roll back to it.

Full fine-tuning — updating every weight in the model — is computationally brutal and increasingly unnecessary. Parameter-efficient methods like LoRA freeze the original weights and train a small set of adapter parameters on top. You get most of the behavioral adaptation for a fraction of the compute, and you can swap adapters in and out the way you swap configuration. For most teams, this is the only form of fine-tuning that's economically viable, and it's a better starting point even when budget isn't the constraint, because the failure modes are gentler.

The honest decision tree looks like this. If you need fresh, factual knowledge, use RAG. If you need a deterministic rule, hard-code it. If you need behavioral adaptation that no amount of prompting can reliably produce — a consistent voice, a learned format, a domain feel — consider fine-tuning, and start with a parameter-efficient method on a small, clean, validated dataset. The skill this topic builds is not the ability to run a training loop. It's the judgment to know when fine-tuning is the right answer, the discipline to curate data that's worth training on, and the rigor to catch overfitting before it ships.

## Level 2 candidates

**Training Loop and Validation Strategy** — Covers the mechanics of forward pass, loss computation, backward pass, and weight updates, alongside the discipline of partitioning data and monitoring validation loss against training loss. Worth a deep dive because the gap between "I ran a training script" and "I produced a model that generalizes" lives entirely in how you structure validation and what you watch during training.

**Prompt Templates and Data Format** — The specific message structures (system/user/assistant roles, special tokens, formatting conventions) that different base models expect for fine-tuning data. Worth going deeper because format mismatches are silent killers — your loss curves will look reasonable while the model learns the wrong thing, and you won't know until inference.

**Overfitting and Checkpoint Selection** — The pattern where training loss keeps dropping while validation loss climbs, marking the transition from generalization to memorization. Worth a deep dive because recognizing the inflection point, saving checkpoints frequently, and choosing the right one to deploy is the difference between a model that works on new data and one that only works on your training set.

**Parameter-Efficient Methods (LoRA, Adapters)** — Techniques that freeze the base model and train a small set of additional parameters, dramatically reducing compute and memory requirements. Worth going deeper because for most practical fine-tuning scenarios this is the *only* viable path, and the design choices (rank, target modules, learning rate) materially affect outcomes.

**Data Curation and Annotation Strategy** — How to source, clean, label, and balance the training set, since fine-tuning quality is bounded almost entirely by data quality. Worth a deep dive because most failed fine-tuning projects fail at this stage, not in the training loop, and the patterns for building high-signal datasets are non-obvious.

**RAG vs. Fine-Tuning Decision Framework** — A structured way to decide which technique (or combination) fits a given problem, based on data freshness, behavioral needs, cost, and maintenance burden. Worth going deeper because this decision shapes the architecture of the entire system, and getting it wrong costs months of work on the wrong solution.

---