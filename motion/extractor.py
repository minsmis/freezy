import os

import pandas as pd


def extract(path):
    # Get file extension
    _, extension = os.path.splitext(path)

    # Extract file
    if extension == 'xlsx':
        data = pd.read_excel(path)
    if extension == 'csv':
        data = pd.read_csv(path)
    return data
