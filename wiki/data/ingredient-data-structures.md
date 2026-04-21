# Ingredient Data Structures

How the AI-ingredient-substitution literature actually *represents* ingredients for search and scoring. Key reference for designing the ingredient layer of the expanded candidate-generation method.

## Graph as the dominant representation

Across the corpus, the dominant representation is a **heterogeneous graph**:

- **Nodes** — ingredients, enriched with metadata (composition, flavour descriptors, functional-role tags, regulatory flags).
- **Edges** — weighted by one or more similarity signals:
  - **Chemical similarity** — molecular descriptors, fingerprint distance, shared volatile compounds.
  - **Sensory similarity** — distance in a perceptual embedding (e.g. the Principal Odor Map).
  - **Recipe co-occurrence** — frequency with which two ingredients appear together in curated recipe corpora (Recipe1M+, FlavorGraph, Flavor Network).
  - **Nutritional similarity** — closeness in composition vectors.
  - **Cultural association** — co-occurrence within a cuisine or dietary tradition.

This structure makes substitution a graph query — "find nodes similar along sensory and functional axes but differing on cost or allergen axis" — and lets GNNs learn embeddings that compress these multi-relation similarities into vector distance.

## Role taxonomies

Ingredients are not just molecules; they are *functions*. The corpus converges on role-tagging taxonomies that capture functional behaviour: **emulsification, foaming, gelation, water binding, viscosity control, structure provision, flavour carrying, colouring, preservation, fortification**. The same protein isolate can have a different tag set in beverages versus baked goods, so role tags need to be conditional on matrix context.

Kuhl's Nature Perspective gives a complementary nine-category ingredient *type* taxonomy: whole-food pieces; extractions; natural substances; condiments; baking and cooking aids; fractional substances; non-food additives; fortifications; manufactured seasonings. This is an orthogonal cut — types for sourcing and regulation, roles for functionality.

## What the ingredient record usually carries

- **Composition** — proximate profile (protein, fat, carbohydrate, fibre, moisture, ash), micronutrient vector, key bioactive compounds.
- **Functional descriptors** — measured values for the ingredient's core functions (emulsion stability index, gel strength, water-holding capacity, viscosity profile at defined shear and temperature).
- **Sensory descriptors** — volatile compound profile; taste attributes; any panel-scored descriptors available.
- **Process descriptors** — what processing history produced this ingredient (wet/dry fractionation, extrusion profile, thermal history).
- **Cost and supply metadata** — price, regional availability, certification flags, LCA metrics.
- **Regulatory and cultural flags** — allergen status, certification eligibility (Halal, Kosher, organic, non-GMO), regional approval.

**Ingredient *fractions* matter as much as identity.** Kuhl notes that an ingredient list without weights cannot reproduce a formulation; composition + weights together are the minimum to make a formulation recomputable and comparable.

## Similarity measures and their shortcomings

Chemical-similarity distance underweights functional behaviour — two molecules with near-identical fingerprints can differ in emulsification capacity because of their tertiary structure or fractionation history. Recipe-co-occurrence similarity captures cultural pairings well but fails on *novel* substitutions (proteins that have never been combined in any published recipe). Sensory similarity needs a reliable sensory embedding, and current embeddings are dominated by Western panel data. Every similarity signal is useful; none is sufficient alone. The Oz et al. review frames substitutability as needing **all** of flavour, function, nutrition, culture, and regulation satisfied simultaneously — a graph with multiple edge types, weighted differently per query, is the natural structure.

## Implication for the expanded method

If the existing method encodes ingredients as flat feature vectors, extending to a heterogeneous graph with typed edges opens (a) better candidate generation (GNN-based proposals, subgraph-matching for substitutions) and (b) clearer reasoning over which similarity axis a substitution is trading off. See [[candidate-generation]] and [[ingredient-substitution]].

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — heterogeneous graph structure, multi-signal edges, role taxonomy, similarity-measure limitations
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — GNN embeddings for formulation search, functional-fraction framing
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — nine-category ingredient typology, ingredient-fractions requirement

## Related

- [[ingredient-functionality]]
- [[ingredient-substitution]]
- [[candidate-generation]]
- [[datasets-and-databases]]
- [[predictive-models]]
