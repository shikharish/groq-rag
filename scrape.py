import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


all_links = set()


def get_all_absolute_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            if href:
                absolute_url = urljoin(url, href)
                print(absolute_url)
                all_links.add(absolute_url)


urls = [
    "https://wiki.metakgp.org/w/Main_Page",
    "https://wiki.metakgp.org/w/Category:Halls_of_Residence",
    "https://wiki.metakgp.org/w/Category:Food_and_Beverages",
    "https://wiki.metakgp.org/w/Category:Academics",
    "https://wiki.metakgp.org/w/Category:Departments",
    "https://wiki.metakgp.org/w/Category:Societies_and_clubs",
    "https://wiki.metakgp.org/w/List_of_how-tos",
]

for url in urls:
    get_all_absolute_links(url)

list_links = list(all_links)
with open("links.json", "w") as file:
    json.dump(list_links, file, indent=4)
