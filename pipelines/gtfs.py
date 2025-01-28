import pandas as pd
import zipfile
from io import TextIOWrapper

def load_gtfs(fpath, files=None):
    """
    Load specified files from a GTFS .zip file.

    Parameters
    ----------
        fpath (str): Path to the GTFS .zip file.
        files (list): List of file names to load. If None, loads all files in the archive.

    Returns
    -------
        list: A list of pandas DataFrames corresponding to the specified files.
    """
    if not str(fpath).endswith('.zip'):
        raise ValueError('The provided file is not a .zip file')

    with zipfile.ZipFile(fpath, 'r') as z:
        # Get the list of files in the archive
        available_files = z.namelist()

        # If no files are specified, load all files
        if files is None:
            files = available_files
        else:
            # Validate that all specified files exist in the archive
            missing_files = [file for file in files if file not in available_files]
            if missing_files:
                raise FileNotFoundError(f"The following files are missing in the archive: {missing_files}")

        # Load the specified files into DataFrames
        result = [
            pd.read_csv(TextIOWrapper(z.open(file), 'utf-8'), low_memory=False)
            for file in files
        ]

    return result