"""
@author: Radosław Pławecki
"""

import os
import csv
import configparser


class ContigsProcessor:
    def __init__(self, config_path="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.raw_path = self.config["files"]["raw_path"]
        self.sequences_path = self.config["files"]["sequences_path"]

        os.makedirs(self.sequences_path, exist_ok=True)

        self.report = []

    def process_all(self):
        print("--- PROGRAM STARTED ---")

        for file in os.listdir(self.raw_path):
            print(f"[INFO] Processing file {file}...")

            if not file.endswith(".fa"):
                print(f"[SKIP] Not a FASTA file: {file}")
                continue

            self.process_file(file)

        self.save_report()
        print("--- PROGRAM FINISHED ---")

    def process_file(self, file):
        dir_name = f"P{file[1:3]}"
        file_path = os.path.join(self.raw_path, file)
        out_path = os.path.join(self.sequences_path, f"{dir_name}_S.txt")

        seq = ""
        seq_count = 0
        total_length = 0

        with open(file_path, "r") as f, open(out_path, "w") as out:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                if not line:
                    continue

                if line.startswith(">"):
                    if seq:
                        if len(seq) >= 100:
                            out.write(seq)
                            seq_count += 1
                            total_length += len(seq)
                        else:
                            print(f"[WARNING] Short sequence skipped ({len(seq)} bp) in {file}")
                        seq = ""
                else:
                    if not all(c in "ACGTNacgtn" for c in line):
                        print(f"[WARNING] Invalid characters at line {line_num} in {file}")
                    
                    seq += line

            if seq:
                if len(seq) >= 100:
                    out.write(seq)
                    seq_count += 1
                    total_length += len(seq)

        print(f"[DONE] {file}: {seq_count} sequences merged → {out_path}")

        self.report.append({
            "file_id": dir_name,
            "source_file": file,
            "sequence_count": seq_count,
            "total_length": total_length
        })

    def save_report(self):
        csv_path = os.path.join(self.sequences_path, "merging_report.csv")

        with open(csv_path, "w", newline="") as csvfile:
            fieldnames = ["file_id", "source_file", "sequence_count", "total_length"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()
            writer.writerows(self.report)

        print(f"[REPORT] CSV saved → {csv_path}")


if __name__ == "__main__":
    processor = ContigsProcessor()
    processor.process_all()
