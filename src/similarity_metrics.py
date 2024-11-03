import numpy as np
import torch
from sklearn.neighbors import NearestNeighbors

def calculate_sdf_similarity(tensor1, tensor2, neighbors=10):
    """
    Calculates similarity between two tensors representing point clouds 
    using a nearest-neighbor SDF approach.

    Parameters:
        tensor1, tensor2 (torch.Tensor): Point clouds.
        neighbors (int): Number of neighbors for similarity calculation.
    
    Returns:
        float: Similarity score.
    """
    points1, points2 = tensor1.cpu().numpy(), tensor2.cpu().numpy()
    nn1 = NearestNeighbors(n_neighbors=neighbors).fit(points1)
    nn2 = NearestNeighbors(n_neighbors=neighbors).fit(points2)

    distances_1to2, _ = nn1.kneighbors(points2, return_distance=True)
    distances_2to1, _ = nn2.kneighbors(points1, return_distance=True)

    avg_distance = (distances_1to2.mean() + distances_2to1.mean()) / 2.0
    return 1.0 / (1.0 + avg_distance + 1e-8)
