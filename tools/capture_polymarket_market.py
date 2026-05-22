"""Capture a Polymarket event (and its sub-markets) via the Gamma API.

Writes a dated markdown snapshot containing the full resolution-rule description,
current odds, volumes, OI, liquidity, and per-sub-market detail to the wiki's
`raw/markets/<slug>/<YYYY-MM-DD>.md` convention (or a custom path via `--out`).

This complements `capture_url` for Polymarket event pages, which are SPA-heavy and
unreliable to scrape; the Gamma API exposes the same data structurally, including
the binding resolution-rule text that the rendered page hides in component 3
(edge cases) per the canonical Polymarket rule grammar — see
`wiki/mention-markets.md` for why this matters.

Usage:
    poetry run python -m tools.capture_polymarket_market --slug <event-slug>
    poetry run python -m tools.capture_polymarket_market --slug <event-slug> --out raw/research/<topic>

The slug is the trailing segment of a Polymarket event URL:
    https://polymarket.com/event/<event-slug>           → use <event-slug>
    https://polymarket.com/event/<event-slug>/<market>  → use <event-slug>

If you pass a full URL, it is parsed for you.

Exits non-zero on HTTP failure, JSON decode failure, or empty result.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import httpx

from tools._common import USER_AGENT, today_iso, write_frontmatter

GAMMA_EVENTS_ENDPOINT = "https://gamma-api.polymarket.com/events"


def slug_from_arg(arg: str) -> str:
    """Accept either a bare slug or a full Polymarket URL; return the event slug."""
    if not arg.startswith("http"):
        return arg.strip("/")
    path = urlparse(arg).path.strip("/")
    parts = path.split("/")
    # URL patterns observed: /event/<slug> and /event/<slug>/<sub-market-slug>
    if parts and parts[0] == "event" and len(parts) >= 2:
        return parts[1]
    # Fall back to last non-empty segment
    return parts[-1] if parts else arg


def fetch_event(slug: str, *, timeout: float = 30.0) -> dict:
    """Fetch a Polymarket event by slug. Returns the first event dict or raises."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    with httpx.Client(follow_redirects=True, timeout=timeout, headers=headers) as client:
        r = client.get(GAMMA_EVENTS_ENDPOINT, params={"slug": slug})
        r.raise_for_status()
        data = r.json()
    if not isinstance(data, list) or not data:
        raise RuntimeError(f"Gamma API returned no events for slug={slug!r}")
    return data[0]


