## Metadata
- **Date:** 01-02-2026
- **Source:** Model-generated (Claude Sonnet 4.6)
- **Model:** claude-opus-4.6
- **Prompt:** cognitive-assets/prompts/competencies_db_level_2_post.txt

## LLM Processed Content

Most engineers use the word "mock" to mean "any fake thing I put in place of a real dependency during a test." This imprecision is not just a vocabulary problem. Each type of test double substitutes something different, verifies something different, and fails in a different way when misused. When you reach for a mock but the situation calls for a fake, or when you verify interactions with a mock when you should be verifying state with a stub, you get tests that are tightly coupled to implementation details, that pass when the real system is broken, and that break when you refactor code that still works. The choice of test double *is* a design decision about what your test actually measures. Getting it wrong means your test suite is confidently asserting things that don't matter.

## What a Test Double Actually Substitutes

A **test double** is any object that stands in for a real dependency during a test. The Level 1 post described unit tests as "fast, isolated tests that validate behavior in complete isolation from external dependencies." Test doubles are the mechanism that makes that isolation possible. But "standing in" for a dependency is not one thing. There are at least four meaningfully different ways to do it, and they differ along two axes.

The first axis is **what the double provides to the system under test**. Some doubles control the *indirect inputs* — the data your code receives from its dependencies. Others provide a *working alternative implementation* that behaves like the real thing but is cheaper to run.

The second axis is **what the double allows you to verify**. Some doubles exist purely to keep your code running during the test; you never inspect the double itself. Others exist specifically so you can assert things about how your code interacted with them.

These two axes produce the four types that matter in practice.

## Stubs: Controlling Indirect Inputs

A **stub** provides predetermined responses to method calls. Its job is to control what your system under test *receives* from its dependencies, so you can test how your code behaves under specific conditions. You never assert anything about the stub itself.

Consider an order service that depends on a payment gateway:

```python
# The stub
class AlwaysSuccessfulPaymentGateway:
    def charge(self, customer_id, amount):
        return ChargeResult(success=True, transaction_id="txn-stub-123")

# The test
def test_order_confirmation_includes_transaction_id():
    gateway = AlwaysSuccessfulPaymentGateway()
    service = OrderService(payment_gateway=gateway, inventory=real_or_other_double)
    
    confirmation = service.place_order(some_order)
    
    assert confirmation.transaction_id == "txn-stub-123"
```

The stub answers the question: "Given that the payment succeeds, does my order service do the right thing with the result?" You are testing your code's logic. The stub is scenery, not the subject.

Stubs are the right choice when you need to put the system under test into a specific state or condition — successful payment, failed payment, network timeout, empty response — and then verify the *output or state* of the thing you're actually testing. This is **state verification**: you check what your system produced, not how it talked to its dependencies.

## Mocks: Verifying Indirect Outputs

A **mock** is pre-programmed with expectations about how it will be called, and the test fails if those expectations aren't met. Its job is to verify that your code sends the right messages to its collaborators. This is **behavior verification**.

```python
def test_order_service_charges_correct_amount():
    gateway = Mock()
    gateway.charge.return_value = ChargeResult(success=True, transaction_id="txn-1")
    
    service = OrderService(payment_gateway=gateway, inventory=stub_inventory)
    service.place_order(Order(customer_id="cust-42", total=99.99, ...))
    
    gateway.charge.assert_called_once_with("cust-42", 99.99)
```

Here, the assertion is *about the mock itself*. You're verifying that your order service called `charge` with the right customer ID and the right amount. The mock isn't just scenery — it's the measurement instrument.

Mocks are the right choice when the *interaction itself is the behavior you care about*. Sending an email after order placement, publishing an event to a message bus, writing an audit log — these are cases where the side effect is the whole point, and there's no meaningful return value to check.

The critical distinction: stubs answer "given this input from my dependency, does my code produce the right output?" Mocks answer "does my code talk to its dependency in the right way?" These are different questions. Confusing them is the root cause of most test double misuse.

## Fakes: Lightweight Working Implementations

A **fake** is a real, working implementation that takes a shortcut that makes it unsuitable for production. An in-memory database instead of PostgreSQL. A local filesystem store instead of S3. A hash map pretending to be a cache server.

```python
class InMemoryInventoryService:
    def __init__(self):
        self.stock = {}
    
    def add_stock(self, item_id, quantity):
        self.stock[item_id] = self.stock.get(item_id, 0) + quantity
    
    def check_stock(self, item_id, quantity):
        return self.stock.get(item_id, 0) >= quantity
    
    def reserve(self, item_id, quantity):
        if not self.check_stock(item_id, quantity):
            raise OutOfStockError()
        self.stock[item_id] -= quantity
```

