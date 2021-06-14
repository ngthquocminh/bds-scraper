import pika
import sys
import os

parameters = pika.ConnectionParameters(host='localhost')




connection = pika.BlockingConnection()

channel = connection.channel()

channel.queue_declare(queue='testing_worker_queue')


def on_request(ch, method, props, body):
    n = body

    print(" [.] Worker responded: ", body)
    response = "Connected"
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
    # ch.basic_publish(exchange='',
    #                  routing_key=props.reply_to,
    #                  properties=pika.BasicProperties(correlation_id = \
    #                                                      props.correlation_id),
    #                  body=str(response))
    # ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='testing_worker_queue', on_message_callback=on_request)

print(" [x] Connecting to worker")
channel.start_consuming()
connection.close()