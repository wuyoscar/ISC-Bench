#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib>=3.8"]
# ///
"""
Generate ISC Leaderboard progress chart from history data.

Reads assets/leaderboard_history.json, outputs assets/leaderboard_progress.svg.
Run manually or via GitHub Actions on push.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

ROOT = Path(__file__).parent.parent
DATA = ROOT / "assets" / "leaderboard_history.json"
OUT = ROOT / "assets" / "leaderboard_progress.svg"

# -- Muted academic palette --
BG = "#FFFFFF"
GRID = "#E8E8E8"
RED = "#C44E52"
GREEN = "#8FBC8F"
TEXT = "#333333"
ACCENT = "#555555"


def main() -> None:
    history = json.loads(DATA.read_text())

    dates = [datetime.strptime(h["date"], "%Y-%m-%d") for h in history]
    confirmed = [h["confirmed"] for h in history]
    total = [h["total"] for h in history]
    remaining = [t - c for t, c in zip(total, confirmed)]

    # Collect contributors
    contributors: dict[str, int] = {}
    for h in history:
        for ev in h.get("events", []):
            by = ev["by"]
            contributors[by] = contributors.get(by, 0) + 1

    fig, ax = plt.subplots(figsize=(8, 3.5), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Stacked area
    ax.fill_between(dates, 0, confirmed, color=RED, alpha=0.25, label="Jailbroken")
    ax.fill_between(dates, confirmed, total, color=GREEN, alpha=0.15, label="Remaining")
    ax.plot(dates, confirmed, color=RED, linewidth=2.5, marker="o", markersize=6, zorder=5)
    ax.plot(dates, total, color=GREEN, linewidth=1, linestyle="--", alpha=0.5)

    # Annotate latest
    latest = history[-1]
    ax.annotate(
        f'{latest["confirmed"]} / {latest["total"]}',
        xy=(dates[-1], confirmed[-1]),
        xytext=(10, 10), textcoords="offset points",
        fontsize=11, fontweight="bold", color=RED,
        arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2),
    )

    # Contributor annotations (small text at bottom)
    contrib_text = "  ".join(f"@{k}: {v}" for k, v in sorted(contributors.items(), key=lambda x: -x[1]))
    ax.text(0.01, -0.18, f"Contributors: {contrib_text}",
            transform=ax.transAxes, fontsize=7, color=ACCENT, style="italic")

    # Style
    ax.set_ylabel("Models", fontsize=10, color=TEXT)
    ax.set_title("Jailbroken Arena Progress", fontsize=13, fontweight="bold", color=TEXT, pad=12)
    ax.set_ylim(0, max(total) + 5)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.tick_params(colors=TEXT, labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID)

    fig.tight_layout()
    fig.savefig(OUT, format="svg", bbox_inches="tight", facecolor=BG)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