def render_markdown(event: dict) -> str:
    """Render a Gamma event JSON dict as the wiki's markdown+frontmatter convention."""
    slug = event.get("slug", "")
    title = event.get("title", "(untitled)")
    end_date = event.get("endDate", "")
    desc = (event.get("description") or "").strip()
    liquidity = event.get("liquidity", 0)
    volume = event.get("volume", 0)
    open_interest = event.get("openInterest", 0)
    vol_24hr = event.get("volume24hr", 0)
    vol_1wk = event.get("volume1wk", 0)
    closed = event.get("closed", False)
    active = event.get("active", False)
    neg_risk = event.get("negRisk", False)
    comment_count = event.get("commentCount", 0)
    markets = event.get("markets") or []

    fm = write_frontmatter({
        "source": f"https://polymarket.com/event/{slug}",
        "api_endpoint": f"{GAMMA_EVENTS_ENDPOINT}?slug={slug}",
        "slug": slug,
        "captured_on": today_iso(),
        "capture_method": "gamma-api",
        "title": title,
        "end_date": end_date,
        "active": active,
        "closed": closed,
        "neg_risk": neg_risk,
    })

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(
        f"Polymarket event captured via Gamma API on {today_iso()}. "
        f"Event slug: `{slug}`. End date: `{end_date}`. "
        f"Active: `{active}`. Closed: `{closed}`. NegRisk: `{neg_risk}`."
    )
    lines.append("")

    # Event-level metrics
    lines.append("## Event metrics")
    lines.append("")
    lines.append(f"- **Liquidity:** ${liquidity:,.2f}")
    lines.append(f"- **Volume (all-time):** ${volume:,.2f}")
    lines.append(f"- **Open interest:** ${open_interest:,.2f}")
    lines.append(f"- **Volume 24hr:** ${vol_24hr:,.2f}")
    lines.append(f"- **Volume 1wk:** ${vol_1wk:,.2f}")
    lines.append(f"- **Comments:** {comment_count}")
    lines.append("")

    # Event-level resolution rules / description (the binding spec)
    lines.append("## Event description / resolution rules")
    lines.append("")
    if desc:
        lines.append(desc)
    else:
        lines.append("_(no event-level description)_")
    lines.append("")

    # Per-sub-market table + per-market rules
    if markets:
        lines.append(f"## Markets ({len(markets)})")
        lines.append("")
        lines.append("| Sub-market | Outcomes | Prices | Vol | Liq | Bond | Reward | Tick | Min Size |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for m in markets:
            q = m.get("question") or m.get("groupItemTitle") or m.get("slug", "")
            outcomes_raw = m.get("outcomes") or "[]"
            prices_raw = m.get("outcomePrices") or "[]"
            try:
                outcomes = json.loads(outcomes_raw)
            except json.JSONDecodeError:
                outcomes = []
            try:
                prices = json.loads(prices_raw)
            except json.JSONDecodeError:
                prices = []
            outcomes_str = " / ".join(outcomes) if outcomes else "—"
            prices_str = (
                " / ".join(f"{float(p):.4f}" for p in prices) if prices else "—"
            )
            vol_m = m.get("volume") or m.get("volumeNum") or 0
            try:
                vol_m_f = float(vol_m)
            except (TypeError, ValueError):
                vol_m_f = 0.0
            liq_m = m.get("liquidity") or m.get("liquidityNum") or 0
            try:
                liq_m_f = float(liq_m)
            except (TypeError, ValueError):
                liq_m_f = 0.0
            uma_bond = m.get("umaBond", "—")
            uma_reward = m.get("umaReward", "—")
            tick = m.get("orderPriceMinTickSize", "—")
            min_size = m.get("orderMinSize", "—")
            # Truncate long questions for table width
            q_short = q if len(q) <= 80 else q[:77] + "..."
            lines.append(
                f"| {q_short} | {outcomes_str} | {prices_str} | "
                f"${vol_m_f:,.0f} | ${liq_m_f:,.0f} | "
                f"{uma_bond} | {uma_reward} | {tick} | {min_size} |"
            )
        lines.append("")

        # Per-market description blocks (the load-bearing component 3 edge-case rules)
        lines.append("## Per-market resolution rules")
        lines.append("")
        for i, m in enumerate(markets, 1):
            q = m.get("question") or m.get("slug", "")
            m_slug = m.get("slug", "")
            m_desc = (m.get("description") or "").strip()
            condition_id = m.get("conditionId", "")
            question_id = m.get("questionID", "")
            uma_resolution_status = m.get("umaResolutionStatus", "")
            closed_time = m.get("closedTime", "")
            resolved_by = m.get("resolvedBy", "")
            lines.append(f"### {i}. {q}")
            lines.append("")
            lines.append(f"- Slug: `{m_slug}`")
            lines.append(f"- `conditionId`: `{condition_id}`")
            lines.append(f"- `questionID`: `{question_id}`")
            if uma_resolution_status:
                lines.append(f"- UMA resolution status: `{uma_resolution_status}`")
            if resolved_by:
                lines.append(f"- Resolved by: `{resolved_by}`")
            if closed_time:
                lines.append(f"- Closed at: `{closed_time}`")
            lines.append("")
            lines.append("**Resolution rules:**")
            lines.append("")
            lines.append(m_desc if m_desc else "_(no description)_")
            lines.append("")

    return fm + "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument(
        "--slug",
        required=True,
        help="Polymarket event slug or full event URL.",
    )
    p.add_argument(
        "--out",
        default=None,
        help=(
            "Output directory. Defaults to raw/markets/<slug>/. "
            "Use this to override (e.g., raw/research/<topic>)."
        ),
    )
    p.add_argument(
        "--filename",
        default=None,
        help="Output filename (without directory). Defaults to <YYYY-MM-DD>.md.",
    )
    args = p.parse_args()

    slug = slug_from_arg(args.slug)
    try:
        event = fetch_event(slug)
    except (httpx.HTTPError, RuntimeError, json.JSONDecodeError) as e:
        print(f"capture_polymarket_market failed: {e}", file=sys.stderr)
        return 1

    body = render_markdown(event)

    out_dir = Path(args.out) if args.out else Path("raw/markets") / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = args.filename or f"{today_iso()}.md"
    out_path = out_dir / filename
    out_path.write_text(body, encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
