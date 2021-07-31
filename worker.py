import sys
import os

from batdongsan import BatDongSanCrawler
import traceback
from ParserEngines import doParse
from reciever import message_loads
# from batdongsan import BatDongSanCrawler


def start_crawling(date_from=None, date_to=None, post_type=None, resume=False, all_date:bool = False):
    ""
    crawler = BatDongSanCrawler(post_type=post_type, date_from=date_from, date_to=date_to, resume=resume)
    crawler.obtain_data()

def start_parsing(list_post, model_name, site, type, resume=False):
    ""
    print("Go to start_parsing")

    doParse(list_post, model_name, site=site, type=type, num=len(list_post), resume=resume)

def main(params):
    try:
        if params["command"] == "crawl":
            if "resume" in params and int(params["resume"]) == 1:
                start_crawling(resume=True)
            else:
                date_from = params["post-date"].split("_")[0].replace("-","/")
                date_to   = params["post-date"].split("_")[1].replace("-","/")
                post_type = params["type"]
                start_crawling(date_from=date_from, date_to=date_to, post_type=post_type)

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
