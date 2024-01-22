import os

import pandas as pd


def extract_data(path):
    # Output
    data = []

    # Get file extension
    _, extension = os.path.splitext(path)

    # Extract file
    if extension == '.xlsx':
        data = pd.read_excel(path)
    if extension == '.csv':
        data = pd.read_csv(path)
    return data


def read_bodyparts(data):
    # Parameters
    # data [DataFrame]: Return of 'extract_data'.
    # Return
    # bodyparts [list]: Name of bodyparts in the data.

    # Read data head
    head = data.head()

    # Read columns containing bodyparts
    bodyparts = list(head.columns[1:])  # 'bodyparts' in index=0

    return bodyparts
