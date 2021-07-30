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
# "apartment": ["https://nhadat247.com.vn/ban-can-ho-chung-cu.html"],
# "house": ["https://nhadat247.com.vn/ban-nha-rieng.html", "https://nhadat247.com.vn/ban-nha-biet-thu-lien-ke.html", "https://nhadat247.com.vn/ban-nha-mat-pho.html"],
# "land": ["https://nhadat247.com.vn/ban-dat-nen-du-an.html", "https://nhadat247.com.vn/ban-dat.html"]
def get_seed_url(post_type):
    data = {
        "apartment" : ["https://batdongsan.com.vn/ban-can-ho-chung-cu"],
        "house" : ["https://batdongsan.com.vn/ban-nha-rieng", "https://batdongsan.com.vn/ban-nha-biet-thu-lien-ke", "https://batdongsan.com.vn/ban-nha-mat-pho"],
        "land" : ["https://batdongsan.com.vn/ban-dat", "https://batdongsan.com.vn/ban-dat-nen-du-an"]
    }
    return data[post_type] if post_type in data else [url for e in data for url in data[e]]

def save_list(data: list, file_name):
    print("Checkpoint: ", file_name)
    with open(file_name, 'w') as file:
        file.write("\n".join(set(data)))
        file.close()

class BatDongSanCrawler():

    BASE_URL = "https://batdongsan.com.vn/"
    SAVE_CHECK_POINT = 20

    def __init__(self, date_from=None, date_to=None, post_type=None, all_date:bool = False):
        self.__str_info = "Site: batdongsan.com.vn, Type: %s, Date: %s-%s, "%(post_type, date_from, date_to) + "Numpost: %d, Error: %d"

        self.post_type  = post_type
        self.buffer     = []
        self.seed_url   = get_seed_url(post_type)

        self.__current_url = ""
        self.__failed_urls = []
        self.__saved_post  = []
    
        self.file_log_visited_url   = "visited_post_log_batdongsan_%s.txt"%(self.post_type)
        self.file_log_new_url       = "local_urls_log_batdongsan_%s.txt"%(self.post_type)
        self.regex_sub_url          = re.compile("https[:][/][/]batdongsan[\.]com[\.]vn/ban-[-a-z0-9]+(/p[0-9]+)?")
        self.regex_post             = re.compile("https[:][/][/]batdongsan[\.]com[\.]vn/ban-[-a-z0-9]+/[-a-z0-9]+pr[0-9]+")

        self.key_type = BatDongSanCrawler.get_key_from_type(self.post_type)
        
        try:
            self.post_date_range = {
                "from": datetime.strptime(date_from, '%d/%m/%Y').date(), 
                "to": datetime.strptime(date_to, '%d/%m/%Y').date()
                }
        except:
            self.post_date_range = None            

        self.db_object = DBObject()
        self.browser = Browser(headless=False)
        
        worker_info = self.db_object.query_wokers_info(Settings.worker_id)
        task_id = worker_info["task_id"] if (worker_info and "task_id" in worker_info) else None
        self.task_exist = self.db_object.query_wokers_logs(Settings.worker_id, task_id)
        if not self.task_exist:
            task_id = (int)(time.time())

        self.__crawling_info = {
            "task_id":task_id,
            "status":"crawling",
            "str_info":""
            }
        self.__crawling_log  = {
            "worker_id":Settings.worker_id,
            "task_id":task_id, 
            "task_info":self.__str_info%(0,0), 
            "saved_posts":[], 
            "error_posts":[]
            }

        if not self.task_exist:
            print("Create log")
            self.db_object.create_wokers_log(self.__crawling_log)
            self.update_crawling_status_info(0, 0)
        else:
            log = self.db_object.query_wokers_logs(Settings.worker_id,task_id)
            print("Get log: ", log if log else "null")
            if log is not None:
                self.__saved_post = log["saved_posts"]
                self.__failed_urls = log["error_posts"]

        print("Init crawler")


    def update_crawling_status_info(self, num_post, num_error):
        self.__crawling_info["str_info"] = self.__str_info%(num_post, num_error)
        self.db_object.update_wokers_info(Settings.worker_id, self.__crawling_info)

    def update_crawling_log(self):
        self.db_object.update_wokers_log(Settings.worker_id, self.__crawling_log["task_id"], self.__saved_post, self.__failed_urls )

    def get_html_and_soup_from_url(self, url):
        """
        Return Beautifulsoup object
        """
        _soup = None
        _html = None
        for i in range(5):
            try:
                element_present = EC.presence_of_element_located((By.XPATH, "/html/body/footer"))              
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

        url_hash            = hashlib.md5(_url.encode()).hexdigest()
        post["url_hash"]    = url_hash
        post["url"]         = _url
        post["type"]        = _type
        post["status"]      = _status
        post["html"]        = _html
        post["date"]        = _crawl_date
        post["post_date"]   = _post_date
        self.__saved_post.append(url_hash)
        self.buffer.append(post)

        post["html"] = "<html>"
        print("-"*10,"\n",post)



    def load_init_url(self) -> tuple:
        local_urls   = self.seed_url
        visited_post = []

        if self.task_exist:
            try:
                local_urls = list(open(self.file_log_new_url, "r").readlines())
            except:
                ""
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
                print("Is a post")
                post_date = self.get_date(page_soup)
                if not self.post_date_range or \
                    (isinstance(post_date, datetime.datetime) and (self.post_date_range["from"] <= post_date <= self.post_date_range["to"])):
                    post_date = post_date.strftime('%d/%m/%Y')
                else:
                    page_source = None

            else:
                page_source = None

            list_href = page_soup.find_all('a')

            for link in list_href:
                anchor = str(link.get('href'))
                if not bool(urlparse(anchor).netloc):
                    anchor = urljoin(self.BASE_URL, anchor)

                if validators.url(anchor) and self.check_type(anchor) and (self.regex_post.search(anchor) or self.regex_sub_url.search(anchor)):
                    local_urls.append(anchor)

        print("<html>" if page_source else "None")
        return page_source, post_date, local_urls


    def obtain_data(self):

        print("START...")
        num_visited = 0
        local_urls, visited_post = self.load_init_url()
        post_count = len(self.__saved_post)
        while local_urls:
            self.__current_url = local_urls.pop(0)
        
            if len(self.__current_url) < 10 and (self.__current_url in visited_post or not self.check_type(self.__current_url)):
                continue
            
            print(" > ", self.__current_url)

            page_source, post_date, new_urls_to_visit = self.visit(self.__current_url)

            visited_post.append(self.__current_url)
            local_urls += new_urls_to_visit

            if page_source:
                post_count += 1
                self.append_data(_url = self.__current_url, _type="post", _status="0", _html  = page_source, _crawl_date = str(date.today().strftime("%d/%m/%Y")), _post_date = post_date)

            # check-point to save buffer data
            if num_visited % self.SAVE_CHECK_POINT == 0:
                self.save_data()
                self.update_crawling_status_info(post_count, len(self.__failed_urls))
                self.update_crawling_log()

                save_list(local_urls,   self.file_log_new_url)
                save_list(visited_post, self.file_log_visited_url)

            num_visited += 1
            print("  >> num: ", post_count)           

        # finishing
        self.save_data()
        self.db_object.update_wokers_info(Settings.worker_id, None)
        print('CRAWLING DONE')


    def save_data(self):
        self.db_object.insert_html_data(self.buffer, many=True)
        # clear buffer
        self.buffer = []