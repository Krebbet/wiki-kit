# Fine-Tuning vs Context Engineering

The decision framework distilled from five sources captured in the April 2026 research run. The corpus converges: **this is not a winner-takes-all question; it is a decision rule over task shape, data availability, and cost structure.** The two approaches are complementary and, increasingly, composable.

## The decision rule

| Axis | Favors fine-tuning (typically of [[slm-agents\|SLMs]]) | Favors [[context-engineering]] |
|---|---|---|
| Task stability | Stable, repetitive, narrow | Rapidly changing; behaviours discovered at runtime |
| Output shape | Strict schema, tool calls, fixed format | Variable, long-form, open |
| Knowledge currency | Training-time snapshot acceptable | Must reflect latest docs / data |
| Data availability | 10k+ task traces available | <1k examples; fast iteration |
| Cost shape | Inference dominates; scale matters | One-off or low-volume |
| Team skills | ML / infra team exists | App-layer team only |
| Behaviour stability | Behaviour internalization preferred | Behaviour under runtime control preferred |

*(Synthesis across all five sources — NVIDIA SLM paper, context engineering survey, SLM agentic systems survey, ACE, NVIDIA dev blog. Editorial framing of the rule; individual row citations below.)*

## What each source says

### Context engineering survey (arXiv 2507.13334, 2025-07)

Frames the two as **complementary, not substitutes**:

- *"In-context learning allows models to adapt to new tasks without explicit retraining … especially valuable in low-resource scenarios"* (§3.2.4).
- Tool use: prompt-based (no training), SFT (imitation), and RL (reward-driven) are three *coexisting* methodologies, not alternatives (§5.3.1).
- *"Modularity facilitates integration with fine-tuning and reinforcement learning, enabling customization for specific applications"* (§5.1.1).

### NVIDIA SLM paper (arXiv 2506.02153, 2025-06)

Argues the *practical* path is **fine-tune small, not context-engineer large**:

- LoRA/QLoRA fine-tuning of SLMs takes GPU-hours, not weeks — *"behaviours can be added, fixed, or specialized overnight rather than over weeks."*
- SLMs 10–30× cheaper than LLMs at inference. See [[slm-agents]].
- Once ≥10k task traces are collected, fine-tuning is "the obvious path." *(NVIDIA framing — lab source, pattern extractable, scope is SLMs specifically.)*

### SLM agentic systems survey (arXiv 2510.03847, 2025-10)

Independent empirical reinforcement:

- *"Specializing SLMs for agentic tasks is remarkably straightforward and efficient."*
- Recipe: log LLM usage → cluster tasks → LoRA/QLoRA per cluster → INT4/INT8 quantize → validators + routing.
- *"Compared to full LLM fine-tuning, these approaches can reduce GPU memory by an order of magnitude while preserving, or improving, quality on specific agent tasks."*
- Implicit position: **task specialization via FT beats scaling context** for structured agent workloads.

### Agentic Context Engineering (arXiv 2510.04618, 2025-10)

Shows the *other direction* — structured context engineering can rival fine-tuning without weight updates:

- *"ACE offers a flexible and efficient alternative to conventional model finetuning, as adapting contexts is generally cheaper than updating model weights."*
- Strong benchmark gains without retraining — see [[agentic-context-engineering]].
- Enables **interpretable selective unlearning** via context edits — impossible with weight updates.
- Explicitly **complements** FT rather than replacing it.

### NVIDIA dev blog (companion to the position paper)

*"You can choose a starting-point SLM for the agent based on general capabilities, and then improve it with finetuning."* FT-first for SLMs. *(Lab blog; marketing framing around NeMo tooling is extractable from the underlying pattern claim.)*

## Synthesis — the composable answer

The two camps dissolve once you separate two axes:

- **Model-size axis** (NVIDIA): don't use a frontier LLM for subtasks a 7B SLM can do. Fine-tune SLMs, route to LLM only for residual complexity.
- **Improvement-mechanism axis** (ACE): if you *are* keeping a capable model in the loop, you can improve it without FT via structured context evolution.

They compose. The production architecture implied by the corpus:

1. **SLM-default**, fine-tuned per task cluster.
2. **LLM fallback** for residual open-ended work.
3. **Context-engineering** (RAG + memory + possibly ACE) on the LLM side.
4. **Validators and uncertainty-aware routing** as the connective tissue.

See [[slm-agents]] for the full architecture and [[agentic-context-engineering]] for the context-side detail.

## Named production exemplars (2026-04 update)

The April 2026 `production-slm-case-studies` research run surfaced three named production deployments that instantiate the synthesis above:

- **[[cursor-fast-apply|Cursor Fast Apply]]** — *fine-tune small, data flywheel*. Llama-3-70b fine-tuned on real CMD+K usage, custom speculative-decoding variant, ~13× speedup vs vanilla. Classic FT-over-context choice for a narrow, high-volume, schema-constrained subtask.
- **[[perplexity|Perplexity]]** — *composed architecture*. Fine-tuned Sonar SLMs (Llama-3.1-70B base) for routine queries, cascade to GPT / Claude / Gemini on complexity. Classifier-based routing is the connective tissue. Demonstrates the composed SLM-first + LLM-fallback pattern at consumer scale.
- **[[stanford-51-enterprise-playbook|Stanford 51-deployment playbook]]** — *"multimodel strategies dominate"* across successful enterprise deployments. Task-specific routing, validation through redundancy, abstraction layers enabling model switching. Academic-synthesis validation of the composable answer.

## What the corpus still doesn't answer

See [[ft-vs-context-engineering]] for the detailed remaining-gaps list. Headline open items:

- Absolute dollar figures at production volumes (sources give ratios only).
- Named-company case studies with measured outcomes.
- Practitioner takes from Eugene Yan, Hamel Husain, Chip Huyen, Shreya Shankar on the FT-vs-RAG axis.
- Long-context vs fine-tuning head-to-head under common workload.
- When context engineering is actively harmful.
- Ablations of the composed SLM-first + LLM-fallback + ACE stack.

## Source

- `raw/research/fine-tuning-vs-context-slms/01-nvidia-developer-blog-slm-agents.md`
- `raw/research/fine-tuning-vs-context-slms/02-arxiv-2506-02153-nvidia-slm-agents.md`
- `raw/research/fine-tuning-vs-context-slms/03-arxiv-2507-13334-context-engineering-survey.md`
- `raw/research/fine-tuning-vs-context-slms/04-arxiv-2510-03847-slm-agentic-systems-survey.md`
- `raw/research/fine-tuning-vs-context-slms/05-arxiv-2510-04618-agentic-context-engineering.md`

## Related

- [[slm-agents]]
- [[context-engineering]]
- [[agentic-context-engineering]]
- [[reasoning-frameworks]]
- [[building-effective-agents]]
- [[cursor-fast-apply]]
- [[perplexity]]
- [[stanford-51-enterprise-playbook]]
- [[production-deployments]]
- [[ft-vs-context-engineering]] — remaining gaps
