import sys
import os
import platform
import json
import re
import hashlib
import urllib
import traceback

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
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import selenium.common.exceptions
from selenium.webdriver import ActionChains

from crawl import CrawlHTML

def save_list(data: list, file_name):
    print("Checkpoint: ", file_name)
    with open(file_name, 'w') as file:
        for row in data:
            file.write(str(row) + "\n")
        file.close()

class BatDongSanCrawler(CrawlHTML):
    """
    """

    TIMEOUT = 10
    BASE_URL = "https://batdongsan.com.vn/"
    
    HTM = "htm"
    NUM_URLS = 30000
    post_count = 0
    save_check_point = 100
    get_soup_retry_times = 5

    CHROME_DRIVER = '\\chrome-driver\\chromedriver.exe'
    HOME_PATH = os.path.abspath(os.getcwd())

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # hide popup
    if platform.system() == "Linux":
        print("Linux chrome")
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        CHROME_DRIVER = '/chrome-driver-linux/chromedriver'
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')

    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/35.0.1916.47 Safari/537.36 '
    }

    def __init__(self, url: list, date_from, date_to, post_type):
        self.driver = self.init_browser_driver()
        self.queue = []
        self.result = []
        self.parser = []
        self.ptype = []
        self.post_type = post_type
        self.status = []
        self.crawl_date = []
        self.buffer = None
        self.seed_url = url
    
        # self.valid_url = re.compile("https[:][/][/]batdongsan[\.]com[\.]vn.+")
        self.regex_sub_url = re.compile("https[:][/][/]batdongsan[\.]com[\.]vn/ban-[-a-z0-9]+(/p[0-9]+)?")
        self.regex_post = re.compile("https[:][/][/]batdongsan[\.]com[\.]vn/ban-[-a-z0-9]+/[-a-z0-9]+pr[0-9]+")

        date_from = datetime.strptime(date_from, '%d/%m/%Y').date()
        date_to = datetime.strptime(date_to, '%d/%m/%Y').date()

        self.key_type = self.get_key_from_type(self.post_type)

        self.post_date = {"from": date_from, "to": date_to}
        print("init crawler")

    def init_browser_driver(self):
        return webdriver.Chrome(
            executable_path=self.HOME_PATH + self.CHROME_DRIVER,
            chrome_options=self.chrome_options)

    def get_html_and_soup(self, url):
        """
        Return Beautifulsoup object
        """
        _soup = None
        _html = None
        for i in range(self.get_soup_retry_times):
            try:                  
                _html = self.get_html(url)
                _soup = BeautifulSoup(_html, 'html.parser')
                if _soup is not None:
                    break
            except Exception as e: 
                traceback.print_exc()
                continue

        return _html, _soup

    def get_key_from_type(self, key):
        if key == "dat":
            return ["ban-dat"]
        if key in ["canho","chungcu"]:
            return ["ban-can-ho-chung-cu"]
        if key == "nhapho_biethu":
            return ["ban-nha-mat-pho", "ban-nha-biet-thu"]
        if key == "nharieng":
            return ["ban-nha-rieng"]

        return ["ban-dat", "ban-can-ho  -chung-cu", "ban-nha-rieng", "ban-nha-mat-pho", "ban-nha-biet-thu"]

    def check_type(self, url):
        for key in self.key_type:
            if key in url:
                # print("ok")
                return True

        return False

    def get_html(self, url):
        """
        Get HTML (page source) of a given url
        """
        html = ""
        driver_error = True # default True allows code to enter while

        retries_time = 4
        count_retry = 0
        while driver_error:
            try:
                self.driver.get(url)
                
                element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/footer"))
                WebDriverWait(self.driver, self.TIMEOUT).until(element_present)
                
                html = self.driver.page_source
                driver_error = False

            except Exception as e: 
                traceback.print_exc()
                if count_retry >= 5:
                    break
                driver_error = True
                count_retry += 1
                if "not reachable" in repr(e) or "no such window" in repr(e):
                    self.driver = self.init_browser_driver()
                else:
                    "others"
                    break

        return html

    def append_data(self, url, parser, ptype, status, html):
        ""
        self.post_count += 1

        post = {}
        post["url"] = url
        post["parser"] = parser
        post["type"] = ptype
        post["status"] = status
        post["html"] = html
        post["date"] = str(date.today().strftime("%d/%m/%Y"))

        data = {}
        data[hash(url)] = post

        if isinstance(self.buffer, list):
            self.buffer.append(data)
        else:
            self.buffer = [data]

    def get_date(self, date_str):
        _date = datetime.strptime(date_str, '%d/%m/%Y').date()
        return _date

    def obtainData(self, file_name):
        print("START...")
        # local_urls = self.seed_url
        local_urls = open("local_urls_log_batdongsan_" + self.post_type + ".txt", "r").readlines()
        visited_post = open("visited_post_log_batdongsan_"+ self.post_type + ".txt", "r").readlines()
        while local_urls:
            url = local_urls.pop(0)
        
            if len(url) < 10 and (url in visited_post or not self.check_type(url)):
                continue
            
            print(" > ", url)

            visited_post.append(url)

  
            _html, _soup = self.get_html_and_soup(url)

            if _soup is None:
                continue

            is_post = re.search(self.regex_post, url)
            if is_post:
                _date = None
                try:
                    _date = _soup.select_one("#product-detail-web > div.detail-product > div.product-config.pad-16 > ul > li:nth-child(1) > span.sp3").get_text()
                    _date = _date.strip()
                    _date = self.get_date(_date)
                except Exception as e: 
                    traceback.print_exc()
                    continue

                if not (self.post_date["from"] <= _date <= self.post_date["to"]):
                    continue

                self.append_data(url, parser="post_batdongsan_com_vn", ptype="post", status="0", html  = _html)
                # print(_date)

            list_href = _soup.find_all('a')

            for link in list_href:
                anchor = str(link.get('href'))
                if not bool(urlparse(anchor).netloc):
                    anchor = urljoin(self.BASE_URL, anchor)

                # print(anchor)
                if validators.url(anchor) and self.check_type(anchor) and (self.regex_post.search(anchor) or self.regex_sub_url.search(anchor)):
                    local_urls.append(anchor)

            # check-point to save buffer data
            if isinstance(self.buffer, list) and len(self.buffer) == self.save_check_point:
                self.save_to_file(file_name)
                save_list(local_urls,"local_urls_log_batdongsan_" + self.post_type + ".txt")
                save_list(visited_post, "visited_post_log_batdongsan_" + self.post_type + ".txt")

            print("      num ", self.post_count)
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
