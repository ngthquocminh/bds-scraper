import traceback

from time import time
import pandas as pd
from datetime import datetime, date
import time

import hashlib

from ParserObject import ParserObject
from ParserModelSelector import ParserModelSelector
from LibFunc import clean_trash
from database import DBObject
from Settings import Settings

#=============================================================================================
#=============================================================================================

database = DBObject()

def parse(posts_data, site=None, type=None, num=None, many:bool=False, model_name=None, resume=False):

    print("Go to Parsing Data")
    the_status = "parsing"
    __failed_urls = []
    __saved_post  = []
    task_id = (int)(time.time())
    worker_info = database.query_wokers_info(Settings.worker_id)
    if resume:
        try:
            info_ = worker_info
            status_ = info_["status"]
            task_id = info_["task_id"]
            log = database.query_wokers_logs(Settings.worker_id,task_id)
            print("Get log: ", log if log else "null")
            if log is not None:
                __saved_post = log["saved_posts"]
                __failed_urls = log["error_posts"]

            info_str_ = info_["str_info"]
            if not ("(pause)" in status_ and "parsing" in status_):
                print(">>", status_)
                return

            info_dict_ = {_i_.split(": ")[0]:_i_.split(": ")[1].lower() for _i_ in info_str_.split(", ")}

            the_status = status_.replace("(pause)","")
            site = info_dict_["site"]
            type = info_dict_["type"]
            num  = info_dict_["num"]
            model_name = log["parser_model"]

            print("Internal loading data to resume")
        except:
            traceback.print_exc()
            return

    __str_info = "Site: %s, Type: %s, Num: %d, "%(site, type, num) + "Parsed: %d, Error: %d"

    __parsing_info = {
            "task_id":task_id,
            "status":the_status,
            "str_info":""
            }

    __parsing_log  = {
            "worker_id":Settings.worker_id,
            "parser_model":model_name,
            "task_id":task_id, 
            "task_info":__str_info%(0,0), 
            "saved_posts":__saved_post, 
            "error_posts":__failed_urls
            }
    

    if not resume:
        database.create_wokers_log(__parsing_log)

    print("Init completed")

    parser_model = None
    if isinstance(model_name,str):
        parser_model=ParserModelSelector(_url=site, model_key=model_name)
        if not isinstance(parser_model.get_model(), pd.DataFrame):
            parser_model = None
    
    
    print("Start parsing")
    # print(posts_data)
    if isinstance(posts_data,list) and many:
        result = []
        for post in posts_data:
            
            if resume and (post["url_hash"] in __saved_post or post["url_hash"] in __failed_urls):
                continue

            engine = ParserEngines(post=post,parser_model=parser_model,test_mode=True)
            _r = engine.process_post()
            if _r["code"] == "OK":
                print("parse OK")
                posts_data = _r["doc"] 

                database.insert_parsed_data(posts_data, many=False)

                #update log adn info
                __parsing_info["str_info"] = __str_info%(len(__saved_post),len(__failed_urls))
                database.update_wokers_info(Settings.worker_id, __parsing_info)
                database.update_wokers_log(Settings.worker_id, __parsing_log["task_id"], __saved_post, __failed_urls)
                database.update_html_post_status(post["url_hash"],int(post["status"]) + 1)

                result.append(posts_data["url_hash"])
                __saved_post.append(post["url_hash"])
            else:
                print("parse Failed")
                __failed_urls.append(post["url_hash"])

        return result

    elif isinstance(posts_data,dict):
        
        engine = ParserEngines(post=date, parser_model=parser_model,test_mode=True)
        _r = engine.process_post()
        return _r["doc"] if _r["code"] == "OK" else {}

    return {}

def doParse(list_post, model=None, site=None, type=None, num=None, resume=False): 
    try:
        print("Go to doParse: ", list_post)
        list_post_url = list_post
        model_name =  model
        list_post_html = database.query_html_db({"$or":[{"url_hash":url_hash} for url_hash in list_post_url]})
        content = parse(posts_data=list_post_html,many=True, site=site, type=type, num=num, model_name=model_name, resume=resume)
        
        return {"code":200,"message":"successfull","content":content}
    except Exception as e:
        traceback.print_exc()
        return {"code":404,"message":"failed"}

class ParserEngines(object):
    def __init__(self, post:dict, parser_model:ParserModelSelector, test_mode:bool=True):
        self.__post = post
        self.__parser_model = parser_model
        self.__test_mode = test_mode
    
    def process_post(self):   
        _status = "XX"
        
        post_url        = self.__post['url']
        post_type       = self.__post["type"]
        post_status     = self.__post["status"]

        print("** POST url : ", post_url)
        # print("Type: ", post_type)
        # print("Status: ", post_status)
            
        doc = dict()
        doc["parse_score"] = 0
        doc["url_hash"] = hashlib.md5(post_url.encode()).hexdigest()
        doc["url"] = post_url

        try:
            doc["crawl_date"] = self.__post["date"]
        except:
            traceback.print_exc()
            doc["crawl_date"] = str(date.today().strftime("%d/%m/%Y"))

        doc["parse_date"] = date.today().strftime("%d/%m/%Y")
        doc["status"] = int(self.__post["status"]) + 1

        page_source = clean_trash(self.__post['html'])

        if self.__parser_model == None:
            self.__parser_model = ParserModelSelector(_url=post_url, _html=page_source)
            
        if self.__parser_model.get_model() is not None:
            def date_convert(attr):
                try:
                    crawl_date = datetime.strptime(self.__post["date"], '%d/%m/%Y').date()
                    post_date = self.__parser_model.get_date(attr,crawl_date)
                    return post_date.strftime("%d/%m/%Y") if post_date else None
                except:
                    # traceback.print_exc()
                    return None

            parser_obj = ParserObject(page_source, self.__parser_model.get_model())
            result  = parser_obj.parse_html({"date":date_convert})

            if self.__test_mode:
                doc["parse_score"] = parser_obj.parser_result()["eff"]

            if parser_obj.parser_result()["eff"] > 5.0 or self.__test_mode:
                doc["detail"] = result
                _status = "OK"


        return {"doc":doc,"code":_status}



    