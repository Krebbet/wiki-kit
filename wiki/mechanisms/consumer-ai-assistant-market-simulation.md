# Consumer AI Assistants in a Market Simulation (Huang & Xiao 2026)

Single-paper mechanism page. Huang & Xiao (arXiv 2610.05823, submitted 5 Oct 2026, cs.MA) simulate a rental market with six adaptive LLM-agent sellers guided by an algorithmic pricing tool and find that consumer-side AI assistants cut adopters' spending, but seller adaptation claws back roughly a third of the gain, while unassisted consumers are not measurably harmed. **Abstract-only capture: no methods, tables or robustness checks were available; full-text re-capture pending (see watchlist).**

## What the abstract reports

- **Setting:** renter-day pricing; contract pairs a fee that only physical action avoids with a pre-selected add-on that an authorised assistant can cancel online (drip-fee / dark-pattern structure).
- **Assistant mandates:** advisory vs executing; executing mandates deliver the gains.
- **Adopter savings:** 13.7 USD per renter-day with frozen sellers, 8.7 once sellers adapt (lower bills plus more rentals completed). Retention is roughly two thirds.
- **Seller adaptation:** sellers raise headline rates while cutting fees; swapping seller models and handing fee-setting to the pricing tool shows fee conduct and the split of gains are seller-determined.
- **Unassisted consumers:** a calibrated behavioural forecast of a +3.6 burden did not transfer; observed mean spending change +0.4 (CI -0.6 to +1.3).
- **Framing:** assistants should be evaluated at market level (completion, total spend, non-users), not per-user.

## Origin / audience / purpose / trust

Academic arXiv preprint, not peer-reviewed; written for multi-agent-systems and economics researchers to document a result and argue for market-level evaluation. Trust: medium-low (simulation, preprint, abstract only).

## Tensions with existing wiki positions

- The "negative externality on non-adopters" framing is not supported in this simulation; surface, do not adopt.
- Complicates the universal buyer disadvantage in bilateral LLM negotiation ([[agent-mediated-negotiation-empirics]]): different setting (market with executing mandates vs bilateral negotiation), likely complementary.

## Design inputs *(editorial)*

- Evaluate assistants and collective tools at market level.
- The cancel-online vs physical-action fee asymmetry is a concrete target for agent tooling (cf. [[tools/dpagent-dark-pattern-repair]]).
- Individual gains erode under seller adaptation, which supports the case for collective or structural levers ([[consumer-collective-bargaining]]). The 13.7 to 8.7 retention is a usable benchmark with a simulation caveat.

## Source

- `raw/research/weekly-2026-10-12/01-personal-ai-assistants-gains.md`
  - **Origin:** arXiv abstract page (2610.05823).
  - **Audience:** MAS / AI / econ researchers.
  - **Purpose:** document a simulation result.
  - **Trust:** medium-low; abstract only.

## Related

- [[agent-mediated-negotiation-empirics]]
- [[pricing-algorithm-taxonomy]]
- [[algorithmic-collusion]]
- [[ghost-tool-calls]]
- [[credential-disclosure-assistants]]
- [[tools/dpagent-dark-pattern-repair]]
- [[consumer-collective-bargaining]]
- [[possible-strategic-levers]]
