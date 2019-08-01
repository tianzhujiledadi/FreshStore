from django.shortcuts import render
from CeleryTask.task import add
from django.http import JsonResponse
def get_add(request):
    add.delay(2,3)
    return JsonResponse({"status":200})
