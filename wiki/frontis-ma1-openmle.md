# Frontis-MA1 / OpenMLE: Recursive Self-Improvement in ML Engineering

Horizon Research/Frontis.AI + Tsinghua (arXiv:2607.28568, Jul 2026). Releases OpenMLE, a full open stack — gym + execution-grounded SFT/RL + experience-guided evolutionary search — that trains a "meta-evolution agent," Frontis-MA1-35B, whose learned Draft/Improve/Debug/Crossover operators double as both the product of post-training and the variation engine of the evolutionary search harness that composes them. Framed as a concrete step from evolution toward recursive self-improvement (RSI) in machine learning engineering.

## Method

Three components: **OpenMLE-Gym** (5,758 quality-gated executable MLE tasks from expert-curated anchors, an extended MLE-Smith Kaggle-dataset pipeline, and a Kaggle-competition crawl, filtered to ~20% of an ~11,000-competition catalog); **OpenMLE-ERL** (trains four reusable atomic operators — Draft, Improve, Debug, Crossover — via a 26,259-example SFT corpus followed by an RL stage using adaptive per-task reward bounds, an "entropic advantage" that replaces GRPO's group-normalized advantage to concentrate signal on the best rollout-group candidate, asynchronous execution-latency-dominated rollout, and fitness-proportional parent-state selection for RL practice); **OpenMLE-Evo** (an AIRA-Evo-style population search loop redesigned around structured "experience cards" and a three-factor parent-selection utility — score, improvement-over-parent, method-family novelty — replacing AIRA-Evo's score-only softmax). Derives from MLE-Dojo/MLE-Bench/MLE-Smith for environments, AIDE/AIRA/AIRA-Evo for search scaffolds, and RLVR SFT-vs-RL division-of-labor literature for the training-stage split.

## Results

Official 22-task MLE-Bench Lite, fixed 12 GPU-hour/task budget on a single RTX 4090 12GB. Post-training gain alone: Frontis-MA1-35B vs Qwen3.6-35B-A3B base under the identical OpenMLE-Evo harness, Medal Average 39.39%→60.61% (+21.22 pp); a 30B companion model replicates the gain (+18.18 pp) across model/scale. System level: Frontis-MA1-35B + OpenMLE-Evo-Max reaches 71.21% Medal Average, exceeding GPT-5.5+Codex (68.18%) and comparable to GPT-5.6 Sol+Codex / Kimi K3+Claude Code (72.73%). Harness-only gains holding the model fixed are consistent across GLM-5.2, MiniMax, and Kimi backbones. Search efficiency vs original AIRA-Evo on the same checkpoint: total tokens −41.7%, new-best validation updates per 1M tokens +84.3%. Transfer to NatureBench Lite (10-task scientific-reproduction subset): Frontis-MA1+adapter reaches 30%/70% (All-S/All-M), matching GPT-5.4/GLM-5.1/MiniMax-M3 reference agents but trailing the best reference agents (Claude Opus 4.7, GLM-5.2 at 70%/100%).

## Applicability

Requires large executable-task infrastructure (sandbox scheduler, isolated workers, per-task evaluators), a 30–35B-class base MoE/dense LLM, SFT+RL infrastructure with async rollout support, and meaningful GPU-hour sandbox budgets even at the paper's deliberately modest 12h/RTX-4090-per-task setting. Best fit: teams building autonomous MLE/AutoML agents, or any team wanting reusable code-transformation operators (draft/refine/repair/merge) shared between post-training targets and an inference-time search harness — the operator-shared-interface idea generalizes beyond MLE to other evolutionary code-search domains.

## Novelty

Recombination plus a genuine methodological refinement: the "meta-evolution" framing — training the operators that the evolutionary search itself composes, closing evolution → learning → search into one loop — is the core novel claim. Individual pieces (task format, operator vocabulary, evolutionary search loop) build directly on cited prior work; the authors position OpenMLE as the first system to jointly span task construction, execution-grounded post-training, and evolutionary deployment of the trained model with full reproducibility artifacts.

## Reproducibility

Stated intent to release datasets, training/evaluation code, sandbox infrastructure, harness code, and final post-trained checkpoints (project page, GitHub, HF collection linked; not independently verified as populated at ingest time). Full task-package data released for 1,415 of 5,758 tasks (licensing-limited); scripts only for the rest.

## Conflicts

Frontis-MA1's NatureBench Lite results are partial, qualified counter-evidence to [[ai-agents-open-ended-research]]'s claim that narrow/verifiable agentic capability does not transfer to open-ended research judgment: execution-grounded MLE post-training does transfer some gains to scientific-reproduction tasks (+10–30pp depending on isolated factor), but the paper explicitly disclaims general RSI and the best reference agents still lead by a wide margin (70%/100% vs 30%/70%). A soft, partial tension rather than a direct contradiction — no dedicated conflict file opened this week.

## Related

- [[huxley-godel-machine]] — closest existing page on trainable self-improving coding agents; HGM scores tree-search parents by clade success rate over a frozen agent, Frontis-MA1 trains the underlying operators themselves via SFT+RL.
- [[evolution-fine-tuning]] — same "distill evolutionary experience into weights" idea as OpenMLE-ERL's SFT stage, at much smaller scale (2B–9B vs 30–35B) and without the RL/search-loop closure.
- [[skillopt]] / [[memoharness]] — both optimize agent harness/skill artifacts rather than weights; OpenMLE instead trains the model that composes with a fixed-ish harness.
- [[gepa-reflective-prompt-evolution]] — another evolutionary (Pareto) optimization approach for compound AI systems, no weight updates.
- [[eggroll]] — different evolutionary-training approach (ES over LoRA perturbations) vs OpenMLE's SFT+RL operator training.
- [[ai-agents-open-ended-research]] — see Conflicts above.

## Source

- `raw/research/weekly-2026-08-08/03-frontis-ma1-recursive-self-improvement.md` (arXiv:2607.28568)
