---
name: recursive-concept-learning
description: Fourth method proposal — failure-driven recursive descent over a lazily-materialised concept DAG. For a target concept, evaluate; if pass move on; if fail, ask the teacher for prereqs, recurse on each, retest the parent, fall back to direct training if children pass but parent still fails. Generalises and elevates the §Variant section of concept-curriculum-method into a standalone method, with the inner-loop = proposed-method.
type: research
---

# Recursive Concept Learning (RCL)

Editorial proposal captured 2026-04-28. Builds on and elevates the failure-driven interactive DAG expansion §Variant of [[concept-curriculum-method]]. Where [[proposed-method]] specifies the *per-concept inner loop* and [[concept-curriculum-method]] specifies the *up-front DAG with bottom-up curriculum*, RCL specifies the *outer loop*: a lazy, top-down, failure-driven recursion over a concept DAG that materialises only what the student needs.

## One-paragraph summary

For a target concept $C^\star$, evaluate the student. If it passes, return. If it fails, ask the teacher to decompose $C^\star$ into prerequisites diagnosed *from the failure trace*; recurse on each prerequisite; once children pass, retest the parent; if children pass but parent still fails, train the parent directly. The DAG is the *trace* of expansion, not a pre-built artefact. The inner training step is [[proposed-method]] verbatim. The method is single-sample-aligned at the curriculum level: each new concept node is paid for by exactly one observed failure trace.

## Goal

Train a small LLM by recursively decomposing a target concept into its observed prerequisites, training only the leaves the student cannot already pass, and verifying parent concepts via held-out evaluation rather than loss convergence.

1. **Each concept is gated by evaluation.** Concepts the student already understands are skipped; concepts it does not are trained or further decomposed.
2. **Decomposition is diagnostic, not enumerative.** The teacher sees the student's failure trace and proposes the *missing* prereqs, not the full curriculum.
3. **The DAG is measured, not estimated.** The frontier between "student already knows" and "student must learn" emerges from passes/failures rather than the teacher's prior beliefs.
4. **Each edit is bounded.** The inner training step inherits [[proposed-method]]'s safety rails (sparse mask, EWC anchor, MDL-on-siblings, KL leash).

## Roles

| Role | Symbol | Capability | Output |
|---|---|---|---|
| **Decomposer** | $M$ | Strong, world-access. Reads concept name + student failure trace. | Ranked list of prerequisite concepts. |
| **Evaluator** | $V$ | Independent of $M$ where possible (different prompt-conditioning, different model class, or human spot-check). | $\langle\text{verdict}, \text{trace}\rangle$ on $S$ for concept $C$. |
| **Trainer** | $B$ | Generates exercises; runs the inner loop ([[proposed-method]]). May share weights with $M$. | Updated student weights. |
| **Student** | $S$ | Small (1–40B). Receives weight updates from $B$. | Trainable; everything else is read-only. |

Letting $M$, $V$, $B$ share a single model is the cheap default. Independence between $V$ and the others is the cheap hedge against rubber-stamp PASS verdicts (gap **A1** below).

## Algorithm

```
state:
    S          # student, mutable
    T  ← {}    # concept-identity hash → status
    snapshots  # checkpoint stack for rollback

function LearnConcept(c, depth=0):
    if depth > MAX_DEPTH:                  raise BudgetExceeded(c)
	    h ← Identity(c)
    if h ∈ T and T[h] = PASS:              return PASS

    # — Evaluation —
    eval ← V.Evaluate(S, c)
    if eval.verdict = PASS:
        T[h] ← PASS;  return PASS

    # — Diagnostic decomposition —
    prereqs ← M.Decompose(c, eval.trace)
    prereqs ← [p for p in prereqs if Identity(p) ∉ T or T[Identity(p)] ≠ PASS]

    if prereqs = ∅:                        # leaf: train directly
        snapshots.push(θ)
        Train(S, c, B)
        eval2 ← V.Evaluate(S, c)
        if eval2.verdict = FAIL: snapshots.pop_and_restore()
        T[h] ← eval2.verdict
        return eval2.verdict

    # — Recurse —
    for p in prereqs:
        LearnConcept(p, depth+1)

    # — Re-test the parent after children pass —
    eval3 ← V.Evaluate(S, c)
    if eval3.verdict = PASS:
        T[h] ← PASS;  return PASS

    # — Children passed but parent still fails: train parent directly —
    snapshots.push(θ)
    Train(S, c, B)
    eval4 ← V.Evaluate(S, c)
    if eval4.verdict = FAIL: snapshots.pop_and_restore()
    T[h] ← eval4.verdict
    return eval4.verdict
```

Differences from the bare user-sketch and from [[concept-curriculum-method]]'s §Variant:
- **`Identity(c)`** — DAG semantics; shared prereqs are not re-trained; cycles cannot recur.
- **`MAX_DEPTH`** — interactive expansion has no natural termination; without a bound it drifts into tangents.
- **Children-pass-but-parent-fails branch** — direct-train fallback before declaring unmasterable.
- **Snapshot rollback on `Train` failure** — bounds the blast radius of a bad packet.

