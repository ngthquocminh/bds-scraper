from re import T
import re
import traceback
import json
from django.http import request
from django.http.request import bytes_to_text
from Workers import serializers
from Workers.models import Parser, Worker
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from Workers.utility.test_worker import test_connection
from Workers.models import Worker
from Workers.serializers import ParserSerializer, WorkerSerializer
from Workers.utility.test_parser import doTestOnParser
from Workers.utility.LibFunc import searchPostHtml
from Workers.utility.LibFunc import load_parser_set
from Workers.utility.workers_handeling import doCrawl, doParse, getAllWorkers, stopWorker, pauseWorker, stopAllWorkers, toggleShield
from Workers.utility.Database import DBObject

# Create your views here.

@csrf_exempt
def workerApi(request: request.HttpRequest, id=0):
    
    if request.method == 'GET':
        
        workers = Worker.objects.all()
        worker_serializer = WorkerSerializer(workers, many=True)
        return JsonResponse(worker_serializer.data, safe=False)

    elif request.method == 'POST':

        worker_data = JSONParser().parse(request)
        worker_serializer = WorkerSerializer(data=worker_data)
        if worker_serializer.is_valid():
            worker_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Added Failed!!", safe=False)

    elif request.method == 'PUT':        


        worker_data = JSONParser().parse(request)
        worker = Worker.objects.get(WorkerID=worker_data["WorkerID"])
        worker_serializer = WorkerSerializer(worker, data=worker_data)
        if worker_serializer.is_valid():
            worker_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)

        return JsonResponse("Added Failed!!",safe=False)

    elif request.method == 'DELETE':
        # id = 1
        id = JSONParser().parse(request)["id"]
        worker = Worker.objects.get(WorkerID=id)
        worker.delete()
        return JsonResponse("Deleted Successfully!!",safe=False) 


@csrf_exempt
def testWorkerApi(request: request.HttpRequest, id=0):
    if request.method == 'POST':
        id = JSONParser().parse(request)["id"]

        worker = Worker.objects.get(WorkerID=id)
        # worker = WorkerSerializer(worker)
        print("-"*10, worker.WorkerIP, worker.WorkerName, worker.RmqPassword)
        response = test_connection(worker.WorkerIP, worker.WorkerName, worker.RmqPassword)
        return JsonResponse(response,safe=False)

def get_sitename(uri):
    return re.compile(r"/parser/(.+)/").search(uri).group(1)

@csrf_exempt
def parserSetGetApi(request: request.HttpRequest, id=0):
    if request.method == "GET":
        site_name    = get_sitename(request.get_raw_uri())
        # print(set_name)
        parser_set = load_parser_set(site_name)
        # print(parser_set)
        return JsonResponse(parser_set, safe=False)

@csrf_exempt
def parserEditApi(request: request.HttpRequest, id=0):    
    if request.method == 'POST':
        try:
            _data = JSONParser().parse(request)
            DBObject().insert_parser_attr(data=_data)
            return JsonResponse("Added Successfully",safe=False)
        except:
            traceback.print_exc()
            return JsonResponse("Added Failed!!", safe=False)
    
    elif request.method == 'PUT':
        try:
            _data = JSONParser().parse(request)
            DBObject().update_parser_attr(_data)
            return JsonResponse("Updated Successfully",safe=False)
        except:
            traceback.print_exc()
            return JsonResponse("Added Failed!!",safe=False)
    
    elif request.method == 'DELETE':
        try:
            _id = JSONParser().parse(request)["id"]
            DBObject().delete_parser_attr(_id)
            return JsonResponse("Deleted Successfully!!",safe=False)
        except:
            return JsonResponse("Deleted Failed!!",safe=False)

    
@csrf_exempt
def testParserApi(request: request.HttpRequest):
    if request.method == 'POST':

        request = JSONParser().parse(request)
        if "model_name_for_all" in request and not request["model_name_for_all"] in ["bat-dong-san-com-vn","cho-tot-com","nha-dat-247-com-vn", "spacy-parser"]:
            request.pop("model_name_for_all")

        dict_res = doTestOnParser(request)
        return JsonResponse(dict_res, safe=False)
    
    return JsonResponse([], safe=False)

@csrf_exempt
def loadPostHtml(request: request.HttpRequest):
    if request.method == 'POST':
        request = JSONParser().parse(request)
        data = searchPostHtml(request)
        return JsonResponse(data, safe=False)
    
    return JsonResponse([], safe=False)
 

@csrf_exempt
def doCrawlApi(request: request.HttpRequest):
    if request.method == 'POST':
        request = JSONParser().parse(request)
        doCrawl(request)    
        return JsonResponse("", safe=False)
    
@csrf_exempt
def doParseApi(request: request.HttpRequest):
    if request.method == 'POST':
        request = JSONParser().parse(request)
        doParse(request)   
        return JsonResponse("", safe=False)

@csrf_exempt
def getWorkerInfoApi(request: request.HttpRequest):
    if request.method == 'GET':
        return JsonResponse(getAllWorkers(), safe=False)

@csrf_exempt
def stopWorkerApi(request: request.HttpRequest):
    if request.method == 'POST':
        request = JSONParser().parse(request)
        stopWorker(request["id"])

    return JsonResponse("", safe=False)

@csrf_exempt
def pauseWorkerApi(request: request.HttpRequest):
    if request.method == 'POST':
        request = JSONParser().parse(request)
        pauseWorker(request["id"])

    return JsonResponse("", safe=False)

@csrf_exempt
def stopAllWorkerApi(request: request.HttpRequest):    
    stopAllWorkers()
    return JsonResponse("", safe=False)

@csrf_exempt
def toggleShieldApi(request: request.HttpRequest):
    if request.method == 'POST':
        request = JSONParser().parse(request)
        toggleShield(request["id"])
    return JsonResponse("", safe=False)

# ----------------------------------------------------------------------------------------------------------------------------------------------------

from Workers.utility.Database import MongoDB
@csrf_exempt
def test(request: request.HttpRequest):
    db = MongoDB()
    model = db.get_parser_model("nha-cho-tot-com")
    for data in model:
        try:
            data["len_valid"] = int(data["len_valid"])
        except:
            data["len_valid"] = 1

        _serializer = ParserSerializer(data=data)

        if _serializer.is_valid(raise_exception=True):
            _serializer.save()

    return JsonResponse("hello", safe=False)