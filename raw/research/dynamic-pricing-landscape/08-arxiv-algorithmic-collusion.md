---
url: "file:///tmp/pdf-cache/arxiv-algorithmic-collusion.pdf"
title: "(untitled)"
captured_on: "2026-04-21"
capture_method: "pdf"
engine: "pymupdf"
assets_dir: "./assets/arxiv-algorithmic-collusion"
---

## ALGORITHMIC PRICING AND ALGORITHMIC COLLUSION


**Matthias Oberlechner**
Department of Computer Science
Technical University of Munich
```
matthias.oberlechner@tum.de

```

**Martin Bichler**
Department of Computer Science
Technical University of Munich
```
   m.bichler@tum.de

```

**Julius Durmann**
Department of Computer Science
Technical University of Munich
```
 julius.durmann@tum.de

```
April 24, 2025


#### ABSTRACT


The rise of algorithmic pricing in online retail platforms has attracted significant interest in how
autonomous software agents interact under competition. This article explores the potential emergence of algorithmic collusion — supra-competitive pricing outcomes that arise without explicit
agreements — as a consequence of repeated interactions between learning agents. Most of the
literature focuses on oligopoly pricing environments modeled as repeated Bertrand competitions,
where firms use online learning algorithms to adapt prices over time. While experimental research
has demonstrated that specific reinforcement learning algorithms can learn to maintain prices
above competitive equilibrium levels in simulated environments, theoretical understanding of when
and why such outcomes occur remains limited. This work highlights the interdisciplinary nature of
this challenge, which connects computer science concepts of online learning with game-theoretical
literature on equilibrium learning. We examine implications for the Business & Information
Systems Engineering (BISE) community and identify specific research opportunities to address
challenges of algorithmic competition in digital marketplaces.

**_Keywords_** algorithmic collusion, online learning, game theory


**_Note_** This article has been accepted in Business & Information Systems Engineering (BISE).

#### 1 Introduction


Worldwide, companies are increasingly using algorithms and artificial intelligence (AI) in order to power their
operations, from product development to manufacturing and marketing, and product pricing is no exception.
This new type of information systems based on learning algorithms has drawn considerable attention aiming to
understand their societal effects (Lysyakov and Viswanathan 2023, Lu and Zhang 2024, Fügener et al. 2021).
An important question in this overall stream is how learning algorithms are used for pricing (Brackmann et al.
2024). Algorithmic pricing is a practice where software agents automatically determine prices for items for
sale, in order to maximize the seller’s profits. This practice is increasingly common in online retail markets.
Chen et al. (2016) estimated that by 2015, algorithms were used in setting prices for roughly one-third of the
top 1600 products on Amazon. By 2018, the average product price on Amazon reportedly changed every ten
minutes and adapts to market conditions.[1] Since then, an industry has developed around automated pricing
software.

The prices determined by the different firms depend on each other’s actions, and the overall environment in
which they operate is that of an oligopoly competition. Economic theory has long aimed to predict the outcome
of such competitive situations. Models of oligopoly competition assume some knowledge about the demand of
customers, such as a readily available demand function, and then they determine a Nash equilibrium price.

