# From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms

arXiv survey (2605.06716, Hong Kong Baptist University + partners) that proposes a three-stage evolutionary framework — Storage → Reflection → Experience — as a unified lens on LLM agent memory research, arguing the field has fragmented between OS-engineering and cognitive-science paradigms and needs a trajectory-abstraction framing to reach continual learning. The taxonomy and its formal Table 1 distinctions are the primary contribution; no novel empirical results are presented.

## Storage → Reflection → Experience axis

The survey's central claim is that memory mechanisms evolve along a **cognitive-depth axis** distinct from the mechanism-family taxonomy in [[memory/memory-architectures]]:

| Stage | Formal definition | Representative systems |
|---|---|---|
| **Storage** | Raw trajectory fidelity; retrieval scores against original context | MemGPT (Structured), Generative Agents (Vector), Mem0 (Storage→Reflection boundary) |
| **Reflection** | Intra-trajectory transformation F_ref(τ_i \| φ) = m'_i; output still tied to original task context | Reflexion (Introspection), CLIN, AgentFold |
| **Experience** | Cross-trajectory induction F_exp(T_batch) = K; output is a policy prior applicable to unseen scenarios without trajectory-level matching | SkillOS-style skill libraries, FLEX, MemSkill |

The key Table 1 distinction: Reflection output is semantically similar to its source trajectory; Experience output is a policy prior that transfers to *unseen* scenarios without trajectory matching. This is why the two stages are distinct, not merely degrees of the same thing.

### Storage sub-taxonomy

Linear (FIFO token stream / attention extension) → Vector (semantic + temporal-decay retrieval) → Structured (relational DB, hierarchical tiering, graph). **Generative Agents** (Park et al.) is the canonical Vector storage system with its recency × importance × relevance scoring formula. **MemGPT / Letta** occupies the Structured tier (hierarchical main/external context with function-call paging). **Mem0** is not explicitly placed but fits the Structured tier or the Storage→Reflection boundary (extract + consolidate with ADD/UPDATE/DELETE/NOOP conflict resolution).

### Reflection sub-taxonomy

Introspection (autonomous self-critic, no external signal) → Environment (real-world outcome anchors) → Coordination (multi-agent consensus). **Reflexion** (Shinn et al.) is the primary Introspection exemplar — verbal RL with failure feedback written into an episodic buffer. The survey notes this places Reflexion at the intra-trajectory level: it refines a single trajectory's errors but does not abstract across trajectories into transferable policy priors.

### Experience sub-taxonomy

Explicit (natural-language policies, executable entities, skill libraries) → Implicit (fine-tuning into model weights) → Hybrid (explicit cache + periodic parameter internalization). **SkillOS** ([[patterns/skillos]]) maps cleanly to Explicit Experience. The distinction from Reflection: Experience outputs (skills, policies) can be retrieved for *semantically dissimilar* future tasks; Reflection outputs are retrieved when the current task resembles the source task.

## Relationship to [[memory/memory-architectures]]

The storage sub-taxonomy (Linear / Vector / Structured) is a more detailed decomposition of the same mechanism-family space. The Reflection stage maps onto the write–manage–read survey's "reflective and self-improving memory" and "policy-learned management" families. The **Experience stage is a new tier above what memory-architectures covers** — the five families in that survey top out at Reflection-equivalent; cross-trajectory policy abstraction and skill libraries represent a frontier those families do not yet address.

The two surveys are complementary rather than competing: [[memory/memory-architectures]] catalogues mechanism families and the write–manage–read loop; this survey frames the *evolutionary direction* from raw storage toward continual learning.

## Three evolutionary drivers

1. **Long-range consistency** — state coherence and goal tracking across sessions.
2. **Dynamic environments** — temporal validity of knowledge and causal structure (maps directly onto [[memory/longmemeval]]'s knowledge-updates axis, the hardest of LongMemEval's five abilities).
3. **Continual learning** — storage scaling constraints and the need for abstraction as corpora grow.

## Unrestricted memory expansion — a noted tension

The survey cites Xiong et al. 2025 and Srivastava and He 2025 in claiming that "the unrestricted expansion of memory is detrimental to the performance of LLM agents, as errors propagate within the system and contaminate the efficacy of learning" (§3.3). This is a collect-but-confirm claim: the cited papers are not independently verified in this wiki. It stands in mild tension with the verbatim/never-summarize discipline in [[memory/mempalace]], which holds that expansion is preferable to lossy compression. See [[conflicts/verbatim-vs-extracted-memory]] for the broader conflict; GroupMemBench's BM25 result ([[memory/groupmembench]]) provides independent evidence for the verbatim/raw-text-first pole.

## Framing axis for the verbatim-vs-extracted conflict

The survey adds an **abstraction-depth** axis to the existing conflict: Storage = verbatim-fidelity pole; Experience = full-abstraction pole; Reflection = middle ground. [[memory/longmemeval]]'s hybrid recommendation (verbatim values + extracted-fact keys) sits at the Storage/Reflection boundary. The survey does not resolve the conflict but locates each position on the evolutionary axis. See [[conflicts/verbatim-vs-extracted-memory]].

## Survey provenance and reproducibility

Living GitHub survey repository accompanies the paper — a positive reproducibility signal for an arXiv preprint. No unified quantitative benchmark across stages exists yet; the Experience stage only emerged as a coherent research direction in late 2025 (recency bias acknowledged by authors). Treat any cited numbers from third-party systems as collect-but-confirm.

## Source

`raw/research/weekly-2026-05-18/03-agent-memory-evolution-survey.md`

## Related

- [[memory/memory-architectures]] — mechanism-family survey; this page's evolutionary axis is orthogonal and extends above it.
- [[memory/groupmembench]] — multi-party benchmark; BM25 result corroborates the Storage/verbatim pole empirically.
- [[conflicts/verbatim-vs-extracted-memory]] — open conflict; this survey adds an abstraction-depth framing axis.
- [[reflexion]] — classified here as Reflection/Introspection exemplar (intra-trajectory, not cross-trajectory).
- [[memory/memgpt]] — placed in Structured Storage tier.
- [[memory/generative-agents]] — placed in Vector Storage tier (canonical recency × importance × relevance scorer).
- [[memory/mem0]] — sits at Storage→Reflection boundary.
- [[memory/longmemeval]] — knowledge-updates axis is the dynamic-environment driver's benchmark instantiation.
- [[patterns/skillos]] — maps to Explicit Experience (skill library with induction/reuse/refinement lifecycle).
- [[patterns/externalization-survey]] — complementary vocabulary (where memory lives vs how it evolves).
