## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content
Most engineers treat API design as a UI problem — pick clean resource names, use the right HTTP verbs, return sensible status codes, and you're done. The real difficulty has almost nothing to do with aesthetics. The moment a second system starts consuming your API, you have made a commitment. Not a commitment you signed or agreed to in a meeting — a commitment that now exists in deployed code, running in production, operated by a team that may not talk to you. That commitment is the contract, and the mechanics of how different API technologies encode and enforce that contract determine how much freedom you retain to evolve your system without breaking theirs.

The Level 1 post established that microservices and event-driven architectures turn every inter-service boundary into a network call or an asynchronous message. This post is about what crosses that boundary — the shape, the semantics, the promises — and why the choice of REST, gRPC, or event schema isn't a style preference. It's a decision about how much of your contract is machine-enforced versus convention-enforced, and that distinction has consequences you'll live with for years.

## What a Contract Actually Promises

An API contract is more than a data shape. It consists of several layers, and the ones people forget about are the ones that cause production incidents.

The **structural contract** is the most visible: the fields, their names, their types, and their nesting. When you return a JSON object with a field `"total_price": 42.99`, consumers write code that reaches into that path and expects a number.

The **semantic contract** is what those fields mean. If `created_at` returns a UTC timestamp today and someone changes it to return local time next month, the structural contract is identical — still a string, still ISO 8601 — but every consumer interpreting it as UTC is now silently wrong. Semantic breaking changes are the most dangerous kind because no schema validator, type checker, or linter will catch them.

The **behavioral contract** includes everything outside the payload: expected latency ranges, idempotency guarantees, error response formats, pagination behavior, rate limiting semantics. When your consumer retries a `POST` because they believe it's idempotent and it isn't, the broken contract was behavioral — and it was never written down.

The **error contract** is often the most neglected. What does a `400` response body look like? Is there a machine-readable error code, or just a human string? Can a consumer programmatically distinguish "invalid email format" from "email already taken"? If you've ever had to parse error messages with string matching in production code, you've experienced what happens when the error contract is undefined.

These layers stack. REST, gRPC, and event schemas each formalize different layers and leave the rest to convention.

## How REST Encodes the Contract

REST APIs over HTTP with JSON bodies are the most common form of service interface. Their contract model is **implicit by default**. Nothing in the technology itself forces you to define a schema, version your API, or specify what happens when a field is missing. This is REST's superpower and its central risk.

JSON's type system is thin: strings, numbers, booleans, nulls, arrays, objects. There is no native distinction between an integer and a float, no date type, no enum type. A field that should only ever contain `"pending"`, `"active"`, or `"cancelled"` is, at the wire level, just a string. The structural constraint exists only in documentation or in validation code that someone remembered to write.

**OpenAPI** (formerly Swagger) exists to formalize REST contracts, and it helps — but the level of enforcement depends entirely on how it's used. If OpenAPI specs are generated from code after the fact, they document what exists; they don't constrain what's allowed. If they're written first and used to generate server stubs and client SDKs, they function closer to a real contract. Most teams fall somewhere in between, which means the spec drifts from reality on a timeline measured in weeks.

REST's flexibility makes additive changes low-friction. Adding a new field to a response body is generally non-breaking because well-behaved JSON parsers ignore unknown fields. But "generally" is doing real work in that sentence. If a consumer is using strict deserialization — a typed language that maps JSON to a struct and rejects unknown keys — your additive change just broke them. You won't know this until they page you at 2 AM. The contract was implicit, so neither side knew they disagreed about what was allowed.

Versioning in REST is convention, not mechanism. You can put the version in the URL path (`/v2/orders`), in a header (`Accept: application/vnd.myapi.v2+json`), or in a query parameter. None of these is enforced by HTTP itself. And none of them solves the hard problem, which is: what does "v2" mean? Does it mean every endpoint changed? Just one? Is v1 still supported? For how long?

## How gRPC Encodes the Contract

