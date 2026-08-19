# Incentives Under Multiple Principals

Dixit's 2002 review is the only source in this wiki that takes agency theory's machinery and runs it on the public sector directly rather than asserting that it transfers. His result: a public bureau's characteristic **weak explicit incentives, thick procedural rules, and evaluation by evidence that the rules were followed** fall out of the standard model once you feed it public-sector parameter values — many principals rather than one, many tasks that are substitutes rather than complements in the agent's attention budget, and outputs that are hard to measure. The formal core is a comparative static: with `n` non-cooperating principals each offering their own incentive scheme, the sum of marginal payment coefficients facing the agent collapses to `m = 1/(1+nrcv)`, because each principal loads positively on their own dimension and negatively on everyone else's. Dixit's own summary of what this implies for the wiki's public/private question is his most quotable and most consequential claim: **"many differences between public and private sector organizations are ones of degree, not kind."** It is his claim, derived from his model, and this wiki has exactly one other source that touches the same ground.

**Evidence tier note.** This is **(b) a formal-model synthesis presented as a review** — Dixit walks through the actual comparative statics of Holmstrom-Milgrom (1987, 1991) and his own 1996/1997 work rather than gesturing at them, but the general claims are derivations, not measurements. The **(a) empirical** content is narrow and is the strongest real evidence in the whole `incentives-and-institutional-form` batch on a public-sector-adjacent institution: Courty & Marschke's administrative micro-data on JTPA termination timing, and Heckman, Smith & Taber on JTPA caseworker selection — one US federal programme, 1980s–90s. The education material Dixit himself describes as yielding "conflicting and unclear results," with several studies using contested performance measures. The weakest claims are the assertions about French and British civil-service idealism and about privatisation efficiency (Megginson & Netter 2001, cited at one remove). Dixit **under-claims** relative to his derivations and warns explicitly against over-generalising: "the public sector is large, complex, and diverse; most of the points below apply only partially to any one agency and not at all to some." **(c) wiki synthesis** is marked inline.

## The multi-principal weakening result

**[framework]** A single agency's actions affect many parties who each hold some funding, legislative, legal or negotiating leverage. Congress, the executive, courts, unions, client groups and diffuse citizen interests are all in a position to attach consequences to what the agency does. If they could bargain in advance to a single joint scheme and split the gains, they would; but where they cannot — no shared information base, no credible commitment to share — they act independently, and the result is a **noncooperative game among principals**, whose subgame-perfect Nash equilibrium is what the agent actually faces.

Dixit quotes Wilson (1989) for the picture: "Policy making in the United States is like a barroom brawl: Anybody can join in, the combatants fight all comers and sometimes change sides, no referee is in charge, and the fight lasts not for a fixed number of rounds but indefinitely.... It's never over." Government agencies are, in his phrase, **common agencies with several principals engaged in a noncooperative game**.

The formal consequence, with an additively separable quadratic effort cost `C = Σᵢaᵢ²`:

> `m = 1 / (1 + n·r·c·v)`  (his eq. 5)

where `m` is the **sum** of the marginal payment coefficients across all principals' schemes for a given outcome type, `n` the number of principals, `r` the agent's risk aversion, and `c`, `v` the cost and variance parameters. Compared with the single-principal benchmark, "the existence of several principals makes the overall incentives for the agent much weaker. This weakening can be dramatic if `n` is large."

**The mechanism, stated plainly.** Each principal offers a *positive* coefficient on the dimension of output that concerns him and *negative* coefficients on the others, because each wants to divert the agent's effort toward his own dimension. Adding all the schemes together leaves a weak positive coefficient on every dimension. Dixit's real-world instance: Congress threatening to cut the funding of an agency that puts effort into a dimension some other principal favours — the National Endowment for the Arts supporting work that artists and critics like. He adds a second consequence that matters for institutional form: **a principal whose own dimension is hard to observe, and therefore not amenable to a smooth incentive, "may resort to imposing crude constraints on the agent's actions."** Rules appear where measurement fails.

## Substitutes, complements, and the organisational-design principle

