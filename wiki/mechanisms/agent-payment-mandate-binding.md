# Agent payment mandate binding (authority gap)

You, Joshi, Kuehlkamp & Nabrzyski (arXiv 2611.25821, preprint) show that stablecoin payments by AI agents (x402, AP2) enforce on-chain only the fields the wallet signs, so most deployed redemptions are bearer-redeemable by any signature holder (98.7% of 26,653 sampled Base USDC authorizations). They propose MANDATELOCK, a recipient contract that binds mandate terms. Companion paper: arXiv 2611.24989 ("Signed, Valid, and Unauthorized"; not captured).

## Findings

- 31,800 trials on deployed bytecode across 12 configurations; 9 constraint classes; game-based proof.
- Intermediaries (facilitators, agent runtimes, merchants) hold the user's signed authority; Coinbase submits 92.5% of x402-attributed events. Gap lets them preempt, delay or misattribute payments; funds cannot be diverted when payee and amount are bound.
- Order substitution comes from x402's random nonce, not EIP-3009 itself; 40.1% of 20-second slices had same-terms overlapping authorizations.
- Fix: commit mandate terms in the nonce, payee-bound `receiveWithAuthorization`, recipient contract checks facilitator/window/order. +25% gas (~$0.00018 per settlement, 16% of the $0.0055 median payment). Visibility trade-off: wallet shows the lock contract, not the merchant (MetaMask 13.33.0).

## Caveats

Preprint; same authors wrote derivation, attacks and oracle (self-flagged circularity); exposure measured, not observed harm; EOA payers, exact-amount single payments only. No public repo seen in the captured portion (read truncated).

## Design input

Treat the wallet signature as the enforcement boundary; relevant to any cooperative buying agent or group-buy escrow with delegated payment. *(editorial)* Adds a payment-authorization layer the wiki's agent pages lack.

## Source

- `raw/research/weekly-2026-11-23/05-agent-commerce-mandate-authority-gap.md` — https://arxiv.org/pdf/2611.25821 (academic preprint; trust medium-high).

## Related

- [[mechanisms/agents-vs-ecommerce-opacity]]
- [[mechanisms/artificial-shoppers-attention-competition]]
- [[mechanisms/accuracy-not-welfare-ai-buyers]]
- [[mechanisms/consumer-ai-assistant-market-simulation]]
- [[mechanisms/agent-mediated-negotiation-empirics]]
- [[mechanisms/agent-interop-protocols]]
- [[mechanisms/decentralized-agent-identity]]
- [[mechanisms/verifiable-local-energy-market-settlement]]
- [[mechanisms/consumer-collective-bargaining]]
