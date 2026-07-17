import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

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
fig.suptitle("Set vs. multi-set Jaccard similarity by model", fontsize=13)

SET_COLOR = "tab:blue"
MULTISET_COLOR = "tab:red"
MULTISET_HATCH = "//"
OFFSET = 0.18
WIDTH = 0.32


def style_violin(parts, color, hatch=None):
    for pc in parts["bodies"]:
        pc.set_facecolor(color)
        pc.set_edgecolor(color)
        pc.set_alpha(0.7)
        if hatch:
            pc.set_hatch(hatch)
            pc.set_alpha(0.5)
    for key in ("cmedians", "cmaxes", "cmins", "cbars"):
        parts[key].set_color(color)


def collect_series(df, models, column):
    data, positions = [], []
    for i, m in enumerate(models):
        values = df.loc[df["model"] == m, column].dropna().values
        if len(values) > 0:
            data.append(values)
            positions.append(i)
    return data, positions


def add_violin(ax, df, models, title):
    positions = range(len(models))

    set_data, set_positions = collect_series(df, models, "set_jaccard")
    set_parts = ax.violinplot(
        set_data,
        positions=[p - OFFSET for p in set_positions],
        widths=WIDTH,
        showmedians=True,
    )
    style_violin(set_parts, SET_COLOR)

    multiset_data, multiset_positions = collect_series(df, models, "multiset_jaccard")
    multiset_parts = ax.violinplot(
        multiset_data,
        positions=[p + OFFSET for p in multiset_positions],
        widths=WIDTH,
        showmedians=True,
    )
    style_violin(multiset_parts, MULTISET_COLOR, hatch=MULTISET_HATCH)

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
