from pymongo import MongoClient
from pprint import pprint
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import traceback

class MongoDB:
    ASC = 1
    DES = -1
    def __init__(self):

        self.client = MongoClient(
            "mongodb+srv://lvtn:minh1709@cluster0.978ef.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            ,ssl=True,ssl_cert_reqs='CERT_NONE'
        )

        self.main_database   = "lvtn_database"
        self.parsed_db_name  = "parsed_db"
        self.html_db_name    = "html_db"
        self.worker_db_name  = "worker_info"
        self.logs_db_name    = "worker_logs"
        self.db_parser_name  = "parser_model"

        self.db_parsed  = self.client[self.main_database][self.parsed_db_name]
        self.db_html    = self.client[self.main_database][self.html_db_name]
        self.db_worker  = self.client[self.main_database][self.worker_db_name]
        self.db_logs    = self.client[self.main_database][self.logs_db_name]
        self.db_parser  = self.client[self.main_database][self.db_parser_name]


    def get_parser_model(self,parser_name):
        res = self.db_parser.find({"site":parser_name})   
        return [i for i in res]

    def update_parser_attr(self,data:dict):
        res = self.db_parser.update_one({"id": data["id"]}, {"$set":{"$and":[{attr:data[attr]} for attr in data]}})
        return res

    def insert_parser_attr(self,data:dict):
        res = self.db_parser.insert_one(data)
        return res

    def delete_parser_attr(self,id:str):
        res = self.db_parser.delete_one({"id":id})
        return res

    def insert_parsed_data(self, json_row=None, many=False):
        result = None
        if json_row is None:
            return 

        if isinstance(json_row,dict) and not many:
            if self.db_parsed.find_one({"url_hash":json_row["url_hash"]}) == None:
                result = self.db_parsed.insert_one(json_row)
            else:
                result = self.db_parsed.replace_one({"url_hash":json_row["url_hash"]},json_row)

        elif isinstance(json_row,list) and many:
            for row in json_row:
                if self.db_parsed.find_one({"url_hash":row["url_hash"]}) == None:
                    result = self.db_parsed.insert_one(row)
                else:
                    result = self.db_parsed.replace_one({"url_hash":row["url_hash"]},row)
            
        return result

    def get_collection(self,collection_name:str):
        return self.client[collection_name]
    
    def update_html_post_status(self,url_hash, status):
        res = self.db_html.update_one({"url_hash":url_hash},{"$set":{"status":str(status)}})
        return res

    def insert_html_data(self, json_row=None, many=False):
        result = None
        if json_row is None:
            return 

        if isinstance(json_row,dict) and not many:
            if self.db_html.find_one({"url_hash":json_row["url_hash"]}) == None:
                result = self.db_html.insert_one(json_row)
            else:
                result = self.db_html.replace_one({"url_hash":json_row["url_hash"]},json_row)

        elif isinstance(json_row,list) and many:
            for row in json_row:
                if self.db_html.find_one({"url_hash":row["url_hash"]}) == None:
                    result = self.db_html.insert_one(row)
                else:
                    result = self.db_html.replace_one({"url_hash":row["url_hash"]},row)
            
        return result

    def query_html_db(self, query_dict: dict, limit=1,sort=None):    
        res = self.db_html.find(query_dict,limit=limit)
        if sort:
            res = res.sort(sort)
        return [i for i in res]

    def query_parsed_db(self, query_dict: dict, limit=1, sort=None):   
        res = self.db_parsed.find(query_dict,limit=limit)
        if sort:
            res = res.sort(sort)     
        return [i for i in res]

    def query_wokers_info(self, worker_id):
        res = self.db_worker.find_one({"worker_id": worker_id})
        return res["info"] if "info" in res and isinstance(res["info"],dict) else {}

    def update_wokers_info(self, worker_id, worker_info):
        res = self.db_worker.update_one({"worker_id": worker_id}, {"$set":{"info":worker_info}})
        return res

    def query_wokers_logs(self, worker_id, task_id):
        res = self.db_logs.find_one({"$and":[{"worker_id":worker_id},{"task_id":task_id}]})
        return res

    def create_wokers_log(self, worker_init_log:dict):
        res = self.db_logs.insert_one(worker_init_log)
        return res

    def update_wokers_log(self, worker_id, task_id, saved_posts:list, error_posts:list):
        res = self.db_logs.update_one({"$and":[{"worker_id":worker_id},{"task_id":task_id}]},{"$set":{"saved_posts":saved_posts,"error_posts":error_posts}})
        return res

    def update_wokers_info(self, worker_id, worker_info):
        res = self.db_worker.update_one({"worker_id": worker_id}, {"$set":{"info":worker_info}})
        return res

    def get_all_free_workers(self):
        res = self.db_worker.find({"$or":[{"info": None},{"info.status":{"$regex":r"^.*(finish).*$"}}]})
        return [w for w in res]

    def get_all_workers(self):
        res = self.db_worker.find()
        return [w for w in res]
    
    def get_worker(self, worker_id):
        res = self.db_worker.find_one({"worker_id": worker_id})
        return res

    def set_shield_on(self, worker_id):
        try:
            w = self.db_worker.find_one({"worker_id": worker_id})
            status = w["info"]["status"]
            if status == "crawling":
                res =self.db_worker.update_one({"$and":[{"worker_id": worker_id},{"info.status":{"$regex":r"^.*crawling.*$"}}]},{"$set":{"info.status":"(anti)crawling"}})
                return True
            return False
        except:
            ""
        return False

    def set_shield_off(self, worker_id):
        
        res = self.db_worker.update_one({"$and":[{"worker_id": worker_id},{"info.status":{"$regex":r"^.*crawling.*$"}}]},{"$set":{"info.status":"crawling"}})
        return res

    def cancel_task(self, worker_id):
        res = self.db_worker.update_one({"worker_id": worker_id},{"$set":{"info":None}})
        return res

    def pause_task(self, worker_id):
        try:
            w = self.db_worker.find_one({"worker_id": worker_id})
            status = w["info"]["status"]
            res = self.db_worker.update_one({"worker_id": worker_id},{"$set":{"info.status":"(pause)%s"%(status)}})
            return res
        except:
            return None

    def finishing_task(self, worker_id):
        try:
            w = self.db_worker.find_one({"worker_id": worker_id})
            status = w["info"]["status"].replace("(pause)","")
            res = self.db_worker.update_one({"worker_id": worker_id},{"$set":{"info.status":"(finish)%s"%(status)}})
            return res
        except:
            return None

    def isWorking(self, worker_id):
        try:
            w = self.db_worker.find_one({"worker_id": worker_id})
            if isinstance(w["info"]["status"], str) and ("pause" not in w["info"]["status"]):
                return True
        except:
            ""
        return False

    def workAs(self, worker_id):
        try:
            w = self.db_worker.find_one({"worker_id": worker_id})
            print(w)
            if isinstance(w["info"]["status"], str):
                return (("pause" not in w["info"]["status"]), ("crawl" if "crawling" in w["info"]["status"] else "parse"))
            
        except:
            traceback.print_exc()
            ""
        return (None, "null")

    def pprint(self, result):
        pprint(result)


