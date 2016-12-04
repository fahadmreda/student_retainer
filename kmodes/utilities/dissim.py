# Some dissimilarity measures for clustering
# Tim Burt
# CS5593 project

import numpy as np


def matching_dissim(a, b):
    """Simple matching dissimilarity function"""
    return np.sum(a != b, axis=1)


def euclidean_dissim(a, b):
    """Euclidean distance dissimilarity function"""
    if np.isnan(a).any() or np.isnan(b).any():
        raise ValueError("Missing values detected in numerical columns.")
    return np.sum((a - b) ** 2, axis=1)
