# Floor vs Small Floor-Object Detection: Methods and Error Modes

Research page (2026-11-13, DRAFT for lead review). The question: how do comparable robots tell the floor apart from small ground objects (cords, socks, toys, pet waste)? What are the known failure modes, and which methods fit a consumer-cost rover? The rover has a tilted 2D LiDAR (RPLIDAR C1), the SVPRO stereo camera and an IMU, runs on a laptop CPU, and blocks anything over 2 cm. Project measurements live in drone-prototype EDA342 / EDA356 / EDA358 / EDA359.

> **Bottom line.** Shipping robots measure low-object height with a dedicated near-field active sensor (structured light or a line laser) and use the camera only for semantics. Research systems avoid enumerating object classes: they **verify the floor** and treat everything else as an anomaly (Jenkin & Jepson 1994; SegmentMeIfYouCan's road-obstacle track), often with a floor-appearance model **self-supervised from range data** (Ulrich & Nourbakhsh 2000; Maier et al. 2011; Wild Visual Navigation 2023). For us that means: (1) a class-agnostic "is this floor" model trained from LiDAR-confirmed floor; (2) local per-cell statistical floor tests with a real per-return noise model; (3) a LiDAR scan-plane flatness term in self-calibration; (4) a stereo floor-homography parallax check as an independent height method.

---

## 1. What comparable robots do

| family | floor / object separation | source |
|---|---|---|
| Roborock Reactive AI 2.0 | 3D structured light (range "ruler") + RGB camera + NPU classifier for 27 obstacle types; reviews report thin cables / shoelaces are inconsistent | [Roborock support](https://support.roborock.com/hc/en-us/articles/33954016850713); [review (weak)](https://shopsavvy.com/answers/how-effective-is-the-obstacle-avoidance-on-the-roborock-s8-maxv-ultra) |
| Ecovacs AIVI 3D | structured light + AI RGB camera; T50 adds a VLM and a strip light | [Ecovacs](https://www.ecovacs.com/uk/blog/robot-vacuum-obstacle-avoidance) |
| iRobot j7 PrecisionVision | front RGB classifier (pet waste, cords, shoes) trained on >1 M images | [iRobot P.O.O.P.](https://protect.irobot.com/poop); [[robot-vacuum-navigation]] |
| Line-laser vacuums | a cheap line laser + camera gives near-field height; flat cables are still the hardest class | [robovacguide (secondary)](https://robovacguide.com/how-obstacle-avoidance-works/) |
| Local ground segmentation | concentric-zone, region-wise plane fits + ground likelihood, >40 Hz; a global plane fails on real ground | Patchwork arXiv:2108.05560; Patchwork++ arXiv:2207.11919 |
| Small-hazard stereo | free-space vs obstacle **hypothesis tests on local patches**, no global road model; 5 cm at 20 m | Pinggera et al., IROS 2016, arXiv:1609.04653 |
| Elevation maps | per-cell height with **confidence bounds**; pose covariance propagated (robot-centric) | Fankhauser et al., RA-L 2018 |
| Floor Anomaly Detection | stereo: verify where the planar-floor assumption holds; anomalies = hoses, tools, drains | Jenkin & Jepson, BMVC 1994 |
| Ground-pixel parallax | robot-motion ground pre-calibration + parallax + appearance (random forest); TPR 77.5 vs 61.7 %; sensitive to odometry error > ±5 % / 0.011 rad | Xue et al. 2024, arXiv:2401.01445 |
| Floor-first segmentation | segment floor, then obstacles inside it; 96.3 % detection, 2.2 FP/frame indoors (RGB-D) | Hua et al., ICCVW 2019, arXiv:1908.11675 |
| Self-supervised floor appearance | floor colour histograms learned while driving | Ulrich & Nourbakhsh, AAAI 2000 |
| Laser-labelled image classifier | image obstacle detector trained online from sparse laser data | Maier, Bennewitz, Stachniss, ICRA 2011 |
| DINO-feature traversability | ViT features + small online-trained head; < 5 min bootstrap | Frey et al., RSS 2023, arXiv:2305.08510 |
| Patch anomaly detection | DINOv2 nominal-patch memory bank, kNN distance, training-free | AnomalyDINO, WACV 2025, arXiv:2405.14529 |
| LiDAR + camera fusion | LiDAR confidence map concatenated to the image for small-obstacle segmentation | Singh et al., IROS 2020, arXiv:2003.05970 |
| Thin structures | stereo misses cables (tiny image coverage); use edge reconstruction over video | Zhou et al., CVPRW 2017, arXiv:1708.04006 |

## 2. Error modes (literature → ours)

- **Sensor tilt / extrinsic error makes the floor look sloped.**
  - Literature: self-calibrate roll and pitch from the ground plane (Meyer, Auburn 2021; ROS `depth_nav_tools`).
  - Ours: a rover-fixed lateral term of -4.7..-5.1 cm/m at -20° (EDA359).
- **The scan plane is not flat by spec.**
  - The C1 datasheet lists "Scan Field Flatness 0°~1.5°" ([datasheet](https://files.waveshare.com/wiki/RPLIDAR-C1/SLAMTEC_rplidar_datasheet_C1_v1.0_en.pdf)).
  - *Inference:* a planar scan-plane tilt gives a tilt-independent lateral term of up to about 2.6 cm/m. That is a candidate for EDA359's "about half tilt-constant" part, and it is untested.
- **Per-return noise is about the size of the threshold.**
  - The C1 spec is ±30 mm accuracy and 15 mm resolution, worse below 10 % reflectivity (black range 6 m vs 12 m).
  - Ours: the 2-return rule false-BLOCKs 1 cm items on 27–47 % of spots (P-01173). Averaging works (EDA342 residual 1.5 mm p50); single returns don't.
- **Mixed pixels at edges** produce phantom heights ([ISPRS 2020](https://isprs-archives.copernicus.org/articles/XLIII-B1-2020/157/2020/)). They are a likely source of the heavy floor-height tails (*inference*).
- **Thin objects fall below the footprint.** Cables are the hardest class for both vacuums and stereo (Zhou 2017).
- **Smooth floor models absorb wide flat objects.** Our GMRF swallows a 1 cm board and a 1.5 cm box (EDA342).
- **Look-alike textures.**
  - Sevastopoulos et al. 2023 (arXiv:2311.01966): tiles read as floor.
  - Open-vocabulary detectors give confident false positives on absent queries (arXiv:2406.19057).
  - Ours: 55–70 % false alarms on the vent grille and baseboard (EDA358).
- **Systematic detector blind spots.** Location and prompt matter more than semantic content (Mütze et al. 2025, arXiv:2506.23751). Ours: misses correlated across stations, M(k) ≫ 0.5^k (EDA356).
- **Label confusion.** Ours: "remote control" for a cable; the exceptions list loses most cords (EDA356).
- **Occlusion / coverage.** Ours: the camera rarely looks at LiDAR-blind cells (EDA356).
- **Pose error smears maps.**
  - Literature: propagate pose covariance (Fankhauser 2018).
  - Ours: the human prefers local floor fits while the rig error remains.

## 3. Ranked options for this project

All run on CPU and can be tested offline on recorded worlds first.

1. **"Is this floor" appearance model, self-supervised from LiDAR-flat floor.**
   - Method: LiDAR-flat pixels → a DINOv2 (or colour/texture-histogram) patch bank → kNN anomaly score.
   - It is class-agnostic, so it should decorrelate misses from Grounding DINO's, and it covers every pixel.
   - Test: per-look miss / M(k) and bare-floor + look-alike false alarms on EDA356's truth, held out on office-fresh1, alone and OR-ed with DINO.
2. **Local per-cell statistical floor test with a measured per-return noise model.**
   - Method: Pinggera hypothesis test + Fankhauser variance; uncertain cells mean "check", not "block".
   - Test: replay plus EDA342 synthetic injection; false-BLOCK rate on drive-over items vs recall at ≥ 2 cm.
3. **Scan-plane flatness term in self-calibration.**
   - Method: a beam-elevation harmonic e(α) in the LiDAR frame.
   - Test: re-fit EDA359's reversal pairs and the 380 stations; does the tilt-constant share vanish? Does it pass planted-truth recovery?
4. **Stereo floor-homography parallax (FAD).**
   - Parallax ≈ f·B·Δh / (Z·h). With f ≈ 1089 px, B = 62 mm and h ≈ 0.4 m, a 2 cm object at 1 m gives about 3.4 px (*inference*).
   - Test: warp right→left by the local LiDAR floor plane; score the residual on the judged items.
5. **Floor mask via MobileSAM prompted with LiDAR-floor points; holes = object proposals.**
   - Cost: about 3 s per image on CPU (arXiv:2306.14289).
   - Gives tight extents for the camera-proposes / LiDAR-eliminates loop.

Lower: detector hard-negative prompts or fine-tuning (keeps class enumeration; use a crop classifier for the cord/tape exceptions list instead); monocular depth (Depth Anything V2: percent-level metric error is several cm at 1 m, so a proposal cue only); a line-laser add-on (the industry answer, but new hardware; see [[floor-map-sensing-options]] §2).

## Source
Inline citations above (web sources, 2026-11-13 research subagent dispatched by the drone-prototype prototyper for EDA368). Project measurements cited: drone-prototype EDA342 / EDA356 / EDA358 / EDA359; the follow-on project record is [[floor-check-visual-first]].

## Related
[[robot-vacuum-navigation]] · [[consumer-robot-vacuum-mapping]] · [[floor-map-sensing-options]] · [[passive-stereo-robustification]] · [[camera-calibration-and-self-calibration]] · [[close-range-depth-sensors]] · [[economical-ir-depth-cameras]] · [[floor-check-visual-first]] · [[visual-floor-anomaly-methods]]
