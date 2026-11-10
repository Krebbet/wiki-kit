# Verification Windows and Treaty Decay

Gan (arXiv, Nov 2026, "Agreements Have a Clock") builds a calibrated takeoff model and a one-block, two-country agreement game to argue that a mutual pause on frontier AI is voluntarily supportable only while the time available to answer a secret advance (the "response window") exceeds a critical value, and that this window shrinks as compute keeps growing during the pause even though the visible capability gap stays fixed. For the wiki the portable content is the mechanism, not the AI setting: a fixed agreement erodes against a growing monitored stock, and a stationary indicator (the visible gap) masks decaying verifiability. Provisional, inter-state, and not a finding about institutions in general.

**Evidence tier note.** Status: **un-refereed arXiv preprint**, economics (JEL F51/F53/D74/O33). Tier (b) throughout: a formal model with derived propositions plus a numerical calibration; no data on actual AI outcomes or on real treaty lifetimes. The propositions are internally derived; the headline dates are conditional on chosen inputs. Claude was used to derive algebra and write simulation code (author-checked). The author self-cites a companion series. Everything here is **[model]** unless marked otherwise; read-across to human institutions is **[wiki synthesis]** and nothing in the paper states it.

## Scope: what is and is not being modelled

**[model]** Two sovereign states (leader and follower), each treated as a unitary actor with one frontier programme. Domestic labs and governments are collapsed into one national payoff; the paper says it does not solve the joint domestic-lab and government equilibrium. The institution being designed is a bilateral verification treaty: very small, new, two members, voluntary entry, no third-party enforcer. The scenario is a hypothetical 2026 US-China frontier-AI pause (the AI Futures Project "Plan A"). One review block is solved, with no repeated renewal or renegotiation. Findings are assumed truthful and public; governments are risk-neutral; "first-arrival closure" (the first state to a decisive milestone closes the game) is a substantive assumption, and independent closure gives much higher catastrophe probabilities.

**Kept apart.** The 12-month catch-up time, 6-month lag and 75% catastrophe figures are imported illustrative inputs from a scenario document, not measured. This page makes no claim about AI-risk magnitudes.

## The mechanism, step by step

1. **[model] Catch-up time exceeds raw lead (Prop. 1).** Follower diffusion fades as the gap closes, so the time to catch up is longer than the lead measured in time; the closed form is T* = ln(1+u)/delta. Prop. 2 gives the overtaking threshold: the gap converges to G* = (nu - a)/delta, so a follower whose own research speed a is at least the leader's speed nu eventually overtakes in finite time, and otherwise never does.
2. **[model] Credible response (Prop. 3).** After a truthful, timely finding, restarting is strictly optimal for a country iff (1-p2)chi*Z > c - d + (p2-p1)Y: the recovered strategic value, weighted by survival, must exceed the extra development cost and extra expected loss. A monitor that can reveal an advance still fails if the advancing country is better off than under compliance, so the sanction has to be worth carrying out.
3. **[model] Costed monitoring (Prop. 4).** Mutual compliance is supportable in equilibrium iff m_min = max xi_i/w_i <= m_max = min (C_i - R_i)/eta_i. Monitoring intensity needed to deter breakout must not exceed what either party will pay out of its cooperation surplus. Both prefer m* = m_min; strict deterrence and strict participation hold iff m_min < m_max.
4. **[model] The clock (Corollary 1).** During a compliant pause compute still grows, so catch-up time T_catch(d) is strictly decreasing and tends to zero. Mutual compliance at review date d requires T_catch(d) >= l + xi_B/m_max (l is implementation delay). The set of supportable review dates is therefore bounded, even though the visible capability gap has not narrowed. A state keeps the same visible lead and still loses time to act.
5. **[model] Widening the lead (Prop. 5).** Comparative statics of catch-up time: the semi-elasticity of T* with respect to follower research speed is minus the raw lead, and with respect to the diffusion rate it is minus (T* minus raw lead), so each lever buys window in proportion to those terms.

## Worked dates: conditional, not forecasts

**[model]** Under the chosen inputs (Y = 1, Z = 4, eta = 27, p0/p1/p2 = 0.1/0.2/0.4) the last supportable review falls at month 18.9. The paper states "No evidence guides Y and Z" and that dates are "not estimated treaty lifetimes". Sensitivities, all simulated inside the model:

