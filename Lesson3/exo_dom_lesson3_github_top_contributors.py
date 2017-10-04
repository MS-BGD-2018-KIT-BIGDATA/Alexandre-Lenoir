'''
Created on Oct 4, 2017

@author: alex
'''

from bs4 import BeautifulSoup
import requests
import json

def getRepositoriesOfUser(user):
    content = requests.get("https://api.github.com/users/"+user+"/repos")
    watchers = 0;
    if content.status_code == 200:
        data = json.decoder.JSONDecoder().decode(content.text)
        print(len(data))
        
        for repo in data:
            watchers += repo['stargazers_count']
        print("average watchers for user " +user + " : " + str(watchers/len(data)))
    else:
        print("Request failed with status " + str(content.status_code))
        content = requests.get("https://api.github.com/rate_limit")
        data = json.decoder.JSONDecoder().decode(content.text)
        print(data)


def main():
    TOP_CONRTIBUTOR_URL = "https://gist.github.com/paulmillr/2657075"
    content = requests.get(TOP_CONRTIBUTOR_URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    # Xpath of the first table entry is "/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/article/table/tbody/tr[1]/td[1]"    
    table_entries = soup.find_all("tr",limit=257)
    top_contributors = []
    for i in range(1,257):
        link = table_entries[i].find("a")
        url = link.get("href")
        name = link.string;
        top_contributors.append([name,url])
        
    for contributor in top_contributors:
        getRepositoriesOfUser(contributor[0])

if __name__ == '__main__':
    main()