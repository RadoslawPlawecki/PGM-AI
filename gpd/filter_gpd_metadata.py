"""
@author: Radosław Pławecki
"""

import pandas as pd

gpd_file = "gpd/data/01a_GPD_metadata.tsv"
gpd_df = pd.read_csv(gpd_file, delimiter='\t')

# 1. Keep only viral regions (checkV_viral_region not NA)
gpd_df = gpd_df[gpd_df['checkV_viral_region'].notna()]

# 2. Exclude prophages 
gpd_df = gpd_df[gpd_df['checkV_prophage'] == 'No']

# 3. Minimum contig length 
gpd_df = gpd_df[gpd_df['Size'] >= 1000]

# 4. Filter by CheckV completeness if desired (e.g., >= 50%)
gpd_df = gpd_df[gpd_df['checkV_completion'] >= 50]

# 5. Filter only sequences with host info for host prediction
gpd_df = gpd_df[gpd_df['Host_range_taxon'].notna()]

# 6. Select columns to export
columns_to_export = [
    "GPD_id",
    "GPD_VC",
    "Source",
    "Size",
    "Host_range_taxon",
    "checkV_viral_region",
]

export_df = gpd_df[columns_to_export]
export_df.to_csv("gpd/data/02_gpd_filtered.csv", sep=';', index=False)
