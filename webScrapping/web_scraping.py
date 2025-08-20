# pip install requests lxml bs4
# pip install lxml
# pip insall bs4

import requests
import bs4

# check if access is allowed

results = requests.get("https://www.yorkbbs.ca/")
results = requests.get("https://www.example.com/")

results = requests.get(
    "https://en.wikipedia.org/wiki/Avengers_(Marvel_Cinematic_Universe)/"
)
# print(results.text)

soup = bs4.BeautifulSoup(results.text, "lxml")
# print(soup)
print(soup.select("title")[0].getText())
print(soup.select("p")[0].getText())


base_url = "http://books.toscrape.com/catalogue/page-{}.html"

two_star_titles = []
for n in range(1, 51):
    scrape_url = base_url.format(n)
    # print(f"{scrape_url}")
    res = requests.get(scrape_url)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    books = soup.select(".product_pod")

    for book in books:
        # if '.star_rating.Two' in str(book)
        if len(book.select(".star-rating.Two")) != 0:
            book_title = book.select("a")[1]["title"]
            two_star_titles.append(book_title)

print(two_star_titles)
