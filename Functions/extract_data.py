import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Setup headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Open Circle K store locator
url = "https://www.circlek.com/store-locator"
driver.get(url)
time.sleep(5)

# Select "Canada" as country (or set region manually)
# The locator auto-detects, but you can input a city or postal code if needed
search_box = driver.find_element(By.ID, "edit-address")
search_box.clear()
search_box.send_keys("Canada")
search_button = driver.find_element(By.ID, "edit-submit-store-locator")
search_button.click()
time.sleep(8)

# Scroll to load all stores
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Parse page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Extract store entries
stores = soup.select(".store-result")
data = []

for store in stores:
    try:
        name = store.select_one("h2").get_text(strip=True)
        address = store.select_one(".street-block").get_text(" ", strip=True)
        city = store.select_one(".locality").get_text(strip=True)
        region = store.select_one(".region").get_text(strip=True)
        postal = store.select_one(".postal-code").get_text(strip=True)
        phone = (
            store.select_one(".telephone").get_text(strip=True)
            if store.select_one(".telephone")
            else ""
        )
        data.append([name, address, city, region, postal, phone])
    except Exception as e:
        print("Error parsing store:", e)

# Save to CSV
with open("circlek_locations.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["Store Name", "Address", "City", "Province", "Postal Code", "Phone"]
    )
    writer.writerows(data)

print(f"✅ Scraped {len(data)} Circle K stores. Saved to circlek_locations.csv")
