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
    BASE_URL = "https://nhadat247.com.vn"
    HTM = "htm"
    NUM_URLS = 10000
    post_count = 0
    save_check_point = 50
    get_soup_retry_times = 5

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

    def __init__(self, date_from, date_to, post_type):
        # self.driver = webdriver.Chrome(
        #     executable_path=self.HOME_PATH + self.CHROME_DRIVER,
        #     chrome_options=self.chrome_options)

        self.queue = []
        self.result = []
        self.parser = []
        self.ptype = []
        self.post_type = post_type
        self.status = []

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

    def get_html(self, url):
        """
        Get HTML (page source) of a given url
        """
        # try:
        #     self.driver.get(url)
        #     self.driver.set_page_load_timeout(self.TIMEOUT)
        #     return self.driver.page_source
        # except:
        #     print('Can not access this post-url !!!')
        #     return None
        for i in range(self.get_soup_retry_times):
            try:
                request = urllib.request.Request(url, data=None,
                                                 headers={"User-Agent": "Mozilla/5.0"})  # make web requests for URL
                html = urllib.request.urlopen(request).read()
                return html
            except:
                print('Re-obtain this link')

        print('Can not access this link !!!')
        return None

    def append_data(self, url, parser, ptype, status):
        ""
        self.post_count += 1
        self.parser.append(parser)
        self.ptype.append(ptype)
        self.status.append(status)
        self.result.append(url)
        self.crawl_date.append(date.today().strftime("%d/%m/%Y"))

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
        local_urls = [self.BASE_URL]
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

            soup = self.get_soup(url)
            if soup is None:
                continue
            list_href = soup.find_all('a')

            if re.search(self.regex_post, url):
                _date = None
                try:
                    _date = soup.select_one("#ContentPlaceHolder1_ProductDetail1_divprice > div").get_text()
                    _date = _date.split("|")[1].strip()
                    _date = self.get_date(_date)
                except:
                    continue
                # print(_date)
                if not (self.post_date["from"] <= _date <= self.post_date["to"]):
                    continue

                self.append_data(url, parser="post_nhadat247_com_vn", ptype="post", status="0")

            if self.regex_seller.search(url) and self.post_type == "seller":
                self.append_data(url, parser="seller_nhadat247_com_vn", ptype="seller", status="0")

            for link in list_href:
                anchor = str(link.get('href'))
                if not bool(urlparse(anchor).netloc):
                    anchor = urljoin(self.BASE_URL, anchor)

                if self.regex_post.search(anchor) or self.regex_sub_url.search(anchor) or \
                        (self.regex_seller.search(anchor) and self.post_type == "seller"):

                    if self.check_url(anchor) and self.check_type(anchor):
                        local_urls.append(anchor)

            # check-point to save buffer data
            if len(self.result) == self.save_check_point:
                self.save_tocsv(file_name)

            print("Num ", self.post_count)
            # reach limit number of url then finish
            if self.post_count >= self.NUM_URLS:
                break

        self.save_tocsv(file_name)
        print('CRAWLING DONE')

    def save_tocsv(self, file_name):
        """
        Save to csv
        """
        print("Saving ... ", len(self.result))
        from pathlib import Path
        from csv import writer

        file_name += ".csv"

        my_file = Path(file_name)
        if my_file.is_file():
            # file exists
            print("file exists")
            with open(file_name, 'a') as fd:
                for index in range(len(self.result)):
                    csv_writer = writer(fd)
                    csv_writer.writerow([self.result[index], self.parser[index], self.ptype[index], self.status[index],
                                         self.crawl_date[index]])
                fd.close()
        else:
            print("new file")
            dic = {"Links": self.result,
                   "Parser": self.parser,
                   "Type": self.ptype,
                   "Status": self.status,
                   "Date": self.crawl_date}
            data = pd.DataFrame(dic)
            data.to_csv(file_name, index=False)

        self.result = []
        self.parser = []
        self.ptype = []
        self.status = []
