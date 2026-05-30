# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-04-24] research + ingest | thesis-foundations (10 papers)

First research run. Captured 10 arXiv papers to `raw/research/thesis-foundations/` via `tools.capture_pdf` (initial attempt blocked by missing `httpx` in the poetry venv; resolved with `poetry install` — kit-level observation logged to `master_notes.md`). Dispatched 10 parallel ingest subagents producing `.ingest/*.summary.md` files; all passed `parse_summary()` schema validation. Review packet synthesized from summaries and approved after user rulings on: page plan (accepted), auxiliary page scope (create 3 multi-source anchors, defer 5 single-source ones — of which one was subsequently absorbed by the 07+08 merge), conflict framings (both open), and the 07+08 merge into `mamba-2-and-ssm-hybrids`.

**Research pages (11):** `expert-choice-routing`, `mixture-of-depths`, `block-operations-and-modular-routing`, `universal-transformer`, `looped-transformers-and-reasoning`, `looped-language-models`, `mamba-2-and-ssm-hybrids` (merged papers 07+08), `modular-deep-learning-survey`, `mixture-of-cognitive-reasoners-micro`, `routing-mechanisms-in-modular-networks` (aux), `brain-inspired-modularity` (aux, logged separately below).

**Open conflicts (2):**
- `learned-routing-specialization` — Position A (EC/MoD/MICRO): learned routing produces genuine specialization. Position B (modular-DL survey citing Mittal/Muqeeth/Lewis): learned routing reliably underspecializes. Ruling: keep open per user direction.
- `looped-vs-depth-scaling` — Position A (Latent-Thoughts): looping trades perplexity for reasoning at iso-FLOP. Position B (Ouro): looping matches dense LMs at scale. Comparison bases differ (iso-FLOP vs iso-param vs iso-token). Ruling: keep open.

Ready for follow-up `/query`, further `/research` runs, or `/lint`.

---

## [2026-04-24] create | thesis-architecture-sketch

Created `wiki/research/thesis-architecture-sketch.md` in response to user query asking for a concrete design recipe for the thesis architecture (looped + routes-to-specialized-blocks + graceful exit). Composed from three attested recipes: [[looped-language-models]] (Ouro weight-shared recurrence + two-stage entropy-regularized exit gate) + [[looped-transformers-and-reasoning]] middle-looping structural variant + [[mixture-of-cognitive-reasoners-micro]] MOB with three-stage curriculum-seeded specialization. Autoregressive compatibility via [[mixture-of-depths]] aux MLP predictor. Sections: composed architecture, considerations, wiki-attested painpoints, design-blocking unanswered questions, prioritized open research questions. Explicit flags on unverified assumptions (heterogeneous block types under learned routing; loop × router × gate composition; curriculum-free specialization). Updated index.md and revisions.md.

---

## [2026-04-24] create | brain-inspired-modularity

Wrote aux/synthesis wiki page `wiki/research/brain-inspired-modularity.md` synthesising cognitive/neuroscience framings from papers 03 (block-operations / SMFR) and 10 (MICRO). Applied mandatory analogical-vs-mechanistic tagging: 03 tagged inspiration-only (Symbol Binding Problem as design metaphor, no localizer experiments); 10 tagged direct-transfer (four brain-network-aligned experts, neuroscience localizer validation, r=0.7 behavioural correlation). Editorial sections cover cross-cutting per-block routing convergence, seeded-vs-emergent specialisation axis, thesis relevance, and open falsification questions. Updated index.md and revisions.md.

---

## [2026-04-23] bootstrap | transformer architectural modularity

Initial bootstrap. Schema and commands tailored for transformer architectural modularity — heterogeneous block integration (CNNs, GNNs, SSMs, etc.), repetitive/looped computation, and routing/dispatch mechanisms for block-level specialization. Primary sources: academic papers (peer-reviewed + arXiv) and textbooks; adjacent-field papers from neuroscience and psychology welcome as analogical grounding. Reader: solo (user), terse/expert tone. Ready to receive first source.
