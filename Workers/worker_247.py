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

from nhadat247_parser import NhaDat247Parser
from nhadat247_crawler import NhaDat247Crawler

def start_crawling():
    ""
    canho = ["https://nhadat247.com.vn/ban-can-ho-chung-cu.html"]
    nha = ["https://nhadat247.com.vn/ban-nha-biet-thu-lien-ke.html","https://nhadat247.com.vn/ban-nha-biet-thu-lien-ke.html","https://nhadat247.com.vn/ban-nha-rieng.html"]
    dat = ["https://nhadat247.com.vn/ban-dat-nen-du-an.html", "https://nhadat247.com.vn/ban-dat.html"]
    crawler = NhaDat247Crawler(dat, "30/5/2021", "29/8/2021", "dat")
    crawler.obtainData("post_urls_nhadat247_dat_new1")


def html_parser():
    ""
    parser = NhaDat247Parser("post_urls_nhadat247_canho_new1", "parsed_post_urls_nhadat247_canho_new1")
    # parser = NhaDat247Parser("post_urls_nhadat247_nha_new1", "parsed_post_urls_nhadat247_nha_new1")
    # parser = NhaDat247Parser("post_urls_nhadat247_dat_new1", "parsed_post_urls_nhadat247_dat_new1")
    # parser.set_save_to_database()
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
