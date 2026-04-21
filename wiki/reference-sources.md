# Reference Sources

Curated trend radar for the AI-research wiki. Seeded 2026-04-21.

## Purpose

This file is the starting list of channels the wiki *watches* for new methods, papers, and community signal — distinct from the captured raw sources under `../raw/`. `/lint` consults this file each run to:

1. Sweep each active source for items published since the last sweep.
2. Compare surfaced items against wiki coverage.
3. Propose candidates for `/research` or `/ingest`, ranked by fit to the domain (LLM/SLM training, fine-tuning, RL, neural architectures, CV, evolutionary approaches to LLMs).
4. Evolve this file: flag dead/low-signal sources for retirement, propose additions.

Nothing here is captured yet. Capture happens only after the user approves a candidate during `/lint` or runs `/research` / `/ingest` directly.

## Status vocabulary

- **active** — sweep every `/lint` run.
- **probation** — sweep, but demote to retired if no signal lands after N lint runs.
- **retired** — historical record; don't sweep. Kept here so a future `/lint` doesn't re-propose something already tried and dropped.

## How `/lint` evolves this list

Each `/lint` run, after the sweep, propose:
- **Add**: a source that was referenced ≥3 times across captured sources or other radar entries and isn't already here.
- **Demote**: move active → probation if two consecutive sweeps surfaced nothing relevant.
- **Retire**: probation → retired after three zero-signal sweeps.
- **Promote**: probation → active after a single high-quality hit (something we actually ingested).

Ask the user before editing this file; don't auto-mutate.

---

## Paper-feed accounts (X / Twitter)

X/Twitter is gated for programmatic capture. `capture_url --js` sometimes works, often fails. Fallback: paste the interesting thread into `raw/manual/<slug>/<slug>.md` and `/ingest`.

| Handle | URL | Role | Added | Status |
|---|---|---|---|---|
| @_akhaliq (AK) | https://x.com/_akhaliq | Highest-volume daily feed of new arXiv papers, model releases, HF Spaces. | 2026-04-21 | active |
| @arankomatsuzaki | https://x.com/arankomatsuzaki | Daily arXiv paper picks with short notes. Strong signal-to-noise. | 2026-04-21 | active |
| @karpathy | https://x.com/karpathy | Thinking and intuition on LLM training / scaling / methods. Low volume, high signal. | 2026-04-21 | active |
| @dair_ai | https://x.com/dair_ai | Weekly ML research threads and paper explainers. | 2026-04-21 | active |
| @alphaxiv | https://x.com/askalphaxiv | alphaXiv — social layer around arXiv; surfaces trending papers. | 2026-04-21 | active |
| @rohanpaul_ai | https://x.com/rohanpaul_ai | Daily paper and model highlights with technical detail. | 2026-04-21 | probation |
| @jackclarkSF | https://x.com/jackclarkSF | Anthropic policy lead; writes "Import AI" newsletter — policy + capability signal. | 2026-04-21 | active |

## GitHub awesome-lists

These are meta-sources: curated link collections maintained by the community. `/lint` should sweep their recent commits / changelogs to spot what was added since the last sweep.

| Repo | URL | Focus | Added | Status |
|---|---|---|---|---|
| Hannibal046/Awesome-LLM | https://github.com/Hannibal046/Awesome-LLM | Flagship general LLM list; broad coverage. | 2026-04-21 | active |
| opendilab/awesome-RLHF | https://github.com/opendilab/awesome-RLHF | RLHF + preference-learning papers, frameworks, datasets. Directly on-topic. | 2026-04-21 | active |
| Curated-Awesome-Lists/awesome-llms-fine-tuning | https://github.com/Curated-Awesome-Lists/awesome-llms-fine-tuning | Fine-tuning tutorials, papers, tools, best practices. | 2026-04-21 | active |
| KbsdJames/Awesome-LLM-Preference-Learning | https://github.com/KbsdJames/Awesome-LLM-Preference-Learning | Preference optimization variants (ORPO, DPO family, GRPO). | 2026-04-21 | active |
| JLZhong23/awesome-reward-models | https://github.com/JLZhong23/awesome-reward-models | Reward model training, reward hacking, process reward models. | 2026-04-21 | active |
| zzli2022/Awesome-System2-Reasoning-LLM | https://github.com/zzli2022/Awesome-System2-Reasoning-LLM | Reasoning-focused methods, RLVR lineage. | 2026-04-21 | active |
| LightChen233/Awesome-Long-Chain-of-Thought-Reasoning | https://github.com/LightChen233/Awesome-Long-Chain-of-Thought-Reasoning | Long CoT, process supervision, reasoning RL. | 2026-04-21 | active |
| glgh/awesome-llm-human-preference-datasets | https://github.com/glgh/awesome-llm-human-preference-datasets | Preference datasets for RLHF / DPO / eval. | 2026-04-21 | probation |
| rkinas/reasoning_models_how_to | https://github.com/rkinas/reasoning_models_how_to | Research notes on training LLMs + RLHF (individual-maintained). | 2026-04-21 | probation |

