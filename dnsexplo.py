import random
import string
import requests

def generate_random_domain(length=6):
    """Génère un nom de domaine aléatoire en .fr"""
    return ''.join(random.choices(string.ascii_lowercase, k=length)) + '.fr'

def check_domain(domain):
    """Vérifie si le domaine existe en envoyant une requête HTTP"""
    url = f"http://{domain}"
    try:
        response = requests.get(url, timeout=3)
        # Si la requête est réussie (même avec 404), le domaine existe
        return response.status_code < 500
    except requests.ConnectionError:
        # Si la connexion échoue, le domaine est probablement inexistant
        return False
    except requests.Timeout:
        # En cas de timeout, on considère aussi que le domaine n'est pas accessible
        return False
    except requests.RequestException as e:
        print(f"Erreur pour {domain}: {e}")
        return False

def main():
    found_domains = []
    for _ in range(100):  # Nombre d'itérations, à ajuster
        domain = generate_random_domain()
        if check_domain(domain):
            print(f"{domain} existe.")
            found_domains.append(domain)
        else:
            print(f"{domain} n'existe pas.")

    print("Domaines trouvés:", found_domains)

if __name__ == "__main__":
    main()
