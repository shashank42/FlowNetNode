import requests
import json
import os

def get_all_files(directory: str) -> list[str]:
    """get a list of absolute paths to every file located in the directory"""
    paths: list[str] = []
    for root, dirs, files_ in os.walk(os.path.abspath(directory)):
        for file in files_:
            paths.append(os.path.join(root, file))
    return paths

def upload_directory_to_pinata(directory):

    all_files: list[str] = get_all_files(directory)
    files = [("file", (file, open(file, "rb"))) for file in all_files]

    print(files)

    headers = {
        "pinata_api_key": "d7cf990fa39fa11534c9",
        "pinata_secret_api_key": "47e5b04d33c137e30a852945cf3c3a6060ac96393603aa3d4e09018872cd2792",
    }

    response = requests.Response = requests.post(
        url="https://api.pinata.cloud/" + "pinning/pinFileToIPFS", files=files, headers=headers
    )

    data = response.json()
    print(data)
    imageLinkBase = "ipfs://" + data["IpfsHash"] + "/"
    return imageLinkBase

upload_directory_to_pinata("/Users/shashank/Downloads/output")