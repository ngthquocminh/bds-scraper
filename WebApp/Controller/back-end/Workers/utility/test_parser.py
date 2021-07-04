import traceback
from Workers.utility.Database import DBObject
from Workers.utility.ParserEngines import parse
from Workers.utility.LibFunc import d_range

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

def searchPostHtml(request:dict):
    # print(request) yg
    try:
        db = DBObject()

        _site        = request["site"]
        _crawl_date  = request["crawl_date"]
        _post_date   = request["post_date"]
        _limit       = int(request["limit"]) if ("limit" in request) and len(request["limit"])>0 else 0
        print(_limit)
        list_filter = []

        if _site in ["batdongsan.com.vn","chotot.com","nhadat247.com.vn"]:
            list_filter.append({"url":{"$regex":"^https://%s/.*$"%(_site)}})

        _d_range = d_range(_crawl_date)
        if len(_d_range) > 0:
            list_filter.append({"$or":[{"date":{"$regex":"^[0-9]{2}/%s/%s$"%(m,y)}} for m,y in _d_range]})
            
        _d_range = d_range(_post_date)
        if len(_d_range) > 0:
            list_filter.append({"$or":[{"post_date":{"$regex":"^[0-9]{2}/%s/%s$"%(m,y)}} for m,y in _d_range]})

        query_return = []
        for post in db.query_html_db(query_dict={"$and":list_filter}, limit=_limit):
            post.pop("html")
            post.pop("_id")

            post["html"] = "content is eliminated"
            query_return.append(post)
        # print(query_return[0])
        return {"code":200,"message":"successfull","content":query_return}
    except:
        # traceback.print_exc()
        return {"code":404,"message":"failed","content":[]}