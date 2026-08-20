# Motivation Crowding

An extrinsic incentive attached to a behaviour can reduce that behaviour. This is the second of the two mechanisms by which high-powered incentives backfire (the first, attention reallocation across tasks of differing measurability, is on [[multitask-incentive-theory]]), and unlike that one it does not require multiple tasks at all — it operates on a single task, holding the agent and the measure fixed, by changing the agent's *disposition* toward the activity rather than the *allocation* of effort across activities. Two sources in this wiki give the phenomenon a mechanism, and **they give two different mechanisms**, which this page keeps apart. Frey's motivation-crowding theory is psychological: an intervention perceived as *controlling* shifts the locus of control outward and signals distrust, damaging perceived self-determination and self-esteem; an intervention perceived as *supportive* crowds motivation *in*. Bénabou & Tirole's is Bayesian and informational: the principal knows something the agent does not, so the agent rationally reads the *size* of the offered reward as a signal — and under a sorting condition, a large reward is equilibrium evidence that the task is unattractive or the agent is thought to be weak. Same observable phenomenon, incompatible underlying stories, different corollaries for design.

**Evidence tier note — read before citing anything on this page.**

- **The Bénabou-Tirole material comes from a 29-page slide deck, not the *Review of Economic Studies* article it presents.** Derivations, robustness checks and the literature review that would appear in the published paper are compressed or absent. **The deck contains no empirical test of its own propositions.** The empirical material it gestures at (Lepper et al. 1973; Deci & Ryan 1985; Etzioni 1971; a Baron & Kreps 1999 quote) is pre-existing external psychology and HR literature that *motivated* the model — it is not a test of the model's comparative statics, and no data are shown confirming that the sorting condition holds in any real reward scheme. Every empirical-sounding claim in that section is **asserted, not shown**, and none of it should be cited as if verified by the peer-reviewed article, which is not what was read. Tier: **(b) formal model, presented in abbreviated form.**
- **Frey is a survey, not a model and not primary evidence.** Condensed from Frey & Jegen (2001), it presents no equations, no utility function and no untested construct of its own beyond a qualitative supply-curve diagram; its "theory" section is Frey's synthesis of Deci & Ryan's self-determination theory. Its evidence is other people's, of **uneven rigour**, and its strongest civic and policy examples are concentrated in **Frey's own prior work** (Frey & Oberholzer-Gee 1997; Frey & Götte 1999; Feld & Frey 2002; Frey 1997b). The conclusion's claim of "strong empirical evidence... collected in many different countries" therefore rests disproportionately on one research programme rather than on independent multi-lab replication. Tier: **(a) empirical, but per-study — see the grading table below.**
- **Frey does not himself flag the selection problem.** He uses "crowding-out" language uniformly across randomised lab experiments and cross-sectional field correlations alike, and nowhere argues away selection as an alternative explanation for the field results. Several of his most institutionally relevant studies — paid volunteering, tax morale, constitutional trust — are exactly the cases where selection or reverse causation is live and unaddressed. **This wiki attaches that caveat; the source does not.**
- The two mechanisms' psychological constructs — "perceived self-determination," "perceived self-esteem" — are **not directly measured** in most of the cited field studies. They are imputed post hoc to explain a behavioural result. This is the reason Frey's central axis is refused admission to [[dimensions-of-institutional-variation]].

---

## Mechanism A — self-determination and self-esteem (Frey)

**[framework — Deci & Ryan lineage, synthesised by Frey]** The causal chain: an extrinsic intervention (a price, a sanction, a rule, a monitoring regime) changes the individual's perceived locus of control and their sense of whether their competence and motives are acknowledged; that changes intrinsic motivation; that changes behaviour. The claim with teeth is that this **indirect channel can outweigh the direct relative-price effect** — so the supply curve can shift by more than it moves along.

Two channels, stated separately:

1. **Impaired self-determination.** An intervention perceived as controlling shifts the locus of control from internal to external. If the person continues to behave the same way afterwards, the behaviour now reads as compliance or payment-seeking rather than as an expression of their own values — they are "over-justified" — so intrinsic motivation is substituted by extrinsic control and the intrinsically-caused portion of effort declines.
2. **Impaired self-esteem.** An intervention carrying the implicit message *we do not trust or acknowledge your motivation or competence* is experienced as a rejection of the person's involvement, lowering the self-worth attached to the activity, and effort falls in response.

