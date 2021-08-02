#!/usr/bin/env python
import pika
import sys
import traceback

if __name__ == '__main__':
    args = sys.argv

    parameters = pika.ConnectionParameters(host='localhost')
    # credentials = pika.PlainCredentials('worker02', 'worker02')
    # parameters = pika.ConnectionParameters('3.142.90.161',
    #                                        5672,
    #                                        '/',
    #                                        credentials)
    try:

        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        channel.queue_declare(queue='hello')

        channel.basic_publish(exchange='', routing_key='hello', body=" ".join(args[1:]))
        print(" [x] Sent %s"%args[1])
        connection.close()

    except pika.exceptions.ProbableAuthenticationError:
        print("Login failed")
    except pika.exceptions.AMQPConnectionError:
        print("Can not reach the client")
    except:
        print("Unknown error")
        traceback.print_exc()

# """
# batdongsan.com.vn
# chotot.com
# nhadat247.com.vn
# command:crawl site:batdongsan.com.vn post-date:08-2021_12-2021 shield:0 type:house limit:1000

# """