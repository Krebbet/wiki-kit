# SCRL: Subproblem Curriculum Reinforcement Learning

SCRL (Subproblem Curriculum Reinforcement Learning) is a curriculum RL framework from Tsinghua/LeapLab that addresses the sparse-reward problem on hard problems by decomposing each problem into a sequence of $K$ verifiable subproblems derived from a reference solution. The model answers all $K$ subproblems in a single on-policy rollout; a novel **subproblem-level normalization** operator normalizes rewards independently at each subproblem position across the rollout group, assigns per-position advantages to the corresponding tagged answer spans, and enforces progress-aware correction (a reward vector like $[1,1,0,1]$ is truncated to $[1,1,0,0]$ — no credit past the first failure). Mixed-group training jointly optimizes curriculum rollouts and original-problem GRPO rollouts to prevent prompt-distribution mismatch. The theoretical justification is an information-geometry metric recovery result: when $p(x;\theta) < \delta$ (hard problem near gradient dead zone), the lifted subproblem manifold recovers a non-degenerate Fisher–Rao gradient signal, with the recovery ratio $\lambda_{\min}(F_{T(x)})/\lambda_{\min}(F_x) = \Omega(1/\delta)$ growing as problems get harder. Empirically, SCRL yields average gains of +4.1 and +1.9 points over GRPO on Qwen3-4B-Base and Qwen3-14B-Base across seven math benchmarks, with +3.7 pass@1 and +4.6 pass@64 on hard benchmarks (AIME24/25, IMO-Bench).

## Source

- **arXiv:** https://arxiv.org/abs/2605.22074
- **Capture:** `raw/research/weekly-2026-05-30/02-scrl-curriculum-credit-assignment.md`
- Jiang, Tang, Lin, Yue, Wang, Huang. LeapLab, Tsinghua University. May 2026.

## Method Details

### Subproblem construction

Given a hard problem $x$ with a reference chain-of-thought solution, an external LLM (DeepSeek-V3.2 in experiments) rewrites intermediate progress nodes into $K$ verifiable subproblems $s^{(1)} \prec s^{(2)} \prec \cdots \prec s^{(K)} = x$. Guidelines: increasing difficulty, each subproblem self-contained but feeding into the next, each answer objectively checkable. The final subproblem is always pinned to $x$ itself. This is an offline preprocessing step — it does not modify the policy's distribution.

### Curriculum prompt and response format

The curriculum prompt $t_K(x)$ presents all $K$ subproblems simultaneously. The model responds using explicit tags `<pj>...</pj>` for each subproblem answer. These tags mark token spans for (a) per-subproblem verification and (b) advantage assignment back to the generating tokens.

### Progress-aware subproblem rewards

Raw reward vector $\mathbf{r}_i = (r_i^{(1)}, \ldots, r_i^{(K)}) \in \{0,1\}^K$. Curriculum progress $k_i = \max\{j : r_i^{(1)} = \cdots = r_i^{(j)} = 1\}$. Progress-aware correction zeroes all rewards beyond the first failure: $\tilde{r}_i^{(j)} = r_i^{(j)}$ if $j \le k_i$, else $0$. This prevents reward-hacking shortcuts where the model solves later subproblems despite failing earlier ones.

### Subproblem-level normalization

For $G$ curriculum rollouts, advantages are normalized independently at each subproblem position $j$:

$$A_i^{(j)} = \frac{R_i^{(j)} - \text{mean}(\{R_i^{(j)}\}_{i=1}^G)}{\text{std}(\{R_i^{(j)}\}_{i=1}^G)}$$

Token-level credit: tokens inside `<pj>...</pj>` receive $A_i^{(j)}$; tokens outside answer spans receive zero. This is strictly finer-grained than GRPO's single sample-level advantage.

### Mixed-group training

$G/2$ rollouts from $t_K(x)$ (curriculum, subproblem-level normalization) + $G/2$ rollouts from $x$ (original prompt, standard GRPO). Both batches are combined in a single policy-gradient update. This bridges the train/eval distribution gap.

## Key Results

| Model | Method | Avg (7 bench) | AIME'24 | AIME'25 | IMO-B |
|---|---|---|---|---|---|
| Qwen3-4B-Base | GRPO | 30.9 | 14.5 | 7.2 | 7.8 |
| Qwen3-4B-Base | QuestA | 32.0 | 14.1 | 11.7 | 8.3 |
| Qwen3-4B-Base | **SCRL** | **35.0** | **16.5** | **15.3** | **8.7** |
| Qwen3-14B-Base | GRPO | 36.4 | 21.6 | 11.9 | 9.9 |
| Qwen3-14B-Base | **SCRL** | **38.3** | **24.4** | 13.1 | **11.9** |
| Llama3.2-3B | GRPO | 15.7 | 10.3 | 0.5 | 5.4 |
| Llama3.2-3B | **SCRL** | **16.4** | 10.3 | **0.8** | **6.8** |

**Hard benchmarks (Qwen3-4B, pass@k):** SCRL +3.7 pass@1 and +4.6 pass@64 over GRPO on AIME24+AIME25+IMO-Bench.

