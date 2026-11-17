# Mozilla Fingerprinting-in-the-Wild Measurement and Firefox 143 Mitigations (Ritter et al. 2026)

Ritter et al. (Mozilla with UC San Diego and Toronto authors; ACM CCS 2026, extended version) measure browser-fingerprint uniqueness across roughly 25M Firefox release users via telemetry, scored against simulated commercial fingerprinters (Fingerprint Pro, Signifyd, Akamai) built from reverse-engineered scripts. Uniqueness is concentrated in a few high-impact characteristics and their combinations. Data-driven protections shipped in Firefox 143 cut uniquely identifiable users from about 75% to 46%.

## Key findings

- **Baseline uniqueness (OS-weighted).** Fingerprint Pro 75.7%, Signifyd 60.9%, Akamai 18.2%. Cookie defences (Total Cookie Protection, ITP) pushed trackers toward stateless fingerprinting.
- **Concentration.** Few characteristics drive uniqueness. Of 64 OS x fingerprinter x technique scenarios, only 6 cut uniqueness by more than 15% relative: Software Canvas accounts for 3, available screen resolution for 2, timezone for 1.
- **Mitigation effect.** Phase 2-3 mitigations take Fingerprint Pro from ~75% to ~44% and Signifyd from 60.9% to 35.4%. Phase 4 targets about 10 further points. Per-API levers: entropy reduction, standardisation, randomisation (software canvas, available screen resolution, timezone).
- **Methodology.** Evaluates uniqueness together with cohort structure (Simpson Index, cohort size), not just the fraction of unique users. Randomisation and standardisation are treated as complementary.
- **Cross-browser comparison (sec. 6.4).** Chrome abandoned its Privacy Budget; Safari adds noise to canvas/WebGL/Audio; Brave "farbles" (randomises); Tor Browser and Mullvad uniformise; Phoenix and LibreWolf carry per-site overrides.
- **Release.** Analysis code and aggregate datasets plus fingerprinter reverse-engineering results at github.com/tomrittervg/fingerprinting_paper_artifacts (the paper text points to an anonymous.4open.science mirror, `fingerprint-mitigation`). Raw telemetry is not released.

## Takeaways

- **Population-scale numbers.** Supplies hard baselines where the wiki otherwise rests on survey figures (Lawall 2024); supports the claim that fingerprinting defeats naive identity-rotation obfuscation ([[obfuscation]]).
- **Design input for audit and parity tooling.** Cohort-size and Simpson-Index metrics, plus the per-characteristic impact ranking, are usable for evaluating any "fingerprint parity" or clean-session auditing tool and for choosing which signals matter most for blending in *(editorial)*.
- **Tension with "uniformity beats randomisation".** Uniqueness being concentrated means cheap targeted entropy reduction goes far; the paper still finds randomisation and standardisation complementary *(editorial)*.
- **Not sufficient alone.** 46% residual uniqueness argues against treating vendor browser hardening as a complete defence, though it is a free mainstream floor *(editorial)*.

## Limits

- Firefox-population bias (not representative of Chrome/Safari users).
- "Fingerprinters" are simulations from reverse-engineered client scripts, not the vendors' server-side models; real vendors may use signals or models not captured.
- Capture is a PDF; some tables may be garbled.

## Source

- `raw/research/weekly-2026-11-16/01-mozilla-fingerprinting-in-the-wild.md` — Ritter et al., *Large-Scale Measurement and Real-World Mitigation of Web Browser Fingerprinting in the Wild* (extended version, 13 Nov 2026). Origin: academic/industry, Mozilla engineers with UCSD and Toronto authors, peer-reviewed at ACM CCS 2026. Audience: browser vendors, standards authors, privacy researchers. Purpose: identify which characteristics drive fingerprintability and prioritise mitigations. Trust: high on methodology (real population-scale telemetry); medium on vendor fidelity (simulated fingerprinters). Capture: https://fingerprinting.study/fingerprinting-in-the-wild-extended.pdf (PDF, captured 2026-11-16).

## Related

- [[browser-fingerprinting]]
- [[fingerprinting-sdk-ecosystem]]
- [[obfuscation]]
- [[obfuscation-strategic-readout]]
- [[possible-strategic-levers]]
- [[privacy-badger]]
- [[adnauseam]]
- [[transparency-tools]]
- [[http2-website-fingerprinting-defences]]
