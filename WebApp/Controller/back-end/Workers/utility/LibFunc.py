from itertools import chain
import re
import pandas as pd
from Workers.models import Parser
from Workers.serializers import ParserSerializer


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
    parser_set_obj  = Parser.objects.raw("""SELECT * FROM Workers_parser WHERE site="{_parser_set}" """.format(_parser_set=key))
    serializers = ParserSerializer(parser_set_obj, many=True)
    return serializers.data if isinstance(serializers.data, list) else [serializers.data]

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