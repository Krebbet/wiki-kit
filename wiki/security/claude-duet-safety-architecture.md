# Claude Duet safety architecture

Anthropic's vendor-primary post on the safety, privacy and security design of Claude Duet (a research-preview, always-on cloud personal agent) describes four distinct mechanisms: an approval gate backed by an out-of-model classifier derived from Claude Code auto mode, a new outbound-message sensitive-information classifier, credentials that never enter the model's context, and a browser isolated in its own VM. The post is a design description and is trustworthy as such; it publishes no pass rates, attack-success numbers or classifier accuracy, so efficacy is unverified. Anthropic says approval cadence, sign-in and classifier accuracy are still changing.

## Mechanisms

- **Approval gate plus out-of-model check.** Before sensitive sends, payments or deletions, Duet shows the action, destination, content and every recipient and waits for approval. A separate automated check runs alongside each action, built on the [[governance/claude-code-auto-mode]] classifier extended for Duet, and runs outside the working model so instructions embedded in pages cannot influence it. The same safeguards apply to unattended routines.
- **Tiered permissions.** Some actions are off-limits even with approval (trading securities, moving money between accounts, accessing someone else's account). Others are excluded from "don't ask me again" rules however often approved (paying or sending money, deleting an order, creating an account). The post names approval fatigue as a calibration problem but gives no thresholds or rates.
- **Outbound sensitive-information classifier.** A new classifier, separate from the main model, checks each drafted message before sending. "Never share" (credentials, full card or bank numbers, government IDs) is blocked even if the user asks; "Needs consent" (health, finances) treats the user's own request as consent. On a block the agent may rewrite the message without the sensitive content and resubmit for approval. Browser file uploads get the same check. The post admits misses and false flags.
- **Credential isolation.** The model never sees passwords, cookies or tokens. Passwords go into an in-app form, are encrypted with a single-use key that exists only on the cloud browser machine, and are passed unopened to the browser (a 1Password flow is planned). Service tokens follow the Claude Managed Agents design (see [[deployments/anthropic-dynamic-workflows]]): a placeholder sits on the agent machine and a proxy outside it injects the real value at request time. Purchases use a one-time, merchant- and amount-limited Link (Stripe) card approved in the Link app. The sign-in form appears only inside the app, never via link, email or text, as a phishing caveat.
- **Browser isolation.** The browser runs in a dedicated VM separate from the model and the agent's compute; the agent drives it through a fixed command set (open, click, type) and cannot read cookies. Page text and downloads do return to the model, so the prompt-injection safeguards from Anthropic's browser-use research remain necessary. The post acknowledges this as residual exposure. The agent self-identifies via a distinct User-Agent and published IP ranges; some large sites chose to block it.

## Testing method

Safeguards-team evals built from routine-shaped tasks in three variants (innocent, injected instructions, temptation to overreach), run alongside shadow traffic from real use; internal red teams; a system-wide threat model; an external pen-test firm with source access (a follow-on covering the cloud browser and sign-in form is in progress); and inclusion in the public HackerOne bounty. No results are published.

## Memory and visibility

Duet keeps conversation history and memory across tasks and also reads the user's Claude account memory. Disconnecting an app stops new access, but already-learned content persists until memory reset. Users get a task list with per-task pages and mid-task steering.

## Assessment

- Vendor-claimed throughout; the closed product releases no code, data or evals, and the post contains no quantitative claims.
- The distinctive contributions are the outbound-content classifier (a data-loss-prevention layer on what the agent says, not only what it does) and the structural separation of secrets and browser state from the model. These limit what a successful injection can reach rather than claiming to detect it.
- Residual exposure is stated: page text still reaches the model, so injection can still steer drafts; the out-of-model classifier and human approval are the backstops.

## Source

- `raw/research/weekly-2026-10-25/02-claude-duet-safety.md` — Anthropic, claude.com resources article on Claude Duet safety, privacy and security, captured 2026-10-25. Vendor primary source; design statements trustworthy, efficacy unquantified.

## Related

- [[governance/claude-code-auto-mode]] — classifier Duet reuses, extended and run out-of-model.
- [[conflicts/auto-mode-prompt-injection-defense]] — Duet adds a sixth reinforcing layered-defense data point (still OPEN).
- [[deployments/anthropic-dynamic-workflows]] — Managed Agents credential-proxy design Duet reuses.
- [[deployments/anthropic-commerce-agents]] — payment safety, scoped one-time cards, sanitize-and-fence.
- [[security/microsoft-execution-containers]] — infrastructure-enforced containment vs. Duet's VM and proxy separation.
- [[security/nvidia-open-agent-safety-platform]] — out-of-band monitor outside the agent's trust boundary.
- [[governance/claude-code-review-at-anthropic]] — risk-tiered human-approval layers.
- [[deployments/openai-dots]] — comparable always-on cloud-computer personal agent.
- [[deployments/nanomuse]] — Sentinel deterministic action gate vs. approval plus classifier gate.
- [[patterns/personal-agent-protocol]] — agent self-identification (User-Agent, published IPs) vs. OAuth-session approach.
- [[deployments/mcp-infrastructure]] — agent identity and delegated-credential roadmap.
