# Agentic Engineering

Simon Willison's 2026 framing for the discipline of **professional software engineers using coding agents** — Claude Code, OpenAI Codex, and peers — to amplify (not replace) engineering expertise.

## Definitions (Simon, 2026-02-23)

- **Agentic engineering** — building software using coding agents that both *generate and execute* code, test independently, and iterate without turn-by-turn human supervision.
- Distinguished from **vibe coding** (Simon's original 2025 definition): writing code you don't read, commonly associated with non-programmers using LLMs to produce functional output.
- Agentic engineering sits at the *professional* end of the spectrum; vibe coding at the *no-attention-paid* end.

*(Practitioner-consensus; Simon's framing has been widely adopted in the 2025–2026 developer-tooling discourse.)*

## Practice — "Writing code is cheap now"

The central shift Simon names (2026-02): the cost of producing initial working code has dropped to near-zero. Knock-on effects worth internalizing:

- **Second-guess "don't bother" instincts.** Things you previously wouldn't attempt (because they'd cost an afternoon) can be a 10-minute prompt.
- **Parallelize asynchronously.** One engineer can have multiple agents implementing, refactoring, testing, and documenting concurrently.
- **Micro-decisions shift.** Refactoring, test coverage, documentation, debug interfaces — all cheaper to include than they were.

**What stays expensive:** "good code." Correctness, verification, solving the right problem, error handling, simplicity, maintained documentation, design flexibility, non-functional qualities (security, maintainability, observability). Steering agents toward *these* remains the substantive engineering work.

## Practice — Red/green TDD

Simon's most-repeated concrete prompting pattern: **"Use red/green TDD."**

- Write automated tests first.
- Run them; confirm they fail (**red**).
- Iterate implementation until they pass (**green**).

Why this works with coding agents specifically:

- Guards against **invented code** that doesn't do what was asked.
- Guards against **unused code** — features built but not exercised.
- Ensures a **regression suite** as the project grows.
- Short enough to paste into any agent prompt. Simon: "Every good model understands 'red/green TDD' as a shorthand." *(Practitioner-consensus; 2026.)*

**Skip the red phase at your peril** — you risk writing a test that already passes, failing to exercise the change you asked for.

## Cross-reference to the broader field

The agent patterns on [[building-effective-agents]] apply inside coding-agent sessions too — prompt chaining for multi-step refactors, evaluator-optimizer for iteration on tests, orchestrator-workers for large migrations. Simon's two-word "red/green TDD" is effectively a hardcoded evaluator-optimizer contract specialized for code.

## Source

- `raw/research/effective-agentic-patterns/03-simon-willison-agentic-engineering-patterns.md` — announcement post (2026-02-23).
- `raw/research/effective-agentic-patterns/06-simon-willison-code-is-cheap.md` — "Writing code is cheap now" chapter.
- `raw/research/effective-agentic-patterns/07-simon-willison-red-green-tdd.md` — "Red/green TDD" chapter.

Simon Willison's guide is a *living document* — chapters are designed to update over time. Captured 2026-04-22. Check the source for newer chapters periodically.

## Related

- [[building-effective-agents]]
- [[error-analysis]]
- [[measurement-vs-architecture]]
