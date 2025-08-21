import requests
from bs4 import BeautifulSoup
import csv
import time

main_url = "https://www.circlek.com/ca/ontario/list-canada-stores"
base_url = "https://www.circlek.com"

response = requests.get(main_url)
soup = BeautifulSoup(response.text, "lxml")

results = []
store_links = soup.select("#content a[href^='/store-locator/CA/']")
print(f"Found {len(store_links)} store links")
for a in store_links:
    store_url = base_url + a.get("href", "")
    store_text = a.get_text(strip=True)
    # Visit the store detail page
    detail_resp = requests.get(store_url)
    detail_soup = BeautifulSoup(detail_resp.text, "lxml")
    # Try to extract postal code, address, store name, etc.
    address_block = detail_soup.select_one(".store-details__address")
    if address_block:
        lines = [line.strip() for line in address_block.stripped_strings]
        # Usually: [Store Name, Address, City, Province, Postal Code, Country]
        store_name = lines[0] if len(lines) > 0 else ""
        address = lines[1] if len(lines) > 1 else ""
        city = lines[2] if len(lines) > 2 else ""
        province = lines[3] if len(lines) > 3 else ""
        postal_code = lines[4] if len(lines) > 4 else ""
        country = lines[5] if len(lines) > 5 else ""
    else:
        # fallback: parse from main list
        parts = [p.strip() for p in store_text.split(",")]
        store_name = ""
        address = parts[0] if len(parts) > 0 else ""
        city = parts[1] if len(parts) > 1 else ""
        province = parts[2] if len(parts) > 2 else ""
        country = parts[3] if len(parts) > 3 else ""
        postal_code = ""
    results.append(
        [store_name, address, city, province, postal_code, country, store_url]
    )
    time.sleep(0.2)  # be polite to the server

with open("circlek_ontario_stores_full.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "Store Name",
            "Address",
            "City",
            "Province",
            "Postal Code",
            "Country",
            "Store URL",
        ]
    )
    writer.writerows(results)

print(
    f"✅ Scraped {len(results)} Circle K Ontario locations. Saved to circlek_ontario_stores_full.csv"
)
