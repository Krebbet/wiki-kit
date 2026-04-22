# Perplexity — Multi-Model Answer Engine

Perplexity's production architecture (as documented in a third-party ByteByteGo systems-analysis) is a working instance of the [[slm-agents|SLM-default / LLM-fallback]] thesis applied to consumer-grade answer-engine workloads. Routing principle: *"use the smallest model that will still give the best possible user experience."*

**Note on source:** the wiki does not have Perplexity's own engineering material captured. This page relies on ByteByteGo's third-party architectural writeup. Cited architecture is reliable; business-moat framing is author synthesis — flagged inline where relevant.

## Five-stage pipeline

1. **Query intent parsing** — LLM-driven semantic parsing.
2. **Live web retrieval** — real-time; stated design principle *"you are not supposed to say anything that you didn't retrieve."*
3. **Snippet extraction.**
4. **Synthesized answer generation with citations** — citations inline, not as a separate link list.
5. **Conversational refinement.**

## Model portfolio

- **Sonar family** — Perplexity's in-house models, fine-tuned on open-source base (Llama 3.1 70B per the source's inference).
- **Third-party LLMs:** OpenAI (GPT series), Anthropic (Claude), Google (Gemini), xAI (Grok), Mistral, Moonshot (Kimi K2) — integrated via Amazon Bedrock.
- **Small classifier models** for intent classification and complexity scoring — drive the routing decision *before* any main-model invocation.

## Routing logic

- Small classifiers decide intent and complexity first.
- Simple definitions / lookups → smaller in-house (Sonar family) model.
- Complex multi-step reasoning → GPT-4, Claude Opus, or reasoning-tier models.
- Free vs Pro vs Deep Research product tiers receive different model mixes.

*(Evidence class: third-party systems analysis; routing rules described at the level of architectural principles, not cited code or exact classifier thresholds.)*

## Infrastructure

- **Vespa AI** as the retrieval substrate — unified vector search + BM25 lexical + machine-learned ranking in a single engine.
- **ROSE** inference engine — Python / PyTorch core, Rust for performance-critical serving paths.
- **AWS NVIDIA H100 GPUs on Kubernetes.**

## What's not in the source

- Specific latency, cost, or quality numbers — the ByteByteGo post is architectural, not benchmark-driven.
- Named Perplexity engineers.
- How the classifier models themselves are trained (likely SLMs fine-tuned on routing data, but not stated).
- Version pins for Sonar (open-source base inferred as Llama 3.1 70B; not explicitly stated).
- Explicit failure-mode discussion.

## Wiki-lever mapping

- **SLM-default routing** at consumer scale. Strong exemplar of [[slm-agents]].
- **Classifier-based intent routing** — the concrete mechanism behind the abstract "uncertainty-aware routing" named on [[slm-agents#architecture-slm-default-llm-fallback]].
- **RAG with strict grounding** — the "don't say anything you didn't retrieve" principle.
- **Multi-model composition** — contrasts with single-vendor reliance (cf. the [[klarna]] single-vendor lock-in lesson).
- **Context engineering** — retrieval / processing / synthesis pipeline matching the taxonomy on [[context-engineering]].

## Source

- `raw/research/production-slm-case-studies/05-bytebytego-perplexity-architecture.md` — ByteByteGo's third-party architecture writeup. Cites Perplexity engineering, Vespa engineering, AWS, NVIDIA in its disclaimer; promises a references section that didn't land in the capture. Treat cited architecture as reliable, business-moat framing as author synthesis.

## Related

- [[slm-agents]]
- [[context-engineering]]
- [[fine-tuning-vs-context-engineering]]
- [[klarna]]
- [[production-deployments]]