**[framework]** With cross-terms in the agent's cost function, `C = Σᵢaᵢ² + k·Σᵢ≠ⱼ aᵢaⱼ`, so that efforts for different principals are **substitutes if k > 0** and **complements if k < 0**:

> `m = 1 / (1 + n·r·c·v·[1 + (n−1)k])`

Substitutability compounds the weakening; complementarity partly offsets it. From which Dixit derives a design principle that is unusually concrete for this literature:

> **Group complementary activities into the same agency; avoid grouping substitute activities.**

This is a genuine formal-model result rather than an intuition, and it is **not tested against any real agency reorganisation** in the source.

**The elimination result, and why it does not help.** The weakening can be removed by **compartmentalisation** — either information is partitioned so each principal sees only his own outcome, or a legal stipulation restricts each principal's payment schedule to depend only on his own `xᵢ`. Then each must use strong incentives to attract effort, and with no cross-terms the `n` drops out of the denominator entirely. Dixit immediately concedes the catch: compartmentalisation "may be impracticable in an open political system or when the principals are top-level players such as the legislature or the executive whose actions cannot be restrained by an outside force." **[wiki synthesis]** The fix is available in the model and structurally unavailable in the polity — which is a sharper statement of the public-sector constraint than the weakening result on its own.

The same qualitative result holds under adverse selection as under moral hazard (Martimort 1992; Stole 1991): weaker incentives in the noncooperative equilibrium when the agent's actions are substitutes, stronger when complements.

## Action-observability × outcome-observability: Wilson's typology

**[framework — Wilson 1989, via Dixit]** Incentive theory conventionally assumes actions are unverifiable and outcomes verifiable. Dixit's point is that public agencies frequently sit in the *opposite* cell, or in neither. Cross the two and you get a four-cell instrument:

