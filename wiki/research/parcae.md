# Parcae: Scaling Laws For Stable Looped Language Models

**Authors:** Hayden Prairie, Zachary Novack, Taylor Berg-Kirkpatrick, Daniel Y. Fu (UC San Diego / Together AI).

**Venue:** arXiv 2604.12946, April 2026.

Parcae is a middle-looped transformer that stabilises recurrence by recasting the loop as a discrete LTI dynamical system and constraining the spectral norm of the state-transition matrix $\mathbf{A}$ via a negative-diagonal parameterisation discretised with ZOH. This eliminates the residual explosion that plagues prior looped models (RDMs, Universal Transformers), enabling clean scaling-law characterisation of loop depth as an orthogonal compute axis. Pretrained checkpoints at 140M–1.3B parameters are publicly available.

## Architecture and stability mechanism

**LTI framing.** The forward pass of any middle-looped model can be exactly written as:

$$h_{t+1} = \mathbf{A}h_t + \mathbf{B}e + R(h_t, e), \quad p = C(h_T)$$

where $e = P(s)$ is the prelude embedding, $R$ is the nonlinear transformer block, and $\mathbf{A}, \mathbf{B}$ govern linear injection. Linearising (dropping $R$) yields a discrete LTI system whose stability is determined by the spectral radius $\rho(\mathbf{A})$: stability requires $\rho(\mathbf{A}) < 1$.

**Prior work instability.** Addition injection ($h_{t+1} = R(h_t + e)$) implicitly sets $\mathbf{A} = I$ → $\rho = 1$ (marginal). Concatenation injection (RDM / Huginn-style: $h_{t+1} = R(W[h_t; e])$) leaves $\mathbf{A}$ unconstrained → $\rho(\mathbf{A})$ drifts above 1 during training, producing residual explosion and loss spikes. Geiping et al. (RDM / Huginn) patched this with combined Pre+Post-Norm ("residual normalisation"), which is sensitive to learning rate and does not prevent spikes late in training.

**Parcae's fix.** $\mathbf{A}$ is parameterised as a negative diagonal matrix:

$$\mathbf{A} = \mathrm{Diag}(-\exp(\log\tilde{A})), \quad \tilde{A} \in \mathbb{R}^{d_h}$$

and discretised with zero-order hold (ZOH): $\mathbf{A} = \exp(\Delta \mathbf{A})$, $\mathbf{B} = \Delta\mathbf{B}$ (Euler), with a learned step size $\Delta \in \mathbb{R}^{d_h}$. Enforcing negative eigenvalues in the continuous representation guarantees $\rho(\mathbf{A}) < 1$ after discretisation, by construction. The input $e$ to $\mathbf{B}$ is layer-normalised (prelude norm) to suppress late-training loss spikes from $\mathbf{B}$ growth.

**Architecture shape.** Parcae follows the prelude / core (recurrent) / coda split. Middle-third layers loop; outer thirds do not. Parameterisation otherwise matches a `nanochat`-style transformer exactly — same attention, MLP, no added Post-Norm. Recurrence depth $T$ is sampled per-sequence within a micro-batch from a Poisson($\mu_{rec}$) distribution (per-sequence sampling, not per-batch), with truncated BPTT at $\mu_{bwd} = \lceil \mu_{rec}/2 \rceil$.

**Vs. Huginn (RDM).** Huginn relies on residual normalisation (Pre+Post-Norm stack) to achieve stable convergence and requires careful LR tuning. Parcae removes that norm entirely; stability comes from the $\mathbf{A}$ constraint. Parcae converges across all tested LRs (2e-4 to 1e-3); Huginn-style RDMs diverge above 4e-4. Against data- and parameter-matched RDMs, Parcae achieves 6.2–6.3% lower validation perplexity.

## Scaling properties

**Training FLOPs.** Under fixed parameters and FLOPs, isoFLOP curves show a clear interior optimum in $\mu_{rec}$: increasing loop depth while proportionally reducing tokens beats training at $\mu_{rec}=1$. Optimal $\mu_{rec}$ and optimal token count both follow power laws in FLOPs with consistent exponents across 140M and 370M scales:

$$\mu_{rec}^* \propto C^{\gamma_\mu}, \quad \gamma_\mu \approx 0.40$$
$$D^* \propto C^{\gamma_D}, \quad \gamma_D \approx 0.78$$

Looping and data should scale in tandem. At 140M, the looping-optimal frontier beats a fixed-depth (non-looped) Parcae by 1.2–2.0 Core points across FLOP budgets.

**Test-time scaling.** Evaluating at $T > \mu_{rec}$ yields predictable gains that saturate near $T = \mu_{rec}$. Decay follows:

$$L(T) = L_\infty + Z\,e^{-z \cdot T}$$

Unified law (training + test-time):

$$\hat{L}(T \mid \mu_{rec}, D) = \underbrace{E + X \cdot N(\mu_{rec})^{-x} + Y \cdot D^{-y}}_{\text{training floor}} + Z\,\exp\!\left(-z \cdot T \cdot \mu_{rec}^{-1}\right)$$

Held-out prediction error: 0.85–1.31% average, dropping to 0.1–0.17% when the empirical $T=\mu_{rec}$ loss anchors the fit.

**Vs. fixed-depth transformer (Table 5).** At 1.3B / 100B tokens with $T=8$: Parcae outperforms a parameter-matched Transformer by 2.99 Core points and 1.18 Core-Extended points. The 770M Parcae matches the 1.3B Transformer on Core (roughly 2× parameter efficiency). Overall relative quality: 23.3–87.5% of the gap to the next larger Transformer.

## Released checkpoints

All four checkpoints on HuggingFace under `SandyResearch/` are base models trained on FineWeb-Edu, no instruction tuning.

