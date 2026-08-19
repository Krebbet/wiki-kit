# Conflict: Why Headcount Grows — Parkinson vs. Knowledge Hierarchies

**Status: OPEN — not adjudicated, and genuinely unresolved.** Parkinson, formalised and partly tested by Klimek, Hanel & Thurner, holds that administrative headcount grows on an internal clock: officials multiply subordinates rather than rivals, officials make work for one another, and the resulting growth rate is fully determined by promotion probability and subordinates-per-promotion — the model has no workload term. Garicano & Rossi-Hansberg hold that headcount and layer count are determined by output and by the cost of knowledge: an organisation adds people and levels because it is producing more and problem-routing must scale. The first predicts staff growth while workload falls; the second predicts staff growth *because* output rises. Each is evidenced only within its own domain, and the domains do not overlap: the Parkinson evidence is entirely public bureaus, the knowledge-hierarchy evidence entirely private firms.

## Position A — headcount growth is independent of workload

**Sources:** `raw/research/scale-effects/04-parkinson-law-original-essay.md` (Parkinson 1955, **partial capture — assertion only, no statistics**); `raw/research/scale-effects/05-parkinson-law-quantified-empirical.md` (Klimek, Hanel & Thurner 2008).
**Evidence tier:** Parkinson is (b)/assertion, and our capture is a ~500-word excerpt that stops before the statistics he promises. Klimek et al. are mixed: the two historical staff series are (a) empirical but are Parkinson's own 1957 figures restated at second hand, n=2; the growth model is (b) simulation with illustrative parameters, never fitted to a real staffing series.

- Stated claim: "the number of officials and the quantity of work to be done are not related to each other at all"; totals rise "whether the volume of work were to increase, diminish or even disappear."
- Mechanism: **Factor I**, an official wants to multiply subordinates, not rivals — two subordinates entrench him, one peer threatens him; **Factor II**, officials make work for each other, so each addition manufactures apparent demand for the next.
- Evidence: British Colonial Office staff 372 → 1661 between 1935 and 1954, ≈ +6%/yr, while the territories administered shrank dramatically. Royal Navy admiralty officials +80% between 1914 and 1928 while ships in commission fell from 62 to 20.
- Formalisation: total staff grows as e^(λt) with λ = (1 − γ + (r−1)p)(1 − q₋) — promotion probability p, subordinates per promotion r, attrition γ. **No workload or output variable appears in the model.**

## Position B — layers and headcount are set by output and knowledge cost

**Source:** `raw/research/scale-effects/08-garicano-rossi-hansberg-knowledge-hierarchies.md` (Garicano & Rossi-Hansberg 2014).
**Evidence tier:** (b) formal model, with (a) associational panel evidence — French administrative firm-worker data 2002–2007, 553,125 firm-year observations, firm fixed effects. The authors describe their empirics as failing to falsify the mechanism, not as establishing it, and call for causal evidence.

- Organisations exist to relax a time constraint on knowledge; layers route exceptional problems upward and span is bounded by the manager's helping-time constraint.
- Layer count is chosen by cost minimisation and is U-shaped in output: minimum efficient scale rises with layer count, so larger output rationally buys more layers.
- Empirically, firms with more layers are larger in value added and hours, and the probability of adding a layer rises with value added — layer transitions track output, not tenure or career structure.
- The reorganisation result gives the mechanism a fingerprint: adding a layer *lowers* the knowledge and wages of pre-existing layers; growing without adding one raises them.

## Where the disagreement actually is

Both positions explain a rising headcount. They disagree about **what the headcount is a function of**, and therefore about what should co-move with it:

| | Position A | Position B |
|---|---|---|
| Headcount is a function of | Promotion rate × subordinates per promotion | Output, given knowledge and communication cost |
| Prediction when workload falls | Staff keep growing | Staff and layers shrink |
| Prediction for wages at existing layers when a level is added | Not modelled | Fall |
| What bounds growth | Tuning p and r so λ ≤ 1 | The output level itself |