gRPC uses **Protocol Buffers (protobuf)** as its interface definition language, and this single decision changes the contract model fundamentally. The contract is defined in a `.proto` file before any code is written, and both server and client generate code from that file. The schema is not documentation — it's the source of truth.

```protobuf
message Order {
  string order_id = 1;
  int64 total_cents = 2;
  OrderStatus status = 3;
  string created_at = 4;
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
}
```

The numbers assigned to each field (`= 1`, `= 2`) are **field tags**, and they matter far more than the names. On the wire, protobuf doesn't transmit field names at all — it transmits tag numbers and values in a binary encoding. This means renaming a field is a non-breaking change (it only affects generated code, not the wire format), but reusing or changing a tag number is catastrophic. If you delete field `2` and later assign tag `2` to a new field with a different type, any old message still in a queue or a cache will have its `total_cents` bytes silently reinterpreted as the new type. Protobuf provides the `reserved` keyword specifically to prevent this:

```protobuf
message Order {
  reserved 2;
  reserved "total_cents";
  // tag 2 and name total_cents can never be reused
}
```

**Backward compatibility** means new code can read old messages. **Forward compatibility** means old code can read new messages. Protobuf achieves both for additive changes: if you add a new field with a new tag, old consumers simply skip the unknown tag when deserializing, and new consumers handle the absence of new fields with default values (zero for numbers, empty for strings, the first enum value for enums). This works reliably because the compatibility rules are built into the wire format, not left to convention.

The tradeoff is rigidity. Changing a field's type — even something that feels safe like `int32` to `int64` — has specific wire-format implications because they use different encodings. gRPC forces you to think about compatibility at design time, which costs more up front and pays off over the lifetime of the contract.

gRPC also formalizes the service interface itself, not just the message shapes:

```protobuf
service OrderService {
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (stream Order);
}
```

This means the set of operations, their request/response types, and whether they're unary or streaming are all part of the machine-enforced contract. In REST, whether `GET /orders` returns a paginated list or a stream is a convention documented in prose.

## How Event Schemas Encode the Contract

Event-driven interfaces have a contract problem that synchronous APIs don't: **the producer has no direct relationship with its consumers**. When a service publishes an `OrderPlaced` event to a message broker, it doesn't know which services subscribe. It can't coordinate a migration. It can't even tell if anyone is still consuming an old format.

This makes event schema evolution the hardest contract problem of the three. Add the fact that events are often persisted — in Kafka, event sourcing systems, or replay-capable queues — and you have multiple schema versions coexisting not just across deployments but across time. A consumer replaying events from six months ago must be able to deserialize events from a schema version that no running producer has used in weeks.

**Schema registries** (Confluent Schema Registry, AWS Glue Schema Registry) exist to address this. They store versioned schemas and enforce compatibility rules at the broker level. When a producer tries to register a new schema version, the registry checks it against the previous version and rejects it if the change is incompatible with the configured compatibility mode — backward, forward, full, or none. This is the only one of the three paradigms where compatibility enforcement happens at the infrastructure layer rather than at the code layer.

**Apache Avro**, commonly used with Kafka, handles compatibility differently from protobuf. Avro serialization doesn't include field identifiers in each message — instead, the reader uses both the writer's schema (embedded or referenced by ID) and the reader's schema, and resolves differences between them at deserialization time. This makes new fields safe only if they have default values, because the reader's schema needs to supply a value when reading old messages that lack the field. If you add a field without a default, the reader will fail when encountering any message written before the change.

The critical distinction is that in synchronous APIs, you have a request-response loop that makes contract mismatches visible immediately (a 400 error, a type mismatch, a failed deserialization). In event-driven systems, a contract mismatch might surface as a consumer silently dropping messages, writing corrupted data to its own store, or falling behind on its consumer group because deserialization exceptions are accumulating in a dead-letter queue. The feedback loop is longer and the blast radius is wider.

## The Spectrum from Flexibility to Enforcement

