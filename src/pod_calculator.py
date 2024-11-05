import os
import torch
import numpy as np
from geometry_loader import load_stl_geometry, resample_geometry
from similarity_metrics import calculate_similarity

def calculate_pod_for_new_file(input_geometry, database_folder, target_points_count):
    """
    Calculate Proof of Design (PoD) score for a new STL file.
    """
    stl_files = [f for f in os.listdir(database_folder) if f.endswith(".stl")]
    similarity_scores = []

    input_tensor = torch.tensor(input_geometry, dtype=torch.float32)

    for file in stl_files:
        path = os.path.join(database_folder, file)
        geometry = load_stl_geometry(path)
        geometry_resampled = resample_geometry(geometry, target_points_count)
        ref_tensor = torch.tensor(geometry_resampled, dtype=torch.float32)

        similarity_score = calculate_similarity(input_tensor, ref_tensor)
        similarity_scores.append(similarity_score)

        if similarity_score >= 0.99:
            print(f"File '{file}' is highly similar to the input file. Process stopped.")
            return 1.0, similarity_scores

    avg_pod_score = np.mean(similarity_scores)
    return avg_pod_score, similarity_scores
