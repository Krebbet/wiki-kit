# Master Notes

Running log of what works and what doesn't — both for this specific wiki's operation and for the collaboration generally. Append-only scratchpad for observations that might deserve to become CLAUDE.md guidance, command updates, or kit-level improvements.

During normal operation, Claude appends observations here with `Status: open`. At `/harvest` time (or whenever you review), entries are triaged: some become kit-level code or doc changes promoted to main via `/harvest`; some become this wiki's project CLAUDE.md updates; some are rejected; some stay open for more signal.

## Format

Append entries using this structure:

```
### YYYY-MM-DD — short title
**Scope:** project | interaction | kit | both
**Observation:** what was noticed
**Implication:** what this suggests for CLAUDE.md, a command, a tool, or process
**Status:** open | proposed | applied | rejected
```

**Scope guide:**
- `project` — specific to this wiki (lands in this wiki's `wiki/CLAUDE.md` or DOMAIN-SLOT content).
- `kit` — generic to wiki-kit itself (gets promoted to main via `/harvest`; every other wiki benefits).
- `interaction` — about how the user and assistant work together (may become memory or user-level CLAUDE.md).
- `both` — overlaps more than one scope.

## Notes

### 2026-04-19 — kickoff
**Scope:** interaction
**Observation:** User established the master_notes workflow itself: track project + interaction feedback, periodically promote learnings to project CLAUDE.md (changes OK, inform if significant) and master CLAUDE.md (never edit without consulting, but don't be shy about proposing).
**Implication:** This file is the substrate for that loop. Saved to memory so the workflow persists across sessions; consider proposing it for master CLAUDE.md once the pattern proves itself here.
**Status:** applied (memory saved, file created)

### 2026-04-19 — bootstrap interview shortcut worked well
**Scope:** project
**Observation:** User wrote bootstrap intent in `boot_stap_instructions.md` (typo: missing 'r') instead of answering the seven interview questions one at a time. I synthesized all seven answers from that file and presented a single proposal. User approved with "looks great. approved" — zero revision rounds needed.
**Implication:** `/bootstrap` could explicitly support an "instructions file" mode: if `boot_strap_instructions.md` (or some canonical name) exists in the repo root, skip the seven serial questions and synthesize from that file. Faster for users who prefer writing thoughts in one go vs. interactive Q&A.
**Status:** applied upstream — main's `90e7420 feat(bootstrap): accept boot_strap_instructions.md as fast-path input` ships this.

### 2026-04-19 — marker GPU assumption
**Scope:** project
**Observation:** First `/research` run crashed because marker tried CUDA on a saturated GPU. Recovered with `TORCH_DEVICE=cpu`, but 5–10× slower per paper. Logged in FEEDBACK.md.
**Implication:** capture_pdf.py needs either auto-fallback or a documented env var. The bootstrap source-type-notes slot for ArXiv should also acknowledge this. Project-level CLAUDE.md change candidate: add a "Capture environment" section noting the GPU caveat.
**Status:** partially addressed upstream — main's `11b2ecb fix(capture_pdf): one-line hint on CUDA OOM instead of stacktrace` covers the surface-level UX; auto-fallback and documentation still open.

### 2026-04-19 — reboot mid-research-run
**Scope:** interaction
**Observation:** User needed to reboot the machine while a long research run was in flight (1 background bash queue + 8 parallel research subagents on CPU). All in-flight processes will die. Wrote `STATE.md` capturing what's on disk, what's missing, and a concrete continuation plan; committed everything before reboot.
**Implication:** Long-running multi-agent workflows should leave a checkpoint file *as a matter of routine*, not just when a reboot is imminent. Anything that takes >30 min on CPU is worth a checkpoint snapshot every ~15 min so resume is trivial. Candidate convention: `STATE.md` at repo root, written by long-running orchestrator after each major phase.
**Status:** open — propose for project CLAUDE.md once we see how resume goes

### 2026-04-20 — fidelity audit should be a wiki-kit primitive
**Scope:** both (project + interaction)
**Observation:** Caught a 33% image-loss bug in capture_pdf only because the user explicitly asked me to "check that you are capturing the raw materials with fidelity." Without that prompt, synthesis would have proceeded against silently-corrupted captures. The fix to capture_pdf is in (`tools/capture_pdf.py` on `single-shot-training-wiki`), but the deeper issue is that the kit has no automated "did the capture actually work end-to-end?" check.
**Implication:** Two CLAUDE.md candidates:
1. **Project CLAUDE.md (this wiki):** add a "Post-capture verification" step to the wiki assistant's session protocol — after any `/research` or `/ingest`, run a fidelity check before declaring success.
2. **Master CLAUDE.md:** add a general principle — "When orchestrating data pipelines that produce large numbers of derived files, verify a sample for end-to-end correctness (not just exit code = 0) before downstream work." This applies far beyond wiki-kit.
Also: build `tools/audit_captures.py` and wire it into `/lint`. See FEEDBACK.md for the spec.
**Status:** tool + lint wiring applied upstream (`tools/audit_captures.py` and `/lint` / `/research` hooks are on main); Project and Master CLAUDE.md language still open.
