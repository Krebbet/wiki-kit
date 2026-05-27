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

<!-- Entries appended during operation go below. -->

### 2026-04-30 — capture_pdf should auto-detect GPU contention and fall back to CPU
**Scope:** kit
**Observation:** `tools/capture_pdf.py --engine marker` defaults to whatever device PyTorch picks (typically CUDA if available). On a host with another GPU job already running, the marker engine either contends with that job or OOMs. Today the only handling is a post-hoc CUDA-OOM error message instructing the user to retry with `--engine pymupdf`. The user's stated preference is that **marker should remain the default for quality, but capture_pdf should pre-flight check GPU availability/free-VRAM and silently fall back to CPU (`CUDA_VISIBLE_DEVICES=""`) when the GPU is busy** — getting the better extraction at the cost of more wall-clock time, instead of getting either a worse extraction (pymupdf) or a crash (OOM).
**Implication:** Modify `tools/capture_pdf.py` to (a) query `nvidia-smi --query-gpu=memory.free,utilization.gpu --format=csv,noheader,nounits` before invoking marker, (b) if free VRAM is below a threshold (e.g. < 4 GB) or another high-utilization process is detected, set `CUDA_VISIBLE_DEVICES=""` in `os.environ` before importing marker/torch, and log "GPU busy — running marker on CPU (slower but better than pymupdf fallback)". Add an `--device {auto,cpu,cuda}` CLI flag with `auto` as the default that runs the pre-flight; explicit `cpu`/`cuda` overrides the heuristic. Update `.claude/commands/research.md` and `ingest.md` source-handling notes to mention auto GPU-contention handling. (Note: the existing `_is_cuda_oom` post-hoc message stays — it's still a useful safety net for late-firing OOMs that slip past the pre-flight check.)
**Status:** open

### 2026-04-30 — ingest subagents drift from strict summary schema; orchestrator should normalise before validation
**Scope:** kit
**Observation:** During the second `/research+ingest` run on selective-replacement-and-training (15 papers), 13 of 15 sonnet ingest subagents wrote summary files that failed `tools.ingest_plan.parse_summary` validation despite each being given the strict schema in their prompt. Failure modes:
- Frontmatter omitted entirely (7/15) — subagents wrote a Markdown header block (`**Source:**`, `**Paper:**`, `**Venue:**`) instead of YAML frontmatter.
- Frontmatter present but missing `schema_version: 1` (6/15) — subagents added their own custom keys (`source_file`, `source_url`, `goal_tags`) and dropped the canonical schema-version marker.
- Section headers renamed (multiple) — `## One-paragraph summary`, `## Summary`, `## Core Method`, `## Goal Relevance`, `## Related Wiki Pages` all appeared instead of the canonical `## One-line`, `## Method core`, `## Goal relevance`, `## Cross-ref candidates`. The validator does case-sensitive exact-match on the four required section headers.
The first run (12 papers, block-training-quantization) had zero schema failures because the prompt template was literal-pasted from `ingest.md` step 3. The second run used a more compact, paraphrased prompt — which is what triggered the drift.
**Implication:** Two complementary fixes:
1. **Prompt level** — `ingest.md` should warn that subagents drift on schema when prompts are paraphrased; the orchestrator should always paste the literal template from the command file rather than rewording it. Could be a one-line warning at the top of the subagent-prompt section.
2. **Tool level** — add `tools/ingest_plan.normalise_summary(path)` that performs the same fixups the orchestrator did in this run: strip non-canonical frontmatter, inject `schema_version: 1`, rename common section-header variants (`Summary` / `One-paragraph summary` → `One-line`, `Core Method` → `Method core`, `Related Wiki Pages` / `Domain context` / `Cross-references` → `Cross-ref candidates`, etc.), and append empty stubs for any required section that's still missing. The orchestrator should call `normalise_summary` *before* `parse_summary` in the validation step (step 4 of `ingest.md`), so subagent drift becomes self-healing rather than blocking.
The fixer used in this run (in-line Python, ~30 lines) is a reasonable starting point. Promote it into `tools/ingest_plan.py`.
**Status:** open


### 2026-05-26 — poetry install hangs silently when system keyring daemon is unavailable
**Scope:** kit
**Observation:** `poetry install` hung for 2+ hours with no output, no network connections, no error, and only 6 packages installed. Root cause: Poetry attempts to unlock credentials via the system keyring (GNOME Keyring / dbus) on every package fetch. On a headless or session-less terminal without a running keyring daemon, the call blocks indefinitely waiting for a GUI prompt that never arrives. `ep_poll` in `/proc/<pid>/wchan` and zero active network connections are the diagnostic fingerprint.
**Implication:** All wiki-kit setup instructions and `bootstrap.md` should prefix any `poetry install` invocation with `PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` to disable the keyring check. Alternatively add a `poetry.toml` at the repo root with `[keyring] enabled = false` so the fix is automatic. Document the diagnostic: if `poetry install` shows no output and `wchan = ep_poll` with no network connections after 30s, it is the keyring hang — not a slow download.
**Status:** open
