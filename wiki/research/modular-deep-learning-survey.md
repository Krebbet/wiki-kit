# Modular Deep Learning (Survey)

This is a survey paper (Pfeiffer, Ruder, Vulić, Ponti; Google DeepMind / Cambridge / Edinburgh) that unifies modular neural architectures under a four-axis taxonomy — computation function, routing function, aggregation function, training setting — and argues that explicit modularity addresses three failure modes of monolithic fine-tuning: negative interference between tasks, catastrophic forgetting, and failure of systematic generalisation. Its value here is as a taxonomy anchor and a catalogue of routing failure modes, not as a source of original empirical claims.

## Four-axis taxonomy

The survey organises the design space along four orthogonal axes:

1. **Computation function** — what a module computes. Instantiations include sparse subnetworks, low-rank adapters (LoRA), sequential/parallel bottleneck adapter layers, prefix/prompt vectors, 1×1 convolutional adapters, and fully independent MLPs/RNNs/CNNs. All compose with a frozen backbone via three modes:
   - *Parameter composition* — element-wise addition of sparse or low-rank delta to existing weights. Best inference efficiency.
   - *Input composition* — prefix/prompt vectors prepended to layer inputs. Most parameter-efficient but worst inference cost.
   - *Function composition* — new sub-function stacked before, after, or in parallel with an existing layer. Best task performance.
   All three reduce to `f'(x) = f_θ(x) + f_ϕ(x)`, differing only in how ϕ is realised.

2. **Routing function** — how inputs are dispatched to modules (see dedicated section below).

