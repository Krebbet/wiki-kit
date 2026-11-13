# Closed-loop fault assessment of a fly-connectome SNN (simulation)

A single-author Waseda University preprint (arXiv 2611.06940) that deletes connection rows from a Drosophila-connectome LIF network (138,639 neurons, 15,091,983 signed rows) controlling a synthetic pursuit-escape task, and counts first-contact collisions within a 1-s horizon in paired healthy/damaged runs. At 50% row deletion the proportional controller collided in 11/48 episodes and the relay controller in 0/48 (RF-0 cohort). **Simulation only (Brian 2): no chip, no device fault model, no energy or area figure.** It is a software methodology for closed-loop fault assessment, not evidence about neuromorphic hardware reliability.

## What was done

- Network (software model): FlyWire v783-derived LIF model with Shiu parameters, 0.1-ms steps. Input via 104 LC4 and 210 LPLC2 cells; eight descending cells give command features. Pursuer 0.3 m/s starting 0.25 m away; contact at 0.05-m separation; horizon 1 s.
- Fault model: nested random deletion of connection rows (25% and 50%), identical across paired runs through shared random uniforms. This is a *functional* connectivity loss; it is not stuck-at, SRAM, router or device-drift faults. The authors state it "establishes no biological tolerance, device upset rate, hardware safety or energy/area benefit".
- Design: 576 test episodes in three cohorts (RF-0 24 seed clusters, RF-A and RF-B 12 each). RF-A/B are recalibrated receptive-field maps, so cohort, calibration and healthy clearance change together.

## Evidenced (in simulation, authors' paired statistics)

- RF-0, 50% deletion: 11/48 proportional vs 0/48 relay collisions by 1 s. Relay-minus-proportional net-loss difference -22.9 percentage points (95% seed-cluster CI [-33.3, -12.5], Holm p = 0.00195; prespecified secondary). All healthy tasks succeed.
- RF-A/B, 50%: each -4.2 pp, CI [-12.5, 0], Holm p = 1; recalibrated mappings give smaller, uncertain estimates. No equivalence or isolated receptive-field effect is established.
- Loss depends on the declared horizon: RF-0 has nine extra proportional contacts in the final 100 ms of the 1-s horizon (descriptive rescoring).
- Timing does not explain outcome: all 288 proportional/relay pairs shared trigger and burst schedules, yet 15 pairs differed in contact outcome. Healthy minimum clearance differs between laws (RF-0 medians 33.1 vs 41.4 mm), so the comparison is of complete controllers with unequal reserve.
- Warnings are weak: a frozen command-rate warning on a 400-ms prefix detected 2/13 RF-0 contacts (2/3 and 0/1 in RF-A/B), with 51/275 false alarms in RF-0. An exact-state forecast detects all contacts but flags 57/275 safe RF-0 runs and uses simulated plant state, so it is not a neural-only detector. Positive support is 12/2/1 seed clusters, so intervals are thin.

## Record-consistency checker

A second contribution is an audit layer for result records (not a fault tolerance mechanism). On an author-designed catalogue of 87 corruptions (plus 24 valid IDs, 20 distinct valid inputs), header checks detected 36/87, common invariants 54/87, native replay 75/87, and the full combination 81/87, rejecting 0/24 valid cases. Six corruptions were missed by the full checker. The authors call the catalogue "not blind generalization evidence". Cost per valid fixture, full vs headers: 1.32 vs 0.0017 s (fly), 0.0168 vs 0.0018 s (tank).

## Limits stated by the authors

- One graph, an assumed receptive-field family, a synthetic plant, sparse failures; bearing readout RMSE about 66 deg.
- 1-s success is finite-horizon preservation, not sustained avoidance.
- Trace consistency cannot authenticate neural execution.

## Relevance (synthesis)

- Closes no gap on the hardware side. [[../chips/neuromorphic-fault-recovery-migration]] studies diagnosed permanent ALU faults in many-core chips (also simulation) at 0-50% fault rates; this paper's 25-50% *row* deletion is a different fault unit (connection rows in a 15.1M-row model vs per-core compute faults), so the two percentages are not comparable.
- The paper's closing claim is a basis for propagating future device-level nonidealities to closed-loop behaviour; none is done here. Treat as methodology to watch, not a viability datapoint.
- The "relay survives 50% loss" result is specific to one plant, one cohort and unequal clearance; the transfer cohorts do not reproduce it with confidence.
- The FPGAFly connectome-on-FPGA item on [[../watchlist]] is a separate paper (arXiv 2610.38118) and this one does not cite it; neither wiki page currently links the two.

## Source

- `raw/research/weekly-2026-11-12/02-fly-connectome-snn-fault.md` — Gao, "From Connection Loss to Collision: Closed-Loop Fault Assessment of a Fly-Connectome SNN", arXiv 2611.06940. Code at git commit b29f089.

## Related

- [[../chips/neuromorphic-fault-recovery-migration]] — hardware-oriented fault recovery (simulation), different fault model
- [[../watchlist]] — FPGAFly fruit-fly connectome on FPGA, unread
- [[../benchmarks/neurobench]] — no fault-tolerance track
- [[../chips/neuroml2loihi-celegans]] — another connectome-to-SNN mapping
- [[../weekly-briefs/2026-11-12]] — brought in by the 2026-11-12 weekly sweep
