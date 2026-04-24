# Strategies

The **editorial / design layer** of this wiki. Where the reference layer (`industries/`, `mechanisms/`, `organizations/`, `tools/`, `counter-power/`) documents what extraction patterns exist and what counter-power mechanisms have been deployed, this section documents **what to build** — strategic levers, development plans, implementation targets.

## How this section differs from the reference layer

| | Reference layer | Strategy layer (this section) |
|---|---|---|
| Claim sourcing | Every substantive claim cites a captured primary source | Claims cite reference-layer wiki pages; novel design claims marked *(editorial)* |
| Tone | Neutral, expert, source-traceable | Design-oriented, opinionated, prescriptive where useful |
| Filter on content | Sources must be authoritative and non-spam | Ideas must be plausible + connected to a documented extraction pattern |
| Output | Pages per concept / mechanism / industry / org | Pages per lever / plan / target |

Strategy-layer content is still subject to discipline — every lever here should be (a) mapped to a reference-layer anchor when one exists, and (b) explicitly tagged *(editorial)* when it goes beyond documented practice. The strategy layer is not a license to drift from evidence; it is a licence to synthesise across evidence into prescriptive design proposals.

## Contents

### Lever inventories

- **[[possible-strategic-levers]]** — the first page. Inventory of 29 strategic levers across 8 categories (aggregation, collective redirection, profile/algorithm manipulation, account arbitrage, disintermediation, information layer, economic-structural, regulatory-proxy). Summary table with research-needed flags and candidate tech solutions. Starting point for any development plan.

### Research readouts

- **[[lever-implementation-readout]]** — strengths / weaknesses / evidence assessment of the four highlights from the 2026-04-22 `lever-implementations` research run. Synthesis across 10 reference-layer pages (AdNauseam, Nightshade/Glaze, Privacy Badger, NOYB, AlgorithmWatch, auto-IRAs, etc.). Ends with a three-layer-strategy synthesis (obfuscation / advocacy / structural).
- **[[obfuscation-strategic-readout]]** — strategy-layer deep-dive on obfuscation as a consumer-action lever (2026-04-23). Directly answers "how to trick pricing algorithms into perceiving users favourably." Source-traceable strengths / weaknesses; technical-approach tiers (mature / formalised / speculative); countermeasure projections (off-the-shelf / deliberate / structural including DP-as-firm-counter from Solanki et al. 2025). Recalibrates the prior H1 readout and the possible-strategic-levers research-needed flags.
- **[[data-disruption-strategy-map]]** — strategy-layer matrix mapping *which data-disruption lever works against which seller-side pricing algorithm family*, with platform-enforcement-risk tiers for each lever (2026-04-23). Six algorithm families × six lever classes × six risk tiers. TL;DR: obfuscation is narrowly applicable (Families 1, 3, partially 6); coordinated behaviour + DSAR coordination are broader-applicability, lower-enforcement-risk levers that are currently under-leveraged. Recommended strategy portfolio with a Tier 1 / Tier 2 / Tier 3 split.

### Development plans

*Candidate plans sketched on [[possible-strategic-levers]]; not yet expanded into full plan documents:*

- **Plan A: Flash-redirection observatory for rental housing** — pending user selection for expansion.
- **Plan B: Buyer-side data cooperative for personalised e-commerce** — pending.
- **Plan C: Pricing-transparency-overlay extension** — pending.
- **Plan D: Consumer-side CCA-port research** — pending.

Each plan, when expanded, gets a page under `wiki/strategies/development-plans/` with: target extraction pattern it addresses; reference-layer mechanism anchor; milestone structure; known unknowns; open dependencies.

### Future sections (placeholder)

- **Implementation targets** — concrete build specs for plans that mature past scoping.
- **Opportunity ranking** — periodic editorial reviews that re-prioritise levers against reference-layer updates. The current implicit ranking sits in [[regulatory-responses|design-input candidates section]] + [[possible-strategic-levers]]; may warrant a dedicated page once plans mature.
- **Pattern library** — architectural primitives common across plans (e.g., redaction pipelines, membership platforms, observatory stacks) worth documenting once so plans can cite them instead of re-specifying.

## Working conventions for this section

- **One concept per page.** A lever is one page; a plan is one page; a pattern is one page. No omnibus documents.
- **Editorial tags required.** Any claim not traceable to a reference-layer page must be marked *(editorial)*, *(synthesis)*, or *(design proposal)*. No hidden drift.
- **Research-needed flags are first-class.** If a lever or plan requires research the reference layer hasn't captured, name it explicitly and check whether it belongs in `research-queue.md`.
- **Revisit cadence.** Strategy-layer content will rot faster than reference-layer content. On major reference-layer updates (new research runs, material lint fixes), re-read strategy pages and update or deprecate accordingly.

## Related

- [[index|Main wiki catalog]]
- [[regulatory-responses]] — reference-layer companion to the lever inventory
- [[dynamic-pricing-overview]] — problem-side reference
