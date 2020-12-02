import hashlib
import time
import urllib.request
import urllib.request
from datetime import datetime

import os
import pika
import sys
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 '
        'Safari/537.36 '
}


def save_to_elasticsearch(self, url, html):
    """
    Save page source to ElasticSearch
    """
    h = hashlib.md5(url.encode()).hexdigest()
    if not self.es.exists(index='urls', id=h, doc_type='_doc'):
        doc = {
            'url': url,
            'document': str(html),
            'status': 1,
            'crawledDate': datetime.now(),
        }
        self.es.index(index="urls", id=h, body=doc, doc_type='_doc')

def html_parser(url):
    """"""
    request = urllib.request.Request(url, data=None, headers=headers)  # make web requests for URL
    request = urllib.request.urlopen(request)

    pages_soup = BeautifulSoup(request, "lxml")
    title = pages_soup.select_one(".threadview-header--title").get_text()
    price = pages_soup.select_one(".threadview-header--classifiedPrice").get_text()
    sale_location = pages_soup.select_one(".TTC_classifiedMeta dl:nth-child(1) dd").get_text()
    status = pages_soup.select_one(".TTC_classifiedMeta dl:nth-child(2) dd").get_text()
    
    phone = pages_soup.select_one(".threadview-header--contactPhone").get_text()
    saler_address = pages_soup.select_one(".threadview-header--classifiedAddr .address").get_text()
    saler_url = pages_soup.select_one(".threadview-header--seller .username")["href"]
    saler_username = pages_soup.select_one(".threadview-header--seller .username span").get_text()
    saler_infor = (saler_url, saler_username, saler_address)

    return [title,price,sale_location,status,phone,saler_infor]
    
def start_crawling():
    """"""
    url = "https://nhattao.com"
    print("=" * 50, "\n   ", url, "\n", "=" * 50)

    request = urllib.request.Request(url, data=None, headers=headers)  # make web requests for URL
    request = urllib.request.urlopen(request)

    pages_soup = BeautifulSoup(request, "lxml")
 
    li = pages_soup.find("ul", {"class": "blockLinksList Nhattao-QuickNav NhattaoMods_DrawerContent"}).findAll("a")
    li.pop(0)
    li.pop(-1)
    li.pop(-1)
    li = [i['href'] for i in li]

    uli = "?type=recent&search_id=123456789&order=up_time&direction=desc"
    ipage = "page-"  # page-1
    url_list = []
    for subli in li:
        subli = url + subli
        print("\n", "-" * 40, "\n", subli, "\n")
        request = None
        try:
            request = urllib.request.Request(subli, data=None, headers=headers)
            request = urllib.request.urlopen(request)
        except:
            continue
        time.sleep(3)

        pages_soup = BeautifulSoup(request, "lxml")
        category = pages_soup.select_one(".media__body h1").get_text()
        print(category)
        for index in range(1, int(pages_soup.select_one(".pageNavHeader").get_text().split("/")[-1]) + 1):
            items_page_url = subli + ipage + str(index) + uli
            print("\n >>>", items_page_url)
            request = None
            try:
                request = urllib.request.Request(items_page_url, data=None, headers=headers)
                request = urllib.request.urlopen(request)
            except:
                continue

            time.sleep(3)

            pages_soup = BeautifulSoup(request, "lxml")

            url_page_list = [(category, url + "/" + a_tag["href"]) for a_tag in
                             pages_soup.select(".Nhattao-CardList .Nhattao-CardItem .Nhattao-CardItem--inner a")]
            url_list.extend(url_page_list)
            print(url_page_list)
            list_info = [html_parser(_url) for _url in url_page_list]
            print(list_info)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        start_crawling()

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    # start_crawling()
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
