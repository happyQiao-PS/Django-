import random
from time import sleep

from django.core.cache import caches
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.cache import cache_page

from app.models import LoadPic


def upload(request):
    if request.method == "POST":
        useranem = request.POST.get("username")
        imgfile = request.FILES.get("img")
        load = LoadPic()
        load.load_name = useranem
        load.load_img = imgfile
        load.save()
        print(load.load_img.url)
        return redirect(r"../../static/media_root/"+load.load_img.url)
    else:
        return render(request,"upload.html")

@cache_page(30,cache="redis_backend")
def showCache(request):
    sleep(5)
    response = HttpResponse("haloman")
    return response

@cache_page(30,cache="redis_backend")
def getMi10(request):
    num = random.randrange(100)
    sleep(5)
    if num >= 98:
        response = HttpResponse("恭喜哦！您抢到了一部小米手机！")
    else:
        response = HttpResponse("不好意思！您没有抢到！")
    return response