# Rheology and Texture

Reference page defining the physical properties that predictive models most often target in food formulation, and the relationship between objective measurement and subjective perception.

**Rheology** is the study of how materials deform and flow under applied stress. In food, the core measured quantities are stiffness *E*, viscosity *η*, yield stress *Y*, storage modulus *G'* (elastic response), loss modulus *G"* (viscous response), and the phase angle *δ* relating them. A solid-dominant food has *G'* > *G"*; a fluid-dominant food has the opposite. Viscoelastic foods (gels, doughs, emulsions) fall between, and their ratios shift with concentration, temperature, shear rate, pH, and ionic strength.

**Texture** has two distinct meanings that the literature often conflates:

- **Physical texture** — objective, instrumented. The standard assay is **texture profile analysis (TPA)**: a double-compression test on a small sample, yielding hardness, cohesiveness, springiness, resilience, chewiness, and adhesiveness.
- **Sensory texture** — subjective human perception (soft, chewy, gummy, meaty, fibrous, springy, sticky, brittle, viscous). Culturally variable.

The physical-to-sensory translation is imperfect and is one of the field's open problems. Kuhl frames TPA outputs as "proxies" for sensory experience — good enough for optimization, insufficient for full preference modeling.

**Processing changes rheology by altering structure.** Illustrative example from the Wageningen thesis: **hot break** tomato paste (pectolytic enzymes inactivated at 90–95°C) yields higher viscosity and less **syneresis** (liquid separation from a gel) than **cold break** (70°C, enzymes active). The mechanism is that intact pectin chains give stronger gel networks.

Models that predict rheology from composition (plant protein–polysaccharide blends with Random Forests; physics-informed neural networks; constitutive neural networks) perform reasonably within a narrow training matrix but generalize poorly across product categories. See [[predictive-models]] for detail.

## Source

- `raw/research/formulation-landscape/02-wageningen-systematic-npd.md` — hot/cold break mechanism, syneresis
- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — rheology models for substitution
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — constitutive neural networks, PINNs, TPA integration
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — rheology quantities (E, η, Y, G', G", δ), TPA definitions, sensory-vs-physical distinction

## Related

- [[predictive-models]]
- [[ingredient-functionality]]
- [[ingredient-substitution]]
- [[candidate-generation]]
