# E2H Reasoner: Curriculum RL from Easy to Hard Tasks

E2H Reasoner (Parashar, Gui, Li et al., Texas A&M / 2025, arXiv:2506.06632) applies curriculum learning to RL post-training for LLM reasoning by scheduling tasks across four difficulty levels (trivial → easy → medium → hard) with parameterized decay schedules that fade out easy tasks after initial skill-building. The central empirical claim is that vanilla RL on hard tasks alone fails for small models (1.5B–3B), producing 0% on structurally hard domains like Blocksworld, whereas E2H-G (Gaussian scheduling) recovers substantial hard-task and OOD performance — e.g., Countdown OOD improves from 9.2% (GRPO) to 19.2% (E2H-G) on Qwen 1.5B, and from 2.7% to 24.3% on LLaMA 3.2 3B. The theoretical contribution is a convergence bound within an approximate policy iteration framework plus finite-sample complexity results showing that appropriately staged curriculum learning requires fewer total samples than direct hard-task learning, with the sample-efficiency advantage scaling with the relative difficulty factor $m$ of direct learning.

## Method

### Difficulty partitioning

Training data is partitioned into $K=4$ levels: trivial, easy, medium, hard. When human-annotated difficulty exists (Blocksworld: plan length; Countdown: operand count; MATH: problem levels), it is used directly. For unlabeled datasets (GSM8K, AQuA), difficulty is estimated from model error rates under chain-of-thought prompting and grouped into quartiles.

### Training schedulers

Each scheduler defines a mixing weight $\mathbf{S}(t,k)$ over difficulty level $k \in \{0,\ldots,K-1\}$ at training step $t \in [0,T]$.

**Cosine (E2H-C):** starts hard, fades out easy levels via cosine annealing toward easy:

$$\mathbf{S}_{\text{cosine}}(t,k)=\alpha_t \cdot (K-k-1)+(1-\alpha_t) \cdot k, \quad \alpha_t = \tfrac{1}{2}\!\left(1+\cos\!\frac{\pi t}{T}\right)$$

This puts maximum weight on the hardest level at $t=0$ and on the easiest at $t=T$ — i.e., the curriculum runs *hard-to-easy* during training, spending later steps consolidating on easier examples.

**Gaussian (E2H-G):** a Gaussian window sweeps from easy to hard, concentrating on intermediate levels progressively:

$$\mathbf{S}_{\text{Gaussian}}(t,k)=\exp\!\left(-\frac{(x_t - \mu_k)^2}{2\sigma^2}\right), \quad x_t=\left(\frac{t}{T}\right)^\beta(K-1)$$

$\sigma$ controls width of the attention window; $\beta > 0$ controls velocity (larger $\beta$ = faster progression to harder levels). This scheduler is empirically best for sparse-reward tasks.

The RL inner loop uses GRPO throughout; schedulers modify only the data-sampling distribution, not the optimizer.

### Theoretical framing

**Theorem 3.1 (CRL Performance Bound).** The policy error after $K$ curriculum stages satisfies:

$$\mathcal{E}_K \leq \sum_{k=1}^K\!\left(\gamma^T\eta_k + \frac{2\gamma(1-\gamma^T)}{(1-\gamma)^2}\delta_k + \frac{2\gamma}{\beta(1-\gamma)^2}\right) + \sum_{k=1}^{K-1}\|Q^*_K - Q^*_k\|_{d_K}$$

Four terms: convergence bias per stage ($\gamma^T \eta_k$), accumulated evaluation error ($\delta_k$ term), policy-update error, and curriculum approximation error (distance between optimal $Q$-functions of intermediate vs. final task under the final distribution $d_K$). The last term is the price paid for imperfect curriculum alignment.

**Theorem 3.2 (Sample Complexity).** CRL achieves total sample complexity:

$$O\!\left(\sum_{k=1}^K\frac{\log^3(1/\epsilon_k)}{\epsilon_k^2} \cdot \tilde{O}\!\left(\frac{L_k^2 n}{(1-\gamma)^7(1-\gamma_c)^3\lambda_{\min}^3}\right)\right)$$

Under geometric error allocation $\epsilon_k \propto r^k$, CRL beats direct learning when:

$$\frac{(e \cdot l)^{2(1-K)}-1}{1-(e\cdot l)^2} < m-1$$

where $m > 1$ is the relative difficulty factor of direct learning. Condition is easier to satisfy as $m$ (hard-task difficulty) grows — curriculum gains are largest exactly where RL alone fails most.

## Results

### Scheduling comparison (Qwen 1.5B, Table 2)

| Task | Metric | CoT | GRPO (Balanced) | CL | E2H-G | E2H-C |
|---|---|---|---|---|---|---|
| Blocksworld | Hard acc. | 0% | 21.1% | 5.8% | **32.9%** | 0% |
| Blocksworld | OOD | 0% | 2.6% | 0.7% | **7.3%** | 0% |
| Countdown | Hard acc. | 0.1% | 18.1% | 31.5% | **41.0%** | 15.8% |
| Countdown | OOD | 0.1% | 9.2% | 12.6% | **19.2%** | 6.4% |
| MATH | Hard acc. | 17.6% | 46.3% | 46.7% | 47.9% | **47.6%** |
| MATH | OOD | 8.2% | 25.7% | 25.6% | 26.5% | **28.6%** |

