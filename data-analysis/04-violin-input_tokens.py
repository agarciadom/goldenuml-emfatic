import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

matplotlib.rcParams["pdf.fonttype"] = 42

nl2ecore = pd.read_csv("nl2ecore.csv").dropna(subset=["input_tokens"])
nl2flexmi = pd.read_csv("nl2flexmi.csv").dropna(subset=["total_input_tokens"])

ecore_models = sorted(nl2ecore["model"].unique())
flexmi_models = sorted(nl2flexmi["model"].unique())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

JITTER_WIDTH = 0.12
rng = np.random.default_rng(0)


def add_violin(ax, df, models, token_col, title):
    data = [df.loc[df["model"] == m, token_col].values for m in models]
    parts = ax.violinplot(data, positions=range(len(models)), showmedians=True)
    for pc in parts["bodies"]:
        pc.set_alpha(0.7)
    for i, values in enumerate(data):
        x = i + rng.uniform(-JITTER_WIDTH, JITTER_WIDTH, size=len(values))
        ax.scatter(x, values, color="black", s=8, alpha=0.4, edgecolors="none", zorder=3)
    label_y_offset = max(values.max() for values in data) * 0.02
    for i, values in enumerate(data):
        median = np.median(values)
        ax.text(
            i,
            median + label_y_offset,
            f"{median:,.0f}",
            fontsize=7,
            ha="center",
            va="bottom",
            bbox=dict(facecolor="white", edgecolor="none", alpha=1.0, pad=1),
        )
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, rotation=20, ha="right", fontsize=9)
    ax.set_title(title)
    ax.set_ylabel("Input tokens")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", linestyle="--", alpha=0.5)


add_violin(axes[0], nl2ecore, ecore_models, "input_tokens", "nl2ecore")
add_violin(axes[1], nl2flexmi, flexmi_models, "total_input_tokens", "nl2flexmi")

plt.tight_layout()
plt.savefig("violin-input-tokens.pdf", bbox_inches="tight")
plt.savefig("violin-input-tokens.png", dpi=150, bbox_inches="tight")
print("Saved violin-input-tokens.pdf and violin-input-tokens.png")
