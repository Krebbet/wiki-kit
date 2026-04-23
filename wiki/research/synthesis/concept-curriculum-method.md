---
name: concept-curriculum-method
description: Teacher-built hierarchical concept curriculum with test-train-retest loops per node. Powerful teacher (with world access) decomposes a goal topic into a concept DAG and materialises (Q, E, A, textbook) packets per concept; frozen-vocabulary student is trained bottom-up, one concept at a time, until it passes held-out tests. Third editorial method proposal on this wiki, distinct from single-sample-concept-skeleton and proposed-method.
type: research
---

# Concept-Curriculum Method

Editorial proposal captured from a conversation with David on 2026-04-23. Third method sketch on this wiki after [[single-sample-concept-skeleton]] (primitive composition) and [[proposed-method]] (reference-grounded RLT-flavoured single-sample). **This sketch is distinct in that it starts from a *hierarchical concept DAG* rather than a single training example, and runs a test-train-retest loop per concept node.**

## One-line

A powerful world-access *teacher* model decomposes a goal topic (e.g. undergrad calculus, or a specific proof) into a dependency DAG of supporting concepts; for each node it synthesises a learning packet (textbook body, (Q, E, A) triples, held-out tests); a small *student* model is trained bottom-up, one concept at a time, with a test-fail-train loop per node, until it can answer both concept-understanding and concept-application questions without external help.

## Roles

| Role | Capability | Access | Optimisation |
|---|---|---|---|
| **Teacher** ($T$) | Large, strong. Knows the target domain. | Open web, reference texts, tools, scratchpad. Read-only w.r.t. student. | None — frozen. Used as a compiler from "goal topic" to "curriculum packets". |
| **Student** ($S$) | Small (1–40B, per project scope). | Only what $T$ provides: the packet for the concept currently being trained, plus any residual behaviour from earlier concepts. | Yes — weights updated via RL fine-tuning per packet. |

This is the axis highlighted in [[../teacher-student-rl/_overview]] as "does the teacher see the answer?" — here the teacher *builds the answer*, including the reference material the student is graded against. The student operates under *information asymmetry*: it learns what the teacher deems sufficient.

## Steps (detailed)

### (a) Goal → concept DAG

$T$ takes the target concept $C^\star$ (e.g. "fundamental theorem of calculus") and produces:
1. A *root set* $\{C^\star\}$.
2. Recursive decomposition: for each node $C$, list its *prerequisite concepts* $\text{prereq}(C)$ (other concepts required to understand or apply $C$).
3. A directed acyclic graph $\mathcal{G} = (V, E)$ where $V$ is the concept set and $(C_i \to C_j) \in E$ iff $C_i \in \text{prereq}(C_j)$.
4. Topological sort of $\mathcal{G}$ → curriculum order $C_1 \prec C_2 \prec \ldots \prec C_n = C^\star$.

**Termination rule:** a prerequisite edge stops when $T$ judges that a *realistic base model* already has that concept (e.g. base arithmetic for an LLM). That frontier — "what does the student already know" — is itself an estimate that $T$ must make.

### (b) Per-concept packet construction

For each concept $C$ in curriculum order, $T$ produces a *packet*:

$$\text{Packet}(C) = \big\langle \text{Textbook}(C),\ \text{Examples}(C),\ \text{TestSet}(C) \big\rangle$$

where:
- $\text{Textbook}(C)$: the main body of explanatory material for $C$ — dense, self-contained given that $\text{prereq}(C)$ are mastered. Analogous to the body of a textbook chapter.
- $\text{Examples}(C)$: a small set of $(Q, E, A)$ triples — Question, worked Explanation, final Answer. This is the RLT-shape (Q + worked solution) from [[../teacher-student-rl/sakana-rlt]], materialised ahead of time by $T$.
- $\text{TestSet}(C)$: held-out items that $S$ has *not* seen, testing (i) concept recall and (ii) novel application. Kept strictly disjoint from $\text{Examples}(C)$.

