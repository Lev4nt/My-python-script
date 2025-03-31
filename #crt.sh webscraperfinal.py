#crt.sh webscraperfinal.py#
import os
import time
import requests
from bs4 import BeautifulSoup
import re
import imgkit  # Requires wkhtmltoimage to be installed

# Create output folder
OUTPUT_DIR = "screenshots"
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# Step 1: Scrape crt.sh for links containing 'ecolab.com'
search_url = "https://crt.sh/?q=%.ecolab.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    time.sleep(5)  # Prevents rate-limiting
except requests.exceptions.RequestException as e:
    print(f"Error fetching {search_url}: {e}")
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

# Find all links from the search results
links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if 'id=' in href:  # crt.sh links have 'id=' in them
        full_link = f"https://crt.sh{href}"
        links.append(full_link)

def sanitize_folder_name(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Step 2: Visit each link and take a screenshot using imgkit
for link in links:
    try:
        print(f"Opening {link}")
        time.sleep(3)  # Prevents too many requests

        folder_name = sanitize_folder_name(link.replace("https://", ""))
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        # Take screenshot using imgkit (requires wkhtmltoimage)
        screenshot_path = os.path.join(folder_path, "screenshot.png")
        imgkit.from_url(link, screenshot_path)

        print(f"Saved screenshot to {screenshot_path}")

    except Exception as e:
        print(f"Error opening {link}: {e}")

print(f"✅ Finished! Screenshots saved in the '{OUTPUT_DIR}' folder.")
