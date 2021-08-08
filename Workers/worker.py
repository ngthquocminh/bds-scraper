import sys
import os

import traceback
from ParserEngines import doParse
from receiver import message_loads
from database import DBObject
from Settings import Settings

# from batdongsan import BatDongSanCrawler

db = DBObject()

def start_crawling(site, date_from=None, date_to=None, post_type=None, resume=False, all_date:bool = False,limit=-1):
    ""
    crawler = None
    if site == "batdongsan.com.vn":
        from batdongsan import BatDongSanCrawler as Crawler
    elif site == "nha.chotot.com":
        from chotot import ChoTotCrawler as Crawler
    elif site == "nhadat247.com.vn":
        from nhadat247 import NhaDat247 as Crawler

    crawler = Crawler(post_type=post_type, date_from=date_from, date_to=date_to, resume=resume, limit=limit)

    crawler.obtain_data()
    db.finishing_task(Settings.worker_id)

def start_parsing(list_post, model_name=None, site=None, type=None, resume=False):
    ""
    print("Go to start_parsing")

    doParse(list_post, model_name, site=site, type=type, num=len(list_post), resume=resume)
    db.finishing_task(Settings.worker_id)

def main(params):
    try:
        if params["command"] == "crawl":
            if "resume" in params and int(params["resume"]) == 1:
                _site = db.query_wokers_info(Settings.worker_id)["str_info"].split(", ")[0].split(": ")[1]
                start_crawling(site=_site, resume=True)
            else:
                site      = params["site"]
                date_from = params["post-date"].split("_")[0].replace("-","/")
                date_to   = params["post-date"].split("_")[1].replace("-","/")
                post_type = params["type"]
                limit     = params["limit"] if "limit" in params else -1
                start_crawling(site=site, date_from=date_from, date_to=date_to, post_type=post_type,limit=limit)

        elif params["command"] == "parse":
            print("Go to parse")
            file = open("parse_posts.data","r")
            posts = file.read()
            file.close()
            list_post = posts.split("_")
            if "resume" in params and int(params["resume"]) == 1:

                start_parsing(list_post=list_post, resume=True)
            else:
                model     = params["model"]
                site      = params["site"]
                post_type = params["type"]
                
                print("NEW parse")
            
                start_parsing(list_post=list_post, model_name = model, site=site, type=post_type)

        return True
    except:
        traceback.print_exc()
        return False


if __name__ == '__main__':

    args = sys.argv[1:]

    params = message_loads(" ".join(args))

    import os
    pid = os.getpid()
    print(sys.argv)
    open("data.lock","w").write(str(pid))

    try:
        main(params)
    except KeyboardInterrupt:
        # print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
