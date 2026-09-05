# LatentPress

Zhou & Sang (Cornell/Iowa State, arXiv:2609.01507) introduce a WRITE/READ interface that compresses conversational history or long documents into continuous soft tokens consumed directly by a frozen decoder's input-embedding interface — no text reconstruction at inference. Matches or beats uncompressed-context and OCR-based compression baselines on LongMemEval at 4–16× compression, with an entirely frozen, unmodified decoder.

## Method

A small writer reuses the frozen decoder's bottom two transformer layers (deep-copied, never updated) as an encoder, then applies a trainable identity-initialized linear adapter to fuse literal token embeddings into fewer soft-token vectors at a hand-specified rate. Two pooling schedules: uniform, or role-based (conversational user turns kept lossless, assistant turns pooled 8–32×). Soft tokens are injected via `inputs_embeds`; only the adapter (4.2M–26.2M params, ~0.1% of decoder) is trained, via reconstruction cross-entropy + forward-KL distillation from the full-context teacher distribution.

## Results

On LongMemEval, uncompressed evidence scores 0.490; role-aware LatentPress reaches 0.504 at 7.70× compression — matching or slightly *beating* the uncompressed baseline while injecting far fewer vectors. Baselines degrade sharply as compression rises (ICAE 0.452→0.174, DeepSeek-OCR 0.426→0.312, text summary 0.184). Uniform (non-role) pooling collapses to 0.06–0.12 over the same range — the role-based allocation is load-bearing. Efficiency: writing is a single forward pass at 43ms/conversation vs. ~934ms for DeepSeek-OCR (~22×); reads are 5–9× faster than raw or cached-OCR context. On document QA (LongBench), in-domain adaptation lifts accuracy at 4× and often 8× compression but degrades at 16×.

Code released: github.com/HJSang/LatentPress.

## Applicability

Any project with a frozen decoder needing cheaper long-context/long-memory reading — conversational agents, RAG-style document QA, role-structured agent traces. No decoder fine-tuning; a small adapter trained on ~2,000 generic conversations transfers zero-shot to conversational memory. Best suited to mild-to-moderate compression (4–8×); one writer per target reader.

## Related

- [[delta-mem]] — parallel long-context technique operating at a different layer: δ-mem modifies attention/state internally, LatentPress is an external compression interface in front of an unmodified decoder.
- [[memagent]] — direct empirical contrast: MemAgent keeps memory as human-readable text (RL-trained buffer), LatentPress argues against text as the machine-facing interface and shows text summarization as the weakest baseline.
- [[sst-v2]] — third path in the long-context cluster (backbone-internal nonlinear state); LatentPress is again an external-interface alternative.
- [[neural-garbage-collection]] — contrasting compression mechanism: KV-cache eviction via RL vs. upstream soft-token compression via a frozen adapter.
