import re
from pymongo import MongoClient
from pprint import pprint
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import pymongo

class MongoDB:
    ASC = 1
    DES = -1
    def __init__(self):

        self.client = MongoClient(
            "mongodb+srv://lvtn:minh1709@cluster0.978ef.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        )

        self.main_database   = "lvtn_database"
        self.parsed_db_name  = "parsed_db"
        self.html_db_name    = "html_db"
        self.worker_db_name  = "worker_info"

        self.db_parsed = self.client[self.main_database][self.parsed_db_name]
        self.db_html  =  self.client[self.main_database][self.html_db_name]
        self.db_worker  =  self.client[self.main_database][self.worker_db_name]

    def insert_parsed_data(self, json_row=None, many=False):
        result = None
        if json_row is None:
            return 
        if isinstance(json_row,dict) and not many:
            result = self.db_parsed.insert_one(json_row)
        if isinstance(json_row,list) and many:
            result = self.db_parsed.insert_many(json_row)

        return result

    def get_collection(self,collection_name:str):
        return self.client[collection_name]
    
    def insert_html_data(self, json_row=None, many=False):
        result = None
        if json_row is None:
            return 
        if isinstance(json_row,dict) and not many:
            result = self.db_html.insert_one(json_row)
        if isinstance(json_row,list) and many:
            result = self.db_html.insert_many(json_row)
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
        res = self.db_worker.find({"worker_id": worker_id},limit=1)
        return res

    def update_wokers_info(self, worker_id, worker_info):
        res = self.db_parsed.update_one({"worker_id": worker_id}, {"$set":{"info":worker_info}})
        return res

    def pprint(self, result):
        pprint(result)


class DBObject: # Interface

    def __init__(self):
        self.db_object = MongoDB()

    def get_collection(self,collection_name:str):
        return self.db_object.get_collection(collection_name)  

    def insert_parsed_data(self, json_row=None, many=False):
        return self.db_object.insert_parsed_data(json_row, many)
    
    def insert_html_data(self, json_row=None, many=False):
        return self.db_object.insert_html_data(json_row, many)

    def query_html_db(self, query_dict: dict, limit=0, sort=None):        
        return self.db_object.query_html_db(query_dict, limit=limit, sort=sort)

    def query_parsed_db(self, query_dict: dict, limit=0, sort=None):        
        return self.db_object.query_parsed_db(query_dict, limit=limit, sort=sort)

    def query_wokers_info(self, worker_id):
        return self.db_object.query_wokers_info(worker_id)

    def update_wokers_info(self, worker_id, worker_info):
        return self.db_object.update_wokers_info(worker_id, worker_info)

    def pprint(self, result):
        pprint(result)


class AzureCosmos:

    def __init__(self):
        endpoint = "https://synapsel1nk.documents.azure.com:443/"
        key = "r0EEApAfBwKARscLmgjPzdAYVVxFbLy5pOf2AU0yLL6FrcHFjySI3NYnb5zpHSvVPFkvRKI4yUTTRIZTmt4mCg=="
        # create_cosmos_client
        client = CosmosClient(endpoint, key)

        database_name = 'lvtn_database'
        client.create_database_if_not_exists(database_name)
        database = client.get_database_client(database_name)
        container_name = 'parsed_data'
        self.container = database.get_container_client(container_name)

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

