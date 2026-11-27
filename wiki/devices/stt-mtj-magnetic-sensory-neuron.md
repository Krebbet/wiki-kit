# STT-MTJ stochastic magnetic sensory neuron

Xi'an Jiaotong, ShanghaiTech and collaborators (arXiv:2611.30740, preprint) use field-dependent stochastic switching in magnetic tunnel junctions made in an unnamed foundry's 40 nm MRAM process as a combined magnetic sensor and rate-coded spike generator. **Measured:** isolated devices on bench instruments. **Simulated:** the 10×10 sensor array and its 90.7% trajectory-recognition accuracy. No energy, endurance or variability data.

## Terms

- **STT-MTJ:** a two-terminal magnetic tunnel junction switched by spin-polarised write current; below threshold, switching is probabilistic.

## Measured (device, room temperature; device count unstated)

- 78 nm pillar; default 500 ns write, 1.5 µs reset–write–read cycle.
- Switching probability at 260 mV: 0.25 / 0.52 / 0.76 at −10 / 0 / +10 mT.
- ±40 mT range, obtained by retuning write voltage; average sensitivity 2.91 %/mT.
- Static field decoding (offline) mean absolute error 0.544 mT for −20 to +20 mT. The figure labels RMSE 0.5 mT, which cannot be below the MAE on the same data.
- Minimum detectable field estimated from noise: ~1.1 mT at 200 cycles, ~0.35 mT at 2,000 (read from plot), i.e. a speed–resolution trade.

## Simulated

- 10×10 array, 1 mm pitch, synthetic magnetic trajectories from UNIPEN digits, SNN in software: 87.2% (encoding ratio 5, 1 device/neuron), 90.7% (ratio 20, 2 devices/neuron), software direct-encoding baseline 92.1%.
- "~170× fewer transistors" than a conventional chain is an estimate against an unspecified design.

## Assessment

(synthesis) The abstract's "10×10 array achieves 90.7%" reads as hardware; it is not. The open items that decide usefulness are write energy under continuous cycling, endurance, temperature sensitivity of thermally activated switching, per-device calibration and array variability — none measured.

## Source

- `raw/research/weekly-2026-11-26/02-spintronic-sensory-neuron-mram.md` (arXiv:2611.30740; supplement not captured)

## Related

- [[vmtj-cmos-izhikevich-neuron]]
- [[sot-mtj-multiweight-wafer-scale-synapse]]
- [[event-cameras]]
- [[../snn/spike-encoding-iot-sensing]]
- [[../viability-ledger]]
- [[../weekly-briefs/2026-11-26]] — brought in by the 2026-11-26 weekly sweep
