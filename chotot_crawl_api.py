import argparse
import multiprocessing
import urllib
import urllib.request
import json
import traceback
import hashlib
from datetime import datetime, date, timedelta
from lxml import etree, html
from slugify import slugify
import re
# pip install python-slugify

LIMIT_POSTS_PER_REQUEST = 100
CATE_ID = "1040" # {"nha":"1020","chung-cu":"1010","":""
NUM_SPLIT = 20000

parser = argparse.ArgumentParser()
parser.add_argument("process", help="The number of processes you want to run")
args = parser.parse_args()

_num_process = 1
try: 
    _num_process = int(args.process)
except:
    """"""

legal_document_data = {
    1 : "Đã có sổ",
    2 : "Đang chờ sổ",
    3 : "Giấy tờ khác"
}

cate_type_data = {
    "1020" : {
        1 : "Nhà mặt phố", 
        3 : "Nhà ngõ", 
        2 : "Nhà biệt thự", 
        4 : "Nhà phố liền kề"
    },
    "1010" : {
        1: "Chung cư",
        2: "Căn hộ dịch vụ",
        3: "Duplex",
        4: "Penthouse",
        5: "Tập thể",
        6: "Officetel"
    },
    "1040" : {
        1: "Đất thổ cư",
        2: "Đất nền dự án",
        3: "Đất công nghiệp",
        4: "Đất nông nghiệp"
    }
}
print(cate_type_data["1020"][1])
def get_cate_type(cate, type):
    try:
        return cate_type_data[cate][type]
    except:
        print("error: ", cate, type)
        traceback.print_exc()
        return None
    
# _profile_api = "https://gateway.chotot.com/v1/public/profile/{acc_oid}".format(
#         acc_oid="<oid>"
#     )

def get_data_from_api(url):
    """
    Get HTML (page source) of a given url
    """

    for i in range(3):
        try:
            request = urllib.request.Request(
                url, 
                data=None,
                headers={"User-Agent": "Mozilla/5.0"})  

            html = urllib.request.urlopen(request).read()
            return html
        except:
            ""
            print("Retry")

    print("Failed")
    return None

def get_date( date_str):
    _date = None
    try:
        date_str = slugify(date_str.lower())
        _l = date_str.split("-")
        if "hom-qua" in date_str:
            _date = date.today() - timedelta(days=1)
        elif "thang" in _l:
            _n = int(_l[_l.index("thang") - 1][0])
            _date = date.today() - timedelta(days=30*_n)
        elif "tuan" in _l:
            _n = int(_l[_l.index("tuan") - 1][0])
            _date = date.today() - timedelta(days=7*_n)
        elif "ngay" in _l:
            _n = int(_l[_l.index("ngay") - 1][0])
            _date = date.today() - timedelta(days=1)
        elif "hom-nay" in date_str or "gio" in _l or "phut" in _l:
            _date = date.today()
        else:
            _date = datetime.strptime(date_str, '%d/%m/%Y').date()
    except:
        _date = date.today()
        traceback.print_exc()
        
    return _date.strftime("%d/%m/%Y")

def safe_get(json, key):
    try:
        return json[key]
    except:
        None

def address_join(num, street, ward, area, region):
    address = []

    if num!=None:
        address.append(num)

    if street!=None:
        address.append(street)
    
    if ward!=None:
        address.append(ward)

    if area!=None:
        address.append(area)

    if region!=None:
        address.append(region)

    return ", ".join(address)

def save_buffer(_process_index, _buf_index, buffer):
    file_save = open("parsed_post_choto_nha_xx_pro{pro}_buf{buf}.json".format(pro=_process_index, buf=_buf_index), "w")
    file_save.write(json.dumps(buffer, indent=5))
    file_save.close()

