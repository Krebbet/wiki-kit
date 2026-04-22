# Priority Improvements

Consolidated prioritisation of the extensions scattered across the method pages' "Implication for the expanded method" sections, ordered by leverage ÷ build-cost. This page is *(synthesis)* — no single source proposes this ordering; it is a reading of the corpus under the wiki's own "data, not algorithms, is the bottleneck" framing from [[open-gaps]] and [[field-overview]].

The existing method is a genetic algorithm coupled to a predictive-model stack, heavily human-in-the-loop (see [[field-overview]]). The extensions below are additive, not replacements.

## Ordering principle *(editorial)*

Three axes determine priority:

1. **Data-substrate dependency.** Changes that require data assets that don't yet exist are deferred; changes that produce or structure those assets come first. [[open-gaps]] is clear that data infrastructure is the field-wide bottleneck.
2. **Reversibility and evaluable-ness.** Changes that can be piloted on one customer case and measured against an internal benchmark are preferred over retools that require the whole pipeline to land before anything can be judged.
3. **Compounding leverage.** A change that makes the next change cheaper — an ingredient graph enables GNN scoring, enables Pareto-aware substitution, enables LLM-assisted proposal — is worth more than a change that stands alone.

## Tier 1 — execute first

### 1. Minimally viable ingredient graph

A heterogeneous graph ingesting the existing historical-formulation corpus: ingredients as nodes, edges typed by composition similarity, recipe co-occurrence, and cost. Defer sensory and cultural edges until the literature-mining layer (Tier 1, item 3) produces; do not block on them.

- **Why first:** every subsequent improvement assumes a graph substrate. See [[ingredient-data-structures]].
- **Dependencies:** existing recipes and ingredient specs; no new data collection.
- **Exit criteria:** the graph can answer "what ingredients are similar to peanut oil along these three axes, within a cost ceiling" without falling back to flat-feature lookups.

### 2. Pareto-aware selection (NSGA-II)

Replace weighted-sum or lexicographic ranking in the existing GA with non-dominated sorting. Split hard constraints (cost ceiling, allergen absence, certification eligibility, regional regulatory approval) from soft objectives (sensory match, sustainability score, cultural compatibility). Report the front, not the winner.

- **Why early:** smallest code change, largest interpretability gain. Keeps the GA backbone intact. See [[multi-objective-optimization]] and [[ga-in-context]].
- **Dependencies:** none (backwards-compatible with existing fitness components).
- **Exit criteria:** customer-facing output is a Pareto front of ~5–10 candidates with the trade-off axes labelled, plus an elicitation interface for picking an operating point.

### 3. LLM literature-mining layer, scoped narrow

Extract ingredient–function–sensory–process relationships from a tight corpus (one ingredient class — e.g. alternative fats — across ~100 peer-reviewed papers) into structured triples that ratify-then-enter the ingredient graph. Human ratification remains in the loop for the first batches; the LLM is proposer, not authority.

- **Why early:** directly addresses the tacit-knowledge bottleneck [[npd-process]] framed 20 years ago; populates the graph edges that unlock substitutability queries. See [[genai-leverage-points]]. FoodAtlas ([[datasets-and-databases]]) — 230,848 food–chemical relationships mined from 155,260 papers — is the existence proof that this works at scale.
- **Dependencies:** the ingredient graph from item 1; a shortlist of ingredient classes; review capacity for the first ratification rounds.
- **Exit criteria:** one ingredient class has its functional, substitutability, and process-dependence edges populated from literature, ratified, and used in a live substitution query.
- **Stopper — resolved for raw-ingredient composition, partial for substitution and process, unresolved for non-Western recipes.** The source-availability stopper previously blocked this item. It has been audited — see [[literature-mining-substrates]] (substrate catalogue) and [[literature-mining-pipelines]] (pipeline architecture and validation). Summary: PMC + Europe PMC OA + Agricola abstracts plus FoodOn / FooDB / USDA FDC grounding are **enough** to execute the Tier-1 shape below without commercial licences. Patents are a separately mineable substrate (USPTO PatentsView, EPO via Google Cloud, Lens API) but the food-formulation patent corpus does not yet exist as a curated dataset — Akhondi et al.'s chemical-patent corpus is the methodology template if building one becomes worth it. The residual risks are (a) **Elsevier / Wiley / Springer hybrid-OA deposits are patchy**, which thins the usable English-language food-science literature; (b) **processed-foods vocabulary is weak across every ontology surveyed** — extraction fails where grounding fails; (c) **culturally diverse recipe corpora beyond Recipe1M+ / AllRecipes don't exist at scale in English** — FoodSky is the Chinese-side existence proof, but nothing comparable for South Asian / African / Latin American cuisines. The pragmatic first-pass plan in [[literature-mining-pipelines]] (pick one ingredient class — alternative fats is a natural candidate — budget ~4,000 dual-annotated sentences across 5–10 active-learning rounds, start with fine-tuned BERT rather than GPT) is executable now.