## Components

| Id | Component | Source / status |
|---|---|---|
| **E1** | Multi-axis `Evaluate(S, c)` battery: correctness + contrast-set + counterfactual + MDL-on-siblings + explanatory probe. | Closes the memorisation false-positive. Tools captured in `raw/research/concept-understanding-eval/` (CheckList, Contrast Sets, GSM-Symbolic, MATH-Perturb, Counterfactual Tasks, Skill-Mix, Causal Abstraction, Hewitt&Liang, Embers). |
| **E2** | Qualitative-concept evaluation (rubric-graded short generation). | **No corpus precedent.** Open. |
| **E3** | `Identity(c)` canonical hash — embedding-similarity / MDL-equivalence / LLM-judged subsumption. | Closest precedent: [[../concept-learning/recursive-concept-evolution]] MDL-on-accept. **Update 2026-04-29:** [[../curriculum-and-decomposition/lecturebank]] and [[../curriculum-and-decomposition/concept-prereq-relations]] (PREREQ) provide concrete operationalisations via Doc2Vec / pairwise-link LDA + Siamese embedding distance. [[../curriculum-and-decomposition/auto-kc-generation]] gives the LLM-based recipe. |
| **D1** | `Decompose(c, trace)` — diagnostic teacher prompt that uses the failure trace, not just the concept name. | Closest precedent: [[../teacher-student-rl/saha-teacher-explanations]] Theory-of-Mind framing. **Update 2026-04-29:** [[../curriculum-and-decomposition/auto-kc-generation]] is the strongest single corpus signal — LLM-generated KCs beat human-written labels on KT (AUC 0.816 vs 0.797). The *failure-trace* conditioning specifically remains untested; no corpus paper extends LLM-KC-generation to trace input. **Update 2026-05-01:** [[../self-play/azr]]'s **three-mode reasoning decomposition** (deduction $(p,i)\to o$ / abduction $(p,o)\to i$ / induction $\{(i_j, o_j)\}_j \to p$) is a candidate alternative or complement to KC-style decomposition — concept-as-mode rather than concept-as-prereq. [[../self-play/info-gain-self-play]]'s epiplexity quantification shows induction carries 3–4× more learnable info than abduction/deduction, suggesting the modes are not equally useful for D1. Open question: does the abduction/deduction/induction triad apply to non-code concepts? |
| **D2** | Decomposition cost bound — `MAX_DEPTH`, max-prereqs-per-call, learnability filter. | [[../teacher-student-rl/soar-edge-of-learnability]] for the learnability filter. **Update 2026-04-29:** [[../curriculum-and-decomposition/acl-deep-rl-survey]] catalogues Learning Progress (LP), ALP-GMM, and teacher-student bandits as the canonical learnability filters. [[../curriculum-and-decomposition/poet]] provides minimal-criterion + novelty filtering. |
| **T1** | Inner training loop — [[proposed-method]] verbatim (RLT reward + sparse mask + EWC anchor + MDL on siblings + KL leash + reference-in-context). | Validation gate is the four-part contract from [[concept-curriculum-method]] §First experiment. |
| **T2** | Per-prereq EWC keyed on each prereq's TestSet. | [[../catastrophic-forgetting/ewc-gemma2-cpt]] anchor, lifted to per-concept granularity. **Untested at curriculum scale** ([[../rlvr-mechanics/rl-sparse-subnetwork]] capacity-bound section). |
| **T3** | Mask composition — freeze $M(c_1)\cap M(c_2)$ during $c_2$, or restrict $c_2$ to $M(c_1)^c$. | [[../rlvr-mechanics/rl-sparse-subnetwork]] capacity-bound section. **Untested.** |
| **T4** | Snapshot/rollback. | Standard checkpointing. |
| **R1** | Children-pass-parent-fail rule — default = direct-train (current). Alternatives: regenerate prereqs, deepen, escalate. | Empirical question; no corpus precedent. |
| **G1** | Compute budget tracker over total `Evaluate` + `Train` calls. | Engineering. |
| **G2** | Compositional root retest — items requiring ≥3 prereqs in novel combination, held out from $M, V, B$. | Mirrors the [[../teacher-student-rl/rlt-followups-2026]] ExGRPO concern about compositional inversion. |
| **A1** | Verifier independence — different model class for $V$ than $M, B$, or different prompt-conditioning, or periodic human spot-check. | Mitigates teacher-as-judge bias; no corpus method. |

## What each component buys, and what fails without it

