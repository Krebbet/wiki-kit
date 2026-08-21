# How SNNs are trained: surrogate gradients and the alternatives

The map this wiki was missing. Every other SNN page here concerns **inference** — energy per token, spike rates, breakeven thresholds. None of them explains how a spiking network gets its weights in the first place, or what that costs. This page is that explanation, and it turns out to bear directly on the on-chip-learning dispute.

Source is Neftci, Mostafa & Zenke (arXiv:1901.09948), the field's foundational tutorial. **It is a 2019 document.** Where it describes the state of the art, that state of the art is 2019. Any specific benchmark number it quotes should be traced to the primary paper it cites, never treated as current.

## The problem, stated precisely

An SNN is formally an RNN whose output nonlinearity is a **Heaviside step function** of membrane potential against threshold: `S(U[n]) ≡ Θ(U[n] − ϑ)`.

That function's derivative is **zero everywhere except at threshold, where it is undefined.** Both the BPTT expression and the forward/RTRL expression carry the activation derivative `σ′` as a *multiplicative* factor. So the derivative doesn't merely degrade the gradient — it **annihilates** it. Gradient descent cannot pass through a spiking unit at all.

This is why SNN training is a distinct field rather than a variation on standard practice, and why it is not simply "backprop but spiky."

## The surrogate gradient

A continuous relaxation **used only in the backward pass.** The forward pass is untouched — the network still computes and propagates real binary spikes through the true Heaviside nonlinearity — but every occurrence of the degenerate `Θ′` in the gradient computation is replaced by the derivative of a smooth surrogate.

The distinction from "smoothed" SNNs is the crux and the paper is explicit about it: **smoothed models change the model; surrogate gradients change only the gradient computation.** The discrete, event-driven, binary-spike forward semantics survive intact — which is precisely what makes the resulting network deployable on event-driven hardware.

That is why the paper treats it as principled rather than a hack: it is a local numerical patch applied exactly where the true gradient is degenerate. Its justification is that along a weight-interpolation path the true loss has flat zero-gradient plateaus, while the surrogate stays non-zero and continuous — the gradient of a "virtual" surrogate loss that is never explicitly computed.

**Commonly used surrogate derivatives:** piecewise linear (Bellec et al.; Esser et al.; Bohte) · derivative of a fast sigmoid (Zenke & Ganguli, underlying **SuperSpike**) · exponential (Shrestha & Orchard, **SLAYER**).

**Does the choice matter?** The paper says a systematic comparison "is still pending," but infers from the breadth of successful published results that "the success of the method is not crucially dependent on the details of the surrogate." ⚠️ That is **claimed, not evidenced** — no controlled ablation is presented. It is an inference from diversity of prior work, and it remains, as far as this wiki knows, untested.

## The taxonomy

The paper's four-way split of approaches to the non-differentiability problem:

**1. Biologically inspired local learning rules** — mentioned, deferred to other reviews.

**2. ANN-to-SNN conversion** — mentioned, deferred. See [[ann2snn-differential-coding]] for where this line has since gone.

**3. Smoothing the network** — covered in depth, four sub-variants, each with a trade-off that matters to this wiki:

| Variant | Mechanism | Trade-off |
|---|---|---|
| Soft nonlinearity | Replace spike generator with continuous gating | **Compromises the binary spike property that defines an SNN** |
| Probabilistic | Stochastic spiking smooths the log-likelihood | Gradients defined only in expectation; needs trial-averaging over injected noise |
| Rate coding | Gradients through the f-I curve | Precise rate estimation needs **high firing rates or long windows** — in direct tension with the sparsity that motivates spiking |
| Single-spike timing | Gradients on continuous spike-time variables | SpikeProp requires **every hidden unit to fire exactly once** — firing time is undefined for silent units, conflicting with sparse operation |

*(synthesis)* Two of those four trade-offs are the same trade-off: **the training method demands activity that the efficiency argument demands you avoid.** Rate coding needs high firing rates; single-spike timing forbids silence. Both push against the low-spike-rate regime that [[snn-energy-breakeven-conditions]] identifies as the *only* place SNNs win on energy. That tension is structural, and it's a good reason surrogate gradients became dominant — they impose no activity requirement.

**4. Surrogate gradients**, split in two:

