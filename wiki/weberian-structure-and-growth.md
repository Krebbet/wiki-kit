# Weberian Structure and Growth

Two papers from one research programme testing whether merit-recruited, career-stable, tenure-protected public administration predicts economic performance. **Evans & Rauch (1999)** built an original dataset — 126 country experts scoring 35 developing countries on a 10-item "Weberianness Scale" describing their core economic-policy agencies — and report the scale correlating with 1970–1990 GDP-per-capita growth at **r = .67, p < .001**, robust to initial income and human capital and to most regional-dummy specifications. **Rauch (1995)** attacks the same question with a domestic natural experiment instead of a cross-section: 144 US cities over 1902–1931, exploiting the staggered adoption of three distinct municipal reforms, and finds that adopting **civil service** (merit exam plus just-cause tenure) raised the share of municipal expenditure going to infrastructure, with an inferred knock-on to manufacturing-employment growth. The two are complementary in exactly the way this wiki cares about: one is correlational and cross-national, the other quasi-experimental and within-country, and **they agree**. What neither supplies — and this is the important limitation — is any decomposition of *which component* of the bundle does the work.

**Read the next section before using either source for anything with "Weber" in it.**

## The Weber gap, stated first because everything else depends on it

**[wiki synthesis]** **This wiki does not hold Weber's own text.** The only openly available copy of "Bureaucracy" (in *Economy and Society*) is a scanned image PDF with no text layer; OCR failed and was discarded. Consequently:

- **Nothing on this page is Weber's argument.** Evans & Rauch's scale is a 1999 operationalisation built by two contemporary social scientists who selected **two** of Weber's characteristics — meritocratic recruitment, and predictable rewarding career ladders — **explicitly for measurability**, from a larger set. Their own words: "we could have selected other Weberian organizational features." Their secondary sources for what Weber said are the Gerth & Mills (1958) and Parsons (1964) translations, not Weber's primary text.
- **The scale's authors exclude one Weberian feature deliberately, and say why.** A footnote names rule-governed decision-making and strictly bounded jurisdictions as a candidate third dimension and drops it because it is "a double-edged sword, enhancing predictability and efficiency up to a certain point but producing rigidity and organizational sclerosis when carried further." That is the authors of the Weberianness Scale anticipating the [[goal-displacement-and-bureaucratic-ritualism]] critique in their own text and bracketing it out of scope. **The scale therefore measures one sub-claim, by its authors' own account, not "the Weberian model."**
- Rauch (1995) is in the same position: he frames his paper against **Evans's (1992) Weberianism measures**, not against Weber. His own summary note is that his paper is *empirical evidence consistent with* Weberian claims, not a statement of the model.
- Guo Xu's review, on [[civil-service-tenure-and-political-insulation]], reaches Weber only through a single footnote glossing an untranslated 1922 German edition — also second-hand.

**Rule for this wiki: never cite anything in this batch as authority for what Weber said.** Cite these sources for what their authors operationalised and measured.

## Evans & Rauch: the cross-national correlation

**[empirical — cross-national OLS on original survey data; the strongest evidence type in this batch, and correlational]**

