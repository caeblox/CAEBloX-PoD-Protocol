import os
import torch
from similarity_metrics import calculate_sdf_similarity
from geometry_loader import load_stl_geometry, resample_geometry

def calculate_proof_of_design(input_geometry, database_folder, target_count):
    """
    Calculates the PoD score by comparing input geometry to database geometries.
    
    Parameters:
        input_geometry (np.ndarray): Input geometry points.
        database_folder (str): Path to the database folder.
        target_count (int): Target point count for resampling.

    Returns:
        float, list: Average PoD score, list of individual scores.
    """
    stl_files = [f for f in os.listdir(database_folder) if f.endswith(".stl")]
    input_tensor = torch.tensor(input_geometry, dtype=torch.float32)
    scores = []

    for file in stl_files:
        path = os.path.join(database_folder, file)
        geometry = load_stl_geometry(path)
        resampled_geometry = resample_geometry(geometry, target_count)
        ref_tensor = torch.tensor(resampled_geometry, dtype=torch.float32)

        score = calculate_sdf_similarity(input_tensor, ref_tensor)
        scores.append(score)

        if score >= 0.99:
            print(f"File '{file}' is highly similar. Process stopped.")
            return 1.0, scores

    avg_score = sum(scores) / len(scores)
    print(f"Average PoD Score: {avg_score:.4f}")
    return avg_score, scores
