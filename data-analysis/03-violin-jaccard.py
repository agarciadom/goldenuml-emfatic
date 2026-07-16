import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

nl2ecore = pd.read_csv("nl2ecore.csv").dropna(subset=["set_jaccard"])
nl2flexmi = pd.read_csv("nl2flexmi.csv").dropna(subset=["set_jaccard"])

ecore_models = sorted(nl2ecore["model"].unique())
flexmi_models = sorted(nl2flexmi["model"].unique())

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
fig.suptitle("Set Jaccard similarity by model", fontsize=13)


def add_violin(ax, df, models, title):
    data = [df.loc[df["model"] == m, "set_jaccard"].values for m in models]
    parts = ax.violinplot(data, positions=range(len(models)), showmedians=True)
    for pc in parts["bodies"]:
        pc.set_alpha(0.7)
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, rotation=20, ha="right", fontsize=9)
    ax.set_title(title)
    ax.set_ylabel("Set Jaccard")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
    ax.set_ylim(0, 1)
    ax.grid(axis="y", linestyle="--", alpha=0.5)


add_violin(axes[0], nl2ecore, ecore_models, "nl2ecore")
add_violin(axes[1], nl2flexmi, flexmi_models, "nl2flexmi")

plt.tight_layout()
plt.savefig("violin-jaccard.pdf", bbox_inches="tight")
plt.savefig("violin-jaccard.png", dpi=150, bbox_inches="tight")
print("Saved violin-jaccard.pdf and violin-jaccard.png")