| | **Outcomes observable** | **Outcomes not observable** |
|---|---|---|
| **Actions observable** | *(Dixit's text does not name this cell)* | **Procedural organisations** — govern by standard operating procedures attached to observable actions rather than by performance incentives. Example: OSHA, where nobody can judge whether "safety and health were furthered" but it is easy to verify that a regulation requiring labels on ladders was promulgated. |
| **Actions not observable** | **Craft organisations** — "the primary loci for applicability of incentive theory." | **Coping organisations** — "the toughest case." Explicit incentives must be very weak; if outcomes are observable but not verifiable, implicit incentives such as career concerns are what is left. |

**Recording caveat.** Wilson's own scheme names the both-observable cell (production organisations); **Dixit's text as captured here names only procedural, craft and coping.** The fourth cell is inferred from the structure of the 2×2 and is not attributable to this source. Dixit also flags, in his footnote 4, that Wilson uses "output" for what economists call action or effort — a vocabulary trap worth remembering when reading the original.

**The typology is situational, not a fixed label.** Dixit: "an army is procedural during peacetime preparations but becomes a craft organization when war starts and its 'fog' descends." The same organisation moves cells.

**A stated prediction about coping organisations, and a case.** In coping agencies Wilson expects sustained conflict between management and lower-tier "operators": management focuses on the more easily observable dimensions and denies operators freedom of action, while operators do the immediate tasks they regard as essential and keep management satisfied on its chosen focus. Where the organisation answers to multiple external principals, the conflict is replicated one level up. Dixit places the US school system "somewhere between being a 'procedural' and a 'coping' organization" and reads off the prediction directly: expect weak explicit incentives, many constraints, and evaluation by evidence that rules were followed — and do **not** expect to convert it into a craft organisation left free to devise its own procedures and judged on outcomes.

## Why bureaus differ: parameters, not laws

**[framework]** Dixit's central structural claim is that the *theory* is invariant across the public/private divide — the same moral-hazard, adverse-selection and multitask mathematics applies to both — and that what differs is the **parameterisation**. Public bureaus systematically have:

1. more principals (`n` larger);
2. more numerous tasks, more often substitutes than complements (`k > 0`);
3. worse output measurability;
4. more risk-averse principals — politicians cannot diversify policy-outcome risk the way shareholders diversify through capital markets;
5. less competition.

Run through the *same* model, those parameter values mechanically produce weaker optimal incentive slopes and more rule-boundedness. **The divergence in observed institutional form is explained without positing any different behavioural law for public-sector actors.** Hence: "many differences between public and private sector organizations are ones of degree, not kind."

Dixit sharpens the point from the other side, too: private firms nominally have a single principal-class (owners), but that is not fully accurate once unions and consumer groups are counted as separate principals. **Principal fragmentation is a continuum both sectors sit on**, not a public-sector property.

**[wiki synthesis] Triangulation status: thin, and one-sided.** This is the wiki's only source that derives public-sector institutional form from public-sector parameters. The one corroborating datapoint in this batch is narrow: Hart's private-prison case ([[property-rights-theory-of-the-firm]]) reaches a compatible conclusion — some services are rationally placed inside government — by a *different* route (residual control over non-contractible guard quality) and only for the make-or-buy boundary decision, not for internal bureau design. Dixit himself cites Hart, Shleifer & Vishny for the same case. Two sources reaching a compatible conclusion on one service in one country is corroboration of the weakest kind. Everything else in the batch is firm-only. Do not treat "degree, not kind" as established; treat it as **the best-specified claim the wiki currently has on [[open-questions]] Q3**, with its evidence base named.

**[wiki synthesis] Nuance added [enabling-institutional-change, 2026-08-19] — a tension, not a conflict, and not filed as one.** Finan, Olken & Pande ([[personnel-economics-of-the-state]]) open their chapter with **five named reasons state personnel economics differs systematically from the private-sector version**: the state's near-indefinite horizon makes long-lived promises (pensions) credible in a way a firm's cannot be; its contracting technology is narrower and coarser because the ultimate principal — citizens voting — has a control mechanism they call "coarser and more limited" than shareholders'; state provision of subsidised, low-competition goods removes market discipline and raises the relative value of direct monitoring; the organisational mission differs (public service vs. profit), shaping who self-selects in; and the state leans on self-regulation where a firm buys third-party audit. **That is a multi-mechanism divergence list, and it reads as kind-graded where Dixit's reads as degree-graded.**

Three things keep this a nuance rather than a contradiction. **(i) Neither source engages the other.** Finan, Olken & Pande never make a degree-vs-kind claim, and Dixit does not address their five mechanisms; there is no stated proposition on either side to contradict. **(ii) Two of their five are Dixit's own parameters under other names** — weak, coarse principal control is `n` and the quality of the principals' instrument; low competition is his fifth parameter verbatim. The genuinely new ones are the horizon asymmetry (which enables a contract form, deferred compensation, rather than changing a parameter of an existing one) and the self-regulation-vs-third-party-audit default. **(iii) Their own data cut against their mechanism list.** The measured public-sector wage premium runs above 100% in the poorest sample countries and 4–20% in the richest — a gap that shrinks continuously with income, which is a degree-graded pattern, not a kind-graded one. Recorded here so that a later source arguing either side finds the tension already stated. The discriminating test remains Q38.

## Micromanagement as rational response, not pathology

**[framework]** Dixit's most direct reframing, and the reason this page matters beyond the public sector: he treats micromanagement not as a pathology but as "an unavoidable consequence of, or a less costly way of coping with, the asymmetric observability of multiple outcomes affecting multiple principals." Where a principal cannot write an outcome-based contract on the dimension he cares about, imposing crude constraints on the agent's actions is his *best available* instrument. The rulebook is the residue of unmeasurable objectives owned by principals who cannot coordinate.

This converges with Holmstrom & Milgrom's reading of bureaucratic constraint as an optimal response to measurement difficulty ([[multitask-incentive-theory]]) while arriving by a different route — principal multiplicity rather than task multiplicity. **[wiki synthesis]** Note what this sets up against the existing register: [[dimensions-of-institutional-variation]] D9 records Libecap's finding that regulators prefer revocable permits to transferable rights specifically to preserve their own discretion, which is a self-serving reading of the same variable. Preserving discretion and reducing it are opposite moves, so the two are not in strict contradiction — but they are opposite priors about what a rule-bound bureau is *for*. Recorded as a tension at D9, not as a conflict.

## Failure modes, with the batch's cleanest public-sector evidence

**[empirical — Courty & Marschke 1997]** The JTPA (Job Training Partnership Act) evidence is the one place in this batch where the multitask/gaming prediction meets administrative micro-data on a publicly funded programme. Agencies were paid a bonus for graduating trainees into jobs by a fixed date; the observed **strategic timing of terminations around the bonus threshold** matches the non-monotonic prediction of the formal model. Two distinct failure modes come out of the same programme:

- **Threshold gaming** — exploiting the functional form of the reward schedule rather than the metric itself.
- **Cream-skimming** — agencies recruit the most placeable clients rather than the neediest (Heckman, Smith & Taber on caseworker selection). A goal-displacement variant specific to public service-delivery contracts, and one with no private-sector analogue in this batch.

Other failure modes Dixit names, on theory plus illustration rather than data:

- **Task substitution.** Patent examiners paid partly through bonuses for "disposal" of cases: issuing a patent always disposes of the case, while denying one may keep it alive through amendment or appeal — so too many patents get issued. Schools favouring equity demonstration over efficiency because equity is easier to prove.
- **Collusion between hierarchical tiers.** Regulator and regulated firm, or middle managers and case workers — modelled through common-agency and post-career-concern channels. The legislature's counter-incentive (rewarding the regulator's rent-honesty) reduces but does not eliminate it.
- **Adverse selection into public employment.** Because private-sector marginal incentives pay more to high-ability, low-risk-aversion types, lower average ability may select into public service — "conform[ing] to the popular impression that public-sector bureaucrats are mediocre." **Dixit does not endorse the folk claim**; he hedges immediately that "the social optimality of moving top talent from the private to the public sector is not self-evident." This is a *modelled* selection channel with no measurement behind it in this source.
- **Tautological self-assessment.** Dixit criticises a proposed education fix — "an assessment device designed to measure what is being taught" — as able to "degenerate into a tautological approval of the existing system."

