import requests
import os
import dotenv
from bs4 import BeautifulSoup

print("!!!!!!!!!!!!!!!!!!!!DO NOT USE THIS!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("THIS WILL DOWNLOAD EVERYTHING FROM PINATA TO YOUR LOCAL MACHINE AND THEN DELETE IT FROM PINATA")
print("!!!!!!!!!!!!!!!!!!!!DO NOT USE THIS!!!!!!!!!!!!!!!!!!!!!!!!!!")

if input("are you sure? (y/n): ").lower() != "y":
    exit()

dotenv.load_dotenv()
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY")

get_url = "https://api.pinata.cloud/data/pinList?status=pinned&pinSizeMin=100"
gateway_url = "https://violet-legal-antelope-340.mypinata.cloud"
base_del_url = "https://api.pinata.cloud/pinning/unpin/{0}"

payload = {}
headers = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_SECRET_KEY,
}

while True:
    # Get the next batch of pins
    response = requests.get(get_url, headers=headers, data=payload, timeout=600).json()

    # Download all content from each of these folders
    for row in response["rows"]:
        # Get the ID and IPFS hash
        cid = row["ipfs_pin_hash"]
        dir_name = row["metadata"]["name"]
        print(f"Downloading {dir_name} at URI {cid}...")

        # Get the url to the entire directory
        dir_url = gateway_url + f"/ipfs/{cid}"
        response = requests.get(dir_url, timeout=600)

        # create beautiful-soup object
        soup = BeautifulSoup(response.content,features="html.parser")

        # find all links on web-page
        links = soup.findAll('a')

        # filter the links down to just the images/gifs/metadata files
        filelinks = [
            gateway_url + link['href'] for link in links
            if (link['href'].endswith('.json') or link['href'].endswith('webp') or link['href'].endswith('gif') or link['href'].endswith('png'))
            and "?filename" not in link['href']
        ]

        # Save the files locally
        outdir = f"SantaBot2022/{dir_name}/"
        os.makedirs(outdir, exist_ok=True)
        for filelink in filelinks:
            filename = outdir + filelink.split('/')[-1]
            print(filelink)
            response = requests.get(filelink, stream = True, timeout=600)

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size = 1024 * 1024):
                    if chunk:
                        f.write(chunk)

        # Delete the data from pinata
        print(f"Deleting {dir_name} at URI {cid}")
        # Construct a request to delete this URI
        del_url = base_del_url.format(cid)
        response = requests.request("DELETE", del_url, headers=headers, data=payload, timeout=600)