- **Surrogate derivative + standard BPTT** — a drop-in replacement inside ordinary autodiff (SuperSpike, SLAYER, piecewise-linear recurrent SNNs on par with LSTMs on some tasks). Retains full BPTT costs.
- **Surrogate gradients that also relax locality** — feedback alignment (random fixed backward weights), direct feedback alignment (output errors projected straight to each hidden layer), local errors (per-layer auxiliary loss via random projection), and **three-factor rules** such as SuperSpike, which uses synaptic eligibility traces for temporal credit assignment online and forward-in-time, sidestepping BPTT and weight transport entirely. Its scaled successor **DCLL** (Deep Continuous Local Learning) reduces space complexity to **O(N)** and — per a claim carried from the DCLL paper, not independently verified — outperforms BPTT-trained SLAYER on DVS-Gestures with fewer iterations.

## What training costs, and why it decides the on-chip question

| Method | Cost | Hardware fit |
|---|---|---|
| **BPTT** | **O(NT) memory per layer** — must hold every timestep's activations until the backward pass. Requires **non-local** backward gradient communication across the whole network | Poor. Weight transport and global communication are exactly what neuromorphic hardware lacks |
| **Forward-in-time (RTRL-style)** | Naively **O(N³)** per layer | Only viable after aggressive approximation |
| SuperSpike | O(N²) | Better |
| **DCLL** | **O(N)** | Online, forward-in-time, local quantities only |

The paper formalises "local" precisely: variables directly available to a given neuron — its own weight, spike train, membrane potential. Anything requiring another neuron's delayed spike train or membrane potential is **non-local** and needs explicit transport and memory infrastructure.

*(synthesis)* This is the piece the wiki was missing, and it reframes the on-chip-learning dispute. [[../devices/memristor-array-integration-gap]] records a **yield-economics** argument for on-chip learning — in-situ training is how you ship an imperfect array. [[../conflicts/analog-onchip-training-viability]] questions how robust that is. What this paper adds is that on-chip learning is not merely desirable but **architecturally constrained**: BPTT's O(NT) memory and non-local gradient transport are not implementable on a substrate whose defining feature is local, event-driven, memory-beside-compute operation. If you want learning on the chip, you are restricted to the three-factor/local family — SuperSpike, DCLL and successors — essentially by construction.

And note the alignment the paper highlights: biological plausibility and hardware implementability point the **same way** here. Locality serves both. They are not competing goals, which is a genuinely useful observation and not the usual framing.

**The training-energy gap.** BPTT over T timesteps costs memory and compute scaling with T — the same T that dominates inference energy in [[snn-energy-hardware-realistic]]. The wiki has no source quantifying SNN *training* energy against ANN training energy. Given that surrogate-gradient BPTT is strictly more expensive than standard BPTT on an equivalent ANN, and that SNN inference wins are already narrow, this is a conspicuous hole in the field's efficiency case.

## Maturity

**2019 tutorial/review.** No quantitative benchmarks of its own — no accuracy figures, no energy numbers. It is a conceptual map, and this page treats it as one. The field has moved substantially since; the taxonomy has aged better than any specific result in it.

## Open questions

- Has a systematic surrogate-function comparison been published since 2019? The paper's "doesn't much matter" claim is still uncontrolled.
- **What does SNN training cost in energy versus ANN training?** No source in this wiki answers this.
- Do DCLL-family local rules hold up beyond DVS-Gestures scale?
- Which local rules are actually implemented in hardware on [[../players/intel-loihi2]], which advertises three-factor learning support but does not enumerate what is hardware-native versus microcode-expressible?

## Source

- `raw/research/neuromorphic-seed-sweep/14-surrogate-gradient-learning.md` — Neftci, Mostafa & Zenke, "Surrogate Gradient Learning in Spiking Neural Networks", arXiv:1901.09948, 2019. ⚠️ pymupdf capture — figures unavailable, 2 broken refs; the surrogate-function shapes (Fig. 3) and the loss-landscape justification (Fig. 4) are reconstructed from caption and body text.

## Related

- [[snn-energy-breakeven-conditions]] — the low-spike-rate regime that several training methods fight against
- [[snn-energy-hardware-realistic]] — T as the dominant energy knob, at inference
- [[ann2snn-differential-coding]] — the conversion branch of the taxonomy, developed
- [[../conflicts/analog-onchip-training-viability]] — whether on-chip training works on real devices
- [[../players/intel-loihi2]] — three-factor learning in silicon
