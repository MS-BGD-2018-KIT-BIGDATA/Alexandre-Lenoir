'''
Created on Oct 6, 2017

@author: alexandre
'''

import googlemaps as gm
from secret.secretstore import MAPS_TOKEN

# Sujet : Ville à ville des 100 plus grandes villes de France (en utilisant une API)



# Fetch top villes par scraping
def fetch_top_villes():
    scrap_url = "https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"
    return ['paris', "marseille", "lyon", "toulouse"]


if __name__ == '__main__':
    top_villes = fetch_top_villes()
    client = gm.Client(key=MAPS_TOKEN)
    result = client.distance_matrix(top_villes, top_villes)
    print(result)
