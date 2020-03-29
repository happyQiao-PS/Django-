from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def show(request,name,age):
    return render(request,"show.html",context={
        "name":name,
        "age":age
    })