| Drop | Failure mode |
|---|---|
| Without **E1** (multi-axis battery) | Single-accuracy PASS verdict fires on memorised TestSet patterns; whole tree compounds confidently-wrong concepts. |
| Without **E2** (qualitative eval) | Method only works for procedural concepts (multiplication, differentiation); fails on supply-and-demand, idealism. |
| Without **E3** (identity) | Lazy expansion re-trains shared prereqs across DAG branches; cycles silently inflate depth. |
| Without **D1** (diagnostic decomposition) | Teacher returns generic prereqs unrelated to the *observed* failure; method degenerates to up-front DAG enumeration with worse coverage. |
| Without **D2** (cost bound) | Recursion drifts into tangentially related skills on frontier topics; never terminates. |
| Without **T1** (inner loop) | Nothing actually trains. |
| Without **T2** + **T3** (forgetting protection) | Sibling concepts erode each other across recursion calls; root retest fails after all leaves pass. |
| Without **T4** (rollback) | A bad inner-loop step poisons all subsequent retests; no clean recovery. |
| Without **R1** (parent retest branch) | Algorithm has no rule when children PASS but parent FAILs; either deadlocks or silently exits. |
| Without **G1** (budget) | Compute amplification (depth × width × inner-loop-rounds) is unbounded. |
| Without **G2** (compositional retest) | Terminal claim "$S$ understands $C^\star$" is unverified beyond per-node tests. |
| Without **A1** (verifier independence) | Teacher-as-judge bias compounds silently across the whole recursion. |

## Known gaps

Numbered list synced with the conversation that produced this page. **Bold** items have no captured corpus method.

### Inherited from [[concept-curriculum-method]] §Variant

1. **Curriculum-level credit assignment.** Which missing prereq caused the parent failure? Step-level credit assignment ([[../process-reward-models/_overview]], [[../process-reward-models/pav-rewarding-progress]]) is per-trajectory. **Update 2026-04-29:** [[../curriculum-and-decomposition/options-framework]] (Sutton-Precup-Singh intra-option learning) is the closest theoretical tool — Theorems 1–3 give SMDP-style credit assignment for hierarchical decisions. Caveat: the curriculum state is non-Markov, so the formal optimality results don't transfer cleanly. [[../curriculum-and-decomposition/poet]]'s transfer-attempt step is the empirical analogue. Still open at the level of LLM curricula. **Update 2026-05-01:** Two new anchors from the self-play theme — [[../self-play/spiral]]'s **Role-conditioned Advantage Estimation (RAE)** gives multi-agent multi-turn credit assignment via per-game × role EMA baselines, and [[../self-play/sqlm]]'s **Goldilocks gate** ($0 < \lvert\{y_i = y_\text{maj}\}\rvert < N$) gives a per-prompt frontier signal. Both are flat-curriculum; lifting either to a *DAG* with parent-child credit-flow remains open. The dedicated [[proposer-reward-shapes]] page tabulates this against four other corpus reward shapes including SOAR's improvement-rate.
2. **Termination without an explicit frontier.** Up-front DAG bottoms out at "what the base student knows"; lazy expansion drifts.
3. **Cycle prevention via re-decomposition.** Lazy expansion can re-spawn an already-mastered concept under different framing. Identity check is not a corpus-validated tool at this level.
4. **TestSet reuse under retest.** A node may be retested after each prereq fills; same items used multiple times invite memorisation.
5. **Diagnosis ≠ decomposition.** "Decompose $c$" is corpus-attested. "Infer the missing prereq from $S$'s failure trace" is **not** at curriculum scale.

### New to RCL's framing

6. **Tree vs DAG.** Real prereq structures are DAGs (linear algebra is a prereq of both differential equations and ML). Pure-tree implementation re-trains shared prereqs and triples forgetting risk.
7. **Sibling forgetting.** Training $c_2$ after $c_1$ erodes $c_1$. Per-prereq EWC ([[../catastrophic-forgetting/ewc-gemma2-cpt]]) and mask composition ([[../rlvr-mechanics/rl-sparse-subnetwork]]) are candidates; **neither tested at curriculum scale**. The full [[../selective-finetuning/_overview]] theme (explicit-constraint answer) and [[../catastrophic-forgetting/_overview]] (implicit-constraint: RL forgets less than SFT) bear directly on T2/T3 here: [[../selective-finetuning/o-lora]] (orthogonal LoRA subspaces per prereq) and [[../catastrophic-forgetting/rls-razor]] (RFT-over-SFT for the inner loop) are the closest realisations; [[../moe-adapters/loramoe]] is the architectural-avoidance alternative (route per-prereq experts instead of masking).
8. **Pass/fail threshold uniformity.** A single threshold across heterogeneous concepts overfits the easy and underfits the hard.
9. **Confidence ≠ competence.** Single TestSet pass can be lucky-guess artefact. Calibrated confidence (multi-sample voting, contrast-set perturbation) needed; hooked to the captured-but-unintegrated GSM-Symbolic / MATH-Perturb / Counterfactual-Tasks / Contrast-Sets / Skill-Mix / CheckList papers.
10. **Open-ended / qualitative concepts.** No corpus method for evaluating idealism, supply-and-demand, etc. Closest is [[../concept-learning/concept-bottleneck-models]] (requires labelled concept vector) and [[../concept-learning/recursive-concept-evolution]] MDL test (requires concrete output space).
11. **Compute amplification.** Depth × width × inner-loop-rounds; needs explicit budget, not just `MAX_DEPTH`.
12. **Teacher role-conflict.** Single teacher generating eval, training items, decomposition, and training compounds errors silently.
13. **Curriculum-state checkpointing.** Recursion blow-up needs an undo (T4 above).
14. **Pre-test discard waste.** `Evaluate(S, c)` on entry consumes items; reusing them on retest is leakage; regenerating is expensive.
15. **Compositional retest.** Per-node mastery does not imply compositional mastery at $C^\star$.

