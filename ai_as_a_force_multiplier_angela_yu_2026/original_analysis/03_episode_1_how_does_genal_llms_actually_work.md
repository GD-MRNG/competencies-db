## Metadata
- **Date:** 19-05-2026
- **Source:** 3_episode_1_how_does_genal_llms_actually_work.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# How GenAI and LLMs Actually Work

Most people using ChatGPT every day couldn't tell you, even roughly, what it is doing when it answers them. That gap matters more than it sounds. The way you prompt an AI, the length of conversation you can sustain with it, the kinds of tasks it will quietly fail at, and the cost of running it at scale — all of these are downstream of a handful of architectural facts. You don't need the maths. You do need a working mental model, because without one you will keep treating the tool as magic, and magic is the worst possible frame for getting reliable work out of it.

The simplest reframe is this: a large language model is a probability engine for the next word. Give it a sentence, and it predicts the most likely token to come next, appends it, and repeats. Everything else — the apparent reasoning, the helpful tone, the ability to write code or summarise a document — is emergent behaviour built on top of that one mechanism, trained on roughly the entire corpus of written human knowledge. Calling it a "calculator for language" is a useful first analogy, but a more honest one is that it is a lossy, probabilistic compression of what humans have written. It does not look things up. It generates plausible continuations.

To see why that distinction matters, it helps to understand how we got here. AI as a field is a stack of ideas, each solving a problem the previous layer couldn't. Machine learning was the first move: instead of programming explicit rules ("a number 8 has two loops"), you feed the computer thousands of labelled examples and let it discover the rules itself. Supervised learning is that pattern with labelled data — here are a thousand pictures of apples, learn what "apple" means. Unsupervised learning drops the labels and asks the model to cluster the data on its own, which is how Spotify groups songs by genre or how your Instagram Explore page diverges from your friend's. Reinforcement learning is different again: the model takes actions, gets rewarded or punished by outcome, and gradually discovers strategy. AlphaGo learned to beat the world champion this way, by playing itself millions of times.

Deep learning sits across all of these. It uses neural networks — layered structures loosely modelled on the brain — to extract features at successive levels of abstraction. The first layer might detect edges in an image, the next shapes, the next objects. Stack enough layers and you can classify cats versus dogs (and, mostly, distinguish a chihuahua from a blueberry muffin). LLMs are the application of deep learning to the hardest unstructured data of all: human language.

The breakthrough that turned language models from a curiosity into ChatGPT happened in 2017, with a Google paper called "Attention Is All You Need." Before it, models read text one word at a time and quickly lost track of context. The Transformer architecture introduced attention — a mechanism that lets the model weigh the relevance of every word in a passage against every other word. In the sentence "the animal didn't cross the street because it was too scared," attention is what lets the model know "it" refers to the animal, not the street. That single capability is what makes modern AI feel like it understands you. It also turned out to scale beautifully with more compute and more data, which is why the field exploded.

Two further pieces complete the picture. Self-supervised learning is how these models are trained at scale: instead of needing humans to label every example, the model is given a sentence with a word hidden and asked to predict it. Do this across the internet and you get a system that has absorbed the statistical structure of human language without anyone manually tagging anything. This is why LLMs scaled so fast — the human labelling bottleneck simply went away. The second piece is the context window: the total amount of text the model can hold in attention at once, measured in tokens (roughly, sub-words). GPT-3 had a window of 2,048 tokens. Newer models reach into the hundreds of thousands. Everything inside the window — your prompt, the model's developing answer, the conversation so far — is "in awareness." Everything that falls outside it is gone.

This last point is where the abstract becomes practical. When a long conversation with an AI starts to drift, contradict its earlier instructions, or forget what you told it at the start, that is not the model being lazy. It is the context window shifting: the early tokens have slid out of view, and the attention mechanism has nothing to attend to. This is why putting your important instructions in the first prompt rather than scattering them across a chat works better. It is why long, meandering threads degrade. It is why summarising and restarting often outperforms continuing. The same fact governs cost — API usage is priced in tokens — and explains why "just paste the whole document in" is not always a free move.

So the working model you want to carry forward is this: an LLM is a Transformer-based neural network trained by self-supervised next-token prediction over human text, generating responses one token at a time within a finite context window, weighted by attention. Every quirk you encounter — the hallucinations, the forgetting, the sensitivity to phrasing, the surprising competence followed by surprising failure — traces back to one of those properties. Once you can see the machinery, you stop arguing with it and start working with it.

