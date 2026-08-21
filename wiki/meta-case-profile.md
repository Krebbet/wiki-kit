# Meta Case Profile

The wiki's paired private-sector case, scored against [[dimensions-of-institutional-variation]] from Meta's FY2025 10-K, its 2026 DEF14A proxy statement, and its Corporate Governance Guidelines. Where the FDA case ([[fda-case-profile]]) tests the register's public-sector axes, this one is the register's cleanest available test of **D128** (ultimate ownership/control-type) — a textbook, current, quantified control/cash-flow wedge.

**Evidence tier note.** **[empirical]** throughout, drawn from SEC filings and Meta's own governance documents. Two of the three source documents (the 10-K and the proxy) initially failed capture — both silently returned SEC's bot-block page instead of real content, caught by manual inspection and re-captured; see `master_notes.md` and `capture-manifests.md`.

## D128, run cleanly: the control/cash-flow wedge, quantified and current

**[empirical]** Meta has two share classes: Class A (1 vote/share, Nasdaq-listed) and Class B (10 votes/share, unlisted, 25 holders of record). Mark Zuckerberg — "our founder, Chairman, CEO, and controlling shareholder" — holds 99.8% of outstanding Class B stock, giving him **60.8% of total voting power** against an economic (cash-flow) interest independently estimated at **13–14%** by two separate shareholder proposals in the same proxy. This is the control/cash-flow wedge [[corporate-ownership-and-control-around-the-world]] documents across 27 countries, here achieved via dual-class stock rather than the pyramids La Porta et al. find more common, on one real, current, large institution.

**A live control-vs-legitimacy conflict, not a hypothetical one**: the 2026 proxy carries a shareholder proposal ("Give Each Share an Equal Vote") to phase out the dual-class structure over seven years, plus a second proposal to disclose voting results by share class. The board's stated rationale for opposing both: "Our capital structure allows our board of directors and management team to focus on the long term... Our board of directors provides robust independent oversight." A companion proposal's own supporting statement claims dual-class-related governance proposals "are estimated to have received majority support among the Company's independent shareholders" while still losing overall, because Zuckerberg's bloc votes them down — **[wiki synthesis]** a directly observed instance of [[dimensions-of-institutional-variation]] **D127**'s absorption logic: the "other" shareholders are formal veto-adjacent actors (a majority-support vote) whose effective power is absorbed entirely within one controlling bloc.

## The "controlled company" exemption, and voluntary non-use of it

**[empirical]** Because Zuckerberg controls a voting majority, Meta qualifies as a Nasdaq "controlled company," exempt from requiring a majority-independent board, an independent compensation committee, or an independent nominating function. Meta's own Governance Guidelines state the board "shall be comprised of a majority of directors" independent "notwithstanding the company's status as a 'controlled company.'" Current board: 12 nominees, 11 independent (all but the CEO), all four standing committees all-independent. **[wiki synthesis]** This is a real instance of an institution holding wide legal discretion (D9) and choosing, unforced, to bind itself more tightly than the law requires — worth reading against [[credible-commitment]]'s self-restraint-usually-fails thesis: here self-restraint on board composition appears to have held, though nothing prevents its reversal, and the Guidelines say so explicitly ("In the future we could elect not to...").

## Incentive structure: the controlling founder as residual claimant, not salary-taker

**[empirical]** Zuckerberg's 2025 compensation: **\$1 base salary**, no bonus, no equity awards, **\$25.1m in "All Other Compensation"** — almost entirely personal security (\$8.5m variable + \$14.0m flat annual allowance) and private-aircraft use (\$2.5m). He does not participate in the annual bonus plan. **[wiki synthesis]** This is coherent with D8 (residual claimancy) rather than an anomaly: a controlling shareholder whose wealth already tracks the firm's equity value has no need for a performance-linked salary — the incentive alignment D8 asks about is already satisfied by the ownership stake itself, and directly observing it required reading the compensation table alongside the ownership table, not either alone.

## Governance guardrails that did run as designed

**[empirical]** Related-party transactions (including Zuckerberg's and COO Javier Olivan's personal aircraft use by Meta, \$2.2m and \$187k respectively in 2025) route through the Audit & Privacy Committee under a written policy, with recusal rules for conflicted committee members. A board-approved framework caps Zuckerberg's share-pledging at 20% of his holdings and loan collateral at 5% of fair market value. **[wiki synthesis]** These are real, working instances of monitoring-design mechanisms (D45-adjacent) operating *underneath* the concentrated-control layer — useful as a caution against reading D128's wedge finding as "no governance exists here": formal checks exist and appear to function on the transactions they cover, while the vote that could remove the wedge itself remains structurally unwinnable.

## What could not be scored

**[wiki synthesis]** D129 (selectorate/winning-coalition ratio) applies awkwardly here rather than cleanly: the "selectorate" for director elections is nominally all shareholders by vote-weight, but because one holder commands a majority, the effective W/S ratio collapses toward a degenerate case (W ≈ 1 person) the model's own assumptions (interchangeable selectorate members, a genuine contest) don't anticipate. Worth flagging as a limit case rather than forcing a number. D110's full 24-provision Gompers/Ishii/Metrick index was not fully extracted (the capture pulled the classified-board and written-consent triggers, both keyed to the Class B voting threshold, but not the complete provision-by-provision inventory) — a partial run, not a complete one; a follow-up read of the governance guidelines and charter/bylaws in full would complete it.

## Source

- `raw/research/institution-case-profiles/04-meta-10k-fy2025.md` — Meta Platforms, Inc., Form 10-K, fiscal year 2025.
- `raw/research/institution-case-profiles/05-meta-proxy-def14a-2026.md` — Meta Platforms, Inc., DEF14A Proxy Statement, 2026 Annual Meeting.
- `raw/research/institution-case-profiles/06-meta-governance-guidelines-2025.md` — Meta Platforms, Inc., Corporate Governance Guidelines, effective June 1, 2025.

## Related

- [[fda-case-profile]] — the paired public-sector case.
- [[meta-oversight-board-case-profile]] — a sub-institution Meta itself created, with a structurally different and more contested authority profile.
- [[corporate-ownership-and-control-around-the-world]] — supplies D128, run here for the first time against a real, current institution.
- [[dimensions-of-institutional-variation]] — D127 and D129 both get their first real-institution test in this case.
- [[credible-commitment]] — the voluntary-independence finding bears on this page's self-restraint thesis from the confirming side, for once.
