---
url: "file:///tmp/pdf-cache/hbs-dynamic-pricing-harm.pdf"
title: "I"
captured_on: "2026-04-21"
capture_method: "pdf"
engine: "pymupdf"
---

**Working Paper 22-050**

## Dynamic Pricing Algorithms, Consumer Harm, and Regulatory Response

#### Alexander J. MacKay Samuel N. Weinstein


-----

### Dynamic Pricing Algorithms, Consumer Harm, and Regulatory Response

##### Alexander J. MacKay
Harvard Business School

##### Samuel N. Weinstein
Yeshiva University

**Working Paper 22-050**

Copyright © 2021, 2022 by Alexander J. MacKay and Samuel N. Weinstein.

Working papers are in draft form. This working paper is distributed for purposes of comment and discussion only. It may
not be reproduced without permission of the copyright holder. Copies of working papers are available from the author.


-----

##### DYNAMIC PRICING ALGORITHMS, CONSUMER
 HARM, AND REGULATORY RESPONSE

_Alexander J. MacKay[*] & Samuel N. Weinstein[*]_

_Pricing algorithms are rapidly transforming markets, from ride-sharing_
_apps, to air travel, to online retail. Regulators and scholars have watched_
_this development with a wary eye. Their focus so far has been on the po-_
_tential for pricing algorithms to facilitate explicit and tacit collusion. This_
_Article argues that the policy challenges pricing algorithms pose are far_
_broader than collusive conduct. It demonstrates that algorithmic pricing_
_can lead to higher prices for consumers in competitive markets and even in_
_the absence of collusion. This consumer harm can be initiated by a single_
_firm employing a superior pricing algorithm. Higher prices arise from the_
_automated nature of algorithms, impacting any market where firms price_
_algorithmically. Thus, pricing algorithms that are already in widespread_
_use may allow sellers to extract a massive amount of wealth from consum-_
_ers. Because this consumer harm arises even when firms do not collude,_
_antitrust law cannot solve the problem. This Article looks to the history_
_of pricing innovation in the early twentieth century to show how government_
_can respond when new pricing technologies and strategies disrupt markets._
_It argues for pricing regulation as a feasible solution to the challenges non-_
_collusive algorithmic pricing poses, and it proposes interventions targeted at_
_when and how firms set prices._

  - Assistant Professor of Business Administration, Harvard Business School.

  - Associate Professor of Law, Benjamin N. Cardozo School of Law. The authors thank
Jon Baker, Zach Brown, Louis Kaplow, Fiona Scott Morton, D. Daniel Sokol, Stewart Sterk,
Ramsi Woodcock, and the participants in the Thurman Arnold Project and Cardozo Junior
Faculty Workshops. The paper also benefitted from comments at the 2021 Inframarginalism
& Internet conference at the University of Kentucky Rosenberg College of Law and the 2021
National Business Law Scholars Conference at the University of Tennessee College of Law.


-----

##### DYNAMIC PRICING ALGORITHMS, CONSUMER
 HARM, AND REGULATORY RESPONSE

CONTENTS

INTRODUCTION ........................................................................................................ 1
I. PRICING ALGORITHMS IN PRACTICE ......................................................... 11
_A._ Function and Relevant Markets ....................................................... 12
_B._ Algorithms and Antitrust: Current Approaches ............................ 16
II. PRICING ALGORITHMS & COMPETITION: ECONOMIC THEORY ........... 20
_A._ Classic Oligopoly Models ................................................................. 20
_B._ Pricing Algorithms Change the Competitive Game ..................... 23
1. Frequency ..................................................................................... 24
2. Commitment ................................................................................ 26
_C._ Empirical Evidence ........................................................................... 30
III. POLICY RESPONSES ...................................................................................... 32

_A._ Antitrust & Pricing ............................................................................ 33
1. Predatory pricing ......................................................................... 34
2. Resale Price Maintenance ........................................................... 35
3. Price Discrimination: The Robinson-Patman Act ................. 36
_B._ Pricing Regulation .............................................................................. 36
1. Disruptive Pricing Technologies: Price Displays and

Discounting Strategies ................................................................ 37
2. Price Controls .............................................................................. 40
_C._ Regulating Algorithmic Pricing ........................................................ 42
1. Regulating Pricing Frequency .................................................... 43
2. Prohibiting Reliance on Rivals’ Prices ...................................... 47
3. Innovation Effects ...................................................................... 50
CONCLUSION ........................................................................................................... 55


-----

INTRODUCTION

magine you are a consumer shopping for over-the-counter allergy medicine online. A search for Allegra, a top brand, leads you to three popular
e-commerce websites. One offers a 15-pack of Allegra for $17, the second
charges $15 for the same pack, and the third asks $13.[1] All other aspects

# I

of the offers being equal, you are of course likely to choose the $13 price. You
are also likely to think your research paid off: you got the best deal available
and saved some money. The price differences among the retailers might suggest that, by purchasing the lowest-priced offering, you are buying at the “competitive price.” But how would you know? What if all three retailers are charging above the competitive price? If the retailers used pricing algorithms to set
their prices, it is quite possible that this is exactly what happened. Despite the
appearance of price competition, you, and every other purchaser of this medicine, paid a supracompetitive price. The retailers used their pricing algorithms
to extract wealth from you and your fellow consumers and shift it to themselves.

Pricing algorithms are becoming an increasingly common feature of many
markets.[2] Ride-sharing apps,[3] airlines,[4] and Amazon,[5] to name just a few examples, all rely on algorithms to set their prices dynamically. These algorithms are
computerized formulas that determine prices automatically based on a set of

1 These are the actual prices (rounded to the nearest dollar) for Allegra at three popular ecommerce websites as of July 6, 2021. All three websites offered free shipping.

2 _See, e.g., Ariel Ezrachi & Maurice Stucke, Artificial Intelligence & Collusion: When Computers_
_Inhibit Competition, 2017 ILL._ L. REV. 1775, 1780 (2017) (“Pricing algorithms dominate online
sales of goods . . . and are widely used in hotel booking, and the travel, retail, sport, and entertainment industries.”); Salil Mehra, Antitrust & the Robo-seller: Competition in the Time of Algorithms,
100 MINN. L. REV. 1323, 1324 (“[Computers’] rising power, plus the growing ubiquity of the
Internet, and increasingly sophisticated data-mining techniques have driven a rapid shift of
pricing decisions away from human-decisionmakers in favor of algorithms. . ..”).

3 _See_ _How Uber’s dynamic pricing model works, UBER_ BLOG, https://www.uber.com/enGB/blog/uber-dynamic-pricing/ (explaining the use of Uber’s dynamic pricing algorithm).

4 _See_ Tom Chitty, _This is how airlines price tickets, CNBC_ (Aug. 3, 2018),
https://www.cnbc.com/2018/08/03/how-do-airlines-price-seat-tickets.html (explaining that
airlines’ pricing decisions “are being made by an algorithm that adjusts fares by using information including past bookings, remaining capacity, average demand for certain routes and
the probability of selling more seats later”).

5 _See Julia Angwin & Surya Mattu, Amazon Says it Puts Customers First. But Its Pricing Algorithm_
_Doesn’t, PROPUBLICA_ (Sept. 20, 2016), https://www.propublica.org/article/amazon-says-itputs-customers-first-but-its-pricing-algorithm-doesnt (arguing that Amazon uses its “market
power and its proprietary algorithm to advantage itself at the expense of sellers and many
customers”).


-----

_DYNAMIC PRICING ALGORITHMS_

data inputs.[6] Pertinent data might include competitors’ prices, supply and demand conditions, day of the week, and even the personal characteristics of
individual purchasers.[7] The advent of pricing algorithms initially seemed to offer the hope of near-perfect competition in online markets. Algorithms give
firms the ability to react in real time to their rivals’ prices, theoretically sharpening price competition. Combined with the enhanced pricing visibility online
shopping offers consumers, pricing algorithms appeared poised to drive prices
down to the competitive level.[8] But this is not how the story has played out in
many markets.

Compared to traditional pricing methods, algorithms provide sellers with
significant advantages. Algorithms can analyze much greater volumes of information in setting prices than can human agents, lowering the cost of employing sophisticated pricing strategies.[9] And algorithms can react much more
quickly to changing market conditions than can human agents, allowing sellers
to set the most advantageous prices more of the time.[10]

While pricing algorithms offer significant benefits to sellers, they also raise
serious concerns about harm to consumers. In particular, scholars and policymakers worry that firms will employ pricing algorithms to raise prices. Indeed,

6 _See, e.g., Michal Gal, Algorithms as Illegal Agreements, 34 BERKELEY TECH._ L. J., 67, 77 (2019)
(“Algorithms are structured decision-making processes that automate computational procedures to generate decisional outcomes on the basis of data input.”).

7 _See, e.g., Joseph E. Harrington, Developing Competition Law for Collusion by Autonomous Artifi-_
_cial Agents, 14 J._ COMPETITION L. & ECON. 331, 341 (2018) (“A pricing algorithm encompasses
a pricing rule which assigns a price to each state,” where, for example, “a state could include
a firm’s cost, inventory, day of the week, and past prices.”).

8 _See, e.g., Jeremy Jones, The Internet: The Perfectly Competitive Market We’ve Been Waiting For_
(Oct. 10, 2018), https://www.youngresearch.com/researchandanalysis/retail/the-internetthe-perfectly-competitive-market-weve-been-waiting-for/ (“In economics, perfect competition is sometimes just a theory, but the Internet is bringing that theory closer to reality for
retail consumers.”).

9 _See, e.g., Gal, supra note 6 at 79 (arguing that a “main advantage of algorithms relates to_
their analytical sophistication” and “[a]dvances in data science [] enable[] algorithms to integrate numerous variables into their decisions[,]” which “provides a level of sophistication that
cannot be achieved by the human mind without substantial time and effort”).

10 _See, e.g., id. (“The most basic advantage [algorithms] offer is speed in collection, organi-_
zation, and analysis of data, enabling exponentially quicker decisions and reactions.”).

2


-----

_DYNAMIC PRICING ALGORITHMS_

current scholarship on pricing algorithms’ competitive impact has focused almost exclusively on enhanced risks of explicit[11] and tacit collusion,[12] which
harm consumers by raising prices and reducing output.

This Article breaks new ground by identifying a distinct form of consumer
harm that arises from the use of pricing algorithms in competitive markets,
analyzing the legal ramifications of this algorithmic harm, and proposing policy
responses. It builds on pioneering theoretical and empirical scholarship in economics by one the authors (MacKay) and Professor Zach Brown, which
demonstrates that competition among pricing algorithms allows firms to
charge consumers supracompetitive prices even in the absence of collusion.[13] These
effects are driven by standard features of algorithms that are already in widespread use, including at the largest online retailers, such as Amazon and
Walmart.com. Unlike algorithmic collusion, which requires some measure of
coordination among firms to raise prices, the harms we identify can be initiated
by a single firm employing a superior algorithm. Because it is likely to affect
most markets where prices are set algorithmically, this threat to consumer wellbeing is in some respects more serious than that posed by explicit or tacit al
11 The Department of Justice has already uncovered a scheme among rival firms to use
pricing algorithms to fix prices. _See Press Release, U.S. Dep’t of Justice, Antitrust Division,_
_Former E-Commerce Executive Charged with Price Fixing in the Antitrust Division’s First Online Market-_
_place Prosecution (April 6, 2015), https://www.justice.gov/opa/pr/former-e-commerce-execu-_
tive-charged-price-fixing-antitrust-divisions-first-online-marketplace (describing guilty plea in
case involving use of pricing algorithms to fix prices for the sale of posters on the Amazon
Marketplace). See also Harrington, supra note 7 at 360 (“If autonomous cars can navigate city
roads and traffic, is it that difficult to imagine autonomous artificial agents figuring out how
to collude? Can we really be so sure that collusion by autonomous artificial agents will never
be commonplace?”).

12 See, e.g., Ai Deng, What do We Know About Algorithmic Tacit Collusion?, 33 ANTITRUST 88,
88 (2018) (“There is growing experimental evidence that an algorithm can be designed to tacitly collude.”). Unlike price fixing, tacit collusion does not involve an explicit agreement among
competing firms. Instead, firms establish a collusive, supracompetitive price by observing
their rivals’ prices and reaching an unspoken understanding that any deviations from the collusive price will be met by immediate retaliatory price cuts. Pricing algorithms facilitate tacit
collusion by increasing the speed and reliability with which firms can observe and react to
rivals’ prices. See OECD, ALGORITHMS & COLLUSION: COMPETITION POLICY IN THE DIGITAL AGE 52 (2017) (“[B]y providing companies with powerful automated mechanisms to monitor prices, implement common policies, send market signals or optimise joint profits with
deep learning techniques, algorithms might enable firms to achieve the same outcomes of
traditional hard core cartels through tacit collusion.”).

13 _See Zach Y. Brown & Alexander MacKay, Competition in Pricing Algorithms, AM._ ECON. J.:
MICRO. (Forthcoming 2022), https://www.hbs.edu/ris/Publication%20Files/20067_21e2440e-751b-4d03-a5e7-653570aa1e75.pdf.

3


-----

_DYNAMIC PRICING ALGORITHMS_

gorithmic collusion, which require more stringent market conditions to be successful.[14] The legal means to address algorithms’ competitive price effects is
the central focus of this Article.

Pricing algorithms facilitate supracompetitive pricing in competitive markets in two ways. First, they allow some firms to update prices faster than
other firms. For example, a firm with an advanced pricing algorithm might be
able to re-price its goods every day or even multiple times per day, while a firm
with a less sophisticated algorithm might be able to re-price only once a week.
Typically, the firm with a faster algorithm will have a competitive advantage,
as it will be able to undercut the price of a rival without a commensurate response. The slower firm can perceive the ability of the faster firm to quickly
reduce prices as a threat, limiting its incentives to compete on price. The slower
firm will charge a price above the competitive level, understanding that it will
lose some customers to its faster rival. The faster rival then chooses a price
below its rival’s price yet above the competitive level, taking share from the
rival while also capturing supracompetitive margins. The result of this asymmet_ric frequency is that both firms will charge above the competitive price and con-_
sumers will pay more for goods than they did before.

A second way in which pricing algorithms lead to higher prices is through
a commitment to pre-specified pricing strategies. Algorithms typically encode
in software a set of instructions to update prices, and this software is used to
update prices many times before the instructions are changed. In this way, the
algorithm allows a firm to commit to a pricing strategy in advance. Just as a
faster algorithm provides a firm with a threat to undercut slower rivals, an
algorithm that can autonomously observe and react to competitors’ price
changes gives a firm an advantage relative to one that lacks this technology.
When firms with superior technology commit to this strategy, firms with inferior technology know that their rivals can be relied on to undercut their prices.
In this asymmetric commitment scenario, as with asymmetric frequency, all firms
will charge above the competitive price. In both scenarios, higher prices can
reduce output and total welfare in addition to generating consumer harm.

While the firms in these scenarios are charging supracompetitive prices, it
is important to emphasize that they are not colluding.[ 15] Collusion—explicit or

14 _See Ariel Ezrachi and Maurice E. Stucke, Sustainable and Unchallenged Algorithmic Tacit Col-_
_lusion, 17 N.W._ J. TECH. INTELLECTUAL PROPERTY 217, 226 (2020) (“Algorithmic tacit collusion . . . will not affect every (or even most) markets.”).

15 Professors Jonathan Baker and Joseph Farrell have identified a category of non-collusive
oligopoly conduct, what they term “nonpurposive conduct,” that can result in higher consumer prices. See Jonathan B. Baker & Joseph Farrell, Oligopoly Coordination, Economic Analysis,
_and The Prophylactic Role of Horizontal Merger Enforcement, 168_ PENN. L. REV. 1985, 1998 (2020)
(“When oligopolists respond to one another’s price changes in a natural business way, they
are engaged in nonpurposive strategic conduct. Although those reactions are not part of an
express scheme or an informal effort to develop a common understanding or deter price
4


-----

_DYNAMIC PRICING ALGORITHMS_

tacit—requires each firm to make short-run sacrifices for long-run gains. Antitrust enforcement against collusion is predicated on finding an agreement
among firms to encourage such short-run sacrifices. We focus instead on settings in which all firms act non-cooperatively to pursue their own rational selfinterest; therefore, no agreement is necessary. Further, key characteristics distinguish collusive regimes from algorithmic competition. In a market subject
to collusion, we would expect firms to charge similar prices and to engage in a
reward-punishment regime to discipline price-cutters.[16] Neither of these conditions are necessary, or even expected, in the markets we describe. Notably—
like in the allergy medicine example above—firms may be charging quite different prices, yet all prices are higher than what consumers would pay in a
competitive market.[17] Perhaps the most significant difference between algorithmic collusion and the model we describe here is that a single firm can initiate a cycle of consumer harm simply by employing a superior pricing algorithm. Several firms—Amazon included—already price using algorithms that
are superior to their rivals’ pricing technologies.

Moreover, an observer may naturally think that algorithms—which enhance the ability of firms to react to rivals’ prices—would intensify competition, but the reverse is true. These theoretical models indicate that the increasing use of pricing algorithms will lead to higher prices for consumers, even
when firms are unable to collude. This conclusion is buttressed by empirical
evidence showing that algorithmic pricing and asymmetric pricing frequency
are already leading to higher prices in certain e-commerce markets.[18]

This trend is concerning because algorithmic pricing is spreading quickly
throughout the economy.[19] In addition to the proprietary algorithms that firms

cutting, those predictable responses will generally affect oligopolists’ incentives and may well
discourage price-cutting.”).

16 _See, e.g., Harrington, supra note 7 at 336 (“Collusion is when firms use strategies that em-_
body a reward-punishment scheme which rewards a firm for abiding by the supracompetitive
outcome and punishes it for departing from it.”).

17 Brown & MacKay, _supra_ note 13 at 2 (finding average price differences for identical
products exceeding 25 percent between the firm with the fastest algorithm and those with the
slowest).

18 _See id. (reporting findings from empirical study tracking the pricing of five online retailers_
of over-the-counter allergy drugs and showing that variability in sophistication of pricing algorithms led to asymmetric pricing frequency, resulting in meaningful price increases above
the competitive level in that market).

19 _See OECD, supra note 12 at 3 (“[A] growing number of firms are using computer algo-_
rithms to improve their pricing models, customise services and predict market trends.”);
Emilio Calvano, Giacomo Calzolari, Vicenzo Denicolo & Sergio Pastorello, _Artificial Intelli-_
_gence, Algorithmic Pricing and Collusion, 110 AM._ ECON. R. 3267, 3267 (2020) (“Firms are increasingly adopting software algorithms to price their goods and services.”); Ivan Zhou, AI-Powered
_Dynamic_ _Pricing_ _is_ _Everywhere,_ SYNCEDREVIEW (Nov. 24, 2018), https://medium.com/syncedreview/ai-powered-dynamic-pricing-is-everywhere-4271a9939d11

5


-----

