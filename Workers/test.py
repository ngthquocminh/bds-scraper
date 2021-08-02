import sys
import os
import platform
import json
import re
import hashlib
from traceback import print_exc
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
# import time
# from random import randint
# from datetime import datetime


# _timer = time.time()
# local_urls = open("local_urls_log_nha.txt", "r").readlines()
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

# file = open("parsed_chotot_nhadat1.json", "r")
# lines = json.loads(file.read())
# list_legal = []
# for post in lines:
#     legal = post["detail"]["legal"]
#     if not legal in list_legal:
#         list_legal.append(legal)

# print(list_legal)


# file = open("visited_post_log_batdongsan_nharieng.txt", "r")
# lines = file.readlines()
# new_lines = []
# for line in lines:
#     if len(line) > 1 and "ban-nha-rieng" in line:
#         new_lines.append(line)
# open("visited_post_log_batdongsan_nharieng2.txt","w").write("\n".join(set(new_lines)))

# file = open("local_urls_log_batdongsan_nhapho_biethu.txt", "r")
# lines = file.readlines()
# new_lines = []
# for line in lines:
#     if len(line) > 1 and ("ban-nha-biet-thu" in line or "ban-nha-mat-pho" in line):
#         new_lines.append(line)
# open("local_urls_log_batdongsan_nhapho_biethu2.txt","w").write("\n".join(set(new_lines)))
# file_path = "data\\nhadat247\\parsed_nhadat247_canho.json"
# file = open(file_path, "r")
# data = file.read()
# data = json.loads(data)
# import traceback

# converted = []
# for post in data:
#     price = post["detail"]["price"]
#     surface = post["detail"]["surface"]
#     try:
#         surface = int(surface)
#     except:
#         surface = None

#     price = price.strip().lower()
#     if "/m" in price and surface is not None:
#         price = price.split(" ")[0]
#         print(price)
#         try:
#             price = price.split(",")
#             price = int(price[0]) + int(price[1]) * pow(0.1, len(price[1]))
#             print(price)
            
#         except:
#             traceback.print_exc()
#             try:
#                 price = price.split(".")
#                 price = int(price[0]) + int(price[1]) * pow(0.1, len(price[1]))
#                 print(price)
#             except:
#                 traceback.print_exc()

#                 continue
#         price = int(surface*price)
#         if price < 100:
#             price *= 10
#     else:
#         continue
#     print(">", price)
    
#     unit = "tỷ"
#     price /= 1000
#     if price < 1:
#         unit = "triệu"
#         price *= 1000

#     post["detail"]["price"] = str(round(price,2)) + " " + unit
#     print(post)
#     # converted.append(post)
# # print(len(converted))
# file.close()

# file = open(file_path + "x", "w")
# file.write(json.dumps(converted, indent=5))


# file = open("post_urls_batdongsan_nharieng.json","r")
# data = []

# i = 0
# a = 0
# s = 0
# import traceback
# post = file.readline()

# while len(post) > 10:
#     s += 1
#     try:
#         data_json = json.loads(post)
#         for p in data_json:
#             data_json = data_json[p]
#         url = data_json["url"]
#         if "ban-nha-rieng" in str(url):        
#             a += 1
#         # data.append(post)
#     except:
#         # traceback.print_exc()
#         # print(post)
#         # print(post)
#         i += 1    
#         data.append(post)
#         break

#     print(i,"/",a,"/",s)
#     post = file.readline()

# file.close()
# file = open("test_nharieng.json","w")
# file.write(json.dumps(data, indent=5))


# file = open("parsed_batdongsan_dat2.json","r")
# print(len(json.loads(file.read())))
import os

if __name__ == "__main__":
    pid = os.getpid()
    print(sys.argv)
    name = sys.argv[1]
    open("data.txt","w").write(str(pid))
    i = 0
    while True:
        i += 1
        print("[%d] %s: %d"%(pid, name, i))


# import signal
# pid = int(open("data.txt","r").read())
# os.kill(pid, signal.SIGTERM) #or signal.SIGKILL 