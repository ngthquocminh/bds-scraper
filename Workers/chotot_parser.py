from base64 import decode
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
import math

import validators
import pandas as pd
from time import time
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from urllib.parse import urlsplit
from urllib.parse import urlparse
from urllib.parse import urljoin
from database import DBTarget

MAXIMUM = 15000


def strip_text(text):
    return text.replace("\t", "").replace("\n", "").strip()

def get_data(name):
    ""
    print("get data")
    data = []
    try:
        file = open(name + ".json", "r")
        # for i in range(0, 100):
        #     print(i)
        data = file.readlines()
        file.close()
    except:
        "nodata"

    return data


class ChototParser(ParseHTML):
    MODEL_PATH = "config/"

    POST_LIMIT = 99999


    def __init__(self, name_get, name_save):

        self.save_func = self.save_to_local

        self.name_get = name_get
        self.name_save = name_save
        self.save_buffer = []
        

    def save_to_db(self, row=None):
        for i in range(10):
            try:                
                return self.save_func(row)
            except:
                continue
        
        return False

    def connect_to_es(self):
        return self.es.search(index=self.name_get, body={'size': 10000, "query": {"match_all": {}}})

    def check_url(self, url):
        return True

    def save_to_es(self, doc):
        h = doc["url_hash"]
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

    def set_save_to_database(self):
        db = DBTarget()
        self.save_func = db.save_to()

    def save_to_local(self, doc):
        ""
        x = self.POST_LIMIT
        step_save = round(250 * x / math.sqrt(x ** 2 + 500000 * x + 10000))
        if doc is not None:
            self.add_to_buffer(doc)
        else:
            step_save = len(self.save_buffer)

        if len(self.save_buffer) % step_save == 0:
            self.save_to_file(self.name_save)
            # self.save_buffer = []

    def save_to_file(self, name):
        f = open(name + ".json", "w")
        f.write(json.dumps(self.save_buffer, indent=5))
        f.close()

    def add_to_buffer(self, post):
        ""
        self.save_buffer.append(post)

    def stringify_children(self, node):

        from lxml.etree import tostring
        from itertools import chain
        parts = ([node.text] +
                 list(chain(*(self.stringify_children(c) for c in node.getchildren()))) +
                 [node.tail])
        # filter removes possible Nones in texts and tails
        return ''.join(filter(None, parts))

    def get_date(self, date_str, crawl_date):
        _date = None
        crawl_date = datetime.strptime(crawl_date, '%d/%m/%Y').date()
        date_str = slugify(date_str.lower())
        _l = date_str.split("-")
        if "hom-qua" in date_str:
             _date = crawl_date - timedelta(days=1)
        elif "thang" in _l:
            _n = int(_l[_l.index("thang") - 1][0])
            _date = crawl_date - timedelta(days=30*_n)
        elif "tuan" in _l:
            _n = int(_l[_l.index("tuan") - 1][0])
            _date = crawl_date - timedelta(days=7*_n)
        elif "ngay" in _l:
            _n = int(_l[_l.index("ngay") - 1][0])
            _date = crawl_date - timedelta(days=1)
        elif "hom-nay" in date_str or "gio" in _l or "phut" in _l:
            _date = crawl_date
        else:
            ""
            # _date = datetime.strptime(date_str, '%d/%m/%Y').date()

        return _date.strftime("%d/%m/%Y")

    def parseData(self, status_parse):
        """
        Retrieve necessary information for each document and save to elasticsearch
        """
        post = None
        file = None
        try:
            file = open(self.name_get + ".json", "r")
            post = file.readline()
        except:
            "nodata"

        print("-" * 50)

        count = 1
        line = 0
        passs = False
        while post:


            line += 1

            try:
                post = json.loads(post)
                for p in post:
                    post = post[p]
            except:
                post = file.readline()
                continue
            
            
            # if passs:
            #     break
            # if post["url"] != "https://nha.chotot.com/tp-ho-chi-minh/quan-tan-phu/mua-ban-nha-dat/85110146.htm":
            #     continue
            # else:
            #     passs = True

            post_url = post['url']
            post_config = post["parser"]
            post_type = post["type"]
            post_status = post["status"]

            # if not passs:
            #     if post_url == "https://nha.chotot.com/quang-nam/huyen-thang-binh/mua-ban-nha-dat/85089346.htm#px=SR-similarad-[PO-3][PL-bottom]":
            #         print("Continue ... ")
            #         passs = True
            #     print(" >> ",count)
            #     count+=1
            #     post = file.readline()
            #     continue
            

            print("** POST NUMBER : ", count)
            print("** POST url : ", post_url)
            print("Config: ", post_config)
            print("Type: ", post_type)
            print("Status: ", post_status)
            if int(post_status) != int(status_parse):
                post = file.readline()
                continue

            model = self.read_config(post_config)
            if model is None:
                post = file.readline()
                continue

            doc = dict()

            doc["url_hash"] = hashlib.md5(post_url.encode()).hexdigest()
            doc["url"] = post_url


            try:
                doc["crawl_date"] = post["date"]
            except:
                doc["crawl_date"] = date.today().strftime("%d/%m/%Y")

            doc["parse_date"] = date.today().strftime("%d/%m/%Y")
            doc["status"] = int(post["status"]) + 1
   
            page_source = post['html']

            page_source = re.sub("(<!--.*?-->)", "", page_source, flags=re.DOTALL)
            page_source = re.sub("(<script.*?>.*?</script>)", "", page_source, flags=re.DOTALL)
            page_source = re.sub(" +", " ", page_source, flags=re.DOTALL)
            page_source = re.sub("(<style.*?>.*?</style>)", "", page_source, flags=re.DOTALL)

            _html = html.fromstring(page_source)
            tree = etree.ElementTree(_html)

            detail = dict()
            none_attr_count = 0
            for index, row in model.iterrows():
                feature = row["features"]

                if row["features"] in detail:
                    if detail[row["features"]] != None and detail[row["features"]] != "":
                        continue

                xpath = str(row["xpath"])
                # print(" > ", index, ". ", feature, ": ", xpath)

                attr = row["default"]
                if xpath != '' or len(xpath) > 0:
                    attr_lst = tree.xpath(xpath)
                    if isinstance(attr_lst, list) and len(attr_lst) > 0:
                        if row['pos_take'] != '':
                            try:
                                _take = attr_lst[int(row['pos_take'])]
                                if isinstance(_take, etree._Element):
                                    attr = self.stringify_children(_take)
                                elif isinstance(_take, etree._ElementUnicodeResult):
                                    attr = _take
                            except ValueError:
                                position_regex = row['pos_take']
                                _str = ""
                                for element in attr_lst:
                                    __str = strip_text(self.stringify_children(element)) + "<eof>"
                                    # print("->> ",position_regex , " ", __str,)
                                    match = re.search(position_regex, __str)
                                    if match:
                                        _str = match.group(1)
                                        # print(">> ", _str)
                                        break
                                attr = strip_text(_str)

                        else:
                            # print(">> full")
                            if isinstance(attr_lst[0], etree._Element):
                                for element in attr_lst:
                                    ele_str = strip_text(self.stringify_children(element))
                                    # print("->> ", ele_str)
                                    attr += " " + ele_str
                            elif isinstance(attr_lst[0], etree._ElementUnicodeResult):
                                for element in attr_lst:
                                    attr += " " + element.text_content()

                # print(" >>>>> ", attr)

                if row["regex_take"] != '':
                    # print("Regex")
                    _attr = strip_text(attr)
                    # print(row["regex_take"])
                    try:
                        _attr = re.search(str(row["regex_take"]), _attr)
                        if _attr:
                            _attr = _attr.group(1).strip()
                    except Exception:
                        _attr = attr
                    # print(_attr)
                    attr = _attr

                _rex = row["regex_valid"]
                try:
                    _rex = re.compile(_rex)
                    if not _rex.search(attr):
                        attr = None
                except:
                    ""

                try:
                    _len = int(row["len_valid"])
                    if len(attr) < _len or "<eof>" in attr:
                        attr = None
                except:
                    ""

                if feature == "date":
                    try:
                        _date = re.sub("(<!--.*?-->)", "", attr, flags=re.DOTALL)
                        attr = self.get_date(_date, post["date"])
                    except:
                        ""

                if attr is None:
                    none_attr_count += 1
                else:
                    from random import randrange
                    if feature == "phone":
                        attr = attr.replace(" ","").replace("***", str(randrange(10)) + str(randrange(10)) + str(randrange(10)) + str(randrange(10))) 
                    # print(attr)

                if attr is None:
                    none_attr_count += 1

                detail[feature] = attr.strip() if isinstance(attr, str) else attr
                

            if none_attr_count / len(detail) > 0.6:
                print("{ Ignored }")
                post = file.readline()
                continue
            


            doc["detail"] = detail
            print(doc)
            
            save_result = self.save_to_db(doc)
            print("Saved " , save_result)

            count += 1
            if 0 < self.POST_LIMIT <= count:
                break
            
            post = file.readline()

        self.finishing_up()

    def finishing_up(self):
        self.save_to_db()
        print('PARSING DONE')
