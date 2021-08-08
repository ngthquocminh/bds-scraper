#!/usr/bin/env python
import pika
from datetime import datetime, date, timedelta

num_workers = 3

def calling(worker, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=worker)

    channel.basic_publish(exchange='', routing_key=worker, body=data)
    # print(" [x] Sent to worker1")
    connection.close()

def get_type(i):
    __ = ["nha","dat","can-ho/chung-cu", "all"]
    return __[i-1]

def main():
    
    while True:
        print("")
        print("="*15,"CRAWLING SYSTEM","="*15)
        print("1. Crawl data")
        print("2. Parse data")
        task = int(input())

        if task == 1:
            print("")
            print(" > Setting up Crawling:")
            print("+ Type: 1. Nhà; 2. Đất; 3. Căn hộ/chung cư 4. All")
            _type = int(input())
            print("+ Date from: (DD/MM/YYYY)")
            _date_from = str(input())
            print("+ Date to: (DD/MM/YYYY)")
            _date_to = str(input())
            print("-"*5)
            print("Calling workers ... ")

            _date_from = datetime.strptime(_date_from, '%d/%m/%Y').date()
            _date_to = datetime.strptime(_date_to, '%d/%m/%Y').date()

            _days = (_date_to - _date_from).days + 1
            _num_calling_workers = num_workers if _days >= num_workers else _days
            days_factor = _days/_num_calling_workers
            for i in range(0, _num_calling_workers):

                _dfrom__ = (_date_from + timedelta(days=days_factor*i))
                _dto____ = (_dfrom__ + timedelta(days=(days_factor - 1) if i < _num_calling_workers else (_days - days_factor*i - 1)))

                _worker = "worker"+str(i+1)
                _data =  str(task) + "|" + _dfrom__.strftime("%d/%m/%Y") + "|" + _dto____.strftime("%d/%m/%Y") + "|" + get_type(_type)
                print(" Sent to ", _worker, " > ", _data)
                calling(_worker, _data)


        elif task == 2:
            print("")
            print(" > Setting up Parsing:")
            print("Parse status: (0, 1, 2 ...)")
            _stts = int(input())
            _data = str(task) + "|" + str(_stts)
            for i in range(0, num_workers):
                _worker = "worker"+str(i+1)
                calling(_worker, _data)
        else:
            "Error"

    # calling("worker1", "1/1/2021|27/03/2021|dat")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
