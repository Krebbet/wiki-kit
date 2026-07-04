# CEBE: Zero-Shot Context Generalization in RL from Few Training Contexts

Context-Enhanced Bellman Equation (CEBE) is a framework for training a policy on one (or very few) contexts of a Contextual MDP and provably generalizing zero-shot to nearby unseen contexts. By augmenting the Bellman operator with first-order Taylor expansions of the transition kernel and reward function around the training context, CEBE approximates the true multi-context Q-function with $O(\|c - c_0\|^2)$ error — without collecting additional environment samples. The practical instantiation, Context Sample Enhancement (CSE), is a data-augmentation procedure compatible with any off-policy RL algorithm: each real transition is synthetically perturbed to a nearby context using only Jacobian information accessible during training. Experiments on SimpleDirection, PendulumGoal, CheetahVelocity, and AntDirection show CSE matches or exceeds Local Domain Randomization (LDR) — a baseline with oracle access to perturbed dynamics — while requiring only a single training context.

## Source

**Paper:** Zero-Shot Context Generalization in Reinforcement Learning from Few Training Contexts
**arXiv:** 2507.07348
**Venue:** NeurIPS 2025

## CMDP Formalism

A **Contextual MDP** is $\mathcal{M} = (\mathcal{C}, \mathcal{S}, \mathcal{A}, \mathcal{M}', \gamma)$ where $\mathcal{C}$ is an open convex subset of a Banach space and $\mathcal{M}'(c) = (\mathcal{S}, \mathcal{A}, \mathcal{T}^c, R^c, \gamma)$ is the per-context MDP. The goal is to train exclusively on context $c_0 \in \mathcal{C}$ and generalize to arbitrary test contexts $c \in \mathcal{C}$.

**Regularity assumptions:**
- $R^c \in \text{Lip}(\mathcal{S} \times \mathcal{A} \times \mathcal{S})$ with $\partial_c R^c$ existing and Lipschitz in $c$
- Transition kernels $\mathcal{T}^c$ have Lipschitz partial derivatives $\partial_c \mathcal{T}^c$
- During training, the agent observes $\partial_c R^{c_0}$ and $\partial_c \mathcal{T}^{c_0}$ alongside standard transition tuples (requires a differentiable simulator)

## CEBE Definition

The Context-Enhanced Bellman Equation replaces the true per-context dynamics with first-order Taylor approximations centered at $c_0$:

$$Q_{CE}(s,a,c) = \mathbb{E}_{s' \sim \mathcal{T}_{CE}^c(s,a)}\!\left[R_{CE}^c + \gamma\,\mathbb{E}_{a' \sim \pi(s',c)} Q_{CE}(s',a',c)\right]$$

**Deterministic transitions** $f^c(s,a)$: the context-enhanced components are

$$\mathcal{T}_{CE}^c(s,a) = \delta_{f^{c_0}(s,a) + \partial_c f^{c_0}(s,a)(c - c_0)}$$

$$R_{CE}^c = R^{c_0} + \partial_c R^{c_0} \cdot (c - c_0) + \partial_{s'} R^{c_0} \cdot \partial_c \mathcal{T}^{c_0} \cdot (c - c_0)$$

The second correction term in $R_{CE}^c$ accounts for the fact that reward depends on the next state $s' = f^c(s,a)$: a context-induced shift in the transition propagates into the reward estimate.

**Stochastic transitions** (finite state space): the context-enhanced distribution is constructed via projection onto the probability simplex:

$$\mathcal{T}_{CE}^c(s,a) = P\!\left[\mathcal{T}^{c_0}(s,a) + \partial_c \mathcal{T}^{c_0}(s,a)(c - c_0)\right]$$

where $P$ is the $\ell_2$ projection ensuring the result is a valid probability distribution.

## Theorems

**Theorem 1 — Q-function stability.** For two MDPs with $\|R^{(1)} - R^{(2)}\|_\infty \leq \delta_R$ and $\sup_{(s,a)} W_p(\mathcal{T}^{(1)}(s,a), \mathcal{T}^{(2)}(s,a)) \leq \delta_T$, under Lipschitz policy $\pi$ (constant $L_\pi$) and discount satisfying $\gamma < 1/(\max(L_{\mathcal{T}^{(1)}}, L_{\mathcal{T}^{(2)}})(1+L_\pi))$:

$$\|Q^{(1)} - Q^{(2)}\|_\infty \leq \frac{1}{1-\gamma}\!\left(\delta_R + \frac{\gamma(1+L_\pi)\delta_T \|R^{(2)}\|_\text{Lip}}{1 - \gamma\max(1, L_{\mathcal{T}^{(2)}}(1+L_\pi))}\right)$$

Establishes that nearby dynamics produce nearby Q-functions — the prerequisite for CEBE approximations to be useful.

**Theorem 2 — Deterministic CEBE accuracy.** Under the smoothness assumptions, when $\gamma < 1/(({\|D\mathcal{T}\|}_\infty + {\|D^2\mathcal{T}\|}_\infty \|c-c_0\|)(1+L_\pi))$:

$$\|Q_{CE}^c - Q_{BE}^c\|_\infty \leq \frac{\|c-c_0\|^2}{1-\gamma}\!\left(\|D^2 R\|_\infty + \frac{\gamma(1+L_\pi)\|D^2\mathcal{T}\|_\infty(\|R\|_\infty + \|DR\|_\infty)}{1 - \gamma\max(1, \|D\mathcal{T}\|_\infty(1+L_\pi))}\right)$$

The CEBE Q-function approximates the true Bellman Q-function to second order in context distance.

**Theorem 3 — Stochastic CEBE accuracy.** Under bounded $\text{diam}(\mathcal{S})$, bounded second derivatives of $\mathcal{T}^c$ and $R^c$, and $\|c - c_0\| < \|\partial^2_c \mathcal{T}\|_\infty^{-1/2}$:

$$\|Q_{CE}^c - Q_{BE}^c\|_\infty \leq \frac{\|c-c_0\|^2}{1-\gamma}\!\left(\|\partial^2_c R\|_\infty + \frac{3\gamma\,\text{diam}(\mathcal{S})(1+L_\pi)\|R\|_\text{Lip}\|\partial^2_c \mathcal{T}\|_\infty}{1 - \gamma\max(1, \text{diam}(\mathcal{S})L_\mathcal{T}(1+L_\pi))}\right)$$

The stochastic bound carries an extra $\text{diam}(\mathcal{S})$ factor introduced by the projection step.

**Theorem 4 — Policy optimality transfer.** If $\pi_{CE}$ is $L$-Lipschitz and $(\mathcal{C}, \varepsilon)$-optimal under CEBE, and $\|Q_{CE}^c - Q_{BE}^c\|_\infty < \delta$ for all $c$, then $\pi_{CE}$ is $(\mathcal{C}, 2\delta + 2\varepsilon)$-optimal for the true Bellman equation. The approximation error enters the suboptimality gap additively; the $O(\|c-c_0\|^2)$ bound from Theorem 2/3 makes $\delta$ small near the training context.

## CSE Augmentation Formula

Given a transition $(s, a, r, s')$ collected under $c_0$ and a perturbation $\Delta c$, CSE constructs a synthetic sample as if collected under $c_0 + \Delta c$:

$$\text{CSE}((s,a,r,s'), \Delta c) = \left(r + \partial_c R^{c_0}(s,a,s')\,\Delta c + \partial_{s'} R^{c_0}(s,a,s')\,\partial_c \mathcal{T}^{c_0}\,\Delta c,\; s' + \partial_c \mathcal{T}^{c_0}\,\Delta c\right)$$

Multiple $\Delta c$ directions can be applied per real sample at negligible cost. The procedure is compatible with any off-policy RL algorithm and requires only Jacobian access, not additional environment rollouts.

Tabular validation (Cliffwalker): log-log plot of $\|Q_{CE}^c - Q_{BE}^c\|_\infty$ vs. $\|c - c_0\|$ gives best-fit slope $\approx 2$, confirming the $O(\|c-c_0\|^2)$ convergence rate empirically.

## Algorithm 1 (Off-Policy RL with CSE)

```
Input: CMDP M, training contexts D_train, iterations N, perturbation radius ε
Initialize: policy π, Q-functions, replay buffer B

for N data collection iterations:
    Sample c ~ D_train
    Collect trajectory {(s_t, c, a_t, r_t, s_{t+1})} using π in M'(c)
    Store in buffer B

    for training iterations:
        Sample batch {(s_t^i, c^i, a_t^i, r_t, s_{t+1}^i)} from B
        Generate perturbations Δc^i ∈ B(c^i, ε)
        Compute (r̄, s̄') = CSE(x^i, Δc^i)
        Update x^i ← (s, c + Δc^i, a, r̄, s̄')
        Train off-policy algorithm on updated batch
    end for
end for
```

Base RL algorithm: Soft Actor-Critic (SAC) in all experiments.

## Experimental Results

Evaluated against vanilla SAC (baseline) and Local Domain Randomization (LDR — oracle upper bound with access to true perturbed dynamics). All results are mean ± 95% CI over 10 trained policies, 64 trajectories per policy per context.

| Environment | Result |
|---|---|
| SimpleDirection | CSE matches LDR; both substantially outperform vanilla SAC |
| PendulumGoal | CSE outperforms LDR when goal torque > 0.6 |
| CheetahVelocity (MuJoCo) | CSE exceeds LDR when goal velocity > 2.6; both beat baseline |
| AntDirection (MuJoCo) | CSE comparable to LDR across most contexts |

CSE closes most of the gap to LDR — which has oracle dynamic access — from first-order gradient information alone. In structured parameter spaces where the Taylor expansion is accurate, the first-order approximation can outperform zeroth-order coverage (LDR).

## Limitations

**Deterministic transitions required for CSE.** The data augmentation formula assumes $\mathcal{T}^c$ is deterministic ($f^c(s,a)$). Stochastic settings would require a transport map between distributions — not generally available and computationally expensive. The stochastic CEBE theorem exists but has no practical CSE implementation.

**Gradient access requirement.** Context derivatives $\partial_c \mathcal{T}^{c_0}$ and $\partial_c R^{c_0}$ must be observable during training. This presupposes a differentiable simulator (e.g., a physics engine with Jacobian support). Black-box simulators and real hardware cannot provide these gradients.

**First-order breakdown at large context distance.** The $O(\|c - c_0\|^2)$ error grows quadratically; CEBE is a local generalization method, not an arbitrary OOD solution.

**Single training context scope.** Extending to a small set of training contexts is noted as future work but not formalized.

**Policy Lipschitz assumption.** Theorem 4 requires $\pi_{CE}$ to be Lipschitz; standard neural network policies do not satisfy this without additional regularization.

**MuJoCo-specific evaluation.** All continuous-control experiments use environments with smooth, differentiable dynamics — the setting most favorable to gradient-based augmentation. Transferability to discrete or non-smooth environments is unvalidated.

## Related

- [[_overview]] — single-sample RL fine-tuning hub; CEBE provides a formal generalization-theory result for single-context training directly relevant to the wiki's core question
- [[../../synthesis/proposed-method]] — CSE as gradient-based data augmentation parallels augmentation strategies in the proposed method; $O(\|c-c_0\|^2)$ bound is a reference point for the no-test-time-adaptation regime
- [[../../weekly-briefs/2026-07-03]] — brought in by the 2026-07-03 weekly sweep
