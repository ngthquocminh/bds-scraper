import pika

# Set the connection parameters to connect to rabbit-server1 on port 5672
# on the / virtual host using the username "guest" and password "guest"
credentials = pika.PlainCredentials('worker01', 'worker01')
parameters = pika.ConnectionParameters('18.217.53.191',
                                       5672,
                                       '/',
                                       credentials)


