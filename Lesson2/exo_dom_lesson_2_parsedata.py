'''
Created on Sep 25, 2017

@author: alexandre
'''
import unittest

from bs4 import BeautifulSoup as bs, BeautifulSoup
import requests

"""
 Reports are read from URLs of the kind
 
 http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013
 
 exercice is a useful parameter. Maybe dep is useful

"""

class Test(unittest.TestCase):


    def testName(self):
        pass

URL_TEMPLATE = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=%0"

def getSoupForYear(year):
    URL = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice={0}".format(year)
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    return soup



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    for year in range(2010,2016):
        soup = getSoupForYear(year)
    