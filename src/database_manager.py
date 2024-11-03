import shutil
import pandas as pd
from geometry_loader import load_stl_geometry, resample_geometry
from similarity_metrics import calculate_sdf_similarity

def add_file_to_database(input_file_path, database_folder):
    """
    Adds a new STL file to the database.
    
    Parameters:
        input_file_path (str): Path to the STL file.
        database_folder (str): Path to the database folder.
    """
    shutil.copy(input_file_path, database_folder)
    print(f"File added to the database: {input_file_path}")

def update_similarity_matrix(new_file, database_folder, similarity_matrix, target_count):
    """
    Updates the similarity matrix after adding a new file to the database.

    Parameters:
        new_file (str): Path to the new STL file.
        database_folder (str): Path to the database folder.
        similarity_matrix (pd.DataFrame): Existing similarity matrix.
        target_count (int): Target point count for resampling.

    Returns:
        pd.DataFrame: Updated similarity matrix.
    """
    new_geometry = load_stl_geometry(new_file)
    new_geometry_resampled = resample_geometry(new_geometry, target_count)
    new_tensor = torch.tensor(new_geometry_resampled, dtype=torch.float32)

    new_row = {}
    for existing_file in similarity_matrix.columns:
        existing_geometry = load_stl_geometry(existing_file)
        existing_resampled = resample_geometry(existing_geometry, target_count)
        existing_tensor = torch.tensor(existing_resampled, dtype=torch.float32)

        score = calculate_sdf_similarity(new_tensor, existing_tensor)
        new_row[existing_file] = score

    similarity_matrix = similarity_matrix.append(new_row, ignore_index=True)
    return similarity_matrix
