"""
@author: Radosław Pławecki
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common.plot_formatting import use_latex

use_latex()

data_path = "hmp/data/"
files = ["hmp_microbiome_p.csv", "hmp_microbiome_k.csv"]

# STACKED BAR CHART | KINGDOMS ABUNDANCE
"""df_k = pd.read_csv(os.path.join(data_path, files[1]), delimiter=';')

df_total = df_k[['Archaea', 'Bacteria', 'Eukaryota']].sum(axis=1)
df_percent = df_k[['Archaea', 'Bacteria', 'Eukaryota']].div(df_total, axis=0) * 100

categories = ['Archaea', 'Bacteria', 'Eukaryota']
colors = ['#002914', '#356920', '#009939']

bottom = np.zeros(len(df_k))
x_positions = np.arange(len(df_k))

plt.figure(figsize=(16,10))
for i, cat in enumerate(categories):
    plt.bar(x_positions, df_percent[cat], bottom=bottom, color=colors[i], label=cat)
    bottom += df_percent[cat]

manual_labels = ['Nasal cavity', 'Oral cavity', 'Skin', 'Stool', 'Vagina'] 
plt.xticks(x_positions, manual_labels, fontsize=16)
plt.yticks(fontsize=16)

plt.ylabel('Relative abundance (%)', fontsize=16)
plt.title('Composition of microbial population', fontsize=20, pad=20)
plt.legend(title='Components', fontsize=16, title_fontsize=18)
plt.ylim(0, 100)
plt.tight_layout()
# plt.savefig("hmp/plots/01_microbiota_abundance.pdf", format="pdf")
plt.show()"""

# BAR CHART | TOP 10 PHYLA IN STOOL
row_index = 3

df_g = pd.read_csv(os.path.join(data_path, files[0]), delimiter=';', skiprows=lambda x: x != row_index + 1 and x != 0).T
df_g.columns = ['value']
df_g['value'] = pd.to_numeric(df_g['value'], errors='coerce')
top10 = df_g['value'].nlargest(5)

fig, ax = plt.subplots(figsize=(16,10))
plt.bar(top10.index, top10.values, color='#356920')

plt.xlabel("Phylum", fontsize=18, labelpad=15)
plt.ylabel("Relative Abundance (\%)", fontsize=18, labelpad=15)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.title("Most abundant phyla in the gut microbiota", fontsize=20, pad=20)
plt.tight_layout()

# plt.savefig("hmp/plots/02_phylum_gut_micr.pdf", format="pdf")
# plt.show()
