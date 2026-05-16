# Deep Knowledge Tracing

Piech et al. (2015): RNN-based temporal model of student knowledge using exercise response histories. arXiv:1506.05908, NeurIPS 2015. Does not require expert concept annotation; learns latent skill structure from correctness data alone.

## Method

DKT models a student's latent knowledge state as a continuous hidden vector $h_t$ evolved via a recurrent neural network (RNN or LSTM). The model receives a sequence of student interactions $x_t = (q_t, a_t)$ — exercise tag and correctness — and outputs per-exercise mastery probabilities $y_t$ (Eq. 1–2).

**Input encoding:** For small exercise sets, $x_t$ is a one-hot encoding of the (exercise, correctness) pair; for large sets, a fixed random Gaussian vector assigned to each pair (compressed sensing, ~log(2M) dimensions for M exercises). **Hidden state update** (vanilla RNN): $h_t = \tanh(W_{hx} \cdot x_t + W_{hh} \cdot h_{t-1} + b_h)$. **Output:** $y_t = \sigma(W_{yh} \cdot h_t + b_y)$, a probability vector over all exercises. LSTM variants use gated cell updates (Eq. 5–12, Appendix A) for longer temporal dependency.

**Training objective:** Minimize binary cross-entropy per predicted response: $L = \Sigma_t \ell(y_t[\delta(q_{t+1})], a_{t+1})$ (Eq. 3), trained with SGD (batch size 100, hidden dim 200), dropout on readout, gradient clipping. No concept labels required; hidden state implicitly captures skill dependencies.

## Claims

- **25% AUC gain on Assistments benchmark:** DKT (LSTM) achieves AUC 0.86 vs. 0.69 best prior BKT result on public dataset (Sec. 6, Table 1).
- **Strong Khan Academy performance:** AUC 0.85 on 1.4M exercises from 47K students vs. AUC 0.68 for standard BKT and 0.63 marginal baseline (Sec. 6, Table 1, Figure 3b).
- **Synthetic data oracle-level accuracy:** On simulated data with 5 latent concepts, LSTM matches oracle (which has ground-truth latent skill + difficulty) while BKT prediction degrades with unlabeled concepts (Sec. 6, Figure 3a).
- **Automatic prereq discovery:** Exercise influence function (Eq. 4) recovers true concept dependencies; synthetic data shows perfect clustering of 5 latent concepts without human annotation (Sec. 6.2, Figure 4).
- **Intelligent curriculum generation via MDP planning:** Expectimax search 8 steps ahead outperforms blocking and mixing rules in predicting student mastery over 30-exercise sequences on Assistments subset (Sec. 6.1, Figure 3c).
- **No expert domain knowledge needed:** Model learns substructure autonomously; BKT relies on manual concept labeling or expensive Cognitive Task Analysis (Sec. 2.1, Sec. 3).
- **Continuous knowledge representation:** RNN hidden state encodes richer, multi-dimensional mastery than BKT's binary skill variables, capturing transfer effects (e.g., learning linear intercepts $\rightarrow$ graphing; Fig. 1).

## Relevance to the project

**Confidence calibration for Evaluate(S, c):** DKT's output $y_t[q]$ is a well-calibrated per-exercise mastery probability. For RCL's $\text{Evaluate}(S, c)$ — estimating $P(\text{mastery} \mid \text{concept } c, \text{response history } S)$ — DKT provides a model architecture: train an LSTM on (exercise, correctness) pairs, then query the hidden state after observing S to predict mastery on concept-tagged items. The continuous hidden state naturally aggregates evidence across related exercises, useful for high-confidence concept diagnostics.

**Implicit prereq discovery and D1 diagnostic decomposition:** DKT's hidden dynamics learn which prior exercises inform future performance (Eq. 4 influence analysis; Fig. 4 concept clustering). This resonates with RCL's D1 goal—decomposing a failing response into prerequisite mastery gaps. The influence graph is a data-driven substitute for manual concept hierarchies. If RCL can access student history on concept-related items, DKT-style analysis could automatically surface which concepts block mastery of target c.

**Project limitations and boundaries:** DKT assumes a fixed, finite concept vocabulary (exercise tags) and requires substantial response history per student for training. Single-sample RCL operates in the regime of minimal historical data ($N \approx 1$–$5$ examples per concept). DKT is not directly applicable at N=1, but (a) if RCL has modest aggregate corpus data, a pretrained DKT could score confidence on new (student, concept) pairs without retraining; (b) DKT's architecture (continuous latent state updated by interaction tuples) is a candidate scaffold for RCL's confidence module, scaled down to small N via few-shot or meta-learning techniques.

## Source

- arXiv: 1506.05908
- Raw markdown: `../../../raw/research/rcl-gap-fillers/01-dkt.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[auto-kc-generation]] — modern LLM-based KT successor; LLM-generated knowledge components beat human-written labels on the same KT task
- [[lecturebank]], [[concept-prereq-relations]] — sibling theme on concept-prereq learning; DKT operates on the *response* side, prereq-graph papers on the *concept-structure* side
- [[../synthesis/recursive-concept-learning]] — DKT as a candidate `Evaluate(S, c)` confidence-calibration backend; influence-function variant relevant to D1 prereq inference
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — DOTS $p\approx0.5$ rule shares the "what concept to train next given current mastery" question DKT answers via response-history modelling