These three approaches represent points on a spectrum, and the axis isn't "which is better." It's **how much contract enforcement is structural versus social**.

| Dimension | REST + JSON | gRPC + Protobuf | Events + Schema Registry |
|---|---|---|---|
| Schema enforcement | Optional (OpenAPI) | Required (`.proto` files) | Configurable (registry rules) |
| Type safety on the wire | Weak (JSON types only) | Strong (binary encoding) | Varies (Avro, Protobuf, JSON Schema) |
| Compatibility checking | Manual/CI-based | Compile-time + wire-format rules | Registry-enforced per write |
| Consumer visibility | Known (direct calls) | Known (direct calls) | Unknown (pub/sub decoupling) |
| Version coexistence | Explicit (URL/header) | Implicit (wire-compatible fields) | Mandatory (persisted events) |

Moving right on this spectrum buys you safety and costs you flexibility. A REST API can evolve quickly and informally when you have two consumers and a shared Slack channel. That same informality becomes a liability when you have forty consumers across six teams and an event stream replayed daily for analytics.

## Tradeoffs and Failure Modes

**The semantic break that no schema catches.** A payments service returns `amount` as cents (integer). A new developer, seeing no documentation, starts returning dollars (float). The schema change from `int` to `float` might cause a type error in some consumers — but in loosely typed consumers (JavaScript, Python with permissive deserialization), the value simply starts being interpreted as 100x its actual magnitude. Orders worth $1 are charged $100. The schema didn't break. The contract did.

**The accidental tight coupling of flexible APIs.** REST's lack of a formal schema means consumers will depend on whatever your API actually returns, not what you intended it to return. If your API returns fields in alphabetical order because of your serializer's default behavior, some consumer will eventually depend on that ordering. If you include a `debug_info` field in development that leaks into production, someone will build a dashboard on it. This is **Hyrum's Law**: with enough consumers, every observable behavior of your system becomes a de facto contract, regardless of what you documented. gRPC's code generation narrows this surface because consumers interact through generated types, not raw payloads — but it doesn't eliminate it entirely.

**The protobuf field number reuse.** This is catastrophic and not hypothetical. A team removes a field, months later a new developer adds a field and picks the vacated tag number. Old messages in caches, logs, or event stores are now silently corrupted when read by new code. The failure mode isn't an error — it's wrong data. This is why `reserved` isn't a nice-to-have; it's a safety mechanism.

**The event schema migration nobody coordinates.** In synchronous APIs, you can deploy the server first with a new optional field, then update clients. In event-driven systems, you may need all consumers to tolerate the new schema before the producer starts emitting it — but you don't control the consumers, and you may not know who they are. Without a schema registry enforcing compatibility modes, any producer change is a unilateral decision with unknown downstream consequences.

**Versioning as a strategy for avoidance.** Teams sometimes reach for a new API version (`/v2/`) every time a change feels risky, deferring the real work of understanding their compatibility constraints. This leads to a proliferation of versions that all need to be maintained, documented, and tested. Each active version multiplies the surface area of the contract. Versioning is a necessary tool, but using it to avoid understanding wire compatibility is expensive.

## The Mental Model

An API contract is not the schema you wrote — it's the set of expectations your consumers have encoded into their running systems. Some of those expectations match your schema. Some match undocumented behavior. Some match behavior you didn't know you had.

The choice between REST, gRPC, and event schemas is a choice about where contract enforcement lives. In REST, it lives in conventions, documentation, and discipline. In gRPC, it lives in the wire format and generated code. In event-driven systems with a schema registry, it lives in infrastructure that gates writes. None of these eliminate the need to think about compatibility — they determine how early and how loudly you find out when you've broken it.

The single most important conceptual shift: **a non-breaking change is defined by what consumers can tolerate, not by what the producer intended**. If you understand this, you can reason about any versioning strategy, any migration plan, and any contract testing approach from first principles.

## Key Takeaways

