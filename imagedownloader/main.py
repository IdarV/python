
import random
import urllib.request

def download_img_from_url(url):
    name = random.randrange(1, 100000)
    full_name = str(name) + ".jpg"
    urllib.request.urlretrieve(url, full_name)

download_img_from_url("http://i.imgur.com/iqwuY7F.png")
