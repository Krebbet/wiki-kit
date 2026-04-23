# Reference sources

What `/weekly-brief` scans for **this wiki**. High-signal-first; aggregators before individual feeds. Setup-approved 2026-04-23 via interview.

## Scope (the brief's frame)

Focus on:
- **New papers that touch the existing thesis** (single-sample RL, concept-based learning, teacher-student RL, RLVR mechanics, curriculum learning, catastrophic forgetting, concept learning, in-context learning theory).
- **Old papers that deepen understanding** of concepts already on the wiki — re-surfacing foundational work when it's becoming load-bearing this quarter.
- **Emerging topics from the evolving thesis** — if the wiki's synthesis pages ([[research/synthesis/single-sample-concept-skeleton]], [[research/synthesis/proposed-method]], [[research/synthesis/concept-curriculum-method]]) grow new directions, signals related to those become in-scope.

Exclude:
- Big-lab foundation-model releases without post-training detail.
- Agentic systems, RAG, long-context evals — unless they directly touch the thesis.
- Product / benchmark-leaderboard news without a method contribution.

## Aggregators (scan first)

| Source | Why | URL |
|---|---|---|
| **alphaXiv weekly trending (cs.LG, cs.CL, cs.AI)** | Explicit popularity ranking on arXiv. | https://www.alphaxiv.org/trending |
| **Hugging Face papers trending** | Community-attention signal. | https://huggingface.co/papers |
| **Papers With Code — trending on reasoning benchmarks** | Benchmark-grounded movement (MATH, AIME, GSM8K, GPQA, HumanEval). | https://paperswithcode.com/sota |
| **r/MachineLearning — hot (past week)** | Broad ML community; better for filtering hype than discovery. | https://www.reddit.com/r/MachineLearning/top/?t=week |
| ~~r/LocalLLaMA~~ | **Flagged for replacement** — user to pick a more appropriate subreddit. Skip for now. | — |

## Curators (weekly scan)

| Source | Why | URL |
|---|---|---|
| **@_akhaliq (AK) X timeline** | Daily arXiv-paper curator; strong frontier-awareness. | https://x.com/_akhaliq |
| **@arankomatsuzaki** | Researcher-curated paper feed; taste overlaps wiki scope. | https://x.com/arankomatsuzaki |
| **Interconnects (Nathan Lambert)** | RL-for-LLMs focused; best for GRPO-family / post-training news. | https://www.interconnects.ai |
| **Import AI (Jack Clark)** | Weekly digest with taste; cross-domain. | https://jack-clark.net |
| **Simon Willison's TIL / blog** | Frontier practitioner notes. | https://simonwillison.net |

## Labs + research blogs (scan for new posts)

| Lab | Why for this wiki |
|---|---|
| **Sakana AI** — https://sakana.ai | RLT lineage; teacher-student RL; small-model training |
| **DeepSeek-AI** — https://www.deepseek.com | GRPO, R1, math-reasoning post-training |
| **Qwen team (Alibaba)** — https://qwenlm.github.io | GSPO; open-weights reasoning models |
| **ByteDance Seed / Tsinghua AIR** — https://team.doubao.com/en | DAPO; open RL at scale |
| **SAIL** — https://sail.sg | Dr. GRPO; R1-Zero critical analyses |
| **Meta FAIR** — https://ai.meta.com/research/ | Kwiatkowski likelihood rewards; MAML |
| **Thinking Machines Lab** — https://thinkingmachines.ai/blog | On-Policy Distillation; post-training efficiency |
| **Anthropic research** — https://www.anthropic.com/research | Constitutional AI; critique/self-correction |
| **DeepMind research** — https://deepmind.google/research | Algorithm Distillation; general RL theory |
| **MIT CSAIL / Meta FAIR collaborations** | SOAR; bilevel meta-RL |
| **Allen AI (AI2)** — https://allenai.org | Tülu post-training recipes; OLMo open-stack; strong research voice |
| **Qualcomm AI Research** — https://www.qualcomm.com/research/artificial-intelligence | On-device / small-model, quantisation, efficient RL — relevant to 1–40B scope |

