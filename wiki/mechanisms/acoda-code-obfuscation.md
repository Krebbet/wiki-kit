# Acoda: Adversarial Code Obfuscation Against LLM Analysis

Acoda (arXiv 2606.11755, June 2026) is a genetic-algorithm framework that applies semantics-preserving code transformations to make source code resistant to LLM-based analysis, achieving up to 70% attack success rate (ASR) against 7 frontier models (GPT-4o, DeepSeek, Qwen, Llama, Gemma) with strong cross-model transferability. The primary application is protecting proprietary software intellectual property from LLM-powered reverse engineering.

**Wiki scope note.** Acoda addresses developer-IP protection, not consumer-side pricing or tracking power. It is captured here for the methodological transfer value: the genetic-algorithm optimisation loop over semantics-preserving transforms is a pattern directly applicable to consumer-side adversarial obfuscation design.

## Mechanism

Two LLM vulnerabilities are exploited as defensive primitives:

1. **Safety alignment.** LLM safety tuning can be triggered by obfuscated code patterns to refuse or degrade code-analysis responses.
2. **Tokenisation sensitivity.** Identifier renaming, control-flow restructuring, and string encoding alter how source code tokenises, disrupting semantic embedding without changing runtime behaviour.

The genetic algorithm optimises a sequence of 8 obfuscation operators (variable renaming, loop restructuring, dead-code insertion, etc.) to maximise ASR while preserving functional correctness. The multi-objective fitness function balances attack success against semantic preservation.

**ASR ceiling.** 70% is the reported upper bound under non-adaptive evaluation — the adversary LLMs are not given counter-obfuscation feedback. Against an adaptive detector (one specifically tuned to detect Acoda-style transforms), ASR would decrease. See [[browser-fingerprinting]] for the analogous result in web-tracking obfuscation: naive per-attribute rotation achieves ~3% TNR against an adaptive classifier.

## Transfer value for consumer-side obfuscation

The Acoda framework generalises to any setting where:
- An adversary uses a neural model to classify or analyse structured input.
- The defender can apply semantics-preserving transforms to that input.
- A fitness signal (ASR proxy) is available to guide optimisation.

Consumer-side applications: optimising noise-injection or feature-manipulation payloads against pricing classifiers, adversarially restructuring browsing patterns to defeat fingerprinting detectors, adapting DSAR request language to exploit LLM-based DSAR-routing classifiers.

## Source

- `raw/research/weekly-2026-06-22/02-acoda-obfuscation.md`
  - **Origin:** Academic preprint (arXiv 2606.11755, June 2026). CS/SE security group.
  - **Audience:** SE security researchers and practitioners.
  - **Purpose:** Propose adversarial code obfuscation as a counter to LLM-based IP extraction.
  - **Trust:** Preprint, no peer review yet; evaluation is non-adaptive (adversary not tuned against Acoda). Moderate trust on ASR claim; pattern validity is robust.

## Related

- [[obfuscation]] — consumer-side obfuscation mechanisms; Acoda is a code-domain sibling
- [[adversarial-data-poisoning]] — same genetic-algorithm / adversarial-sample paradigm at training time
- [[adversarial-prompt-injection-defense]] — sibling technique exploiting LLM safety alignment as a defensive primitive
- [[browser-fingerprinting]] — adaptive adversary result (97% TNR) that bounds Acoda-style non-adaptive ASR claims
