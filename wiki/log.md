# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-04-21] bootstrap | computational food-formulation system design

Initial bootstrap. Domain: extending an existing GA + predictive-model formulation pipeline with richer food-science-aware models and GenAI leverage points. Goal: living design doc for the expanded method. Reader: solo, ML-fluent, food-science novice — tone is explanatory, food-science terms defined on first use. Authoritative sources tuned to peer-reviewed food-science and ML/optimization venues plus trusted textbooks; marketing, vendor whitepapers, and diet pop-science excluded. Takeaway prompts emphasise candidate generation, predictive/evaluation models, food-science mechanisms, ingredient substitutability, HITL patterns, and GenAI leverage points. Domain lint checks added for term definitions, generation-vs-evaluation separation, claim sourcing, method-expansion axis naming, and surfaced open questions. The `conflicts/` workflow will be used actively to build a POV rather than merely record pre-existing disputes. Ready to receive first source.

---

## [2026-04-21] research | formulation-landscape (broad orientation)

Broad orientation run on "how food formulation works in organisations, what information is required, state of the science, and big gaps." Shortlisted 8 candidate sources, captured 6: Benner's Wageningen CIM thesis (2004, canonical NPD/chain baseline), IUFoST formulation-and-processing classification paper (npj Sci Food 2025), Oz et al. AI-enabled ingredient-substitution review (Foods 2025, directly on the user's peanut-oil-replacement problem), AI for Sustainable Food Futures consortium survey (arXiv 2509.21556), Zhou et al. Future of Food (arXiv 2511.15728, UC Davis / AIFS), Kuhl's AI-for-Food Perspective (npj Sci Food 2025). Dropped 2: the MDPI NPD challenges review (edgesuite bot-wall on both HTML and direct-PDF routes) and the Trends in Food Sci. & Tech. ML systematic review (ScienceDirect Cloudflare IP-block). Flagged four kit-scope harvest items in `master_notes.md`: audit_captures crash on inline `data:` URIs; protocol-relative URL handling in `capture_url`'s asset downloader; plain-relative URL handling (arXiv HTML figures); and lack of bot-wall detection / size-based capture-failure warnings.

## [2026-04-21] ingest | formulation-landscape (18 pages, first ingest)

Ingested the 6-source formulation-landscape capture into the wiki as 18 pages across 5 topical subdirectories. Heavy emphasis on methods/ (ingredient substitution, candidate generation, multi-objective optimisation, GA-in-context) per user direction; landscape/ gives a field overview and a recommended reading order. The GA-in-context page is explicitly editorial — the recent literature barely names GA, and the page lays out an evaluation axis for whether to extend the existing method or flank it with Bayesian optimisation, generative models, and LLM-assisted substitution. No `conflicts/` page opened this pass; NOVA-vs-IUFoST is noted in `food-classification-schemes.md` as the obvious candidate if it becomes operationally relevant. The wiki now has a coherent first draft of the design-doc spine around ingredient substitution, candidate generation, and MOO, with food-science reference pages to anchor novice-facing definitions.