## Where an activity should sit, and the not-for-profit form

**[framework]** Dixit extends Williamson's discriminating-alignment logic to the public/private boundary itself: activities close to pure private goods (excludable, rival) are argued to be more efficiently produced privately, citing Megginson & Netter's (2001) survey finding privatised state enterprises generally more efficient — cited at one remove and not independently assessed. But privatisation does not guarantee competition, and multidimensional quality-versus-cost tradeoffs persist in private monopolies.

The **not-for-profit form** is explained (via Glaeser & Shleifer 2001) as a credible-commitment device against quality-cutting: an NFP manager can capture cost savings only as perquisites, which are worth less to him than cash, so NFP status is a more credible signal of quality maintenance than a for-profit rival can send. Public agencies face tighter constraints still on appropriating cost savings — which is Dixit's argument for why activities with severe quality-measurement problems are sometimes rationally placed in government rather than contracted out. He cites Hart, Shleifer & Vishny on prisons for the case. **[wiki synthesis]** Structurally this is the same move as the shackling arguments on [[credible-commitment]]: remove the actor's ability to capture the gain from the behaviour you fear, rather than trying to detect the behaviour.

## Levers

**[framework]** With Dixit's own evidentiary grading, which is unusually honest:

1. **A standing "devil's advocates" unit** in every agency, tasked solely with red-teaming how current policies can be gamed or arbitraged. Purely a recommendation — "no sure remedy... a small reform may help a lot." Untested.
2. **Group complements, split substitutes** across agencies. Formally derived from the `k` result above; never tested against a real reorganisation.
3. **Prefer linear schemes to step functions and thresholds**, to reduce gaming; and "be content with the second or third best" rather than chasing one powerful metric. Derived from the Holmstrom-Milgrom aggregation-over-time result. Formal, not empirical — though the JTPA threshold-gaming evidence is consistent with it.
4. **Reform systemically, not piecemeal.** Endorsing Hannaway (1996) that education reform must move on several dimensions at once because partial fixes just relocate the gaming. Dixit flags the empirical support as ambiguous: "It is not immediately clear that the net result will be beneficial."
5. **Cultivate implicit incentives** — career concerns, professionalism, mission focus — where explicit incentives are structurally weak. Supported by Dewatripont, Jewitt & Tirole's (1999) formal result that career concerns work best with a **narrow, clear mission**; Dixit flags the multiplicity and vagueness of most public mandates as the binding limit on this lever.

