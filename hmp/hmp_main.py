"""
@author: Radosław Pławecki
"""

from pipeline.data_preprocessor import HMPDataPreprocessor

metadata_path, abundance_path = "./hmp/data/hmp_metadata.csv", "./hmp/data/abundance_matrix.csv"
try:
    pd_hmp = HMPDataPreprocessor(metadata_path=metadata_path, abundance_path=abundance_path, rank="phylum", save_csv=True, output_path="./hmp/data/hmp_microbiome_p.csv")
    df_microbiome = pd_hmp.get_df_microbiome()
except Exception as e:
        print(f"✖ Failed ({e})")
