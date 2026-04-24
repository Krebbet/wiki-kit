# The Markup — Citizen Browser

The Citizen Browser Project is a **crowdsourced algorithmic-audit infrastructure** run by The Markup (US nonprofit investigative newsroom). Launched October 2020. A custom standalone desktop application installed by ~1,000+ paid, demographically diverse panelists that periodically captures their Facebook and YouTube feeds, feeding a statistically-valid dataset The Markup uses to audit what content social-media algorithms amplify and to whom. The operational template closest to what a **continuous [[transparency-tools|personalised-pricing observatory]]** would need (see [[regulatory-responses|design-input #1]]), though Citizen Browser itself targets social-media feeds rather than e-commerce prices.

## Structure

- **Host organisation:** The Markup (US nonprofit investigative newsroom focused on how powerful institutions use technology to reshape society). Co-founders Julia Angwin and Jeff Larson — the same team that pioneered data-journalism-on-algorithms at ProPublica (Facebook discriminatory advertising, COMPAS criminal risk scores). See [[regulatory-responses]] for the broader journalism-as-counter-power framing.
- **Partner:** The New York Times — data analysis and co-reporting. Later extended to Süddeutsche Zeitung for Germany.
- **Platform targets:** initially Facebook and YouTube; methodology developed first for Facebook.
- **Launched:** project page dated October 16, 2020.

## Methodology (per *How We Built a Facebook Inspector*, Jan 2021, Mattu, Yin, Waller, Keegan)

- **Panel recruitment:** nationally representative panel of ~1,000+ paid participants, recruited via a survey research provider. 48 US states represented.
- **Technical architecture:** **custom standalone desktop application** (not a browser extension). Distributed to the panel; panelists connected it to their personal Facebook accounts and the app periodically captured feed data.
- **Demographic data collected from panelists:** gender, race, location, age, political leanings, education level.
- **Privacy pipeline:** raw captured data passes through a **Redactor** that auto-strips potential identifiers. Raw data is never seen by a person and is **automatically deleted after one month**.
- **Security:** third-party security audit of the application, data-processing pipeline, and cloud infrastructure by **Trail of Bits**.
- **Output:** after redaction, The Markup stores links, news articles, and promoted groups/pages in a database for analysis. The Markup publishes underlying datasets and code alongside its investigations per its standard practice.
- **Panel-size reality:** ~95% of approached prospects **failed to complete registration** (requirements were desktop/laptop with Chrome installed and active Facebook use). Panel size fluctuated as panelists dropped out and were replenished.
- **Panel demographics as of Dec 2020:** skewed older and more educated than the US population (reflects desktop-computer usage); under-represented Hispanic/Latino panelists and Trump voters (both known polling challenges cited by The Markup).

## Prior work Citizen Browser built on (per The Markup's methodology piece)

- **Blue Feed, Red Feed** (Wall Street Journal, 2016, Jon Keegan — now at The Markup) — used Facebook's own data for 10M US users over 6 months; compared liberal vs conservative feed simulations.
- **NYU Ad Observatory** — browser-extension project archiving political ads on Facebook and Google; Facebook sent a cease-and-desist letter to NYU in the run-up to the 2020 US election.
- **Nieman Lab** — one-off study surveying 173 people via Amazon Mechanical Turk about their Facebook feeds.
- **Charlie Warzel (NYT opinion)** — observed two strangers' Facebook feeds by credential-sharing for a Boomer-misinformation piece.

Citizen Browser's architectural advance over these is **continuous, large-N, privacy-preserving panel data collection** with published methodology.

## Counter-power mechanism

Citizen Browser is a **crowdsourced audit** / **observatory** — one of three functional sub-categories of [[transparency-tools|transparency tools]] documented in this wiki. The Markup's framing (quote from Editor-in-Chief Julia Angwin, October 2020):

> Social media platforms are the broadcasting networks of the 21st century. They dictate what news the public consumes with black box algorithms designed to maximize profits at the expense of truth and transparency. The Citizen Browser Project is a powerful accountability check on that system that can puncture the filter bubble and point the public toward a more free and democratic discourse.

**Against what:** platform-level algorithmic opacity. Unlike single-user transparency tools (like [[keepa]]), Citizen Browser's output is *aggregate* — "what do Facebook's algorithms do across demographics" rather than "what price am I seeing right now."

**Structural limits** per the Facebook-Inspector methodology piece:
- The platform (Facebook) does not cooperate. The NYU Ad Observatory received a Facebook legal letter; Facebook's prior "Social Science One" research partnership (2018) delivered less than promised per the partnership's own co-chairs. Observatory work exists in an explicitly adversarial relationship to the platforms it audits.
- Dependence on paid panelists — recruiting is hard (95% failure rate), demographics are skewed, and panel decay requires continuous replenishment.
- Privacy safeguards (auto-delete after one month, redaction pipeline, third-party security audit) consume engineering budget that a purely extractive tool would not bear.

## Relevance for pricing-observatory design

Citizen Browser is the closest live template for [[regulatory-responses|design-input #1]] (consumer-side pricing observatory). Transferable architectural choices:

1. **Standalone app, not browser extension.** Avoids platform-extension policy exposure (see the [[paypal-honey|Chrome Web Store policy changes]] that followed the Honey controversy). Harder to install — but more durable once installed.
2. **Paid demographically-representative panel.** Addresses the Hannak 2014 methodology's "300 AMT users" scale limit; supports demographic slicing (which is where personalised pricing lives).
3. **Redactor pipeline + auto-delete.** Makes the privacy story durable in the face of regulator / platform scrutiny and panelist trust concerns.
4. **Third-party security audit.** Trail of Bits-or-equivalent audit is budget that a pricing observatory would need for the same reason.
5. **Published methodology + data + code.** The academic-transparency standard. See the Hannak 2014 equivalent (`personalization.ccs.neu.edu`) on [[transparency-tools]].
6. **Partner-newsroom co-reporting model.** The Markup/NYT partnership amplifies output; a pricing observatory would plausibly work with FTC/CMA/EU Commission plus a reputable beat-reporter outlet (ProPublica equivalent).

Non-transferable: the social-media focus and the specific panel-demographic requirements. Pricing-observatory panel would need e-commerce-purchase frequency as the main recruitment filter. *(editorial / synthesis)*

## Scope and limitations (of this wiki page)

- **Capture depth.** The Citizen Browser project page is a short announcement (~4KB captured); the Facebook-Inspector methodology piece (~43KB) carries most of the load. The full series of Citizen Browser *findings* (individual investigations) is not captured here; future runs should pull specific investigations if relevant to this wiki's domain.
- **Temporal.** The methodology piece is from January 2021. The Markup is still publishing (as of 2026); the project's *current* architecture may have evolved. Citizen Browser extended to Germany (Süddeutsche Zeitung partnership) after the methodology piece was published.

## Source

- `raw/research/price-transparency-tools/05-07-markup-citizen-browser.md`
  - **Origin:** The Markup — Citizen Browser project announcement page, October 16, 2020.
  - **Audience:** press, research community, potential panelists.
  - **Purpose:** announce the project and describe its scope.
  - **Trust:** primary organisational source.
- `raw/research/price-transparency-tools/06-08-markup-facebook-inspector.md`
  - **Origin:** The Markup — *How We Built a Facebook Inspector*, January 5, 2021 (Surya Mattu, Leon Yin, Angie Waller, Jon Keegan).
  - **Audience:** journalists, technologists, academics, and the general public.
  - **Purpose:** detailed methodology piece documenting the Citizen Browser panel recruitment, architecture, redaction pipeline, security audit, and limitations.
  - **Trust:** primary investigative-newsroom methodology publication. The Markup publishes underlying datasets and code. Third-party security audit by Trail of Bits is explicitly cited.

## Related

- [[transparency-tools]]
- [[keepa]]
- [[paypal-honey]]
- [[fakespot]]
- [[open-tenant-screening]]
- [[regulatory-responses]]
- [[surveillance-pricing-retail]]