[1https://www.businessinsider.com/amazon-price-changes-2018-8](https://www.businessinsider.com/amazon-price-changes-2018-8)


-----

For example, in the celebrated Bertrand competition model, companies producing identical (homogeneous)
products simultaneously choose their pricing strategies based on a given demand function that takes the prices
of the competitors into account (Bertrand 1883). In this model, the competitors play their equilibrium strategy
from the start. Usually, sellers entering the market have limited information about competitors’ costs or
customer demand at different prices, and they must learn over time which prices optimize profit. Additionally,
changes in demand and supply over time require recalculating the equilibrium strategy, which emphasizes
the need for an adaptive and learning pricing software agent. From the perspective of an individual seller,
algorithmic pricing aims to solve an online learning problem (Shalev-Shwartz 2011), where the seller’s actions
are the prices they set, and the objective is to maximize profit. But what is the outcome of markets with such
learning agents? Can we assume that they converge to an equilibrium price?

Recent experimental research showed that learning algorithms can lead to prices higher than the Nash
equilibrium in the static oligopoly pricing game (Waltman and Kaymak 2008, Calvano et al. 2019, Abada and
Lambin 2023, Klein 2021, Abada et al. 2024b, Brown and MacKay 2023). This phenomenon is referred to as
_algorithmic collusion._ Explicit collusion refers to anti-competitive conducts that are maintained with explicit
agreements. Firms interact directly and agree on the optimal level of price or output (OECD 2017). In contrast,
“tacit collusion refers to forms of anti-competitive co-ordination which can be achieved without any need for
an explicit agreement, but which competitors are able to maintain by recognizing their mutual interdependence.
In a tacitly collusive context, the non-competitive outcome is achieved by each participant deciding its own
profit-maximizing strategy independently of its competitors.” (OECD 2017) Algorithmic collusion is a form
of tacit collusion where supra-competitive outcomes different from the Nash equilibrium of the static gametheoretical model of competition are produced by learning algorithms without being programmed to produce
those outcomes. Similar definitions are provided by den Boer (2023) and Abada et al. (2024a).

There are also cases suggesting that algorithmic collusion happens in real-world markets. For example, Assad
et al. (2024) showed that margins increased 28% in local duopoly retail gasoline markets in Germany when
both firms adopted algorithmic pricing software, while there was no price change in local monopolies. The
paper finds pricing algorithms can learn tacitly collusive pricing strategies which are legal in most jurisdictions
without explicit communication. An investigation in the UK revealed that online poster retailers were using
simple pricing algorithms in the context of a horizontal cartel among retailers to coordinate their prices on
Amazon.[2] The phenomenon raised concerns among regulators as it may reduce consumer welfare. In recent
years, several competition authorities, including France and Germany, Denmark, Japan, Norway, and Sweden,
have published policy papers considering the relationship between algorithms and competition (OECD 2024).

However, the magnitude of the threat from algorithmic collusion by autonomous self-learning algorithms in
other markets is still disputed in the academic literature. Ultimately, algorithmic collusion touches on a deep
and non-trivial question, that of learning in games. Under which conditions do learning algorithms converge
to an equilibrium in repeated play and when is this not the case? When do we see algorithmic collusion,
inefficient price cycling, or even chaotic price dynamics as a result of automated pricing decisions? Currently,
there is no comprehensive theory that would provide answers to these questions. Up to now, there are only very
few articles in Business & Information Systems Engineering outlets on algorithmic collusion (Kang et al. 2022,
Douglas et al. 2024, Deng et al. 2024, Bichler et al. 2023). The topic is central for the welfare of electronic
markets today and it draws on learning algorithms from computer science as well as game-theoretical models
as they have been developed in economics.

The aim of this catchword article is to discuss algorithmic collusion and make the basic problem and the
related questions accessible to a broader community. This will allow us to point to avenues for future research
in Business & Information Systems Engineering.

#### 2 Oligopoly Pricing

Pricing in online retail markets is an environment that can be modeled as a Bertrand competition (Bertrand
1883). In this model, firms compete by setting prices for a homogeneous product. The demand for the product
depends on the prices set by all firms. The firms’ objective is to maximize their profit, which is the revenue
from selling the product minus the cost of producing it. The revenue depends on the price set by the firm and

[2https://www.gov.uk/cma-cases/online-sales-of-discretionary-consumer-products](https://www.gov.uk/cma-cases/online-sales-of-discretionary-consumer-products)


-----

the demand for the product. The demand is a function of the prices set by all firms. The cost of producing the
product is typically assumed to be linear in the quantity produced.

More formally, the Bertrand competition can be described as a normal-form game, where n players (or firms)
make decisions at the same time. Each player i = 1, 2, . . ., n has a set of possible actions ai _∈Ai_ to choose
from - like different prices they could set for their products. Each player’s goal is to maximize their payoff they
get based on everyones actions, which is given by their individual payoff function ui : A1 × · · · × An _→_ R.
Normal-form games are used to model environments where multiple agents interact and influence each others’
outcomes. Other examples include, for instance, the Cournot oligopoly, platform competition, auctions, and
contests. Most of the literature on algorithmic collusion is based on the classic Bertrand competition model.

In a Bertrand competition, the firms’ action ai _∈Ai_ is the price for a good it wants to produce. All firms
produce the same good, and they all take action simultaneously. Firms compete for demand with their prices
and affect each others’ revenues. The demand di(ai, a−i) depends on all actions, their own actions ai and the
others’ actions a−i, and is decreasing in their own price. Assuming that the cost functions are linear in the
demand, the payoff (or utility) function of firm i can be described by

_ui(ai, a−i) = di(a) · (ai −_ _ci)._ (1)

This model allows for various assumptions about consumer demand (e.g., all-or-nothing or logit), and the
equilibrium prices in these scenarios have been analyzed. In the standard case, with all-or-nothing demand,
the firm with the lowest price gets all the demand. If multiple firms offer the lowest price, the demand is shared
equally. This leads to a demand function given by


_di(ai, a−i) =_


� _nminD_ [(1][ −] _[a][i][)]_ if i ∈ arg minj∈N _aj_ _,_ (all-or-nothing)
0 else


where D _> 0 is the maximum total demand, N_ is the set of market participants, and nmin := |arg minj∈N _aj|_
is the number of firms with the lowest price.

Another demand model used in a widely cited article by Calvano et al. (2020), is the multinomial or logit
_demand._ In this setting, the demand is split between the n agents/goods and some outside good (indexed with
0) according to

� _αi−ai_ �
exp _µ_
_di(ai, a−i) =_ _._ (logit)

� _α0_ � � _αj_ _−aj_ �
exp _µ_ + [�]j[n]=1 [exp] _µ_

The parameters αi _> 0 capture different product quality indices and µ > 0 models a product differentiation_
between the goods, i.e., if µ → 0, the goods are perfect substitutes.

In a standard Bertrand model with homogeneous products and symmetric firms, prices equal marginal costs
in equilibrium. However, this changes with asymmetries or product differentiation. With asymmetric costs
between firms, the Nash equilibrium typically involves the low-cost firm pricing at or just below the marginal
cost of the high-cost firm. With product differentiation (as in logit demand), equilibrium prices are typically
above marginal costs due to firms having some market power. These equilibrium prices are below a monopoly
price because the competition drives down profits.

Note that the static model of Bertrand competition has been extended to repeated games. A repeated game
consists of a number of repetitions of some base game (called a stage game). In such dynamic settings, a price
above the Nash equilibrium of the stage game can be an equilibrium of this repeated game depending on the
strategy used by each firm and other exogenous factors (Maskin and Tirole 1988). Actually, the Folk Theorem
in repeated game theory shows that if players are sufficiently patient, a wide range of payoffs can be sustained
as Nash equilibria, including outcomes that are better for each player than their min-max (or punishment)
payoff (Maschler et al. 2020). The literature on algorithmic collusion takes the Nash equilibrium of the stage
game of such repeated games as a baseline to determine algorithmic collusion (Abada et al. 2024a).

Much of the discussion around algorithmic collusion relies on simulations of learning algorithms in repeated
Bertrand competition models with fixed sellers and specific demand functions. Although real-world scenarios
may be more complex, this abstraction allows for an analysis of the model and the computation of its static
Nash equilibrium. This knowledge enables comparative statics based on cost and demand knowledge, which


-----

is typically unavailable in empirical studies. If algorithmic collusion does not arise in a repeated Bertrand
pricing game, it may be even less likely in more complex scenarios with fluctuating demand and supply. If it
does arise, it is a strong indicator that the phenomenon is not limited to the specific model but may also occur
in more complex settings.

In what follows, we introduce important online learning algorithms, the emerging literature on algorithmic
collusion, and the key results from the literature on learning in games that are related to it. These literature
streams are important for the study of algorithmic collusion and inter-related.

**2.1** **Online Learning**

A major challenge in developing algorithmic pricing agents is deciding whether to focus on short-term profit
(by exploiting a known high-yield price) or on exploring alternative prices that may lead to better long-term
outcomes. Online learning algorithms are designed to balance this exploration-exploitation trade-off and can
handle large product portfolios effectively (Bubeck 2011). On online platforms, these algorithms operate with
bandit feedback, meaning that after setting a price, a seller observes the profit associated with that specific price.
The multi-armed bandit model is especially relevant to algorithmic pricing, a connection recognized early on.
Bandit algorithms were proposed for pricing as far back as Rothschild (1974), well before digital marketplaces
emerged. Today, multi-armed bandit algorithms for pricing are widely studied in academia (Trovo et al.
2015, den Boer 2015, Bauer and Jannach 2018, Mueller et al. 2019, Elreedy et al. 2021, Taywade et al. 2023,
Qu 2024, Kasa and Rajan 2021), and practitioners also provide numerous resources on implementing these
algorithms.[3]

Online optimization and learning algorithms are prime candidates for pricing algorithms on online platforms
(Mueller et al. 2019, Elreedy et al. 2021, Taywade et al. 2023, Qu 2024). Online optimization is concerned
with making sequential decisions in an unknown environment with the goal of optimizing a performance
metric over time. Let us briefly introduce the basic model of online learning in the context of algorithmic
pricing in its most abstract form (see Algorithm 1). At each stage t = 1, 2, . . ., the agent chooses an action
_at_ _∈A from some action set according to some strategy st_ _∈S_ and gets a payoff ut(at). In algorithmic
pricing, this action would be the price of an agent. The agent would leverage the information about the utility,
i.e., feedback, she gets in order to update his actions or prices.

**Algorithm 1: Online Learning**
**Require :action set A, sequence of payoff functions ut** : A → R
**for t = 1, 2, . . .** **do**

select action at _∈A according to strategy st;_
realize payoff ut(at) and observe feedback ft;
update strategy st _←_ _st+1 using feedback ft;_
**end**

Algorithms are widely analyzed in two models, the adversarial model and the stochastic model. In both models,
the objective goal is to maximize the expected reward by selecting the best action(s). In the stochastic setting,
we assume that the rewards are drawn independently and identically from some underlying distribution that
does not change over time. In the adversarial model, the input can be chosen by an adversary that can react to
the agent’s past decisions and its algorithm. There are different types of feedback available to the agents in
online optimization algorithms such as bandit or gradient feedback.

Real-world implementations of learning pricing agents are best modeled with bandit feedback. This means that
the feedback consists of a pointwise evaluation of the payoff function at the chosen action: _ft_ ˆ= ut(at). For
example, after setting a price in an oligopoly competition, an agent observes a specific profit in the next period.
They often have no or only incomplete information about the demand model or the strategies used by all other
sellers. This is particularly true on large online retail platforms where there are many substitutes for a good.

[3https://towardsdatascience.com/dynamic-pricing-with-multi-armed-bandit-learning-by-doi](https://towardsdatascience.com/dynamic-pricing-with-multi-armed-bandit-learning-by-doing-3e4550ed02ac)
```
ng-3e4550ed02ac, https://www.griddynamics.com/blog/dynamic-pricing-algorithms

```

-----

In the stochastic or adversarial model, one can analyze the performance of an algorithm. The key characeristic
in this literature is regret, i.e. the difference between the cumulative payoff if the algorithm played the
best fixed price in hindsight and the cumulative payoff of the learning algorithm. For some online learning
algorithms the regret vanishes over time. These algorithms are also referred to as no regret algorithms. As an
example, Exponential Weights (or the Exp3 variant) is a well-known online learning algorithm that uses bandit
feedback and updates the weights associated with each action based on the cumulative reward observed for
that action. The algorithm then chooses actions with probabilities proportional to their weights. Exp3 is a no
regret algorithm in the adversarial model.

There are also academic articles using (deep) reinforcement learning algorithms for algorithmic pricing
(Rana and Oliveira 2014, Kastius and Schlosser 2022, Deng et al. 2024). Different from the online learning
algorithms discussed so far, reinforcement learning algorithms allow the agent to take into account the state
of a system. This state could be historical prices, the day of the week, or other variables that are potentially
relevant. With an increasing state and action space, learning requires a lot of training rounds and doesn’t scale
well. Interestingly, the most prevalent reinforcement learning algorithm in the algorithmic collusion literature
is Q-learning. However, in related articles, the state space is limited to the current price, letting the algorithm
resemble an online learning algorithm. Yet, Lambin (2024) shows that algorithmic collusion can arise with
Q-learning even in a stateless version of Q-learning.

**2.2** **Algorithmic Collusion**

While the literature on online learning gives us methods to find optimal strategies in stochastic or even
adversarial settings, it does not capture the interaction of multiple agents using such algorithms (see Figure 1).
The literature on algorithmic collusion attempts to fill this gap and has attracted considerable attention from
the research community and policymakers.

(a) Online Learning (b) Equilibrium Learning

Figure 1: Learning Agents in Different Contexts

In the classical online learning setting, a single agent selects actions and observes stochastic (or adversarial) payoffs.
By contrast, algorithmic collusion studies the outcomes when multiple agents interact using online learning algorithms.
Understanding the results of these multi-agent learning processes requires consideration of the algorithm, but also of the
structure and properties of the underlying game, which is analyzed in equilibrium learning.

Most of this literature analyzes specific algorithms such as Q-learning for specific model variations, i.e.,
Bertrand oligopolies with standard all-or-nothing demand, linear, or logit demand. Calvano et al. (2020)
analyzed a Bertrand competition with logit demand and constant marginal cost. They found that when all
agents employ Q-learning, the competition of these agents can lead to supra-competitive prices higher than the
Nash equilibrium. A related sequential move pricing duopoly environment with linear demand (instead of the
simultaneous move Bertrand model in Calvano et al. (2020)) was analyzed by Klein (2021), who also found
collusion with Q-learning agents. Asker et al. (2022) detected in their experiments on Bertrand competition
with standard (all-or-nothing) demand that collusion depends on specifics of the Q-learning algorithm (e.g.,
synchronous vs. asynchronous updating).

In contrast, Abada et al. (2024b) analyzed Q-learning in Bertrand oligopolies and showed that Q-learning
algorithms with sufficiently large ϵ-greedy exploration exhibit no collusion. den Boer et al. (2022) provided a


![](raw/research/dynamic-pricing-landscape/assets/arxiv-algorithmic-collusion/arxiv-algorithmic-collusion.pdf-4-0.png)

-----

detailed analysis of the inner workings of Q-learning and argue that Q-learning would not lead to collusion
easily. In addition, Eschenbaum et al. (2022) criticized the claim that algorithms can be trained offline to
successfully collude online in different market environments. The authors found that collusion breaks down
when collusive reinforcement learning policies are extrapolated from a training environment to the market.
While most of this experimental literature on algorithmic collusion is based on Q-learning, there is little
evidence that this algorithm is particularly important or widespread for algorithmic pricing. More recently,
Hansen et al. (2021) analyzed the price levels that arise in a duopoly setting where agents based on the UCB
("Upper Confidence Bound") algorithm determine prices. They ran a series of experiments where a variant of
symmetric UCB algorithms interact simultaneously in a Bertrand economy competition with linear demand
functions. The agents observed a perturbed estimate of their revenues which are a result of their prices and
the corresponding demand. Hansen et al. (2021) found that sometimes agents explore prices in a correlated
manner, giving rise to supra-competitive outcomes.

The literature on algorithmic collusion in Information Systems is still scarce. Kang et al. (2022) and Douglas
et al. (2024) analyze the possibility of collusion in a repeated Prisonner’s Dilemmata. Deng et al. (2024)
discuss deep reinforcement learning in a repeated Bertrand competition, while Bichler et al. (2024) analyze
the phenomenon in the context of display advertising auctions.

Online learning algorithms address problems where agents optimize against an unknown and independent
stochastic process. However, game-theoretical problems such as the Bertrand competition differ because
each player’s actions impact the objectives of others. In games, the Nash equilibrium (NE) represents a
situation where no agent has an incentive to unilaterally deviate. Note that this is different from the adversarial
setting in optimization discussed earlier, because each agent aims to maximize his payoff. If agents are not
in equilibrium, then individual agents have an incentive to deviate from the current strategy profile, and the
outcome is not stable. Independently, one might ask if the equilibrium reached maximizes welfare.

**2.3** **Learning in Games**

Although, the term algorithmic collusion is relatively new, the topic is related to a long standing stream of
literature in game theory. Actually, the question if learning agents converge to a Nash equilibrium in repeated
play is as old as the concept of the Nash equilibrium itself (Brown 1951). Actually, even Cournot’s study of
duopoly competition via quantity (Cournot 1838) already introduced a particular learning process. However,
when learning algorithms converge to the Nash equilibrium and which properties they need to possess, is still
not fully resolved (Young 2010, Cesa-Bianchi and Lugosi 2006).

Research on learning in games (Young 2010, Foster and Vohra 1997) has shown that not all games can be
learned (Hart and Mas-Colell 2006, Milionis et al. 2022): learning dynamics may cycle, diverge, or be chaotic
(Mertikopoulos et al. 2018, Bailey and Piliouras 2018). While there is no comprehensive characterization
of games that are “learnable”, there are some important results regarding learners. A classical result is that
the class of no-regret learning algorithms converges to the so-called coarse correlated equilibrium (CCE) of
a game Fudenberg and Levine (1999). CCEs are superclasses of Nash equilibria. However, CCEs can also
contain dominated strategies and the set of CCEs in a game can be very large. For the analysis of algorithmic
collusion, we want to understand whether learning algorithms converge to a Nash equilibrium.

Less is known about conditions of games in which learning algorithms converge to a Nash equilibrium.
Monderer and Shapley (1996) introduced the class of potential games, and they showed that Cournot oligopolies
with linear price or cost functions are potential games. Potential games are guaranteed to have at least one pure
Nash equilibrium. Importantly, it was shown that several bandit algorithms converge to a Nash equilibrium in
potential games (Palaiopanos et al. 2017, Cohen et al. 2017). However, while Cournot oligopoly models are
potential games, this property rarely holds in other economic games.

Another central condition for which positive results are known is that of the (payoff) monotonicity of a game.
Games that admit a strictly concave potential are strictly monotone (Mertikopoulos and Zhou 2019). Games
that satisfy this condition have a unique Nash equilibrium. It is known that simple algorithms such as projected
gradient ascent converge to an equilibrium of strictly monotone games (Dong et al. 2018). Yet, the class of
games that are strictly monotone is rather restricted.


-----

Overall, the class of games for which learning algorithms converge to a Nash equilibrium is not well understood.
More specifically, not much is known about properties of Bertrand competition models that would guarantee
convergence to a Nash equilibrium. Note that each demand model assumed in the Bertrand competition model
leads to a different game and thus might have different convergence properties.

#### 3 Implications for BISE Research

A lot of the research in BISE and more broadly in the economic sciences aims to understand human behavior
in certain market interactions. Electronic markets have been a central research topic in BISE for many years
(Malone et al. 1987, Schmid 2000, Bichler et al. 2010). More and more markets are automated with learning
agents, and we need to understand if these markets are in equilibrium and if they lead to efficient outcomes.
These questions are not new, but the presence of learning algorithms is.

Figure 2: Overview of BISE Research Opportunities

Pricing agents on retail platforms such as Amazon are an example, and so are display ad auctions. The
question of how these agents interact and what outcomes they produce is of great interest to researchers and
policymakers. Does the use of learning algorithms in pricing lead to efficient equilibrium outcomes or does it
jeopardize consumer welfare by leading to algorithmic collusion? Algorithmic collusion challenges traditional
theories that assume firms cannot sustain collusive arrangements without explicit coordination. The question
has implications on policy, competition law, and the development of responsible algorithmic practices in
pricing. In what follows, we discuss a variety of research questions that the BISE community is well-equipped
to address. We provide a short overview in Figure 2.

**Algorithms** A key question in the study of algorithmic collusion is determining which types of algorithms
are more prone to collusive behavior. This inquiry involves examining specific properties of pricing algorithms
that may influence their tendency to collude. Additionally, the assumptions within game-theoretical models
can affect how different algorithms converge to equilibrium: some model setups may facilitate collusive
outcomes for certain algorithms, while others may not. Although there are initial findings on Q-learning and
some bandit algorithms within specific Bertrand competition models, a comprehensive understanding of these
dynamics constitutes a wide open research question.

The type of feedback an algorithm receives significantly impacts its potential for collusion. Algorithms
with bandit feedback, receiving only information on the outcomes of their own actions, are likely to behave
differently than those which can access more information about the environment or competitors’ actions.
State-based information, like historical prices or observed demand patterns, can further enhance an algorithm’s
capacity to predict optimal prices, potentially leading to tacit collusion. Research is needed examining how
different levels of information influence the emergence of collusive strategies.


![](raw/research/dynamic-pricing-landscape/assets/arxiv-algorithmic-collusion/arxiv-algorithmic-collusion.pdf-6-0.png)

-----

**Detection** Detecting algorithmic collusion presents a major challenge for regulators because price patterns
resulting from collusion can closely resemble those from equilibrium strategies, especially in dynamic markets.
Statistical methods might help to identify pricing patterns that may indicate collusion (Bonjour et al. 2022).
Another area of focus is the development of algorithms trained to recognize subtle signals of collusion, such as
price matching or retaliatory price adjustments (Xu et al. 2024). Effective detection methods could play a key
role in helping regulators monitor and address collusive pricing practices on digital platforms.

**Regulations & Monitoring** Even if a competition authority were to identify a potential case of tacit collusion,
the current state of the law could make such practice irreproachable in the absence of explicit communication
or contact among the companies using such autonomous algorithms. Existing competition laws often focus on
explicit, human-driven collusion rather than implicit algorithmic cooperation. New regulatory frameworks
may be necessary to address algorithmic behaviors that lead to collusive outcomes, even without direct
communication between firms. The OECD and other regulators are aware of shortcomings of the existing
legislation, and several calls to action have been made for policy changes to address this potential enforcement
gap (OECD 2024). For example, the European Commission’s revised guidelines on horizontal cooperation
agreements, adopted in 2023, stipulate that an explicit agreement among competitors to use the same pricing
algorithm is considered an infringement of article 101 of the Treaty on the Functioning of the European Union.
Note that this action addresses a different form of collusion where several firms use the same third-party
pricing software to determine their prices. This may result in a hub-and-spoke situation that can facilitate
information exchanges in the context of an agreement or concerted practice (OECD 2024). This is different
from the type of algorithmic collusion we discuss in this paper, where firms use their own pricing algorithms
and learn to collude without explicit communication. We need to understand alternative means of detecting and
preventing algorithmic collusion such as transparency requirements, restrictions on certain types of algorithms,
or real-time monitoring tools.

**Accountability** Algorithmic accountability can play an important role in this context (Horneber and Laumer
2023). The concept refers to the responsibility of organizations and individuals to ensure that algorithms
operate fairly, transparently, and ethically. In particular, transparency in algorithmic design could be an
important tool in minimizing the risk of collusion. Transparency assumes center stage in the Preventing
Algorithmic Collusion Act of 2024,[4] a bill that has been introduced in the US Senate. Transparency is also an
important aspect of the European Union’s Digital Markets Act (DMA)[5] and the Digital Services Act (DSA),[6]

although they do not yet address algorithmic collusion. By establishing design guidelines that discourage
collusive strategies or by requiring algorithms to be transparent in their decision-making processes, firms may
be able to mitigate unintended collusive behavior. Research might explore how different levels of transparency
and design constraints affect algorithmic behavior and whether greater openness among algorithms would
reduce or inadvertently increase the likelihood of collusion. Ultimately, the research in this field might
lead to rules that can be implemented in regulatory audits and compliance tests. Firms might be asked to
disclose their use of pricing algorithms and ensure that these tools are designed to comply with antitrust laws.
Such measures aim to create an environment where algorithmic behaviors are subject to scrutiny, thereby
discouraging collusive outcomes (Beneke and Mackenrodt 2021). It is crucial to understand the regulatory
measures needed to effectively minimize the risk of algorithmic collusion.

**Beyond** **oligopoly** **competition** While the focus of research on algorithmic collusion is on traditional
oligpoloy models, there is no reason to believe that the phenomenon can only arise there. Bichler et al. (2024)
analyzed display advertising auctions which are known to be automated via learning agents. Some recent
research also explores algorithmic collusion in platform competition models such as that for ride-hailing
or video streaming (Bichler et al. 2025). Pricing of platforms on two-sided markets has drawn substantial
attention in the BISE literature and the impact of algorithmic pricing describes a natural extension of this
research (Dou and Wu 2021, Constantinides et al. 2018, Parker et al. 2016).

[4https://www.congress.gov/bill/118th-congress/senate-bill/3686/text](https://www.congress.gov/bill/118th-congress/senate-bill/3686/text)
[5https://digital-markets-act.ec.europa.eu/](https://digital-markets-act.ec.europa.eu/)
[6https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/europe-fit-digit](https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/europe-fit-digital-age/digital-services-act_en)
```
al-age/digital-services-act_en

```

-----

A central question in the economic sciences has long been under which conditions efficient outcomes can be
achieved with market mechanisms. The welfare theorems provide conditions for a competitive equilibrium to
exist that is Pareto efficient (Varian 2014). Over decades, the game-theoretical literature identified conditions
under which efficient outcomes can be expected in equilibrium. Game theory highlights the role of incentives
and strategic interaction in markets, and the Nash equilibrium assumes center stage. In game theory, agents are
assumed to have enough information and that they can derive Nash equilibrium strategies that they use from
the start.

On real-world markets, agents often don’t have the required information to derive an equilibrium, and even if
they had, the equilibrium problem is computationally hard in general (Daskalakis et al. 2009). Importantly,
agents don’t have the information necessary about their competitors costs or values to derive an equilibrium.
This is why on automated markets, agents rely on learning algorithms, exploring various prices, and exploiting
the information gained over time. There is limited understanding of the circumstances under which such
repeated interactions among such learning agents yield efficient outcomes. However, this understanding is
important to understand the outcomes of algorithmic pricing in online retail markets. Gaining insights into
these algorithmic markets represents an important and fundamental challenge.

The BISE community has long analyzed electronic markets. The event of learning algorithms in this market
is more than a detail. It is fundamental that we understand how such learning agents impact the outcome
of markets and whether such algorithmic markets can be expected to be efficient. This requires technical
understanding of learning algorithms as well as the economic principles of market institutions. As such, the
Business & Information Systems Engineering community is well equipped to address this challenging and yet
hardly understood phenomenon.

#### Acknowledgments

This project was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) GRK 2201/2 - Project Number 277991500 and BI 1057/9.

#### References

Abada I, Harrington Jr JE, Lambin X, Meylahn JM (2024a) Algorithmic collusion: Where are we and where should we be
going? _Available at SSRN 4891033 ._
Abada I, Lambin X (2023) Artificial Intelligence: Can Seemingly Collusive Outcomes Be Avoided? _Management Science_
69(9):5042–5065.
Abada I, Lambin X, Tchakarov N (2024b) Collusion by mistake: Does algorithmic sophistication drive supra-competitive
profits? _European Journal of Operational Research 318(3):927–953._
Asker J, Fershtman C, Pakes A (2022) Artificial intelligence, algorithm design, and pricing. AEA Papers and Proceedings,
volume 112, 452–56.
Assad S, Clark R, Ershov D, Xu L (2024) Algorithmic pricing and competition: Empirical evidence from the german retail
gasoline market. Journal of Political Economy 132(3):723–771.
Bailey JP, Piliouras G (2018) Multiplicative weights update in zero-sum games. Proceedings of the 2018 ACM Conference
_on Economics and Computation, 321–338._
Bauer J, Jannach D (2018) Optimal pricing in e-commerce based on sparse and noisy data. Decision Support Systems
106:53–63.
Beneke F, Mackenrodt MO (2021) Remedies for algorithmic tacit collusion. Journal of Antitrust Enforcement 9(1):152–176.
Bertrand J (1883) Book review of theorie mathematique de la richesse social and of recherches sur les principes mathematiques de la theorie des richesses. Journal des Savants .
Bichler M, Buergermeister J, Schiffer M (2025) Predatory pricing in two-sided markets: An equilibrium learning approach.
_ArXiV_ .
Bichler M, Fichtl M, Oberlechner M (2023) Computing Bayes–Nash Equilibrium Strategies in Auction Games via
Simultaneous Online Dual Averaging. Operations Research .
Bichler M, Gupta A, Ketter W (2010) Research commentary—designing smart markets. Information Systems Research
21(4):688–699.
Bichler M, Gupta A, Mathews L, Oberlechner M (2024) Low revenue in display ad auctions: Algorithmic collusion vs.
non-quasilinear preferences. Conference on Information Systems and Technology .


-----

Bonjour T, Aggarwal V, Bhargava B (2022) Information theoretic approach to detect collusion in multi-agent games.
_Uncertainty in Artificial Intelligence, 223–232 (PMLR)._

Brackmann C, Wulfert T, Busch J, Schütte R (2024) The art of retail pricing: Developing a taxonomy for describing
pricing algorithms. European Conference on Information Systems .

Brown GW (1951) Iterative solution of games by fictitious play. Activity Analysis of Production and Allocation 13(1):374–
376.

Brown ZY, MacKay A (2023) Competition in Pricing Algorithms. _American_ _Economic_ _Journal:_ _Microeconomics_
15(2):109–156.

Bubeck S (2011) Introduction to Online Optimization.

Calvano E, Calzolari G, Denicolò V, Pastorello S (2020) Artificial Intelligence, Algorithmic Pricing, and Collusion.
_American Economic Review 110(10):3267–3297._

Calvano E, Calzolari G, Denicolò V, Pastorello S (2019) Algorithmic Pricing What Implications for Competition Policy?
_Review of Industrial Organization 55(1):155–171._

Cesa-Bianchi N, Lugosi G (2006) Prediction, learning, and games (Cambridge University Press).

Chen L, Mislove A, Wilson C (2016) An empirical analysis of algorithmic pricing on amazon marketplace. Proceedings of
_the 25th International Conference on World Wide Web, 1339–1349, WWW ’16 (International World Wide Web_
Conferences Steering Committee).

Cohen J, Heliou A, Mertikopoulos P (2017) Learning with bandit feedback in potential games. _Advances_ _in_ _Neural_
_Information Processing Systems 30._

Constantinides P, Henfridsson O, Parker GG (2018) Introduction—platforms and infrastructures in the digital age.
_Information Systems Research 29(2):381–400._

Cournot AA (1838) Recherches sur les principes mathématiques de la théorie des richesses (L. Hachette).

Daskalakis C, Goldberg PW, Papadimitriou CH (2009) The complexity of computing a nash equilibrium. SIAM Journal on
_Computing 39(1):195–259._

den Boer AV (2015) Dynamic pricing and learning: Historical origins, current research, and new directions. Surveys in
_Operations Research and Management Science 20(1):1–18._

den Boer AV (2023) Algorithmic Collusion: A Mathematical Definition and Research Agenda for the OR/MS Community.
_Available at SSRN 4636488 ._

den Boer AV, Meylahn JM, Schinkel MP (2022) Artificial Collusion: Examining Supracompetitive Pricing by Q-Learning
Algorithms. Available at SSRN 4213600 .

Deng S, Schiffer M, Bichler M (2024) Algorithmic collusion in dynamic pricing with deep reinforcement learning.
_Proceedings of Wirtschaftsinformatik 2024 ._

Dong QL, Cho Y, Zhong L, Rassias TM (2018) Inertial projection and contraction algorithms for variational inequalities.
_Journal of Global Optimization 70:687–704._

Dou Y, Wu D (2021) Platform competition under network effects: Piggybacking and optimal subsidization. Information
_Systems Research 32(3):820–835._

Douglas C, Provost F, Sundararajan A (2024) Naive algorithmic collusion: When do bandit learners cooperate and when
do they compete? _[arXiv preprint arXiv:2411.16574 .](http://arxiv.org/abs/2411.16574)_

Elreedy D, Atiya AF, Shaheen SI (2021) Novel pricing strategies for revenue maximization and demand learning using an
exploration–exploitation framework. Soft Computing 25(17):11711–11733.

[Eschenbaum N, Mellgren F, Zahn P (2022) Robust algorithmic collusion. arXiv preprint arXiv:2201.00345 .](http://arxiv.org/abs/2201.00345)

Foster DP, Vohra RV (1997) Calibrated learning and correlated equilibrium. Games and Economic Behavior 21(1-2):40.

Fudenberg D, Levine DK (1999) The Theory of Learning in Games, volume 2 of MIT Press Series on Economic Learning
_and Social Evolution (Cambridge:_ MIT Press), 2. edition, ISBN 978-0-262-06194-0.

Fügener A, Grahl J, Gupta A, Ketter W (2021) Will humans-in-the-loop become borgs? merits and pitfalls of working
with ai. Management Information Systems Quarterly (MISQ)-Vol 45.

Hansen KT, Misra K, Pai MM (2021) Frontiers: Algorithmic Collusion: Supra-competitive Prices via Independent
Algorithms. Marketing Science 40(1):1–12.

Hart S, Mas-Colell A (2006) Stochastic uncoupled dynamics and nash equilibrium. _Games_ _and_ _economic_ _behavior_
57(2):286–303.

Horneber D, Laumer S (2023) Algorithmic Accountability. Business & Information Systems Engineering 65(6):723–730.

Kang S, Kim MH, Kim K (2022) Raising skepticisms on the feasibility of algorithmic tacit collusion. _International_
_Conference on Information Systems ._


-----

Kasa SR, Rajan V (2021) Dependency modeling with copulas in multi-armed bandits. _International_ _Conference_ _on_
_Information Systems ._

Kastius A, Schlosser R (2022) Dynamic pricing under competition using reinforcement learning. Journal of Revenue and
_Pricing Management 21(1):50–63._

Klein T (2021) Autonomous algorithmic collusion: Q-learning under sequential pricing. The RAND Journal of Economics
52(3):538–558.

Lambin X (2024) Less than meets the eye: simultaneous experiments as a source of algorithmic seeming collusion.
_Available at SSRN 4498926 ._

Lu T, Zhang Y (2024) 1+ 1> 2? information, humans, and machines. Information Systems Research .

Lysyakov M, Viswanathan S (2023) Threatened by ai: Analyzing users’ responses to the introduction of ai in a crowdsourcing platform. Information Systems Research 34(3):1191–1210.

Malone TW, Yates J, Benjamin RI (1987) Electronic markets and electronic hierarchies. Communications of the ACM
30(6):484–497.

Maschler M, Zamir S, Solan E (2020) Game theory (Cambridge University Press).

Maskin E, Tirole J (1988) A theory of dynamic oligopoly, i: Overview and quantity competition with large fixed costs.
_Econometrica:_ _Journal of the Econometric Society 549–569._

Mertikopoulos P, Papadimitriou C, Piliouras G (2018) Cycles in adversarial regularized learning. _Proceedings_ _of_ _the_
_twenty-ninth annual ACM-SIAM symposium on discrete algorithms, 2703–2717 (SIAM)._

Mertikopoulos P, Zhou Z (2019) Learning in games with continuous action sets and unknown payoff functions. Mathemati_cal Programming 173(1-2):465–507._

Milionis J, Papadimitriou C, Piliouras G, Spendlove K (2022) Nash, conley, and computation: Impossibility and incom[pleteness in game dynamics. arXiv preprint arXiv:2203.14129 120(41):e2305349120.](http://arxiv.org/abs/2203.14129)

Monderer D, Shapley LS (1996) Potential games. Games and economic behavior 14(1):124–143.

Mueller JW, Syrgkanis V, Taddy M (2019) Low-rank bandit methods for high-dimensional dynamic pricing. Advances in
_Neural Information Processing Systems 32._

OECD (2017) Algorithms and Collusion: Competition Policy in the Digital Age. Technical report, OECD.

OECD (2024) Algorithms competition. Technical report, OECD.

Palaiopanos G, Panageas I, Piliouras G (2017) Multiplicative weights update with constant step-size in congestion games:
Convergence, limit cycles and chaos. Advances in Neural Information Processing Systems, volume 30 (Curran
Associates, Inc.).

Parker GG, Van Alstyne MW, Choudary SP (2016) Platform revolution: _How networked markets are transforming the_
_economy and how to make them work for you (WW Norton & Company)._

Qu J (2024) Survey of dynamic pricing based on multi-armed bandit algorithms. Applied and Computational Engineering
37:160–165.

Rana R, Oliveira FS (2014) Real-time dynamic pricing in a non-stationary environment using model-free reinforcement
learning. Omega 47:116–126.

Rothschild M (1974) A two-armed bandit theory of market pricing. Journal of Economic Theory 9(2):185–202.

Schmid BF (2000) Elektronische märkte. Handbuch Electronic Business: _Informationstechnologien—Electronic Com-_
_merce—Geschäftsprozesse 179–207._

Shalev-Shwartz S (2011) Online Learning and Online Convex Optimization. _Foundations_ _and_ _Trends®_ _in_ _Machine_
_Learning 4(2):107–194._

Taywade K, Goldsmith J, Harrison B, Bagh A (2023) Multi-armed Bandit Algorithms for Cournot Games. Under review.

Trovo F, Paladino S, Restelli M, Gatti N, et al. (2015) Multi-armed bandit for pricing. Proceedings of the 12th European
_Workshop on Reinforcement Learning, 1–9._

Varian HR (2014) Intermediate microeconomics with calculus: _a modern approach (WW norton & company)._

Waltman L, Kaymak U (2008) Q-learning agents in a cournot oligopoly model. _Journal_ _of_ _Economic_ _Dynamics_ _and_
_Control 32(10):3275–3293._

Xu YE, Ling CK, Fang F (2024) Learning coalition structures with games. _Proceedings_ _of_ _the_ _AAAI_ _Conference_ _on_
_Artificial Intelligence, volume 38, 9944–9951._

Young HP (2010) Strategic learning and its limits. Number 2002 in The Arne Ryde memorial lectures (Oxford Univ. Pr),
repr edition.


-----