_DYNAMIC PRICING ALGORITHMS_

like airlines, ride-sharing companies, and hotel chains employ to set their
prices, there has been explosive growth in the development of third-party pricing algorithms that firms can purchase and use to set their pricing strategies.[20]
These developments are significantly affecting retail pricing, particularly in ecommerce.[21] Many of the third-party algorithms that firms use are targeted at
helping sellers win business on the Amazon Marketplace.[22] Already some empirical evidence has demonstrated that increasing numbers of merchants are
employing pricing algorithms on Amazon and that these merchants win more
sales than sellers using traditional pricing methods.[23]

When pricing technologies distort markets, what is the appropriate response? The remedy for explicit algorithmic collusion is obvious: antitrust
enforcement. Price fixing is per se illegal and a criminal offense under section

(“[A]lgorithmic dynamic pricing is transforming transportation, E-commerce, entertainment,
and a wide range of other industries.”).

20 _See_ COMPETITION AND MARKETS AUTHORITY, PRICING ALGORITHMS: ECONOMIC
WORKING PAPER ON THE USE OF ALGORITHMS TO FACILITATE COLLUSION AND PERSONALISED PRICING (2018), https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/746353/Algorithms_econ_report.pdf (“As well as simple
pricing rules provided by the platforms themselves, some third-party firms sell more sophisticated pricing algorithms to retailers or directly take on the role of pricing using computer
models on behalf of their clients.”); Le Chen, Alan Mislove, and Christo Wilson, An Empirical
_Analysis of Algorithmic Pricing on Amazon Marketplace, PROCEEDINGS OF THE_ 25[TH] INTERNATIONAL CONFERENCE ON WORLD WIDE WEB at 1339 (2016) (“Travel websites and large, well
known e-retailers have already adopted algorithmic pricing strategies, but the tools and techniques are now available to small-scale sellers as well.”).

21 _See, e.g., Chen, et al., supra note 21 at 1349 (noting that certain “algorithmic sellers change_
prices tens or even hundreds of times per day, which would be difficult for humans to maintain
over time. . . .”); Ilya Katsov, Algorithmic pricing, part 1: the risks and opportunities, GRID DYNAMICS
(Dec. 11, 2018), https://blog.griddynamics.com/algorithmic-pricing-part-i-the-risks-and-opportunities/ (“Algorithmic pricing technologies and the transparency of the Internet have had
a major impact on the pricing behavior of retailers and even the U.S. economy as a whole.”).

22 _See, e.g., Amazon repricing features that get you the Buy Box, REPRICER.COM,_ https://www.repricer.com/features (promotional material from a third-party algorithm software vendor
promising that users can “[c]ompete on Amazon your way with flexible, targeted rules.”); Jessica Leber, Algorithmic Pricing is Creating an Arms Race on Amazon’s Marketplace, FAST COMPANY
(June 14, 2016), https://www.fastcompany.com/3060803/algorithmic-pricing-is-creating-anarms-race-on-amazons-marketplace (“In the last few years, some startups have made it easy
for even small sellers to use algorithmic pricing on Amazon’s marketplace with their own
custom criteria.”).

23 _See Chen, et al., supra note 21 at 1339 (describing dataset including sellers of around 1,600_
“best-seller products” on the Amazon Marketplace, identifying in that dataset “over 500”
sellers using algorithmic pricing, and concluding that such sellers are more successful than
non-algorithmic sellers).

6


-----

_DYNAMIC PRICING ALGORITHMS_

1 of the Sherman Act.[24] That rule should apply whether price fixing is agreed
upon and executed over the phone or through an algorithm. More challenging
cases arise when the algorithm is not explicitly programmed to collude and
does so on its own via communication with other algorithms. But in the standard case, human agents will have agreed to use their algorithms to fix prices
and Sherman Act liability will attach.

Tacit collusion is a more difficult problem to remedy. Because there is no
explicit agreement in a tacit collusion scenario, section 1 of the Sherman Act
would not apply under current law.[25] Scholars and policy makers have suggested expanding antitrust law to capture tacit collusion, for example, by
broadening what qualifies as an “agreement” for purposes of section 1, or,
more simply, by prohibiting tacit collusion altogether.[26] Regulation is another
possibility, including restrictions on how algorithms operate and direct price
regulation of markets subject to tacit collusion.[27]

The problem this Article addresses—non-collusive algorithmic pricing
leading to higher consumer prices—is likely both more common than explicit
or tacit collusion and more difficult to remedy. Because, by definition, we are
focusing on competitive markets where firms are not colluding, this conduct
is beyond the current reach of antitrust, even broadly defined. How can governments address new harms arising from technology that fall outside traditional bounds of enforcement? Regulation is one potential solution.

24 _See_ _Price Fixing, Bid Rigging, and Market Allocation Schemes, U.S. DEP’T OF_ JUSTICE,
http://www.justice.gov/sites/default/files/atr/legacy/2007/10/24/211578.pdf (“[P]rice fixing and bid rigging schemes are per se violations of the Sherman Act . . . and are subject to
criminal prosecution by the Antitrust Division of the United States Department of Justice.”).

25 _See In re Text Messaging Antitrust Litig., 782 F. 3d 867, 879 (7th Cir, 2015) (“Tacit col-_
lusion . . . does not violate Section 1 of the Sherman Act. Collusion is illegal only when based
on agreement.”). This situation is different in the European Union, where under section 102
of the Treaty of Functioning of the European Union (TFEU), liability for tacit collusion can
be characterized as an “abuse of dominance.” See Ariel Ezrachi & Maurice Stucke, Algorithmic
_Collusion: Problems & Countermeasures, ORGANISATON FOR ECONOMIC COOPERATION AND DE-_
VELOPMENT, DIRECTORATE FOR FINANCIAL AND ENTERPRISE AFFAIRS COMPETITION COMMITTEE note 61 (2017) (“Tacit collusion may serve to establish Collective Dominance under
Article 102 TFEU, but absent a separate abuse, it will also escape scrutiny under this provision.”).

26 _See, e.g., Gal, supra note 6 at 117 (arguing, in light of the threat of algorithmic tacit collu-_
sion, that “the time may be ripe to reconsider prohibiting any conduct with potential anticompetitive tendencies with no offsetting pro-competitive ones, even where such conduct does
not constitute an agreement in the traditional sense”).

27 _See, e.g., Ezrachi & Stucke, supra note 2 at 1806-07 (detailing options for responding to_
tacit algorithmic collusion, including “an ex ante approach by which, under certain market conditions, companies must report the use of certain algorithms” and “price regulation” powered
by “Big Data and Big Analytics”).

7


-----

_DYNAMIC PRICING ALGORITHMS_

Pricing regulation has a checkered reputation, at best, among economists
and policy makers.[28] But it remains a viable option when market conditions
warrant, and we argue that the consumer harm algorithmic pricing will cause
can be addressed by regulatory intervention. This would not be the first time
that advances in pricing technologies have triggered a regulatory response. In
the early twentieth century, price display innovations, including price cards and
price-card holders, led to a sea change in retail markets.[29] Suddenly, retailers
gained the ability to easily advertise prices to consumers and to change those
prices quickly by replacing a price or quantity card. These technologies led to
the development of new pricing strategies, including batch pricing (e.g., four
50 cent items for a dollar) and loss leaders.[30] Before this technological revolution, retailers set prices on an ad hoc basis for each buyer, based on the seller’s
costs and other variables.[31] Now, prices were the same for all buyers and comparison shopping became possible, forcing retailers for the first time to take
their rivals’ prices into account when setting price.[32] The result was a period of
intense price-cutting and deflation leading up to and during the Great Depression.[33]

Policy makers proposed several different market interventions to address
the deflationary effect of these pricing innovations, culminating in the industrial codes authorized by the National Industrial Recovery Act of 1933
(NIRA).[34] The NIRA permitted industry organizations to propose “codes of
fair competition,” which instituted price floors and restricted price cutting.[35]
Once approved by the federal government, these codes were exempted from
the antitrust laws.[36] A number of scholars have argued that the Roosevelt ad
28 _See, e.g., Hugh Rockoff,_ _Price Controls, THE CONCISE ENCYCLOPEDIA OF ECONOMICS_
(David R. Henderson ed.) (2008), https://www.econlib.org/library/Enc/PriceControls.html
(“[E]conomists are generally opposed to price controls.”).

29 _See Franck Cochoy, Johan Hagberg, and Hans Kjellberg,_ _The technologies of price display:_
_mundane retail price governance in the early twentieth century, 47 ECON._ & SOC. 572, 579-80 (2018)
(describing the development of “new price tag devices” in the 1920s and its effect on retail
pricing).

30 _Id. at 580-86._

31 _Id. at 577._

32 _Id. at 577-79._

33 _Id. at 574 (arguing that the implementation of price-cutting strategies after World War_
One “led to the development of price wars that worsened the effects of the Great Depression”).

34 National Industrial Recovery Act of 1933, Pub. L. 73-67 (1933).

35 _Id., Title 1, Section 3._

36 _Id.,_ Title 1, Section 5.

8


-----

_DYNAMIC PRICING ALGORITHMS_

ministration’s decision essentially to suspend the antitrust laws to control deflation was a mistake.[37] But this episode demonstrates how advances in pricing
technologies can destabilize markets and the potential for government to respond with broad price regulation.

While policy makers in the 1920s and 1930s were faced with pricing innovations that led to what they viewed as ruinous price cutting, current innovations in algorithmic pricing instead can result in significant price increases for
consumers. Any regulatory intervention would be aimed at forcing prices back
to competitive levels. One candidate is to use price controls to directly reduce
prices in markets subject to algorithmic pricing. We oppose this solution as
too disruptive, expensive, and overbroad. Price controls have proved in the
past to be ineffective over the long term and to lead to undesirable outcomes
like surpluses of goods whose price is set too high and shortages of goods
whose price is set too low.[38] Further, because the shift to algorithmic pricing
is a long-term trend that affects many different products, any price-control
regime would involve establishing a huge new bureaucracy and fundamentally
altering the relationship between the federal government and the market.

We advocate instead a more surgical intervention to promote competition:
using regulation to limit key features of algorithms, without requiring detailed
knowledge of the calculations that algorithms perform or what the competitive
price levels might be. The mechanisms by which pricing algorithms raise prices
even in the absence of collusion—asymmetric pricing frequency and commitment to react to rivals’ prices in a pre-specified way—suggest the forms this
regulation could take. One approach would be to prohibit asymmetric pricing
frequency by requiring firms to price at the same time and on the same schedule, say once a day at 6 am. This reform would eliminate the possibility of the
type of leader-follower conduct that results in all sellers in a market charging
supracompetitive prices. It would also be a relatively administrable reform
because it would not require a regulator to evaluate individual firms’ algorithms. The regulator’s task simply would be to ensure that firms are pricing
only at authorized times. A potential downside to this reform is that it would
prevent firms from reacting quickly to changes in market conditions. And it is
possible that requiring firms to price at the same time would make it easier for
firms to collude.[39]

37 _See, e.g., Christina Romer, Why did Prices Rise During the 1930s?, 59 J._ ECON. HISTORY 167,
197 (1999) (arguing that the NIRA “prevented the economy’s self-correction mechanism from
working” and that “the NIRA can best be thought of as a force holding back recovery.”).

38 _See Rockoff, supra note 29 (“Price ceilings, which prevent prices from exceeding a certain_
maximum, cause shortages. Price floors, which prohibit prices below a certain minimum,
cause surpluses, at least for a time.”).

39 _See Ralf Dewenter & Ulrich Heimeshoff,_ _Less Pain at the Pump? The Effects of Regulatory_
_Interventions_ _in_ _Retail_ _Gas_ _Markets_ 4 (2012), https://www.dice.hhu.de/filead
9


-----

_DYNAMIC PRICING ALGORITHMS_

A second option is a rule prohibiting firms from incorporating rivals’
prices into their algorithms. This intervention would prevent superior algorithms from automatically undercutting prices set by inferior algorithms, disrupting the leader-follower pattern that would otherwise develop. Further, it
would allow firms to re-price whenever and as often as they want, so firms
could react quickly to changes in market conditions (other than changes in
rivals’ prices). Algorithms still would have significant amounts of data to work
with, including supply and demand conditions, seasonal conditions, and customer characteristics.

This type of regulation would be more challenging to administer than rules
restricting when firms can set prices. To ensure compliance, a new bureaucracy
likely would have to be created to review each individual pricing algorithm.
Another drawback to this approach is that it may make it more difficult for
some firms to compete aggressively on price. In a healthy market, firms are
expected to compete on multiple fronts—including quality and product variety—but price competition is especially important.[40] Consumers typically benefit from this competition by paying less for their goods and services. Restrictions that limit automated responses therefore may be perceived as dulling
price competition. However, these restrictions are likely to have only shortrun effects on competition. Over longer periods, firms can adjust the parameters governing their algorithms to deliver lower price levels and compete more
effectively, without relying on automated responses to rivals’ prices.

One shared risk of these two regulatory regimes is that they might dull
incentives to innovate in algorithmic pricing. If firms are restricted from pricing more than once a day, for example, the incentive to produce faster algorithms is reduced. But if innovation in pricing algorithms harms consumers,
should we care about these dulled incentives? We think not. Pricing algorithms can harm consumers, even in competitive markets. They are what we
term an “extractive innovation.” Such innovations result in lower consumer
welfare—in this case, by raising prices without an increase in product quality,
as it is not clear that consumers receive any meaningful benefit from highfrequency price changes in online retail. Regulators’ approach to innovative

min/redaktion/Fakultaeten/Wirtschaftswissenschaftliche_Fakultaet/DICE/Discussion_Paper/051_Dewenter_Heimeshoff.pdf (describing experimental studies predicting that Austrian
and Western Australian retail gas pricing regulations that limit when firms are allowed to price
would increase the likelihood of collusion and lead to higher prices).

40 _See FED._ TRADE COMM’N, COMPETITION COUNTS: HOW CONSUMERS WIN WHEN BUSINESSES COMPETE 1 https://www.ftc.gov/sites/default/files/attachments/competitioncounts/zgen01.pdf (“Competition in America is about price, selection, and service. It benefits
consumers by keeping prices low and the quality and choice of goods and services high.”).
Economic theory predicts that, even with a restriction in place on incorporating rivals’ prices
in algorithms, sophisticated firms still would be able to attain competitive prices. But in practice such a restriction might cause some firms to raise prices.

10


-----

_DYNAMIC PRICING ALGORITHMS_

but dangerous products—flavored e-cigarettes that are targeted at young consumers, for example—provides a useful example of how to treat extractive
innovation: mitigate risks through targeted regulation.[41] In sum, when they
identify extractive innovations, courts, enforcers, and regulators should be less
concerned about policies that reduce related innovation incentives. Indeed,
they should consider ways to discourage additional innovative harm.

Both the potential interventions we consider—regulating when firms price
or how they price—have significant advantages and disadvantages. Today, requiring firms to adjust prices at the same time and at the same interval seems
the less intrusive, less expensive, and superior intervention for most markets
subject to algorithmic pricing competition. But that could change as pricing
technology develops and more empirical evidence about the effects of algorithmic pricing emerges.

The Article is presented in three Parts. Part I surveys the use of pricing
algorithms in practice, including how these algorithms work and the markets
in which they are currently being used. This Part also describes current scholarly approaches to algorithmic pricing, which focus almost exclusively on its
facilitation of explicit and tacit collusion. Part II applies game theory to describe the effects of pricing algorithms in competitive markets. It demonstrates
that algorithmic pricing will lead to supracompetitive prices even in the absence of collusion and it discusses empirical evidence of these effects. Part III
addresses potential policy responses to the consumer harm pricing algorithms
cause in competitive markets. This Part argues that there is no practical antitrust solution to this problem and that a regulatory response will be necessary.
It proposes and analyzes two regulatory approaches to the challenges pricing
algorithms pose: restricting when firms price and whether their algorithms can
incorporate competitors’ prices.

I. PRICING ALGORITHMS IN PRACTICE

Evaluating the scope and seriousness of the effects of algorithmic pricing
on consumers requires understanding how pricing algorithms currently operate in practice. To this end, this Part describes the different types of pricing
algorithms firms employ and the sectors where their effects are most likely to
be felt. It also surveys the growing body of scholarly literature on algorithmic
pricing.

41 _See_ U.S. DEP’T OF HEALTH & HUMAN SERVICES, FOOD & DRUG ADMIN., CTR. FOR
TOBACCO PRODUCTS, ENFORCEMENT PRIORITIES FOR ELECTRONIC NICOTINE DELIVERY
SYSTEMS (ENDS) AND OTHER DEEMED PRODUCTS ON THE MARKET WITHOUT PREMARKET
AUTHORIZATION (REVISED) (April 2020) (stating that the FDA intends to “prioritize enforcement against[] [f]lavored, cartridge-based ENDS products.”).

11


-----

_DYNAMIC PRICING ALGORITHMS_

_A._ Function and Relevant Markets

The use of pricing algorithms is exploding, particularly in e-commerce.[42]
While their sophistication varies, pricing algorithms all function in the same
general manner: they automatically apply a computerized rule to set prices
based on various inputs. These inputs commonly include demand for and
supply of specific products, competitors’ prices, customer demographics and
preferences, time of day, day of the week, and time of year.[43] Pricing algorithms
allow firms, particularly e-commerce firms, to quickly and continually update
and optimize their pricing.

Algorithmic pricing is not a new technology. The major airlines have used
pricing algorithms to set their prices for many years.[44] But the development
of Internet-based commerce and the advent of increasingly advanced computing equipment, combined with the availability of tremendous amounts of consumer data, have increased the power and reach of these algorithms. Many
sophisticated firms have developed their own proprietary pricing algorithms.
Uber and Lyft are well-known examples of companies whose business models
are based on algorithms that continually reprice in response to changes in demand and supply conditions.[45] These companies are able to take advantage of
the huge amounts of customer data they collect to adjust prices on the fly as
conditions warrant.[46] The airlines continue to use their proprietary pricing algorithms to finely adjust ticket prices for different routes, different days of the
week and times of day, and even for different travelers.[47] Hotel chains and

42 _See, e.g., Calvano, Calzolari, Denicolo & Pastorello, supra note 20 at 2 (“Firms are increas-_
ingly adopting software algorithms to price their goods and services.”); Zhou, _supra note 20_
(“[A]lgorithmic dynamic pricing is transforming transportation, E-commerce, entertainment,
and a wide range of other industries.”).

43 _See, e.g., Ezrachi & Stucke, supra note 2 at 1780 (“Pricing algorithms . . . [o]ptimize the_
price based on available stock and anticipated demand. . . .”); Harrington, supra note 7 at 341
(“A pricing algorithm encompasses a pricing rule which assigns a price to each state. For
example, a state could include a firm’s cost, inventory, day of the week, and past prices.”).

