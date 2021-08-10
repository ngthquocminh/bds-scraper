
import pika
import sys
import traceback

class TaskSender():
    def __init__(self):
        """Initial"""
        return

    def connect(self,host,name=None,password=None,port=5672):
        # name = None
        try:
            if (name is not None) and (password is not None) and isinstance(password,str) and isinstance(name,str):
                credentials = pika.PlainCredentials(name,password)
                parameters = pika.ConnectionParameters(host=host, port=port,virtual_host='/',credentials=credentials)
            else:
                parameters = pika.ConnectionParameters(host='localhost')
                print("connect to localhost")

            self.connection = pika.BlockingConnection(parameters)

            self.channel = self.connection.channel()

            return self

        except pika.exceptions.ProbableAuthenticationError:
            return "Login failed"
        except pika.exceptions.AMQPConnectionError:
            return "Can not reach the client"
        except:
            traceback.print_exc()
            return "Unknown error"

    def send_task(self,queue="test",message="hi, there!"):
        try:
            self.channel.queue_declare(queue=queue)
            self.channel.basic_publish(exchange='', routing_key=queue, body=message)
        except:
            traceback.print_exc()
        return self
    
    def close(self):
        self.connection.close()



# """
# batdongsan.com.vn
# chotot.com
# nhadat247.com.vn
# command:crawl site:batdongsan.com.vn post-date:08-2021_12-2021 shield:0 type:house limit:1000

# """
