## Metadata
- **Date:** 19-05-2026
- **Source:** 5_episode_3_how_to_use_al_to_succeed_at_work.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# How to Use AI to Succeed at Work

The instinct most people have when they start using AI at work is to point it at the things they're worst at. You don't know how to write a marketing plan, so you ask the AI for one. You've never built a financial model, so you have it draft one. This feels rational — you're plugging your gaps — but it's almost exactly backwards. The value of AI at work is highest in the areas where you already have deep expertise, and it gets dangerous fastest in the areas where you don't.

The reason is hallucination. Large language models generate text that sounds true regardless of whether it is true, and even the frontier models haven't escaped this. If you're an expert in the domain, you can read an AI's output and immediately spot the parts that are wrong, lazy, or confidently misleading — and discard them. If you're not, you can't. You'll take a plausible-sounding answer at face value and act on it. There's a study where small business owners in Kenya were given access to GPT-4o through WhatsApp; on average, the access made no difference to profits. But when researchers split the group, the already-successful businesses improved meaningfully and the struggling ones got worse. The good operators could filter the advice. The bad ones followed instructions to buy newspaper ads when their actual problem was that their diapers were made of sandpaper.

The right mental model, then, is not "AI as oracle" but "AI as a fleet of brilliant, inexperienced junior assistants." Imagine your company hired you a team of PhDs who know an enormous amount in the abstract but have never done your specific job, don't understand your context, and have no common sense about what would be catastrophic to get wrong. You wouldn't tell them to "manage the marketing campaign for Nike this fall." You'd give them small, well-defined tasks that you already know how to do yourself, so you can verify the output in seconds. You'd be precise about what you want. And you'd give them feedback — it almost doesn't matter whether it's warm praise or sharp criticism, only that it's clear. That's how you should be prompting.

Once you're operating in that mode, the obvious targets are the well-defined, boring tasks that fill your day. Email is the canonical one — you know what the reply should say, you just don't want to write it, and the Gemini plugin in Gmail or Copilot in Outlook can draft it from your inbox context with a button. Meetings you only half-need to attend become transcripts you feed to Gemini and get back action points in five minutes. Slide decks become Canva AI prompts that produce a workable first draft you edit rather than build from scratch. Checklists for any non-trivial project — the same checklists Atul Gawande argued surgeons and pilots rely on precisely because expertise alone isn't enough — can be generated in seconds. None of this requires the AI to be smarter than you. It requires it to be faster than you on things you've already mastered.

For anything more complex, the single highest-leverage habit is to put the model into thinking mode and use a frontier model deliberately rather than letting the product route you to whatever's cheapest. When GPT-5 underwhelmed people, part of what happened was that the programmatic router was sending most queries to lighter models behind the scenes; the breakthrough was mostly that free users occasionally got routed to the heavy ones. If you're paying for a subscription, bypass the router. Send hard problems to the smartest available model and let it think. You can run several of these in parallel — it's like dispatching multiple researchers — and you'd rather have one of them reason carefully than have five give you fast guesses. For anything that requires pulling fresh information from the web, use deep research: an agentic loop that searches, evaluates what it found against your goal, and searches again to fill gaps. It can take half an hour, but it runs in the background and produces something genuinely different from a single search.

There's a second category of use that most people miss entirely: AI as a coach. A real strategy consultant might cost thousands of pounds an hour; a real interview coach isn't much cheaper. An LLM can replicate a meaningful chunk of that value for the kinds of small-scale problems most of us actually have — not solving oil spills, but preparing for a salary negotiation, pressure-testing a strategy you're about to present, or running mock interviews using the voice feature so you walk in polished rather than improvising. It won't have the empathy or organisational context of a top-tier human coach, and it doesn't have the proprietary data of a McKinsey. But for an individual contributor trying to get sharper on a specific conversation, the gap is smaller than the price difference suggests.

The final thing to internalise is that everyone you work with is going to be using AI too. The baseline is rising. Writing a competent report, building a clean spreadsheet, generating a passable deck — all of this is becoming table stakes, which means it's becoming a worse and worse way to stand out. The 80% that AI handles well is now everyone's 80%. The differentiation lives in the remaining 20%: judgment, taste, empathy, understanding what your boss actually needs, knowing which problem is worth solving in the first place. Your job is to use AI ruthlessly on the grunt work so you have time and attention left for the part of the job that AI still can't do — and then to be visibly excellent at that part. That's the actual game.

## Level 2 candidates

**The expert advantage and the hallucination problem** — A deeper treatment of why AI helps experts more than novices, what kinds of hallucinations show up in different domains, and how to build a verification habit. Worth going deeper because the "use AI on what you know well" principle is the foundation of everything else, and the supporting research (the Kenya study, the Harvard/BCG studies on consultants) deserves proper unpacking.