| HF repo | Parameters | Prelude layers | Core (looped) layers | Coda layers | Model dim | Default $\mu_{rec}$ |
|---|---|---|---|---|---|---|
| `SandyResearch/parcae-140m` | 140M | 2 | 2 | 2 | 768 | 8 |
| `SandyResearch/parcae-370m` | 370M | 4 | 4 | 4 | 1024 | 8 |
| `SandyResearch/parcae-770m` | 770M | 6 | 6 | 6 | 1280 | 8 |
| `SandyResearch/parcae-1.3b` | 1.3B | 8 | 8 | 8 | 1536 | 8 |

Usage: `pip install parcae-lm`, then `parcae_lm.from_pretrained("SandyResearch/parcae-140m")`. Config mutation is supported pre-build (e.g., set `config.mean_recurrence = 16`).

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (isolated block training / swappable blocks) | **High — base model for Exp 1** | Parcae-140M or -370M is the primary candidate fallback base for Exp 1 if Huginn-3.5B exceeds GPU budget. Frozen-weight Exp 1 uses Parcae as a read-only host; the spectral-norm constraint is not exercised (weights don't change). The prelude/core/coda split gives a natural boundary for block-level isolation experiments. |
| **G2** (per-block dynamic parameter allocation) | **Medium** | Parcae's scaling laws show $\mu_{rec}$ is an orthogonal compute axis; this supports reasoning about per-block allocation. However, Parcae allocates compute via loop depth, not per-block parameter count — the mechanism is not directly transferable. Relevant if Exp 2 involves joint fine-tuning: the spectral-norm stability constraint becomes load-bearing when unfreezing Parcae weights. |
| **G3** (token-conditional routing) | **Low — indirect** | Parcae is depth-uniform (all tokens loop the same number of times); there is no token-conditional routing. The stochastic-depth training objective (variable $T$ per sequence) is adjacent to per-token adaptive compute but operates at sequence granularity. Test-time scaling results bound the ceiling for what depth-routing could achieve from a Parcae base. |

## Credibility

- arXiv 2604.12946, submitted 14 April 2026. UC San Diego / Together AI. No peer-review record at ingest.
- Four HuggingFace checkpoints publicly released (`parcae-140m` through `parcae-1.3b`), weights auto-download.
- Full training code on GitHub (`SandyResearch/parcae`), Docker image at `ghcr.io/sandyresearch/parcae`, sweep scripts for replicating all scaling law experiments.
- Instability diagnosis (Table 1, Figure 3) is mechanistic and falsifiable: spectral radius trajectory logged during training directly confirms the LTI prediction.
- Scaling law exponents consistent across 140M and 370M; held-out extrapolation error < 1.3%. Parametric form borrowed from Chinchilla methodology.

## Empirical claims

- Parcae (T=8) vs. RDM (T=8), 350M param / matched data: 9.1% lower WikiText PPL, +1.8 avg downstream benchmark points (Table 3).
- Parcae (T=8) vs. Transformer, 1.3B / 100B tokens: +2.99 Core, +1.18 Core-Extended (Table 5).
- 770M Parcae ≈ 1.3B Transformer on Core; parameter efficiency gain 23.3–87.5% depending on scale and benchmark.
- Training scaling law exponents $\gamma_\mu \approx 0.40$, $\gamma_D \approx 0.78$, consistent at 140M and 370M.
- Test-time law average Huber loss: $2.5 \times 10^{-7}$ (140M), $1.8 \times 10^{-7}$ (370M).
- Looping-optimal frontier beats fixed-depth ($\mu_{rec}=1$) by 1.2–2.0 Core points at extended FLOP budgets (Table 6).
- Parcae converges at all LRs 2e-4 to 1e-3; baseline RDM diverges above 4e-4 (Table 2).

## Open questions / failure modes

1. **Scaling observations are limited to ≤1.3B parameters / ≤100B tokens.** The paper explicitly flags that whether these scaling laws hold at larger budgets is unknown.
2. **Three-way trade-off (parameters × data × looping) not fully characterised.** Current laws fix parameters and co-optimise data and looping. Joint optimisation of all three axes is future work.
3. **Test-time scaling saturates near $T = \mu_{rec}$.** Gains are bounded; models do not benefit from arbitrarily more inference loops. This is a ceiling for adaptive compute schemes built on Parcae.
4. **Spectral-norm constraint is moot for frozen-weight use (Exp 1)** — relevant only when weights are updated (Exp 2+). For Exp 1 the choice between Parcae and Huginn reduces to size / VRAM fit and tokenizer compatibility.
5. **Tokenizer mismatch.** Parcae uses a GPT-4-style BPE (32k vocab, trained on FineWeb-Edu); Huginn uses a different tokenizer. Experiments requiring a single shared tokenizer must pick one and accept the mismatch.
6. **Per-sequence depth sampling adds micro-batch complexity.** Each sequence in a batch can have a different $T$; this complicates batched inference benchmarking and any downstream evaluation that assumes uniform depth.

## Source

- `raw/research/loop-computation/06-parcae-abs.md`
- `raw/research/loop-computation/08-parcae-github.md`
- `raw/research/loop-computation/14-parcae-pdf.md`

## Related

- [[huginn]] — RDM / Huginn is the primary prior looped model; Parcae's instability analysis is a direct critique of Huginn's residual-normalisation approach. Huginn-3.5B is the Exp 1 first-choice base; Parcae-140M/370M is the fallback.
- [[universal-transformers]] — original middle-looped architecture (Dehghani et al., 2019); Parcae's LTI analysis also applies to Universal Transformer's addition-injection ($\rho(\mathbf{A})=1$, marginal stability).
