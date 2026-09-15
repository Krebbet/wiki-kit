# Mecanum Wheel Handedness — the X rule

**Summary.** Mecanum wheels are **handed**: a set is two left- and two right-handed wheels (rollers mirrored at ±45°), and they are not interchangeable. Viewed from directly above (mast/front at the top), the top-visible roller lines of the four wheels must draw an **X** — every roller points at the robot's centre. Any other arrangement silently changes what every drive command does, and no channel map or sign table can compensate. On this project's rover the "wrong turn-direction sign" chased across three sessions (drone-prototype parked item P-00047) was this: the wheels had been mounted in a **V**, so a rotate command became a **strafe** with a little turn. Swapping the two rear wheels fixed it; the turn sign then verified first time. *(measured on the rig, 2026-09-14)*

## The rule

```
        front / mast
   FL  \        /  FR
   RL  /        \  RR
```

Ignore any L/R stamped on the hubs — vendors do not agree on what the letters mean. Check the X.

## Why (one line)

A driven mecanum wheel pushes the vehicle *along its contact roller's axis* (the roller cannot slide along its own axis; it rolls freely across it). With a differential mix (left pair, right pair) the result of a rotate command depends only on the arrangement:

| arrangement (top rollers, from above) | forward | rotate (left back, right fwd) |
|---|---|---|
| **X** — `\ /` front, `/ \` rear | straight | **spin**, no drift; torque ∝ wheelbase + track |
| **V** — `\ /` front, `\ /` rear (each side one handedness) | straight, wheels fight | **strafe** + a little turn |
| O — `/ \` front, `\ /` rear | straight | torque ∝ track − wheelbase → almost nothing |

## Symptoms that mean "check the X"

- A diagonal pair "works harder / falls out of sync" on a straight command.
- A rotate command produces a sideways stride, or a turn in the *wrong* direction with lateral drift.
- Sign/channel tables verified wheels-up on a stand look right but the rover misbehaves on the floor — bare axles cannot show which way the rover would travel.

## Procedure (from the prototype)

drone-prototype `docs/wheel-calibration.md` §Procedure C: (1) photograph from above, confirm the X; (2) wheels-up `wheel_walk.py` spins each *logical* wheel alone and asks which *physical* wheel turned — labels, not just directions; (3) then, and only then, verify the turn sign on the floor with one question per fact ("did it rotate CCW?" — not a two-part question). Consequence for odometry: mecanum rollers compress and scrub, so the effective rolling circumference (0.282 m) is −7 % vs geometric and the effective track for rotation is wider than the chassis — see [[odometry-self-calibration-classical]] §What this rig measured.

## Source

drone-prototype `docs/wheel-calibration.md` §Procedure C + §Turn direction (2026-09-14); `docs/prototype-diary.md` 2026-09-14 (evening) "P-00047 closed"; hardware-debug-ladder memory (rung 2 = vendor docs/hardware setup before code).

## Related

[[land-rover-v1-rig]] · [[land-rover-v1-build-guide]] · [[odometry-self-calibration-classical]] · [[learned-odometry-correction]] · [[home-tidy-drone-prototype]]
