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


class BatDongSanCrawler(CrawlHTML):
    """
    """
    
    TIMEOUT = 10
    BASE_URL = "https://nhadat247.com.vn/"
    HTM = "htm"
    NUM_URLS = 5
    post_count = 0

    get_soup_retry_times = 5

    regex_sub_url = "ban-[-a-z]((.html)|(/[0-9]+))?"
    regex_post = "ban-[-a-z0-9]+/[-a-z0-9]+pr[0-9]+.html"
    regex_seller = "xxxxxxxxxxxxx" # "ban-[-a-z0-9]+/[-a-z0-9]+pr[0-9]+.html"

    CHROME_DRIVER = '\\chrome-driver\\chromedriver.exe'
    HOME_PATH = os.path.abspath(os.getcwd())

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # hide popup
    if platform.system() == "Linux":
        chrome_options.binary_location = '/usr/bin/google-chrome'
        CHROME_DRIVER = '/chrome-driver-linux/chromedriver'
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')

    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/35.0.1916.47 Safari/537.36 '
    }

    def __init__(self, date_from, date_to, post_type):
        self.driver = webdriver.Chrome(
            executable_path=self.HOME_PATH + self.CHROME_DRIVER,
            chrome_options=self.chrome_options)

        self.queue = []
        self.result = []
        self.parser = []
        self.type = []
        self.post_type = post_type
        self.status = []
        
        date_from = datetime.strptime(date_from, '%d/%m/%Y').date()
        date_to = datetime.strptime(date_to, '%d/%m/%Y').date()

        self.post_date = {"from":date_from, "to":date_to}
        print("init crawler")

    def set_connection(self, url):
        """
        Return Beautifulsoup object
        """
        for i in range(self.get_soup_retry_times):
            try:
                request = urllib.request.Request(url, data=None, headers = {"User-Agent": "Mozilla/5.0"})  # make web requests for URL
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
        if key == "can-ho/chung-cu":
            return ["can-ho","chung-cu"]
        
        return ["-nha","-dat","can-ho","chung-cu"]

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
        try:
            self.driver.get(url)
            self.driver.set_page_load_timeout(self.TIMEOUT)
            return self.driver.page_source
        except:
            print('Can not access this post-url !!!')
            return None

    def obtainData(self, file_name):
        local_urls = [self.BASE_URL]
        visited_post = []
        while local_urls:
            url = local_urls.pop(0)
            if url in self.result or url in visited_post:
                continue

            visited_post.append(url)

            try:
                # print('-' * 10, 'STARTING TO CONSIDER THE URL', '-' * 10)
                print(" > ", url)
                print("Num ", self.post_count)
            except:
                pass

            soup = self.set_connection(url)
            if soup is None:
                continue

            if re.search(self.regex_post, url):
                # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                _date = None
                # print(soup.find("div",{"id":"ContentPlaceHolder1_ProductDetail1_divprice"}))
                try:
                    _date = soup.select_one("#ContentPlaceHolder1_ProductDetail1_divprice > div").get_text()
                    _date = _date.split("|")[1].strip()
                except:
                    continue

                if _date == "hôm kia":
                    _date = date.today() - timedelta(days=2)
                elif _date == "hôm qua":
                    _date = date.today() - timedelta(days=1)
                elif _date == "hôm nay":
                    _date = date.today()                    
                else:
                    try:
                        _date = datetime.strptime(_date, '%d/%m/%Y').date()
                    except:
                        continue
     
                # print(_date, " - ", self.post_date)
                if _date >= self.post_date["from"] and _date <= self.post_date["to"]:
                    self.post_count += 1
                    self.parser.append("post_nhadat247_com_vn")
                    self.type.append("post")
                    self.status.append("0")             
                    self.result.append(url)



            if re.search(self.regex_seller, url) and self.post_type == "seller":
                self.post_count += 1
                self.parser.append("seller_nhadat247_com_vn")
                self.type.append("seller") 
                self.status.append("0")             
                self.result.append(url)

            for link in soup.find_all('a'):
                # print(link)
                anchor = str(link.get('href'))
                if re.search(self.regex_post, anchor) \
                        or re.search(self.regex_sub_url, anchor) \
                        or (re.search(self.regex_seller, anchor) and self.post_type == "seller"):
                    if not self.check_url(anchor):
                        anchor = self.BASE_URL + ("/" if not anchor[0] == "/" else "") + anchor
                        # print("Anchor post", anchor)
                    if self.check_url(anchor) and self.check_type(anchor):
                        local_urls.append(anchor)
                        # print("post ", anchor)
            
            # may be higher because we set it here
            if self.post_count >= self.NUM_URLS:
                break

        print('CRAWLING DONE')
        self.save_tocsv(file_name) 

    def save_tocsv(self, file_name):
        """
        Save to csv
        """
        dic = {"Links": self.result, "Parser": self.parser, "Type": self.type, "Status": self.status}
        data = pd.DataFrame(dic)
        data.to_csv(file_name+'.csv', index=False)
        print('TASK DONE')

