import torch
import numpy as np
from sklearn.neighbors import NearestNeighbors

def sign_distance_function(tensor1, tensor2, n_neighbors=10):
    """
    Calculate similarity based on a nearest neighbors approach in the SDF space.
    """
    points1 = tensor1.cpu().numpy()
    points2 = tensor2.cpu().numpy()

    nn1 = NearestNeighbors(n_neighbors=n_neighbors).fit(points1)
    nn2 = NearestNeighbors(n_neighbors=n_neighbors).fit(points2)

    distances_1to2, _ = nn1.kneighbors(points2, return_distance=True)
    distances_2to1, _ = nn2.kneighbors(points1, return_distance=True)

    sdf_distance = (distances_1to2.mean() + distances_2to1.mean()) / 2.0
    epsilon = 1e-8
    similarity_score = 1.0 / (1.0 + sdf_distance + epsilon)
    
    return similarity_score

def calculate_similarity(tensor1, tensor2):
    """
    Calculate similarity using the sign distance function.
    """
    return sign_distance_function(tensor1, tensor2)

def calculate_network_similarity_score(matrix_data):
    """
    Calculate the average similarity score of the network.
    """
    return matrix_data.stack().mean()
