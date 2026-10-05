# SpaceX–Cursor $60B Acquisition — Completed 2026-08-14 (option announced 2026-04-21)

**Update 2026-08-19: the option was exercised and the acquisition closed.** SpaceX completed its $60B all-stock acquisition of Cursor, merger effective **2026-08-14** — Cursor's common and preferred shares converted into the right to receive 389,289,254 SpaceX Class A shares; Cursor now operates as a wholly-owned subsidiary inside a new **SpaceXAI** division. Confirmed by multiple independent outlets (Seeking Alpha, Yahoo Finance, SatNews, crypto.news) cross-checked via WebSearch, plus VentureBeat's 2026-08-17 Origin-launch coverage citing Bloomberg. See [[../startups/cursor|cursor]] for the product/market follow-through (Origin code-hosting launch, three days after close).

On **2026-04-21**, SpaceX had announced a partnership with **Cursor** to build a "coding and knowledge-work AI" using the **Colossus** supercomputer (xAI, claimed ~1M H100-equivalent), paired with an option to **acquire Cursor for $60B or pay $10B for the work**. Article frames the structure partly as an IPO value-add story for SpaceX. The deal reignited the harness-vs-model debate and compounded valuation-cycle concerns; the original announcement and analysis below is retained for the historical record.

## OpenAI terminates Cursor's model access (2026-09-02)

OpenAI announced it is **terminating Cursor's contractual access to OpenAI models**, effective **2026-11-12** (a ~10-week wind-down notice). Per OpenAI's own post: the decision follows Cursor's acquisition by SpaceX and rests on an inability to trust SpaceX/Musk-affiliated entities' terms-of-service compliance — OpenAI cites X/Twitter's past ToS violations post-Musk-acquisition, and xAI's own admitted-under-oath ToS violation via model distillation from OpenAI (Forbes, 2026-04-30), as the pattern informing this call. A change-of-control cancellation clause in the original OpenAI–Cursor commercial agreement is the mechanism enabling termination.

**Why it's load-bearing for this page's thesis:** this is the first concrete, dated consequence of the **supplier-is-also-competitor** risk flagged in the "Why it's interesting" section above — materializing not as competitive product pressure but as an outright model-access cutoff triggered by *who owns Cursor*, not by anything Cursor did. It sharpens the harness-vs-model read: Cursor's $60B valuation assumed continued access to both Claude and GPT; losing one of its two model suppliers ~3 weeks after the SpaceX deal closed is a direct test of whether the harness (not the model) really is the asset. Cursor retains Claude access; whether it can maintain product parity model-less-diversified, and whether xAI/Grok models backfill the gap, are the open questions through the Nov 12 cutoff.

See [[../startups/cursor|cursor]] for Cursor-side product/positioning follow-through and [[../llms/xai-grok-family|xai-grok-family]] for SpaceXAI organizational context.

## Deal structure