class DBObject: # Interface

    def __init__(self):
        self.db_object = MongoDB()

    def isWorking(self, worker_id):
        return self.db_object.isWorking(worker_id)

    def workAs(self, worker_id):
        return self.db_object.workAs(worker_id)

    def get_parser_model(self,parser_name):
        return self.db_object.get_parser_model(parser_name)

    def cancel_task(self, worker_id):
        return self.db_object.cancel_task(worker_id)  
    
    def finishing_task(self, worker_id):
        return self.db_object.finishing_task(worker_id)

    def pause_task(self, worker_id):
        return self.db_object.pause_task(worker_id)  

    def get_collection(self,collection_name:str):
        return self.db_object.get_collection(collection_name)  

    def insert_parsed_data(self, json_row=None, many=False):
        return self.db_object.insert_parsed_data(json_row, many)

    def update_html_post_status(self,url_hash, status):
        return self.db_object.update_html_post_status(url_hash,status)
        
    def insert_html_data(self, json_row=None, many=False):
        return self.db_object.insert_html_data(json_row, many)

    def query_html_db(self, query_dict: dict, limit=0, sort=None):        
        return self.db_object.query_html_db(query_dict, limit=limit, sort=sort)

    def query_parsed_db(self, query_dict: dict, limit=0, sort=None):        
        return self.db_object.query_parsed_db(query_dict, limit=limit, sort=sort)

    def query_wokers_info(self, worker_id):
        return self.db_object.query_wokers_info(worker_id)

    def query_wokers_logs(self, worker_id, task_id):
        return self.db_object.query_wokers_logs(worker_id, task_id)

    def update_wokers_info(self, worker_id, worker_info):
        return self.db_object.update_wokers_info(worker_id, worker_info)

    def create_wokers_log(self, worker_init_log:dict):
        return self.db_object.create_wokers_log(worker_init_log)

    def update_wokers_log(self, worker_id, start_time, saved_posts:list, error_posts:list):
        return self.db_object.update_wokers_log(worker_id,start_time,saved_posts,error_posts)

    def set_shield_on(self, worker_id):
        return self.db_object.set_shield_on(worker_id)

    def set_shield_off(self, worker_id):
        return self.db_object.set_shield_off(worker_id)

    def get_all_free_workers(self):
        return self.db_object.get_all_free_workers()
    
    def get_all_workers(self):
        return self.db_object.get_all_workers()

    def get_worker(self, worker_id):
        return self.db_object.get_worker(worker_id)

    def pprint(self, result):
        pprint(result)


