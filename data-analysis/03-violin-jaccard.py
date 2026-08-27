import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

matplotlib.rcParams["pdf.fonttype"] = 42

nl2ecore = pd.read_csv("nl2ecore.csv")
nl2flexmi = pd.read_csv("nl2flexmi.csv")

ecore_models = sorted(
    nl2ecore.dropna(subset=["set_jaccard", "multiset_jaccard"], how="all")[
        "model"
    ].unique()
)
flexmi_models = sorted(
    nl2flexmi.dropna(subset=["set_jaccard", "multiset_jaccard"], how="all")[
        "model"
    ].unique()
)

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

SET_COLOR = "tab:blue"
SET_EDGE_COLOR = "tab:blue"
MULTISET_COLOR = "tab:red"
MULTISET_EDGE_COLOR = "darkred"
MULTISET_HATCH = "//"
OFFSET = 0.18
WIDTH = 0.32
JITTER_WIDTH = WIDTH * 0.35
LABEL_Y_OFFSET = 0.02

rng = np.random.default_rng(0)


def style_violin(parts, face_color, edge_color, hatch=None):
    for pc in parts["bodies"]:
        pc.set_facecolor(face_color)
        pc.set_edgecolor(edge_color)
        pc.set_alpha(0.7)
        if hatch:
            pc.set_hatch(hatch)
            pc.set_alpha(0.5)
    for key in ("cmedians", "cmaxes", "cmins", "cbars"):
        parts[key].set_color(edge_color)


def collect_series(df, models, column):
    data, positions = [], []
    for i, m in enumerate(models):
        values = df.loc[df["model"] == m, column].dropna().values
        if len(values) > 0:
            data.append(values)
            positions.append(i)
    return data, positions


def add_jitter(ax, data, positions, color):
    for values, p in zip(data, positions):
        x = p + rng.uniform(-JITTER_WIDTH, JITTER_WIDTH, size=len(values))
        ax.scatter(x, values, color=color, s=8, alpha=0.6, edgecolors="none", zorder=3)


def annotate_medians(ax, data, positions, side, color):
    x_offset = -OFFSET if side == "left" else OFFSET
    for values, p in zip(data, positions):
        median = np.median(values)
        ax.text(
            p + x_offset,
            median + LABEL_Y_OFFSET,
            f"{median:.2f}",
            fontsize=7,
            ha="center",
            va="bottom",
            color=color,
            bbox=dict(facecolor="white", edgecolor="none", alpha=1.0, pad=1),
        )


def add_violin(ax, df, models, title):
    positions = range(len(models))

    set_data, set_positions = collect_series(df, models, "set_jaccard")
    set_parts = ax.violinplot(
        set_data,
        positions=[p - OFFSET for p in set_positions],
        widths=WIDTH,
        showmedians=True,
    )
    style_violin(set_parts, SET_COLOR, SET_EDGE_COLOR)
    add_jitter(ax, set_data, [p - OFFSET for p in set_positions], SET_EDGE_COLOR)
    annotate_medians(ax, set_data, set_positions, "left", SET_EDGE_COLOR)

    multiset_data, multiset_positions = collect_series(df, models, "multiset_jaccard")
    multiset_parts = ax.violinplot(
        multiset_data,
        positions=[p + OFFSET for p in multiset_positions],
        widths=WIDTH,
        showmedians=True,
    )
    style_violin(multiset_parts, MULTISET_COLOR, MULTISET_EDGE_COLOR, hatch=MULTISET_HATCH)
    add_jitter(ax, multiset_data, [p + OFFSET for p in multiset_positions], MULTISET_EDGE_COLOR)
    annotate_medians(ax, multiset_data, multiset_positions, "right", MULTISET_EDGE_COLOR)

    ax.set_xticks(list(positions))
    ax.set_xticklabels(models, rotation=20, ha="right", fontsize=9)
    ax.set_title(title)
    ax.set_ylabel("Jaccard similarity")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
    ax.set_ylim(0, 1)
    ax.grid(axis="y", linestyle="--", alpha=0.5)


add_violin(axes[0], nl2ecore, ecore_models, "nl2ecore")
add_violin(axes[1], nl2flexmi, flexmi_models, "nl2flexmi")

legend_handles = [
    plt.Rectangle((0, 0), 1, 1, facecolor=SET_COLOR, alpha=0.7, label="Set Jaccard"),
    plt.Rectangle(
        (0, 0),
        1,
        1,
        facecolor=MULTISET_COLOR,
        edgecolor=MULTISET_EDGE_COLOR,
        alpha=0.5,
        hatch=MULTISET_HATCH,
        label="Multi-set Jaccard",
    ),
]
fig.legend(handles=legend_handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
plt.savefig("violin-jaccard.pdf", bbox_inches="tight")
plt.savefig("violin-jaccard.png", dpi=150, bbox_inches="tight")
print("Saved violin-jaccard.pdf and violin-jaccard.png")
