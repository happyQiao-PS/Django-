from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def hello(request):
    return HttpResponse("hello world")


def login(request):
    if request.method == "POST":
        response = HttpResponseRedirect(reverse("home:mine"))
        try:
            request.session["name"] = request.POST.get("name")
            return response
        except Exception as e:
            return HttpResponse("ErrorMsg: %s" %e)
    else:
        return render(request,"login.html")


def mine(request):
    name = request.session["name"]
    return render(request,"mine.html",locals())