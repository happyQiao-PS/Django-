import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def getMI10(request):
    if random.randrange(100)>85:
        response = HttpResponse("恭喜你抢到一部小米手机！")
    else:
        response = HttpResponse("不好意思你没有抢到小米手机")
    return response