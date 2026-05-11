# Direct Corpus Interaction — Beyond Semantic Similarity (arXiv 2605.05242, May 2026)

Multi-institution academic paper that argues agentic search should let the agent **search the raw corpus** using general-purpose terminal tools (`grep` / `rg` / `find` / `head` / `cat` / `bash`) instead of querying a vector index or BM25 retriever. Headline: with the same Claude Sonnet 4.6 backbone, replacing Qwen3-Embedding-8B retrieval with **direct corpus interaction (DCI)** lifts BrowseComp-Plus 69.0% → 80.0% (+11 pp) **while reducing cost 29.4%**. The mechanism is *retrieval interface resolution*, not better recall: DCI surfaces *fewer* gold documents on average but localises within them more precisely. The clearest 2026 academic articulation of the practitioner CLI-skepticism running through [[case-studies/notion-token-town]] and [[deployments/openai-symphony]]. Currently #1 on HuggingFace papers.

## Source

- arXiv 2605.05242, "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction" — `raw/research/weekly-2026-05-11/05-beyond-semantic-similarity.md` (marker on CPU). May 2026.
- Authors: Zhuofeng Li (TAMU), Haoxiang Zhang (Waterloo/UCSD), Cong Wei, Pan Lu (Stanford), Ping Nie, Yi Lu, Yuyang Bai, Shangbin Feng (UW), Hangxiao Zhu, Ming Zhong (UIUC), Yuyu Zhang (Verdent AI), Jianwen Xie (Lambda), Yejin Choi, James Zou (Stanford), Jiawei Han (UIUC), Wenhu Chen, Jimmy Lin, Dongfu Jiang (Waterloo), Yu Zhang (TAMU). Multi-institution academic; primary source.
- Code: `https://github.com/DCI-Agent/DCI-Agent-Lite` (referenced in the abstract page).
- High-attention crystallisation of a doctrinal shift; not yet independently replicated.

> **The medium shapes and controls the scale and form of human association and action.** *— Marshall McLuhan, paper epigraph.*

## Core argument

The bottleneck isn't the retriever — it's the **retrieval interface resolution**. As models become stronger, the constraint isn't reasoning-over-retrieved-snippets but the granularity of what the retrieval interface exposes. Top-k similarity collapses the corpus into a fixed-format ranked list and silently filters out evidence that downstream reasoning cannot recover.

DCI moves the semantic interpretation **downward into the LLM at query time** rather than concentrating it in an offline index built ahead of time. No offline indexing, no embedding model, no top-k retrieval API. The agent uses general-purpose terminal tools — `grep`, `rg`, `find`, `head`, `tail`, `cat`, lightweight shell scripts — to traverse the raw corpus.

The paper frames retrieval as a **medium-design problem**: the retrieval interface determines what the agent can observe, verify, and act upon.

## Two scaffolds (interface vs harness, separated)

- **DCI-Agent-Lite.** Minimal Pi-based harness, only `bash` + `read`, lightweight runtime context-management. Default backbone GPT-5.4 nano, reasoning effort high, 300-turn budget. Used for controlled ablations.
- **DCI-Agent-CC.** Claude Code as the off-the-shelf CLI agent, Sonnet 4.6 backbone, reasoning effort medium. Web-search, web-fetch, and subagents *disabled*; data directory blocked to prevent answer leakage. Probes the performance frontier.

## Headline results

### BrowseComp-Plus (matched backbone)

| System | Backbone | Retriever / Interface | Accuracy | Cost |
|---|---|---|---|---|
| **DCI-Agent-CC** | Sonnet 4.6 | DCI | **80.0%** | **$1,016** |
| Claude Code + retrieval | Sonnet 4.6 | Qwen3-Embedding-8B | 69.0% | $1,440 |
| Best retrieval baseline | GPT-5 | Qwen3-Embedding-8B | 71.7% | — |

Same backbone, swapping retriever for DCI: **+11.0 pp accuracy and −29.4% cost**. Beats the strongest retrieval baseline overall by **+8.3 pp**.

### Lightweight setting

DCI-Agent-Lite on **GPT-5.4 nano** hits **62.9%** on BrowseComp-Plus at **$93** — competitive with `o3 + Qwen3-Embedding-8B` (66.0%) at one-seventh the cost.

### Multi-hop QA (DCI-Agent-CC)

**83.0% average across six knowledge-intensive QA benchmarks** (Sonnet 4.6 backbone). Best retrieval-agent baseline (ASearcher-Local-14B): 52.3%. **+30.7 pp.**

- MuSiQue: +50 pp
- HotpotQA: +30 pp
- 2Wiki: +26 pp

### IR ranking

