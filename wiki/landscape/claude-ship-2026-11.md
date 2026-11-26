# Claude Ship (beta, 2026-11)

Anthropic's Claude Ship reviews GitHub pull requests, fixes them, and approves those a repository policy file allows. **Trial in observe-only mode; check eligibility first: Zero Data Retention, HIPAA-configured and customer-managed-key organizations cannot use it.** Vendor source only. The capture carries no publication date (TechCrunch URL dates the launch 2026-11-23; that article was not captured).

## Components (captured 2026-11-25)

| Component | Status | Role |
|---|---|---|
| Code Review | GA | Reviews PRs against the codebase through several lenses, adversarially verifies findings, posts them categorized |
| PR Steward | beta | Acts on failing CI, merge conflicts and review feedback; comments after each push with changes and how to undo them; `@claude stop`; designed not to approve or merge |
| Claude Approvals | beta | Approves per a policy file on the default branch; signals include Code Review findings and natural-language classifiers |

`/ship` is rolling out in Claude Code and the desktop app. Claude Team and Enterprise plans; works with existing branch protection and required checks. Admins enable per repository and can turn approvals off.

## Cost and limits (2026-11-25)

- Token-billed, driven by PR count and size, review level (Quick/Standard/Deep), frequency and Steward work. Monthly spend limits for Code Review and PR Steward.
- Claude Approvals has no base charge, but classifiers are token-billed, and a policy that uses Claude's review triggers a billed Code Review **even in observe mode**.
- Eligible Enterprise organizations: at least $10,000 in credits, claim by 2027-01-15, use within 30 days.
- Only GitHub is listed.

## Evidence

- Vendor-internal: on the Claude Code team, merged PRs more than doubled June to September and the reverted share fell over 40%. Cited for Code Review as one layer of a broader process, not for Claude Ship as a whole.
- Two customer quotes, unattributed in the capture. The vendor notes it may miss bugs and security vulnerabilities.

## Techniques worth stealing

- Observe before enforcing.
- Approval policy as a versioned repo file.
- Keep the fixing agent separate from the approving one.

## Build vs buy

The control point to watch is agent approval authority over merges. Treat the policy file and classifiers as security-sensitive code: whoever can change them can change what merges unreviewed *(inference)*. Policy and classifiers are Claude-specific, a switching cost *(inference)*.

## Source

- `raw/research/weekly-2026-11-25/01-claude-ship.md` (claude.com, captured 2026-11-25)

## Related

- [[llms/anthropic-claude-family]]
- [[landscape/agentic-compute-pricing-2026-04]]
- [[landscape/github-copilot-local-sandboxing-2026-10]]
- [[landscape/claude-unified-enterprise-2026-10]]
