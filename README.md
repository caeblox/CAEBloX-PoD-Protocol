# CAEBloX PoD Protocol

## Overview
The Similarity-Analyzer is an advanced geometry similarity scoring system built to support the minting process for CAEBlox, a platform focused on verifying 3D geometries Similarity. This tool automates the evaluation of 3D STL files, leveraging Signed Distance Function (SDF) to deliver highly accurate similarity scoring between Network designs.
**STL-Similarity-Analyzer** is a Python tool designed for comparing 3D geometries within STL files. It leverages Signed Distance Function (SDF) and nearest-neighbors techniques to compute similarity scores, assess Proof of Design (PoD) compliance, and manage a database of unique STL designs.




## Features
- **STL Geometry Processing**: Load and normalize point clouds from STL files.
- **Similarity Computation**: Calculate similarity scores using nearest-neighbor SDF.
- **Proof of Design (PoD)**: Compare new STL files against existing designs in the database.
- **Database Management**: Add unique STL files to the database and update similarity metrics.

## Setup
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt

README.txt

# STL-Similarity-Analyzer

## Overview

**STL-Similarity-Analyzer** is a Python-based tool for assessing geometric similarity between 3D CAD files, specifically in STL and VTK formats. The system uses Signed Distance Functions (SDF) with nearest-neighbor approaches to evaluate similarity between CAD files, supporting a Proof of Design (PoD) scoring system. This tool helps identify unique designs and prevents redundant CAD files from being added to the network.

The tool processes all files in the `new_cad` folder, checks their similarity to the existing CAD files in the `database`, and only adds unique files to the database.

---

## Directory Structure

├── src/ │ ├── main.py # Main script to run the analyzer │ ├── geometry_loader.py # Module for loading STL geometry │ ├── similarity_metrics.py # Module for similarity calculations │ ├── database_manager.py # Manages database and minting of new CAD files │ ├── pod_calculator.py # Calculates Proof of Design (PoD) score │ ├── file_converter.py # Handles STL/VTK file reading and VTK-to-STL conversion ├── data/ │ ├── database/ # Folder for storing database CAD files │ ├── new_cad/ # Folder for storing incoming CAD files for analysis ├── README.txt # Project documentation └── requirements.txt # Python dependencies


---

## Module Descriptions

### `src/main.py`

The main entry point for the STL-Similarity-Analyzer. This script:
1. Builds an initial similarity matrix from the database.
2. Iterates over each file in the `new_cad` folder.
3. Calculates the Proof of Design (PoD) score for each file.
4. Checks if the file already exists in the database based on the PoD score.
5. Mints (adds) the file to the database if it is unique and updates the similarity matrix.
6. Calculates network similarity scores before and after each addition.

**Key Variables**:
- `new_cad_folder_path`: Path to the folder containing new CAD files.
- `database_folder_path`: Path to the folder containing the existing CAD files (database).
- `target_points_count`: Target number of points for resampling the CAD geometries.

**Outputs**:
- Displays similarity scores before and after minting each unique file.
- Prints the complete similarity matrix after each minting operation.
- Indicates whether each new CAD file "rewards" the network.

### `src/geometry_loader.py`

This module loads STL files and resamples geometry data to standardize the number of points.

**Functions**:
- `load_stl_geometry(stl_file_path)`: Loads geometry from an STL file and returns it as a 3D point array.
- `resample_geometry(source_points, target_points_count)`: Resamples the point cloud to achieve a consistent point count for comparison.

### `src/similarity_metrics.py`

Contains functions for calculating similarity between CAD files using Signed Distance Functions (SDF) with nearest-neighbor methods.

**Functions**:
- `calculate_similarity(tensor1, tensor2, n_neighbors=10)`: Calculates similarity between two tensors. Returns `1.0` if they are identical (self-similarity).
- `calculate_network_similarity_score(matrix_data)`: Calculates the average similarity score across the entire network.

### `src/database_manager.py`

This module manages the CAD database and similarity matrix.

**Functions**:
- `mint_new_file(input_stl_file_path, database_folder)`: Adds a unique CAD file to the database by copying it to the database folder.
- `build_initial_similarity_matrix(database_folder, target_points_count)`: Builds the initial similarity matrix using all existing CAD files in the database.
- `update_similarity_matrix(new_file, database_folder, matrix_data, target_points_count)`: Updates the similarity matrix after minting a new file, adding new rows and columns for the file.

### `src/pod_calculator.py`

Calculates the Proof of Design (PoD) score by comparing the new CAD file against existing designs in the database.

**Functions**:
- `calculate_pod_for_new_file(input_geometry, database_folder, target_points_count)`: Computes the PoD score for a new CAD file. If the score is greater than or equal to `0.99`, the file is considered redundant.

### `src/file_converter.py`

Handles reading of STL and VTK files, converting VTK files to STL format if needed.

**Functions**:
- `read_geometry(file_path)`: Reads a geometry file (STL or VTK). If the file is in VTK format, it converts it to STL and returns the STL geometry.
- `convert_vtk_to_stl(vtk_file_path)`: Converts a VTK file to STL format.

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git https://github.com/caeblox/CAEBloX-PoD-Protocol.git
   cd CAEBloX-PoD-Protocol
   py main.py
