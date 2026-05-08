# AGENTS.md effectiveness eval

ETH Zürich rigorous test of whether AGENTS.md / CLAUDE.md context files actually improve coding-agent task resolution — something agent developers have widely recommended without empirical backing. Across four agents and multiple LLMs on both SWE-bench Lite (popular repos, LLM-generated context) and a new benchmark **AGENTbench** (138 instances from 12 niche Python repos with developer-written context files), LLM-generated context files *reduce* success rate ~3% on average and inflate inference cost over 20%; developer-written files give a marginal +4%. The headline conclusion contradicts current agent-vendor recommendations: omit LLM-generated context files, and keep human-written ones to *minimal requirements only*.

## AGENTbench setup

- **138 instances** drawn from 5,694 PRs across 12 repositories — niche/less-popular Python projects with developer-committed `AGENTS.md` or `CLAUDE.md` at root, test suites, and minimum PR thresholds.
- Tasks: bug-fixing and feature-addition from real GitHub issues. PR-derived task descriptions LLM-standardised; unit tests LLM-generated and manually verified to fail pre-patch / pass post-patch (avg 75% coverage of modified code).
- **Three settings per task**: *None* (context file removed even if developer-provided), *LLM* (context generated via the agent's built-in `/init`-style command on the pre-patch repo), *Human* (developer-written file used as-is).

The benchmark complements [[swe-bench-pro]]: SWE-bench Pro tests against contamination at the *repo* level (private/GPL); AGENTbench tests against an *intervention* (the context file itself) and pulls from a different distribution (niche, recent, developer-context-equipped).

## Results

| Setting | Success delta vs no-context | Cost delta | Steps delta |
|---|---|---|---|
| LLM-generated, AGENTbench | **−3%** (drops in 5/8 model×dataset combos) | **+23%** | +5.4 |
| LLM-generated, SWE-bench Lite | **−3%** | **+20%** | +2.8 |
| Developer-provided, AGENTbench | **+4%** | up to **+19%** | +4.6 |

Reasoning-token deltas: LLM context adds 22% (GPT-5.2) / 14% (GPT-5.1 mini) on SWE-bench Lite; developer context adds 20% / 2%.

**Behavioural change:** context files cause more testing, more file traversal/grep/read, more use of repo-specific tooling. Agents do follow instructions: `uv` invoked 1.6× per instance when mentioned vs <0.01× otherwise; repo-specific tools 2.5× when mentioned vs <0.05× otherwise. Compliance is not the problem — *exploration inflation* is.

**The reconciling ablation.** When all `.md`/`docs/` files are removed from the repo, LLM-generated context files become helpful (+9% on average, outperforming developer context). This shows the negative result is specific to *well-documented* repos where context files duplicate what's already discoverable. In undocumented repos the same files become load-bearing.

## Recommendations (stated explicitly in the paper)

1. **Omit LLM-generated context files** for now, contrary to current agent-developer recommendations.
2. If using human-written context files, **include only minimal requirements** — specifically tooling the agent cannot otherwise discover (`use uv`, repo-specific test runner invocations).
3. **Do not include codebase overviews or directory enumerations** — the paper shows these do *not* reduce the steps required for agents to find relevant files.

## Limitations

- **Python-only** — models may have strong parametric knowledge of Python tooling that nullifies the context-file benefit; niche-language results may differ.
- **138 instances from 12 repos** — context-file adoption is recent and uneven, constraining the qualifying repo pool.
- **Four agents** (Claude Code/Sonnet 4.5, Codex/GPT-5.2, Codex/GPT-5.1 mini, Qwen Code/Qwen3-30B); doesn't cover all available agents.
- **Single dimension measured** — issue-resolution success only; security and code-quality dimensions not evaluated; prior work suggests context prompting can help security.

## Why it matters

- **Empirical correction to vendor guidance.** Agent vendors (Anthropic, OpenAI, the AGENTS.md spec at agents.md) all recommend context files; this is the first rigorous test and the average effect is *negative* in well-maintained mid-sized Python repos.
- **Operationalises the redundancy mechanism.** Inflated exploration tokens — not non-compliance — is the failure mode: context files prompt the agent to over-explore the directory tree before attempting a targeted fix, exhausting reasoning tokens on confirmation rather than action.
- **Sets the boundary condition for [[codified-context]].** The optimism in the Codified Context paper applies at a different scale and documentation regime; see [[../conflicts/agents-md-effectiveness]] for the reconciliation.

## Source

- `raw/research/long-horizon-context/03-03-agents-md-eval.md` (captured 2026-04-25 from https://arxiv.org/abs/2602.11988)

## Related

- [[swe-bench-pro]] — peer benchmark; AGENTbench is the intervention-side complement to Pro's repo-side contamination defence.
- [[codified-context]] — opposing optimism on context infrastructure at 100k+ line scale.
- [[../conflicts/agents-md-effectiveness]] — resolution of the apparent contradiction.
- [[topology-taxonomy#long-horizon-context-loss]] — exploration inflation is one concrete mechanism behind the long-horizon failure mode.
- [[airs-bench]] — research-agent peer benchmark; together with this page and swe-bench-pro forms the three-way coding/research/intervention eval set.
