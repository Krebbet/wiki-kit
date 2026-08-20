# Reconciling Two Competing Measurements of the Same Quantity — Cross-Field Methods

We have **two independent estimates of the same physical thing** — a robot's trajectory and the room's floor plan — from two sensors: **2D LiDAR SLAM** and **monocular visual SfM (hloc)**, tied by a known yaw extrinsic ([[relocalization-method-bakeoff]], [[camera-lidar-temporal-calibration-and-pose-interpolation]]). They **mostly agree (~0.14 m)** but diverge in places. We want a principled way to (a) **fuse** them into one tight, trustworthy estimate weighted by each source's reliability, and (b) **detect and flag** the points where they *irreconcilably* disagree — **without over-pruning** real-but-disagreeing data to force an unrealistically clean fit.

This page surveys the named techniques for that problem **from across fields** (estimation theory, geoscience/weather, robust statistics, decision theory, evidence theory, change detection, machine learning) and, for each, gives the core idea, **when it applies to us**, and the **over-pruning guard**. It is the general-methods companion to the problem-specific [[lidar-visual-fusion-slam]] (where the two signals come from) and [[global-alignment-wall-refinement]] (the geometry refinement that consumes the result), and it operationalises the human's **robust-evidence mapping principle** — *don't use all the noisy signal; extract the pieces many observations agree on, build the picture from those with confidence, and flag the rest as unknown rather than forcing a fit.* *(synthesis — assembled from the cited primary sources.)*

> **Read alongside:** [[lidar-visual-fusion-slam]] (our LiDAR-geometry + camera-cross-val regime — *de facto* loose fusion already), [[global-alignment-wall-refinement]] (plane/line-constrained pose refinement that the fused trajectory feeds), [[2d-lidar-slam]] (the pose-graph back-end), [[slam]] (the concept hub), [[passive-stereo-robustification]] (why the visual signal is the less-reliable one here).

---

## 0. The framing: same quantity, two noisy views, unknown correlation

Two estimators of one quantity differ for three distinct reasons, and **conflating them is the classic over-pruning trap**:

1. **Random noise** — both are right on average; fusion should *average them down* (variance reduction). Down-weight, never delete.
2. **Real structure one sensor can't see** — e.g. the LiDAR scan plane sits ~7 cm above the camera and sees a wall *behind* an against-wall counter that the camera never images ([[land-rover-v1-rig]]). Here the "disagreement" is **a true difference of observed quantity**, not error. Deleting it destroys real map information — this is exactly what the over-pruning guard must protect.
3. **A gross fault / blunder** — a bad loop closure, an SfM scale slip, a mis-association. These *should* be rejected, but only after (1) and (2) are ruled out.

Every method below is, at heart, a different policy for telling these three apart. The two practical knobs are **down-weighting vs trimming** (soft vs hard rejection) and **the model of how the two sources are correlated** (independent, fully unknown, or partially known).

Before any fusion, the two trajectories must be in a **common frame**: solve the rigid (here SE(2)+known-yaw, not Sim(3) — our LiDAR fixes metric scale) alignment by the **Umeyama/Horn closed form** (SVD least-squares), the de-facto standard for trajectory comparison and ATE evaluation [src: zhang-tutorial-2018, evo-umeyama]. Our known +99° yaw makes this a *constrained* alignment (estimate only the residual offset), which is more robust than a free fit and itself a cross-check: a large residual rotation would mean the yaw or a time-sync is wrong, not the data ([[camera-lidar-temporal-calibration-and-pose-interpolation]]).

---

## 1. Bayesian sensor fusion — Kalman/EKF/UKF, factor graphs, MAP

**Core idea.** Treat each estimate as a Gaussian `x_i ± Σ_i`. The Bayes-optimal fusion of independent Gaussians is the **inverse-variance-weighted mean**: the fused estimate weights each source by its **information matrix** (inverse covariance), so the more certain sensor dominates and the fused covariance is *tighter than either input*. The Kalman filter is the recursive form over time; the **EKF/UKF** linearise/sigma-point the nonlinear pose case; the modern back-end form is a **factor graph** where each measurement is a factor and **MAP estimation** (least-squares on the negative-log-posterior) is solved by GTSAM/g2o/Ceres [src: zhang-tutorial-2018]. This is already the substrate of our LiDAR pose graph ([[2d-lidar-slam]], [[global-alignment-wall-refinement]]).

