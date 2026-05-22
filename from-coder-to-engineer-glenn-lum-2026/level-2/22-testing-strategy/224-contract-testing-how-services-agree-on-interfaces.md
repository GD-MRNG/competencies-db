## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers, when they first hear about contract testing, mentally file it as "schema validation between services." They picture something that checks whether Service A sends a JSON body that matches the shape Service B expects. That understanding is close enough to pass a conversation but wrong enough to produce a broken implementation. Contract testing is not about validating schemas. It is about capturing what a consumer actually does with a provider's API — the specific requests it makes and the specific parts of the response it relies on — and turning those expectations into independently verifiable tests on both sides. The directionality matters. The specificity matters. The independence matters. Getting any of those wrong produces a test suite that either catches nothing useful or becomes so brittle it gets abandoned.

## Why the Consumer Drives the Contract

The defining mechanic of contract testing — the thing that separates it from API schema validation or integration tests with mocks — is that **the consumer defines the contract, not the provider**.

This is counterintuitive. In most testing paradigms, the provider is the source of truth. The provider publishes an API spec. Consumers conform to it. If a consumer sends a malformed request, that is the consumer's problem. Contract testing inverts this. The consumer says: "Here are the specific API calls I make and the specific fields I read from the response." That declaration becomes the contract.

Why invert it? Because in a microservices system, the failure you are trying to prevent is not "the provider changed its API spec." That is visible. The failure you are trying to prevent is "the provider changed something it did not realize a consumer depended on." A provider might add a field, rename an internal enum value that leaks into a response, change a date format from ISO 8601 to Unix timestamps, or start returning `null` where it previously returned an empty array. None of these necessarily violate the provider's own API documentation. All of them can break a consumer in production.

Consumer-driven contracts make the implicit explicit. If Service A reads the `email` and `status` fields from a `/users/{id}` response, the contract says exactly that — and nothing more. Service A does not care about the other fifteen fields in the response. It does not care about the provider's internal data model. It cares about two fields and their types. This precision is the mechanism that allows contracts to be both stable and useful: they are narrow enough to avoid breaking on irrelevant changes and specific enough to catch the changes that actually matter.

## What a Contract Actually Contains

A contract is a collection of **interactions**. Each interaction is a pair: a request the consumer makes and the minimum response the consumer needs to function.

In Pact — the most widely adopted contract testing framework — an interaction looks roughly like this:

```json
{
  "description": "a request for user 42",
  "request": {
    "method": "GET",
    "path": "/users/42",
    "headers": {
      "Accept": "application/json"
    }
  },
  "response": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "id": 42,
      "email": "user@example.com",
      "status": "active"
    }
  }
}
```

But the values in the body are not meant literally. The contract is not asserting that the email is literally `"user@example.com"`. It is asserting that there is a field called `email` and that its value is a string. This is where **matchers** do their work. In practice, the consumer test specifies matching rules:

```json
{
  "$.body.id": { "match": "type" },
  "$.body.email": { "match": "type" },
  "$.body.status": { "match": "regex", "regex": "^(active|inactive|suspended)$" }
}
```

This distinction between exact values and matching rules is critical. Exact-value contracts break on every provider change, even harmless ones. Matcher-based contracts break only when the structural expectations are violated — the field disappears, the type changes, or the value falls outside the expected range. Getting the matcher granularity right is one of the most consequential design decisions in a contract testing implementation. Too loose (everything is `"match": "type"`) and you miss real breakage. Too tight (exact string matching on dynamic values) and you get false failures on every test run.

## The Two-Phase Verification Workflow

Contract testing splits into two completely independent phases that run in separate codebases, in separate CI pipelines, at separate times.

### Phase 1: Consumer Side

The consumer team writes a test. In this test, the consumer's HTTP client code runs against a **mock provider** — a local stub server that the contract testing framework spins up. The test declares: "When I make this request, I expect this response." The framework records this expectation. If the consumer's code actually makes the declared request and correctly handles the declared response, the test passes. As a side effect, the framework serializes the interaction into a **contract file** (sometimes called a pact file).

The important thing here is that the consumer test is not testing the provider. It is testing the consumer's own code against its own stated expectations. The contract file is the artifact — the exportable, portable record of what the consumer needs.

### Phase 2: Provider Side

The provider team takes the contract file and replays it. The provider's real API (running locally or in a test environment) receives each request from the contract. The framework then checks: does the actual response satisfy the matchers defined in the contract? If the consumer expected a 200 with an `email` field of type string and the provider returns a 200 with an `email_address` field, the verification fails.