**The conditioning variable is perceived valence, not the presence of an incentive.** Controlling interventions crowd out (both channels damaged); **supportive** interventions crowd *in* (self-esteem boosted, perceived self-determination enlarged). This is the axis Frey proposes as his central contribution.

**[wiki synthesis]** It is also the axis this wiki declines to admit to the framework register, and the reason is precise: Frey supplies **no operational procedure for determining ex ante whether a given intervention will read as controlling or supportive**. He gives examples on both sides (verbal rewards positive; unexpected or non-contingent tangible rewards do not crowd out; loose collective blame attribution beats individual attribution) but no rule. In practice the label is applied *after* the behavioural result is known, which makes the axis unfalsifiable as stated. Recorded as a `rejected` row at [[dimensions-of-institutional-variation]] D52 with a readmission condition, so the problem stays visible rather than being silently dropped.

### Grading the evidence

**[empirical — per study]** The distinction that matters is whether the design holds the population fixed. Where it does, a behavioural change is an incentive effect. Where it does not, selection is an unexcluded alternative.

**Clean incentive-effect evidence (population held fixed by design):**

| Study | Design | Finding |
|---|---|---|
| Deci, Koestner & Ryan (1999) | Meta-analysis of 128 lab experiments; randomised assignment within subject pool | Tangible contingent rewards significantly reduce intrinsic motivation for interesting tasks; **verbal** rewards significantly increase it; tangible rewards do **not** crowd out when unexpected or non-contingent |
| Gneezy & Rustichini (2000a), Israeli day-care | Same population observed before, during and after a fine for late collection | Late collections **increased** after the fine was introduced and **stayed elevated after the fine was cancelled** — the persistence is what rules out a simple price-substitution story |
| Fehr & Rockenbach (2003) | Lab, randomised | Sanctions crowd out altruism |
| Bohnet, Frey & Huck (1999) | Lab, enforcement level manipulated within design | **Non-monotonic**: near-perfect enforcement is fine (institutional trust substitutes for personal trust) and low enforcement is fine (intrinsic fairness motives crowd in); *intermediate* enforcement is worst for trust and reciprocity |
| Frohlich & Oppenheimer (1998) | Public-goods game, random payoff reassignment | Same subjects shift toward self-interest |
| Frey & Oberholzer-Gee (1997), Swiss nuclear-waste siting | Survey of the community selected by the national government to host the site | **50.8%** accepted the repository uncompensated; **24.6%** accepted when monetary compensation was offered. Clean *if* the split-sample was randomised — **the source's text does not specify the design**, so if respondents self-selected into which version they answered, selection contaminates it. Flagged as needing the underlying paper. |

**Field evidence where selection is a live and unaddressed alternative:**

| Study | Why it is contaminated |
|---|---|
| Frey & Götte (1999), volunteering | Correlational: receiving *any* payment reduces volunteer hours (~4 hours), though larger payments increase hours. Whether people who accept paid volunteer positions differ systematically from those who do not is never addressed. |
| Barkema (1995), managerial supervision | Cross-sectional comparison of performance under parent-company vs. personalised CEO monitoring. Which managers end up under which regime, and which firms adopt which structure, is not treated as a confound. |
| Austin & Hoffer Gittell (1999), airline delay attribution | Cross-carrier comparison. Airlines differ on culture, route networks, labour relations and fleet age; "team delay" framing is treated as the operative variable with no controls. |
| Tax morale and constitutional trust (Frey 1997b; Feld & Frey 2002; Tyler 1990) | Cross-country or cross-jurisdiction associations between trust-signalling institutions and compliance. Cannot separate "this constitution changed behaviour" from "high-trust populations adopt high-trust constitutions" — reverse causation at the polity level. |
| Cardenas, Stranlund & Willis (1999), Colombian forest commons | Described as a field experiment (externally imposed regulation *increased* forest destruction relative to a self-governed baseline). Too little methodological detail to confirm random assignment vs. comparison across already-different sites. |

