from bs4 import BeautifulSoup
import requests
import pandas as pd


URL_DELL = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-dell.html#_his_"
URL_ACER = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-acer.html#_his_"

def getSoupForURL(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    return soup


def parse_normal_price(normal_price):
    try:
        cents = normal_price.find("sup").string[1:]
        return float(normal_price.contents[0]) + float(cents)/100
    except:
        print("Could not parse normal price html part " + str(normal_price))

def parse_discounted_price(discounted_price):
    try:
        price = float(discounted_price.string.replace(",","."))
        return price
    except:
        print("Could not parse discounted price html part " + str(discounted_price))

def getPricesAndDiscount(soup):
    # select instances of <prdtBZPrice> tags that contain plain prices and may contain discounted price
    result = []
    price_containers = soup.find_all("div", class_ = "prdtBZPrice")
    for price_container in price_containers:
        discounted_price = price_container.find("div", class_="prdtPrSt")
        if discounted_price != None:
            normal_price = price_container.find("span", class_="price")
            discounted_price = parse_discounted_price(discounted_price)
            normal_price = parse_normal_price(normal_price)
            if normal_price and discounted_price:
                result.append([normal_price,discounted_price])
    return result


def getDiscountMoyen(url):
    soup = getSoupForURL(url);
    dell_discount = getPricesAndDiscount(soup)
    
    df = pd.DataFrame(dell_discount)
    df.discounts = df[1] - df[0]
    discount_moyen = df.discounts.mean()
    return discount_moyen

if __name__ == "__main__":
    discount_moyen_dell = getDiscountMoyen(URL_DELL)
    discount_moyen_acer = getDiscountMoyen(URL_ACER)
    
    if discount_moyen_acer < discount_moyen_dell:
        print("Le discount moyen pour DELL ({:.2f}€) est supérieur à celui pour ACER ({:.2f}€).".format(discount_moyen_dell,discount_moyen_acer))
    elif discount_moyen_acer > discount_moyen_dell:
        print("Le discount moyen pour ACER ({:.2f}€) est supérieur à celui pour DELL ({:.2f}€).".format(discount_moyen_acer,discount_moyen_dell))
    else:
        print("Les discount moyen pour ACER et pour DELL sont égaux à ({:.2f}€).".format(discount_moyen_acer))