The provider does not need the consumer's code. It does not need the consumer to be running. It only needs the contract file. This is the independence that makes contract testing scalable: each side runs its own tests in its own pipeline on its own schedule.

### The Broker Connects the Two

In practice, the contract file moves from consumer to provider through a **contract broker** — a central service (Pact Broker or Pactflow being the most common) that stores contracts and verification results. The consumer publishes its contract after a successful consumer-side test. The provider fetches the latest contracts for all its consumers and verifies against them. The broker tracks which versions of which services have been verified against which contracts, creating a matrix of compatibility.

This matrix is what enables the **can-i-deploy** check: before deploying a new version of Service B, you query the broker: "Has this version of Service B been verified against the contracts of all consumers currently in production?" If yes, deploy. If not, stop. This is where contract testing connects directly to your deployment pipeline, and it is where most of the operational value actually lives.

## Provider States: The Complexity That Surprises Everyone

Consider a contract interaction that says: "When I request `GET /users/42`, I expect a 200 with user data." For the provider to satisfy this during verification, user 42 must exist in whatever data store the provider is using during the test. The contract does not create this data. Something else has to.

This is where **provider states** come in. Each interaction can declare a precondition: "Given that user 42 exists and is active." The provider's verification harness must include a state setup mechanism — a hook that runs before each interaction replay and puts the provider's data store into the required state.

```ruby
provider_state "user 42 exists and is active" do
  set_up do
    User.create(id: 42, email: "test@test.com", status: "active")
  end
  tear_down do
    User.delete(42)
  end
end
```

Provider state management is the part of contract testing that scales worst. For a provider with three consumers and a handful of interactions, it is manageable. For a provider with twenty consumers and hundreds of interactions, the state setup harness becomes a substantial piece of test infrastructure that must be maintained alongside the provider's actual code. When provider state setup breaks or drifts, verification failures become ambiguous: is the contract actually violated, or is the test data wrong?

## How This Differs from Schema Validation

OpenAPI specs, JSON Schema, gRPC protobuf definitions — these all define what a provider's API looks like. Contract tests define what a consumer actually uses. The distinction matters in both directions.

Schema validation is provider-centric and exhaustive. It describes every endpoint, every field, every possible response code. A contract is consumer-centric and minimal. It describes only the interactions one specific consumer cares about. A provider can have an OpenAPI spec with fifty endpoints, and a contract from Consumer A might cover three of them.

Schema validation catches "the response body does not conform to the published spec." Contract testing catches "the response body no longer contains what Consumer A is actually reading." These are different failure classes. A provider can ship a response that is perfectly valid according to its OpenAPI spec and still break a consumer, because the spec allows `null` for a field that the consumer's code does not handle. A contract for that consumer would encode the expectation that the field is non-null.

The two approaches are complementary, not competing. Schema validation protects the provider's structural commitments. Contract tests protect the consumer's operational assumptions.

## Where Contract Testing Breaks Down

**Contracts test structure, not semantics.** A contract can verify that a `status` field returns a string matching `active|inactive|suspended`. It cannot verify that the meaning of `suspended` has not changed. If the provider starts using `suspended` to mean "temporarily paused" instead of "permanently banned," every consumer that makes authorization decisions based on status will break, and the contract test will pass. Contract tests catch interface drift, not behavioral drift.

**Organizational friction is the real bottleneck.** Contract testing requires consumer and provider teams to share a contract format, share a broker, and coordinate on provider state naming conventions. In organizations where teams have strong autonomy and weak coordination, getting provider teams to run consumer contracts in their pipeline is a political problem, not a technical one. The framework is easy. The adoption is hard.

**Thin contracts give false confidence.** If the consumer test only declares a single interaction with a single field using a type matcher, the contract is technically valid but operationally useless. It will pass even when the provider has made breaking changes to every other aspect of the response. Contract quality depends entirely on how thoroughly the consumer team encodes their actual dependencies. There is no automated way to verify that a contract is complete — it requires discipline and review.

**Async interactions add complexity.** Contract testing originated in HTTP request-response contexts. Extending it to message-based systems (Kafka, RabbitMQ, SNS) is possible — Pact supports message pacts — but the model is less natural. There is no request-response pair to capture. Instead, you are verifying that a published message conforms to the shape the consumer expects. The provider verification step becomes "generate a message using my real code and check it against the contract," which requires different test harness infrastructure.

