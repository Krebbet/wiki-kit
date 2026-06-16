# Meta Ray-Bans NameTag Surveillance — Dormant FRT Code and Static-Analysis Rollback

Meta shipped dormant facial recognition technology (FRT) code — internally designated "NameTag" — in the Meta AI companion app for its Ray-Ban smart glasses, covering an installed base of 50M+ devices. EFF's Threat Lab confirmed the code's presence through static analysis (decompiling the app binary) in June 2026. Within 48 hours of public disclosure, Meta removed the code in a quiet June 5 app update. The episode is significant on two levels: (1) as an extraction-mechanism case study — covert biometric infrastructure deployed to consumer hardware without disclosure, planned for launch during a moment of civil-society distraction; and (2) as a counter-tool technique case study — adversarial static analysis of a consumer-app binary as a reproducible method for surfacing dormant extraction capabilities before activation.

## Source

- [Move Fast, Surveil Things](https://www.eff.org/deeplinks/2026/06/move-fast-surveil-things) — EFF Threat Lab disclosure of NameTag code in Meta AI app. Intended audience: general public / policy advocates. Purpose: disclose confirmed presence of FRT code via static analysis; flag BIPA history; contextualize Meta's own internal planning document. Trust tag: org-announcement / primary technical finding (code confirmed via decompile).
- [VICTORY: Meta Strips Facial Recognition Code From Smart Glasses App After Public Outcry](https://www.eff.org/deeplinks/2026/06/victory-meta-strips-facial-recognition-code-smart-glasses-app-after-public-outcry) — EFF follow-up confirming removal and issuing standing call for enforceable privacy law. Intended audience: advocates / legislators. Purpose: document the rollback; warn against treating removal as permanent; push for private right of action. Trust tag: org-announcement.

## Extraction Mechanism

**Faceprint storage format.** The code stores faceprints as arrays of 2,048 numbers uniquely representing facial feature positions — the same mathematical representation class as [[browser-fingerprinting|browser fingerprints]] but applied to biometric identity.

**Activation logic.** When enabled, the code would: (a) convert every face in the glasses' field of view into a 2,048-number vector; (b) compare it against all faceprints in the user's database; (c) surface a "Person recognized" alert. Independent researcher verification: when a face was manually added to the app database via debug-mode commands, the glasses subsequently detected that face on sight.

**Deployment scope.** Code present and active in the app but not yet exposed to consumers at time of disclosure. Target hardware: Meta Ray-Ban smart glasses, 50M+ device installed base — always-on cameras worn in public.

**Intentional timing strategy.** Meta's internal planning document (reported by NYT, Feb 2026) stated the intent to launch "during a dynamic political environment where many civil society groups that we would expect to attack us would have their resources focused on other concerns." This is explicit adversarial framing — plan launch when opposition bandwidth is constrained.

**Prior enforcement history.** Meta paid $650M in 2021 to settle a BIPA class action covering mass facial recognition of photos on Facebook. The settlement led to that feature being shut down. The NameTag code represents a resumed attempt via a different surface (wearable hardware).

## Counter-Tool Technique: Adversarial Static Analysis

**The technique.** EFF Threat Lab decompiled the Meta AI app binary (static analysis — no runtime required, no cooperation from Meta). This surfaces code paths, data structures, and logic that are present but not yet user-visible. The technique is platform-agnostic and requires no privileged access.

**What it found.** FRT code, the "Person recognized" alert trigger, ML models, and the biometric database system — none of it disclosed in the app store listing or privacy policy.

**Causal chain to rollback.** Disclosure → WIRED story → public pressure → Meta executives on defensive → June 5 app update scrubbing "nearly all traces of the FRT system" — all within 48 hours. This is a documented case of pre-activation disclosure forcing rollback before a surveillance capability went live.

**Reproducibility.** Static analysis of consumer app binaries is a mature technique. Any researcher with a decompiler (e.g., jadx, apktool, Ghidra) and knowledge of what to look for can replicate this workflow on any app. The EFF Threat Lab methodology here is not novel in tooling — what it demonstrates is the *institutional practice*: systematic auditing of consumer-facing app binaries as a standing counter-power function, not one-off journalism.

**Limitation.** EFF explicitly notes: quiet code removal ≠ permanent policy change. Meta has not disclosed whether data was collected during internal testing. Meta has not committed to not reintroducing the capability. The rollback was reactive and undisclosed — Meta launched no public statement acknowledging the FRT code's existence.

## Policy / Regulatory Context

- BIPA (Illinois Biometric Information Privacy Act) was the lever that produced the $650M settlement on the prior FRT deployment. It carries a private right of action — individuals can sue without waiting for a regulator.
- CCPA does not carry a private right of action (except for a narrow data-breach provision), which EFF treats as the gap that made the current episode possible: regulators were the only enforcement vector, and no regulator acted before disclosure.
- EFF's stated position: "We need robust, enforceable consumer privacy laws, complete with a private right of action that allows everyday people to sue companies that violate their biometric privacy."
- See [[regulatory-responses]] for BIPA / CCPA comparative enforcement landscape.

## Strategic Significance

Two distinct wiki-level learnings:

1. **Extraction mechanism pattern.** Shipping dormant surveillance infrastructure to consumer hardware — activated later, optionally, without a fresh consent moment — is a documented Meta playbook. The 50M-device installed base means activation could be near-instantaneous at scale. The explicit timing-window strategy shows this is not accidental; it is optimized for minimizing civil society response.

2. **Counter-tool pattern.** Static analysis as pre-activation surveillance disclosure is faster and cheaper than litigation and does not require regulatory action. The 48-hour rollback demonstrates meaningful deterrence effect. The implication for [[transparency-tools]]: sustained binary-audit programs on major consumer apps are a viable institutional counter-power function, particularly for biometric and behavioral surveillance that is easiest to hide in dormant code paths.

## Related

- [[transparency-tools]] — static analysis / binary auditing as the counter-tool technique demonstrated here; this case is the strongest documented example of pre-activation disclosure via decompile
- [[obfuscation]] — adversarial consumer counter-power cluster; dormant-code shipping as extraction obfuscation from the platform side
- [[browser-fingerprinting]] — biometric fingerprinting analog; faceprints as 2,048-number arrays parallel the fingerprint-as-hash structure
- [[surveillance-pricing-retail]] — extraction mechanism context; biometric identification at point-of-sale as an adjacent capability
- [[consumer-facing-dynamic-pricing]] — per-identity pricing enabled by persistent biometric identification
- [[regulatory-responses]] — BIPA private right of action as the enforcement lever; CCPA gap as the policy failure mode
- [[noyb]] — strategic litigation model; BIPA-style enforcement vs. GDPR-style regulatory-complaint models compared
- [[privacy-badger]] — EFF tool context; EFF Threat Lab as institutional home of the static-analysis disclosure