## Level 2 candidates

**The Transformer and the attention mechanism** — A closer look at how attention actually weighs tokens against each other and why the 2017 shift from recurrent networks unlocked the current generation of models. Worth deeper treatment because attention is the single most consequential idea in modern AI, and a stronger grasp of it sharpens intuitions about why models excel at some tasks and stumble on others.

**Tokens, context windows, and the economics of prompting** — How text is broken into tokens, how context windows are consumed by prompt plus response, and how window-shifting degrades long conversations. Worth deeper treatment because nearly every practical prompting decision — placement, length, when to restart, when to summarise — is governed by these mechanics, and they also drive API cost.

**The taxonomy of learning paradigms: supervised, unsupervised, reinforcement, self-supervised** — A tour of the four main training approaches with concrete examples of which problems each one solves. Worth deeper treatment because choosing the right approach is the core decision when applying AI to a real business problem, and most people conflate these into a single "AI" bucket.

**Deep learning and neural networks** — How layered networks extract progressively abstract features, and why depth matters for unstructured data like images, audio, and language. Worth deeper treatment because deep learning is the substrate underneath LLMs, and understanding the layered feature-extraction model demystifies a great deal of AI behaviour beyond text.

**LLMs as probabilistic next-token predictors** — A focused dive on the generative loop itself: how a single next-token prediction, fed back into the model, produces coherent multi-paragraph output, and why this framing explains hallucinations and sensitivity to phrasing. Worth deeper treatment because this is the mental shift that separates intentional users from superficial ones, and it directly informs how to write prompts that actually work.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Most people interact with LLMs at the level of symptoms: sometimes they are brilliant, sometimes they forget instructions, sometimes they confidently invent things. If you do not have even a rough model of what the system is doing underneath, those behaviors feel arbitrary. And when behavior feels arbitrary, you cannot engineer around it — you can only poke at it and hope.

That becomes a practical problem fast. Prompt design, context management, latency, cost, hallucination risk, and reliability all come from the architecture. If you think the model is “thinking like a person,” you will keep expecting the wrong things from it. If you understand it as a system that predicts tokens within constraints, its quirks become much easier to anticipate.

This topic matters because engineering with LLMs requires the same thing engineering with any system requires: a model of the mechanism. Not full math, but enough causal structure to know why the system behaves the way it does and what levers you actually have.

## What You Need To Know First

**1. Token**  
A token is a chunk of text the model processes, often smaller than a word and sometimes larger. The model does not literally read “words” the way humans think of them; it reads sequences of tokens. This matters because both context limits and API costs are usually measured in tokens, not sentences or pages.

**2. Training**  
Training is the process where a model adjusts its internal parameters by seeing massive amounts of data and learning statistical patterns. For LLMs, this is mostly not hand-coded rules. The model is shaped by exposure to text and repeated correction during learning.

**3. Neural network**  
A neural network is a layered mathematical system that learns patterns from data. You do not need the equations here. The useful idea is that each layer can learn more abstract structure than the one before it, which is why these systems can handle messy inputs like images and language.

**4. Context window**  
The context window is the amount of text the model can attend to at one time. Your prompt, prior messages, and the model’s own partial response all consume that space. Once older material falls outside the window, it is no longer available to influence the answer.

## The Key Ideas, Connected

**1. An LLM is fundamentally a next-token prediction system.**  
At its core, the model is not retrieving facts from a database or reasoning from first principles in the human sense. It is repeatedly predicting what token is most likely to come next given the tokens already in view. Then it adds that token and does the same thing again. This sounds simple, but it is the base mechanism from which the impressive behavior emerges. Once you grasp that, the next question is obvious: how can something so simple produce outputs that seem so capable?

**2. The apparent intelligence comes from learning statistical structure across huge amounts of human text.**  
Because the model has been trained on enormous corpora, it has absorbed patterns about how language, explanations, arguments, code, and documentation tend to continue. That is why it can often produce useful answers: not because it “looks things up” on demand, but because it has compressed a vast amount of textual regularity into its parameters. This is also why the article calls it a probabilistic, lossy compression of human writing. And once you see that it learned from data rather than rules, it becomes helpful to place it inside the broader family of machine learning methods.

