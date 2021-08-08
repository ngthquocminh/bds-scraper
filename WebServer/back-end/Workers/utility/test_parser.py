import traceback
from Workers.utility.Database import DBObject
from Workers.utility.ParserEngines import ParserEngines

from time import time
import pandas as pd
from datetime import date

from Workers.utility.ParserModelSelector import ParserModelSelector

#=============================================================================================
#=============================================================================================


def parse(data, many:bool=False, model_name=None):
    parser_model = None
    if model_name:
        parser_model=ParserModelSelector(model_key=model_name)

    if isinstance(data,list) and many:
        result = []
        for post in data:
            
            engine = ParserEngines(post=post,parser_model=parser_model,test_mode=True, threshold=0)
            _r = engine.process_post()
            result.append(_r["doc"] if _r["code"] == "OK" else {})
        return result
    elif isinstance(data,dict):
        
        engine = ParserEngines(post=date, parser_model=parser_model,test_mode=True)
        _r = engine.process_post()
        return _r["doc"] if _r["code"] == "OK" else {}

    return {}

def doTestOnParser(dict_request:dict): 
    print(dict_request)
    try:
        list_post_url = dict_request["list_url_hash"]
        model_name =  dict_request["model_name_for_all"] if "model_name_for_all" in dict_request else None
        database = DBObject()
        list_post_html = database.query_html_db({"$or":[{"url_hash":url_hash} for url_hash in list_post_url]})
        content = parse(list_post_html,many=True, model_name=model_name)
        
        return {"code":200,"message":"successfull","content":content}
    except Exception as e:
        traceback.print_exc()
        return {"code":404,"message":"failed"}
