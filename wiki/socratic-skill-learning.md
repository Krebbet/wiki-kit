# Socratic Skill Learning (SSL)

Nanjing University / Alibaba (arXiv:2610.17860). A stronger Educator model coaches a Student *during* practice while the Student alone operates the environment and authors the Agent Skill (SKILL.md package; no weight updates). Interleaved guidance beats expert authoring, post-hoc teaching and trajectory/contrastive distillation on held-out transfer; ships SkillTransferBench (35 task families, 408 cases, 6 domains). Code and trajectories released (NJU-LINK/Socratic-Skill-Learning).

## Method
- Student = target solver and sole Skill author; Educator reads the Student's recent work and live package, may explain/challenge/diagnose/stay silent; the Student may reject advice. 3 rounds per family, each ending with a fresh-solver test of the frozen package on the anchor task.
- Fixed-Window SSL: Educator reviews every g=10 tool calls. Issue-Guided SSL: lessons become persistent "learning issues" (focus + observable acceptance criterion) in a Learning-Issue Tree; Student commits revisions declaring evidence and issue; review triggers only when an issue opens/changes/reopens.
- Baselines: No Skill, Expert Authoring, Post-hoc Teaching, adapted Trace2Skill and SKILL-KD. Harness: Pi 0.81.1, Docker.

## Results
- Table 1 (Qwen3.7-Plus Student, Qwen3.7-Max Educator, family-macro Avg@3, main cohort 22 families / 155 cases): No Skill 72.3; Expert Authoring 72.8 (+0.5); Post-hoc 74.8; Trace2Skill 76.1; SKILL-KD 75.1; Fixed-Window 80.1 (+7.8); Issue-Guided 80.5 (+8.2). Full-pass 32.5% → 50.8%. Fixed-Window beats Trace2Skill by 3.99 pp (95% CI [1.45, 6.49]).
- Lite subset across Qwen / DeepSeek / Kimi: SSL +2.5 to +8.2 pp; Post-hoc trails Expert Authoring in every pair and is −0.7 on Qwen.
- Issue-Guided vs Fixed-Window: equal utility with 61.7% fewer Educator tokens, 16.9% fewer total acquisition tokens, 47.8% fewer reviews. Lesson-delivering reviews fall from 73.0% (round 1) to 16.1% (round 3); silent reviews are 85.8% of final-round review tokens.

## Caveats
- Absolute gains modest (~8 pp); DeepSeek/Kimi are single runs on 10 families; Educators are stronger same-vendor models; Educator APIs limit exact reproduction. Summariser read ~450/793 source lines (later appendices unreviewed). A strong-model-authored skill barely helps a weaker solver (+0.5 pp) — a counterweight to optimistic skill-authoring framing in [[skillopt]]-style pages.

## Source
- raw/research/weekly-2026-10-24/05-socratic-skill-learning.md (arXiv:2610.17860)

## Related
- [[skillopt]] — separate-optimizer skill editing
- [[disco-arex-skill]] — repo/paper→skill distillation
- [[skill-self-play]] — RL skill-library co-evolution
- [[memoharness]] — experience-bank / harness optimisation
- [[self-evolving-agent-harness]] — fresh-validation admission bounds
- [[rl-teachers]] — teacher as comprehension maximiser
- [[gepa-reflective-prompt-evolution]] — reflective text-artifact optimisation
- [[coevo-rsi]] — sibling 2026-10 self-evolving-agent paper
