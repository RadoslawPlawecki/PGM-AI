"""
@author: Radosław Pławecki
"""


from project.FCGR import FCGR
import configparser
import os
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from common.plot_formatting import use_latex

use_latex()

config = configparser.ConfigParser() 
config.read("config.ini") 

sequences_path = config["files"]["sequences_path"]
fcgr_path = config["files"]["fcgr_path"]

files = [f for f in os.listdir(sequences_path) if f.endswith(".txt")]

k_mers = [10]

print("--- PROGRAM STARTED ---")
for k_mer in k_mers:
    plot_dir = os.path.join("plots", "fcgr", f"km{k_mer}")
    os.makedirs(plot_dir, exist_ok=True)

    matrix_dir = os.path.join(fcgr_path, f"km{k_mer}")
    os.makedirs(matrix_dir, exist_ok=True)

    for file in tqdm(files):
        print(f"[INFO] Processing file {file}...")
        input_path = os.path.join(sequences_path, file)
        
        with open(input_path, "r") as f:
            seq = f.read().replace("\n", "")  

        fcgr = FCGR(sequence=seq, k_mer=k_mer)
        matrix = fcgr.fill_matrix()
        matrix_array = np.array(matrix, dtype=np.float32)

        name, _ = os.path.splitext(file)
        matrix_txt_path = os.path.join(matrix_dir, f"{name}_M.txt")
        np.savetxt(matrix_txt_path, matrix_array, fmt="%.6f")

        plot_path = os.path.join(plot_dir, f"{name}.pdf")
        plt.figure(figsize=(6, 6))
        plt.imshow(matrix_array, cmap="gray")
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(plot_path, format="pdf")
        plt.close()

        print(f"[DONE] {file} (k={k_mer}) → matrix: {matrix_txt_path}, plot: {plot_path}")
