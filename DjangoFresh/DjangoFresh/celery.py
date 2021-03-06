from __future__  import absolute_import,unicode_literals
from django.conf import settings
from celery import Celery
import os
#设置celery执行的环境变量，执行django项目的配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE","CeleryTask.settings")
#创建celery应用
app=Celery('art_project')#celery应用的名称
app.config_from_object('django.conf:settings')#加载的配置文件
#如果在工程的应用中创建了tasks.py模块，那么Celery应用就会自动去检索创建的任务。比如你添加了一个任务
#在django中会实时地检索出来。
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)
from  __future__  import   absolute_import,unicode_literals
#literals文字literals,literals文字literals;unicode采用双字节对字符进行编码，统一的字符编码标准
from  django.conf  import settings
from  celery import  Celery
import  os
#设置celery执行的环境变量，执行django项目的配置文件
os.environ.setdefault('DJANGO-SETTINGS_MODULE',"CeleryTask.settings")
#创建celery应用
app=Celery('art_project')#celery应用的名称
app.config_from_object('django.conf:settings')#加载的配置文件
#如果在工程的应用中创建了tasks.py模块,那么Celery应用就会自动去检索创建的任务。比如你添加了一个任务
#在django中会实时的检索出来。
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)