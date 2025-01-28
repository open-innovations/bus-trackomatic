import requests
import os
from datetime import datetime
from utils.filesystem.paths import *

def download_zip_file(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP request errors

        # Write the content to a file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"File successfully downloaded and saved to: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ ==  '__main__':
    region = 'yorkshire'
    url = f"https://data.bus-data.dft.gov.uk/timetable/download/gtfs-file/{region}/"
    save_path = DOWNLOADS / f"timetable/{region}_{datetime.now().date().isoformat()}.zip"

    # Create the downloads directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    download_zip_file(url, save_path)

