from pymongo import MongoClient
from pprint import pprint


class MongoDB:
    client = MongoClient(
        "mongodb://synapselynk:SaHj2L86s2pC0YvvAdV26u25M74RDhaWhUglTyRsuKa0xrcFdfh9y1RZkTZQX55F12bpd6Dc3WqlBWWcvCI32Q"
        "==@synapselynk.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS"
        "=120000&appName=@synapselynk@")
    db = client.bds_database

    def __init__(self):
        ""

    def status(self):
        return self.db.command("serverStatus")

    def getdb(self):
        return self.db

    def insert_to(self, jsonrow=None):
        if jsonrow is None:
            return
        result = self.db.parse_data_02.insert_one(jsonrow)
        return result

    def pprint(self, result):
        pprint(result)
