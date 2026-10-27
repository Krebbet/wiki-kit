# Collusion Enforcement Audit

Tran and Yu (UMass, arXiv 2610.28787) propose a counterfactual "paired deviation" audit that tests whether cartel-like prices from LLM and RL agents are actually enforced by punishment. Applied to small RL-trained LLMs in a stylised trading market and a two-firm logit-Bertrand pricing game, it finds that most cartel-like outcomes are habits, deterrence, or thin by-product punishment, so outcome indices alone cannot identify collusion.

## Audit method (four parts)

1. **Paired deviation test.** Clone the market, force one agent to deviate for one period, and compare the rival's response against an undeviated copy under shared sampling seeds. Same-vs-same agreement of rival actions is 94-98% on vLLM-served models but only 23-45% via the OpenAI API, so the test needs controllable sampling.
2. **Placebos.** Lone agent, myopic agent (gamma = 0), and no-rival prompt, to separate habit from response to a rival.
3. **Scale sweeps.** Rescale currency or book depth. A true equilibrium keeps its collusion index; a fixed-markup or anchored rule does not. This part is outcome-only.
4. **Positive controls.** Agents told to punish, and tabular Q-learners, confirm the audit detects punishment when it exists.

## Findings

- Self-play yields fixed rules that ignore the rival.
- Against a punisher, agents learn to be deterred. Against a cheater, they learn to match price cuts (tit-for-tat) but not the costly price war, which they rarely try; war is learned only where forced.
- Matching agents can enforce, but thinly: 4 of 9 seeds, and only against large cuts (a 10% cut loses in 4 of 9 seeds, a ~16% best-response cut in 7 of 9).
- Tabular Q-learners enforce in the pricing game only.
- Prompted LLMs: 1 of 9 punish in pricing. Cartel-like outcomes come from depth-blind or anchored rules. What agents write about price wars often does not match what they do.

## Code and cost

Code and data: https://github.com/fatebreaker/rl-trading-collusion. Reported experiment cost about $245 in API calls.

## Limitations

- Small open models (Qwen3-0.6B/8B, Mistral-7B, gpt-oss up to 120B) and four OpenAI API models; no other frontier providers or tool-using agent scaffolds.
- Stylised markets: Kyle trading model with a fixed market-maker rule, and a Calvano-style two-firm pricing game. Punishment results are specific to these and to the prompts; trading levels are sensitive to wording.
- Negotiation, longer memories or explicit coordination devices may enable collusion not seen here.
- Preprint, not peer-reviewed. Transfer to deployed pricing systems is unestablished.

## Design input *(editorial, not source content)*

- The test needs counterfactual access (forcing a deviation and replaying under fixed seeds). Outsiders observing market prices lack it, so it fits regulator-mandated audits or simulation of a candidate algorithm, not crowdsourced observation.
- The scale-invariance screen is outcome-only and cheap: it can flag rule-based pricing from price data alone, though it cannot show enforcement.
- Positive controls and placebos are the part worth copying into any collusion-detection sandbox (see [[algorithmic-collusion]]).

## Source

- `raw/research/weekly-2026-10-26/07-enforcing-the-cartel.md`
  - **Origin:** arXiv 2610.28787, Tran and Yu, UMass.
  - **Audience:** AI-safety, algorithmic-collusion and evaluation researchers.
  - **Purpose:** methodological audit plus empirical evidence on what RL teaches LLM agents in markets.
  - **Trust:** preprint, not peer-reviewed; authors self-flag limitations. Moderate-high on method, low-moderate on real-world transfer.

## Related

- [[algorithmic-collusion]] — parent page; enforcement-vs-outcome section
- [[oblivious-algorithmic-collusion]] — rival-ignoring rules also give cartel-like outcomes without enforcement
- [[learning-rate-delegation-pricing]] — learning dynamics as a determinant of supracompetitive outcomes
- [[pricing-algorithm-taxonomy]]
- [[fairness-testing-algorithmic-pricing]] — audit statistics for pricing algorithms
- [[dp-audit-methodology]] — audit method with positive controls
- [[transparency-tools]] — audit analogue; contrast: needs counterfactual access
- [[consumer-ai-assistant-market-simulation]]
- [[agent-mediated-negotiation-empirics]]
