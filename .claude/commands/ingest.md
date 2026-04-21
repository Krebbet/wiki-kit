# Ingest a New Source

Process a raw source document and integrate its content into the wiki.

## Arguments

$ARGUMENTS — the file path to the source document (e.g., `raw/research/my-topic/01-article.md`). If it's a directory, process all markdown files within it.

## Process

1. **Read the source** — Read the file at the given path. If it's a directory, read all `.md` files within it.

   **For large corpora (rule of thumb: total size over ~200KB, or more than three non-trivial source files), do not read every file into main context.** Dispatch parallel subagents (Explore or general-purpose) — one per source — and hand each the domain-specific takeaway prompts from the `DOMAIN-SLOT: takeaway-prompts` block below as its extraction structure. Ask each agent for a word-bounded structured report (headings matching the slot prompts, per-section bullets attributed to the file, a short quote budget). Synthesise those reports into the step-2 takeaway summary. This keeps the main conversation's context free for synthesis and the ingest-to-wiki writing step, and it makes the per-source extraction bounded and reproducible.

2. **Discuss key takeaways** — Present a brief summary to the user:
   - Main ideas and claims
   - What is new or different from what the wiki already covers
   - Conflicts with existing wiki positions
   <!-- DOMAIN-SLOT: takeaway-prompts -->
   Domain-specific prompts — explicitly scan for and flag the following:
   - **Candidate generation** — methods or representations for producing formulation candidates (GA, BO, RL, generative models, constraint programming, LLM-driven). Note the search space, the encoding, and any feasibility constraints.
   - **Predictive and evaluation models** — models over food properties (viscosity, emulsion stability, texture, shelf life, sensory attributes). Record inputs, training data, accuracy claims, and stated limitations.
   - **Food-science mechanisms** — the underlying chemistry, physics, or engineering that explains *why* a property behaves as it does. Define any non-trivial food-science term on first use (the wiki reader is ML-fluent but new to food science).
   - **Ingredient data and substitutability** — structured ingredient info, functional roles, substitute ingredients, cost/sensory/functional tradeoffs (the "cheaper peanut-oil replacement" pattern).
   - **Human-in-the-loop patterns** — where expert judgment is necessary, where it can be automated, and what the interface between human and system looks like.
   - **GenAI leverage points** — concrete ways LLMs or other generative models could enter the workflow (literature reasoning, tacit-knowledge encoding, candidate generation, evaluation/critique, UI).
   - **Claims that disagree with other sources** — flag for the `conflicts/` workflow; the wiki is actively building a POV on contested questions.
   <!-- /DOMAIN-SLOT -->

3. **Wait for user input** — Let the user guide emphasis before writing. They may want to highlight specific aspects or skip others.

4. **Integrate into wiki** — Based on the discussion:
   - Create new wiki pages for genuinely new topics.
   - Update existing pages where the source adds depth, nuance, or corrections.
   - Add cross-references between new and existing content.
   - Follow page format: title, summary paragraph, `## Source`, `## Related`.

5. **Handle conflicts** — If the new source contradicts existing wiki positions:
   - Document the conflict clearly.
   - Present both positions to the user.
   - Wait for a ruling before changing existing wiki content.
   - Record resolution in `wiki/conflicts/`.

6. **Update tracking files:**
   - `wiki/index.md` — add/update entries for created or modified pages.
   - `wiki/revisions.md` — add a row recording the ingest.
   - `wiki/log.md` — append a dated ingest entry: `## [YYYY-MM-DD] ingest | Source Title`.

7. **Report** — List all pages created or updated, and any unresolved conflicts.

8. **Harvest checkpoint.** Did anything surface during this ingest that would help *any* wiki, not just this one? Examples: a source-format gotcha worth warning about in this file, a synthesis pattern worth codifying, a capture bug you worked around. If yes, append a brief entry to `master_notes.md` with `Scope: kit` and `Status: open`, and mention it inline. `/harvest` will pick it up.
