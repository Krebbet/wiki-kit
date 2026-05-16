# Automatic Curriculum Learning For Deep RL: A Short Survey

Portelas, Colas, Weng, Hofmann, Oudeyer (2020). Foundational survey systematizing automatic curriculum learning (ACL) mechanisms in deep RL across three organizing dimensions: *why* (objectives), *what* (control targets), and *what optimizes* (surrogate objectives). Covers learning-progress-based task selection, teacher-student bandits, and intrinsic-motivation framings. arXiv 2003.04664.

## Method

The survey classifies ACL as a meta-learning mechanism that learns a task selection function D: H → T to maximize performance on a target task distribution after N training steps. Two main control axes: *data collection* (organizing task presentation by modifying environments, initial states, reward functions, or goals via procedural content generation) and *data exploitation* (prioritized experience replay, hindsight experience replay, transition filtering).

Within each axis, ACL mechanisms optimize surrogate objectives to approximate the intractable global learning-progress objective. Key surrogate objectives include: (1) *intermediate difficulty* — selecting tasks neither too easy nor too hard (GoalGAN, Reverse Curriculum Learning); (2) *learning progress (LP)* — favoring tasks where performance improvement is steepest, cast as a multi-armed bandit problem with LP values (ALP-GMM, CURIOUS, Teacher-Student CL via Matiisen et al.); (3) *diversity/novelty* — low-density goal regions and state visitation counts; (4) *surprise* (model prediction error or disagreement); (5) *adversarial reward maximization* in self-play settings. The survey emphasizes that ACL's core insight is adaptive data distribution rather than emergent curricula.

## Claims

- **Learning progress as a bandit criterion** — Maximizing LP (derivative of competence) under concave learning profiles is optimal and avoids threshold tuning required for "intermediate difficulty" (Lopes & Oudeyer, 2012; Matiisen et al., 2017; Mysore et al., 2018).

- **Teacher-student framing as a foundational analogy** — Matiisen et al. (2017) frames curriculum learning as a teacher selecting tasks for a student learner, instantiated via bandit algorithms on discrete task sets; Racaniére et al. (2019) extends this with a "Setter-Solver" model where a judge network predicts feasibility, decoupling task generation from difficulty.

- **ALP-GMM bridges continuous task spaces** — Portelas et al. (2019) recovers a bandit structure over continuous environments via Gaussian Mixture Models, selecting niches of high LP and maintaining exploration through residual uniform sampling.

- **Intrinsic motivation via surprise signals** — Uncertainty-driven exploration (ICM, RND, Disagreement-based) use model prediction error or ensemble disagreement as intrinsic rewards, guiding agents to high-entropy / rarely-visited state regions (Pathak et al., 2017, 2019; Burda et al., 2019).

- **Multi-goal ACL through goal-conditioned curriculum** — Hindsight Experience Replay and its variants (HER, HER-curriculum, CURIOUS) use LP or diversity metrics to select substitute goals or prioritize transitions, enabling agents to solve hard goals by learning easier ones first.

- **Data exploitation complements data collection** — Prioritized Experience Replay (Schaul et al., 2015) and LP-weighted transition sampling achieve complementary gains; in sparse-reward and multi-goal settings, biasing replay toward high-information transitions (high reward, high LP, or high diversity) improves sample efficiency.

- **Self-Play as adversarial curriculum** — AlphaGo Zero, AlphaStar, Hide & Seek maintain a league of opponent versions selected for challenge; maintains diversity and robustness, avoiding single-mode overfitting.

- **Lack of theoretical grounding in NL domains** — The survey notes ACL lacks formal foundations in RL and does not address natural-language concept spaces or structured symbol manipulation, limiting applicability beyond continuous parameter and discrete task selection.

## Relevance to the project

The survey's "learning progress" signal maps directly to RCL's *D2 learnability filter*: when should recursive concept decomposition give up on learning a prerequisite? In bandit-theoretic terms, once the LP derivative for a subgoal flattens (competence plateaus), the agent should either backtrack or switch to an alternative decomposition. ALP-GMM's continuous task-space bandit formulation via Gaussian Mixture Models is particularly relevant — RCL's concept lattice could be analogously structured as a hierarchy of concept clusters, with LP metrics driving which concepts to foreground next.

The teacher-student and Setter-Solver framings provide structural homology to RCL's `M.Decompose` operation: when the decomposer returns a candidate prerequisite skill, a feasibility estimator (analogous to the Setter-Solver's judge network) could predict whether the current agent has sufficient capability to learn it. This decouples concept generation from difficulty assessment. Matiisen et al. (2017) and Racaniére et al. (2019) offer concrete implementations.

However, critical limitations emerge. ACL in the survey operates on continuous parameter spaces (environment randomization, initial state distributions, goal reachability) or discrete task libraries (Minecraft levels, opponents). RCL's conceptual curriculum operates on *structured symbolic knowledge* — concept definitions, prerequisite graphs, and proof-search strategies — where intermediate difficulty is less cleanly defined. Notions of "surprise" (model prediction error) do not translate directly to concept learnability. Moreover, the survey's curriculum-state representation (agent performance metrics, task difficulty estimates) differs from RCL's learner state (what concepts have been internalized, which proof strategies are reliable), requiring substantial domain translation.

## Source

- arXiv: 2003.04664
- Authors: Rémy Portelas, Cédric Colas, Lilian Weng, Katja Hofmann, Pierre-Yves Oudeyer
- Raw markdown: `../../../raw/research/rcl-gap-fillers/08-acl-deep-rl-survey.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[curriculum-survey]] — broader curriculum-learning survey covering supervised + RL; this paper is the RL-specific specialisation
- [[poet]] — POET is one of the canonical ACL methods this survey catalogues
- [[bengio-curriculum]] — pre-RL theoretical ancestor of the ACL frame
- [[../synthesis/recursive-concept-learning]] — Learning Progress (LP) signal is a candidate for **D2** (decomposition cost bound / `MAX_DEPTH` learnability filter); teacher-student bandit framings are structural analogues of `M.Decompose`
- [[../teacher-student-rl/soar-edge-of-learnability]] — bilevel meta-RL with teacher reward = student improvement; SOAR is the LM-frontier descendant of the ACL teacher-student frame
