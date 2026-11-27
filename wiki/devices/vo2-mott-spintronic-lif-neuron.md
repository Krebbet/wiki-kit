# VO2 Mott LIF neurons writing into spintronic memory

Max Planck Halle (Parkin group; Nature Nanotechnology, 2026-11-25) has a two-device VO2 leaky integrate-and-fire (LIF) neuron write its spikes straight into a domain-wall racetrack on the same sapphire chip, and separately into an SOT-MTJ on another substrate, with no amplifier or ADC in the write path. **Measured** at device-pair level. The 51.9 nJ per spike-to-memory conversion is **calculated**; the ~200 pJ sub-200 nm figure has an unshown basis; the 96.3% MNIST result is **software**, and the 16×16 array is **simulated**.

## Terms

- **Mott memristor:** a volatile threshold switch; VO2 turns metallic near ~340 K and relaxes back when current drops.
- **Racetrack / domain wall:** a magnetic strip where the position of a domain boundary stores analog history.
- **SOT-MTJ:** magnetic tunnel junction switched by current in an adjacent heavy-metal track.

## Device

- Two 5×5 µm² VO2 devices, 2 µm apart, ~23 nm film on c-plane sapphire. One integrates; the second is thermally triggered and fires. No external R or C for integration.
- The write path does use passives (capacitor + diode rectifier, added 3 kΩ series resistor) and external current sources.
- Co-integration is on one substrate only for the micrometre VO2 + racetrack pair. The nanoscale pair (500 nm neuron, 100×400 nm² MTJ) is on two substrates, wired externally. No CMOS, no BEOL, no foundry.

## Measured (device level, room temperature)

- Single VO2 device: threshold ~1.5 mA; switching stable beyond 10⁶ cycles (supplement not captured; exponent reconstructed from extraction).
- ~1 µm domain-wall travel per identical spike, up to 6 spikes per process cycle, 10 repetitions.
- Second-spike recovery 500 µs (−0.65 mA bias) to 277 µs (−0.85 mA).
- Digit 0 vs 1 separated by domain-wall position, read by Kerr microscopy; no hardware accuracy figure.
- A 10×10 VO2 neuron crossbar was fabricated without co-integrated memory; no yield or uniformity numbers in the main text.

## Energy and algorithm (not measured at system level)

| Figure | Basis | Boundary |
|---|---|---|
| 51.9 nJ per spike-to-memory conversion | calculated | two 5 µm VO2 devices; excludes sources, reset and read-out (synthesis) |
| ~200 pJ per spike | stated for sub-200 nm VO2; measured vs extrapolated not shown | device |
| 96.3% MNIST, 100 neurons | software model with fitted leak constant | not hardware |
| 16×16 1T hybrid array | simulation | — |

## Assessment

(synthesis) An integration demonstration at the single-device-pair rung. Open: read sensors with a usable on/off ratio on racetracks (authors' stated key challenge), CMOS compatibility, temperature sensitivity of a ~340 K transition, variability and yield. Compare [[vmtj-cmos-izhikevich-neuron]] (spintronic neuron, simulated) and [[sot-mtj-multiweight-wafer-scale-synapse]] (foundry-line synapse); energy boundaries differ across all three. Minor internal inconsistencies in the source (2 vs 20 repetitions; 81 pulses of 6 µs against a stated 400 µs window).

## Source

- `raw/research/weekly-2026-11-26/08-vo2-mott-spintronic-hybrid.md` (Nature Nanotechnology s41565-026-02311-0; main text captured, supplement not)

## Related

- [[vmtj-cmos-izhikevich-neuron]]
- [[sot-mtj-multiweight-wafer-scale-synapse]]
- [[ecram-short-term-plasticity-neuron]]
- [[memristor-array-integration-gap]]
- [[../conflicts/snn-energy-payoff]]
- [[../viability-ledger]]
- [[../weekly-briefs/2026-11-26]] — brought in by the 2026-11-26 weekly sweep
