# Loihi 2 — fully on-chip Q-learning with embedded CartPole simulation

LANL, Drexel and Northwestern (Nesbit et al.) run a tabular Q-learning agent *and* its CartPole-v0 simulator entirely on one Intel Loihi 2 board, with no host computation between environment transitions. The paper claims half the training time and ~600x lower power / >1000x lower energy than a laptop CPU, at a lower success rate (36% vs 62% peak). The measured tables support a much smaller total-energy gap (~67x board-level); the headline rests on dynamic-only figures. It is the wiki's first on-chip *learning* data point on Loihi 2, and a second instance of the dynamic-only-headline pattern seen in [[loihi2-persistent-monitoring]].

## Device / chip

Intel Loihi 2 digital asynchronous neuromorphic chip on an "Oheogulch" board (ncl-ext-og-05, generation N3B3), Lava on Loihi v0.6.0 with custom microcode neuron processes. The process node is not stated in this source. Learning engine: 8-bit signed weights, 8-bit signed tag register, 24-bit activations. The board uses 34 neurocores for training (12 for inference) plus on-board x86 cores. No memristor or emerging-memory material is involved. Research hardware, access gated through INRC.

## Workload

**Tabular Q-learning, not a spike-trained SNN.** A synfire-gated chain (9 gating neurons, 9-step loop) uses a Hebbian weight update via the tag register to implement the TD update. State is a one-hot 72-state encoding (6 angle x 12 angular-velocity bins) into a 2x72 8-bit Q-table (range [-127, 126]). Reward +/-8, gamma 0.99; epsilon and alpha share one score-dependent decay, with alpha scaled by 1/8 to avoid overflow.

CartPole-v0 is simulated on-chip as a single neuron (Euler step 0.02 s) using a polynomial sin/cos approximation, Newton division and a 23-bit LCG random-number generator. Training stops at episode score 500; evaluation is by inference in the real OpenAI Gym CartPole-v0. This is the easiest standard RL benchmark, as the authors acknowledge.

## Measured numbers

All from the paper's Table II: on-chip energy/time probes for Loihi 2, HWiNFO64 (package-level software readout) for the CPU, a Dell Alienware m15 R4 laptop (i7-10870H, Windows 10).

| Platform / boundary | Power (W) | Latency per update (µs) | Energy per action (µJ) |
|---|---|---|---|
| Loihi 2 whole board, training | 1.80 (1.78 static, 0.02 dynamic) | 58.42 | 104.75 (1.32 dynamic) |
| Loihi 2 neurocores only, training | 0.25 | — | 14.25 |
| Loihi 2 on-board x86 cores | 1.56 | — | 90.51 |
| Loihi 2 whole board, inference | 1.81 | 12.86 | 23.23 |
| CPU i7-10870H, training | 43.22 (12.00 dynamic) | 162.54 | 7,024 |
| CPU i7-10870H, inference | 43.27 | 128.55 | 5,562 |

The on-board x86 cores account for ~86% of board energy, while the source states "no host computation between transitions." Also reported: ">17 kHz weight-update rate" (consistent with 58.42 µs); function-approximation errors of sin 0.00229, cos 0.00020, division 0.00291, and a maximum theta-ddot error of 0.03632 rad/s².

**Success rate** (solving CartPole-v0 = mean >=195 over 100 trials; 100 agents at each of 10 update counts from 10k to 100k, 1,000 agents per platform): CPU peaks at 62% (90k updates); Loihi 2 peaks at 36% (50k updates) and plateaus near 30% from 60k. Best single agent scores 200 on both. Mean score over all agents: CPU 182.94, Loihi 167.03.

**GPU:** one sentence only (V100S via PyTorch, 67% success, "three orders of magnitude higher energy and an order of magnitude longer execution"). No table, no figures, and the setup is not matched. The authors explicitly decline a GPU comparison; treat as anecdote.

## Baseline and comparison honesty — the headline is boundary-dependent

Claims below are the paper's; ratios marked *recomputed* are this wiki's arithmetic on Table II, not figures the paper states.

