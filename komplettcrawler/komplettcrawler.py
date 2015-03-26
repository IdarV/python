__author__ = 'idar'
import requests
import threading
from bs4 import BeautifulSoup

lock = threading.Lock()
lock_list = threading.Lock()
items = set()
page_nr = 1000
# update = 1


def komplett_spider(max_pages, thread_name):
    print('thread ' + thread_name + 'starting ' + str(max_pages) + ' iterations')
    page = 1
    while page <= max_pages:
        url = "https://www.komplett.no/k/kc.aspx?bn=" + str(get_page_nr())
        print(thread_name + ' visiting ' + url)
        data = requests.get(url)
        plain_text = data.text

        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('h3'):
            name = str(link.get('title'))
            # Why is this counter intuitive?
            if name.find("None"):
                add_to_list(name)
        page += 1


def add_to_list(name):
    lock_list.acquire()
    print('Adding ' + name + ' to list')
    global items
    items.add(name)
    lock_list.release()


def get_page_nr():
    lock.acquire()
    global page_nr
    page_nr += 1
    a = page_nr
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
    number_of_threads = 3
    number_of_visits = 5
    target_method = komplett_spider
    threads = []
    for x in range(0, number_of_threads):
        threads.append(threading.Thread(target=target_method, args=(number_of_visits, ('t' + str(x)))))
    try:
        for thr in threads:
            thr.daemon = False
            thr.start()
        for thr in threads:
            thr.join()
    except:
        print('Error: unable to start thread')

    print('Writing to file..')
    write_to_file(items)
    print("done")


####################################
########## Program start ###########
####################################
start_threads()
