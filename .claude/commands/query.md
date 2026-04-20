# Query the Wiki

Answer a question using the wiki as the primary source, and reflect any new insights back into the wiki.

## Arguments

$ARGUMENTS — the question to answer.

## Process

1. **Search** — Read `wiki/index.md` to identify relevant pages. Read those pages.

2. **Answer** — Synthesise an answer **strictly from the wiki content**. Do not introduce outside knowledge, training-data recall, or personal opinion unless the user explicitly asks for it (e.g., "what do you think?", "add your own take", "go beyond the wiki"). Use `[[wiki-link]]` citations so the user can drill deeper in Obsidian.

   **Sourcing rules:**
   - Every substantive claim must be traceable to a wiki page via `[[wiki-link]]`.
   - If the wiki does not cover part of the question, say so explicitly ("the wiki does not address X") rather than filling the gap from outside knowledge.
   - If the user explicitly invited outside input, segregate it under a clearly labelled `## Beyond the wiki` (or `## My take`) section at the end. Everything above that heading must come from the wiki; everything below must be marked as not-from-wiki.
   - Never blend wiki content and outside content in the same paragraph or bullet without a marker. If a sentence mixes both, split it.

   <!-- DOMAIN-SLOT: answer-tone -->
   **Tone and voice:** Terse, expert. The reader is the researcher (David) — assume an ML/RL background, no need to explain gradients, transformer architecture, or PPO. Equations and notation are welcome; use LaTeX-style inline (`$x$`) and display blocks. When the question invites synthesis or comparison across multiple methods/papers, prefer a comparison table (columns like *method × claim × sample-cost × concept-learning evidence × source*) over prose lists. Cite every claim with `[[wiki-link]]`.
   <!-- /DOMAIN-SLOT -->

3. **Judge whether to update the wiki** — Does the answer contain:
   - A novel synthesis or comparison not already on any page?
   - A clarification that would help future readers of the relevant pages?
   - A new connection between concepts not currently cross-referenced?
   - A gap in the wiki that the question exposed?

   If none of the above: no wiki update needed. Stop here.

4. **If update warranted** — Make the minimum useful change:
   - Add a paragraph or section to an existing page (preferred over creating a new page).
   - Add missing cross-references between related pages.
   - Create a new page only if the question revealed a topic that deserves standalone coverage.
   - Follow page format: title, summary, source, related.

5. **Update tracking:**
   - `wiki/revisions.md` — add a row.
   - `wiki/index.md` — only if a new page was created or a summary changed.

6. **Tell the user** — If you updated the wiki, mention what you changed briefly at the end.
