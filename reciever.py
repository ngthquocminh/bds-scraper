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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        command = "nothing"
        try:
            body = body.decode('ascii')
            message = message_loads(body)
            command = message["command"]
            if command == "crawl" or command == "parse":
                pid = int(open("data.lock","r").read())
                if not psutil.pid_exists(pid):
                    Popen(['python', 'worker.py', body])
                else:
                    command = "is runing"
            
            if command == "parse":
                pid = int(open("data.lock","r").read())
                if not psutil.pid_exists(pid):
                    open("parse_posts.data","w").write(message["posts"])
                    Popen(['python', 'worker.py', "command:parse"])
                else:
                    command = "is runing"
                   
            elif command == "stop":
                                
                db = DBObject()
                db.cancel_task(Settings.worker_id)
                
                pid = int(open("data.lock","r").read())
                os.kill(pid, signal.SIGTERM) 


            elif command == "pause":
                
                pid = int(open("data.lock","r").read())
                os.kill(pid, signal.SIGTERM) 

            elif command == "resume":

                pid = int(open("data.lock","r").read())
                if not psutil.pid_exists(pid):
                    Popen(['python', 'worker.py', "command:resume"])
                else:
                    command = "is runing"

            elif command == "shield":
                if "shield" in message:
                    if int(message["shield"]) == 1:
                        Settings.enableShield()
                    else:
                        Settings.disableShield()
                else:
                    if Settings.isShieldEnable():
                        Settings.disableShield()
                    else:
                        Settings.enableShield()

            else:
                # command = "nothing"
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
