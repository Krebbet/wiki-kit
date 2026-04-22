# Framework Skepticism

The captured corpus converges, across lab and practitioner voices, on a skeptical stance toward agent frameworks. Not rejection — a warning that the abstractions have costs the glossy docs don't surface.

## The convergent claim

- **Anthropic (2024–2025):** "Frameworks often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug. They can also make it tempting to add complexity when a simpler setup would suffice." *(Lab blog — flagged as marketing-tainted; the mechanism-level claim about abstraction opacity is extractable from the framing.)*
- **Hamel Husain (2026):** rejects "tools-first" mindset; treats framework choice as a vanity metric relative to eval discipline. *(Practitioner-consensus.)*
- **arXiv taxonomy (2026-01):** surveys frameworks neutrally but notes the pace of churn and the difficulty isolating framework contribution from model-capability improvements. *(Literature-review observation.)*
- **Stanford 51-deployment playbook (2026-03):** *"Technology choice is commodity for 42% of deployments"*; durable advantage is the **orchestration layer**, not the foundation model. Multimodel abstraction layers that enable model switching recur as a pattern across successful deployments. *(Academic synthesis — see [[stanford-51-enterprise-playbook]].)*
- **Cursor (2025–2026):** built their own fine-tuned models (Fast Apply Llama-3-70b, Composer-1 RL-trained on Cursor bench) rather than chaining generic frameworks. Production example of prioritizing specialized FT + inference engineering over higher-level framework adoption. *(Vendor blog; see [[cursor-fast-apply]].)*

## Specific failure modes of over-frameworked systems

- **Debugging opacity.** Prompt-and-response traces buried under framework machinery. *(Anthropic, Hamel.)*
- **Incorrect mental models.** Developers assume framework internals work one way; bugs live in the gap. Anthropic calls this "a common source of customer error."
- **Premature complexity.** Frameworks make sophisticated multi-agent shapes one-line-able, encouraging premature adoption before it's earned.
- **Version churn.** Framework APIs break across minor versions; any wiki reference (including this one) goes stale within weeks without explicit version pinning. See the `/lint` model-version-pinning rule.

## MCP exception

**Model Context Protocol (MCP)** is the exception this corpus treats as *actually* stabilizing — cross-framework standardization for tool discovery and governance. Named in Anthropic's own engineering posts and the 2026 arXiv taxonomy as the convention with cross-framework buy-in. *(Emerging, 2024–2026.)*

If you're investing in any framework-level abstraction, MCP is the safest bet per this corpus. Note that MCP is *not* a framework in the Anthropic sense (one-line orchestration); it is a protocol layer *below* frameworks, defining how agents discover and invoke tools. Different category.

## The practical recommendation

The convergent advice across voices:

1. Start with direct API calls. Many patterns are 10–30 lines. *(Anthropic.)*
2. If you adopt a framework, **ensure you understand the underlying code** — not just the wrapper.
3. Pin framework versions explicitly in any reference material; unpinned references rot in weeks.
4. Measure whether the framework is actually saving you time before committing further. *(Hamel.)*

This is not "frameworks are bad." It is "frameworks should earn their place by measurable benefit, not by smooth onboarding."

## Source

- `raw/research/effective-agentic-patterns/01-anthropic-building-effective-agents.md` — Anthropic 2025 engineering blog.
- `raw/research/effective-agentic-patterns/04-hamel-field-guide.md` — Hamel Husain 2026.
- `raw/research/effective-agentic-patterns/08-arxiv-2601-12560-agentic-ai-taxonomy.md` — Arunkumar V et al., arXiv 2601.12560, 2026-01.

## Related

- [[building-effective-agents]]
- [[measurement-vs-architecture]]
- [[topology-taxonomy]]