- An API contract has four layers — structural, semantic, behavioral, and error — and most tooling only validates the first. The other three are where the hardest bugs live.

- REST's flexibility is a double-edged property: it makes rapid evolution easy when consumer coordination is cheap, and makes silent breakage easy when it isn't.

- Protobuf field tags, not field names, define wire identity. Reusing a tag number doesn't cause an error — it causes silent data corruption, which is worse.

- Backward compatibility (new code reads old data) and forward compatibility (old code reads new data) are distinct properties with distinct design requirements. Additive-only changes with sensible defaults satisfy both in protobuf and Avro.

- Event schemas are the hardest contract problem because the producer cannot identify its consumers, events persist across schema versions, and contract mismatches surface as silent data corruption rather than immediate errors.

- Hyrum's Law applies to every API style: consumers depend on observable behavior, not documented behavior. The only way to narrow that gap is to minimize what's observable beyond the formal contract — which is exactly what code generation and binary wire formats do.

- Schema registries are the only common mechanism that enforces compatibility at the infrastructure level, rejecting incompatible schema changes before they reach any consumer. This makes them uniquely valuable in event-driven systems where coordination is impractical.

- Versioning is a tool for managing contract evolution, not a substitute for understanding wire compatibility. Every active version is a contract you're maintaining whether you acknowledge it or not.

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

As soon as another system integrates with your API, your implementation stops being just your code and starts being part of someone else’s runtime assumptions. That matters because changes that look harmless from the producer side — renaming a field, changing timestamp interpretation, altering pagination behavior, returning different error bodies — can break consumers in ways that don’t show up in your own tests. The failure mode is often not “request failed loudly.” It is “consumer kept running, but did the wrong thing.”

This gets worse as systems become more distributed. In a monolith, changing a function signature breaks at compile time. Across service boundaries, the break is delayed, partial, and often invisible until production. A REST consumer may silently misread a field. A gRPC consumer may fail on incompatible schema evolution. An event consumer may start dead-lettering messages hours after a producer deploys, or worse, deserialize old data into the wrong meaning.

So the real engineering problem is not “how do I design a nice API?” It is “how do I make and evolve cross-system promises without creating hidden breakage, silent corruption, or an ever-growing maintenance burden?” The article is about the mechanics of those promises: where they are encoded, how strongly they are enforced, and what kinds of mistakes each approach makes easy or hard.

---

## What You Need To Know First

**1. Serialization**
Serialization is just how data is turned into bytes so it can cross a network or be stored. JSON, protobuf, and Avro are all serialization formats. The important point here is that the format determines what information survives onto the wire: JSON carries field names as text, protobuf carries numeric field tags, and Avro relies on schemas to interpret the bytes. That difference is why “safe change” means different things in each system.

**2. Producer and consumer**
The producer is the system sending data; the consumer is the system receiving and interpreting it. In synchronous APIs, these are usually the server and client in a direct request-response relationship. In event systems, the producer may not even know who the consumers are. That matters because compatibility is really about whether consumers can still interpret what producers emit.

**3. Backward vs forward compatibility**
Backward compatibility means new code can read old data. Forward compatibility means old code can read new data. They sound similar, but they protect different deployment orders. If you deploy producers and consumers at different times, you usually need to reason about both, because mixed versions will exist at once.

**4. Schema**
A schema is a formal description of data shape: fields, types, maybe defaults, maybe constraints. But a schema usually describes only structure. It does not automatically capture meaning like “timestamp is UTC” or behavior like “retrying this request is safe.” That gap is central to the article.

---

## The Key Ideas, Connected

**An API contract is broader than payload shape.**

Most engineers first think of a contract as “what fields are in the request and response.” That is only the structural layer. The article’s main move is to widen the frame: consumers also depend on what fields mean, how operations behave, and how errors are represented. If you only think structurally, you will miss the most dangerous breakages, because many production incidents come from semantics or behavior changing while the payload shape stays valid.

