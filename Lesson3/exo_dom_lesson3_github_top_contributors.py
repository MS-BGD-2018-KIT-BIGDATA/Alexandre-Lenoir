'''
Created on Oct 4, 2017

@author: alex
'''

from bs4 import BeautifulSoup
import requests
import json
from secret.secretstore import TOKEN
import pandas as pd
from multiprocessing import Pool


def getRepositoriesOfUser(user):
    request_link = "https://api.github.com/users/" + user + "/repos"
    repo_count = 0
    repo_watchers = 0
    while request_link:
        content = requests.get(request_link, headers={
                               'Authorization': 'token ' + TOKEN})
        if content.status_code == 200:
            repositories = json.decoder.JSONDecoder().decode(content.text)
            repo_count += len(repositories)
            for reposotory in repositories:
                repo_watchers += reposotory['stargazers_count']
        else:
            print("Request failed with status " + str(content.status_code))
            content = requests.get("https://api.github.com/rate_limit", headers={
                                   'Authorization': 'token ' + TOKEN})
            data = json.decoder.JSONDecoder().decode(content.text)
            print(data)
        if content.links and 'next' in content.links:
            request_link = content.links['next']['url']
        else:
            request_link = None
    return repo_count, repo_watchers


def scrap_github(arguments):
    rank, contributor = arguments
    repo_count, repo_watchers = getRepositoriesOfUser(contributor['name'])
    print("Contributor <{}> ranked {} owns {} repositories with an average star count of {:.2f}.".format(
        contributor['name'], rank + 1, repo_count, repo_watchers / repo_count if repo_count != 0 else 0))
    return [contributor['name'], repo_count, repo_watchers]


def main():
    TOP_CONRTIBUTOR_URL = "https://gist.github.com/paulmillr/2657075"
    content = requests.get(TOP_CONRTIBUTOR_URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    table_entries = soup.find_all("tr", limit=257)
    top_contributors = []
    for i in range(1, 8):
        link = table_entries[i].find("a")
        url = link.get("href")
        name = link.string
        top_contributors.append({'name': name, 'url': url})

    df = []
    input_data = [(rank, contributor)
                  for rank, contributor in enumerate(top_contributors)]
    for single_data in input_data:
        df.append(scrap_github(single_data))

    df = pd.DataFrame(data=df, columns=["name", "repo_count", "repo_watchers"])
    df.to_csv("contributors.csv")
    df['average_watchers'] = df['repo_watchers'] / df['repo_count']
    df = df.sort_values(by='average_watchers', ascending=False)
    print(df.head())


if __name__ == '__main__':
    main()
