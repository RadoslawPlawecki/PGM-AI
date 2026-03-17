"""
@author: Radosław Pławecki
"""

import os
import configparser
from tqdm import tqdm
import numpy as np
from project.FCGR import FCGR

config = configparser.ConfigParser()
config.read("config.ini")

preprocessed_path = config["files"]["preprocessed_path"]
fcgr_path = config["files"]["fcgr_path"]

k_mers = [4, 5, 6]

print("--- PROGRAM STARTED ---")
directories = os.listdir(preprocessed_path)
for directory in directories:
    directory_path = os.path.join(preprocessed_path, directory)

    files = os.listdir(directory_path)
    for file in tqdm(files):

        contig_path = os.path.join(directory_path, file)
        with open(contig_path, "r") as f:
            sequence = f.read().replace("\n", "").strip()

            for k_mer in k_mers:
                matrix = FCGR(sequence=sequence, k_mer=k_mer).fill_matrix()
                out_path = os.path.join(fcgr_path, f"{k_mer}-mer", directory)

                os.makedirs(out_path, exist_ok=True)
                out_path = os.path.join(out_path, f"{os.path.splitext(file)[0]}_FCGR.npy")
                np.save(out_path, matrix)
print("--- PROGRAM FINISHED ---")
