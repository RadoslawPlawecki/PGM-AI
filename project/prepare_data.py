"""
@author: Radosław Pławecki
"""

import os
import configparser
from tqdm import tqdm

config = configparser.ConfigParser()
config.read("config.ini")

raw_path = config["files"]["raw_path"]
preprocessed_path = config["files"]["preprocessed_path"]

print("--- PROGRAM STARTED ---")
for file in os.listdir(raw_path):
    print(f"[INFO] Processing file {file}...")
    if not file.endswith(".fa"):  
        continue

    dir_name = f"P{file[1:3]}"
    dir_path = os.path.join(preprocessed_path, dir_name)
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(raw_path, file)
    with open(file_path, "r") as f:
        lines = f.readlines()

        for i in tqdm(range(0, len(lines), 2)):
            header = lines[i].strip()
            seq = lines[i + 1].strip()
            contig_id = header[1:].split()[0]  # ID bez '>'
            
            out_path = os.path.join(dir_path, f"{dir_name}_{contig_id}.txt")
            with open(out_path, "w") as out:
                out.write(seq)

print("--- PROGRAM FINISHED ---")
