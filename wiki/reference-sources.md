# Reference sources

What the `/weekly-brief` sweep scans. High-signal-first; aggregators before individual feeds. Edit this file to narrow or broaden the radar — the brief agent reads this to decide where to look.

Wiki scope, for tuning relevance: novel fine-tuning methods for small LLMs (1–40B), **single-sample / concept-based learning**, teacher-student RL, RLVR mechanics (GRPO-family optimisers, length-bias fixes, sparse subnetworks), on-policy distillation, catastrophic forgetting in post-training, concept learning (CBMs / RCE), data-efficient fine-tuning, in-context learning theory, meta-learning, test-time training.

## Aggregators (scan first)

| Source | Why | URL |
|---|---|---|
| **alphaXiv weekly trending (cs.LG, cs.CL, cs.AI)** | Explicit popularity ranking on arXiv; first stop for "what's moving". | https://www.alphaxiv.org/trending |
| **Hugging Face papers trending** | Community-attention signal, surfaces practitioner-relevant releases. | https://huggingface.co/papers |
| **Papers With Code — trending on reasoning benchmarks** | Benchmark-grounded movement on MATH, AIME, GSM8K, GPQA, HumanEval. | https://paperswithcode.com/sota |
| **r/MachineLearning — hot (past week)** | Broad ML community; better for filtering hype than discovery. | https://www.reddit.com/r/MachineLearning/top/?t=week |
| **r/LocalLLaMA — hot (past week)** | Small-model / open-weights practitioner signal; good for fine-tuning / RL releases. | https://www.reddit.com/r/LocalLLaMA/top/?t=week |

## Curators (weekly scan)

| Source | Why | URL |
|---|---|---|
| **@_akhaliq (AK) X timeline** | Daily arXiv-paper curator; strong frontier-awareness. | https://x.com/_akhaliq |
| **@arankomatsuzaki** | Researcher-curated paper feed; taste overlaps wiki scope. | https://x.com/arankomatsuzaki |
| **@natolambert** — Interconnects newsletter / blog | RL-for-LLMs focused; best for GRPO-family / post-training news. | https://www.interconnects.ai |
| **Jack Clark — Import AI** | Weekly digest with taste; cross-domain AI news. | https://jack-clark.net |
| **Simon Willison's TIL / blog** | Frontier practitioner notes; surfaces fine-tuning / agent releases. | https://simonwillison.net |

## Labs + research blogs (scan for new posts)

| Lab | Why for this wiki |
|---|---|
| **Sakana AI** — https://sakana.ai | RLT lineage; teacher-student RL; small-model training innovations |
| **DeepSeek-AI** — https://www.deepseek.com | GRPO, R1, math-reasoning post-training |
| **Qwen team (Alibaba)** — https://qwenlm.github.io | GSPO; open-weights reasoning models; post-training recipes |
| **ByteDance Seed / Tsinghua AIR** — https://team.doubao.com/en | DAPO; open RL at scale |
| **SAIL** — https://sail.sg | Dr. GRPO; R1-Zero critical analyses |
| **Meta FAIR** — https://ai.meta.com/research/ | Kwiatkowski likelihood rewards; MAML / meta-learning |
| **Thinking Machines Lab** — https://thinkingmachines.ai/blog | On-Policy Distillation; post-training efficiency |
| **Anthropic research** — https://www.anthropic.com/research | Constitutional AI; critique/self-correction |
| **DeepMind research** — https://deepmind.google/research | Algorithm Distillation; general RL theory |
| **MIT CSAIL / Meta FAIR collaborations** | SOAR; bilevel meta-RL |

## Podcasts (scan last 2 weeks)

| Source | Why |
|---|---|
| **Latent Space** — https://www.latent.space | Frontier-model-deployment signal; interviews often reveal paper directions ahead of publication. |
| **Dwarkesh Podcast** — https://www.dwarkeshpatel.com | Deep interviews with frontier researchers. |
| **Cognitive Revolution** — https://www.cognitiverevolution.ai | ML-research-heavy episode notes. |
| **NeurIPS / ICML / ICLR / COLM / COLT recorded talks** — appear on YouTube after conference dates | Authoritative primary source; use only when a talk directly expands a captured paper. |

## Code / release proxies (discovery only)

| Signal | Why |
|---|---|
| **GitHub stars on tracked repos** (Sakana RLT, verl, DAPO, Dr. GRPO repos, `siyan-zhao/OPSD`, `lasgroup/SDPO`, `thunlp/OPD`, `RUCBM/G-OPD`, `Zhen-Tan-dmml/ExGRPO`) | Indirect adoption signal — star spike often precedes a follow-up paper. |
| **Hugging Face model releases** — watchlist: SakanaAI, Qwen, DeepSeek-AI, mistralai, meta-llama | Post-training recipe changes often ship as model cards first. |
| **Tinker-cookbook (Thinking Machines)** — https://github.com/thinking-machines-lab/tinker-cookbook | Reference implementations tracking OPD state of the art. |

## Selection priority for the brief

When trimming candidates to the (≤5) capture list, prioritise (in order):
1. Papers that resolve an *open question* in [[research/synthesis/single-sample-concept-skeleton]], [[research/synthesis/proposed-method]], or [[research/synthesis/concept-curriculum-method]].
2. Papers that would resolve a conflict already open in `wiki/conflicts/*.md`.
3. Papers from labs with prior corpus presence (Sakana, DeepSeek, SAIL, ByteDance, Meta FAIR, Alibaba Qwen, Thinking Machines).
4. Papers with code released and non-trivial empirical results on MATH / AIME / GSM8K / GPQA.

## What to deprioritise

- Pure benchmark-scaling papers without a method contribution.
- New foundation-model announcements without post-training detail.
- Speculative theory with no empirical grounding, unless it directly informs one of the project's three method proposals.
- Application papers (agentic systems, RAG evaluation, etc.) unless they demonstrate something relevant to concept-based learning.

## Related

- [[watchlist]] — the persistent radar this file is meant to populate
- [[index]] — wiki-wide page catalog
- [[research/synthesis/concept-curriculum-method]] — current project north star