3. **Aggregation function** — how module outputs are combined. Ranges from hard selection (use one module's output only) to soft weighted mixture (full MoE) to hypernetwork-generated interpolation.

4. **Training setting** — joint multi-task, sequential/continual, or few-shot/zero-shot. Affects whether routing collapse and catastrophic forgetting are live concerns.

## Routing mechanisms

### Fixed routing
Dispatch signal is metadata known a priori: task identity, language, domain, modality. Hard, deterministic, hand-designed. Specialization is guaranteed by construction; no collapse is possible. Representative systems: MAD-X, bilingual MT adapters, domain adapters. **Mittal et al. (2022) and Muqeeth et al. (2022) show fixed routing generally outperforms learned routing** — the primary empirical pillar for the learned-routing-underspecializes position.

### Learned routing
Dispatch signal is the input representation x or a task embedding t, passed through a linear projection or MLP. Two sub-families:

- **Hard learned routing** — top-1, top-k, or variable-size selection via Gumbel-Softmax, Concrete distribution, RL-REINFORCE, or evolutionary search. Discrete, non-differentiable by default.
- **Soft learned routing** — continuous weighted mixture over all modules (standard MoE). Differentiable but computationally prohibitive at scale; reduces parameter locality.

**Documented failure modes of learned routing:**
- *Training instability* — at init, modules are random; the router cannot make principled decisions, and modules won't specialise until routed consistently.
- *Module collapse* — router over-exploits a small subset, leaving others untrained. Requires load-balancing auxiliary losses, epsilon-greedy exploration, or mutual-information losses to mitigate.
- *Out-of-domain degradation* — token-level routing leads to out-of-domain performance drops (Artetxe et al., 2022); pre-training MoE gains do not always transfer to fine-tuning (Fedus et al., 2021).

**Routing granularity:** global (same config all layers), per-layer (independent per layer), or hierarchical (sub-routers, dispatched routing of Rosenbaum et al.). Token-level vs. example-level vs. task-level routing are distinguished explicitly for MoE transformers.

### Hypernetworks
A small network generates module parameters conditioned on a task/language embedding. Formally equivalent to unnormalised routing scores over a module bank. Routing and computation are intertwined — violating strict modularity — but enables systematic generalisation by interpolating in embedding space.

## Why monolithic fine-tuning fails

Three failure modes motivate the survey's thesis:

1. **Negative interference** — gradient updates for one task degrade performance on others when parameters are shared without modularity.
2. **Catastrophic forgetting** — sequential task learning overwrites earlier task representations in shared weights.
3. **Systematic generalisation failure** — vanilla transformers (Csordás et al., 2021) develop emergent sub-networks that are *not* consistently reused across similar sub-tasks and cannot be composably combined; performance on simple vs. composite tasks is largely uncorrelated (Li et al., 2022a).

Prompt/input composition methods further underperform at small model scales (Mahabadi et al., 2021a; Liu et al., 2022c), suggesting modularity benefits are not uniform across regimes.

## Contrarian evidence: learned routing underspecializes

This is the survey's main feed into the [[learned-routing-specialization]] conflict:

- **Mittal et al. (2022)** — on synthetic data, learned routing under-utilizes modules and achieves *less* specialization as task count grows. Fixed routing is generally superior.
- **Muqeeth et al. (2022)** — in real-world multi-task settings, fixed routing again generally outperforms learned routing.
- **Lewis et al. (2021)** — MoE models route syntactically/semantically similar *tokens* (not sentences or tasks) to the same experts, limiting expressiveness and true specialization.
- Counterpoint within the survey: Ponti et al. (2022) find learned routing can surpass expert selection in procedurally constructed environments — the failure is not universal but is the dominant empirical pattern.

## Iteration, recurrence, and looping structure

Not the survey's primary focus, but touched in two contexts:

- *Programme simulation* — Routing Networks (Rosenbaum 2018), Modular Networks (Kirsch 2018), CRL (Chang 2019) construct FSA-like computation graphs dynamically with a memoryless routing function selecting transition functions until a halt action; variable-length computation depth.
- *Recurrent Independent Mechanisms* (Goyal et al., 2021) — independent recurrent modules with separate parameters, top-k activated per step, inter-module communication via attention, applied over sequence steps. The same module inventory is reused at each timestep. Validated on sequential/RL tasks; no large-scale LLM validation.

The survey does not evaluate weight-tied looped transformer architectures (e.g., Universal Transformers) or address whether iteration beats depth-scaled non-iterative baselines.

## Scale anchoring

The survey is a literature synthesis; empirical claims are anchored to cited works:

- PEFT (LoRA, adapters): primarily GLUE/SuperGLUE on BERT-scale (~100M–350M) encoders.
- MoE (Switch Transformer / GShard): 100B–1.6T parameters, trillion-token pre-training.
- LoRA: validated on GPT-3 (175B) and RoBERTa (125M, 355M); <0.5% parameters updated.
- Cross-lingual adapters (MAD-X): mBERT/XLM-R (~270M) across dozens of languages on NER, NLI, dependency parsing.
- Routing specialization studies: mostly <1B parameters on multi-task NLP or RL benchmarks.

## Open questions

From §9.1 (authors' explicit flags):

1. **Combining computation function types** — combining parameter, input, and function composition within a module (e.g., sparsity constraints on adapters).
2. **Learned module structure** — all current modules share the same architecture; per-module architecture search is unexplored.
3. **Standardising modularity evaluation** — no unified benchmark measures specialization, compositionality, and efficiency jointly.
4. **Nature of modular representations** — how computation function choice affects internal representations is unknown.
5. **Hierarchical modularity** — no differentiation of high-level vs. low-level skill nesting.
6. **Learned routing for heterogeneous pre-training** — fixed routing requires metadata (language, task) not always available; learned routing for heterogeneous pre-training is unsolved.
7. **Modular instruction tuning** — combining instruction tuning with modular skill acquisition.
8. **Benchmarking routing quality** — existing benchmarks measure task performance, not routing quality or specialization degree.
9. **Structured/sparse aggregation** — targeting salient subnetworks rather than averaging all parameters.
10. **Learned aggregation** — non-linear learned aggregation may outperform arithmetic interpolation.
11. **Merging modular models** — training modules designed for post-hoc merging.
12. **Extensible multi-task models** — modular pre-training enabling cheap extension to new tasks/modalities.

## Source
- `raw/research/thesis-foundations/09-modular-deep-learning-survey.md` — *Modular Deep Learning*, Jonas Pfeiffer, Sebastian Ruder, Ivan Vulić, Edoardo M. Ponti; Google DeepMind / University of Cambridge / University of Edinburgh; TMLR 2023 (survey track).

## Related
- [[expert-choice-routing]] — EC is a primary instantiation of the survey's "load balance structural, not incentivized" design point.
- [[mixture-of-depths]] — concrete instance of the survey's hard routing / conditional-compute family.
- [[mamba-2-and-ssm-hybrids]] — SSM+attention hybrid at fixed ratios is a concrete instance of survey's "fixed routing" category.
- [[mixture-of-cognitive-reasoners-micro]] — MICRO's MOB, top-1 router, 3-stage curriculum all instance the survey's taxonomy.
- [[block-operations-and-modular-routing]] — SMFR Multiplexer is an instance of the survey's soft-routing category.
- [[routing-mechanisms-in-modular-networks]] — this page is a primary anchor for the routing aux page.
- [[learned-routing-specialization]] (open conflict) — this survey provides the main contrarian evidence (Mittal, Muqeeth, Lewis).
