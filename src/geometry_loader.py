import vtk
import numpy as np
import os

def load_stl_geometry(stl_file_path):
    """
    Load geometry data from an STL file and return it as a numpy array.
    """
    if not os.path.exists(stl_file_path):
        raise FileNotFoundError(f"The file {stl_file_path} does not exist.")

    reader = vtk.vtkSTLReader()
    reader.SetFileName(stl_file_path)
    reader.Update()
    polydata = reader.GetOutput()

    if polydata is None or polydata.GetPoints() is None:
        raise ValueError(f"Failed to load STL file: {stl_file_path}. The file may be corrupted or empty.")

    points = polydata.GetPoints()
    return np.array([points.GetPoint(i) for i in range(points.GetNumberOfPoints())])

def resample_geometry(source_points, target_points_count):
    """
    Resample point data to match the target count.
    """
    source_count = source_points.shape[0]
    if source_count == target_points_count:
        return source_points
    elif source_count < target_points_count:
        oversample_factor = target_points_count // source_count
        remainder = target_points_count % source_count
        resampled_points = np.repeat(source_points, oversample_factor, axis=0)
        if remainder > 0:
            resampled_points = np.vstack([resampled_points, source_points[:remainder]])
        return resampled_points
    else:
        indices = np.linspace(0, source_count - 1, target_points_count).astype(int)
        return source_points[indices]
