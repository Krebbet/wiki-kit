# Adversarial Interoperability

Adversarial interoperability is the practice of building software that restores, removes or replaces vendor-controlled device behaviour without vendor permission (jailbreaks, alternative firmware, drop-in OSes). Cory Doctorow (opinion/advocacy, 2026-10-21) argues that DMCA s.1201-style anticircumvention law is the legal enabler of enshittification, that AI-assisted ("vibe-coded") jailbreaks help individuals but cannot create alternative markets, and that the systemic fix is repealing anticircumvention law and legalising reverse engineering. All claims below are the author's; none are independently verified here.

## Source trust

Origin: Cory Doctorow, Pluralistic (ad-free personal blog, CC-BY). Audience: general tech-policy readers. Purpose: advocacy, responding to Jason Koebler's 404 Media article and podcast on "Reverse Engineer Anything". Trust tag: expert opinion, strongly partisan; cites primary events (Sonos, Chamberlain, Deere) by link without independent verification here.

## Argument (as stated by the author)

- **Premise:** computers are universal (Turing-complete), so any vendor anti-feature can in principle be countered by an interoperable patch, distributed at zero marginal cost. That threat should discipline enshittification.
- **Blocker:** DMCA s.1201 makes circumvention and modification without vendor permission a felony (5 years / $500k); the US Trade Representative exported equivalent anticircumvention laws to trading partners. Result: vendors may brick devices, strip features, add ads or tier features via update; owners commit a crime by countering.
- **Examples cited:** Sonos update removing most speaker functionality; Chamberlain blocking third-party garage-door apps (seven ads before opening); smart-TV ads and surveillance; John Deere software-tiered tractors; Apple's ~$100b "app tax"; printer ink.
- **New technical lever:** local LLMs lower the cost of jailbreaks and bespoke OSes (e.g. the open-source `morluto/rea` repo; replacement smart-TV software; revived bricked devices).
- **Limit of individual action:** individual jailbreaks suffice for bricked devices and TV ads, but alternative app stores or a generic-ink sector need legal permission so firms can raise capital, staff, support and sell. Doctorow's thesis: "team sport"; policy first, then code.
- **Audit argument:** jailbreak code must be publishable to be inspected and hardened; criminal liability forces secrecy.
- **Security caveat (acknowledged by author):** vibe-coded replacements can carry vulnerabilities; he holds the defect, not the act of replacement, is the problem.

## Contested points

- Koebler/Cox (404 Media) voice misgivings: security of unvetted code on critical equipment (accepted as legitimate by Doctorow), and the fairness of unlocking functionality vendors sell in paid tiers (Deere). Doctorow rejects the second as "spurious": ownership means no duty to preserve the vendor's revenue model. The manufacturer security/fairness case is documented in [[the-firms-view]].
- Doctorow's claim that individual tooling cannot form markets contrasts with the individual-level countermeasure posture of [[obfuscation]].

## Unreviewed pointer

EFF reportedly ran a parallel piece, "Interoperability vs. Security", the same day. Not captured or reviewed; treat as a lead only.

## Source

- Cory Doctorow, "Adversarial interoperability is a team sport", Pluralistic, 2026-10-21 (opinion/advocacy). Raw capture: `raw/research/weekly-2026-10-26/05-adversarial-interop-team-sport.md`

## Related

- [[keep-android-open]] — sideloading and alternative-store freedom; same legal-freedom-to-install dependency
- [[regulatory-responses]] — adds an anticircumvention front alongside the other legal levers
- [[the-firms-view]] — manufacturer security and fairness arguments against owner modification
- [[obfuscation]] — individual technical countermeasures vs. systemic fix
- [[transparency-tools]] — public audit of consumer-side code
- [[platform-cooperatives]] — capitalised or cooperative organisations needed to productise individual hacks
- [[natural-price]] — local, open-source consumer-side tooling that needs public auditability
- [[possible-strategic-levers]] — lever 30, repeal anticircumvention / legalise reverse engineering
