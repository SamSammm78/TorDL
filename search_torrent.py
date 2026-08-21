import re
import requests 
import urllib
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_TOKEN=os.getenv("TMDB_TOKEN")
TMDB_API_KEY=os.getenv("TMDB_API_KEY")


#Nettoyer le titre du film
def clean_movie_name(raw_name):

    # Supprime tous les éléments entre [...]
    title = re.sub(r"\[.*?\]", "", raw_name)

    # Supprime l'année
    title = re.sub(r"\(\d{4}\)", "", title)

    # Nettoyage espaces
    title = " ".join(title.split())

    #également possible de retourner l'année

    return title

#Récuperer le lien magnet
def hex_hash_to_magnet(info_hash: str, display_name: str = None) -> str:
    # Nettoyer les espaces inutiles et s'assurer que la chaîne est en minuscules/majuscules valides
    clean_hash = info_hash.strip()
    
    # Structure de base du lien magnet
    magnet_link = f"magnet:?xt=urn:btih:{clean_hash}"
    
    # Optionnel : Ajouter un nom d'affichage au torrent (&dn=)
    if display_name:
        import urllib.parse
        encoded_name = urllib.parse.quote(display_name)
        magnet_link += f"&dn={encoded_name}"
        
    return magnet_link

#Récuperation du poster
def get_poster(title):
    url = "https://api.themoviedb.org/3/search/movie"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    params = {
        "api_key": TMDB_API_KEY,
        "query": title
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    clean_name = clean_movie_name(title)

    if not results:
        print("Aucun résultat TMDB pour :", clean_name)
        return None

    poster_path = results[0].get("poster_path")

    if not poster_path:
        print("Film trouvé mais aucun poster :", clean_name)
        return None

    return f"https://image.tmdb.org/t/p/w500{poster_path}"


def search_movie(query):
    #Demande à l'utilisateur d'entrer le nom du film, on l'encode format url puis on l'intègre dans l'api
    query_encoded = urllib.parse.quote(query)
    url = f"https://torrents-csv.com/service/search?q=`{query_encoded}`"

    #On fait la requet vers l'api torrents csv
    results = requests.get(url)
    #print(results.json()["torrents"])

    movie_results = []

    #On découpe les resultats pour chaque lien trouver
    n = 1
    for p in results.json()["torrents"]:
        number = str(n)

        #Afficher proprement les informations du torrent et les mettre dans un json
        size_gb_binary = p["size_bytes"] / (1024 ** 3)
        size_clean = f"{size_gb_binary:.2f} Go"
        clean_name = clean_movie_name(p["name"])
        poster_url = get_poster(clean_name)

        movie_result = {
            "movie_title":clean_name,
            "torrent_title":p["name"],
            "size": size_clean,
            "poster_url": poster_url,
            "magnet":hex_hash_to_magnet(p["infohash"])
        }

        movie_results.append(movie_result)

        n = n + 1
    return movie_results
