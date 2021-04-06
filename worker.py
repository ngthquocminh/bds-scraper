import pika
import sys
import os
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Process
import pandas as pd
import bs4
import multiprocessing

import requests
import urllib.request
import shutil
import csv
import time

import re
import hashlib
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from urllib.parse import urlsplit
from urllib.parse import urlparse
from urllib.parse import urljoin
from elasticsearch import Elasticsearch

from batdongsan_parser import BatDongSanParser
from batdongsan_crawler import BatDongSanCrawler



def start_crawling():    
    ""
    crawler = BatDongSanCrawler("1/1/2020","27/4/2021", "all")
    crawler.obtainData("post_urls_0")


def html_parser():
    ""
    parser = BatDongSanParser("post_urls_0", "data_parsed1")
    parser.set_save_to_mongodb()
    parser.parseData(0)


def main():
    # start_crawling()
    html_parser()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