DCI-Agent-CC at **68.5 NDCG@10** across BRIGHT and BEIR datasets — **+21.5 pp** over ReasonRank-32B, the strongest reasoning-oriented reranker baseline.

## Mechanism: interface resolution, not recall

The most important conceptual contribution. On a 100-question BrowseComp-Plus subset:

| Metric | DCI | Qwen3-Embedding-8B retrieval |
|---|---|---|
| Mean coverage (recall) | **28.0** (lower) | 56.7 |
| Localization (within-doc) | **48.4** (higher) | 21.7 |

DCI surfaces *fewer* gold documents on average but **once a useful document is reached, narrows to a small high-value evidence span**. It trades exhaustive recall for fine-grained local progress.

**Trajectory analysis (RQ2).** DCI-Agent-CC wins 176 questions where the matched retrieval agent (Qwen3-Embedding-8B + Sonnet 4.6) loses, vs only 76 in reverse. Of the 176 CC-wins, only 34 had no gold documents retrieved by the retrieval agent — meaning **142 (81%) were post-retrieval-failure or partial-chain failures** where retrieval surfaced gold but the agent couldn't use it. *DCI's win is in evidence use, not evidence reach.*

## Where the lift comes from (tool-set ablation)

- With only `read + grep` (no full bash), DCI-Agent-Lite hits 61% on BrowseComp-Plus — already +16 pp over Qwen3-Embedding-8B retrieval.
- Open bash adds another +12 pp at higher cost.

**The interface change carries the bulk of the gain; tool-set richness adds incremental value.**

## Tool-call distribution

