from django.db import models
from django.db.models import fields
from rest_framework import serializers
from Workers.models import Worker, Parser

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ("WorkerID","WorkerIP","WorkerName","RmqPassword")

class ParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parser
        fields = ("id","site","features","default","xpath","pos_take","regex_take","regex_valid","len_valid")

