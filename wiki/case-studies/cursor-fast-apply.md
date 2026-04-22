# Cursor — Fast Apply

Cursor's **Fast Apply** is a production deployment exemplifying the [[slm-agents|SLM-style task-specific fine-tuning]] pattern at the 70B scale. Fine-tuned Llama-3-70b + a custom speculative-decoding variant → ~1,000 tokens/s on the 70B model and ~13× speedup over vanilla inference. Published via the Fireworks vendor blog (Fireworks provides the inference stack).

## The problem

Frontier models struggled with large code edits: laziness, inaccuracy, high latency, and repetition loops in multi-line rewrites. Fast Apply is the subtask of *applying proposed code changes to files* — distinct enough from general code generation to warrant a specialized model.

## Architecture / method

- **Base model:** Llama-3-70b, custom fine-tune internally named *llama-70b-ft-spec*.
- **Training data:** synthetic, generated from real **CMD+K prompts and instant-apply inputs** — the training set derives from Cursor's own production usage. **Data-flywheel exemplar.** See [[slm-agents#the-data-flywheel]].
- **Speculative decoding variant — "speculative edits":** long speculations validated with greedy generation (temperature = 0), then generation resumes respecting the request's normal parameters.
- **Inference:** Fireworks inference stack with the speculative-decoding API flag.

## Measured outcomes

- ~**1,000 tokens/sec** on the 70B model (≈3,500 characters/second).
- **~13× speedup** over vanilla Llama-3-70b inference.
- **~9× speedup** over Cursor's prior GPT-4 speculative-edits deployment.

*(Evidence class: Cursor-measured but published via Fireworks vendor blog. No reproducible benchmark code or independent verification. Speedup magnitudes consistent with speculative-decoding literature but not externally audited.)*

## What the post does not cover

- Token-accuracy or quality metrics — speed is the headline, quality is implicit.
- Model-size tradeoffs (why 70B specifically, not a smaller specialized model).
- Cold-start or non-speculative fallback latency.
- Applicability beyond code-rewriting tasks.
- Cost-per-token economics.

## Wiki-lever mapping

- **SLM-style task-specific fine-tuning at the 70B scale.** Extends the [[slm-agents|SLM agents]] thesis upward — "small" is workload-relative; 70B is "small" for the specialized-subtask-via-FT pattern if it's beating frontier-LLM latency on that subtask.
- **Data flywheel** — real CMD+K + instant-apply usage → synthetic training data → fine-tuned task-specific model. Archetypal pattern.
- **Speculative decoding** as a practical latency win, composable with fine-tuning.
- **Task decomposition** — *apply changes* was split out from *propose changes*, letting the specialized FT model focus on what it does well.

## Complementary deployment: Cursor's Composer

The Fireworks post references **Composer / Composer-1**, Cursor's RL-trained coding model, trained on *Cursor bench* (real agent requests from real users). Same data-flywheel pattern at a different layer of the stack. Details not in this source; worth a separate capture if Cursor publishes more.

## Source

- `raw/research/production-slm-case-studies/03-fireworks-cursor-fast-apply.md` — Fireworks vendor blog on Cursor's Fast Apply. Marketing-tainted framing around Fireworks' speculative-decoding API; the Cursor mechanism and numbers are the extractable content.

## Related

- [[slm-agents]]
- [[fine-tuning-vs-context-engineering]]
- [[agentic-engineering]]
- [[production-deployments]]
