from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def showdemo(request,name):
    return HttpResponse("halo: %s" %name)


def createobj(request):
    res = HttpResponse("hahaha  ")
    res.write("hehehe")
    res.flush()
    return res


def creat(request):
    return render(request,"create.html")


def show(request):
    # data = {
    #     "name":"lalala",
    #     "age":500
    # }
    # return JsonResponse(data)
    response = HttpResponse()

    response.set_cookie("name","qiaodemo333")

    return response


def showmsg(request):
    url = reversed("home:show")
    return HttpResponseRedirect(url)


def getCookie(request):
    cookie = request.COOKIES.get("username")
    return HttpResponse(cookie)


def login(request):
    return render(request,"login.html")


def setCookie(request):
    uname = request.POST.get("username")
    response = HttpResponseRedirect(reverse("home:mine"))
    response.set_signed_cookie("username",uname,"lalala")
    return response


def mine(request):
    data = request.get_signed_cookie("username","没获取到","lalala")
    if data:
        return HttpResponse(data)
    return HttpResponseRedirect(reverse("home:login"))