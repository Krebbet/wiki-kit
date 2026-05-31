# Prompt Injection Impossibility Result

A May 2026 preprint (Abdelnabi & Bagdasarian, arXiv 2605.17634) argues that the dominant defense strategy against prompt injection — separating data from instructions — is fundamentally insufficient. The paper goes further than cataloguing its failures: it derives an impossibility result showing that any norm-tightening defense will either miss attacks that disguise themselves as legitimate context, or block genuinely appropriate agent behavior. To explain why, the authors borrow Contextual Integrity (CI) theory from privacy research and use it to classify existing attack classes and predict future ones. The proposed alternative is CI-aware alignment, treating context-sensitivity as a first-class design constraint rather than an afterthought.

## Source

Sahar Abdelnabi, Eugene Bagdasarian. "AI Agents May Always Fall for Prompt Injections." arXiv:2605.17634 [cs.CR], submitted 17 May 2026.
URL: https://arxiv.org/abs/2605.17634
DOI: https://doi.org/10.48550/arXiv.2605.17634

**Note:** Only the abstract was captured. All claims below are sourced from the abstract only. The full paper may contain empirical scenarios, proofs, and nuances not reflected here. Treat specifics as collect-but-confirm until the full text is reviewed.

## Core argument

Data-instruction separation — the prevailing defense paradigm — fails in two distinct ways:

1. It does not detect prompt injection attacks that operate through **contextual manipulation** rather than explicit instruction injection. An adversary does not need to inject a recognizable command; manipulating the ambient context to shift what appears "legitimate" is sufficient to bypass the defense.
2. It **degrades contextually appropriate behavior**. A rule strict enough to block adversarial context flows will also suppress legitimate ones that share the same surface features. The defense is not merely incomplete — it actively impairs the agent in benign cases.

From these two failure modes the authors derive an impossibility result: an adversary can always construct a context under which a blocked information flow appears legitimate, and conversely, a defender who tightens norms will inevitably block some genuinely legitimate flows. No purely structural defense (one that classifies data vs. instruction at the channel level) escapes this bound.

The paper's prescriptive conclusion is that future defenses must be **context-sensitive** rather than structural, evaluating whether an information flow conforms to the norms of its context rather than merely identifying its syntactic form.

## The Contextual Integrity framework

Contextual Integrity (CI) is a privacy theory developed by Helen Nissenbaum that judges whether an information flow is appropriate by asking whether it conforms to the **norms of the context** in which it occurs. An information flow that would be appropriate in one context (e.g., a doctor sharing a patient's diagnosis with another treating physician) is inappropriate in another (the same doctor sharing it with an employer). Appropriateness is not a property of the data or the channel — it is a property of the flow relative to contextual norms.

Abdelnabi and Bagdasarian apply this lens to prompt injection: an adversarial payload succeeds when it induces the agent to accept a flow that violates contextual norms as if it were appropriate. Because the agent must evaluate context to act usefully at all, any defense that ignores context cannot fully distinguish attack from legitimate action.

CI also provides a **taxonomy** rather than just a critique: by characterizing attacks in terms of how they distort contextual norms, the framework predicts attack classes that have not yet been encountered, as agents become more autonomous and contextually capable.

## Attack typology

The abstract identifies three mechanisms by which an adversary can force an agent to violate contextual norms:

**1. Misrepresenting the flow.** The attacker makes a blocked information flow appear to be a legitimate one. The flow itself is adversarial, but its contextual framing is constructed to match the norms under which the agent would accept a benign flow. Detection requires evaluating the actual context, not the syntactic form of the instruction.

**2. Manipulating the norms.** Rather than disguising the flow, the attacker shifts the norms themselves — altering the agent's model of what the current context calls for, so that the adversarial flow becomes compliant under the modified norm. This class is particularly relevant to long-horizon agents that build up context over time.

**3. Mixing multiple flows.** The attacker combines flows from different contexts in a way that confuses norm evaluation. The agent cannot resolve which contextual norm applies and may default to a behavior the attacker can exploit.

These three categories are presented as both descriptive (accounting for known attacks) and predictive (anticipating attack classes that current research does not yet address).

## Implications for agent security

The impossibility result has direct consequences for how agent security should be approached:

- **Structural defenses have a ceiling.** Any approach that classifies channels or labels data vs. instruction at the pipeline level is bounded by the impossibility result. Incremental improvements to such defenses will address a "shrinking fraction" of the attack surface as agents become more contextually capable.

- **Detection and action layers may differ.** The impossibility applies to the **injection-detection layer** — determining whether a prompt injection is occurring. Defenses that operate at the **action layer** (detecting whether a resulting agent action is malicious, after injection has already succeeded) may be outside the bound's scope. This distinction matters when evaluating existing systems such as [[security/adr-uber-mcp-detection]], which targets observable malicious actions rather than injection detection per se. Whether ADR's approach escapes the impossibility bound depends on reading the full paper.

- **CI-aware alignment as a research direction.** The authors propose that alignment for frontier autonomous agents should be designed with contextual norm compliance as an explicit objective, not as a downstream property of structural rules. This would require agents to model the context of information flows and evaluate norm compliance as part of inference.

- **Scope widens with autonomy.** The attack surface governed by the impossibility result grows as agents become more autonomous and contextually capable. Systems that today face limited contextual manipulation (because they operate in narrow, well-defined contexts) will face a larger fraction of CI-class attacks as they are deployed in richer, more open environments.

**Conflict flag:** This paper's impossibility result is in tension with the framing of [[security/adr-uber-mcp-detection]] (which presents a two-tier LLM detector at F1 0.800, 0 FP as a viable production defense) and [[deployments/mcp-infrastructure]] (which treats indirect prompt injection as a manageable threat surface). The conflict may partially resolve if ADR is understood as operating at the post-injection action layer rather than the injection-detection layer. Collect-but-confirm pending full-paper review.

## Related

[[security/adr-uber-mcp-detection]] — ADR provides the detection infrastructure that CI theory says is insufficient for contextual attacks; the impossibility result bears directly on the scope of any norm-tightening approach, though ADR may operate at a different layer (action detection vs. injection detection)

[[deployments/mcp-infrastructure]] — MCP threat surface includes indirect prompt injection; the CI impossibility bound applies to defenses at the injection-detection layer of MCP pipelines

[[patterns/harness-design-space]] — safety is a dimension of the harness design space; the impossibility result implies that context-sensitivity must be a first-class safety constraint, not just a structural pipeline property
