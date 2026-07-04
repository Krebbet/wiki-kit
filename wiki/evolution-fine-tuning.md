# Evolution Fine-Tuning (EFT / Finch)

Evolution Fine-Tuning (EFT) is a mid-training paradigm from Minnesota NLP / CMU / KAIST (arXiv:2606.29082) that internalizes LLM-driven evolutionary discovery capability into model weights rather than leaving it in the search scaffold. A teacher model (Qwen3.5-397B-A17B) runs OpenEvolve over 371 optimization tasks, generating 156K parent→child solution trajectories (Finch Collection); smaller open-source models (2B–9B, the Finch family) are then SFT-trained on these trajectories to act as stronger mutation operators. On 22 held-out tasks, Finch-9B achieves +10.24% average improvement over its base model, with Finch-4B matching non-EFT models 2× its size. Combined with offline RL (KTO) or test-time RL (nanodiscover), Finch-8B reaches state-of-the-art on two circle-packing tasks and surpasses best human scores on AC1/AC2. The key practical payoff: cross-domain strategy transfer — Finch applies techniques learned from recommender systems and numerical optimization to solve competitive programming problems, a behavior absent in base models.

## Method

**Data construction.** Finch Collection covers 371 tasks across 10 domains: competitive programming (172 tasks, 43K trajectories), symbolic regression physics oscillation (44 tasks, 51K), numerical algorithm optimization (47 tasks), heuristic optimization (35 tasks), mathematical discovery (28 tasks), SR bio/chem, GPU kernel optimization (4 tasks), single-cell RNA denoising (3 tasks), and constructive search (2 tasks). Each task provides a spec, initial candidate, and deterministic evaluator. OpenEvolve runs the teacher model with two mutation strategies (diff-based edit for exploitation, full rewrite for exploration), producing 172,997 raw trajectories filtered to 156,731 by removing systematic errors (missing parent scores, timeouts), unrecoverable/breakage cases, and sequences exceeding 32K tokens.

**Training.** Only the 61,802 improving (Imp) trajectories are used for SFT to avoid imitating regressions, yielding 30,445 training examples (one per task to counter symbolic-regression class imbalance). Full SFT via LLaMA-Factory, 1 epoch, batch 128, lr 1e-5, 8×H200 GPUs. Follow-on KTO preference training on Imp+Reg pairs further improves discovery quality. EFT is orthogonal to the test-time scaffold: the resulting Finch model works inside frozen-weight search scaffolds or as a starting point for test-time RL.

**Positioning.** Prior test-time search methods (AlphaEvolve, OpenEvolve, GEPA) leave the model frozen — all discovery lives in the scaffold. Test-time learning methods (ThetaEvolve, TTT-Discover) update weights per-task but discard the learned strategies afterward. EFT is the first approach to consolidate cross-task discovery capability persistently into weights via SFT before deployment.

## Results

| Model | Avg. gain | Key highlights |
|---|---|---|
| Finch-2B vs Qwen3.5-2B | +1.56% | CP +22.51%, Transaction +4.13% |
| Finch-4B vs Qwen3.5-4B | +3.40% | ahc058 from 0→331M, Transaction +74.30% |
| Finch-8B vs Qwen3-8B | +3.17% | +KTO: AC1 1.5089 < best human 1.5097, AC2 0.9146 > best human 0.9015 |
| Finch-9B vs Qwen3.5-9B | +10.24% | CP n=26 +65.09%, ahc058 +290.59% |

Competitive programming (6 tasks): Finch-4B avg 31.97 vs base 14.52; Finch-9B avg 46.01 vs base 32.46.

Scaling law: training tasks 15→355 improves held-out average by 14.1% (clear positive trend on AC2, CP n=26, PRISM).

Test-time RL (nanodiscover): Finch-8B matches TTT-Discover + GPT-OSS-120B on CP n=26 (2.635983) and CP n=32 (2.939573); still trails GPT-OSS-120B on Erdos, indicating 8B scale is a ceiling for frontier-pushing on that task.

## Source
- arXiv: 2606.29082
- Captured: `raw/research/weekly-2026-07-04/02-evolution-fine-tuning.md`
- Code/data: Apache 2.0 (code + weights), CC-BY 4.0 (Finch Collection)

## Related
- [[eggroll]] — evolutionary strategies for LLM training (ES weight updates vs EFT's trajectory SFT — different mechanisms)
- [[gepa-reflective-prompt-evolution]] — genetic-Pareto prompt evolution (search-based, no weight updates; cited as baseline scaffold)
- [[huxley-godel-machine]] — self-improving agents via tree search
- [[seal-self-adapting]] — internalizing adaptation capability into weights via self-generated experience
- [[tempo-test-time-rl]] — test-time RL approach compared directly in paper
- [[conflicts/grpo-vs-evolution-strategies]] — EFT bridges evolutionary search and SFT/RL training paradigms