**Provider state explosion.** As the number of consumers grows, the number of distinct provider states grows combinatorially. Consumer A needs user 42 to be active. Consumer B needs user 42 to be suspended. Consumer C needs user 42 to not exist at all. The provider's state setup harness becomes a matrix of scenarios that must be maintained independently of the provider's own test suite. This is where contract testing's maintenance cost concentrates, and it is the primary reason teams abandon it.

## The Mental Model

Think of contract testing as a protocol for encoding and verifying assumptions across a service boundary. In any distributed system, every service call carries implicit assumptions: the consumer assumes certain fields will be present, certain types will be stable, certain status codes will mean certain things. These assumptions are invisible until they break. Contract testing makes them explicit, portable, and verifiable.

The key conceptual shift is that the unit of testing is not the provider's API and not the consumer's code — it is the **relationship between them**. A contract is an artifact of that relationship. It is generated by one side and verified by the other. It encodes not the full capability of the API but the subset that one specific consumer depends on. This is why it catches failures that unit tests (which never cross the boundary) and E2E tests (which cross it but too late and too slowly) cannot.

If you remember one thing: a contract test does not prove the provider works correctly. It does not prove the consumer works correctly. It proves that the two can still talk to each other. That narrow, specific guarantee is precisely what makes it valuable.

## Key Takeaways

- **Consumer-driven means the consumer defines the contract.** The consumer declares the requests it makes and the response fields it depends on; the provider verifies it can still satisfy those expectations. The directionality is the mechanism that catches unintentional breaking changes.

- **A contract is a collection of interactions, not a schema.** Each interaction is a specific request-response pair with matchers that define acceptable response shapes, not exact values.

- **The two phases — consumer test and provider verification — run independently in separate pipelines.** This independence is what makes contract testing fast and scalable compared to integration or E2E tests.

- **The contract broker and the can-i-deploy check are where contract testing connects to deployment safety.** Without them, contracts are just documentation. With them, they become deployment gates.

- **Provider state management is the primary maintenance cost.** Every interaction that requires specific test data creates a setup obligation on the provider side, and this grows with each new consumer.

- **Contract tests catch structural drift, not semantic drift.** If a field's type and name stay the same but its meaning changes, the contract will still pass. Contracts protect interfaces, not business logic.

- **Schema validation and contract testing solve different problems.** Schema validation ensures the provider conforms to its own spec. Contract testing ensures the provider still satisfies what specific consumers actually use.

- **The most common failure mode is thin contracts that test almost nothing.** A contract is only as useful as the assumptions it encodes. Incomplete contracts create false confidence that the integration is safe.

# Discussion

## Why This Conversation Is Happening

In a service-based system, teams break each other most often not by taking an API fully offline, but by changing something that looked harmless locally. A provider renames a field, starts returning `null` instead of `[]`, changes a timestamp format, or swaps one enum value for another. Its own tests still pass. Its OpenAPI spec may still be valid. But some consumer in production was depending on that exact behavior, and now requests fail, parsing breaks, or business logic silently misfires.

The problem is that ordinary testing leaves a gap around the service boundary. Unit tests stay inside one codebase. End-to-end tests cross the boundary, but they are slow, late, and usually sparse. Schema validation tells you what the provider says it offers, not what consumers truly rely on. Contract testing exists to close that gap: to turn hidden cross-service assumptions into explicit artifacts that can be checked before deployment.

If engineers only understand contract testing as “schema validation between services,” they usually build the wrong thing. They either make contracts so broad they catch nothing useful, or so brittle they fail constantly and get ignored. The mechanics matter because the value comes from the exact shape of the guarantee: not “the API is good,” but “this consumer and this provider can still talk in the ways that matter.”

---

## What You Need To Know First

### 1. API schemas/specifications
An API schema or spec, like OpenAPI, JSON Schema, or protobuf, is a formal description of an API’s structure. It usually says what endpoints exist, what fields may appear, and what types they have. That is useful, but it is provider-centered: it describes the full interface the provider publishes, not the narrower subset that any one consumer actually uses.

### 2. Mocks and stubs
A mock or stub is a fake version of another service used during testing. Instead of calling the real provider, your code talks to a local stand-in that returns pre-arranged responses. In contract testing, the consumer test uses a mock provider not to simulate reality perfectly, but to record exactly what the consumer expects.

