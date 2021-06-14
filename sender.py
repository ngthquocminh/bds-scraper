#!/usr/bin/env python
import pika

# parameters = pika.ConnectionParameters(host='localhost')
credentials = pika.PlainCredentials('worker01', 'worker01--')
parameters = pika.ConnectionParameters('18.217.53.191',
                                       5672,
                                       '/',
                                       credentials)
try:

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='hello1')

    channel.basic_publish(exchange='', routing_key='hello1', body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()

except pika.exceptions.ProbableAuthenticationError:
    print("Login failed")
except pika.exceptions.AMQPConnectionError:
    print("Can not reach the client")
except:
    print("Unknow error")
