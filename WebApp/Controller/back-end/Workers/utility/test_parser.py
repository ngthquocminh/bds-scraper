from Workers.utility.Database import DBObject
from Workers.utility.ParserEngines import parse
from Workers.models import Parser
from Workers.serializers import ParserSerializer

def doTestOnParser(dict_request:dict): 
    # try:
    list_post_url = dict_request["list_url_hash"]
    model_name =  dict_request["model_name_for_all"] if "model_name_for_all" in dict_request else None
    database = DBObject()
    list_post_html = database.query_html_db({"$or":[{"url_hash":url_hash} for url_hash in list_post_url]})
    content = parse(list_post_html,many=True, model_name=model_name)
    
    return {"code":404,"message":"successfull","content":content}
    # except Exception as e:
    #     return {"code":200,"message":repr(e)}