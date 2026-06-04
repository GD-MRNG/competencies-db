## Metadata
- **Date:** 05-06-2026
- **Source:** 11_graph_based_workflow_and_llm_routing.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-11 · Graph-Based Workflows and LLM Routing

There is a moment in every agentic project where you realise the pure loop is failing you. The agent works, mostly, but it wanders. It re-fetches data it already had. It skips the validation step you assumed it would always run. It picks the right tools in the right order eighty percent of the time, which is another way of saying it picks the wrong path one run in five. You add more instructions to the system message. You add more constraints. And eventually you notice that what you actually want is not more prompting — it's structure. You want to guarantee that the data gets fetched before it gets analysed, and analysed before the agent decides what to do. You want the shape of the work to be fixed, even if the reasoning inside each step is not.

This is what graph-based workflows give you. A graph is a map of the work: nodes are steps, edges are transitions between them. Some nodes are deterministic functions (fetch this URL, write this row to the database, format this output). Other nodes are agents or LLM calls that handle the parts you genuinely cannot script. The graph constrains the overall flow; the agents handle the ambiguity within it. You are no longer asking the model to invent the pipeline on every run. You are asking it to make the specific decisions that only a model can make, inside a pipeline you designed.

The right way to see this is as a third point on a spectrum you already know. On one end is the hard-coded workflow: a Python script that calls step A, then step B, then step C. Cheap, predictable, brittle the moment the world deviates from your assumptions. On the other end is the pure agent loop: a model in a while-loop choosing its next tool from scratch every iteration. Flexible, capable of handling surprises, prone to drift and unbounded cost. Graphs sit in the middle and give you the dial. You decide which parts of the system are fixed — because you know the right answer, or because the cost of getting it wrong is too high to leave to a model — and which parts stay dynamic, because the input is genuinely ambiguous and reasoning is genuinely required.

The two pieces that make this work are conditional routing and state. Routing is the question of which edge to follow when a node has more than one out. Sometimes the router is a classifier — a small model whose only job is to label the input and pick a branch. Sometimes the router is the agent itself, returning a structured output that names the next node. Sometimes the router is a plain Python function inspecting the state. The point is that the decision is explicit and inspectable. You can log it, test it, and reason about it. Compare this with a pure agent loop, where "why did it take this path" is buried in the model's reasoning over fifty turns. In a graph, branching is a first-class concept.

State is the other half, and it is the part people underestimate. In a single agent loop, state is just the message history — everything the model has seen, accumulated in one list. In a graph, state has to flow between nodes that may not share the same context. You need to decide what each node reads from the shared state, what it writes back, and how parallel branches reconcile when they merge. Get this right and your graph is debuggable: you can pause at any node, inspect the state, and understand exactly what the system knows and what it is about to do. Get it wrong and you have race conditions, stale data, and nodes that fail because an upstream branch never wrote the field they expected. State management is where graph-based systems either become more reliable than agents or quietly inherit the worst of both worlds.

Graphs also compose. A node in your graph can itself be a sub-graph — a self-contained workflow with its own internal nodes and edges, exposed to the parent as a single step. This is how you manage complexity at scale. A "research" sub-graph might internally fan out across several sources, deduplicate, and summarise, but to the parent graph it is just a node that takes a query and returns findings. The same discipline you apply to breaking a large program into functions applies here: hide internal complexity behind a clean interface, and the top-level graph stays readable.

The frameworks in this space — LangGraph is the obvious current example, though specific tools shift quickly and you should check what's actively maintained when you read this — give you the primitives: typed state objects, node definitions, conditional edges, visualisation. They are not magic. You can build the same thing with a dictionary, a dispatch table, and some discipline. The reason to use a framework is the visualisation and the conventions; the reason to understand the underlying model is so you can debug it when the framework's abstraction leaks.

The practical takeaway is that graphs are not a replacement for agents or workflows — they are the tool you reach for when neither is enough on its own. If you find yourself adding more and more constraints to a pure agent's system message to force it down a particular path, you are reinventing a graph badly. If you find your hard-coded workflow needs an "and then figure out what to do" step in the middle, you are reinventing a graph badly. Make the structure explicit, put the reasoning where reasoning is needed, and let the rest be code. That is the whole pattern.

## Level 2 candidates

**Graph Definition and Visualisation** — How to define nodes and edges in code, and how to render the resulting graph as a diagram you can show a teammate. Worth a deep dive because the design phase — drawing the graph before writing it — is where most of the value lives, and most engineers skip it.

**Conditional Routing and Decision Points** — The different ways to implement the "which edge do I follow" question: classifier nodes, structured-output routers from the agent itself, deterministic functions over state. Each has different tradeoffs in transparency, latency, and testability, and choosing well is non-obvious.

**Sub-Graphs and Hierarchical Composition** — How to break a large graph into reusable, encapsulated sub-graphs with clean state interfaces. Deserves its own treatment because composition is where graph-based systems either scale gracefully or collapse into unreadable spaghetti.

**State Management in Graphs** — The schema of the shared state object, what each node is allowed to read and write, and how parallel branches merge their writes without corrupting each other. This is the single most common source of bugs in graph-based systems and warrants careful, example-driven treatment.

**Graphs vs. Pure Agent Loops: When to Choose Which** — A decision framework for when the added structure of a graph is worth the upfront design cost, versus when a pure agent loop will get you there faster. The Level 1 post sketches this, but the operational heuristics — task ambiguity, failure cost, observability needs — deserve their own pass.

---