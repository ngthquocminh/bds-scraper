import sys
import os

from batdongsan import BatDongSanCrawler
from ParserEngines import ParserEngines
import traceback
from LibFunc import doParse
from reciever import message_loads, message_dumps
# from batdongsan import BatDongSanCrawler


def start_crawling(date_from=None, date_to=None, post_type=None, all_date:bool = False):
    ""
    crawler = BatDongSanCrawler(post_type=post_type)
    crawler.obtain_data()


def start_parsing():
    ""
    doParse()

def main(params):
    try:
        if params["command"] == "crawl":
            date_from = params["post-date"].split("_")[0]
            date_to   = params["post-date"].split("_")[1]
            post_type = params["type"]
            start_crawling(date_from=date_from, date_to=date_to, post_type=post_type)
        elif params["command"] == "parse":
            list_post = params["post"].split("_")
            start_parsing(list_post)
        elif params["command"] == "resume":
            ""
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
