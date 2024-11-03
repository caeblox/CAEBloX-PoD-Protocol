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
