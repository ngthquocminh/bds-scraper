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
    canho = ["https://batdongsan.com.vn/ban-can-ho-chung-cu"]
    nharieng = ["https://batdongsan.com.vn/ban-nha-rieng"]
    nhapho_biethu = ["https://batdongsan.com.vn/ban-nha-biet-thu-lien-ke", "https://batdongsan.com.vn/ban-nha-mat-pho"]
    dat = ["https://batdongsan.com.vn/ban-dat", "https://batdongsan.com.vn/ban-dat-nen-du-an"]
    crawler = BatDongSanCrawler(canho, "1/1/2018", "29/5/2021", "canho")
    crawler.obtainData("post_urls_batdongsan_canho2")


def html_parser():
    ""
    parser = BatDongSanParser("post_urls_batdongsan_canho", "parsed_batdongsan_canho")
    # parser.set_save_to_database()
    parser.parseData(0)


def main():
    start_crawling()
    # html_parser()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
