# src/database_manager.py

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

def build_initial_similarity_matrix(database_folder, target_points_count):
    """
    Build the initial similarity matrix from existing CAD files in the database.
    """
    stl_files = [f for f in os.listdir(database_folder) if f.endswith(".stl")]
    matrix_data = pd.DataFrame(index=stl_files, columns=stl_files)

    for i, file1 in enumerate(stl_files):
        path1 = os.path.join(database_folder, file1)
        geometry1 = load_stl_geometry(path1)
        geometry1_resampled = resample_geometry(geometry1, target_points_count)
        tensor1 = torch.tensor(geometry1_resampled, dtype=torch.float32)

        for j, file2 in enumerate(stl_files[i:], i):  # Only calculate the upper triangular matrix
            path2 = os.path.join(database_folder, file2)
            geometry2 = load_stl_geometry(path2)
            geometry2_resampled = resample_geometry(geometry2, target_points_count)
            tensor2 = torch.tensor(geometry2_resampled, dtype=torch.float32)

            similarity_score = calculate_similarity(tensor1, tensor2)
            matrix_data.at[file1, file2] = similarity_score
            matrix_data.at[file2, file1] = similarity_score  # Mirror the score for symmetry

    return matrix_data

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
    new_row_series = pd.Series(new_row, name=new_file)
    matrix_data = pd.concat([matrix_data, new_row_series.to_frame().T], axis=0)
    matrix_data[new_file] = new_row_series  # Add as a new column to maintain matrix symmetry

    print("Updated Network Similarity Matrix:")
    print(matrix_data)
    return matrix_data
