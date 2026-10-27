# Agentic Privacy Preference Taxonomy

Kochar et al. propose a five-category taxonomy of enforceable privacy preferences for AI agents (A Presence, B Collection, C Secondary use/sharing/human review, D Persistence, E Autonomy), audit 30 AI assistants/agent platforms against it, and release eight open-source prototypes that extend Global Privacy Control (GPC) through MCP and A2A interceptors. Individual opt-out infrastructure with no collective layer; deletion rights are out of scope. Preprint; the audit is a snapshot of company documentation, not observed behaviour.

## Taxonomy

Default posture is data minimization: an agent does only what the task needs unless the user asserts otherwise.

| Cat. | Subcategory | Governs |
|---|---|---|
| A. Presence | A1 Integration | AI may not be added to a product without genuine consent (no silent enablement via updates) |
| | A2 Activation | No background/ambient agent unless affirmatively chosen; foreground on-demand use is implicit consent |
| B. Collection | B1 Input | Data the user knowingly submits, beyond what the task needs; discard once no longer necessary |
| | B2 Metadata | Passively generated signals (hover, dwell time, deleted text, location) not collected unless necessary |
| | B2a Delegated action | An agent's record of its own actions (which agents it called, when) kept only as needed |
| C. Secondary use, sharing, human review | C1 Secondary use (a targeting, b inference/personalization, c commercial and analytical incl. sale/sharing) | Any use beyond the requested task needs explicit user permission |
| | C2 Repurposing | Training, fine-tuning, improving, evaluating models |
| | C3 Sharing | How far data travels along sub-task chains across systems/agents |
| | C4 Human review | Provider staff, contractors, third-party reviewers reading inputs, outputs, action records |
| D. Persistence | D1 Post-task presence | Access, integrations, scheduled jobs removed on task completion (implies D2, D3) |
| | D2 Unprompted initiation | Persistent agent may not start tasks, monitor, or send check-ins unasked (implies D3) |
| | D3 Scope expansion | No new apps, devices, domains, roles, or access without approval |
| E. Autonomy | (none) | Which decisions the agent may make without referring back to the user; default is not to act unprompted |

Retention is handled prospectively under B (task-based rule), not as a separate category. Legally required exceptions are carved out.

## Audit (30 products, 18 companies)

- 788 settings/actions found; 567 (72%) map to a subcategory, 21 (3%) are retention-duration only, 200 (25%) fall outside.
- Opt-out of sale/sharing for advertising, incl. GPC (C1c): 14 of 29 products.
- Opt-out of analytics/product-improvement use (C1c): 7 of 29.
- Opt-out of human review (C4): 6 of 30.
- Revoke agent access and clear working state (D1): 11 of 28. Turn off memory (C1b): 18 of 28.
- "Temporary" modes still retain: 30 days (Claude incognito), 72 hours (Gemini temporary chats), 24 hours (Perplexity incognito); contrast B1 discard-on-completion.
- Only 40% of settings document their default state; 19% for opt-outs exercised by request to the company.
- Carve-outs weaken signals: legal holds, abuse prevention (Gemini API prompts kept 55 days), user-initiated feedback. Claude Code's classifier-approved action mode is cited as weaker than the E default.

## Prototypes

Eight prototypes mirroring real agentic apps (search, medical, memory, writing, booking and similar scenarios) show preferences integrated structurally into MCP and A2A: preference-checking interceptors and header signals enforce minimization at each delegation hop, and blocked writes are logged so enforcement is visible. Code: https://github.com/privacy-tech-lab/gpc-ai-agents-prototypes. Implementation examples are recommendations, not measured comparisons of latency or attack success.

## Gaps

- **No collective layer.** Per-user signals only; no bargaining or cooperative mechanism. The paper itself warns of choice fatigue and cookie-banner repetition. Contrast [[collective-bargaining-for-data]].
- **Deletion out of scope.** Retention is prospective; no retrospective deletion right. See [[dsar-and-data-deletion]].
- **Verifiability.** End-to-end verification and auditing of signals across multi-hop delegation chains is unsolved; mapping contextual integrity to technical task boundaries is open. Related: [[decentralized-agent-identity]].
- **Legal dependence.** Relies on a duty to honor signals (CCPA-style); no US federal framework for agents. GPC non-compliance on the web is already documented in [[regulatory-responses]].
- Outputs-based harms and manipulation are out of scope.

## Source

- **Raw capture:** `raw/research/weekly-2026-10-26/06-agentic-privacy-preferences.md`
- **Citation:** Kochar, Sugsavanvit, Gupta, Calandrino, Kumar, Frischmann, Zimmeck et al. "Privacy Preference Controls for Agentic Systems." arXiv:2610.29929 (UCSD, Wesleyan, Stanford, CMU, Villanova), 2026. Preprint, not peer-reviewed. Trust: medium-high; Zimmeck is a GPC spec co-author. Audit reflects documentation as of October 2026.

## Related

[[agent-interop-protocols]], [[credential-disclosure-assistants]], [[adversarial-prompt-injection-defense]], [[auto-enrollment-opt-out]], [[health-data-opt-out-dark-patterns]], [[dpagent-dark-pattern-repair]], [[transparency-tools]], [[ghost-tool-calls]], [[possible-strategic-levers]]