### 3. CI/CD pipelines
A CI/CD pipeline is the automated path that runs tests and checks before code is merged or deployed. This matters because contract testing is not just a local developer tool. Its real operational value appears when consumer-side contract generation and provider-side verification happen automatically in separate pipelines and influence deploy decisions.

### 4. Service boundaries
A service boundary is the point where one system calls another over a network or via messages. Once you cross that boundary, you lose the safety of in-process types and direct code control. Failures become versioning problems, compatibility problems, and coordination problems. Contract testing is specifically about managing those boundary risks.

---

## The Key Ideas, Connected

### 1. Contract testing is about verifying a relationship between two services, not validating a provider’s whole API.
What matters is not whether the provider’s interface is internally consistent in the abstract, but whether a specific consumer can still make the calls it needs and read the parts of the response it depends on. That shifts the unit of concern from “the API” to “this consumer-provider interaction.”

Once you frame the problem that way, it becomes clear why a general schema is not enough. A schema tells you everything the provider allows; it does not tell you which parts actually matter to Consumer A. That is why the next idea follows.

### 2. The consumer must define the contract, because the failure you care about is hidden consumer dependency.
If the provider authors the contract, it will usually describe what the provider believes it offers. But production breakages often come from things the provider did not realize a consumer depended on: a field being non-null, an enum having a certain spelling, a list being empty rather than missing.

So contract testing inverts the usual authority. The consumer declares: “These are the requests I make, and these are the parts of the response I actually read.” That inversion is the mechanism that surfaces hidden dependencies. Once the consumer is the source of truth for its own needs, the contract can be narrower and more accurate. That leads directly to what a contract actually contains.

### 3. A contract is a set of interactions: concrete requests plus the minimum acceptable responses.
The contract is not an exhaustive interface definition. It is a collection of examples of real usage: “when I send this request, I need a response with these fields, these types, and this status.” That makes the contract operational rather than descriptive.

This matters because a consumer does not depend on an entire response body equally. It may only read `email` and `status` and ignore fifteen other fields. Encoding only the minimum needed response is what keeps contracts useful instead of brittle. But if you encode examples literally, harmless value changes would fail the contract every time. So you need a way to separate structure from sample data, which leads to matchers.

### 4. Matchers make contracts stable by expressing what must stay true, instead of freezing exact example values.
The sample response in a contract file is just an example instance. The real rule is carried by matchers: this field must be a string, this one must match a regex, this one must be an integer. Without matchers, contracts would fail whenever dynamic data changed. With only loose matchers, contracts become too weak to catch real breakages.

That tradeoff is central: too strict means constant false failures; too loose means false confidence. The contract’s usefulness depends on choosing matcher granularity that reflects what the consumer truly depends on. Once the consumer has defined these interactions and matching rules, they need to become portable so the provider can verify them independently. That creates the two-phase workflow.

### 5. Contract testing works because consumer testing and provider verification are separate phases.
On the consumer side, the consumer runs its own code against a mock provider and generates a contract artifact. This test checks that the consumer can make the expected call and handle the expected response shape. It is not proving anything about the real provider yet.

Then, separately, the provider takes the generated contract and replays those interactions against its real implementation. This checks whether the provider can satisfy the consumer’s declared needs. The separation matters because it removes runtime coupling between teams: the consumer does not need a live provider to generate its contract, and the provider does not need the consumer’s code to verify it. That independence is what makes the approach scalable enough for CI. But once you have independent artifacts, you need a way to distribute and track them across versions, which is where the broker comes in.

### 6. A contract broker turns isolated tests into a compatibility system.
If contract files just sit in repos, they are hard to discover, version, and relate to deployments. A broker stores published contracts and provider verification results, effectively keeping a map of who has been verified against whom.

That map enables the crucial question: “Can I deploy this provider version, given the consumer versions currently in production?” This is the operational payoff. The broker is not just storage; it is what lets contract testing influence deployment safety. Without that, contracts are mostly documentation plus some test automation. With it, they become a release gate. But verification only works if the provider can actually reproduce the situations each interaction assumes, which introduces provider states.

### 7. Provider states exist because a contract describes expected interactions, not how to create the world needed for them.
A contract may say, “GET /users/42 returns a 200 with user data.” For that to be true during provider verification, user 42 must exist in the provider’s test environment. The contract does not and should not explain how to insert that user into the database. That setup belongs to the provider.

