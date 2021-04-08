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
        endpoint = "https://synapselynk.documents.azure.com:443"
        key = "EOdozau4gWO1KCXaSWxffMEp25qh1ZUc53JNECyFB460ov2xe5WggWXmrBEX0u9TIksOa5qo2PO91bZ9STMjCg=="

        # create_cosmos_client
        client = CosmosClient(endpoint, key)

        database_name = 'bds_database'
        client.create_database_if_not_exists(database_name)
        database = client.get_database_client(database_name)
        container_name = 'parse_data'
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
    cosmos.insert(data_row)
