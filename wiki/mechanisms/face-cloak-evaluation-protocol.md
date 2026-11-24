# Face-cloak evaluation protocol (alignment and threshold defects)

Parlayici, Aptoula & Saygin (Sabanci Univ.; arXiv 2611.21923, preprint) argue that published >90% black-box protection numbers for adversarial face-privacy cloaks (Fawkes, LowKey, TIP-IM, AMT-GAN, CLIP2Protect, DiffAM lineage) come from a flawed protocol: no detect/align/crop front end, inherited thresholds, and a saturating success-rate metric. Under realistic pipelines protection is much lower and method rankings change. A caveat page for individual image-cloak efficacy claims, including [[tools/seal-face-cloaking]] and [[tools/nightshade-glaze]].

## Findings

- Re-scoring the same protected files through detect, 5-landmark align, crop costs MI-FGSM 56% of dodging protection (30.5 of 54.8 pp); a budget-allocating attack loses 7%.
- Cause is a resampling mismatch (aligned crop resamples ~1.28x), not lost information. Optimising through a differentiable alignment operator recovers +24 to +58 pts on unseen recognizers and a commercial endpoint.
- Nine of 13 surveyed methods copy one threshold table; it admits 2.3-5.4% false accepts vs nominal 1%.
- Success-rate differences saturate (8.2x swing vs 1.34x real effect); paired cosine shift proposed instead.
- Published method ranking does not survive correction (the one aligning method understated by 25.2 pp).

## Limits

Input defect established on dodging only; no impersonation drop at calibrated thresholds; one recognizer (MobileFace) disagrees; second commercial endpoint weakly protected. Preprint, not peer-reviewed. Code stated at github.com/7unahan/privacy_treshold (abstract says "will be released"; unverified).

## Design implication

Consumer cloaking tools must be evaluated and optimised against detect-align-crop front ends with per-pipeline threshold calibration. Individual protection, no collective angle. Tempers efficacy claims; consistent with the wiki's "obfuscation is narrow-applicability" recalibration ([[strategies/obfuscation-strategic-readout]]).

## Source

- `raw/research/weekly-2026-11-23/02-adversarial-face-privacy-reevaluation.md` — https://arxiv.org/pdf/2611.21923 (academic preprint; trust medium-high; ingest summary read only part of the source).

## Related

- [[tools/seal-face-cloaking]] — resampling mismatch explains its reported resize fragility
- [[tools/nightshade-glaze]]
- [[mechanisms/obfuscation]]
- [[mechanisms/adversarial-data-poisoning]]
- [[mechanisms/unlearnable-trajectories]]
- [[mechanisms/meta-raybans-nametag-surveillance]] — the threat model
- [[counter-power/dp-audit-methodology]]
