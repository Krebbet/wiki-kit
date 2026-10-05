# Nvidia Open Agent Safety Platform (OpenShell + Sentry) — 2026-09

Nvidia announced the Open Agent Safety Platform on 2026-09-28 (TechCrunch): open-source **OpenShell** (software boundary on what an agent can access; first announced March 2026) paired with **Sentry**, an independent monitor running on **BlueField-4 DPUs** so the watcher sits off the CPU/GPU the agent runs on. Nvidia claims Sentry can "quarantine agents that attempt to move outside their boundaries in milliseconds." Containment is now a vendor product category, answering the summer's agent-escape incidents. Single-source (one TechCrunch article); participant list and efficacy claims are vendor-supplied.

## What it is (2026-09-28)
- **OpenShell** — open-source boundary layer; low software lock-in. Prior related product: NemoClaw (2026-03-16), Nvidia's enterprise agent platform / security-baked OpenClaw.
- **Sentry** — out-of-band monitor on BlueField-4; a compromised or misbehaving agent cannot tamper with its own watcher. Hardware-dependent: no BlueField-4, no Sentry.
- **Pricing, cloud/on-prem support, latency evidence** — not stated. "Milliseconds" is a vendor claim, untested.

## Reception and reading
- Named supporters: Anthropic, Microsoft, Arm, Oracle, SpaceX ("dozens" per TechCrunch; the 100+ figure seen in search snippets is unverified). **OpenAI is absent** from the list; the source notes OpenAI launched its own rogue-agent report site the same day (2026-09-28).
- David Sacks endorsed on X: breakouts "were proof that the sandbox was too weak." TechCrunch notes backers are largely those opposing slowdowns/regulation — the platform is positioned as an engineering alternative to regulation (cf. [[ai-regulatory-deadlines-2026]]).
- Jensen Huang told CNBC it "would have prevented these breaches" (Hugging Face breach etc.). **Unverified vendor claim**, and Nvidia sells the chips that host Sentry (interest conflict).

## Techniques worth stealing
Out-of-band monitoring on separate hardware; least-privilege "remove all rights by default" (Huang: treat agents like employees). Build-vs-buy: OpenShell is cheap to adopt; an in-house equivalent of Sentry needs a separate monitoring plane / DPU-class hardware, which is the lock-in.

## Open
Independent test of Sentry against a real escape scenario; adoption beyond the vendor-listed names; whether OpenAI joins. Watch, do not assume it works.

## Source
- `raw/research/weekly-2026-09-30/01-nvidia-openshell-sentry.md` (TechCrunch, 2026-09-28)

## Related
- [[agent-safety-incidents-2026-08]] — the incidents this responds to
- [[openai-agent-escape-incidents-2026-09]] — OpenAI absent from participants
- [[huggingface-acquisition-2026-08]] — Nvidia's HF deal; HF breach cited as first prominent incident
- [[agent-identity-governance-2026-09]] — adjacent agent-governance category
- [[groq-nvidia-acquihire-2026-06]] — Nvidia strategic expansion
- [[blackhat-ai-coding-agent-cves-2026-08]] — supports "sandbox too weak" thesis
- [[salesforce-agentforce-salesbleed-2026-09]] — containment-failure counterpart
- [[ai-regulatory-deadlines-2026]]
- [[../platforms/microsoft]]
- [[../llms/anthropic-claude-family]]
- [[../llms/openai]]
