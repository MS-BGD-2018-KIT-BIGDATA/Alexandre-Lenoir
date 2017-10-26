'''
Created on Oct 20, 2017

@author: alexandre
'''


"""
Site open-medicament.fr
On s'intéresse à l'ibuprofène. On veut connaitre la quandtité d'ibuprofène par boite de médicament.
On veut le labo, equi traitement, anne de com, mois de com, prix, restriction age, restriction poids
"""


import requests
import json

def getMedicamentList():
    response = requests.get("https://www.open-medicaments.fr/api/v1/medicaments?query=ibuprofene")
    print(response)
    resp = json.decoder.JSONDecoder().decode(response.text)
    return [med["codeCIS"]for med in resp]
    print(resp)
    
def getMedicamentInfo(id):
    response = requests.get("https://www.open-medicaments.fr/api/v1/medicaments/" + id)
    resp = json.decoder.JSONDecoder().decode(response.text)
    return resp
        
def getEquivTraitemement(info):
    print(info)
    dosage = info["compositions"][0]["substancesActives"][0]["dosageSubstance"][:-2]
        
def main():
    res = []
    list = getMedicamentList()
    for med in list:
        info = getMedicamentInfo(med)
        res.append([info["titulaires"], getEquivTraitemement(info),info["dateAMM"][:4],info["dateAMM"][5:7]])
    print(res)
    
if __name__ == '__main__':
    main()