44 _See R. Preston McAfee & Vera te Velde, Dynamic Pricing in the Airline Industry, HANDBOOK_
ON ECONOMICS AND INFORMATION SYSTEMS 1 (T.J. Hendershot ed., 2007) (“The initial development of dynamically adjusted pricing is often credited to American Airlines’ Robert
Crandall, as a response to the rise of discount airline People’s Express in the early 1980s.”).

45 _See Zhou, supra note 20 (describing Uber’s and Lyft’s “real-time dynamic pricing” and_
how their algorithms respond to driver supply and customer demand data); UBER BLOG supra
note 3.

46 _See Zhou, supra note 20_ (“Uber and Lyft are evolving the [dynamic pricing] concept by
leveraging their massive data in real time.”).

47 _See David Krieghbaum Jr., Algorithms Take Flight: Modern Pricing Algorithms’ Effect on Anti-_
_trust Laws in the Aviation Industry, 32 LOY._ CONSUMER L. REV. 282, 289 (2020) (explaining that
airlines adjust their prices based on type of customer, “time of day and week,” and specific
route).

12


-----

_DYNAMIC PRICING ALGORITHMS_

rental car companies do the same.[48] Large online retailers like Walmart and
eBay also employ proprietary algorithms on their e-commerce platforms.[49]

Amazon, which is projected to surpass 50 percent of all e-commerce revenues in 2021,[50] employs a dynamic pricing algorithm for its products. Analysts
have asserted that Amazon changes its prices 2.5 million times a day.[51] Amazon’s pricing algorithm takes advantage of the company’s trove of customer
and competitor data, incorporating customer preferences, rivals’ prices, product supply, and many other criteria in setting prices.[52]

Amazon is an enormous company with the resources to develop a sophisticated algorithm. But firms no longer need to invest in creating their own
algorithms to take advantage of this pricing technology. Third-party vendors
sell pricing algorithms that even small firms can use to customize their pricing.[53] These third-party algorithms are transforming Internet retail, making it
much more likely that consumers will purchase products that algorithms have
priced. Companies like Repricer.com, 5Analytics, and Antuit provide off-theshelf algorithmic pricing tools for retailers.[54] Repricer.com promises that its
solution will allow sellers to “Beat competitors with super-fast repricing,”[55]
while Antuit claims that its strategic pricing tool will “build[] optimal list price

48 _See_ Atakan Kantarci, _Dynamic pricing: What it is, Why it matters & Top Pricing Tools, AI_
MULTIPLE (Aug. 23, 2020), https://research.aimultiple.com/dynamic-pricing/ (explaining the
use of dynamic pricing in the hospitality and car rental industries).

49 _See Suman Battacharyya, Pressured by Amazon, Retailers are Experimenting with Dynamic Pric-_
_ing, DIGIDAY (Feb. 21, 2019), https://digiday.com/retail/amazon-retailers-experimenting-dy-_
namic-pricing/ (“Walmart had to ‘change its religion’ of everyday low prices for dynamic pricing to compete with Amazon . . .”); (Shreya Raval, _eBay Makes Search More Efficient Through_
_Personalization, EBAY (JUNE 23,_ 2020) (describing eBay’s “efforts to enhance [its] machine learning algorithms to improve the quality of search results for each buyer,” and explaining eBay’s
“price propensity” feature, which “customize[s] the search results based on a user’s price preference” by taking into “consideration a user’s past purchases at eBay.”).

50 https://www.statista.com/statistics/788109/amazon-retail-market-share-usa/.

51 _See, e.g.,_ Neel Mehta, Parth Detroja, and Aditya Agashe, Amazon changes prices on its products
_about every 10 minutes – here’s how and why they do it, BUSINESS_ INSIDER (Aug. 10, 2018),
https://www.businessinsider.com/amazon-price-changes-2018-8.

52 _Id._

53 _See Chen, et al., supra note 21 at 1 (“[T]he tools and techniques” to adopt algorithmic_
pricing strategies “are now available to small-scale sellers as well.”).

54 _See_ Antuit.ai, _Dynamic Pricing, https://www.antuit.ai/dynamic-pricing (explaining the_
“Antuit Dynamic Pricing Advantage”); Repricer .com (“Join the 5,000+ retailers who trust
Repricer.com to automate pricing across 17 Amazon marketplaces.”); Tannistho, AI in Retail:
_of Chatbots, conversations and dynamic pricing, MEDIUM_ (Nov. 29, 2016), https://medium.com/@tannistho/ai-in-retail-of-chatbots-conversations-and-dynamic-pricingbf418ae3096c (describing the 5Analytics AI platform, “where shops can integrate dynamic
pricing into their existing systems via standard interfaces”).

55 Repricer.com.

13


-----

_DYNAMIC PRICING ALGORITHMS_

based on market competition, price/pack architecture, and market sensitivity.”[56]

Third-party providers offer various strategies or “modules” to customize
pricing algorithms. For example, a “key-value-items module” (KVI) focuses
on pricing those items that significantly affect customers’ general perception
of individual merchants.[57] If sellers can identify these key items and price them
appropriately, they can modify consumers’ overall view of their market competitiveness.[58] A “competitive-response module” focuses on varying prices in
response to real-time changes in rivals’ prices,[59] while an “elasticity module”
calculates the effects of prices on demand, taking into account seasonality and
other factors.[60] Firms also might employ an “omnichannel module,” which
coordinates pricing strategy among a merchant’s various distribution outlets,
including between on-line and brick-and-mortar sales channels.[61]

A significant part of the business of these third-party algorithm vendors is
helping companies win sales on the Amazon Marketplace. The Marketplace is
Amazon’s e-commerce platform, where independent merchants and Amazon
compete to make sales to end-users.[62] Third-party sellers pay Amazon various
fees to join the platform and to gain access to Amazon’s enormous customer
base.[63] Amazon offers these independent merchants a service called Selling
Partner API (SP-API) (formerly Amazon Marketplace Web Service “MWS”),
which allows them to interface with Amazon and automate their selling activities, including managing their listings, orders, and payments.[64] SP-API and

56 Antuit.ai/solutions/strategic-pricing.

57 _See, e.g., Kantarci, supra note 49 (providing overview of dynamic-pricing and describing_
key-value-items module); Mathias Kullmann & Stephen Zimmermann, _Dynamic Pricing in e-_
_Commerce, MCKINSEY_ & CO., https://www.mckinsey.com/business-functions/marketingand-sales/how-we-help-clients/dynamic-pricing (Introducing McKinsey’s dynamic-pricing
services and describing key-value-item module).

58 _See Kantarci, supra note 49; Kullmann & Zimmermann, supra note 58._

59 _See Kantarci, supra note 49; Kullmann & Zimmermann, supra note 58._

60 _See Kantarci, supra note 49; Kullmann & Zimmermann, supra note 58._

61 _See Kantarci, supra note 49; Kullmann & Zimmermann, supra note 58. Other standard_
modules include a “long-tail” module, which assists companies focused on selling limited volumes of hard-to-find items, and a “time-based pricing module,” which adjusts pricing based
on time of day items are bought, time of desired delivery, and product expiration dates. _See_
Kantarci, supra note 49; Kullmann & Zimmermann, supra note 58.

62 _See Chen, et al., supra note 21 at 1340 (describing the Amazon Marketplace)._

63 _See id. (describing the various fees third-party sellers are required to pay Amazon to do_
business on the Amazon Marketplace).

64 Amazon Selling Partner API Docs, What is Selling Partner API?,
https://github.com/amzn/selling-partner-api-docs/blob/main/guides/developerguide/SellingPartnerApiDeveloperGuide.md#what-is-the-selling-partner-api (“The Selling

14


-----

_DYNAMIC PRICING ALGORITHMS_

MWS also provide merchants with market price updates for their products.
Third-party pricing algorithms connect to Amazon’s APIs, enabling merchants
to automatically adjust their prices on the Marketplace.[65]

Algorithmic pricing appears to be having a significant impact on the Amazon Marketplace. A 2016 study by Le Chen, Alan Mislove, and Christo Wilson applied a methodology for detecting algorithmic pricing on the Marketplace.[66] Using data from four months of sales of more than 1,500 best-selling
products, the study identified 500 sellers employing algorithmic pricing on the
platform.[67] The authors found that merchants using pricing algorithms generally outperformed rivals that did not use this technology.[68] These merchants
received more customer feedback, which the authors concluded meant that
they had higher sales volumes, and they “won” the Amazon Buy Box more
frequently than their competitors, even when they did not offer the best price
for a specific product.[69] Winning the Buy Box is crucial, because over 80 percent of Amazon sales are made via the Buy Box.[70] This study and other similar
analyses show that Amazon consumers likely are subject to algorithmic pricing
for a growing portion of their purchases.

***

With its deep penetration into transportation services (Uber, airlines), hospitality (hotels), and e-commerce (Amazon and many other e-retailers), algorithmic pricing now touches the lives of most consumers. And its reach is only
going to spread, through expanded deployment in e-commerce but also in
physical retail, where the use of digital labelling technology will allow brickand-mortar merchants to change prices on the fly.[71]

Partner API helps Amazon sellers programmatically access their data on listings, orders, payments, reports, and more.”).

65 _See Chen, et al., supra note 21 at 1341, (algorithmic pricing “services enable any merchant_
to easily become a 3P seller and leverage sophisticated dynamic pricing strategies”).

66 _Id._

67 _Id. at 1339._

68 _Id. at 1340._

69 _Id. The Amazon “Buy Box” is the white box on the right side of each Amazon product_
page. The Buy Box includes a button that allows customers to purchase the product listed in
the Box. When multiple sellers offer a product, they compete to be featured in the Buy Box.

70 Eyal Lanxner, The Amazon Buy Box: How it Works for Sellers and Why It’s So Important,
BIGCOMMERCE, https://www.bigcommerce.com/blog/win-amazon-buy-box/ (“82% of
Amazon sales go through the Buy Box, and the percentage is even higher for mobile purchases.”).

71 _See, e.g., Zhou,_ _supra_ note 21 (noting that a German supermarket group already has
adopted digital labeling technology which allows it to make “instantaneous price changes to
hundreds of different products in thousands of stores”).

15


-----

_DYNAMIC PRICING ALGORITHMS_

_B._ Algorithms and Antitrust: Current Approaches

The explosion in the use of pricing algorithms over the past decade has
sparked concerns about their effects on competition and consumers. Accordingly, a growing body of scholarship has analyzed algorithms’ potential impact
on pricing and competitive conditions. This literature has focused predominantly on two issues: (1) whether pricing algorithms can be used to facilitate
express collusion among competing firms, and (2) the conditions under which
the use of pricing algorithms might result in tacit collusion among rivals.

On the first issue, a scholarly consensus has emerged that pricing algorithms can facilitate price-fixing and other forms of express collusion.[72] In
their influential article on the competitive impact of pricing algorithms, professors Ariel Ezrachi and Maurice Stucke identified two scenarios in which
firms can maintain a price-fixing conspiracy using pricing algorithms.[73] The
first, which they term the “messenger” model, is the simplest: human agents
at rival firms agree to fix prices and that they will do so through the use of
computers.[74] This is more than merely a theoretical issue: in 2015, the Department of Justice’s Antitrust Division prosecuted participants in just such a
scheme. The Division alleged that rival sellers of posters entered a conspiracy
to fix prices by using “commercially available algorithm-based pricing software
to set prices” on the Amazon Marketplace.[75] An individual defendant pled
guilty to “agree[ing] to adopt specific pricing algorithms” for selling the posters, “with the goal of coordinating changes to” the conspirators’ “respective
prices.”[76]

The second algorithmic price-fixing strategy Ezrachi and Stucke identified
is the “Hub and Spoke,” which involves rival sellers’ use of a common pricing
algorithm to coordinate prices among them.[77] The distinction between this
model and the more straightforward “messenger” model is that the rival firms
do not agree among themselves to fix prices; instead they each enter vertical
agreements to work with a third-party algorithm, which sets the price.[78] If
there is evidence that the common algorithm is being used as a tool for fixing

72 _See, e.g., Ezrachi & Stucke,_ _supra_ note 2 at 1784-89 (describing scenarios where firms
could use pricing algorithms to explicitly collude); Harrington, supra note 7 at 346 (“[P]ricing
algorithms . . . are rich enough to encompass the collusive strategies that have been used by
human agents.”).

73 Ezrachi & Stucke, supra note 2.

74 _Id. at 1784-87._

75 Complaint at 2, U.S. v. Daniel William Aston & Trod Limited, CR 15-0419 (Aug. 27,
2015).

76 Plea Agreement at 3, U.S. v. David Topkins, CR 15-00201 (April 30, 2015).

77 Ezrachi & Stucke, supra note 2 at 1787-89 (“Here, competitors use the same (or a single)
algorithm to determine the market price or react to market changes.”).

78 _Id._

16


-----

_DYNAMIC PRICING ALGORITHMS_

prices or otherwise facilitating collusion, the elements of a hub-and-spoke conspiracy might be satisfied.

When algorithms are used to maintain an explicit price-fixing conspiracy,
the legal intervention is clear: prosecution under section 1 of the Sherman
Act.[79] The involvement of an algorithm may change the nature of the available
evidence, but the legal analysis is not novel, especially in cases where human
agents from rival firms agree to employ an algorithm to fix prices.

The second question posed above—can the use of pricing algorithms facilitate tacit collusion—raises more difficult problems of proof and remedies.
Tacit collusion, or conscious parallelism as it is sometimes called, occurs when
rival firms recognize their shared interest in setting prices at a supracompetitive
level.[80] In this scenario, the firms have not entered an explicit agreement to fix
prices. Instead, by observing each other’s prices and understanding that rivals
will match any price cut, competing firms can charge consumers higher prices
than would obtain in a competitive market. Not all markets are susceptible to
tacit collusion; for conscious parallelism to take place, markets must exhibit
certain characteristics. Some combination of transparent pricing, homogeneous products, high entry barriers, and market concentration is necessary for
firms to be able to maintain prices above a competitive level in the absence of
an explicit agreement to do so.[81]

Some scholars have argued that pricing algorithms can facilitate tacit collusion.[82] One way they might do so is through the speed at which they can
discover and react to changes in rivals’ pricing. Once competing firms realize
that algorithms will quickly detect any price reduction and react by cutting

79 _See Roger Alford, Deputy Ass’t Att’y Gen’l, Antirust Div., U.S. Dep’t of Justice, The Role_
_of Antitrust in Promoting Innovation (Feb. 23, 2018) (“Where firms agree to set their pricing algo-_
rithms to coordinate on price, this is a traditional Section 1 violation.”).

80 _See, e.g., Brooke Group v. Brown and Williamson Tobacco Corp., 509 U.S. 209, 227_
(1993) (“Tacit collusion, sometimes called oligopolistic price coordination or conscious parallelism, describes the process, not in itself unlawful, by which firms in a concentrated market
might in effect share monopoly power, setting their prices at a profit-maximizing, supracompetitive level by recognizing their shared economic interests and their interdependence
with respect to price and output decisions.”).

