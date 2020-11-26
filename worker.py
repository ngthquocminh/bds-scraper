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

from nhat_tao import NhatTaoCrawler

# def main():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()
#
#     channel.queue_declare(queue='hello')
#
#     def callback(ch, method, properties, body):
#         print(" [x] Received %r" % body)
#         start_crawling()
#
#     channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
#
#     print(' [*] Waiting for messages. To exit press CTRL+C')
#     channel.start_consuming()

def start_crawling():
    list_url = ["https://nhattao.com/threads/ban-dt-ss-galaxy-s9-plus-tim-ban-han.8996989/", "https://nhattao.com/"]
    crawler = NhatTaoCrawler(list_url)



start_crawling()
# if __name__ == '__main__':
#     try:
#         pass
#         # main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
