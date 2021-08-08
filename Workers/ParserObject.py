
# import traceback

import pandas as pd
import re
from lxml import etree, html

from LibFunc import strip_text, stringify_children


class ParserObject(object):
    def __init__(self, _html:str, _model:pd.DataFrame):
        self.__html = _html
        self.__model = _model
        # print(self.__model)
        self.__parse_result = {}

    def parser_result(self):
        return self.__parse_result

    def parse_html(self, filter_func:dict = {}):
        # print(self.__html)
        tree = etree.ElementTree(html.fromstring(self.__html))        

        none_attr_count = 0
        detail = dict()

        _total_score = 0
        _attr_score = 0
        
        for index, row in self.__model.iterrows():
            
            feature = row["features"]
            
            if row["features"] in detail:
                if detail[row["features"]] != None and detail[row["features"]] != "":
                    continue
                none_attr_count -= 1

            xpath = str(row["xpath"])

            print(" > ", index, ". ", feature, xpath)

            attr = row["default"]
            if xpath != '' or len(xpath) > 0:
                attr_lst = tree.xpath(xpath)
                if isinstance(attr_lst, list) and len(attr_lst) > 0:
                    if row['pos_take'] != '':
                        try:
                            _take = attr_lst[int(row['pos_take'])]
                            if isinstance(_take, etree._Element):
                                
                                attr = stringify_children(_take)
                            elif isinstance(_take, etree._ElementUnicodeResult):
                                attr = _take
                        except ValueError:
                            position_regex = row['pos_take']
                            _str = ""
                            for element in attr_lst:
                                __str = strip_text(stringify_children(element))
                                match = re.search(position_regex, __str)
                                if match:
                                    _str = match.group(1)
                                    break
                            attr = strip_text(_str)

                    else:
                        if isinstance(attr_lst[0], etree._Element):
                            for element in attr_lst:
                                ele_str = stringify_children(element)
                                attr += " " + ele_str
                        elif isinstance(attr_lst[0], etree._ElementUnicodeResult):
                            for element in attr_lst:
                                attr += " " + element

            if row["regex_take"] != '':
                _attr = strip_text(attr)

                try:
                    _attr = re.search(str(row["regex_take"]), _attr)
                    if _attr:
                        _attr = _attr.group(1).strip()
                except Exception:
                    # traceback.print_exc()
                    _attr = attr
                # print(_attr)
                attr = _attr

            _rex = row["regex_valid"]
            try:
                _rex = re.compile(_rex)
                if not _rex.search(attr):
                    attr = None
            except:
                # traceback.print_exc()
                ""

            try:
                _len = int(row["len_valid"])
                if len(attr) < _len:
                    attr = None
            except:
                # traceback.print_exc()
                ""

            # apply filter functions
            if feature in filter_func:
                attr = filter_func[feature](attr)

            if attr is None:
                none_attr_count += 1
            else:
                _attr_score += row["importance"]

            _total_score += row["importance"]

            detail[feature] = attr.strip() if isinstance(attr, str) else attr

        try:
            if detail["length"] == "" or detail["length"] == None:
                detail["length"] = str(int(detail["surface"])//int(detail["width"]))
        except:
            # traceback.print_exc()
            ""  
            
        eff = _attr_score/_total_score
        self.__parse_result = {"detail":detail,"code":"OK","eff": eff}
        return detail