## Podcasts

Podcasts with RSS feeds can be programmatically sampled for episode titles + descriptions (capture_url on the show's episode-index page works). Episode transcripts via `fetch_transcript` when a YouTube version exists.

| Podcast | URL | Role | Added | Status |
|---|---|---|---|---|
| Dwarkesh Podcast | https://www.dwarkesh.com/podcast | Long-form interviews with frontier researchers (OpenAI, DeepMind, Anthropic). Alignment, scaling, capabilities. | 2026-04-21 | active |
| Latent Space | https://www.latent.space/ | AI-engineering deep dives; fast to cover new techniques. | 2026-04-21 | active |
| The Cognitive Revolution | https://www.cognitiverevolution.ai/ | Nathan Labenz — balance of technical and strategic AI content. | 2026-04-21 | active |
| TWIML AI Podcast | https://twimlai.com/podcast/twimlai/ | Sam Charrington — research-oriented ML interviews. Long-running, broad. | 2026-04-21 | active |
| Practical AI | https://changelog.com/practicalai | Applied ML; occasionally surfaces tooling relevant to fine-tuning / MLOps. | 2026-04-21 | probation |

## Subreddits

Reddit captures cleanly via `capture_url` on `old.reddit.com/r/<sub>/top/?t=week` (or a specific thread URL).

| Subreddit | URL | Role | Added | Status |
|---|---|---|---|---|
| r/MachineLearning | https://old.reddit.com/r/MachineLearning/ | Paper breakdowns, method debates, job-board noise — filter for `[R]` flair. | 2026-04-21 | active |
| r/LocalLLaMA | https://old.reddit.com/r/LocalLLaMA/ | Open-model practitioners; fast signal on new open weights, fine-tuning recipes, quantization. | 2026-04-21 | active |
| r/MLScaling | https://old.reddit.com/r/MLScaling/ | Scaling laws, compute/data efficiency, frontier model analysis. Low volume, high signal. | 2026-04-21 | active |
| r/LanguageTechnology | https://old.reddit.com/r/LanguageTechnology/ | NLP-specific discussion, occasionally surfaces niche fine-tuning work. | 2026-04-21 | probation |
| r/computervision | https://old.reddit.com/r/computervision/ | CV-specific threads; on-topic for the CV side of the wiki. | 2026-04-21 | probation |

## Discord communities

Discord is gated — no public capture. Relevant channels to monitor manually. When something interesting shows up, paste the excerpt into `raw/manual/<slug>/<slug>.md` with channel + author + date metadata, then `/ingest` that path.

| Community | Notes | Added | Status |
|---|---|---|---|
| EleutherAI | Long-running open ML research community; #announcements and #papers channels are high-signal. | 2026-04-21 | active |
| Hugging Face | Official HF Discord; `#papers` channel. | 2026-04-21 | active |
| Latent Space | Community associated with the podcast; practitioner-heavy. | 2026-04-21 | probation |
| Nous Research | Open-model research collective; fine-tuning, synthetic data. | 2026-04-21 | probation |
| LocalLLaMA | Discord companion to the subreddit. | 2026-04-21 | probation |

Invite links change; find current invites through each community's website or pinned posts in their subreddit / X profile.

---

## Related

- [[CLAUDE]] — wiki operating manual
- [[index]] — content catalog
