import re
import sys

import pandas as pd
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from lxml import etree, html
from lxml.etree import ElementTree as ET
from lxml.etree import tostring
from itertools import chain
from os import listdir
from parse import ParseHTML
from slugify import slugify
import json

import hashlib
import urllib

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
LOGGER.setLevel(logging.WARNING)


class   BatDongSanParser(ParseHTML):

    MODEL_PATH = "config/"
    POST_LIMIT = 100
    BASE_URL = "https://nhadat247.com.vn/"

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
    chrome_options.add_argument("--log-level=3")

    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/35.0.1916.47 Safari/537.36 '
    }


    def __init__(self, name_get, name_save):
        
        self.driver = webdriver.Chrome(
            executable_path=self.HOME_PATH + self.CHROME_DRIVER,
            chrome_options=self.chrome_options)
        
        self.name_get = name_get
        self.name_save = name_save
        self.es = Elasticsearch()
        self.result = dict()

    def connect_to_es(self):
        return self.es.search(index=self.name_get, body={'size': 10000, "query": {"match_all": {}}})

    def check_url(self, url):
        pass

    def save_to_es(self, _id, doc):
        h = _id
        print("Saving")
        if not self.es.exists(index=self.name_save, id=h, doc_type='_doc'):
            doc = doc
            print("Saved")
            self.es.index(index=self.name_save, id=h, body=doc, doc_type='_doc')

    def read_config(self, config_model):
        try:
            return pd.read_csv(self.MODEL_PATH + config_model + ".csv").fillna('')
        except:
            e = sys.exc_info()
            print("Error: ", e)
            try:
                return pd.read_csv(self.MODEL_PATH + "general.csv").fillna('')
            except:
                return None
    
    def get_html(self, url):
        get_soup_retry_times = 4
        for i in range(get_soup_retry_times):
            try:
                request = urllib.request.Request(url, data=None, headers = {"User-Agent": "Mozilla/5.0"})  # make web requests for URL
                request = urllib.request.urlopen(request)
                html = request.read().decode("utf8")

                request.close()
                return html

                # self.driver.get(url)
                # self.driver.set_page_load_timeout(5)
                # return self.driver.page_source

            except Exception as e:
                # print(e.__class__)
                print('Re-obtain this link')

    

    def save_to_db(self, name):
        f = open(name + ".json", "a")
        f.write(json.dumps(self.result))
        f.close()

    def get_url(self, name): 
        ""
        df = pd.read_csv(name + '.csv')
        return df

    def add_to_buffer(self, post, post_type):
        ""
        if post_type in self.result:
            if type(self.result[post_type] != list):
                self.result.pop('key', None)
        else:
            self.result[post_type] = []
        
        self.result[post_type].append(post)
        
    def stringify_children(self, node):
        # _list = []
        # for c in node.getchildren():
        #     _item = [c.text]
        #     print(" > ",_item[0])
        #     _list.append(_item)

        # parts = list(chain(*([c.text] for c in node.iter())))
        # # filter removes possible Nones in texts and tails
        # return ''.join(filter(None, parts))
        from lxml.etree import tostring
        from itertools import chain
        parts = ([node.text] +
                list(chain(*(self.stringify_children(c) for c in node.getchildren()))) +
                [node.tail])
        # filter removes possible Nones in texts and tails
        return ''.join(filter(None, parts))

    def parseData(self, status_parse):
        """
        Retrieve necessary information for each document and save to elasticsearch
        """
        _parse = self.get_url(self.name_get)

        print('\nNUMBER OF POSTS: \n', _parse)
        posts = _parse
        
        count = 1

        for index, post in posts.iterrows():
            post_url = post['Links']
            post_config = post["Parser"]
            post_type = post["Type"]
            post_status = post["Status"]
            print("** POST NUMBER : ", count)
            print("** POST url : ", post_url)
            print("Config: ", post_config)
            print("Type: ", post_type)
            print("Status: ", post_status)
            print(status_parse)
            if (int(post_status) != int(status_parse)):
                continue

            model = self.read_config(post_config)
            if model is None:
                continue

            doc = dict()

            doc['post_url_hash'] = hashlib.md5(post_url.encode()).hexdigest()
            page_source = self.get_html(post['Links'])

            page_source = re.sub("(<!--.*?-->)", "", page_source, flags=re.DOTALL)
            _html = html.fromstring(page_source)
            tree = etree.ElementTree(_html)

            for index, row in model.iterrows():
                xpath = row["xpath"]
                feature = row["features"]
                print(" > ", index, ". ", feature, ": ", xpath)

                attr = ''
                if xpath != '':
                    attr_lst = tree.xpath(str(xpath))
                    if isinstance(attr_lst, list) and len(attr_lst) > 0:
                        print("list")
                        if row['pos_take'] != '':
                            try:
                                _take = attr_lst[int(row['pos_take'])]
                                if (isinstance(_take, etree._Element)):
                                    attr = self.stringify_children(_take)
                                elif (isinstance(_take, etree._ElementUnicodeResult)): 
                                    attr = _take
                            except ValueError:                                
                                position_regex = row['pos_take']
                                _str = ""
                                for element in attr_lst:
                                    _str = self.stringify_children(element).strip().replace("\n","") + "<eof>"
                                    # print("->> ", _str)
                                    match = re.search(position_regex,_str)
                                    if match:
                                        _str = match.group(1)
                                        # print(">> ", _str)
                                        break
                                attr = _str.strip()

                        else:
                            if (isinstance(attr_lst[0], etree._Element)):
                                for element in attr_lst:
                                    ele_str = self.stringify_children(element).replace("\t", "").replace("\n", "")
                                    # print("->> ", ele_str)
                                    attr += "" + ele_str
                            elif (isinstance(attr_lst[0], etree._ElementUnicodeResult)): 
                                for element in attr_lst:
                                    attr += "" + element.text_content()

                # print(" >>>>> ", attr)

                if row["regex_take"] != '':
                    # print("Regex")
                    _attr = attr.replace("\n", "").replace("\t", "").strip() + "<eof>"
                    print(_attr)
                    
                    try:
                        _attr = re.search(str(row["regex_take"]), _attr)
                        if _attr:
                            _attr = _attr.group(1).strip()
                    except Exception:
                        _attr = attr
                    # print(_attr)
                    attr = _attr

                doc[feature] = attr.strip() if isinstance(attr, str) else attr

            print(doc)
            self.add_to_buffer(doc, post_type)
            # self.save_to_es(post['_id'], doc)

            count += 1
            if count >= self.POST_LIMIT:
                break
        
        self.save_to_db(self.name_save)
        print('PARSING DONE')
