## Metadata
- **Date:** 26-05-2026
- **Source:** 07_natural_language_processing_nlp_tasks_and_fine_tuning.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-07 · Natural Language Processing (NLP) Tasks and Fine-Tuning

The temptation in 2026 is to treat every language problem as an LLM problem. You have a classification task? Prompt GPT-4. You need to extract entities? Prompt GPT-4. You want to summarize? Prompt GPT-4. This works often enough that it feels like the answer. It is not the answer. It is one answer among several, and reaching for it reflexively will cost you accuracy where you need accuracy, latency where you need latency, and money where you didn't need to spend any.

The mental model worth building is this: NLP is a small zoo of task shapes, and each shape has a natural solution. Once you can recognize the shape, the solution mostly picks itself. The shapes are classification (assign a label to a piece of text), sequence labeling (assign a label to each token in a piece of text), generation (produce new text from input text), and retrieval (find relevant text in a corpus). Most real problems are one of these, sometimes two stacked together. Knowing which shape you're holding is more important than knowing the latest model name.

Classification is the workhorse. Sentiment, topic, intent, spam, toxicity — they are all "given this text, pick a label." A fine-tuned encoder model (something in the BERT family) on a few thousand labeled examples will usually beat an LLM prompt on accuracy, run a hundred times faster, and cost a fraction as much. The trade is that you need labeled data and a fine-tuning pipeline. If you have ten labeled examples and need something working tomorrow, prompt an LLM and accept the latency. If you're scoring a million tickets a day, fine-tune. The decision is economic, not ideological.

Sequence labeling is the one that surprises people. Named entity recognition, part-of-speech tagging, span extraction — these tasks operate at the token level, not the document level, and that distinction matters more than it sounds. The hard part of NER is not "is this a person or a company"; it is boundary detection (does the entity start at "New" or at "York"?) and ambiguity (is "Apple" the company or the fruit, given context?). Token-level fine-tuning handles this naturally because the model learns to label each position. LLM prompting can do it, but extracting clean spans from generated text is brittle in ways that bite you in production. When the task is structured, prefer structured outputs from a structured model.

Generation tasks — summarization, translation, paraphrasing, question answering — are where LLMs genuinely shine and where the older fine-tuning playbook (encoder-decoder models like T5 or BART) still has a place when you need predictability and lower cost. The harder problem with generation is evaluation, not modeling. Metrics like BLEU and ROUGE measure n-gram overlap with a reference, which is a stand-in for "is this output good." They miss paraphrases that are correct, reward outputs that copy the input verbatim, and tell you nothing about factuality. If you ship generation systems, you will end up evaluating them with humans, with an LLM-as-judge, or with task-specific checks. Plan for that from the start.

Retrieval is the task that often hides inside other tasks. Semantic search, document retrieval, the R in RAG — they all rest on the same trick: turn text into dense vectors (embeddings) such that semantically similar texts end up close in vector space, then use cosine similarity to find neighbors. You fine-tune embedding models with contrastive objectives (pull related pairs together, push unrelated ones apart), and the resulting vectors are the substrate for everything from product search to clustering to deduplication. If you find yourself building a retrieval system from scratch with keyword matching, stop and consider whether embeddings would solve your problem in a quarter of the code.

The practical question — fine-tune or prompt — has a few honest answers. Fine-tune when you have labeled data, when you need consistent latency or cost, when the task is narrow enough that a smaller model can master it, or when the output format is structured. Prompt when you have no labels, when the task is broad or shifts often, when you need flexibility more than throughput, or when you're prototyping. Use classical methods (regex, rule-based extraction, dictionary lookups) when the patterns are deterministic — phone numbers, postal codes, fixed vocabularies — because a 200-character regex will outperform any neural model on the things regexes are good at, forever. The mistake is not in choosing the wrong tool; the mistake is in not knowing the menu.

What this topic builds in you is taxonomic instinct. When a stakeholder describes a problem in business language ("we need to flag complaints," "we need to pull dates out of contracts," "we need to summarize meeting notes"), you should be translating it into one of the four task shapes within seconds, then narrowing to a solution within minutes. That instinct is what separates someone who reaches for the same hammer every time from someone who actually ships NLP systems that work, run cheaply, and don't embarrass themselves in production.

## Level 2 candidates

**Text classification and sentiment analysis** — Covers framing classification as a fine-tuning task, choosing the right metric (accuracy vs. F1 vs. weighted precision depending on class balance and cost asymmetry), and the threshold at which prompting beats fine-tuning. Worth deeper treatment because the metric choice often matters more than the model choice, and most teams get it wrong.

**Named entity recognition and sequence labeling** — Covers the mechanics of token-level fine-tuning, the BIO/IOB tagging schemes, and why boundary detection and entity ambiguity make NER harder than it looks. Worth depth because sequence labeling is the task most often mishandled by reaching for an LLM, and the fixes are specific.

**Semantic similarity and embedding-based retrieval** — Covers how embedding models are trained with contrastive objectives, how to evaluate retrieval quality (recall@k, MRR), and how cosine similarity becomes the substrate for search, clustering, and RAG. Worth depth because embeddings are the hidden infrastructure of modern NLP and most practitioners use them without understanding what they encode.

**Abstractive summarization and paraphrasing** — Covers encoder-decoder vs. decoder-only setups for generation, why BLEU and ROUGE are imperfect, and how to evaluate generation in practice. Worth depth because evaluation is harder than modeling here, and the evaluation choices shape what you can actually ship.

**Machine translation and multilingual models** — Covers what makes translation different from other generation tasks (no single correct answer, strong reference effects), and why multilingual pre-trained models like XLM-RoBERTa are useful even for non-translation tasks in non-English languages. Worth depth if any of your work touches more than one language.

**Information extraction and relation extraction** — Covers extracting structured data (entities, relations, events) from unstructured text, and where rule-based methods complement neural ones. Worth depth because hybrid systems (regex + model) often outperform pure approaches in this area, and the engineering patterns are non-obvious.

---
