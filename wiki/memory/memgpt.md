# MemGPT: Towards LLMs as Operating Systems

UC Berkeley paper (Charles Packer et al., arXiv 2310.08560, Oct 2023) that introduces **virtual context management** — treating the LLM context window as a constrained memory resource managed like an OS manages virtual memory, with paging between in-prompt "physical" tokens and out-of-prompt "disk" stores. The paper's framing: *"virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems which provide the illusion of an extended virtual memory via paging between physical memory and disk... we allow the LLM to manage what is placed in its own context (analogous to physical memory) via an 'LLM OS', which we call MemGPT."* MemGPT is the foundational paper for the [[memory-architectures]] *hierarchical virtual context* family; [[letta-memory-blocks]] is its productionised form, and [[codified-context]] is a hand-engineered application-layer instance.

## The two-tier memory

**Main Context** (RAM-like; in-prompt tokens) — three contiguous sections:
- **System instructions** — read-only static block describing control flow, memory hierarchy, and function schemas.
- **Working context** — fixed-size read/write block of unstructured text holding key facts, user preferences, agent persona. Writable only via MemGPT function calls.
- **FIFO queue** — rolling message history (user, agent, system, function I/O). The first slot holds a *recursive summary* of evicted messages.

**External Context** (disk-like; out-of-prompt) — two stores:
- **Recall storage** — full message database; every incoming message and LLM output is written here; searchable via function calls.
- **Archival storage** — arbitrary-length text objects (read/write database); used for long documents and anything evicted from working context.

## Memory operations (function-call interface)

MemGPT exposes its memory management as LLM-callable functions, defined in the system instructions:

- `recall_storage.search(...)` — paginated retrieval of past messages by keyword/semantic query.
- Archival search — vector search (cosine similarity via pgvector/HNSW) over long documents.
- Write to working context — update the fixed-size read/write block with new facts or persona info.
- Write to archival storage — push arbitrary text out-of-context.
- `request_heartbeat=true` — special flag returning control to the LLM processor immediately after a function completes, enabling sequential multi-step retrieval without user intervention.
- Yield (no flag) — pause processor until the next external event.

## Interrupts and control flow

The Queue Manager is the OS-style interrupt mechanism:

- **Memory pressure warning (soft interrupt)** — at ~70% prompt-token utilisation, the queue manager inserts a system message warning of impending eviction, giving the LLM time to flush important content to working context or archival storage.
- **Queue flush (hard interrupt)** — at ~100% capacity, evict ~50% of messages, generate a new recursive summary from existing summary plus evicted messages, write evicted messages to recall storage.

LLM inference is triggered by user messages, system messages (including memory warnings), user interaction alerts (login, file upload), and scheduled timed events — the last enabling MemGPT to act unprompted.

## Evaluation: multi-session chat (DMR)

**Dataset**: Multi-Session Chat (MSC) from Xu et al. 2021 — five human-labelled sessions per conversation; authors added a sixth session with a QA pair. **Deep Memory Retrieval (DMR)** task: agent answers a narrow question only resolvable from prior sessions. Baselines see a lossy recursive summary; MemGPT has paginated recall search.

| Model | Baseline accuracy | + MemGPT |
|---|---|---|
| GPT-3.5 Turbo | 38.7% / ROUGE-L 0.394 | **66.9%** / 0.629 |
| GPT-4 | 32.1% / 0.296 | **92.5%** / 0.814 |
| GPT-4 Turbo | 35.3% / 0.359 | **93.4%** / 0.827 |

Conversation opener task (engagement): MemGPT openers score similarly to or exceed human-written openers on CSIM against gold persona labels (e.g., GPT-4 + MemGPT SIM-1 = 0.868 vs human 0.800).

## Evaluation: document analysis (nested KV retrieval)

**Multi-document QA** (NaturalQuestions-Open with Wikipedia passages in archival storage): fixed-context baselines are capped by the retriever — if the gold article isn't in the top-K passages that fit the context, they cannot recover. MemGPT pages through retriever results via archival search; performance is not capped by context window size. Baselines degrade further as documents are truncated to fit larger K.

**Nested KV retrieval** (paper's new task): 140 UUID key-value pairs (~8k tokens); values may themselves be keys requiring multi-hop lookup across 0–4 nesting levels.

- GPT-3.5 baseline: 0% at 1 nesting level.
- GPT-4 / GPT-4 Turbo baselines: 0% at 3 nesting levels.
- **MemGPT + GPT-4: unaffected across all nesting levels** — handles multi-hop via sequential function calls with `request_heartbeat=true`.

## Self-documented limitations

The conclusion frames these as future work rather than failures:
- Applying MemGPT to other domains with massive or unbounded contexts.
- Integrating different memory tier technologies (databases, caches).
- Improving control flow and memory management policies.

Empirically: MemGPT with GPT-3.5 has significantly degraded document QA performance due to weaker function-calling capability. MemGPT also often stops paging through retrieval results before exhausting the database — a practical failure mode not fully resolved.

## Why it matters

- **Foundation paper for the *hierarchical virtual context* family.** [[memory-architectures]] cites MemGPT as the canonical example. The two-tier RAM/disk framing has propagated through the entire memory ecosystem.
- **Function-call interface as the memory primitive.** The idea that the LLM itself decides when to page memory in or out — via tool calls in its own forward pass — became the dominant pattern. Anthropic's [[anthropic-memory-tool]] is the same idea exposed as an API tool with six commands (view/create/str_replace/insert/delete/rename) over a `/memories` directory.
- **Letta is MemGPT productionised.** [[letta-memory-blocks]] reframes external context as two named stores (Recall + Archival) and adds memory blocks as user-editable schema; the runtime is the same paging logic.
- **Codified Context is MemGPT hand-engineered.** [[codified-context]] applies the same hot/cold tiering as application infrastructure (660-line constitution + cold KB) instead of LLM-self-directed function calls.

## Source

- `raw/research/memory-management/05-01-memgpt.md` (captured 2026-04-26 from https://arxiv.org/pdf/2310.08560 via marker on CPU; figures preserved in `assets/01-memgpt/`)

## Related

- [[memory-architectures]] — survey places MemGPT in the *hierarchical virtual context* mechanism family.
- [[letta-memory-blocks]] — productionisation of MemGPT's tiered memory with persisted memory blocks.
- [[anthropic-memory-tool]] — Claude API's expression of the same paradigm with six explicit commands.
- [[codified-context]] — hand-engineered MemGPT-lineage at application-infrastructure level.
- [[generative-agents]] — contemporaneous (2023) memory-stream paper; cited as related work; both papers are foundational to the modern memory-architecture vocabulary.
- [[topology-taxonomy#long-horizon-context-loss]] — MemGPT is one of the earliest concrete mitigations for the long-horizon context-loss problem.
