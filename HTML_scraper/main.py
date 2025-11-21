from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlsplit
from bs4 import MarkupResemblesLocatorWarning
import warnings
import pandas as pd

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}


def inspect_url(url):
    web_request = requests.get(url,headers= headers, proxies= proxies).text
    soup = BeautifulSoup(web_request,'html.parser')
    return soup

def find_book_urls(base_url, base_url_soup):
    articles = base_url_soup.find_all('article', class_=['product_pod'])
    book_urls = []
    for article in articles:
        url_fragment = article.find('a')['href']
        splitted_url = urlsplit(url_fragment).path
        book_url = urljoin(base_url, splitted_url)
        book_urls.append(book_url)
    return book_urls

def get_stars_count(book_soup):
    p_tag = book_soup.find('p',class_="star-rating")
    rating_class = p_tag["class"][1]
    rating_dictionary = {"One": 1,"Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return rating_dictionary[rating_class]

def is_available(book_soup):
    availability = book_soup.find('p', class_ ="instock availability").text
    if "available" in availability:
        return 1
    else:
        return 0

def get_book_infos(book_soup):
        stars = get_stars_count(book_soup)
        title = book_soup.h1.text
        price = book_soup.find("p", class_="price_color").text
        availability = is_available(book_soup)
        return title, stars, price, availability

def main():
    base_url = "https://books.toscrape.com/catalogue"

    base_urls = []   
    books_info = {"titles":[],
                  "stars":[],
                  "price":[],
                  "availability":[],
                  } 

    for page in range(1,51):
        page_base_url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        base_urls.append(page_base_url)
        
    for page_base_url in base_urls:
        page_base_url_soup = inspect_url(page_base_url)
        books_urls = find_book_urls(page_base_url, page_base_url_soup)
        
        for book_url in books_urls:
            book_soup = inspect_url(book_url)
            title, stars, price, availability = get_book_infos(book_soup)
            books_info["titles"].append(title)
            books_info["stars"].append(stars)
            books_info["availability"].append(availability)
            books_info["price"].append(price)
            
    
    books_df = pd.DataFrame(books_info)
    books_df.to_csv("books_information.csv")

if __name__ == "__main__":
    main()
