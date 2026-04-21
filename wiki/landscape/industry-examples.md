# Industry Examples

Companies, platforms, and deployed systems named across the corpus. Useful as a reference when the literature references them in method descriptions, and as a competitive / comparative landscape for the expanded method.

## NotCo

Chilean-US food-tech company. The most-cited AI-driven formulation company in the corpus.

- **Giuseppe** — proprietary AI platform analysing molecular structure of animal-origin reference products and proposing plant-based analogues. Stated approach: latent-space embedding of ingredients, conditional generation against a reference product, iterative expert sensory feedback.
- **Generative Aroma Transformer** — natural-language-conditioned flavour-molecule generation (example input: *"cherry, candy, vanilla"*).
- **Products** — NotMilk (discovered combination: pineapple juice + cabbage juice + pea protein); NotChicken (tomato-strawberry pairing cited).
- **Partnerships** — Kraft Heinz (reported).
- **Patents** — described as embedding ingredients in latent spaces, conditioning on target profiles, iteratively incorporating sensory feedback.

## Brightseed

US biotech company focused on bioactive-compound discovery.

- **Forager** — proprietary AI platform that analyses ~700,000 phytochemicals for bioactivity prediction.
- **Discoveries** — N-trans-caffeoyltyramine and N-trans-feruloyltyramine (bioactives identified from the search), leading to the Brightseed Bio Gut Fiber product.
- Illustrates an inverse-design-adjacent pattern: target bioactivity → candidate compounds → source ingredients.

## Climax Foods

Plant-based cheese, AI-aided ingredient mining and formulation. Named in Oz et al. and the consortium paper.

## Perfect Day

Precision-fermentation dairy (makes dairy proteins without cows). Cited alongside Climax Foods as examples of AI-informed alternative-dairy companies.

## Meati

Plant-based whole-cut "meat" products based on mycoprotein. Cited in the consortium paper as a scale-up example.

## Live Green Co

Chilean plant-based ingredient company.

- **Charaka** — knowledge integration platform combining traditional / ancestral plant knowledge with computational methods; claimed categorisation of >15,000 plants.
- Notable product: plant-only ice cream formulation discovered via the platform (bananas, avocados, sunflower seeds).
- Uses precision fermentation for ingredient synthesis.

## Plant Jammer

Formulation platform exemplifying constraint-aware design.

- Lets food manufacturers set hard constraints (Halal-certified texturisers required, allergens excluded, carbon footprint capped) as first-class inputs.
- Illustrates the pattern of ontology / rule-based filtering layered on top of AI-based proposal.

## Ajinomatrix

AI platform correlating chemical composition with sensory perception (taste, smell, aroma). Named in Kuhl's Perspective as a platform "bridging the gap between chemistry and human sensory perception."

## Foodpairing + Knorr (Unilever)

- **Foodpairing** — proprietary AI platform discovering complementary ingredient pairings based on flavour profiles.
- Used by **Knorr (Unilever)** to support its target of 50% plant-based portfolio (by 2025).

## PIPA and the Digital Extruder

- **PIPA** (Predictive Intelligence for Protein Analytics) — cited by Zhou et al. as a tool that simulates thousands of formulations under extrusion virtually before physical testing.
- Context: Rivalz (snack-development company) reportedly used PIPA to test thousands of formulations virtually.
- Validation data not published; illustrates the simulation-first formulation pattern.

## FoodProX

Machine-learning classifier predicting degree of processing on a 0–1 scale from nutritional features. Referenced by Kuhl. Illustrates a reformulation direction: classify a product's processing level, then reformulate to reduce it while preserving the target property profile.

## ChefFusion

Foundation-model-style system trained on >1 million recipes and 900,000 images. Translates between recipes and food images. Early-stage / academic; cited by Kuhl as a demonstration of multimodal food-AI potential.

## Agentic AI systems (food-adjacent)

Not food companies, but named in the consortium paper as general-science agentic systems whose patterns apply to food discovery:

- **ProtAgents** — multi-agent LLM collaboration for protein design, combining physics and ML.
- **Sparks** — multi-agent AI for discovering protein design principles.
- **BioDiscoveryAgent** — autonomous genetic-perturbation experiment design.
- **Virtual Lab** — autonomous SARS-CoV-2 nanobody design.

## Academic and institutional

- **AIFS (AI Institute for Next Generation Food Systems)** — UC Davis / USDA-NSF, hosting the symposium behind Zhou et al.'s paper.
- **Wageningen University** — longstanding food-product-development research programme; Benner's CIM thesis is the method baseline.
- **Periodic Table of Food Initiative (PTFI)** — emerging global initiative for molecular-resolution food databases. See [[datasets-and-databases]].

## Takeaway

The deployed-system landscape is dominated by a handful of AI-native alt-protein / alt-dairy companies (NotCo, Climax, Perfect Day, Meati, Live Green Co), a discovery-platform tier (Brightseed, Foodpairing, Ajinomatrix, PIPA), and research-stage academic / multi-agent demonstrations. Classical food manufacturers (Unilever/Knorr) are partnering with the AI-native companies rather than building from scratch. No public-domain general-purpose formulation platform exists; the expanded method the user is designing sits in that gap.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — NotCo Giuseppe, Plant Jammer, Climax, Perfect Day
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — NotCo patent detail, Climax, Meati, Eat Just, ProtAgents, Sparks, Virtual Lab, BioDiscoveryAgent
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — PIPA / Digital Extruder, AIFS, Bühler, Blentech, Dragonfly SCI, The U&I Group
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — NotCo, Brightseed, Ajinomatrix, Knorr/Foodpairing, Live Green Co (Charaka), FoodProX, ChefFusion

## Related

- [[field-overview]]
- [[ingredient-substitution]]
- [[candidate-generation]]
- [[genai-leverage-points]]
- [[inverse-design]]
- [[datasets-and-databases]]
