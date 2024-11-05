from pod_calculator import calculate_pod_for_new_file
from database_manager import mint_new_file, update_similarity_matrix
from geometry_loader import resample_geometry
from file_converter import read_geometry
from similarity_metrics import calculate_network_similarity_score
import pandas as pd

input_stl_file_path = './data/new_cad/airfoil.vtk'
database_folder_path = './data/database'
target_points_count = 1000

try:
    similarity_matrix = pd.DataFrame()

    # Load geometry from either STL or VTK and get STL path
    input_geometry, stl_file_path = read_geometry(input_stl_file_path)
    input_geometry_resampled = resample_geometry(input_geometry, target_points_count)

    # Calculate initial network similarity score
    initial_network_score = calculate_network_similarity_score(similarity_matrix)

    # Calculate PoD score for the new file
    pod_score, _ = calculate_pod_for_new_file(input_geometry_resampled, database_folder_path, target_points_count)
    
    # Mint the file if PoD is unique
    if pod_score >= 0.99:
        print("File found in network. Process stopped.")
    else:
        print("File PoD score is unique. Proceeding with minting.")
        mint_new_file(stl_file_path, database_folder_path)

        updated_matrix = update_similarity_matrix(stl_file_path, database_folder_path, similarity_matrix, target_points_count)
        updated_network_score = calculate_network_similarity_score(updated_matrix)

        # Display network similarity scores
        print(f"Network Similarity Score (Before Minting): {initial_network_score:.4f}")
        print(f"Network Similarity Score (After Minting): {updated_network_score:.4f}")

        score_difference = updated_network_score - initial_network_score
        if score_difference <= 0.99:
            print("The incoming CAD file is new to the network.")
        else:
            print("The incoming CAD file is found to be similar to an existing CAD in the network.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
