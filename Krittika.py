import requests  
from bs4 import BeautifulSoup  # For parsing HTML
from urllib.parse import urlparse, urljoin  

# defined a function to retrieve internal and external links from a given URL
def get_links(url):
    internal_links = set()  
    external_links = set()  

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = urlparse(url).scheme + '://' + urlparse(url).netloc

        # look for all anchor tags with href attribute
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href.startswith('#'):
                continue
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                internal_links.add(full_url)
            else:
                external_links.add(full_url)

        for link in soup.find_all(src=True):
            src = link.get('src')
            full_url = urljoin(base_url, src)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                internal_links.add(full_url)
            else:
                external_links.add(full_url)

        return internal_links, external_links

    # catch any exceptions that occur 
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return internal_links, external_links

# defined a function to crawl the website recursively up to a certain depth
def crawl(url, depth):
    if depth == 0:
        return set(), set()

    internal_links, external_links = get_links(url)
    all_internal_links = set(internal_links)

    # recursion for crawling individual internal link
    for link in internal_links:
        new_internal_links, new_external_links = crawl(link, depth - 1)
        all_internal_links.update(new_internal_links)
        external_links.update(new_external_links)

    return all_internal_links, external_links


start_url = 'https://krittikaiitb.github.io'
max_depth = 2 # took the depth as 2, can be an arbitrary depth

internal_links, external_links = crawl(start_url, max_depth)

print("Internal Links:")
for link in internal_links:
    print(link)

print("\nExternal Links:")
for link in external_links:
    print(link)
