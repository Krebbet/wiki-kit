# Capture Manifests

Exactly which source URLs were verified and captured for each research job, in the order they were captured.

**Verification standard.** A `HTTP 200` is NOT verification. Two sources in job 6 were discovered, marked
verified, and then failed at capture — both returned 200 while serving HTML instead of the PDF the URL
implied. Confirm the actual `content-type` and a plausible byte size before trusting a URL, and confirm the
captured markdown is a plausible length for a full paper afterwards. Three further sources this session were
fetchable and real but were not what their URL implied (a slide deck, an excerpt, a paper by a different
author) — capture success does not establish that a source is what it claims to be.

**Why this page exists.** `raw/research/` is gitignored — captures do not survive a fresh clone, and they are
large and regenerable. This page is the recipe for regenerating them. Every URL here was verified to return
real full-text content (not a 403, login wall, or abstract page) before capture. Without this page, resuming a
job after a clear would mean re-running source discovery from scratch and probably landing on a different set.

**To regenerate a job's captures**, write its block below to a spec file and run:

```bash
while IFS='|' read -r kind slug url; do
  case "$kind" in
    pdf) CUDA_VISIBLE_DEVICES="" poetry run python -m tools.capture_pdf --src "$url" --out "raw/research/<slug>" --slug "$slug" ;;
    url) poetry run python -m tools.capture_url --url "$url" --out "raw/research/<slug>" --slug "$slug" ;;
    url-js) poetry run python -m tools.capture_url --url "$url" --out "raw/research/<slug>" --slug "$slug" --js ;;
    yt) poetry run python -m tools.fetch_transcript --url "$url" --out "raw/research/<slug>" --slug "$slug" ;;
  esac
done < spec.txt
```

`CUDA_VISIBLE_DEVICES=""` is deliberate: marker runs on CPU here at ~30-60s/paper, which keeps a GPU with
known VRAM degradation out of the loop. Do not remove it without checking `~/bin/gpu_safe_setup.sh` first.

**Slug prefixes carry meaning.** `crit-` marks a source deliberately captured to challenge or falsify the
job's thesis; `fail-` marks a source documenting failure rates rather than successes. Both exist to satisfy
the ideological-balance gate in `/research` — if you regenerate a job and drop those, the job is no longer
balanced.

---

## Job 1 — `foundations-nie`

Foundations — what institutions are and why they exist

```
pdf|north-institutional-change-framework|https://econwpa.ub.uni-muenchen.de/econ-wp/eh/papers/9412/9412001.pdf
pdf|ostrom-nobel-polycentric|https://www.nobelprize.org/uploads/2018/06/ostrom_lecture.pdf
pdf|wallis-north-persistence-change|http://econweb.umd.edu/~wallis/MyPapers/Wallis_Persistence&Change.10.10.26.pdf
pdf|nber-north-transaction-costs|https://www.nber.org/system/files/working_papers/w24585/w24585.pdf
pdf|williamson-nobel-transaction-cost|https://www.nobelprize.org/uploads/2018/06/williamson_lecture.pdf
pdf|wallis-north-persistence-change|https://econweb.umd.edu/~wallis/MyPapers/Wallis_Persistence&Change.10.10.26.pdf
```

## Job 2 — `institutional-evolution`

How institutions evolve over time

```
url|north-nobel-lecture|https://www.nobelprize.org/prizes/economic-sciences/1993/north/lecture/
pdf|arthur-increasing-returns-lockin|http://rochelleterman.com/ir/sites/default/files/arthur%201989.pdf
pdf|pierson-increasing-returns|https://www.almendron.com/tribuna/wp-content/uploads/2017/01/pierson.pdf
pdf|dimaggio-powell-iron-cage|https://ics.uci.edu/~corps/phaseii/DiMaggioPowell-IronCageRevisited-ASR.pdf
pdf|meyer-rowan-institutionalized-organizations|http://www.iot.ntnu.no/innovation/norsi-pims-courses/harrison/Meyer%20&%20Rowan%20(1977).PDF
pdf|streeck-thelen-institutional-change|https://pure.mpg.de/rest/items/item_1232475_4/component/file_3556514/content
pdf|krasner-approaches-to-the-state|http://www.critical-juncture.net/uploads/2/1/9/9/21997192/krasner_approaches_to_the_staet.pdf
```

## Job 3 — `scale-effects`

Large vs small institutions

