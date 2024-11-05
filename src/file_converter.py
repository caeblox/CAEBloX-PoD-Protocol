import vtk
import numpy as np
import os
from geometry_loader import load_stl_geometry

def read_geometry(file_path):
    """
    Reads a geometry file in STL or VTK format. 
    If the file is in VTK format, it will be converted to STL.

    Parameters:
        file_path (str): Path to the STL or VTK file.

    Returns:
        np.ndarray: Array of 3D points from the STL geometry.
        str: Path to the STL file (converted if input was VTK).
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == ".stl":
        return load_stl_geometry(file_path), file_path  # Function from geometry_loader.py

    elif file_extension == ".vtk":
        stl_file_path = convert_vtk_to_stl(file_path)
        return load_stl_geometry(stl_file_path), stl_file_path  # Function from geometry_loader.py

    else:
        raise ValueError("Unsupported file format. Only STL and VTK files are supported.")

def convert_vtk_to_stl(vtk_file_path):
    """
    Converts a VTK file to STL format.

    Parameters:
        vtk_file_path (str): Path to the VTK file.

    Returns:
        str: Path to the converted STL file.
    """
    # Create a reader for VTK format
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(vtk_file_path)
    reader.Update()

    polydata = reader.GetOutput()

    # Create an STL writer
    stl_file_path = vtk_file_path.replace(".vtk", ".stl")
    writer = vtk.vtkSTLWriter()
    writer.SetFileName(stl_file_path)
    writer.SetInputData(polydata)
    writer.Write()

    print(f"Converted {vtk_file_path} to {stl_file_path}")
    return stl_file_path
