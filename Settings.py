from database import DBObject
import json
import traceback

db = DBObject()

data_settings = {}
try:
    settings_file = open("worker.settings","r")
    data_settings = json.loads(settings_file.read())
except:
    traceback.print_exc()
    ""


class Settings(object):

    worker_id = data_settings["worker_id"] if "worker_id" in data_settings else ""
    worker_name = data_settings["worker_name"] if "worker_name" in data_settings else ""

    def isShieldEnable():
        try:
            if (open("shield.data").read() == "TRUE"):
                return True
            else:
                return False
        except:
            return False

    def disableShield():
        try:
            db.set_shield_off(Settings.worker_id)
            with open("shield.data","w") as shield:
                shield.write("FALSE")
                shield.close()

            return True

        except:
            return False

    def enableShield(on=None):
        try:
            if on is None or on is True:
                if db.set_shield_on(Settings.worker_id):
                    with open("shield.data","w") as shield:
                        shield.write("TRUE")
                        shield.close()
            else:
                Settings.disableShield()

            return True
            
        except:
            return False