**When it applies to us.** This is the *default* and the right backbone: add the SfM trajectory as a **set of relative-pose (or absolute-pose-prior) factors** into the existing LiDAR pose graph, each weighted by an honest SfM covariance, and re-optimise. Reliability **is** the inverse covariance — the well-measured LiDAR geometry (ATE ~0.024 m) outweighs the noisier visual poses (~0.163 m) automatically ([[lidar-visual-fusion-slam]]), without a hand-tuned global weight.

**Over-pruning guard.** Pure Gaussian MAP has **no rejection at all** — it trusts every factor, so a single gross outlier drags the whole solution. That is *under*-pruning, and the fix is the robust kernels of §4. The complementary risk is **dishonest (too-small) covariances**: if you understate SfM uncertainty the optimiser will fight the LiDAR and "resolve" real differences by smearing them. The guard is calibrated covariances (estimate them empirically from residuals) so genuine disagreements show up as *large normalized residuals to be flagged* (§7), not silently averaged away.

## 2. Covariance Intersection — fusing when the cross-correlation is unknown

**Core idea.** Inverse-variance fusion is only correct when the two estimates are **independent**. Two SLAM/SfM trajectories that share the same scene, the same gravity, overlapping loop closures, and a common starting frame are **correlated by an unknown amount** — fusing them as independent is over-confident and can diverge. **Covariance Intersection (CI)** (Julier & Uhlmann, 1997) fuses two estimates *without knowing their cross-correlation* and is guaranteed **consistent (non-divergent) for any true correlation**: it takes a convex combination of the two information matrices, `Σ_f⁻¹ = ωΣ_a⁻¹ + (1−ω)Σ_b⁻¹`, choosing the scalar `ω∈[0,1]` to minimise the fused trace/determinant [src: julier-uhlmann-ci-1997, ci-revisited]. **Inverse Covariance Intersection (ICI)** is a tighter (less conservative) variant when a common-information bound is known [src: ici-2017].

**When it applies to us.** **This is very likely our case.** We cannot compute the LiDAR↔SfM cross-correlation (they share the room and a common origin), so the clean inverse-variance fusion of §1 is technically over-confident. CI gives a **safe, conservative fused trajectory/map** whose covariance is honest — exactly right when we want a *trustworthy* estimate rather than an over-tight one, and it degrades gracefully when the two are actually highly correlated.

**Over-pruning guard.** CI's conservatism is *itself* an anti-over-pruning property: because it never claims more certainty than warranted, it does **not** manufacture an artificially tight fit that would make benign disagreements look like outliers. The cost is some loss of sharpness; the guard against *that* is ICI or partial-correlation CI when a correlation bound is genuinely available [src: ci-partial-2022, ici-2017].

## 3. Data assimilation — 3D-Var, 4D-Var, Ensemble Kalman Filter (geoscience)

**Core idea.** Weather/ocean modelling solves *exactly our problem at planetary scale*: reconcile a **model trajectory (the "background")** with **sparse, heterogeneous observations**, weighted by the error covariances of each. **3D-Var** minimises a cost `J = (x−x_b)ᵀB⁻¹(x−x_b) + (y−Hx)ᵀR⁻¹(y−Hx)` — a snapshot MAP fit balancing background `B` and observation `R` covariances. **4D-Var** extends this over a **whole time window**, finding the single trajectory most consistent with the model dynamics *and* all observations across the window at once — i.e. it fits a *trajectory*, not a point. The **Ensemble Kalman Filter (EnKF)** propagates a Monte-Carlo ensemble to estimate flow-dependent covariances instead of a static `B`; hybrid **EnVar** blends ensemble and static covariances [src: da-wikipedia, gabbard-var, lorenc-4dvar-enkf].

**When it applies to us.** The **4D-Var analogy is the strongest cross-domain transfer for us**: treat the **LiDAR trajectory as the background/model** and the **SfM poses as observations over the time window**, and solve for the single reconciled trajectory minimising a joint cost over the *whole run* — which is precisely a smoothing factor graph (§1) but framed as *model-vs-observations* rather than *sensor-vs-sensor*. The geoscience framing also supplies the vocabulary for **observation QC** (gross-error check, buddy/consistency check) that the field uses to admit-or-flag observations before assimilation — directly reusable as our flagging stage.

