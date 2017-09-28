'''
Created on Sep 25, 2017

@author: alexandre
'''
import unittest

from bs4 import BeautifulSoup as bs, BeautifulSoup
import requests
import numpy as np

"""
 Reports are read from URLs of the kind
 
 http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013
 
 exercise is a useful parameter. Maybe dep is useful

"""


class Test(unittest.TestCase):

    def testName(self):
        pass


URL_TEMPLATE = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=%0"


def getSoupForYear(year):
    URL = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice={0}".format(
        year)
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    return soup


def getStratesValues(soup, indices):
    result = []
    for index in indices:
        value = soup.select(
            "body > table:nth-of-type(3) > tr:nth-of-type({}) > td:nth-of-type(2)".format(index))
        result.append(int(value[0].text))
    return result


def buildHeader(soup, descriptors):
    result = []
    DONT_ = "dont : "
    for descriptor in descriptors:
        for index in descriptor[1]:
            value = soup.select(
                "body > table:nth-of-type(3) > tr:nth-of-type({}) > td:nth-of-type(4)".format(index))
            result.append(descriptor[0] + " : " + (value[0].text if value[0].text.find(
                DONT_) == -1 else value[0].text[len(DONT_):]))
    return u", ".join(["Année"] + result)


if __name__ == "__main__":
    A_LINES = ("A", [7, 8, 9])
    B_LINES = ("B", [11, 12, 13, 14, 15])
    C_LINES = ("C", [19, 20, 21, 22])
    D_LINES = ("D", [24, 25, 26, 27])

    header_ = None
    data_frame = []
    for year in range(2010, 2016):
        soup = getSoupForYear(year)
        if not header_:
            header_ = buildHeader(soup, [A_LINES, B_LINES, C_LINES, D_LINES])
        a_values = getStratesValues(soup, A_LINES[1])
        b_values = getStratesValues(soup, B_LINES[1])
        c_values = getStratesValues(soup, C_LINES[1])
        d_values = getStratesValues(soup, D_LINES[1])
        data_frame.append([year] + a_values + b_values + c_values + d_values)

    array = np.asarray(data_frame)
    np.savetxt("scraped-paris.csv", data_frame, header=header_,fmt="%d", delimiter=",")
