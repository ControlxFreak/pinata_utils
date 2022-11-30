import requests
import os
import dotenv

print("!!!!!!!!!!!!!!!!!!!!DO NOT USE THIS!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("THIS WILL DELETE EVERYTHING YOU HAVE ON PINATA AND IT IS YOUR ONLY BACKUP")

if input("are you sure? (y/n): ").lower() != "y":
    exit()

dotenv.load_dotenv()
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY")

get_url = "https://api.pinata.cloud/data/pinList?status=pinned&pinSizeMin=100"
base_del_url = "https://api.pinata.cloud/pinning/unpin/{0}"
payload = {}
headers = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_SECRET_KEY,
}

def clear_pinata():
    while True:
        # Get the next batch of pins
        response = requests.request("GET", get_url, headers=headers, data=payload).json()

        # Delete them
        for row in response["rows"]:
            # Get the ID and IPFS hash
            ipfs_uri = row["ipfs_pin_hash"]
            name = row["metadata"]["name"]
            print(f"Deleting {name} at URI {ipfs_uri}")

            # Construct a request to delete this URI
            del_url = base_del_url.format(ipfs_uri)

            response = requests.request("DELETE", del_url, headers=headers, data=payload)
            print(response.text)
