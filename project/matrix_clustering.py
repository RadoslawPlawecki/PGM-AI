"""
@author: Radosław Pławecki
"""

import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

class MatrixClustering:
    """
    Class to perform clustering on patient matrices with multiple algorithms.
    Supports normalization, scaling, and ARI evaluation.
    """
    def __init__(self, matrices, true_labels):
        self.matrices = [np.atleast_2d(M) for M in matrices]  # ensure 2D
        self.true_labels = np.array(true_labels)
        self.patient_vectors = np.array([M.flatten() for M in self.matrices])
        self.results = {}
        self.scaler = None

    def scale_data(self):
        self.scaler = StandardScaler()
        self.patient_vectors = self.scaler.fit_transform(self.patient_vectors)

    def run_kmeans(self, n_clusters=2, random_state=42):
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
        labels = kmeans.fit_predict(self.patient_vectors)
        ari = adjusted_rand_score(self.true_labels, labels)
        self.results['KMeans'] = (labels, ari)
        return labels, ari

    def run_agglomerative(self, n_clusters=2, linkage='ward'):
        agglo = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        labels = agglo.fit_predict(self.patient_vectors)
        ari = adjusted_rand_score(self.true_labels, labels)
        self.results['Agglomerative'] = (labels, ari)
        return labels, ari

    def run_gmm(self, n_components=2, random_state=42, reg_covar=1e-4):
        if self.scaler is None:
            self.scale_data()
        gmm = GaussianMixture(
            n_components=n_components,
            random_state=random_state,
            reg_covar=reg_covar
        )
        labels = gmm.fit_predict(self.patient_vectors)
        ari = adjusted_rand_score(self.true_labels, labels)
        self.results['GMM'] = (labels, ari)
        return labels, ari

    def run_dbscan(self, eps=None, min_samples=2):
        if eps is None:
            eps = np.std(self.patient_vectors) + 12  # heuristic
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(self.patient_vectors)
        ari = adjusted_rand_score(self.true_labels, labels)
        self.results['DBSCAN'] = (labels, ari)
        return labels, ari

    def run_spectral(self, n_clusters=2, random_state=42):
        spectral = SpectralClustering(
            n_clusters=n_clusters,
            random_state=random_state,
            affinity='nearest_neighbors'
        )
        labels = spectral.fit_predict(self.patient_vectors)
        ari = adjusted_rand_score(self.true_labels, labels)
        self.results['Spectral'] = (labels, ari)
        return labels, ari

    def plot_pca(self, labels=None, color_by='true', title="PCA Plot"):
        pca = PCA(n_components=2)
        patient_pca = pca.fit_transform(self.patient_vectors)

        plt.figure(figsize=(8,6))

        if color_by == 'true' or labels is None:
            labels_to_plot = self.true_labels
            legend_labels = ['Healthy', 'Allergy']
        else:
            labels_to_plot = labels
            legend_labels = [f'Cluster {i}' for i in np.unique(labels)]

        for val, name in zip(np.unique(labels_to_plot), legend_labels):
            plt.scatter(
                patient_pca[labels_to_plot==val,0],
                patient_pca[labels_to_plot==val,1],
                s=100,
                label=name
            )

        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.title(title)
        plt.legend()
        plt.show()

    def run_all(self, use_dbscan=False):
        self.run_kmeans()
        self.run_agglomerative()
        self.run_gmm()
        self.run_spectral()
        if use_dbscan:
            self.run_dbscan()
        return {k: v[1] for k,v in self.results.items()}
