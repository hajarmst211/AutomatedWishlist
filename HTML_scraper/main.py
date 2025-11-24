from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlsplit
from bs4 import MarkupResemblesLocatorWarning
import warnings
import pandas as pd
import time

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

rating_dictionary = {"One": 1,"Two": 2, "Three": 3, "Four": 4, "Five": 5}
    
def inspect_url(url, session):
    web_request = session.get(url, headers = headers).text
    #lxml is faster than html.parser
    soup = BeautifulSoup(web_request,'lxml')
    return soup

def select_book_urls(base_url, base_url_soup):
    articles = base_url_soup.select('article', class_=['product_pod'])
    book_urls = []
    for article in articles:
        url_fragment = article.select_one('a')['href']
        splitted_url = urlsplit(url_fragment).path
        book_url = urljoin(base_url, splitted_url)
        book_urls.append(book_url)
    return book_urls
    
def is_available(book_soup):
    in_stock_element = book_soup.select_one('p', class_='instock availability')
    if in_stock_element.text == "In stock":
        return 1
    else:
        return 0

def get_price(book_soup):
    price_text = book_soup.select_one('p', class_='price_color').text
    price_number = ''.join(c for c in price_text if c.isdigit() or c == '.')
    return price_number

def get_stars(book_soup):
    p_tag = book_soup.find('p',class_="star-rating")
    rating_class = p_tag["class"][1]
    return rating_dictionary[rating_class]       
                
def get_book_infos(book_soup):
        title = book_soup.h1.a
        stars = get_stars(book_soup)
        price = get_price(book_soup)
        availability = is_available(book_soup)
        return title, stars, price, availability

def main():
    base_url = "https://books.toscrape.com/catalogue"
    session = requests.Session()
    
    base_urls = []   
    books_info = {"titles":[],
                  "stars":[],
                  "price":[],
                  "availability":[],
                  } 

    for page in range(1,51):
        page_base_url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        page_base_url_soup = inspect_url(page_base_url,session)
        books_urls = select_book_urls(page_base_url, page_base_url_soup)
        
        for book_url in books_urls:
            book_soup = inspect_url(book_url, session)
            title, stars, price, availability = get_book_infos(book_soup)
            books_info["titles"].append(title)
            books_info["stars"].append(stars)
            books_info["availability"].append(availability)
            books_info["price"].append(price)
    
    #Writing and reading from parquet files is a lot faster and uses less memory on disk than csv files
    books_df = pd.DataFrame(books_info)
    books_df.to_parquet("books_information.parquet")

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print("the time the programe took is:", end-start)