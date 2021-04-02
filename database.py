from pymongo import MongoClient
from pprint import pprint


class MongoDB:
    
    client = MongoClient("mongodb://synapselink:eVPegAamvOAeDBunQP63s0zcgFCIeqATZlCKpSL8xczE7KsRRt7nKoteatXZshyxkpxuaNi0IlBArbo5wUkgSQ%3D%3D@synapselink.mongo.cosmos.azure.com:10255/?authSource=admin&replicaSet=globaldb&maxIdleTimeMS=120000&readPreference=primary&appname=MongoDB%20Compass&retryWrites=false&ssl=true")
    db=client.Data

    def __init__(self):
        ""

    def status(self):
        return self.db.command("serverStatus")

    def getdb(self):
        return self.db

    def insert_to(self, jsonrow):
        result = self.db.ParsedData.insert_one(jsonrow)
        return result

    def pprint(result):
        pprint(result)

