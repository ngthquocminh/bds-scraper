from pymongo import MongoClient
from pprint import pprint
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import pymongo


class MongoDB:


    def __init__(self):

        self.client = MongoClient(
            "mongodb+srv://lvtn:minh1709@cluster0.978ef.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        )

        self.lvtn_database   = "lvtn_database"
        self.parsed_db_name  = "parsed_db"
        self.html_db_name    = "html_db"

        self.db_parsed = self.client[self.lvtn_database][self.parsed_db_name]
        self.db_html  =  self.client[self.lvtn_database][self.html_db_name]

    def insert_parsed_data(self, json_row=None):
        if json_row is None:
            return 
        result = self.db_parsed.insert_one(json_row)
        return result

    
    def insert_html_data(self, json_row=None):
        if json_row is None:
            return 
        result = self.db_html.insert_one(json_row)
        return result

    def query_html_db(self, query_dict: dict):        
        return self.db_html.find(query_dict)

    def query_parsed_db(self, query_dict: dict):        
        return self.db_parsed.find(query_dict)

    def pprint(self, result: pymongo.results.InsertOneResult):
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
    database = MongoDB()
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
        
        if not isinstance(self.database, MongoDB):
            self.database = MongoDB()

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

