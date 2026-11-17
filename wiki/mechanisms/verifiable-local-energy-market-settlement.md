# Verifiable Settlement for Local Energy Markets (Fabi and Leloup 2026)

Fabi and Leloup (arXiv 2611.16495, preprint) propose a hybrid architecture for community electricity markets: a community operator runs an automated market maker (AMM) that prices local trades every 15 minutes, while a permissioned Hyperledger Besu chain (QBFT consensus) records commitments and settles daily. Zero-knowledge proofs (Poseidon2 commitments, UltraHonk proofs from Noir circuits) let members check that the operator's settlement was computed correctly without seeing other households' meter data. The operator is kept, not removed; the design makes its financial calculations auditable. Evidence is a simulated 10-household experiment, not a field deployment.

## Mechanism

- **Surplus source.** Under net billing, the spread between retail tariff (which carries network costs, taxes, margins) and feed-in tariff is what a local market can capture by matching neighbours' supply and demand.
- **Pricing.** Fixed-in-advance AMM rule in smart contracts; price depends only on aggregate min(supply, demand) and tariff band, so individual positions need not be disclosed.
- **Verification.** Households commit to meter readings; proofs show the daily settlement follows the fixed rule from those commitments. Signed receipts per member.
- **Recourse and governance.** Member-triggered on-chain recourse, 12-hour dispute window, atomic settlement (no partial transfers), member fund recovery if the operator goes inactive, community-chosen validators. ERC-20 settlement token without issuance.

## Reported results (simulated, illustrative)

- 10 households, NREL ResStock load profiles, assumed tariffs.
- 34.4% of demand matched locally; 30.5% grid-only cost reduction; 83-88% of planner (optimal) surplus.
- About 19M gas/day on-chain; about 2.4 s proof time for 8 members.

## Takeaways

- **Auditable intermediary, not decentralisation.** Counter-power via verifiability of a coordinator that controls both position data and payment calculation (PMO in France, community-solar administrator, aggregator). Assumes a trusted-but-auditable operator.
- **Transferable pattern** *(editorial)*: fixed pricing rule + public verifiable settlement + signed receipts + recourse could apply to other collective-purchasing or data-pooling schemes where a coordinator handles money.
- **Aggregate-only disclosure** parallels privacy-preserving aggregation in [[federated-learning]].
- **Limits.** Permissioned chain (validator choice is the trust root); aggregates can still leak in small communities; operator still needs metering data access; simulation only; earlier P2P energy ventures failed on coordination cost and regulatory friction, which this does not address. No code or data release found in the sampled text.

## Source

- `raw/research/weekly-2026-11-16/05-verifiable-local-energy-market-settlement.md` — Fabi and Leloup (Telecom Paris/CREST, ENSAE Paris), *Verifiable Settlement and Pricing for Local Energy Markets: Architecture and Deployment on Hyperledger Besu*, arXiv 2611.16495. Origin: academic preprint. Audience: energy-market designers, applied cryptography researchers. Purpose: show operator settlement can be independently verified while household data stays private. Trust: preprint, not peer reviewed; simulated results, treat numbers as illustrative. Capture URL: https://arxiv.org/pdf/2611.16495

## Related

- [[community-choice-aggregation]] — collective energy buying vehicle; this adds a verifiable settlement layer
- [[transparency-tools]] — auditability of an intermediary
- [[data-cooperatives]] — community operator holding member data under governance
- [[platform-cooperatives]] — member-governed coordinator
- [[consumer-collective-bargaining]]
- [[federated-learning]]
- [[dynamic-pricing-overview]] — tariff structure and 15-minute pricing
