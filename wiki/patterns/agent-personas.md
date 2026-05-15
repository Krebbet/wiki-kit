# Agent personas & personalities

What the evidence says about giving an agent a persona or personality via the system prompt — and what practitioners recommend doing anyway. Synthesised from three sources with deliberately different authority levels: a large-scale empirical study (Zheng et al., arXiv 2311.10054, "When 'A Helpful Assistant' Is Not Really Helpful"), a 2026 follow-up that decomposes the effect (Hu, Rostami, Thomason, arXiv 2603.18507, "Expert Personas Improve LLM Alignment but Damage Accuracy / PRISM"), and a practitioner tutorial (The New Stack, "How To Define an AI Agent Persona by Tweaking LLM Prompts"). The headline reconciliation: **a persona's value is task-type dependent — it helps alignment-style generation and hurts knowledge retrieval, and the two cancel so naive persona prompting nets ≈ zero on mixed workloads**. The older "personas don't help" null result is an aggregation artefact of exactly that cancellation. This page deliberately presents the practitioner advice *bracketed against* the empirical evidence rather than as standalone best practice.

## What practitioners recommend (practitioner-level, collect-but-confirm)

The New Stack tutorial frames the system prompt as the agent's "job description" — it persists across the conversation, defines the expertise domain, sets tone and communication style, and establishes behavioural boundaries. Its persona-design checklist:

- **Be specific and detailed** — explicitly define area of expertise, background, relevant limitations.
- **Use strong modal verbs** — instructive language ("must"/"should") to reinforce behavioural guidelines.
- **Establish boundaries** — state explicitly what the agent can and cannot do.
- **Incorporate personality traits** — communication style, formality level, distinctive characteristics.

Canonical prompt pattern: `You are a [role] with expertise in [domains]…` + directive clauses (provide X, always emphasise Y, **never** do Z, escalate to a licensed professional). Worked exemplars: financial advisor, e-commerce support rep, English tutor — each = (role + expertise) + (behavioural directives) + (hard prohibitions) + (escalation/disclaimer clause). Implementation: Claude `system=` parameter or OpenAI `{"role":"system"}` first message; a `persona`-property class spawns many domain-specialised agents from one codebase.

**These claims are practitioner-level — no measurements, benchmarks, or ablations.** The asserted benefits ("improved response quality", domain specialisation, consistent persona) are stated as best practice, not demonstrated. Per the wiki's source-authority weighting, the empirical findings below outrank them where they conflict.

## What the empirical evidence says

### Zheng et al. 2024 (arXiv 2311.10054) — the null result

A large-scale study: **162 personas × 4 prompt templates × 2,410 MMLU factual questions × 9 open-source instruction-tuned LLMs across 4 model families** (FLAN-T5-XXL, Llama-3-Instruct 8B/70B, Mistral-7B-Instruct, Qwen2.5-Instruct 3B–72B). Personas = 112 occupational + 50 interpersonal roles (categories: work, school, social, family, romantic, occupation, AI). Templates: No-Role control, speaker-specific ("You are a/an {role}"), audience-specific ("You are talking to a/an {role}"), plus an "Imagine…" paraphrase.

Findings (objective factual MC tasks only):
- **Adding a persona does not yield statistically better performance than the no-persona control** across all four families; effects are "no or small negative". Llama3-70B shows *more* negative-effect personas (possible scaling effect); Qwen2.5 is insensitive to all 162.
- **Domain alignment** (matching role to question domain) helps but with a tiny effect size (coef 0.004, p<0.01).
- **Gender-neutral roles significantly outperform gendered roles**; occupational gender composition is not a significant predictor (coef −5.79e-4, p=0.561). Ethics recommendation: prioritise gender-neutral roles.
- **Persona selection is near-random.** A per-question oracle ("best role per question") *does* yield significant gains — so correct personas exist per-question — but every automatic selection strategy (random, in-domain-best, similarity, RoBERTa domain/role classifiers) is only marginally better than random, and for Qwen worse than random. The effect is largely unpredictable.

**Scope caveat (important):** this tests *objective factual* accuracy (MMLU multiple-choice). It explicitly does **not** test subjective/style/safety uses of personas, which the authors acknowledge as legitimate reasons providers set roles.

### Hu et al. 2026 (arXiv 2603.18507) — the task-type decomposition + PRISM

This 2026 follow-up **refines rather than contradicts** the null result: it argues the null is an aggregation artefact and recovers a net positive via task-type routing.

**The central law — persona effectiveness is task-type dependent:**
- **Damages pretraining-dependent / discriminative tasks.** Every expert-persona variant underperforms base on MMLU: 68.0% (best, minimal persona) vs **71.6% baseline**; long persona worst at 66.3%. MT-Bench pretraining-heavy categories degrade: Coding −0.65, Humanities −0.20, Math −0.10. Hypothesised mechanism: persona prefixes activate an instruction-following mode that crowds out factual recall.
- **Boosts alignment-dependent tasks.** Long expert personas help 5/8 MT-Bench categories (Extraction +0.65, STEM +0.60, Reasoning +0.40, Writing, Roleplay). A "Safety Monitor" persona raises refusal on all three safety benchmarks; JailbreakBench +17.7% (53.2→70.9%) for long persona.
- **Naive persona prompting nets ≈ zero** because the two cancel (Qwen2.5-7B 72.2 vs 71.8 baseline; Mistral-7B actively hurt, 7.16 vs 8.74). *This is precisely the cancellation that produces Zheng et al.'s aggregate null.*

