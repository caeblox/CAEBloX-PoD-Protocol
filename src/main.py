# src/main.py

from pod_calculator import calculate_pod_for_new_file
from database_manager import mint_new_file, update_similarity_matrix, build_initial_similarity_matrix
from geometry_loader import resample_geometry
from file_converter import read_geometry
from similarity_metrics import calculate_network_similarity_score
import pandas as pd
import os
from datetime import datetime

# Set folder paths and target points
new_cad_folder_path = './data/new_cad'
database_folder_path = './data/database'
target_points_count = 1000

try:
    # Initialize Network_state.txt to log network state after each minting process
    with open("Network_state.txt", "w") as report_file:
        report_file.write("Network State Report\n")
        report_file.write("====================\n\n")

        # Build initial similarity matrix from existing files in the database
        similarity_matrix = build_initial_similarity_matrix(database_folder_path, target_points_count)

        # Calculate initial network similarity score
        initial_network_score = calculate_network_similarity_score(similarity_matrix)
        report_file.write(f"Initial Network Similarity Score (Excluding Self-Similarity): {initial_network_score:.4f}\n")
        report_file.write(f"Initial Network Similarity Matrix:\n{similarity_matrix}\n\n")

        # Loop over each file in the new_cad folder
        for file_name in os.listdir(new_cad_folder_path):
            input_file_path = os.path.join(new_cad_folder_path, file_name)
            
            # Load and resample input geometry
            input_geometry, _ = read_geometry(input_file_path)  # Only use input_file_path here
            input_geometry_resampled = resample_geometry(input_geometry, target_points_count)

            # Calculate Proof of Design (PoD) score for the new file
            pod_score, similarity_scores = calculate_pod_for_new_file(input_geometry_resampled, database_folder_path, target_points_count)
            report_file.write(f"\nProcessing file: {file_name}\n")
            report_file.write(f"Minting Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_file.write(f"PoD Similarity Score: {pod_score:.4f}\n")
            
            # Skip if PoD score >= 0.99 (indicating the file is already similar to one in the database)
            if pod_score >= 0.99:
                report_file.write(f"File '{file_name}' found in network. Skipping.\n")
                continue
            else:
                # File is unique, proceed with minting
                report_file.write(f"File '{file_name}' is unique. Proceeding with minting.")
                
                # Mint new file by copying it to the database folder
                mint_new_file(input_file_path, database_folder_path)

                # Pass only the filename (not the full path) to update_similarity_matrix
                similarity_matrix = update_similarity_matrix(file_name, database_folder_path, similarity_matrix, target_points_count)
                
                # Calculate and display network similarity scores before and after minting
                updated_network_score = calculate_network_similarity_score(similarity_matrix)
                report_file.write(f"Network Similarity Score (Before Minting): {initial_network_score:.4f}\n")
                report_file.write(f"Network Similarity Score (After Minting): {updated_network_score:.4f}\n")

                # Determine if the new file "rewards" the network and write details
                score_difference = initial_network_score - updated_network_score
                if score_difference > 0:
                    report_file.write("Network Reward: The new CAD file rewards the network.\n")
                else:
                    report_file.write("Network Reward: The new CAD file does not reward the network.\n")

                # Record similarity scores of the new CAD file with existing files
                report_file.write("Similarity Scores for the New CAD File:\n")
                for db_file, score in similarity_matrix[file_name].items():
                    report_file.write(f"  {db_file}: {score:.4f}\n")

                report_file.write("\nUpdated Similarity Matrix:\n")
                report_file.write(f"{similarity_matrix}\n\n")

                # Update initial network score for the next file in the loop
                initial_network_score = updated_network_score

except Exception as e:
    print(f"An unexpected error occurred: {e}")
