import time
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = "https://hastymarketcorp.com/locations/"

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

try:
    # Wait up to 20 seconds for at least one store item to appear
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.sl-item"))
    )
except Exception as e:
    print("Timeout waiting for store list:", e)

soup = BeautifulSoup(driver.page_source, "lxml")
driver.quit()

results = []

# print()

for li in soup.select("li.sl-item"):
    # print(li)
    store_name_tag = li.select_one("p.sl-addr-list-title")
    store_name = store_name_tag.get_text(strip=True) if store_name_tag else ""

    addr_span = li.select_one("li.sl-addr span")
    if addr_span:
        parts = list(addr_span.stripped_strings)
        if len(parts) == 2:
            address = parts[0]
            city_prov_postal = parts[1]
            match = re.match(
                r"(.+),\s*([A-Z]{2}),\s*([A-Z]\d[A-Z] ?\d[A-Z]\d)", city_prov_postal
            )
            if match:
                city = match.group(1)
                province = match.group(2)
                postal = match.group(3)
            else:
                city = province = postal = ""
        else:
            address = parts[0] if parts else ""
            city = province = postal = ""
    else:
        address = city = province = postal = ""

    country = "Canada"
    print(
        f"Store: {store_name} | Address: {address} | City: {city} | Province: {province} | Postal: {postal} | Country: {country}"
    )
    results.append([store_name, address, city, province, postal, country])

with open("hasty_market_stores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["Store Name", "Address", "City", "Province", "Postal Code", "Country"]
    )
    writer.writerows(results)

print(
    f"✅ Scraped {len(results)} Hasty Market locations. Saved to hasty_market_stores.csv"
)