**Over-pruning guard.** Operational DA is built around **not** throwing data away cheaply: observations failing a gross-error check are **flagged and down-weighted (variational QC, inflated `R`)**, not silently dropped, precisely so a stubborn-but-real observation is retained at reduced weight and revisited. **Covariance inflation** in EnKF is the standard cure for an over-confident ensemble that would otherwise reject good observations — a direct analogue of our "don't understate SfM covariance" guard [src: lorenc-4dvar-enkf, hunt-letkf].

## 4. Robust statistics & consensus — M-estimators, RANSAC, LMedS, GNC

**Core idea.** Replace the squared-error loss (which lets one outlier dominate) with a **robust cost** that bounds the influence of large residuals:
- **M-estimators** — Huber, Cauchy/Lorentzian, Geman-McClure, Welsch — **down-weight** large residuals smoothly instead of deleting them; **Barron's general loss** unifies all of these under a *single continuous robustness parameter* that can even be *learned/adapted* per problem [src: barron-2019].
- **RANSAC / Least-Median-of-Squares (LMedS)** — **trim**: fit on minimal random subsets, keep the hypothesis with the largest inlier set (RANSAC) or smallest median residual (LMedS); hard inlier/outlier split.
- **Consensus maximization** — find the estimate explaining the *most* measurements within a tolerance (NP-hard in general).
- **Graduated Non-Convexity (GNC)** (Yang, Antonante, Tzoumas, Carlone, 2020) — solve a sequence of progressively less-convex surrogates of a robust cost, so you reach the robust optimum **without an initial guess**; robust to **70–80% outliers**, beating RANSAC and needing no inlier-threshold tuning, via the **Black–Rangarajan duality** between robust losses and outlier "weight" processes [src: yang-gnc-2020].
In SLAM back-ends this appears as **switchable constraints** (Sünderhauf) and **dynamic covariance scaling (DCS)** — each loop-closure/factor gets a continuous switch/weight estimated jointly with the poses, so bad constraints are smoothly de-activated rather than hard-cut, surviving up to ~1000 false loop closures [src: suenderhauf-switchable, agarwal-dcs]; **AEROS** adapts the robust kernel shape online à la Barron [src: aeros-2022].

**When it applies to us.** Use a **robust kernel (Huber/Cauchy/GNC) on the SfM-vs-LiDAR residuals** inside the §1 factor graph. This is the workhorse for goal (a)+(b) together: it fuses where the two agree and automatically **down-weights** the segments where SfM diverges, *and* the per-factor weight it assigns **is** the disagreement flag for goal (b).

**Over-pruning guard.** This is the **central guard of the whole page**: prefer **down-weighting (M-estimators, switchable constraints, DCS, GNC)** over **hard trimming (RANSAC/LMedS)**. A soft weight keeps a disagreeing-but-real point in the estimate at reduced influence and leaves it *recoverable* if later evidence supports it; a hard cut is irreversible and, applied with a tight threshold, is exactly how you "force an unrealistic fit." Keep the robust scale parameter **honest/loose** (tune it to the noise floor, not to make residuals vanish), and treat down-weighted ≠ deleted: a cluster of consistently down-weighted points is a *finding* (a real cross-sensor difference, cf. the 7 cm scan-plane offset), not garbage to discard.

## 5. Distribution / opinion pooling & conflation (decision theory)

**Core idea.** Combine two *probability distributions* (not just point±covariance) over the quantity:
- **Linear opinion pool** — weighted **average** of the densities (a mixture). Stays multimodal: if the two sources flatly disagree it produces a **two-humped** distribution that *honestly preserves the disagreement* rather than hiding it. No source can veto.
- **Logarithmic opinion pool (log-linear)** — weighted **product**, renormalised. Sharper, unimodal, and **lets a confident source veto** regions the other rules out; this is the distributional form of inverse-variance fusion (product of two Gaussians = Gaussian) [src: logpool-genest, logpool-distributed].
- **Conflation** (Hill, 2008/2011) — the **normalized product** of densities, proven to be the **unique** combination that **minimises loss of Shannon information** when consolidating independent experiments measuring the *same* quantity; for Gaussians it reduces exactly to inverse-variance fusion. Designed for *literally our problem*: "how best to consolidate several independent experiments designed to measure the same unknown quantity" [src: hill-conflation-2008, hill-miller-2011].
- **Bayesian Model Averaging / stacking** — weight whole models by posterior/predictive performance instead of picking one.