Unlike a stub, this fake has *real behavior*. You can add stock, check stock, reserve items, and the internal state changes accordingly. Unlike a mock, you don't assert how it was called — you use it as a working dependency and verify the outcome of the whole operation.

Fakes are the right choice when your test needs a dependency that *behaves realistically* but where the real thing is too slow, too expensive, or too difficult to set up. They shine in scenarios where the interaction between your code and the dependency is complex enough that a stub's canned responses would be too simplistic to exercise the real logic paths.

The cost of fakes is that they are real code. They need to be written, maintained, and — ideally — validated against the real implementation they replace. A fake that behaves differently from the real system is a lie that your tests tell you.

## Spies: Recording What Happened

A **spy** wraps an object (real or not) and silently records every interaction, letting you inspect those interactions after the fact. The difference from a mock is timing and coupling: a mock's expectations are declared *before* the act, and the test fails immediately if the expectation isn't met. A spy records everything and you query it *after* the act, asserting only on the interactions you care about.

```python
def test_order_service_publishes_event():
    event_bus = SpyEventBus(real_event_bus)
    service = OrderService(event_bus=event_bus, ...)
    
    service.place_order(some_order)
    
    assert event_bus.was_called_with("OrderPlaced", order_id=some_order.id)
    # We don't care about other calls to event_bus — only this one
```

Spies are less prescriptive than mocks. A mock that expects exactly two calls in a specific order will fail if your refactored code makes three calls or changes the order. A spy lets you assert on the things that matter and ignore the rest. This makes spy-based tests marginally less brittle, though they still couple you to interaction patterns.

In practice, many modern mocking frameworks (Mockito, unittest.mock, Jest) blur the line between mocks and spies. When you use `unittest.mock.Mock()` in Python and call `assert_called_with` after the fact, you're using it as a spy even though the class is called `Mock`. The conceptual distinction matters more than the framework's naming.

## The Substitution Boundary

Every time you use a test double, you are drawing an invisible line around the system under test. Everything inside the line runs as real code. Everything outside the line is replaced with a double. **Where you draw this line determines what your test actually tests.**

Draw the boundary too tightly — replace every collaborator of a class with a mock — and your test verifies only that the class calls its collaborators in the right order with the right arguments. It tests *wiring*, not *behavior*. You can refactor the internal logic of the class, maintaining identical external behavior, and every test breaks because the call sequence changed.

Draw the boundary too loosely — use all real dependencies — and you're writing an integration test. That's not wrong, but it's not a unit test, and it comes with integration test costs: slower execution, infrastructure requirements, harder failure diagnosis.

The skill is in drawing the boundary at the level where your test verifies something you genuinely care about. For a function that transforms data, you probably don't need any doubles — pass data in, check data out. For a service that orchestrates calls to three external systems, you need doubles for those external systems, but you might let the internal helper classes run as real code. The boundary should follow the architectural seam, not the class hierarchy.

## Where Test Doubles Break

### Mock-Heavy Tests That Test Implementation

The most common failure mode is overusing mocks for behavior verification when state verification would suffice. You see this in codebases where every test constructs five mocks, wires them together, calls the method under test, and then asserts that each mock was called exactly once with specific arguments. These tests are exhausting to read, break every time someone refactors, and tell you almost nothing about whether the system works correctly.

The symptom is: your tests break when you change *how* code works but not *what* it does. If you refactor a method to batch two database calls into one for performance, and a dozen tests break because they expected two calls instead of one, those tests were testing implementation details. They provided negative value — they cost time to fix and never could have caught a real bug.

### Stubs That Encode Stale Assumptions

Every stub contains a hardcoded assumption about what the real dependency returns. If the real dependency changes — a new required field in the response, a different error format, a changed status code — your stubs still return the old structure. Your tests pass. Production breaks.

This is the fundamental limitation of stubs: they freeze a dependency's behavior at the time you wrote the stub. They don't keep up with reality. Contract tests (as described in the Level 1 post) exist specifically to close this gap, but many teams use stubs without contract tests and silently accumulate incorrect assumptions.

### Fakes That Diverge

A fake is a parallel implementation of a real system. Two implementations of the same behavior will eventually diverge. Your in-memory database fake doesn't enforce the same constraint semantics as PostgreSQL. Your fake S3 doesn't replicate eventual consistency or the exact error behavior of the real service. Tests pass against the fake and fail in production because the fake was a simplification, and the behavior that matters was in the part that was simplified away.

