import os
import shutil
import pandas as pd
import torch
from geometry_loader import load_stl_geometry, resample_geometry
from similarity_metrics import calculate_similarity

def mint_new_file(input_stl_file_path, database_folder):
    """
    Mint a new STL file by copying it to the database.
    """
    shutil.copy(input_stl_file_path, os.path.join(database_folder, os.path.basename(input_stl_file_path)))
    print(f"New file '{os.path.basename(input_stl_file_path)}' added to the database.")

def update_similarity_matrix(new_file, database_folder, matrix_data, target_points_count):
    """
    Update the similarity matrix after adding a new file to the database.
    """
    new_row = {}
    new_geometry = load_stl_geometry(new_file)
    new_geometry_resampled = resample_geometry(new_geometry, target_points_count)
    new_tensor = torch.tensor(new_geometry_resampled, dtype=torch.float32)

    for existing_file in matrix_data.columns:
        existing_path = os.path.join(database_folder, existing_file)
        existing_geometry = load_stl_geometry(existing_path)
        existing_geometry_resampled = resample_geometry(existing_geometry, target_points_count)
        existing_tensor = torch.tensor(existing_geometry_resampled, dtype=torch.float32)

        similarity_score = calculate_similarity(new_tensor, existing_tensor)
        new_row[existing_file] = similarity_score

    new_row[new_file] = 1.0  # Self-similarity
    matrix_data = matrix_data.append(pd.Series(new_row, name=new_file))
    print("Updated Network Similarity Matrix:")
    print(matrix_data)
    return matrix_data
