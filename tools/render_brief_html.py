"""Render a weekly-brief markdown file as a legible HTML email body.

Used by /weekly-brief step 8 to produce the HTML alternative sent alongside
the plain-text markdown. Styling is inlined / in a <style> block; Outlook
(web + desktop) and Gmail both render this cleanly. Width is capped for
readability on a phone.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import markdown

EMAIL_CSS = """
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  line-height: 1.55;
  color: #24292f;
  max-width: 760px;
  margin: 0 auto;
  padding: 20px 24px;
  background: #ffffff;
}
h1 {
  font-size: 20px;
  font-weight: 600;
  border-bottom: 1px solid #d0d7de;
  padding-bottom: 6px;
  margin-top: 28px;
  margin-bottom: 12px;
  color: #1f2328;
}
h2 {
  font-size: 16px;
  font-weight: 600;
  margin-top: 20px;
  margin-bottom: 8px;
  color: #3b434d;
}
h3 {
  font-size: 14px;
  font-weight: 600;
  margin-top: 14px;
  margin-bottom: 6px;
  color: #3b434d;
}
p { margin: 8px 0; }
ul, ol { padding-left: 24px; margin: 8px 0; }
li { margin-bottom: 4px; }
code {
  background: #f6f8fa;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 90%;
  font-family: "SF Mono", ui-monospace, Menlo, Consolas, "Liberation Mono", monospace;
  color: #24292f;
}
pre {
  background: #f6f8fa;
  padding: 12px 14px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 88%;
  line-height: 1.45;
  margin: 10px 0;
  border: 1px solid #eaeef2;
}
pre code { background: transparent; padding: 0; }
blockquote {
  margin: 10px 0;
  padding: 6px 14px;
  border-left: 3px solid #d0d7de;
  color: #57606a;
  background: #f6f8fa;
}
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
strong { font-weight: 600; color: #1f2328; }
em { color: #57606a; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 20px 0; }
.banner {
  background: #fff8c5;
  border-left: 4px solid #d4a72c;
  padding: 10px 14px;
  margin: 0 0 16px 0;
  border-radius: 4px;
  font-size: 95%;
}
.banner code {
  background: #fff4a3;
}
.footer {
  color: #6e7781;
  font-size: 85%;
  margin-top: 28px;
  border-top: 1px solid #d0d7de;
  padding-top: 10px;
}
""".strip()


def render(md_text: str, title: str = "Weekly AI radar") -> str:
    body_html = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "sane_lists", "nl2br"],
        output_format="html5",
    )
    body_html = _style_banner(body_html)
    body_html = _style_footer(body_html)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{EMAIL_CSS}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""


def _style_banner(html: str) -> str:
    """Wrap the opening ⚠ paragraph(s) in a .banner div for visual emphasis."""
    marker = "<p>⚠"
    if marker not in html:
        return html
    start = html.index(marker)
    # Banner runs until the first <h1> (end of intro block).
    end = html.find("<h1", start)
    if end == -1:
        return html
    before, middle, after = html[:start], html[start:end], html[end:]
    return f'{before}<div class="banner">{middle}</div>{after}'


def _style_footer(html: str) -> str:
    """Wrap the trailing em-dash attribution line in a .footer div."""
    marker = "<p>— Weekly brief generated"
    if marker not in html:
        return html
    start = html.index(marker)
    return html[:start] + '<div class="footer">' + html[start:] + "</div>"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="inp", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--title", default="Weekly AI radar")
    args = parser.parse_args()

    md_text = args.inp.read_text(encoding="utf-8")
    # Drop any "Subject: ..." first line — that belongs in the email header, not the body.
    lines = md_text.splitlines()
    if lines and lines[0].lower().startswith("subject:"):
        md_text = "\n".join(lines[1:]).lstrip()

    html = render(md_text, title=args.title)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(str(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