**When it applies to us.** Two complementary roles. For **fusion**, conflation/log-pool is the principled justification for the inverse-variance/product fuse of §1 (and tells us *when* it's optimal: independent sources, same quantity). For **flagging**, the **linear pool is the better diagnostic**: per-pose, pool the LiDAR and SfM position beliefs *linearly* — wherever the pooled belief stays **bimodal / wide**, the two sources disagree and the point should be flagged, not fused.

**Over-pruning guard.** The linear pool is structurally anti-over-pruning — it **cannot delete** a source's mass, so a genuine disagreement persists as a second mode you can detect and surface as "unknown," exactly the robust-evidence-principle behaviour. The product/conflation pool *does* let a confident source suppress the other, so apply it **only after** you trust independence and the absence of gross faults — otherwise it will confidently erase a real difference.

## 6. Dempster–Shafer evidence theory & conflict mass

**Core idea.** Represent each sensor's belief as a **mass function** over *sets* of hypotheses (allowing explicit "don't know" mass on the whole frame). **Dempster's combination rule** fuses two bodies of evidence and, crucially, computes a **conflict mass `K`** — the product mass assigned to *contradictory* (empty-intersection) hypotheses. `K` is a **direct, quantitative measure of how much two sources disagree**. The known weakness — **Zadeh's paradox** — is that Dempster's rule *normalises `K` away* (`÷(1−K)`), producing absurd confident answers under high conflict; the fix is to **keep and surface the conflict** via **Yager's rule** (conflict → the universe/ignorance) or **Dubois–Prade / evidence-distance weighted** combinations [src: dempster-shafer-aldous, ds-paradox-2019, ds-iot-2023].

**When it applies to us.** Less natural for continuous poses than §1–4, but the **conflict mass `K` is a clean, principled flag for goal (b)**: discretise the per-pose/per-wall agreement into "LiDAR says here / SfM says here / unknown," and a high `K` on a segment is an *evidence-theoretic alarm* that the two irreconcilably disagree there. It also natively models the **"only one sensor can see it"** case (rig scan-plane offset, [[land-rover-v1-rig]]) via mass on *ignorance* rather than forcing a choice.

**Over-pruning guard.** Use a **conflict-preserving rule (Yager/Dubois–Prade), never raw Dempster normalisation** — Zadeh's paradox *is* the over-pruning failure mode (it makes high-conflict data look like a confident agreement). Routing conflict to **ignorance/"unknown"** is precisely the robust-evidence principle: flag the disputed region as unknown instead of fabricating a fit.

## 7. Anomaly / change-point / disagreement detection for two streams

**Core idea.** Treat the **per-step difference (residual / innovation)** between the two trajectories as a stream and watch it:
- **Innovation gating / NIS χ² test** — the normalized-innovation-squared follows a **chi-square** distribution under "all consistent"; a residual exceeding the χ² gate flags an inconsistent measurement. The standard online consistency test in Kalman/EKF systems [src: nis-chi2].
- **CUSUM** — cumulative sum of residuals detects a **persistent drift/shift** in the mean with asymptotically minimum detection delay for a given false-alarm rate; pairs naturally with a Kalman residual stream to separate *abrupt faults* from *slow drift* [src: cusum-kf, severo-cusum-kf].
- **Change-point detection** — segments the run into regimes, isolating *where along the trajectory* agreement breaks (e.g. one room vs a corridor).

**When it applies to us.** This is the **dedicated machinery for goal (b)**. Run the aligned LiDAR−SfM position/heading residual through a **χ² gate per pose** (instantaneous spikes = candidate mis-associations) **and a CUSUM** (sustained excursion = a real divergent segment, e.g. SfM scale drift or a region only one sensor sees). The two together distinguish a one-frame blunder from a structured, persistent disagreement — the difference between §0's case (3) and case (2).

**Over-pruning guard.** Gating is a **flag, not a delete**: a gated/changed segment should be **routed to down-weighting (§4) or to the conflict/unknown bucket (§5–6)**, *not* removed. CUSUM specifically guards against over-pruning by demanding **persistence** before alarming — a single noisy frame won't trip it, so you don't trim transient noise that inverse-variance fusion would have correctly averaged. Tune gates to a calibrated false-alarm rate so the threshold is statistical, not chosen to make the data look clean.

## 8. Trust / reliability-weighted fusion & mixture-of-experts gating

**Core idea.** Make the fusion weights **adaptive and context-dependent** instead of fixed. A **mixture-of-experts (MoE)** uses a **gating network** that judges the *instantaneous reliability* of each expert (sensor) from context and outputs a per-point/per-region weight distribution; **adaptive multimodal fusion** does the same with a learned or heuristic trust signal, favouring different sensors in different regions [src: moe-fusion, choosing-smartly-2017]. **Hierarchical Bayesian data fusion** is the principled (non-learned) version: a layer of latent reliability variables modulates each sensor's weight [src: hier-bayes-fusion].

**When it applies to us.** We *know* the reliability is region-dependent: SfM is good in texture-rich, well-lit areas and bad on blank walls / low-parallax motion ([[passive-stereo-robustification]]); LiDAR is good on flat walls and weaker in clutter ([[indoor-cluttered-slam]]). A **gating signal need not be a neural net** — a simple heuristic gate from SfM inlier count / reprojection RMS / local feature density, and LiDAR scan-match score, gives a **per-region trust weight** that feeds the robust factor weights of §4. This is the most direct way to encode *"trust LiDAR for geometry, trust the camera where it has texture."*

**Over-pruning guard.** Reliability-weighting is intrinsically soft (a continuous trust weight, never a delete) — its guard is to **bound the weights away from 0/1** so a low-trust sensor is *attenuated, not silenced*, and to make the gate depend on **sensor-internal quality signals** (inlier count, match score) rather than on **agreement with the other sensor** — gating on agreement is circular and would suppress exactly the real-but-disagreeing data we must preserve.

---

## Synthesis — what to actually do with our two trajectories

A single coherent pipeline reuses most of the above without picking one in isolation:

1. **Align** the SfM trajectory into the LiDAR frame with the **known +99° yaw as a hard constraint**, solving only the residual offset (Umeyama/Horn) — and treat a large residual rotation as a *calibration alarm*, not data to fit (§0).
2. **Fuse** by adding SfM as factors into the LiDAR pose graph (§1), under a **robust kernel (Huber/GNC or switchable constraints/DCS)** so agreement averages-down and divergence down-weights (§4) — the inverse-covariance weighting makes LiDAR-for-geometry automatic.
3. Because the two are **correlated by an unknown amount**, sanity-check the fused covariance with **Covariance Intersection** so the result is *honest, not over-tight* (§2).
4. **Flag** divergence on the residual stream with a **χ² gate (spikes) + CUSUM (sustained drift)** (§7), and route flagged segments to **down-weight or "unknown"** (§5 linear pool / §6 conflict mass) — **never delete** (§4 guard).
5. Drive the robust weights with a **simple reliability gate** from each sensor's *internal* quality signals (§8), not from cross-agreement.

The result feeds [[global-alignment-wall-refinement]] as a cleaner, trust-weighted trajectory, and the flagged-as-unknown regions are an honest output (the robust-evidence principle), not a fitting failure.

---

## Sources

- [src: julier-uhlmann-ci-1997] S. J. Julier & J. K. Uhlmann, *A Non-divergent Estimation Algorithm in the Presence of Unknown Correlations*, American Control Conf. (ACC) 1997 — original Covariance Intersection. https://ui.adsabs.harvard.edu/abs/1997acc.....4...35J/abstract
- [src: ci-revisited] *Estimation Under Unknown Correlation: Covariance Intersection Revisited* — IEEE TAC; consistency for any true correlation, ω chosen to minimise trace/det. https://www.researchgate.net/publication/260661631_Estimation_Under_Unknown_Correlation_Covariance_Intersection_Revisited
- [src: ici-2017] B. Noack et al., *Decentralized Data Fusion with Inverse Covariance Intersection*, Automatica 2017 — tighter ICI variant. https://www.sciencedirect.com/science/article/abs/pii/S0005109817300298
- [src: ci-partial-2022] *Covariance Intersection fusion with element-wise partial knowledge of correlation*, Automatica 2022. https://www.sciencedirect.com/science/article/abs/pii/S0005109822000127
- [src: da-wikipedia] *Data assimilation* — overview of 3D-Var, 4D-Var, EnKF, hybrid EnVar (NWS 3D-Var 6-hourly; ECMWF 4D-Var 12 h window). https://en.wikipedia.org/wiki/Data_assimilation
- [src: gabbard-var] J. Gabbard, *Variational Data Assimilation: 3D-Var and 4D-Var* (MIT 16.940) — the J = background + observation cost derivation. https://www.mit.edu/~jgabbard/assets/16940_Final_Project.pdf
- [src: lorenc-4dvar-enkf] A. C. Lorenc, *Relative Merits of 4D-Var and Ensemble Kalman Filter*, ECMWF — covariance inflation, flow-dependent B, hybrid. https://www.ecmwf.int/sites/default/files/elibrary/2003/10817-relative-merits-4d-var-and-ensemble-kalman-filter.pdf
- [src: hunt-letkf] B. R. Hunt, E. J. Kostelich, I. Szunyogh, *Efficient Data Assimilation for Spatiotemporal Chaos: a Local Ensemble Transform Kalman Filter (LETKF)*, arXiv physics/0511236. https://arxiv.org/pdf/physics/0511236
- [src: barron-2019] J. T. Barron, *A General and Adaptive Robust Loss Function*, CVPR 2019 — single-parameter family unifying Huber/Cauchy/Geman-McClure/Welsch; adaptive robustness. https://openaccess.thecvf.com/content_CVPR_2019/papers/Barron_A_General_and_Adaptive_Robust_Loss_Function_CVPR_2019_paper.pdf
- [src: yang-gnc-2020] H. Yang, P. Antonante, V. Tzoumas, L. Carlone, *Graduated Non-Convexity for Robust Spatial Perception: From Non-Minimal Solvers to Global Outlier Rejection*, IEEE RA-L 2020 (arXiv 1909.08605) — GNC, Black–Rangarajan duality, 70–80% outlier robustness, no initial guess. https://arxiv.org/abs/1909.08605
- [src: suenderhauf-switchable] N. Sünderhauf & P. Protzel, *Switchable Constraints for Robust Pose Graph SLAM*, IROS 2012 — per-loop-closure switch variables. https://nikosuenderhauf.github.io/projects/switchableConstraints/
- [src: agarwal-dcs] P. Agarwal et al., *Robust Map Optimization using Dynamic Covariance Scaling (DCS)*, ICRA 2013 — closed-form switch, no extra variables. (carried via [src: aeros-2022])
- [src: aeros-2022] M. Ramezani et al., *AEROS: Adaptive Robust Least-Squares for Graph-Based SLAM*, Frontiers in Robotics & AI 2022 (arXiv 2110.02018) — online Barron-style adaptive kernel in the SLAM back-end. https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2022.789444/full
- [src: logpool-genest] C. Genest & J. V. Zidek, *Combining Probability Distributions: A Critique and an Annotated Bibliography* / *Aggregating opinions through logarithmic pooling*, Theory and Decision — linear vs log pool properties (veto, unimodality). https://link.springer.com/article/10.1007/BF00140056
- [src: logpool-distributed] *Distributed Bayesian filtering using logarithmic opinion pool for dynamic sensor networks*, Automatica 2019. https://www.sciencedirect.com/science/article/abs/pii/S0005109818303704
- [src: hill-conflation-2008] T. P. Hill, *Conflations of Probability Distributions*, arXiv 0808.1808 (Trans. AMS 2011) — normalized product = unique minimum-Shannon-information-loss consolidation of same-quantity experiments. https://arxiv.org/pdf/0808.1808
- [src: hill-miller-2011] T. P. Hill & J. Miller, *How to Combine Independent Data Sets for the Same Quantity*, Chaos 21(3):033102 (2011), arXiv 1005.4978. https://arxiv.org/abs/1005.4978
- [src: dempster-shafer-aldous] G. Shafer, *Combination of Evidence in Dempster–Shafer Theory* (overview, conflict mass K, Dempster's rule). https://www.stat.berkeley.edu/~aldous/Real_World/dempster_shafer.pdf
- [src: ds-paradox-2019] *Paradox Elimination in Dempster–Shafer Combination Rule with Novel Entropy Function*, Entropy/Sensors 2019 (PMC6865203) — Zadeh paradox, Yager/Dubois–Prade conflict handling. https://pmc.ncbi.nlm.nih.gov/articles/PMC6865203/
- [src: ds-iot-2023] *Multisensor Data Fusion in IoT Environments in Dempster–Shafer Setting: An Improved Evidence-Distance-Based Approach*, Sensors 23(11):5141 (2023). https://www.mdpi.com/1424-8220/23/11/5141
- [src: nis-chi2] Normalized-Innovation-Squared (NIS) χ² consistency / innovation gating — standard Kalman/EKF consistency test (Bar-Shalom, *Estimation with Applications to Tracking and Navigation*); applied for anomaly/fault detection. (textbook standard; cf. [src: severo-cusum-kf])
- [src: cusum-kf] M. Severo & J. Gama, *Change Detection with Kalman Filter and CUSUM*, Discovery Science / LNCS 2006 — regression+KF+CUSUM residual change detector. https://link.springer.com/chapter/10.1007/11893318_25
- [src: severo-cusum-kf] *Kalman Filter Changepoint Detection and Trend Characterization* — KF innovation monitoring for change points. https://www.researchgate.net/publication/337794541_Kalman_Filter_Changepoint_Detection_and_Trend_Characterization
- [src: moe-fusion] *Mixture-of-Experts for multi-modal sensor fusion* — gating network estimates instantaneous per-expert reliability, per-point input-conditional weighting (MoME and related). https://www.emergentmind.com/topics/multi-modal-sensor-fusion
- [src: choosing-smartly-2017] O. Mees, A. Eitel, W. Burgard, *Choosing Smartly: Adaptive Multimodal Fusion for Object Detection in Changing Environments*, IROS 2017 (arXiv 1707.05733) — learned gating of sensor reliability. https://arxiv.org/pdf/1707.05733
- [src: hier-bayes-fusion] *Hierarchical Bayesian Data Fusion for Robotic Platform Navigation*, arXiv 1704.06718 — latent reliability variables modulate sensor weights. https://arxiv.org/pdf/1704.06718
- [src: zhang-tutorial-2018] Z. Zhang & D. Scaramuzza, *A Tutorial on Quantitative Trajectory Evaluation for Visual(-Inertial) Odometry*, IROS 2018 — Umeyama/Horn alignment, ATE, Sim(3) vs SE(3). https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf
- [src: evo-umeyama] M. Grupp, *evo* trajectory-evaluation toolbox — Umeyama alignment in practice (SE(3) when scale observable, Sim(3) for monocular). https://github.com/MichaelGrupp/evo
- [src: prototype] drone-prototype: LiDAR ATE ~0.024 m vs visual ~0.163 m and SfM-into-map localization, carried via [[lidar-visual-fusion-slam]], [[relocalization-method-bakeoff]], [[land-rover-v1-rig]] (scan-plane offset → only-one-sensor-sees-it case).

## Related

- [[sfm-error-sources.md]] — why the SfM signal is the deformable one: monocular scale drift / gauge freedom / degenerate motion produce the smooth warp this page reconciles
- [[lidar-visual-fusion-slam]] — where our two signals come from; the coupling spectrum and why we're *de facto* loosely-coupled already
- [[global-alignment-wall-refinement]] — the plane/line-constrained pose refinement the reconciled trajectory feeds into
- [[2d-lidar-slam]] — the Cartographer/SLAM-Toolbox pose-graph back-end (the MAP substrate of §1)
- [[slam]] — concept hub: localization + mapping + loop-closure
- [[relocalization-method-bakeoff]] — the hloc SfM front-end that produces the visual trajectory we fuse
- [[camera-lidar-temporal-calibration-and-pose-interpolation]] — the time-sync / extrinsic tie between the two trajectories
- [[land-rover-v1-rig]] — the rig geometry / scan-plane offset: the canonical "real disagreement, not error" case the over-pruning guards protect
- [[passive-stereo-robustification]] — why SfM is the less-reliable signal (texture/parallax dependence) → the region-dependent trust of §8
- [[indoor-cluttered-slam]] — LiDAR failure modes (symmetric corridors, clutter) that motivate region-dependent gating