**DCI-Agent-CC on BrowseComp-Plus:** Bash 62.4%, Grep (Claude Code's built-in) 33.0%. Within Bash: chained search (`rg|rg`) 22.3%, local context peeking (`rg|head`) 18.0%, regex matching 17.0%, file localization (`find|rg`) 14.0%, **full-document reads only 9.1%**. The agent uses bash as a high-resolution search interface, not a document fetcher.

**DCI-Agent-Lite on 100 cases (3,168 commands):** `rg|head` 56.2%, `rg|rg` 20.6%, `wc` 7.8%, single-keyword `rg` 6.3%, `ls` 4.3%, `python -c` 2.4%, `find|rg` 2.1%, **`cat` 0.1%**.

Six chronological operation patterns observed:

1. Corpus exploration
2. Broad keyword search
3. Iterative narrowing
4. Targeted reading
5. In-document deep search
6. Cross-document comparison

## Operating envelope

**Scales well in depth, poorly in breadth.** Doubling the corpus (100K → 200K docs) more than doubles tool calls and cost while dropping accuracy 13.6 pp. At 400K docs, accuracy falls to 37.5% with 122 calls/q on average. The high-resolution interface remains powerful *once* the agent reaches a promising document; finding that anchor in larger candidate spaces is the limit.

This is the paper's central operational caveat: DCI is a workspace / project-scale solution in its current form, not a 10M-doc enterprise-corpus solution. Hybrid (cheap retriever to narrow the candidate set, then DCI within that subset) is **unexplored** — see [Open questions](#open-questions).

## Runtime context-management is non-monotonic

Five policies tested (L0–L4 = none / truncation / + compaction / + summarization). **L3 wins on accuracy (77)** despite L1 retaining more verbatim gold evidence (31.3 vs 27.0). **L4 (full summarization) underperforms L3** — adds cost (4531s latency) without accuracy gain (73 vs 77).

> Selectively forgetting is beneficial; preserving more isn't the same as maintaining the right working state for continued search.

Three-layer mechanism:

- *Truncation* — cap each tool result (50K → 20K char cap).
- *Compaction* — zero-LLM in-memory clearing of older tool-result turns above a threshold, replacing with placeholders preserving tool-call structure.
- *Summarization* — model-generated summary replacing compacted history when token budget pressed.

## Where this fits the wiki

### Convergence with practitioner findings

- [[case-studies/notion-token-town]] — Notion's four-axis MCP-vs-CLIs framing identifies CLIs as winning on *capability/bootstrap power* (`--help` progressive disclosure, agent self-debug). DCI generalises this from tool-API retrieval to **corpus retrieval**. Notion's "vector embeddings are less and less" finding for agent-driven enterprise search is industry corroboration of this academic claim.
- [[deployments/openai-symphony]] — Lopopolo's MCP-skepticism on token-economic grounds is the practitioner counterpart; DCI is the academic version. Symphony's praise of `gh` as a token-efficient agent-legible CLI exemplifies the same "interface resolution" principle.
- [[deployments/mcp-infrastructure]] — DCI extends the practitioner MCP-vs-CLIs framing already on this page with a third (academic, benchmarked) data point. The retrieval-API-as-MCP-style-mediation connection is implicit but real: a fixed-format top-k retriever interface is a special case of the abstracted-tool-surface critique.

### Adjacent threads

- [[patterns/sierra-context-engineering]] — Sierra's eight-block taxonomy treats Knowledge as a separately-retrieved block; DCI argues that for *agent-resident* corpora the right primitive may not be a Knowledge block at all but direct corpus access. Boundary: Knowledge-block-as-retrieval-injection makes more sense for cloud/SaaS knowledge bases than for local files.
- [[patterns/agentic-context-engineering]] — ACE's playbook-as-evolving-context approach is orthogonal but compatible: DCI handles retrieval, ACE handles accumulated tactical knowledge. Could compose.
- [[patterns/context-engineering]] — DCI reframes the `c_know` component of the C = {c_instr, c_know, c_tools, c_mem, c_state, c_query} formalism: knowledge is no longer a pre-retrieved injection but a tool-mediated direct-access primitive, blurring `c_know` into `c_tools`.
- [[patterns/effective-harnesses]] — Anthropic's harness emphasises initialiser agents and progress files as the persistence substrate; DCI complements with a corpus-access discipline. Both reject the abstracted-API-mediates-everything posture.
- [[patterns/harness-design-space]] — DCI is a new data point for the *tools* design dimension; the "raw bash + grep" stance is closest to the Lightweight harness pattern (21.4% of surveyed projects per that page) but applied to retrieval, not coding.
- [[patterns/topology-taxonomy]] — candidate ninth mitigation class for *long-horizon-context-loss*: high-resolution local retrieval reduces context burden by fetching evidence on demand.

### Memory cluster — load-bearing tensions

- [[memory/memory-architectures]] — DCI is a new addition to the *retrieval-augmented memory stores* family — but a *radical* one. It removes the index entirely and treats the raw corpus as the retrieval substrate. Should be flagged as a **no-index extreme** sub-family, or as a separate sixth family ("direct substrate access") — see [Conflict flags](#conflict-flags) below.
- [[memory/longmemeval]] — LongMemEval explicitly assumes the indexing → retrieval → reading framework. DCI collapses indexing+retrieval into a single tool-mediated traversal. Boundary: the framework assumes the indexing stage exists; DCI is an existence proof that for capable agents on small-to-medium corpora the assumption is wrong.
- [[memory/mempalace]] — MemPalace's verbatim discipline is doctrinally adjacent (preserve original substrate; don't lossy-compress). DCI takes verbatim further: *no extracted index at all*, search the original substrate directly. Verbatim-storage + DCI-access is a coherent pairing.
- [[memory/mem0]] — Mem0's extract-and-consolidate pipeline is the doctrinal opposite. Mem0 *moves* semantic understanding into the index ahead of time; DCI *moves* it into the agent's reasoning at retrieval time.

## Conflict flags

No current wiki page argues vector-RAG is the default, so DCI does not conflict head-on with an existing positive-vector-RAG position. The contradiction it crystallises is with **implicit assumptions**:

1. **Implicit-assumption tension with [[memory/memory-architectures]].** The survey enumerates *retrieval-augmented memory stores* as a family characterised by "non-parametric external index... live interaction records... queries it at inference time." DCI removes the index, contradicting the family-defining mechanism. Not a head-on benchmark-vs-benchmark conflict — DCI is evaluated on QA / IR / agentic search tasks, not the LongMemEval / LoCoMo / MemoryArena memory benchmarks the survey uses. Conceptual: does the *family* still cohere if a member can drop indexing entirely, or is DCI a separate family?

2. **Live tension with [[memory/mem0]] doctrine.** Mem0: 91% p95 latency reduction by selective retrieval. DCI counter: latency-and-cost favourable on BrowseComp-Plus too (29% cost reduction with Sonnet 4.6, +11 pp accuracy), so the latency-cost case for index-mediated extraction may be regime-dependent.

3. **Pressure on [[conflicts/verbatim-vs-extracted-memory]].** That conflict pages two positions (MemPalace verbatim vs Mem0 extract). DCI introduces a third position: *no separate index at all — search the raw substrate via terminal tools*. The reconciling-axes table needs an **"Index existence" axis** ranging from *no index* (DCI) → *fact-augmented keys + verbatim values* (LongMemEval-recommended hybrid) → *extracted-fact graph* (Mem0g).

4. **Tension with [[memory/longmemeval]]'s three-stage framework.** The benchmark explicitly positions long-term memory as decomposing into indexing → retrieval → reading. DCI collapses indexing+retrieval into one. The framework assumes the indexing stage exists; DCI is an existence proof that for capable agents on small-to-medium corpora the assumption is wrong.

5. **Pressure on [[patterns/sierra-context-engineering]]'s Knowledge block.** Not an active conflict — Sierra targets customer-support journeys with help-centre articles, where DCI's no-index argument is weaker (centralised, stable corpus). But the boundary is real.

## Caveats

- **Single-retriever comparison.** Compared retriever is Qwen3-Embedding-8B (single dense). Whether stronger retriever stacks (late-interaction ColBERTv2, hybrid sparse+dense+rerank, Qwen3-Reranker-4B + Qwen3-Embedding-8B + RRF) close the gap is untested. The localisation argument (DCI wins on within-document evidence isolation, not document recall) suggests the gap is more fundamental, but this remains untested.
- **Cost-per-question is roughly 2× retrieval baseline at the small end** (35 vs 18 tool calls/q on a 100-q subset; $0.10 vs $0.05/q for Lite). At larger scale the cost story flips (Sonnet 4.6 DCI is cheaper than retrieval). Gains come from accuracy not efficiency at the lite end.
- **Cross-vendor harness portability untested.** All DCI-Agent-CC results are with Claude Code + Sonnet 4.6. The Lite results (different harness, different model) suggest the result generalises, but no cross-vendor matched-corpus comparison.
- **Failure cases 5a/5b in the appendix** are flagged as DCI-Agent-CC and DCI-Agent-Lite failure modes on agentic search — likely the corpus-breadth ceiling and ambiguous-keyword regimes. Worth a deeper read for any follow-up `/research`.

## Open questions

- **Stronger retrievers.** Does the no-index advantage hold against late-interaction or hybrid rerank stacks?
- **Corpus scale ceiling.** 200K already costs +110% with −13.6 pp; 400K → 37.5%. Real corporate corpora are often 10M+. Hybrid (BM25 to narrow, then DCI within subset) is unexplored.
- **Lower-bound model capability.** GPT-5.4 nano works at lite scale; Sonnet 4.6 at full scale. Below GPT-5.4-nano-class? If DCI requires frontier-tier reasoning, it widens the haves/have-nots gap — vector-RAG is more democratic.
- **DCI under summarization pressure.** Runtime ablations are non-monotonic. Does DCI's localization advantage erode after compaction? Not tracked.
- **MCP server design implications.** If DCI is the right interface for capable agents on local/workspace corpora, should MCP servers expose `grep` / `find` primitives over their underlying data substrates rather than top-k retrieval APIs? The paper hints but does not engage.
- **In-memory lazy index hybrid.** The paper opposes "no index" to "offline-indexed top-k retrieval" but doesn't explore a middle: build a tiny inverted index lazily as the agent explores. Aider and Anthropic Code do something like this implicitly.

## Related-work bridge

The paper extends two adjacent threads:

- **Agentless / SWE-agent** — CLI primitives suffice for code localization.
- **Subramanian et al. 2026** ("Keyword search is all you need: achieving RAG-level performance without vector databases using agentic tool use," arXiv 2602.23368) — keyword search over raw PDFs approaches vector RAG for document QA.

DCI generalises both into "retrieval interface resolution" as a broader principle.

The **on-policy cohort** the paper cites — Anthropic Claude Cowork (2026), OpenAI's deep research, Steinberger's OpenClaw — explicitly positions DCI as the natural retrieval paradigm for the *workspace-resident agent* class that's now mainstream.

## Related

- [[case-studies/notion-token-town]] — direct convergence on MCP-vs-CLIs and "vector embeddings are less and less."
- [[deployments/openai-symphony]] — practitioner counterpart on token-economic grounds.
- [[deployments/mcp-infrastructure]] — third (academic) data point for the practitioner MCP-vs-CLIs framing.
- [[patterns/sierra-context-engineering]] — Knowledge-block boundary case.
- [[patterns/agentic-context-engineering]] — orthogonal and compatible; ACE handles tactical knowledge, DCI handles retrieval.
- [[patterns/context-engineering]] — reframes `c_know` ↔ `c_tools` boundary.
- [[patterns/effective-harnesses]] — both reject abstracted-API-mediates-everything.
- [[patterns/harness-design-space]] — Lightweight harness pattern data point.
- [[patterns/topology-taxonomy]] — candidate ninth mitigation class for long-horizon-context-loss.
- [[memory/memory-architectures]] — no-index extreme entry; assumption-boundary on indexing.
- [[memory/longmemeval]] — three-stage framework boundary.
- [[memory/mempalace]] — verbatim-storage doctrinal pair.
- [[memory/mem0]] — extract-and-consolidate doctrinal opposite.
- [[conflicts/verbatim-vs-extracted-memory]] — DCI as third pole + new "Index existence" reconciling axis.
- [[patterns/skillos]] — same week; SkillOS's "agentic search over experiential memory" future direction echoes DCI's no-index argument from a different angle.
