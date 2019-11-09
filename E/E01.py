import requests
from bs4 import BeautifulSoup
import re
import sys


# wyciaganie linkow do podstron podanej strony
def List_of_href_from_page(url, base):
    list = set()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = re.search(r'href=\"([^"]+)\"', str(link))
        if href is not None:
            if re.search(r"^http", href.group(1)) is not None:
                list.add(href.group(1))
            else:
                if base[-1] == "/" and href.group(1)[0] == "/":
                    list.add(get_url(base + href.group(1)[1:]))
                elif base[-1] != "/" and href.group(1)[0] != "/":
                    list.add(get_url(base + href.group(1)))
                else:
                    list.add(get_url(base + "/" + href.group(1)))
    return list

def get_pages_content(url):
    content = ""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    flag = False
    for string in soup.strings:
        if re.search(r"^\n+$", string) is None:
            content += repr(string)[1:-1]
            flag = True
        elif flag:
            content += repr(string)[1:-1]
            flag = False

    return content

def get_url(url):
    return requests.get(url).url

to_visit = set()
visited = set()
links = set()

content = ""
base_url = ""

if len(sys.argv) > 1:
    to_visit.add(sys.argv[1])
    base_url = sys.argv[1]
else:
    to_visit.add("http://rjawor.home.amu.edu.pl/")
    base_url = to_visit[0]

while len(to_visit) > 0:
    for url in to_visit:
        content += get_pages_content(url)
        links.update(List_of_href_from_page(url, base_url))
        visited.add(url)
    with open("page.txt", "a", encoding='utf-8', errors='ignore') as file:
        file.write(content)
    file.close()
    to_visit = set()
    for link in links:
        if link not in visited:
            to_visit.add(link)
