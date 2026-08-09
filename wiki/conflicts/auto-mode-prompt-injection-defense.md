# Conflict: Does Claude Code auto mode's 0% attack-success rate contradict the prompt-injection impossibility result?

**Status:** OPEN, likely reconcilable — the two claims plausibly operate at different defense layers (structural injection-detection vs. post-injection action-gating), but neither source states this distinction explicitly enough to close the conflict outright.

Anthropic's August 2026 auto-mode announcement reports a third-party evaluation (Trajectory Labs, 72 scenarios × 10 trials) in which 0 of 720 prompt-injection attempts succeeded against Claude models running auto mode. A May 2026 preprint (Abdelnabi & Bagdasarian, arXiv 2605.17634) derives an impossibility result: any defense that classifies information flows structurally (data vs. instruction) can always be evaded by an attacker who disguises an adversarial flow as contextually legitimate, or manipulates the agent's model of context norms. Read at face value, "0/720 successful attacks" and "structural defenses are provably evadable" sit in tension.

## Position A — Anthropic: auto mode empirically blocks all tested prompt-injection attacks

From [[governance/claude-code-auto-mode]]: Trajectory Labs' independent evaluation found 0/720 successful attacks against Claude Fable 5 / Opus 5 / Sonnet 5 running auto mode, versus 5.83% ASR for GPT-5.6 Sol in Codex's Auto-review mode and 19.03% ASR in Codex Full Access. Auto mode's classifier gates tool calls in real time — including an API-side prompt-injection probe that annotates ingested external content with a warning — and layers this on top of a hard-deny category for data exfiltration and destination-aware gating for git operations.

**Implication:** if taken as a general claim about structural prompt-injection defenses, this reads as strong empirical evidence against the impossibility result's practical bite, at least within the tested scenario space (72 scenarios, browser + tool-result vectors).

## Position B — Abdelnabi & Bagdasarian: structural defenses have a provable ceiling

From [[security/prompt-injection-impossibility]]: data-instruction separation — classifying information flows at the channel level — cannot fully distinguish attack from legitimate action, because an adversary can always construct a context under which a blocked flow appears legitimate (misrepresenting the flow, manipulating the norms, or mixing multiple flows). The paper's own related-work section already flags that the impossibility bound applies specifically to the **injection-detection layer**, and that defenses operating at the **action layer** — detecting whether a resulting action is malicious *after* injection has already succeeded — may fall outside the bound's scope, citing [[security/adr-uber-mcp-detection]] as a case needing full-paper review to place correctly.

**Implication:** if auto mode's classifier is better characterized as an action-layer gate (it evaluates the *tool call an agent is about to make*, not just whether the incoming content is data vs. instruction) rather than a structural injection-detection defense, it may sit outside the impossibility bound's scope — the same distinction this wiki already flagged as unresolved for ADR.

## Working position

This conflict is likely to resolve in favor of "different layers, not a contradiction," but neither source states the reconciliation explicitly:

- Auto mode's mechanism is described as gating *tool calls* based on classifier judgment of irreversibility/destructiveness/exfiltration risk — a description that sounds closer to the action layer (evaluating the consequence of an action) than to structural data-instruction separation at the injection-detection layer (classifying incoming content itself as data vs. instruction).
- However, auto mode *also* includes an explicit "API-side prompt-injection probe on ingested external content" — this piece does sound like injection-layer detection, which is exactly the layer the impossibility result targets.
- The Trajectory Labs eval covers 72 scenarios — a bounded, likely known-attack-class test set. The impossibility result predicts evasion specifically via *novel* contextual-manipulation attacks (misrepresenting flows, manipulating norms, mixing flows) that a fixed eval battery may not probe. A 0% ASR against a fixed scenario set does not contradict a claim that some unseen attack class remains findable — this is the same "structural defenses address a shrinking fraction of the attack surface as agents become more capable" caveat already on the impossibility-result page.
- Anthropic's own framing is consistent with this: the post explicitly states auto mode "does not eliminate risk" and keeps a non-classifier hard-deny category for the highest-stakes action (data exfiltration) precisely because the classifier is not treated as a complete defense.

Resolution rule: escalate to curator ruling once the impossibility paper's full text (currently only the abstract is captured) is reviewed, specifically to determine whether its action-layer/injection-layer distinction is developed with enough precision to classify auto mode's hybrid (content-probe + action-gate) architecture on one side or the other.

## Source
- `raw/research/weekly-2026-08-09/01-anthropic-auto-mode-default.md`
- `raw/research/weekly-2026-05-*` (prompt-injection-impossibility capture — abstract only; see [[security/prompt-injection-impossibility]] for capture provenance)

## Related
- [[governance/claude-code-auto-mode]] — source of Position A.
- [[security/prompt-injection-impossibility]] — source of Position B; already carries an open, structurally identical conflict flag against [[security/adr-uber-mcp-detection]] for the same action-layer/injection-layer question.
- [[security/adr-uber-mcp-detection]] — the precedent case for this exact reconciliation question; resolving one likely resolves the other.
- [[security/memory-poisoning-mpbench]] — adjacent, not identical: concerns persistent memory poisoning rather than in-session tool-call/browser injection.
