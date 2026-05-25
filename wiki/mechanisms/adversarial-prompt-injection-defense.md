# Adversarial Prompt-Injection Defense (Publisher-Side)

Mechanism page for **publisher-side adversarial defense against scraper-LLMs via repurposed indirect prompt injection**. The page owner embeds optimised hidden HTML fragments into their own pages; when a browsing-enabled LLM assistant fetches the page in service of a contact-seeking query, the embedded fragments steer the model away from verbatim or reconstructible disclosure of contact PII (emails, phone numbers, addresses). Anchored on Liu, Zha & Chen 2026 *PIIGuard: Mitigating PII Harvesting under Adversarial Sanitization* (arXiv 2605.03129, cs.CR). The mechanism inverts the usual framing of indirect prompt injection: instead of an *attacker* injecting hidden content to subvert a target's agent, the *publisher* injects hidden content into their own resource to subvert hostile scraping agents. Conceptual sibling of [[adversarial-data-poisoning]] (Glaze/Nightshade — artist-side defense against generative-AI training scrapers) but operates at a different layer: **inference-time prompt steering**, not training-time data poisoning.

## Threat model

The defender is an ordinary webpage owner with contact PII on a public page (a small business, an academic with a "Contact" page, a community organisation). The attacker is **not** a classical crawler — it is a browsing-enabled LLM assistant ("ChatGPT search," Claude with web tools, DeepSeek-chat, etc.) operating on behalf of a user querying for contact information at scale. The attack channel:

1. Attacker (or a downstream user) issues a contact-seeking query to the LLM assistant.
2. The assistant fetches the target webpage via its browsing tool.
3. The assistant extracts and emits the contact PII verbatim or in a reconstructible form (e.g., obfuscation patterns the user can trivially undo).

The paper notes that **most prior defenses sit at the model, service, or agent layer** — i.e., they require the LLM vendor or the agent platform to cooperate. Ordinary page owners have no deployable option in that stack. PIIGuard's contribution is a **webpage-level defense** that ships entirely in the page's own HTML and remains under the page owner's control.

The paper additionally evaluates an **adversarial sanitization** layer: an attacker-side LLM pre-processes the fetched HTML to strip suspected defensive injections before passing the cleaned page to the answering model. PIIGuard's robustness under sanitization is the harder evaluation regime.

## Mechanism

PIIGuard searches for a **hidden HTML fragment** (text + insertion position) that, when added to the target page, causes the scraper-LLM to refuse or scramble disclosure of the contact PII while preserving benign same-page question-answering utility.

The search loop combines three components (per the abstract):

1. **Rule-based leakage scoring** — fast scoring of candidate fragments against rule-based detectors for verbatim and reconstructible PII disclosure.
2. **Evolutionary mutation** — fragment text and insertion position are mutated under the leakage-score objective; this is a black-box optimisation over the prompt-injection design space.
3. **Final judge-based recoverability assessment** — a separate LLM judge evaluates whether the model's output, even when not verbatim, allows a user to reconstruct the PII.

The fragment is embedded **hidden** in the HTML (the abstract does not specify the hiding mechanism — likely `display:none`, off-screen positioning, or `aria-hidden` patterns; full PDF read would confirm). Hidden content is invisible to human visitors but ingested by browsing-enabled LLMs that consume the raw HTML.

## Evaluation (as reported in the abstract)

Three target models evaluated in direct-HTML mode: **GPT-5.4-nano, Claude-haiku-4.5, DeepSeek-chat (latest v3.2)**. Two leakage metrics: rule-based and judge-based.

| Setting | Defense Success Rate |
|---|---|
| Direct HTML, rule-based leakage | "at least 97.0%, often reaching 100.0%" |
| Direct HTML, judge-based leakage | "at least 97.0%, often reaching 100.0%" |
| Benign same-page QA utility | "preserved" (no quantitative figure in abstract) |

Two **harder settings** are also evaluated:

- **Public-URL browsing** — the scraper retrieves the page via its standard browsing tool rather than direct HTML ingestion. Robustness depends on the browsing interface's HTML-rendering choices.
- **Attacker-side LLM sanitization** — an adversarial sanitizer pre-processes the fetched page to strip suspected defensive fragments before the answering model sees them. Robustness depends on the sanitizer's prompt.

The paper's stated finding on the harder settings (abstract):

> "Page-side defensive fragments can remain effective in deployment for some model-position pairs, but robustness varies substantially across browsing interfaces and sanitizer prompts."

This is the load-bearing caveat: PIIGuard works well against direct-HTML scraping, but adversarial sanitization is **not** uniformly defeated. The defense is real but not robust to the strongest current attacks.

## Code / artefact status

The arXiv abstract page (captured 2026-05-11) **does not link to a code repository**. The "Code, Data and Media Associated with this Article" arXiv panel lists only generic third-party services (alphaXiv, CatalyzeX, DagsHub, Hugging Face) with no paper-specific links populated at capture time. v1 was submitted Mon 4 May 2026; reproducibility tooling has not yet been disclosed. **Watch the arXiv listing for a v2 with a `github.com/...` link, or a Hugging Face Space release.** Until then, the mechanism is documented but not directly forkable.

## Position in the wiki's taxonomy

Three mechanism pages now sit on the **publisher / data-owner counter-tooling against scrapers** axis. They are distinct and complementary:

