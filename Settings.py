from database import DBObject

db = DBObject()
class Settings(object):
    worker_id = "64875478"
    worker_name = "worker01"

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

    def enableShield():
        try:
            db.set_shield_on(Settings.worker_id)
            with open("shield.data","w") as shield:
                shield.write("TRUE")
                shield.close()

            return True
            
        except:
            return False