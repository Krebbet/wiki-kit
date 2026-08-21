# IBM NorthPole

The strongest available evidence in this wiki's analog-vs-digital dispute — and arguably in a broader one about whether spiking is necessary at all. IBM built TrueNorth, a genuinely spiking neuromorphic chip. Then it built NorthPole, which keeps the brain-inspired *architectural* idea — compute co-located with memory, no off-chip DRAM — and **discards both the analog physics and the spikes**. It is a fully digital, non-spiking, low-precision inference engine that markets itself on neuroscience metaphors.

A detail worth noting: the community reference page describing it never actually calls NorthPole "neuromorphic." It uses "neural inference architecture" and "spatial computing architecture" with soft brain-inspired language. Whether NorthPole belongs in this wiki at all is a live question — and the fact that it's hard to answer *is* the finding.

## Architecture

| Attribute | Value |
|---|---|
| Type | Fully digital, non-spiking CMOS. No analog compute, no memristive element, no spike-based signalling |
| Cores | 256 programmable cores, each with local memory and compute units |
| On-chip SRAM | **224 MB** total, distributed across cores |
| Off-chip DRAM | **None.** "Once configured, NorthPole operates self-sufficiently without needing to access external DRAM" |
| Networks-on-chip | Four separate NoCs — activations, inter-core, weight loading, instructions |
| Node | 12 nm (fab not named in captured sources) |

**The design thesis in one line:** the model must fit entirely in 224 MB of on-chip SRAM, and in exchange you never pay to move weights from DRAM. That is the same insight the rest of this wiki keeps arriving at from the other direction — [[../devices/memristor-array-integration-gap]] finds conversion overhead dominating analog systems, [[intel-loihi2]] finds a 6.9× penalty from inter-chip static power and communication, and the SNN energy literature finds per-timestep memory traffic dominating. NorthPole's answer is to make the data movement structurally impossible rather than merely cheap.

**Not stated anywhere captured:** transistor count, clock frequency. Without the latter, a chip-level TOPS figure cannot be derived from the public architecture description.

## Measured results