## Tier 2 — execute second

### 4. LLM-assisted substitution proposal

A parallel generator alongside the GA for the ingredient-substitution problem class. Accepts a reference product plus a change budget plus a natural-language brief ("cheaper peanut-oil replacement that keeps a kid-friendly profile"), proposes substitute candidates respecting soft constraints; constraint/ontology layer downstream filters hard constraints; predictive models score. See [[genai-leverage-points]], [[ga-in-context]], [[ingredient-substitution]].

- **Dependencies:** items 1 and 3 (graph populated enough for substitute proposal); constraint/ontology layer from item 7.
- **Evaluated by:** recovery rate on historical substitution cases the team has already solved.

### 5. Substitution-query mode vs. new-formulation mode

Explicitly split the interface and search: substitution has a reference product and a change budget (minimal-deviation search); new-formulation does not. Current pipeline blurs them. See [[ingredient-substitution]].

- **Dependencies:** none technically; product decision.

### 6. Predictive-stack upgrades

Incremental replacements, not a rewrite. GNN surrogate for flavour/aroma (Principal Odor Map as starting architecture); physics-informed or constitutive neural networks for rheology rather than pure deep nets; explicit integration of process parameters (shear, temperature, pH) alongside ingredient vectors; **calibrated uncertainty output**, not point estimates. See [[predictive-models]].

- **Dependencies:** (a) sensory-labelled data for the flavour GNN — potentially use the Principal Odor Map as transfer-learning starting point; (b) rheological training data from the historical corpus.
- **Why uncertainty matters:** required for Pareto-aware Bayesian acquisition, for regulatory defensibility, and for honest customer communication.

### 7. Constraint / ontology layer as first-class

Allergen, certification (Halal, Kosher, organic, non-GMO), regional regulatory, and customer-specific clean-label constraints expressed as ontology rules applied at proposal time — not post-hoc filters after a predictive scorer ranks. Plant Jammer is the reference deployment pattern [[industry-examples]]. See [[multi-objective-optimization]] and [[ingredient-substitution]].

- **Dependencies:** the ingredient graph from item 1 carries the flags; the ontology is the rules over them.
- **Why this matters disproportionately.** Constraint errors are more consequential than suboptimal proposals. An ontology bug that lets an allergenic substitute through is a product-recall risk; an LLM proposal bug is just a wasted scoring cycle. Correct-by-construction matters more here than anywhere else in the pipeline.
- **Open questions the wiki does not yet answer** (candidates for a focused `/research` pass): (a) schema — OWL/RDF vs typed-edge graph DB vs custom DSL; (b) reuse vs build — whether FoodOn, AGROVOC, LanguaL, FIRO, or other existing food ontologies are fit-for-purpose; (c) sources of machine-readable regulatory data for EU/FDA/Codex/Halal-certifier/Kosher-agency/USDA-organic rulesets; (d) update cadence for keeping the ontology fresh as regulations change; (e) multi-region product handling (intersect-over-regions feasibility vs per-market variants); (f) customer-specific constraint extensibility patterns; (g) testability, versioning, and audit trails for constraint rules. [[open-gaps]] names the field-wide version of this problem but does not propose a solution.

### 8. Inverse-design framing of the fitness function

Reframe customer briefs as target-property vectors and search against them — no new models, just a different fitness specification. Longer-term, add conditional generators (VAE / diffusion) when a labelled (formulation, property) corpus supports them. See [[inverse-design]].

