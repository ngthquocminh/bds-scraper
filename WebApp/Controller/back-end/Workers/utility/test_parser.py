from Workers.utility.Database import DBObject
from Workers.utility.ParserEngine import parse
from Workers.models import Parser
from Workers.serializers import ParserSerializer

def doTestOnParser(dict_request:dict): 
    try:

        parser_set = dict_request["parser_set"]
        list_post_url = dict_request["list_post_url"]

        parser_set  = Parser.objects.raw("""SELECT * FROM Workers_parser WHERE site="{_parser_set}" """.format(_parser_set=parser_set))
        serializers = ParserSerializer(parser_set, many=True)
        database = DBObject()
        list_html = database.query_html_db({"$or":[{"url_hash":url_hash} for url_hash in list_post_url]})
        content = [parse(html) for html in list_html]
        return {"code":404,"message":"successfull","content":content}
    except Exception as e:
        return {"code":200,"message":repr(e)}