**[wiki synthesis] Bottom line.** The mechanism is well demonstrated in the lab and in one field natural experiment (day-care). The field studies that matter most for *institutions* — volunteering, tax morale, NIMBY siting, constitutional design — are exactly the ones that are evidentially weakest on selection, and Frey's article does not flag the gap. Do not cite Frey & Götte or the tax-morale and constitutional-trust studies as clean incentive-effect evidence without that caveat attached.

### The measurability gloss

**[framework — Frey's interpretation, not a tested joint model]** Frey's one explicit measurability claim: pay-for-performance is well supported in "simple task environments" where output is cleanly measurable and intrinsic motivation "can be assumed to play no role" — his standing example is Lazear's windshield-mounting piece-rate study — and crowding-out is "far less likely" there than under "complex working conditions." The implication he draws is that complex tasks are precisely those where output is harder to measure and intrinsic motivation is doing more of the work, making high-powered extrinsic incentives both harder to design and more likely to backfire.

He names the two sides. **Low crowding risk / high measurability**: piece-rate manufacturing. **High crowding risk / low or contested measurability**: managerial judgment, volunteering, tax compliance, civic acceptance of unwanted facilities, creativity and entrepreneurship, and airline on-time attribution — where the "cause" of a delay is itself a contested sociotechnical measurement, which is Frey's explanation for why loose attribution outperformed precise attribution.

He does **not** formalise this. There is no model trading measurement cost against crowding cost; it is an interpretive gloss offered to explain why the Lazear result and the crowding results do not contradict each other. Label it as Frey's reading.

**A methodological failure mode he names, worth keeping:** "rash generalisation" from simple, measurable task settings to complex ones. A standing caution against using single-task, high-measurability incentive studies to justify institution-wide pay-for-performance design.

### Levers, with their evidence base

**[model]** (1) Prefer non-controlling interventions, or frame monetary ones as supportive, where intrinsic or civic motivation is doing real work — the central actionable claim, with **no operational recipe** for making an intervention read as supportive. (2) Avoid intermediate enforcement stringency: either near-perfect or low dominates a half-hearted middle — **a single lab result**, not policy doctrine. (3) Constitutional design extending trust and participation rights to citizens sustains tax morale better than "constitutions for knaves" — **Frey's own normative extension**, resting on his own correlational work. (4) Restrict high-powered extrinsic incentives to simple, low-intrinsic-motivation environments — **one field study contrasted against one piece-rate study**. None of these rise to a level the wiki should treat as settled.

---

## Mechanism B — reward size as a Bayesian signal (Bénabou & Tirole)

**Slide-deck caveat, restated because it governs everything in this section: the captured source is a 29-page presentation of the 2003 *Review of Economic Studies* article, not the article. It contains no empirical test of its own propositions, and the psychology it cites was the model's motivation, not its validation.**

**[model]** The setting is a dyad — parent and child, teacher and student, boss and employee, spouse and spouse — in which the **principal has private information the agent lacks**: about the agent's ability or the task's difficulty (Setting A, unknown θ), or about the task's cost and attractiveness (Setting B, unknown c).

The principal offers a contingent reward `b`, choosing it to maximise `θ[1 − G(σ*(b)|θ)][W − b]` — trading a higher probability the agent tries (via a lower effort threshold `σ*(b)`) against the cost of paying. The agent tries iff `E(θ|σ,b)(V+b) ≥ c`.

Because the principal's optimal `b` depends on what he privately knows, the agent can **invert** the choice of `b` to infer it. The equilibrium is monotonic under the **sorting condition** — the principal is systematically *more* tempted to offer a reward precisely when the agent's ability is low or the task is unattractive. Three propositions follow:

1. **Rewards are positive short-run reinforcers.** A higher reward still lowers the effort threshold, so current-period effort probability rises. The model does not deny that incentives work now.
2. **Rewards are bad news.** A higher observed reward correlates with the principal privately rating the task or the agent lower.
3. **Rewards undermine future self-confidence.** `E[θ|σ₁,b₁] > E[θ|σ₂,b₂]` for `b₁ < b₂` — the agent's posterior falls as the reward rises, **regardless of the realised action or outcome**, depressing intrinsic motivation for future similar tasks.

**Setting B gives the "forbidden fruit" result.** Where the principal knows the task's cost, a higher reward signals a *less attractive* task — so bonuses mark work as unpleasant, and activities that are unpaid and unconstrained are read as intrinsically more appealing. Illustrated with Tom Sawyer's fence and with English gentlemen driving coaches for pleasure. The same logic covers monitoring: close surveillance signals distrust and can produce the distrust it fears (cited to Pfeffer).

**The structural claim this yields.** A compensation scheme's *size* is not incentive-neutral information. It is itself a signal, and the sign of that signal's effect on future motivation is set by **whichever way the sorting condition cuts for the principal's own temptations**.

**The lever the model implies but does not state.** The backfire equilibrium exists only because the principal's temptation to reward correlates with bad news. Breaking that correlation — flat or non-contingent rewards, or delegating and reducing monitoring so that trust is what gets signalled — would remove it. **This is a corollary of the model's structure that the deck does not spell out and certainly does not test.**

**A separate power result worth recording.** In the "battle of the egos" extension, two parties hold *joint* formal control rights, and real bargaining authority is shown to flow to whoever can disclose private information that damages the other's self-confidence. **Nominal joint control is overridden by an informational asymmetry** — a mechanism by which formal and de facto authority diverge that is distinct from anything else in this wiki's power material.

**[wiki synthesis]** The **sorting condition** is the deck's load-bearing assumption and is refused admission to the framework register for the same reason as Frey's valence axis: the deck supplies no procedure for determining, from an institution's observable records, whether the condition holds — no data are shown confirming it holds in any real reward scheme. Recorded as a `rejected` row at [[dimensions-of-institutional-variation]] D53 with a readmission condition.

---

## Why these are two mechanisms and not one

**[wiki synthesis]** The distinction is not pedantic; the two accounts make different predictions, and the sources themselves keep them apart. Frey's paper does **not** draw a Bénabou-Tirole-style inference distinction — it does not model crowding as agents updating beliefs about task quality or their own ability from the principal's contract choice. Its channels are purely psychological, about the *meaning* the intervention carries for autonomy and worth. Bénabou & Tirole's mechanism, by contrast, requires no psychological damage at all: a fully rational Bayesian agent with correct beliefs updates downward because the reward is genuinely informative.

| | Frey | Bénabou & Tirole |
|---|---|---|
| Channel | Perceived locus of control; perceived acknowledgement of competence | Rational inference from the principal's revealed choice |
| Requires the principal to know something the agent doesn't? | No | **Yes** — this is the whole engine |
| Conditioning variable | Perceived valence: controlling vs. supportive | The **sorting condition**: does the principal's temptation to reward correlate with bad news? |
| Would crowding survive if the agent knew the principal's information? | Yes | **No** — the signal carries nothing |
| Prescribed fix | Change how the intervention *reads* | Break the correlation, e.g. non-contingent reward |
| Rationality assumption | Motivated psychology | Full Bayesian rationality |

**The sharpest discriminating test the two imply** — not proposed by either source — is transparency: publish the principal's information, and Bénabou-Tirole crowding disappears while Frey crowding does not. Neither source runs it.

## Relation to the rest of the incentive literature

**[wiki synthesis]** Crowding and multitasking are independent. Multitasking needs at least two tasks of differing measurability and works through the agent's attention constraint; crowding works on a single task and changes the agent's disposition or beliefs. An institution can suffer either, both, or neither. This is why [[multitask-incentive-theory]] presents "high-powered incentives: good or bad?" as resolving by scope rather than as a conflict — the informativeness principle holds for a single cleanly-measurable task, and these are two separate ways it stops holding.

Note also what the sources do **not** support. Bénabou & Tirole are explicitly a fixed-agent story: the agent whose beliefs update is the same agent throughout, and the deck has no stage at which heterogeneous types choose whether to enter. Neither source offers a *selection*-based account of crowding — that agents who would work for intrinsic reasons stop applying once the job is priced. That hypothesis is not in this wiki's sources. Frey's one selection-flavoured claim, that government employees accept lower pay because higher-intrinsic-motivation people self-select into public employment, sits in the same paragraph as a *crowding* claim (that increased supervision and reduced discretion erode that motivation) without the two being disentangled, and is correlational as stated.

## What is not established

- **No public-bureau evidence in Bénabou & Tirole at all.** The named contexts are parent-child, teacher-student, spouse, boss-employee, colleague. No public-sector example, statute or claim appears anywhere in the deck; whether the signalling mechanism survives in settings with compressed pay scales, no profit signal and a legislature rather than a residual claimant as principal is an open extrapolation.
- **Frey pools public and private without comparing them.** He mixes firm cases (Barkema, Lazear, the airlines, Bewley's employer survey) with civic and public cases (day-care fines, NIMBY siting, tax morale, constitutional design, volunteering, pollution-standard compliance, forest commons, adversarial dispute resolution, procedural fairness in legal authority) and never tests whether the magnitude or even the **sign** of crowding differs between them. Of roughly 13 distinct empirical studies, only three or four are squarely private-firm settings. **[wiki synthesis]** This source is therefore a better anchor for crowding in civic, regulatory and public contexts than for corporate pay design, notwithstanding its own framing as general economic theory.
- **Neither source says anything about scale or age.** No headcount, budget, hierarchy depth, or organisational age anywhere. Bénabou & Tirole's model is static and dyadic. Frey's nearest analogue is a claim about *task* complexity, which is not a scale claim and must not be read as one.
- **Neither source engages measurability heterogeneity across tasks.** Bénabou & Tirole treat reward as contingent on a single binary observable and say nothing about the multitask case; Frey's measurability material is an interpretive gloss, not a model.
- **Geographic and temporal narrowness.** Frey's evidence is Switzerland, the US, Israel and one Colombian field experiment, 1970s–2003, all developed-market democracies bar one. No authoritarian cases, no large-firm or multinational cases.

## Source

- `raw/research/incentives-and-institutional-form/08-frey-crowding-intrinsic-motivation.md` — Bruno S. Frey, "Crowding effects on intrinsic motivation" (condensed from Frey & Jegen, "Motivation Crowding Theory", *Journal of Economic Surveys* 15(5), 2001). https://www.bsfrey.ch/wp-content/uploads/2021/08/crowding-effects-on-intrinsic-motivation.pdf
- `raw/research/incentives-and-institutional-form/07-benabou-tirole-motivation.md` — Roland Bénabou & Jean Tirole, "Intrinsic and Extrinsic Motivation" — **a 29-page slide deck presenting the paper published in *Review of Economic Studies* 70(3), July 2003; not the article itself.** https://www.princeton.edu/~rbenabou/papers/IEM.pdf

## Related

- [[multitask-incentive-theory]] — the other, independent mechanism by which the same incentive backfires; the scope-resolution of "high-powered incentives: good or bad?" lives there.
- [[incentives-under-multiple-principals]] — Dixit's lever 5 (cultivate professionalism and mission where explicit incentives are weak) is the same intrinsic-motivation resource these sources say incentive design can destroy; neither source cites the other.
- [[governance-structures]] — Frey points at "the limits of the firm... in view of the possible limits of relying purely on extrinsic incentives" (Osterloh & Frey 2000) as a motivational alternative to Williamson's asset-specificity account of firm boundaries; recorded there as a fourth, weakest candidate.
- [[polycentric-governance]] — Ostrom's design principles turn on monitoring and graduated sanctions, which Frey's theory says can crowd out cooperative motivation. Frey's own conditions plausibly reconcile this (community-designed graduated sanctions read as legitimate and supportive; sanctions imposed by a distant authority read as controlling), and Cardenas et al.'s Colombian forest result is on Ostrom's side of it — but neither source states the reconciliation, so it stays a flagged tension.
- [[self-organisation-vs-property-rights-in-commons]] — Cardenas, Stranlund & Willis is a candidate mechanism for why externally imposed regulatory solutions can underperform self-organisation in that open conflict.
- [[credible-commitment]] — Frey's "constitution for knaves" argument concerns a constitution's stance toward *citizens*, where that page concerns constraints on a *ruler*; a parallel, not a merge.
- [[dimensions-of-institutional-variation]] — D52 and D53 record the two axes this page's sources propose and that the register **rejects**, with the reason and the readmission condition.
- [[open-questions]] — Q4 and the new Q37 (whether crowding has a selection channel at all).
