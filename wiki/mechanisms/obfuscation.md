# Obfuscation

Obfuscation is the deliberate production of **misleading, ambiguous, or plausibly-similar data** to frustrate surveillance and profiling. The theoretical anchor is Helen Nissenbaum (NYU) — her 2015 book *Obfuscation* (cited on [[adnauseam|AdNauseam]]) frames the strategy as a user-side defence against information-asymmetric surveillance. The mechanism underpins several of the [[possible-strategic-levers|profile-manipulation levers]] on the strategy layer (levers #6, #7, #10, #11). This page catalogues the theoretical anchor, live tool implementations, extracted strengths and weaknesses from the evidence base, the technical approach taxonomy, the countermeasure landscape, and the legal risk surface — in that order. For the editorial synthesis of what this means for building against dynamic pricing, see [[obfuscation-strategic-readout]].

## Core claim (Nissenbaum tradition)

Per the [[adnauseam|AdNauseam Wikipedia capture]]: "Nissenbaum, a professor at New York University, published her book *Obfuscation* to explain how irrelevant data can be used to preserve user privacy." The principle: where withdrawing data is infeasible (surveillance is ambient) or insufficient (the watcher can still infer from behaviour), producing **counterfeit data** that is indistinguishable from real data degrades the watcher's inferences.

Two live variants captured in this wiki:

| Variant | Target watcher | Method | Live tool | Banned / sustained? |
|---|---|---|---|---|
| Ad / tracking obfuscation | Advertising networks and tracker pipelines | Fake click events on blocked ads + decoy search queries | [[adnauseam]] (ad clicks), TrackMeNot (search queries) | **Banned by Google from Chrome Web Store January 2017** (per AdNauseam Wikipedia) — operational via Firefox and Chromium dev-mode |
| AI-training obfuscation | Generative AI model trainers scraping web images | Pixel-level perturbations that change the AI's feature representation while leaving human perception intact | [[nightshade-glaze|Nightshade (offensive) + Glaze (defensive)]] | Sustained; Glaze >6M downloads since March 2023 (per WebSearch preamble, MIT Tech Review Oct 2024) |

## Strengths — source-traceable claims

**Cost-asymmetry as the economic goal.** Nightshade's stated objective (per its primary source, cited on [[nightshade-glaze]]) is to "increase the cost of training on unlicensed data, such that licensing images from their creators becomes a viable alternative." The mechanism does not need to defeat adversary inference; it needs to raise the adversary's unit cost past the point where the legitimate alternative becomes preferable.

**Operational autonomy — no third-party data custodian.** The AdNauseam authors articulate this as a first-order design constraint: "AdNauseam was designed to function without ever communicating to a 'home server' or sending user-data to any other entity, for any reason" (Howe & Nissenbaum 2017, §III.B, on [[adnauseam|AdNauseam]] sources). Nightshade's primary source makes the same claim: "designed to run without a network, so there is no data (or art) sent back to us or anyone else" (per [[nightshade-glaze]]).

**Social / collective-goods framing — not just individual protection.** Howe & Nissenbaum 2017 quote Priscilla Regan: "privacy may serve social ends, similar to collective goods such as clean air or national defense." They reject the individual-utility framing and position obfuscation as expressive protest: "Rather than enacting privacy as concealment, AdNauseam provides a means for users to express, in plain sight, their dissent by disrupting the dominant model of commercial surveillance" (Howe & Nissenbaum 2017, §VI).

**Consumers DO manipulate when the pricing context is legible.** Bó, Chen & Hakimov 2024 (arXiv 2304.11415, Section 4.2) ran an online experiment where participants knew a statistical model would set their price from their survey answers. In the Risk-survey treatment (context similar to the product, a lottery ticket), they found "significant manipulation in seven questions in the Risk survey"; the predicted willingness-to-pay was significantly *lower* in the Risk survey than in the training data. This is direct empirical evidence that obfuscation-by-response-manipulation is not hypothetical — it happens naturally when consumers can reason about which inputs drive the price.

**Collective action scales super-linearly with size — up to a DP ceiling.** Solanki et al. 2025 (arXiv 2505.05707) formalise Algorithmic Collective Action (ACA): "a group of individuals, through coordinated changes in their data, can impact the behavior of deployed models" (§2.1, quoting Hardt et al. 2023). Their Theorem 1 (reproducing Hardt et al.) gives a lower bound on collective success that grows with the collective-size parameter α. Empirical validation on MNIST, CIFAR-10, and Bank Marketing confirms the qualitative shape: larger collectives push the success metric toward 100% on modified test data.

## Weaknesses — source-traceable claims

### Naive query / click obfuscation is statistically defeated by off-the-shelf ML

Peddinti & Saxena 2014 (JCS, captured as `06-03-peddinti-trackmenot-attack.md`) is the canonical attack paper on TrackMeNot. Headline result: an adversary using WEKA's default classifiers (Logistic Regression, Random Forest, SVM) on a two-month AOL query history achieved **"a mean false positive rate over all users [of] only 0.02%"** at distinguishing real from TMN-generated fake queries (§5.5). Real user queries were then identified with an average true-positive rate of 48.88% and, for some users, as high as 100% (§5.6).

Two root causes, both stated in the paper:

1. **The decoy source is fingerprintable.** TMN initializes from "popular RSS feeds and publicly available recent searches" (§5.1.1). Most users leave defaults. An independently-run TMN instance produces a similar seed vocabulary, so the search engine can train on that instance and apply the classifier to any user: "many users are not likely to pay attention to the RSS feeds chosen for query generation and may use the default ones" (§5.3).
2. **Real user queries are linkable by vocabulary tail.** "Prior research shows that users tend to pose exact same queries over and over" (§7.3); unique terms in each user's training history pull test queries into their cluster in word-vector space. Bookmarked queries were <6% of the test set but achieved true-positive rates 58–90%.

Rate manipulation (running TMN at 10/min vs 1/hr) did not help: "using different TMN average query frequencies would more or less provide the same level of privacy. In other words, higher TMN frequency may not help in hiding user's query, contrary to one's intuition" (§5.5, Table 2).

The authors frame this as a lower bound — an "unsophisticated" adversary using only default tools. Their forward-looking remark: "it would certainly be possible to improve our attacks by taking into account other information... exact query timestamps... exit node IP addresses... long-term (longer than 2 months) search histories" (§8).

### The indistinguishability–expression dilemma (Howe & Nissenbaum 2017 self-critique)

The AdNauseam authors' own published self-appraisal identifies a structural contradiction. From §IV: "For obfuscation to function effectively as a means of counter-surveillance, the noise generated must exhibit a high degree of *indistinguishability*... However, there are times when this goal comes into tension with other aims of the software, specifically that of protection, e.g., from malware." And the sharper version: "if a tool is undetectable to an adversary, its expressive capability is minimal... It appears, at least in a simplistic analysis, that a tool cannot simultaneously achieve expressivity and protect social privacy" (§IV, on [[adnauseam|AdNauseam]] sources).

If the click-probability is tuned high enough to register as protest, the adversary can simply "discard all clicks from the user in question; a result similar to that obtained from a successful blocking-only strategy... since the data is discarded there is no net gain in what we have referred to as social privacy" (Howe & Nissenbaum 2017, §IV).

### The individualistic-framing critique (Richards & Hartzog 2015)

Richards & Hartzog 2015 (Yale Law Journal book review of *Obfuscation*, captured as `08-02-yale-privacys-trust-gap.md`) concede that obfuscation is "pretty good protection" and "frequently good enough" and explicitly useful "when our backs are against the wall." They level a sharper structural critique:

> "It falls into the all-too-common trap of thinking about privacy in primarily individualistic terms, leveraging the weak power of individuals rather than the strong power of law and society. It reinforces the standard narrative of privacy that emphasizes control, choice, and privacy self-management above all else — a narrative that is likely doomed to failure." (§III)

And on the trust side:

> "Obfuscation is a creature of distrust — a last resort of the weak, the marginalized, and the betrayed. Obfuscation is not merely *motivated* by distrust; it also *creates* additional distrust by hiding from the surveillance economy or intentionally feeding bad data into it." (§II)

### Asymmetric resources favour the adversary at scale

Richards & Hartzog 2015 again: "If a motivated adversarial party is willing to invest the resources to counteract obfuscation, the rich and powerful will eventually win" (§III). They also note that obfuscation is available to the powerful — police and corporations can deploy it as cloaks: "increased use of obfuscation across the board could worsen existing power imbalances rather than shrink them." At best, "it preserves the status quo, perhaps minimizing the exploitation of the powerless, but doing relatively little to upset the power differentials that constitute the status quo."

### Users make *worse* privacy choices when the pricing context is opaque

Bó et al. 2024 contradict the intuition that opaque pricing would push consumers to buy privacy protection. In their Movies-survey treatment (context dissimilar from the lottery product), participants:

- Demanded privacy *less* than in the transparent Risk treatment — "the proportion of participants who chose the privacy option is significantly higher in the Risk treatment than in the Movies treatment" (23.2% vs 31.1%; Table 10, coefficient −0.078, p<0.05).
- Made worse decisions: "in the Movies survey, only 24% of participants who did not choose the privacy option did it optimally, while this proportion is 67% in the Risk survey" (Result 3).

Their stated interpretation: "These behavior patterns are consistent with participants being naïve regarding the relevance of their responses to movie ratings for personalized pricing" (§1). Payoffs were significantly lower in Movies, and the welfare gap was fully explained by the price difference (§4.3, Result 4).

The authors draw an explicit policy conclusion: "the sole use of notice and consent is probably insufficient to protect consumers due to strategic mistakes" (§1). This is the "notice-and-consent is broken" result from the consumer side — precisely the regime GDPR/CCPA rely on.

### Trust dependencies within collective obfuscation

Richards & Hartzog: "Collective obfuscation usually requires us to trust our confederates... The same gladiators who protected Spartacus from the Roman authorities could just as easily have identified him to those who would kill him" (§III). This applies directly to any proposed pricing-obfuscation co-op: the co-op operator becomes the new single point of trust.

## Technical approach taxonomy — source-traceable

This section inventories technical approaches that the captured sources describe or formalise. Each is a specific method a builder could implement; countermeasures to each are catalogued in the next section.

### 1. Decoy-traffic generation (query / click / behavioural)

Generate plausible-but-fake interactions that dilute the signal from real interactions. Live instances: [[adnauseam|AdNauseam]] (ad clicks) and TrackMeNot (search queries). Howe & Nissenbaum 2017 describe the AdNauseam decoy-generation approach (§III): "implemented via AJAX, which simulates requests (matching headers, referer, etc.) that the browser would normally send." Peddinti & Saxena 2014 document the failure mode (see Weaknesses above) — a naive RSS-seeded query generator is separable from user queries with 0.02% FPR.

### 2. Per-session identity rotation / fingerprint randomization

Cycle the user's apparent identity (cookies, fingerprint attributes, network egress) per session. See [[browser-fingerprinting]] for the fingerprint attribute catalogue from Lawall 2024. Countermeasure evidence: FP-Inconsistent (Venugopalan et al. 2024, arXiv 2406.07647) demonstrates that naive attribute-by-attribute rotation introduces cross-attribute inconsistencies detectable at ~97% true-negative-rate on real users.

### 3. Feature-label coordinated collective action (Solanki et al. formalism)

The most formally-characterised technical approach in the captured evidence. Solanki et al. 2025, §2.1: "the collective modifies both the features and labels for all data under their control... The data is modified in such a way that the classifier *f* learns to associate the transformed version of features with the chosen target label *y**... resulting in the strategy *h(x, y) = (g(x), y**)*." The collective picks a trigger function *g* and a target label *y**; a large enough collective forces the deployed model to associate *g(x)* with *y**.

Success scales with the collective-size parameter α. Solanki et al.'s Theorem 2 adds a DP-noise degradation term (see Countermeasures). Empirical validation across MNIST, CIFAR-10 (with pretrained ResNet18), and Bank Marketing (tabular feedforward) all show the same critical-mass threshold pattern.

### 4. Profile-injection / shilling attacks on recommender systems

Wang et al. 2024 (arXiv 2401.01527, captured as `03-08-poisoning-recsys-survey.md`) survey the recommender-system poisoning literature. Their top-level taxonomy has three dimensions (§1, Figure 1):

- **Component-Specific.** Target a specific RS component. Input-specific (interaction records, graph, KG, sequence, image, text); Recommender-specific (matrix factorization, neural CF, GNN, SSL, federated, explainable); Optimization-specific (targeting BPR loss, contrastive-learning loss).
- **Goal-Driven.** System degradation (untargeted — "deteriorate the user experience"), Targeted manipulation ("elaborately tailored to either promote or demote specific items within distinct user groups or all users"), Hybrid-goal.
- **Capability-Probing.** Knowledge-constrained (white-box / grey-box / black-box), Cost-efficient (minimize required manipulation — SUI-Attack injects a single user), Invisibility-assured (GAN-based methods like AUSH, LegUP, GOAT, GSPAttack that "engage in a competitive interaction to enhance the resemblance of generated user profiles to real user profiles").

### 5. Browser-level noise injection at sensitive APIs

Lawall 2024 (arXiv 2411.12045, captured as `04-09-fingerprinting-tracing-shadows.md`) catalogues Canvas, WebGL, AudioContext, and Font fingerprinting — the primary JavaScript-API-exposed entropy sources — and documents the extension-level noise response: "CanvasBlocker... allow[s] users to prevent data retrieval or manipulate Canvas data, continuously generating new fingerprints to prevent identification." Tor Browser takes a different approach ("fixed size of 1000x1000 pixels, reducing uniqueness") — uniformity rather than randomization.

### 6. Perturbation that survives downstream transformations

The Nightshade design principle as cited on [[nightshade-glaze]]: poison data that "is robust to normal changes one might apply to an image. You can crop it, resample it, compress it, smooth out pixels, or add noise, and the effects of the poison will remain." This is adversarial-example-style robustness explicitly budgeted into the tool, not an emergent property.

## Countermeasure landscape — source-traceable

Each obfuscation approach has a documented or emergent countermeasure. A builder must budget for these.

### vs decoy-traffic: off-the-shelf ML classifiers

Peddinti & Saxena 2014 (see Weaknesses). Key generalisable finding: the decoy *source* (RSS seed, bot-service vendor) is fingerprintable at the population level; the real-user *tail vocabulary* is linkable. A builder must diversify the decoy source *per user* and match the user's own tail distribution — the paper does not claim this is impossible, but notes it was not done by TMN.

### vs fingerprint rotation: cross-attribute inconsistency detection

Venugopalan et al. 2024 — "FP-Inconsistent" (arXiv 2406.07647, captured as `05-10-fp-inconsistent.md`). Core claim: "it is challenging to tell a complex lie while keeping the story always straight… a browser fingerprint is a high dimensional feature set with numerous — often subtle — correlations between attributes that are difficult to anticipate and account for when altering fingerprints" (Conclusion).

Dataset: 507,080 requests from 20 purchased bot services, Sept–Nov 2023. Findings:

- DataDome and BotD (two black-box anti-bot services) detected 55.44% and 47.07% of bot requests respectively as a baseline.
- FP-Inconsistent, applied on top, "reduce[s] the evasion rate of evasive bots by 44.95%–48.11% while maintaining a true negative rate of 96.84% on traffic from real users" (§5).
- Specific inconsistency signals documented:
  - "9 out of the top 10 screen resolutions that have the highest probability of evading DataDome among requests claiming to use iPhones do not exist in the real world" (§6.1).
  - "83 unique screen resolutions from iPhones" in bot traffic versus 12 in reality (§6.1).
  - On BotD: "100% of requests detected by BotD did not support any plugins" while "the presence of any PDF plugin nearly guarantees evasion" (§6.2) — indicating the detector was keying on plugin absence and the bots knew.
  - UTC-offset vs IP-geolocation mismatch: a bot service advertising European traffic had "only 56% of requests mapped to UTC offsets in Europe" by the browser timezone API versus "99.83% of requests to originate from Europe" when inferring from IP (§6.3).

Implication for obfuscators: per-attribute spoofing is insufficient. Any rotation strategy must model joint distributions of real device configurations — which is a harder engineering problem than attribute-by-attribute rotation.

### vs collective action: differential privacy, inverted

Solanki et al. 2025 is the surprise result here. Differential privacy has been framed as a user-side defence, but their Theorem 2 shows **DP can be used by firms to blunt consumer collective action**:

> "The success of the collective is inversely proportional to noise scale σ" (§3).

And:

> "As the privacy loss decreases (corresponding to higher privacy), the critical mass required for the success increases... when a firm deploys a model that prioritizes privacy at the expense of accuracy, it negatively raises the threshold for effective collective action" (§4.3).

Their strategic interpretation: "firms may also strategically adopt such privacy-preserving techniques not only to protect individual data but also to weaken the influence of groups acting on their learning algorithm" (§6.5).

This reverses the standard political reading of DP. A pricing operator that publicly trains with strong DP guarantees is protected from individual re-identification *and* from coordinated consumer counter-action — even though the public positioning is "we protect your privacy."

The paper also documents the opposite-direction finding (§4.4, Table 1): ACA improves empirical privacy against membership-inference attacks — on CIFAR-10, a 1%-collective reduces LiRA attack AuC from 81.78% to ~50.23%. ACA and DP are thus not straightforward substitutes: each buys different things, in ways firms and collectives will read differently.

### vs profile injection: detection methods

Wang et al. 2024 explicitly scope their survey to attacks, not defences (§1: "we focus on the attack strategies"). What they do note in passing:

- Heuristic attacks "lacked adaptability, rendering them detectable to defense measures once their patterns are deciphered" (§2.2 contextual). Modern attacks therefore use adversarial-ML methods designed to evade detection.
- GAN-based profile generators (RecUP, GSA-GANs) "employ state-of-the-art malicious user detection methods to evaluate whether generated fake users can evade detection mechanisms" — the attack literature has already internalised the detector-as-training-signal pattern.

The survey identifies five explicit future-direction gaps (§6), one of which is direct evidence the arms race is open:

> "The latest trajectory of research on the PAR [poisoning attacks against recommenders] is **intrinsically aligned with the iterative advancements in recommendation techniques**. The evolution from factorization-based... to network-based, and currently to the cutting-edge large language model (LLM)-based recommendations... not only yields more precise recommendation outcomes but also introduces a range of new vulnerabilities" (Introduction).

A builder should assume the defender's detection will co-evolve with the attack's sophistication.

### vs browser-level noise: detection and the "blending in" paradox

Lawall 2024 documents the reverse-threat countermeasure in fingerprinting:

> "Reducing APIs and data sources for fingerprinting can ironically make users more identifiable. Thus, widely adopted browsers and protection mechanisms should be used to stay less conspicuous" (citing Al-Fannah & Mitchell 2020).

A user with CanvasBlocker + NoScript + User-Agent Switcher + a heavily-customised fingerprint-resistance stack becomes *more* uniquely identifiable than a user on default Chrome. The defence-as-signal dynamic is well-known but rarely priced in.

Lawall also documents WebGPU (successor to WebGL) as a countermeasure-to-countermeasures: "allowing for classifications with up to 98% accuracy in 150 milliseconds, a reduction from the 8 seconds WebGL took" (§III).

### vs distribution: platform enforcement

Separately documented on [[adnauseam]] and [[lever-implementation-readout|H2]]. The mechanism that ended AdNauseam's mainstream distribution in January 2017 is a class-level risk for any obfuscation tool. The [[paypal-honey|Honey]] 2024–25 affiliate-commission policy change shows the Chrome Web Store using platform-policy changes (not enforcement actions) to invalidate whole tool categories.

## Legal-risk layer — CFAA post-Van Buren / hiQ

Capture: `09-11-whitecase-hiq-vanburen-cfaa.md` — White & Case 2022 analysis of the Ninth Circuit's April 2022 decision on remand from the Supreme Court in *Van Buren v. United States*.

**The CFAA question.** Does accessing a website in a way the site-owner has forbidden (ToS violation, cease-and-desist) constitute "access without authorization" under 18 U.S.C. §1030(a)(2), which imposes criminal and civil liability? The Ninth Circuit, applying *Van Buren*'s "gates-up-or-down" test, held:

> "It is likely that when a computer network generally permits public access to its data, a user's accessing that publicly available data will not constitute access without authorization under the CFAA" (quoted in capture).

Reasoning: "public websites have 'no gates to lift or lower in the first place' because 'a defining feature of public websites is that... [they] are open to anyone with a web browser' (i.e., they lack systems of authentication). Accordingly, the Court found that the 'without authorization' clause does not apply to public websites" (capture).

**What this means for obfuscation / automation tools.** Accessing publicly-available pricing pages, competitor-price pages, or product-detail pages at scale with automated tools — in violation of site ToS — is **unlikely to constitute a CFAA violation** in the Ninth Circuit under current doctrine. This reduces the federal-criminal risk surface for price-transparency overlays, observatory tools, and decoy-traffic generators that interact with public endpoints.

**What this does NOT protect.** The capture is explicit: the Ninth Circuit "emphasized that its analysis was limited in scope to the CFAA and did not apply to potential claims against web scrapers under other theories, including trespass to chattels, copyright infringement, misappropriation, unjust enrichment, conversion, breach of contract or breach of privacy claims." Each of these remains available to a pricing operator that wants to litigate against a consumer-side tool.

**Open questions the capture flags.**
- The decision is Ninth Circuit, not Supreme Court. Circuit split on CFAA "without authorization" persists.
- Authenticated pages (logged-in views, loyalty-account dashboards, member portals) are a different legal surface — the "gates-up" test does apply, so automation against authenticated views has significantly more CFAA risk.
- The nature, collection-source, and collection-method of the data still matter under non-CFAA theories: "(i) the nature of the data; (ii) where it is being collected from; and (iii) how it is being collected."

For consumer-collective tools aimed at pricing algorithms, the practical read: **public-endpoint automation is federally defensible; authenticated-endpoint automation is a materially higher risk**. This shapes the design space for [[possible-strategic-levers|levers #6, #7, #10, #11]].

## Relationship to other mechanisms

- **Vs [[transparency-tools]]:** transparency tools make the watcher's behaviour visible; obfuscation makes the user's behaviour invisible/unreliable. Complementary strategies on opposite sides of the information asymmetry.
- **Vs [[collective-bargaining-for-data]]:** Porat 2024's individual algorithmic bargaining via strategic cookie/erasure exercise is a **consented-withdrawal** tactic; obfuscation is a **counterfeit-production** tactic. Porat works within existing legal rights; obfuscation generally does not rely on them.
- **Vs [[data-cooperatives]]:** data coops aggregate member data under member control; obfuscation aggregates nothing and governs nothing — it is a per-user client-side tactic.
- **Vs [[adversarial-data-poisoning]]:** the poisoning-attacks-on-RS literature is the formal ML counterpart to consumer-side obfuscation. The same technical machinery (profile injection, adversarial examples, feature-label strategies) that researchers use to attack recommender systems is what a consumer-collective tool would deploy against a pricing model.
- **Vs [[browser-fingerprinting]]:** fingerprinting is the watcher-side technique stack obfuscation must defeat at the session/identity layer. Lever #6 (session-identity rotation) and lever #11 (fingerprint parity network) are attempts to defeat fingerprinting specifically.

## Source

- `raw/research/lever-implementations/01-01-wikipedia-adnauseam.md` — Wikipedia AdNauseam article. Starting reference.
- `raw/research/lever-implementations/02-02-nightshade-primary.md` — Nightshade primary site, UChicago SAND Lab (Ben Zhao et al.). Primary organisational source.
- `raw/research/lever-implementations/03-03-glaze-primary.md` — Glaze "About Us" page. Same research group.
- `raw/research/obfuscation-deep-dive/06-03-peddinti-trackmenot-attack.md` — Peddinti & Saxena, *Web Search Query Privacy: Evaluating Query Obfuscation and Anonymizing Networks*, JCS 2014 (combining PETS 2010 + ASIACCS 2011). Origin: academic, peer-reviewed. Audience: security researchers. Purpose: attack evaluation of TMN and Tor. Trust: high — methodology and numbers fully disclosed.
- `raw/research/obfuscation-deep-dive/07-04-howe-adnauseam-case-study.md` — Howe & Nissenbaum, *Engineering Privacy and Protest: a Case Study of AdNauseam*, IWPE 2017. Origin: tool authors, workshop-paper. Audience: privacy engineers. Purpose: design-lessons self-report with normative framing. Trust: high, but declare-your-interest — the tool authors are reporting on their own tool.
- `raw/research/obfuscation-deep-dive/08-02-yale-privacys-trust-gap.md` — Richards & Hartzog, *Privacy's Trust Gap: A Review* (review of Brunton & Nissenbaum's *Obfuscation*), Yale Law Journal 2015. Origin: law-professor book review. Audience: privacy-law scholars. Purpose: critical appraisal of obfuscation as strategy. Trust: high; balanced, concedes ground.
- `raw/research/obfuscation-deep-dive/01-05-strategic-responses-personalized-pricing.md` — Bó, Chen & Hakimov, *Strategic Responses to Personalized Pricing and Demand for Privacy: An Experiment*, Nov 2024 (arXiv 2304.11415). Origin: academic experimental economics. Audience: economists and policy. Purpose: test whether consumers manipulate when they know pricing is personalized. Trust: high — preregistered experimental design, control treatments reported.
- `raw/research/obfuscation-deep-dive/02-07-crowding-out-noise-aca-dp.md` — Solanki, Bhange, Aïvodji & Creager, *Crowding Out The Noise: Algorithmic Collective Action Under Differential Privacy*, arXiv 2505.05707. Origin: academic ML. Audience: ML / trustworthy-AI community. Purpose: formalise collective action vs DP tradeoff. Trust: high — theoretical bounds plus empirical validation across three datasets.
- `raw/research/obfuscation-deep-dive/03-08-poisoning-recsys-survey.md` — Wang et al., *Poisoning Attacks against Recommender Systems: A Survey*, arXiv 2401.01527. Origin: academic survey. Audience: RS researchers. Purpose: attack-only taxonomy. Trust: high for attack literature; this paper does not cover defences.
- `raw/research/obfuscation-deep-dive/04-09-fingerprinting-tracing-shadows.md` — Lawall, *Fingerprinting and Tracing Shadows*, arXiv 2411.12045. Origin: academic survey. Audience: privacy researchers. Purpose: catalogue fingerprinting techniques + legal context. Trust: high.
- `raw/research/obfuscation-deep-dive/05-10-fp-inconsistent.md` — Venugopalan, Munir, King & Ahmed, *FP-Inconsistent: Measurement and Analysis of Fingerprint Inconsistencies in Evasive Bot Traffic*, arXiv 2406.07647. Origin: academic, defender-side. Audience: anti-bot / security. Purpose: measurement + detection method. Trust: high — novel dataset of purchased bot traffic, disclosed cross-validation.
- `raw/research/obfuscation-deep-dive/09-11-whitecase-hiq-vanburen-cfaa.md` — White & Case LLP, *Web scraping, website terms and the CFAA: hiQ's preliminary injunction affirmed again under Van Buren*, April 2022. Origin: law firm client update. Audience: corporate tech litigation clients. Purpose: doctrinal summary. Trust: high for citation traceability (case citations verbatim); bear in mind it is written for firms defending against scrapers, not scrapers.

## Related

- [[adnauseam]]
- [[nightshade-glaze]]
- [[privacy-badger]]
- [[adversarial-data-poisoning]]
- [[browser-fingerprinting]]
- [[transparency-tools]]
- [[collective-bargaining-for-data]]
- [[data-cooperatives]]
- [[possible-strategic-levers]]
- [[obfuscation-strategic-readout]]
- [[lever-implementation-readout]]
