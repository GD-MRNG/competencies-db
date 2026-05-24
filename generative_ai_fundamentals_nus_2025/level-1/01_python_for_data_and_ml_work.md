## Metadata
- **Date:** 24-05-2026
- **Source:** 01_python_for_data_and_ml_work.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-01 · Python for Data and ML Work

Most people who arrive at machine learning already know Python. That is the trap. The Python you wrote to glue together a web scraper, automate a report, or pass a coding interview is not the Python that survives contact with a training loop. The vocabulary overlaps almost completely — same syntax, same standard library, same `for` loops — but the mental model underneath is different, and the gap shows up at exactly the moment you can least afford it: when something has gone wrong inside a model that took six hours to start training.

The shift you need to make is from thinking about Python as a sequence of instructions to thinking about Python as a way of expressing operations on data. In scripting Python, you write a loop because a loop is the obvious way to do a thing to each item in a list. In ML Python, writing that loop is usually a mistake — not because it is wrong, but because it is slow by orders of magnitude and it does not compose with the libraries you are about to spend most of your time inside. NumPy, Pandas, PyTorch, and TensorFlow all assume you will hand them whole arrays and let them dispatch to optimised C or CUDA code underneath. The moment you reach for an explicit `for i in range(len(x))`, you have stepped outside the system the libraries were designed for.

This is the first conceptual pivot: vectorisation. A NumPy array is not a list of numbers; it is a contiguous block of memory with a shape and a dtype, and operations on it are operations on the whole block at once. Pandas DataFrames extend this idea to labelled, heterogeneous columnar data. Once you internalise that `df['price'] * 1.2` multiplies a million rows in a single dispatched call, and that writing `for row in df.iterrows()` to do the same thing is hundreds of times slower, you start to read and write data code differently. You stop asking "how do I iterate?" and start asking "what is the shape of what I have, and what is the shape of what I want?"

The second pivot is composition. ML frameworks are not just function libraries; they are object systems with conventions. A PyTorch model is a class that inherits from `nn.Module`. A custom dataset is a class that implements `__len__` and `__getitem__`. A training callback is an object passed into a trainer that gets its methods called at specific points in a lifecycle. If you cannot read a class definition, trace a method resolution order, or understand what `super().__init__()` is doing, framework code will look like incantation. You will copy examples that work and be unable to modify them when they don't. Object-oriented Python is not a sophistication you can defer; it is the literal interface to the tools.

The third pivot is debugging. In ordinary Python, when a line fails, the stack trace points at the line and you fix it. In ML code, the line that fails is rarely the line that caused the problem. A shape mismatch on layer seven is almost always a wrong assumption made about the data three preprocessing steps earlier. A NaN in your loss is a divide-by-zero or an exploding gradient that happened thousands of iterations before the symptom appeared. A silent CUDA error can take down the kernel without a Python traceback at all. Defensive coding — asserting shapes, checking dtypes, plotting intermediate values — is not paranoia in this world; it is the only way to pin down problems that span layers of abstraction. Knowing how Python actually executes, what exceptions propagate where, and how to read a traceback that crosses into compiled code is the difference between a stuck training run and a fixed one.

The fourth pivot is visual. You cannot debug a model by reading its weights. You debug by looking — at a loss curve, at a confusion matrix, at sample predictions, at a histogram of activations. Matplotlib is not a presentation tool in this context; it is an instrument. The practitioners who train models well are the ones who, when something feels off, instinctively plot it. Loss going up? Plot it against the learning rate schedule. Validation diverging from training? Plot both. Predictions look weird? Plot the input alongside them. Treating visualisation as a first-class debugging tool, not a final-report afterthought, separates people who guess at what is wrong from people who see it.

What you are building, across all of this, is fluency in a particular dialect: Python that thinks in arrays, composes with framework objects, fails informatively, and renders itself visually when interrogated. None of it is glamorous, and none of it is what people mean when they talk about "doing AI." But every topic downstream — backpropagation, attention, RLHF, RAG — is going to be expressed in this dialect. The clearer your Python, the more transparent the rest of the curriculum becomes. The fuzzier your Python, the more often you will mistake a bug for a concept you don't understand.

## Level 2 candidates

**Object-oriented programming in Python** — Covers classes, instances, inheritance, and the special methods (`__init__`, `__call__`, `__getitem__`) that ML frameworks rely on. Worth deeper study because reading framework source code — knowing what `nn.Module` actually does when you subclass it — is the difference between using a library and being able to extend or debug one.

**Pandas data manipulation** — Covers DataFrames, indexing, groupby, merge/join, and the vectorised idioms that make Pandas fast. The mental model of operations-over-columns rather than loops-over-rows is non-obvious and is where most data-preprocessing performance problems are silently created; getting this right pays off in every dataset you ever touch.

**Matplotlib and visualisation for ML debugging** — Covers the plotting primitives needed for loss curves, confusion matrices, activation histograms, and sample inspection. Worth its own treatment because visualisation is a debugging skill, not a reporting skill, and the practitioners who use it instinctively diagnose problems faster than those who treat plots as the last step.

**NumPy and vectorisation** — Covers arrays, shapes, broadcasting, and the mental shift from element-wise iteration to whole-array operations. This is the foundational layer beneath both Pandas and the deep learning frameworks; broadcasting in particular is a small set of rules that, once internalised, removes an entire class of confusing errors.

**Exception handling and the Python execution model** — Covers how exceptions propagate, how tracebacks read across compiled boundaries, and why ML errors so often surface far from their cause. Worth deeper attention because debugging strategy in ML code depends on understanding what Python is and is not telling you when something fails inside a training loop.

---