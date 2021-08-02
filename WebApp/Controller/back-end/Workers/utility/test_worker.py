import pika
from Workers.utility.TaskSender import TaskSender

def test_connection(ip, name, password):

    test_connection = TaskSender()
    
    test_connection = test_connection.connect(host=ip,name=name,password=password)
    if isinstance(test_connection, TaskSender):
        test_connection.send_task(queue="hello").close()
        return "Connected successfully!!"
    else:
        return test_connection
