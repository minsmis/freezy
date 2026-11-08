import os

import numpy as np
import pandas as pd


def extract_data(path):
    """Load a DLC coordinate table from a CSV or Excel file."""
    _, extension = os.path.splitext(path)
    extension = extension.lower()
    if extension == '.xlsx':
        data = pd.read_excel(path, skiprows=1)
    elif extension == '.csv':
        # Standard DLC CSVs have scorer, bodyparts, and coords metadata rows.
        # Combine bodypart + coordinate names to keep duplicate CSV headers distinct.
        with open(path, encoding='utf-8-sig', newline='') as source:
            first_rows = [source.readline().rstrip('\r\n').split(',') for _ in range(3)]
        if first_rows[0] and first_rows[0][0].strip().lower() == 'scorer':
            bodyparts, coords = first_rows[1], first_rows[2]
            names = ['frame']
            for bodypart, coord in zip(bodyparts[1:], coords[1:]):
                bodypart, coord = bodypart.strip(), coord.strip().lower()
                names.append(f'{bodypart}_{coord}' if coord in {'x', 'y', 'likelihood'} else bodypart)
            data = pd.read_csv(path, skiprows=3, header=None, names=names)
        else:
            # Simpler DLC exports have bodyparts and coords rows.
            data = pd.read_csv(path, skiprows=1)
    else:
        raise ValueError(f"Unsupported file type '{extension or '(no extension)'}': {path}. Select a .csv or .xlsx DLC file.")
    if data.empty or len(data.columns) == 0:
        raise ValueError(f"No coordinate data found in file: {path}")
    return data


def read_bodyparts(data):
    # Parameters
    # data [DataFrame]: Return of 'extract_data'.
    # Return
    # bodyparts [list]: Name of bodyparts in the data.

    # Read data head
    head = data.head()

    # Read columns containing bodyparts
    bodyparts = [column for column in head.columns[1:]
                 if not str(column).lower().endswith('_likelihood')]

    return bodyparts


def extract_coordinates(data, x_bodypart, y_bodypart):
    # Parameters
    # data [DataFrame]: Return of 'extract_data'.
    # x_bodypart, y_bodypart [str]: Bodypart name to extract coordinates.
    # Return
    # x_coordinates, y_coordinates [list]: Coordinates for each bodypart.

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame from extract_data; check that the selected file is a .csv or .xlsx DLC file.")
    missing = [name for name in (x_bodypart, y_bodypart) if name not in data.columns]
    if missing:
        raise KeyError(f"Bodypart column(s) not found: {', '.join(missing)}")

    x_coordinates = pd.to_numeric(data[x_bodypart], errors='raise').astype(float).tolist()
    y_coordinates = pd.to_numeric(data[y_bodypart], errors='raise').astype(float).tolist()

    return x_coordinates, y_coordinates


def make_route(x_coordinates, y_coordinates):
    return np.array([x_coordinates, y_coordinates])
