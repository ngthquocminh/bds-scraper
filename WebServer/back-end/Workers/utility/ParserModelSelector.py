
import pandas as pd
from time import time
from datetime import datetime, timedelta, date
from slugify import slugify
import re

from Workers.models import Parser
from Workers.serializers import ParserSerializer
from Workers.utility.ParserObject import ParserObject
from Workers.utility.LibFunc import load_parser_set


class ParserModelSelector(ParserObject):
    def __init__(self, _url:str=None, _html:str=None, model_key:str=None):
        self.__url = _url
        self.__html = _html
        self.__key_site = model_key
        self.__model = None
        self.__as8a9z = {
            "bat-dong-san-com-vn": {
                "url-check-rgx": re.compile("^http(s?)://(www.)?batdongsan.com.vn/.+"),
                "html-check-rgx": None,
            },
            "nha-cho-tot-com": {
                "url-check-rgx": re.compile("http(s?)://(www.)?nha.chotot.com/"),
                "html-check-rgx": None
            },
            "nha-dat-247-com-vn": {
                "url-check-rgx": re.compile("^http(s?)://(www.)?nhadat247.com.vn/.+"),
                "html-check-rgx": None
            }            
        }

    def get_model(self):
        if self.__model is None:
            if isinstance(self.__key_site,str) and (self.__key_site in self.__as8a9z):
                print("---->", self.__key_site)
                return load_parser_set(self.__key_site)

            for _site_key in self.__as8a9z:
                site = self.__as8a9z[_site_key]
                if site["url-check-rgx"].search(self.__url) and (site["html-check-rgx"] is None or site["html-check-rgx"].search(self.__html)):         
                    self.__key_site = _site_key
                    self.__model = pd.DataFrame(load_parser_set(self.__key_site))

        # display(self.__model)
        return self.__model

    def get_date(self, date_str:str, date_origin:datetime):
        _date = None

        if not isinstance(date_str, str):
            return _date

        if self.__key_site == "bat-dong-san-com-vn":
            
            if isinstance(date_str, str) and re.compile("^[0-9]{2}/[0-9]{2}/[0-9]{4}$").search(date_str):
                _date = datetime.strptime(date_str, '%d/%m/%Y').date()
            
        elif self.__key_site == "nha-cho-tot-com":
            _date = None
            print(date_str)
            date_str = slugify(date_str.lower())
            _l = date_str.split("-")
            if "hom-qua" in date_str:
                _date = date_origin - timedelta(days=1)
            elif "thang" in _l:
                _n = int(_l[_l.index("thang") - 1])
                _date = date_origin - timedelta(days=30*_n)
            elif "tuan" in _l:
                _n = int(_l[_l.index("tuan") - 1])
                _date = date_origin - timedelta(days=7*_n)
            elif "ngay" in _l:
                _n = int(_l[_l.index("ngay") - 1])
                _date = date_origin - timedelta(days=1)
            elif ("hom-nay" in date_str) or ("gio" in _l) or ("phut" in _l):
                _date = date_origin
            elif re.compile("^[0-9]{2}-[0-9]{2}-[0-9]{4}$").search(date_str):
                _date = datetime.strptime(date_str, '%d-%m-%Y').date()
                
        elif self.__key_site == "nha-dat-247-com-vn":
            
            date_str = slugify(date_str.lower())

            if re.compile("^[0-9]{2}-[0-9]{2}-[0-9]{4}$").search(date_str):
                _date = datetime.strptime(date_str, '%d-%m-%Y').date()
            elif "hom-kia" in date_str:
                _date = date_origin - timedelta(days=2)
            elif "hom-qua" in date_str:
                _date = date_origin - timedelta(days=1)
            elif "hom-nay" in date_str:
                _date = date_origin

        return _date #.strftime("%d/%m/%Y")