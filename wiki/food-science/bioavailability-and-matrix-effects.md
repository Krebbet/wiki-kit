# Bioavailability and Matrix Effects

Reference page defining the food-science concepts that tie a formulation's *composition* to what the body actually absorbs — the gap between nutrient label and biological effect.

**Bioavailability** is the fraction of a nutrient (or bioactive compound) released during digestion and absorbed into the bloodstream. It is not a property of the ingredient in isolation — it depends on how the ingredient is embedded in the surrounding food and how that structure behaves during digestion.

**Digestibility** is the related upstream property: how readily the digestive system breaks the food down in the first place. Processing can enhance digestibility (partial protein denaturation exposes cleavage sites) or hinder it (tight starch–protein complexes resist amylase).

**Food matrix** is the collective term for the physical structure embedding the nutrients — the water content, rheology, gelling behaviour, particle size, and interfacial architecture. Matrix effects mean that the *same* nutrient in two different foods can absorb at very different rates. IUFoST's 2025 classification paper formalises this with the **Process–Structure–Property (S-Pro²)** principle: *process makes structure, and structure encodes properties*.

Concrete mechanisms illustrated across the corpus:

- **Lycopene** (carotenoid in tomatoes) — processing disrupts the plant cell matrix and releases lycopene, *increasing* bioavailability; the same heat exposure can drive trans-to-cis isomerisation and oxidative loss. Processed tomato products (paste, sauce) are generally higher in bioavailable lycopene than fresh tomato.
- **Glucosinolates** (bioactives in Brassica vegetables) — coexist with myrosinase enzyme but physically separated in intact plants. Cell damage brings them into contact, triggering hydrolysis. Volatile breakdown products are lost if the reaction runs early in the supply chain, so intact glucosinolates at the point of consumption are preferred.
- **Heme vs. non-heme iron** — animal-source (heme) iron is absorbed more efficiently than plant-source (non-heme) iron. Phytate-rich plant foods further inhibit non-heme uptake.
- **Fat-soluble vitamins** — their uptake depends on the lipid phase's digestion kinetics, which in turn depends on the emulsion microstructure. Swapping animal fat for plant oil can shift vitamin bioavailability even when the fat quantity is matched.

**Antinutrients** — phytic acid (phytate), tannins, lectins — bind minerals and proteins, reducing uptake. Most can be inactivated by soaking, fermentation, or thermal processing; matching these routes is part of a responsible substitution.

The practical takeaway for candidate generation: predictive models that only optimise over the nutrient label leave bioavailability effects unmodelled, and the AI-ingredient-substitution review (Oz et al.) explicitly flags micronutrient bioavailability tools as "underdeveloped." See [[predictive-models]] and [[open-gaps]].

## Source

- `raw/research/formulation-landscape/02-wageningen-systematic-npd.md` — lycopene, glucosinolate mechanisms; bioavailability definition in functional-food context
- `raw/research/formulation-landscape/03-iufost-formulation-classification.md` — S-Pro² principle; bioavailability/digestibility as classification axes
- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — heme vs non-heme iron, fat-soluble vitamin matrix dependence, antinutritional factors, bioavailability modelling gap

## Related

- [[ingredient-functionality]]
- [[food-classification-schemes]]
- [[predictive-models]]
- [[ingredient-substitution]]
- [[open-gaps]]
