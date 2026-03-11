"""
@author: Radosław Pławecki
"""

import pandas as pd

class HMPDataPreprocessor:
    """
    Class to join `hmp_metadata.csv` with `abundance_matrix.csv` by `sample_id`.
    """
    def __init__(self, metadata_path, abundance_path, save_csv=False, output_path="./hmp/data/hmp_microbiome.csv"):
        self.metadata = self._load_metadata(metadata_path)
        self.abundance = self._load_abundance(abundance_path)
        self.df_microbiome = self._merge()
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
