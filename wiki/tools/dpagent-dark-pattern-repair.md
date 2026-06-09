# DPAgent-in-the-Middle: Dark Pattern Detection and Repair

An agentic four-agent browser proxy (DPAgent) that intercepts HTTP traffic, detects privacy dark patterns on live web pages with 81.6% micro-F1 (new SOTA), and automatically repairs 77% of them — while also defending against "AI grooming," a formalized threat in which adversaries exploit data voids to seed LLM training pipelines with benign-looking but deceptive UI artifacts that normalize dark patterns in future AI-generated interfaces.

## Source

- **Raw capture:** `raw/research/weekly-2026-06-08/01-dpagent-dark-patterns.md`
- **Paper:** Zewei Shi et al., "DPAgent-in-the-Middle: Agentic Defense and Repair Against AI-Groomed Deceptive Patterns," arXiv:2606.06914, June 2026. Authors from University of Melbourne, CSIRO, Macquarie University, Gachon University. Funded by ARC (DP230101540, DE240101089) and NSF-CSIRO Responsible AI program.
- **Trust level:** Peer-reviewed-quality preprint; expert-annotated dataset (5 annotators, Cohen's κ = 0.85); extensive empirical evaluation.

## Architecture: Four-Agent Pipeline

DPAgent runs as a local MITMProxy instance that mediates all HTTP(S) traffic between the browser and the network. Four specialized sub-agents are orchestrated in sequence:

1. **Grooming Purifying Agent** — Fine-tuned EfficientNet-V2-L classifier filters AI-generated deceptive artifacts (groomed samples) before they reach downstream agents. Achieves F1 = 0.9022 on grooming detection; defends 90.98% of generated grooming images. Also applies defensive prompting to the downstream MLLM.

2. **Task Generation Agent** — RL-optimized prompt generation (PPO on Qwen-QWQ-32B as policy, o4-mini as target MLLM) drives realistic user-behavior-simulated browser exploration. Achieves 80.6% dark pattern type coverage while visiting only ~9.5–12.2% of the pages required by BFS, random, or policy-based baselines.

3. **PDP Detection Agent** — Gemini 2.5 Pro with expert-validated prompts and structured taxonomy. Micro-F1 = 0.816, macro-F1 = 0.691. New SOTA; improves 27.84% (micro) and 38.64% (macro) over prior best (DPGuard). Browser automation via Claude 3.7 Sonnet Computer Use.

4. **Interface Repairing Agent** — Claude Computer Use + MITMProxy DOM rewriting applies five PMT-grounded repair approaches. Successfully repairs 77% of detected deceptive instances. Repaired page snapshots (HTML + cookie state) are cached; subsequent visits are served from cache with no re-inference cost.

**Runtime (cold-start, per page):** 1.6 s exploration + 0.9 s detection + 1.1 s repair. Heavy inference runs during device idle time; active browsing served from cache.

## AI Grooming Threat Model

AI grooming is distinct from classical data poisoning, backdoor attacks, and jailbreaks. It operates through **semantic deception**: injecting logically coherent, human-benign content into data voids — underrepresented query spaces where authoritative content is absent — so that LLM training pipelines preferentially ingest and reproduce deceptive UI patterns.

Two attack vectors:

- **User-Facing Grooming** — An LLM is manipulated to generate UI content (consent dialogs, ad frames, privacy notices) that appears visually and statistically benign to humans but carries hidden deceptive intent (hidden trackers, manipulative consent logic). Bypasses human-in-the-loop review because the semantic gap lies between human perception and machine execution.

- **Supply-Chain Grooming** — Groomed samples are seeded into data voids so that future foundation models learn to normalize or reproduce deceptive patterns by default. Because these samples lack the statistical anomalies of conventional poisoning, they evade standard automated data quality audits.

Real-world evidence cited: state-aligned disinformation networks operating hundreds of affiliated sites to flood crawlers; NewsGuard-documented state-sponsored network exploiting low-competition spaces to manipulate Western AI systems; millions of AI-generated articles that have already misled major AI systems into propagating false narratives (2024 record). The Open Source Foundation audit found LLMs reproduce state-backed disinformation under benign prompts.

**Bidirectionality note:** The same data-void-exploitation mechanism used by consumers defensively (see [[adversarial-data-poisoning]]) is actively deployed by industry and state actors offensively to normalize dark patterns in AI training pipelines. The mechanism is not unambiguously consumer-favorable.

## Dark Pattern Taxonomy (Privacy Deceptive Patterns)

DPAgent uses the **Privacy Deceptive Patterns (PDP) taxonomy** — an extension of DPGuard's taxonomy that adds privacy-specific use-case descriptions and targeted repair methods. Seven pattern types across three categories:

| Category | Pattern | Repair Approach |
|---|---|---|
| Information Concealment | Hidden Information | Warning + Highlight Links |
| Information Concealment | Disguised Ads (without hint) | Block Content |
| Information Concealment | Disguised Ads (with hint) | Warning |
| Interface Obstruction | Pre-Selection | Warning |
| Interface Obstruction | False Hierarchy | Auto Cookie Setting + UI Cleaning |
| Interface Obstruction | Small Close Button | Warning |
| Forced Data Disclosure | Privacy Zuckering | Warning + Highlight Links |
| Forced Data Disclosure | Forced Action | Warning + Highlight Links |

**Five repair approaches (PMT-grounded):**
- **Warning** — adds highlighted alert before deceptive element; used where regulatory constraints prevent direct removal (pre-selection, small close button, privacy zuckering, forced action)
- **Highlight Links** — makes visually obscured privacy-related hyperlinks prominent
- **Block Content** — removes element entirely; restricted to clear regulatory violations (undisclosed ads)
- **Auto Cookie Setting** — resets cookies to match user's stated intent (necessary-only), countering false-hierarchy-induced over-acceptance
- **UI Cleaning** — standardizes button appearance to eliminate false visual hierarchy

## Empirical Findings (485 Real Sites)

- **98.14%** of 485 real-world websites contain at least one PDP when fully explored (vs. 34.43% on homepage only)
- **>90%** of detected PDPs can be mitigated by DPAgent
- Top violations: Hidden Information (18.2%), Forced Action (15.6%), Disguised Ads (10.6%)
- Hardest to repair: Disguised Ads (ambiguous decision boundary + complex HTML hierarchy)
- Geographic prevalence (homepage only): Oceania 84%, Asia 80%, Americas 78%, Europe 70%
- GDPR measurably reduces prevalence in European sites — useful regulatory lever argument

User study (40 participants, 8 use cases): average effectiveness rating 4.10/5; average browsing experience impact rating 4.16/5.

## Code and Tool Availability

Research prototype; **not yet publicly released as a browser extension**. Modular architecture is designed to allow lightweight extension packaging. Key components (grooming filter, PDP detector) are identified as independently modularizable. Privacy preserved: data processed locally or via anonymized APIs with no user-identifier storage. Future work targets real-time and edge deployment.

## Actionable Design Patterns

1. **Idle-time + cache architecture** — MITMProxy + cached repair snapshots is a directly adoptable pattern for a privacy-protective browser extension: run heavy AI inference once per domain during device idle time, serve cached repaired pages on subsequent visits.
2. **RL-based task generation** is substantially more efficient than BFS or random crawling for dark pattern discovery — relevant design choice for any automated audit tool.
3. **PMT-grounded repair vocabulary** provides a legally conservative framework: Warning is used where direct removal would be legally or functionally problematic; Block Content only where regulatory violation is unambiguous.
4. **Grooming defense in training pipelines** — building training data filters and maintaining a curated high-quality dark pattern taxonomy is a counter-strategy for tool designers facing adversarial seeding.

## Related

[[obfuscation]], [[adversarial-data-poisoning]], [[transparency-tools]], [[health-data-opt-out-dark-patterns]], [[dsar-and-data-deletion]], [[privacy-badger]], [[adnauseam]], [[data-disruption-strategy-map]]