Secondary modifiers: longer personas amplify *both* directions (more knowledge damage, more alignment help); more instruction-tuning-optimised models (Llama) are both more helped and more harmed; reasoning-distilled models (DeepSeek-R1) gain only from *context length*, not expertise (and R1 distillation erased safety fine-tuning — 0% refusal).

**PRISM** (Persona Routing via Intent-based Self-Modeling) is the proposed mitigation: a fully self-bootstrapped pipeline (input = 12 domain names + an expert-persona template, no external data/models/annotation) that self-distils only the *beneficial* persona behaviour into a **gated LoRA adapter** with a binary gate that falls back to the unmodified base model when a persona wouldn't help. Five stages: query generation → with/without-persona answers → conservative self-verification (persona kept only if it wins both position-swapped orderings) → gate training on layer-0 hidden state → KL self-distillation of the winning persona-conditioned logits *without* the persona prompt. Net gain with knowledge preserved: Qwen2.5-7B +1.7 Overall (MMLU unchanged), Mistral-7B +1.6, Llama-3.1-8B +2.8. The gate correlates with task type (r=0.65) *with no task-type supervision*: ~6% of MMLU routed to the adapter vs 73–78% of safety queries.

**When persona routing is/ isn't worth it.** Worth it: instruction-tuned models on alignment-dependent generation (style, format, safety, preference). Not worth it: reasoning-distilled models (gate routes ~98% to base), MoE architectures (sparse activation breaks LoRA finetuning), already-narrowly-specialised models. Untested above 7–8B.

## Synthesis — what works, what doesn't *(editorial)*

Resolved tension, not an open conflict (per the conflict protocol — there is no impasse to elevate; Hu et al. explicitly reconciles Zheng et al.):

| Use case | Does a persona help? | Evidence |
|---|---|---|
| Objective factual recall (knowledge QA, MMLU, math, coding) | **No — net negative.** Persona prefixes crowd out factual recall. | Zheng (null), Hu (MMLU 68 vs 71.6) |
| Alignment-style generation (tone, formatting, writing, roleplay, extraction) | **Yes — reliably positive.** | Hu (5/8 MT-Bench categories up) |
| Safety / refusal behaviour | **Yes — strongly positive.** | Hu (JailbreakBench +17.7%) |
| Mixed workload, naive single persona | **≈ zero** (gains and losses cancel — this *is* the Zheng null) | Hu |
| Picking the "right" persona automatically | **Near-random** — don't expect a selection heuristic to help on objective tasks | Zheng |

Practical reading: the practitioner checklist (boundaries, escalation clauses, tone) is defensible *for the alignment/safety/style behaviours it mostly targets* — exactly where personas reliably help. Its unqualified "improves response quality" claim is wrong for knowledge-retrieval tasks. If a persona must coexist with knowledge work, the empirically-supported move is **task-type-conditioned routing** (PRISM) rather than a single static system-prompt persona. Two corroborating fragility data points: [[../case-studies/anthropic-claude-code-postmortem]] Bug 3 (a single brevity system-prompt instruction → ~3% eval drop) and [[agentic-harness-engineering]]'s ablation (+system_prompt only −2.3 pp) — both independent evidence that system-prompt prose is the *weakest, most fragile* layer to add behaviour at, consistent with the personas-hurt-knowledge finding.

## Source

- `raw/research/agentic-skills-personalities/05-05-helpful-assistant-personas.md` (https://arxiv.org/abs/2311.10054 — Zheng, Pei, Logeswaran, Lee, Jurgens; code+data released)
- `raw/research/agentic-skills-personalities/06-06-prism-expert-personas.md` (https://arxiv.org/abs/2603.18507 — Hu, Rostami, Thomason, USC)
- `raw/research/agentic-skills-personalities/07-07-newstack-agent-persona.md` (https://thenewstack.io/how-to-define-an-ai-agent-persona-by-tweaking-llm-prompts/ — practitioner tutorial; collect-but-confirm)

## Related

- [[agent-skills]] — the procedural-capability counterpart: how to package *what* an agent knows how to do, vs this page's *who* it acts as.
- [[externalization-survey]] — persona-via-system-prompt is the weights→context externalization arc; PRISM moves a context-level persona into weights via gated self-distillation.
- [[skillos]] — methodological sibling of PRISM: both are learned curation-of-behaviour over a frozen base (RL Markdown curator vs gated LoRA distillation); "small learned controller beats naive baseline".
- [[sierra-context-engineering]] — the "phrasing" / "rules" context-block types are the productionised superset of a single persona block.
- [[../case-studies/anthropic-claude-code-postmortem]] — Bug 3 system-prompt fragility corroborates the personas-hurt-knowledge direction.
- [[agentic-harness-engineering]] — +system_prompt only −2.3 pp; the prompt layer is empirically the weakest place to add behaviour.
- [[../conflicts/agents-md-effectiveness]] — same family of debate (does handwritten context/instruction text reliably help?); persona evidence is a system-prompt-layer data point.
- [[../deployments/anthropic-finance-agents]] — vendor packaging of "expert personas" as skills+subagents; PRISM is the empirical caveat that naive expert personas net ≈ zero on mixed workloads.
