# CorVer: Verifiable Rewards Beyond Math and Code

CorVer (Corpus Verify) replaces neural-verifier process rewards with a corpus-grounded co-occurrence signal for factual QA: each generated sentence is scored by extracting its subject-object pair via a 0.5B triplet extractor (QuCo-extractor-0.5B, a Qwen2.5-0.5B-Instruct fine-tune) and querying a fixed Wikipedia Infini-gram index for that pair's co-occurrence count within a 1,000-token window. The resulting piecewise-constant reward $r_i^c \in \{\alpha_0, \alpha_1, \alpha_2, \alpha_3\} = \{-0.3, -0.1, 0.0, +0.1\}$ at count thresholds $(\tau_1, \tau_2) = (5, 20)$ is mapped to token-level returns via a token-to-sentence alignment $\sigma$ and combined with a response-level judge reward (string-match, $+2/-1$) and format reward under GRPO. Across all 30 (model, benchmark) cells spanning six instruction-tuned models (3B–14B: Llama-3.2-3B, Llama-3.1-8B, Qwen3-4B, Qwen3-8B, OLMo-2-13B, Qwen3-14B) and five factual QA benchmarks (TriviaQA, NQ-Open, PopQA, SimpleQA, TruthfulQA), CorVer improves over the unmodified baseline in every cell (average TriviaQA gain +4.1 pp) and beats four neural-verifier baselines (FoRAG, RLFH, FSPO, KnowRL) in 18 of 20 cells under feasible training configurations, at 4.8–8.4× lower training cost (3.2 h vs 14.5–29.5 h average across four models).

## Key details

**Reward architecture.** The per-token return is $R_t = R^r(x,y) + \mathbf{1}[\sigma(t)>0] \cdot \lambda_c \cdot r^c_{\sigma(t)}$, where $R^r = \lambda_j R^j + \lambda_f R^f$ is the response-level component and $\lambda_f = \lambda_j = \lambda_c = 1.0$. The co-occurrence contribution is capped at $\bar{m}_\text{sent} \cdot \alpha_3 \approx 0.3$, one order of magnitude below the judge swing of $r_\text{good} - r_\text{bad} = 3.0$, so factuality shapes credit without overriding correctness. Tokens at tag positions and inter-sentence whitespace ($\sigma(t) = 0$) receive only $R^r$.

**Empirical calibration.** On 700 manually annotated sentences, $P(\text{correct}|c_i)$ increases monotonically from 23% at $c_i = 0$ to 81% at $c_i \geq 20$. The two largest precision jumps (+17 pp at $c_i = 5$, +8 pp at $c_i = 20$) determine $\tau_1$ and $\tau_2$.

**Ablation (Llama-3.1-8B-Instruct).** Removing the co-occurrence signal (A1, vanilla GRPO) drops TriviaQA from 76.52 to 71.3. Removing per-token alignment while keeping the same total QuCo reward mass as a response-level scalar (A3) recovers only 72.9, near A1 — the gain comes from per-token distribution, not reward magnitude. Removing the judge (A2) causes NQ-Open to drop from 48.34 to 42.6 and PopQA from 35.30 to 31.7.

**Gain attribution.** PopQA popularity-quartile analysis (Llama-3.1-8B, OLMo-2-13B) shows improvement at all quartiles but with a signal-density pattern: gains peak on popular entities (Q4: +7.5–+9.0 pp) rather than rare ones (Q1: +3.7–+5.5 pp). This is the opposite of the "rare-entity rescue" hypothesis — the reward is most informative where corpus co-occurrence statistics are densest.

**Cost.** CorVer's per-sentence cost is one 0.5B forward pass plus one mmap Infini-gram lookup (millisecond-scale). At the paper's configuration ($N_\text{steps}=100$, $B=24$, $G=16$, $\bar{m}_\text{sent} \approx 3$) this yields ~$1.2 \times 10^5$ reward calls per run. FSPO (NLI verifier) is 8.4× slower; KnowRL (atomic-fact pipeline + GPT-4o-mini) is 7.8×; RLFH (LLM judge) is 4.8×.

**Training configuration.** LoRA $r/\alpha = 128/256$, $G = 16$ rollouts, 100 GRPO steps, prompt-batch 24, max completion 1024 tokens. Direct GRPO from the raw instruction-tuned model without SFT cold-start (an SFT distillation attempt from a 397B MoE teacher underperformed). Small models (3B/4B) require anchor questions ($n_\text{correct} = G$) mixed into the learning-zone pool to prevent accuracy deterioration; models $\geq 8B$ do not.

**Triplet aggregation.** FIRST (keep first valid subject-object pair, discard relation) outperforms MIN (take minimum across all triplets; causes length collapse) and RELCHECK (re-query with relation token; brittle to surface-form variation). FIRST is also the fastest at 1.0× vs 1.2–1.7×.

**Limitations.** Co-occurrence captures subject-object co-presence, not predicate semantics — cannot detect errors where correct entities appear in a factually wrong relation. Signal strength tracks corpus coverage (Wikipedia, 6.4M articles, 5.5B tokens), so the reward is weakest precisely for rare entities where the policy most needs guidance. Validated only under GRPO; PPO, REINFORCE, and DPO integration are left to future work.

## Source

- arXiv: https://arxiv.org/abs/2605.29648
- Capture: `raw/research/weekly-2026-05-30/05-corver-verifiable-rewards-factual.md`
- Code (forthcoming): https://github.com/shichengf/CorVer

## Related

- [[_overview]] — process-reward-models theme overview
- [[uprm]] — another lightweight PRM (unsupervised, frozen-LLM markers); contrasts with CorVer's corpus-lookup approach; both avoid neural verifier calls in the reward loop
- [[../rlvr-mechanics/_overview]] — GRPO and verifiable-reward mechanics underlying CorVer
- [[../weekly-briefs/2026-05-30]] — brought in by the 2026-05-30 weekly sweep
