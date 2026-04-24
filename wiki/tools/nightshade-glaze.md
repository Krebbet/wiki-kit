# Nightshade + Glaze (UChicago SAND Lab)

**Glaze** and **Nightshade** are paired software tools developed by the University of Chicago SAND Lab (Security, Algorithms, Networking, Data) under Prof. Ben Zhao and Prof. Heather Zheng. Both operate by adding "barely perceptible" pixel-level perturbations to images that leave human perception intact but cause generative-AI models to see different content. **Glaze is defensive** (protects individual artists from style-mimicry attacks); **Nightshade is offensive** (used by artists collectively, poisons models that scrape their work without consent). The cleanest working real-world case of [[obfuscation|obfuscation-as-counter-power]] applied at scale to a live AI-training extraction pattern.

## Structure

- **Host lab:** UChicago SAND Lab.
- **Team leads:** Ben Zhao (UChicago CS professor), Heather Zheng (UChicago CS professor).
- **Team members (per the Nightshade primary source):** Shawn Shan (Lead), Wenxin Ding, Josephine Passananti, Stanley Wu.
- **Distribution:** direct download via nightshade.cs.uchicago.edu and glaze.cs.uchicago.edu. Not distributed through app stores or browser web stores — avoiding the [[adnauseam|AdNauseam-style]] platform-ban failure mode.
- **Networking:** "Nightshade is designed to run without a network, so there is no data (or art) sent back to us or anyone else" (per the captured Nightshade source). Same for Glaze.

## Scale (per WebSearch preamble, not primary capture)

- **Glaze:** >6 million downloads since March 2023 release (per MIT Tech Review, Oct 2024).
- **Nightshade:** released October 2023; standalone tool as of v1.0. Planned integration with Glaze/WebGlaze for combined one-pass application.
- **Academic publication:** *Nightshade: Prompt-Specific Poisoning Attacks on Text-to-Image Generative Models*, Shan, Ding, Passananti, Zheng, Zhao. Accepted at **IEEE Symposium on Security and Privacy, San Francisco, May 2024.** Preprint: arXiv 2310.13828, February 2024.

## Mechanism

From the captured Nightshade primary source:

- Both tools use "barely perceptible perturbations to an image's pixels so that machine-learning models cannot read them properly."
- **Glaze (defence):** prevents style-mimicry — an AI trained on Glazed images cannot reliably reproduce the artist's style even when prompted.
- **Nightshade (offence):** transforms images into "poison" samples. "A prompt that asks for an image of a cow flying in space might instead get an image of a handbag floating in space." Model behaviour becomes incorrect when trained on enough shaded images.
- **Robustness:** per the captured source, "Nightshade effects are robust to normal changes one might apply to an image. You can crop it, resample it, compress it, smooth out pixels, or add noise, and the effects of the poison will remain. You can take screenshots, or even photos of an image displayed on a monitor, and the shade effects remain." Not steganography; behavioural-signature forging.

## Stated goal (per primary source)

> Nightshade's goal is not to break models, but to **increase the cost of training on unlicensed data, such that licensing images from their creators becomes a viable alternative.**

This is the clearest articulation in captured sources of the **cost-asymmetry lever** as a strategic goal. The attacker (here, artists) does not expect to halt the surveillance / scraping pipeline; they expect to raise its unit cost until the legitimate alternative (licensing) becomes economically preferable. See [[obfuscation]] for the cross-mechanism design principle.

## The Glaze-vs-Nightshade distinction

From the captured Nightshade source:

> Glaze is a defensive tool that individual artists can use to protect themselves against style mimicry attacks, while Nightshade is an offensive tool that artists can use as a group to disrupt models that scrape their images without consent (thus protecting all artists against these models).

Nightshade is **explicitly collective**. The authors describe "artists who post their own art online should ideally have both Glaze AND Nightshade applied to their artwork." Individual poisoning is inefficient; coordinated poisoning is how the mechanism shifts industry behaviour.

## Artist collaborators (per captured Nightshade source)

Per the primary source's listed collaborators: Katria Raden, Karla Ortiz, Eva Toorenent, Jingna Zhang, Kelly McKernan, Jon Lam, Sarah Andersen, Zakuga Mignon, Yujin Choo, Jess Cheng, Steven Zapata, Viktoria Sinner, Edit Ballai, Kim Tran, Kat Loveland, Autumn Beverly, Kim Van Deun, Katharina Jahn, Paloma McClain, Lyndsey Gallant, Nathan Fowkes, "and many more."

## Relevance to dynamic-pricing strategy

*(editorial / synthesis — the captured sources are in the AI-training domain, not the pricing domain.)*

Nightshade/Glaze is the clearest working analogue for [[possible-strategic-levers|strategy-layer levers #10 (adversarial training-data injection) and #11 (fingerprint parity network)]]. Transferable design decisions documented in the primary source:

1. **No network dependency.** Runs client-side; no telemetry. Directly addresses the "tool is a surveillance vector" failure mode that sinks most well-intentioned consumer tools.
2. **Direct distribution.** Not on any app/web store. Not subject to [[adnauseam|AdNauseam-style]] gatekeeper removal.
3. **Robustness to countermeasures.** Explicit design for crop / resample / compress / noise survival — a design budget item that a pricing-obfuscation tool would also need.
4. **Collective use explicitly intended.** The authors' distinction between Glaze (individual) and Nightshade (collective) is the cleanest articulation in captured sources of how obfuscation scales from personal privacy to structural market pressure.
5. **Cost-asymmetry as explicit goal.** The authors do not claim to defeat the model — they claim to raise the cost until licensing becomes viable. A pricing-obfuscation tool should adopt the same framing.

## Risks and limitations (per primary source)

- "Changes made by Nightshade are more visible on art with flat colors and smooth backgrounds." Low-intensity setting available for visual-quality-conscious users.
- "As with any security attack or defense, Nightshade is unlikely to stay future-proof over long periods of time. But as an attack, Nightshade can easily evolve to continue to keep pace with any potential countermeasures/defenses." — the authors explicitly frame it as an evolving adversarial surface, not a solved problem.

## Source

- `raw/research/lever-implementations/02-02-nightshade-primary.md`
  - **Origin:** nightshade.cs.uchicago.edu — Nightshade primary site, UChicago SAND Lab.
  - **Audience:** artists, AI/ML researchers, press.
  - **Purpose:** explain the tool, its mechanism, intended use, and limitations.
  - **Trust:** primary organisational source from the research lab that built the tool. Load-bearing claims (mechanism, stated goals, team, publication status) are all from the primary source.
- `raw/research/lever-implementations/03-03-glaze-primary.md` — Glaze About Us page (same lab). Primary source.
- WebSearch preamble cited MIT Tech Review coverage for the 6M-download figure; the figure is not in the captured primary source and is therefore lower-trust than the rest of this page.

## Related

- [[obfuscation]]
- [[adnauseam]]
- [[possible-strategic-levers]]
- [[collective-bargaining-for-data]]
- [[data-cooperatives]]
