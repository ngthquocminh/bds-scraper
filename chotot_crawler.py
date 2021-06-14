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
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
# LOGGER.setLevel(logging.WARNING)


def soup_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

class ChototCrawler():
    """
    """

    TIMEOUT = 10
    BASE_URL = "https://nha.chotot.com"
    HTM = "htm"
    NUM_URLS = -1
    post_count = 0
    save_check_point = 10
    get_soup_retry_times = 5

    regex_sub_url = re.compile("([a-z][-a-z]*)?ban-[-a-z]+((.htm)|(/[0-9]+))?")
    regex_post = re.compile("([a-z][-a-z]+)?[/][a-z][-a-z0-9]+/[-a-z0-9]+.htm")
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
    chrome_options.add_argument('--log-level=OFF')
    
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/35.0.1916.47 Safari/537.36 '
    }

    def __init__(self, url: list, date_from, date_to, post_type):
        self.driver = webdriver.Chrome(
            executable_path=self.HOME_PATH + self.CHROME_DRIVER,
            chrome_options=self.chrome_options)

        self.queue = []
        self.result = []
        self.parser = []
        self.ptype = []
        self.post_type = post_type
        self.status = []
        self.crawl_date = []
        self.html = []
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
        if key == "can-ho/chung-cu":
            return ["can-ho", "chung-cu"]

        return ["-nha", "-dat", "can-ho", "chung-cu"]

    def check_type(self, url):
        list_key = self.get_key_from_type(self.post_type)
        for key in list_key:
            if key in url:
                # print("ok")
                return True

        return False

    def get_html(self, url, is_post):
        """
        Get HTML (page source) of a given url
        """
        for i in range(self.get_soup_retry_times):
            try:
                self.driver.get(url)

                element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div/div[4]/div[5]/div[1]"))
                WebDriverWait(self.driver, self.TIMEOUT).until(element_present)

            except:
                # print('Can not access this post-url !!!')
                continue
            finally:
                if is_post:
                    click_phone_script = """
                        function getElementByXpath(path) {
                            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        }

                        var phone = getElementByXpath("/html/body/div[1]/div/div[1]/div/div[4]/div[3]/div/linkcontact/span");
                        if (phone != null) {
                            phone.click();
                        }                    
                    """
                    self.driver.execute_script(click_phone_script)

                return self.driver.page_source

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
        post["html"] = html
        post["date"] = date.today().strftime("%d/%m/%Y")

        data = {}
        data[hash(url)] = post

        if isinstance(self.buffer, list):
            self.buffer.append(data)
        else:
            self.buffer = [data]

    def get_date(self, date_str):
        _date = None

        date_str = slugify(date_str.lower())
        _l = date_str.split("-")
        if "hom-qua" in date_str:
            _date = date.today() - timedelta(days=1)
        elif "thang" in _l:
            _n = int(_l[_l.index("thang") - 1][0])
            _date = date.today() - timedelta(days=30*_n)
        elif "tuan" in _l:
            _n = int(_l[_l.index("tuan") - 1][0])
            _date = date.today() - timedelta(days=7*_n)
        elif "ngay" in _l:
            _n = int(_l[_l.index("ngay") - 1][0])
            _date = date.today() - timedelta(days=1)
        elif "hom-nay" in date_str or "gio" in _l or "phut" in _l:
            _date = date.today()
        else:
            _date = datetime.strptime(date_str, '%d/%m/%Y').date()

        return _date

    def obtainData(self, file_name):
        local_urls = self.seed_url
        visited_post = []
        while local_urls:
            url = local_urls.pop(0)
            if url in visited_post:
                continue

            visited_post.append(url)

            try:
                print(" > ", url)
            except:
                pass
            is_post = re.search(self.regex_post, url)
            
            phtml = self.get_html(url, is_post)
            soup = soup_from_html(phtml)
            if soup is None:
                continue
            
            list_href = soup.find_all('a')

            if is_post:
                _date = None
                try:
                    _date = soup.select_one("#__next > div > div.ct-detail.adview > div > div.col-md-8 > div.adImageWrapper___KTd-h > div.imageCaption___cMU2J > span").get_text()
                    _date = re.sub("(<!--.*?-->)", "", _date, flags=re.DOTALL)
                    _date = self.get_date(_date)
                except:
                    continue

                if not (self.post_date["from"] <= _date <= self.post_date["to"]):
                    continue

                self.append_data(url, parser="post_chotot", ptype="post", status="0", html = phtml)

            if self.regex_seller.search(url) and self.post_type == "seller":
                self.append_data(url, parser="seller_chotot", ptype="seller", status="0", html  = phtml)

            for link in list_href:
                anchor = str(link.get('href'))
                if not bool(urlparse(anchor).netloc):
                    anchor = urljoin(self.BASE_URL, anchor)

                if self.regex_post.search(anchor) or self.regex_sub_url.search(anchor) or \
                        (self.regex_seller.search(anchor) and self.post_type == "seller"):

                    if self.check_url(anchor) and self.check_type(anchor):
                        local_urls.append(anchor)

            # check-point to save buffer data
            if isinstance(self.buffer, list) and len(self.buffer) == self.save_check_point:
                self.save_to_file(file_name)

            print("Num ", self.post_count)
            # reach limit number of url then finish
            if self.post_count >= self.NUM_URLS and self.NUM_URLS > 0:
                break

        self.save_to_file(file_name)
        print('CRAWLING DONE')

    def save_to_file(self, file_name):
        """
        Save to local file
        """
        if not isinstance(self.buffer, list):
            return

        print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n Saving ... ", len(self.result))
        from pathlib import Path

        file_name += ".json"

        my_file = Path(file_name)

        if my_file.is_file():
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

