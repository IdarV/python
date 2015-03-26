__author__ = 'idar'
import requests
import threading
from bs4 import BeautifulSoup
#TODO: get price?

lock = threading.Lock()
lock_list = threading.Lock()
items = set() #standard set
page_nr = 10087 #starting page nr, i.e. #10087 is RAM-page
update = 1


def komplett_spider(max_pages, thread_name):
    print('thread ' + thread_name + 'starting ' + str(max_pages) + ' iterations')
    page = 1
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
    global items
    items.add(name)
    lock_list.release()


def get_page_nr():
    lock.acquire()
    global page_nr
    page_nr += 1
    a = page_nr
    print(str(a) + 'visited by' + threading.current_thread().name)
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
        # Set threads
        t1 = threading.Thread(target=komplett_spider, args=(100, 't1'))
        t2 = threading.Thread(target=komplett_spider, args=(100, 't2'))
        t3 = threading.Thread(target=komplett_spider, args=(100, 't3'))
        t4 = threading.Thread(target=komplett_spider, args=(100, 't4'))
        t5 = threading.Thread(target=komplett_spider, args=(100, 't5'))
        # Make threads daemon
        t1.daemon = False
        t2.daemon = False
        t3.daemon = False
        t4.daemon = False
        t5.daemon = False
        # Start threads
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        # Join threads to main thread
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()


        print('Writing to file..')
        write_to_file(items)
        print("done")
    except:
        print('Error: unable to start thread')


####################################
########## Program start ###########
####################################

start_threads()