81 _See, e.g., Deng, supra note 12 at 92 (“[T]he structural characteristics that tend to facili-_
tate/disrupt collusion” include “Symmetric competitors; Fewer competitors; More homogeneous products; Higher barrier to entry; More market transparency; More stable demand;
Small and frequent purchases by customers.”); In re Text Messaging Antitrust Litig., 782 F.
3d 867, 871 (7[th] Cir. 2015) (Posner J.) (“[T]he fewer the firms” in a relevant market “the easier
it is for them to engage in ‘follow the leader’ pricing (‘conscious parallelism,’ as lawyers call it,
‘tacit collusion,’ as economists prefer to call it … .”).

82 _See. e.g., Deng, supra note 12 at 88 (“[T]here is growing experimental evidence that an_
algorithm can be designed to tacitly collude.”); Gal, supra note 6 at 69 (“Coordination-facilitating algorithms are already available off the shelf, and such coordination is only likely to become
more commonplace.”); Mehra, supra note 2 at 1373 (“[T]acit collusion becomes more likely
with robo-sellers. . ..”).

17


-----

_DYNAMIC PRICING ALGORITHMS_

prices even further, they are less likely to deviate from the supracompetitive
collusive price.[83] Or, pricing algorithms might facilitate tacit collusion because
their use requires increased pricing transparency and they set prices in a predictable manner, reducing uncertainty.[84] The increasing sophistication of pricing algorithms makes it easier for them to figure out how to coordinate pricing
successfully and to do so more quickly.[85]

Other scholarship, particularly in the computer science and experimental
economics literature, disputes the extent to which algorithmic collusion is a
threat at present.[86] This body of work asserts that, absent explicit instructions
from human agents, it is difficult for algorithms in markets with more than
two competitors to tacitly collude. Professor Ulrich Schwalbe describes the
likelihood of algorithmic collusion currently as “belong[ing] to the realm of
legal sci-fi.”[87]

To the extent pricing algorithms increase the threat of tacit collusion, finding an appropriate intervention is challenging. Courts have interpreted section
1 of the Sherman Act, which addresses collusion, to require an explicit agreement among firms for liability to attach.[88] Conscious parallelism therefore is
lawful even though it causes consumers to pay higher prices than they would
in a competitive market.[89] Scholars have suggested a number of strategies for
addressing algorithm-driven tacit collusion. These include market-based solutions, antitrust, and regulatory interventions. Professor Michal Gal, for example, has proposed that consumers can employ their own algorithms to counter

83 _See Ezrachi & Stucke, supra note 2 at 1789 (pricing algorithms can reach “a similar com-_
mon understanding that is not explicitly negotiated but comes about with the computer learning to quickly detect and punish rivals’ price-cutting”).

84 _Id. at 1190 (“By shifting pricing decisions to computer algorithms, competitors increase_
transparency, reduce strategic uncertainty . . ., and thereby stabilize the market.”).

85 _See Gal, supra note 6 at 82._

86 _See, e.g., Ulrich Schwalbe, Algorithms, Machine Learning, & Collusion, 14 J._ COMPETITION
L. ECON. 568, 570 (2019) (“Given the current state of research in artificial intelligence and
machine learning, the concerns with respect to algorithmic collusion do not seem to be justified at the moment.”); Thibault Schrepel, The Fundamental Unimportance of Algorithmic Collusion
_for Antitrust Law, JOLT DIGEST (February 7, 2020), https://jolt.law.harvard.edu/digest/the-_
fundamental-unimportance-of-algorithmic-collusion-for-antitrust-law (“Algorithmic collusion is the subject of a growing literature, yet, empirical studies documenting the frequency of
the phenomenon in the real-world remain to be produced.”).

87 Schwalbe, supra note 87 at 600 (2019).

88 _See In re Text Messaging Antitrust Litigation, 782 F. 3d 867, 879 (7th Cir. 2015) (“Tacit_
collusion . . . does not violate Section 1 of the Sherman Act. . . . Collusion is illegal only when
based on agreement.”).

89 _Id. at 874-75 (observing that competing firms raising prices absent a conspiracy to do so_
is “merely tacit collusion, which to repeat is not illegal. . .”).

18


-----

_DYNAMIC PRICING ALGORITHMS_

sellers’ algorithms.[90] This market-based approach would empower consumers
to fight back by using algorithms to identify coordinated pricing so they can
avoid those sellers and, potentially, to create buyer power for negotiating leverage.[91] Gal cautioned that these potential solutions have significant limitations, however, including presenting their own antitrust risks if buyers use their
algorithms to enter anticompetitive agreements.[92] She concluded that marketbased approaches to countering pricing algorithms are “at best, partial” cures
and are not “a panacea.”[93]

Legal interventions also present challenges. Proposed responses fall into
two main buckets: antitrust solutions—which typically would require a reinterpretation or expansion of current case law—and regulatory solutions. On
the antitrust front, scholars have suggested a range of fixes, including expanding the definition of “agreement” for purposes of section 1, broadening antitrust law to bar tacit collusion altogether, and treating the use of algorithms as
an unlawful “facilitating practice” that makes achieving collusion easier.[94] Gal,
for instance, contends that the section 1 agreement requirement should be satisfied—even where human agents from rival firms have not entered an agreement—if a programmer intended an algorithm to reach a collusive pricing outcome.[95]

If an antitrust solution is unavailable to address the increased risk of algorithmic tacit collusion, then regulation may be necessary to protect consumers.
Scholars have proposed various regulatory interventions to counter the threat
that algorithms pose to competitive pricing. These include requiring firms to
disclose the details of their algorithms and their data inputs; barring algorithms
from using certain types of data inputs (e.g., rivals’ prices); and imposing time
lags on pricing adjustments so that a maverick firm could profitably lower its
prices without its rivals immediately matching those price cuts.[96] Another potential solution is direct price regulation in markets where algorithms have facilitated tacit collusion. Ezrachi and Stucke suggest that “Big Data” and “Big
Analytics” might allow governments to effectively set prices using their own

90 _See Gal, supra note 6 at 94-97 (describing several ways consumers can use algorithms to_
counteract algorithmic collusion).

91 _Id. at 96._

92 _Id._

93 _Id. at 96-97._

94 _See Ezrachi & Stucke, supra note 14 at 242_ (“The F.T.C. can attempt to reach the industry-wide use [of] algorithms as a facilitating practice.”).

95 Ezrachi & Stucke refer to this as the “predictable agent” scenario. See Ezrachi & Stucke,
_supra note 2 at 1789-91._

96 _See id. at 1805._

19


-----

_DYNAMIC PRICING ALGORITHMS_

algorithms, though they note various risks with this approach, including distorting industry incentives and regulatory capture.[97] Further, as pricing algorithms become more common and are adopted in more markets, price regulation would become an enormous regulatory undertaking that likely would alter
the nature of government and its relationship to the economy and the citizenry.

The existing competition literature on pricing algorithms focuses on the
potential for collusive outcomes, be they explicit or tacit. These studies presume immediate or eventual cooperation among algorithms, leading to higher
prices. They also presume that the algorithms firms employ are essentially
equivalent in quality and in their ability to collude. There will be markets, however—perhaps many markets—where firms employ competing algorithms of
differing quality. Take a market with three firms, 1, 2, and 3. Firm 3 may use
a highly sophisticated algorithm that is able to set prices many times a day in
response to changes in market conditions, while Firm 2 relies on a less sophisticated algorithm that can set prices only once a day, and Firm 1 employs an
algorithm that can set prices just once a week. Despite the likely prevalence
of this type of market, there have been no legal analyses to date of scenarios
where, instead of colluding, algorithms compete. To address this gap in the
literature, the next Part describes a game-theoretical model of algorithmic
competition developed by Professors Zach Brown and Alexander MacKay,
and demonstrates how this model differs from standard approaches to oligopoly theory. This analysis shows that competition among pricing algorithms results in higher prices for consumers even absent collusion.

II. PRICING ALGORITHMS & COMPETITION: ECONOMIC THEORY

Economic analyses of the types of competitive scenarios involving pricing
algorithms that concern antitrust scholars are grounded in oligopoly theory.
This robust body of theoretical literature has its origins in the 19[th] century work
of Antoine Cournot and Joseph Bertrand, and it extends to contemporary
game theoretical analysis pioneered by John Nash. To understand how pricing
algorithms might affect firm behavior, this Part begins by surveying classic oligopoly models. It then discusses how pricing algorithms can change the outcomes these classic models might predict by allowing firms to shift between
modes of competition. This analysis shows that algorithmic pricing will result
in supracompetitive prices even in the absence of collusion. Emerging empirical evidence supports this conclusion.

_A._ Classic Oligopoly Models

While economists have developed many sophisticated models to explain
the competitive interactions of firms, three key contributions dominate this
theoretical landscape: the Cournot model, the Bertrand Model, and the Nash
non-cooperative equilibrium.

97 _Id. at 1807._

20


-----

_DYNAMIC PRICING ALGORITHMS_

The Cournot model, introduced in 1838, posits a market for a single, undifferentiated (homogeneous) product in which a set of firms compete by
choosing the quantity of that product to produce.[98] The Bertrand model, from
1883, is often applied to markets featuring differentiated (non-homogeneous)
products and it assumes that firms compete by choosing prices, not quantities.[99] In modern oligopoly theory the Cournot and Bertrand models are interpreted in light of the Nash equilibrium theory, pioneered in 1950.[100] Using
game theory to describe the interactions of competing firms, Nash posited that
an equilibrium[101] outcome in a non-cooperative game[102] will occur when each
player, knowing the strategies of the other players, has no incentive to change
their current strategy. So, if three firms compete in a market and each, by observing the market, understands its rivals’ strategies, and all three determine
that they cannot gain a competitive advantage by unilaterally changing their
own strategy, the market has achieved a Nash non-cooperative equilibrium.
Another way to think about the Nash equilibrium is that it describes a selfenforcing agreement among firms.[103] Without explicitly agreeing on any specific course of action, the firms in a Nash equilibrium have reached a state
where none of them will unilaterally change their current strategy.

Modern economic theory uses the Nash non-cooperative equilibria of the
Bertrand and Cournot models to determine competitive price levels. The
Cournot-Nash equilibrium describes a model in which, based on their
knowledge of the quantities their rivals produce, each firm is satisfied with the
quantity it chooses to produce and will not unilaterally alter its competitive
strategy. The Bertrand-Nash equilibrium describes a model in which, based
on their knowledge of their rivals’ prices, each firm is satisfied with the price it
chooses to charge, and will not unilaterally change its competitive strategy.

While these two equilibria may appear similar in some respects, their outcomes can be significantly different. Both models predict lower prices and
higher output as the number of competitors in a market increases. When applied to differentiated products, the Bertrand-Nash equilibrium price depends
on how differentiated the products are.[104] If they are imperfect substitutes,

98 _See Gregory J. Werden, Economic Evidence on the Existence of Collusion: Reconciling Antitrust_
_Law with Oligopoly Theory, 71 ANTITRUST L._ J. 719, 722, 724 (2004).

99 _Id. at 723._

100 _Id. at 721-723._

101 An equilibrium is a set of strategies chosen by all players such that no player has an
incentive to alter its strategy. See, e.g., Werden, supra note 99 at 721.

102 In a Nash non-cooperative game, each player chooses strategies independently of the
other players, taking as given the strategies chosen by the other players.

103 _See Dennis W. Carlton, Robert H. Gertner & Andrew M. Rosenfield,_ _Communication_
_among Competitors: Game Theory and Antitrust, 5 GEO._ MASON L. REV. 423, 430 (1997).

104 _See Werden, supra note 99 at 723._

21


-----

_DYNAMIC PRICING ALGORITHMS_

each firm will charge a markup, and equilibrium prices will be above marginal
costs. The closer the products are to being perfect substitutes, the lower the
markup and the resulting equilibrium price.[105] With homogeneous products,
which are perfect substitutes, the Bertrand-Nash equilibrium generates prices
that are equal to marginal costs, even when only two firms are in the market.[106]

The Cournot model is also applied to markets with homogenous products.
However, unlike the Bertrand-Nash equilibrium, the Cournot-Nash equilibrium price in an oligopoly market is above marginal costs, so that all firms earn
positive markups.[107] Thus, despite facing identical demand conditions, the
mode of competition—i.e., whether firms compete à la Bertrand or à la
Cournot—has substantial implications for price levels.

The Cournot and Bertrand models therefore present an interesting case
where different models of firm behavior deliver different market outcomes,
even when other market conditions are identical. Moreover, the Nash equilibria under both models are considered competitive equilibria because each firm is
acting non-cooperatively to pursue its own self-interest. This provides a useful
illustration of a key mechanism in our paper: the choice of the mode of competition (in prices or in quantities) can affect equilibrium prices.[108] If firms in
homogeneous product markets could choose between the two, they would opt
for the Cournot model that yields higher prices.

One challenge in applying these theories to antitrust analysis is deciding
which model to employ in a given market. Both models are actively used in
empirical work. Researchers and antitrust authorities have almost exclusively
applied the Cournot model to industries with homogeneous products, likely
because firms usually earn some markup over marginal costs in real-world settings.[109]

Another challenge is determining what happens when firms have repeated
interactions in the same market over time.  Much of modern oligopoly theory
focuses on this second challenge, and in particular on whether collusion can
be sustained when firms choose quantities or prices in such settings. The
Cournot and Bertrand models discussed above are “one-shot games” in which
firms have one opportunity to make their quantity or pricing decisions. In most

105 _Id. at 723._

106 _Id. at 724._

107 _Id. at 724._

108 _See id. (“As a general matter, changing the rules of the game (e.g., from having players_
choose prices to having them choose quantities) can substantially affect the outcome.”).

109 The Cournot model can alternatively be justified as a two-stage game where firms first
choose production capacities, and then compete in prices after pre-committing to capacities.
_See David M. Kreps & José A. Scheinkman, Quantity Precommitment and Bertrand Competition Yield_
_Cournot Outcomes, 14 BELL J. ECON. 326 (1983). Thus, the Cournot model has been applied_
to industries such as cement and electricity, where products are homogenous and capacities
are observable.

22


-----

_DYNAMIC PRICING ALGORITHMS_

real-world markets, firms are continually making quantity and pricing decisions. “Repeated games,” which comprise multiple “stage games,” are intended to capture this reality. In these games, firms play the Cournot or Bertrand game multiple times with the same rivals. Under these circumstances,
firms in a concentrated market can move from the competitive equilibrium of
a one-shot game toward a collusive equilibrium, in which firms—recognizing
their mutual interests and employing strategies to discipline price-cutters—will
raise prices above the competitive level.[110] In other words, given repeated interactions over time, firms in concentrated markets can coordinate on supracompetitive prices even without an explicit agreement to do so. These tacitly collusive outcomes are more fragile than the competitive equilibria, as
every firm has a short-run incentive to steal market share from their rivals,
either by cutting prices or increasing output. Explicit collusion also faces the
same pressures to deviate, even though all rivals have agreed to the strategies
that will be played. An analysis of whether or not collusion is likely in a market
is guided by a set of factors that render cooperation favorable.[111]

The theoretical landscape therefore features three models of firm interaction: a competitive outcome (one-shot games), a collusive outcome absent explicit agreement (repeated games), and explicit collusion where an agreement
governs firm interaction. To date, scholars working in this landscape share the
assumption that firms cannot alter the model of competition in a specific market. If market characteristics suggest that firms compete by choosing quantities
(Cournot model), current scholarship assumes that firms will not switch to a
model in which they choose prices instead (Bertrand model). The development
of pricing algorithms undermines this key assumption by allowing firms to
change the model of competition in a market.

_B._ Pricing Algorithms Change the Competitive Game

Pricing algorithms add a new element to the theoretical analysis of price
competition. When firms use pricing algorithms, it is no longer accurate to
represent a firm’s strategic decision in terms of prices, as is done in the Bertrand model. Firms’ strategies consist of algorithms that determine prices.
Thus, instead of choosing prices directly, each firm chooses an algorithm to
effectively act as a “representative” for the firm. The algorithm then sets prices
according to a specific set of rules, which are determined by the firm. By
choosing the rules instead of the prices, firms can effectively select among different modes of competition, akin to allowing firms to switch from Bertrand
to Cournot. Brown and MacKay show that pricing algorithms provide firms
with two mechanisms for changing the competitive game: they allow firms to

110 This is often discussed in terms of the “Folk Theorem.” See, e.g., Werden, supra note 99
at 729-731.

111 _See, e.g., U.S. DEP’T OF JUSTICE, supra note 25 (listing industry conditions “favorable to_
collusion”).

23


-----

_DYNAMIC PRICING ALGORITHMS_

vary the frequency with which they price and to signal _commitment to a pricing_
strategy.[112] In equilibrium, these mechanisms can produce different competitive outcomes than the Cournot or Bertrand models would predict. We consider the impacts of one or more firms adopting pricing algorithm technology
relative to a hypothetical starting point where both firms compete on prices.

These effects can be captured by three scenarios. First, imagine a scenario
where a pricing algorithm allows one firm to update its prices more frequently
than its rival. For example, one firm may have technology that allows it to
update prices multiple times per day, whereas the other firm can update prices
only once per week. Brown and MacKay describe this situation as a market
with “asymmetric frequency.”[113] Second, consider a scenario where one firm
has encoded its pricing strategy into an algorithm, and this algorithm determines price changes at a high frequency without human intervention. If the
algorithm has the ability to monitor and react to the price changes of its rival,
this market features “asymmetric commitment.”[114] Finally, the third scenario
is one in which both firms have high-frequency algorithms that adjust prices
without human intervention, and both algorithms react autonomously to the
price changes of rivals. Brown and MacKay term this situation “symmetric
commitment.”

Brown and MacKay’s analysis shows that asymmetric frequency and asymmetric commitment both result in prices above the competitive level for each
firm. It also demonstrates that symmetric commitment can generate higher
prices, including the fully collusive price, even when algorithms are prohibited
from employing collusive strategies. Indeed, when each firm’s algorithm depends on the prices of rivals, in equilibrium, prices will never be at the competitive (Bertrand) level.[115] Considered together, these models demonstrate that
algorithms will fundamentally change the pricing landscape by allowing firms
to charge supracompetitive prices even in the absence of collusion.

_1._ _Frequency_

To understand the impact of algorithms on pricing frequency, consider a
simple scenario with two firms. Firm 1 has technology that enables it to update
its price once per week. Initially, its rival, Firm 2, has the same technology and
also sets its price at the same time each week. Assume that each firm has a
single product, that these products are imperfect substitutes, and that the firms
are symmetric in terms of demand conditions and costs. This scenario approximates the historical pricing patterns for brick-and-mortar grocery and drug
stores. In this setting, the competitive Bertrand-Nash equilibrium is one in

112 _See Brown & MacKay, supra note 13 at 7._

113 _Id._

114 _Id. at 24._

115 _Id. at 29-30._

24


-----

_DYNAMIC PRICING ALGORITHMS_

which each firm charges the same price. Firms earn a markup over marginal
costs because the products are differentiated.

Next, consider what happens when one firm introduces pricing technology
that allows it to set prices at a higher frequency. In this revised scenario, assume Firm 1 continues to set prices only at the beginning of the week, but
Firm 2 adopts new pricing technology that allows it to update its prices once
each day during the week. The firms now price at an asymmetric frequency,
and this is known by both firms.

Brown and MacKay show that under these circumstances the competitive
outcome will be different than the Bertrand-Nash equilibrium.[116] Firm 1 will
determine its price for the entire week with the knowledge that Firm 2 can
change its price the next day. In typical cases, it is optimal for Firm 2 to undercut any price chosen by Firm 1 that is above the Bertrand-Nash level.[117]
Because Firm 2 can change its price in response to Firm 1’s price, Firm 2 can
now effectively “threaten” Firm 1 with deeper price cuts. As a result, the Bertrand logic where Firm 1 considers price changes assuming Firm 2’s price is
fixed no longer applies. Firm 1 instead will choose a price that will maximize
its profit in light of Firm 2’s anticipated response the following day.[118]

Knowing that Firm 2 will undercut its price, Firm 1 will set a price above
the competitive level.[119] Firm 2 will choose its price (each day) to maximize its
own profits. This price will be below Firm 1’s price but above the competitive
level. Because the products are differentiated, Firm 1 will continue to attract
some customers, despite its higher price. In this scenario, both firms can obtain
higher profits than they would in the Bertrand-Nash equilibrium.[120] Firm 2’s
adoption of a superior pricing technology creates an asymmetry in pricing frequency that allows the firms to commit to a leader-follower pricing pattern,
resulting in higher prices for consumers.[121]

Even though Firm 1 is disadvantaged relative to Firm 2, Firm 1 earns
higher profits than in the scenario where both firms have the same pricing
frequency. If Firm 1 were to adopt daily pricing frequency to match Firm 2’s
technology, prices would revert to the Bertrand-Nash level. The difference in
pricing frequency is what permits firms to maintain a leader-follower order and
charge higher prices. Thus, in markets where firms employ pricing algorithms,
there are potentially strong profit incentives leading firms to choose different

116 _Id. at 19._

117 Brown & MacKay focus on the case where prices are strategic complements, which is
the usual case for differentiated products. _See JEAN TIROLE, THE THEORY OF INDUSTRIAL_
ORGANIZATION (1988).

118 _Id. at 18._

119 Brown & MacKay, supra note 13 at 19.

120 _Id. at 21-22._

121 _Id. at 22._

25


-----

_DYNAMIC PRICING ALGORITHMS_

pricing frequencies. Firms do not need to coordinate or collude on this arrangement, as it is in their unilateral best interests. This means that in markets
where firms sustain symmetric pricing, other factors likely are at work. For
example, in some markets, it may be technologically challenging or prohibitively expensive to adopt technology that allows for more frequent price
changes.[122] Or less frequent price variations might be too costly, because they
may prohibit a firm from adjusting to changes in demand and supply. To enhance the ability to adjust to changing conditions, in some circumstances we
may see all firms in a market adopting higher-frequency pricing technology,
even if it results in symmetric pricing frequency.[123]

In our example, we have discussed a case with two firms, but the same
logic applies to an oligopoly setting with several firms and a wide range of
choices for pricing frequency. The firms with slower price changes will internalize the subsequent reactions of faster firms, causing them to increase prices
above Bertrand-Nash levels.

While these firms will react to each other’s prices in a way that leads to
supracompetitive pricing, the outcome is different from that of collusion. In
the example above, colluding firms would charge the same price. At that price,
each firm would want to undercut its rival, stealing market share and increasing
profits. In the scenario we describe, the firms are competing on price, and the
prices differ, with superior-technology firms charging lower prices. Further,
collusion is maintained by a reward-punishment scheme where firms are rewarded when they maintain a supracompetitive price and punished when they
deviate from it.[124] That is not the strategy we describe here. By introducing
differences in pricing frequency, algorithms enable all firms to price above the
competitive level in a non-cooperative equilibrium.

_2._ _Commitment_

The second feature of pricing algorithms that can change the competitive
game is commitment. In the discussion of pricing frequency above, the assumption is that firms have the flexibility to choose any price whenever they
update prices. In practice, algorithms often have less flexibility and are restricted by a set of rules that are encoded in software.[125] These rules may be
quite complicated, and they may evolve over time. Regardless, the chosen price
can be traced directly to underlying code. Thus, algorithms provide firms with
the ability to commit to a set of (inflexible) rules when determining prices.
Importantly, these rules often depend on the prices of rivals.

122 _Id._

123 _Id._

124 _See, e.g., Harrington,_ _supra_ note 7 at 336 (“Collusion is when firms use strategies that
embody a reward-punishment scheme which rewards a firm for abiding by the supracompetitive price and punishes it for departing from it.”).

125 _Id. at 7._

26


-----

_DYNAMIC PRICING ALGORITHMS_

If firms choose algorithms optimally, how would the encoded pricing rules
reflect rivals’ prices? Brown and MacKay address this question by considering
two different scenarios, one in which only one firm has the ability to make
such a commitment and a second in which both firms have this ability.

In the first scenario, “asymmetric commitment,” one firm has an algorithm
that allows for an automated response to the price changes of its rival. As before, consider Firm 1 to have the inferior technology. Each firm can set their
algorithms once at the beginning of the week. Over the course of the week,
these algorithms may adjust prices due to changing demand conditions or inventories, but only Firm 2 can adjust to changes in its rival’s prices. For example, suppose that Firm 2’s algorithm scrapes Firm 1’s price once per day and
uses the observed price to update its own price. In this way, Firm 2’s algorithm
commits it to react to price changes by Firm 1. This is a realistic scenario: many
markets feature competitors with varying abilities to monitor and react to rivals’ pricing.[126]

In this setting, Firm 1 will determine its algorithm in a way that will maximize its own profits, taking into account Firm 2’s algorithmic response.[127]
What pricing rule will Firm 2 use to react to the price of Firm 1? Brown and
MacKay show that it is optimal for Firm 2 to encode in its algorithm the exact
behavior Firm 2 would want to use if it were flexibly choosing prices each
day.[128] Thus, the outcome in the asymmetric commitment setting mirrors the
outcome in the case of asymmetric frequency discussed above. Firm 1 ends up
with a price above the competitive level and Firm 2 has a price that is lower
yet also above the competitive level. Both asymmetric frequency and asymmetric commitment lead to the same equilibrium with supracompetitive
prices.[129]

In the second scenario, “symmetric commitment,” both firms employ algorithms that autonomously react to changes in rivals’ prices. Unlike the asymmetric scenarios described above, these firms have equivalent pricing technology. The hypothetical real-world environment is one in which all firms adopt
algorithms that adjust at a very high frequency. Again, a key assumption is that
these algorithms can update prices faster than the firms update their algorithms, so that the algorithms provide short-term commitment to their pricing
strategies. In determining what pricing rules to employ, each firm considers
that rivals also have commitment encoded in their algorithms. Brown and

126 _See, e.g., infra Part II.C (discussing empirical evidence of variations in pricing technolo-_
gies in the online market for over-the-counter allergy drugs).

127 _See Brown & MacKay, supra note 13 at 25._

128 _Id. Formally, Firm 2 would find it optimal to encode its Bertrand reaction function into_
its algorithm.

129 _Id._

27


-----

_DYNAMIC PRICING ALGORITHMS_

MacKay address this scenario by extending the Nash non-cooperative equilibrium to a game where firms choose pricing algorithms that are functions of
rivals’ prices.

Thus described, this model is flexible enough to allow algorithms to encode collusive schemes directly. Brown and MacKay use potential enforcement by a competition authority to rule out such cases, under the notion that
these “obviously collusive” strategies would be subject to typical price-fixing
charges. They then focus on strategies that (1) do not admit multiple solutions
and (2) are continuous functions of rivals’ prices. Both of these conditions are
sufficient to rule out reward-punishment schemes that characterize collusion.[130]

Despite narrowing the focus only to strategies that appear to be competitive, symmetric commitment allows firms to support supracompetitive prices.
In fact, Brown and MacKay show that the joint profit-maximizing price levels
(i.e., the collusive outcome), can be achieved using only very simple algorithms.[131] Specifically, Brown and MacKay explore linear algorithms of the
form 𝑝2 = 𝑎 + 𝑏𝑝1, where the slope, 𝑏, specifies how much Firm 2’s price
changes for every one cent change by Firm 1. For example, the algorithm may
follow the heuristic “reduce my price by $0.50 for every $1 reduction by my
rival.” Due to the high frequency with which the algorithms are able to react,
a rule along these lines may increase prices by as much as an agreement to
collude.[132] Because firms do not want their rivals to reduce prices, such a commitment may discourage all firms from cutting prices, thereby maintaining
prices at high levels. The slope of the algorithm may be chosen so that rivals
do not want to deviate from collusive price levels.

This result raises two key challenges for antitrust. First, the algorithms do
not appear in any way to resemble reward-punishment strategies that characterize collusion. Moreover, the optimal competitive price response may qualitatively appear the same as a strategy that delivers higher prices. For example,
in some settings the optimal competitive reaction is a linear function of rivals’
prices, as in the example above.[133] In such settings, the only difference between
linear strategies that deliver competitive price levels and those that deliver collusive price levels are different values of 𝑎 and 𝑏. Thus, the distinction is quantitative, rather than qualitative. This poses a detection challenge for competition authorities: it may be possible to observe all firms’ algorithms, yet still not
know whether the resulting prices are substantially elevated above competitive
levels. To make that determination, authorities would have to know the competitive values of 𝑎 and 𝑏. By contrast, competition authorities are able to

130 _Id. at 28._

131 _Id. at 31._

132 _Id._

133 _Id._

28


-----

_DYNAMIC PRICING ALGORITHMS_

identify whether a strategy is collusive because of its reward-punishment characteristics. Brown and MacKay provide an important qualitative result in this
regard: if both firms’ algorithms depend on rivals’ prices, then we should not
expect competitive price levels in equilibrium.[134] The presence of reciprocal
automated price reactions is a flag for supracompetitive price levels.

The second challenge is that firms may arrive at these strategies unilaterally,
without any incentive to deviate from the achieved equilibrium. In other
words, when using algorithms, behavior that is consistent with a Nash noncooperative equilibrium can enable firms to reach outcomes that are only possible with cooperation or collusion when firms compete by choosing prices. It
is not clear that, legally, the unilateral adoption of such algorithms constitutes
any sort of agreement, tacit or explicit. As Brown and MacKay demonstrate,
firms can independently arrive at collusive prices solely through random experiments to test and improve the parameters of their linear algorithms.[135]

The presence of algorithms does not rule out the possibility of collusive
equilibria occurring in repeated interactions. Instead, it raises what is perhaps
a more troublesome prospect: that algorithms provide firms with an opportunity to increase prices without resorting to collusive behavior. If firms have
the option to choose between adopting algorithms or pursing collusion, they
may opt for algorithms that deliver higher prices and profits without the risk
of antitrust enforcement.

In this way, pricing algorithms may reduce the likelihood of explicit collusion. The benefit to be gained from colluding versus competing in algorithms
is smaller relative to the gain versus competing in prices, precisely because algorithms move firms closer to the joint profit-maximizing outcome.

***
The models discussed above support two conclusions about the effects of
pricing algorithms. First, when the use of algorithms results in asymmetries in
pricing frequency or commitment, prices will be higher than the competitive
equilibrium. Second, when firms compete using algorithms that can incorporate rival firms’ pricing, very simple algorithms can generate supracompetitive

134 _Id. at 29._

135 The game with symmetric commitment supports many different equilibria. Brown and
MacKay argue that higher-price equilibria are likely to result in typical cases, for two key reasons. First, algorithms are likely to adjust prices in the same direction of the price changes of
rivals, i.e., a price cut by a rival results in a price decrease for the firm. If the algorithms have
this feature, higher prices result. In typical settings, it would be counterintuitive for a firm to
increase its price in response to a price cut by a rival. Second, Brown and MacKay use simulations to show that firms that use experiments to test and improve their algorithms end up
with supracompetitive prices near the collusive price. This result occurs because many of the
possible equilibria are “knife-edge” cases, arising only if the parameters of the algorithms
across firms line up in an exact way. It is more likely for a firm to realize an increase in profits
when choosing parameters that push it toward the collusive price level. Id. at 30.

29


-----

_DYNAMIC PRICING ALGORITHMS_

prices, including the collusive price, even in the absence of collusion. In all
these scenarios, pricing algorithms function as self-enforcing agreements, as in
the Nash non-cooperative equilibrium. While firm interaction leads to higher
prices in these models, algorithms provide many more possibilities than the
collusive outcome. In cases with asymmetric technology, there may be large
differences in prices across firms. It is possible for each firm to charge a different price, though all prices exceed the competitive price. These models allow us to predict that even in competitive markets, the increasing use of pricing
algorithms will result in higher prices for consumers.

_C._ Empirical Evidence

While there is substantial evidence on the spread and scope of algorithmic
pricing in many markets, and especially in e-commerce, few empirical studies
have been performed measuring the effects of these technologies on market
prices. The Chen, Mislove, and Wilson study discussed above tracked the penetration of algorithmic pricing in the Amazon Marketplace and showed how
the technology affects competitiveness among merchants, but it did not attempt to demonstrate whether algorithmic pricing results in higher or lower
prices for consumers.[136] Brown and MacKay performed an empirical study addressing this issue.

Brown and MacKay compiled data on the hourly prices five online retailers
charged for seven brands of over-the-counter allergy drugs.[137] The data is
from the period April 2018 through October 2019 and comprises over 3.5
million price observations.[138] Those data show significant differences among
the five retailers in the number of products they reprice each day and the frequency of those price adjustments. Labeling the retailers A through E, the authors found that retailer A repriced around a third of its products a day and
made about two price adjustments per product per day, while retailer C repriced less than one percent of its products per day and made just one price
change per day for those products.[139] The study also demonstrated that the
pricing technologies the retailers employed varied greatly in quality. Three of
the retailers (A, B, and C) changed prices at various times during the week,
while the remaining two retailers (D and E) made almost all of their price
changes on Sundays.[140] Further, retailers A and B made pricing changes at different times during the day, while retailers C, D, and E made changes only
during the morning.[141] Brown and MacKay concluded that retailers A and B

136 _See supra notes 67-70._

137 Brown & MacKay, supra note 13 at 8.

138 _Id._

139 _Id. at 9._

140 _Id. at 10-11._

141 _Id._

30


-----

_DYNAMIC PRICING ALGORITHMS_

employed superior pricing technology that allowed them to change prices at
any hour of any day.[142] Retailer C had technology that allowed for price updates at most once per day, while retailers D and E could change prices only
on Sunday mornings.[143]

Brown and MacKay also found evidence that the faster firms were more
likely to change the price of a particular product after a slower retailer changed
the price of that product.[144] The authors concluded that this was an indication
that the faster firms’ algorithms were monitoring and responding to slower
firms’ prices, which is consistent with their theoretical model.[145]

Brown and MacKay next evaluated how these disparities in algorithmic
sophistication affected these retailers’ prices. The game theoretical models described above predict that asymmetric pricing frequency (and asymmetric
commitment) would result in the firms with more sophisticated pricing technology offering lower prices than the firms that price less often. The data from
this study bear out that prediction. Firm A, which had the most sophisticated
technology—allowing it to change its prices more frequently than its rivals—
had the lowest prices of the five retailers.[146] Firms D and E, which had the
lowest-quality pricing technology and could change prices only once a week,
had the highest prices.[147] According to the authors, firms D and E’s prices for
identical products were over 25 percent higher than the prices firm A charged.
Firm C, possessing moderate pricing frequency, priced products approximately
10 percent higher than firm A.[148] This correlation between pricing frequency
and price levels is one of the key predictions of the Brown and MacKay model.

To measure the effect of asymmetric pricing technologies on equilibrium
prices, Brown and MacKay applied an econometric model to the data to estimate demand. The authors compared the observed price levels to counterfactual Bertrand-Nash prices, which they obtained by assigning firms symmetric
price-setting technology and simulating the equilibrium. The authors estimated
that algorithmic competition among these firms with varying levels of pricing
technology resulted in average prices more than five percent higher than if the

142 _Id._

143 The authors define pricing technologies in this setting as including not only the algorithm itself and the computers that implement it, but also “managerial or operational constraints” that limit the ability to change prices more frequently. Id. at 11.

144 _Id. at 12-13._

145 _Id. at 14._

146 _Id. at 15._

147 _Id._

148 _Id._

31


-----

_DYNAMIC PRICING ALGORITHMS_

firms had symmetric technologies.[149] Firm A, with the fastest technology, enjoyed substantial increases in both price and market share due to algorithmic
competition, resulting in the highest gain in profits (22 percent).[150]

Despite these price increases, the estimated model predicted only a modest
output reduction (around one percent) due to asymmetric algorithmic competition.[151] While decline in total welfare therefore is small, Brown and MacKay
found that algorithmic competition leads to a significant wealth transfer from
consumers to merchants. The model showed a decline in consumer surplus
of 4.1 percent and an increase in firm profits of 9.6 percent due to asymmetric
algorithmic competition.[152] The authors calculated that, if similar effects were
realized across the personal care category in which all five retailers have significant shares, the switch from Bertrand competition to algorithmic competition
would cost online consumers $300 million a year.[153]

***
Economic models and emerging empirical evidence suggest that algorithmic pricing can harm consumers even in competitive markets where rivals do
not collude. The rapid expansion of algorithmic pricing throughout the economy means that this consumer harm will be widespread and significant. When
firms use algorithmic pricing to explicitly collude, antitrust is an obvious remedy. But what should be the policy response when consumers are harmed by
non-collusive conduct? The following Part addresses that question.

III. POLICY RESPONSES

When pricing strategies harm consumers, typical policy responses include
antitrust enforcement and, if that fails, direct price regulation. Despite its focus
on pricing and competition, however, in practice antitrust law can reach only
a select few types of pricing practices, none of which are implicated by the
non-collusive algorithmic pricing strategies described in the previous Part. Direct regulation therefore is likely to be the best solution for ameliorating the
transfer of surplus from consumers to sellers that algorithmic pricing makes
possible.

This is not the first time that advances in pricing technology have led to
economic disruption. In the early twentieth century, the introduction of price
displays, price tags, and new pricing strategies like loss leaders contributed to
fierce price-cutting and a dangerous deflation which exacerbated the economic
shock of the Great Depression. The policy response then was direct pricing
regulation: legislation and industrial codes limiting price cutting. We argue that

149 _Id. at 39._

150 _Id. at 40._

151 _Id. at 40._

152 _Id. at 40._

153 _Id. at 40._

32


-----

_DYNAMIC PRICING ALGORITHMS_

direct regulation of a different type might be appropriate today, when a new
revolution in pricing technology is again reshaping the nature of competition.

This Part begins by exploring the possibility of using antitrust to address
the problems non-collusive algorithmic pricing poses for consumers. It concludes that antitrust’s prohibitions do not reach this type of pricing conduct.
The discussion then turns to a history of early twentieth century pricing innovations and resulting regulatory reactions. It closes with a review of potential
regulatory responses to non-collusive algorithmic pricing.

_A._ Antitrust & Pricing

While much of antitrust law is focused on prices, the specific types of pricing conduct it prohibits ultimately are quite narrow. Most famously, antitrust
forbids firms from explicitly colluding on prices. Price-fixing, bid-rigging, and
market allocation agreements are per se unlawful under section 1 of the Sherman Act and are considered criminal conduct.[154] Explicitly collusive algorithmic pricing falls directly into this forbidden zone. When sellers of wall art
agreed to use their pricing algorithms to fix prices on the Amazon Marketplace,
their method may have been novel, but the legal theory the Department of
Justice used to successfully prosecute them was the same applied to conspiracies hatched in the smoke-filled rooms of the early twentieth century.[155] Antitrust is therefore the best available tool for dealing with algorithmic price-fixing conspiracies.

But liability under section 1 of the Sherman Act, which bars price-fixing,
requires that there be an agreement among the defendants.[156] It is challenging
to craft an antitrust intervention when firms do not explicitly collude. This is
the case even when rivals employ parallel pricing conduct to reach a collusive
price. Tacit collusion is not currently unlawful under the antitrust laws.[157] As
described above, a number of scholars have argued that algorithmic pricing
facilitates conscious parallelism, in their view necessitating a new look at ways
that antitrust should adapt to bar tacit collusion.[158]

The conduct this paper focusses on—non-collusive algorithmic pricing—
is even further removed from the explicitly collusive conduct section 1 prohibits. In the scenarios described in the previous Part, neither human agents

154 _See U.S. Dep’t of Justice, supra note 25._

155 _See_ U.S. Dep’t of Justice, _supra_ note 11 (announcing guilty plea in scheme involving
fixing “the prices of certain posters sold online through Amazon Marketplace” and quoting
Assistant Attorney General Bill Baer as stating that the Antitrust Division “will not tolerate
anticompetitive conduct, whether it occurs in a smoke-filled room or over the internet using
complex pricing algorithms”).

156 _See In re Text Messaging Antitrust Litig., 782 F. 3d 867, 879 (7th Cir, 2015) (“Collusion_
is illegal only when based on agreement.”).

157 _See id. (“Tacit collusion . . . does not violate Section 1 of the Sherman Act.”)._

158 _See supra notes 27-28._

33


-----

_DYNAMIC PRICING ALGORITHMS_

nor algorithms are agreeing on prices.[159] Indeed, the firms in these markets
may not be setting a collusive price at all; supracompetitive prices can be supported even when some firms are charging a lower price than others. Section
1 conspiracy law simply has no bearing on this type of conduct.

In addition to its prohibitions on price fixing and bid rigging, antitrust specifically bars or restricts three other types of pricing conduct: predatory pricing,
resale price maintenance, and certain forms of price discrimination. None of
these rules address the challenges posed by non-collusive algorithmic pricing.

_1._ _Predatory pricing_

Section 2 of the Sherman Act prohibits firms from unlawfully acquiring or
maintaining monopoly power in a relevant market.[160] To prevail on a section 2
claim, a plaintiff must prove that a firm has monopoly power and that it either
acquired or maintained that position unlawfully.[161] Predatory pricing is one
form of unlawful conduct firms might use to gain or maintain a monopoly.
The idea is that a big and powerful firm can use below-cost pricing to drive its
smaller and less well-capitalized rivals out of business, thereby allowing it to
raise prices to supracompetitive levels. Courts and enforcers are wary of predatory pricing claims because, at least in the short run, consumers benefit from
the price war.[162] The bar therefore is high for plaintiffs in these cases. They
must demonstrate that the defendant charged prices that were below some
measure of its costs and that it had a “reasonable prospect” or a “dangerous
probability” of recouping its losses after the predation period.[163] To prove
recoupment, a plaintiff must show that the defendant’s conduct could or did
drive its rival(s) out of the market and that barriers to entry are sufficiently

159 A key condition for demonstrating collusion is the presence of an agreement. Werden
provides the following general principle regarding such agreements: “The existence of an
agreement cannot be inferred from actions consistent with Nash, non-cooperative equilibrium
in a one-shot game oligopoly model.” Werden, supra note 99 at 779. Yet the Brown and MacKay model shows precisely how elevated prices can be sustained in a Nash, non-cooperative
equilibrium of a one-shot oligopoly game.

160 15 U.S.C. § 2 (2012).

161 _See_ U.S. v. Grinnell Corp., 384 U.S. 563, 570-71 (1966) (“The offense of monopoly
under s 2 of the Sherman Act has two elements: (1) the possession of monopoly power in the
relevant market and (2) the willful acquisition or maintenance of that power as distinguished
from growth or development as a consequence of a superior product, business acumen, or
historic accident.”).

162 _See Brooke Group Ltd v. Brown & Williamson Tobacco Corp., 509 U.S. 209, 223 (1993)_
(holding that any exclusionary effect of above-cost pricing either “reflects the lower cost structure of the alleged predator . . . or is beyond the practical ability of a judicial tribunal to control
without courting intolerable risks of chilling legitimate price-cutting.”).

163 _See id. at 222-24 (holding that to prevail on a predatory pricing claim a plaintiff “must_
prove that the prices complained of are below an appropriate measure of its rival’s costs” and
“that the competitor had a reasonable prospect, or, [] a dangerous probability, of recouping
its investment in below-cost prices”).

34


-----

_DYNAMIC PRICING ALGORITHMS_

high that the defendant subsequently would be able to raise prices to a supracompetitive level for a sufficient amount of time to gain back the losses it
incurred from pricing below cost.[164]

Predatory pricing may have a role to play in certain kinds of algorithmic
pricing settings. Professor (and now Chairwoman of the Federal Trade Commission) Lina Khan has argued, for example, that Amazon’s pricing algorithm
allows it to strategically undercut its rivals’ prices.[165] The equilibrium analysis
presented in this Article shows that algorithmic pricing may have the opposite
effect, leading to increased prices for all firms. Predatory pricing theory is inapplicable to situations where pricing algorithms facilitate multiple sellers raising prices above the competitive level.

_2._ _Resale Price Maintenance_

For almost a century in the United States, federal antitrust law prohibited
manufacturers from agreeing with retailers on resale prices for their goods.[166]
Under that regime, a producer of board games or knives or toilet paper could
not directly control the prices retailers charged for those products. In a pair
of cases in 1997 and 2007, the U.S. Supreme Court held that minimum and
maximum resale price maintenance no longer would be treated as per se unlawful, but rather should be evaluated on a case-by-case basis under antitrust’s
rule of reason.[167] Resale price maintenance remains per se unlawful under the
laws of some states.[168]

It is possible that manufacturers’ resale price maintenance policies could
affect price levels in markets subject to non-collusive algorithmic pricing. If a

164 _See id. at 225-26 (“For recoupment to occur, below-cost pricing must be capable, as a_
threshold matter, of producing the intended effects on the firm’s rivals, whether driving them
from the market or [] causing them to raise their prices to supracompetitive levels within a
disciplined oligopoly. . .. Determining whether recoupment of predatory losses is likely requires an estimate of the cost of the alleged predation and a close analysis of both the scheme
alleged by the plaintiff and the structure and conditions of the relevant market.”).

165 _See Lina M. Khan, Amazon’s Antitrust Paradox, 126 YALE L.J. 710, 768-770 (2017) (de-_
scribing how Amazon used its “pricing bots” to strategically undercut prices its rival Quidsi
charged for diapers and other baby products, ultimately resulting in Quidsi being forced to sell
itself to Amazon).

166 _See Dr. Miles Medical Co. v. John D. Park & Sons Co., 220 U.S. 373 (1911) (holding_
that minimum resale price maintenance agreements violate the Sherman Act). See also Albrecht
v. Herald Co., 390 U.S. 145 (1968) (finding a maximum resale price agreement per se unlawful
under section 1 of the Sherman Act).

167 _See Leegin Creative Leather Prods., Inc. v. PSKS, Inc., 551 U.S. 877 (2007) (overturning_
Dr. Miles’ per se rule and subjecting minimum resale price agreements to the rule of reason);
State Oil Co. v. Barkat U. Khan & Kahn & Associates, Inc., 522 U.S. 3 (1997) (overturning
_Albrecht’s_ per se rule against maximum resale price maintenance agreements and subjecting
such agreements to the rule of reason).

168 _See Matthew L. Powell, A Primer on Resale Price Maintenance, MICH._ BAR J. (2017) (“[A]
number of states continue to treat vertical price fixing as per se unlawful under state laws . . ..”).

35


-----

_DYNAMIC PRICING ALGORITHMS_

manufacturer was unhappy with the prices some retailers charged for its products, either because it believed those prices were too high or too low, it could
intercede, potentially upsetting the pricing structure retailers’ algorithms constructed. However, in situations where non-collusive algorithmic pricing has
resulted in supracompetitive prices across retailers, it seems unlikely that manufacturers would employ resale price maintenance policies that reduced prices
for consumers.

In any event, the restrictions federal and state antitrust laws place on resale
price maintenance should not directly affect retailers’ ability to engage in noncollusive algorithmic pricing, as long as their algorithms are not calibrated to
take into account manufacturer-required price maximums or minimums.

_3._ _Price Discrimination: The Robinson-Patman Act_

The Robinson-Patman Act (RPA) prohibits firms from charging competing customers different prices for goods of “like grade and quality” or discriminating in any “allowances” (typically advertising funds) they provide.[169] Enacted in 1936, the RPA was intended to protect local retailers from encroaching chain stores that, due to their buying power, were able to purchase goods
at a lower price and in turn charge lower prices to consumers.[170]

Like restrictions on predatory pricing and resale price maintenance, it is
possible that the RPA could affect algorithmic pricing policies. It might be
unlawful, for example, for a manufacturer to employ a pricing algorithm that
charged competing customers different prices for the same goods. But such
prohibitions would not ameliorate the generalized harm consumers will suffer
from the higher prices caused by pricing algorithms in competitive markets.

Indeed, none of the restrictions antitrust currently places on pricing strategies directly addresses this specific type of consumer harm. In the absence of
any obvious antitrust solution, direct regulation may the best way to prevent a
massive redistribution of wealth from consumers to sellers.

_B._ Pricing Regulation

Pricing regulation has a checkered history in the United States. Outside of
heavily regulated industries like electric utilities, pricing regulation is generally
disfavored currently.[171] But that has not always been the case, especially when
innovations in pricing technology have upended markets. Algorithmic pricing
represents a sea change in pricing technology that is already redefining the re
169 15 U.S.C. §13(a) and (c) (2012).

170 _See Buyer’s Liability for Inducing Price Discrimination in Absence of Seller Liability, 93 HARV._ L.
REV. 234, 239 (1979) (“The Robinson-Patman Act was enacted to eliminate large buyers’ use
of purchasing power to exact price concessions and thereby gain an advantage over smaller
businesses.”).

171 _See Rockoff, supra note 29 (“[E]conomists are generally opposed to price controls.”)._

36


-----

_DYNAMIC PRICING ALGORITHMS_

lationship between sellers and customers. This type of disruption is not without precedent, however. In the early part of the twentieth century, another set
of pricing innovations transformed retail markets, ultimately leading to regulation to correct what were seen as existential threats to the economy.

_1._ _Disruptive Pricing Technologies: Price Displays and Discounting Strategies_

For centuries prior to the twentieth century, most retail pricing was done
on a customer-by-customer basis. Retailers kept track of what they paid for
goods and determined prices based on those costs.[172] Prices were not listed
or displayed, so individual consumers could bargain with sellers and prices
fluctuated constantly.[173] This lack of pricing transparency also meant that comparison shopping among retailers was nearly impossible for consumers.[174]

A number of factors contributed to the rapid decline of this pricing regime
in the early twentieth century. These included the development of new pricing
technologies, like price cards, and the new pricing strategies that these technologies made possible, like batch sales and loss leaders. The early 1920s saw
an explosion of new price display technologies.[175] The Clamp-Swing Price
Card Holder, for example, was a metal device that was attached to a shelf below the products for sale by means of a metal clamp. It listed the product’s
price and allowed the customer to grab an item off the shelf without knocking
down the display.[176] Clamp-Swing and several competitors, including F.M.
Zimmerman, also developed price displays designed to facilitate batch sales.[177]
The Clamp-Swing batch sale device had two parts, one that described the
amount of a good for sale and the other that stated the price.[178] This design
allowed shopkeepers to easily display an offering of five pounds of potatoes
for 50 cents or three cans of corn for 25 cents and to quickly change those
terms at any time by replacing either the amount or the price card.

172 _See Cochoy, et al., supra note 30 at 577 (at the turn of the twentieth century, retailers_
would mark goods with their costs and use the cost “as a base for bargaining with each individual customer”).

173 _Id. (“[P]rice-cutting was both systematic and limited: every transaction would include a_
price negotiation often ending in a price reduction.”).

174 _Id. (“[P]rice comparisons and the related economic pressures on prices were effectively_
restricted.”).

175 _See id. at 579 (“From the early 1920s, prices spread on the shelves, thanks to the rapid_
development of new price tag devices promoted by several companies.”).

176 Clamp-Swing Pricing Company, _History of Clamp-Swing Pricing Company,_
http://www.clampswing.com/about-us.php (describing Clamp-Swing Price Card Holders
and noting that they “created a minor revolution in the 1920s in the price marking field”).

