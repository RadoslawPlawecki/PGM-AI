"""
@author: Radosław Pławecki
"""

import os
import configparser
import numpy as np
from project.matrix_clustering import MatrixClustering
from common.plot_formatting import use_latex

use_latex()

config = configparser.ConfigParser() 
config.read("config.ini") 

fcgr_path = config["files"]["fcgr_path"]

label_map = {"healthy": 0, "allergy": 1}

matrices = []
true_labels = []

dir_k_mer = "km6"
dir_path = os.path.join(fcgr_path, dir_k_mer)
for folder in os.listdir(dir_path):
    folder_path = os.path.join(dir_path, folder)
    if not os.path.isdir(folder_path):
        continue

    for file in os.listdir(folder_path):
        filepath = os.path.join(folder_path, file)
        matrix = np.loadtxt(filepath)
        matrices.append(matrix)
        true_labels.append(label_map[folder.lower()])


clustering = MatrixClustering(matrices, true_labels)

ari_scores = clustering.run_all(use_dbscan=False)
print(ari_scores)

clustering.plot_pca(color_by='true', title="PCA coloured by true labels")

labels_kmeans, ari_kmeans = clustering.results['KMeans']
clustering.plot_pca(labels=labels_kmeans, color_by='cluster', title=f"KMeans PCA (ARI={ari_kmeans:.2f})")
