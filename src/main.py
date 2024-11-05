# src/main.py

from pod_calculator import calculate_pod_for_new_file
from database_manager import mint_new_file, update_similarity_matrix, build_initial_similarity_matrix
from geometry_loader import resample_geometry
from file_converter import read_geometry
from similarity_metrics import calculate_network_similarity_score
import pandas as pd
import os

# Set folder paths and target points
new_cad_folder_path = './data/new_cad'
database_folder_path = './data/database'
target_points_count = 1000

try:
    # Build initial similarity matrix from existing files in the database
    similarity_matrix = build_initial_similarity_matrix(database_folder_path, target_points_count)

    # Calculate initial network similarity score
    initial_network_score = calculate_network_similarity_score(similarity_matrix)
    print("\nInitial Network Similarity Matrix:")
    print(similarity_matrix)

    # Loop over each file in the new_cad folder
    for file_name in os.listdir(new_cad_folder_path):
        input_file_path = os.path.join(new_cad_folder_path, file_name)
        
        # Load and resample input geometry
        input_geometry, stl_file_path = read_geometry(input_file_path)
        input_geometry_resampled = resample_geometry(input_geometry, target_points_count)

        # Calculate Proof of Design (PoD) score for the new file
        pod_score, _ = calculate_pod_for_new_file(input_geometry_resampled, database_folder_path, target_points_count)
        print(f"\nProcessing file: {file_name}")
        print(f"PoD Similarity Score: {pod_score:.4f}")
        
        # Skip if PoD score >= 0.99 (indicating the file is already similar to one in the database)
        if pod_score >= 0.99:
            print(f"File '{file_name}' found in network. Skipping.")
            continue
        else:
            # File is unique, proceed with minting
            print(f"File '{file_name}' is unique. Proceeding with minting.")
            mint_new_file(stl_file_path, database_folder_path)

            # Update the similarity matrix with the new file and print the matrix
            similarity_matrix = update_similarity_matrix(stl_file_path, database_folder_path, similarity_matrix, target_points_count)
            
            # Display the updated similarity matrix
            print("\nUpdated Similarity Matrix After Minting:")
            print(similarity_matrix)

            # Calculate and display network similarity scores before and after minting
            updated_network_score = calculate_network_similarity_score(similarity_matrix)
            print(f"Network Similarity Score (Before Minting): {initial_network_score:.4f}")
            print(f"Network Similarity Score (After Minting): {updated_network_score:.4f}")

            # Determine if the incoming CAD file is unique
            score_difference = initial_network_score - updated_network_score
            if score_difference > 0:
                print("The incoming CAD will reward the network.")
            else:
                print("The incoming CAD file will not reward the network.")

            # Update initial network score for the next file in the loop
            initial_network_score = updated_network_score

except Exception as e:
    print(f"An unexpected error occurred: {e}")
