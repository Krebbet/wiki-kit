# When Do Institutions Beat Intelligence? (multi-agent LLM ecologies)

**PROVISIONAL.** Un-refereed, single-author arXiv preprint (Zhengye Han, NYU; arXiv 2608.11357). The evidence is synthetic: controlled multi-agent LLM simulations on tasks the author designed, so several headline numbers (e.g. 1.00 vs 0.00 accuracy) reflect task construction as much as general behaviour. Nothing here is evidence about human institutions; read-across is flagged **[wiki synthesis]**. Summary: the paper argues that rules governing a collective of LLM agents (routing, validation, audit, state representation) beat a stronger model only when they repair how the collective builds a usable shared decision state, and lose the advantage when signals are invalid or uncheckable, when capability can substitute for the rule, or when the resulting state cannot be acted on.

**Evidence tier note.** Findings are (a) design-based but synthetic: seed-paired experiments with matched-call baselines and mechanism-breaking controls (50 to 100 seeds per cell; Llama 3.1 8B / 3.3 70B core, plus Qwen, Mistral and a frontier panel of Claude Sonnet 4.6, Gemini 2.5 Pro, DeepSeek V3.2), bootstrap 95% CIs. Natural-task panels are small (HotpotQA 20 paired questions per model; hosted execution 21 or 30 questions). Strategic/incentive results are simulation only: a hosted pilot of 2,400 Llama/Mistral decisions found zero misreports, so scaling stopped. The decision rule at the end is (b), and the author calls it non-universal.

## Unit of analysis and definition

**[empirical]** (setup, not a finding) The unit is a collective of LLM agents on one task. "Institution" means externally specified rules I = <rho (observation/reporting rights), V (admission), U (state update), Phi (representation/action interface)>. That is an information-pipeline definition, closer to Ostrom's rules-in-use than to North's, and narrower than [[what-is-an-institution]]. Human-group literature (hidden profiles, transactive memory, accountability) supplies the variables only; the author disclaims any claim that LLM agents share human mechanisms. Agent counts are fixed at 3 to 4 workers, so nothing is said about span, layers or size.

## Four mechanisms, each tested by breaking it

1. **Routing completeness.** **[empirical]** Decisive-evidence coverage drives a unique public decision state, which drives accuracy. Accuracy 0.26 / 0.96 / 1.00 and coverage 0.357 / 0.760 / 1.000 for 3x2 / 3x4 / 4x4 assignments. Failure is hidden-profile-like: information held but not jointly available.
2. **Grounded vs syntactic validation.** **[empirical]** Admitting reports on evidence-checked grounds beats format-checked admission by +0.50 [0.30, 0.70]. Repeated agreement is not independent evidence (correlated wrong consensus). Reformatting already-accepted evidence gives no detectable benefit.
3. **Sanctions need checkability.** **[empirical]** At zero checkability every sanction level yields exactly 0.00 gain. A 10% audit at capability 0.55 beat unaudited capability 0.65 by +0.135 [0.096, 0.175]. A sanction without observability is "an unenforceable declaration".
4. **Action interface.** **[empirical]** Better evidence can be erased by an interface the finalizer cannot use: with evidence held fixed, the ordered interface beats the graph one (graph minus ordered -0.067 [-0.128, -0.010]). A learned reranker beats the hand-specified graph by +0.070 [0.036, 0.104].

Weak or imprecise results: dynamic-state validity interactions are small (0.15, 0.15, 0.30; only Qwen 235B excludes zero); graph-vs-BM25 answer transfer is +0.079 [-0.143, 0.302], uninformative.

## Capability substitution and the crossover test

**[empirical]** Institutional advantage is "relative to a capability frontier, not a permanent property of a workflow". Claude showed 0.00 incremental institution-by-capability interaction in all three tested ecologies, Gemini partial, DeepSeek retained large interactions. The paper's operational test of "institutional credit" is the mechanism-validity interaction Gamma = tau(+) - tau(-) (effect of the institution when its signal is valid minus when it is broken) and a crossover point C against capability. The diagnostic decomposition (B, L, X, O, S) organises evidence; it is not an identified structural theory.

## The author's decision rule

**[model]** Buy intelligence when capability can directly do the required transformation. Build an institution when the structural failure survives scaling, the rule observes it reliably, and the resulting state supports action under explicit resource accounting. Redesign the interface, or do neither, when the rule is uninformative, redundant or yields an unusable state. The author states these are cross-ecology regularities, "not a sequential certification algorithm or a universal theorem". Call-matching also does not equal token, latency, money or engineering-burden matching, so overhead is under-counted.

## Candidate dimensions (scoped to artificial collectives)

Candidate rows only; none is scoreable for a real institution yet. See [[dimensions-of-institutional-variation]]: (i) coverage / routing completeness; (ii) grounded vs syntactic admission validity; (iii) evidential independence of admitted reports; (iv) checkability of violations, separate from sanction strength and audit probability; (v) currency of shared state; (vi) action-interface representation; (vii) capability-substitutability; (viii) overhead.

## Read-across to this wiki

All **[wiki synthesis]**, analogy only:
- Grounded-vs-syntactic validity has the same structure as format-vs-function in [[institutional-myths-and-decoupling]], [[isomorphic-mimicry-and-capability-traps]] and the reliability-vs-validity split in [[measurement-validity-framework]]. Correlated consensus parallels the correlated-errors critique in [[critiques-of-governance-indicators]].
- Checkability as precondition for sanctions parallels measurability in [[multitask-incentive-theory]], [[incentives-under-multiple-principals]] and [[team-production-and-monitoring]], and the monitoring principle in [[polycentric-governance]]. Direction differs from [[covenants-with-and-without-a-sword]]: Ostrom's lab study found communication alone worked at zero enforceability, whereas here zero checkability makes sanctions inert; the two are consistent but test different things.
- A finalizer unable to use the state it is given echoes the uninformed principal in [[formal-and-real-authority]].

## Limits and silences

- Power: silent. The rule-setter is benevolent and exogenous; no selection, removal or capture of the designer. Misaligned reporters with a "capture option" are simulated only (cf. [[regulatory-capture]]).
- Scale, age, economic production, public/private invariance: not addressed. Do not cite for the scale/age theme except as flagged analogy.
- Results depend on hosted model versions and provider implementations (2026 models). Title and framing invite generalisation to human institutions that the evidence does not support.
- Methodological strength: explicit nulls and reversals reported, and every intervention paired with a mechanism-breaking control, an analogue of the review logic in [[experimentalist-governance]] (not a claim in either source).

## Source

- raw/research/weekly-2026-10-06/02-institutions-beat-intelligence.md (derived summary: raw/research/weekly-2026-10-06/.ingest/02-institutions-beat-intelligence.summary.md)

## Related

- [[what-is-an-institution]]
- [[dimensions-of-institutional-variation]]
- [[measurement-validity-framework]]
- [[critiques-of-governance-indicators]]
- [[institutional-myths-and-decoupling]]
- [[isomorphic-mimicry-and-capability-traps]]
- [[covenants-with-and-without-a-sword]]
- [[incentives-under-multiple-principals]]
- [[multitask-incentive-theory]]
- [[team-production-and-monitoring]]
- [[formal-and-real-authority]]
- [[hierarchy-and-near-decomposability]]
- [[regulatory-capture]]
- [[polycentric-governance]]
- [[experimentalist-governance]]
