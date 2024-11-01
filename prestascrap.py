
import requests
from bs4 import BeautifulSoup

def check_prestashop(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Vérifie si la requête a réussi
    except requests.RequestException as e:
        print(f"Erreur pour {url}: {e}")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    # Vérifie la présence de balises ou scripts typiques de PrestaShop
    if soup.find('meta', {'name': 'generator', 'content': 'PrestaShop'}):
        return True
    if "prestashop" in response.text.lower():  # Vérifie les mentions du mot "prestashop" dans le texte
        return True

    return False

def main():
    # Liste des sites à tester
    sites = [
        "https://www.insectosphere.fr",
        "https://printlabs.bureau-vallee.fr",
        "https://shop.toureiffel.paris/fr/",
        "https://www.chaussea.com/fr/",
    ]

    for site in sites:
        if check_prestashop(site):
            print(f"{site} utilise PrestaShop.")
        else:
            print(f"{site} n'utilise pas PrestaShop.")

if __name__ == "__main__":
    main()
