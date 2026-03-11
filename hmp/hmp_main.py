"""
@author: Radosław Pławecki
"""

from pipeline.hmp_data_preprocessor import HMPDataPreprocessor

print("[1] Preprocessing HMP data...")
metadata_path, abundance_path = "./hmp/data/hmp_metadata.csv", "./hmp/data/abundance_matrix.csv"
try:
    pd_hmp = HMPDataPreprocessor(metadata_path=metadata_path, abundance_path=abundance_path)
    df_microbiome = pd_hmp.get_df_microbiome()
    print(f"[INFO] ✔ Success! {len(df_microbiome)} rows loaded.")
    
    is_close = df_microbiome.iloc[:, 2:].sum(axis=1) - 100 < 1.E-5

    # Rows where the sum is NOT close to 100
    rows_false = df_microbiome[~is_close]

    print(rows_false)
except Exception as e:
        print(f"✖ Failed ({e})")
