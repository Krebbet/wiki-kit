# Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability

**Geiger, Ibeling, Zur, Chaudhary, Chauhan, Huang, Arora, Wu, Goodman, Potts, Icard** (Pr(Ai)²R Group & Stanford University). JMLR 2025. arXiv:2301.04709. Generalizes causal abstraction theory to arbitrary mechanism transformations, providing a unified formal framework for mechanistic interpretability methods including path patching, concept erasure, sparse autoencoders, and causal scrubbing. Core innovation: interchange intervention accuracy (IIA) as a graded fidelity metric.

## Method

**Causal abstraction** formalizes when a high-level causal model faithfully represents the low-level internals of a system. The paper generalizes prior work from hard/soft interventions to *interventionals*—functionals that map mechanisms to mechanisms, enabling description of operations like zeroing or rotating activation subspaces.

**Exact transformations** (Def. 25) characterize when two models describe the same causal phenomena under a mapping (τ, ω), where τ translates low-level variable states to high-level ones and ω maps interventions. **Constructive causal abstraction** (Def. 33) is a special case where a high-level model H is an exact transformation of a low-level model L under an alignment ⟨Π, π⟩: a partition Π clusters low-level variables into high-level concepts, and maps π specify how low-level settings map to high-level values. Any abstraction decomposes into three operations: marginalization (remove variables), variable merge (cluster variables), and value merge (partition value spaces).

**Interchange interventions** (Def. 44) fix variables to counterfactual values from alternate inputs, enabling causal effect measurement. In a model with inputs and outputs: IntInv(M, ⟨s₁, …, sₖ⟩, ⟨X₁, …, Xₖ⟩) sets variables Xⱼ to values they would have under source input sⱼ. **Interchange intervention accuracy (IIA)** (Def. 48) measures the proportion of interchange interventions where high-level and low-level models agree on outputs:

IIA(H, L, (Π, π)) = E_{i∼P}[1[Proj_{X^Out_H}(τ_π(L_i)) = Proj_{X^Out_H}(H_{ωπ}(i))]]

This quantifies approximate abstraction via a similarity function Sim and statistic S (e.g., expected value). Unlike behavioral accuracy, IIA tests whether internal causal structure is preserved.

## Claims

- **Intervention algebras formalize model components**: Intervention algebras (subsets of mechanism replacements satisfying commutativity and left-annihilativity) act like hard interventions under composition; Examples include digit-masking and programming language mutations (Theorems 20–21, Examples 1–2).

- **Constructive abstraction via alignment**: A high-level model is a faithful simplification of a low-level model iff it is an exact transformation under an alignment; the alignment partitions low-level variables into clusters corresponding to high-level variables (Definition 31–33, Theorem 30).

- **Three decomposable operations**: Any alignment-based abstraction decomposes into marginalization, variable merge, and value merge, connecting causal abstraction to philosophy of science on variable choice and proportionality (Definitions 36–38, Proposition 40).

- **IIA as graded fidelity**: Interchange intervention accuracy measures approximate abstraction on a continuous scale, distinct from behavioral accuracy; IIA can be high while task accuracy is high (exposing "right answer, wrong reason" models) (Definition 41, 48).

- **Unified framework for interpretability methods**: Activation patching, causal mediation, causal scrubbing, concept erasure, sparse autoencoders, and steering are all special cases of causal abstraction under different alignment structures (Section 3.1–3.7).

- **Aligned models define unique intervention maps**: An alignment ⟨Π, π⟩ canonically induces functions ω_π and τ_π mapping low-level to high-level interventions and states (Remark 32, Equation 4–5).

- **Distributed interventions via bijective translation**: Interventions targeting variables distributed across overlapping neuron sets are handled via bijective translation to a transformed variable space, enabling intervention algebras on distributed features (Definition 46, Section 2.5).

## Relevance to the project

**IIA as a non-behavioral concept-fidelity metric**: The paper provides a theoretically grounded alternative to MDL-on-siblings for evaluating whether a model has truly learned a concept's causal structure. Rather than measuring behavioral accuracy on concept-masked siblings, IIA directly tests whether internal causal relationships match the high-level conceptual model. For a concept C like "supply increases demand decreases," IIA would measure whether interventions swapping causal variables (e.g., fixing supply to an alternate input's value) produce the same output as the high-level economic model. This is stronger than behavioral fidelity: a model can memorize correct predictions without representing causal structure, but high IIA implies structural alignment.

**Gap between behavioral and IIA accuracy as a memorization detector**: If a fine-tuned model achieves high behavioral accuracy on a concept but low IIA, it indicates the model "gets the right answer without representing the concept"—a key risk for single-sample learning. The gap exposes superficial pattern matching or shortcut learning, particularly relevant when training on a single example where memorization risk is highest. Measuring both metrics reveals whether the model has genuinely internalized the concept's causal logic or merely learned spurious correlations.

**Practical cost and applicability limits**: IIA requires identifying and aligning high-level causal variables with model internals. For "supply and demand," this means defining the causal graph (supply → demand, price → quantity) and identifying internal representations that implement these edges—likely distributed across attention heads and MLPs. The alignment burden scales with concept complexity and model opacity. The paper's framework handles this via partition Π and maps π, but in practice, discovering Π requires either interpretability tools (sparse autoencoders, linear representation hypothesis verification) or domain engineering. For single-sample concept learning, this cost may be justified as a quality gate: if you can't align the concept to the model, you lack confidence it was truly learned.

## Source

- arXiv: 2301.04709
- Venue: JMLR 2025
- Raw markdown: `../../../raw/research/concept-understanding-eval/07-causal-abstraction.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[control-tasks-probes]] — methodological floor for any internal-representation probe; causal-abstraction provides the *intervention-based* alternative to probe-based concept claims
- [[../synthesis/recursive-concept-learning]] — **E1** alternative axis: IIA (interchange-intervention accuracy) as a non-behavioral concept-fidelity metric; complement to MDL when the concept has identifiable internal variables
- [[../synthesis/proposed-method]] — gap #6 (LLM concept-probe metric); IIA is the alternative when MDL on text-output siblings is intractable
- [[../concept-learning/concept-bottleneck-models]] — CBM-style intervention is the simplest case of an interchange intervention
- [[../concept-learning/recursive-concept-evolution]] — RCE's gate activations could be probed by interchange intervention as an alternative to MDL acceptance
