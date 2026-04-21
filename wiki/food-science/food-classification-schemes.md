# Food Classification Schemes

Reference page summarising the **IUFoST formulation-and-processing** classification scheme and its critique of **NOVA**. Peripheral to the main formulation-optimisation workflow, but relevant when regulatory framing, nutrient profiling, or public-health arguments enter the conversation.

**NOVA** is a widely cited classification system that groups foods into four categories by processing level (unprocessed → ultra-processed). NOVA is frequently used in nutrition epidemiology to argue that "ultra-processed" foods drive adverse health outcomes.

**IUFoST** (International Union of Food Science and Technology) published a 2025 paper (npj Science of Food) arguing NOVA has a fatal definitional ambiguity: it *conflates formulation with processing*. NOVA's categories appear to scale with processing intensity but actually sort foods by *ingredient composition* — sugar, salt, fats, additives — not by quantified processing impact. The IUFoST scheme proposes two independent, measurable axes:

- **Formulation (F)** — captured by the Nutrient Rich Food index (e.g. NRF9.3: nine beneficial nutrients minus three to limit), computed on ingredient composition per 100 kcal.
- **Processing (P)** — captured by **ΔNRF9.3**: the change in the formulation's NRF9.3 score *before and after* processing. Positive ΔNRF means processing improved nutritional value; negative means it degraded it.

These combine into the **FPFIN** (Formulation & Processing Food Index) and are plotted on a 2D Classification Matrix Diagram with iso-FPFIN contour lines.

Positions the IUFoST paper takes that are likely to be contested:

- Approved additives in "ultra-processed" foods are Codex-reviewed and their health risk is unproven; treating them as intrinsically harmful is unjustified.
- Existing nutrient-profiling indices already capture NOVA's health signal; the "ultra-processing" label adds little once nutrient density, energy density, and matrix are accounted for.
- Processed foods are essential in contexts where nearly a billion people fail to meet nutritional needs — NOVA's framing risks vilifying a necessary technology.

Evidence for NOVA's fragility in practice: Braesco et al. (2022) had French food and nutrition specialists assign foods to NOVA groups with full ingredient lists; Fleiss' κ showed **low inter-rater reliability**. If experts with the same information can't agree, the scheme is not reproducible.

This wiki uses the IUFoST formulation/processing separation as working vocabulary — see [[bioavailability-and-matrix-effects]] for the S-Pro² principle the paper relies on — but does not yet take a position on the NOVA debate. If this turns out to matter for a specific formulation decision (for example, when a customer brief specifies "minimally processed"), a `conflicts/nova-vs-iufost.md` page should record a ruling.

## Source

- `raw/research/formulation-landscape/03-iufost-formulation-classification.md` — the primary source for everything above

## Related

- [[bioavailability-and-matrix-effects]]
- [[open-gaps]]
- [[field-overview]]