- **Dependencies:** existing predictive surrogate (near-term); labelled dataset (long-term).

## Defer *(editorial)*

Premature given current data assets and team scale:

- **Conditional generators (VAE / GAN / diffusion) for de novo formulation.** The wiki is explicit that training requires a labelled (formulation, property) corpus that doesn't yet exist ([[inverse-design]], [[open-gaps]]). Revisit after Tier 1 + 2 produce labelled data.
- **Multi-agent agentic AI loops** (ProtAgents / Sparks / Virtual Lab class). Pilot-stage across the field ([[genai-leverage-points]]); complexity-to-payoff ratio poor for a solo or small-team effort.
- **Foundation models for food.** Kuhl's vision is correct ([[inverse-design]]) but the pre-training corpus is not assembled by anyone. Not actionable until someone builds it.
- **Real-time in-line process sensors / digital twins.** Requires instrumentation investment at production scale ([[open-gaps]]). Worth tracking, not worth building.

## Cross-cutting discipline *(editorial)*

Regardless of which items land first:

- **Track which matrix each predictive model was validated on.** Never silently reuse a model across product categories ([[open-gaps]]).
- **Emit calibrated uncertainty from every surrogate.** Required by Bayesian acquisition and regulatory defensibility.
- **Keep LLM outputs in proposal / reasoning roles.** Human-written justifications accompany any quantitative commitment, every regulatory filing, every health claim ([[genai-leverage-points]], [[open-gaps]]).
- **Design the Pareto-preference-elicitation interface early.** The corpus flags this as a real gap ([[multi-objective-optimization]]); the method won't feel different to customers until the interface makes the trade-off visible.

## Evaluation strategy *(editorial)*

Two practices that make the roadmap measurable:

### Pilot customer cases

Each improvement is driven by a concrete customer brief, not by a refactor goal. "Extend the method to handle peanut-oil replacement under a 30 % cost-reduction target" is a plan; "implement Pareto-aware selection" is a refactor that has no way to be judged good or bad on its own. Picking one pilot case per improvement lets each change be evaluated and shipped independently.

### Internal benchmark

A fixed holdout of 15–25 historical formulation cases the team has already solved. After each change, replay the case and compare:

- For Pareto-aware selection: did the new front surface a richer set than weighted-sum did in cases where the team later chose a non-winner?
- For the GNN flavour surrogate: did it rank the eventual sensory-panel winner in the top 3?
- For LLM-assisted substitution: on historical substitution decisions, does the proposal include the answer the team ended up choosing?

The benchmark is internal and noisy; it does not replace sensory panels. But it makes "the method is better" an evaluable claim rather than a narrative one. The field-wide absence of standardised benchmarks ([[open-gaps]]) means no external benchmark exists — the internal one is load-bearing.

## Source

This page is a synthesis over the existing wiki pages. Per-claim attribution lives on those pages; the ordering and dependency reasoning is editorial:

- [[field-overview]], [[open-gaps]] — the "data not algorithms" framing and cross-cutting gaps.
- [[ga-in-context]] — "flank GA rather than replace" argument and evaluation axes.
- [[candidate-generation]], [[multi-objective-optimization]], [[ingredient-substitution]] — the four-lever structure (generators, scorers, selection, constraint layer) these three pages each propose.
- [[predictive-models]], [[inverse-design]], [[genai-leverage-points]] — the per-stack upgrade paths and the ordering of GenAI entry points.
- [[ingredient-data-structures]] — the graph-substrate argument.
- [[npd-process]], [[human-in-the-loop]] — the methodology and HITL context that the extensions plug into.
- [[industry-examples]] — concrete deployment patterns (Plant Jammer constraint-filtering, NotCo iterative feedback).

## Related

- [[field-overview]]
- [[ga-in-context]]
- [[ingredient-data-structures]]
- [[multi-objective-optimization]]
- [[ingredient-substitution]]
- [[genai-leverage-points]]
- [[predictive-models]]
- [[inverse-design]]
- [[open-gaps]]
- [[human-in-the-loop]]
- [[industry-examples]]
- [[literature-mining-substrates]]
- [[literature-mining-pipelines]]
