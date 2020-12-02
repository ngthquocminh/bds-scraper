import re
import sys

import pandas as pd
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from lxml import html
from os import listdir
from parse import ParseHTML
from slugify import slugify
import hashlib


class NhatTaoParser(ParseHTML):
    """
    Retrieve information from HTML which is stored in elasticsearch
    @param name is the name of the HTML database
    @param saved_name is the name of saved database
    @param es is the ElasticSearch object
    @param result is the dictionary of post information which are retreived
    """
    MODEL_PATH = "config/"
    POST_LIMIT = 100
    BASE_URL = "https://nhattao.com"

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

    def main(self):
        """
        Retrieve necessary information for each document and save to elasticsearch
        """
        _parse = self.connect_to_es()

        print('NUMBER OF POSTS:', _parse['hits']['total'])
        posts = _parse['hits']['hits']

        count = 1
        for post in posts:
            print('** POST NUMBER:', count)
            print('** POST ID:', post["_id"])
            print('Post type:', post["_source"]["type"])
            print("Config: ", post["_source"]["parser_config"])
            print("Status: ", post["_source"]["status"])

            model = self.read_config(post['_source']["parser_config"])
            if model is None:
                continue

            doc = dict()

            doc['url'] = post['_source']['url']
            page_source = post['_source']['document']
            tree = html.fromstring(page_source)

            doc['data_details'] = dict()
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
                if feature == "seller_url":
                    feature = "seller_id"
                    attr = hashlib.md5((self.BASE_URL + "/" + attr).encode()).hexdigest()
                doc['data_details'][feature] = attr.strip() if isinstance(attr, str) else attr

            doc['data_details']["type"] = post["_source"]["type"]
            print(doc)
            self.result[post['_id']] = doc
            self.save_to_es(post['_id'], doc)

            count += 1
            if count >= self.POST_LIMIT:
                break

        print('PARSING DONE')


parse = NhatTaoParser('info', 'urls')
parse.main()
