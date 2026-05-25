## Metadata
- **Date:** 26-05-2026
- **Source:** 11_model_deployment_and_serving.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-11 · Model Deployment and Serving

The hardest part of machine learning is not training the model. It is the gap between a notebook that produces good predictions on your laptop and a system that produces good predictions for real users, at real traffic, on real hardware, for months. Most AI projects die in that gap. The model works. The deployment doesn't. And the team is surprised, because nothing in the modeling phase prepared them for it.

The reframe you need is this: a model is not a product. A serving system is. The model is one component inside a system that has to accept requests, validate inputs, run inference within a latency budget, return responses in a format the caller expects, log what happened, recover from failures, and keep doing all of that as the model is updated and the world shifts underneath it. When you say "we deployed the model," what you actually deployed is that whole apparatus. The model is the easy part to swap out. Everything else is what you live with.

Start with the serving environment, because it determines almost everything else. There are roughly three shapes a deployment takes. An API serves predictions on demand: a request comes in, the model runs, a response goes out, usually within hundreds of milliseconds. Batch serving runs predictions on a schedule against a pile of data — overnight, hourly, whenever — and writes results to a table. Edge deployment puts the model on the device itself: a phone, a browser, a sensor. Each of these has different constraints. An API needs to be fast and always up. A batch job needs to be cheap and finish before the next one starts. An edge model needs to fit in tight memory and run without a network. Picking the wrong shape is one of the more expensive mistakes you can make, because the rest of your stack — your hardware, your monitoring, your release process — is built around it.

Once you've picked a shape, you discover that the model you trained is too slow, too big, or both. This is where inference optimization comes in. Quantization shrinks weights from 32-bit floats to 8-bit integers and often costs you a percent or two of accuracy in exchange for a 4x speedup and a 4x reduction in memory. Pruning removes weights that contribute little to predictions. Distillation trains a smaller model to mimic a larger one. None of these are free, and all of them require you to re-validate that the optimized model still does what the original did. The optimized model is, technically, a different model. Treat it that way.

Then there is versioning, which is where teams that haven't shipped before tend to underestimate the work. You will deploy a new model. The new model will be worse than the old one in some specific way you didn't anticipate. You need to be able to find that out before all your traffic is on it, and you need to be able to roll back when you do. That means running two models side by side, routing some fraction of requests to each, comparing their outputs and their downstream business metrics, and having a clean way to promote the winner or kill the loser. If you can't do that, you are not deploying — you are flipping a switch and praying. The framework you choose for serving (TensorFlow Serving, Triton, KServe, or whatever your platform offers) earns its complexity here: it handles versioning, batching, and scaling so you don't have to write that code yourself.

Containerization is the boring layer that makes the rest of this possible. Your model runs against specific versions of specific libraries with specific CUDA drivers. The fact that it works on your laptop tells you nothing about whether it will work on a production server. Docker, or its equivalent, freezes the environment so that the model you tested is the model that runs. This is not optional in 2026. It is the floor.

The thread that ties all of this together is the latency budget. Every layer of the system — input validation, preprocessing, inference, postprocessing, serialization, the network — eats some of it. If your product needs a response in 200 milliseconds and your model takes 180, you have 20 milliseconds for everything else, and you do not have it. Working backwards from the latency budget tells you what model size you can afford, what hardware you need, whether you can batch requests, and whether you need a cache in front of the model. A team that doesn't know its latency budget is a team that will discover it the hard way, in a postmortem.

The skill this topic builds is the discipline of treating the model as one component in a system whose job is to keep working. Once you have that mindset, everything downstream — monitoring, retraining, debugging — has a place to live. Without it, every production incident feels like a surprise. With it, the surprises get smaller.

## Level 2 candidates

**Inference optimization: quantization and pruning** — Covers the techniques for shrinking model size and speeding up inference, primarily quantization (reducing numerical precision) and pruning (removing low-impact weights). Worth a deep dive because the trade-offs are non-obvious, the tooling has matured, and the difference between a naive and a well-optimized model is often the difference between viable and unviable economics.

**Batch vs. online serving** — Covers when to score data on a schedule versus on demand, and the architectural consequences of that choice. Worth its own treatment because the decision touches data infrastructure, latency expectations, cost, and how you handle failures, and most teams default to online serving when batch would have been simpler and cheaper.

**Model serving frameworks** — Covers the landscape of tools that expose models as APIs with batching, versioning, and scaling built in: TensorFlow Serving, Triton, KServe, and their managed equivalents. Worth a deep dive because the choice has long-term consequences and the frameworks differ meaningfully in what they assume about your stack.

**API design and latency budgets** — Covers how to design the prediction endpoint itself: input/output schemas, error handling, timeouts, and how to reason about end-to-end latency. Worth going deeper because the API is the contract your callers depend on, and bad early choices are expensive to undo.

**Model versioning and A/B testing** — Covers the mechanics of running multiple model versions in production, splitting traffic, measuring outcomes, and rolling back safely. Worth a deep dive because the cultural and tooling shift from "deploy and hope" to "deploy and measure" is the line between teams that improve their models and teams that ship once and freeze.

**Containerization with Docker** — Covers packaging a model and its dependencies into a reproducible image that runs identically across environments. Worth its own treatment because GPU drivers, CUDA versions, and Python dependency hell make ML containers meaningfully harder than typical web service containers.

**Edge deployment** — Covers running models on phones, browsers, and devices using TensorFlow Lite, ONNX, CoreML, and similar runtimes. Worth a deep dive because the constraints (memory, power, no network) and the tooling are entirely different from server-side deployment, and the format conversions are where most teams hit walls.

---
