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


# url = "https://nhadat247.com.vn/ban-nha-rieng/ban-nha-moi-xay-5-tang-pho-bo-de-lap-thang-may-gia-6-ty-pr85802.html"

# request = urllib.request.Request(url, data=None, headers = {"User-Agent": "Mozilla/5.0"})  # make web requests for URL
# html = urllib.request.urlopen(request).read()
# soup = BeautifulSoup(html, 'html.parser')


# _date = soup.select_one("#ContentPlaceHolder1_ProductDetail1_divprice > div").get_text()
# _date = _date.split("|")[1].strip()
# print(_date)
# _date = "hôm qua"

# if _date == "hôm qua":
#     _date = date.today() - timedelta(days=1)
# elif _date == "hôm nay":
#     _date = date.today()
# else:
#     _date = datetime.strptime(_date, '%d/%m/%Y')

# print(date.today() >= _date)

# date_from = datetime.strptime("22/3/2021", '%d/%m/%Y').date()
# date_to = datetime.strptime("23/3/2021", '%d/%m/%Y').date()
# print((date_from + timedelta(days=0)).strftime("%d/%m/%Y"))

# url = re.compile("https[:][/][/]nhadat247[\.]com.vn.*")

# a = url.search("""https://nhadat247.com.vn/ban-nha-mat-pho-phuong-10-5.html""")
# print(a)

# a = re.compile("tel:([0-9]+)<eof>")
# b = re.search("Khu Vực:.*Tại(.+)", "Khu Vực: Bán Căn Hộ Chung Cư Tại Đường Gia Quất - Phường Thượng Thanh - Long Biên - Hà Nội")
# print(b.group(1))
import time
from random import randint
from datetime import datetime


_timer = time.time()
local_urls = open("local_urls_log_nha.txt", "r").readlines()
# file = open("test.txt", "w")
# local_urls += local_urls*100

# i = 0
# for url in local_urls:
#     url = url.strip() + str(datetime.timestamp(datetime.now())) + str(randint(0,9)) + str(randint(0,9))
#     file.write(url + "\n")
#     print(url)
#     i += 1
#     # if i == 10:
#     #     break
# file.close()

# print("read completed", time.time() - _timer)

# _timer = time.time()
# local_urls += local_urls*100
# print(len(local_urls), time.time() - _timer)

# _timer = time.time()
# url = "https://nhadat247.com.vn/ban-nha-rieng-an-giang.html"
# print(url in local_urls, time.time() - _timer)
# # visited_post = open("visited_post_log_nha.txt", "r").readlines()

# _timer = time.time()
# res = False
# for _url in local_urls:
#     if _url == url:
#         res = True
# print(res, time.time() - _timer)