Design choice: the ratio of conceptual-recall to novel-application test items matters. Straight recall catches memorisation; novel application catches concept vs pattern (see [[../concept-learning/recursive-concept-evolution]]'s MDL sibling test for the hardest version of this).

### (c) Dependency tree → curriculum order

Curriculum follows the topological sort. The simplest is bottom-up: train on $C_1$ first (the most rudimentary), then $C_2$, ..., terminating at $C^\star$. Variants to consider later: interleaved (spaced-repetition style revisiting of earlier $C_i$ to combat catastrophic forgetting), branch-depth-first (exhaust one subtree before moving to the next).

### (d) Per-concept training algorithm (open — the hard part)

For each $C$ in curriculum order:

```
given: current student S, packet(C) = (Textbook, Examples, TestSet)
repeat:
    test S on TestSet(C)   → pass_rate
    if pass_rate >= threshold(C):
        break  # concept mastered, move on
    else:
        train S on packet(C) using an inner loop
        (inner loop = the open design question)
end
```

The inner loop is where the wiki corpus intersects most heavily. Candidates, in declining closeness to the teacher-builds-the-solution paradigm:

| Inner loop candidate | Corpus ref | What it gives | What it costs |
|---|---|---|---|
| **RLT-flavour** — student scored on $\log \pi_S(A \mid Q, E, \text{Textbook})$ | [[../teacher-student-rl/sakana-rlt]] | Dense per-token reward; textbook naturally fills the "reference in context" role | Requires differentiable likelihood access; packet's $E$ must not leak into the eval |
| **OPSD-flavour** — same model plays teacher (with solution) and student (without); reverse-KL between the two on student trajectories | [[../teacher-student-rl/rlt-followups-2026]] | No second model needed; same information asymmetry | Student and "privileged self" must be distinguishable; needs verified reasoning traces |
| **1-shot RLVR** on each $(Q, A)$ as a single training datum | [[../single-sample-rl-finetuning/1-shot-rlvr]] | Proven existence at $N=1$; post-saturation generalisation | Packet has $\geq 1$ example; diminishing return past the first; sparse reward |
| **ExGRPO / explanatory probes** — generate probes that test the *logic* behind $A$; reward coherent reasoning across probes | [[../teacher-student-rl/rlt-followups-2026]] | Specifically targets memorisation-vs-understanding | Requires probe generation by $T$; adds compute |
| **Critique-fine-tune on one problem** — $T$ critiques $S$'s attempts, student SFTs on the critique | [[../single-sample-rl-finetuning/critique-ft-one-problem]] | Captures *why* an answer is wrong, not just *that* it is | Not RL; no exploration; sample-efficient but doesn't build from rollouts |

The natural composition is probably *RLT-flavour reward + textbook-in-context + 1-shot RLVR–style single-packet rollouts + GRPO/DAPO/Dr. GRPO as the outer optimiser* (see [[../rl-optimizers/_overview]] for the optimiser lineage and [[../rl-optimizers/dr-grpo]] for the length-bias fix). But this is an open design choice — brainstorm required. *(editorial — this is a design opinion, not a result from any captured source)*

### (e) Test-train-retest loop per concept

Per concept $C$:
1. **Test** $S$ on $\text{TestSet}(C)$. Compute pass rate.
2. **Pass**: move to the next concept.
3. **Fail**: run one round of the inner loop on $\text{Packet}(C) \setminus \text{TestSet}(C)$, then retest.
4. Repeat with a bounded budget (max rounds or max compute per concept).

Stopping criterion is per-concept, not per-epoch. A concept is "done" when $S$ passes a held-out test, not when the loss converges on the training items.

### (f) Terminal state

When the curriculum's last concept $C^\star$ is mastered, $S$ should by construction have the full dependency chain. The hope: $S$ now has "foundational understanding" of the DAG — understanding that does not depend on external help at inference time.

## Per-step assessment

### Step (a): Goal → DAG

**Strengths:**
- Matches how humans actually structure learning; has precedent in curriculum learning research *(editorial)*.
- Makes the training objective *auditable* — we can see what $S$ is being asked to know.
- $T$'s world access means decomposition quality can be very high.

**Weaknesses:**
- DAG construction is open-ended; two teachers may produce very different DAGs for the same goal, and the wiki has no captured method for auditing concept-DAG correctness.
- The "what does the base student already know" frontier estimate is error-prone — if $T$ overestimates student prior knowledge, crucial prereqs are omitted; if it underestimates, training wastes budget on concepts already present.

**Unknowns:**
- Granularity. How fine-grained should a "concept" be? A whole chapter? A single lemma? Corpus has no direct guidance. [[../concept-learning/concept-bottleneck-models]] uses supervised discrete concept coordinates; [[../concept-learning/recursive-concept-evolution]] uses low-rank subspaces spawned on failure — neither maps cleanly to a curriculum DAG.
- DAG width vs depth tradeoff. Deep skinny chains are simpler; wide branching increases forgetting risk.

**Challenges:**
- Measuring DAG completeness. How do you know $T$ didn't miss a prereq? Detection only happens when $S$ fails a downstream concept for a surprising reason.
- Determinism: if we re-run the method, the DAG may differ. Reproducibility suffers.

### Step (b): Packet construction

**Strengths:**
- Directly materialises the RLT "teacher given (Q, A) generates worked solution" primitive ([[../teacher-student-rl/sakana-rlt]]) at curriculum scale.
- Held-out test set enforces a pass/fail contract. This is stronger than loss-convergence.
- Textbook-in-context is a setup [[../synthesis/proposed-method]] already calls out as the novel element of the method design.

**Weaknesses:**
- Test/training set leakage is a persistent risk — $T$ generates both; separation must be verified.
- Packet size trades off with "1-shot" purity. At 20 examples per concept, across say 30 concepts, the student has seen 600 examples — not "single-sample" anymore. The [[../single-sample-rl-finetuning/1-shot-rlvr]] result shows a *single* example suffices for a strong prior; it is not established that 20 examples are strictly better than 1 *within* a concept.
- Textbook + Examples + TestSet tripling — $T$ has to generate all three consistently, for every concept. Compute cost and consistency both nontrivial.

**Unknowns:**
- Example diversity requirement. [[../teacher-student-rl/ho-reasoning-teachers]] shows diversity of reasoning is load-bearing; [[../teacher-student-rl/sakana-rlt]] shows reward correlates $r=0.89$ with student gain. Neither tells us the minimum diversity for curriculum packets.
- Whether explanation $E$ should be present in the student's context during training. If yes, student learns to *use* $E$; if no, student must reconstruct it — different skills.
- Test difficulty calibration. Per [[../single-sample-rl-finetuning/data-efficiency-rft]] Theorem 1, gradient magnitude is maximised when $p = 0.5$; if tests are too easy or too hard, train-signal is weak.

**Challenges:**
- Generating *novel* application tests that require the concept but don't appear in $\text{Textbook}$ or $\text{Examples}$. $T$ may accidentally produce near-duplicates.
- Grading the student's answers on TestSet. For math, answer-equality is tractable; for proofs or open-ended reasoning, $T$ must also *judge*, which introduces its own error.

### Step (c): Curriculum order

**Strengths:**
- Topological order is principled.
- Separates "what's hard because the concept is hard" from "what's hard because prereqs are missing" — when training on $C_k$, by construction $C_1 \ldots C_{k-1}$ are mastered.

**Weaknesses:**
- Serial curriculum is slow. No parallelism across DAG branches.
- Single-pass topological sort does not address [[../catastrophic-forgetting/ewc-gemma2-cpt]]'s catastrophic-forgetting problem — later concepts can overwrite earlier ones.

**Unknowns:**
- Whether to revisit earlier concepts (spaced repetition) or trust that later concepts compositionally exercise them. Human pedagogy uses revisiting; no captured corpus source evaluates this for LLMs under RL.
- Whether EWC anchors ([[../catastrophic-forgetting/ewc-gemma2-cpt]]) or a Balashov-style sparse mask ([[../rlvr-mechanics/rl-sparse-subnetwork]]) — applied per concept — are sufficient to prevent forgetting without a revisit schedule.

**Challenges:**
- Diamond-shaped dependencies (two concepts share a prereq used differently): topological sort picks *some* linearisation but not necessarily the right one.
- Adaptive curriculum (skip mastered concepts) sounds desirable but requires a pre-test the student passes — which means generating a TestSet you may then throw away.

### Step (d): Inner loop training algorithm

**Strengths:**
- The wiki has strong candidates for the inner loop (see the table above).
- The "information asymmetry" shape of student-sees-textbook-teacher-scores is directly supported by [[../teacher-student-rl/sakana-rlt]]'s empirical result (7B teacher beats 670B teachers).

**Weaknesses:**
- **This is genuinely open.** The user has explicitly flagged this as the step requiring most design work. None of the candidate inner loops in the corpus is proven at the "small curriculum, $N \approx 10$–$100$ examples per concept" scale that the project targets.
- Compute per concept is high if a full RL loop runs per node.

**Unknowns:**
- Which reward signal works best in this setting: student log-prob of $A$ given $(Q, E, \text{Textbook})$? Or binary pass/fail on application? Or process-alignment ([[../teacher-student-rl/pm4grpo]])? Or information-gain ([[../rlvr-mechanics/learning-to-think]])?
- Whether the textbook-in-context survives the RL loop without the student just learning to copy it.
- Whether [[../rl-optimizers/dr-grpo]]'s bias fixes or [[../rl-optimizers/dapo]]'s Dynamic Sampling help or hurt in this curriculum regime.

**Challenges:**
- Zero-variance collapse. If $S$ always passes a concept's TestSet immediately, the inner loop produces no signal. (DAPO's Dynamic Sampling filters these out at scale — but if one concept in the curriculum already passes, skip-and-move-on is likely the right behaviour anyway.)
- Conversely, if $S$ never passes, the inner loop runs forever. A compute budget per concept is essential.
- Textbook size vs context window: a full textbook chapter may not fit at training time. Some form of retrieval or chunking is needed. Wiki has no captured source covering *training-time* retrieval (as opposed to RAG at inference time) — explicit gap flagged in [[proposed-method]].