177 Cochoy, et al. supra note 30 at 579-80.

178 _Id. at 580._

37


-----

_DYNAMIC PRICING ALGORITHMS_

Pricing card companies created similar displays for “specials,” which allowed retailers to implement pricing strategies based on loss leaders.[179] The
idea was to strategically pick certain goods and assign them a low price to get
customers into the store, where they might buy additional items at a more
profitable price.[180] If well executed, the loss-leader strategy could convince
consumers that the retailer’s prices were low overall.

These new pricing technologies and strategies had several important ramifications. First, as Professors Franck Cochoy, Johan Hagberg, and Hans Kjellberg have argued, retail prices shifted from being flexible and set on an ad hoc
basis for individual customers to being fixed for all of a seller’s customers.[181]
Second, public pricing displays made comparison shopping much easier for
consumers.[182] For the first time, retailers felt sustained pricing pressure based
not only on their own costs, but also on their competitors’ prices.[183] Third,
this new competitive environment, combined with pricing strategies that emphasized discounting—through batch sales and specials—led to a period of
intense retail price reductions and deflation.[184]

These changes were taking place in the period leading up to and during the
first years of the Great Depression, exacerbating what were seen as the perils
of systematic price cutting and “cut-throat competition.” Contemporary policy experts warned against the evils of overly aggressive price competition.
Speaking at an advertising convention in 1933, General Hugh S. Johnson, who
would become the head of the Roosevelt administration’s National Recovery
Administration, asserted that “[g]ood advertising is opposed to senseless price
cutting and to unfair competition[,] . . . two business evils which we hope to
reduce under the plan of the new administration.”[185] Johnson advised that
“[c]onstructive selling competition will be as strong as ever” and “[t]he only
kind of competition that is going to be lessened is the destructive cut-throat
kind of competition which harms the industry and the public as well.”[186] Manufacturers were especially unhappy about retailers’ new price-cutting strategies,

