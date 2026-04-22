# World Models: Pure Video Scaling vs Explicit 3D Structure

**Status:** open. Pre-flagged from radar-2026-04 ingest. Pure-video-scaling source not yet captured.

## Position A — Pure video diffusion at scale cannot yield interactive world simulators

**Source:** [[moonlake-world-models]] (Moonlake position post).

**Claim:** *"Asking a latent video model to spontaneously discover a stable, persistent notion of 3D state from pixels alone is an ill-posed task."* Action-paired training data is scarce; 3D recovery from pixels is under-constrained. Therefore pure video scaling cannot deliver interactive world simulation; **explicit 3D structure must be supplied as a scaffold**.

**Basis:** Section "Why Scaling Video Alone Does Not Suffice", paragraphs on action-paired data scarcity and ill-posed 3D recovery from pixels.

Moonlake's proposed alternative is a hybrid: coarse explicit 3D meshes + neutral information-free latent codes bound to mesh patches → conditioning a video diffusion transformer.

## Position B — Pure video scaling solves coherence

**No source captured.** Awaiting an ingest of a Sora-class or Genie-class paper that argues large-scale video diffusion alone produces persistent 3D-coherent generation. Capturing one is the next step to make this conflict resolvable.

## Caveat — Moonlake is a position post

Moonlake's claim has **no quantitative results, no benchmarks, no code, no comparison tables**. It's a research-direction signal from a frontier lab, not a paper. Position B may already exist in published form; the conflict only becomes substantive once a primary pure-video-scaling source is captured and compared on shared evals (camera consistency over time, object identity across occlusion, action-conditional rollout fidelity).

## Resolution rule when Position B arrives

Define "interactive world simulator" precisely (action-conditioned next-frame prediction, multi-step rollout, object permanence under occlusion) and identify shared benchmarks. If a pure-video model reaches Moonlake's interactive thresholds without 3D scaffolds, Position A weakens. If hybrid 3D+video reaches the same thresholds at much lower compute, Position A strengthens.

## Related

- [[moonlake-world-models]], [[sharp-view-synthesis]] (adjacent CV cluster).
- [[conflicts/regression-vs-diffusion-view-synthesis]] — adjacent debate, different scope.
- [[watchlist]] — Sora, Genie, Gen3C, ViewCrafter not captured.
