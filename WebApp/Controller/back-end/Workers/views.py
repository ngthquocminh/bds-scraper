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

# Create your views here.

@csrf_exempt
def workerApi(request: request.HttpRequest, id=0):
    if request.method == 'GET':
        
        workers = Worker.objects.all()
        worker_serializer = WorkerSerializer(workers, many=True)
        # print(worker_serializer.data)
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
        response = test_connection(worker.WorkerIP, worker.WorkerName, worker.RmqPassword)
        return JsonResponse(response,safe=False)

def get_sitename(uri):
    return re.compile(r"/parser/(.+)/").search(uri).group(1)

@csrf_exempt
def parserSetGetApi(request: request.HttpRequest, id=0):
    if request.method == "GET":
        site_name    = get_sitename(request.get_raw_uri())
        # print(set_name)
        parser_set  = Parser.objects.raw("""SELECT * FROM Workers_parser WHERE site="{site_name}" """.format(site_name=site_name))
        serializers = ParserSerializer(parser_set, many=True)
        # print(serializers.data)
        return JsonResponse(serializers.data if isinstance(serializers.data, list) else [serializers.data], safe=False)

@csrf_exempt
def parserEditApi(request: request.HttpRequest, id=0):    
    if request.method == 'POST':

        _data = JSONParser().parse(request)
        _serializer = ParserSerializer(data=_data)

        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Added Failed!!", safe=False)
    
    elif request.method == 'PUT':
        _data = JSONParser().parse(request)
        object = Parser.objects.get(id=int(_data["id"]))
        _serializer = ParserSerializer(object , data=_data)
        if _serializer.is_valid():
            _serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Added Failed!!",safe=False)
    
    elif request.method == 'DELETE':
        try:
            _id = JSONParser().parse(request)["id"]
            object = Worker.objects.get(id=_id)
            object.delete()
            return JsonResponse("Deleted Successfully!!",safe=False)
        except:
            return JsonResponse("Deleted Failed!!",safe=False)

    
    
        
 
