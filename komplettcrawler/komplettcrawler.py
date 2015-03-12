__author__ = 'idar'
import requests
import threading
from bs4 import BeautifulSoup

lock = threading.Lock()
lock_list = threading.Lock()
items = set()
page_nr = 10087
update = 1


def komplett_spider(max_pages, thread_name):
    print('thread ' + thread_name + 'starting ' + str(max_pages) + ' iterations')
    page = 1
    item = 0
    while page <= max_pages:
        url = "https://www.komplett.no/k/kc.aspx?bn=" + str(get_page_nr())
        print(thread_name + 'Visiting ' + url)
        data = requests.get(url)
        plain_text = data.text

        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('h3'):
            name = str(link.get('title'))
            if name.find("None"):
                add_to_list(name)
        page += 1


def add_to_list(name):
    lock_list.acquire()
    print('Adding ' + name + ' to list')
    items.add(name)
    lock_list.release()


def get_page_nr():
    lock.acquire()
    global page_nr
    page_nr += 1
    a = page_nr
    print(str(a))
    lock.release()
    return a


def add_to_set(item):
    items.add(item)


def write_to_file(item_list):
    file = open("items.txt", "w")
    list_items = list(item_list)
    list_items.sort()
    for item in list_items:
        file.write(item + "\n")


def start_threads():
    try:
        t1 = threading.Thread(target=komplett_spider, args=(5, 't1'))
        t2 = threading.Thread(target=komplett_spider, args=(3, 't2'))
        t1.daemon = False
        t2.daemon = False
        t1.start()
        t2.start()
        t1.join()
        t2.join()


        print('Writing to file..')
        write_to_file(items)
        #_thread.start_new_thread(komplett_spider, (5,w))
        #_thread.start_new_thread(komplett_spider, (3,))
    except:
        print('Error: unable to start thread')



start_threads()
#write_to_file(list(items).sort())
#komplett_spider(1)
