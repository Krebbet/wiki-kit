# Hierarchy and Near-Decomposability

Simon's 1962 argument is that hierarchy — systems of subsystems, recursively — is the near-universal architecture of complex systems, and that this is a claim about *what can get built*, not about authority. Two mechanisms carry it. The watchmaker parable, formalised: with a per-step interruption probability, assembling a system from stable intermediate subassemblies takes time proportional to the number of levels, log_s(n), while assembling the same n elements without them grows near-exponentially, because every interruption destroys all work in progress. And near-decomposability: within-subsystem interactions are systematically stronger than between-subsystem ones, which yields two proved dynamical properties — in the short run each component behaves approximately independently of the others, and in the long run each depends on the others only through their *aggregate* behaviour. The second is the formal licence for divisional delegation: a headquarters that receives only aggregates from a nearly-decomposable division is not being negligent, it is using all the information the dynamics make relevant. Simon is unusually explicit about grading his own evidence, and disclaims the social and historical extrapolations that make the essay quotable.

**Evidence tier note.** (b) throughout, and Simon says so. Strongest: the watchmaker probability calculation and the near-decomposable-matrix theorem proved in Simon & Ando (*Econometrica*, 1961), applied to a heat-diffusion example and to input-output economics. Weaker: cross-domain illustration — bond-strength hierarchies, astronomical systems, sociometric networks, firms and governments named together as instances. **Weakest, and self-flagged as such:** Alexander's empire, T. E. Lawrence and the Arab revolt, curriculum design. Simon writes "I shall not elaborate upon my fancy... I shall leave it to historians", and says of his own headline number that it should not "be taken seriously" — only the qualitative log-versus-exponential conclusion. There is no dataset of actual institutions anywhere in the paper.

## Why complexity forces depth

**[model]** Two watchmakers assemble watches of 1000 parts and are interrupted at the same rate. Hora builds stable subassemblies of ten; an interruption costs him at most the subassembly in hand. Tempus builds each watch as one run of 1000; an interruption costs him everything done so far. At an interruption probability of 0.01 per step, Simon's illustration puts Hora roughly **4,000×** faster. Generalised: assembly time for a hierarchic system with span s grows as **log_s(n)** — with the number of *levels* — while the flat system's grows catastrophically with the number of elements.

**[wiki synthesis]** The claim's force is selective, not normative. It does not say hierarchic systems perform better; it says non-hierarchic complex systems mostly never come into existence, because the time required to assemble one exceeds the interval between disturbances. Observed hierarchy is therefore weak evidence of anything about hierarchy's merits — it is what survives a construction filter. That is a different argument from every cost-minimisation account of layers, including [[knowledge-hierarchies-and-the-cost-of-scale]], and it is compatible with them.

## Near-decomposability

**[model]** Coupling is continuous, not binary. Fully decomposable systems (no cross-interaction) and fully coupled ones (all elements interacting equally) are both rare limiting cases; nearly-decomposable systems, where between-subsystem interaction is weak but non-zero relative to within-subsystem interaction, are the dominant observed case. The theorem gives two properties:

1. **Short run** — each component's behaviour is approximately independent of the others.
2. **Long run** — each component depends on the others only through their aggregate behaviour.

Simon's worked physical case is a suite of rooms and cubicles with differential wall insulation: temperatures equalise fast within a room, slowly between rooms. The economic case is an input-output matrix, where industries cluster into strongly-linked groups via raw-material and semifinished-product flows and are weakly linked across groups — with one exception he flags himself, the consumption subsystem, which is strongly linked to nearly everything and breaks clean decomposability.

**[model — the design implication]** Keep inter-module coupling weak, and delegation becomes cheap: subsystems can be managed and analysed independently, with only aggregate information about the rest of the system — budget totals rather than line-item cross-department detail. Build from stable subassemblies rather than components that only cohere when the whole is finished, and the structure survives interruption.

## Span, and what Simon does not explain

**[model]** Span at a given level is bounded by a cognitive fact: "a human being is more nearly a serial than a parallel information-processing system" — one conversation at a time, and relational roles that cannot be enacted with unbounded numbers of others. This is a specific micro-mechanism for a ceiling on breadth, distinct from the supervision-cost arguments in [[governance-structures]].

Simon then flags the gap in his own theory: "A more complete theory... would presumably have something to say about the determinants of width of span in these systems." The essay explains why *depth* emerges with size; it does not say what sets *breadth* at each level. [[knowledge-hierarchies-and-the-cost-of-scale]] later supplies one answer (span bounded by the manager's helping-time constraint), and [[bureaucratic-growth-and-parkinsons-law]] supplies a rival one (span set by the promotion regime, r subordinates per promotion).

**[model]** Position within a hierarchy correlates with the time-scale of dynamics: higher levels have longer planning horizons and lower-frequency, longer-duration interactions. This is a claim about vertical position at a point in time — not about how a system changes as it ages.

**[model — nominal vs. actual]** Simon notes directly that "the real flesh-and-blood organization has many interpart relations other than the lines of formal authority." The org chart is not the interaction network. He does not develop it, but it is the earliest statement in this wiki's sources of the nominal-versus-actual accountability distinction that [[open-questions]] Q11 asks for a method to resolve.

## Two things the paper is not evidence for

**[wiki synthesis — gaps]**

- **Public/private invariance is assumed, not shown.** Simon groups "business firms, governments, universities" as instances of one phenomenon and never contrasts a bureau against a firm on any axis. The invariance is built into the level at which the theory is pitched. Treat it as an asserted scope, not a finding — it is one of the two sources in this batch that assert invariance without testing it. See [[open-questions]] Q3.
- **The paper says nothing about institutional age.** Its only time claims concern *evolutionary and assembly time* — how long a complex form takes to come into being. Post-formation ageing, ossification and behavioural drift are outside its scope entirely. The one age-adjacent idea, "ontogeny recapitulates phylogeny" applied to curricula, is about developmental sequence replaying history, and is among the passages Simon disclaims. See [[open-questions]] Q7.

## Source

- `raw/research/scale-effects/07-simon-architecture-of-complexity.md` — Herbert A. Simon, "The Architecture of Complexity", *Proceedings of the American Philosophical Society* 106(6), 1962 (read 26 April 1962). https://www.cs.brandeis.edu/~cs146a/handouts/papers/simon-complexity.pdf

## Related

- [[knowledge-hierarchies-and-the-cost-of-scale]] — the modern formalisation of the same intuition at firm level, with prices on the frictions Simon left qualitative; it also fills the span gap Simon flags.
- [[bureaucratic-growth-and-parkinsons-law]] — the opposing reading of depth: layers as the residue of career incentive rather than as the precondition for complexity.
- [[governance-structures]] — Williamson's bounded rationality is Simon's, and near-decomposability is a formal rationale for the M-form delegation TCE treats as a governance choice.
- [[polycentric-governance]] — Ostrom's nested, quasi-autonomous units and Simon's weakly-coupled subsystems describe the same shape from different traditions; whether polycentricity is near-decomposability applied to governance is worth testing.
- [[path-dependence-and-increasing-returns]] — both are "history matters" arguments and must not be merged: Simon's is about how a structure *forms*, path dependence about why a formed structure resists change.
- [[dimensions-of-institutional-variation]] — supplies D38 (coupling strength / decomposability) and reinforces D36 (span) and D37 (depth).
- [[what-is-an-institution]] — Simon's bare structural definition of hierarchy sits beneath the North/Ostrom/Williamson definitional dispute rather than inside it.