The discipline required: fakes should be tested against the same interface contract as the real implementation. Some teams run their test suite against both the fake and the real dependency in CI, using the real dependency run to validate that the fake hasn't drifted. This is expensive but it's the only reliable way to maintain a fake long-term.

### The Green Suite, Broken Integration

The deepest failure mode is structural, not specific to any one type of double. A team with 95% unit test coverage, all using test doubles for external dependencies, can have a perfectly green test suite and a completely broken system. Every class works perfectly against its doubles. No class works correctly against the real dependencies.

This happens because test doubles verify that your code works *given your assumptions about the outside world*. They cannot verify that your assumptions are correct. Only integration tests against real dependencies — or contract tests that formalize those assumptions and verify them independently — close the loop.

## The Mental Model

Test doubles are not interchangeable. Each type controls a different axis of the test. Stubs and fakes control the *environment* — they shape what your code sees, so you can test your logic under specific conditions. Mocks and spies verify the *interactions* — they check that your code communicates correctly with its collaborators. The choice between them is a choice about what your test measures.

The question to ask before reaching for any test double is: "Am I testing what my code *does*, or am I testing how my code *talks*?" If the answer is what it does, use stubs or fakes and verify state. If the answer is how it talks — because the communication *is* the behavior — use mocks or spies and verify interactions. If you can't clearly articulate which one, you don't yet know what your test is for.

## Key Takeaways

- **Stubs control indirect inputs** — they provide canned responses so you can test how your code behaves under specific conditions, and you verify the output of your code, not the stub itself.
- **Mocks verify indirect outputs** — they assert that your code called the right methods with the right arguments, making them appropriate only when the interaction itself is the behavior you care about.
- **Fakes are working implementations with shortcuts** — they have real behavior (unlike stubs) but are unsuitable for production, and they require ongoing maintenance to prevent divergence from the real system.
- **Spies record interactions for after-the-fact verification**, making them less prescriptive and less brittle than mocks, though most modern frameworks blur the distinction between the two.
- **The substitution boundary — where you draw the line between real code and test doubles — determines what your test actually tests.** Drawing it too tight tests wiring; drawing it too loose tests integration.
- **Overusing mocks for behavior verification produces tests that break on every refactor** without catching real bugs, because they assert *how* code works rather than *what* it does.
- **Every stub and fake encodes assumptions about real dependencies that go stale over time.** Without contract tests or validation against real implementations, a green test suite can mask broken integrations.
- **Before choosing a test double, ask whether you are testing what your code does or how your code talks** — that question determines whether you need state verification (stubs/fakes) or behavior verification (mocks/spies).


<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

Tests are supposed to tell you whether your system still works. But a lot of test suites end up telling you something weaker and less useful: that the code still makes the same calls in the same order to the same collaborators that it did when the test was written. That sounds close to correctness, but it is not correctness. It means you can get a green suite while the real system is broken, or a red suite after a harmless refactor that preserved behavior.

This happens because “mock” is often used as a catch-all for any fake dependency in a test, even though different test doubles answer different questions. If you use the wrong one, your test measures the wrong thing. The concrete failure modes are familiar: tests that shatter when you change internals but not outputs, tests that pass against hardcoded assumptions while the real API has changed, and tests that only prove your code works against a toy replacement of the real world.

So this topic matters because choosing a test double is not a small implementation detail. It is you deciding what evidence the test will collect. If you do not see that clearly, you can spend a lot of time maintaining tests that are expensive, brittle, and misleading.

---

## What You Need To Know First

### Dependency
A dependency is any other thing your code relies on to do its job: a database, payment gateway, cache, clock, file store, message bus, or even another class. In tests, dependencies matter because they bring in slowness, nondeterminism, cost, and setup complexity. Test doubles exist so you can replace those real dependencies when you do not want them inside the test.

### System under test
The system under test is the specific piece of code the test is trying to learn about. Sometimes that is one function, sometimes one class, sometimes a small cluster of collaborating classes. This matters because test doubles sit outside that boundary. If you are unclear about what is “the thing being tested,” you will also be unclear about what should stay real and what should be replaced.

### State verification vs interaction verification
State verification means you run the code and then inspect its output or resulting state: returned value, saved record, changed object, emitted result. Interaction verification means you inspect how the code talked to another object: whether method X was called, with what arguments, how many times. This distinction is the backbone of the article: different doubles support different kinds of verification.

### Integration test
An integration test runs real components together to see whether they actually work as a combined system. It is broader and more realistic than a tightly isolated unit test, but usually slower and harder to diagnose when it fails. You need this idea because the article is not saying “replace everything with doubles”; it is saying the boundary between real dependencies and doubles determines what kind of test you are writing.

