# PGPO: relational-fidelity text obfuscation

Lin et al. (Zhejiang Univ. / XJTU; arXiv 2611.23236, preprint) propose PGPO, a GRPO-trained LLM that rewrites item side-information words so text embeddings resist Vec2Text inversion while preserving inter-item similarity structure ("relational fidelity") for recommenders. **Platform-side, not consumer-side**: it protects the data holder's item catalogue sent to third-party embedding APIs. Low direct consumer actionability.

## Mechanism

- Select high-influence "prototype" words by a similarity-influence score; build a static top-K neighbour graph.
- LLM explores obfuscated variants for prototypes (anchors); anchors propagate through the graph to the full vocabulary.
- Rewards: individual dissimilarity, structural consistency (Spearman of neighbour similarity), semantic-category constraint.

## Results (MovieLens-1M, Amazon-Book; simulated attacker)

- Spearman 0.198 / 0.181 vs baselines 0.03-0.16; recsys HR/NDCG roughly on par with raw text (e.g. SASRec HR@10 0.1133 vs 0.1129).
- Inversion defence comparable to baselines, not clearly stronger (F1 0.072 vs InferDPT 0.070; SanText+ 0.094). Headline is utility at equal defence.
- Limits stated: sensitivity-unaware budget allocation, LLM overhead, text-only; decentralised deployment is future work.

## Transferable idea

"Preserve relative topology while shifting absolute semantics" — a possible pattern for a [[mechanisms/data-cooperatives]] releasing pooled data to third parties. *(editorial)* Code reportedly at github.com/Shengxiang-Lin/PGPO (unverified).

## Source

- `raw/research/weekly-2026-11-23/04-pgpo-recsys-embedding-obfuscation.md` — https://arxiv.org/pdf/2611.23236 (academic preprint; trust medium; ingest summary skimmed appendices).

## Related

- [[mechanisms/obfuscation]] — same primitive, opposite beneficiary
- [[mechanisms/the-firms-view]]
- [[privacytrace-mcp-leakage]]
- [[mechanisms/unlearnable-trajectories]]
- [[mechanisms/acoda-code-obfuscation]]
- [[mechanisms/federated-learning]]
