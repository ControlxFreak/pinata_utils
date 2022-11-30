import os
from typing import List
from requests import Session, Request
import dotenv

# Initialize the environment variables
dotenv.load_dotenv()
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY")

# Prepare the IPFS url, payload and header
ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
ipfs_headers = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_SECRET_KEY,
}

def multi_pin_to_ipfs(filenames: List[str]) -> str:
    """Pins all contents of a directory to IPFS and returns the CID hash.
    NOTE: All files must be in the same directory for this to work.
    """
    # Prepare the files
    directory = os.path.dirname(filenames[0])
    files = [
        ("pinataMetadata", (None, '{"name":"' + directory.split(os.sep)[-1] + '"}'))
    ]

    for filename in filenames:
        files.append(
            ("file", (os.sep.join(filename.split(os.sep)[-2:]), open(filename, "rb")))
        )

    # Post the request
    request = Request(
        "POST",
        ipfs_url,
        headers=ipfs_headers,
        files=files,
    ).prepare()
    response = Session().send(request)

    if not response.ok:
        raise RuntimeError(f"Could not pin to IPFS.\n{response.text}")
