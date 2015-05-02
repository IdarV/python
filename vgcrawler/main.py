__author__ = 'idar'
import requests
import re
from bs4 import BeautifulSoup

url = 'http://www.vg.no/'


# Gets all news headers from ^url
def vg_crawler():
    print('Starting crawling ' + url)
    data = requests.get(url)
    page = data.text
    soup = BeautifulSoup(page)
    print(soup.get_text())
    index = 0
    for title in soup.findAll("div", {"class": "article-content"}):
        name = str(title.get_text()).rstrip()
        if re.search('[a-zA-Z]', name):
            name = " ".join(re.sub(r'[^\w]', ' ', name).split())
            print(str(index) + ') ' + repr(name) + '\n')
            index += 1



# PROGRAM RUN
vg_crawler()