```
pdf|coase-nature-of-the-firm|http://econdse.org/wp-content/uploads/2014/09/firm-coase.pdf
url|coase-nobel-lecture-institutional-structure|https://www.nobelprize.org/prizes/economic-sciences/1991/coase/lecture/
pdf|niskanen-peculiar-economics-bureaucracy|https://sites.socsci.uci.edu/~jkbrueck/course%20readings/Econ%20272B%20readings/niskanen.pdf
url|parkinson-law-original-essay|http://doc.cat-v.org/economics/parkinsons-law/
pdf|parkinson-law-quantified-empirical|https://arxiv.org/pdf/0808.1684
pdf|rajan-wulf-flattening-firm|https://www.nber.org/system/files/working_papers/w9633/w9633.pdf
pdf|simon-architecture-of-complexity|https://www.cs.brandeis.edu/~cs146a/handouts/papers/simon-complexity.pdf
pdf|garicano-rossi-hansberg-knowledge-hierarchies|https://www.nber.org/system/files/working_papers/w20607/w20607.pdf
```

## Job 4 — `incentives-and-institutional-form`

Incentives and how they form institutions

```
pdf|holmstrom-nobel-lecture|https://www.nobelprize.org/uploads/2018/06/holmstrom-lecture.pdf
pdf|hart-nobel-lecture|https://www.nobelprize.org/uploads/2018/06/hart-lecture.pdf
pdf|holmstrom-milgrom-multitask|https://www.sfu.ca/~allen/HolmstromMilgrom.pdf
pdf|grossman-hart-property-rights|https://dash.harvard.edu/bitstreams/7312037c-527a-6bd4-e053-0100007fdf3b/download
pdf|prendergast-incentives-firms|http://qed.econ.queensu.ca/pub/faculty/ferrall/econ861/papers/prendergast.pdf
pdf|dixit-incentives-public-sector|https://www.edegan.com/pdfs/Dixit%20(2002)%20-%20Incentives%20and%20Organizations%20in%20the%20Public%20Sector.pdf
pdf|benabou-tirole-motivation|https://www.princeton.edu/~rbenabou/papers/IEM.pdf
pdf|frey-crowding-intrinsic-motivation|https://www.bsfrey.ch/wp-content/uploads/2021/08/crowding-effects-on-intrinsic-motivation.pdf
```

## Job 5 — `risk-aversion-in-large-institutions`

Why large institutions are risk averse

```
pdf|hood-blame-game-ch1|http://assets.press.princeton.edu/chapters/s9353.pdf
pdf|kahneman-lovallo-timid-choices|https://bear.warrington.ufl.edu/brenner/mar7588/Papers/kahneman-lovallo-mansci1993.pdf
pdf|holmstrom-career-concerns|https://www.nber.org/system/files/working_papers/w6875/w6875.pdf
pdf|manso-motivating-innovation|https://web.mit.edu/manso/www/mi.pdf
pdf|nicholson-crotty-public-managers-risk-averse|https://journal-bpa.org/index.php/jbpa/article/download/35/34
pdf|hammond-veto-points-bureaucratic-autonomy|https://press.umich.edu/pdf/0472113178-ch4.pdf
pdf|bozeman-theory-of-red-tape|https://selc.wordpress.ncsu.edu/files/2013/03/A-Theory-of-Government-Red-Tape.pdf
pdf|oecd-innovative-capacity-governments|https://www.oecd.org/content/dam/oecd/en/publications/reports/2022/04/innovative-capacity-of-governments_e3de34c4/52389006-en.pdf
```

## Job 6 — `enabling-institutional-change`

Empowering change in institutions

```
url|cox-design-principles-review|https://www.ecologyandsociety.org/vol15/iss4/art38/main.html
pdf|bunse-fritz-public-sector-reforms|https://openknowledge.worldbank.org/server/api/core/bitstreams/359c2b9d-cfc7-56fb-a732-55b3bd21508c/content
pdf|oreilly-tushman-ambidexterity-dynamic-capability|https://www.hbs.edu/ris/Publication%20Files/07-088.pdf
pdf|sabel-zeitlin-experimentalist-governance|https://charlessabel.com/papers/Sabel%20and%20Zeitlin%20handbook%20chapter%20final%20(with%20abstract).pdf
pdf|finan-olken-pande-personnel-economics|https://www.nber.org/system/files/working_papers/w21825/w21825.pdf
pdf|true-jones-baumgartner-punctuated-equilibrium|https://fbaum.unc.edu/teaching/articles/True_Jones_Baumgartner_2006_chapter.pdf
pdf|fail-nao-reorganising-government|https://www.nao.org.uk/wp-content/uploads/2010/03/0910452.pdf
pdf|fail-andrews-pritchett-woolcock-pdia|https://www.cgdev.org/sites/default/files/1426292_file_Andrews_Pritchett_Woolcock_traps_FINAL_0.pdf
```

