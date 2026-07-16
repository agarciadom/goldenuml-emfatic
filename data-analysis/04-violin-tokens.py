import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

nl2ecore = pd.read_csv("nl2ecore.csv").dropna(subset=["input_tokens"])
nl2flexmi = pd.read_csv("nl2flexmi.csv").dropna(subset=["total_input_tokens"])

ecore_models = sorted(nl2ecore["model"].unique())
flexmi_models = sorted(nl2flexmi["model"].unique())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Input token counts by model", fontsize=13)


def add_violin(ax, df, models, token_col, title):
    data = [df.loc[df["model"] == m, token_col].values for m in models]
    parts = ax.violinplot(data, positions=range(len(models)), showmedians=True)
    for pc in parts["bodies"]:
        pc.set_alpha(0.7)
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, rotation=20, ha="right", fontsize=9)
    ax.set_title(title)
    ax.set_ylabel("Input tokens")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", linestyle="--", alpha=0.5)


add_violin(axes[0], nl2ecore, ecore_models, "input_tokens", "nl2ecore")
add_violin(axes[1], nl2flexmi, flexmi_models, "total_input_tokens", "nl2flexmi")

plt.tight_layout()
plt.savefig("violin-tokens.pdf", bbox_inches="tight")
plt.savefig("violin-tokens.png", dpi=150, bbox_inches="tight")
print("Saved violin-tokens.pdf and violin-tokens.png")
