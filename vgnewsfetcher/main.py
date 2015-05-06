__author__ = 'idar'
import requests
import re
from bs4 import BeautifulSoup

url = 'http://www.vg.no/'


# Gets all news headers from ^url
def vg_crawler():
    data = requests.get(url)
    page = data.text
    soup = BeautifulSoup(page)
    index = 0

    for title in soup.findAll("div", {"class": "article-content"}):
        # Strip name for newlines
        name = str(title.get_text()).rstrip()
        if re.search('[a-zA-Z]', name):
            # Remove all non-letters and unnecessary whitespaces
            name = " ".join(re.sub(r'[^\w]', ' ', name).split())
            # Print and increase index
            print(str(index) + ') ' + name + '\n')
            index += 1



# PROGRAM RUN
vg_crawler()