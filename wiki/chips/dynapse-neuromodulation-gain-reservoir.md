# Input-dependent neuromodulation on DYNAP-SE

INI Zurich / ETH / Imperial (arXiv 2610.41265, 2026-10-30, short paper) close a loop around a fixed 60-neuron reservoir on the DYNAP-SE mixed-signal chip: an off-chip MLP rewrites shared synaptic-gain parameters every 40 ms. **Evidenced (measured on physical chips, chip in the loop):** binary Spiking Heidelberg Digits (five vs nine) test accuracy 71.4% → 88.6% (+17.3 ± 10.4 pp over 5 reservoirs, 213 test trials). **Caveat the abstract omits:** retraining the readout alone reaches 83.9%, so the modulation-specific gain is **+4.7 ± 7.7 pp (p = 0.24, not significant)**; the headline has q = 0.082 after multiple-comparison correction.

## Setup

- **Chip:** DYNAP-SE (INI research chip, 0.18 µm CMOS, 4 cores × 256 neurons, sub-threshold analog AdExp-I&F neurons, DPI log-domain synapses). Mismatch (CoV up to 0.2) is treated as useful heterogeneity. Research-access hardware only.
- **Reservoir:** 48 excitatory + 12 inhibitory neurons on separate cores (Dale's law), fixed random input and recurrent weights, 5 physical instantiations. τ_mem = 40 ms; τ_AMPA = τ_GABA = 10 ms.
- **Modulation primitive:** the DPI's gain current (distinct from weight) is shared per core per synapse type, so two on-chip gains (excitatory and inhibitory onto the E population) can be rewritten at runtime without resetting dynamics; band [g₀/1.3, g₀·1.3]. A readout gain is applied on the host.
- **Training around analog imprecision:** no gradient through the analog circuits. Activity is recorded on-chip over a 4×4 grid of the two gains; a per-neuron quadratic response surface is fitted by least squares, and its derivative combines with backprop through the off-chip readout to estimate a gain gradient. Estimator validated only in simulation ("comparable" to backprop through the reservoir; no numbers).

## Controls (measured)

| Condition | Δ vs modulated |
|---|---|
| Readout retrained, no modulation (A) | −4.7 ± 7.7 pp (n.s.) |
| Constant gains (B) | −18.8 ± 13.1 pp (q = 0.082) |
| Another trial's gain trajectory (C) | −14.1 ± 11.4 pp (q = 0.085) |

The B/C gaps show the trained modulator is input-dependent, but nothing here beats a better-trained static readout reliably. Only binary SHD, 5 reservoirs; no energy, power or latency reported; modulator and readout run off-chip.

## Assessment

(synthesis) A small, honest-ish lab result on a research chip: useful as a data point that chip-in-the-loop fitting of measured response surfaces is a workable alternative to on-chip training for imprecise analog substrates ([[../conflicts/analog-onchip-training-viability]]), but it neither moves a viability date nor supports a hardware-native claim. Scaling limit: the recording grid grows rapidly with the number of modulated parameters; 64-synapse fan-in forced input compression 700 → 96 channels. No code/data link; no commercial signal (SNSF-funded).

## Source

- `raw/research/weekly-2026-11-05/03-neuromodulation-mixed-signal.md` (arXiv 2610.41265)

## Related

- [[../conflicts/analog-onchip-training-viability]]
- [[../devices/analog-training-nonidealities]]
- [[../devices/reciprocal-tau-cell-log-domain-learning]] — log-domain CMOS, mismatch
- [[../devices/optoelectronic-reservoir-computing-si3n4-ttd]] — another fixed physical reservoir with trained readout
- [[texel-gas-classification]] — other mixed-signal chip
- [[../snn/snn-training-surrogate-gradients]]
- [[../players/roster]]
- [[../weekly-briefs/2026-11-05]] — brought in by the 2026-11-05 weekly sweep