| Mechanism | Defender | Layer | Attack surface | Example tools |
|---|---|---|---|---|
| [[adversarial-data-poisoning]] (Glaze / Nightshade variant) | Artist / image-author | **Training-time** | Image-scraping for generative-model training | Glaze (defensive cloak), Nightshade (offensive poison) |
| [[browser-fingerprinting]] defenses + obfuscation | Browsing consumer | **Inference-time (request)** | Tracker + fingerprinter scripts | CanvasBlocker, Brave, Ephemeral (PETS 2026) |
| **adversarial-prompt-injection-defense** (this page) | Webpage owner | **Inference-time (response)** | Browsing-enabled LLM scrapers extracting page content | PIIGuard (Liu, Zha & Chen 2026) |

All three are *adversarial publisher counter-tooling against scrapers*, but the mechanisms operate on different objects: image pixels (Glaze/Nightshade), browser-API surface (fingerprint defenses), and the scraper-LLM's prompt context (PIIGuard). The threat actor in each case is also different — generative-model trainers (Glaze/Nightshade), tracker networks (fingerprint defenses), and agentic LLM scrapers (PIIGuard).

The **inversion** PIIGuard performs is notable: indirect prompt injection has been the canonical *offensive* technique in agent-security literature (an attacker plants hidden instructions in resources a victim's agent will fetch, hijacking the agent). PIIGuard reuses the same primitive *defensively* — the page owner is now the planter, and the hostile scraper is the agent being hijacked. The same mechanism class that [[agent-interop-protocols]] documents as a **60–100% leakage vector** against A2A baseline (Louck et al. 2025) is here repurposed as a defense. This dual-use pattern echoes [[adversarial-data-poisoning]]'s framing of poisoning attacks as both threat and "response from below."

## Relevance for consumer counter-power

*(editorial / synthesis — the captured source targets the PII-harvesting use case specifically, not the broader counter-power frame.)*

- **Direct application to [[noyb]]-class data-subject-rights organisations**: any web-published contact information for individual members, lawyers, or coordinating staff is potential PII-harvesting territory for hostile scraping. PIIGuard-style page-side defenses are a deployable counter that does not require LLM-vendor cooperation.
- **Substrate for [[the-firms-view|the firm-side / publisher-side]] equivalent of [[obfuscation|consumer-side obfuscation tools]]**: an arms-race symmetry exists where both extraction and counter-extraction sides can deploy adversarial-prompt-injection tooling. The wiki has so far documented the consumer-side adversarial layer (obfuscation, ACA, fingerprint rotation); PIIGuard is the first systematic publisher-side equivalent.
- **Watch for community-data-cooperative deployment**: a [[data-cooperatives|data cooperative]] or [[platform-cooperatives|platform cooperative]] that publishes member contact pages could deploy PIIGuard-class defenses at the cooperative-platform level, giving every member fragment-level protection without per-member configuration. Tier-3 build candidate pending code release.
- **Caveat — sanitization arms race**: the paper's "robustness varies substantially across sanitizer prompts" finding suggests this is an early-stage arms race, not a settled defense. Tracking subsequent papers (sanitizer-robust prompt injection, recursive sanitizer-vs-injector co-training) is the natural watchlist follow-on.

## Caveats and open questions

1. **Code-release status unconfirmed.** The arXiv abstract does not link to a repository at capture time (2026-05-11). The mechanism is documented; the artefact is not yet forkable.
2. **Single research group, single paper, single version.** v1 only; no peer review yet.
3. **Hiding mechanism specifics deferred to PDF read.** The abstract does not specify exactly how fragments are hidden (CSS, ARIA, off-screen positioning). Relevant to whether ordinary CMS workflows can deploy the defense.
4. **Adversarial sanitization is not uniformly defeated.** The honest reading of the abstract is that PIIGuard works well against direct-HTML scraping (97–100% defense success) but is *not* a closed defense against scraping pipelines that include an LLM-based sanitizer. The arms-race is open.
5. **Benign-utility quantification absent from abstract.** "Preserving benign same-page QA utility" is asserted but not numerically anchored at the abstract level. Worth checking in the PDF.
6. **Scaling unknown.** No data in the abstract on per-page optimisation cost (search-loop wall-clock) or whether one fragment generalises across pages. Deployability at cooperative scale depends on this.

## Source

- `raw/research/weekly-2026-05-11/04-piiguard.md` — Liu, Zha & Chen, *PIIGuard: Mitigating PII Harvesting under Adversarial Sanitization*, arXiv 2605.03129 [cs.CR]. Submitted 4 May 2026. Captured via pymupdf, arXiv abstract page (PDF). Origin: academic arXiv preprint. Trust: medium-high for the documented direct-HTML defense rate (clean evaluation regime); medium for sanitization-robustness claims (paper itself flags variance across sanitizer prompts). Code release: not yet linked at capture time.

## Related

- [[adversarial-data-poisoning]] — sibling mechanism on the publisher / data-owner counter-tooling axis; operates at training-time rather than inference-time
- [[obfuscation]] — consumer-side adversarial counter-tooling (decoy-behaviour / noise injection); same arms-race frame from the consumer side
- [[browser-fingerprinting]] — adjacent watcher-side / counter-watcher-side technique stack; documents the consumer-side inference-time arms race
- [[agent-interop-protocols]] — documents prompt injection as an **offensive** primitive against A2A-based agents (60–100% leakage in Louck et al. 2025 baseline); PIIGuard inverts the same primitive defensively
- [[agent-mediated-negotiation-empirics]] — adjacent empirical literature on LLM-agent robustness; Abdelnabi et al. 2024 cooperative-collapse-under-adversary result is the symmetric case for negotiation rather than scraping
- [[noyb]] — concrete deployment candidate: data-subject-rights organisations publishing contact pages
- [[the-firms-view]] — the firm/publisher-side counter-perspective frame; PIIGuard fits as publisher-side adversarial tooling