**Design.** 35 developing countries (Chenery's 30 "semi-industrialized" countries plus Haiti, Nigeria, Pakistan, Sri Lanka and Zaire, added to widen the low end of the distribution). Data collected 1993–1996 from **126 country experts** — at least 3 per country for 32 of them, 2 for Morocco, Thailand and Uruguay — via fixed-response questionnaire, **retrospectively describing the bureaucratic structure they believe characterised 1970–1990**. Growth from Penn World Tables 5.5; human capital from Barro & Lee (1993). The baseline specification is built on Levine & Renelt's (1992) robust-variables list.

**Results.**

| Claim | Number | Note |
|---|---|---|
| Weberianness ↔ GDP-per-capita growth 1970–1990 | **r = .67, p < .001** | Robust to initial GDP per capita and human capital; largest standardised coefficient in every specification it enters |
| Weberianness → domestic investment share | standardised coefficient **.489, t = 3.508, p < .01** | The paper's own preferred channel: states raise growth chiefly by eliciting **private** investment, not by direct production |
| Weberianness ↔ government consumption / GDP | **r = −.35, p < .05** | More-Weberian states are fiscally *smaller*, not bigger — a claim about spending, not about organisational size |
| Weberianness × government consumption; Weberianness × public investment | **both null** | So the "public infrastructure investment is the channel, conditional on Weberianness" story is floated in the theory section and **not supported by the paper's own tests** |

**Robustness, reported by the authors against themselves.** The effect **drops below significance** when the East Asia dummy is combined with either the Sub-Saharan Africa or the Latin America dummy, and is **not robust** with all three regional dummies entered simultaneously — 18 of the 35 countries. The authors call this "an extremely stringent test", which it is; the result is disclosed rather than concealed, and it should travel with the headline. The findings are anchored heavily on two regional extremes: Sub-Saharan Africa (lowest on both) and the four East Asian Tigers (highest on both).

**The unit of analysis is narrower than "the bureaucracy".** Experts were asked to name "the four most important agencies… to shape overall economic policy" and to score *those* agencies. The dependent variable is national. The authors flag the gap themselves: "the implication is not that the entire bureaucratic apparatus must be structured in this way… Having Weberian structures in the strategic core of the bureaucracy may be sufficient." This is a claim about **a subset of state organisations acting as a lever on national outcomes**, and it is one of the very few sources in this wiki that decomposes below the national scalar at all — see [[open-questions]] Q90.

## The Weberianness Scale, item by item

**[empirical — the instrument itself, and the source of the page's central limitation]** All ten items, with what each measures:

| # | Item | Measures |
|---|---|---|
| 1 | Importance of the core agencies in originating economic policy | Agency salience — establishes *which* agencies are scored; not a personnel measure |
| 2 | Proportion of higher officials entering via formal examination | Recruitment mechanism (exam vs. patronage) |
| 3 | Modal years a higher-level official spends in the agency | Career length / tenure stability |
| 4 | Promotion prospects — how many of ~6 hierarchical steps a career entrant expects to climb | Internal promotion ladder |
| 5 | How common it is to interleave private- and public-sector spells | Career stability / revolving-door frequency |
| 6 | Salary of higher officials relative to comparable private managers, **excluding** bribes | Competitive pay |
| 7 | The same comparison **including** bribes and extra-legal perquisites | Total compensation including corruption |
| 8 | Trajectory of legal income relative to private salaries, 1970–1990 | Pay trend |
| 9 | Composite (investigator-constructed from two questionnaire items) on the importance of civil-service exams for entry generally | Second, broader recruitment measure |
| 10 | Whether a public-sector career is the best option for graduates of elite universities | Prestige / attractiveness — a demand-side recruitment-pool proxy |

By content: **2 items on recruitment mechanism (2, 9), 2 on career/tenure stability (3, 5), 1 on promotion structure (4), 4 on career rewards, pay and prestige (6, 7, 8, 10)**, and 1 establishing agency relevance.

**[wiki synthesis — the limitation that matters most]** Every item is recoded into 2–3 categories and combined into **one aggregate scale before any growth regression is run. No component-level regression is reported anywhere in the paper.** So this source cannot tell you whether recruitment, tenure, promotion or pay is doing the work — only that the bundle correlates with growth. That is the same shape of limitation the wiki records for composite governance indices at [[dimensions-of-institutional-variation]] D90, and it is why the randomised, single-lever evidence on [[personnel-economics-of-the-state]] and the two-margin decomposition on [[civil-service-tenure-and-political-insulation]] are not redundant with this page.

**Two further design caveats, both the authors'.** The independent variable is a **retrospective expert description**, collected up to 23 years after the start of the growth window, resting on an assumption that bureaucratic structures are stable ("notoriously resistant to change") — tested only by asking the experts whether they observed change. And the three mechanisms the paper offers — competence and esprit de corps raising the internalised cost of corruption; long-horizon career rewards biasing officials toward investment over consumption; a competent bureaucracy lowering perceived investment risk and acting as an honest broker — are **asserted, never measured**. The authors say so: adjudicating between them "would be a challenging and worthwhile task, but it is not our aim here."

## Rauch: the Progressive-Era natural experiment

**[empirical — quasi-natural-experiment panel; the cleanest identification on this page]**

**Design.** 144 US cities with population over 30,000 in 1904, observed 1902–1931 — **3,312 city-year observations** — with city and year fixed effects. Three municipal reforms adopted at staggered, plausibly exogenous dates:

| Reform | What it changes | Role in the design |
|---|---|---|
| **Civil service** | Merit-exam hiring **plus** dismissal only for just cause, determined by a civil-service commission | The treatment |
| **City-manager** | A single appointed executive with no legal tenure protection, answerable to the council | Intermediate case |
| **Commission** | Multiple **elected** commissioners holding both executive and legislative power | **The control** — it changes structure without insulating any agent |

**Mechanism.** An explicit principal-agent argument (formalised in a companion paper, sketched here). Pre-reform, the bureaucratic agent's job tenure is tied to the same electoral risk as the council's. Post-reform, lifetime just-cause tenure **lengthens the agent's effective horizon relative to the principal's electoral horizon**. Infrastructure has a long gestation; current expenditure (police, fire, pothole-filling — and the patronage and kickback opportunities that ride on it) pays off immediately. A longer-horizon agent, using his informational advantage over budget preparation under imperfect monitoring, tilts allocation toward infrastructure. **The mechanism itself is not measured — only its predicted allocation consequence is.**

**Results.**

| Estimate | Value | Note |
|---|---|---|
| CIVSER on roads+sewers share (RS), fixed effects | **0.0147 (SE 0.0057)** | Significant at 1% |
| CIVSER on roads+sewers+water share (RSW) | 0.0079 (SE 0.0069) | Weaker |
| CIVSER on RS, dynamic/partial-adjustment long run | **0.022** | = 0.0120 / (1 − 0.4528); a 2.2pp steady-state rise in the road+sewer share of total municipal expenditure |
| City-manager government | ~0, statistically insignificant | |
| Commission government | **−0.0177 (SE 0.0059) on RSW; −0.0161 (SE 0.0049) on RS** | Negative and significant — reform without insulation moves the *opposite* way |
| Inferred effect on manufacturing employment growth | ~**+0.005** (0.5pp), ≈ ¼ of the sample's mean 2% growth | **An extrapolation, not a joint test** — see below |
| Manufacturing **value-added** growth | **Not statistically significant** | Reported here because the source reports it |

**Both halves of the growth result travel together.** The employment-growth effect is robust; the **value-added effect is not significant**, and the author attributes this to noisy value-added series rather than treating it as evidence against the effect. That attribution is his judgement, not a demonstration. Separately, the headline "economic significance" figure is constructed by combining *this* paper's infrastructure-share coefficient with a growth coefficient (0.21–0.26) estimated in a **different, companion paper** — an extrapolation across two estimations, not one system. The two corroborating case studies (the Port of New York Authority; Los Angeles) are illustrative anecdote cited for plausibility, not tests.

**[empirical — the design feature worth stealing]** The commission-government control is what makes this paper unusual. Commission reform changes municipal structure dramatically while insulating nobody, so it separates **"a reform occurred"** from **"insulation actually changed."** Its coefficient is negative and significant, which is stronger than a null: structural upheaval without agent insulation does not merely fail to reproduce the effect, it moves against it. Registered as [[dimensions-of-institutional-variation]] **D102**. A further check in the same spirit: interacting city-manager and commission adoption with a "later rescinded" dummy returns positive but insignificant coefficients, which the author reads as weak evidence against the story that reforms were rescinded because bad governments underinvested.

**Nominal versus actual accountability, cleanly instanced.** Under city-manager government the manager is *de jure* at-will, hireable and fireable by the council at any time. The tenure record says otherwise: of 48 cities surveyed by Stone et al. (1940), 23 had managers with effectively permanent tenure and 22 of the 48 managers served a single city for 10+ years. Bears on [[open-questions]] Q11.

**What Rauch declines to measure.** Corruption. He states an agnostic view on reform's effect on it in a footnote, so patronage and kickbacks are a **named but unmeasured** baseline in this paper, not a demonstrated one. He also flags the political-economy confound himself — the Hays/Weinstein thesis that Progressive-Era reform was driven by a corporate-minded businessman coalition, i.e. pro-growth reformers selecting into reform — and designs the commission control specifically against it.

## Why Rauch is anchored here and not on the personnel page

**[wiki synthesis — a placement decision, recorded because it was genuinely close]** Rauch is a personnel mechanism (recruitment method plus tenure protection) tested through a growth outcome, so it could equally have extended [[personnel-economics-of-the-state]]. It sits here for three reasons. (i) **Shared programme**: Rauch is a co-author of Evans & Rauch, frames his 1995 paper explicitly against the same Evans (1992) Weberianism measures, and the two papers test the same bundle by opposite methods — separating them would break the comparison that is the whole point. (ii) **The methodological contrast is the finding.** A correlational cross-section with acknowledged regional-dummy fragility and a within-country natural experiment with a control-group reform, agreeing, is a stronger statement than either alone; that argument only exists if they share a page. (iii) **Unit of analysis.** The personnel-economics page is built on micro-level randomised evidence with individual- or facility-level outcomes; Rauch's outcome is a municipal budget share and a city growth aggregate. [[personnel-economics-of-the-state]] carries a cross-reference to this page rather than a duplicate of the result.

## What this page does not establish

**[wiki synthesis]**

- **No component is isolated.** Evans & Rauch never decompose the scale; Rauch's civil-service treatment bundles merit hiring *and* just-cause tenure and cannot separate them. Guo Xu's review is where that separation is attempted — and its own headline case (Aneja & Xu on the Pendleton Act) attributes the gains to the tenure margin, not the exam margin. See [[civil-service-tenure-and-political-insulation]].
- **No causal claim survives untouched.** Evans & Rauch is correlational with a retrospective independent variable and self-reported robustness failures; Rauch is quasi-experimental with an extrapolated growth figure and an insignificant value-added result.
- **No age evidence.** Rauch's dynamic specification (lagged dependent variable ≈ 0.43–0.45) captures **persistence in the outcome** — multi-year project gestation — **not treatment-effect dynamics**. It is not a claim that the reform's effect grows or decays with years since adoption, and must not be read as one. Neither paper interacts reform with city size either.
- **No size evidence.** City population is a sample restriction and a control in Rauch, never a moderator. Evans & Rauch's one scale-adjacent result is about *government spending* share, not organisational size.
- **Public/private invariance: absent from both, in different ways.** Evans & Rauch study state bureaucracies only, and their own footnote 2 observes that new-institutionalist reasoning about mixing market and non-market governance "is rarely invoked in studies of state bureaucracies" — the authors flagging the two literatures as running on separate tracks. Rauch is silent; the one public/private analogy in his paper (Progressive-Era businessmen wanting the city run "as a large corporation") is about the *politics of reform adoption*, not about whether the mechanism transfers. Record as open for Q3, not as evidence either way.
- **Scope.** Evans & Rauch: 35 developing countries only, deliberately excluding advanced-industrial ones because Weberianness varies too little among rich countries; growth window 1970–1990. Rauch: US municipal government, population >30,000, 1902–1931, with several years of missing or incomplete Census data. Neither licenses a claim about advanced-economy national bureaucracies or about private organisations.
- **Ideological placement.** Evans (sociologist) and Rauch (economist) write explicitly against the "Smithian" laissez-faire view *and* against 1970s–80s rational-choice rent-seeking analysis, naming Buchanan/Tollison/Tullock and Krueger as the position they counter — i.e. directly against the camp on [[rent-seeking-and-the-welfare-cost-of-transfers]] and [[rational-actor-accounts-of-bureaucratic-behaviour]]. They align with the developmental-state case-study tradition (Johnson, Amsden, Wade) and with Evans's own *Embedded Autonomy*. This is a source written from inside a camp to supply that camp's missing systematic evidence, and its conclusions track its authors' priors; the disclosure of the regional-dummy fragility is what keeps it honest.

## Source

- `raw/research/bureaucracy-and-public-choice/04-evans-rauch-weberian-growth.md` — Peter Evans & James E. Rauch, "Bureaucracy and Growth: A Cross-National Analysis of the Effects of 'Weberian' State Structures on Economic Growth", *American Sociological Review* 64(5), October 1999, 748–765. https://akademik.apmd.ac.id/module/e_materi/file_upload/134118070420Text+-+evansrauch.pdf (JSTOR: http://links.jstor.org/sici?sici=0003-1224%28199910%2964%3A5%3C748%3ABAGACA%3E2.0.CO%3B2-G)
- `raw/research/bureaucracy-and-public-choice/05-rauch-progressive-era-bureaucracy.md` — James E. Rauch, "Bureaucracy, Infrastructure, and Economic Growth: Evidence from U.S. Cities During the Progressive Era", *American Economic Review* 85(4), September 1995, 968–979. https://econweb.ucsd.edu/~jrauch/pdfs/AER_Sept_1995.pdf

## Related

- [[personnel-economics-of-the-state]] — the same substantive terrain (recruitment, career structure, pay) at the opposite end of the evidence-tier spectrum: ~40 randomised experiments isolating single levers, against one aggregate correlational scale that is never decomposed. Rauch's natural experiment is anchored here and cross-referenced there.
- [[civil-service-tenure-and-political-insulation]] — where the entry-margin/progression-margin decomposition this page cannot perform is actually attempted, on a reform-evaluation evidence base that includes Rauch (1995) as one of its eleven studies.
- [[organizational-economics-of-the-state]] — Besley, Burgess, Khan & Xu's V-Dem "Weberian Facts" are a third operationalisation of the same construct, with the same proxy problem and the same authors' caveat that it is not causal.
- [[developmental-state-and-embedded-autonomy]] — the case-study tradition Evans & Rauch set out to test quantitatively, and whose authority (Evans 1995) they cite for their own investment-channel claim.
- [[goal-displacement-and-bureaucratic-ritualism]] — the mechanism Evans & Rauch name in footnote 7 as the reason they excluded rule-governed jurisdiction from the scale: rigidity and organisational sclerosis as the far side of the same design. A second source acknowledging Merton's tradeoff unprompted.
- [[credible-commitment]] — Rauch's mechanism is commitment via **agent** insulation (tenure lengthens the bureaucrat's horizon) rather than via constraint on the ruler; a distinct commitment technology that page's shackling-vs-self-restraint framing does not currently include.
- [[endogenous-state-capacity]] — Besley & Persson's fiscal and legal capacity is a different operationalisation of "state capacity"; this page's is personnel and organisational structure, with independent support.
- [[does-institutions-growth-survive-identification]] — Evans & Rauch is an additional cross-national growth regression using a wholly different identification approach (assumed structural stability rather than an instrument); a parallel case for that dispute, not a party to it.
- [[political-economy-of-public-sector-reform]] — Rauch's Hays/Weinstein confound (a businessman coalition drove reform adoption) is a concrete historical instance of the who-adopts-reform-and-why question.
- [[reform-levers]] — civil-service reform with just-cause tenure belongs near tier (i), with the caveat that identification rests on a control-group reform rather than random assignment.
- [[dimensions-of-institutional-variation]] — supplies **D102** (content vs. fact of institutional reform, from Rauch's commission-government control) and bears on D90's measurement-validity gate for the expert-survey scale.
- [[open-questions]] — bears on Q4 (selection, at recruitment and now at tenure), Q11 (nominal vs. actual accountability, via the city-manager tenure record), Q90 (this is one of the few sources decomposing below the national scalar) and Q101.
