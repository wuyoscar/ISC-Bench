#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib>=3.8"]
# ///
"""
Generate Jailbroken Arena progress chart from history data.

Reads assets/leaderboard_history.json, outputs assets/leaderboard_progress.svg.
Run manually or via GitHub Actions on push.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from datetime import datetime, timedelta

ROOT = Path(__file__).parent.parent
DATA = ROOT / "assets" / "leaderboard_history.json"
OUT = ROOT / "assets" / "leaderboard_progress.svg"

# -- SCI Academic Palette (muted, desaturated) --
BG = "#FAFAFA"
GRID = "#E0E0E0"
RED_STRONG = "#B64342"
RED_LIGHT = "#F6CFCB"
BLUE_MAIN = "#0F4D92"
NEUTRAL_MID = "#767676"
NEUTRAL_DARK = "#4D4D4D"
NEUTRAL_BLACK = "#272727"
TEAL = "#42949E"


def main() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
        "axes.unicode_minus": False,
    })

    history = json.loads(DATA.read_text())

    dates = [datetime.strptime(h["date"], "%Y-%m-%d") for h in history]
    confirmed = [h["confirmed"] for h in history]
    total = [h["total"] for h in history]

    # Collect contributors
    contributors: dict[str, int] = {}
    for h in history:
        for ev in h.get("events", []):
            by = ev["by"]
            contributors[by] = contributors.get(by, 0) + 1

    latest = history[-1]

    # --- Figure ---
    fig, ax = plt.subplots(figsize=(9, 3.2), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Gradient fill under curve
    ax.fill_between(dates, 0, confirmed, color=RED_LIGHT, alpha=0.6, zorder=2)
    ax.fill_between(dates, 0, confirmed, color=RED_STRONG, alpha=0.08, zorder=2)

    # Main line
    ax.plot(dates, confirmed, color=RED_STRONG, linewidth=2.5,
            marker="o", markersize=7, markerfacecolor="white",
            markeredgecolor=RED_STRONG, markeredgewidth=2, zorder=5)

    # Annotate each data point with value
    for d, c in zip(dates, confirmed):
        if c > 0:
            ax.annotate(str(c), xy=(d, c), xytext=(0, 10),
                        textcoords="offset points", fontsize=10,
                        fontweight="bold", color=RED_STRONG,
                        ha="center", va="bottom", zorder=6)

    # Top-right stats box
    stats_text = f"{latest['confirmed']} / {latest['total']} models jailbroken"
    ax.text(0.98, 0.92, stats_text, transform=ax.transAxes,
            fontsize=10, fontweight="bold", color=NEUTRAL_BLACK,
            ha="right", va="top",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=GRID, linewidth=0.8, alpha=0.9))

    # Contributor badges at bottom
    contrib_parts = []
    for name, count in sorted(contributors.items(), key=lambda x: -x[1]):
        contrib_parts.append(f"@{name} ({count})")
    contrib_text = "   ".join(contrib_parts)
    ax.text(0.5, -0.22, contrib_text, transform=ax.transAxes,
            fontsize=7.5, color=NEUTRAL_MID, ha="center", style="italic")

    # --- Styling ---
    ax.set_title("Jailbroken Arena", fontsize=14, fontweight="bold",
                 color=NEUTRAL_BLACK, pad=14, loc="left")
    ax.set_ylabel("Models Jailbroken", fontsize=9, color=NEUTRAL_DARK, labelpad=8)

    # Y-axis: auto-scale to data with headroom
    y_max = max(confirmed) * 1.6 + 3
    ax.set_ylim(0, y_max)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True, nbins=6))

    # X-axis: date formatting with padding
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    if len(dates) > 1:
        pad = (dates[-1] - dates[0]) * 0.15
    else:
        pad = timedelta(days=2)
    ax.set_xlim(dates[0] - pad, dates[-1] + pad)

    # Grid and spines
    ax.grid(axis="y", color=GRID, linewidth=0.6, linestyle="-", alpha=0.7)
    ax.grid(axis="x", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=NEUTRAL_DARK, labelsize=8, length=3)

    fig.tight_layout()
    fig.savefig(OUT, format="svg", bbox_inches="tight", facecolor=BG)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
