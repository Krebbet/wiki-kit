# Cognition: What We Learned Building Cloud Agents

Cognition's April 23 2026 engineering post on the infrastructure underpinning Devin's cloud agents. Argues that VM-level isolation with hypervisor-level state snapshotting is the only viable foundation for agents that span the *async gaps* of real software development life-cycle work — the minutes-to-days waits between PR opens, CI runs, code reviews, retests, and follow-up commits. Frames enterprise adoption as two sequential phases: build the infrastructure, then redesign engineering processes around an "agents execute, humans direct/review/decide" operating model. Includes concrete deployment numbers from Itaú (largest private bank in Latin America, ~17,000 engineers, ~11 months in).

## Source

- `raw/research/weekly-2026-04-27/02-02-cognition-cloud-agents.md` — captured 2026-04-27 from `https://cognition.ai/blog/what-we-learned-building-cloud-agents`.

## Phase 1: infrastructure

### VM-level isolation as industry consensus

> "The industry consensus for running untrusted code is VM-level isolation — each workload gets its own kernel, with no shared attack surface."

Cognition's microVM implementation took "over a year of hypervisor engineering." Each session runs on its own dedicated kernel with isolated storage, networking, and compute. Side benefit: agents can use a full browser, desktop applications, and arbitrary tool stacks — the same workstation that a human engineer uses.

### Containers cannot survive the async gap

The defining property of real engineering work is asynchrony: an agent opens a PR, waits on CI, responds to review, retests, pushes a follow-up. The gaps between steps are minutes, hours, sometimes days. Containers force a binary choice: burn compute to stay alive, or lose the session. Reschedules, time-outs, and crashes destroy the work.

For *bounded* tasks (e.g., dependency upgrades), a single-pass container that completes and exits is sufficient. For work that spans the SDLC, it is not.

### Hypervisor-level snapshotting

Cognition's solution: snapshot full machine state (memory, process trees, filesystem) at the hypervisor level. Compute shuts down while the agent is idle and resumes exactly where it left off when the next trigger arrives — a CI result, a review comment.

> "Making this work reliably across thousands of concurrent sessions, each with different repos, dependencies, and runtime environments, took us longer than any other piece of infrastructure we have built to date."

### The three orchestration challenges

Even after isolation and persistence, running hundreds of cloud agents across an engineering org requires governance, integrations, and scale. Cognition reports speaking with "a leading cloud data platform company [that] attempted this and ultimately moved on after the project scope overwhelmed their infrastructure team." The pattern across attempts is that the *combined surface area* becomes untenable, not any single component.

Cognition staffs "a dedicated team to manage each layer of this stack." The orchestration layer alone "took over three quarters of dedicated engineering to build."

## Phase 2: organizational redesign

> "Every engineering process inside an enterprise was designed for a world where humans do the work: how projects get scoped, how teams get staffed, how code gets reviewed and shipped. When agents are doing a significant share of the execution, those processes need to be rebuilt around a different operating model. One where agents execute and humans direct, review, and decide."

Phase 2 cannot start until Phase 1 is deployed, and fluency only develops "by operating with agents on real projects over months." This sequencing is the post's central organizational claim.

## Itaú deployment numbers

Eleven months in, ~17,000 engineers using Devin:

- **Migrations completed 5–6× faster.**
- **70% of static-analysis security vulnerabilities auto-remediated.**
- **Test coverage 2× the prior baseline.**

The post does not disclose seat count, concurrency footprint, or per-session cost — only outcome-level multipliers. Treat as Cognition-curated marketing data; the qualitative architectural detail elsewhere in the post is the load-bearing content.

## How this slots into the wiki

- **Async-gap framing as a topology entry.** The "container burns compute or loses state" failure mode is a distinct entry in the long-horizon-context-loss family — orthogonal to *context-window* exhaustion (which is what [[context-folding]] and [[anthropic-effective-harnesses]] address). This page covers *compute / state continuity* as a peer to *context continuity*.
- **Phase-2 framing parallels [[anthropic-internal-study]]'s engineer-as-orchestrator role shift.** The two are different vantage points on the same transformation — Cognition from the infrastructure-vendor side, Anthropic from the inside-the-shop side.
- **Three-orchestration-challenges framing parallels [[mcp-infrastructure]].** Both posts converge on a thesis that 2026-era enterprise adoption of agents requires serious governance and orchestration investment beyond the agent itself.
- **Practitioner-side counterpart in [[willison-cognitive-cost]].** The bottleneck Willison names — review and testing overload — is the human-side manifestation of the Phase-2 process redesign Cognition describes.

## From the Latent Space Interview (May 2026)

In a May 28 2026 Latent Space episode, Walden Yan provided richer primary-source detail on several architectural topics not covered in the original engineering post. The full treatment is in [[case-studies/latent-space-async-agents]]; key additions:

### Harness Architecture: Brain/Machine Separation

Devin separates the "brain" (LLM inference and decision logic, running on a separate control plane) from the "machine" (the sandbox VM that executes tool calls). This is the "out of the box" harness pattern. The practical security benefit: secrets scoped to the machine are inaccessible from the brain, and per-user GitHub app permission scoping is trivially enforced. The trade-off is additional state-management complexity across the control plane/sandbox boundary.

### Memory and Always-On Agents

Devin's memory system is called Knowledge. ~95% of memories are auto-generated (collect-but-confirm): when the user corrects Devin, it prompts to save the correction. Generation quality (avoiding over-generalisation from one-off requests) and retrieval precision (not flooding context from a large memory store) are the two active engineering problems. Cognition is exploring rebuilding memory as a file system the agent navigates natively, citing models' improving capability at file-system interfaces.

An emerging use case beyond coding: always-on agents as permanent product owners — maintaining a `memory.md`, triaging tickets, tagging humans on recurring priorities, and creating issues that humans or other agents then execute. Walden's framing: "How can we upstream above the engineering process?"

## Caveats

- Cognition is the vendor. The post is a primary engineering source on Devin's infrastructure choices but is not independent.
- Itaú numbers are uplift multipliers only; no absolute baselines, denominators, or attribution methodology disclosed.
- "Over a year of hypervisor engineering" and "over three quarters" of engineering are framed as moats; an org with serious infrastructure capability could in principle build either, and the post implicitly argues against doing so.

## Related

- [[case-studies/latent-space-async-agents]] — May 2026 Latent Space episode with Walden Yan; richer primary-source detail on brain/machine architecture, memory, multi-agent regime, and enterprise use cases.
- [[anthropic-effective-harnesses]] — peer Anthropic source on the same long-running-agent problem from the harness-design side rather than the infrastructure side.
- [[topology-taxonomy]] — adds *async-gap state continuity* as an axis to the long-horizon-context-loss synthesis.
- [[anthropic-internal-study]] — the engineer-as-orchestrator role shift this Phase-2 framing rebuilds processes around.
- [[willison-cognitive-cost]] — practitioner-side bottleneck that motivates Phase-2 redesign.
- [[mcp-infrastructure]] — parallel governance-and-orchestration thesis at protocol level.
- [[codified-context]] — context-continuity counterpart to this page's compute-continuity framing.
- [[ai-scientist-v2]] — adjacent multi-session async-tolerant pipeline; experiment-manager hierarchy faces analogous async-gap issues.