**Prompting as managing a junior assistant** — The practical mechanics of writing prompts: clarifying questions, scoping tasks small enough to verify, giving feedback, addressing assumptions before work starts. Worth its own treatment because this is where most users plateau, and the "junior PhD" mental model unlocks a much richer set of behaviours than people typically use.

**Thinking mode, model selection, and routers** — When to bypass programmatic routers, how frontier models differ from lightweight ones, why parallel inference changes how you work, and how to choose between Gemini, Claude, and ChatGPT for different task types. Worth depth because most users default to whatever the product gives them and never learn the meaningful performance differences between models.

**Deep research and agentic search** — How iterative agentic search actually works, what makes it different from single-shot search, what kinds of tasks it's overkill for, and where it genuinely outperforms a human researcher. Worth a deep dive because it's a qualitatively different capability from chat and most people haven't built intuition for when to reach for it.

**AI as coach: negotiation, interviews, strategy** — Concrete prompts and workflows for using AI to roleplay high-stakes interpersonal scenarios, including the voice feature for interview practice and the strategy-consultant framing for work problems. Worth going deeper because this is the highest-leverage non-obvious use case and benefits from worked examples rather than a summary.

**Standing out when everyone has AI** — How to identify the 20% of your job that AI can't do, and how to deliberately invest the time AI frees up rather than letting it evaporate. Worth its own post because it's a career-strategy question, not a tooling question, and deserves to be treated as such rather than tacked on at the end.

---

<details>
<summary>Discussion</summary>

## Why This Conversation Is Happening

The biggest mistake people make with AI at work is using it as a substitute for competence instead of an amplifier for competence. That feels efficient in the moment: you hand the model the task you least understand and hope it fills the gap. But that is exactly where AI is most dangerous, because plausible output is only useful if you can evaluate it. If you cannot tell good work from confident nonsense, the tool does not remove risk — it concentrates it.

This matters at work because most business tasks are not judged by whether something looks polished. They are judged by whether they are right, appropriate, timely, and aligned with the actual situation. A marketing plan, negotiation strategy, hiring rubric, spreadsheet model, or customer email can all look excellent while being subtly wrong in ways that cost real money or trust. Engineers and knowledge workers need a better model than “AI makes me good at things I’m bad at.”

The useful framing is that AI creates the most value where you already have enough expertise to supervise it well. Once you see that, the question changes from “what can AI do for me?” to “which parts of my work can I delegate safely, review quickly, and use to free time for the higher-judgment parts of the job?”

## What You Need To Know First

**1. Hallucination**  
A hallucination is when the model states something false or unsupported with confidence. In work settings, this is often dangerous not because it is obviously absurd, but because it sounds reasonable enough to pass a quick skim. The article depends on the idea that hallucinations are manageable for experts and hazardous for novices.

**2. Domain expertise**  
Domain expertise means having enough real understanding of a field to judge quality, spot omissions, and notice when something feels off. You do not need to be the world expert; you just need enough grounding to review the output intelligently. This matters because AI produces more value when paired with someone who can filter it.

**3. Task scoping**  
Task scoping means defining a task narrowly enough that expectations, inputs, and outputs are clear. “Draft three follow-up email options” is scoped. “Handle our Q4 marketing strategy” is not. The article assumes that good AI use at work often comes from shrinking tasks until they are easy to verify.

**4. Grunt work vs. judgment work**  
Grunt work is repetitive, pattern-heavy, and time-consuming but not strategically central: formatting, summarizing, drafting, note extraction, checklist generation. Judgment work is choosing priorities, interpreting context, managing tradeoffs, and making accountable decisions. The article’s core advice is to use AI heavily on the first category so you can spend more of yourself on the second.

## The Key Ideas, Connected

**1. AI is most useful in areas where you already know what good looks like.**  
The article begins by reversing a common instinct. People often point AI at their weakest areas, hoping it will fill capability gaps. But that is exactly where they are least able to judge the output. In contrast, when you already understand the task well, AI can save time without taking away control, because you can review the result quickly and reject bad work. That leads directly to the reason expertise matters so much.

**2. The limiting factor is not output generation but your ability to detect error.**  
Because LLMs can produce fluent but false or misaligned output, the key question is whether the human can spot what is wrong. Experts usually can: they notice bad assumptions, shallow reasoning, or domain-specific mistakes. Non-experts often cannot, so they inherit risk they do not know they have. This is why the same tool can help strong performers and mislead weak ones. Once you see that, the right metaphor for working with AI becomes clearer.

