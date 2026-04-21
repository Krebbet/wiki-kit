# Ingredient Functionality

Reference page defining the technological roles ingredients play in a formulation — the "functions" that substitutes must match, not just the ingredient's chemical identity.

**Functional properties** are what an ingredient *does* in a food system: how it binds water, stabilises emulsions, forms gels, contributes to viscosity, entraps gas, or creates texture. The same molecule can have different functionality depending on its processing history, the food matrix, pH, ionic strength, and temperature — so functionality is always *context-dependent*.

The common functional roles referenced across the corpus:

- **Gluten** — a disulfide-linked protein network from wheat that traps gas and converts mesoscopic structures into fibrous, viscoelastic textures under extrusion or shear. Its replacement without hydrocolloids causes reduced loaf volume and poor texture in baked goods.
- **Casein micelles** — the abundant milk protein assemblies that stabilise dairy emulsions and form gels (cheese, yogurt). The literature (Oz et al., arXiv 2509) is emphatic that **no single plant protein offers equivalent multifunctionality** — casein replacement is currently the hardest problem in dairy analogue design.
- **Hydrocolloids** — water-binding polysaccharides (pectins, alginates, carrageenans, konjac glucomannan, xanthan) used as viscosity modifiers, gelling agents, and stabilisers. Often combined with plant proteins to cover what the protein alone cannot do.
- **Emulsifiers** — amphipathic molecules (phospholipids, mono/diglycerides, saponins) that stabilise oil-in-water or water-in-oil interfaces. Example: glycyrrhizin identified as a natural emulsifier via QSAR screening.
- **Oleosomes** — naturally occurring plant emulsion structures (seed oil droplets surrounded by oleosin proteins) that are increasingly used as animal-fat substitutes because they carry intrinsic interfacial stability.
- **Fibres** — structural polysaccharides that modulate viscosity, emulsion stability, and lubrication; a common route to mimic the mouthfeel of animal fat.

**Protein fractionation modes** shape functionality directly. **Wet fractionation** yields purer isolates at the cost of denaturation (losing native functionality). **Dry fractionation** preserves native protein structure but keeps functional-enriched *fractions* rather than isolates — trading purity for cost and native behaviour.

**Antinutritional factors** such as phytates and tannins bind minerals and proteins, reducing bioavailability; processing (thermal, mechanical, enzymatic) can inactivate them. See [[bioavailability-and-matrix-effects]].

The implication for candidate generation: an ingredient-substitution problem is a function-matching problem, not a composition-matching problem. See [[ingredient-substitution]] and [[ingredient-data-structures]].

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — gluten, casein multifunctionality claim, hydrocolloid roles, antinutritional factors
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — oleosomes, wet vs dry fractionation, glycyrrhizin QSAR, high-moisture extrusion
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — nine ingredient-role taxonomy

## Related

- [[rheology-and-texture]]
- [[bioavailability-and-matrix-effects]]
- [[ingredient-substitution]]
- [[ingredient-data-structures]]
- [[predictive-models]]
