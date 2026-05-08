# LongMemEval

ICLR 2025 benchmark by Di Wu (UCLA), Hongwei Wang & Wenhao Yu (Tencent AI Lab Seattle), Yuwei Zhang (UC San Diego), Kai-Wei Chang (UCLA), Dong Yu (Tencent AI Lab) — arXiv 2410.10813. **500 manually-curated questions** embedded in extensible user-AI chat histories, designed to evaluate five core long-term memory abilities: **information extraction (IE), multi-session reasoning (MR), knowledge updates (KU), temporal reasoning (TR), and abstention (ABS)**. Headline empirical finding: long-context LLMs and commercial chat assistants (ChatGPT memory, Coze) show a **30–60% accuracy drop** on LongMemEval relative to offline reading of the same content — the benchmark's gap-vs-ceiling is the cleanest current signal that "has long context" ≠ "has working long-term memory." The paper's second contribution is a **unified three-stage framework** (indexing, retrieval, reading) with four control points (value, key, query, reading strategy), plus four design optimisations the authors identify as broadly effective.

## What it tests — five abilities, seven question types

Each instance is a 4-tuple `(S, q, t_q, a)`: a sequence of timestamped sessions `S`, a question `q` with timestamp `t_q > t_N`, and an answer `a`. Sessions arrive online, one at a time, before the question. The five abilities map to seven question types:

1. **Information Extraction (IE)** — recall specific information (user-side or assistant-side) from the history.
2. **Multi-Session Reasoning (MR)** — synthesise information across multiple sessions (aggregation, comparison).
3. **Knowledge Updates (KU)** — recognise changes in user state and update accordingly.
4. **Temporal Reasoning (TR)** — reason about timestamp metadata + explicit time references.
5. **Abstention (ABS)** — refuse to answer questions whose information is not in the history (false-premise questions, 30 of the 500).

Question types: single-session-user, single-session-assistant, single-session-preference, multi-session, knowledge-update, temporal-reasoning, plus the 30 abstention variants.

## Two standard sizes

- **LongMemEval_S** — ~115k tokens per question (the working dataset for most benchmarks).
- **LongMemEval_M** — 500 sessions per question, ~1.5 million tokens (stress-test).

Histories are constructed needle-in-a-haystack style: evidence sessions (LLM-simulated by self-chatting, then human-edited so the user conveys the evidence indirectly rather than stating it outright) are inserted into a sea of unrelated sessions drawn from ShareGPT and UltraChat plus self-chats on non-conflicting attributes. Length is freely scalable beyond the two standard settings.

## The three-stage framework

The paper's positioning is that long-term memory in chat assistants decomposes into:

| Stage | What happens | Control points |
|---|---|---|
| **Indexing** | Sessions are chunked and stored | *value* (what gets stored — session, round, fact?), *key* (what indexes the value — text, expanded keys?) |
| **Retrieval** | At query time, candidate values are scored and selected | *query* (raw vs expanded query) |
| **Reading** | Retrieved values are read by the LLM to produce the answer | *reading strategy* (Chain-of-Note, structured format) |

This formalism is the paper's lens for comparing memory designs.

## The four recommended design optimisations

§5.2–§5.5 of the paper identify four optimisations the authors find broadly effective on LongMemEval:

1. **Round-level value granularity** (§5.2) — *round* (one user message + one assistant response) outperforms session-level storage. Compressing further into individual user facts harms overall performance (information loss) but **improves multi-session-reasoning accuracy specifically**.
2. **Fact-augmented key expansion** (§5.3) — using the value text itself as the key is a strong baseline; **expanding the key with extracted user facts improves recall@k by 9.4pp and downstream QA accuracy by 5.4pp**. This is the design that justifies hybrid index layers (compact-pointer keys → verbatim values).
3. **Time-aware query expansion** (§5.4) — naive time-agnostic memory designs fail on temporal-reasoning questions; explicit timestamp association + query expansion improves temporal-reasoning recall by 6.8–11.3pp when a strong LLM is used for the expansion step.
4. **Chain-of-Note + structured reading** (§5.5) — even with perfect recall, naive reading is non-trivial; Chain-of-Note prompting plus structured-format presentation of retrieved items improves QA accuracy by up to 10 absolute points across three LLMs.