class AzureCosmos:

    def __init__(self):
        endpoint = "https://synapselink1.documents.azure.com:443/"
        key = "zM8dZNCWIi03JWziWAr2JGBlU2uEsmU1651YA4p5HCKp1DpGeQ0fH3gNDCHVEId5JIhHXhTI7Rkfnl4pZurqfg=="
        # create_cosmos_client
        client = CosmosClient(endpoint, key)

        database_name = 'data'
        # database_name = 'lvtn_database'
        client.create_database_if_not_exists(database_name)
        database = client.get_database_client(database_name)
        # container_name = 'parsed_data'
        container_name = 'test'
        self.container = database.get_container_client(container_name)
        self.update_container = database.get_container_client("update_data")
        self.final_container = database.get_container_client("final_data")


    def insert(self, row_json):
        self.container.upsert_item(row_json)

    def getAll(self):
        return self.container.query_items(
            query='SELECT * FROM c',
            enable_cross_partition_query=True)


def save_to(data_row=None):
    save_to_azure_cosmos(data_row)

def save_to_mongodb(data_row):
    if data_row is None:
        return
    database = DBObject()
    database.insert_to(data_row)

def save_to_azure_cosmos(data_row):
    if data_row is None:
        return
    cosmos = AzureCosmos()
    try:
        cosmos.insert(data_row)
    except exceptions.CosmosResourceExistsError:
        return "Entity exists"

class DBTarget():

    database = None

    def __init__(self):
        self.database = AzureCosmos()

    def save_to(self):
        return save_to_azure_cosmos

    def save_to_mongodb(self, data_row):
        if data_row is None:
            return
        
        if not isinstance(self.database, DBObject):
            self.database = DBObject()

        self.database.insert_to(data_row)

    def save_to_azure_cosmos(self, data_row = None):
        if data_row is None:
            return
        res = "None"
        if not isinstance(self.database, AzureCosmos):
            self.database = AzureCosmos()
            res = "create new db"

        try:
            self.database.insert(data_row)
            return res
        except exceptions.CosmosResourceExistsError:
            return "Entity exists"