## Deliverables to determine, test, and create

Restated from the design conversation as a single accountable list:

| Id | Deliverable | Validation |
|---|---|---|
| **E1** | Multi-axis evaluation battery on a procedural concept (e.g. multiplication). | Discriminate a memorising baseline (1-shot SFT on TestSet items) from a generalising baseline (multi-shot diverse training). |
| **E2** | Qualitative-concept evaluation (rubric + grader). | Two independent graders on one qualitative concept; Cohen's κ ≥ 0.8. |
| **E3** | `Identity(c)` function. | Hand-built canonical DAG (10 nodes); zero false-positives, zero false-negatives. |
| **D1** | Diagnostic `Decompose`. | A/B vs generic decomposition on a 3-node DAG; diagnostic converges in fewer node visits. |
| **D2** | Decomposition cost bound. | Recursion depth measured on 5 target concepts; bottoms out within bound. |
| **T1** | Inner training loop ([[proposed-method]]) on one concept. | Pass [[concept-curriculum-method]] §First-experiment four-part contract. |
| **T2** | Per-prereq EWC. | Two-prereq experiment; $c_1$ retention with vs without $c_1$-keyed Fisher. |
| **T3** | Mask composition. | Same two-prereq experiment, mask composition replacing EWC. Compare. |
| **T4** | Snapshot/rollback. | Inject bad packet; verify rollback restores prior PASS states. |
| **R1** | Children-pass-parent-fail rule. | Contrived case where direct-train-parent is wrong; verify algorithm escapes. |
| **G1** | Compute budget tracker. | RCL on a 3-node DAG within 2× the up-front-DAG baseline cost. |
| **G2** | Compositional root retest. | After full curriculum: pass-rate on $\text{TestSet}^\star$ ≥ pass-rate on individual node TestSets. |
| **A1** | Verifier independence. | Disagreement-rate between two independently-conditioned $V$s ≥ 5%; below that, suspect rubber-stamp. |

## Research list keyed to RCL

Tags: **(a)** evaluation, **(b)** decomposition, **(c)** training inner loop, **(d)** forgetting protection, **(e)** theory.

### Tier 1 — gates the MVP

| # | Page | Tag | Why |
|---|---|---|---|
| 1 | [[concept-curriculum-method]] §Variant | (b) | The exact algorithm with prior gap analysis. Read first. |
| 2 | [[proposed-method]] | (c) | The inner loop. RCL is the outer loop wrapping this. |
| 3 | [[../concept-learning/recursive-concept-evolution]] | (a)+(b) | $F(x)=H/(M+\varepsilon)$ failure score; MDL on siblings. Closest corpus precedent for spawn-on-failure + accept-on-compression at the *concept-library* level. RCL lifts this to the *curriculum* level. |
| 4 | [[../teacher-student-rl/sakana-rlt]] | (c) | Reward function + teacher-given-(Q,A) packet shape for `Train`. |
| 5 | [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] | (a) | CoT-Pass@K format-vs-substance separator; one axis of `Evaluate`. |
| 6 | [[../teacher-student-rl/saha-teacher-explanations]] | (b) | Theory-of-Mind framing for *when/how* a teacher diagnoses; closest precedent for `Decompose(c, trace)`. |

### Tier 2 — needed once MVP works

| # | Page | Tag | Why |
|---|---|---|---|
| 7 | [[../catastrophic-forgetting/ewc-gemma2-cpt]] | (d) | EWC anchor for forgetting protection. T2 deliverable. |
| 8 | [[../rlvr-mechanics/rl-sparse-subnetwork]] | (d) | Mask composition for forgetting protection. T3 deliverable. |
| 9 | [[../teacher-student-rl/soar-edge-of-learnability]] | (b) | Bilevel meta-RL: teacher reward = student improvement. Direct candidate for "did this prereq actually unblock the parent?" — also a learnability filter for D2. |
| 10 | [[../teacher-student-rl/knowrl]] | (a)+(c) | Atomic knowledge-points + Constrained Subset Search — minimal-sufficient hint design; informs concept granularity. |
| 11 | [[../teacher-student-rl/rlt-followups-2026]] (ExGRPO, OPSD) | (a) | Explanatory probes — third axis of `Evaluate`; OPSD as cheap single-model trainer. |
| 12 | [[../single-sample-rl-finetuning/data-efficiency-rft]] | (a)+(c) | DOTS $p=0.5$ rule for calibrating both eval-item difficulty and training-item difficulty. |

### Tier 3 — newly captured (concept-evaluation theme; see [[../concept-evaluation/_overview]])

