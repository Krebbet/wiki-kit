---
url: "https://moonlakeai.com/blog/why-world-models-need-structure-not-just-scale"
title: "Why World Models Need Structure, Not Just Scale"
captured_on: "2026-04-21"
capture_method: "url"
assets_dir: "./assets"
---

The idea of typing a single prompt and instantly generating a world you can inhabit, explore, and interact with is deeply compelling. But how close are we actually to this vision?

When we evaluate world simulators, we find that progress is best understood along two largely orthogonal axes: how good the world looks, and how well it responds to interaction. Visual realism matters, but so does coherence under motion, action, and time.

## What Immersion Really Demands

When you turn your head, you expect nearby surfaces to shift more than distant ones. When you move through space, the world should respond smoothly and predictably. If these expectations are violated — if motion is inconsistent, if objects drift in appearance, or if turning 360 degrees fails to return you to the same scene — immersion collapses.

Even when motion is correct, subtle failures break the illusion: a car moves properly, but its color changes; an object re-enters view but is no longer quite the same. Once interaction enters the picture, expectations rise further — contact, friction, and deformation must all behave sensibly and consistently.

These are not aesthetic preferences. They are structural constraints imposed by the fact that the world we inhabit is three-dimensional. Any simulator meant for human immersion — or for training embodied agents — must encode these constraints either explicitly or implicitly.

## Two Axes, Two Paradigms

Optimizing for visual realism and optimizing for interaction realism pull technology in different directions. Visual realism favors 2D video: it is a native human medium, abundant at scale, and diffusion transformers improve reliably with more data and parameters.

Interaction realism favors explicit 3D. Persistence, object identity, camera coherence, and physical plausibility all emerge naturally when the world is represented in three dimensions.

The challenge is that each paradigm struggles to borrow the other’s strengths for free. Video models must infer 3D structure implicitly from pixels, which is fragile under long horizons or novel interactions. 3D pipelines, meanwhile, do not automatically inherit the visual richness of large-scale video data.

## Why Scaling Video Alone Does Not Suffice

For a video model to function as a true world simulator, it must respond accurately to user actions and internalize 3D principles. Both requirements are difficult under a purely data-driven, 2D paradigm.

Action-paired video is far scarcer than passive footage, and the problem worsens as actions become continuous and compositional. This is why most world models plateau at discrete controls, while richer interaction spaces remain largely unexplored.

More fundamentally, asking a latent video model to spontaneously discover a stable, persistent notion of 3D state from pixels alone is an ill-posed task. It requires rediscovering physical structure that we already understand — inside a high-dimensional representation not designed for it.

## Reframing the Role of 3D

A common objection is that explicit 3D does not scale. It is true that today’s 3D generative models cannot match video in poly detail, materials, or cinematic lighting.

But the coherence we need from 3D — persistence, motion consistency, and physical simulability — exists at a much coarser scale. For these purposes, current 3D models are already sufficient.

This suggests a different paradigm: use vibe-generated, lightweight 3D scenes as structural scaffolds, and let video diffusion models render them into high-fidelity imagery. The goal is not to replace video, but to constrain it.

## Distilling Coherence Without Compromising Appearance

In practice, this hybrid approach has struggled because coarse 3D often leaks low-quality appearance into the final output. Textured renders enforce identity but import poor materials and lighting; untextured signals like depth avoid this, but under-specify identity.

We believe this tension arises because texture plays two roles at once: it encodes material identity, and it prescribes appearance. These roles need to be disentangled.

Our approach binds neutral, information-free latent codes to the mesh — texture-like in their ability to disambiguate material patches, but without encoding color, shading, or style. These codes persist across space and time, biasing the diffusion model to render each patch consistently without dictating how it should look.

## Constraining the Right Subspace

Conceptually, this restricts video generation to a 3D-coherent submanifold of its natural output space. Unlike approaches that steer diffusion toward out-of-distribution exemplars, this preserves visual diversity while enforcing structural invariants.

The result is a workflow that preserves vibe-codeability, inherits coherence from explicit 3D, and maintains the visual potency of video diffusion.

## Outlook

World simulation does not require choosing between beauty and structure. It requires using each representation where it is strongest.

By constraining high-fidelity generative video with explicit 3D structure — while carefully disentangling appearance from coherence — the problem of world simulation becomes concrete and tractable.

This is why we believe structure, not scale alone, is the shortest path to worlds that can truly be played.

## About Moonlake

We are a frontier research lab building world models.

If you share this vision, [join us](https://jobs.ashbyhq.com/Moonlake) or get in touch at [[email protected]](/cdn-cgi/l/email-protection#b9dad6d7cdd8dacdf9d4d6d6d7d5d8d2dcd8d097dad6d4)