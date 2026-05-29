## Metadata
- **Date:** 26-05-2026
- **Source:** 03_recurrent_and_sequential_models_lstm_gru.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-03 · Recurrent and Sequential Models: LSTM and GRU

Most data you encounter is not a sequence. A row in a database, an image, a tabular feature vector — these are bags of features where order is either irrelevant or implicit in the schema. Sequences break this assumption. "The cat sat on the mat" and "the mat on sat cat the" contain identical tokens and produce identical bag-of-words representations, yet only one of them means anything. The moment order carries information, you need a model that processes inputs in order and remembers what came before. That is what recurrent networks were built for, and even though Transformers have largely replaced them, the problem they solve has not gone away.

The core idea of a recurrent neural network is straightforward. You process the sequence one element at a time, and at each step you maintain a hidden state — a vector that summarises everything the network has seen so far. To process the next element, you combine it with the current hidden state to produce a new hidden state. The same weights are applied at every timestep, which means an RNN is really a single small network applied repeatedly, with its output feeding back into its input. This is elegant and it works in principle. In practice, it has a fatal flaw: gradients have to flow backward through every timestep during training, and across long sequences they either vanish (the network forgets) or explode (training diverges). A vanilla RNN can technically remember arbitrary history; it just cannot learn to.

LSTMs were the dominant fix. The trick is to add a separate memory channel — a cell state — that runs alongside the hidden state and is modified through a small set of learned gates. A forget gate decides what to discard from memory, an input gate decides what new information to write, and an output gate decides what to expose to the next layer. The gates are themselves small neural networks with sigmoid activations, so they produce values between zero and one that act as soft switches. The crucial property is that the cell state passes through these gates with mostly multiplicative updates, which means gradients can flow backward through long stretches of time without collapsing. The model learns what to remember and what to forget, instead of being forced to remember everything or nothing.

GRUs are the same idea with fewer parts. They merge the cell state and the hidden state, and collapse the three LSTM gates into two (an update gate and a reset gate). The result is a model with fewer parameters, faster to train, and in most benchmarks indistinguishable from an LSTM. If you reach for an LSTM today and find yourself worrying about parameter count, switch to a GRU and stop worrying. The choice between them is rarely the thing that determines whether your model works.

Recurrent models also extend naturally to two patterns worth knowing. A bidirectional RNN runs two RNNs in parallel — one forward, one backward — and concatenates their hidden states, so each position has access to both past and future context. This is essential when you can see the whole input before predicting (tagging, classification) and forbidden when you cannot (generation, real-time prediction). A sequence-to-sequence model uses one RNN as an encoder that compresses the input into a fixed representation, and a second RNN as a decoder that generates the output one token at a time. Translation, summarisation, and the original neural machine translation systems were all built this way. Attention, which would later eat the entire field, was first introduced as a patch on this architecture — a way for the decoder to look back at the encoder's hidden states instead of relying on a single bottleneck vector.

In 2026, you will rarely train an LSTM as your primary model. Transformers handle long-range dependencies more cleanly, parallelise on GPUs (RNNs are inherently sequential and waste hardware), and benefit from the entire pre-training ecosystem that has grown around them. But LSTMs and GRUs have not vanished. They show up in older codebases you inherit, in time-series forecasting where the inductive bias of sequential processing still pays off, in low-resource edge deployments where a small RNN beats a tiny Transformer, and in any setting where streaming inference matters and you want to update state one element at a time without recomputing attention over a growing context.

The more durable lesson is recognising when a problem is sequential at all. Order-sensitive data is more common than people assume: log lines, user sessions, sensor streams, financial ticks, clinical events. The moment you find yourself flattening a time-ordered sequence into a feature vector and feeding it to a feedforward model, ask whether the order is doing work. If it is, you need a sequential model — and whether that model is an LSTM, a GRU, or a Transformer is a secondary question. Recognising the structure of your data is the primary one.

The intuition LSTMs gave the field — that a model should learn what to remember and what to forget — outlived the architecture itself. Attention is a different mechanism for the same goal. Understanding LSTMs is less about being able to deploy one and more about understanding the problem they were trying to solve, because that problem is what every modern sequence model is still solving.

## Level 2 candidates

**RNN fundamentals: unrolling and backprop through time** — How an RNN is applied at each timestep and how gradients propagate backward through the unrolled computation graph. Worth a deep dive because the mechanics of backprop through time explain both why RNNs are expensive to train and why they are unstable.

**Vanishing and exploding gradients in RNNs** — Why repeated multiplication of Jacobians across timesteps causes gradients to collapse or blow up. Worth going deeper because this same dynamic underlies why deep networks of any kind are hard to train, and the standard fixes (gradient clipping, careful initialisation) generalise.

**LSTM cells and gates in detail** — The exact equations of the forget, input, and output gates, and how the cell state update creates a gradient highway. Worth a deeper treatment because the gating intuition recurs in many later architectures, including highway networks and gated attention variants.

**GRU and its trade-offs against LSTM** — How GRUs collapse the LSTM's gates and merge state, and the empirical evidence on when the simpler model suffices. Worth covering because the practical default in most RNN code today is a GRU, not an LSTM.

**Sequence-to-sequence models and the attention bottleneck** — How encoder-decoder RNNs work, why a single fixed-size context vector limits them, and how attention was originally introduced as a fix. Worth deeper treatment because this is the historical bridge from RNNs to Transformers and clarifies what attention was actually invented to do.

**Bidirectional RNNs and when they apply** — How running forward and backward passes in parallel improves tagging and classification, and why bidirectionality is incompatible with autoregressive generation. Worth a focused treatment because the same constraint shapes how modern models like BERT and GPT differ.

**Practical handling of variable-length sequences** — Padding, masking, packed sequences, and the bookkeeping required to batch sequences of different lengths efficiently. Worth covering because this is where most RNN implementations silently break, and the same issues recur in any sequential architecture.

---