| # | Source | Tag | Why |
|---|---|---|---|
| 13 | GSM-Symbolic (Mirzadeh et al., ICLR 2025) | (a) | Symbolic-template perturbations expose memorisation in math reasoning; direct payload for E1 on procedural concepts. |
| 14 | MATH-Perturb (Huang et al., 2025) | (a) | Hard perturbations break the original solution path. Closes E1 for advanced math concepts. |
| 15 | Counterfactual Tasks (Wu et al., 2023) | (a) | Same abstract task, counterfactual content (base-9, modified chess). The cleanest "abstraction vs procedure" axis. |
| 16 | Skill-Mix (Yu, Kaur, Gupta, Brown-Cohen, Goyal, Arora, 2023) | (a) | Compositional combination of $k$ skills; direct prior art for G2 (compositional root retest). |
| 17 | CheckList (Ribeiro et al., ACL 2020) | (a) | Capability × test-type matrix (MFT/INV/DIR). Methodological frame for E1 across domains. |
| 18 | Contrast Sets (Gardner et al., EMNLP 2020) | (a) | Local-decision-boundary perturbations — operationalises the proposed-method **V** sibling-set construction. |
| 19 | Causal Abstraction (Geiger et al., JMLR 2025) | (a)+(e) | Interchange-intervention accuracy as concept-fidelity metric distinct from behavioral accuracy; alternative to MDL for E1. |
| 20 | Designing Probes with Control Tasks (Hewitt & Liang, EMNLP 2019) | (a) | Selectivity floor — any concept-probe must beat a random control task. |
| 21 | Embers of Autoregression (McCoy et al., PNAS 2024) | (a)+(e) | Task/output/input probability predict LLM accuracy on deterministic tasks. Diagnostic prior for *why* understanding-evals are hard. |

### Tier 4 — newly captured (curriculum-and-decomposition theme; see [[../curriculum-and-decomposition/_overview]])

| # | Page | Tag | Why |
|---|---|---|---|
| 22 | [[../curriculum-and-decomposition/auto-kc-generation]] | (b) | **Strongest single corpus signal that D1 is feasible.** LLM-generated KCs beat human-written labels on KT (AUC 0.816 vs 0.797). |
| 23 | [[../curriculum-and-decomposition/dkt]] | (a) | KT canon; backbone for `Evaluate` confidence calibration; influence-function variant relevant to D1 prereq inference. |
| 24 | [[../curriculum-and-decomposition/lecturebank]] | (b)+(e) | Canonical NLP prereq dataset; concrete operationalisation of E3 (concept identity) via prereq-pair labels. |
| 25 | [[../curriculum-and-decomposition/concept-prereq-relations]] | (b) | PREREQ method — pairwise-link LDA + Siamese network for asymmetric prereq inference. Non-LLM baseline for D1. |
| 26 | [[../curriculum-and-decomposition/options-framework]] | (e) | HRL canon. RCL's `LearnConcept(p)` is structurally an option ⟨I, π, β⟩. Intra-option learning for curriculum credit assignment (gap #1). |
| 27 | [[../curriculum-and-decomposition/bengio-curriculum]] | (b) | Curriculum-as-continuation-method theoretical frame. The "decompose to prereqs first" non-convex argument. |
| 28 | [[../curriculum-and-decomposition/curriculum-survey]] | (b) | Soviany et al. 2022 — broad taxonomy of curriculum-learning approaches. |
| 29 | [[../curriculum-and-decomposition/acl-deep-rl-survey]] | (b)+(c) | RL-specific curriculum survey. LP / ALP-GMM as candidates for D2 learnability filter. |
| 30 | [[../curriculum-and-decomposition/poet]] | (b) | Co-evolving environments + agents + transfer attempts; closest spirit-match to RCL's failure-driven lazy DAG. |

### Tier 5 — corpus-external, future `/research` (post-ingest residue)

After Tiers 3 and 4 ingests, the original 6-item corpus-external list reduces to 2 still-open topics:

| # | Topic | Tag | Why |
|---|---|---|---|
| 31 | Compositional generalisation benchmarks (SCAN, COGS, CFQ) | (a) | Direct prior art for **G2** (compositional root retest). [[../concept-evaluation/skill-mix]] partially covers this; SCAN/COGS/CFQ are stricter and synthetic. |
| 32 | Failure-trace-conditioned LLM concept decomposition | D1 (deeper) | The 2025 [[../curriculum-and-decomposition/auto-kc-generation]] result generates KCs from problem text, not failure traces. The trace-conditioned variant of D1 has no corpus prior; this is the single *deepest* gap remaining. |

## Relation to the other three synthesis pages

