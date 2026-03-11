"""
@author: Radosław Pławecki
"""

from pipeline.hmp_data_preprocessor import HMPDataPreprocessor

metadata_path, abundance_path = "./hmp/data/hmp_metadata.csv", "./hmp/data/abundance_matrix.csv"
try:
    pd_hmp = HMPDataPreprocessor(metadata_path=metadata_path, abundance_path=abundance_path, rank="genus", save_csv=True)
    df_microbiome = pd_hmp.get_df_microbiome()
except Exception as e:
        print(f"✖ Failed ({e})")