## Headline empirical findings

- **Commercial assistants degrade sharply.** ChatGPT (with memory) on GPT-4o: **0.5773 accuracy on LongMemEval_S vs 0.9184 on offline reading of the same content** — a 37% drop. Coze on GPT-4o: 0.3299 vs offline-reading equivalent — a 64% drop.
- **Long-context LLMs show 30–60% drops** on LongMemEval_S relative to oracle/offline reading of the same content. The gap widens for smaller models: GPT-4o drops 30.3% (Oracle 0.870 → S 0.606), Llama 3.1 70B drops 55.1%, Phi-3.5 Mini drops 48.1%.
- **Chain-of-Note narrows but does not close the gap** — even with CoN, GPT-4o sits at 0.640 on S vs 0.924 on Oracle (still a 30.7% drop).

## How LongMemEval compares to peer benchmarks

Per Table 1 of the paper:

| Benchmark | Domain | #Sess | #Q | Context depth | IE | MR | KU | TR | ABS |
|---|---|---|---|---|---|---|---|---|---|
| MSC | Open-domain | 5k | — | 1k | ✗ | ✗ | ✗ | ✗ | ✗ |
| MemoryBank | Personal | 300 | 194 | 5k | ✓ | ✗ | ✗ | ✓ | ✗ |
| PerLTQA | Personal | 4k | 8593 | ~1M | ✓ | ✗ | ✗ | ✗ | ✓ |
| LoCoMo (used by [[mem0]]) | Personal | 1k | 7512 | 10k | ✓ | ✓ | ✗ | ✓ | ✓ |
| DialSim | TV shows | 1k–2k | 1M | 350k | ✓ | ✓** | ✗ | ✓ | ✓ |
| **LongMemEval** | Personal | **50k** | **500** | **115k, 1.5M** | ✓ | ✓ | **✓** | ✓ | ✓ |

LongMemEval's distinguishing properties: **only benchmark covering all five abilities including knowledge updates**, freely-extensible context depth, and task-oriented (not open-domain) dialogues.

## Why it matters for the wiki

- **It is the benchmark MemPalace's headline number is computed against.** [[mempalace]]'s 96.6% R@5 raw-mode claim is on LongMemEval. The paper's own design recommendations (round-granularity values + fact-augmented key expansion) frame the gap between MemPalace's *intended* architecture (closets pointing to drawers) and its *benchmarked* configuration (raw ChromaDB cosine over drawer text).
- **It complements [[memory-architectures]]'s evaluation roster.** The survey already documents LoCoMo, MemBench, MemoryAgentBench, and MemoryArena. LongMemEval fills the *recall* slot (vs LoCoMo's QA-leaning slot, MemoryArena's agentic-task slot).
- **The 30–60% drop on long-context LLMs is the cleanest signal** that pure context-window scaling does not solve the long-term memory problem. This is the academic counterpart to [[anthropic-internal-study]]'s cold-start observation and [[willison-cognitive-cost]]'s practitioner account.

## Source

- `raw/research/mempalace/11-longmemeval-paper.md` (captured 2026-04-27 from https://arxiv.org/pdf/2410.10813 via marker on CPU; figures preserved in `assets/longmemeval-paper/`)

## Related

- [[memory-architectures]] — survey; evaluation section now extends to include LongMemEval alongside LoCoMo / MemBench / MemoryAgentBench / MemoryArena.
- [[mempalace]] — the most-cited 2026 implementation graded on this benchmark, with the architecture-vs-benchmark-path gap discussed.
- [[mem0]] — graded on the peer LoCoMo benchmark; same long-context regime, different question-type coverage.
- [[memgpt]] — original LLM-as-OS framing; LongMemEval's three-stage indexing/retrieval/reading framework is a generalisation that subsumes the MemGPT mechanism.
- [[generative-agents]] — the paper's "fact-augmented key expansion" design is the academic-benchmark counterpart to Generative Agents' importance-scored memory stream; both expand the addressable surface beyond raw text.