| Aspect                | [[single-sample-concept-skeleton]] | [[proposed-method]]      | [[concept-curriculum-method]]     | This page (RCL)                       |
| --------------------- | ---------------------------------- | ------------------------ | --------------------------------- | ------------------------------------- |
| Unit of training      | One example                        | One example              | One concept (packet $\geq 1$)     | One *failure* (packet $= 1$ trace)    |
| Outer structure       | None                               | None                     | Pre-built DAG, bottom-up          | **Lazy DAG, top-down failure-driven** |
| When DAG is built     | n/a                                | n/a                      | Up-front by teacher               | **On demand from failure traces**     |
| Frontier estimation   | n/a                                | n/a                      | Estimated by teacher              | **Measured by passes/failures**       |
| Inner loop            | RCE+Balashov+L2T+CAI               | RLT+RCE+Balashov+EWC+ref | Open (RLT+textbook proposed)      | **= [[proposed-method]]**             |
| Forgetting mitigation | Not addressed                      | EWC anchor (F)           | Untargeted v1; EWC/mask candidate | **Per-prereq EWC + mask composition** |
| Compositional retest  | n/a                                | n/a                      | Implicit at $C^\star$             | **Explicit (G2 deliverable)**         |
| Teacher-burden        | Light                              | Medium                   | Heavy                             | **Heavy + diagnostic**                |

RCL is the *outer-loop dual* of [[proposed-method]]: where proposed-method is the per-concept inner algorithm, RCL is the across-concept recursion that decides which concepts to train. It is the *failure-driven* dual of [[concept-curriculum-method]]: same concept-DAG ontology, opposite construction order (lazy vs eager).

## Phase 0: Component proof on a single non-recursive concept

The recursion is decoration until the leaf primitives work. **Phase 0 reduces RCL to its leaf path** — `Evaluate → Train → Re-evaluate`, no decomposition exercised. Pick one simple concept the student can already partially do, prove the three components (dataset, evaluation, training) in isolation, and only then graduate to Phase 1.

### Concept-choice criteria

- **Procedural with crisp correctness.** Avoid qualitative concepts in Phase 0 — they entangle E1 (battery) with E2 (qualitative-eval gap).
- **No prereq decomposition needed.** The student can already produce *some* correct answers; training improves consistency under perturbation.
- **Easy to perturb without changing the abstraction.** Counterfactual and contrast variants must be mechanically constructible.
- **Short textbook.** A 1-page reference suffices.
- **No tooling dependency.** Pure-text in/out — no calculator or compiler in the loop yet.

**Recommended defaults** (pick one in A1):
- "Solve a single-variable linear equation $ax+b=c$ for $x$."
- "Convert a decimal integer $n \in [0,255]$ to binary."
- "Compute $(a \times b) \bmod n$ for small $a, b, n$."

All three pass the criteria. Linear equations is closest to the wiki's existing math frame ([[../single-sample-rl-finetuning/1-shot-rlvr]] uses MATH/AIME); decimal-to-binary maximises clean perturbation surface (different bases as counterfactuals).

### Locked decisions (2026-04-28)

| Decision | Value | Notes |
|---|---|---|
| Target concept (A1) | **Modular multiplication** $(a \times b) \bmod n$ | Linear equation and decimal-to-binary held as fallbacks. |
| Base student (A2) | **Qwen2.5-1.5B** | Capacity caveat — escalate to 7B before declaring method falsified. |
| Sibling generator (B4) | **LLM-generated, audited** | Teacher LLM with faithfulness sample-audit; validates the teacher pipeline in parallel. |

### Workstreams and prioritised task list

Critical path: **A → B → C → C9 (gate) → D → E**. C9 is the no-go checkpoint before training begins.

#### A. Setup and infrastructure (P0)

| # | Task | Output | Notes |
|---|---|---|---|
| A1 | Choose the Phase-0 target concept | One concept-name string | **Locked 2026-04-28: modular multiplication** — compute $(a \times b) \bmod n$ for small $a, b, n$. Linear equation and decimal-to-binary remain as fallbacks if mod-mult turns out to be too easy or too contaminated. |
| A2 | Choose base student $S$ | Model id | **Locked 2026-04-28: Qwen2.5-1.5B.** Caveat noted by David: 1.5B may lack capacity to produce meaningful concept installation; if Phase-0 results are weak across the four-part contract, escalate to Qwen2.5-7B (matches Sakana RLT student class — [[../teacher-student-rl/sakana-rlt]]) before declaring the method falsified. |
| A3 | Choose teacher $M{=}V{=}B$ for Phase 0 | Model id (frontier) | Single shared teacher in Phase 0; verifier-independence (A1 deliverable) deferred to Phase 2. |
| A4 | Set up training stack | Working repo | HF `transformers` + `trl` + `accelerate`; or vLLM + custom GRPO. Dr. GRPO recommended ([[../rl-optimizers/dr-grpo]]). |
| A5 | Set up evaluation harness skeleton | `eval/` module | Just enough to run a model against a battery of scorers and emit a JSON report. |

#### B. Concept-level dataset (P1)

