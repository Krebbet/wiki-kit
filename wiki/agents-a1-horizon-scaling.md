# Agents-A1: Horizon Scaling for 35B MoE Agent

Agents-A1 (Shanghai AI Laboratory, arXiv:2606.30616) is a 35B Mixture-of-Experts agentic model that reaches or exceeds 1T-parameter frontier model performance (Kimi-K2.6, DeepSeek-V4-Pro) on long-horizon agent benchmarks by scaling training trajectory length and domain heterogeneity rather than model parameters. Built on Qwen3.5-35B-A3B, it achieves state-of-the-art results among both 35B and 1T-class models on SEAL-0 (56.4), IFBench (80.6), HiPhO (46.4), FrontierScience-Olympiad (79.0), and FrontierScience-Research (40.0), while remaining competitive on search and MLE tasks. Code and weights are publicly released.

## Method

**Knowledge-Action Graph (KAG).** The data backbone is a typed 4-tuple G_d = (corpus, action space, observation space, verifier set) where evidence, actions, observations, and verifier outcomes are linked as first-class objects. A proposer-solver-verifier self-play loop expands each domain's KAG: tasks are accepted only if verifiable, process-informative (not one-shot lookup), evidence-covering, and unambiguous. This produces ~100K SFT trajectories averaging 45K tokens — the "horizon" being scaled. Six domains are covered: deep research (44K avg tokens), coding/MLE engineering (48K), scientific reasoning (37K), instruction following (3K), general agentic tasks (39K), and tool calling.

**Three-stage training recipe.**

*Stage 1 — Full-domain SFT.* Fine-tune Qwen3.5-35B-A3B on the full 100K trajectory mix with standard cross-entropy (response tokens only). Produces a general long-horizon agent but suffers domain-conflict performance drops: long-thinking single-turn reasoning patterns clash with multi-turn tool-use patterns.

*Stage 2 — Domain teacher training.* Six specialized teachers are trained via targeted SFT or RL:
- Search teacher: SFT + GRPO RL (correctness reward + efficiency penalty for excess rounds + repetition penalty).
- Science teacher: two-stage SFT (reasoning-enhanced first, then tool-augmented with search/visit/code/scholar tools).
- Instruction-following teacher: two-stage GRPO RL (fine-grained constraint satisfaction stage then long-context ICL stage with dynamic sampling to filter uninformative groups).
- Tool-calling teacher: SFT + PAPO-style GRPO RL with asymmetric process/outcome advantage on a 64-sample hard-task reuse set.

*Stage 3 — Multi-teacher Domain-Routed On-Policy Distillation (OPD) with Salient Vocabulary Alignment (SVA).* The student (initialized from Stage 1) generates on-policy rollouts; each rollout is routed to its domain-specific teacher. SVA replaces the standard sampled-token KD surrogate: at each position, both student and routed teacher are evaluated on the teacher's top-k token support (teacher-selected salient vocabulary), and the loss is the truncated reverse KL over this renormalized support. A domain-normalized aggregation objective averages losses within each active domain then across domains, preventing any single domain from dominating gradients. Tool outputs, user turns, and environment observations are masked from the loss; optimization applies only to student-generated tokens.

## Results

Against 35B and 1T-scale baselines (Table 9 in paper):

| Benchmark | Agents-A1 | Kimi-K2.6 | DSV4-Pro | GPT-5.5 |
|---|---|---|---|---|
| SEAL-0 | **56.4** | 50.5 | 55.0 | 42.3 |
| IFBench | **80.6** | 71.8 | 73.5 | 75.9 |
| HiPhO | **46.4** | 41.1 | 38.7 | 43.3 |
| FS-Olympiad | **79.0** | 73.0 | 76.0 | 78.0 |
| FS-Research | **40.0** | 17.9 | 13.3 | 26.7 |
| GAIA | 96.0 | 80.6 | **98.1** | 87.4 |
| BrowseComp | 75.5 | 83.2 | 83.4 | **84.4** |
| SciCode | 44.3 | 53.5 | 50.0 | **56.1** |
| MLE-Bench-Lite | 43.9 | 62.1 | 63.6 | **72.7** |
| MolBench-Bind | 56.8 | 21.6 | 37.8 | **62.2** |

Agents-A1 leads all 35B baselines on all benchmarks. On MLE-Bench-Lite and SciCode, 1T models retain a clear advantage — attributed to the demands of maintaining long-horizon goal consistency and memory across many experiments. In a 12-hour autonomous MLE run (whale call detection), Agents-A1 raised validation AUC from 0.58 to 0.9935 (gold-medal level) by autonomously chaining temporal analysis, audio augmentation, architectural refinement, and large-scale augmentation steps.

## Limitations

MLE-Bench-Lite and SciCode gaps vs. 1T models persist; authors attribute this to atomic abilities required for stable long-horizon engineering: planning before reasoning, reflection before acting, long-context summarization, and identifying important past information. OPD does not always match individual domain teachers on their specialty — it trades peak domain performance for unified breadth.

## Source
- arXiv: 2606.30616
- Code: https://github.com/InternScience/Agents-A1
- Model: https://huggingface.co/InternScience/Agents-A1
- Captured: `raw/research/weekly-2026-07-04/03-agents-a1-horizon-scaling.md`

## Related
- [[agentflow]] — on-policy Flow-GRPO for agentic systems; complementary trajectory-level RL approach
- [[qwen-agentworld]] — same 35B-class MoE scale, multi-domain agentic training; uses world-model simulation as training environment vs. Agents-A1's real-environment KAG
- [[memagent]] — long-horizon agent via RL-trained memory buffer; third path to long-horizon competence
- [[huxley-godel-machine]] — self-improving coding agent; SWE-bench domain overlap
- [[seal-self-adapting]] — self-improving agents via RL on self-generated data; methodological sibling
- [[deepseek-v4]] — primary 1T-parameter comparison baseline
- [[polar-rl-harness]] — async agentic RL infrastructure for scaling rollout training
- [[skillopt]] — text-space agent skill optimizer; complementary to KAG infrastructure approach
