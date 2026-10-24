# PAR — Progress-Aligned Recurrence

Ant International / NUS (arXiv:2610.27628). Recipe for retrofitted looped LMs that extrapolate to 16× training length on sequential state tracking: train iteration k to predict the state after c·k operations (depth–length correspondence) and RMS-anchor the recurrent state to its first-iteration norm. Qwen2.5-0.5B trained on ≤32 swaps reaches 95.5% at 512 moves vs 55.7% for RLT. No code link in the captured text.

## Method
- Retrofitted recurrence (McLeish et al.): Qwen2.5-0.5B's 24 layers → prelude (1–8) / weight-tied core (9–16) / coda (17–24); adapter initialised to [0 | I]; gradients through last 8 iterations; classification head at the query position; no CoT tokens.
- Progress-aligned targets: L_PAR = Σ_k CE(Q(s_k), z_min(ck,d)) — iteration k must hold the answer after the first ck operations; forced depth R = ⌈d/c⌉ per batch (alternative "hold" schedule with heavy-tailed R).
- State-norm anchoring: rescale each token's state to the RMS norm of its first-iteration state (stop-grad reference) to keep the step map stationary.
- Parameter-free learned halting: existing coda head emits Yes/No "finished"; stop at first iteration with P(Yes)>0.5 confirmed by ≥6 of the next 8. Replaces ACT/PonderNet modules.
- Prefix self-distillation for tasks without step labels: truncated prefixes are valid shorter problems; EMA teacher KL target. Positional stretch (index ×[1,8]) fine-tune needed for the label-free variant.

## Results
- Swap-S5, train ≤32 moves (6 seeds): 256 moves 99.5±1.2 (RLT 97.3); 512 moves 95.5±11.0 (RLT 55.7±25.8; explicit CoT 0.8; vanilla Transformer 0.85). Single-query S5/A5: 100/100/99.3 at 2×/4×/8×; fixed-depth and random-R baselines extrapolate <2×.
- Both components needed (Table 7): final-answer-at-every-loop G≈2; aligned targets without norm G≈1.8; full PAR G=16 on all seeds. Warm-starting from a one-pass solver G≈1.4.
- Learned halting 92.9% at 16× vs oracle 93.2%. Prefix self-distillation 85% at d=256 on S5; with stretch up to 99.7% at 16×.
- Natural-language shuffled-objects tracking (≤16 swaps train): 94–96% at 32 swaps, 79% at 64.

## Caveats
- Large seed variance on bigger backbones (Qwen2.5-1.5B/3B/7B at 16×: mean 71.7/57.8/80.7, sd 33–43; non-monotonic in size; Qwen3 0.6B–4B at d=256: 36–53%). Halting, self-distillation evaluated only on 0.5B. RLT number copied from its paper (best split).
- Fails on parallel-frontier tasks (graph reachability <3.5×) — no canonical intermediate state. Not shown on open-ended reasoning.
- Consistent with [[recirculation]]'s claim that loop count alone doesn't help; PAR supplies the training signal that makes extra iterations useful.

## Source
- raw/research/weekly-2026-10-24/02-par-progress-aligned-recurrence.md (arXiv:2610.27628)

## Related
- [[hyperloop-transformers]] — weight-tied looped Transformer with a loop stabilizer
- [[recirculation]] — training-free depth recurrence
- [[hrm]] — recurrent latent reasoning with iteration supervision
- [[hrm-text]] — recurrent-depth LM
- [[gram-recursive-reasoning]] — recursive reasoning models
- [[ssm-tool-use-length-generalization]] — length generalisation via external memory
- [[mamba-3]] — state-tracking expressivity via SSM state
- [[latent-grpo]] — latent reasoning via RL