**LLM inference** (IEEE HPEC 2024, IBM Research blog reporting the team's own paper). A **3-billion-parameter** model derived from IBM's Granite-8B-Code-Base, quantized to **4-bit weights and activations**, on a **16-card NorthPole setup** in an off-the-shelf 2U server, cards linked by PCIe:

| Metric | Value | Boundary |
|---|---|---|
| Latency | **<1 ms/token** | Not explicit — likely system-level generation latency |
| Throughput | **28,356 tokens/s** | 16-card system, not per chip |
| "46.9× faster" | vs *"the next most energy-efficient GPU"* | ⚠️ baseline unnamed |
| "72.7× more energy efficient" | vs *"the next lowest latency GPU"* | ⚠️ baseline unnamed |

**Earlier edge result** (published in *Science*, cited for context, not re-measured here): **25× more energy efficient** than "commonly available 12 nm GPUs and 14 nm CPUs," measured as frames interpreted per unit power, on ResNet-50 and YOLOv4.

### The baselines are unnamed, and that is disqualifying

Every headline multiplier — 46.9×, 72.7×, 25× — is stated against a GPU that is **never named**. No model, no generation, no node, no precision. There is no disclosure of whether the GPU baseline ran the same 4-bit-quantized model or full precision, and no batch size or sequence length for either side. Nor is any absolute figure given: no watts, no joules per token, no tokens per joule — only the ratio.

Nor is the accuracy cost stated. The model was quantized to 4 bits and "fine-tuned to match accuracy," with **no accuracy-delta figure** — no perplexity, no benchmark score, no loss number.

*(synthesis)* This is a textbook instance of the pattern [[../conflicts/snn-energy-payoff]] exists to track, and it is worth noting that it appears here in work that is otherwise serious — a *Science* paper, an IEEE HPEC paper, a real chip. The underlying HPEC paper very likely contains the missing detail; the vendor blog reporting it does not. The wiki records the multipliers as **claimed with an owner and a date**, not as facts, and the earlier 25× figure ranks slightly higher only because it at least names process nodes for the comparison parts.

## Maturity

**Research prototype**, in IBM's own framing — "brain-inspired NorthPole research prototype chip." No product name, no SKU, no stated commercial availability in any captured source. 12 nm, fab unnamed.

The 16-card server demonstration is nonetheless a meaningful rung: it is a working multi-chip system running a 3B-parameter model, not a single-die benchmark.

## Why NorthPole matters to this wiki

*(synthesis)* Three reasons, in increasing order of importance:

1. **It is a serious digital-neuromorphic datapoint** with real silicon and a *Science* publication, from a group with a decade of neuromorphic history.
2. **It reframes the analog-vs-digital dispute.** The wiki's analog pages document conversion overhead and device variability eating the theoretical win. NorthPole sidesteps both by staying digital and low-precision, and keeps only the architectural insight — memory next to compute. If that captures most of the available benefit, the case for analog crossbars narrows considerably.
3. **It is evidence against spiking being necessary.** IBM's own trajectory runs TrueNorth (spiking) → NorthPole (not spiking), and the not-spiking chip is the one running 3B-parameter LLMs. Combined with [[intel-loihi2]]'s best LLM result also coming from a **non-spiking** attention-free architecture, and [[../snn/snn-energy-breakeven-conditions]]'s finding that spiking transformers lose outright, a pattern is forming: **the neuromorphic ideas that are working at scale are the architectural ones — locality, sparsity, low precision, memory beside compute — not the neuroscience-literal one of communicating in spikes.**

That is a synthesis across sources, not a claim any of them makes, and it is falsifiable: a spiking system beating a non-spiking one at matched accuracy on a real workload would undercut it. [[../benchmarks/neurobench]]'s system track is where that would show up.

**Do not file NorthPole under SNN evidence.** It is not a spiking network and its numbers must never be merged into SNN energy comparisons — a mistake that would be easy to make given it sits under the neuromorphic banner.

## Gaps in the current sources

The community reference page turned out notably thin: **no efficiency, energy or throughput figures at all**, no transistor count, no clock frequency, no primary-source citation (its "Related Publications" table has a bare "October 2023" row with no title, authors or venue — presumably the *Science* paper). Its provenance for every spec is therefore unconfirmed. It also **never mentions TrueNorth**, so the trajectory argument above is assembled by this wiki, not inherited from the source.

The *Science* paper itself — "Neural inference at the frontier of energy, space, and time", doi:10.1126/science.adh1174 — **could not be captured**: science.org hangs rather than refusing, exit 124 at 90 s on three separate attempts. It is on the [[../watchlist]].

## Open questions

- The unnamed GPU baselines. The IEEE HPEC paper (linked from modha.org) probably names them — worth a targeted capture attempt.
- What accuracy was lost to 4-bit quantization?
- Absolute power figures — watts, joules per token — at a stated boundary.
- Is NorthPole productised, or does it stay a research vehicle?
- How does the 224 MB on-chip-only constraint scale? A 3B model at 4-bit fits 16 cards; what happens at 70B?

## Source

- `raw/research/neuromorphic-seed-sweep/01-northpole-llm-results.md` — IBM Research blog, NorthPole LLM inference results, reporting the team's own IEEE HPEC 2024 paper. Vendor primary; tier 3.
- `raw/research/neuromorphic-seed-sweep/02-on-northpole.md` — Open Neuromorphic community reference page. Secondary, thin, no quantitative content, provenance unconfirmed.

## Related

- [[roster]] · [[intel-loihi2]] — the other incumbent, which kept spiking
- [[../conflicts/snn-energy-payoff]] — the unnamed-baseline multipliers as Position A
- [[../devices/memristor-array-integration-gap]] — the analog approach NorthPole declines to take
- [[../snn/snn-energy-breakeven-conditions]] — where spiking transformers lose
- [[../viability-ledger]]