**Subproblem generator quality (Qwen3-4B, subset):** DeepSeek-V3.2 → 44.2 avg; Qwen3-4B-Instruct → 43.0 avg; GRPO → 40.3 avg. Weaker generator still gains +2.7 points, so high-quality subproblem generation is helpful but not required.

**Number of subproblems $K$ (Qwen3-4B):** $K=4$ (avg 44.2) $>$ $K=3$ (42.8) $>$ $K=2$ (41.8) $>$ GRPO (40.3). More subproblems = finer progression + more rollouts with $k_i > 0$.

**Data-scaling controls:** SCRL on `hard_1024` (44.2) outperforms GRPO on `hard_4096` (41.2) and GRPO on `subproblem_4096` (41.7). The gain is algorithmic, not from seeing more questions.

**Response length:** SCRL curriculum rollouts average only $\approx1.5\times$ the length of GRPO rollouts despite $K=4$ subproblems — subproblem structure supports more efficient exploration per token.

## Ablations

**Credit assignment variants (Qwen3-4B, subset):**

| Method | Avg |
|---|---|
| Both-GRPO (subproblems as hints only, sample-level credit) | 43.9 |
| Subproblem-level normalization w/o progress-aware correction | 41.9 |
| Subproblem-level normalization w/ correction (SCRL) | **44.2** |

Both components matter: subproblem-specific signals and progress-aware correction. Removing correction drops performance substantially (dense rewards without the consecutive-prefix gate create a reward-hacking incentive).

## Theoretical Framing

**Gradient dead zone (Theorem 4.2):** Under GRPO, if $p(x;\theta) < \delta$, then $\lambda_{\min}(F_x(\theta)) \le G\delta \cdot C_{\hat A}^2 \cdot B_s^2 = O(\delta)$. When correct rollouts are rare, reward groups collapse to all-zero advantage and the effective gradient information vanishes.

**Metric recovery (Theorem 4.3):** If subproblems satisfy $p_j(x;\theta) \in [p^\star, 1-p^\star]$ for $j < K$ (intermediate subproblems are neither trivially easy nor impossibly hard), then $\lambda_{\min}(F_{T(x)}(\theta)) \ge \frac{1}{K} c(p^\star, G, \sigma_{\min}) > 0$ even when the original problem is in the dead zone. Recovery ratio $= \Omega(1/\delta)$: larger relative gains predicted as original problem difficulty increases.

## Positioning vs Prior Curriculum RL Methods

**Hint-driven methods** (StepHint, Scaf-GRPO, TAPO, R3L, HiPO): supply expert rationales as a static prefix, lowering the exploration threshold. The model optimizes continuation from the hint — it never self-generates the scaffolding. SCRL keeps the model fully on-policy; all subproblem answers are generated by the student.

**Problem-reformulation methods** (QuestA, MQR, NuRL): rewrite the original problem into simpler versions. Orthogonal to SCRL's decomposition-within-a-rollout structure; the model must still solve the full problem from scratch.

**SCRL's key claim:** the on-policy constraint (model generates all intermediate steps itself) is load-bearing for generalization. Distribution shift between expert prefix and student policy hurts OOD generalization (Shenfeld et al., 2025; Chu et al., 2025).

## Limitations and Open Questions

- Subproblem generation requires a reference solution per hard problem. Applicable where such solutions exist (competition math with answer keys); less obvious for open-ended or novel problem types.
- $K=4$ is a practical trade-off; longer curricula increase rollout complexity and create blocking risks if intermediate subproblems are ambiguous.
- Experiments are math-only. Transfer to code or multi-step agentic tasks is not demonstrated.
- The weaker generator (Qwen3-4B-Instruct) still gets +2.7 over GRPO — but there is a quality ceiling: poorly constructed intermediate subproblems block credit for later progress under progress-aware correction.
- Mixed-group training splits the rollout budget $G/2$/$G/2$; whether the ratio is optimal is not ablated.

## Related

- [[_overview]] — curriculum and decomposition theme
- [[bengio-curriculum]] — theoretical predecessor; continuation method framing of curriculum learning
- [[../synthesis/concept-curriculum-method]] — wiki's primary proposed method; SCRL's subproblem decomposition from reference solutions is a closely related primitive (teacher decomposes, student solves on-policy)
- [[../rl-optimizers/dapo]] — DAPO baseline in SCRL experiments; Dynamic Sampling addresses all-zero reward groups via a different mechanism (filter prompts with $p=0$ or $p=1$)
- [[../rl-optimizers/dr-grpo]] — debiased GRPO; related family of fixes to GRPO's credit-assignment pathologies
- [[../rl-optimizers/ep-grpo]] — another GRPO variant; same sparse-reward motivation
- [[../process-reward-models/_overview]] — process-level reward supervision is the alternative to subproblem decomposition for dense credit; SCRL avoids needing a trained PRM
- [[../process-reward-models/lets-verify-step-by-step]] — Lightman et al. ORM vs PRM; SCRL's subproblem-level normalization provides verifiable process supervision without annotation
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO origin paper; SCRL builds directly on GRPO
- [[../self-play/yue-rlvr-boundary]] — Yue et al. on RLVR improving sampling efficiency vs capability; SCRL specifically targets capability expansion beyond the base model's boundary
- [[../weekly-briefs/2026-05-30]] — brought in by the 2026-05-30 weekly sweep
