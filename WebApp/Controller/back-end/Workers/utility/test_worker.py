import pika


def test_connection(ip, name, password):
    credentials = pika.PlainCredentials(name, password)
    parameters = pika.ConnectionParameters(
        ip,
        5672,
        '/',
        credentials)

    try:
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        channel.queue_declare(queue='hello1')
        channel.basic_publish(exchange='', routing_key='hello1', body='Hello World!')

        connection.close()
        return "Connected successfully!"
    except pika.exceptions.ProbableAuthenticationError:
        return "Login failed: check the worker's name or password"
    except pika.exceptions.AMQPConnectionError:
        return "Can not reach the worker: check the IP address"
    except:
        return "Unknown error"