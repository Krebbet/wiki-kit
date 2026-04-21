---
url: "file:///tmp/pdf-cache/nber-algorithmic-pricing.pdf"
title: "NBER WORKING PAPER SERIES"
captured_on: "2026-04-21"
capture_method: "pdf"
engine: "marker"
assets_dir: "./assets/nber-algorithmic-pricing"
---

# NBER WORKING PAPER SERIES

# ALGORITHMIC PRICING: IMPLICATIONS FOR MARKETING STRATEGY AND REGULATION

Martin Spann Marco Bertini Oded Koenigsberg Robert Zeithammer Diego Aparicio Yuxin Chen Fabrizio Fantini Ginger Zhe Jin Vicki Morwitz Peter Popkowski Leszczyc Maria Ana Vitorino Gizem Yalcin Williams Hyesung Yoo

Working Paper 32540 http://www.nber.org/papers/w32540

NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 June 2024, Revised June 2025

The authors thank the organizers of the 12th Invitational Choice Symposium at INSEAD. The views expressed herein are those of the authors and do not necessarily reflect the views of the National Bureau of Economic Research.

NBER working papers are circulated for discussion and comment purposes. They have not been peer-reviewed or been subject to the review by the NBER Board of Directors that accompanies official NBER publications.

© 2024 by Martin Spann, Marco Bertini, Oded Koenigsberg, Robert Zeithammer, Diego Aparicio, Yuxin Chen, Fabrizio Fantini, Ginger Zhe Jin, Vicki Morwitz, Peter Popkowski Leszczyc, Maria Ana Vitorino, Gizem Yalcin Williams, and Hyesung Yoo. All rights reserved. Short sections of text, not to exceed two paragraphs, may be quoted without explicit permission provided that full credit, including © notice, is given to the source.

Algorithmic Pricing: Implications for Marketing Strategy and Regulation Martin Spann, Marco Bertini, Oded Koenigsberg, Robert Zeithammer, Diego Aparicio, Yuxin Chen, Fabrizio Fantini, Ginger Zhe Jin, Vicki Morwitz, Peter Popkowski Leszczyc, Maria Ana Vitorino, Gizem Yalcin Williams, and Hyesung Yoo NBER Working Paper No. 32540 June 2024, Revised June 2025 JEL No. D4,L1,L4,L5

### **ABSTRACT**

Over the past decade, a growing number of firms have delegated pricing decisions to algorithms in consumer and business markets such as travel, entertainment, and retail, as well as in platform markets such as ride-sharing. We define algorithmic pricing as "the use of programs to automate the setting of prices." Firms adopt algorithmic pricing to optimize their prices in response to changing market conditions and to leverage the efficiency gains from automation. Advances in information technology and the increased availability of digital data have further facilitated the use of algorithm-driven pricing strategies. Yet adopting algorithmic pricing is not merely a technical upgrade—it is a strategic decision that must align with a company's existing and future marketing strategies. Moreover, algorithmic pricing can raise various regulatory concerns regarding potential threats to competition and the legality of price discrimination. This paper discusses the implementation of algorithmic pricing in the context of firms' marketing strategies and regulatory frameworks, while outlining an agenda for future research in this increasingly important area.

Martin Spann LMU Munich School of Management Ludwig-Maximilians-Universität München Geschwister-Scholl-Platz 1 80539 Munich Germany spann@lmu.de

Marco Bertini Esade Business School Universitat Ramon Llull Avinguda d'Esplugues, 92-6 08034 Barcelona Spain marco.bertini@esade.edu

Oded Koenigsberg London Business School R238 Regent's Park London, NW1 4SA United Kingdom okoenigsberg@london.edu Robert Zeithammer Anderson School of Management University of California at Los Angeles 110 Westwood Plaza Los Angeles, CA 90095 robert.zeithammer@anderson.ucla.edu

Diego Aparicio IESE Business School Carrer d'Arnus i de Gari, 3-7 Spain daparicio@iese.edu

Yuxin Chen NYU Shanghai Center for Business Education and Research 1555 Century Avenue Pudong New Area Shanghai 200122 China yc18@nyu.edu

Fabrizio Fantini Evo Pricing London United Kingdom fab@evopricing.com Ginger Zhe Jin University of Maryland Department of Economics College Park, MD 20742-7211 and NBER ginger@umd.edu

Vicki Morwitz Columbia Business School Columbia University 795 Kravis Hall New York, NY 10027 USA vgm2113@columbia.edu

Peter Popkowski Leszczyc School of Business University of Queensland St Lucia QLD 4072 Australia p.popkowski@business.uq.edu.au

Maria Ana Vitorino INSEAD maria-ana.vitorino@insead.edu

Gizem Yalcin Williams McCombs School of Business The University of Texas at Austin gizem.yalcin@mccombs.utexas.edu

Hyesung Yoo University of Toronto hyesung.yoo@rotman.utoronto.ca

#### **1. Introduction**

Over the past decade, a growing number of firms have delegated pricing decisions to algorithms in consumer and business markets such as travel, entertainment, and retail, as well as in platform markets such as home- or ride-sharing. We define algorithmic pricing as "the use of programs to automate the setting of prices." Although airlines have used yield management systems for decades (Elmaghraby & Keskinocak, 2003), and individualized or time-varying discounts have been common since scanners and loyalty programs were introduced in retail (Gabel & Guhl, 2022), the past decade has witnessed a dramatic surge in the use of algorithmic pricing.

For example, Airbnb introduced an algorithmic tool to help hosts set prices in 2013 (Hill, 2015). L. Chen, Mislove, and Wilson (2016) found that one-third of Amazon sellers of best-selling products likely used algorithmic pricing, although the specific algorithms remain unclear. Cohen, Hahn, Hall, Levitt, and Metcalfe (2016) showed that surge pricing on UberX—set by the platform's algorithm—helped match ride-sharing demand and supply in real time, resulting in \$6.8 billion in consumer surplus in the United States (U.S.) in 2015.

More recently, Brown and MacKay (2023) tracked high-frequency price data for OTC allergy medications at the five largest online retailers and found that while these retailers updated prices at regular intervals, the intervals varied widely across firms, and some retailers committed to use faster pricing technology to quickly respond to price changes by slower rivals. Calder-Wang and Kim (2023) examined the adoption of rent-optimization software by property management companies and found that, as of 2019, at least 25 percent of buildings—34 percent of units—in their data were using algorithmic pricing. As with ride-sharing, they found that algorithmic pricing enabled building managers to set prices more responsively to macro conditions, such as booms and busts, than non-adopters in the same market.

3

Firms adopting algorithmic pricing seek to optimize prices in response to market changes and to leverage automation efficiency gains (Bertini & Koenigsberg, 2021). The increasing availability of digital data and advances in information technology have further facilitated the use of algorithms in pricing.

However, the adoption of algorithmic pricing is a strategic decision that must align with a company's marketing strategies. It also requires careful navigation of the regulatory environment. Regulators are particularly concerned about risks such as anti-competitive behavior, in particular price collusion—where pricing algorithms may even independently learn to coordinate on higher prices without explicit agreements—and unlawful price discrimination, especially when AI systems personalize prices based on protected or opaque consumer attributes. To ensure compliance, firms may need to adjust their pricing strategies and algorithms accordingly.

Despite the widespread adoption of algorithmic pricing, a comprehensive analysis of its implementation considerations within firms' business strategies and regulatory frameworks remains lacking. Furthermore, there is no simple, consistent definition of algorithmic pricing. Several review articles have focused on different aspects of algorithmic pricing or related concepts. Seele, Dierksmeier, Hofstetter, and Schultz (2019) explored ethical considerations and distinguish dynamic and personalized pricing as subcategories of algorithmic pricing. Calvano, Calzolari, Denicolò, and Pastorello (2019) discussed competition-related issues of algorithmic pricing. Kopalle, Pauwels, Akella, and Gangwar (2023) studied dynamic pricing in the retail industry and discuss the main drivers of dynamic price changes. However, previous research has largely overlooked the managerial challenges of implementing algorithmic pricing. This paper addresses these gaps by examining the following three research questions:

1. What is algorithmic pricing, and how does it compare to other forms of pricing?

2. What challenges do managers face in implementing algorithmic pricing, and how can firms successfully integrate it in their marketing strategies while accounting for key stakeholders, competitive dynamics, and regulatory constraints?

4

3. What are the key questions and priorities for future research on algorithmic pricing?

We contribute to the literature by examining the strategic alignment of algorithmic pricing with respect to customers, competition, and the firm, i.e., its organization and marketing mix, and the consideration of key regulatory concerns. We also provide empirical support for the views we offer on this alignment through interviews with pricing executives, a survey of pricing managers, and a case study. Our discussion highlights the interdependencies between the implementation of algorithmic pricing, a firm's marketing strategy, and regulatory frameworks. For example, we show that firms' strategic considerations and market forces help mitigate many regulatory concerns**—**fear of customer backlash discourages unfair algorithmic pricing practices, while managers anticipate increased price competition rather than collusive behavior.

