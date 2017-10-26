'''
Created on Oct 19, 2017

@author: alex
'''

from bs4 import BeautifulSoup as bs
from enum import Enum
import requests
import re
import json

LACENTRALE_URL = "https://www.lacentrale.fr/cote-voitures-renault-zoe--{}-.html"
LEBONCOIN_URL = "https://www.leboncoin.fr/voitures/offres/"

REGIONS = ["ile_de_france", "provence_alpes_cote_d_azur", "aquitaine"]


class TypesVendeur(Enum):
    Professionel = 1
    Particulier = 2


class Regions(Enum):
    AQUITAINE = "aquitaine"
    IDF = "ile_de_france"
    PACA = "provence_alpes_cote_d_azur"


class Versions(Enum):
    Life = "Life"
    Zen = "Zen"
    Intens = "Intens"


def isProfessionel(carSoup):
    if carSoup.find("span", class_="ispro"):
        return True
    return False


def getVersionFomText(text):
    for modele in Versions:
        value = modele.value
        if re.search(value, text, flags=re.IGNORECASE):
            return modele.value
    return None


def getVersion(soup):
    title = soup.find("h1").text.strip()
    version = getVersionFomText(title)
    if version == None:
        description = soup.find("p", itemprop="description").text.strip()
        version = getVersionFomText(description)
    return version


def getSoupFromURL(url, method='get', data={}):
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url, data=data)
    else:
        return None

    if res.status_code == 200:
        soup = bs(res.text, 'html.parser')
        return soup
    else:
        return None


def getUrlArgus():
    return [LACENTRALE_URL.format(annee) for annee in [2012, 2018]]


def getUrlList():
    result = []
    for region in Regions:
        url = LEBONCOIN_URL + region.value + "/?th=1&q=zoe"
        siteSoup = getSoupFromURL(url)
        result.append(url)
        pageCount = int(siteSoup.find_all(
            "a", class_="element page")[-1].text.strip())
        if pageCount:
            for page in range(2, pageCount + 1):
                result.append(LEBONCOIN_URL + region.value + "/?o=" +
                              str(page) + "&th=1&q=zoe")
    return result


def getLinks(url):
    soup = getSoupFromURL(url)
    links = soup.find_all("a", class_="list_item clearfix trackable")
    linkList = ["http:" + link['href'] for link in links]
    return linkList


def getPhoneNumber(annonceId):
    res = requests.post("https://api.leboncoin.fr/api/utils/phonenumber.json", data={
                        "list_id": annonceId, "app_id": "leboncoin_web_utils", "key": "54bb0281238b45a03f0ee695f73e704f", "text": 1})
    print(res.text)
    try:
        return json.decoder.JSONDecoder().decode(res.text)["utils"]["phonenumber"]
    except:
        return None


def getDetailAnnonce(url):

    details = {}

    print("Lecture de la page " + url)
    soup = getSoupFromURL(url)

    details["prix"] = int(soup.find_all("span", class_="value")[
                          0].text.strip().replace("\xa0€", "").replace(" ", ""))

    details["année"] = int(soup.find_all(
        "span", class_="value")[4].text.strip())

    details["kilometrage"] = int(soup.find_all("span", class_="value")[
                                 5].text.strip().replace("KM", "").replace(" ", ""))

    details["version"] = getVersion(soup)
    annonceId = re.findall("http.*/([0-9]*)\.htm", url)
    details["telephone"] = getPhoneNumber(annonceId[0])
    details["isProfessionel"] = isProfessionel(soup)

    return details


def main():
    urlList = getUrlList()
    detailsAnnonces = []
    for url in urlList:
        annonces = getLinks(url)
        for annonce in annonces:
            details = getDetailAnnonce(annonce)
            detailsAnnonces.append(details)
    print(detailsAnnonces)


if __name__ == '__main__':
    main()
