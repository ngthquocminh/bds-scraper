#!/usr/bin/env python
import os
import pika
import sys
import signal
import json
from subprocess import Popen
import traceback
import psutil
from Settings import Settings
from database import DBObject
import subprocess

def message_loads(message:str):
    try:
        data = {part.split(":")[0]:part.split(":")[1] for part in message.split(" ")}        
        return data 
    except:
        traceback.print_exc()

def message_dumps(data:dict):
    try:
        return " ".join([key + ":" + data[key] for key in data])
    except:
        traceback.print_exc()

def main():
    
    parameters = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        command = "nothing"
        try:
            body = body.decode('ascii')
            message = message_loads(body)
            command = message["command"]

            if command == "crawl":

                pid = int(open("data.lock","r").read())
                if not psutil.pid_exists(pid):
                    Popen(['python', 'worker.py', body])
                else:
                    command = "is runing"
            
            elif command == "parse":
                
                pid = int(open("data.lock","r").read())
                if not psutil.pid_exists(pid):
                    file = open("parse_posts.data","w")
                    file.write(message["posts"])
                    file.close()
                    model = message["model"] if "model" in message else "auto"
                    type = message["type"] if "type" in message else "all"
                    site = message["site"] if "site" in message else "all"

                    Popen(['python', 'worker.py', "command:parse site:%s type:%s model:%s"%(site,type,model)])
                else:
                    command = "is runing"
                   
            elif command == "stop":
                                
                db = DBObject()
                db.cancel_task(Settings.worker_id)
                pid = int(open("data.lock","r").read())
                os.kill(pid, signal.SIGTERM) 
                subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")
                subprocess.call("TASKKILL /f  /IM  CHROME.EXE")


            elif command == "pause":

                db = DBObject()
                pid = int(open("data.lock","r").read())
                _working, _as = db.workAs(Settings.worker_id)
                if _working:                    
                    db.pause_task(Settings.worker_id)
                    os.kill(pid, signal.SIGTERM) 
                    subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
                    subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")
                else:
                    if not psutil.pid_exists(pid):
                        Popen(['python', 'worker.py', "command:%s resume:1"%(_as)])
                    else:
                        command = "is runing"


            elif command == "shield":
                shield_on = True if (("shield" in message and int(message["shield"]) == 1) or (not Settings.isShieldEnable())) else False
                Settings.enableShield(shield_on)
            else:
                command = "nothing"
                ""
        except:
            traceback.print_exc()

        print(" [x] Received \n    -> Do %s" % (command))

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
