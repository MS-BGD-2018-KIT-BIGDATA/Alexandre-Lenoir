'''
Created on Oct 6, 2017

@author: alexandre
'''

import googlemaps as gm
from secret.secretstore import MAPS_TOKEN
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd


# Sujet : distance ville à ville des 100 plus grandes villes de France (en
# utilisant une API)


MAX_VILLE = 7
MAX_PER_REQUEST = 10

# Récupération des top villes par scraping
def fetch_top_villes():
    scrap_url = "https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"
    content = requests.get(scrap_url)
    soup = BeautifulSoup(content.text, 'html.parser')
    selected = [soup.select("table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(" +
                            str(2 + i) + ") > td:nth-of-type(2)")[0].text.strip() for i in range(MAX_VILLE)]
    return selected


if __name__ == '__main__':
    top_villes = fetch_top_villes()
    top_villes = [ville + ", France" for ville in top_villes]
    client = gm.Client(key=MAPS_TOKEN)

    distance_matrix = np.zeros((MAX_VILLE, MAX_VILLE))
    for i in range(MAX_VILLE):
        partial_depart = top_villes[i]
        for j in range(i + 1, MAX_VILLE, MAX_PER_REQUEST):
            partial_arrivée = top_villes[j:min(MAX_VILLE, j + MAX_PER_REQUEST)]
            distances = client.distance_matrix(partial_depart, partial_arrivée)
            distances_addition = [distances['rows'][0]['elements'][x]['distance']
                                  ['value'] for x in range(min(MAX_VILLE - j, MAX_PER_REQUEST))]
            distance_matrix[i][j:j + MAX_PER_REQUEST] = distances_addition
            print(distance_matrix)

    df = pd.DataFrame(distance_matrix, columns=top_villes[:MAX_VILLE])
    df.insert(0, "villes", top_villes[:MAX_VILLE])
    df.to_csv("distance_matrix-{}.csv".format(MAX_VILLE))
