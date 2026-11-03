# PrivacyTrace: Profile Inference from MCP Tool-Call Traces

Duan, Liu et al. (Shanghai AI Laboratory) show that ordinary, protocol-valid MCP tool-call traces (tool names, arguments, returned results, call order) are a behavioural side channel. An observer with no access to the conversation infers latent user attributes with 26.25% attack success (ASR) versus 17.97% for prior-only guessing, averaged over four attacker LLMs. Arguments and results carry most of the signal, and linking traces across sessions and servers raises ASR to 32.77%. Exact identifiers stay hard to recover. Preprint on synthetic users; no defense is evaluated.

## Benchmark and threat model

- **PrivacyTrace:** 1,000 population-calibrated synthetic profiles (17 ground-truth attributes each), 4,000 agent trajectories over four domains (travel, health, shopping, career learning), 25 real MCP servers, 67,950 tool-call records. Attackers: MiniMax-M3, DeepSeek-V4-Flash, GPT-5.5, Gemini-3-Flash.
- **Trace:** per call, server endpoint, tool name and schema, arguments, response. Excludes user dialogue and agent reasoning.
- **Semi-honest observers** that retain traces and run passive inference:
  - *Local observer:* one MCP server, sees only its own calls.
  - *Global observer:* a gateway or platform with persistent user identity, aggregates traces across sessions and servers.

## Results

| Finding | Value |
|---|---|
| ASR, trace vs prior-only | 26.25% vs 17.97% |
| Arguments / results over metadata + call sequence alone | +13.18 / +10.01 points |
| Cross-domain linked traces | 32.77% ASR |
| Exact identifiers recovered | 35 of 16,000 slots |
| Completion of remaining attributes, trace-conditioned vs prior-only | +3.30 points |
| Two-stage (partial profile, then completion) vs one-shot | comparable |

Example in the paper: geocoding results and requested transport modes and times support inferences about location, health condition and religion, none disclosed and none needed for the task.

## Limits

- Synthetic profiles and tasks; demographic margins match statistics but behavioural realism is not guaranteed.
- Two-stage behavioural account is not shown to describe one-shot attackers.
- Candidate defenses (query obfuscation, reducing exposed trace content, session isolation across services) are named but untested.

## Relation to existing wiki material

Extends [[ghost-tool-calls]] from leakage through unauthorized speculative calls to leakage through authorized, task-necessary calls. In the [[agentic-privacy-preference-taxonomy]] frame this is the harm that B2a (delegated-action records) and C3 (sharing along sub-task chains) aim to limit. Structurally similar to [[browser-fingerprinting]]: passive cross-session linkage builds a profile without explicit disclosure. Server operators have a commercial incentive to retain traces ([[the-firms-view]]).

## Counter-tool ideas *(editorial)*

- *(editorial)* Consumer-side gateway that strips or coarsens arguments and results, and rotates identity per server, targeting the global-observer linkage gain. Applies [[obfuscation]] at the MCP layer.
- *(editorial)* Use the released benchmark as an evaluation harness for such a gateway, as a [[transparency-tools]] style audit of MCP servers.
- *(editorial)* Linkage limits are the cheapest lever: the largest measured gain is from aggregation, not from any single call.

## Source

- **Raw capture:** `raw/research/weekly-2026-11-02/01-privacytrace-mcp-leakage.md`
- **Citation:** Duan, Liu, Liu, Zou, Hu, Liu. "How Much Can Tool Calls Reveal About You? Privacy Leakage from Tool-Call Traces." arXiv:2610.41885 (Shanghai AI Laboratory, UESTC, Univ. of Sydney), 2026. Code and data: https://github.com/AI45Lab/PrivacyTrace. Preprint, not peer-reviewed. Trust: medium.

## Related

[[ghost-tool-calls]], [[agentic-privacy-preference-taxonomy]], [[obfuscation]], [[agent-interop-protocols]], [[browser-fingerprinting]], [[adversarial-prompt-injection-defense]], [[transparency-tools]], [[dsar-and-data-deletion]], [[the-firms-view]]
