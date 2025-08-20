import requests
from bs4 import BeautifulSoup
import csv

base_url = (
    "https://www.yellowpages.ca/search/si/{page}/Great+Canadian+Dollar+Store/Canada"
)
results = []

# Get the total number of pages
resp = requests.get(base_url.format(page=1))
soup = BeautifulSoup(resp.text, "lxml")
try:
    last_page = int(soup.select_one("a[aria-label='Last']")["href"].split("/")[4])
except Exception:
    last_page = 1

for page in range(1, last_page + 1):
    url = base_url.format(page=page)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")

    for listing in soup.select("article[data-ypid]"):
        address = listing.select_one("span[itemprop='streetAddress']")
        city = listing.select_one("span[itemprop='addressLocality']")
        province = listing.select_one("span[itemprop='addressRegion']")
        postal = listing.select_one("span[itemprop='postalCode']")
        country = "Canada"

        results.append(
            [
                address.get_text(strip=True) if address else "",
                city.get_text(strip=True) if city else "",
                province.get_text(strip=True) if province else "",
                postal.get_text(strip=True) if postal else "",
                country,
            ]
        )

with open("great_canadian_dollar_stores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Address", "City", "Province", "Postal Code", "Country"])
    writer.writerows(results)

print(
    f"✅ Scraped {len(results)} Great Canadian Dollar Store locations. Saved to great_canadian_dollar_stores.csv"
)