## Podcasts (low priority — skim only if a specific episode flags a paper)

Deprioritised per setup interview. The brief's agent should not invest significant time on podcast content unless a candidate paper is being cross-surfaced with other signals and a podcast episode adds context.

## Code / release proxies (discovery only)

| Signal | Why |
|---|---|
| **GitHub stars on tracked repos** — SakanaAI/RLT, BytedTsinghua-SIA/DAPO, sail-sg/understand-r1-zero, siyan-zhao/OPSD, lasgroup/SDPO, thunlp/OPD, RUCBM/G-OPD, Zhen-Tan-dmml/ExGRPO, QwenLM/Qwen | Indirect adoption signal — star spikes often precede follow-up papers. |
| **Hugging Face model releases** — watchlist: SakanaAI, Qwen, DeepSeek-AI, allenai, mistralai, meta-llama | Post-training recipe changes often ship as model cards first. |

## Selection priority (per the setup interview)

When trimming candidates to the (≤5) capture list, priorities **in this order** for this wiki:

1. **Technical novelty over volume** — a single new mechanism > five reframings of one.
2. **Conflict-resolving** — would the paper resolve an open `wiki/conflicts/*.md` or one of the open contradictions in the wiki? Prioritise.
3. **Wiki-fit** — tightly on-scope per the Scope section above.
4. **Reproducibility** — code released > promised > closed.
5. **Multiple independent signals** — useful but deliberately deprioritised (trust thesis-fit judgment over mob attention).

## Local conventions for the brief (per setup interview)

These are preferences specific to *this* wiki. The agent running `/weekly-brief` in this checkout must honour them.

- **Never force entries.** If a section (Trends, Top 3, Other watchlist references, Conflicts) has nothing load-bearing to report, **omit the section entirely**. Do not pad. If the whole brief has nothing to report, the empty-run policy fires (3-line "nothing this week" email).
- **Tone for trend bullets:** *terse + factual + thesis-relevant*. Every trend bullet should include a clause answering "how does this touch our thesis?" — i.e. which synthesis page, corpus theme, or open question the trend interacts with. If you can't answer that, the bullet is probably noise and shouldn't be in the brief.
- **Autogenerated wiki pages link back to the brief.** Every page written during the autonomous ingest step must include in its `## Related` section: `- [[../weekly-briefs/<YYYY-MM-DD>]] — brought in by the <YYYY-MM-DD> weekly sweep`. This makes the ingest provenance traceable.
- **Frequency:** Sunday 7am local (America/Toronto). Cron line:
  ```
  0 7 * * 0 cd /home/david/code/wiki-single-sample-learning && claude -p "/weekly-brief" >> /tmp/weekly-brief-cron.log 2>&1
  ```
  The `0` at the end is Sunday in cron (0=Sun, 1=Mon, …, 6=Sat). Note: no `git checkout` step — this wiki keeps weekly output on the main working branch (`single-shot-training-wiki`), per D5 of the setup interview.
- **Branch policy:** weekly output goes on whatever the current branch is — no dedicated `weekly-*` branch. The brief is part of the wiki.
- **Delivery:** email to `david.hugh.mcnamee@outlook.com`; Telegram ping enabled.
- **Watchlist seeding policy:** user-driven only. Do not pre-populate. If the weekly sweep finds a surplus candidate worth tracking, the *agent* can add it to watchlist.md as a 1-line entry (cap 10/run) — but the *initial* watchlist state must stay empty until the user chooses what to seed.

## Related

- [[watchlist]] — the persistent radar this file is meant to populate
- [[index]] — wiki-wide page catalog
- [[research/synthesis/concept-curriculum-method]] — current project north star