**3. LLMs are one outcome of a larger progression in machine learning.**  
The article walks through supervised, unsupervised, and reinforcement learning to show that AI did not appear all at once. Each paradigm solves a different kind of learning problem: learning from labeled examples, finding patterns without labels, or improving through reward and feedback. This matters because it situates LLMs as part of a stack of ideas rather than a magical exception. That stack then narrows into the technical substrate that made them work at scale: deep learning.

**4. Deep learning made it possible to learn high-level structure from messy, unstructured data.**  
Traditional rule-based systems struggled with language because language is ambiguous, contextual, and full of exceptions. Deep neural networks helped by learning layered abstractions directly from data. In images, that might mean edges, then shapes, then objects. In language, it means increasingly rich representations of syntax, semantics, and relationships between tokens. This sets up the key architectural leap the article wants you to understand next: the Transformer.

**5. The Transformer’s attention mechanism solved the context-tracking problem that older models handled badly.**  
Before Transformers, sequence models tended to process text in order and had difficulty retaining long-range relationships. Attention changed that by letting the model weigh the relevance of different tokens against one another directly. Instead of carrying context forward in a fragile chain, it can examine relationships across the visible text more flexibly. This is the reason modern models feel dramatically more coherent over long passages. And once attention exists, another scaling question appears: how do you train such a system without labeling the internet by hand?

**6. Self-supervised learning provided a scalable way to train language models on massive text corpora.**  
The trick is that the text itself supplies the supervision. Hide or predict tokens, compare the prediction to the actual continuation, and use the error signal to improve the model. That means you do not need humans to manually annotate every example. This is what made modern LLM scale economically and technically. Once trained this way, though, the model still has a very practical operating limit: it can only work over a finite amount of text at once.

**7. The context window is the model’s working memory, and many practical failures come from its limits.**  
Everything the model can actively use must fit inside the current context window: your instructions, previous turns, source text, and the answer being generated. When that space fills up, older material falls out. That is why long chats drift, why early instructions get ignored, why summarizing and restarting can help, and why input length affects both quality and cost. This is where the architecture turns into day-to-day practice.

**8. Once you see these mechanisms together, LLM behavior stops looking mysterious and starts looking engineerable.**  
Hallucination follows from generating plausible continuations rather than checking a ground-truth database. Sensitivity to phrasing follows from statistical conditioning on token sequences. Forgetfulness follows from context limits. Strong performance on common patterns and weaker performance on edge cases follow from the distribution of training data. This is the payoff of the whole chain: the model’s quirks are not random personality traits; they are consequences of how it is built.

## Handles and Anchors

**1. Think “autocomplete at enormous scale.”**  
This is not the full story, but it is a good anchor. An LLM is a vastly more sophisticated autocomplete system trained on huge amounts of text. That framing helps explain both its fluency and its tendency to produce plausible but false continuations.

**2. Attention is selective spotlight, not human understanding.**  
The model can spotlight which earlier tokens matter for predicting the next one. That is powerful, but it is not the same as comprehension in the human sense. This helps keep expectations calibrated.

**3. The context window is a moving whiteboard.**  
Everything currently on the whiteboard can influence the work. Once text is erased to make room for new text, the model cannot use it anymore. That is an easy way to remember why long chats degrade and why instruction placement matters.

## What This Changes When You Build

**An engineer who understands this will put critical instructions and source constraints into the active context deliberately because the model can only use what is currently visible to it.**  
That changes prompt design: important requirements go in the working prompt or refreshed summary, not buried 40 messages back.

**An engineer who understands this will treat long chats as degrading environments because context-window pressure causes drift even when the model still sounds confident.**  
So they will summarize, restart, and re-anchor the task instead of assuming continuity is free.

**An engineer who understands this will verify factual or niche claims externally because the model generates likely continuations rather than retrieving guaranteed truth.**  
That is especially important for recent libraries, internal systems, edge-case APIs, and specialized domain knowledge.

**An engineer who understands this will decompose complex tasks because next-token generation is locally strong but globally fragile across long chains of dependency.**  
Smaller staged prompts reduce the chance that one hidden misunderstanding contaminates an entire multi-step output.

**An engineer who understands this will reason about cost and latency in tokens, not just in requests, because the architecture processes text through a finite context window and pricing tracks that unit.**  
That affects practical design decisions like whether to paste whole documents, how much history to retain, and when a summary is cheaper and more reliable than brute-force context retention.

</details>
