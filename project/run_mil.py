"""
@author: Radosław Pławecki
"""

import os
import configparser
import torch
import ast
import random
import numpy as np
from project.MILModel import MILModelK5

config = configparser.ConfigParser()
config.read("config.ini")
preprocessed_path = config["files"]["preprocessed_path"]

fcgr_path = config["files"]["fcgr_path"]

seed = 42
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

input_dim = 16*16
hidden_dim = 128

def get_bag_from_matrix(patient_path):
    print(f"  → Creating BAGs for a patient: {os.path.basename(patient_path)}")
    bag_vectors = []
    files = os.listdir(patient_path)
    for file in files:
        matrix_path = os.path.join(patient_path, file)
        matrix = np.load(matrix_path) 
        vector = torch.tensor(matrix.flatten(), dtype=torch.float32)
        bag_vectors.append(vector)
    if len(bag_vectors) == 0:
        return None
    bag_tensor = torch.stack(bag_vectors)
    bag_tensor = (bag_tensor - bag_tensor.mean(dim=1, keepdim=True)) / \
                 (bag_tensor.std(dim=1, keepdim=True) + 1e-8)
    return bag_tensor

directories = os.listdir(preprocessed_path)
predictions = {}

print(f"Starting LOOCV for {len(directories)} patients...\n")

for i, test_patient in enumerate(directories, start=1):
    print(f"[{i}/{len(directories)}] Test patient processing: {test_patient}")
    
    test_path = os.path.join(fcgr_path, "4-mer", test_patient)
    test_bag = get_bag_from_matrix(test_path)
    if test_bag is None:
        print("  → No contigs, patient skipped")
        continue

    train_bags = []
    print("  → Creating training BAGs...")
    for patient in directories:
        if patient == test_patient:
            continue
        bag = get_bag_from_matrix(os.path.join(fcgr_path, "4-mer", patient))
        if bag is not None:
            train_bags.append(bag)

    print("  → MIL model initialization...")
    model = MILModelK5(input_dim=input_dim, hidden_dim=hidden_dim)
    model.eval()  

    print("  → Prediction for a test patient...")
    with torch.no_grad():
        pred, attention = model(test_bag)

    predictions[test_patient] = {
        "prediction": pred.item(),
        "attention": attention.squeeze().numpy()
    }
    print("  → Done!\n")

print("\nAll predictions finished. Results:")
for patient, result in predictions.items():
    print(f"Patient: {patient}")
    print("Prediction (0-1):", result["prediction"])
    print("Attention:", result["attention"])
    print("-"*50)