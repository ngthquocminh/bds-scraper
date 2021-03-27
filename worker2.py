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

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='worker2')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)        
        data = body.decode().split("|")
        task = data[0]  
        if int(task) == 1:
            start_crawling(data[1:])
        elif int(task) == 2:
            start_parsing(data[1:])

    channel.basic_consume(queue='worker2', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def start_crawling(param):
    date_from = param[0]
    date_to = param[1]
    post_type = param[2]

    crawler = BatDongSanCrawler(date_from, date_to, post_type)
    crawler.obtainData("post_urls_2")



def start_parsing(param):
    status_parse = param[0]
    parser = BatDongSanParser("post_urls_2", "data_parsed2")
    parser.parseData(status_parse)


if __name__ == '__main__':
    try:
        pass
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
