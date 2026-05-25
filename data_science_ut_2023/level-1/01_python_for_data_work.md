## Metadata
- **Date:** 26-05-2026
- **Source:** 01_python_for_data_work.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-01 · Python for Data Work

Python is not a subject you study; it is the medium you think in. This is the reframe that the 2023 curriculum got wrong, and it is the reframe that costs people the most time when they come back to data work in 2026. If you treat Python as a topic — something to be "learned" alongside statistics and machine learning — you will keep reaching for it as a tool, switching contexts, looking up syntax, breaking flow. If you treat it as the language you do data work in, the question stops being "do I know Python?" and becomes "how fast can I move from a question to an answer without leaving the keyboard?"

That speed is the actual skill. Not knowing every method on a DataFrame, not memorizing the standard library, not writing elegant one-liners. Speed: how quickly you can read a file, reshape it, check an assumption, and move on. The bottleneck in real data work is almost never the algorithm — it is the dozens of small interrogations you make of the data before you ever train a model. If each of those takes you two minutes instead of fifteen seconds, you will lose entire days per project, and worse, you will avoid asking questions you should be asking because asking them is too expensive.

The mental model worth holding is this: your Python environment is a workbench, and a workbench is judged by how fast you can pick up a tool, use it, and put it down. Three things determine that speed. The first is the libraries you reach for by default. The second is whether your code runs fast enough that you stay in the loop instead of waiting on it. The third is whether, when something goes wrong — and it will, constantly, because real data is messy — you can find the problem in seconds rather than minutes.

The library defaults have shifted, and this is the part where 2023 muscle memory will actively hurt you. Pandas, which was the default DataFrame library for a decade, has been dethroned for new work by Polars. Polars is faster — often by an order of magnitude on real datasets — but the more important difference is that it is honest about nulls and types in a way Pandas never was. Pandas will silently coerce, silently broadcast, silently produce a result that looks right and is wrong. Polars makes you say what you mean. The speed is what gets you to try it; the honesty is what keeps you on it. You lose some ecosystem maturity (older tutorials, some integrations) and you gain a tool that does not lie to you.

DuckDB is the other shift, and it is a quieter one. DuckDB is an in-process SQL engine that reads CSVs, Parquet files, and DataFrames directly, with no setup. It has become the default tool for "does this query make sense?" — the quick interrogation you would otherwise do by writing five lines of Pandas, getting it wrong, fixing it, and finally seeing the answer. With DuckDB you write the SQL you would have written anyway, against the file you already have, and get the answer in one shot. The point is not that SQL is better than Python; the point is that the friction of switching tools is gone, so you stop avoiding the right tool for the question.

Underneath the library choices sit two skills that compound across everything you do. The first is recognizing when your code is looping where it should be vectorizing — when you are iterating row by row in Python while NumPy or Polars sits underneath you, ready to do the same operation in parallel C code a hundred times faster. This is not a stylistic preference. It is the difference between a transform that takes 200 milliseconds and one that takes 30 seconds, and that difference determines whether you stay in flow or go make coffee. The second is profiling — knowing where your code is actually slow, which is almost never where you guessed. Both of these are habits, not knowledge. You build them by paying attention when something feels slow, not by reading about them.

Type hints deserve a mention because they are quietly the highest-leverage habit you can adopt in data code. They are not documentation. They are a contract — a declaration that this function takes a DataFrame with these columns and returns one with those columns — and your editor will catch the misalignment before you run the code. In data work, where most bugs are shape mismatches and type coercions, this catches the class of error that eats the most time.

The practical takeaway is narrow but important. The Python worth learning is the Python that keeps you in flow: defaults that don't lie to you (Polars), tools that don't make you switch context (DuckDB), code that runs fast enough to stay in the loop (vectorization, profiling), and contracts that catch mistakes before you run them (type hints). Everything else — the elegant comprehensions, the clever decorators, the deep standard library — is optional. The goal is not to know Python. The goal is to think in it.

## Level 2 candidates

**Polars over Pandas** — Covers why Polars has replaced Pandas as the default DataFrame library for new work, what you give up (ecosystem maturity, older tutorials, some integrations), and what you gain (speed, explicit null handling, lazy evaluation). Worth deeper treatment because the migration is not just syntactic — Polars asks you to think about data transforms differently, and that mental shift is where the real productivity gain lives.

**Vectorization and broadcasting** — Covers how to recognize when your code is looping in Python while the underlying library is ready to parallelize, and how to rewrite it. Worth depth because the gap between vectorized and looped code is often 50–100x, and most people do not see the loop until they profile.

**Type hints and debugging in data code** — Covers why type hints function as contracts in data pipelines (not just documentation), how to use them with DataFrames specifically, and how they shorten debug cycles. Worth depth because data bugs are mostly shape and type mismatches, and the tooling around typed DataFrames has matured enough that this is now practical, not aspirational.

**Writing fast iteration loops** — Covers how to structure code, notebooks, and caching so that you can rerun an experiment in under ten seconds instead of two minutes. Worth depth because iteration speed compounds: it determines how many questions you ask, which determines how good your final answer is.

**Profiling: memory and time** — Covers the practical tools (cProfile, line_profiler, memory_profiler, and their modern equivalents) and the habit of measuring before optimizing. Worth depth because almost everyone optimizes the wrong thing the first time, and the cost of guessing wrong is high.

**DuckDB as a Python companion** — Covers using DuckDB to query files and DataFrames directly from Python without leaving your environment, and when this beats writing Pandas or Polars. Worth depth because the workflow it enables — SQL against any file, instantly — eliminates a context switch most people don't realize they're paying for.

---