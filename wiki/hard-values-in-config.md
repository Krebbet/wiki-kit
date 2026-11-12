# Hard values live in config, rules in one index (drone-prototype EDA354)

A project rule set by the human on 2026-11-12, and how it was applied to the rover's codebase. **Every shared or
safety-relevant number lives once, in `config/*.json`, read through one leaf loader. Every rule has one row in a rules
index naming who decided it, where it is implemented, and its config keys.** The human's words: "We shouldn't have
repeat values in a bunch of different places ... It is crazy that we have battery cutoff written all over the code."
A heavier YAML rule registry (EDA352, PR #270) was proposed and not adopted. The plain index won.

## Source

drone-prototype repo, master `1fda3950`:
- `eda/EDA354-config-values/FINDINGS.md` (PR #273): inventory, stage-1 scope, behaviour check, plan for stages 2+ (§6)
- `docs/rules-index.md`: the index; `docs/architecture/README.md` rule 26 (values in config, read through `drone/params.py`)
- `eda/EDA354-config-values/inventory.py` (AST scan of constants, dataclass defaults and argparse defaults)
- parked P-01260 (stages 2+), P-01261 (env switches not yet declared in the loader), P-01267 (`FLOOR_Z_M` has five meanings)

## What the inventory found (before stage 1)

- 1,548 hard-coded numbers in `src/drone` and `src/rover`: 1,344 constants, 96 dataclass defaults, 108 CLI defaults.
- 84 constant names defined in more than one file: 40 with the same value, **44 with different values**.
- 10 CLI options repeated their default across 2–10 tools.
- Classes: (a) physical / rig measurement, (b) behaviour or rule parameter, (c) code constant (math, enum, protocol).
  The classes were assigned by a heuristic; the stage-1 values were checked by hand.

## The method (stage 1)

1. Move the shared, safety-relevant values into a few config files (power, body, floor bands, hard tiers), read through
   **one leaf loader** (`drone/params.py`) that imports nothing from the project.
2. **Delete every literal copy.** A test fails, by name, if a copy comes back.
3. Declare environment overrides **only in the loader**. Env overrides of safety switches stay allowed on the live
   rover (human 2026-11-12: "we control them").
4. Prove behaviour identical. 97 of 103 affected values were bit-identical. The other 6 were library copies that now
   equal their source, and changed no grid cell. The one intended change was a stale 10.6 V battery cutoff in a
   diagnostic, which now reads the config's 10.3 V.
5. The rules index names the config **key**, never a copy of the number. A new or changed rule gets its row in the same PR as the code.

## Lessons worth keeping

- Copies drift silently. 44 same-named constants already disagreed before anyone looked.
- One name can hide several meanings (`FLOOR_Z_M`: five). Split the name before you centralise it, or centralising
  merges meanings that should differ.
- Values that a tool rewrites (the rig calibration file, rewritten by a rig pull) cannot be the single source for a
  hand-set rule value (P-01268).

## Related

- [[system-architecture]] · [[mapping-stack-design]]
- [[open-source-rover-stack-options]]: ROS 2 parameter servers are the off-the-shelf form of the same rule
