__author__ = 'idar'
import requests
import re
from bs4 import BeautifulSoup

url = 'http://www.vg.no/'

def vg_crawler():
    print('Starting crawling ' + url)
    data = requests.get(url)
    page = data.text
    soup = BeautifulSoup(page)
    print(soup.get_text())
    index = 0
    for title in soup.findAll("div", {"class": "article-content"}):
        name = str(title.get_text()).strip().rstrip()
        if re.search('[a-zA-Z]', name):
            print(str(index) + ') ' + name + '\n')
            index += 1



# PROGRAM RUN
vg_crawler()