So each interaction may require a named precondition, or provider state, like “user 42 exists and is active.” The provider verification harness must translate that name into concrete test setup. This is where contract testing stops being just a neat idea and becomes real engineering work. Provider state machinery can grow large, fragile, and expensive to maintain. That maintenance burden explains many adoption failures and also helps clarify where contract testing sits relative to other tools.

### 8. Contract testing is different from schema validation because it protects actual usage, not published possibility.
A schema says what the provider considers valid across the whole interface. A contract says what one consumer actually needs for one slice of that interface. Those are different objects serving different failure modes.

That is why a provider can remain schema-compliant and still break a consumer. The schema may allow `null`, optional fields, or multiple enum values; the consumer may only function correctly for a narrower subset. Contract testing captures that narrower subset explicitly. So schema validation and contract testing are complementary: one guards provider promises broadly, the other guards consumer assumptions specifically. But even with that specificity, there is a limit to what contracts can prove.

### 9. Contract tests catch interface drift, not semantic drift.
A contract can verify that a field named `status` exists and contains one of a set of strings. It cannot verify that the meaning of those strings has not changed in a way that breaks the consumer’s business logic. If `suspended` still appears as a valid string but now means something different, the contract passes while the system behavior breaks.

This is the key limit of the technique. Contract testing gives a narrow but valuable guarantee: the consumer and provider are still structurally compatible at the boundary. It does not prove either side is correct in a deeper business sense. Understanding that boundary is what keeps teams from expecting too much and then concluding the technique “doesn’t work” when it misses a semantic failure.

---

## Handles and Anchors

### 1. Handle: “Schemas describe the menu; contracts describe what a diner actually orders.”
A restaurant menu may list fifty items. That tells you what the kitchen can in theory produce. But if you want to know whether a regular customer will be satisfied tonight, you care about the few dishes they actually order and the parts they care about. Contract testing is about those real orders, not the whole menu.

### 2. Handle: “A contract test proves compatibility, not correctness.”
If you remember one sentence, make it this one. The provider may still have bugs. The consumer may still have bugs. But the contract test says: given the assumptions this consumer declared, the provider still responds in a shape the consumer can use.

### 3. Question to ask of any system: “What assumptions is the consumer making that the provider does not know it is making?”
That question usually reveals whether contract testing is relevant. If consumers rely on undocumented field presence, non-null behavior, enum values, header behavior, or message shapes, those are contract candidates. If no such hidden assumptions exist, the benefit is smaller.

---

## What This Changes When You Build

### 1. An engineer who understands this will define contracts from consumer behavior, not from provider documentation, because the whole point is to capture real dependencies rather than advertised capability.
The unaware engineer often starts by exporting the provider’s schema or hand-writing a broad provider-owned contract. That usually recreates API documentation, not consumer protection. The result is a contract suite that passes while consumers still break on unrecorded assumptions.

### 2. An engineer who understands this will design matcher strictness carefully because matcher granularity determines whether the suite finds breakages or creates noise.
The default unaware move is either exact-value matching everywhere or type-matching everywhere. Exact matching causes fragile failures on harmless changes like dynamic IDs or timestamps. Type-only matching misses critical breaks like invalid enum values, nullable fields, or loosened formats. A knowledgeable engineer asks field by field: what does the consumer truly require here?

### 3. An engineer who understands this will invest early in provider state strategy because verification quality depends on reproducible preconditions.
The unaware engineer often treats provider states as a small setup detail and adds them ad hoc as tests appear. Over time, this turns into an unstructured pile of brittle fixtures and mysterious verification failures. The better approach is to treat provider-state setup as test infrastructure: naming conventions, reusable setup helpers, isolation rules, and cleanup discipline.

### 4. An engineer who understands this will connect contract verification to deployment decisions because the operational value comes from compatibility checks before release.
The unaware engineer may run contract tests occasionally or treat them as informative only. That misses the main payoff. If contract results do not feed a broker and a deploy gate like `can-i-deploy`, teams still discover incompatibilities late, often after merge or in staging. Understanding the model changes contract testing from “extra tests” into release safety infrastructure.

### 5. An engineer who understands this will use contract tests alongside schema validation and higher-level behavioral tests, because each protects a different failure class.
The unaware engineer often replaces one with the other: “We have OpenAPI, so we don’t need contract tests,” or “We have contract tests, so integration tests are unnecessary.” That leaves blind spots. A working engineer uses schema validation for provider-wide structure, contract testing for consumer-specific boundary compatibility, and other tests for semantics and end-to-end behavior.

---