## Job 7 — `institutional-stagnation`

Why institutions become stagnant

```
pdf|merton-bureaucratic-personality|http://www.csun.edu/~snk1966/Robert%20K%20Merton%20-%20Bureaucratic%20Structure%20and%20Personality.pdf
pdf|stigler-theory-economic-regulation|https://bfi.uchicago.edu/wp-content/uploads/2023/02/3003160.pdf
pdf|fukuyama-america-in-decay|https://gwern.net/doc/history/2014-fukuyama.pdf
pdf|selznick-foundations-theory-organization|http://www.iot.ntnu.no/innovation/norsi-pims-courses/harrison/Selznick%20(1948).PDF
pdf|miller-dudley-regulatory-accretion|http://www.administrativelawreview.org/wp-content/uploads/2016/03/MillerDudley_PublishedVersion-1.pdf
pdf|schleicher-bagley-state-capacity-crisis|https://bclawreview.bc.edu/articles/3226/files/6908e05e769a8.pdf
pdf|crit-carpenter-moss-preventing-capture-intro|https://tobinproject.org/sites/default/files/assets/Introduction%20from%20Preventing%20Regulatory%20Capture.pdf
pdf|crit-novak-revisionist-capture|https://tobinproject.org/sites/default/files/assets/Novak%20Revisionist%20History%20of%20Regulatory%20Capture%20(1.13).pdf
pdf|crit-heckelman-explaining-the-rain|https://heckeljc.sites.wfu.edu/papers/published/SEJ2007.pdf
```

---

## Job 13 — `organisational-ecology`

The demography of organisations — liability of newness, structural inertia, age-dependent mortality

```
pdf|hannan-freeman-population-ecology|http://www.iot.ntnu.no/innovation/norsi-pims-courses/harrison/Hannan%20&%20Freeman%20(1977).PDF
pdf|hannan-freeman-structural-inertia|http://www.iot.ntnu.no/innovation/norsi-pims-courses/harrison/Hannan%20&%20Freeman%20(1984).PDF
pdf|yang-aldrich-liability-newness-revisited|https://faculty.wharton.upenn.edu/wp-content/uploads/2017/10/The-Liability-of-Newness.pdf
pdf|coad-firm-age-performance|https://vbn.aau.dk/ws/files/310573536/JEE_Firm_Age.pdf
pdf|crit-searing-zombies-nonprofit-demise|https://jpna.org/index.php/jpna/article/download/357/356
```

Two further candidates were sought and failed on retry, and are not in this list: **Thornhill & Amit**
(`repository.upenn.edu`, `application/json` redirect pointer — see the known-bad-sources table below, this is
the age-stratified failure dataset this job most wanted) and **Le Mens** (Wayback host, persistent `503`, the
disconfirming/obsolescence source). Neither is captured. See `STATE.md`'s manual-acquisition note for Thornhill
& Amit.

---

## Known-bad sources (do not retry without a fix)

