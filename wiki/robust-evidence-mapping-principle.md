# Robust-Evidence Mapping Principle

The governing project rule (human-stated) for what earns a place in the map: **for every point we keep, we must be able to explain where it came from — if not, it is noise or it is unexplained, and must be flagged, not silently kept.** Reliability is treated as a function of *agreement/redundancy* across independent evidence, not of any single observation. This page exists to give the rule cited across the point-cloud/mapping-refinement cluster ([[point-cloud-denoising-methods]], [[point-cloud-semantic-classification]], [[point-cloud-object-segmentation-models]], [[stereo-3d-mapping-known-poses]], [[3d-shape-completion-for-object-footprints]]) an actual page instead of a dangling citation.

## The rule, precisely

Two equivalent phrasings appear across the citing pages:

> "For every point we keep we must be able to explain where it came from; if not, it is noise or it is unexplained — flag it, do not silently keep it." ([[point-cloud-denoising-methods]])

> "For every point we must be able to explain where it came from; if yes, does it fit our assumptions about co-located points; if no, is it noise or genuinely unexplained?" ([[point-cloud-semantic-classification]])

This decomposes into three dispositions for any candidate point or claim, never two:
1. **Explained and consistent** — keep, with its provenance attached.
2. **Noise** — sparse, unsupported by redundant evidence, discard (or down-weight, never silently trust).
3. **Genuinely unexplained** — coherent and *recurring* but matching no current model — keep as **unknown**, flagged for a human or a downstream detector. This third bucket is the one naive pipelines collapse into either (1) or (2) by mistake; the rule exists specifically to keep it open rather than force a premature call.

The corollary that recurs most often in application: **reliability = agreement/redundancy, not single-observation confidence.** A point (or a claim) that recurs across multiple independent looks — sweeps, sensors, or modalities — is trustworthy; one that appears once, however clean it looks, is not yet earned.

## How it's applied across the wiki

- **Denoising as evidence gating**, not signal processing — keep points that agree with redundant evidence (a surface, a cluster, a stable structure across scans), drop or flag the rest ([[point-cloud-denoising-methods]]).
- **Point-to-primitive accounting** — order matters (gate noise first, fit the most-reliable primitive — walls, since many points agree on one — before objects); every assigned point's residual against its primitive is tracked, and the unexplained residual becomes a first-class **unknown** category rather than being silently dropped ([[point-cloud-semantic-classification]]).
- **Cross-modal agreement as a confidence signal** — when two independent object-proposal routes (a BEV/LiDAR pass and a stereo-SAM lift) agree on an object, that agreement *is* the reliability signal; where only one fires, it's flagged, not trusted outright ([[point-cloud-object-segmentation-models]]).
- **Measured vs. inferred provenance** — an object's observed front/footprint is *measured*; a completed 3D back is *prior-derived*. The two must be tagged with different provenance and a hallucinated completion must never be presented as observed geometry ([[3d-shape-completion-for-object-footprints]]).
- **"Agreement = reliability" for fused stereo** — a point that survives downsample → statistical/radius outlier removal → multi-view consistency has been vouched for by redundancy at each stage; that chain *is* this principle applied to stereo fusion ([[stereo-3d-mapping-known-poses]]).

## Why it's a project principle and not just a denoising heuristic

The rule generalizes past any one sensor or pipeline stage: it's a standing test applied to *any* claim entering the map — a point, an object hypothesis, a completed shape, a cross-sensor residual. The binding failure mode it guards against is silent over-trust: an unexplained observation quietly kept as if it were verified, or a plausible-looking inference quietly presented as measured fact. Both directions of error (silently discarding real structure, and silently keeping unverified structure) are treated as equally wrong — the rule's job is to force an explicit flag instead of a silent default either way.

## Source

Project-internal (human-stated governing principle, not an external citation). The canonical phrasing is carried in [[point-cloud-denoising-methods]] and [[point-cloud-semantic-classification]]; this page consolidates it from its applications across the point-cloud/mapping-refinement cluster rather than introducing new content.

## Related

[[point-cloud-denoising-methods]] · [[point-cloud-semantic-classification]] · [[point-cloud-object-segmentation-models]] · [[stereo-3d-mapping-known-poses]] · [[3d-shape-completion-for-object-footprints]] · [[reconciling-competing-signals]] · [[mapping-stack-design]]
