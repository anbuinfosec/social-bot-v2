import requests
import json
import os
from urllib.parse import urljoin

def fetch_file_list(json_url):
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("files", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file list: {e}")
        return []

def download_and_replace(base_url, file_list):
    for file_name in file_list:
        file_url = urljoin(base_url, file_name)
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            with open(file_name, "wb") as f:
                f.write(response.content)
            print(f"Updated: {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {file_name}: {e}")

def update():
    base_url = "https://raw.githubusercontent.com/anbuinfosec/social-bot-v2/main/"
    json_url = urljoin(base_url, "files.json")
    
    file_list = fetch_file_list(json_url)

    if file_list:
        download_and_replace(base_url, file_list)
    else:
        print("No files to update.")

if __name__ == "__main__":
    update()
