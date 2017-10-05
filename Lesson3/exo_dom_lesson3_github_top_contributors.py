'''
Created on Oct 4, 2017

@author: alex
'''

from bs4 import BeautifulSoup
import requests
import json
from secret.secretstore import TOKEN

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
    return repo_count, repo_watchers / repo_count


def main():
    TOP_CONRTIBUTOR_URL = "https://gist.github.com/paulmillr/2657075"
    content = requests.get(TOP_CONRTIBUTOR_URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    table_entries = soup.find_all("tr", limit=257)
    top_contributors = []
    for i in range(1, 257):
        link = table_entries[i].find("a")
        url = link.get("href")
        name = link.string
        top_contributors.append({'name': name, 'url': url})

    for rank, contributor in enumerate(top_contributors):
        repo_count, average_watchers = getRepositoriesOfUser(
            contributor['name'])
        print("Contributor <{}> ranked {} owns {} repositories with an average star count of {:.2f}.".format(
            contributor['name'], rank + 1, repo_count, average_watchers))


if __name__ == '__main__':
    main()
