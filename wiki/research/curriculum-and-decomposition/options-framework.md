# Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement Learning

Sutton, Precup, and Singh introduce options—closed-loop policies for temporally extended action—to extend MDPs with temporal abstraction. An option $\langle I, \pi, \beta \rangle$ consists of an initiation set, internal policy, and termination condition, and naturally embeds in the SMDP framework. Core result: any MDP with a fixed set of options is formally an SMDP, enabling learning and planning at multiple timescales. Artificial Intelligence Journal 112 (1999) 181–211.

## Method

An option $\langle I, \pi, \beta \rangle$ is defined by three components: an initiation set $I$ specifying states where it can begin, a (Markov or semi-Markov) policy $\pi$ that selects actions while the option runs, and a termination condition $\beta(s)$ giving the probability of termination in state $s$. Execution is straightforward: when initiated in state $s \in I$, the option selects actions according to $\pi$ until termination occurs stochastically via $\beta$. Primitive actions are special cases where $I = \{s: a \in A_s\}$, $\pi(s,a) = 1$, and $\beta(s) = 1$.

The key theoretical foundation is Theorem 1: an MDP augmented with a fixed set of options $O$ forms a discrete-time SMDP. This formalizes the interplay between levels: the underlying MDP governs primitive action dynamics, while options impose a layer of temporal abstraction. Value functions generalize naturally: $V^\pi(s)$ and $Q^\mu(s,o)$ are defined over option-level decisions using multi-time models that accumulate discounted rewards and state transitions over variable-length option executions.

Planning and learning follow SMDP machinery. Synchronous value iteration over options updates $V_k(s) = \max_{o \in O_s} (r_s^o + \Sigma_{s'} p_{ss'}^o V_{k-1}(s'))$, where the state-transition probabilities $p_{ss'}^o$ and rewards $r_s^o$ aggregate all outcomes of executing $o$ from $s$ to termination. SMDP Q-learning similarly updates $Q(s,o)$ after each option terminates, converging to optimal $Q^*_O(s,o)$ under standard conditions.

## Claims

- **Theorem 1 (MDP + Options = SMDP)**: Any MDP with a fixed set of options defines a discrete-time SMDP, providing the foundation for planning and learning methods that treat options as indivisible units (Sec. 3). Results on convergence of value iteration and Q-learning for SMDPs directly apply.

- **Planning speedup**: Multi-step options can dramatically reduce the computational cost of dynamic programming by grouping transitions and achieving good approximations in fewer iterations, as shown in the rooms domain (Sec. 3.1, Fig. 2). Hallway options let agents plan room-to-room rather than cell-by-cell.

- **Learning acceleration**: SMDP Q-learning over options converges to optimal policies while requiring fewer updates than learning over primitive actions alone, particularly when high-level options allow agents to explore goals more efficiently (Sec. 3.2, Fig. 6).

- **Theorem 2 (Interruption)**: Plans found via SMDP methods can be improved at execution time by interrupting options when switching becomes more valuable. If $V^\mu(s) > Q^\mu(s,o)$, terminating $o$ and selecting a new option yields weakly better value, often strictly better. This enables performance exceeding $V^*_O$ without recomputing (Sec. 4, Theorem 2). Demonstrated on landmark navigation and mass-control tasks (Figs. 7–8).

- **Intra-option learning**: For Markov options, temporal-difference updates can learn from fragments of experience within an option execution, avoiding the need to wait for termination (Sec. 5–6). Equations (18)–(19) define one-step intra-option model learning; equations (20)–(21) define intra-option Q-learning. Both converge faster than SMDP methods and enable off-policy learning about multiple options simultaneously from the same trajectory.

- **Theorem 3 (Intra-option Q-learning convergence)**: One-step intra-option Q-learning with deterministic option policies converges to $Q^*_O$ regardless of which options are executed, provided all actions are taken sufficiently often (Sec. 6, Theorem 3). This enables learning about options without executing them.

- **Subgoals**: Options can be learned by defining terminal subgoal values $g(s)$ on a goal set $G$ and optimizing the cumulative reward plus subgoal bonus. Q-learning with subgoal-modified rewards learns option policies that achieve the subgoal (Sec. 7, Fig. 11). Formalizes the relationship between options and abstract goals.

## Relevance to the project

The options framework is direct prior art for RCL's curriculum-level temporal abstraction. RCL's outer loop—$\text{Decompose}(c) \rightarrow \{\text{LearnConcept}(p) \text{ for } p \text{ in } \text{prereqs}(c)\} \rightarrow \text{Retest}(c)$—structurally mirrors an option execution. A single call to $\text{LearnConcept}(p)$ is an option $\langle I, \pi, \beta \rangle$ where $I$ = "concept $c$ failed," $\pi$ = inner training loop for $p$, and $\beta(s) = 1$ when $p$ passes its Evaluate criterion. The prerequisite training becomes a sub-policy with its own start-state ($c$ failed) and termination ($p$ learned), enabling curriculum-level credit assignment—exactly the gap that intra-option learning addresses.

Intra-option methods are a candidate mechanism for RCL's primary gap (Gap #1: no curriculum-level credit signal). Standard SMDP Q-learning treats each $\text{LearnConcept}(p)$ as opaque and only updates $Q(c, p)$ after termination; intra-option learning would update $Q(c, p)$ from fragments of the training trajectory within $\text{LearnConcept}(p)$—e.g., observing that $p$ made progress partway through training. This allows the parent loop to adapt prerequisite selection earlier, without waiting for full training convergence.

However, the formal SMDP results do not cleanly transfer. The options framework assumes the base system is Markov: state transitions and outcomes depend only on the current state and action. Curriculum state—which concept is failing, what prior prerequisite training has occurred, how the learner's model has changed—is not Markov. A state transition that succeeds given one training history may fail given another, and the timing of prerequisite success depends on the learner's current knowledge, not just the current concept. Thus Theorems 1–3 (convergence, optimality, interruption) cannot be applied directly; curriculum-level policy improvement and credit assignment require additional reasoning about non-Markov curriculum state.

## Source

- Venue: Artificial Intelligence Journal 112 (1999) 181–211
- Authors: Richard S. Sutton, Doina Precup, Satinder Singh
- Raw markdown: `../../../raw/research/rcl-gap-fillers/04-options-framework.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[poet]] — open-ended-evolution sibling; both papers structure recursion / hierarchy through emergent rather than pre-built scaffolds
- [[../synthesis/recursive-concept-learning]] — RCL's $\text{LearnConcept}(p)$ is structurally an option $\langle I, \pi, \beta \rangle$ with initiation = "concept $c$ failed", policy = inner training loop, termination = "$p$ passes Evaluate". Intra-option learning is the canonical mechanism for curriculum-level credit assignment (RCL gap #1).
- [[../rl-optimizers/_overview]] — RCL's inner loop sits inside the option's internal policy; the optimiser choice ([[../rl-optimizers/dr-grpo]] et al.) is orthogonal to the SMDP framing
- [[../rlvr-mechanics/_overview]] — flat (non-hierarchical) RL setting that RCL extends with curriculum-level abstraction
