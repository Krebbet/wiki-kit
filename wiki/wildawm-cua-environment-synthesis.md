# WildAWM — Computer-Use Agent Environment Synthesis

UNC / Microsoft Research (arXiv:2610.26828). Open-model-only pipeline that synthesises persona-driven personal-computer worlds (GUI + MCP services + local files, persistent multi-day state) and 341 verified long-horizon cross-interface tasks. GRPO on these alone lifts Qwen3.6-35B-A3B by +10.58 and Qwen3.5-4B by +8.21 avg points over 8 OOD benchmarks. Code released (MSR-Orchard/WildAWM).

## Method
- World synthesis: a coding agent (GLM-5.2 in OpenCode) generates personas and day plans, then deterministic replayable programs advancing world state W(c,d-1)→W(c,d); 15 WebHarbor mirror sites, 8 synthesised MCP services, local files. A state is kept only if two replays match; reusable event-skill library (83); similarity-feedback regeneration for persona diversity.
- Cross-interface (XAI) tasks must use GUI, MCP and CLI, with executable checklist verifier, rubric, hint and sub-task decomposition. Six rollouts per task from 18 model-harness pairs (3 open models × OpenCode, Codex, Claude Code, Nanobot, [[openclaw]], Hermes Agent). Five gates: judge consistency (programmatic + LLM + agent judge agree on all rollouts), initial unsatisfaction V(W0,W0)=0, solvability, difficulty (k successes of 3 unhinted; k=3 too easy), counterfactual probe (judge shown opposite verdict must hold — anti-sycophancy). Up to 2 revision rounds.
- Training: SFT warm start (100 trajectories) then GRPO ≤64 steps, G=4; reward min(1, V + 0.1·checklist), −1 on format failure; DAPO-style adaptive rollout multiplier.

## Results
- Corpus: 36 personas, 640 world states, 341 tasks (273 hard); mean synthesis success 21.3% unhinted / 45.6% hinted; acceptance 53%. GPT-6-Astra ~60% pass@1, still fails 27.3% after 8 attempts.
- OOD avg (O2W, WA, QCB, CLE, CUG, OSV, OSWorld-2, ALE): 35B 42.84→53.42 (O2W 80.77 above GPT-5.5's 72.22); 4B 21.83→30.04; every benchmark improves. Frontier avg 64–73, so a large gap remains.
- Gate ablation (4B, SFT data): full 31.86; dropping judge-consistency 22.56, initial-unsatisfaction 24.08, counterfactual probe 27.91. RL ablation: no SFT warm start −5.31 (largest).
- Verifier vs agent-judge majority: 95% agreement, κ=0.90.

## Caveats
- ~8×B200 budget; mean 69.8M input tokens per task generated. Only main body read by the summariser (Fig. 5 behaviour analysis, appendices not). No RL variance reported; some baselines are cited numbers.
- Complementary, not opposed, to [[qwen-agentworld]] (LLM-simulated environments vs real executable code worlds).

## Source
- raw/research/weekly-2026-10-24/04-agent-world-model-wild.md (arXiv:2610.26828)

## Related
- [[qwen-agentworld]] — LLM-simulated agentic environments for RL
- [[terminal-universe]] — verifier-filtered terminal environment synthesis
- [[polar-rl-harness]] — harness-agnostic agentic RL
- [[openclaw]] — one of the rollout harnesses
- [[kimi-k3]] — large-scale agentic RL sandboxes
- [[skill-self-play]] — skill library driving task generation
- [[jev-as-a-judge]] — judge agreement analysis
- [[co-cheating-crossfit]] — agreement-based reward pitfalls
