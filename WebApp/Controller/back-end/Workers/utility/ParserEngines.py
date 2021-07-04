import traceback

from time import time
import pandas as pd
from datetime import datetime, date

import hashlib

from Workers.utility.ParserObject import ParserObject
from Workers.utility.ParserModelSelector import ParserModelSelector
from Workers.utility.LibFunc import clean_trash


#=============================================================================================
#=============================================================================================


def parse(data, many:bool=False, model_name=None):
    parser_model = None
    if model_name:
        parser_model=ParserModelSelector(model_key=model_name)
        if not isinstance(parser_model.get_model(), pd.DataFrame):
            parser_model = None

    if isinstance(data,list) and many:
        result = []
        for post in data:
            
            engine = ParserEngines(post=post,parser_model=parser_model,test_mode=True)
            _r = engine.process_post()
            result.append(_r["doc"] if _r["code"] == "OK" else {})
        return result
    elif isinstance(data,dict):
        
        engine = ParserEngines(post=date, parser_model=parser_model,test_mode=True)
        _r = engine.process_post()
        return _r["doc"] if _r["code"] == "OK" else {}

    return {}


#=============================================================================================


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

        # print("** POST url : ", post_url)
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



    