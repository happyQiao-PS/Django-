from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def showdemo(request):
    return HttpResponse("hello world")


def home(request):
    return render(request,"home.html")


def hehe(request):
    return HttpResponse("hehe")

def hehehe(request,suzi):
    return HttpResponse("hehe %s" %suzi)