from django.db import models
from django.db.models.base import Model
from django.db.models.lookups import Regex

# Create your models here.

class Worker(models.Model):
    WorkerID    = models.AutoField(primary_key=True)
    WorkerIP    = models.CharField(max_length=15)
    WorkerName  = models.CharField(max_length=50)
    RmqPassword = models.CharField(max_length=256)

class Parser(models.Model):
    id          = models.AutoField(primary_key=True)
    site        = models.CharField(max_length=64,blank=True, null=True)
    features    = models.CharField(max_length=32,blank=True, null=True)
    default     = models.CharField(max_length=256,blank=True, null=True)
    xpath       = models.CharField(max_length=256,blank=True, null=True)
    pos_take    = models.CharField(max_length=256,blank=True, null=True)
    regex_take  = models.CharField(max_length=256,blank=True, null=True)
    regex_valid = models.CharField(max_length=256,blank=True, null=True)
    len_valid   = models.IntegerField(blank=True, null=True)
    

