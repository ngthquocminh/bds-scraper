import sys
import os
import json
import re
import hashlib
import urllib

import validators
import pandas as pd
from slugify import slugify
from time import time
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlsplit
from urllib.parse import urlparse
from urllib.parse import urljoin
from elasticsearch import Elasticsearch

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import selenium.common.exceptions
from selenium.webdriver import ActionChains

from crawl import CrawlHTML


class NhatTaoCrawler(CrawlHTML):
    """
    Crawl HTML of given links and also crawl all
    possible links which are not in given list
    @param queue is the provided list which is sent to queue
    @param result is list of all post links
    @param post_count is the number of post urls
    @param nonpost_count is the number of crawled non-post urls
    @param es is the ElasticSearch object
    """
    TIMEOUT = 10
    BASE_URL = "https://nhattao.com"
    HTM = "htm"
    NUM_URLS = 10
    SAVE_TO_ES = True  # to save to ES -> True
    post_count = 0

    get_soup_retry_times = 5

    regex_sub_url = "f/[-a-z0-9]+[.][0-9]+/"
    regex_post = "threads/[-a-z0-9]+[.][0-9]+/"
    regex_seller = "members/[-a-z0-9]+[.][0-9]+/"

    CHROME_DRIVER = 'chrome-driver\\chromedriver.exe'
    HOME_PATH = os.path.abspath(os.getcwd())

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # hide popup
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')

    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/35.0.1916.47 Safari/537.36 '
    }

    def __init__(self, given_list):
        self.driver = webdriver.Chrome(
            executable_path=self.HOME_PATH + "\\" + self.CHROME_DRIVER,
            chrome_options=self.chrome_options)

        self.queue = []
        self.result = []
        self.html = []
        self.parser = []
        self.es = Elasticsearch()
        print("init crawler")
        self.main()

    def set_connection(self, url):
        """
        Return Beautifulsoup object
        """
        for i in range(self.get_soup_retry_times):
            try:
                request = urllib.request.Request(url, data=None, headers=self.headers)  # make web requests for URL
                html = urllib.request.urlopen(request)
                soup = BeautifulSoup(html, 'html.parser')
                return soup
            except:
                print('Re-obtain this link')

        print('Can not access this link !!!')
        return None

    def check_if_url_is_post(self, url):
        """
        Check whether an url is post url (the last level url) or not
        """
        pass

    def check_url(self, url):
        """
        Check whether an url is valid or not
        """
        return validators.url(url)

    def get_html(self, url):
        """
        Get HTML (page source) of a given url
        """
        try:
            self.driver.get(url)
            self.driver.set_page_load_timeout(self.TIMEOUT)
            return self.driver.page_source
        except:
            print('Can not access this post-url !!!')
            return None

    def main(self):

        """
        Set driver
        Step 1: Start with a queue of urls, retrieve the first one
        Step 2: Check this url is valid or not
        Step 3: Set connection and retrieve html of this url
        Step 4: Extract all urls from the content of the origin url
        Step 5: Check every urls which have already extracted,
        - Case 1: if this url is post url, check if it exist in result or not and add to this list
        - Case 2: It is not post url, check if it exists in queue or not, add to queue
        Step 6: Delete origin url and all checked urls
        Step 7: Check queue is empty or not come back to Step 1
        """

        local_urls = [self.BASE_URL]
        visited_post = []
        while local_urls:
            url = local_urls.pop(0)
            if url in self.result or url in visited_post:
                continue

            visited_post.append(url)

            try:
                print('-' * 10, 'STARTING TO CONSIDER THE URL', '-' * 10)
                print(" > ", url)
                print("Num ", self.post_count)
            except:
                pass

            soup = self.set_connection(url)
            if soup is None:
                continue

            if re.search(self.regex_post, url):
                self.post_count += 1
                parser = slugify(soup.find_all("span", {"itemprop": "title"})[2].text).replace("-", "_")
                if self.SAVE_TO_ES:
                    self.save_to_elasticsearch("item", url, str(soup), parser)
                else:
                    self.result.append(url)
                    self.parser = parser
                    self.html.append(str(soup))
            elif re.search(self.regex_seller, url):
                if self.SAVE_TO_ES:
                    self.save_to_elasticsearch("seller", url, str(soup), "seller")
                else:
                    self.result.append(url)
                    self.parser = parser
                    self.html.append(str(soup))

            for link in soup.find_all('a'):
                anchor = str(link.get('href'))
                if re.search(self.regex_post, anchor) \
                        or re.search(self.regex_sub_url, anchor) \
                        or re.search(self.regex_seller, anchor):
                    if not self.check_url(anchor):
                        anchor = self.BASE_URL + ("/" if not anchor[0] == "/" else "") + anchor
                        # print("Anchor post", anchor)
                    if self.check_url(anchor):
                        local_urls.append(anchor)
                        # print("post ", anchor)

            # may be higher because we set it here
            if self.post_count >= self.NUM_URLS:
                break

        print('CRAWLING DONE')
        self.save_tocsv()

    def save_tocsv(self):
        """
        Save to csv, but it is not recommended
        """
        dic = {"Links": self.result, "HTML": self.html, "Parser": self.parser}
        data = pd.DataFrame(dic)
        data.to_csv('post_urls_1.csv')
        print('TASK DONE')

    def save_to_elasticsearch(self, _type, url, html, config):
        """
        Save page source to ElasticSearch
        """
        h = hashlib.md5(url.encode()).hexdigest()
        if not self.es.exists(index='urls', id=h, doc_type='_doc'):
            doc = {
                'type': _type,
                'url': url,
                'document': str(html),
                'parser_config': config,
                'status': 1,
                'crawled_date': datetime.now(),
            }
            try:
                self.es.index(index="urls", id=h, body=doc, doc_type='_doc')
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)
