# The camera vote's "hundreds of inliers" were an uninitialised mask (drone-prototype EDA364, PR OPEN)

A general OpenCV pitfall found in the rover's cold-start "bearings" camera vote. **Status: PR #293 is still OPEN, in
a review fix round (last verdict REQUEST_CHANGES) on 2026-11-13. Nothing here is on master yet, and the numbers may
move. Replay only, one room; nothing ran on the rover (P-01472). Update this page when the PR merges or closes.**

## Source

drone-prototype PR #293 (branch `eda364-camera-vote`): PR body; `eda/EDA364-camera-vote/` on the branch;
`tests/test_camera_vote_eda364.py`. Parked P-01450 (the symptom), P-01462 (wrong accept as a prior), P-01470…P-01474
(on the branch).

## The bug

`cv2.findFundamentalMat` with RANSAC can find no fundamental matrix. In OpenCV 4.13 it then returns `F = None`
together with an **uninitialised inlier mask**. `CameraEvidence._inliers` summed that mask, so it counted garbage
bytes as inliers. A recorded pair with 13 ratio-test matches scored 184–676 "inliers" depending on the heap.

General rule: when `F is None` (or not a single valid 3×3), the mask is meaningless. Count only mask entries equal to
1, and cap the count at the number of matches.

## What it did on the rover

- The live data held 3 wrong decisive camera votes, all for the mirror basin (529, 793 and 1134 "inliers"). Each
  caused a refusal. EDA363 counted accepts only, so it reported 0 ([[relocalisation-far-check]]).
- It also explains the flaky localise test P-01322: a sim camera drawing a wall clock was decisive on 49 / 60 drawn
  seconds before the fix and 0 / 60 after (max 13 inliers).

## The proposed fix (four switches, default ON, in `config/localise.json`)

| switch | rule | what |
|---|---|---|
| `camera_valid_geometry` | 15zb a | inliers only from one valid 3×3 F, mask entries == 1, capped at the match count |
| `camera_room_scope` | 15zb b | only station frames recorded in the loaded map's frame count; sim and new rooms get no camera vote |
| `camera_needs_beams` | 15zb c | a camera win counts only when a beam win backs it; a contrary camera vote still refuses |
| `bearings_verify` | 15zc | after a bearings accept, the next fixes re-check the beaten rivals on the new view; a contradicted fix is refused |

Replay evidence (9 recorded live bearings runs): all 7 accepts kept, the 2 camera-caused refusals become right
accepts, 0 wrong; all 470 valid-F calls count the same as before. For P-01462, replaying each accept from its losing
hypothesis: the far check catches 1 / 6, a cold start 0 / 6, `bearings_verify` 6 / 6.

## Related

- [[relocalisation-far-check]] · [[mcl-shadow-localiser]] · [[new-room-start]] (room / frame scoping)
- [[relocalization-method-bakeoff]] (earlier camera relocalisation work)