| Job | Source | Problem |
|---|---|---|
| 1 | Wallis, *Persistence and Change in Institutions* — `econweb.umd.edu` | `SSL: CERTIFICATE_VERIFY_FAILED`; the host's cert chain is incomplete on both http and https. Needs a manual browser download into `raw/research/foundations-nie/`, then `capture_pdf --src <local-path>`. |
| 6 | Cox et al., design-principles review — `ecologyandsociety.org/.../ES-2010-3704.pdf` | The `.pdf` path now serves `text/html`. The article page is a legacy `<frameset>`; the full text lives at `.../art38/main.html`, which is what the manifest now points at. |
| 6 | O'Reilly & Tushman — `gsbapps.stanford.edu/researchpapers/library/RP2130.pdf` | Returns a 6KB HTML page, not the PDF. Replaced with the HBS-hosted 2007 working paper (`hbs.edu/ris/Publication Files/07-088.pdf`), same authors and topic. |
| 13 | Thornhill & Amit, *Learning from Failure* — `repository.upenn.edu` | DSpace returns `application/json` on both the `/bitstreams/.../download` and `/server/api/core/bitstreams/.../content` paths — a redirect pointer, never the file. **This was the batch's age-stratified failure dataset** (young-firm failures traced to management/financing, old-firm failures to strategic/leadership factors) and is the most concrete empirical age evidence the project located. Its loss leaves organisational ecology with theory (Hannan & Freeman), one confirming study that separates resources-at-birth from later (Yang & Aldrich), and two critiques — but no hazard-rate dataset. Worth acquiring manually; the *Organization Science* 2003 version is titled "Learning About Failure: Bankruptcy, Firm Age, and the Resource-Based View". |
| 11 | Mills, *The Power Elite* — `archive.org` | Persistent HTTP 500 on the item across retries. Not a bot wall — the archive item itself errors. Elite theory in job 11 therefore rests on Michels (captured) without Mills. |
| 8 | Weber, "Bureaucracy" (*Economy and Society* ch. VIII) — `burawoy.berkeley.edu` | **Scanned image PDF with no text layer.** marker hung on it for **2h08m** doing OCR, blocking seven other sources in the job; pymupdf returned a 64-word stub, which was deleted rather than ingested. This is the "capture succeeded but is not the source" failure mode in its purest form — a 64-word file would have passed any size check a human skimmed. No alternative could be sought: the session's WebSearch budget was exhausted. **Job 8 was ingested without Weber's own text.** The Weberian camp is represented empirically by Evans & Rauch and Rauch, but the canonical statement of rational-legal bureaucracy is absent and any page describing it must say so. Worth acquiring manually — a digital-native copy of the chapter would close it. |
| 15 | FD&C Act — `govinfo.gov` Title 21 USC | Captured **PARTIAL: first 260 of 1030 pages**, deliberately. FDA publishes no standalone FD&C Act PDF — only a table-of-contents page linking out — so the consolidated Title 21 US Code is the sole verifiable full text. The FD&C Act is Chapter 9, roughly pp.30-717; a full marker run on CPU would take hours. The slice covers the definitions and core authorities, which is what the mandate/authority axes need. **Do not cite it for any provision beyond p.260**, and do not describe the wiki as holding the FD&C Act in full. |
| 15 | GAO on FDA user fees | `gao.gov` returns 403 via Akamai on every path (products, assets, search, and GAO's own API) — an infrastructure block, not a missing document. Served from a Wayback memento instead, but the only one obtainable is **GAO-02-958 from 2002**. Treat as a historical baseline, never as current-state evidence. If gao.gov is reachable from another network, a current report would materially improve this. |
| 4 | Bénabou & Tirole, *Intrinsic and Extrinsic Motivation* — `princeton.edu/~rbenabou/papers/IEM.pdf` | Not the RES 2003 article — a **29-page slide deck** presenting it. Capture is faithful; the source is slides. Usable as a statement of the authors' model and position, never as the paper. Motivation-crowding ground is covered in full text by `frey-crowding-intrinsic-motivation`. |
| 3 | Parkinson 1955 essay — `doc.cat-v.org` | The page is an **excerpt** (561 words) that stops before the Admiralty/Colonial Office headcount data. Verified against raw HTML: the capture is faithful, the page is partial. `--js` returns the same. Do not attribute Parkinson's own empirics to it. **Further:** the modern quantitative test (`parkinson-law-quantified-empirical`) does NOT independently replace them — its two historical staff series are Parkinson's own 1957 figures restated at second hand, n=2, with workload proxies that plausibly move opposite to administrative work. Its cross-country cabinet-size result is its own contribution; the growth series are not. |

## Canonical sources with no open copy

Recorded so later sessions do not re-spend effort hunting them. Each would be worth capturing if a legitimate
full text ever becomes reachable, or if the user can supply a PDF manually.

- Mancur Olson, *The Rise and Decline of Nations* (1982) — in-copyright; only reviews and symposia. Job 7 covers
  the sclerosis thesis via Heckelman's 25-year empirical review instead.
- Daniel Carpenter, *The Forging of Bureaucratic Autonomy* — the best source on administrative discretion as a
  precondition for renewal. Job 6 has no substitute for it.
- Williamson, *Markets and Hierarchies* (1975) and "Hierarchical Control and Optimum Firm Size" (1967).
- Niskanen, *Bureaucracy and Representative Government* (1971) — job 3 uses his 1968 AER paper instead.
- Selznick, *TVA and the Grass Roots* (1949) — job 7 uses his 1948 ASR article instead.
- Mahoney & Thelen, "A Theory of Gradual Institutional Change" (2010) — job 2 covers layering/drift/conversion
  via Streeck & Thelen instead.
- Courty & Marschke on gaming responses to performance incentives — job 4 covers gaming via Prendergast and
  Bénabou-Tirole instead.
- Bevan & Hood, "What's Measured Is What Matters" (2006).

## Source

- Compiled during the 2026-08-19 research run. Each URL verified by a discovery subagent before capture.

## Related

- [[research-agenda]] — the job queue these manifests belong to; its blocked log records live failures.
- [[index]] — the content catalog.
