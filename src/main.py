import os
from geometry_loader import load_stl_geometry, resample_geometry
from pod_calculator import calculate_proof_of_design
from database_manager import add_file_to_database, update_similarity_matrix

def main():
    input_path = 'data/input_files/sample.stl'
    database_folder = 'data/database'
    target_points_count = 1000

    input_geometry = load_stl_geometry(input_path)
    resampled_geometry = resample_geometry(input_geometry, target_points_count)

    pod_score, _ = calculate_proof_of_design(resampled_geometry, database_folder, target_points_count)

    if pod_score >= 0.99:
        print("Design found in database. Minting skipped.")
    else:
        add_file_to_database(input_path, database_folder)
        print("New design added to the database.")

if __name__ == "__main__":
    main()
