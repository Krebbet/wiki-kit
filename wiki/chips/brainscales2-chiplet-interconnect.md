# BrainScaleS-2 chiplet interconnect (Heidelberg)

A routing-chiplet design from Heidelberg University (Heinemann & Schemmel, IEEE 2026) that lets the analog BrainScaleS-2 (BSS-2) neuromorphic SoC scale past a single die by multiplexing unreliable/real-time spike traffic and reliable/ARQ-protected configuration traffic over one chip-to-chip (C2C) link. The motivating problem: BSS-2's analog core (512 neurons, 131,072 synapses/chip, 65 nm CMOS) is area-constrained and doesn't benefit from process-node shrinks, so scaling has to come from tiling chips together rather than making one chip bigger. **Everything reported is pre-silicon** — RTL simulation and post-synthesis estimates, no routing chiplet has been fabricated.

## What it does

Prior BSS-2 interconnects either carried only spike events with no non-event channel (the FPGA star-topology) or packed both traffic types into larger timestamped packets that add latency (the EXTOLL-based link). This design's contribution is **phit-level dynamic bandwidth partitioning**: event and non-event traffic share a single link under a weighted priority arbiter, with a dedicated Hamming-protected framing bit for fast resync and a compact prefix-coded phit-pair header. Non-event traffic gets credit-based flow control plus link-level ARQ; event traffic gets neither (unlike EXTOLL/spiNNlink, which secure events too) — the tradeoff that buys event traffic its latency priority.

## Measured numbers — all simulated, not fabricated

- Physical C2C link (from cited prior work, itself presumably measured): ≤1×10⁻¹⁰ BER at 2 Gbit/s/link; ~11 links/direction/port → 22 Gbit/s total per direction per port.
- Non-event message latency (simulation, BER=0): minimum 610 ns at 4 routing chiplets in a row under low event rate.
- MTBF for sustained non-event bandwidth (BER=1×10⁻¹⁰, extrapolated from only 200 injected bitflips under an independent-error assumption, not a direct measurement): ≥O(1 day) per link at 95% utilization; for a 16×16 mesh (960 links), system-level MTBF drops to **O(minutes)** in the worst case.
- Event round-trip latency (co-simulated with a real BSS-2 FPGA design, no errors injected): 32 ns between two routing chiplets; ≥16 ns lower bound for a single hop.
- Post-synthesis area (65 nm): ≈0.17 mm² for the non-event router + ARQ + link-level protocol (≈0.13 mm² of that is buffers), excluding I/O cells.

**Table II cross-system comparison** (physical link bandwidth, not effective payload bandwidth) — this work: 22 bits/event, ≥16 ns min single-hop latency, 22 Gbit/s C2C bandwidth, vs. BSS-2 FPGA (20 bits/event, 0.17 µs, 5 Gbit/s), BSS-2 EXTOLL (29 bits/event, 75 ns, 16 Gbit/s), SpiNNaker-1 C2C (40/72 bits/event, 0.44 µs, avg 275 Mbit/s), spiNNlink (32/64 bits, 665 ns, 3 Gbit/s), DYNAP-SE2 (24 bits, not reported, not reported).

**Comparison-honesty note.** The authors caveat the table itself ("a simple table cannot capture all details," five footnotes on differing latency definitions per system) — good practice. What the table does *not* flag: this work's own figures are pre-tape-out simulation/post-synthesis estimates, while at least some comparators (BSS-2 FPGA, EXTOLL) are numbers from deployed hardware. Simulated-vs-measured is not called out as a comparison axis. Treat the 22 Gbit/s and ≥16 ns figures as "what the design should achieve if fabricated as simulated," not as a like-for-like measurement against the other rows.

## Maturity

RTL design (SystemVerilog/Amaranth) + cycle-accurate simulation (CXXRTL) + post-synthesis area estimate. No tape-out, no physical chiplet. The event router used for evaluation is a "simple broadcast" placeholder — a multicast-capable event router is named as the primary remaining challenge before this could support a real multi-chip BSS-2 deployment.

## Algorithm context

Not an SNN-algorithm paper. The non-event traffic pattern used to stress-test the network (the source of realistic message-rate statistics, not a task result) is modeled on hardware-in-the-loop surrogate-gradient training on BSS-2 (Cramer et al., PNAS 2022): forward pass on the analog substrate, ADC-captured membrane traces streamed off-chip as non-event traffic, backward pass on a host.

## Blockers stated

- Multicast-capable event router not yet designed.
- Design is BSS-2-specific; generalizing would need longer multi-phit event messages and a third traffic class (detected-but-uncorrected errors).
- MTBF at realistic BER is an extrapolated upper bound, not a direct measurement.
- Traffic patterns are synthetic (Bernoulli-process events, constant-rate non-event), aside from the one surrogate-gradient-training scenario.
- No physical prototype — every number above is pre-silicon.

## Commercial signal

None — purely academic (Heidelberg University, ZITI Institute of Computer Engineering), funded by EU Horizon 2020 Human Brain Project and Horizon Europe EBRAINS 2.0. No commercial partners or availability dates.

## Reproducibility

No indication that the RTL, simulation harness, or traffic-generation code is publicly released. Closed.

## Source

- `raw/research/weekly-2026-09-24/01-brainscales-chiplet-interconnect.md` — "A Unified Interconnection Network for Chiplet-Based Scaling of the BrainScaleS Neuromorphic System" (Heinemann & Schemmel, IEEE, 2026; arXiv:2609.13563). Academic primary, captured via arXiv PDF.

## Related

- [[loihi2-persistent-monitoring]] — the wiki's other named-chip/system entry; Table II in this source does not include Loihi
- [[../devices/memristor-array-integration-gap]] — thematically parallel: device/chip capability not surviving to system level, here for die-area/interconnect bandwidth rather than ADC/DAC power
- [[../players/roster]] — BrainScaleS-2/Heidelberg is not yet a roster row (academic, not a company); flagged there as a research target
- [[../viability-ledger]] — chiplet scaling addresses the "analog cores don't benefit from node shrinks" blocker class
- [[../weekly-briefs/2026-09-24]] — brought in by the 2026-09-24 weekly sweep