| # | Task | Output | Notes |
|---|---|---|---|
| B1 | Author the Textbook for the chosen concept | `Textbook(c).md` | One page. Stays in the prompt during every gradient step (proposed-method **C**). |
| B2 | Generate Examples (Q, E, A) triples, $N{=}10$ | `examples.jsonl` | Diverse $E$ per [[../teacher-student-rl/ho-reasoning-teachers]]; sweep $N\in\{1,5,10\}$ later. |
| B3 | Generate held-out TestSet | `testset.jsonl` | Strictly disjoint from Examples; size 50–100. |
| B4 | Generate Siblings | `siblings.jsonl` | **Locked 2026-04-28: LLM-generated, audited.** Teacher LLM produces concept-family variants following the contrast-set recipe ([[../concept-evaluation/contrast-sets]]); audit step samples a subset for human/independent-LLM faithfulness verification. Validates the teacher pipeline at the same time as building the dataset. Fallback to manual if audit fails. |
| B5 | Generate Counterfactual variants | `counterfactual.jsonl` | Same abstraction, different surface (e.g., binary→base-5; $ax+b=c$→base-9 arithmetic inside). Recipe from [[../concept-evaluation/counterfactual-tasks]]. |
| B6 | Generate Contrast set | `contrast.jsonl` | Minimal label-flipping perturbations of TestSet items. Recipe from [[../concept-evaluation/contrast-sets]]. |
| B7 | Audit dataset | `dataset_audit.md` | Leakage check (no TestSet item near-duplicate of any Example); difficulty calibration to $p\approx0.5$ ([[../single-sample-rl-finetuning/data-efficiency-rft]]). |

#### C. Evaluation battery (P2 — gates training)

| # | Task | Output | Notes |
|---|---|---|---|
| C1 | Correctness scorer | `eval/correct.py` | Binary or fuzzy answer-match. |
| C2 | Contrast-set pass-rate scorer | `eval/contrast.py` | Per Gardner et al.; expect ~25% drop vs raw TestSet on a memoriser. |
| C3 | Counterfactual pass-rate scorer | `eval/counterfactual.py` | Per Wu et al.; default-vs-counterfactual gap = procedure-vs-abstraction signal. |
| C4 | MDL-on-siblings scorer | `eval/mdl.py` | Compression estimator — RCE recipe ([[../concept-learning/recursive-concept-evolution]]); flag if vision-only operationalisation fails to port to text. |
| C5 | Explanatory-probe scorer | `eval/probe.py` | LLM-as-judge for CoT coherence. ExGRPO-style ([[../teacher-student-rl/rlt-followups-2026]]). |
| C6 | Run battery on untrained base | `baselines/base.json` | Record numbers for every axis. |
| C7 | Build memorising baseline (SFT on TestSet) | `baselines/memoriser.ckpt` | Should ace TestSet, fail contrast/counterfactual/MDL — proves the battery isn't fooled. |
| C8 | Build generalising baseline (multi-shot diverse SFT) | `baselines/generaliser.ckpt` | Should pass the full battery — proves the battery is achievable. |
| **C9** | **Discrimination gate** | Pass/fail | The battery distinguishes C7 from C8 on contrast/counterfactual/MDL. **No-go on training if this fails.** |

#### D. Inner training loop (P3 — proposed-method components)

| # | Task | Output | Notes |
|---|---|---|---|
| D1 | Reference-in-context prompting | `train/reference_prompt.py` | Textbook prepended to every rollout. |
| D2 | RLT reward $r^{SS} - \lambda r^{KL}$ | `train/reward.py` | Per [[../teacher-student-rl/sakana-rlt]]. |
| D3 | Failure trigger $F(x){=}H/(M+\varepsilon)$ | `train/trigger.py` | Skip-known-items gate. |
| D4 | Sparse mask via $\lvert F\cdot\theta\rvert$ top-$k$ | `train/mask.py` | LayerNorms excluded; $k$ small enough for ~5–30% sparsity ([[../rlvr-mechanics/rl-sparse-subnetwork]]). |
| D5 | EWC Fisher anchor | `train/ewc.py` | Diagonal Fisher on a small held-out general task; $\lambda_{\text{EWC}}$ swept ([[../catastrophic-forgetting/ewc-gemma2-cpt]]). |
| D6 | MDL sibling validation gate | `train/mdl_gate.py` | Commit step iff $\Delta DL(\text{siblings})<0$; revert otherwise. Component **V**. |
| D7 | Stopping signal | `train/stop.py` | Info-gain plateau + MDL stable. Component **S**. |
| D8 | Diversity sampling | `train/sample.py` | Group $G\geq4$; entropy bonus. Component **G**. |
| D9 | Wire as Dr. GRPO outer loop | `train/loop.py` | End-to-end RL trainer. |

#### E. Four-part contract validation (P4)

| # | Task | Output | Pass criterion |
|---|---|---|---|
| E1 | Run inner loop on the packet | Training run | Completes without divergence. |
| E2 | TestSet pass-rate | Number | Strictly above C6 (untrained baseline). |
| E3 | MDL on siblings | Number | $\Delta DL < 0$ post-training vs pre-training. |
| E4 | Explanatory-probe coherence | Number | Non-regressive vs C6. |
| E5 | KL / mask ablation | Comparison | Removing KL leash OR mask shows fluency degradation; with both intact, no degradation. |
| E6 | Beat critique-FT baseline | Comparison | RL stack beats SFT-on-critique-pairs on the battery ([[../single-sample-rl-finetuning/critique-ft-one-problem]]). |
| E7 | Phase 0 report | `wiki/research/experiments/phase-0-report.md` | Go/no-go for Phase 1. |