---

## The Key Ideas, Connected

### 1. A test double is any replacement for a real dependency, but not all replacements do the same job.
The useful starting point is that “test double” is the umbrella term, not the specific tool. Engineers often stop there and think the only question is “real dependency or fake one?” But the actual question is more specific: what kind of substitute are you putting there, and what do you want it to let the test prove?

That matters because replacing a dependency can serve two different purposes. One purpose is to control what your code receives from the outside world. Another is to observe how your code talks to the outside world. Once you see those as different jobs, you can see why one generic category is not enough.

### 2. The first major split is between doubles that shape inputs and doubles that measure interactions.
Some doubles exist to create conditions for the test: “pretend payment succeeded,” “pretend inventory is empty,” “pretend the timeout happened.” Their role is to feed your code a controlled environment. Other doubles exist so the test can later ask, “did my code send the right message to its collaborator?”

This split is important because it maps directly to two kinds of testing evidence. If you care about your code’s result under a given condition, you want a double that shapes inputs. If you care that your code communicated correctly with another component, you want a double that records or enforces interactions. That distinction sets up the specific types.

### 3. A stub is for controlling indirect inputs, so the test can verify your code’s resulting behavior.
A stub returns predetermined answers when your code calls it. The test uses that to place the system under test into a known situation. For example: the payment gateway says success, or says decline, or raises a timeout. The test then asks what your code did in response.

The mechanism here is simple: the stub is not being judged. It is just supplying a condition. The actual assertion is about your code’s output or state. That is why the article says the stub is scenery, not the subject. Seeing that leads to the next idea: sometimes the interaction with the dependency is itself the behavior you care about, and then a stub is not enough.

### 4. A mock is for verifying indirect outputs, when the act of calling the dependency is the behavior.
A mock is configured so the test can assert that certain calls happened: method called once, with these arguments, maybe in this order. Here the dependency replacement is not just providing a condition. It is acting as a measuring device for communication.

Why does this become necessary? Because some behaviors do not leave a convenient state to inspect. If the important thing is “an email was sent,” “an event was published,” or “an audit record was written,” the evidence lives in the interaction. In those cases, checking only return values may miss the thing the code was meant to do. That is when behavior verification is appropriate.

But this also explains the danger: if you use mocks when you could have verified state, you start asserting communication patterns that are only one possible implementation. That pushes us to a richer form of replacement.

### 5. A fake is a lightweight real implementation, used when canned answers are too simple.
A fake is not just a response script like a stub. It has actual working behavior, but implemented with shortcuts that make it practical for tests and unsuitable for production. An in-memory store is the classic example: it really stores, retrieves, and mutates data, but without persistence, network, concurrency semantics, or production constraints.

This matters when your code’s logic depends on a dependency behaving like a small system, not just returning one canned value. A stub can say “stock exists,” but a fake inventory service can model stock changing over time as orders reserve items. The more the code under test relies on ongoing realistic behavior, the more useful a fake becomes.

But because a fake contains logic, it can drift away from the real system. That naturally leads to another category: what if you want real behavior but also visibility into what happened?

### 6. A spy records interactions after the fact, giving you looser interaction checks than a mock.
A spy observes calls and stores them so the test can inspect them later. Unlike a strict mock, it usually does not require declaring every expectation up front. That means the test can assert only on the interactions it actually cares about and ignore incidental ones.

Mechanically, this reduces coupling. A strict mock often encodes a full script: exactly these calls, exactly this order. A spy says, more or less, “run the system, then let me inspect whether this meaningful interaction happened.” That makes the test somewhat less brittle because it is asserting less about internal choreography.

This distinction matters because it reveals a broader truth: the more precisely your test constrains internal interaction patterns, the more likely it is to break during refactoring. Which brings us to the boundary question.

### 7. Choosing a test double is really choosing the substitution boundary around the system under test.
Every test draws a line: code inside the line runs for real, code outside the line is substituted. The type and number of doubles tell you where that line is. If you replace every collaborator with mocks, your test is examining a very small unit in extreme isolation. If you keep many real collaborators and substitute only external infrastructure, the test covers a larger slice of behavior.

The mechanism is direct: whatever is doubled is no longer being tested as real code in that test. So if you mock out all collaborators, you are not learning whether those collaborators and the main class work together in reality. You are learning whether your class sends the expected messages to stand-ins. That is why overly tight boundaries tend to produce wiring tests instead of behavior tests.

