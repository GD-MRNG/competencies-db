## Metadata
- **Date:** 24-05-2026
- **Source:** 06_code_and_technical_execution.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-06 · Code and Technical Execution

The most important shift in AI-assisted development isn't speed. It's that the bottleneck has moved. For most of the history of software, the constraint on shipping was implementation: you knew roughly what you wanted, and the work was translating that into syntax that compiles, runs, and doesn't break the build. AI has collapsed that step for any problem that isn't genuinely novel. What's left is everything that was always harder — knowing precisely what you want, knowing whether what you got is right, and knowing when the approach itself is wrong. If you don't see this shift, you'll think AI made you faster. If you do see it, you'll realize it changed what your job actually is.

The clearest way to think about this is by category. AI is genuinely transformative for templating, refactoring, test generation, and documentation — the high-friction, low-creativity work that engineers habitually procrastinate on or skip entirely. These are tasks where the answer is mostly determined by the surrounding code and conventions, where there's a right shape that AI has seen ten thousand times, and where the cost of a mistake is bounded because tests catch it. Force multiplication here is real and immediate. You write the test suite you would have skipped. You document the function you would have left bare. You refactor at a scope you wouldn't have attempted manually because the cost was too high.

It's a different story when you move toward architecture, novel algorithms, and subtle debugging. AI can describe trade-offs it has read about, but it cannot weigh them against constraints it doesn't know — your team's skill profile, your operational tolerance for complexity, the political reality of which dependency you're allowed to take on. It can suggest plausible explanations for a bug, but plausible explanations for subtle failures are exactly the kind of output that wastes hours when wrong. The pattern is consistent: AI is strong where the answer lives in patterns it has seen, and weak where the answer requires understanding context it doesn't have.

This is why the real work shifts upstream and downstream of the code itself. Upstream, the bottleneck becomes specification — describing what you want with enough precision that the generated output is actually what you need. Vague prompts produce code that compiles, runs, and solves the wrong problem. The discipline of writing a good prompt for code is the discipline of writing a good ticket: stating the inputs, the outputs, the edge cases, the constraints, the conventions. If you can't articulate those, you don't actually know what you want yet, and the AI will fill the gap with whatever pattern is most common in its training. That pattern is rarely your pattern.

Downstream, the bottleneck becomes review. Generated code looks right. It uses the right libraries, follows familiar idioms, names variables sensibly, and frequently runs on the first try. None of that is evidence that it's correct. AI-generated code fails in subtle ways: off-by-one errors, mishandled null cases, security assumptions that don't match your environment, calls to APIs that don't exist but sound like they should. The cost of these failures isn't just the bugs themselves — it's that they accumulate quietly in code that nobody scrutinized because it looked fine. If you're not good at reading and critiquing code, AI amplifies your mistakes. If you're good at it, AI multiplies your output. The asymmetry here is unforgiving.

This changes what working at the terminal means. You're shifting from typing to reviewing, from implementation to specification. The skills that mattered most when you were writing every line — fluency with syntax, memory for library APIs, speed of typing — matter less. The skills that mattered less — precise specification, code review judgment, testing discipline, architectural taste — matter more. Junior engineers feel this most sharply, because the path that built those review-and-judgment skills used to run through years of writing code by hand. That path is now shorter and the destination is further away, which is a problem worth taking seriously rather than waving away.

The practical consequence is that AI in your codebase rewards engineers who already have judgment and punishes those who don't. It is not a leveler. A senior engineer using AI can specify carefully, review critically, and catch the failures that the AI introduces; their output multiplies. A junior engineer using AI may ship code they don't fully understand, miss the subtle failures, and develop habits that paper over the gaps in their judgment with confident-looking output. The same tool produces opposite results. If you're leading a team, this is the dynamic to design around: structure work so that AI handles the mechanical parts, but the review and specification work — where judgment lives — stays with the humans who can do it. Protect that work, or you'll wake up to a codebase that nobody actually understands.

## Level 2 candidates

**Specification as the real work** — How to write prompts and tickets precise enough that generated code is actually what you need, including how to specify inputs, outputs, edge cases, and conventions. Worth deeper exploration because this is the new core competence and most engineers underestimate how much of their old job was implicit specification done in their head while they typed.

**Code review competence with AI-generated code** — The specific failure modes of generated code (hallucinated APIs, plausible-but-wrong logic, security assumptions) and how to develop review and testing practices that catch them. Deserves its own treatment because the failure modes are different from human-written code and require different review instincts.

**Architectural decisions and what to protect from automation** — What AI cannot help with at the system design level (trade-off analysis, choosing between approaches given organizational context) and how to keep that work intentionally human. Worth deeper exploration because the failure here is silent — you don't notice the architectural decisions you outsourced until the system can't evolve.

**Debugging with AI** — When pattern matching against common errors genuinely accelerates debugging versus when AI hallucinates plausible explanations and burns hours. Worth a deep dive because the line between useful and harmful is non-obvious and the cost of getting it wrong is high.

**Documentation and test generation as the gateway use case** — Why these are the highest-ROI applications of AI in code, how good coverage cascades into higher productivity downstream, and how to build the habit. Worth deeper treatment because most engineers still treat these as low-priority work even when AI has eliminated the friction that justified skipping them.

**The junior developer problem** — How AI changes what early-career engineers should focus on learning, given that the path from typing to judgment used to run through years of hand-written code. Worth its own post because the team and career implications are significant and most organizations haven't reckoned with them.

---