179 _Id. at 582._

180 _Id._

181 _Id. at 578 (“During the bargaining era, prices were fully flexible . . . prices were adjust-_
able, but at the individual level only. . .. With the new price display regime, prices were largely
available . . ., but at the expense of becoming more fixed. . .. [P]rices were now the same for
every customer and worked according to a new ‘take it or leave it’ logic. . ..”).

182 _Id. at 577 (“[O]pen prices . . . offer[ed] both commercial appeal and a basis for price_
comparison and competition.”).

183 _Id. at 579 (“While the displayed prices might be fixed within the store during any given_
day, their fixity was challenged [] from the outside, via price competition.”).

184 _Id. at 586 (“[A]t the level of the aggregated economy . . . [p]rice cuts started a vicious_
circle of price competition that contributed, if not to creating, at least accelerating deflation.”).

185 Hugh S. Johnson, Speech Before the Advertising Fed. of Am. (June 1933).

186 _Id._

38


-----

_DYNAMIC PRICING ALGORITHMS_

which they viewed as undermining public confidence in the true value of their
goods.[187]

Within years of the introduction of these novel pricing technologies and
strategies, a widespread sentiment developed that price-cutting and deflation
were out of control and that legislative or regulatory responses were necessary
to stabilize the situation. Manufacturers supported legislation in the 1910s,
1920s, and early 1930s that would have allowed them to engage in resale price
maintenance, which at the time was per se unlawful under the antitrust laws. [188]
In 1927, the FTC launched an “economic investigation” into “the practice of
resale price maintenance” that was supported by the U.S. Chamber of Commerce.[189] The investigation’s goals included determining “the causes and motives for price cutting” and “how far price cutting has eliminated manufacturers and distributors from business.”[190]

Ultimately, these efforts at addressing falling prices through resale price
maintenance legislation failed to come to fruition. Instead, the new Roosevelt
administration attacked the problem through the industrial codes of the National Recovery Administration. The National Industrial Recovery Act of 1933
invited trade and industrial organizations to submit to the President for his
approval “codes of fair competition.”[191] The Act stated that “[w]henever the
President shall find that destructive wage or price cutting or other activities
contrary to the policy of this title are being practiced in any trade or industry,”
such that the President deems it “essential to license business enterprises in
order to make an effective code of fair competition,” no firms could carry on
business in that industry absent a license.[192]

More than 500 industries ultimately adopted these codes, most of which
limited price cutting and set minimum prices.[193] For example, the Code of
Fair Competition of the Cotton Textile Industry stated that the Cotton Textile

187 Cochoy, et al. supra note 30 at 590 (noting the sentiment in the early 1930s that “manufacturers . . . lost goodwill because low prices were raising doubts as to the real value and
quality of their products”).

188 _See, Comment, Resale Price Maintenance and the Anti-trust Laws, 18 U._ CHI. L. REV.
369, 371 (1951) (from 1914 to 1932 “repeated efforts were made to pass federal legislation
legalizing resale price maintenance agreements in interstate commerce”).

189 _See Commissioner Abram F. Myers, Memorandum of Economic Investigation of Fed._
Trade Comm’n 1, 8-9 (Dec. 12, 1927), https://www.ftc.gov/system/files/documents/public_statements/673541/19271212_myers_memorandum_re_economic_investigations_of_ftc.pdf.

190 _Id. at 16._

191 National Industrial Recovery Act of 1933, Pub. L. 73-67, Title I, Section 3 (1933).

192 _Id. at Title 1, Section 4(b)._

193 _See, Harold L. Cole & Lee E. Ohanian,_ _New Deal Policies and the Persistence of the Great_
_Depression: A General Equilibrium Analysis, Fed. Reserve Bank of Minneapolis 7-9 (2001) (“Min-_
imum price was the most widely adopted provision” in the Codes of Fair Competition”).

39


-----

_DYNAMIC PRICING ALGORITHMS_

Industry Committee would make recommendations to the NRA administrator
regarding “the naming and reporting of prices which may be appropriate . . .
to prevent and eliminate unfair and destructive competitive prices and practices.”[194] The Code of Fair Competition for the Electrical Manufacturing Industry required producers to submit current pricing information and barred
them from charging prices below those submitted.[195] Many of these codes forbade producers to charge prices below their costs.[196] The NIRA exempted
these codes from the antitrust laws.[197]

The U.S. Supreme Court invalidated the NIRA in 1935,[198] but for two
years, the Act transformed pricing policy in the United States in an attempt to
reverse the deflationary trends caused in part by the new pricing technologies
and strategies developed in the 1910s and 1920s. This episode demonstrated
the potential for swift regulatory responses to the perceived negative consequences of advances in pricing techniques. Algorithmic pricing presents a very
different challenge than that posed by price cards and loss leaders. Rather than
lowering prices for consumers, the concern is that algorithmic pricing is raising
retail prices. Therefore, even if one believed that industry-wide price floors and
prohibitions on discounting were effective policies in the 1930s, they are certainly not the correct tools for the current era, though their analog, price caps
or price controls, might be.

_2._ _Price Controls_

Despite its general dedication to free market principles, there is a robust
history of price controls in the United States, especially during emergency periods. Price controls were implemented during both World Wars and the Korean War, for example, periods where there was widespread concern about
rampant inflation.[199] Other familiar forms of price controls include the minimum wage (setting a floor on the price of labor), rent control (setting a ceiling
on the price of housing), and anti-usury laws (setting a ceiling on interest

194 National Recovery Administration Codes of Fair Competition, Vol.1 at 17 (1933),
http://moses.law.umn.edu/darrow/documents/codes_fair_competion_vol_1.pdf.

195 _Id. at 50-51._

196 _See, e.g., Code of Fair Competition for the Compressed Air Industry, id. at 655 (“No_
employer shall sell or exchange any product of his manufacture at a price or upon terms and
conditions that will result in the customer paying for the goods received less than the cost to
the seller.”).

197 National Industrial Recovery Act of 1933, Pub. L. 73-67, Title 1, Section 5.

198 _See A.L.A. Schechter Poultry Corp. v. U.S., 295 U.S. 495, 541-42 (1935) (striking down_
the NIRA on the ground that it represented an unconstitutional delegation of legislative power
to the President).

199 _See Rockoff, supra note 29._

40


-----

_DYNAMIC PRICING ALGORITHMS_

charged on loans). In the 1970s, the federal government twice placed price
caps on gasoline.[200]

The most sweeping recent example of a price control regime in the United
States is the Nixon administration’s New Economic Policy, which froze prices
and wages for a 90-day period in 1971 and again in 1973. In 1970, Congress
had passed the Economic Stabilization Act, which gave the president the authority to “issue such orders and regulations as he may deem appropriate to
stabilize prices, rents, wages, and salaries at levels not less than those prevailing
on May 25, 1970.”[201] The Nixon administration enacted the New Economic
Policy as a response to fears about out-of-control inflation and rising unemployment.[202] It created the Cost of Living Council, which oversaw two components: the Price Commission—which dealt with price increases—and the
Pay Board—which dealt with wage increases. The New Economic Policy initially had a great deal of popular support and was viewed as a bold response to
a growing national crisis.[203] The Policy led to some short-term political successes for President Nixon, but ultimately it was judged by many to have failed
at its central task of controlling inflation.[204]

Price controls continue to be considered a viable regulatory tool. Indeed,
price controls recently have been proposed as a way to address the high costs
of certain drugs. In 2019, the U.S. House of Representatives passed a bill that
would require the U.S. Department of Health and Human Services to negotiate
maximum prices for certain drugs, including insulin and drugs that do not face
generic competition.[205] The bill mandates that the negotiated price for these
drugs not exceed either 120 percent of the price paid in six countries that have
drug price controls or, if pricing information from those countries in unavailable, 85 percent of the U.S. average manufacturer price.[206]

