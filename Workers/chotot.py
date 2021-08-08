import re
import hashlib
import traceback
import time
import calendar

import validators
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from slugify import slugify

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from database import DBObject
from Browser import Browser
from Settings import Settings
from CrawlerObject import CrawlerObject

# "apartment": ["https://nhadat247.com.vn/ban-can-ho-chung-cu.html"],
# "house": ["https://nhadat247.com.vn/ban-nha-rieng.html", "https://nhadat247.com.vn/ban-nha-biet-thu-lien-ke.html", "https://nhadat247.com.vn/ban-nha-mat-pho.html"],
# "land": ["https://nhadat247.com.vn/ban-dat-nen-du-an.html", "https://nhadat247.com.vn/ban-dat.html"]


class ChoTotCrawler(CrawlerObject):

    BASE_URL = "https://nha.chotot.com/"
    SAVE_CHECK_POINT = 5

    def __init__(self, date_from=None, date_to=None, post_type=None, all_date:bool = False, resume=False, limit=-1):
        
        self.limit = int(limit)
        self.db_object = DBObject()
        the_status = "crawling"
        worker_info = self.db_object.query_wokers_info(Settings.worker_id)
        self.resume = resume
        if self.resume:
            try:
                info_ = worker_info
                status_ = info_["status"]
                task_id = info_["task_id"]
                info_str_ = info_["str_info"]
                if not ("(pause)" in status_ and "crawling" in status_):
                    print(">>", status_)
                    return
                info_dict_ = {_i_.split(": ")[0]:_i_.split(": ")[1] for _i_ in info_str_.lower().split(", ")}
                if info_dict_["site"] != "nha.chotot.com":
                    return
                date_from  = info_dict_["date"].split("-")[0]
                date_to    = info_dict_["date"].split("-")[1]
                
                try:
                    self.limit = int(info_dict_["limit"])
                except:
                    self.limit = -1

                post_type  = info_dict_["type"]
                the_status = status_.replace("(pause)","")
                print("Internal loading data to resume")
            except:
                traceback.print_exc()
                return


        self.__str_info = "Site: nha.chotot.com, Type: %s, Date: %s-%s, Limit: %s, "%(post_type, date_from, date_to, str(self.limit) if isinstance(self.limit,int) and self.limit > 0 else "No") 
        self.__str_info += "Numpost: %d, Error: %d"

        self.post_type  = post_type
        self.buffer     = []
        self.seed_url   = ChoTotCrawler.get_seed_url(post_type)

        self.__current_url = ""
        self.__failed_urls = []
        self.__saved_post  = []
    
        self.file_log_visited_url   = "visited_post_log_chotot_%s.txt"%(self.post_type)
        self.file_log_new_url       = "local_urls_log_chotot_%s.txt"%(self.post_type)

        self.regex_sub_url          = re.compile("([a-z][-a-z]*)?ban-[-a-z]+((.htm)|(/[0-9]+))?")
        self.regex_post             = re.compile("([a-z][-a-z]+)?[/][a-z][-a-z0-9]+/[-a-z0-9]+.htm")

        self.key_type = ChoTotCrawler.get_key_from_type(self.post_type)
        
        try:
            last_day_to = calendar.monthrange(int(date_to.split("/")[1]), int(date_to.split("/")[0]))[1]
            self.post_date_range = {
                "from": datetime.strptime("1/" + date_from, '%d/%m/%Y').date(), 
                "to": datetime.strptime(str(last_day_to) + "/" + date_to, '%d/%m/%Y').date()
                }
            print("-"*200,"\n", self.post_date_range)
        except:
            traceback.print_exc()
            self.post_date_range = None            

        self.browser = Browser(headless=False)        

        
        if not self.resume:
            task_id = (int)(time.time())

        self.__crawling_info = {
            "task_id":task_id,
            "status":the_status,
            "str_info":""
            }
        self.__crawling_log  = {
            "worker_id":Settings.worker_id,
            "task_id":task_id, 
            "task_info":self.__str_info%(0,0), 
            "saved_posts":[], 
            "error_posts":[]
            }


        if not self.resume:
            print("Create log")
            self.db_object.create_wokers_log(self.__crawling_log)
            self.update_crawling_status_info(0, 0)
        else:
            log = self.db_object.query_wokers_logs(Settings.worker_id, task_id)
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
        click_phone_script = """
            function getElementByXpath(path) {
                return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            }

            var phone = getElementByXpath("/html/body/div[1]/div/div[1]/div/div[4]/div[3]/div/linkcontact/span");
            if (phone != null) {
                phone.click();
            }                    
        """

        for i in range(5):
            try:
                is_post = re.search(self.regex_post, url)
                element_present = EC.presence_of_element_located((By.XPATH, """//html/body/div[1]/footer"""))
                _html = self.browser.get_html(url=url, until_ec=element_present, run_script=click_phone_script if is_post else None)
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
            return ["mua-ban-dat"]
        elif key == "apartment":
            return ["mua-ban-can-ho-chung-cu"]
        elif key == "house":
            return ["mua-ban-nha-dat"]

        return ["mua-ban-dat","mua-ban-nha-dat","mua-ban-can-ho-chung-cu"]


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

        # post["html"] = "<html>"
        # print("-"*10,"\n",post)


    def load_init_url(self) -> tuple:
        local_urls   = self.seed_url
        visited_post = []

        if self.resume:
            try:
                local_urls = list(open(self.file_log_new_url, "r").readlines())
            except:
                ""
            try:
                visited_post = list(open(self.file_log_visited_url, "r").readlines())
            except:
                ""

        return local_urls, visited_post

    def convert_str2date(date_str):
        _date = None

        date_str = slugify(date_str.lower())
        _l = date_str.split("-")
        if "hom-qua" in date_str:
            _date = date.today() - timedelta(days=1)
        elif "thang" in _l:
            _n = int(_l[_l.index("thang") - 1][0])
            _date = date.today() - timedelta(days=30*_n)
        elif "tuan" in _l:
            _n = int(_l[_l.index("tuan") - 1][0])
            _date = date.today() - timedelta(days=7*_n)
        elif "ngay" in _l:
            _n = int(_l[_l.index("ngay") - 1][0])
            _date = date.today() - timedelta(days=1)
        elif "hom-nay" in date_str or "gio" in _l or "phut" in _l:
            _date = date.today()
        else:
            _date = datetime.strptime(date_str, '%d/%m/%Y').date()

        return _date

    def get_date(self, page_soup: BeautifulSoup) -> date:
        post_date = None
        try:
            str_date = page_soup.select_one("#__next > div > div.ct-detail.adview > div > div.col-md-8 > div.adImageWrapper___KTd-h > div.imageCaption___cMU2J > span").get_text()
            str_date = str_date.strip()
            post_date = ChoTotCrawler.convert_str2date(str_date)         

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
                    (isinstance(post_date, date) and (self.post_date_range["from"] <= post_date <= self.post_date_range["to"])):
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

                ChoTotCrawler.save_list(local_urls,   self.file_log_new_url)
                ChoTotCrawler.save_list(visited_post, self.file_log_visited_url)

            num_visited += 1
            print("  >> num: ", post_count)  
            if self.limit > 0 and post_count >= self.limit:
                break      

        # finishing
        self.save_data()
        self.update_crawling_status_info(post_count, len(self.__failed_urls))
        self.update_crawling_log()
        self.browser.close()
        print('CRAWLING DONE')

    def rotate_ip(self, enable=False):
        self.browser.set_rotate_ip(enable)
        return

    def save_data(self):
        self.db_object.insert_html_data(self.buffer, many=True)
        # clear buffer
        self.buffer = []

    def get_seed_url(post_type):
        data = {
            "apartment" : ["https://nha.chotot.com/toan-quoc/mua-ban-can-ho-chung-cu"],
            "house" : ["https://nha.chotot.com/toan-quoc/mua-ban-nha-dat"],
            "land" : ["https://nha.chotot.com/toan-quoc/mua-ban-dat"]
        }
        return data[post_type] if post_type in data else [url for e in data for url in data[e]]

    def save_list(data: list, file_name):
        print("Checkpoint: ", file_name)
        with open(file_name, 'w') as file:
            file.write("\n".join(set(data)))
            file.close()