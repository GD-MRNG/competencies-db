You are turning a Level 0 course map into a minimal retrieval index. Many such indexes, one per domain, are loaded into a model's context at once; at query time the model scans them to route a question to the right domain and the right L1 topic — and, where useful, the L2 candidate within it — then sends the user to the full L1 document. Your output is read by that model, not by a human.

{level_0_map}

The reading model is a capable LLM. It already knows how concepts relate, what they mean, and why they matter — do not encode any of that. Encode only what the model **cannot** know from its own training: which domain this is, where its boundary falls, which L1 topics exist and what they are called, the L2 candidates inside each, and any specific terms a user would search for that aren't obvious from the titles. The index is a map of *this* repo, not an explanation of the subject.

Output this schema exactly — nothing else, no prose:

```
DOMAIN: <name>
SCOPE: <what this domain covers> | Excludes: <what it does not — be specific; this boundary is what stops misrouting>
DEPENDS-ON: <names of other domain maps this draws from, if any; else "none">

[ID] <Title>
  L2: <candidate name> | <candidate name> | …
  keys: <named tools, proper nouns, and inclusions a reader would NOT predict from the title>

ORDER: <ID → ID → … the sequence a learner should follow>
```

**Rules**

- `L2:` — the bare candidate names, pipe-separated. These are the addressable routing targets, so keep every one — but give it no explanation. The reading model supplies the meaning.
- `keys:` — only terms that are both specific/searchable and not predictable from the title: named tools (Tiktoken, Pinecone, Terraform) and surprising coverage (a "Databases" topic that also handles GDPR deletion). If a topic has no such terms, omit the line.
- `SCOPE` — spend your care here. When everything else is thin, the *excludes* are what stop the model routing confidently to a domain that doesn't hold the answer.
- `DEPENDS-ON` — names only. Each named domain has its own full entry loaded alongside this one, so don't describe its contents.
- Drop everything inferable: definitions, explanations, "why it matters," relationships between topics, cross-links, and pairwise dependency links. The model infers all of it. Keep only the repo-specific skeleton.

**Example** *(abridged — a real map runs every topic)*

```
DOMAIN: AI Engineer Production Track
SCOPE: Deploying, scaling, and operating AI systems from prototype to enterprise — infrastructure, reliability, observability, cost, security, multi-agent orchestration | Excludes: model training, fine-tuning, prompting and context management (Core Track), agentic loops and tool calling (Agentic Track)
DEPENDS-ON: Core Track | Agentic Track

[03] Containerization (Docker) as Portability and Reproducibility
  L2: Dockerfile & Image Layers | Multi-Stage Builds | Platform-Specific Images | Image Registry & Versioning | Docker Compose
  keys: ARM64 vs x86, --platform flag, ECR

[07] Databases and State Persistence
  L2: Relational Databases & Schemas | Vector Databases for Embeddings | NoSQL & Document Stores | Caching & Redis | Data Retention & Compliance
  keys: Aurora, Pinecone, DynamoDB, Redis, S3, GDPR deletion, similarity search

[12] Cost Optimization and Budget Management
  L2: Token Counting & Estimation | Model Selection & Routing | Caching & Deduplication | Batch Processing | Resource Right-Sizing
  keys: Tiktoken, classifier-based routing, batch API tiers

[… remaining topics in the same form …]

ORDER: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16
```

Before returning, confirm: no L2 carries an explanation, and every `keys` term is something a model could not guess from the title. If either fails, cut it.

Produce the index now for the Level 0 map provided.