It is likely unsurprising that most economists view price controls with disfavor.[207] In the orthodox view, direct government intervention in markets is
typically ineffective and results in dangerous economic distortions such as

200 _Id._

201 The Economic Stabilization Act of 1970, Sec. 202, Pub. L. 91-379 (Aug. 15, 1970).

202 _See Exec. Order No. 11615, 36 Fed. Reg. 15727, 15727 (Aug. 15, 1971) (stating that the_
purpose of the Order is to “stabilize the economy, reduce in inflation, and minimize unemployment”.)

203 _See Rocco C. Siciliano, The Nixon Pay Board—A Public Administration Disaster, 62 PUB._
ADMIN. REV. 368, 368 (2002) (describing the New Economic Policy as a “bold—perhaps
drastic—move” that “delighted the country”).

204 _Id. at 373_ (arguing that the New Economic Policy “stymied inflation” through the 1972
election, but that the “nation suffered for it” and “by 1974 inflation was on a rampage”).

205 H.R. 3, The Elijah E. Cummings Lower Drug Costs Now Act, Title I, Sec. 1191.

206 _Id._

207 _See Rockoff, supra note 29 (“[E]conomists are generally opposed to price controls.”)._

41


-----

_DYNAMIC PRICING ALGORITHMS_

shortages of a good whose price is capped or surpluses of a good whose price
is supported by a price floor.[208] Price controls also often lead to rationing and
black markets.[209] If they support them at all, economists view price controls as
appropriate only during short-term emergencies.[210]

The higher prices algorithms can cause are likely neither an emergency
(compared to wartime price-gouging, for example), nor short-term, as it seems
likely that algorithmic pricing is here to stay. Further, price controls are a blunt
instrument that would prove unwieldy in addressing the thousands of markets
and millions of products potentially affected by algorithmic pricing.[211] A price
control regime would require standing up a new bureaucracy to set prices and
would result in a long-term, massive expansion of the federal government’s
role in the market. These ramifications counsel against price controls and towards a more targeted solution, one that would be directed specifically at markets where algorithmic pricing is leading to higher prices and reducing consumer welfare. In short, the most effective approach to the challenges algorithmic pricing raises likely is one that would regulate the algorithms themselves.

_C._ Regulating Algorithmic Pricing

Pricing algorithms create several risks for competition and consumers,
some of which antitrust law can address and some of which might require
regulatory solutions. Firms can use pricing algorithms to facilitate explicit collusion, like price-fixing. These types of schemes are subject to criminal sanction under section 1 of the Sherman Act.[212] Pricing algorithms also might allow
firms to more effectively engage in tacit collusion, conduct that currently falls
outside the bounds of antitrust law.[213] As discussed above, scholars have proposed expanding the antitrust laws to reach tacit collusion and also have recommended regulatory interventions.[214] There is no question that the conduct
this Article focuses on—non-collusive algorithmic pricing competition—falls
outside the reach of the antitrust laws, even broadly conceived. Still, pricing

208 _Id. (“The reason most economists are skeptical about price controls is that they distort_
the allocation of resources.”).

209 _Id._

210 _Id. (asserting that economists generally oppose price controls “except perhaps for very_
brief periods during emergencies”).

211 One source estimated Amazon.com to have an inventory of 12 million products. Including third-party Marketplace sellers, this figure balloons to over 350 million products.
https://www.repricerexpress.com/amazon-statistics/.

212 _See supra note 25._

213 _See_ In re Text Messaging Antitrust Litig., 782 F. 3d 867, 879 (7th Cir, 2015) (“Tacit
collusion . . . does not violate Section 1 of the Sherman Act.”).

214 _See supra notes 27-28 and accompanying text._

42


-----

_DYNAMIC PRICING ALGORITHMS_

algorithms can harm consumers by allowing competing firms to charge supracompetitive prices even absent collusion.

As explained above, the two key characteristics that empower pricing algorithms to facilitate higher prices are asymmetries in pricing frequency and
the ability to commit to an automated price response to changes in rivals’
prices. Accordingly, an effective regulatory approach might be based on eliminating one or both of these characteristics. This would mean either barring
asymmetries in pricing frequency or prohibiting firms from incorporating rivals’ pricing in their algorithms. The following subparts discuss these interventions.

_1._ _Regulating Pricing Frequency_

Recall that when variations in the sophistication of pricing technologies
create asymmetries in pricing frequency, firms will adopt a leader-follower
pricing pattern.[215] Firms with more advanced technology will undercut firms
with inferior technology and all firms will price above the competitive level.
The key to this arrangement is the understanding among firms with inferior
pricing technology that whatever price they set for a particular period can be
beaten by firms that price more often. Their incentive to compete on price
therefore is blunted. But if the asymmetry was eliminated, firms in healthy
markets would resume vigorous price competition.

One way to achieve this goal would be to regulate when firms can set
prices. For example, regulations could require firms to price only once a day
or only once a week and to do so at the same time every day or every week. In
that scenario, it would be difficult to establish a leader-follower pattern and
firms would be incentivized to propose their best price every period. Algorithms still would have a role to play in this regulatory regime: firms could
program their algorithms to account for the same factors they do now, including supply and demand, market prices, consumer preferences, and seasonality,
and firms with superior technology still might win more customers. But sellers
with inferior pricing technology no longer would be de-incentivized to cut
prices and, in well-functioning markets, all firms would charge prices closer to
the competitive level.

Further, though regulating pricing frequency would not directly address
the second key feature of algorithms—commitment to react to rivals’ price
changes—it can eliminate the ability of firms to employ strategies that appear
competitive but generate higher prices, drawing a clearer line between competitive and collusive conduct. By making the time between price changes long
enough, firms’ algorithms would have to incorporate large, discrete punishments to support higher prices. These punishments would be easily detectable
by regulators and consumer groups.

215 _See supra Part II.B._

43


-----

_DYNAMIC PRICING ALGORITHMS_

Regulators have employed restrictions on asymmetric pricing before. In
both Austria and Western Australia, governments imposed regulations on the
frequency of price changes in retail gasoline markets. The goal of these regulations was to decrease price volatility in markets where price changes were
common and consumers wanted increased price transparency.[216] The Austrian law, enacted in 2009, limited gas stations to increasing their prices only
once a day, though they could decrease prices as often as they wanted.[217] Price
increases could be initiated only at certain times of day, depending on the hours
the gas station was open. So, for example, gas stations that were open 24 hours
a day had to make any price increases at midnight.[218] In 2011, the law was
revised to require all gas stations to make any price increases once a day at
noon.[219] The Austrian law also mandated that every gas station post its prices
on a public website so consumers could comparison shop.[220]

The pricing program in Western Australia was instituted pursuant to the
Petroleum Products Pricing Act of 1983, as amended in 2000-2001.[221] Under
the auspices of this law, the Western Australian government created the
FuelWatch program, which was designed to increase price transparency for
consumers.[222] These rules require gas stations to notify regulators of their pricing for the following day by 2 pm every day; to keep prices the same for every
24-hour period starting at 6 am; and to display their prices on “roadside price
boards.”[223] These prices are also posted on the FuelWatch website.

While these Austrian and Western Australian regulations succeeded in increasing pricing transparency for consumers, there was concern among economists that they might also raise the likelihood of collusion among gas stations,
leading to higher prices. Two experimental studies predicted that the Austrian
law would result in increased gas prices, though one of those studies found
that the Western Australian regulation would not have a significant impact on
pricing.[224] An empirical study of both sets of regulations, however, concluded

216 _See,_ _e.g.,_ FuelWatch, _Legislative_ _Framework,_
https://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/contentholder.jspx?key=legal.html (noting Western Australian “motorists’ frustration at intra-day price fluctuations . . .”).

217 _See Dewenter & Heimeshoff, supra note 40 at 4 (describing 2009 Austrian pricing regu-_
lation for gas stations).

218 _Id._

219 _Id._

220 _Id._

221 _See_ FuelWatch, _Legislative_ _Framework,_
https://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/contentholder.jspx?key=legal.html.

222 _Id. (explaining how the FuelWatch program strives “to achieve its goal of price trans-_
parency”).

223 _Id._

224 _See Dewenter & Heimeshoff, supra note 40 at 4 (describing experimental studies)._

44


-----

_DYNAMIC PRICING ALGORITHMS_

that gas prices in Austria fell after the pricing regulation was implemented, and
that there were no significant changes to gas prices in Western Australia due
to the FuelWatch program.[225]

Restrictions on when firms price have been proposed for other markets
where advances in technology appear to harm consumers. Professors Eric
Budish, Peter Cramton, and John Shim have argued that what they call the
high-frequency trading “arms race” in financial markets results in increased
costs to provide liquidity and that those costs are passed on to customers in
the form of higher bid-ask spreads on trades.[226] They trace this problem to
what they describe as “a basic flaw in the design of modern financial exchanges: continuous-time trading.”[227] Today’s financial exchanges operate using a continuous limit order book design, which allows trades to be made continuously and at any time. Firms are competing to trade ever-faster, and indeed
speeds are increasing. But this dimension of competition, the authors assert,
is not beneficial for most investors and leads to increased liquidity costs.[ 228]
Because competition will not address the issue, the authors propose regulating
when firms can trade. Rather than allowing continuous trading, they argue for
“frequent batch auctions,” which happen at discrete times during the trading
day. In this system, all trade requests that arrive during a particular time period
would be treated as having arrived at the same time for purposes of the auction.[229] As a result, speed would matter less and firms would compete purely
on price, lowering costs for consumers.[230]

In addition to the concerns about collusion noted above, policy makers
and firms might object to this type of regulatory intervention on the ground
that it reduces incentives to innovate in pricing technologies. As we argue below, however, we believe that developments in pricing algorithms represent

225 _Id. at 15 (describing results of empirical study showing that the Austrian pricing rule_
“has a significant negative effect on fuel price levels” but that the authors could not “find
statistically significant effects of the [Western Australian] fuel price regulation on price levels”).
_But see David P. Byrne & Nicolas de Roos, Learning to Coordinate: A Study in Retail Gasoline, 109_
AM. ECON. REV. 591, 592 (2019) (reporting results of empirical study finding “a substantial
increase in [retail gas stations’] margins” in wake of Western Australian pricing regulation).

226 _See_ Eric Budish, Peter Cramton & John Shim, _The High-Frequency Trading Arms Race:_
_Frequent Batch Auctions as a Market Design Response, 130_ QUARTERLY J. ECON. 1547, 1554 (2015)
(arguing that “arbitrage rents” caused by high-frequency trading “increase the cost of liquidity
provision” and that such costs are “incorporate[d] . . . into the bid-ask spread that [trading
firms] charge”).

227 _Id. at 1549._

228 _Id. at 1555 (“[C]ompetition in speed does not fix the underlying problem . . ..”)._

229 _Id. at 1549._

230 _Id._ at 1556 (arguing that frequent batch auctions “reduce[] the value of a tiny speed
advantage, which eliminates the arms race” and results in traders being “forced to compete on
price instead of speed”).

45


-----

_DYNAMIC PRICING ALGORITHMS_

what we call “extractive innovation” that, while undeniably constituting technological progress, harms rather than helps consumers.[ 231] Accordingly, policy
makers should be less concerned about regulations that de-incentivize advancements in pricing algorithms than they would be about other policies that
blunt innovation incentives. Recall too that currently firms with inferior pricing technology generally have no incentive to upgrade.[232] These firms typically
prefer to have less sophisticated technology because the disparity among rival
technologies creates the asymmetries that allow all firms to price above the
competitive level.

Another likely objection to this type of regulation is that limiting when
firms can price restricts their ability to be nimble and respond quickly to changing market conditions. This argument is not without merit. In a market with
competitive prices, enabling firms to adjust prices as often as they like would
allow them to efficiently respond to changes in supply and demand. But, as
Brown and MacKay demonstrate, asymmetries in pricing algorithms distort
prices away from competitive levels. Firms with superior technologies re-price
more often—in some cases, many times a day—but can still price above the
competitive level.[233] In markets where non-collusive algorithmic pricing has
this effect, consumers would benefit from increased competition and lower
prices if firms were required to price simultaneously.

Further, in many cases, variation in supply and demand is predictable in
advance. For example, in ridesharing markets, demand increases during rush
hour and after sporting events. In these markets, firms may be permitted to
choose a price schedule to specify how rates change over time—e.g., every 30
minutes—but this schedule would be set at a lower frequency, such as once a
day or once a week.[234] Such a regulation would prevent asymmetries in frequency that soften price competition. Though firms pricing in this manner
would not be able to adjust to unpredictable within-day swings in demand and
supply, we suspect that, in most cases, consumers would benefit.

231 Professor Ramsi Woodcock has introduced the concept of “extractive technologies,”
which he defined as “new technologies that facilitate the related practices of price discrimination [and] dynamic pricing.” Letter from Ramsi Woodcock, Assistant Professor of Law, University of Kentucky College of Law, to Office of the Secretary, Fed. Trade Comm’n (Oct. 14,
2018) (on file with authors). Our conception of “extractive innovation” is broader than Professor Woodcock’s categorization. We define “extractive innovation” as any technological
advance that harms rather than helps consumers by transferring wealth from consumers to
sellers. Pricing algorithms are the example we explore in this Article, but we believe that
“extractive innovation” could describe a range of anti-consumer innovations.

232 _See Brown & MacKay, supra note 13 at 22 (a firm with inferior pricing technology “has_
a disincentive to upgrade its technology to match that of” a firm with superior pricing technology).

233 _Id. at 9-11, 39-40._

234 In a key distinction from commitment through an algorithm, prices would not adjust
within a day to reflect the prices of rivals.

46


-----

_DYNAMIC PRICING ALGORITHMS_

A concern with any new regulatory program is its expense and administrability. In some respects, restrictions on asymmetric pricing frequency would
be relatively easy to enforce. Regulators would not need to take on the timeconsuming task of carefully evaluating the functionality of individual firms’
algorithms, they would only have to police when pricing takes place. It would
not be easy to evade these regulations, though the regulator would need to
expend resources monitoring the markets it oversees for compliance. Challenges presented by this type of regulation include identifying markets affected
by algorithmic pricing and choosing an appropriate pricing frequency for each
market. In each identified market, regulators would need to determine a schedule, or maximum frequency, for when firms can adjust prices. The goal would
be to limit the frequency sufficiently to increase competition, while still allowing prices to adjust to changing market conditions. We conjecture that, for
many consumer products, limiting price changes to once per day would enhance competition and not generate significant costs. However, making these
determinations could be difficult and resource intensive.

Nonetheless, the Austrian and Western Australian experiences restricting
pricing frequency for retail gas demonstrate that this type of regulatory intervention can be implemented successfully. The goals of those programs (increased transparency) were different than the aims such a regulatory intervention would have for markets subject to algorithmic pricing (returning prices to
competitive levels). But these real-world examples of regulatory regimes established to limit asymmetries in pricing frequency provide a road map for how
such regulations could be developed and enforced in markets where algorithmic pricing harms consumers.

_2._ _Prohibiting Reliance on Rivals’ Prices_

Another regulatory intervention that likely would ameliorate the consumer
harm non-collusive algorithmic pricing causes is to bar firms from incorporating rivals’ prices in their algorithms. Asymmetric pricing is a problem only to
the extent that firms with superior pricing technology can reference and undercut their competitors’ prices. If that practice was outlawed, concerns about
asymmetries in pricing frequency and commitment would recede. Pricing algorithms still would have a great deal of data to work with, even without rivals’
prices, including supply and demand conditions, consumer characteristics and
preferences, and seasonal conditions, such as the time of year and time of day
a purchase is made. And to the extent firms are concerned about responding
quickly to market conditions, this intervention would allow re-pricing at any
time and with any frequency.

The downside to this proposal is that it might reduce firms’ ability to compete on price. Firms typically compete on a variety of product characteristics,

47


-----

_DYNAMIC PRICING ALGORITHMS_

but especially price.[235] Economic theory indicates that sophisticated firms can
predict the prices that their rivals will choose, leading to competitive prices
even when firms cannot actually observe rivals’ prices. These predictions require detailed knowledge about demand and rivals’ costs, however. In practice,
firms do not always have such rich knowledge and may rely on the information
obtained from observed prices.[236] Whether the loss of this information raises
or lowers prices is ambiguous, but it is possible that this will cause some firms
to increase prices.

Another objection to this intervention is that it would be difficult to police.
Regulators would have relatively easy visibility into when firms price, simplifying enforcement of a regulation barring asymmetric pricing frequency, but it
would be difficult for them to determine how firms are pricing and if an algorithm is referring to rival firms’ prices. Enforcement likely would require firms
to submit their algorithms to the relevant regulator to ensure that they are not
relying on competitors’ prices.[237] Absent such a mandate, firms will have a
strong incentive to evade the regulation so they can gain market share and
charge supracompetitive prices. Enforcing this type of regulation would require standing up a new bureaucracy to review pricing algorithms, increasing
the size, power, and expense of government.

Indeed, some scholars have advocated for the creation of a centralized algorithm regulator.[238] Such an entity would oversee a large body of algorithms,
including those that set bail, determine insurance rates, choose among job candidates, and suggest potential romantic partners. In many cases, this regulator
would be tasked with rooting out pernicious racial and gender bias in algorithms. But such a regulator also could oversee pricing algorithms. In all these
contexts, firms (and governmental agencies, in some cases) would submit their
algorithms to the regulator for review.[239] This regulatory agency potentially

235 _See Fed. Trade Comm’n, Competition Counts: How Consumers Win When Businesses Compete,_
https://www.ftc.gov/sites/default/files/attachments/competition-counts/zgen01.pdf
(“[P]rice is usually the principal basis for competition and consumer choice.”).

236 In our proposal, we would allow firms to indirectly respond to historical prices by tuning the parameters of their algorithms. This would, in principle, lead to competitive prices in
markets where demand and supply conditions are stable over time, but may not if conditions
fluctuate often.

237 A relevant question is whether firms could hire enough employees to monitor and manually adjust prices in a manner similar to an algorithm. Given the vast number of products
sold online by individual retailers, we do not find this possibility particularly realistic.

238 _See, e.g., Andrew Tutt, An FDA for Algorithms, 69 ADMIN._ L. REV. 83, 115 (2017) (“The
case for regulation by a single expert agency outweighs the case for regulation by the states or
jurisdiction distributed across multiple agencies because algorithms have qualities that make
centralized federal regulation uniquely appealing.”).

239 _Id. at 122 (“Rather than wait for an algorithm to harm many people, we might take the_
FDA's history as a lesson and instead develop an agency now with the capacity to ensure that
algorithms are safe and effective for their intended use before they are released.”).

48


-----

_DYNAMIC PRICING ALGORITHMS_

