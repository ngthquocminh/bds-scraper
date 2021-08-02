import json
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup
import traceback
from database import DBObject

# file = open("post_urls_batdongsan_nharieng5.json","r")
# file_write = open("post_urls_batdongsan_nharieng5_x.json","w")

# for i in range(50000):
#     try:
#         row = file.readline()
#         if row == None or len(row)<10:
#             continue
#         row = json.loads(row)
#         for _r in row:
#             row = row[_r]
#             break
#         row["url"] = row["url"].strip()
#         row["url_hash"] = hashlib.md5(row["url"].encode()).hexdigest()
#         soup = BeautifulSoup(row["html"],'html.parser')
#         _date = soup.select_one("#product-detail-web > div.detail-product > div.product-config.pad-16 > ul > li:nth-child(1) > span.sp3").get_text()
#         _date = _date.strip()
#         _date = datetime.strptime(_date, '%d/%m/%Y').date()
#         row["post_date"] = _date.strftime("%d/%m/%Y")
        
#         file_write.write(json.dumps(row) + "\n")
#         print(i,". ",_date)
#     except:
#         print("-"*20)
#         print("ERROR",i,":")
#         traceback.print_exc()
#         print("-"*20)


file = open("post_urls_batdongsan_dat4_x.json","r")

data = []
for i in range(50):
    try:
        row = file.readline()
        if row == None or len(row)<10:
            continue
        row = json.loads(row)
        
        row["url"] = row["url"].strip()
        row["url_hash"] = hashlib.md5(row["url"].encode()).hexdigest()

        soup = BeautifulSoup(row["html"],'html.parser')
        _date = soup.select_one("#product-detail-web > div.detail-product > div.product-config.pad-16 > ul > li:nth-child(1) > span.sp3").get_text()
        _date = _date.strip()
        _date = datetime.strptime(_date, '%d/%m/%Y').date()
        row["post_date"] = _date.strftime("%d/%m/%Y")

        row.pop('parser', None)

        data.append(row)

        print(i,". ",_date)
    except:
        print("-"*20)
        print("ERROR",i,":")
        traceback.print_exc()
        print("-"*20)

db = DBObject()
db.insert_html_data(json_row=data, many=True)