To guide our discussion of the strategic integration of algorithmic pricing, we structure its implementation around the components of an algorithmic process, i.e., the data input, the rules that transform that input, and the output (see [Figure 1\)](#page-6-0). This provides a framework for analyzing key factors in implementing this pricing strategy, with a focus on alignment with marketing strategies and addressing regulatory concerns that firms must consider.

The remainder of the paper is organized as follows. In Section [2,](#page-6-1) we define algorithmic pricing, compare it to other forms of pricing, and outline our framework for analyzing implementation [\(Figure 1\)](#page-6-0). In Section [3,](#page-11-0) we discuss the implementation of algorithmic pricing in terms of marketing strategy alignment and in Section [4](#page-30-0) in terms of regulatory concerns. Section [5](#page-41-0) concludes the paper with a discussion of research priorities in this area.

![](./assets/nber-algorithmic-pricing/_page_6_Figure_0.jpeg)

### <span id="page-6-0"></span>**Figure 1: Algorithmic Pricing Implementation**

#### <span id="page-6-1"></span>**2. Algorithmic Pricing: Definition, Comparison, and Analysis Framework**

#### **2.1. Definition and Comparison to Other Forms of Pricing**

We define algorithmic pricing as "*the use of programs to automate the setting of prices.*"1 In algorithmic pricing systems, input data is transformed into output based on the algorithm's rules with the goal of automatically setting prices (see [Table 1\)](#page-6-2). Input data refers to the selection of variables to include in pricing, such as weather, consumer characteristics and behavior, competitor prices, and historical data (Seele et al., 2019). The rules determine how prices, which may vary across time, consumers, and products, are set based on a particular combination of the input data. Output refers to the prices determined by the algorithm.

<span id="page-6-2"></span>**Table 1: Components of Algorithmic Process to Set Prices**

| Component  | Examples                                                                                                                    |
|------------|-----------------------------------------------------------------------------------------------------------------------------|
| Input data | Consumer characteristics, historical consumer behavior, product attributes,<br>competitor prices, weather, inventory levels |

<sup>1</sup> Our definition of algorithmic pricing does not include algorithms that may indirectly influence pricing, such as those used by donation-based live streaming platforms (e.g., S. Lu, Yao, Chen, and Grewal (2021)).

| Pricing rules | Price-sensitivity to changes in demand, supply, competitor prices |
|---------------|-------------------------------------------------------------------|
| Output        | Price(s) across time,<br>consumers, and products                  |

[Table 2](#page-7-0) compares different forms of pricing along four dimensions: the automation of pricing decisions, the ability to adjust prices in real time, the primary data input, and whether customers interact directly in setting prices. In particular, Table 2 shows that algorithmic pricing includes both dynamic pricing and personalized pricing: The algorithm adjusts prices over time, for different consumers, and across products (Seele et al., 2019). Dynamic pricing refers to (automated) price changes triggered by shifts in market demand drivers (Kopalle et al., 2023)2, while personalized pricing involves charging consumers different prices based on personal characteristics and/or behavior (OECD, 2018). Both dynamic and personalized pricing are typically implemented through algorithms, and are therefore considered forms of algorithmic pricing.

Algorithmic pricing differs from participative pricing, where prices result from direct customer interaction via consumer price offers in a participative pricing mechanism such as an auction or negotiation (Spann et al., 2018).

|                             | Algorithmic pricing                 |                             |                          |                        |
|-----------------------------|-------------------------------------|-----------------------------|--------------------------|------------------------|
| Dimensions                  | Dynamic<br>pricing                  | Personalized<br>pricing     | Participative<br>pricing | Traditional<br>pricing |
| Pricing automation          | Usually                             | Usually                     | No                       | No                     |
| Real-time price changes     | Yes                                 | No                          | No                       | No                     |
| Primary data input          | Real-time demand<br>and supply data | Individual<br>consumer data | Consumer<br>price offers | Demand<br>data         |
| Direct customer interaction | No                                  | No                          | Yes                      | No                     |

<span id="page-7-0"></span>**Table 2: Differences Between Algorithmic Pricing and Other Forms of Pricing**

<sup>2</sup> Consistent with this definition, pre-announced price differences over time that do not adjust dynamically—such as daily happy hour offers between 6 p.m. and 8 p.m. at a bar—are not considered dynamic pricing.

The key difference between algorithmic and traditional pricing methods is automation and real-time adjustments. While traditional methods involve manual price-setting by managers, algorithmic pricing uses algorithms to set prices based on predefined rules and data analysis. Prices based on algorithmic pricing systems are typically neither predetermined nor pre-announced as in traditional pricing.

#### **2.2. Framework to Analyze the Implementation of Algorithmic Pricing**

[Figure 1](#page-6-0) illustrates our framework for the strategic and implementation aspects of algorithmic pricing. The horizontal process follows the logic of algorithms, using input data that is transformed into output based on the algorithm's rules. As outlined above, input data includes the selection of variables, while rules determine how prices are set based on a particular combination of input data. Output decisions involve implementing and communicating algorithmically determined prices, such as through different channels. Additionally, the firm must monitor each step of the algorithmic process and adjust as needed.

These decisions along the algorithmic process must align with the firm's marketing strategy and external (regulatory) concerns. Next, we describe the components of marketing strategy according to customers, competition, company (organization and marketing mix), and outline potential regulatory concerns regarding price collusion and (unlawful) price discrimination that firms must consider when implementing algorithmic pricing. In the following sections, we discuss each of these aspects. While our focus is on business models that sell directly to individual consumers (B2C), many ideas also apply to business-to-business (B2B) models.

#### **2.3. Empirical Support**

To provide empirical support for our discussion of algorithmic pricing, we present results from in-depth interviews with pricing executives, a survey of pricing managers, and a case study (see [Table 3\)](#page-9-0). Below, we outline the methodology of each study and incorporate the results into our discussion. Additional results and details can be found in the Web Appendix.

*Type of study Data description In-depth interviews* Five pricing executives *Managerial insights survey* Seventy-one pricing managers *Case study* Price automation with electronic shelf labels (ESLs) in 225 offline stores

<span id="page-9-0"></span>**Table 3: Empirical Support Used in This Paper**

### **2.3.1. Interviews with Pricing Executives**

We conducted five in-depth interviews with knowledgeable, global pricing experts from major consultancies or presidents of major industry organizations involved in pricing. The purpose of these interviews was to gain a high-level strategic perspective on the use and perceptions of algorithmic pricing based on interviewees' experiences with client and member firms. [Table 4](#page-10-0) lists the interviewees and their roles.

All interviews were conducted by the same author and followed a predetermined structure. After introducing our objective, each interviewee was presented with our framework for analyzing the key aspects of algorithmic pricing implementation (see [Figure 1\)](#page-6-0). The interviews followed this structure, with follow-up questions about the issues highlighted by the interviewee. Each interview lasted approximately 30 minutes, was recorded and transcribed. We report quotes from these interviews in Sections [3.1,](#page-11-1) [3.2,](#page-18-0) [3.3,](#page-19-0) and [5](#page-41-0) to highlight key insights.

| Name               | Position                                                                                       |
|--------------------|------------------------------------------------------------------------------------------------|
| Mark Billige       | Chief Executive Officer, Simon-Kucher & Partners                                               |
| Kevin Bright       | Former Head of Pricing, Europe, McKinsey & Company                                             |
| Jean-Manuel Izaret | Managing Director & Senior Partner; Global Leader, Marketing, Sales &<br>Pricing Practice, BCG |
| Kevin Mitchell     | President, Professional Pricing Society                                                        |
| Pol Vanaerde       | Founder and Chair, European Pricing Platform                                                   |

<span id="page-10-0"></span>**Table 4: List of Pricing Excecutives Interviewed**

#### <span id="page-10-1"></span>**2.3.2. Managerial Insights Survey**

We conducted a survey of pricing managers to assess their perceptions and use of pricing algorithms, particularly with respect to reasons for (non-)adoption of algorithmic pricing. The survey was distributed via the EPP Pricing Platform (www.pricingplatform.com), a non-profit platform with over 25,000 registered pricing professionals, and through links shared on the authors' LinkedIn accounts (see Web Appendix A & B for the survey materials and further details).

Eighty-three managers participated in the survey, with 12 responses excluded3, leaving 71 responses available for analysis. Over 80 percent (87.3%) of respondents said they were very or extremely familiar with their company's pricing strategies, and most (79.6%) of them were responsible for pricing decisions in their companies. The majority of companies sold less than 25 percent of their business through online channels (81.5%), had been in business for more than 20 years (79.6%), employed more than 1,000 people (68.5%), and sold products in Europe (68.5%) and the U.S. (24.1%). See Section [3.3](#page-19-0) for the results of the survey.

<sup>3</sup> Ten were excluded for incompleteness, and two for inconsistencies in statements about their use of algorithmic pricing.

### **2.3.3. Case Study: Price Automation via Electronic Shelf Labels in Offline Retailing**

We present a case study on the implementation of algorithmic pricing in offline retail settings, supported by the use of Electronic Shelf Labels (ESLs) to facilitate more frequent and automated price adjustments. Evo4 provided field data from a client who operates gift and memorabilia stores in zoos, aquariums, and museums. The client previously followed a corporate policy of updating prices only twice a year due to the high labor costs of printing price tags, determining new prices, and other operational challenges. This inflexible pricing approach limited the stores' ability to respond to changes in consumer preferences, seasonal trends, cost fluctuations, and customer demographics.

To overcome these limitations and enable algorithmic pricing in physical stores, ESLs were installed to automate the display of algorithmically generated prices, significantly reducing the cost and effort associated with price changes. The data cover 225 stores in the U.S. and Canada. See Sections [3.3](#page-19-0) and [3.4.3](#page-27-0) for the case study results.

### <span id="page-11-0"></span>**3. Implementation and Marketing Strategy Alignment**

Algorithmic pricing must align with the firm's overall marketing strategy. This section assesses its fit with the overall business strategy in terms of customers, competition, and the company, i.e., its organization and marketing mix. [Table 5](#page-13-0) provides an overview of the key aspects.

# <span id="page-11-1"></span>**3.1. Customers**

Algorithmic pricing can dynamically adjust prices based on changing market conditions and personalize them for different customer segments or even individuals, using various inputs

<sup>4</sup> Evo is a consulting company that uses artificial intelligence to help clients optimize business decisions for pricesetting. See Fantini and Das Narayandas (2023) for further details.

such as behavior, price elasticity, willingness-to-pay, geo-location and demographics. When done correctly, this can enhance customer satisfaction by offering discounts or personalized offers that align with customer expectations and willingness to pay. However, it is important to consider how consumers may react to various aspects of algorithmic pricing implementation in terms of input data, rules, and resulting prices (i.e., output). Existing research highlights how algorithms shape the way consumers think and feel about themselves, products, and companies, ultimately affecting their behaviors (G. Y. Williams & Lim, 2024; Yalcin, Lim, Puntoni, & van Osselaer, 2022). However, existing studies on consumer reactions to algorithmic pricing remain scarce.

Consumers' reactions to the adoption and implementation of algorithmic pricing are shaped by their beliefs and perceptions about the data used by the algorithms, the rules they assume govern price-setting, the prices themselves, and their dynamic nature. Additionally, customer perceptions of algorithmic pricing are affected by how transparent a firm is regarding its use of algorithms, the information used by its pricing algorithm, and how prices are set. Transparency here can play a critical role in building consumer trust and influencing valuation, similar to how consumers value price transparency (Seim, Vitorino, & Muir, 2017).

|                          | Key factors                                                                                                                                           | Related<br>implementation features (inputs, rules, outputs)                                                                                                                                                                                                                                         |  |  |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
| Customers                | •<br>Willingness to pay<br>•<br>Perceived price fairness<br>•<br>Discriminatory prices<br>•<br>Price transparency<br>•<br>CRM integration             | •<br>Input: Customer-level data (past behavior, purchase<br>history, demographics, preferences)<br>•<br>Rules: Limit price increases (e.g., during high demand),<br>avoid perceived unfair<br>pricing, align<br>with CRM<br>objectives<br>•<br>Output: Personalized prices, transparency in pricing |  |  |
| Competition              | •<br>Influence of<br>competition<br>Influence on<br>competition<br>•<br>Risk of price wars                                                            | •<br>Input: Competitor prices, market structure data<br>•<br>Rules and output: Avoid reactive pricing loops or<br>similar algorithms by competing firms                                                                                                                                             |  |  |
| Company:<br>Organization | •<br>Managerial perceptions of<br>algorithmic pricing<br>•<br>Managerial qualifications<br>•<br>Market role of firm<br>•<br>Organizational structures | •<br>Input: Clarify managers' roles, integrate within<br>company functions<br>•<br>Rules: Include human oversight, align algorithm with<br>organizational goals and the firm's market role<br>•<br>Output: Provide training; managers understand and<br>trust algorithmic outputs                   |  |  |
| Company:<br>Price        | •<br>Pricing strategy alignment<br>•<br>Revenue model alignment<br>•<br>Impact on consumer behavior                                                   | •<br>Input: Customer behavior, pricing history<br>•<br>Rules: Differentiate for subscription vs. pay-per-use,<br>adjust frequency of price change to market norms<br>•<br>Output: Prices that reflect strategic pricing goals across<br>a product line                                              |  |  |
| Company:<br>Product      | •<br>Different product types (e.g.,<br>durable vs. consumable)<br>•<br>Consistency with brand image<br>•<br>Weight of product characteristics         | •<br>Input: Product characteristic<br>•<br>Rules: Adjust rules for product-specific price sensitivity<br>•<br>Output: Align price levels and variation with consumer<br>expectations for the given<br>product type                                                                                  |  |  |
| Company:<br>Place        | •<br>Fit with distribution channel<br>•<br>Price consistency across<br>channels (online vs. offline)                                                  | •<br>Input: Channel-specific data availability<br>•<br>Rules: Allow differentiated pricing across channels<br>within consumer tolerance<br>•<br>Output: Dynamic pricing for online and offline channel<br>(e.g., via electronic shelf labels)                                                       |  |  |
| Company:<br>Promotion    | •<br>Effect on price promotions<br>•<br>Interplay of advertising and<br>algorithmic pricing                                                           | •<br>Input: Advertising engagement (e.g., CTR), promotions<br>history<br>•<br>Rules: Align promotion timing/size with algorithmic<br>rules; enable synergy between pricing and advertising<br>•<br>Output: Targeted, data-driven promotions; consistent<br>messaging across ads and prices          |  |  |

<span id="page-13-0"></span>**Table 5: Algorithmic Pricing Implementation and Marketing Strategy Alignnment**

Beyond inputs, rules, and outputs—and the transparency surrounding them—consumers' reactions may also depend on their broader beliefs about companies using pricing algorithms. A key consideration in the implementation of algorithmic pricing is that some consumers may believe the use of pricing algorithms is inherently unfair (Haws & Bearden, 2006). Perceptions of price

fairness can vary with the source of information; thus, even when observed prices are held constant, consumers' perceptions of fairness may differ if they become aware that an algorithm was involved in price-setting (Campbell, 2007).

13

Consumers may be aware of, or believe, that factors such as their demographics, geographics, and past behavior (e.g., clicks, purchases, views) can be used as inputs in pricing algorithms. In such cases, their reactions are likely to be affected by the inputs they believe are being used. Duani, Barasch, and Morwitz (2024) found that while consumers generally perceive pricing algorithms to be less fair than human price-setters, when price discrimination is based on demographics, they view prices set by algorithms (vs. humans) as fairer. This is because, in the case of demographic price discrimination, consumers feel less judged by algorithms (vs. humans), and perceive their decisions as less exploitative and more justified. However, adding nuance to this discussion, previous research has also shown that consumers from marginalized groups may be concerned that using such data could lead to biased or discriminatory outcomes, prompting them to avoid companies that use such algorithms (Barocas & Selbst, 2016).

While past research has shown that consumers are sometimes willing to share personal information for discounts or better service—and tend to share data with algorithms than with humans (Lucas, Gratch, King, & Morency, 2014; Raveendhran & Fast, 2019, 2021), pricing algorithms still harbor privacy concerns regarding the use of personal data (Kim, Barasz, John, & Norton, 2022), which can lead to perceptions of unfairness in price-setting.

There are several reasons related to the rules used by pricing algorithms that may lead consumers to perceive their use as unfair. First, if consumers believe that the pricing rules violate the dual entitlement principle (Kahneman, Knetsch, & Thaler, 1986), they may perceive algorithmically set prices to be unfair. In general, this principle suggests that customers are entitled to receive a price at or near their reference price, while companies are entitled to earn their reference profit. Accordingly, if a company increases its price to offset higher costs, consumers may view this as fair. However, when an algorithm is used to deploy dynamic pricing, prices often rise independently of cost increases (e.g., due to fluctuations in demand, inventory levels, market buying patterns, or demographics; Choi, Song, & Jing, 2023). Consumers may then perceive such price increases as unfair, and avoid buying from that seller.

14

Second, consumers may believe that the algorithm's rules allow for more frequent price changes, with prices fluctuating more often than when set by humans (Haws & Bearden, 2006). Past research has shown that consumers perceive such frequent changes over short periods to be unfair. More broadly, perceptions of unfairness may arise if consumers believe that algorithms allow companies to implement price changes more extensively and with greater impact than human decision-makers would (Duani et al., 2024).

Finally, consumers' fairness perceptions may be shaped by belief about the rules used to set prices in the market more generally. For instance, fairness perceptions and attitudes toward companies using pricing algorithms can be significantly influenced by market norms surrounding algorithmic pricing. In markets where algorithmic pricing is common and many competitors use the technology (e.g., the airline, live entertainment, and hospitality industries), consumers may view price fluctuations more favorably. The same strategy, however, may be perceived differently in markets where frequent price changes are not as common or expected (e.g., public transportation).

The interviews with the pricing executives highlight that customers' perceptions of price fairness and potential reputational damages are a large concern for managers. *Kevin Bright* (Former Head of Pricing, Europe, McKinsey & Company) sees fairness considerations as more important than other concerns: "It's the reputational risk that is top of mind for them." *Mark Billige* (Chief Executive Officer, Simon-Kucher & Partners) highlights the observation that customers tend not to complain about price level, but rather about price differences over time and compared to other customers: "It's rarely, I think expensive, inexpensive or too much, too little." It's more than someone else or more than it was yesterday. And that is what people struggle with. I think it's the dynamism of pricing."

15

*Pol Vanaerde* (Founder and Chair, European Pricing Platform) recommends two things to avoid potential reputational damage: "First of all, it's important to understand if your customers accept dynamic pricing. The second thing is that in your rule-based pricing, you install guidance when you say you're not going to do things that are unfair or perceived as unfair." *Jean-Manuel Izaret* (Managing Director & Senior Partner; Global Leader, Marketing, Sales & Pricing Practice, Boston Consulting Group) explains that "in our approach, every variable that's about consumer identity is completely out of the algorithms" and that behavioral variables are sufficient: "We think there is enough ability to adjust around behavior without adjusting about who people are."

Consumers' perceptions of price algorithms are affected by their observations or beliefs about the algorithm's outputs. For example, if consumers believe or observe that others are paying different prices for the same product or service, they may perceive these algorithmically set prices as unfair (Feinberg et al., 2002; Haws & Bearden, 2006; Kuo et al., 2016; Lyn Cox, 2001).

Additionally, consumer's perceptions depend on other price comparisons they make after obtaining a price. For example, it is reasonable to expect that consumers aware of price fluctuations over time will revisit the websites or stores where they made a purchase and check whether they could have gotten a better or worse deal by waiting. Such ongoing price checking may lead to feelings of regret or elation, depending on the outcome (Pizzutti, Gonçalves, & Ferreira, 2022).

16

Regardless, this behavior likely introduces stress due to the price uncertainty and lack of closure. This (dis)satisfaction may also affect important customer behaviors, including product returns, repeat purchases (i.e., customer retention), word-of-mouth, referrals or complaints (e.g., on social media).

For these reasons, algorithmic pricing should be integrated with a company's customer relationship management (CRM) systems. This integration involves sharing the input data (e.g., customer purchase history) as well as the goals of the CRM system (e.g., customer lifetime value (CLV)), which will then inform the pricing algorithm. For example, the algorithm can set comparatively lower prices for products in categories the customer has shown interest in but has yet to purchase, thereby increasing their CLV through cross-selling. To prevent unfavorable price comparisons based on inaccurate recall of past (reference) prices, the algorithm could display current prices relative to what the customer previously paid. Additionally, the algorithm could monitor consumer reactions to the frequency of past price changes, and where possible, adjust that frequency to optimize satisfaction and minimize unfavorable reactions.

More generally, to address customer perceptions of algorithmic pricing, firms must account for potential violations of fairness norms discussed above by implementing guardrails in pricing rules—such as capping price increases during periods of excess demand. Avoiding discriminatory pricing based on demographics that are view as unfair and in some cases illegal (e.g., gender, race) requires not only excluding such input data, but also actively monitoring algorithmic outputs to ensure that algorithms do not inadvertently learn and replicate discriminatory practices and patterns from training data. Companies need to be transparent about the input data they use and their general pricing rules, and need to continue to monitor consumer reactions to the prices set by algorithms as their use expands in general and within their specific industry.

#### <span id="page-18-0"></span>**3.2. Competition**

The competitive landscape and competitors' use of algorithmic pricing may influence a company's decision to adopt it. In addition, competitors' prices are often a key input to algorithmic pricing, potentially shaping the algorithm's rules (e.g., if price matching is a desirable outcome). *Mark Billige* highlights the risk to focus too much on competitors' prices: "So you get very fixated on prices and I think there's a lot of danger if you follow your competitors' prices too closely and therefore ignoring other differences." Therefore, a firm that just matches competitor prices might neglect other important factors of customers' buying decisions: "It's very hard to benchmark their value or their quality and that's part of the problem which is, we have all these numbers on prices, but we lack similar numbers on quality, perception, value, all this kind of stuff."

17

An important consideration in implementing algorithmic pricing is its impact on competition, particularly with respect to whether algorithms are designed to mitigate the negative effects of price competition. Potential risks that need to be considered include tacit collusion and firms being trapped in prisoner's dilemmas (see Section [4.1\)](#page-31-0). *Kevin Mitchell* (President, Professional Pricing Society) emphasized the need to think about the strategic implications of using pricing algorithms: "Once you install an algorithm…things don't happen in a vacuum in our space. You're going to make a move with an algorithm. Your marketplace, you know all the seeds, your customer, your competition, your cost might change. What are the effects down the line?"

While studies on algorithmic pricing have shown its short-term effectiveness, the longterm effects of algorithmic pricing on competition remain understudied. Recent studies have suggested the potential for collusive behavior due to the use of similar algorithms by competing firms and algorithms converging on similar pricing strategies (Assad, Clark, Ershov, & Xu, 2024; Brown & MacKay, 2023; Calvano, Calzolari, Denicolò, & Pastorello, 2020; Hansen, Misra, & Pai, 2021; Miklós-Thal & Tucker, 2019). Such a collusive outcome can also emerge in the context of competitive price-setting using large language models (LLMs) directly (Fish, Gonczarowski, & Shorrer, 2024). However, it is inconclusive whether this holds true across industries, given the proliferation of algorithms and advances in the methodologies used in algorithms (see Section [4.1](#page-31-0) for a more detailed discussion of algorithmic collusion).

Interestingly, our interview partners expressed less concerned about potential collusion among pricing algorithms and believed it more likely that algorithms would intensify price competition. For example, *Jean-Manuel Izaret* observes that "the behaviors you see from algorithms in the market so far tend to be deflationary more than inflationary." Rather, pricing executives worry that pricing algorithms increase the risk of starting price wars. For example, *Kevin Mitchell* emphasizes that: "we have all seen and heard about instances where price wars started over very, very small pricing moves." Therefore, the implementation of algorithmic pricing rules must consider and avoid triggering price wars.

#### <span id="page-19-0"></span>**3.3. Company: Organization**

Algorithmic pricing can benefit firms by making price-setting processes more efficient and by simplifying managers' pricing decisions. It allows managers and firms to respond more quickly to market changes, especially changes in supply and demand, thereby increasing profits (Ham, He, & Zhang, 2022; J. P. Johnson, Rhodes, & Wildenbeest, 2023). However, successful implementation of algorithmic pricing must consider managers' perceptions and acceptance of the use of algorithmic pricing, their skillsets, and how well algorithms align their incentives with the firm's objectives (Bertini & Koenigsberg, 2021). In addition, algorithmic pricing needs to be integrated into a firm's organizational structures, processes, and information systems.

In terms of managers' perceptions, it is critical that new tools, such as algorithmic pricing, are introduced across all relevant business functions, and that managers are both persuaded to accept these tools and trained to use them effectively. Managers may resist adopting algorithms, mirroring resistance often observed among consumers. Previous research suggests that people may avoid relying on algorithms, even when algorithms consistently outperform humans (Dietvorst, Simmons, & Massey, 2015). Algorithm aversion may be due to various reasons, including the opacity of the algorithmic decision-making process (Yeomans, Shah, Mullainathan, & Kleinberg, 2019), a desire for control, and the ability to modify (imperfect) algorithms (Dietvorst, Simmons, & Massey, 2018), reluctance to adopt new options, and overconfidence in personal experiences (Diab, Pui, Yankelevich, & Highhouse, 2011; Y. Lu, Wang, Chen, & Xiong, 2023).

19

To explore these factors, we surveyed 71 pricing managers to understand their perceptions and use of algorithmic pricing (see Section [2.3.2\)](#page-10-1). Our findings reveal that reluctance to adopt pricing algorithms stems from several negative perceptions, including concerns about reduced transparency, the "black box" nature of algorithms, diminished managerial control over pricing decisions, decreased trust, and unfavorable consumer perceptions of fairness. This reluctance is not due to a lack of understanding of their benefits, as pricing managers who did not implement pricing algorithms tend to overestimate their advantages (for further details and analyses related to pricing practices and types of pricing algorithms used, see Web Appendix B).

This relates to the insight of *Kevin Bright* (Former Head of Pricing, Europe, McKinsey & Company) that managers are likely to adopt pricing algorithms they understand: "My experience has been that most of the models are simpler than they could be because you need that link between the intuition of the decision-maker and their ability to see the variables in the model that they would have used themselves." *Jean-Manuel Izaret* adds that understanding the algorithm is also important for communicating prices to customers: "Having transparency for the sales force about why prices are going one way or the other is important because they need to explain it to customers."

20

Managers are also likely to be concerned about how adopting algorithms will impact their roles, potentially leading to reluctance and resistance. These concerns can be addressed through a three-pronged approach. First, managers should be educated and informed about how the algorithm works. The development of explainable artificial intelligence (AI) that demystifies the black-box nature of machine learning algorithms would be helpful in this regard. Second, managers' insights could be incorporated into the algorithm. This can be particularly valuable when historical data are limited. However, care should be taken to avoid introducing human bias into the algorithm. Third, and perhaps most importantly, managers should be invited and actively involved in overseeing the algorithms to mitigate the potential risks of using them. Managers should be encouraged to interact with customers and gather feedback on their reactions to and concerns about pricing algorithms that may not be observable or inferred from revealed customer behavior. Depending on the nature of the concerns uncovered, managers may need to adjust the algorithms.

The concerns managers have about their roles were also raised by the pricing executives we interviewed. *Kevin Mitchell* (President, Professional Pricing Society) highlights that managers may feel threatened by algorithms: "Sometimes people feel that they're losing a little bit of control over their product, which might from a career perspective, be their baby." He also emphasized the need for (some) human oversight was mentioned several times, especially in case of important customers: "I think for a really big deal, if it's really, really important to the organization, then oversight is important just because there are always in pricing literature examples of algorithms that have basically gone on their own and done their own things that may or may not be completely in line with the company's KPIs." The lack of control over pricing decisions was also a concern raised in the survey of pricing managers (see Web Appendix B).

21

In the *case study*, keeping a "human in the loop" to have human oversight was also a critical issue for the managers involved. In the case study implementation, the managers added several constraints to the price optimization process, such as restrictions on overnight price adjustments, limits on price differences between comparable products, limits on maximum or minimum prices, considerations for price endings, and rules on the frequency of price changes per week.

Similar concerns may also arise if the company operates a two-sided platform. Many twosided platforms adopt pricing algorithms to assist sellers who often lack managerial capabilities. The efficacy of such algorithms depends not only on their performance but also on their adoption by sellers. However, seller skepticism—rooted in a general aversion towards algorithms—can present a barrier. Sellers may also be unclear whether the algorithm is designed to maximize the platform's revenue or their own. One reason is that platforms often lack accurate information about sellers' marginal costs, and therefore, platforms earn a fixed share of sellers' revenues rather than profits. This gives an incentive for platforms to adopt algorithms that set seller revenuemaximizing prices instead of seller profit-maximizing prices. Consequently, while platforms may seek to support sellers' pricing decisions, their objectives may not always align with those of the sellers. A key challenge in implementing algorithmic pricing rules on two-sided platforms is the potential tension between the platform's revenue goals and those of third-party sellers.

Using algorithms for pricing decisions requires coordination with managers responsible for marketing and operational inputs, such as the level of quality built into products and services, inventory levels, promotions, and channel design. Since some of these decisions, like inventory

levels and promotions, occur frequently, automating them through an integrated algorithm would be ideal. Input from various functional units responsible for these aspects would be critical to the success of such an algorithm. In addition, a company may choose to assign responsibility for the inputs, rules, and outputs of algorithmically set prices to a single department, rather than dividing responsibilities among multiple departments, such as IT handling the input data and marketing managing the rules and output. This approach is increasingly feasible and efficient to implement given the general trend toward digitization of business.

Our interview partners highlighted the question of the organizational embeddedness of algorithmic pricing. *Mark Billige* (Chief Executive Officer, Simon-Kucher & Partners) emphasizes: "Who owns pricing? It is irrelevant whether it's a person that comes up with it or your system comes up with it—someone has to own the pricing decision in the company." However, it may depend on the status and hierarchy-level of the pricing algorithm owner "people accept the numbers that come out of these systems." *Pol Vanaerde* adds that: "you need to have your full organization aligned. And that's the biggest challenge that I see in organizations if you start installing algorithm driven pricing, it takes a lot of alignment in your organization. You need your data science team, you need your marketing, you'll need your category managers and your pricing aligned. You need to bring them together and explain what you do with the system."

Managers must ensure that new tools are effectively adopted across relevant business functions. Ideally, firms should leverage pricing algorithms to streamline pricing decisions within the organization and improve coordination between different functional units. This requires ongoing monitoring, such as through a corporate oversight committee.

#### **3.4. Company: Marketing Mix**

The implementation of algorithmic pricing needs to be integrated into a firm's marketing mix—price, product, place and promotion—ensuring alignment with broader strategic goals.

#### **3.4.1. Price**

Algorithmic pricing must align with the firm's overall pricing strategy and revenue model, while considering its impact on customer price sensitivity, which in turn affects optimal pricing decisions. Skimming and penetration pricing are important strategic choices for long-term pricing (Spann, Fischer, & Tellis, 2015). For example, a firm's goal may be to gain market share through a penetration pricing strategy, so the pricing algorithm would be set to price competitively relative to competitors' prices. Conversely, a price skimming strategy would factor in the price sensitivity of a target segment of "innovative customers," as well as the predicted product life cycle, to determine the timing for price reductions. The use of algorithmic pricing allows for tailored application of a skimming or penetration strategy for each product in a large product line.

While the use of algorithmic pricing is more straightforward in the case of a pay-per-use revenue model, subscription-based companies can leverage algorithms to determine promotional discounts for new customers, pricing for additional add-on sales not included in the subscription, and to offer targeted discounts to prevent customer churn.

The use of algorithmic pricing can also change the price sensitivity in the market, thereby affecting optimal pricing strategies. For instance, the use of pricing algorithms may alter how frequently or in what manner consumers search for purchase options (e.g., incognito mode; Lagerlöf, 2023) and seek information about prices or other attributes. Since pricing algorithms often consider consumers' online search behavior (e.g., the frequency and duration of website visits), consumers may adjust their search strategies based on the (actual or assumed) rules pricing

algorithms follow. Common strategies for airline ticket shoppers, for example, include clearing browser cookies, booking flights on certain days of the week (e.g., Tuesday), or minimizing repeated searches for the same flight.

24

While past research has shown that consumers' reactions to price depend on deviations from an expected or reference price (Thaler, 1985), dynamic pricing models might affect the strength of reference price effects (Prakash & Spann, 2022), or replace a fixed reference with a reference price distribution. This may lead to more complex patterns of price sensitivity, as consumers' expectations are shaped by both current and previously observed price levels.

#### **3.4.2. Product**

The implementation of algorithmic pricing may vary substantially across different product types, such as durable vs. consumable, hedonic vs. utilitarian, and luxury vs. mainstream products. Furthermore, algorithmic pricing may influence product quality perceptions and shift the weight consumers place on price compared to other product attributes.

Durable products (e.g. laptops) tend to be purchased less frequently and are generally more expensive than consumables. As a result, consumers tend to be more involved in decision-making and make more careful choices. Price fluctuations driven by pricing algorithms can be expected to have a more substantial impact in these cases as consumers may choose to wait to get a better deal or use price recommendation tools to (supposedly) improve decision quality. Therefore, implementing algorithmic pricing for durable products may provoke stronger behavioral responses from consumers, affecting optimal pricing.

A second product characteristic influencing consumers' reactions to algorithmic pricing is the nature of the product—namely, whether it is predominantly hedonic or utilitarian (Ratneshwar & Mick, 2013). While hedonic products are mainly driven by sensory or experiential pleasure,

utilitarian products are cognitively driven, based on functional and instrumental goals (e.g., lemonade vs. sports drink; Botti & McGill, 2011). As consumers are already more driven by immediate rewards and find themselves in a more affect-driven mindset, they may be more inclined to bypass the evaluation process and make quicker purchases when pricing algorithms push reductions on hedonic products. In contrast, utilitarian products are likely to involve careful, cognitively driven evaluations.

25

Third, depending on their position in the brand hierarchy, companies can be seen as luxury or mainstream (Keinan, Crener, & Goor, 2020). Luxury brands often carry symbolic and aspirational meanings (e.g., power, success) and are associated with higher-than-average prices. Importantly, their positioning influences how consumers perceive the company, its products (e.g., perceived quality), and how they evaluate purchases when these companies adopt pricing algorithms. For example, if a luxury brand lowers prices through dynamic pricing, consumers may view this as a rare opportunity to own a luxury item (e.g., Hermès purse), skipping the evaluation stage and making an impulsive purchase. More broadly, consumers may hold perceptions regarding the frequency of price changes and perceptions of product quality, status, and luxury. For example, while they have already experienced frequent price changes for less expensive household products, they may expect that prices should vary less for high-end luxury products.

The implementation of pricing algorithms can also affect how consumers draw conclusions about product quality. Past research has shown that prices are often (positively) correlated with actual product quality. Thus, it is not irrational for consumers to infer quality from the prices they observe (Rao & Monroe, 1989). However, if prices vary constantly, consumers may be less willing to draw conclusions about product quality from prices. Frequent price changes may lead consumers to infer that price and quality are not necessarily related, and they may turn to other

proxies and indicators to judge quality. Alternatively, consumers may make quality inferences not just based on price, but also on price distributions. For example, they may reason that prices that vary less (e.g., an upscale resort hotel) are of higher product quality than those that vary more (e.g., a lower-end budget hotel). In addition, previous research has shown that frequent price promotions may negatively affect perceived brand equity (Erdem, Keane, & Sun, 2008).

26

More generally, algorithmic pricing may alter how consumers weigh price relative to other product attributes. On the one hand, pricing algorithms may increase the salience of price, leading consumers to place greater weight on it compared to other product attributes. On the other hand, since evaluating a price or using it as a signal of quality is presumably more challenging with constant variation introduced by pricing algorithms, consumers may de-emphasize price and place more weight on other product features.

### <span id="page-27-0"></span>**3.4.3. Place**

Just as with brands, pricing strategies need to align with retail strategies. Some retailers, even in the absence of pricing algorithms, employ frequent price changes, using a form of highlow pricing, while others maintain less varying pricing through EDLP (Everyday Low Pricing; Alba, Mela, Shimp, & Urbany, 1999). Price algorithms facilitate more frequent price changes and the ability to adjust prices for more items at once. However, when and how these changes are permitted by the rules of the algorithm should align with the retail positioning.

Implementing algorithmic pricing presents unique challenges for companies selling through both online and offline channels. While the digital nature of algorithmic pricing is wellsuited for online environments, it requires digital technology in physical stores to facilitate dynamic price changes. One such technology is Electronic Shelf Labels (ESLs), which display prices on small digital screens next to products. ESLs allow for the implementation of algorithmic

pricing at offline retailers (Aparicio & Misra, 2023), as shown in a case study in collaboration with a consulting company offering AI solutions for price-setting.

We obtained data from one of their solutions, namely automating pricing and implementing ESLs for 225 gift and memorabilia stores in museums, aquariums, and zoos in the U.S. and Canada. Prior to this implementation, the stores had a corporate policy of updating prices no more than twice a year (due to the high labor costs of manual price updates). However, by implementing the ESL technology, the stores were able to make numerous price changes for offline products on the shelf with a single click or algorithmically. In fact, our evidence suggests that stores that increasingly adopted ESLs across categories increased the frequency of price changes. This is consistent with extant literature which utilizes the frequency of price changes to infer adoption or use of algorithmic pricing (Aparicio & Misra, 2023). See Web Appendix C for additional details.

While technology facilitates the adoption of algorithmic pricing, there are numerous managerial and organizational challenges. One is that algorithmic pricing may determine different optimal prices for online and offline channels. In particular, retailers may want to charge an offline price premium to reflect higher costs of offline channels. However, previous research has shown that consumers may be unwilling to accept an offline price premium (Homburg, Lauer, & Vomberg, 2019). Therefore, algorithmic pricing that optimizes online and offline prices should consider the maximum price differential customers are willing to accept between channels. Moreover, there may be differences in the input data available for both channels, with offline channels likely having less consumer and competitor data.

Although it may be easier for online retailers to identify individual customers, it is likely to be more difficult in physical stores unless customers are members of the firm's loyalty program. Similarly, the types of customers (and their behaviors) who enter a physical store may differ from

those who browse online. Finally, there may be important management frictions or barriers for omnichannel retailers if the algorithms (or their inputs and capabilities) differ across channels. For example, a retailer's online assortment may be significantly larger than its offline assortment. Moreover, online prices often change multiple times a day, and it is unclear whether managers would want to replicate this variability in stores. As such, managers interested in algorithmic pricing should be prepared to deal with a variety of algorithms, decision rules, human-in-the-loop criteria, and data constraints that can vary dramatically between customer touch points.

### **3.4.4. Promotions**

Companies need to be mindful of how and when they communicate their use of algorithmic pricing, as well as how they describe what their algorithms do and the price variations consumers may encounter (Kahneman et al., 1986). For example, a company would likely be better off framing a pricing algorithm in a way that emphasizes that consumers will receive a lower price during periods of low demand, rather than emphasizing the possibility of higher prices during periods of high demand. A recent example of this is the controversy over Wendy's use of dynamic pricing,5 which was framed in the press as surge pricing—leading consumers to associate the pricing with higher costs during peak demand. Had Wendy's instead emphasized discounts during off-peak hours, consumer reactions might have been more favorable.

The implementation of algorithmic pricing also affects how price promotions are utilized. Frequent algorithmic price changes could replace or eliminate traditional price promotions altogether. However, a firm may still be interested in signaling price promotion to consumers, such

<sup>5</sup> See[: https://www.inc.com/bruce-crumley/dynamic-pricing-keeps-spreading-despite-protest-from-wendys](https://www.inc.com/bruce-crumley/dynamic-pricing-keeps-spreading-despite-protest-from-wendys-customers.html)[customers.html.](https://www.inc.com/bruce-crumley/dynamic-pricing-keeps-spreading-despite-protest-from-wendys-customers.html) 

as highlighting a specific absolute or relative discount (S.-F. S. Chen, Monroe, & Lou, 1998). In such cases, the firm must determine how to calculate discounts relative to past dynamic prices, while ensuring compliance with any potential regulatory requirements (Friedman, 2015).

29

Algorithmic pricing can be integrated with other algorithmically driven marketing mix elements, such as digital ad buying and targeting. For example, customer data can serve as input for both algorithmic pricing personalization and ad targeting, while advertising metrics such as click-through rate can be used to evaluate and optimize both pricing and advertising strategies.

## <span id="page-30-0"></span>**4. Key Regulatory Concerns in Algorithmic Pricing Implementation**

In recent years, researchers, policymakers, and antitrust agencies worldwide have been examining the opportunities and risks associated with algorithms, particularly pricing algorithms. While algorithms can have pro-competitive effects by enhancing supply- and demand-side efficiencies (OECD, 2017), they also raise significant concerns among regulators that firms must consider when implementing algorithmic pricing (OECD, 2023).

A primary concern is their potential to facilitate collusion, resulting in higher prices. This can occur through algorithms that support explicit agreements, hub-and-spoke arrangements where multiple firms rely on the same third-party pricing software, or algorithmic autonomous tacit collusion (Competition & Markets Authority, 2021; Li, Xie, & Feyler, 2021). Additionally, there are concerns about the extent of price discrimination enabled by the availability of vast consumer data and the use of advanced dynamic or personalized pricing algorithms. [Table 6](#page-31-1) outlines the key implementation features of these algorithms in relation to these regulatory concerns, which we discuss in more detail in the following sections.

| Regulatory concerns                |                                                                         | Related<br>implementation features (inputs, rules, outputs)                                                                                                                                                                                                                                                                                                                                 |  |  |
|------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
|                                    | Algorithms<br>facilitating explicit<br>collusion                        | •<br>Input: Shared pricing rules or access to common pricing<br>data.<br>•<br>Rules: Implement coordinated pricing rules via the<br>algorithm or use it to detect and respond to deviations in<br>order to stabilize agreements (e.g., price-fixing or resale<br>price maintenance).<br>•<br>Output: Supracompetitive prices aligned with the<br>collusive agreement or retaliatory prices. |  |  |
| Price collusion                    | Algorithmic<br>collusion<br>in hub<br>and-spoke settings                | •<br>Input: Information exchange facilitated by third-party<br>software.<br>•<br>Rules: Pricing algorithm provided by a central data<br>analytics company.<br>•<br>Output: Potential collusive pricing—intentional<br>or not—<br>due to shared algorithm reliance.                                                                                                                          |  |  |
|                                    | Algorithmic<br>autonomous tacit<br>collusion                            | •<br>Input: Data on market conditions and competitor behavior.<br>•<br>Rules: Self-learning algorithms autonomously adapt<br>pricing strategies to avoid competition.<br>•<br>Output: Supracompetitive prices without explicit<br>communication or agreement.                                                                                                                               |  |  |
|                                    | (Unlawful)<br>discrimination from<br>dynamic pricing<br>algorithms      | •<br>Input: Real-time demand and supply data.<br>•<br>Rules: Adjust prices dynamically based on market<br>fluctuations without personalizing to individuals.<br>•<br>Output: Dynamic pricing that may inadvertently lead to<br>unfair outcomes for some consumers.                                                                                                                          |  |  |
| (Unlawful) price<br>discrimination | (Unlawful)<br>discrimination from<br>Personalized pricing<br>algorithms | •<br>Input: Consumer-specific data (e.g., behavior, location,<br>purchasing history).<br>•<br>Rules: Use algorithms to estimate willingness to pay and<br>set individualized prices.<br>•<br>Output: Tailored prices that maximize revenue, with<br>potential risks of discrimination or unfair practices.                                                                                  |  |  |

# <span id="page-31-1"></span>**Table 6: Regulatory Concerns and Key Implementation Features**

### <span id="page-31-0"></span>**4.1. Price Collusion**

While the existing work on algorithmic collusion is growing, empirical studies remain limited. On the theoretical front, Calvano et al. (2020) studied the potential impact of algorithmic pricing on collusion using simulations. Using a canonical oligopoly model with repeated, simultaneous price competition, they allow each simulated firm to use Q-learning to update their pricing rules. They find that the algorithms consistently learn to charge supracompetitive prices, without communicating with one another. Consistent with theory, the high prices are sustained by collusive strategies with a finite phase of punishment followed by a gradual return to cooperation. Similarly, after documenting heterogeneity among firms in the pricing technology employed and the frequency of price updates for OTC allergy drugs, Brown and MacKay (2023) developed a model in which firms can differ in pricing frequency and adopt pricing algorithms that respond to rivals' prices. Their model and simulation show that, in a competitive (Markov perfect) equilibrium, the introduction of simple pricing algorithms can generate price dispersion, raise price levels, and amplify the price effects of mergers.

31

More recently, Fish et al. (2024) used Open AI's GPT-4 to conduct experiments with algorithmic pricing agents, demonstrating that LLM-based pricing agents quickly and consistently collude in oligopoly settings, even when instructed only to seek long-run profits, with no explicit or implicit suggestion of collusion. Conversely, others argued that algorithmic pricing may improve firms' price responses to demand fluctuations, increasing incentives for firms to deviate from collusive prices. This could make collusive pricing less sustainable under algorithmic pricing (Miklós-Thal & Tucker, 2019; O'Connor & Wilson, 2021). Overall, while there is little theoretical certainty about the impact of algorithmic price competition on collusive outcomes, the recent capabilities of LLM-driven agents raise concerns about algorithmic collusion.

Empirical research has primarily focused on hub-and-spoke settings where multiple firms use the same third-party pricing software. Assad et al. (2024) studied the impact of algorithmic pricing in Germany's retail gasoline market. Using instrumental variables to control for the potential endogeneity of the adoption decision, Assad et al. (2024) found that pricing algorithm adoption increases the profit margin in duopoly and triopoly markets, but only if all stations adopt the algorithm. Calder-Wang and Kim (2023) examined algorithmic pricing in property

management and found that adoption enables managers to set more responsive prices. Buildings using the software increased prices during booms and lower them during busts compared to nonadopters. Applying a structural housing demand model and a conduct test in the Seattle market, they found limited evidence of coordination. These studies underscore that the mere use of the same pricing algorithm by firms is not sufficient to imply a tacitly coordinated outcome. Beyond collusion, another concern that arises when market players rely on the same algorithms is error propagation, potentially leading to lasting price bubbles even in competitive markets. Fu, Jin, and Liu (2022) studied Zillow's Zestimate algorithm and, while highlighting the human-algorithm feedback loop, dismissed concerns about persistent error propagation.

Despite the existing research on algorithmic collusion, its practical feasibility and scale remain uncertain. While the adoption of pricing algorithms has increased, their use is not yet universal, particularly for autonomous systems, and evidence of significant tacit collusion remains lacking. Nonetheless, competition authorities remain vigilant, publishing studies and organizing roundtables on this topic discussing the applicability and limitations of current regulations. 6

In the U.S., many experts argue that the current legal framework is sufficient to assess the pricing algorithms' collusive behavior. For example, the Sherman Act's Section 1 can impose criminal penalties for explicit collusion. A notable case occurred in November 2023 when the DC Attorney General announced a lawsuit alleging that 14 of DC's largest landlords coordinated through RealPage's centralized price-setting algorithm to artificially inflate rent prices.7 Addressing tacit collusion poses a greater challenge, and, at present, the Federal Trade

<sup>6</sup> See OECD (2023) for an extensive list of examples.

<sup>7</sup> Calder-Wang and Kim (2023) study is motivated by a series of class action lawsuits filed against RealPage regarding its use of algorithmic pricing.

Commission's (FTC) authority under Section 5 of the FTC Act, which targets prosecuting 'unfair methods of competition,' might be the only existing mechanism to oversee tacit algorithmic collusion. More recently, new bills have been proposed in the U.S. to strengthen enforcement under the Sherman Act and the FTC Act. For instance, on January 30, 2024, Senator Amy Klobuchar (D-MN), Chair of the Senate Subcommittee on Competition Policy, introduced the *Preventing Algorithmic Collusion Act* to prohibit pricing algorithms that facilitate collusion.8

33

In Europe, both the European Union (EU) (European Union, 2017) and the United Kingdom (UK) (OECD, 2017) largely share the U.S.'s position on algorithmic pricing, recognizing that most concerns can be effectively addressed within the existing competition law framework. For example, in 2018, the European Commission utilized existing antitrust legislation (namely, Article 101 TFEU), to penalize Asus, Denon & Marantz, Philips, and Pioneer for engaging in resale price maintenance tactics enabled by price comparison websites and specialized pricing platforms. These tools enabled the manufacturers to monitor online retailers' pricing, identify discrepancies, and enforce minimum retail prices.9

While existing tools may suffice to address algorithms that facilitate collusive agreements, the Organization for Economic Co-operation and Development (OECD) and other regulators recognize perceived shortcomings in current legislation, particularly regarding mechanisms to address cases involving a lack of explicit communication.

<sup>8</sup> U.S. legislators are also moving to adopt laws that prevent or regulate the use of algorithmic pricing in specific sectors. For example, two House representatives introduced the Preventing Algorithmic Facilitation of Rental Housing Cartels Act on 6 June 2024, which would prohibit digital price-fixing by landlords.

<sup>9</sup> See https://ec.europa.eu/competition/antitrust/cases/dec\_docs/40465/40465\_337\_3.pdf

#### **4.2. (Unlawful) Price Discrimination**

Price discrimination is often regarded by economists as a way to enhance market efficiency, especially when it approaches first-degree price discrimination. While not inherently illegal, it becomes prohibited when linked to anticompetitive, unfair, or deceptive practices. The use of pricing algorithms, combined with increasing customer data availability, has made price discrimination more feasible, drawing greater legislative and regulatory scrutiny.

Algorithmic price discrimination can result from dynamic pricing, which adjusts prices in real time based on fluctuations in supply and demand, or personalized pricing, which tailors prices using individual consumer data, such as search history, location, or device.

### **4.2.1. Dynamic Pricing**

Because dynamic pricing can optimize prices based on real-time market conditions such as demand, it can be harmful, by potentially enabling the exploitation of consumers and creating a perception of unfairness. For example, during unusual events that disrupt markets, such as floods (Crane, 2023), bombings, and terrorist attacks (Roberts, 2016), prices for car share rides for companies like Uber and Lyft rose to much higher levels than were usually experienced in the market. Other examples of "price gouging" include the high observed prices of flights and water sold through online markets before an approaching hurricane (Popomaronis, 2017). Although some firms impose price caps during emergencies and override their dynamic pricing algorithms (Mutzabaugh, 2017), or explore alternative solutions to balance supply and demand, such as offering higher compensation to car share drivers during emergencies (Carlson, 2012), these practices are not always implemented and their effectiveness can vary. In other situations, there may be concerns that dynamic pricing might disproportionately adversely affect lower income or other disadvantaged consumers. For example, when dynamic pricing is used for energy prices,

lower income consumers might have less flexibility for reducing their energy use (e.g., seniors who need to use air conditioning for their health) or shifting their use to lower priced times such as nights (e.g., if lower income individuals are more likely to work at those times).

35

Charging "excessive" prices constitutes an abuse of dominance in many countries, including almost all OECD members; under EU competition law, agencies can sanction dominant firms for using their market power to exploit consumers directly through Article 102 TFEU. In the U.S., excessive prices per se are not a matter of federal competition enforcement, but many states have laws that regulate price gouging by limiting price increases for essential goods and services, such as gasoline during emergencies. 10

#### **4.2.2. Personalized Pricing and Data Privacy**

While personalized pricing does not seem to be as widespread as dynamic pricing, advancements in technology and the increasing availability of customer data have made it more feasible and, consequently, a focus of legislative and regulatory scrutiny.11, <sup>12</sup>

Traditionally, the economics literature identifies three cumulative conditions for effective price discrimination, all of which apply to personalized pricing: firms must have some degree of market power, consumers must exhibit heterogeneity in willingness to pay that firms can identify,

<sup>10</sup>Despite the efforts of existing state laws to curb price gouging, concerns persist regarding their effectiveness in addressing algorithmic price gouging practices, primarily due to the fact that these laws were enacted before the emergence of algorithmic pricing and digital commerce (K. R. Williams (2022)).

<sup>11</sup>For an overview of evidence on the practical occurrence of personalized pricing, see Rott, Strycharz, and Alleweldt (2022).

<sup>12</sup>The OECD defines personalized pricing as "any practice of price discriminating final consumers based on their personal characteristics and conduct, resulting in each consumer being charged a price that is a function—but not necessarily equal—to his or her willingness to pay;" (OECD (2018)). This means that personalized pricing is not limited to perfect or first-degree price discrimination but can also encompass second- and third-degree price discrimination. However, with increasingly accurate and accessible data on customer characteristics, particularly for digital companies, adopting first-degree price discrimination and charging each consumer their exact willingness to pay, enabling the firm to capture the entire consumer surplus becomes more feasible (Ezrachi and Stucke (2016)).

36

and businesses need a mechanism to measure consumers' willingness to pay. Additionally, there must be no arbitrage among buyers. Among these, the ability of firms to measure consumer willingness to pay has grown significantly in recent years, driving concerns about the risks associated with personalized pricing.13

Economists have studied the impact of price discrimination in both monopoly and imperfectly competitive markets (see Verboven (2016), for a literature review on price discrimination and Botta and Wiedemann (2019) for a discussion in the digital context). This research highlights that personalized pricing can, on the one hand, substantially improve allocative efficiency by enabling companies to serve low-end consumers who would otherwise be underserved. On the other hand, its effects on distributional outcomes—across firms and different types of consumers—and on dynamic efficiency remain unclear, as such practices can promote both innovation and rent-seeking behavior. Using two randomized field experiments on ZipRecruiter, Dubé and Misra (2023) are the first to document both the feasibility and implications of scalable personalized pricing. They found that personalized pricing can improve expected profits by 19 percent relative to the uniform price optimized to reflect the firm's market power, and by 86 percent relative to the nonoptimized uniform price. While total consumer surplus decreased under personalized pricing, they showed that over 60 percent of consumers benefit from personalization. Under some inequity-averse welfare functions, they showed that consumer welfare may even increase with personalized pricing.

<sup>13</sup>Personalized pricing requires market power, as perfectly competitive markets drive prices down to marginal costs. It is, however, not limited to monopolies and is feasible in markets with economies of scale, scope, network effects, entry costs, or switching costs, which allow firms to charge prices above marginal cost.

While the effect of price discrimination on consumers' welfare is ambiguous, research suggests that, while consumers may accept traditional forms of price discrimination, such as thirddegree price discrimination (e.g., age-based discounts), they tend to be less receptive to personalized pricing. This resistance is largely attributed to perceived fairness concerns and a lack of transparency in pricing algorithms. Consumers may view personalized pricing as unfair, as it can lead to different prices for identical goods or services. Furthermore, the opacity of pricing algorithms can erode consumer trust and satisfaction (Xia, Chatterjee, & May, 2019; Zuiderveen Borgesius & Poort, 2017). See also Section [3.1](#page-11-1) for the detailed discussion of fairness perceptions.

37

In addition to concerns about consumer welfare, fairness, and transparency, Cheng and Nowag (2022) argued that personalized algorithmic pricing can also enable firms to engage in harmful exclusionary business practices. Through the use of predatory pricing, rebates, tying, and bundling, firms can limit or exclude competitors from the market, thus engaging in anticompetitive conduct. Personalized pricing makes it easier for incumbent firms to implement predatory strategies by targeting specific customer segments that pose a threat to their market position. By focusing on the entrant's strongest customer groups while maintaining control over their own, incumbent firms can minimize losses and effectively deter competition.

Considering this body of research, personalized pricing presents policymakers with the challenge of balancing competing goals. On the one hand, it can expand market access for consumers with lower willingness to pay. On the other hand, it raises concerns about fairness, transparency, and potential discrimination. Consumers often perceive personalized pricing as unfair, particularly when the criteria for pricing decisions are unclear, undermining trust in digital markets. Moreover, unjustifiable forms of discrimination, such as price differences based on race or gender, cannot be ruled out.

The risks of personalized pricing can be addressed through policies and legal instruments. Privacy and data protection laws, which govern the collection, storage, and processing of personal data, indirectly affect pricing practices, particularly personalized pricing, which relies on the ability to gather and analyze consumer data to set individualized prices.14 Under the EU's General Data Protection Regulation (GDPR), the use of personal data, including internet identifiers, for price personalization must adhere to the principles of transparency, fairness, and lawfulness. Processing sensitive data, such as racial or ethnic origin, political opinions, health, or sexual orientation, is generally prohibited for price personalization unless the individual provides explicit consent. The GDPR also grants individuals the right not to be subject to decisions based solely on automated processing, including profiling, with significant or legal effects— except with consent. Countries like Australia, Brazil, Canada, China, India, Israel, Japan, South Africa, South Korea, Switzerland, Turkey, and the UK have enacted similar data privacy laws (Zafar, 2023).

In the U.S., various federal and state laws protect sensitive data that could influence personalized pricing. For example, the Equal Credit Opportunity Act (ECOA), enforced by the FTC, prohibits credit discrimination based on race, color, religion, sex, or other protected characteristics. Regulators have introduced tools like "algorithmic disgorgement" to adapt to the rise of AI. Since 2019, this penalty has required companies to delete machine learning models and algorithms developed using improperly obtained data, such as children's location data collected without parental consent.15 In July 2024, the FTC ordered eight companies to provide information

<sup>14</sup>Dube et al. (2024) offer a perspective based on the academic marketing literature that evaluates the various benefits and costs of existing and pending government regulations and corporate privacy policies.

<sup>15</sup>See Kate Kaye, The FTC's New Enforcement Weapon Spells Death for Algorithms, PROTOCOL (Mar. 14, 2022), https://www.protocol.com/policy/ftc-algorithm-destroy-data- privacy.

for a study on "surveillance pricing", out of the concern that firms that harvest consumers' personal data can put their privacy at risk and charge them higher prices via personalized pricing.16

However, even if an algorithm does not explicitly use protected characteristics like race, discrimination may still occur. This can happen when correlations exist between a person's protected attributes and their behaviors or other features in the data, leading to biased outcomes (Ascarza & Israeli, 2022).

Complementing privacy and data protection laws, disclosure regulations play a role in mitigating unfair personalized pricing practices. For instance, the GDPR requires data controllers to inform individuals about automated decision-making, including the logic involved and its potential consequences. However, as noted by Rott et al. (2022), this information is provided at data collection, not when used. Moreover, such disclosures are often buried in privacy notices that consumers rarely read or recall, rendering them ineffective when personalized prices are presented.

The Modernization Directive, adopted in 2019 and implemented in mid-2022, introduced significant updates to EU consumer protection law. Under the Consumer Rights Directive (CRD), it mandates that traders disclose the use of personalized pricing based on automated decisionmaking at the point of sale. This complements the GDPR by ensuring a minimum level of transparency during transactions. The updated CRD has shown some effectiveness. For example, Tinder, after dialogue with the European Commission, committed to informing consumers by mid-April 2024 about the use of automated means for personalized discounts, including age-based

<sup>16</sup>See FTC press release "FTC Issues Orders to Eight Companies Seeking Information on Surveillance Pricing" (July 23 2024), https://www.ftc.gov/news-events/news/press-releases/2024/07/ftc-issues-orders-eight-companiesseeking-information-surveillance-pricing.

pricing, and explaining the reasons for such discounts, like consumers' lack of interest in premium services at standard rates.

However, the Modernization Directive's scope is limited. It excludes contracts related to healthcare, social services, gambling, financial services, real estate, passenger transport, package travel, and food or beverage delivery to consumers' homes. Additionally, disclosure requirements apply only to distance selling and off-premises contracts and do not cover dynamic pricing unless based on automated decision-making with personal data. Traders also are not required to disclose the parameters used to personalize prices—only that the price has been personalized.

More broadly, the effectiveness of disclosure requirements remains questionable. A 2021 OECD study, based on lab experiments in Ireland and Chile, revealed that online disclosures had limited impact on consumers' ability to identify and comprehend personalized pricing and did not significantly influence purchasing behavior (OECD, 2021).

Lastly, exclusionary business practices and other anticompetitive effects of price discrimination can be addressed within the framework of competition law. In the U.S., the Sherman Antitrust Act and subsequent legislation, such as the Robinson-Patman Act of 1936, provide mechanisms to regulate such practices. Similarly, Article 102 of the TFEU in the EU prohibits abuses of dominant market positions, including certain forms of discriminatory pricing. However, these rules typically applied to firms with significant market power, which, while likely aligning with the situations where personalized pricing is most problematic, may limit their applicability to broader concerns about personalized pricing.

### <span id="page-41-0"></span>**5. Conclusion and Research Priorities**

In this paper, we define algorithmic pricing and clarify its relationship with other forms of pricing. We explore the issues and challenges associated with the strategic alignment of

algorithmic pricing with respect to customers, competition, and the firm, i.e., its organization and marketing mix, and the consideration of key regulatory concerns. Additionally, we offer empirical insights into the implementation of algorithmic pricing through interviews with pricing executives, a survey of pricing managers, and a case study.

41

Our discussion highlights the interdependencies of algorithmic pricing with a firm's marketing strategy and regulatory concerns. Our empirical evidence shows that while firms recognize the potential of algorithmic pricing, they face organizational and implementation challenges. Firms are particularly concerned about customer reactions to the implementation of algorithmic pricing, which interestingly appears to mitigate some regulatory concerns. For example, fears of customer backlash likely limit firms' use of unfair algorithmic pricing practices, including discriminatory use of consumer data. Furthermore, managers expect pricing algorithms to foster competition and lower prices rather than promote collusive behavior.

We next outline questions and priorities for future research related to algorithmic pricing, which we structure based on our discussions in Section [3](#page-11-0) and [4,](#page-30-0) and in line with [Figure 1.](#page-6-0) See [Table 7](#page-48-0) below for a summary of the key research priorities.

In particular, we identify five research priorities related to customers and algorithmic pricing: (i) customers' perceptions of the use of algorithmic pricing and the price levels resulting from its use. It is also important to understand how these perceptions evolve as algorithmic pricing becomes more widespread. Future research can explore how customers' perceptions of algorithmic pricing change over time and across industries, with changes in the overall price level (i.e., whether prices are increasing or decreasing on average) and the degree of price dispersion (i.e., whether there is a lot of variation in prices paid across customers over time and/or at a point in time) as important moderators. (ii) The effect of transparency regarding the use and specific features of pricing algorithms on customer perceptions of algorithmic pricing. Future research can examine how firm's transparency and communication about algorithmic pricing influence customer perceptions of the fairness, and how these perceptions evolve over time. Future research may help to better understand the extent to which disclosure of the use of algorithmic pricing affects consumer decisions. Another promising area for transparency-related research is how Generative AI (GenAI) can be used to better explain the results of algorithmic pricing to customers and enhance customers' perceptions. For example, *Jean-Manuel Izaret* suggests adding GenAI as an additional layer of explanation: "GenAI is now becoming a tool to help explain what the algorithms are doing and make it more accessible. Pricing algorithms that make millions of pricing decisions, tend to be quite opaque, it's hard to understand what's happening."

42

(iii) The impact of algorithmic pricing on consumers' quality inferences from prices across product categories. Future research can measure price-quality inferences for different product categories, considering firms' use of algorithmic pricing in those categories (e.g., the price of a bottle of wine), or of a meal at a restaurant that uses algorithmic pricing vs. one that does not. (iv) The impact of algorithmic pricing on reference prices and price sensitivity. Future research can experimentally test the impact of different degrees of pricing automation on consumers' price sensitivity and (ability to form) reference prices. (v) Future research can test the effect of a firm's use of algorithmic pricing on consumers' perceptions of and loyalty to a brand, considering both the firm's implementation and its transparency about the practice (e.g., whether algorithmic pricing increases price search and sensitivity, leading to higher chances of switching and reduced loyalty).

With respect to the impact of algorithmic pricing on competition, future research should (vi) examine the longer-term impact of pricing algorithms on market structure, price levels, price dispersion and firms' profitability. This would allow testing whether managers' expectations that pricing algorithms will increase competition rather than facilitate collusive behavior are correct. Relatedly, future research can assess how managers react to the competitive aspects of algorithmic pricing in their preferences for different competitive strategies. Moreover, we invite future research to (vii) examine the risk of firms inadvertently colluding, as pricing algorithms may enable new forms of collusion that firms are unaware of.

43

With respect to the alignment of algorithmic pricing within the organization, we recommend future research to (viii) examine the antecedents and moderators of managers' potential aversion to acceptance of pricing algorithms. The results from our survey and interviews provide insights into what factors impact the adoption of pricing algorithms, including managers' reduced transparency and control over pricing decisions, along with negative consumer perceptions. However, more research is needed as managers' perceptions of algorithms are likely to evolve with the increasing adoption of AI applications. Future research should also (ix) investigate the optimal level and type of managerial input required, along with its implications for data requirements. This is particularly relevant given that only slightly more than half of the companies in our survey used information about competing firm's prices and past consumer behavior. It is essential to study the importance of incorporating such information sources. Finally, we invite future research to (x) examine whether firms need to adopt institutional and technical measures to prevent discriminatory and anticompetitive outcomes of algorithmic pricing. Relatedly, firms should assess the implications for organizational governance as decision-making shifts to pricing algorithms, with a particular focus on adjustments to accountability and (internal) oversight.

With respect to the marketing mix instrument Price, future research can (xi) examine the prevalence of different types of pricing algorithms (dynamic vs. personalized, vs. both) and how they have evolved over time. This may require developing new empirical methods to study these algorithms. Future research should also (xii) examine how algorithmic pricing models can be adapted to the increasing use of subscription-based revenue models, for example, in digital products like content streaming or subscriptions to digital features in cars (e.g., extended battery range). Furthermore, future research can (xiii) explore how algorithmic pricing affects strategic pricing considerations, including the implementation of skimming vs. penetration strategies.

44

Future research on the Product marketing mix instrument can (xiv) quantify the effectiveness of algorithmic pricing across product types (durable vs. consumable, goods vs. services, utilitarian vs. hedonic) and across industries (including business vs. consumer markets). In addition, future research can (xv) explore how firms should calibrate pricing algorithms across product lines to ensure consistency with brand positioning and avoid unintended signaling effects. Moreover, future research can (xvi) explore how a firm's use of algorithmic pricing affects the design of new products, e.g., regarding the (digital) modification of product features and add-ons.

Future research on the Place marketing mix element can (xvii) examine the effectiveness of algorithmic pricing across geographic locations and online vs. offline markets, as well as (xviii) how consumers perceive and respond to cross-channel price differences when prices are determined algorithmically. Finally, future research can (xix) study whether algorithmic pricing can help moderate or accelerate channel challenges such as channel conflicts.

Future research on the marketing mix element of Promotion can (xx) examine whether and how algorithmic pricing integrates with advertising and targeting strategies. Moreover, we invite future research to (xxi) investigate promotion framing effects regarding consumers' interpretation of algorithmically generated discounts compared to traditionally advertised promotions. Further, future research can (xxii) examine the extent to which frequent algorithmic price adjustments complement or substitute for traditional price promotions.

From a regulatory perspective, future studies are needed to (xxiii) investigate whether algorithmic price collusion exists across markets. This may require the development of new tools to detect algorithmic collusion, as well as (xxiv) the development of new tools for algorithmic auditing.17 In addition, future research needs to (xxv) examine the longer-term effects of pricing algorithms on competition, price levels, price dispersion, firm profitability, and consumer welfare.

Future research needs to (xxvi) examine the potential anticompetitive effects of dynamic or personalized pricing, and of different types of pricing algorithms (such as the "win-continuelose-reverse" rule and adaptive machine learning). For example, incumbents may use personalized pricing to minimize losses and effectively deter competition by focusing on an entrant's strongest customer groups while maintaining control over their own. In addition, future research can examine whether, as has been shown for ranking algorithms, algorithmic pricing can lead to selfpreferencing, thereby excluding competitors. In addition, (xxvii) firms and researchers need to assess the impact of emerging regulations (e.g., in the EU, the US, and China) on the adoption, conduct, and performance of pricing algorithms.

Future research can (xxviii) explore potential trade-offs between data requirements for efficient use of pricing algorithms and privacy or other data regulations, including the benefits and costs of pricing algorithms vs. other non-pricing algorithms that use personal data (e.g., personalized search rankings, advertising, and product recommendations). In addition, future

<sup>17</sup>Existing tools and methods used by for algorithmic auditing are discussed in detail in OECD (2023).

research can (xxix) explore the impact of data provided by consumers at the point of purchase and assess the influence of third-party data or consumer profiles on (personalized) pricing.

<span id="page-48-0"></span>

|  |  | Table 7: Key Research Priorities |  | for Algorithmic Pricing |  |
|--|--|----------------------------------|--|-------------------------|--|
|  |  |                                  |  |                         |  |

| Customers                                                 |                                                                                                                                                        |
|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| (i) Adoption and perceptions                              | How does the increasing adoption of<br>algorithmic pricing<br>affect<br>customer perceptions?                                                          |
| (ii) Transparency and<br>perceptions                      | How does transparency about algorithmic pricing affect customers'<br>(fairness) perceptions of pricing algorithms<br>and their decisions?              |
|                                                           | How can GenAI help explain algorithmically determined prices?                                                                                          |
| (iii) Price-quality relationships                         | How does algorithmic pricing change consumers' quality inferences<br>from prices (across<br>different product categories)?                             |
| (iv) Reference price effects and<br>price sensitivity     | How does algorithmic pricing affect reference price formation and<br>price sensitivity?                                                                |
| (v) Brand loyalty                                         | Does algorithmic pricing affect consumers' brand loyalty?                                                                                              |
| Competition                                               |                                                                                                                                                        |
| (vi) Long-term impact on<br>Competition                   | What is the long-term impact of pricing algorithms on market<br>structure, price levels, price dispersion,<br>and firms' profitability?                |
| (vii) Risk of collusion                                   | What is the risk of<br>firms inadvertently colluding?                                                                                                  |
| Company: Organization                                     |                                                                                                                                                        |
| (viii) Algorithmic aversion of<br>managers                | What are the key antecedents and moderators of managers' aversion<br>to<br>algorithms that inhibit their use?                                          |
| (ix) Input to pricing algorithms                          | What is the optimal level and type of managerial input,<br>and what are<br>the data requirements?                                                      |
| (x) Organizational governance<br>and (internal) oversight | Should firms establish institutional and technical policies to avoid<br>discriminatory and anticompetitive outcomes of algorithmic pricing?            |
| Company: Price                                            |                                                                                                                                                        |
| (xi) Prevalence of pricing<br>algorithms                  | What is<br>the prevalence of different types of pricing algorithms<br>(dynamic vs. personalized, vs. both),<br>and how have they evolved<br>over time? |
| (xii) Revenue model alignment                             | How can algorithmic pricing be aligned with subscription-based<br>models?                                                                              |
| (xiii) Strategic pricing                                  | How does the use of pricing algorithms affect strategic pricing<br>considerations?                                                                     |
| Company: Product                                          |                                                                                                                                                        |
| (xiv) Effectiveness of algorithmic<br>pricing             | How effective<br>is algorithmic pricing across product types (durable<br>vs. consumable, goods vs. services, utilitarian vs. hedonic)?                 |
| (xv) Product line consistency                             | How should firms calibrate pricing algorithms across product lines?                                                                                    |
| (xvi) New product design                                  | How does the firm's use algorithmic pricing affect the design of new<br>products?                                                                      |

### **Table 7 (cont.)**

| Company: Place                                                            |                                                                                                                         |  |  |  |
|---------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|--|--|--|
| (xvii) Channel-specific<br>effectiveness                                  | Studying the effectiveness of algorithmic pricing across geographic<br>locations, and online vs. offline markets        |  |  |  |
| (xviii) Cross-channel price<br>perception                                 | How do consumers perceive and respond to cross-channel price<br>differences when prices are algorithmically determined? |  |  |  |
| (xix) Channel conflicts                                                   | How does algorithmic pricing affect<br>channel challenges such as<br>channel conflicts?                                 |  |  |  |
| Company: Promotion                                                        |                                                                                                                         |  |  |  |
| (xx) Integration with advertising                                         | How should algorithmic pricing be integrated with advertising and<br>targeting strategies?                              |  |  |  |
| (xxi) Promotion framing effects                                           | How do consumers interpret algorithmically generated discounts<br>compared to traditional advertised promotions?        |  |  |  |
| (xxii) Substitution for traditional<br>promotions                         | To what extent does frequent algorithmic price adjustment<br>complement or substitute for traditional price promotions? |  |  |  |
| Regulatory concerns<br>and possible actions: Collusion                    |                                                                                                                         |  |  |  |
| (xxiii) Empirical definitions and<br>tests of collusive behavior          | Developing<br>new definitions for and empirical tests of potential price<br>collusion                                   |  |  |  |
| (xxiv) Automatic auditing tools                                           | Developing<br>new tools for algorithmic auditing                                                                        |  |  |  |
| (xxv) Long-term impact on<br>competition                                  | Studying<br>longer-term impact of pricing algorithms on competitive<br>behavior                                         |  |  |  |
| Regulatory concerns and possible actions: (Unlawful) Price discrimination |                                                                                                                         |  |  |  |
| (xxvi) Price discrimination and<br>anti-competitive behavior              | Studying<br>potential anticompetitive effects of dynamic or<br>personalized prices, such as self-preferencing           |  |  |  |
| (xxvii) Impact of new regulations                                         | Assessing<br>the impact of new<br>regulations on conduct and<br>performance of pricing algorithms                       |  |  |  |
| (xxviii) Data requirements and<br>privacy regulation                      | Studying<br>the trade-off between data requirements for efficient use of<br>pricing algorithms and privacy regulation   |  |  |  |
| (xxix) Third party data                                                   | Assessing<br>the influence of third-party data on pricing                                                               |  |  |  |

# **References**

- Alba, J. W., Mela, C. F., Shimp, T. A., & Urbany, J. E. (1999). The Effect of Discount Frequency and Depth on Consumer Price Judgments. *Journal of Consumer Research*, *26*(2), 99–114. https://doi.org/10.1086/209553
- Aparicio, D., & Misra, K. (2023). Artificial Intelligence and Pricing. In K. Sudhir & O. Toubia (Eds.), *Review of Marketing Research. Artificial Intelligence in Marketing* (pp. 103–124). Emerald Publishing Limited. https://doi.org/10.1108/S1548-643520230000020005
- Ascarza, E., & Israeli, A. (2022). Eliminating unintended bias in personalized policies using bias-eliminating adapted trees (BEAT). *Proceedings of the National Academy of Sciences of the United States of America*, *119*(11), e2115293119. https://doi.org/10.1073/pnas.2115293119
- Assad, S., Clark, R., Ershov, D., & Xu, L. (2024). Algorithmic Pricing and Competition: Empirical Evidence from the German Retail Gasoline Market. *The Journal of Political Economy*, 0. https://doi.org/10.1086/726906
- Barocas, S., & Selbst, A. D. (2016). Big Data's Disparate Impact. *California Law Review*, *104*(3), 671–732.
- Bertini, M., & Koenigsberg, O. (2021). The Pitfalls of Pricing Algorithms: Be Mindful of How They Can Hurt Your Brand. *Harvard Business Review*, *99*(5), 74–83. Retrieved from https://hbr.org/2021/09/the-pitfalls-of-pricingalgorithms
- Botta, M., & Wiedemann, K. (2019). Exploitative Conducts in Digital Markets: Time for a Discussion after the Facebook Decision. *Journal of European Competition Law & Practice*, *10*(8), 465–478. https://doi.org/10.1093/jeclap/lpz064
- Botti, S., & McGill, A. L. (2011). The Locus of Choice: Personal Causality and Satisfaction with Hedonic and Utilitarian Decisions. *Journal of Consumer Research*, *37*(6), 1065–1078. https://doi.org/10.1086/656570
- Brown, Z. Y., & MacKay, A. (2023). Competition in Pricing Algorithms. *American Economic Journal: Microeconomics*, *15*(2), 109–156. https://doi.org/10.1257/mic.20210158
- Calder-Wang, S., & Kim, G. H. (2023). Coordinated vs Efficient Prices: The Impact of Algorithmic Pricing on Multifamily Rental Markets. *SSRN Electronic Journal.* Advance online publication. https://doi.org/10.2139/ssrn.4403058
- Calvano, E., Calzolari, G., Denicolò, V., & Pastorello, S. (2019). Algorithmic Pricing What Implications for Competition Policy? *Review of Industrial Organization*, *55*(1), 155–171. https://doi.org/10.1007/s11151-019- 09689-3
- Calvano, E., Calzolari, G., Denicolò, V., & Pastorello, S. (2020). Artificial Intelligence, Algorithmic Pricing, and Collusion. *American Economic Review*, *110*(10), 3267–3297. https://doi.org/10.1257/aer.20190623
- Campbell, M. C. (2007). "Says Who? !" How the Source of Price Information and Affect Influence Perceived Price (Un)fairness. *Journal of Marketing Research*, *44*(2), 261–271.
- Carlson, N. (2012). How A Sandy-Related PR Nightmare Cost Startup Uber \$100,000 In A Day. *Business Insider*. Retrieved from https://www.businessinsider.com/how-sandy-related-pr-nightmare-cost-startup-uber-100000-ina-day-2012-11
- Chen, L., Mislove, A., & Wilson, C. (2016). An Empirical Analysis of Algorithmic Pricing on Amazon Marketplace. In J. Bourdeau, J. A. Hendler, R. N. Nkambou, I. Horrocks, & B. Y. Zhao (Eds.), *Proceedings of the 25th International Conference on World Wide Web - WWW '16* (pp. 1339–1349). New York, New York, USA: ACM Press. https://doi.org/10.1145/2872427.2883089
- Chen, S.‑F. S., Monroe, K. B., & Lou, Y.‑C. (1998). The effects of framing price promotion messages on consumers' perceptions and purchase intentions. *Journal of Retailing*, *74*(3), 353–372. https://doi.org/10.1016/S0022- 4359(99)80100-6
- Cheng, T. K., & Nowag, J. (2022). Algorithmic Predation and Exclusion: LundLawCompWP. Retrieved from https://hub.hku.hk/bitstream/10722/311575/1/content.pdf?accept=1
- Choi, S., Song, M., & Jing, L. (2023). Let your algorithm shine: The impact of algorithmic cues on consumer perceptions of price discrimination. *Tourism Management*, *99*, 104792. https://doi.org/10.1016/j.tourman.2023.104792
- Cohen, P., Hahn, R., Hall, J., Levitt, S., & Metcalfe, R. (2016). *Using Big Data to Estimate Consumer Surplus: The Case of Uber*. Cambridge, MA: National Bureau of Economic Research. https://doi.org/10.3386/w22627

- Competition & Markets Authority (2021). Algorithms: How They Can Reduce Competition and Harm Consumers. Retrieved from https://www.gov.uk/government/publications/algorithms-how-they-can-reduce-competition-andharm-consumers/algorithms-how-they-can-reduce-competition-and-harm-consumers
- Crane, E. (2023). Uber, Lyft Ripped for Surging NYC Prices during Storm, Flooding: 'Slime Balls'. *New York Post*. Retrieved from https://nypost.com/2023/09/29/new-yorkers-rip-uber-lyft-for-surging-prices-during-storm/
- Diab, D. L., Pui, S.‑Y., Yankelevich, M., & Highhouse, S. (2011). Lay Perceptions of Selection Decision Aids in US and Non-US Samples. *International Journal of Selection and Assessment*, *19*(2), 209–216. https://doi.org/10.1111/j.1468-2389.2011.00548.x
- Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015). Algorithm aversion: People erroneously avoid algorithms after seeing them err. *Journal of Experimental Psychology. General*, *144*(1), 114–126. https://doi.org/10.1037/xge0000033
- Dietvorst, B. J., Simmons, J. P., & Massey, C. (2018). Overcoming Algorithm Aversion: People Will Use Imperfect Algorithms If They Can (Even Slightly) Modify Them. *Management Science*, *64*(3), 1155–1170. https://doi.org/10.1287/mnsc.2016.2643
- Duani, N., Barasch, A., & Morwitz, V. (2024). Demographic Pricing in the Digital Age: Assessing Fairness Perceptions in Algorithmic versus Human-Based Price Discrimination. *Journal of the Association for Consumer Research.* Advance online publication. https://doi.org/10.1086/729440
- Dube, J.‑P. H., Bergemann, D., Demirer, M., Goldfarb, A., Johnson, G., Lambrecht, A., . . . Lynch, J. G. (2024). The Intended and Unintended Consequences of Privacy Regulation for Consumer Marketing: A Marketing Science Institute Report. *SSRN Electronic Journal.* Advance online publication. https://doi.org/10.2139/ssrn.4847653
- Dubé, J.‑P., & Misra, S. (2023). Personalized Pricing and Consumer Welfare. *The Journal of Political Economy*, *131*(1), 131–189. https://doi.org/10.1086/720793
- Elmaghraby, W., & Keskinocak, P. (2003). Dynamic Pricing in the Presence of Inventory Considerations: Research Overview, Current Practices, and Future Directions. *Management Science*, *49*(10), 1287–1309. https://doi.org/10.1287/mnsc.49.10.1287.17315
- Erdem, T., Keane, M. P., & Sun, B. (2008). A Dynamic Model of Brand Choice When Price and Advertising Signal Product Quality. *Marketing Science*, *27*(6), 1111–1125. https://doi.org/10.1287/mksc.1080.0362
- European Union (2017). Algorithms and Collusion Note from the European Union. Retrieved from https://one.oecd.org/document/DAF/COMP/WD(2017)12/en/pdf
- Ezrachi, A., & Stucke, M. E. (2016). *Virtual Competition*. Harvard University Press. https://doi.org/10.4159/9780674973336
- Fantini, F., & Das Narayandas (2023). Analytics for Marketers: When to Rely on Algorithms and When to Trust Your Gut. *Harvard Business Review*, *101*(3), 82–91. Retrieved from https://hbr.org/2023/05/analytics-for-marketers
- Feinberg, F. M., Krishna, A., & Zhang, Z. J. (2002). Do we care what others Get? A Behaviorist Approach to Targeted Promotions. *Journal of Marketing Research*, *39*(3), 277–291. https://doi.org/10.1509/jmkr.39.3.277.19108
- Fish, S., Gonczarowski, Y. A., & Shorrer, R. I. (2024). *Algorithmic Collusion by Large Language Models*. arXiv. https://doi.org/10.48550/arXiv.2404.00806
- Friedman, D. A. (2015). Reconsidering Fictitious Pricing. *Minnesota Law Review*, *100*, 921–982.
- Fu, R., Jin, G. Z., & Liu, M. (2022). *Does Human-algorithm Feedback Loop Lead to Error Propagation? Evidence from Zillow's Zestimate*. Cambridge, MA: National Bureau of Economic Research. https://doi.org/10.3386/w29880
- Gabel, S., & Guhl, D. (2022). Comparing the effectiveness of rewards and individually targeted coupons in loyalty programs. *Journal of Retailing*, *98*(3), 395–411. https://doi.org/10.1016/j.jretai.2021.08.001
- Hansen, K. T., Misra, K., & Pai, M. M. (2021). Frontiers: Algorithmic Collusion: Supra-competitive Prices via Independent Algorithms. *Marketing Science*, *40*(1), 1–12. https://doi.org/10.1287/mksc.2020.1276
- Haws, K. L., & Bearden, W. O. (2006). Dynamic Pricing and Consumer Fairness Perceptions. *Journal of Consumer Research*, *33*(3), 304–311. https://doi.org/10.1086/508435
- Hill, D. (2015). The Secret of Airbnb's Pricing Algorithm. *IEEE Spectrum*. Retrieved from https://spectrum.ieee.org/computing/software/the-secret-of-airbnbs-pricing-algorithm
- Kahneman, D., Knetsch, J., & Thaler, R. (1986). Fairness as a Constraint on Profit Seeking: Entitlements in the Market. *American Economic Review*, *76*(4), 728–741.
- Keinan, A., Crener, S., & Goor, D. (2020). Luxury and environmental responsibility. In F. Morhart, K. Wilcox, & S. Czellar (Eds.), *Research Handbook on Luxury Branding*. Edward Elgar Publishing. https://doi.org/10.4337/9781786436351.00031
- Kim, T., Barasz, K., John, L. K., & Norton, M. I. (2022). When Identity-Based Appeals Alienate Consumers. *Harvard Business School NOM Unit Working Paper No. 19-086*.
- Kopalle, P. K., Pauwels, K., Akella, L. Y., & Gangwar, M. (2023). Dynamic pricing: Definition, implications for managers, and future research directions. *Journal of Retailing*, *99*(4), 580–593. https://doi.org/10.1016/j.jretai.2023.11.003
- Kuo, A., Rice, D. H., & Fennell, P. (2016). How fitting! The influence of fence-context fit on price discrimination fairness. *Journal of Business Research*, *69*(8), 2634–2640. https://doi.org/10.1016/j.jbusres.2016.04.020
- Lagerlöf, J. N. (2023). Surfing incognito: Welfare effects of anonymous shopping. *International Journal of Industrial Organization*, *87*, 102917. https://doi.org/10.1016/j.ijindorg.2022.102917
- Li, S., Xie, C. C., & Feyler, E. (2021). Algorithms & Antitrust: An Overview of EU and National Case Law. Retrieved from https://www.concurrences.com/en/bulletin/special-issues/algorithms-competition/algorithms-antitrust-anoverview-of-eu-and-national-case-law
- Lu, S., Yao, D., Chen, X., & Grewal, R. (2021). Do Larger Audiences Generate Greater Revenues Under Pay What You Want? Evidence from a Live Streaming Platform. *Marketing Science*, *40*(5), 964–984. https://doi.org/10.1287/mksc.2021.1292
- Lu, Y., Wang, Y., Chen, Y., & Xiong, Y. (2023). The role of data‐based intelligence and experience on time efficiency of taxi drivers: An empirical investigation using large‐scale sensor data. *Production and Operations Management*, *32*(11), 3665–3682. https://doi.org/10.1111/poms.14056
- Lucas, G. M., Gratch, J., King, A., & Morency, L.‑P. (2014). It's only a computer: Virtual humans increase willingness to disclose. *Computers in Human Behavior*, *37*, 94–100. https://doi.org/10.1016/j.chb.2014.04.043
- Lyn Cox, J. (2001). Can differential prices be fair? *Journal of Product & Brand Management*, *10*(5), 264–275. https://doi.org/10.1108/10610420110401829
- Miklós-Thal, J., & Tucker, C. (2019). Collusion by Algorithm: Does Better Demand Prediction Facilitate Coordination Between Sellers? *Management Science*, *65*(4), 1552–1561. https://doi.org/10.1287/mnsc.2019.3287
- Mutzabaugh, B. (2017). Airlines Cap Fares Starting at \$99 from Florida Amid Price Gouging Complaints. *USA Today*. Retrieved from https://www.usatoday.com/story/travel/flights/todayinthesky/2017/09/06/airlines-cap-faresflorida-amid-price-gouging-complaints/640332001/
- O'Connor, J., & Wilson, N. E. (2021). Reduced demand uncertainty and the sustainability of collusion: How AI could affect competition. *Information Economics and Policy*, *54*, 100882. https://doi.org/10.1016/j.infoecopol.2020.100882
- OECD (2017). Algorithms and Collusion Note from the United Kingdom. Retrieved from https://one.oecd.org/document/DAF/COMP/WD(2017)19/en/pdf
- OECD (2018). Personalised Pricing in the Digital Era: Background Note by the Secretariat. Retrieved from https://one.oecd.org/document/DAF/COMP(2018)13/en/pdf
- OECD (2021). The effects of online disclosure about personalised pricing on consumers: Results from a lab experiment in Ireland and Chile. Retrieved from https://www.oecd.org/en/publications/the-effects-of-onlinedisclosure-about-personalised-pricing-on-consumers\_1ce1de63-en.html
- OECD (2023). Algorithmic Competition: OECD Competition Policy Roundtable Background Note. Retrieved from www.oecd.org/daf/competition/algorithmic-competition-2023.pdf
- Pizzutti, C., Gonçalves, R., & Ferreira, M. (2022). Information search behavior at the post-purchase stage of the customer journey. *Journal of the Academy of Marketing Science*, *50*(5), 981–1010. https://doi.org/10.1007/s11747-022-00864-9
- Popomaronis, T. (2017). Amid Preparations For Hurricane Irma, Amazon Draws Scrutiny For Price Increases. *Forbes*. Retrieved from https://www.forbes.com/sites/tompopomaronis/2017/09/06/hurricane-irma-resulting-in-claimsthat-amazon-is-price-gouging-what-we-know/?sh=1d35967e2bd3
- Prakash, D., & Spann, M. (2022). Dynamic pricing and reference price effects. *Journal of Business Research*, *152*, 300–314. https://doi.org/10.1016/j.jbusres.2022.07.037
- Rao, A. R., & Monroe, K. B. (1989). The Effect of Price, Brand Name, and Store Name on Buyers' Perceptions of Product Quality: An Integrated Review. *Journal of Marketing Research*, *16*(August), 351–357.
- Ratneshwar, S., & Mick, D. G. (2013). *Inside Consumption: Consumer Motives, Goals, and Desires*. Hoboken: Taylor and Francis.
- Raveendhran, R., & Fast, N. J. (2019). Technology and Social Evaluation: Implications for Individuals and Organizations. In R. N. Landers (Ed.), *The Cambridge Handbook of Technology and Employee Behavior* (pp. 921– 943). Cambridge University Press. https://doi.org/10.1017/9781108649636.034
- Raveendhran, R., & Fast, N. J. (2021). Humans judge, algorithms nudge: The psychology of behavior tracking acceptance. *Organizational Behavior and Human Decision Processes*, *164*, 11–26. https://doi.org/10.1016/j.obhdp.2021.01.001
- Roberts, J. J. (2016). Uber Slammed for Surge Prices After New York City Bombing. *Fortune*. Retrieved from https://fortune.com/2016/09/19/uber-chelsea-bomb/
- Rott, P., Strycharz, J., & Alleweldt, F. (2022). Personalised Pricing. Retrieved from https://www.europarl.europa.eu/RegData/etudes/STUD/2022/734008/IPOL\_STU(2022)734008\_EN.pdf
- Seele, P., Dierksmeier, C., Hofstetter, R., & Schultz, M. D. (2019). Mapping the Ethicality of Algorithmic Pricing: A Review of Dynamic and Personalized Pricing. *Journal of Business Ethics*, *65*(5), 2161. https://doi.org/10.1007/s10551-019-04371-w
- Seim, K., Vitorino, M. A., & Muir, D. M. (2017). Do consumers value price transparency? *Quantitative Marketing and Economics*, *15*(4), 305–339. https://doi.org/10.1007/s11129-017-9193-x
- Spann, M., Fischer, M., & Tellis, G. J. (2015). Skimming or Penetration? Strategic Dynamic Pricing for New Products. *Marketing Science*, *34*(2), 235–249. https://doi.org/10.1287/mksc.2014.0891
- Spann, M., Zeithammer, R., Bertini, M., Haruvy, E., Jap, S. D., Koenigsberg, O., Mak, V., Popkowski Leszczyc, P., Skiera, B., & Thomas, M. (2018). Beyond Posted Prices: The Past, Present, and Future of Participative Pricing Mechanisms. *Customer Needs and Solutions*, *5*(1-2), 121–136. https://doi.org/10.1007/s40547-017-0082-y
- Thaler, R. H. (1985). Mental Accounting and Consumer Choice. *Marketing Science*, *4*(3), 199–214.
- Verboven, F. (2016). Price Discrimination (Empirical Studies). In *The New Palgrave Dictionary of Economics* (pp. 1– 5). London: Palgrave Macmillan UK. https://doi.org/10.1057/978-1-349-95121-5\_2256-1
- Williams, G. Y., & Lim, S. (2024). Psychology of AI: How AI impacts the way people feel, think, and behave. *Current Opinion in Psychology*, *58*, 101835. https://doi.org/10.1016/j.copsyc.2024.101835
- Williams, K. R. (2022). The Welfare Effects of Dynamic Pricing: Evidence From Airline Markets. *Econometrica*, *90*(2), 831–858. https://doi.org/10.3982/ECTA16180
- Xia, F., Chatterjee, R., & May, J. H. (2019). Using Conditional Restricted Boltzmann Machines to Model Complex Consumer Shopping Patterns. *Marketing Science*, *38*(4), 711–727. https://doi.org/10.1287/mksc.2019.1162
- Yalcin, G., Lim, S., Puntoni, S., & van Osselaer, S. M. J. (2022). Thumbs Up or Down: Consumer Reactions to Decisions by Algorithms Versus Humans. *Journal of Marketing Research*, *59*(4), 696–717. https://doi.org/10.1177/00222437211070016
- Yeomans, M., Shah, A., Mullainathan, S., & Kleinberg, J. (2019). Making sense of recommendations. *Journal of Behavioral Decision Making*, *32*(4), 403–414. https://doi.org/10.1002/bdm.2118
- Zafar, F. (2023). 18 Countries with GDPR-like Data Privacy Laws. Retrieved from https://finance.yahoo.com/news/18-countries-gdpr-data-privacy-121428321.html
- Zuiderveen Borgesius, F., & Poort, J. (2017). Online Price Discrimination and EU Data Privacy Law. *Journal of Consumer Policy*, *40*(3), 347–366. https://doi.org/10.1007/s10603-017-9354-z