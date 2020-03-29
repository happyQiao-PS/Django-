import random

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app.models import Student


def getMi10(request):
    return HttpResponse("不好意思你没有得到手机")

# @csrf_exempt
def login(request):
    if request.method=="POST":
        return HttpResponse("POST 请求是成功的 ！")
    return render(request,"login.html")


def addData(request):
    for i in range(100):
        s =Student()
        s.s_name = random.choice(["Tom","Peter","Packer"])+str(i)
        s.save()
    return redirect(reverse("home:addData"))


def showData(request):
    page = request.GET.get("page",1)
    per_page = int(request.GET.get("per_page",10))
    students = Student.objects.all()
    pages = Paginator(students,per_page)
    page_num = pages.page_range
    page_list = pages.page(page)
    return render(request,"show.html",locals())