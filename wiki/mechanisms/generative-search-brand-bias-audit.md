# Generative Search Brand Bias Audit

Monaco, Lenti & Pierri (Politecnico di Milano; arXiv 2611.07614) audit GPT-5.5, Gemini-3.6-flash and Perplexity Sonar on Italian commercial queries. Two biases persist: popularity bias (top-quintile brands are mentioned and cited 1.4x-2.8x as often as the average brand, across 1,176 brands) and familiarity bias (an invented brand name lowers a page's rank at equal content). Retrieval (search-on) and fact-preserving GEO rewrites do not remove either bias. The mechanism is visibility allocation, not price extraction: parametric priors act as a Matthew-effect filter and a cold-start barrier for long-tail and post-cutoff brands. The identity-swap paired-ranking test is a cheap black-box audit method.

## Findings

- **Popularity bias:** present in almost all engine/sector pairs; unchanged between search-on and search-off. Retrieval often injects popular brands into the engine's own search queries, so RAG does not counteract the prior.
- **Mitigation:** only buyer-persona conditioning (budget, profile, constraints) weakens the bias; personas add price terms to search queries.
- **Familiarity bias (Study 2):** swapping the real brand for an invented one lowers target-page rank. A less popular real brand still ranks ~0.19 positions above an invented one [0.11, 0.30]. The brand-product coherence penalty (0.08) is not significant after correction.
- **GEO:** three fact-preserving rewrite styles move rank ~0.02 positions (+0.022 [-0.001, 0.049]); the original brand is worth 0.42 positions more than rewriting. Narrows the manipulation surface relative to prior GEO claims (author attributes prior wins to unverified or fabricated claims).
- **Scale:** Study 1 = 19,200 answers (80 prompts x 4 personas x 2 search settings x 10 repeats x 3 engines); Study 2 = 38,400 rankings (4 models incl. DeepSeek v3.2, search-off only).
- **Caveats:** single snapshot, Italian market from Rome, four sectors (Sport, Fashion & Beauty, Insurance, Travel); Study 2 omits live retrieval; personas are purchase contexts, not demographics.

## Takeaways

- **Extraction-side audit method:** the incumbent prior sits in the assistant itself, independent of seller manipulation. A consumer agent built on a frontier LLM inherits it; grounding does not fix it. Complicates framings where sellers are the only manipulators ([[mechanisms/agents-vs-ecommerce-opacity]]) and simulations where assistants improve outcomes ([[mechanisms/consumer-ai-assistant-market-simulation]]).
- **Counter-audit tool as design input:** the equal-rank-at-equal-content identity swap works on any named entity without model access, sidestepping the access barriers in [[mechanisms/barriers-to-evidence]]. Paired-input statistics parallel [[tools/fairness-testing-algorithmic-pricing]]. Candidate component for a generative-search recommendation observatory alongside [[tools/markup-citizen-browser]]-style audits. The paper also suggests audit frameworks cover inline entity mentions, not only citation links ([[counter-power/regulatory-responses]]).
- **Code link is anonymised:** code, prompts, product pages and aggregate data are released at an anonymous.4open.science link (brand-bias-generative-search-3E74). Check for a de-anonymised repository before relying on it.
- No collective-action mechanism is proposed. Persona-prefix prompting is a weak consumer-side workaround; the vendor-side advice is to get named in sources models train on and retrieve.

## Source

- `raw/research/weekly-2026-11-09/05-generative-search-brand-bias-audit.md` (arXiv 2611.07614)
  - **Origin:** academic preprint, Politecnico di Milano (3 authors).
  - **Audience:** algorithm-audit, recsys-fairness and GEO researchers; regulators, vendors and engine developers.
  - **Purpose:** formalise and measure provider fairness in generative search.
  - **Trust:** medium-high; hypotheses H1-H5 with multiple-comparison correction and CIs, code released. Preprint, single snapshot.

## Related

- [[mechanisms/agents-vs-ecommerce-opacity]] — seller-side blocking; this page adds an incumbent prior inside the agent
- [[mechanisms/consumer-ai-assistant-market-simulation]] — simulated assistant gains vs measured head-brand bias
- [[mechanisms/agent-mediated-negotiation-empirics]] — other capability qualifications on consumer agents
- [[mechanisms/transparency-tools]] — audit tools for opaque market behaviour
- [[tools/markup-citizen-browser]] — crowdsourced audit template
- [[organizations/algorithmwatch]] — DSA Art. 40.4 audits of generative search
- [[mechanisms/barriers-to-evidence]] — black-box audit under access barriers
- [[tools/fairness-testing-algorithmic-pricing]] — paired-input counterfactual audit statistics
- [[mechanisms/adversarial-data-poisoning]] — content-side manipulation of model outputs
- [[mechanisms/the-firms-view]] — firm-side counter-tactics (GEO)
- [[counter-power/regulatory-responses]] — audit scope for entity mentions
- [[strategies/possible-strategic-levers]] — information-layer and disintermediation levers
