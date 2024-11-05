# src/similarity_metrics.py

import torch
import numpy as np
from sklearn.neighbors import NearestNeighbors

def calculate_similarity(tensor1, tensor2, n_neighbors=10):
    """
    Calculate similarity between two tensors based on a nearest neighbors approach.
    Returns 1.0 if tensor1 and tensor2 are identical (self-similarity).
    """
    if torch.equal(tensor1, tensor2):
        return 1.0  # Return 1.0 for identical files to ensure perfect self-similarity

    # Convert tensors to numpy arrays
    points1 = tensor1.cpu().numpy()
    points2 = tensor2.cpu().numpy()

    # Fit nearest neighbors
    nn1 = NearestNeighbors(n_neighbors=n_neighbors).fit(points1)
    nn2 = NearestNeighbors(n_neighbors=n_neighbors).fit(points2)

    # Calculate distances for both directions
    distances_1to2, _ = nn1.kneighbors(points2, return_distance=True)
    distances_2to1, _ = nn2.kneighbors(points1, return_distance=True)

    sdf_distance = (distances_1to2.mean() + distances_2to1.mean()) / 2.0
    epsilon = 1e-8  # Avoid division by zero
    similarity_score = 1.0 / (1.0 + sdf_distance + epsilon)
    
    return similarity_score

def calculate_network_similarity_score(matrix_data):
    """
    Calculate the average similarity score across the entire network, excluding self-similarity scores (1.0).
    """
    # Exclude diagonal (self-similarity) values from calculation
    matrix_no_self_similarity = matrix_data.where(matrix_data != 1.0)
    mean_similarity_score = matrix_no_self_similarity.stack().mean()
    
    return mean_similarity_score