That leads directly to the next idea: if contracts have multiple layers, different API technologies do not just transport data differently — they formalize different parts of the contract differently.

**REST, gRPC, and event schemas differ mainly in where contract enforcement lives.**

The article is not arguing that one style is universally better. It is arguing that the real distinction is where the system puts pressure on correctness. With REST, much of the contract is implicit unless you add tooling and discipline. With gRPC, the schema and service interface are defined up front and used to generate code. With event schemas plus a registry, compatibility checks can be enforced by infrastructure before new messages are even accepted.

Once you see contract enforcement as the axis, the tradeoff becomes clearer: more enforcement usually means less freedom to change things casually, but also fewer ambiguous, consumer-specific interpretations.

**REST is flexible because the wire contract is weakly enforced.**

JSON is easy to produce and consume, but its type system is minimal. Many important constraints — enum values, timestamp semantics, optionality, unknown field handling — are not strongly represented on the wire. That makes REST easy to evolve informally when teams coordinate closely. But the same looseness means producer and consumer can each form different beliefs about what is allowed.

That is why additive changes in REST are only “usually safe.” They are safe only if consumers actually ignore unknown fields. If some consumer uses strict deserialization, your harmless extra field becomes a breaking change. The mechanism here is important: because the format and protocol do not define unknown-field tolerance strongly enough, compatibility depends on consumer implementation choices, not just producer intent.

That weakness naturally motivates stronger schemas.

**gRPC changes the game by making the schema the source of truth, not just documentation.**

In gRPC, the `.proto` file is not an optional description written after the fact. It is the artifact both sides generate code from. That means the structural contract is far more explicit and machine-enforced. Types, field presence, enums, and RPC method signatures are all specified in one formal place.

This matters because it narrows the range of accidental disagreement. Consumers interact with generated types rather than arbitrary JSON blobs. That reduces ambiguity, but it also introduces hard compatibility rules tied to the wire format itself. Once field tags become the identity of fields on the wire, some changes become safe and others become dangerous in a very specific way.

**In protobuf, field tags are the real wire identity, which makes some refactors cheap and others catastrophic.**

A field name is mostly for humans and generated code. On the wire, protobuf sends field numbers. So renaming `total_cents` to `amount_cents` is usually fine if the tag stays the same; the bytes still mean the same thing. But reusing tag `2` for a different field means old bytes will be interpreted as the new field. That produces silent corruption rather than an obvious failure.

This is why `reserved` exists. It is not style polish. It is a mechanism to preserve wire history. Once a tag has existed in the world, it may still exist in stored messages, caches, queues, or logs. If you reuse it, you are not “cleaning up.” You are changing how historical bytes are interpreted.

From there, the article extends the compatibility story beyond direct RPC.

**Event-driven systems make schema evolution harder because producers and consumers are decoupled in time and visibility.**

With a synchronous API, a producer usually knows its consumers at least indirectly: clients call the server, and contract mismatches tend to show up immediately as failed requests or deserialization errors. In event systems, the producer emits data into a broker and may not know who consumes it. Consumers may lag behind, be deployed independently, or replay old events later.

That changes the mechanics of compatibility. You no longer just need “new server works with current clients.” You need “new producers don’t break unknown consumers” and “current consumers can still read months-old events.” Because events persist, schema versions coexist over time, not just during rollout windows.

That persistence creates the need for explicit compatibility enforcement beyond application code.

**Schema registries exist because event systems need compatibility checks at the infrastructure boundary.**

A schema registry stores versioned schemas and can reject incompatible changes when producers try to register or publish them. This is especially useful in event systems because the producer cannot manually coordinate with every consumer. The infrastructure acts as the gatekeeper.

The mechanism is different from gRPC. In gRPC, generated code and protobuf rules constrain application behavior. In event systems, the broker/registry can prevent bad schema evolution from entering the shared stream at all. That is valuable because once a bad event is published, many consumers may ingest it, persist derived state from it, or fail asynchronously long after the deploy.

This also helps explain why Avro’s compatibility rules feel different.

