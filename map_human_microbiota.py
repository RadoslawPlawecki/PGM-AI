"""
@author: Radosław Pławecki
"""

from common import use_latex
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

use_latex()

df = pd.read_csv("hmp_data.csv")

print(df.columns)

table_binary = pd.crosstab(
    df["HMP Isolation Body Site"],
    df["Domain"]
)

table_binary = (table_binary > 0).astype(int)

manual_xticks = ["Archaeal", "Bacterial", "Eukaryal", "Virus"]
manual_yticks = ["Airways", "Blood", "Bone", "Ear", "Eye", "Gastrointestinal tract", "Heart", "Liver", "Lymph nodes", "Nose", "Oral", "Other", "Skin", "Unknown", "Urogenital tract", "Wound"]

fig, ax = plt.subplots(figsize=(12,8))

sns.heatmap(
    table_binary,
    cmap="Greens",           
    linewidths=0.5,
    linecolor='gray',
    cbar_kws={
        "label": "Presence (1) / Absence (0)",
        "ticks": [0, 1]
    },
    vmin=0,
    vmax=1
)

# map ticks manually
ax.set_xticks([i + 0.5 for i in range(len(manual_xticks))])
ax.set_yticks([i + 0.5 for i in range(len(manual_yticks))])
ax.set_xticklabels(manual_xticks, rotation=0, fontsize=16)
ax.set_yticklabels(manual_yticks, rotation=0, fontsize=16)

# access the colorbar and set fontsize
cbar = ax.collections[0].colorbar
cbar.ax.yaxis.label.set_size(18)  # fontsize for colorbar label
cbar.ax.tick_params(labelsize=16)

# labels and title
ax.set_xlabel("Domain", fontsize=18)
ax.set_ylabel("Body site", fontsize=18)
ax.set_title("Presence of microbial domains across human body sites", fontsize=24, pad=20)

ax.spines['right'].set_visible(True)
ax.spines['top'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

plt.tight_layout()
plt.show()