E2H-G dominates on sparse-reward tasks (Blocksworld, Countdown); E2H-C slightly better for dense-reward MATH OOD. Traditional curriculum learning (CL = monotone easy→hard with no fading) is inferior to E2H-G in all sparse-reward cases and matches on MATH.

### Cross-model generalization (Table 3)

| Model | Task | GRPO OOD | E2H-G OOD |
|---|---|---|---|
| Qwen 1.5B | Blocksworld | 2.6% | 7.3% |
| Qwen 1.5B | Countdown | 9.2% | 19.2% |
| Qwen 1.5B | MATH | 25.7% | 26.5% |
| LLaMA 3.2 3B | Blocksworld | 13.3% | 17.6% |
| LLaMA 3.2 3B | Countdown | 2.7% | **24.3%** |
| LLaMA 3.2 3B | MATH | 10.2% | 14.5% |

### Automatic difficulty labeling (Table 4, Qwen 1.5B)

| Dataset | CoT | GRPO | E2H-G |
|---|---|---|---|
| GSM8K | 67.7% | 77.1% | **78.7%** |
| AQuA | 40.9% | 63.3% | **66.1%** |

Gains transfer even when difficulty is estimated from model error rates rather than human labels.

### Hard benchmark generalization (Table 7, Qwen 1.5B, Pass@32)

| Benchmark | GRPO | E2H |
|---|---|---|
| AIME24 | 10.0% | **16.7%** (E2H-G) |
| OlympiadBench | 33.3% | **40.0%** (E2H-C) |

### Key ablation finding

Hard-only training produces **0% on Blocksworld trivial tasks** — the model completely fails to learn when initialized directly on hard problems. Full 4-level curriculum (trivial+easy+medium+hard) reaches 98% trivial, 100% easy, 83.3% medium, 21.1% hard. This is the core motivation: hard-task RL requires prerequisite skill scaffolding.

## Positioning vs. related work

**vs. SCRL ([[scrl-curriculum-credit-assignment]]):** SCRL decomposes individual *problems* into ordered subproblems solved within a single rollout, with per-subproblem advantage normalization. E2H operates at the *dataset* level — it schedules which difficulty bucket to sample from, not how to credit within a rollout. Orthogonal mechanisms; could be composed.

**vs. traditional curriculum learning ([[bengio-curriculum]]):** Bengio's continuation framing starts easy and monotonically increases difficulty. E2H adds explicit *fading* of easy tasks — the key empirical finding is that never removing easy examples causes overfitting (CL underperforms E2H-G on sparse-reward tasks because it doesn't fade).

**vs. DAPO ([[../rl-optimizers/dapo]]):** DAPO's Dynamic Sampling filters out prompts with pass-rate 0 or 1 (degenerate gradient signal). E2H operates on difficulty-conditional *curriculum scheduling*, not pass-rate filtering. The paper reports complementary gains when combined.

## Limitations

- Difficulty partitioning requires either human labels or a separate CoT error-rate estimation pass; the latter adds preprocessing cost proportional to dataset size.
- Experiments are on small models (1.5B, 3B); behavior at 7B+ is not reported.
- The Gaussian scheduler's hyperparameters ($\sigma$, $\beta$) require tuning; sensitivity analysis is limited.
- Math/planning/counting domains only; no code or agentic tasks.

## Source

- `raw/research/weekly-2026-06-05/04-e2h-curriculum-rl.md`
- arXiv:2506.06632v3 (last revised 16 Mar 2026)
- Parashar, Gui, Li, Ling, Vemuri, Olson, Li, Zhang, Caverlee, Kalathil, Ji. Texas A&M University.

## Related

- [[_overview]] — curriculum and decomposition theme overview
- [[scrl-curriculum-credit-assignment]] — SCRL: subproblem-level decomposition within a rollout; orthogonal to E2H's dataset-level scheduling
- [[bengio-curriculum]] — continuation method framing; E2H extends Bengio with explicit easy-task fading
- [[acl-deep-rl-survey]] — LP / ALP-GMM teacher-student bandits; E2H's Gaussian scheduler is a hand-designed analogue of LP-based automatic curriculum
- [[curriculum-survey]] — taxonomy; E2H fits the "predefined" + "self-paced" hybrid quadrant
- [[../rl-optimizers/dapo]] — Dynamic Sampling addresses the complementary pass-rate degenerate-gradient problem; paper reports combined gains
- [[../rl-optimizers/_overview]] — GRPO is the RL inner loop; E2H is optimizer-agnostic but experiments use GRPO
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO baseline throughout E2H experiments
- [[../weekly-briefs/2026-06-05]] — brought in by the 2026-06-05 weekly sweep
