# FEST tuned-LR pure RL vs the demonstration-necessity premise

## Positions

**Position A — FEST ([[../research/single-sample-rl-finetuning/fest]]).** Pure RLVR is a *formidable* baseline once the learning rate is tuned. FEST §4.1 observation (ii) and Table 2 fn. 3: raising the GRPO LR from 1e-6 to 5e-6 lifts pure RL to Avg@8 = 39.79 on Qwen2.5-Math-1.5B — matching ReLIFT trained on the full 46K-trace dataset. Explicitly: *"Contrary to findings in prior work [HPT, ReLIFT, LUFFY], we observe that pure RL remains a formidable baseline when the learning rate is optimized."* Demonstration guidance still helps (FEST-GRPO 42.38), but the *gap it must close* is much smaller than prior work implies, and 128 random traces suffice to close it — no large curated SFT corpus is necessary.

**Position B — the demonstration-necessity premise ([[../research/single-sample-rl-finetuning/_overview]], implicitly).** HPT (~10K traces), ReLIFT (8.6K), and LUFFY (46K) are presented as demonstrating that substantial demonstration guidance is *needed* to overcome RLVR's limitations at scale on weaker/smaller bases — the theme's "amplification beats teaching, but teaching is still required to seed the amplification" reading. Their reported pure-RL baselines are weak enough that the demonstration delta looks large and load-bearing.

## Resolution rule

*(Open — no ruling yet.)*

The conflict is plausibly an **artefact of baseline-tuning rigour**, not a substantive disagreement about mechanism:

- If FEST's claim generalises, much of the apparent "demonstration necessity" in HPT/ReLIFT/LUFFY is an under-tuned pure-RL baseline, and the true contribution of demonstration guidance is (a) **sample-efficiency of the closing delta** (128 random traces, not 8–46K) and (b) **stability** (avoiding the HPT-G/ReLIFT-G mid-training collapse), not unlocking otherwise-unreachable performance.
- Position B is not refuted: FEST itself still adds +2.6 Avg@8 over its own tuned-RL baseline and a larger OOD/Pass@k margin — demonstration guidance is not redundant, just smaller than advertised.

**What would resolve it:** a controlled study holding base model, data, and *LR-tuning budget* fixed across (a) tuned pure RL, (b) FEST-128, (c) HPT/ReLIFT at their native data scales — measuring whether the demonstration delta survives equal baseline-tuning effort, and whether it is concentrated in the hardest-problem / OOD regime rather than aggregate accuracy.

**Relevance to the project ([[../research/synthesis/proposed-method]], [[../research/synthesis/single-sample-concept-skeleton]]):** the single-sample thesis assumes a small, well-chosen demonstration set is the load-bearing intervention. If tuned pure RL is much stronger than the literature suggests, the project's value proposition shifts from *"demonstrations unlock performance"* toward *"demonstrations make the closing delta sample-efficient and training stable"* — a weaker but still real claim. The pre-flight question becomes: for the chosen base model and LR budget, how large is the residual gap a single concept-example is being asked to close? (Connects to BOLT's coverage–ESS wall in [[../research/rl-optimizers/bolt-kl-rlvr-boltzmann]].)

## Source

Surfaced via the 2026-05-17 weekly sweep. FEST (arXiv:2605.15012) §4.1 obs. (ii), Table 2 fn. 3 — see `## Conflict raised` in [[../research/single-sample-rl-finetuning/fest]].

## Related

- [[../research/single-sample-rl-finetuning/fest]] — Position A paper
- [[../research/single-sample-rl-finetuning/_overview]] — Position B (implicit demonstration-necessity premise)
- [[../research/single-sample-rl-finetuning/cbrl]] — adjacent: cold-start demo annealing also closes an RL gap from the low-data side
- [[../research/rl-optimizers/bolt-kl-rlvr-boltzmann]] — coverage–ESS wall: a complementary lens on "how big is the gap to close"
- [[../research/synthesis/proposed-method]] — project value proposition shifts if Position A generalises
- [[../weekly-briefs/2026-05-17]] — brought in by the 2026-05-17 weekly sweep
