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

date_from = datetime.strptime("22/3/2021", '%d/%m/%Y').date()
date_to = datetime.strptime("23/3/2021", '%d/%m/%Y').date()
print((date_from + timedelta(days=0)).strftime("%d/%m/%Y"))