| Element | Detail |
|---|---|
| Announcement date | 2026-04-21 |
| Acquisition option value | $60B |
| Services-only alternative | $10B |
| Compute substrate | Colossus (xAI), ~1M Nvidia H100-equivalent |
| Precursor | Week-prior xAI→Cursor compute rental (tens of thousands of xAI chips for Cursor's own model training) |
| Payment structure | Cash/stock split not disclosed |

## Cursor valuation trajectory

| Date | Valuation | Event |
|---|---|---|
| Jan 2025 | $2.5B | — |
| May 2025 | $9B | — |
| Nov 2025 | $29.3B (post-money) | $2.3B Series D |
| Apr 2026 | $50B target | Fundraise talks (reported prior week) |
| 2026-04-21 | $60B | SpaceX option |

~24x valuation jump in ~15 months. At an assumed ~$2B ARR (prior reports), $60B is ~30x ARR — the starkest current data point for the apps-layer premium, and direct fuel for the bubble-vs-reality framing (see [[../conflicts/open-questions-2026-04|C13]]).

## Why it's interesting

- **Harness, not model.** Cursor has no proprietary frontier model. It uses Claude and GPT as the underlying LLMs. The $60B market price is for distribution, enterprise penetration, and IDE-layer integration — the harness is the asset. This is the strongest proof point yet for the [[../thesis/ai-apps-layer-2026|apps-layer thesis]] and a concrete counter to the "models will eat apps" narrative.
- **SpaceX AI strategy = IPO theater.** Article explicitly cites "investors seeking more value in the IPO" as motivation. SpaceX is "widely seen to be losing money" post-xAI/X acquisitions. Cursor bundled into the IPO story demonstrates AI value without requiring SpaceX to build a frontier lab.
- **Musk cross-entity resource shuffling.** xAI chips → Cursor training → SpaceX acquisition option. Each leg depends on continued access across Musk entities; not a stable structural arrangement.
- **Model-dependency escape attempt.** Article calls Cursor's continued Claude/GPT use while Anthropic and OpenAI build competing coding tools an "awkward arrangement." The SpaceX deal is framed partly as an escape route from supplier-is-also-competitor risk.

## Counter-signals

- **Talent drain.** Two senior Cursor engineering leaders (Andrew Milich, Jason Ginsberg) departed to xAI the week prior, reporting directly to Musk. Retention and quality questions for whoever ends up operating the asset.
- **Losing-money SpaceX.** Stated in the article as financial-strain context for the IPO motivation.
- **No proprietary moat.** Without its own frontier model, Cursor's value depends on continued Claude/GPT availability — and on the IDE-layer stickiness being real, not vendor-marketed.

## Read for clients

For build-vs-buy advisory on the **coding-IDE category** ([[ai-app-categories-2025]]):

- The $60B option validates harness durability and enterprise procurement commitment to platform-coupled coding tools. Buying Cursor (or any IDE-layer incumbent — GitHub Copilot, Claude Code, Codex) is a credible enterprise procurement choice on 2026 timelines.
- The 30x revenue multiple is **not** validation of each individual coding-IDE vendor's revenue quality — it's a market bet on distribution. Treat this as evidence for *the category*, not any one pick.
- **Supplier-is-also-competitor** risk is now explicit, named in the trade press, and a live M&A driver. Enterprise coding-tool procurement should assume the underlying LLM supplier may at some point ship a competing product; evaluate portability accordingly.

## Conflict-flag cross-refs

- **C7** — "Cursor $200M revenue before first enterprise sales rep." Article references "enterprise growth surges" qualitatively; no new ARR figure. Prior C7 data stands; this is consistent with product-led growth framing.
- **C8** — "Coding agents = AGI for near-term enterprise tasks." $60B option is a strong market signal supporting enterprise-adoption side of C8. HN skepticism of the valuation (not in this source) is the counter.
- **C9** — ">$1B new coding-startup revenue 2025." No ARR figure here; not updated.
- **C13** — Practitioner revenue skepticism vs Menlo spend. $60B at ~$2B ARR = ~30x = bubble-side fuel. Article's own "losing money / IPO value-add" framing reinforces the bear case within the source.

See [[../conflicts/open-questions-2026-04|open-questions-2026-04]] for updated positions.

## Source

- `raw/research/weekly-2026-04-23/03-spacex-cursor-60b-option-2026-04.md` (TechCrunch, 2026-04-21)
- Deal-completion update, 2026-08-19: `raw/research/weekly-2026-08-19/05-cursor-origin-launch-2026-08.md` (VentureBeat, 2026-08-17, citing Bloomberg) + WebSearch cross-verification (Seeking Alpha, Yahoo Finance, SatNews, crypto.news — merger effective 2026-08-14)
- OpenAI model-access termination, 2026-09-02: `raw/research/weekly-2026-09-02/01-openai-cursor-spacex-termination.md` (OpenAI news, 2026-08-28/29; also CNBC)

## Related

- [[ai-app-categories-2025]]
- [[../thesis/ai-apps-layer-2026|ai-apps-layer-2026]]
- [[../thesis/agents-eating-saas|agents-eating-saas]]
- [[llm-api-enterprise-share]]
- [[../llms/anthropic-claude-family|anthropic-claude-family]]
- [[ai-infrastructure-frontiers-2026]]
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C7, C8, C13)
- [[../startups/cursor|cursor]] — post-close product/market follow-through
