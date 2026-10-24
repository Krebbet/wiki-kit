# Self-Evolving Agent Harness (Harness RSI)

Zhongguancun Academy/USTC survey-plus-theory paper (arXiv:2610.18813; 66 pages, ingested copy is the short version) defining "harness self-evolution": revising prompts, memory, workflows and code around a fixed model, with persistence across runs. It supplies a taxonomy of update targets and conditional bounds on generalization, retention and fresh-validation admission. No new experiments; empirical tables are secondhand. Framing and theory contribution, not a new algorithm. It explicitly criticizes search-time reuse of held-out splits.

## Definition

- Harness H = software/config around a fixed model M in environment E (seven runtime functions, following DeepSeek-AI's model-harness decomposition, see [[deepseek-v4]]). Rollout tau ~ Run(M,H,E), score y = J(tau). H_k = Update(H_{k-1}, B_k), with Update = diagnosis + proposal + assessment + admission; the incumbent is retained if nothing is admitted.
- Requirements: operational feedback with a retained update mechanism, and persistence across runs. The final assessment J must lie outside the editable surface.

## Taxonomy

- Interpreted-state updates: instructions, memory, task-level workflow over fixed operators (representative: [[gepa-reflective-prompt-evolution]]).
- Executable revisions: (a) tools/code patches at component level (Self-Harness, HarnessCompass, Agentic Harness Engineering, skill libraries); (b) repository/runtime logic (whole-agent synthesis, ADAS/DGM-style lineages, see [[huxley-godel-machine]]); (c) plugin composition ("Everything Is a Plugin", EIP / DSH Everything).

## Theory (Sec 4)

- Continual-PAC-style analysis via algorithmic stability: expected generalization gap bounded by beta_{s,k}; retention E R_s(H_k) <= E R-hat_s(H_s) + beta_{s,s} + sum of per-transition regression budgets eps_{s,u} (the budgets are separate assumptions).
- High-probability admission via a fresh independent validation set, Hoeffding + union bound over K*T comparisons: accept only if Delta-hat + sqrt(2 ln(KT/delta)/m) < 0; extended with an evaluator-target discrepancy eta (adds 2*eta).
- Prerequisites: independent task draws, losses in [0,1], unbiased paired estimates, eta calibrated from executable checks or human assessment. Assumption-conditional; not verified empirically.

## Held-out-split reuse caveat

The paper argues that reusing the held-out split during search (it names HarnessBank and Self-Harness) breaks the independence the admission bound needs, pointing to adaptive-validity inference (Dwork et al. 2015). This applies, as a methodological caveat and not a factual dispute, to wiki-recorded validation-gated methods: [[skillopt]] (accept only on strict validation improvement), [[memoharness]] (validation gate), [[argus-agentic-runtime]] (ManagerAdmit). Parallel critiques: [[evolutionary-search-eval-rigor]] (validator exploits), and cross-fitting in [[co-cheating-crossfit]] as a related leakage fix.

## Results (secondhand, vendor-adjacent, no matched cost)

- SpreadsheetBench (Shen et al. 2026a), HarnessOpt + skill on GPT-5.4-nano/mini/GPT-5.4/GPT-5.5: 77.58/82.56/85.05/85.77 vs SkillOpt-Lite 66.19/73.31/79.36/79.72 (+5.69 to +11.39 pp) and SkillOpt 51.60/47.50/61.50/76.20; Initial 29.89/28.21/39.86/37.37. GPT-5.4-nano + HarnessOpt (77.58) beats GPT-5.5 + SkillOpt (76.20); authors caveat not matched-cost.
- EIP spreadsheet task (Pan 2026): first-task tool calls 13 to 3, but tokens +15.7% and wall time +54.9%; cumulative savings from task 2 (-110,351 tokens, -22.97 s after 5 tasks). The paper flags that first-task deltas disagree with the cumulative row, unresolved.
- LiveBrowseComp (Pan 2026, unit unspecified): "XYZ + dsh-everything" 51.39 vs XYZ-Aquila-mini 48.7, Nex-N2-mini 41.4 (<40B group, incl. [[agents-a1-horizon-scaling]] 29.6); DeepSeek V4-Pro 38.3, Kimi-K2.6 31.7. Authors say repeated runs and matched budgets are needed.

## Safety framing

Persistence propagates errors (monoculture, specification gaming, irreversible physical/clinical harm). Recommends keeping J, e-stops, privileges and authorization outside the editable surface. Echoes [[ai-agents-open-ended-research]], [[co-cheating-crossfit]] and shared-artifact exploit spread in [[research-swarm-whistleblowing]].

## Applicability

A checklist for persistent-harness builders (skill libraries, memory files, CLAUDE.md-style stores such as [[openclaw-claude-code-memory]], self-patching tool libraries): hold J outside the editable surface; admit revisions only against fresh independent validation; track cumulative regression budgets; version-link artifacts for rollback. Sits with the harness-as-training-target cluster ([[macaron-v1]], [[polar-rl-harness]] as the weight-side counterpart) and skill co-evolution ([[skill-self-play]], [[disco-arex-skill]]).

## Reproducibility and adoption

Companion repo github.com/zgcagi/Harness-RSI. Brand new, no external uptake; aggregates a clustering sub-field (Self-Harness, HarnessCompass, HarnessBank, EMHO, RoboRSI) rather than leading it. HarnessOpt, EIP/DSH Everything and others cited here are not captured as pages.

## Source

- raw/research/weekly-2026-10-17/02-self-evolving-agent-harness.md
- https://arxiv.org/pdf/2610.18813

## Related

[[skillopt]], [[memoharness]], [[argus-agentic-runtime]], [[macaron-v1]], [[gepa-reflective-prompt-evolution]], [[huxley-godel-machine]], [[disco-arex-skill]], [[skill-self-play]], [[evolutionary-search-eval-rigor]], [[co-cheating-crossfit]], [[ai-agents-open-ended-research]], [[research-swarm-whistleblowing]], [[openclaw-claude-code-memory]], [[openclaw]], [[deepseek-v4]], [[agents-a1-horizon-scaling]], [[polar-rl-harness]]
- [[coevo-rsi]] — model+harness co-evolution instance (checkpoint archive, TIMR); [[socratic-skill-learning]] — teacher-in-the-loop skill acquisition
