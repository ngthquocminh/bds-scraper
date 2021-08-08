import re
from Workers.utility.Database import DBObject
from Workers.utility.LibFunc import d_range, searchPostHtml
from Workers.utility.TaskSender import TaskSender
from datetime import datetime, timedelta

db = DBObject()

def doParse(request: dict):
    print(request)
    list_post = [post["url_hash"] for post in searchPostHtml(request)["content"]]
    if len(list_post) < 1:
        return False
        m
    num_workers = int(request["num_workers"]) if "num_workers" in request else None
    type  = request["type"]  if "type"  in request else "all"
    site  = request["site"]  if "site"  in request else "all"
    model = request["model"] if "model" in request else "null"

    workers = db.db_object.get_all_free_workers()
    workers = workers[:num_workers]

    print(workers)
    if len(list_post) < 10:
        print(len(list_post))
        workers = workers[0:1]

    num_posts_per_worker = int(len(list_post)/len(workers))
    print(num_posts_per_worker)
    print(workers)

    for i, worker in enumerate(workers):
        data_message = "command:parse site:%s type:%s model:%s"%(site,type,model) + " posts:" + "_".join(list_post[i*num_posts_per_worker:(i+1)*num_posts_per_worker if (i < len(workers)-1) else None])

        print(data_message)
        task = TaskSender()
        task.connect(host=worker["ip"], password=worker["password"], name=worker["name"])\
        .send_task("hello",message=data_message).close()

    return

def stopWorker(id):
    worker = db.get_worker(id)
    if isinstance(worker,dict):
        task = TaskSender()
        conn = task.connect(host=worker["ip"], password=worker["password"], name=worker["name"])
        if isinstance(conn, TaskSender):
            conn.send_task("hello",message="command:stop").close()
            print("Connection OK!")
            return True
        print(conn)

    return False

def pauseWorker(id):
    worker = db.get_worker(id)
    if isinstance(worker,dict):
        task = TaskSender()
        conn = task.connect(host=worker["ip"], password=worker["password"], name=worker["name"])
        if isinstance(conn, TaskSender):
            conn.send_task("hello",message="command:pause").close()
            print("Connection OK!")
            return True
        print(conn)

    return True

def stopAllWorkers():
    workers = db.get_all_workers()
    for worker in workers:
        task = TaskSender()
        conn = task.connect(host=worker["ip"], password=worker["password"], name=worker["name"])
        if isinstance(conn, TaskSender):
            conn.send_task("hello",message="command:stop").close()
            print("Connection OK!")
        else:
            print(conn)
    return

def toggleShield(id):
    worker = db.get_worker(id)
    if isinstance(worker,dict):
        task = TaskSender()
        conn = task.connect(host=worker["ip"], password=worker["password"], name=worker["name"])
        if isinstance(conn, TaskSender):
            conn.send_task("hello",message="command:shield").close()
            print("Connection OK!")
            return True
        print(conn)
    return False

def getAllWorkers():
    workers = db.get_all_workers()
    result = []
    for w in workers:

        worker = {}
        worker["id"] = w["worker_id"]
        worker["name"] = w["name"]
        if w["info"] == None:
            worker["status"] = "free"
            worker["info"] = ""
        else:
            worker["status"] = w["info"]["status"]
            worker["info"]   = w["info"]["str_info"]

        result.append(worker)
    return result


def doCrawl(request: dict):

    site = request["site"] if "site" in request else None
    num_workers = int(request["num_workers"]) if "num_workers" in request else None
    date = request["post_date"] if "post_date" in request else None
    shield = 1 if "shield" in request and request["shield"] == True else 0
    type = request["type"] if "type" in request else "all"
    limit_post = int(request["limit"]) if "limit" in request else -1

    workers = db.db_object.get_all_free_workers()
    workers = workers[:num_workers]

    # limit and date are devider params

    if site is not None and len(workers) > 0:
        message_origin = "command:crawl site:{site} shield:{shield} type:{type}".format(site=site,shield=shield,type=type)
        
        date_range = d_range(date)

        workers_len = len(workers)
        date_range_len = len(date_range)

        if date_range_len == 0: # set default date when input is None:
            date_range_len = workers_len if workers_len < limit_post else limit_post
            from_month = datetime.now() - timedelta(days=date_range_len*31) 
            to_month = datetime.now()
            date_range = d_range({"from":from_month.strftime("%m/%Y"),"to":to_month.strftime("%m/%Y")})
            print(date_range)


        if (limit_post <  workers_len and limit_post > 0) or date_range_len < workers_len: # devider must be >= num of workers
            workers = workers[0:workers_len if workers_len < date_range_len else date_range_len]
            workers_len = len(workers)    


        limit_per_worker = int(limit_post / workers_len) if limit_post >  0 else -1
        date_range_per_worker = int(date_range_len / workers_len)
        for i, worker in enumerate(workers):

            this_limit = limit_per_worker if i < workers_len - 1 and limit_post > 0 else (limit_post - limit_per_worker*i)
            data_message = message_origin + " limit:{limit}".format(limit=this_limit) 
            
            _date_range = date_range[i*date_range_per_worker:(i+1)*date_range_per_worker if (i < workers_len - 1) else None]
            _date_range = [_date_range[0],_date_range[-1]]
            _date_range = [_date[0] + "-" + _date[1] for _date in _date_range]

            data_message += " post-date:" + "_".join(_date_range)
            
            task = TaskSender()
            conn = task.connect(host=worker["ip"], password=worker["password"], name=worker["name"])
            if isinstance(conn, TaskSender):
                conn.send_task("hello",message=data_message).close()
                print("Connection OK!")
            else:
                print(conn)
            print(worker["ip"], worker["password"], worker["name"], data_message)

        return True

    return False