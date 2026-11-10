# Clear Human Web: Blind-Signed Personhood Tokens

Design paper (Porcelli, arXiv 2611.06286) for a gated "human-only" slice of the web. A person exchanges an EU Digital Identity Wallet (EUDI) PID at one issuer for a bounded batch of blind-signed Privacy Pass tokens; sites see only "a person vouches for this client", with at most k identities per person per site per epoch (epoch = issuer key lifetime). Tokens are unlinkable across sites and reveal no attributes. Motivated by the bot/AI-crawler flood (bots >53% of 2025 traffic; CAPTCHAs and robots.txt failed). Roadmap: A0 blind RSA tokens (deployable now) -> A1 one pseudonym per person -> A2 ZK proof of PID possession (needs a zero-attribute circuit; Longfellow not yet) -> A3 per-site pseudonym + Tor, k=1.

## Takeaways

- **Blind-signed personhood tokens.** Privacy Pass-style blind signatures separate the issuer (sees PID presentation and refill times) from the verifier (sees token only). Tokens say a person vouches for the client, not that a human is reading or wrote the content. Declared crawlers can be admitted by site choice.
- **Sybil resistance with bounded multiplicity.** k identities per site per epoch (P4). Identity rental/sale is priced, not prevented: renter can sell at most k identities per site per epoch. Cited evidence of the threat: Idena (23 entities ~40% of accounts), credential-fraud bounty marketplaces (median $25).
- **Residual leaks.** Issuer-site collusion narrows anonymity sets via refill timing; token names the issuer and so a Member State; network address leaks absent Tor; PID revocation lets the state stop refills.
- **Exit-pathway hook is weak.** Root of trust is state-issued PID (eIDAS 2.0, Reg. 2024/1183): EU-only, excludes non-PID holders (third-country residents, no smartphone), and concentrates gatekeeping power in issuers and states. It is infrastructure a collective could consume, not a parallel institution. Writing (comments, votes, reviews) needs per-site pseudonyms, which only arrive at A3. *(editorial)* Potential use as a sybil-resistance primitive for petitions, review platforms, data-donation panels and membership counts ([[algorithmic-collective-action]], [[data-cooperatives]], [[gesis-surf-data-donation]]); none of this is in the paper beyond a stated extension.
- **Code status.** No code released; design paper only. Relies on the EUDI reference wallet and Privacy Pass. Open problems: issuer-list governance, multiple wallet units per person, non-transferable/rate-limited tokens against rental, zero-attribute circuit.
- **Contrast with [[decentralized-agent-identity]].** That page covers credentialed agents (DID/VC); this excludes undeclared machines and vouches for persons. Both leave issuer governance as the load-bearing open question.

## Source

- `raw/research/weekly-2026-11-09/04-clear-human-web-blind-token.md` — Lorenzo Porcelli, *Clear Human Web: Where a Person Vouches for Every Client*, arXiv 2611.06286 (draft 22 May 2026, revised 31 Oct 2026).
  - Origin: independent researcher, preprint.
  - Audience: academic/standards community (EUDI wallet, Privacy Pass, IETF-style).
  - Purpose: define 5 properties and 7 adversaries and show which a deployable construction meets.
  - Trust tag: **medium** — unreviewed single-author preprint, theory/design only, no implementation; heavily cited to EU specs and measurement studies.

## Related

- [[decentralized-agent-identity]] — DID/VC agent identity; contrasting trust root and issuer-governance problem
- [[agent-interop-protocols]] — adjacent agent/web protocol layer (x401 comparison)
- [[agents-vs-ecommerce-opacity]] — site-side bot/agent exclusion
- [[browser-fingerprinting]] — the bot-detection signals this replaces with unlinkable tokens
- [[credential-disclosure-assistants]] — EUDI wallet oversharing; selective-disclosure parallel
- [[dignity-centric-stack]] — privacy-preserving identity layer parallel
- [[algorithmic-collective-action]] — sybil resistance as precondition for verified collective signals
- [[data-cooperatives]] — one-person-one-membership without identity disclosure
- [[gesis-surf-data-donation]] — verified-human data-donation panels
- [[regulatory-responses]] — eIDAS 2.0 / EUDI as regulatory substrate
- [[possible-strategic-levers]] — candidate infrastructure lever
