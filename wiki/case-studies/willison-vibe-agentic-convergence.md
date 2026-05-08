# Willison — Vibe Coding and Agentic Engineering Are Getting Closer Than I'd Like (2026-05-06)

Simon Willison, who drew a firm public line between vibe coding and agentic engineering in March 2025, reports in May 2026 that the two practices have converged in his own production work as model reliability has risen. He is no longer reviewing every agent-generated line even for production systems, a drift he explicitly names as normalization of deviance. Four new claims anchor this post: a "treat-agent-as-team" review heuristic, a quality-signal shift from artefact richness to evidence of sustained use, and full-SDLC bottleneck migration driven by code-throughput scaling. The combination makes this the sharpest practitioner-level challenge yet to the supervised-delegation posture the wiki has documented elsewhere.

## Source

- Simon Willison, "Vibe coding and agentic engineering are getting closer than I'd like," 2026-05-06 — `raw/research/weekly-2026-05-08/03-willison-vibe-agentic-convergence.md`. Practitioner blog post (highlights from Heavybit High Leverage podcast, Ep. #9, with Joseph Ruscio).

## The convergence claim

Willison's March 2025 taxonomy was crisp: vibe coding = zero code review, non-programmer cross-fingers loop; agentic engineering = professional-grade delegation backed by 25 years of experience, security and maintainability awareness still engaged. By May 2026 that line has blurred in his own practice:

> "The problem is that as the coding agents get more reliable, I'm not reviewing every line of code that they write anymore, even for my production level stuff."

His framing of why: for a well-scoped task — "build a JSON API endpoint that runs a SQL query and outputs the results as JSON" — he trusts the agent to produce correct output with automated tests and documentation without reviewing the source. The guilt this produces is the subject of the post. His resolution is not "review more" but rather "reframe what review means."

He notes that as recently as his March 2025 post he considered no-review to be definitionally vibe coding. He is now doing no-review on production code while still considering himself an agentic engineer. The distinction has not collapsed entirely — his 25 years of experience inform *what tasks he assigns* and *what constraints he specifies* — but the output-inspection step has dropped out for routine tasks.

## Named patterns and heuristics

**Black-box trust model.** Willison reframes no-review by analogy to depending on an internal team's service: you consume the API surface (documentation, demonstrated behavior), not the implementation. You read the source only when problems surface. This is a practitioner-articulated heuristic for when full code review becomes operationally impractical at scale. The analogy is explicit and deliberately borrowed from his experience as an engineering manager. The discomfort he flags: unlike a team, an agent cannot accumulate professional reputation or be held accountable — the analogy is structurally imperfect.

> "Claude Code does not have a professional reputation! It can't take accountability for what it's done. But it's been proving itself anyway."

**Normalization of deviance.** Willison explicitly names this safety-engineering concept. Each successful unreviewed output increases the probability of misplaced trust at the wrong moment. He links to his own December 2025 write-up on the pattern. The risk is not that the agent is unreliable in aggregate; it is that rising average reliability trains the engineer to skip review in cases where the agent would fail — exactly the failure mode that safety engineering predicts from repeated-success streaks. This is the most structurally precise framing of the no-review risk in the wiki.

**Treat-agent-as-team heuristic.** A practical norm for when to not review: treat agent output the way you would treat a trusted internal team's service boundary. Review is triggered by observed failures, not by default. The heuristic operationalises the black-box trust model as a decision rule. It does not resolve the accountability gap — it acknowledges it and proceeds anyway, which is itself a practitioner judgment about acceptable risk.

**Quality-signal shift from artefact richness to evidence of sustained use.** Agent-generated repositories can now present as indistinguishable from carefully hand-crafted ones:

> "I can knock out a git repository with a hundred commits and a beautiful readme and comprehensive tests of every line of code in half an hour! It looks identical to those projects that have had a great deal of care and attention."

The signal Willison now trusts is not commit count, test coverage, or README quality but whether someone has *used* the artefact continuously: "If you've got a vibe coded thing which you have used every day for the past two weeks, that's much more valuable to me than something that you've just spat out and hardly even exercised." He notes this applies to his own projects — he cannot tell from the artefact alone whether it is good. He generalises this to enterprise adoption: organisations want peer enterprises who have successfully used a solution for six months before taking a risk on it.

**Full-SDLC bottleneck migration.** Code throughput scaling from ~200 to ~2,000 LOC/day does not only break code-review norms. It breaks assumptions across the entire development lifecycle. Willison frames this via Jenny Wen (Anthropic design lead): design gates exist because building the wrong thing for three months is catastrophic; if the build is three hours, the cost of building the wrong thing has collapsed and design processes can tolerate more risk and iteration. The bottleneck has migrated upstream and downstream simultaneously: upstream (design can be riskier), downstream (verification is the new expensive step). This extends the bottleneck-shift framing from [[case-studies/willison-cognitive-cost]] — there the bottleneck moved to testing; here it has migrated to the full SDLC.

## Tensions with existing wiki positions

**No-review drift vs. effective-harnesses' supervised delegation.** [[patterns/effective-harnesses]] prescribes `feature_list.json` + `claude-progress.txt` + git as a recovery substrate and implies continued engineer oversight — the initializer/coding-agent split exists precisely to keep a human in the loop between stages. [[case-studies/anthropic-internal-study]] frames the engineer-as-orchestrator role as still engaged, not delegating blindly. Willison's own practice has drifted to no-review for well-scoped tasks and he calls it production-appropriate. The conflict is not theoretical: Willison is a careful practitioner who has written extensively on responsible AI use, and he is uncomfortable with where his own practice has landed. The wiki currently has no reconciling position.

**Use-evidence > test/doc-richness vs. automated-test gates.** [[deployments/openai-symphony]] treats 1,500+ PRs and comprehensive test infrastructure as meaningful quality evidence and operates with 0% pre-merge human review precisely because the automated gates are trusted. [[patterns/effective-harnesses]] and [[patterns/agentic-harness-engineering]] both rely on automated tests as quality gates for production-grade agent output. Willison's claim cuts the other way: test and documentation richness are no longer reliable quality signals because they can be generated at near-zero cost. These positions are incompatible at the level of what "evidence of quality" means. Both sides can be correct in their own deployment context — Symphony's test suite is long-running and CI-gated; a freshly generated repo's tests are untested in production — but no reconciling framework is currently documented.

## Related

- [[case-studies/willison-cognitive-cost]] — earlier Willison interview; this page extends with four new claims around convergence
- [[case-studies/anthropic-internal-study]] — engineer-as-orchestrator framing; accountability gap echoes skill-atrophy tensions documented there
- [[case-studies/anthropic-claude-code-postmortem]] — prompt-layer fragility relevant to convergence concerns; single-instruction degradation is the kind of subtle failure a no-review norm would miss
- [[deployments/openai-symphony]] — 0% pre-merge human review is the maximal expression of the pattern Willison finds uncomfortable; provides a concrete production data point bracketing the review-norm question
- [[patterns/effective-harnesses]] — supervised-delegation posture; direct tension with no-review drift documented here
- [[patterns/agentic-harness-engineering]] — automated tests as quality gates; tension with quality-signal-shift claim
- [[patterns/topology-taxonomy]] — bottleneck migration across full SDLC is relevant to the long-horizon-context-loss and harness-evolution axes tracked there
