import zipfile
from timetable import *
from utils.filesystem.paths import *
import shutil

def extract_and_save_as_bin(zip_path):
    """
    Extracts the contents of a zip file (assumes a single binary file inside),
    overwrites the zip file with the extracted content, and renames it to .bin.

    Parameters:
        zip_path (str): Path to the zip file.

    Returns:
        str: The new path of the saved .bin file.
    """
    # Ensure the file exists and is a zip file
    if not os.path.isfile(zip_path) or not str(zip_path).endswith('.zip'):
        raise ValueError("Invalid zip file path provided.")

    # Extract the binary file
    with zipfile.ZipFile(zip_path, 'r') as z:
        file_names = z.namelist()
        
        if len(file_names) != 1:
            raise ValueError("The zip file must contain exactly one file.")
        
        binary_data = z.read(file_names[0])

    # Determine the new file name (same directory, with .bin extension)
    new_file_path = os.path.splitext(zip_path)[0] + '.bin'

    # Write the binary content to the new file
    with open(new_file_path, 'wb') as f:
        f.write(binary_data)

    # Remove the original zip file
    os.remove(zip_path)

    return new_file_path

def get_creation_time(item):
    return item.stat().st_ctime

def copy_latest_file(IN, OUT=None):
    path_object = Path(IN)
    items = path_object.iterdir()
    sorted_items = sorted(items, key=get_creation_time)
    most_recent = sorted_items[-1].name
    shutil.copyfile(IN / most_recent, OUT / 'locations.bin')
    return most_recent

if __name__ ==  '__main__':

    # Set params
    url = f"https://data.bus-data.dft.gov.uk/avl/download/gtfsrt"
    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    save_path = ARXIV / f"{now}.zip"
    
    # Download the live locations zip file
    download_zip_file(url, save_path)
    # Extract the binary file and save it
    extract_and_save_as_bin(save_path)
    # Copy the most recent locations to the `current` dir
    copy_latest_file(DOWNLOADS / 'gtfs-rt/archive', DOWNLOADS / 'gtfs-rt/current')