### Step (e): Test-train-retest loop

**Strengths:**
- Pass/fail gating is principled. Matches how exams work.
- Avoids the "is it converged?" ambiguity of loss-watching.

**Weaknesses:**
- Risk of overfitting to TestSet if the loop retrains, retests, retrains, retests, using the same held-out items. Classic test-set-leak problem.
- A per-concept budget is necessary but arbitrary. How many rounds is a "fair try" before we conclude $S$ cannot master $C$ under the given packet?

**Unknowns:**
- Pass threshold. 80%? 95%? Human exam benchmarks are not obviously the right calibration for an LLM.
- What to do when $S$ persistently fails: regenerate the packet (with $T$ told "$S$ failed like this")? Spawn a sibling concept ([[../concept-learning/recursive-concept-evolution]] RCE-style)? Give up?

**Challenges:**
- Rebuilding TestSet each retest is expensive; reusing it risks memorisation.
- Adversarial test generation (items designed to trip up the *current* student's error modes) is attractive but requires $T$ to analyse student failures.

### Step (f): Terminal state

**Strengths:**
- The hoped-for outcome — "foundational understanding of the DAG" — is falsifiable: you just hold out a concept that was not in any TestSet and see if $S$ can handle it.
- Curriculum completeness provides a natural *stopping point* for training, unlike open-ended RL.

**Weaknesses:**
- No guarantee that mastering each node separately produces a model that can *compose* them. Catastrophic forgetting is the main threat; compositional generalisation is the second.
- Concepts mastered in isolation may not transfer to realistic problems that blend multiple concepts (the [[../teacher-student-rl/rlt-followups-2026]] ExGRPO / "conceptual inversion" critique).

**Unknowns:**
- Whether the terminal model, tested on *novel* application problems combining multiple concepts, succeeds. The captured corpus has no curriculum-RL method tested on this.
- Whether the process transfers. Does a curriculum built for calculus produce a model that can *also* learn physics with a new curriculum? Or does the first curriculum damage priors needed for transfer?

**Challenges:**
- Evaluating "foundational understanding" vs "pattern memorisation" at the DAG root. [[../concept-learning/recursive-concept-evolution]]'s MDL sibling test is the closest captured proxy.

## Overall assessment

### Strengths of the proposal as a whole

- **It's a concrete, end-to-end story.** Most wiki method pages compose primitives; this one has an end-to-end process from "goal topic" to "trained student". That's rarer.
- **The teacher-does-the-hard-part factoring is right.** Offloading curriculum construction, packet generation, and grading to $T$ is consistent with [[../teacher-student-rl/sakana-rlt]]'s result that a strong frozen teacher + student-side reward is a high-leverage setup.
- **Test-fail-train is an honest contract.** The student does not progress until it demonstrably passes. This is cleaner than loss-convergence.
- **Curriculum is a natural fit for single-sample / small-N RL.** Each packet is small (N ≈ 1–100); the 1-shot RLVR line ([[../single-sample-rl-finetuning/1-shot-rlvr]]) shows this regime can work.

### Weaknesses of the proposal as a whole

- **The inner loop is not yet specified.** Step (d) is where the real algorithm lives, and the user explicitly flagged it as open. Strengths and weaknesses of the surrounding scaffolding depend on it.
- **Multiple "teacher produces everything" steps chain errors.** If $T$'s DAG is wrong OR its packets are wrong OR its grading is wrong, the student learns a confabulation confidently. No captured source audits this end-to-end pipeline.
- **Not strictly single-sample.** The project's framing has been single-sample/concept-based learning ([[single-sample-concept-skeleton]], [[proposed-method]]). This proposal is *small-curriculum* with per-concept packets that may each contain tens of examples. Depending on packet size, the total training set is 100s–1000s of items — closer to data-efficient learning than to single-sample.

### Unknowns

- **Compositional generalisation at the root.** Does mastering the DAG bottom-up yield a model that handles novel mixes?
- **Forgetting rate.** Without EWC anchors or sparse masks, how many concepts can be trained before early ones degrade?
- **Minimum packet size.** Is 1 (Q, E, A) triple + a textbook chapter enough per concept, or does concept mastery need diverse (Q, E, A) triples?
- **Transfer across domains.** Does a calculus-trained student learn physics faster via the same method? This tests whether "concepts were installed" or "calculus-shaped circuits were installed".

### Challenges

- **Catastrophic forgetting** (flagged by the user). Every subsequent concept trained could erode earlier concepts. Candidate counters in the corpus: [[../catastrophic-forgetting/ewc-gemma2-cpt]] (Fisher-weighted EWC anchor), [[../rlvr-mechanics/rl-sparse-subnetwork]] (Balashov masks restrict which weights move). Both are applied *once* in their source settings; applying them repeatedly across a curriculum is untested.
- **Teacher-dependent correctness.** The whole pipeline's quality is capped by $T$. For calculus or other well-codified domains this is fine; for frontier topics or where $T$ is wrong, the student learns to be confidently wrong. There is no Peer-review or critic loop in the current sketch.
- **Test-set construction reliability.** Generating *novel-application* test items that are (i) actually novel, (ii) actually testing the concept, and (iii) solvable without external help given the prereqs, is non-trivial even for a strong $T$.
- **Test-set reuse under retest.** If the loop reuses the same TestSet across retrains, we are training-on-test. Rebuilding the TestSet per retry is expensive.
- **Compute footprint.** A full RL inner loop per concept × many concepts × possibly several retest rounds × a strong teacher doing packet generation is not cheap.
- **Explicit compositionality test.** The proposal ends when the last concept is mastered — but end-of-curriculum tests should probe *combinations* of concepts, not just $C^\star$ in isolation. No sketch of this yet.
- **Granularity drift.** Nothing in the sketch prevents $T$ from generating concepts that are too fine (waste) or too coarse (skip important substructure). This is a DAG-quality problem without a captured audit method.

## Relation to the other two synthesis pages

| Aspect | [[single-sample-concept-skeleton]] | [[proposed-method]] | This page (concept-curriculum) |
|---|---|---|---|
| Unit of training | One example | One example | One concept (with a packet of $\geq 1$ examples) |
| Primary primitive | RCE failure trigger + Balashov mask + L2T info-gain + CAI | RLT reward + RCE trigger + Balashov mask + EWC anchor + reference-in-context | Teacher-built DAG + per-concept packet + test-fail-train loop |
| Curriculum? | No — single example focus | No — implementation roadmap for single-sample | **Yes — DAG-based bottom-up** |
| Forgetting mitigation | Not addressed | EWC Fisher anchor (component F) | Untargeted in v1; EWC or sparse mask candidate |
| Teacher role | Minimal (student critique, primitives internal) | Frozen RLT-style grader | Dominant — builds DAG, packets, tests, and grades |
| "Single-sample" in name? | Yes | Yes (reference-grounded variant) | **No — small-curriculum / hierarchical** |

This method is the *most teacher-heavy* and the *least single-sample* of the three. It's closer in spirit to classical curriculum learning + RLT/OPSD than to the 1-shot RLVR line.

## Where this intersects the corpus

- **Teacher-builds-solution paradigm:** [[../teacher-student-rl/sakana-rlt]], [[../teacher-student-rl/rlt-followups-2026]] (OPSD, ExGRPO)
- **Curriculum / data selection:** [[../single-sample-rl-finetuning/data-efficiency-rft]] (DOTS, $p=0.5$ rule), [[../teacher-student-rl/soar-edge-of-learnability]] (bilevel curriculum)
- **Single-example RL as the inner-loop primitive:** [[../single-sample-rl-finetuning/1-shot-rlvr]]
- **Concept-level learning:** [[../concept-learning/concept-bottleneck-models]], [[../concept-learning/recursive-concept-evolution]]
- **Forgetting:** [[../catastrophic-forgetting/ewc-gemma2-cpt]], [[../rlvr-mechanics/rl-sparse-subnetwork]]
- **Optimiser choice:** [[../rl-optimizers/_overview]], [[../rl-optimizers/dr-grpo]], [[../rl-optimizers/dapo]]
- **Memorisation-vs-understanding probes:** [[../teacher-student-rl/rlt-followups-2026]] (ExGRPO), [[../concept-learning/recursive-concept-evolution]] (MDL sibling test)

## Open questions for the project

*(editorial — these are the decisions that would turn this sketch into an implementation plan)*

1. **Is this a competing method to [[proposed-method]], or do they compose?** A concept-curriculum where each concept's inner loop is [[proposed-method]]'s single-sample RLT+mask+EWC stack is the obvious composition — but no captured source demonstrates it.
2. **What is the MVP that would falsify the method fastest?** Proposal: one 3-node DAG (e.g. "addition → multiplication → simple linear equations"), one packet per node, one inner-loop algorithm, on a small base student. Success = pass root TestSet without external help; failure = any node retest loops indefinitely, or root test fails despite all nodes passing.
3. **What inner-loop algorithm to prototype first?** The wiki evidence points at RLT-flavour ($r^{SS}$ with textbook in context) + GRPO/Dr. GRPO as the least-risky starting point, but [[../teacher-student-rl/rlt-followups-2026]] OPSD is a cheaper alternative worth keeping in reserve.
4. **How to test compositional generalisation at $C^\star$?** Candidate: build a *second* TestSet for $C^\star$ that requires combining $\geq 3$ DAG nodes in novel ways, held out from everything $T$ has ever seen. Critical missing piece in the sketch.
5. **Does the curriculum approach belong in the project at all, or is it a separate method?** The project's stated goal in [[../../index]] is "single-sample, concept-based learning". The curriculum proposal is arguably *concept-based* but not *single-sample*. A decision is needed on whether this is a parallel exploration or a scope expansion.

## Source

Editorial proposal captured from a conversation with David on 2026-04-23. Not synthesised from any single captured source — the method composition is the project frame. Individual primitives trace to the corpus pages linked above.

## Related

- [[single-sample-concept-skeleton]] — first method proposal on this wiki (primitive composition; single-example focus)
- [[proposed-method]] — second method proposal (reference-grounded RLT-flavoured single-sample; implementation roadmap)
- [[../teacher-student-rl/sakana-rlt]] — the teacher-given-answer paradigm
- [[../teacher-student-rl/rlt-followups-2026]] — OPSD, ExGRPO, OPD-wave; adjacent methods in the same family
- [[../teacher-student-rl/soar-edge-of-learnability]] — teacher generates Q-A pairs (closest to the packet-generation step)
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — the inner-loop primitive in its purest form
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — DOTS $p=0.5$ rule, relevant for packet difficulty calibration
- [[../concept-learning/recursive-concept-evolution]] — MDL sibling test and spawn-on-failure dynamics; possible audit tool for the DAG-node level
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — Fisher-weighted anchor; candidate forgetting mitigation across the curriculum
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — Balashov sparse mask; alternative forgetting mitigation
- [[../rl-optimizers/_overview]] — optimiser menu for the inner loop
- [[../rl-optimizers/dr-grpo]] — most likely concrete optimiser candidate (length-bias fix matters at small $G$)
