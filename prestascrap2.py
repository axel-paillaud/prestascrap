import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def check_prestashop(url):
    """Checks if a site uses PrestaShop."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur pour {url}: {e}")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    # Check PrestaShop indication
    if soup.find('meta', {'name': 'generator', 'content': 'PrestaShop'}):
        return True
    if "prestashop" in response.text.lower():
        return True

    return False

def find_french_links(url, visited):
    """Explore the links on the start page to find French sites."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de l'accès à {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link["href"])
        parsed_url = urlparse(full_url)

        # Filter .fr domains and avoid duplicates
        if parsed_url.netloc.endswith(".fr") and full_url not in visited:
            links.add(full_url)

    return links

def main():
    # Starting list of sites to explore
    start_urls = [
        "https://www.pagesjaunes.fr",
        "https://www.lafourchette.com",
    ]

    visited = set()

    for start_url in start_urls:
        to_visit = find_french_links(start_url, visited)

        for url in to_visit:
            visited.add(url)  # Set URL as visited
            if check_prestashop(url):
                print(f"{url} utilise PrestaShop.")
            else:
                print(f"{url} n'utilise pas PrestaShop.")

if __name__ == "__main__":
    main()
