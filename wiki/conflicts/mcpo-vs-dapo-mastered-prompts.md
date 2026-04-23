# MCPO vs DAPO — discard or regularise mastered prompts?

## Positions

**Position A — DAPO ([[../research/rl-optimizers/dapo]]).** *Dynamic Sampling* is one of DAPO's four headline tricks: filter prompts where all rollouts succeed ($p = 1$) or all fail ($p = 0$) before forming the GRPO gradient — those groups produce zero advantage and therefore zero learning signal, so including them wastes compute and adds noise. DAPO's empirical result (AIME 2024 50 pts on Qwen2.5-32B) is obtained *with* Dynamic Sampling in the recipe.

**Position B — MCPO ([[../research/rl-optimizers/mcpo]]).** Discarding *all-correct* prompts removes an *anchoring gradient* that would otherwise prevent policy drift on those prompts. MCPO Sec 4.1 Fig 2 shows that after mastery, unregularised drift causes ~5% one-step accuracy regression on mastered prompts — the student gets *worse* at problems it had already solved. MCPO's alternative: retain mastered prompts in the gradient, apply a hinge-KL regulariser that bounds drift between successive steps while leaving unmastered prompts untouched. Fig 5 shows MCPO achieves higher mastered-prompt fractions and lower all-wrong fractions than GRPO + Dynamic Sampling.

## Resolution rule

*(Open — no ruling yet.)*

The two positions diagnose *different* problems. DAPO's concern is *compute efficiency* and *signal-to-noise ratio* during training. MCPO's concern is *preventing silent regression on already-mastered capability* — which DAPO's filter cannot detect because filtered prompts produce no gradient either way. Both can be right: Dynamic Sampling is a sensible efficiency measure when the mastered-prompt set is stable, but falls down when the student can silently drift away from mastery in the absence of anchoring signal.

**What would resolve it:** a longitudinal tracking of *mastered-prompt retention rate* across training steps, comparing DAPO and MCPO on the same base model and prompt pool. MCPO provides this for a subset of conditions (Fig 5). A cross-paper replication on the same task would be dispositive.

**Relevance to the single-sample regime:** in single-sample or very small $N$ training, prompts naturally pass through the $p = 1$ boundary (1-shot RLVR's post-saturation generalisation shows this explicitly — see [[../research/single-sample-rl-finetuning/1-shot-rlvr]]). If the single training prompt becomes mastered by step 100 but test performance keeps climbing for 1000+ steps, *what is pulling the gradient during steps 100–1000?* Under DAPO's Dynamic Sampling, the answer is "nothing — the prompt would be filtered". Under MCPO's hinge-KL, the answer is "a bounded anchoring gradient preventing drift while other prompts (or the entropy term) provide exploration". This conflict is more severe at small $N$ than at DAPO's 32B-model training scale, where filtered prompts are immediately replaced by other in-batch prompts.

**Potentially compositional:** Dynamic Sampling + hinge-KL on retained mastered prompts = both the compute efficiency gain and the drift prevention. Neither paper evaluates this hybrid.

## Source

Surfaced via the 2026-04-23 weekly sweep. MCPO (arXiv:2604.16972) Sec 4.1 critiques DAPO (arXiv:2503.14476) — see the basis quote in [[../research/rl-optimizers/mcpo]]'s `## Conflicts raised` section.

## Related

- [[../research/rl-optimizers/mcpo]] — Position B paper
- [[../research/rl-optimizers/dapo]] — Position A paper
- [[../research/rl-optimizers/dr-grpo]] — related; shares MCPO's diagnosis of the std-normalisation bias
- [[../research/single-sample-rl-finetuning/1-shot-rlvr]] — post-saturation generalisation is the single-sample instance of this conflict
- [[../weekly-briefs/2026-04-23]] — brought in by the 2026-04-23 weekly sweep