- Doubling compute growth: 18.9 to 10.9 months.
- Halving monitoring cost: to 31.8 months.
- Matched, verified safety research as a treaty term: to 25.5 months; each point of p0 cut adds about 2 months.
- Each month of implementation delay cuts the date by roughly 4 months.
- Halving follower diffusion adds 2.9 months.
- A leader with larger control share (chi_A = 0.55-0.60) tempts the follower and pulls the date to 10.8 or 2.9 months. Near-peer parties shorten the window from the start.
- Domestic pacing rules can raise global risk when a follower races (catastrophe probability 80% to 97% and 87%), an AI-specific scenario result.

These support a mechanism and its direction, not a rate.

## Design variables the paper names

**[model]** Monitoring intensity and cost; detection and implementation delay; response window relative to the speed of the monitored thing; verifiability of terms; credibility of the sanction (Prop. 3); voluntary versus imposed entry; symmetry of the parties; a date-dependent detection standard that tightens over time versus a fixed one; scheduled review or restart dates; matched verified side-obligations that raise the value of cooperating. Levers are design principles from a hypothetical model, not tested reforms. Omissions the paper lists: false findings, private monitoring, endogenous compute investment, repeated renewal.

## Read-across to human institutions (wiki synthesis)

**[wiki synthesis]** The paper is silent on firms, regulators and domestic bodies; it borrows verification logic from START, Montreal and Paris, and does not claim transfer. Three candidate readings, all untested here:

- **Monitor outpaced by monitored capacity.** Any regulator or auditor whose response time is fixed while the regulated party's capacity grows exponentially faces the same shrinking window. The question for the wiki is whether this operates alongside, or independently of, capture ([[regulatory-capture]]); it is a different channel (speed, not incentives).
- **Stationary indicator, decaying quantity.** The visible capability gap is a poor measure of time-to-respond: a measure constant while the quantity it stands for decays. This fits the validity concerns in [[measurement-validity-framework]] and [[critiques-of-governance-indicators]].
- **Fixed rules ageing against a moving environment.** A fixed detection standard outliving the conditions it was designed for resembles drift, but here the decay is driven by an exogenous growing stock, not by rule accumulation, capture or inertia. It should not be cited as evidence on the age-decay question; it is a model with chosen inputs and no institution-level test.

## Candidate additions to the dimension register

**[wiki synthesis]** Two rows proposed for [[dimensions-of-institutional-variation]], status `candidate`, flagged as inter-state and untested at institution level: (1) response window relative to the growth rate of the monitored capacity; (2) monitoring cost as a share of the cooperation surplus (the m_min versus m_max interval).

## Caveats

**[model]** Results depend on stipulated payoffs, a stipulated follower path, a stipulated closure rule and an illustrative calibration, as the paper discloses. Power asymmetry and the question of who runs the monitor and how it is trusted sit outside the model. No rent-extraction analysis. Single review block only.

**Ideological priors.** Mainstream academic economist; accepts the AI catastrophic-risk framing and the scenario document's numbers as illustrative inputs; favours verified reciprocal restraint over unilateral pacing. Conclusions are hedged ("hard, but not out of reach").

## Source

- `raw/research/weekly-2026-11-10/03-agreements-have-a-clock.md` (arXiv 2611.04272, Li Gan, "Agreements Have a Clock: Compute Growth and the Verification of AI Restraint"). Read via the structured summary and targeted slices of the propositions; the appendix proofs and calibration were not independently checked.

## Related

- [[credible-commitment]] — Prop. 3 is a quantified credibility inequality for a restart threat.
- [[covenants-with-and-without-a-sword]] — the sword's credibility depends on time-to-respond.
- [[team-production-and-monitoring]] — monitoring cost priced against a cooperation surplus.
- [[agency-costs-and-ownership-structure]] — m_min / m_max as an inter-state analogue of monitoring and bonding costs.
- [[organizational-lifespan-as-commitment]] — scheduled expiry or review as a commitment device; also formal-only.
- [[measurement-validity-framework]] — stationary indicator masking decaying verifiability.
- [[critiques-of-governance-indicators]] — indicators misused beyond what they can bear.
- [[when-institutions-beat-intelligence]] — another provisional [model]-tier preprint in the AI-and-institutions space.
- [[regulatory-capture]] — contrast: monitored capacity outgrowing the monitor is a speed channel, not capture.
- [[dimensions-of-institutional-variation]] — candidate rows for response window and monitoring share.