**3. AI should be treated like a team of smart but inexperienced junior assistants.**  
This is the article’s main operating model. The model knows a lot in the abstract, works quickly, and can be useful across many tasks, but it lacks your specific context and does not know which mistakes are unacceptable in your environment. So you would not delegate open-ended ownership to it. You would give it bounded tasks, specify clearly, and check the result. That framing naturally points toward the kinds of work it handles best.

**4. The best early use cases are repetitive, well-defined tasks you can verify in seconds.**  
Email drafting, meeting summarization, extracting action items, building first-pass slides, and generating checklists are valuable not because they are strategically deep, but because they consume time and are easy for a competent person to inspect. AI is strong when the target is “save me 20 minutes on something I already know how to do.” This matters because it separates safe leverage from false leverage. From there, the article expands to more advanced use: not just delegation, but structured reasoning support.

**5. For harder problems, the value comes from using stronger models in deliberate thinking mode.**  
When the task is planning, problem-structuring, or research, speed matters less than quality of reasoning. The article argues that people often let the product route them to lightweight models optimized for cost or responsiveness, when the task really calls for a frontier model thinking more carefully. The implication is that model choice is part of work design. And once you are willing to use the model more deliberately, you can extend beyond single-shot chat into richer workflows.

**6. Deep research and parallel model use turn AI into a background research process, not just a chat interface.**  
For tasks that require current information or broad synthesis, the article points to agentic research loops: searching, evaluating results, identifying gaps, and searching again. That is qualitatively different from asking one question and getting one answer. Running several models or several threads in parallel also changes the economics of your time: you can compare approaches, let one critique another, or have multiple drafts generated while you work elsewhere. This naturally broadens the role of AI beyond production into professional development.

**7. AI can also function as a coach for high-value interpersonal and strategic situations.**  
The article highlights negotiation prep, interview practice, and strategy pressure-testing. In these use cases, the model is not replacing expertise so much as giving you cheap rehearsal, critique, and simulation. That matters because some of the highest-return work is not document generation at all; it is sharpening performance before a consequential conversation or decision. And that leads to the final career-level implication.

**8. As AI raises the baseline on basic competence, differentiation shifts toward judgment and taste.**  
If everyone can generate a decent report, clean slide deck, or serviceable spreadsheet with AI, those outputs stop being strong signals of exceptional ability. The value moves to the remaining layer: choosing the right problem, sensing what matters in context, making tradeoffs, communicating with empathy, and taking responsibility for decisions. This closes the chain: AI should absorb the repetitive 80% so you can invest visibly in the human 20% that becomes more, not less, valuable as the baseline rises.

## Handles and Anchors

**1. Use AI on work you can grade, not work you can only admire.**  
If you can inspect the result and know quickly whether it is good, AI is probably helping. If the output merely sounds impressive and you are not equipped to judge it, you are in a danger zone.

**2. AI is an eager junior, not an oracle.**  
A strong junior can move fast, produce drafts, summarize, and suggest options. But they still need scope, supervision, and correction. That is a much safer mental model than treating the model as a source of authority.

**3. Spend AI on the 80% so you can be exceptional in the 20%.**  
The goal is not to automate your whole job. The goal is to automate the generic parts so your attention is available for the parts where human judgment still compounds.

## What This Changes When You Build

**A worker who understands this will start by applying AI to tasks they already perform competently because their expertise lets them review output fast and catch subtle errors before those errors become decisions.**  
So they will often begin with drafting, summarization, first-pass analysis, or checklist creation in domains they already know well.

**A worker who understands this will scope requests narrowly and concretely because a bounded task is easier for the model to execute and easier for the human to verify.**  
Instead of “make a strategy,” they will ask for “three risks in this strategy memo,” “a draft reply to this email in my tone,” or “a checklist for launching this feature based on these constraints.”

**A worker who understands this will reserve stronger models and slower reasoning passes for ambiguous, high-value work because not all tasks deserve the same tradeoff between speed and depth.**  
That changes how they use AI subscriptions: lightweight models for routine transformation, frontier models for planning, critique, and hard decisions.

**A worker who understands this will use AI as a rehearsal and critique partner for consequential conversations because practice and feedback can materially improve performance before the real event.**  
That includes mock interviews, negotiation roleplay, stakeholder objection drills, and presentation pressure-testing.

**A worker who understands this will deliberately reinvest the time AI saves into judgment-heavy work because baseline competence is becoming cheap and visible differentiation is shifting upward.**  
They will spend more attention on prioritization, stakeholder understanding, tradeoff calls, clarity of communication, and the nuanced parts of execution that polished generic output cannot replace.

</details>
