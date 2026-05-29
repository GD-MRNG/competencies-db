## Metadata
- **Date:** 24-05-2026
- **Source:** 07_analysis_and_decision_making.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-07 · Analysis and Decision-Making

The most common mistake leaders make with AI is asking it to decide. The second most common is refusing to let it near their decisions at all. Both errors come from the same misunderstanding: treating analysis as a single act rather than a stack of distinct cognitive moves, some of which AI handles brilliantly and some of which it cannot do at all. Once you separate the layers, the question stops being "should I use AI for this decision?" and becomes "which parts of this decision is AI actually good for?"

Analysis, when you look at it carefully, is three different kinds of work stacked on top of each other. There is the structuring work — choosing the lens, the framework, the way of cutting up the problem. There is the generation work — producing options, scenarios, counterarguments, and edge cases that fill in the structure. And there is the judgment work — deciding which lens fits your actual situation, which option is feasible given context you cannot fully articulate, and what matters enough to act on. AI is genuinely strong at the first two. It is genuinely weak at the third. The leverage is in moving the first two off your plate so you have more time and clarity for the third.

The structuring layer is where AI is most quietly useful. Ask it to give you five frames for a pricing decision and you will get Porter's five forces, jobs-to-be-done, willingness-to-pay segmentation, competitive anchoring, and unit-economics modelling — produced in seconds, with the right vocabulary, ready to adapt. You did not need to remember every framework you have ever read. You did need to recognise which one cuts your problem the right way, and that recognition is yours, not the model's. The same is true when you ask for stakeholder maps, decision matrices, or risk taxonomies. The structuring is commodity. The selection is judgment.

The generation layer is where AI's volume advantage shows up most cleanly. Humans are bad at generating options under pressure — we tend to produce two or three and then anchor. AI will produce ten without flinching, including the obvious ones you would have reached anyway, the obviously bad ones you would have dismissed, and one or two genuinely useful ones you would not have considered. The same applies to scenarios ("what would have to be true for this to fail?"), to counterarguments ("steel-man the opposite position"), and to assumption extraction ("list every unstated premise in the following plan"). The volume itself is the value. You are not looking for the right answer in the list; you are looking for the option you missed.

The judgment layer is where AI fails, and it fails in a particular way that is dangerous if you do not see it. AI does not know which lens matters for your specific organisation, because it does not know your organisation. It does not know which option is feasible, because feasibility depends on relationships, history, political capital, and constraints you have never written down. It does not know what actually matters, because mattering is a function of strategy and identity that lives in your head and your team's, not in the prompt. When AI produces a confident recommendation in this layer, it is usually pattern-matching to surface features of similar problems it has seen — and the surface features are exactly what mislead.

This is the trap to watch for: AI is most willing to give you a definitive answer precisely where it has the least grounding to do so. It will hedge on a factual question it could verify and confidently rank your strategic options. The confidence is uncorrelated with the reliability. Your defence is structural — keep AI in the structuring and generation layers, keep yourself in the judgment layer, and notice when you are letting the model's fluency substitute for your decision.

There is also a quieter failure mode worth naming: false precision. Ask AI to quantify a tradeoff and it will. Ask it to weight options on a 1-10 scale and it will produce numbers that look rigorous and are essentially fabricated. The model is not lying, exactly — it is doing what you asked, which is to produce a number where no number exists. Quantification is a tool you should reach for when the underlying data supports it, not a default. Knowing the difference between "I have data and AI helped me model it" and "AI produced numbers that feel like data" is one of the harder calibration skills to build, and one of the most consequential.

The skill this topic builds is decomposition. A leader who has internalised this distinction stops asking AI "what should I do?" and starts asking it "what are the five ways to think about this?", "what are ten options I might be missing?", "what assumptions am I making that I have not stated?", and "where might my reasoning be wrong?" Then they make the call. The output is better analysis, faster, with judgment kept intact. The trap is using AI to feel decisive when you are actually being lazy. The discipline is using it to be more thorough than you would otherwise have been, and then doing the part that is yours alone.

## Level 2 candidates

**Framework generation and adaptation** — How to use AI to surface candidate decision frameworks and adapt them to your specific context, rather than reasoning from scratch or anchoring on the first one that comes to mind. Worth deeper treatment because the failure mode here is subtle: applying a generated framework that fits the surface of the problem but not its structure, and not noticing the mismatch because the framework looks legitimate.

**Scenario analysis and stress-testing** — Using AI to generate scenarios, edge cases, and counterfactuals at volume, then using your judgment to identify which represent real risks. Deserves a deep dive because scenario quality varies enormously with prompt construction, and most people generate either too few scenarios (anchoring) or too many low-signal ones (noise).

**The assumptions audit** — Techniques for using AI to extract and list the unstated assumptions in a plan, position, or analysis, then verifying them systematically. Worth its own treatment because most strategic mistakes trace back to unexamined assumptions, and AI is unusually good at surfacing them precisely because it has no investment in the conclusion.

**Quantification and false precision** — When AI can genuinely help build models or quantify tradeoffs, and when it produces numbers that look rigorous but are fabricated. This deserves depth because the failure mode is socially costly — quantified analysis carries authority in organisations, and AI-generated false precision can drive real decisions before anyone notices the foundation is sand.

**Knowing what you don't know** — Using AI to identify information gaps before deciding, and learning to distinguish between "I lack data I could get" and "this is fundamentally uncertain." Worth deeper exploration because the conflation of these two categories is one of the most common executive errors, and AI both helps and hurts depending on how you prompt it.

**Pressure-testing your own reasoning** — Structured techniques for asking AI to argue against your conclusion, find the flaw in your logic, or steel-man the opposing view. Earns a deep dive because the prompt structures that produce genuine challenge versus polite disagreement are non-obvious, and the difference determines whether this practice strengthens or flatters your thinking.

---
