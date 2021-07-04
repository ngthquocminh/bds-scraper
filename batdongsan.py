import sys
import os
import json
import re
import hashlib
import traceback
import time

import validators
from datetime import datetime, date
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import urljoin

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from crawl import CrawlHTML
from database import DBObject
from Browser import Browser
from Settings import Settings


def save_list(data: list, file_name):
    print("Checkpoint: ", file_name)
    with open(file_name, 'w') as file:
        file.write("\n".join(set(data)))
        file.close()

class BatDongSanCrawler(CrawlHTML):

    BASE_URL = "https://batdongsan.com.vn/"
    SAVE_CHECK_POINT = 20

    def __init__(self, url: list, date_from, date_to, post_type, all_date:bool = False):

        self.__str_info = "Site: batdongsan.com.vn, Type: %s, %s-%s, "%(post_type, date_from, date_to)

        self.post_type  = post_type
        self.buffer     = []
        self.seed_url   = url

        self.__current_url = ""
        self.__failed_urls = []
        self.__saved_post  = []
    
        self.file_log_visited_url   = "visited_post_log_batdongsan_%s.txt"%(self.post_type)
        self.file_log_new_url       = "local_urls_log_batdongsan_%s.txt"%(self.post_type)
        self.regex_sub_url          = re.compile("https[:][/][/]batdongsan[\.]com[\.]vn/ban-[-a-z0-9]+(/p[0-9]+)?")
        self.regex_post             = re.compile("https[:][/][/]batdongsan[\.]com[\.]vn/ban-[-a-z0-9]+/[-a-z0-9]+pr[0-9]+")

        self.key_type = BatDongSanCrawler.get_key_from_type(self.post_type)

        self.post_date_range = {
            "from": datetime.strptime(date_from, '%d/%m/%Y').date(), 
            "to": datetime.strptime(date_to, '%d/%m/%Y').date()
            }

        self.db_object = DBObject()
        self.browser = Browser(headless=False)
        
        worker_info = self.db_object.query_wokers_info(Settings.worker_id)
        task_id = worker_info["task_id"] if (worker_info and worker_info["task_id"]) else (int)(time.time())

        self.__crawling_info = {"task_id":task_id,"status":"crawling","str_info":""}
        self.__crawling_log  = {"worker_id":Settings.worker_id, "task_id":task_id, "task_info":self.__str_info, "saved_posts":[], "error_posts":[]}

        if worker_info["task_id"] is None:
            self.db_object.create_wokers_log(self.__crawling_log)
            self.update_crawling_status_info(0,0)
        else:
            log = self.db_object.query_wokers_logs(Settings.worker_id,task_id)
            if log is not None:
                self.__saved_post = log["saved_posts"]
                self.__failed_urls = log["error_posts"]

        print("Init crawler")


    def update_crawling_status_info(self, num_post, num_error):
        self.__crawling_info["str_info"] = self.__str_info + "Numpost: %d, Error: %d"%(num_post, num_error)
        self.db_object.update_wokers_info(Settings.worker_id, self.__crawling_info)

    def update_crawling_log(self, saved_posts:list, error_posts:list):
        self.__crawling_log["saved_posts"] = saved_posts
        self.__crawling_log["error_posts"] = error_posts

        self.db_object.update_wokers_log(Settings.worker_id, self.__crawling_log["task_id"], self.__crawling_log["saved_posts"])

    def get_html_and_soup_from_url(self, url):
        """
        Return Beautifulsoup object
        """
        _soup = None
        _html = None
        for i in range(5):
            try:
                element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/footer"))              
                _html = self.browser.get_html(url, until_ec=element_present)
                _soup = BeautifulSoup(_html, 'html.parser')
                if _soup is not None:
                    return _html, _soup
            except Exception as e: 
                traceback.print_exc()
                continue
        
        self.__failed_urls.append(self.__current_url)
        return None, None

    @staticmethod
    def get_key_from_type(key) -> list:
        if key == "land":
            return ["ban-dat"]
        elif key == "apartment":
            return ["ban-can-ho-chung-cu"]
        elif key == "house":
            return ["ban-nha-mat-pho", "ban-nha-biet-thu","ban-nha-rieng"]

        return ["ban-dat", "ban-can-ho  -chung-cu", "ban-nha-rieng", "ban-nha-mat-pho", "ban-nha-biet-thu"]


    def check_type(self, url) -> bool:
        for key in self.key_type:
            if key in url:
                # print("ok")
                return True

        return False


    def append_data(self, _url, _type, _status, _crawl_date, _post_date, _html):

        post                = {}
        post["url_hash"]    = hashlib.md5(_url.encode()).hexdigest()
        post["url"]         = _url
        post["type"]        = _type
        post["status"]      = _status
        post["html"]        = _html
        post["date"]        = _crawl_date
        post["post_date"]   = _post_date

        self.buffer.append(post)


    def load_init_url(self) -> tuple:
        local_urls = self.seed_url
        try:
            local_urls = list(open(self.file_log_new_url, "r").readlines())
        except:
            ""
        visited_post= []
        try:
            visited_post = list(open(self.file_log_visited_url, "r").readlines())
        except:
            ""

        return local_urls, visited_post


    def get_date(self, page_soup: BeautifulSoup) -> date:
        post_date = None
        try:
            str_date = page_soup.select_one("#product-detail-web > div.detail-product > div.product-config.pad-16 > ul > li:nth-child(1) > span.sp3").get_text()
            str_date = str_date.strip()
            post_date = datetime.strptime(str_date, '%d/%m/%Y').date()
            if not (self.post_date_range["from"] <= post_date <= self.post_date_range["to"]):
                post_date = None                     

        except Exception as e: 
            self.__failed_urls.append(self.__current_url)
            traceback.print_exc()
        return post_date


    def visit(self, current_url) -> tuple:       
        local_urls = []
        post_date = None
        page_source, page_soup = self.get_html_and_soup_from_url(current_url)

        if page_soup:

            is_post = re.search(self.regex_post, current_url)
            if is_post:
                post_date = self.get_date(page_soup)
                if not (self.all_date or post_date):
                    page_source = None

            list_href = page_soup.find_all('a')

            for link in list_href:
                anchor = str(link.get('href'))
                if not bool(urlparse(anchor).netloc):
                    anchor = urljoin(self.BASE_URL, anchor)

                if validators.url(anchor) and self.check_type(anchor) and (self.regex_post.search(anchor) or self.regex_sub_url.search(anchor)):
                    local_urls.append(anchor)

        return page_source, post_date, local_urls


    def obtain_data(self):

        print("START...")

        local_urls, visited_post = self.load_init_url()
        post_count = len(self.__saved_post)
        while local_urls:
            self.__current_url = local_urls.pop(0)
        
            if len(self.__current_url) < 10 and (self.__current_url in visited_post or not self.check_type(self.__current_url)):
                continue
            
            print(" > ", self.__current_url)

            page_source, post_date, new_urls_to_visit = self.visit(self.__current_url)

            visited_post.append(self.__current_url)
            local_urls.append(new_urls_to_visit)

            if page_source:
                post_count += 1
                self.append_data(_url = self.__current_url, _type="post", _status="0", _html  = page_source, _crawl_date = str(date.today().strftime("%d/%m/%Y")), _post_date = post_date)

            # check-point to save buffer data
            if isinstance(self.buffer, list) and len(self.buffer) == self.SAVE_CHECK_POINT:
                self.save_data()
                self.update_crawling_status_info(post_count, len(self.__failed_urls))
                self.update_crawling_log()
                save_list(local_urls, self.file_log_new_url)
                save_list(visited_post, self.file_log_visited_url)

            print("  >> num: ", post_count)           

        # finishing
        self.save_data()

        print('CRAWLING DONE')


    def save_data(self):
        self.db_object.insert_html_data(self.buffer)
        # clear buffer
        self.buffer = None