**[wiki synthesis]** Lever 5 and the multi-principal result are in tension with each other and Dixit half-says so: the parameter that makes explicit incentives weak (many principals, many objectives) is the same parameter that makes the implicit substitute weak (no narrow, clear mission). The public-sector incentive problem does not have a slack instrument to fall back on.

## What is not established

- **No organisational scale or age content.** No claim about agency headcount, budget size, or years since founding. The scale claim that exists is about **stakeholder count** (`n`), not headcount, and the age claim is about **career stage**: career-concerns incentives are strong early — young workers exert effort under weak explicit incentives because output signals ability and raises future wages — and decay as reputation is revealed, so senior workers need sharper explicit incentives late. That is tenure, not institutional age. See [[open-questions]] Q7.
- **The formal theory is untested at the level Dixit applies it.** The Sections II–III derivations are presented as general and are not tested in this source; every case-level claim is US, late 20th century (JTPA 1982–90s; US public schools 1990s; State Department, SSA, USPS, Patent Office as illustrations). France and Britain appear only in passing on civil-service professionalism. There is no non-US, non-Anglophone material anywhere.
- **Selection is modelled, not measured.** The adverse-selection-into-public-employment channel above is a derivation with a hedge attached, not a finding.
- **Agency leadership selection and removal is out of scope**, though post-career-concern collusion between regulator and regulated is modelled.

## Source

- `raw/research/incentives-and-institutional-form/06-dixit-incentives-public-sector.md` — Avinash Dixit, "Incentives and Organizations in the Public Sector: An Interpretative Review", *Journal of Human Resources* 37(4), 2002, 696–727. https://www.edegan.com/pdfs/Dixit%20(2002)%20-%20Incentives%20and%20Organizations%20in%20the%20Public%20Sector.pdf
- `raw/research/incentives-and-institutional-form/05-prendergast-incentives-firms.md` — Canice Prendergast, "The Provision of Incentives in Firms", *JEL* 37(1), 1999 (for the independent account of the Courty & Marschke JTPA evidence and the cream-skimming failure mode). http://qed.econ.queensu.ca/pub/faculty/ferrall/econ861/papers/prendergast.pdf

## Related

- [[multitask-incentive-theory]] — the model Dixit is re-parameterising; it reaches rule-boundedness through task multiplicity where Dixit reaches it through principal multiplicity.
- [[property-rights-theory-of-the-firm]] — the only other public/private treatment in this batch, and the sole corroboration of Dixit's conclusion, on one service (prisons) by a different mechanism.
- [[governance-structures]] — Dixit extends Williamson's discriminating alignment to the public/private boundary using incentive-theoretic microfoundations rather than asset specificity.
- [[bureaucratic-growth-and-parkinsons-law]] — Niskanen's budget-maximising bureaucrat is the rival prior: Dixit explicitly declines the public-choice framing and treats bureaucratic form as rational equilibrium.
- [[dimensions-of-institutional-variation]] — supplies D50 (action-observability × outcome-observability) and D51 (principal multiplicity and heterogeneity), and half of D49.
- [[credible-commitment]] — the not-for-profit form as a commitment device is structurally the same move as shackling, on a different actor.
- [[transaction-costs]] — Dixit's account of why activities migrate across the public/private boundary is a transaction-cost-politics argument, citing his own 1996 book.
- [[what-is-an-institution]] — "degree, not kind" is a direct position on whether public and private governance are one analytical object.
- [[open-questions]] — Q3 (public/private invariance) and Q9 (measurable vs. unmeasurable output) both turn on this source.
- [[personnel-economics-of-the-state]] — the five-mechanism public/private divergence list that sits in tension with "degree, not kind", recorded above as a nuance rather than a conflict.
- [[reorganisation-base-rate]] — a candidate kind-difference on a different variable: NAO's own analysis shows private M&A wrapped in a mandatory disclosure regime that government reorganisation entirely lacks, whatever the underlying outcome rates.
- [[political-economy-of-public-sector-reform]] — reforms opposed simultaneously by parliament, unions, judiciary and uncoordinated donors are this page's mechanism applied to implementation.