def crawler(cate, process_index):

    finish = False
    split_save_index = 0
    
    api_index = 0
    
    buffer = []
    count = 0
    while not finish:
        api_index
        api_url = "https://gateway.chotot.com/v1/public/ad-listing?cg={cateid}&limit={limit}&o={offset}&st=s".format(
            cateid=cate,
            limit=str(LIMIT_POSTS_PER_REQUEST),
            offset=str((process_index + api_index * _num_process) * LIMIT_POSTS_PER_REQUEST)
        )
        print(api_url)
        data_dict = json.loads(get_data_from_api(api_url).decode("UTF-8"))
        
        finish = True
        
        for post in data_dict["ads"]:
            
            _post_id = safe_get(post,"list_id")
            _region = safe_get(post,"region_name")
            _area = safe_get(post,"area_name")
            _post_url = "https://nha.chotot.com/{region}/{district}/mua-ban-nha-dat/{id}.htm".format(
                region=slugify(_region if isinstance(_region, str) else ""),
                district=slugify(_area if isinstance(_area, str) else ""),
                id=str(_post_id)
            )
            try:
                post = json.loads(etree.ElementTree(
                html.fromstring(get_data_from_api(_post_url).decode("UTF-8"))
                ).xpath("//*[@id='__NEXT_DATA__']/text()")[0])["props"]["initialState"]["adView"]["adInfo"]["ad"]
            except:
                traceback.print_exc()

            _date       = str(get_date(safe_get(post,"date")))
            _category   = get_cate_type(cate, safe_get(post,"land_type")) # land_type, house_type, apartment_type 
            _street_num = safe_get(post, "street_number")
            _street     = safe_get(post,"address")
            _street     = _street if isinstance(_street, str) and "Đường" in _street else None
            _ward       = safe_get(post,"ward_name")
            _area       = safe_get(post,"area_name")
            _region     = safe_get(post,"region_name")
            _address    = address_join(_street_num,_street,_ward,_area,_region)
            _size       = safe_get(post,"size")
            _width      = safe_get(post,"width")
            _length     = safe_get(post,"length")
            _rooms      = safe_get(post,"rooms")
            _toilets    = safe_get(post,"toilets")
            _price      = safe_get(post,"price_string")

            doc = dict()
            
            doc["url_hash"]     = hashlib.md5(_post_url.encode()).hexdigest()
            doc["url"]          = _post_url
            doc["crawl_date"]   = str(date.today().strftime("%d/%m/%Y"))
            doc["parse_date"]   = doc["crawl_date"]
            doc["status"]       = 1
            
            detail = dict()
            detail["homepage"]      = "chotot.com"
            detail["date"]          = _date
            detail["title"]         = safe_get(post,"subject")
            detail["category"]      = _category
            detail["description"]   = safe_get(post,"body")
            detail["region"]        = _region.replace("Tỉnh","").strip() if isinstance(_region, str) else None 
            detail["street"]        = (_street.replace("Đường","").strip() if not re.search("Đường [0-9]+", _street) else _street) if isinstance(_street, str) else None
            detail["district"]      = _area.replace("Quận","").replace("Huyện","").strip() if isinstance(_area, str) and not re.search("Quận [0-9]+", _area) else _area
            detail["user"]          = safe_get(post,"account_name")
            detail["price"]         = _price.replace(",",".") if isinstance(_price, str) else None
            detail["address"]       = _address
            detail["surface"]       = str(_size) if isinstance(_size, int) else None
            detail["bedrooms"]      = str(_rooms) if isinstance(_rooms, int) else None
            detail["toilets"]       = str(_toilets) if isinstance(_toilets, int) else None
            detail["width"]         = str(_width) if isinstance(_width, int) else None
            detail["length"]        = str(_length) if isinstance(_length, int) else None
            detail["legal"]         = safe_get(legal_document_data, safe_get(post,"property_legal_document"))
            detail["phone"]         = safe_get(post,"phone")
            
            doc["detail"] = detail
            buffer.append(doc)
            count += 1
            if (count == NUM_SPLIT):
                save_buffer(process_index, split_save_index, buffer)
                buffer = []
                count = 0
                split_save_index += 1

            print(doc)
            finish = False

        api_index += 1
    
    save_buffer(process_index, split_save_index, buffer)
    

def main():
    cate_id = CATE_ID
    for i in range(_num_process):
        multiprocessing.Process(target=crawler, args=(cate_id, i, )).start()
    # print("https://gateway.chotot.com/v1/public/ad-listing?cg=1020&limit=1&o=1")

if __name__ == "__main__":
    main()