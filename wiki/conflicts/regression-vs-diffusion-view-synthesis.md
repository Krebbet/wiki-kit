# Single-Image View Synthesis: Feedforward Regression vs Diffusion

**Status:** open. Pre-flagged from radar-2026-04 ingest. Diffusion-side source not yet captured.

## Position A — Regression Pareto-dominates diffusion for nearby views

**Source:** [[sharp-view-synthesis]] (Apple, arXiv:2512.10685).

**Claim:** End-to-end feedforward regression on a 3D Gaussian Splatting representation **Pareto-dominates** diffusion-based view synthesis for *nearby* novel views — better fidelity *and* faster runtime by 3 orders of magnitude.

**Basis (Table 1 cells):**
- LPIPS reduced 25–34% vs Gen3C.
- DISTS reduced 21–43% vs Gen3C.
- Synthesis time: <1s vs ~1000× longer for diffusion baselines.
- Best on every (DISTS, LPIPS) cell across 6 zero-shot datasets (Middlebury, Booster, ScanNet++, WildRGBD, ETH3D, Tanks and Temples).

**Scope claim:** the dominance is for *nearby-view, single-image* synthesis. SHARP explicitly does **not** claim this for far-away viewpoints — authors flag diffusion+distillation as future work for that regime.

## Position B — Diffusion is the right primitive for view synthesis

**No source captured.** Diffusion-side baselines named in SHARP: Gen3C (Ren CVPR 2025), ViewCrafter, ZeroNVS, CAT3D, Wonderland. Capturing one of these as a primary source is the next step to make this conflict resolvable.

## Resolution rule when Position B arrives

The two camps may not be in genuine conflict — SHARP scopes its claim to nearby views; diffusion proponents typically focus on larger viewpoint changes where amortized regression is harder. Resolution likely takes the form of a viewpoint-distance partition:
- Nearby views (small headbox): regression wins on the SHARP datasets.
- Far / extrapolated views: open.

If a diffusion-side paper claims dominance on the same shared datasets at the same viewpoint distance, that's a real conflict. Otherwise it's a scope/methodology partition.

## Related

- [[sharp-view-synthesis]], [[moonlake-world-models]] (adjacent: Moonlake's hybrid 3D+video sidesteps the binary).
- [[watchlist]] — Gen3C, ViewCrafter, CAT3D, ZeroNVS, Wonderland not captured.