would face the massive task of evaluating all algorithms in use across the private and public sectors. In this context, reviewing pricing algorithms to determine if they are relying on competitors’ prices would seem a relatively simple
task, compared, for instance, to evaluating whether an algorithm produces biased results, especially if that bias is unintentional.[240] Nonetheless, as algorithmic pricing spreads across markets, as it is likely to do, reviewing all pricing
algorithms will be a significant lift. Further, firms will still be incentivized to
evade this regulation, because relying on their rivals’ prices will allow them to
charge prices above the competitive level. This threat will add policing and
enforcement to the regulator’s plate.

In the absence of regulation, consumers may change their behavior in response to higher prices brought about by pricing algorithms. For example,
consumers may adopt algorithmic tools to detect lower prices or increase their
use of price comparison websites. These strategies may provide an avenue to
mitigate some of algorithms’ price effects, to the extent that they reduce search
costs and make consumers more likely to choose websites offering the lowest
prices. Thus, consumers cannot counter the effects of algorithms directly, but
they can invest in tools that make them more price responsive. However, even
if these tools become more prevalent, the potential effects of algorithms that
remain may make regulation an appealing policy solution.

Deciding which regulatory intervention makes the most sense to address
the problems non-collusive algorithmic pricing presents is not an easy task.
The interventions we discuss in this Part—restricting pricing frequency and
prohibiting algorithms from incorporating rivals’ prices—present clear
tradeoffs. Regulations on pricing frequency limit firms’ ability to react quickly
to shifting market conditions but allow them to rely on the full menu of data
inputs, including rivals’ prices, when setting price. This type of regulation is
probably the easier of the two approaches to implement and administer. These
regulations would be difficult to evade and do not require an agency to carefully study individual algorithms. Prohibiting algorithms from relying on rivals’
pricing places no limits on firms’ ability to react nimbly to market conditions
(other than changes in their competitors’ prices). Firms would be able to adjust
their prices whenever they see fit. But pricing without reference to competitors’ prices could raise prices in some cases. And implementing this type of
regulation will be expensive and greatly expand the role of government. The
proliferation of algorithms across society may make such a regulatory expansion inevitable, but it is an added cost to consider when comparing solutions
to the algorithmic pricing problem.

Based on what we know currently about algorithmic pricing, a regulatory
scheme that limits when firms price, rather than one that restricts how they
price, is appealing for typical markets. We believe that this approach would be

240 _See Jason R. Bent, Is Algorithmic Affirmative Action Legal?, 108 GEO._ L. J. 803, 806 (2020)
(“The basic problem of unintentional algorithmic bias is by now well recognized.”).

49


-----

_DYNAMIC PRICING ALGORITHMS_

equally effective but less expensive and less intrusive than one that directly
regulated firms’ algorithms. Further, there are already real-world models
demonstrating that regulating pricing frequency is an administrable reform that
can help consumers. That being said, widespread use of pricing algorithms is
a relatively new phenomenon. Any definitive conclusions about whether and
how to regulate markets where pricing algorithms are harming consumers may
have to wait until society gains additional experience with these technologies
and further empirical evidence on their impact emerges.

_3._ _Innovation Effects_

In addition to their other strengths and weaknesses, both regulatory approaches to algorithmic pricing share the risk of dulling innovation incentives
for pricing technologies. Restricting pricing frequency reduces the incentive
to create faster algorithms, while barring algorithms from considering rivals’
prices softens incentives to develop more sophisticated price competition
strategies. Competition policy typically aims to enhance innovation, not dull
it. However, we contend that pricing algorithms are an exception to this general rule and that they represent a form of “extractive innovation” that competition policy should not encourage.

Enhanced innovation is well understood to be a central goal of competition policy.[241] In general, more competitive markets are thought to produce
more innovation, while restraints on competition are viewed as likely to reduce
innovation.[242] Not surprisingly, courts, enforcers, and antitrust scholars remain focused on identifying conduct that might threaten innovation.[243]

241 Makan Delrahim, Ass’t Att’y Gen., U.S. Dept. of Justice, Antitrust Division, _“Video_
_Killed the Radio Star”: Promoting a Culture of Innovation (Oct. 8, 2020), https://www.jus-_
tice.gov/opa/speech/assistant-attorney-general-makan-delrahim-delivers-remarks-47th-annual-conference (stating that the Antitrust Division of the U.S. Department of Justice “is committed to ensuring that competition policy remains a force for good in fostering innovation.”)

242 _See, e.g., U.S._ DEP’T OF JUSTICE & THE FED. TRADE COMM’N, HORIZONTAL MERGER
GUIDELINES at 23 (Aug. 19, 2010), https://www.ftc.gov/sites/default/files/attachments/merger-review/100819hmg.pdf (“Competition often spurs firms to innovate.”); Giulio
Federico, Fiona Scott Morton, and Carl Shapiro, Antitrust and Innovation: Welcoming and Protecting
_Disruption, in INNOVATION POLICY AND THE ECONOMY 20, 125 (Josh Lerner & Scott Stern,_
eds.) (2020) (“Competition promotes innovation” as “[e]ffective rivalry spurs firms to introduce new and innovative products”, and exclusionary conduct by a dominant firm “suppresses
innovation by foreclosing disruptive rivals and by reducing the pressure to innovate on the
incumbent”).

243 _See, e.g., U.S. v. Microsoft Corp., 147 F. 3d 935, 948 (D.C. Cir. 1998) (“[A]ny dampening_
of technological innovation would be at cross-purposes with antitrust law.”); C. Scott
Hemphill & Tim Wu, Nascent Competitors, 168 U. PENN. L. REV. 1879, 1881 (2021) (outlining
a “program of antitrust enforcement” to protect “prospective innovation by [] future direct
competitor[s]” of firms possessing market power).

50


-----

_DYNAMIC PRICING ALGORITHMS_

This goal of promoting innovation does not exist in a vacuum, however.
Innovation is considered valuable because it is thought to benefit consumers.[244] Contemporary competition policy and antitrust theory is centered on
the concept of consumer welfare.[245] But what if the innovation in question
_reduces consumer welfare? As Professor Tim Wu has noted, antitrust scholar-_
ship suffers from a “serious failure to explain what kind of innovation antitrust
should try to encourage” and that generally “the concept” has been “left
vague.”[246] Professor Wu was referring to the distinction between large-scale
industrial innovation and “small-firm, decentralized innovation,” but the point
applies more broadly too.[247] The Horizontal Merger Guidelines and other
antitrust agency guidance tend to refer generally to innovation as an unalloyed
good to be encouraged. Pricing algorithms’ impact on consumer welfare raises
serious questions about this undifferentiated approach.

The closest antitrust law has come to addressing the possibility of harmful
innovation is in cases involving claims of predatory product design. In these
types of disputes, plaintiffs are often third-party producers of products that
interconnect with a monopoly product. If the monopolist changes its offering
such that third-party interconnection becomes more difficult, more expensive,
or simply impossible, those producers might claim that the monopolist harmed
competition by unlawfully excluding its competitors. The key issue in these
product design cases is whether the product change at the heart of the dispute
could be characterized as a genuine innovation. Courts generally have found
no antitrust problem if the defendant’s changes to the relevant product represent an “improvement.”[248] Put another way, there is only an antitrust issue with
a product design change if it involves no innovation.

244 _See Federico, et al., supra note 243 at 125-26 (“Competition policy seeks to protect and_
promote a vigorous competitive process by which new ideas are transformed into realized
consumer benefits.”).

245 _See, e.g., Brooke Group Ltd. v. Brown & Williamson Tobacco Corp., 509 U.S. 209, 221_
(1993) (noting “the antitrust laws' traditional concern for consumer welfare and price competition.”); Jacobs v. Tempur-Pedic Intern., Inc., 626 F.3d 1327, 1339 (11th Cir. 2010) (“[C]onsumer welfare, understood in the sense of allocative efficiency, is the animating concern of the
Sherman Act.”).

246 Tim Wu, Taking Innovation Seriously: Antitrust Enforcement if Innovation Mattered Most, 78
ANTITRUST L. J. 313, 315 (2012).

247 _Id. at 315-316._

248 _See, e.g., In re IBM Peripheral EDP Devices Antitrust Litig., 481 F. Supp. 965, 1004_
(N.D. Cal. 1979), aff'd, 698 F.2d 1377 (9th Cir. 1983) (holding that plaintiff “will not be
heard to complain that it was somehow injured by an improved product”).

51


-----

_DYNAMIC PRICING ALGORITHMS_

Under this “improvement” standard, the advances in pricing algorithms
discussed above undoubtedly qualify as innovation. Pricing algorithms are becoming faster and able to incorporate increasing amounts of data.[249] These are
certainly improvements for direct consumers of the algorithms, whether these
consumers are in-house or purchase an algorithm on the open market. Further,
in most cases, firms do not use improvements in pricing algorithms to exclude
competitors in the antitrust sense. They might rely on the algorithm to beat
their rivals’ prices, but as long as those prices are not predatory, this is not an
antitrust violation. Winning market share through a superior pricing algorithm, even when that innovation harms consumers of the products the algorithm prices, has no antitrust remedy under current law.

Antitrust therefore has no doctrinal answer for what to do about innovations that, while genuine improvements, harm consumer welfare. It is also
worth highlighting that the consumers harmed in this scenario are not direct
purchasers of pricing algorithms. Firms that employ pricing algorithms, as well
as their rivals, benefit from advances in algorithmic technology. Innovation in
pricing algorithms, when spread unequally among firms, creates the asymmetries that facilitate supracompetitive pricing even in competitive markets.[250]
The harm to retail consumers is a result of the advantages pricing algorithms
confer on retailers.

While antitrust may not be best equipped to address issues raised by innovations that harm consumers, regulators are more familiar with this scenario
and are better able to deal with it. It is not uncommon for firms that produce
dangerous products to improve them (i.e., innovate) so that they become more
effective and therefore more dangerous. Certain genuine improvements to
tobacco consumption devices, guns, and even cars, for example, make these
products more harmful for consumers and the broader public, sometimes
prompting regulators to ban or limit the effects of these improvements despite
their innovative character.[251]

Consider, for example, flavored e-cigarettes. E-cigarettes are devices that
allow individuals to ingest nicotine and other chemicals without smoking tobacco. According to the Center for Disease Control and Prevention (CDC), ecigarettes might have positive health benefits for adult smokers if they use

249 _See Zhou, supra note 20 (“As algorithms become more powerful and more data becomes_
available, companies’ product and service prices can automatically respond to demand and competition in real time.”).

250 _See supra Part II.B._

251 _See James Niels Rosenquist, Fiona M. Scott Morton & Samuel N. Weinstein, Addictive_
_Technology & its Implications for Antitrust Enforcement, 100 N._ CAROLINA L REV. __ (forthcoming
2022) (“A reason for regulation of risky products could be that government judges that the
preferences of some consumers are dangerous or unacceptable for society as a whole, either
as a moral matter or because of externalities on others.”).

52


-----

_DYNAMIC PRICING ALGORITHMS_

them to replace traditional cigarettes.[252] But the CDC asserts that e-cigarettes
are “not safe” for “youth, young adults, and pregnant women.”[253] For “kids,
teens, and young adults,” e-cigarettes are unsafe because nicotine “is highly
addictive and can harm adolescent brain development.”[254] Flavored e-cigarettes provide the same chemical mix as any other e-cigarette, but include an
appealing taste, like fruit or mint. From the point of view of the e-cigarette
user, a flavored e-cigarette is an improvement over non-flavored e-cigarettes.
Based on antitrust case law and most non-legal definitions, the flavored e-cigarette is an innovation. But the science concerning youth smoking shows that
it is a harmful innovation. Flavored e-cigarettes increase the likelihood that
young people will use these devices, creating serious health risks.[255] Recognizing the danger that flavored e-cigarettes pose, the FDA stated in April 2020
that it would “prioritize enforcement against [a]ny flavored” e-cigarettes “that
do not have premarket authorization.”[256]

More powerful automobile engines are another example of potentially
harmful innovation. Car manufacturers, especially the luxury brands, compete
in part on the power of their vehicles’ engines.[257] Engine torque and top speed
are selling points for some car buyers.[258] Competition to increase zero-to-sixty
speeds and top speeds routinely produces product improvements and certainly

252 Centers for Disease Control & Prevention, _Electronic_ _Cigarettes,_
https://www.cdc.gov/tobacco/basic_information/e-cigarettes/index.htm.

253 _Id._

254 Centers for Disease Control & Prevention, Quick Facts on the Risks of E-cigarettes for Kids,
_Teens,_ _and_ _Young_ _Adults,_ https://www.cdc.gov/tobacco/basic_information/e-cigarettes/Quick-Facts-on-the-Risks-of-E-cigarettes-for-Kids-Teens-and-Young-Adults.html.

255 _See Bridget K. Ambrose, Hannah R. Day, Brian Rostron, Kevin P. Conway, Nicollete_
Borek, Andrew Hyland, & Andrea C. Villanti, Flavored Tobacco Product Use Among US Youth Aged
_12-17 Years, 2013-2014, 314 J._ AM. MED. ASSOC. 1871, 1872 (2015) (surveying flavored tobacco
use among U.S. youth and finding that “[t]he majority of” youth who had ever used tobacco
products “reported that the first product they had used was flavored, including . . . 81% of
ever e-cigarette users. . .”).

256 _See U.S._ DEP’T OF HEALTH & HUMAN SERVICES, FOOD & DRUG ADMIN., CTR. FOR
TOBACCO PRODUCTS, ENFORCEMENT PRIORITIES FOR ELECTRONIC NICOTINE DELIVERY
SYSTEMS (ENDS) AND OTHER DEEMED PRODUCTS ON THE MARKET WITHOUT PREMARKET
AUTHORIZATION (REVISED) (April 2020) at 2-3.

257 George Kennedy, The 13 Fastest Cars, U.S. NEWS & WORLD REPORT (March 4, 2020),
https://cars.usnews.com/cars-trucks/fastest-cars-in-the-world (ranking cars on time to go
from zero to 60 miles per hour, and observing that “[y]ou’re never too old to have a wish list”
and “[f]or some, that list is dominated by extremely fast cars”).

258 _Id._

53


-----

_DYNAMIC PRICING ALGORITHMS_

represents innovation. Speeding is widely considered to lead to increased traffic deaths, however.[259] Cars that can go faster are more dangerous, all things
equal. The obvious regulatory reaction in most jurisdictions around the world
is speed limits. Capping maximum speed is a response to the harmful innovation of faster cars.[260] Speed limits de-incentivize innovation in car engines, at
least as far as top speed is concerned. But their safety benefits are significant,
so society accepts the tradeoff.

Innovation in pricing algorithms does not risk direct physical harm, unlike
e-cigarettes and speeding cars. The harm pricing algorithms cause—higher
prices for consumers—is distinct from many other types of innovation harms.
It is a rare example of innovation making products more expensive, rather than
cheaper, without improving product quality. But the examples of dangerous
products show that one way to mitigate these harms is through regulation,
even if that means blunting innovation incentives. To be sure, not all innovations that raise prices for consumers should necessarily be discouraged. For
example, pricing algorithms may help a less-sophisticated firm recognize that
it was (erroneously) pricing below the competitive level, foregoing profits unnecessarily. Thus, algorithms may raise prices by improving the information
available to firms. Pricing algorithms also may allow for personalized pricing
that charges individuals different prices based on their willingness to pay. This
strategy could raise prices to some consumers, but it could also make the product available to more consumers at lower prices. This is a more difficult case
for regulation, even though such price discrimination will shift surplus from
consumers to sellers in many cases.[261]

The effects of pricing algorithms show that the character of specific innovations should matter to policy makers. Where innovations harm consumers
or the broader public, policy makers, regulators, enforcers, and courts should
be less concerned about policies that might reduce related innovation incentives. Indeed, we propose that there is a category of innovation that reduces
welfare, generates consumer harm, and deserves close scrutiny by regulators
and antitrust enforcers. Dangerous products are an obvious example, but advances in pricing algorithms may also represent an extractive innovation that

259 _See e.g., Paul A. Eisenstein,_ _Your next car may not allow you to speed on the highway, NBC_
NEWS (April 9, 2019), https://www.nbcnews.com/business/autos/your-next-car-may-not-allow-you-speed-highway-n992606 (“[A]ccording to U.S. safety regulators, excess speed plays a
role in about 26 percent of all highway fatalities.”).

260 _See INSTITUTE OF TRANSPORTATION ENGINEERS,_ METHODS AND PRACTICES FOR
SETTING SPEED LIMITS: AN INFORMATIONAL REPORT 1 (“One of the most frequently used
methods of managing travel speeds is the posted speed limit.”),
[https://safety.fhwa.dot.gov/speedmgt/ref_mats/fhwasa12004/.](https://safety.fhwa.dot.gov/speedmgt/ref_mats/fhwasa12004/)

261 _See, e.g., The Law & Economics of Price Discrimination in Modern Economies, Time for Reconcili-_
_ation?, 42 U.C._ DAVIS L. REV., 1235, 1240 (“First-degree price discrimination involves charging
every customer the maximum amount they are willing to pay for each unit of the product sold.
This removes all ‘consumer surplus’ . . ..”).

54


-----

_DYNAMIC PRICING ALGORITHMS_

should be reined in by regulation. In general, more nuance is required in discussions of innovation policy. Just because a product is improved does not
mean it enhances consumer welfare or societal well-being.

CONCLUSION

Algorithmic pricing is spreading quickly throughout the economy.
Chances are high that most consumers already are buying algorithmically
priced products on a regular basis, especially when they make e-commerce
purchases. Pricing algorithms offer powerful advantages to sellers, which
means their adoption will only grow in the near future, perhaps even extending
to brick-and-mortar stores. Academics, policy makers, and antitrust enforcers
quickly realized the potential for pricing algorithms to facilitate both explicit
and tacit collusion. And these groups also recognized that while antitrust is a
useful tool for addressing explicit algorithmic price-fixing conspiracies, tacit
collusion is likely beyond the reach of the antitrust laws as currently enforced.

We identify a more fundamental challenge posed by algorithmic pricing: in
many markets it will raise prices for consumers even in the absence of collusion. The result could be a massive redistribution of wealth from buyers to
sellers. Because the mechanism we describe by which algorithmic pricing
raises prices does not involve collusion, antitrust—even broadly defined—cannot reach this conduct. As a result, price regulation may be the best solution
for protecting consumers in affected markets.

This Article explored the historical precedent for a regulatory response to
advances in pricing technologies and strategies. It also proposed two potentially effective regulatory approaches to non-collusive supracompetitive algorithmic pricing: restricting _when firms price, to eliminate asymmetric pricing_
frequency, and how they price, to bar firms from incorporating rivals’ prices in
their algorithms. Both approaches are designed to limit the ability of a firm
with a superior algorithm to soften competition through reactive price cuts.
They each have relative benefits and risks. We propose that the less intrusive
reform—restricting when firms can change prices—might be the preferable
approach based on our current knowledge of algorithmic pricing. But the
technology will continue to develop in unpredictable ways, and we argue that
regulators must remain nimble as the landscape changes.

55


-----

