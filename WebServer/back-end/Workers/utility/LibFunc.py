import re
import pandas as pd
from itertools import chain 
from Workers.models import Parser
from Workers.serializers import ParserSerializer
from Workers.utility.Database import DBObject
import traceback

db = DBObject()

def strip_text(text):
    return text.replace("\t", "").replace("\n", "").strip()

def stringify_children(node):
    # print(str(node.tag))

    parts = ([node.text] +
                list(chain(*((stringify_children(c) + ("\n" if str(c.tag) == "div" else "")) for c in node.getchildren()))) +
                [node.tail])

    return ''.join(filter(None, parts))
    
def clean_trash(html):
    html = re.sub("( +)"," ", html)
    return re.sub("(<!--.*?-->)|(<script.*?>.*?</script>)|(<style.*?>.*?</style>)", "", html, flags=re.DOTALL)

def load_parser_set(key:str):     
    print("load_parser_set " + key) 
    return db.get_parser_model(key)

def d_range(from_to): 
    # from_to ~ {"from":"8/2021","to":"10/2021"}
    try:
        _from = [int(i) for i in from_to["from"].split("/")]
        _to   = [int(i) for i in from_to["to"].split("/")]
        result = []
        for y in range(_from[1],_to[1] + 1):
            for m in range(_from[0] if y == _from[1] else 1, (_to[0] + 1) if y == _to[1] else 13):
                result.append((str(m) if m>9 else ("0" + str(m)),str(y)))
        return result
    except:
        return []

def searchPostHtml(request:dict):
    # print(request) 
    site_type_re = {
        "nha.chotot.com":
        {
            "land":r"^.*/mua-ban-dat/.*$",
            "house":r"^.*/mua-ban-nha-dat/.*$",
            "apartment":r"^.*/mua-ban-can-ho-chung-cu/.*$"
        },
        "nhadat247.com.vn":
        {
            "land":r"^.*nhadat247.com.vn/ban-dat.*$",
            "apartment":r"^.*nhadat247.com.vn/ban-can-ho-chung-cu.*$",
            "house":r"^.*nhadat247.com.vn/ban-nha.*$"
        },
        "batdongsan.com.vn":
        {
            "land":r"^.*batdongsan.com.vn/ban-dat.*$",
            "apartment":r"^.*batdongsan.com.vn/ban-can-ho-chung-cu.*$",
            "house":r"^.*batdongsan.com.vn/ban-nha.*$"
        }
    }

    try:
        db = DBObject()

        _site        = request["site"] if "site" in request else None
        _crawl_date  = request["crawl_date"] if "crawl_date" in request else None
        _post_date   = request["post_date"] if "post_date" in request else None
        _type        = request["type"] if "type" in request else "all"
        _limit       = int(request["limit"]) if ("limit" in request) and len(request["limit"])>0 else 0
        
        list_filter = []

        if _site in site_type_re:
            list_filter.append({"url":{"$regex":"^https://%s/.*$"%(_site)}})

        if _type in site_type_re[_site]:            
            list_filter.append({"url":{"$regex":site_type_re[_site][_type]}})
        else:
            list_filter.append({"$or":[{"url":{"$regex":site_type_re[_site][_t]}} for _t in site_type_re[_site]]})

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