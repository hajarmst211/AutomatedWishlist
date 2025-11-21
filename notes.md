# Scrapping
## Steps involved in web scraping
1. Send an HTTP Request: Use the requests library to send a request to the webpage URL and get the HTML content in response.
2. Parse the HTML Content: Use a parser like html.parser or html5lib to convert the raw HTML into a structured format (parse tree).
3. Extract Data: Use BeautifulSoup to navigate the parse tree and extract the required data using tags, classes, or IDs. 
<br>
**NOTE:** make sure you always use a header, a proxy and 

---
# HTML tree:
• a node in the HTML tree becomes a dictionary holding its attributes in python.

-->A dictionary is a key → value mapping.

<br> Example:<br>
`<a href="catalogue/x.html" title="Something">...</a>`<br>
is internally stored as:

```pgsql
tag.name = "a"
tag.attrs = {
    "href": "catalogue/x.html",
    "title": "Something"
}
```

- So to get the link we should call soup.find('a')['href']

#### To find the wanted class:
- [class~="word"]: class that contains a word
- [class^="prefix"]: starts with prefix
- class_='word': contains exactly the word
<br>
When you scrape a paragraph or 
Here’s what the structure looks like inside BeautifulSoup:

• The `<p>` tag becomes a Tag object.
• Its "class" attribute becomes a Python list: ["star-rating", "Three"].
• The `<i>` children become a list of Tag objects, accessible via .contents or .find_all().
<br>
**Example:**
`<p class="star-rating Three"></p>`
tag['class'] → ['star-rating', 'Three']

BeautifulSoup automatically splits the string on spaces and returns a list.
<br>
When you get a `<p>` object with the attributs: class and id like:
```
p_tag = soup.find('p', id="book1")
```
The element itself is a Tag object. Attributes of the element are accessed like a dictionary: tag['attribute_name'].
```
print(p_tag['class'])  # ['star-rating', 'Three']
print(p_tag['id']) 
```
- Nested elements (like `<i>` inside `<p>`) are accessible via .find(), .find_all(), or .contents.

---
# Proxies:
- To begin with, you should know that if too many requests come from the same IP in a short interval, the server’s rate-limiter will often throttle, challenge, or block that address.
- A proxy is a server that lies between the client and the host. 
## Benefits of using proxies

- **connection optimization**: hiding or masking the user's ID or changing the IP address to access geographically blocked websites.
- **Bypassing Restrictions:** Proxies let you get around access limits set up by firewalls, filters, or blocking based on your location.
<br>....
---
- **Proxy management:** your code must detect ip addresses failures(detected by the website or got handed captchas), stop using the bad ones, and rotate to healthy ones. 
## Relation between IP address type(IPv4 or 6) and the proxie
- IPv6 proxies can be much cheaper if the target website supports the new version of the protocol.
- Most websites use ipv4 so we can't use ipv6 proxies unless we explicitly know our target website supports it.

## Proxy protocols: HTTP and SOCKS
- SOCKS Proxy: SOCKS proxies are designed for any type of traffic
- HTTP Proxy: This type of proxy is designed for HTTP requests. It only supports HTTP and HTTPS. HTTP proxies are suitable for general web browsing, accessing websites, and interacting with web APIs.



# Network tab in the invest part of the website
1. Disable your extensions
2. In the inspect window go to the network tab.
3. Click on  a web request and look for the essential headers' informations.
Servers almost always care only about this handful:

    - User-Agent
    - Accept
   - Accept-Language
    - Referer (sometimes)
    - Origin (for CORS)
   -  Cookie (if login is needed)
    - CSRF or JWT tokens if present in cookies or headers
    <br>
4. Make your custom headers