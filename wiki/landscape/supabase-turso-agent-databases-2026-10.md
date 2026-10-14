# Supabase $150M Raise and Turso Acquisition: Agent-Created Databases (2026-10)

Supabase announced (2026-10-07 capture) a $150M round led by GIC (with CapitalG, IronArc, SquarePeg) and the acquisition of database company Turso, four months after its $500M Series F. Headline claim: ~70% of new Supabase databases are created by agents or AI-driven tools. Turso's tech targets provisioning very large numbers of isolated databases cheaply, aimed at agent-driven workloads.

## What happened

- **$150M new funding**, led by **GIC**; participants **CapitalG, IronArc, SquarePeg**. Part of the round is employee liquidity.
- Follows the **$500M Series F** from four months earlier (per source; see [[2026-07-01]] brief for the Series F entry).
- **Turso acquired.** Founder **Glauber Costa** becomes Head of Agentic Services; co-founder **Pekka Enberg** and the Turso team also join.
- Turso continues operating its existing platform; Supabase says it plans a path for Turso customers to use the wider Supabase ecosystem. Timeline not specified in source.

## What it does

- Supabase: open-source Postgres development platform; products span Postgres, authentication, storage, edge functions, real-time subscriptions, vector search. Positioned as backend for both human developers and agents.
- Turso adds tech to provision large numbers of isolated databases at "relatively low cost" (vendor framing).

## Techniques

Architecture detail not specified in source beyond: on-demand databases, per-database isolation. Turso founder's stated goal is serving "upwards of a billion databases" (quote, 2026-10-07).

## Deployment

Turso supports on-demand databases in public cloud and bring-your-own-cloud (BYOC). Named Turso customers: Superhuman, Sauna.ai, CTO.new, Mastra.

## Costs

Pricing not specified in source.

## Limits

Not specified in source. Isolation model, cold-start, and Postgres-vs-SQLite-style compatibility between the two stacks are unaddressed *(editorial: the integration path is the open question)*.

## Reception and growth claims (vendor-reported, unverified)

- More than **1M users and 4M databases added per month**; ~**70%** of new databases created by agents or AI tools.
- **600% YoY** database growth reported in June 2026, when agents already deployed the majority of new databases.
- **13M+ developers**; **100+** integrated partner tools; founded 2020.
- CEO Paul Copplestone: "the future is agents"; attributes growth to coding tools including Claude Code and Codex. CapitalG's Derek Zanutto calls Supabase the "critical open infrastructure layer powering the AI revolution" (investor quote).
- *(Editorial)* Thesis: agents, not humans, become the primary database creators, so the unit of provisioning shifts from one-per-app to one-per-task/agent. Single press-release-derived source; metrics are self-reported.

## Source

- raw/research/weekly-2026-10-07/02-supabase-turso.md (Pulse 2, https://pulse2.com/supabase-raises-150-million-and-acquires-turso/, captured 2026-10-07)

## Related

- [[ai-app-categories-2025]]
- [[agentic-compute-pricing-2026-04]]
- [[ai-infrastructure-frontiers-2026]]
- [[databricks]]