The Colonial Office and Navy series are, on their face, direct evidence against Position B's prediction — headcount rising as workload fell. They are also two British public bodies, a century old, reported at second hand, in a sector where "workload" is proxied by territories administered and ships in commission, neither of which is the administrative work actually generated. Decolonisation and demobilisation both plausibly *raise* administrative work while lowering the physical proxy. The authors do not address this; nor does any source in the batch.

## Why this stays open

**[wiki synthesis]** There is no overlap in evidence. Position A has been observed only in public bureaus with lump-sum funding and no market test of output. Position B has been observed only in private firms with priced output and a competitive labour market. Neither has been run on the other's cases, so the two accounts have never been given the chance to disagree on the same data. That is not a scope condition anyone has established — it is an absence of any test at all.

Three further reasons not to resolve it by preference:

1. Position A's quantitative core rests on n=2 restated historical cases plus a model with illustrative parameters; Position B's rests on one country's manufacturing panel with fixed effects but no identification.
2. Rajan & Wulf's firm panel tested the empire-building hypothesis (Position A's mechanism, in a firm) directly — regressing hierarchy depth on institutional shareholding and the Gompers-Ishii-Metrick governance index — and found no relationship, with depth also uncorrelated with market-to-book. That is a **null result against Position A inside firms**, which cuts against the easy generalisation but does not adjudicate the bureau case.
3. The mechanisms are not mutually exclusive. Nothing prevents career-driven multiplication and output-driven layering from operating in the same organisation; no source models both, so their relative magnitudes are unknown.

## What would settle it

1. **A workload-controlled staff panel for public bureaus.** Position A's whole claim is that headcount is workload-independent. It has never been tested with a workload measure that is not a physical proxy for the wrong thing. Casework volume, decisions issued, or applications processed against staff counts, across many agencies, would do it.
2. **Test Position B's reorganisation signature in a bureau** — layer added ⇒ pre-existing layers' pay and knowledge fall. It is sharp, it needs only personnel records, and it discriminates.
3. **Estimate λ's parameters from real staffing records.** Klimek et al. supply r, p and γ as measurable quantities and never measure them. If the observed promotion regime predicts observed growth, Position A gains what it currently lacks.
4. **A private-firm test of Factors I and II.** Parkinson claims nothing about firms; Rajan & Wulf's null is the only evidence either way in this batch, and it tests the governance-pressure corollary rather than the hiring incentive itself.

## Source

- `raw/research/scale-effects/04-parkinson-law-original-essay.md` — C. Northcote Parkinson, "Parkinson's Law", *The Economist*, November 1955. http://doc.cat-v.org/economics/parkinsons-law/ — **partial capture**, no statistics.
- `raw/research/scale-effects/05-parkinson-law-quantified-empirical.md` — Klimek, Hanel & Thurner, "Parkinson's Law Quantified", 2008. https://arxiv.org/pdf/0808.1684
- `raw/research/scale-effects/08-garicano-rossi-hansberg-knowledge-hierarchies.md` — Garicano & Rossi-Hansberg, NBER WP 20607, 2014. https://www.nber.org/system/files/working_papers/w20607/w20607.pdf
- `raw/research/scale-effects/06-rajan-wulf-flattening-firm.md` — Rajan & Wulf, NBER WP 9633, 2003 (cited for the null result on the empire-building hypothesis inside firms). https://www.nber.org/system/files/working_papers/w9633/w9633.pdf

## Related

- [[bureaucratic-growth-and-parkinsons-law]] — Position A in full, with the evidence graded piece by piece.
- [[knowledge-hierarchies-and-the-cost-of-scale]] — Position B in full, including the reorganisation signature.
- [[functional-vs-rent-seeking-growth]] — the adjacent open conflict, on structure and output rather than on headcount.
- [[governance-structures]] — carries Rajan & Wulf's span and depth findings, including the null result cited above.
- [[dimensions-of-institutional-variation]] — D35 (funding mechanism), D36 (span), D37 (depth) are the axes a discriminating test would need.
- [[open-questions]] — Q3 (public/private invariance) and Q7 (age vs. size vs. competitive pressure).
