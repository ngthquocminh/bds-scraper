
# import traceback

import pandas as pd
import re
from lxml import etree, html
import html2text
from bs4 import BeautifulSoup
import traceback

from Workers.utility.LibFunc import strip_text, stringify_children

class ParserObject(object):
    def parse_html():
        pass


class SpacyModel():

    def __init__(self):
        self.text = "Not thing"

    def set_text(self,text):
        self.text = text

    # --------------------------------

    def get_date(self):
        
        return ("date", [])

    def get_user(self):

        return ("user", [])

    def get_phone(self):

        return ("phone", [])

    def get_title(self):

        return ("title", [])

    def get_category(self):

        return ("category", [])

    def get_description(self):

        return ("description", [])

    def get_address(self):
        
        return ("address", [])

    def get_region(self):

        return ("region", [])

    def get_district(self):

        return ("district", [])

    def get_street(self):

        return ("street", [])

    def get_price(self):

        return ("price", [])

    def get_surface(self):

        return ("surface", [])

    def get_width(self):

        return ("width", [])

    def get_length(self):

        return ("length", [])

    def get_bedrooms(self):

        return ("bedrooms", [])

    def get_rooms(self):

        return ("rooms", [])

    def get_legal(self):

        return ("legal", [])



class XpathSelectorParser(ParserObject):
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

            # print(" > ", index, ". ", feature, xpath)

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
        
        eff = _attr_score/(_total_score if _total_score > 0 else 1)
        self.__parse_result = {"detail":detail,"code":"OK","eff": eff}
        return detail


class SpacyParser(ParserObject):
    def __init__(self, _html:str, _model:SpacyModel):
        self.__html = _html
        self.__model = _model
        
        self.__parse_result = {}
    
    def __htm2text(self):
        text = ""

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        converter.ignore_images = True
        try:
            soup = BeautifulSoup(self.__html, "html.parser")
            html_product = None
            if ("product-detail" in self.__html):
                html_product = str(soup.select_one(".product-detail"))
            elif ("ct-detail" in self.__html):
                html_product = str(soup.select_one(".ct-detail"))

            if html_product is not None:
                text = converter.handle(html_product).replace("\n\n","\n").replace("**","").replace("|","").replace("  "," ").replace("\-"," - ")
        except:
            traceback.print_exc()
            ""

        return text

    def parser_result(self):
        return self.__parse_result

    def parse_html(self, filter_func:dict = {}):
        
        none_attr_count = 0
        detail = dict()

        text = self.__htm2text()

        self.__model.set_text(text)
        
        # --------------------------------------------------------------

        date_key, date_value = self.__model.get_date()
        detail[date_key] = date_value[0] if len(date_value) > 0 else None

        # --------------------------------------------------------------

        user_key, user_value = self.__model.get_user()
        detail[user_key] = user_value[0] if len(user_value) > 0 else None

        # --------------------------------------------------------------
        
        phone_key, phone_value = self.__model.get_phone()
        detail[phone_key] = phone_value[0] if len(phone_value) > 0 else None

        # --------------------------------------------------------------

        title_key, title_value = self.__model.get_title()
        detail[title_key] = title_value[0] if len(title_value) > 0 else None

        # --------------------------------------------------------------

        category_key, category_value = self.__model.get_category()
        detail[category_key] = category_value[0] if len(category_value) > 0 else None

        # --------------------------------------------------------------

        description_key, description_value = self.__model.get_description()
        detail[description_key] = description_value[0] if len(description_value) > 0 else None

        # --------------------------------------------------------------

        address_key, address_value = self.__model.get_address()
        detail[address_key] = address_value[0] if len(address_value) > 0 else None

        # --------------------------------------------------------------

        region_key, region_value = self.__model.get_region()
        detail[region_key] = region_value[0] if len(region_value) > 0 else None

        # --------------------------------------------------------------

        district_key, district_value = self.__model.get_district()
        detail[district_key] = district_value[0] if len(district_value) > 0 else None

        # --------------------------------------------------------------

        street_key, street_value = self.__model.get_street()
        detail[street_key] = street_value[0] if len(street_value) > 0 else None

        # --------------------------------------------------------------

        price_key, price_value = self.__model.get_price()
        detail[price_key] = price_value[0] if len(price_value) > 0 else None

        # --------------------------------------------------------------

        surface_key, surface_value = self.__model.get_surface()
        detail[surface_key] = surface_value[0] if len(surface_value) > 0 else None

        # --------------------------------------------------------------

        width_key, width_value = self.__model.get_width()
        detail[width_key] = width_value[0] if len(width_value) > 0 else None

        # --------------------------------------------------------------

        length_key, length_value = self.__model.get_length()
        detail[length_key] = length_value[0] if len(length_value) > 0 else None

        # --------------------------------------------------------------

        bedrooms_key, bedrooms_value = self.__model.get_bedrooms()
        detail[bedrooms_key] = bedrooms_value[0] if len(bedrooms_value) > 0 else None

        # --------------------------------------------------------------

        rooms_key, rooms_value = self.__model.get_rooms()
        detail[rooms_key] = rooms_value[0] if len(rooms_value) > 0 else None

        # --------------------------------------------------------------

        legal_key, legal_value = self.__model.get_legal()
        detail[legal_key] = legal_value[0] if len(legal_value) > 0 else None

        # --------------------------------------------------------------

        _total_score = 0
        _attr_score  = 0

        for key in detail:
            value = detail[key]
            _total_score += 1
            _attr_score  += 1 if value is not None else 0


        eff = _attr_score/(_total_score if _total_score > 0 else 1)
        self.__parse_result = {"detail":detail,"code":"OK","eff": eff}
        return detail






