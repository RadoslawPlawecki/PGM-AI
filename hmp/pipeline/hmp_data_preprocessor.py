"""
@author: Radosław Pławecki
"""

import pandas as pd
from pipeline import hmp_utils

class HMPDataPreprocessor:
    """
    Class to join `hmp_metadata.csv` with `abundance_matrix.csv` by `sample_id`
    and automatically preprocess microbiome abundance data.
    """
    def __init__(self, metadata_path, abundance_path, rank="genus", tol=1, save_csv=False, output_path="./hmp/data/hmp_microbiome.csv"):
        self.metadata = self._load_metadata(metadata_path)
        self.abundance = self._load_abundance(abundance_path)
        self.df_microbiome = self._merge()
        self.df_microbiome = hmp_utils.abundance_validator(self.df_microbiome, tol=tol)
        self._rename_taxonomy_cols(rank)
        self._collapse_duplicated_taxa()
        self._compute_body_site_means()
        if save_csv:
            self._save_csv(output_path)

    def _load_metadata(self, path):
        """Load samples data."""
        return pd.read_csv(path, usecols=["sample_id","body_site"])

    def _load_abundance(self, path):
        """Load abundance data."""
        df = pd.read_csv(path, index_col=0)
        return df.T.rename_axis("sample_id").reset_index()

    def _merge(self):
        """Merge on `sample_id`."""
        return self.metadata.merge(self.abundance, on="sample_id")

    def _save_csv(self, path):
        "Save new DataFrame to a CS file."""
        self.df_microbiome.to_csv(path, sep=";", index=False)
        
    def get_df_microbiome(self):
        """Get data for display."""
        return self.df_microbiome

    def _rename_taxonomy_cols(self, rank="genus", start_col=2):
        """Rename taxonomy columns in the DataFrame using a selected taxonomic rank."""
        cols = list(self.df_microbiome.columns)
        for i in range(start_col, len(cols)):
            tax_dict = hmp_utils.parse_taxonomy(cols[i])
            cols[i] = tax_dict.get(rank, cols[i])
        self.df_microbiome.columns = cols
        print(f"[INFO] Taxonomy columns renamed to {rank} level.")

    def _collapse_duplicated_taxa(self, start_col=2):
        """
        Collapse duplicate taxa columns by summing their abundances.
        """
        meta_cols = self.df_microbiome.columns[:start_col]
        df_tax = self.df_microbiome.iloc[:, start_col:]
        df_tax = df_tax.T.groupby(level=0).sum().T
        self.df_microbiome = pd.concat([self.df_microbiome.loc[:, meta_cols], df_tax], axis=1)
        print("[INFO] Duplicate taxa columns collapsed.")

    def _compute_body_site_means(self, start_col=2):
        """
        Compute mean abundance of each taxon for each body site.
        """
        taxa_cols = self.df_microbiome.columns[start_col:]
        self.df_microbiome = (self.df_microbiome.groupby("body_site")[taxa_cols].mean().reset_index())
        print("[INFO] Mean abundances by body site computed.")
