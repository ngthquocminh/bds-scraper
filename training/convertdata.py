import pymongo
import re
import json

_re = lambda r, v, l: re.compile(r).search(str(v)) and len(str(v)) >= l

def check_validate(key, value):
    
    if value == None or ("<eof>" in str(value)) or len(str(value)) < 1:
        return False
    
    if key=="price":
        return _re(r'[0-9]+', value, 3) 
    
    if key == "front":
        return _re(r'[0-9]+', value, 2) 
    
    if key == "surface":
        return _re(r'[0-9]+', value, 2) 
    
    if key == "room":
        return _re(r'[0-9]+', value, 1) 
    
    if key == "floor":
        return _re(r'[0-9]+', value, 1) 
    
    if key == "title":
        return len(str(value)) >= 20
    
    if key == "date":
        return len(str(value)) >= 5
    
    if key == "phone":
        return _re(r"0|\+84[0-9]+",value.replace(" ",""),9)
    
    if key == "email":
        return _re(r"[a-zA-Z0-9.]+@[a-zA-Z0-9.]+.[a-z]+",value.replace(" ",""),9)
    
    if key == "address":
        return len(str(value)) >= 10
    
    if key == "type":
        return len(str(value)) >= 5
    
    if key == "description":
        return len(str(value)) >= 50
        
    if key == "user":
        return len(str(value)) >= 2
    
    return False

def changekey(key):
    if key == "surface":
        return "area"
    if key == "user":
        return "saller"
    if key == "room":
        return "rooms"
    if key == "floor":
        return "floors"    
    
    return key
    
def new_attr():
    ""

def main():
    
    myclient = pymongo.MongoClient("mongodb://synapselynk:SaHj2L86s2pC0YvvAdV26u25M74RDhaWhUglTyRsuKa0xrcFdfh9y1RZkTZQX55F12bpd6Dc3WqlBWWcvCI32Q==@synapselynk.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@synapselynk@")
    mydb = myclient["bds_database"]
    mycol = mydb["parse_data"]

    query = None
    mydoc = mycol.find(query)
    index = 0
    for post in mydoc:
        # print(post)
        print(post["url"])
        detail = post["detail"]
        # print(detail)
        for key in detail:
            value = detail[key]
            
            if check_validate(key, value):
                key = changekey(key)
                print(key, ": ", value)
                                
                
        index += 1
        if index > 100:
            break
        
if __name__ == "__main__":
    main()