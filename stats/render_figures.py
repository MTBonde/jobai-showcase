"""Render the showcase figures from stats/stats.json.

Usage (from the repo root):  python3 stats/render_figures.py

Stdlib only. Writes figures/funnel.svg. Every number comes from stats.json;
nothing is computed from raw postings.
"""

import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
STATS_PATH = REPO_ROOT / "stats" / "stats.json"
FIGURES_DIR = REPO_ROOT / "figures"

FIGURE_WIDTH = 720
ROW_HEIGHT = 46
TOP_MARGIN = 64
LABEL_COLUMN_WIDTH = 190
BAR_AREA_WIDTH = 400
MINIMUM_BAR_WIDTH = 6

THEME_STYLE = """
  .bg { fill: #ffffff; }
  .bar { fill: #2f6f9f; }
  .bar-last { fill: #c2611f; }
  .label { fill: #1f2328; font: 14px system-ui, -apple-system, Segoe UI, sans-serif; }
  .count { fill: #1f2328; font: 600 14px system-ui, -apple-system, Segoe UI, sans-serif; }
  .title { fill: #1f2328; font: 600 16px system-ui, -apple-system, Segoe UI, sans-serif; }
  .note { fill: #59636e; font: 12px system-ui, -apple-system, Segoe UI, sans-serif; }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #0d1117; }
    .bar { fill: #4f9bd1; }
    .bar-last { fill: #e8894a; }
    .label, .count, .title { fill: #e6edf3; }
    .note { fill: #9198a1; }
  }
"""


def format_danish_thousands(number):
    return f"{number:,}".replace(",", ".")


def scaled_bar_width(count, largest_count):
    """Log scale: 10.245 and 5 cannot share a linear axis and both stay readable."""
    if count <= 1:
        return MINIMUM_BAR_WIDTH
    fraction = math.log10(count) / math.log10(largest_count)
    return max(MINIMUM_BAR_WIDTH, round(fraction * BAR_AREA_WIDTH))


def render_funnel_svg(funnel):
    steps = funnel["steps"]
    if not steps:
        raise ValueError("stats.json funnel has no steps; nothing to draw")
    largest_count = max(step["count"] for step in steps)
    figure_height = TOP_MARGIN + ROW_HEIGHT * len(steps) + 40

    title = f"Fra opslag til ansøgning, runde {funnel['round']} ({funnel['date']})"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{FIGURE_WIDTH}" '
        f'height="{figure_height}" viewBox="0 0 {FIGURE_WIDTH} {figure_height}" '
        f'role="img" aria-label="{escape(title)}">',
        f"<style>{THEME_STYLE}</style>",
        f'<rect class="bg" width="{FIGURE_WIDTH}" height="{figure_height}" rx="8"/>',
        f'<text class="title" x="20" y="34">{escape(title)}</text>',
    ]
    for index, step in enumerate(steps):
        row_top = TOP_MARGIN + index * ROW_HEIGHT
        bar_width = scaled_bar_width(step["count"], largest_count)
        bar_class = "bar-last" if index == len(steps) - 1 else "bar"
        parts.append(
            f'<text class="label" x="20" y="{row_top + 22}">{escape(step["label"])}</text>'
        )
        parts.append(
            f'<rect class="{bar_class}" x="{LABEL_COLUMN_WIDTH + 20}" y="{row_top + 6}" '
            f'width="{bar_width}" height="24" rx="4"/>'
        )
        parts.append(
            f'<text class="count" x="{LABEL_COLUMN_WIDTH + 30 + bar_width}" '
            f'y="{row_top + 23}">{format_danish_thousands(step["count"])}</text>'
        )
    parts.append(
        f'<text class="note" x="20" y="{figure_height - 16}">'
        "Logaritmisk skala. Tæller rækker; samme job kan stå på flere portaler.</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    if not STATS_PATH.exists():
        sys.exit(f"FAILED: {STATS_PATH} not found; run from a checkout of the showcase repo")
    stats = json.loads(STATS_PATH.read_text(encoding="utf-8"))
    FIGURES_DIR.mkdir(exist_ok=True)
    funnel_path = FIGURES_DIR / "funnel.svg"
    funnel_path.write_text(render_funnel_svg(stats["funnel"]), encoding="utf-8")
    print(f"wrote {funnel_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