- **Power, "600x lower":** dynamic-only (12.00 W vs 0.02 W). Total power is 43.22 vs 1.80 W, ~24x (recomputed).
- **Energy, ">1000x":** not supported by total energy. Recomputed from Table II: ~67x whole-board (7,024 / 104.75 µJ), ~490x neurocores-only (7,024 / 14.25 µJ), ~1,476x dynamic-only (≈1,948 / 1.32 µJ). The ">1000x" and "two orders of magnitude less dynamic power" language appears to rest on the dynamic-only boundary. Needs checking against the paper's own derivation. The ~490x neurocore-only figure also excludes the x86 cores that are physically part of the board.
- **Static power dominates:** 1.78 of 1.80 W is static, and the x86 cores are ~86-87% of board energy. The efficient part of the system (neurocores) is a small fraction of what the board draws.
- **Mismatched instruments and boundaries:** on-chip probes at board level for Loihi 2 vs package-level HWiNFO64 on a laptop CPU.
- **Weak baseline:** the CPU runs a 64-bit-float Python Gym environment, likely single-threaded. No same-precision CPU baseline (8-bit integer tabular Q-learning in C) is given, so the gain is largely "Python on a laptop vs purpose-built microcode," not neuromorphic vs conventional at equal effort.
- **"Same successes in half the time"** relies on the 2.8x per-update speed (162.54 vs 58.42 µs) combined with 36% vs 62% success; it is an iso-success framing, not a like-for-like speed claim.
- **Quality gap untested:** the 36% vs 62% gap is attributed to precision and the LCG RNG, but this is not isolated experimentally.
- Single chip, single task, 72-state tabular problem; no scaling evidence.

This is a second same-pattern case, alongside [[loihi2-persistent-monitoring]], of a Loihi 2 efficiency headline that is dynamic-only while the table-derived total gap is far smaller; see [[../conflicts/snn-energy-payoff]] for the cross-source picture. (Synthesis: because the model is tabular Q-learning, treat this as chip/systems evidence on measurement boundaries, not as an SNN-algorithm data point.)

## Maturity

Integrated chip running an end-to-end closed-loop demonstration: research prototype on a toy task. No product path evidenced; the Lava SDK was archived 2026-05-13 per the wiki, which bears on reuse.

## Commercial signal

None evidenced. Funded by US DOE NNSA DNN R&D at LANL; Intel Labs/INRC provide hardware access. "Commercially relevant AI" appears only as an aspiration.

## Blockers stated

- 24-bit fixed point and 8-bit weights: lower success rate (36% vs 62%).
- Low-quality LCG RNG (MT19937 infeasible on-chip); sin/cos accurate to only 2-3 decimals.
- CartPole is only an initial benchmark; more complex tasks (e.g. UAS control) are untested.
- Limited microcode instruction set, local-only memory, small Q-table.
- Real sustainability impact requires the gains to extend to complex benchmarks and deployed applications.

## Novelty

Recombination and engineering: extends Renner et al.'s synfire-gated neuromorphic backprop (Nat. Commun. 2024) to Q-learning and embeds the environment on-chip. Closest prior work: Akl et al. (2021) deep spiking Q-networks on Loihi, Tang et al. (2020) co-learning navigation, Plank et al. (2025) CartPole benchmark. The real novelty is the boundary: update, action selection, reward and environment are all co-located on Loihi 2. The authors' "first demonstration of successful end-to-end RL training on neuromorphic hardware" is **stronger than their own related work supports** (memristor in-situ RL by Wang et al., 2019 is cited in the same paper). Treat as hype.

## Reproducibility

Figure videos at github.com/nesbitsc/all-on-board-figure-1; no code release for the Loihi 2 circuit is stated. Requires INRC access to Loihi 2 hardware, and the Lava SDK is archived. LA-UR-25-31518, approved for unlimited release.

## Source

- `raw/research/weekly-2026-10-01/02-loihi2-onchip-q-learning.md` — "All On-Board: Fully On-Chip Neuromorphic Q-Learning with Embedded CartPole Simulation" (Nesbit et al., arXiv:2609.32317v1, 26 Sep 2026). Primary, government/academic.

## Related

- [[../conflicts/snn-energy-payoff]] — second dynamic-only-headline vs table-derived-total case (>1000x claimed vs ~67x board total, recomputed)
- [[loihi2-persistent-monitoring]] — sibling Loihi 2 source with the same boundary pattern
- [[../players/intel-loihi2]] — Intel Loihi 2 entry; x86-core static-power share and Lava dependency
- [[../benchmarks/neurobench]] — static/dynamic/total reporting, but with mismatched instruments across platforms
- [[../snn/snn-training-surrogate-gradients]] — contrast: local Hebbian tag-based Q-update, no BPTT
- [[../snn/snn-energy-hardware-realistic]] — claimed vs hardware-measured gap
- [[../conflicts/analog-onchip-training-viability]] — contrast: digital 8-bit on-chip learning works for tabular RL, with no analog non-idealities
- [[../viability-ledger]] — on-chip RL / edge-control row (digital neuromorphic, research only)
- [[../players/roster]] — Intel / LANL entry
