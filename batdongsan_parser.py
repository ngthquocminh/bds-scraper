import re
import sys

import pandas as pd
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from lxml import html
from os import listdir
from parse import ParseHTML
from slugify import slugify
import json

import hashlib
import urllib


class   BatDongSanParser(ParseHTML):

    MODEL_PATH = "config/"
    POST_LIMIT = 100
    BASE_URL = "https://nhadat247.com.vn/"

    def __init__(self, saved_name, name):
        self.name = name
        self.saved_name = saved_name
        self.es = Elasticsearch()
        self.result = dict()
        self.main()

    def connect_to_es(self):
        return self.es.search(index=self.name, body={'size': 10000, "query": {"match_all": {}}})

    def check_url(self, url):
        pass

    def save_to_es(self, _id, doc):
        h = _id
        print("Saving")
        if not self.es.exists(index=self.saved_name, id=h, doc_type='_doc'):
            doc = doc
            print("Saved")
            self.es.index(index=self.saved_name, id=h, body=doc, doc_type='_doc')

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
            # try:
            request = urllib.request.Request(url, data=None, headers = {"User-Agent": "Mozilla/5.0"})  # make web requests for URL
            html = urllib.request.urlopen(request).read()
            return html
            # except:
            #     print('Re-obtain this link')

        print('Can not access this link !!!')
        return None 

    def save_to_db(self):
        f = open("data_parsed.json", "a")
        f.write(json.dumps(self.result))
        f.close()

    def get_url(self): 
        ""
        df = pd.read_csv('post_urls_1.csv')
        return df

    def add_to_buffer(self, post, post_type):
        ""
        if post_type in self.result:
            if type(self.result[post_type] != list):
                self.result.pop('key', None)
        else:
            self.result[post_type] = []
        
        self.result[post_type].append(post)
        

    def main(self):
        """
        Retrieve necessary information for each document and save to elasticsearch
        """
        _parse = self.get_url()

        print('\nNUMBER OF POSTS: \n', _parse)
        posts = _parse

        count = 1

        for index, post in posts.iterrows():
            post_url = post['Links']
            post_config = post["Parser"]
            post_type = post["Type"]
            post_status = ""
            print("** POST NUMBER : ", count)
            print("** POST url : ", post_url)
            print("Config: ", post_config)
            print("Type: ", post_type)
            print("Status: ", post_status)

            model = self.read_config(post_config)
            if model is None:
                continue

            doc = dict()

            doc['post_url_hash'] = hashlib.md5(post_url.encode()).hexdigest()
            page_source = self.get_html(post['Links'])
            tree = html.fromstring(page_source)

            for index, row in model.iterrows():
                xpath = row["xpath"]
                feature = row["features"]
                print(" > ", index, ". ", feature, ": ", xpath)

                attr = ''
                if xpath != '':
                    attr_lst = tree.xpath(str(xpath))
                    if len(attr_lst) > 0:
                        if row['pos_take'] != '':
                            attr = attr_lst[int(row['pos_take'])]
                        else:
                            for element in attr_lst:
                                attr = attr + element.text_content()

                if row["regex_take"] != '':
                    attr = re.search(str(row["regex_take"]), attr)
                    if attr:
                        attr = attr.group(0)

                doc[feature] = attr.strip() if isinstance(attr, str) else attr

            print(doc)
            self.add_to_buffer(doc, post_type)
            # self.save_to_es(post['_id'], doc)

            count += 1
            if count >= self.POST_LIMIT:
                break
        
        self.save_to_db()
        print('PARSING DONE')


parse = BatDongSanParser('info', 'urls')
parse.main()
