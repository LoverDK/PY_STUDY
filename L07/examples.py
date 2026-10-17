#!/usr/bin/env python3
"""L07 examples. Default: PNG rendering to memory only.
Optional user command: python examples.py --out-dir out
No seaborn. Requires matplotlib only; CSV uses the standard library.
"""
import argparse
import csv
from io import BytesIO
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent

def render(fig, name, out_dir):
    target = BytesIO() if out_dir is None else out_dir / (name + ".png")
    fig.savefig(target, format="png", dpi=150, bbox_inches="tight")
    if out_dir is None:
        payload = target.getvalue()
        assert payload.startswith(b"\x89PNG\r\n\x1a\n")
        print(name, "PNG bytes:", len(payload))
    else:
        print("saved:", target)

def demo_categories(out_dir):
    with (HERE / "data" / "category_totals.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    names = [r["category"] for r in rows]
    values = [int(r["exercises"]) for r in rows]
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        bars = ax.bar(names, values, width=0.6,
                      color="steelblue", edgecolor="black")
        ax.set(xlabel="Course", ylabel="Exercises",
               title="Exercises by course", ylim=(0, None))
        assert [p.get_height() for p in bars] == [12, 8, 10]
        render(fig, "category_totals", out_dir)
    finally:
        plt.close(fig)

def demo_histogram(out_dir):
    with (HERE / "data" / "durations.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        values = [float(r["minutes"]) for r in csv.DictReader(handle)]
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        counts, edges, patches = ax.hist(
            values, bins=[10, 20, 30, 40], density=False,
            color="darkorange", edgecolor="black"
        )
        ax.set(xlabel="Minutes", ylabel="Count",
               title="Completion time", ylim=(0, None))
        assert counts.tolist() == [2.0, 2.0, 4.0]
        assert edges.tolist() == [10.0, 20.0, 30.0, 40.0]
        print("hist counts:", counts.tolist())
        render(fig, "duration_histogram", out_dir)
    finally:
        plt.close(fig)

def demo_groups(out_dir):
    categories = ["Week1", "Week2", "Week3"]
    a, b = [6, 8, 10], [5, 9, 7]
    positions, width = list(range(3)), 0.36
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        ax.bar([i-width/2 for i in positions], a,
               width=width, color="blue", label="A")
        ax.bar([i+width/2 for i in positions], b,
               width=width, color="orange", label="B")
        ax.set_xticks(positions)
        ax.set_xticklabels(categories)
        ax.set(xlabel="Week", ylabel="Exercises",
               title="A vs B practice", ylim=(0, None))
        legend = ax.legend(loc="upper left", title="Group")
        assert [t.get_text() for t in legend.get_texts()] == ["A", "B"]
        assert len(ax.patches) == 6
        render(fig, "grouped_bars", out_dir)
    finally:
        plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Explicitly enable PNG file output.")
    args = parser.parse_args()
    if args.out_dir is not None:
        args.out_dir.mkdir(parents=True, exist_ok=True)
    original_figures = set(plt.get_fignums())
    demo_categories(args.out_dir)
    demo_histogram(args.out_dir)
    demo_groups(args.out_dir)
    assert set(plt.get_fignums()) == original_figures
    print("L07 example assertions passed")

if __name__ == "__main__":
    main()