**Compatibility always depends on how missing or unknown data is interpreted.**

In protobuf, old consumers skip unknown fields, and new consumers use defaults when old messages lack new fields. In Avro, reader and writer schemas are resolved together, so adding a field is only safe if the reader has a default for cases where old messages never carried that field. Different mechanism, same underlying problem: mixed versions exist, so the system needs a rule for “what happens when one side expects data the other side never sent?”

That brings the article to its broadest point.

**A non-breaking change is defined by consumer tolerance, not producer intention.**

This is the core mental shift. Producers do not get to declare a change non-breaking just because it seems harmless locally. A change is non-breaking only if existing consumers can continue functioning correctly with it. That includes undocumented dependencies created by real usage, which is why Hyrum’s Law matters: consumers depend on observed behavior, not only specified behavior.

Once you accept that, versioning, schema discipline, and compatibility rules stop looking like ceremony. They are ways of managing the fact that deployed consumers hold assumptions you do not fully control. Different technologies simply move the point where you discover those assumptions: in docs review, in generated code, in registry enforcement, or in production incidents.

---

## Handles and Anchors

**1. “An API contract is whatever consumers have encoded into running code.”**  
Not what you documented. Not what you meant. What their systems actually assume. If they assume timestamps are UTC, retries are safe, and error bodies contain machine-readable codes, those assumptions are part of the contract whether you wrote them down or not.

**2. Think of REST, gRPC, and event schemas as different places to put guardrails.**  
REST puts more responsibility on people and process. gRPC puts more responsibility in schema and code generation. Event systems often need guardrails in infrastructure, because producers cannot coordinate directly with all consumers. Same problem, different enforcement location.

**3. Ask this question of any interface: “If I change this today, who can still read yesterday’s data, and who can still handle tomorrow’s data?”**  
That question forces you into real compatibility thinking. It separates backward from forward compatibility and exposes where your assumptions are only social conventions.

---

## What This Changes When You Build

**An engineer who understands this will treat “add a field” as a compatibility question, not an automatically safe change, because consumer deserialization behavior determines whether additive change is actually non-breaking.**  
The unaware engineer assumes JSON consumers will ignore unknown fields and ships the change casually. The consequence is that one strict consumer fails in production, often one the producer team did not know existed.

**An engineer who understands this will document and test semantics separately from schema, because schema validation cannot catch meaning changes.**  
The unaware engineer sees that `created_at` is still a string and assumes nothing broke. The informed engineer asks whether timezone, unit, precision, or business interpretation changed, because that is where silent data corruption comes from.

**An engineer who understands protobuf will reserve deleted field tags immediately, because tag reuse corrupts historical messages instead of throwing obvious errors.**  
The unaware engineer deletes a field and later reuses the number as cleanup. The consequence is not a clean compile failure; it is misinterpreted bytes in queues, caches, or persisted records, which is much harder to detect and recover from.

**An engineer who understands event contracts will design migrations assuming unknown and slow-moving consumers exist, because producer-consumer coordination is structurally weak in pub/sub systems.**  
The unaware engineer updates the producer first and expects consumers to catch up. The consequence is consumers dead-lettering messages, lagging behind, or replay jobs failing on older schema versions.

**An engineer who understands where enforcement lives will choose API style based partly on coordination cost, not just team preference, because loose contracts are manageable only when social coordination is cheap.**  
If there are two teams with tight communication, REST plus disciplined conventions may be enough. If there are many consumers across org boundaries, stronger machine-enforced contracts pay for themselves. The unaware engineer inherits a style by habit and then discovers too late that the coordination model did not match the system’s social reality.

**An engineer who understands this will use versioning sparingly and intentionally, because each active version is an additional contract surface to maintain.**  
The unaware engineer creates `/v2` whenever compatibility gets confusing. The consequence is permanent multi-version support, duplicated tests, consumer fragmentation, and a growing reluctance to clean anything up.

---

</details>
