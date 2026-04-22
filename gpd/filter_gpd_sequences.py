"""
@author: Radosław Pławecki
"""

from Bio import SeqIO
import pandas as pd
from tqdm import tqdm
import os

out_dir = "gpd/data/seq/raw/"
gpd_metadata = "gpd/data/03_gpd_taxa_split.csv"
gpd_sequences = "gpd/data/01b_GPD_sequences.fa"

gpd_ids = set(pd.read_csv(gpd_metadata, delimiter=';', usecols=['GPD_id'])['GPD_id'])

if not os.path.isdir(out_dir):
    os.makedirs("data/genome/chr/", exist_ok=True)

for record in tqdm(SeqIO.parse(gpd_sequences, "fasta")):
    if record.id in gpd_ids:
        with open(os.path.join(out_dir, f"{record.id}.txt"), 'w') as f:
            f.write(str(record.seq).upper())