### Phase 0 dependency graph

```
A1 ──┬──> A2,A3,A4,A5 (parallel)
     │
     └──> B1 ──> B2,B3 (parallel) ──> B4,B5,B6 (parallel) ──> B7
                                                                │
                                                                ▼
                                          C1,C2,C3,C4,C5 (parallel) ──> C6 ──> C7,C8 (parallel) ──> C9
                                                                                                     │ pass
                                                                                                     ▼
                                                                            D1..D9 (mostly parallel) ──> D9 wire
                                                                                                          │
                                                                                                          ▼
                                                                                          E1 ──> E2,E3,E4,E5 (parallel) ──> E6 ──> E7
```

### Phase 0 falsifiers (any one kills the method)

1. **C9 fails** — the battery cannot distinguish a memoriser from a generaliser. The whole "concept vs pattern" frame is unmeasurable on this concept.
2. **E2 fails** — TestSet doesn't rise above untrained baseline. The training loop doesn't adapt; revisit reward, mask, or sample diversity.
3. **E3 fails while E2 passes** — pattern memorised, concept not installed. Revisit sibling-set construction (B4) and reward shaping.
4. **E4 fails** — explanations regress while answers improve. Memorisation again, in a more subtle form.
5. **E5 fails** — model fluency collapses without the KL/mask guardrails. The bounded-edit story is broken.
6. **E6 fails** — RL stack does not beat critique-FT. The RL machinery isn't earning its complexity.

Pass all six → graduate to Phase 1.

## Phase 1: validate the recursion at $N=3$

*Only after Phase 0 passes.*

**Scope.** A 3-node hand-built DAG (e.g. `addition → multiplication → simple linear equations`), but the algorithm is *not told* the DAG. Start the student at the root; observe; let the recursion materialise.

**Pass/fail contract:**

1. The algorithm reaches the right leaves via failure-driven recursion (D1 working).
2. Each leaf passes its TestSet via `Train` (T1 working — i.e. Phase 0 contract holds at the leaf).
3. After all leaves pass, the *root* TestSet passes without further training, OR the children-pass-parent-fail branch fires once and recovers (R1 working).
4. Sibling forgetting: $c_1$'s post-training TestSet pass-rate after $c_2$ trains is within a tolerance (T2/T3 working).
5. Compute budget within 2× the equivalent up-front-DAG baseline (G1 working).

**Falsification.** RCL is dead if any of (i) $V$'s verdicts are uncalibrated (E1 fails), (ii) $M$ surfaces wrong prereqs from the trace (D1 fails), (iii) sibling forgetting wipes $c_1$ before root retest (T2/T3 fail), (iv) compute exceeds 5× the up-front baseline (G1 fails).

## Open questions

1. **Should the trainer $B$ see the parent-concept context when training a child $c_i$?** Reference-in-context (proposed-method **C**) suggests yes — child training is *for the sake of* the parent. But this couples child training to a possibly-wrong parent framing.
2. **What if the wrong prereqs are returned?** The retest-after-children branch catches this for the parent, but a *prereq* trained on a wrong premise wastes compute and risks pollution. No detector specified.
3. **Granularity floor.** When does `Decompose` stop returning prereqs and the algorithm hit a leaf? For procedural concepts, "the student already knows arithmetic" is a clean floor; for qualitative concepts, it's not.
4. **Can RCL bootstrap its own concept identity?** I.e. can the model that runs $V$ also build the `Identity(c)` similarity space, or does that need separate training?
5. **Where does this method belong in the project?** Single-sample at the *failure-trace* level, not at the example level. Decision needed on whether the project's "single-sample" frame extends to this.

## Source

Editorial proposal captured 2026-04-28 from a design conversation with David. Refines and elevates the §Variant section of [[concept-curriculum-method]]. Inner loop is [[proposed-method]]; evaluation battery wires in the [[../concept-evaluation/_overview|concept-evaluation theme]] (GSM-Symbolic, MATH-Perturb, Counterfactual Tasks, Skill-Mix, CheckList, Contrast Sets, Causal Abstraction, Hewitt&Liang, Embers).

## Related

- [[concept-curriculum-method]] — eager-DAG sibling; §Variant is RCL's direct ancestor
- [[proposed-method]] — the inner training loop RCL invokes per leaf
- [[single-sample-concept-skeleton]] — earliest synthesis; RCL inherits its primitives via proposed-method
- [[../concept-learning/recursive-concept-evolution]] — RCE spawn-on-failure + MDL-on-accept; RCL is the curriculum-scale analogue
- [[../teacher-student-rl/saha-teacher-explanations]] — Theory-of-Mind diagnostic intervention; closest precedent for D1
- [[../teacher-student-rl/soar-edge-of-learnability]] — bilevel teacher reward + learnability filter; candidate for D2
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — Fisher anchor; per-prereq variant is T2
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — sparse mask + capacity bound; mask composition is T3
