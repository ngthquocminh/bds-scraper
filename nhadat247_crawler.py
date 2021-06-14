import sys
import os
import platform
import json
import re
import hashlib
import urllib

import validators
import pandas as pd
from slugify import slugify
from datetime import datetime, date, timedelta
from time import time
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlsplit
from urllib.parse import urlparse
from urllib.parse import urljoin

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

def soup_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def save_list(data: list, file_name):
    print("Checkpoint: ", file_name)
    with open(file_name, 'w') as file:
        for row in data:
            file.write(str(row) + "\n")
        file.close()

class NhaDat247Crawler(CrawlHTML):
    """
    """

    TIMEOUT = 20
    BASE_URL = "https://nhadat247.com.vn"
    
    HTM = "htm"
    NUM_URLS = 30000
    post_count = 0
    save_check_point = 10
    get_soup_retry_times = 5

    valid_url = re.compile("https[:][/][/]nhadat247[\.]com.vn.*")
    regex_sub_url = re.compile("([a-z][-a-z]*)?ban-[-a-z]+((.html)|(/[0-9]+))?")
    regex_post = re.compile("([a-z][-a-z]*)?ban-[-a-z0-9]+/[-a-z0-9]+pr[0-9]+.html")
    regex_seller = re.compile("xxxxxxxxxxxxx")  # "ban-[-a-z0-9]+/[-a-z0-9]+pr[0-9]+.html"

    CHROME_DRIVER = '\\chrome-driver\\chromedriver.exe'
    HOME_PATH = os.path.abspath(os.getcwd())

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # hide popup
    if platform.system() == "Linux":
        print("Linux chrome")
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        CHROME_DRIVER = '/chrome-driver-linux/chromedriver'
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')

    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/35.0.1916.47 Safari/537.36 '
    }

    def __init__(self, url: list, date_from, date_to, post_type):

        self.queue = []
        self.result = []
        self.parser = []
        self.ptype = []
        self.post_type = post_type
        self.status = []
        self.crawl_date = []
        self.buffer = None
        self.seed_url = url

        date_from = datetime.strptime(date_from, '%d/%m/%Y').date()
        date_to = datetime.strptime(date_to, '%d/%m/%Y').date()

        self.post_date = {"from": date_from, "to": date_to}
        print("init crawler")

    def get_soup(self, url):
        """
        Return Beautifulsoup object
        """
        for i in range(self.get_soup_retry_times):
            try:
                request = urllib.request.Request(url, data=None,
                                                 headers={"User-Agent": "Mozilla/5.0"})  # make web requests for URL
                html = urllib.request.urlopen(request).read()
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

    def get_key_from_type(self, key):
        if key == "nha":
            return ["-nha"]
        if key == "dat":
            return ["-dat"]
        if key in ["canho","chungcu"]:
            return ["can-ho", "chung-cu"]

        return ["-nha", "-dat", "can-ho", "chung-cu"]

    def check_type(self, url):
        list_key = self.get_key_from_type(self.post_type)
        for key in list_key:
            if key in url:
                # print("ok")
                return True

        return False

    def get_html(self, url):
        """
        Get HTML (page source) of a given url
        """

        for i in range(self.get_soup_retry_times):
            try:
                request = urllib.request.Request(url, data=None,
                                                 headers={"User-Agent": "Mozilla/5.0"})  # make web requests for URL
                html = urllib.request.urlopen(request).read()
                return html
            except:
                ""
                print('Re-obtain this link')

        print('Can not access this link !!!')
        return None

    def append_data(self, url, parser, ptype, status, html):
        ""
        self.post_count += 1

        post = {}
        post["url"] = url
        post["parser"] = parser
        post["type"] = ptype
        post["status"] = status
        post["html"] = html.decode("utf-8") 
        post["date"] = str(date.today().strftime("%d/%m/%Y"))

        data = {}
        data[hash(url)] = post

        if isinstance(self.buffer, list):
            self.buffer.append(data)
        else:
            self.buffer = [data]

    def get_date(self, date_str):
        _date = None

        if date_str == "hôm kia":
            _date = date.today() - timedelta(days=2)
        elif date_str == "hôm qua":
            _date = date.today() - timedelta(days=1)
        elif date_str == "hôm nay":
            _date = date.today()
        else:
            _date = datetime.strptime(date_str, '%d/%m/%Y').date()

        return _date

    def obtainData(self, file_name):
        # local_urls = self.seed_url
        local_urls = open("local_urls_log_nha.txt", "r").readlines()
        visited_post = open("visited_post_log_nha.txt", "r").readlines()
        while local_urls:
            url = local_urls.pop(0)
            is_post = re.search(self.regex_post, url)

            if url in visited_post or self.valid_url.search(url) == None:
                continue

            visited_post.append(url)

            try:
                print(" > ", url)
            except:
                pass
            
            

            phtml = self.get_html(url)
            soup = soup_from_html(phtml)
            if soup is None:
                continue
            
            list_href = soup.find_all('a')

            if is_post:
                _date = None
                try:
                    _date = soup.select_one("#ContentPlaceHolder1_ProductDetail1_divprice > div").get_text()
                    _date = _date.split("|")[1].strip()
                    _date = self.get_date(_date)
                except:
                    continue
                if not (self.post_date["from"] <= _date <= self.post_date["to"]):
                    continue

                self.append_data(url, parser="post_nhadat247_com_vn", ptype="post", status="0", html  = phtml)

            if self.regex_seller.search(url) and self.post_type == "seller":
                self.append_data(url, parser="seller_nhadat247_com_vn", ptype="seller", status="0", html  = phtml)

            for link in list_href:
                anchor = str(link.get('href'))

                if not bool(urlparse(anchor).netloc):
                    anchor = urljoin(self.BASE_URL, anchor)
                
                if self.valid_url.search(anchor) == None:
                    continue

                if self.regex_post.search(anchor) or self.regex_sub_url.search(anchor) or \
                        (self.regex_seller.search(anchor) and self.post_type == "seller"):

                    if self.check_url(anchor) and self.check_type(anchor):
                        local_urls.append(anchor)

            # check-point to save buffer data
            if isinstance(self.buffer, list) and len(self.buffer) == self.save_check_point:
                self.save_to_file(file_name)
                save_list(local_urls,"local_urls_log_" + self.post_type + ".txt")
                save_list(visited_post, "visited_post_log_" + self.post_type + ".txt")

            print("Num ", self.post_count)
            # reach limit number of url then finish
            if self.post_count >= self.NUM_URLS:
                break

        self.save_to_file(file_name)
        print('CRAWLING DONE')

    def save_to_file(self, file_name):
        """
        Save to local file
        """
        if not isinstance(self.buffer, list) or len(self.buffer) < 1:
            return 

        print("Saving ... ", len(self.buffer))
        from pathlib import Path
        from csv import writer

        file_name += ".json"

        my_file = Path(file_name)
        if my_file.is_file():
            # file exists
            print("file exists")
            with open(file_name, 'a') as file:
                for row in self.buffer:
                    file.write(json.dumps(row) + "\n")
                file.close()
        else:
            with open(file_name, 'w') as file:
                for row in self.buffer:
                    file.write(json.dumps(row) + "\n")
                file.close()


        self.result = []
        self.parser = []
        self.ptype = []
        self.status = []
        self.html = []
        self.buffer = None
