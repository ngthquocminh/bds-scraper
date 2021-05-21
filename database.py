from pymongo import MongoClient
from pprint import pprint
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import pymongo


class MongoDB:
    
    def __init__(self):
        self.client = MongoClient(
            "mongodb://synapselynk"
            ":SaHj2L86s2pC0YvvAdV26u25M74RDhaWhUglTyRsuKa0xrcFdfh9y1RZkTZQX55F12bpd6Dc3WqlBWWcvCI32Q==@synapselynk"
            ".mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
            "&appName=@synapselynk@")
        self.db = self.client.bds_database

    def status(self):
        return self.db.command("serverStatus")

    def getdb(self):
        return self.db

    def insert_to(self, jsonrow=None):
        if jsonrow is None:
            return
        result = self.db.parse_data_02.insert_one(jsonrow)
        return result

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