And if you draw the line too loosely, you stop writing a focused unit test and start paying integration-test costs. So the real engineering skill is not “always mock” or “always use real code”; it is placing the boundary where the evidence matches the question you care about.

### 8. The most common testing failure is measuring implementation details instead of behavior.
When tests are mock-heavy, they often assert call counts, call order, and exact argument flows that are merely one implementation strategy. If you refactor the code to produce the same external result in a cleaner or faster way, those tests fail even though the behavior is still correct.

The underlying mechanism is that interaction assertions bind the test to internal structure. They say not just what must be true, but how it must have been achieved. That is sometimes necessary, but often accidental. The result is brittle tests that create drag on design improvement and provide little protection against actual regressions.

Once you see that, the next failure mode is easier to understand: even when the tests are not brittle, doubles can encode assumptions that stop matching reality.

### 9. Stubs and fakes can silently freeze stale assumptions about real dependencies.
A stub hardcodes a response shape. A fake hardcodes a simplified model of behavior. Neither automatically updates when the real dependency changes. So your tests can continue passing while production fails because the real API added a field, changed an error format, enforced a constraint differently, or exposed timing behavior your fake does not model.

This is not a minor edge case. It is a structural limit of doubles: they only represent your assumptions about the outside world, not the outside world itself. That is why a green isolated suite cannot prove the whole system integrates correctly. To close that gap, you need integration tests, contract tests, or some validation of fakes against the real implementation.

That leads to the final idea, which is the one you want to carry into practice.

### 10. The real decision is: are you testing what the code does, or how it talks?
This is the compact mental model that organizes everything else. If the behavior you care about is the outcome your code produces, then shape the environment with stubs or fakes and verify state. If the behavior you care about is the communication itself, then use mocks or spies and verify interaction.

This question matters because it forces clarity before you write the test. If you cannot answer it, you probably do not yet know what evidence your test should collect. And if you do not know what evidence you need, you are likely to reach for whatever your framework makes easy, which is how brittle and misleading tests accumulate.

---

## Handles and Anchors

### 1. “Is the dependency part of the scenery, or part of the measurement?”
If the dependency is just there to create conditions, use a stub or fake. If the dependency is what you are measuring, use a mock or spy. This is a simple way to decide whether you are controlling the environment or inspecting communication.

### 2. “Am I testing the result, or the conversation?”
That single question captures the core split. Results push you toward state verification. Conversations push you toward interaction verification. It is the fastest practical check when writing a new test.

### 3. Think of the substitution boundary as drawing a circle on a whiteboard.
Everything inside the circle is real code this test is actually exercising. Everything outside is simulated. If your circle is tiny and surrounded by mocks, you are mostly testing coordination. If your circle is broad and uses real collaborators, you are testing more real behavior but paying more setup and runtime cost.

---

## What This Changes When You Build

### 1. An engineer who understands this will default to state verification when possible because it survives refactoring better.
Instead of immediately mocking every collaborator, they will ask whether the test can assert on a returned value, changed state, persisted record, or emitted artifact. The unaware engineer often inherits the framework default of “mock all dependencies,” and ends up with tests that fail whenever internals are reorganized, even if user-visible behavior is unchanged.

### 2. An engineer who understands this will use mocks only when the interaction itself is the behavior because otherwise the test couples itself to implementation.
For something like “publish this event” or “send this email,” they will verify the call because that call is the outcome. But for logic that transforms inputs into outputs, they will avoid mock assertions on every collaborator. The unaware engineer writes choreography tests that assert exact call sequences and then wonders why optimization or cleanup causes widespread test breakage.

### 3. An engineer who understands this will choose fakes when realistic dependency behavior matters because a stub may be too shallow to exercise real logic paths.
If a service’s behavior depends on stateful interactions with storage, cache, or inventory, they may use an in-memory fake rather than a pile of canned stub responses. The unaware engineer often stacks increasingly elaborate stubs until the test no longer resembles the real dependency model and misses meaningful paths.

### 4. An engineer who understands this will treat stubs and fakes as assumptions that need validation because isolated tests cannot prove integration correctness.
They will add contract tests, integration tests, or periodic runs against real dependencies to detect drift. The unaware engineer trusts the green unit suite as if it validated production reality, and then gets surprised when the external API changed months ago and none of the isolated tests noticed.

### 5. An engineer who understands this will draw the test boundary at architectural seams rather than at arbitrary class edges because the boundary determines what the test actually tests.
They may keep internal helpers real and substitute only true external systems like databases, queues, gateways, or clocks. The unaware engineer often mocks every constructor parameter by habit, producing tiny tests that only verify object wiring and never exercise the meaningful collaboration inside the module.

---

</details>
