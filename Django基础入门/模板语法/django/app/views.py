import random

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from app.models import AppStudent as Student, AppIdcard as IDcard, AppGoods as Goods, AppCustomer as Customer, \
    uploadFiles


def hello(request):
    return render(request, "sayhello.html")


def addStudent(request):
    student = Student()
    student.s_name = request.GET.get("name")
    student.save()
    return HttpResponse("学生%s创建成功" % student.s_name)


def addIdcard(request):
    idcard = IDcard()
    idcard.id_num = request.GET.get("id")
    idcard.save()
    return HttpResponse("学生证%s创建成功" % idcard.id_num)


def bindStudent(request):
    student = Student.objects.last()
    idcard = IDcard.objects.last()
    idcard.id_Student = student
    idcard.save()
    return HttpResponse("%s和学生证号%s关联成功了" % (student.s_name, idcard.id_num))


def deleteStudent(request):
    idcard = IDcard.objects.last()
    student = idcard.id_Student
    student.delete()
    return HttpResponse("学生%s删除成功" % student.s_name)


def deleteIdcard(request):
    student = Student.objects.last()
    idcard = student.idcard
    idcard.delete()
    return HttpResponse("学生证编号%s删除成功" % idcard.id_num)


def addGoodes(request, goodsName):
    good = Goods()
    good.g_name = goodsName
    good.save()
    return HttpResponse("商品%s添加成功了" % good.g_name)


def addCustomer(request, customerName):
    customer = Customer()
    customer.c_name = customerName
    customer.save()
    return HttpResponse("购买者%s添加成功啦 " % customer.c_name)


def addToShoppingCar(request):
    customer = Customer.objects.get(pk=random.choice([4, 5, 6]))
    good = Goods.objects.get(pk=random.choice([1, 2, 3]))
    customer.c_goods.add(good)
    return HttpResponse("%s购买了%s的产品" % (customer.c_name, good.g_name))


def addToBuyers(request):
    customer = Customer.objects.get(pk=random.choice([4, 5, 6]))
    good = Goods.objects.get(pk=random.choice([1, 2, 3]))
    good.customer_set.add(customer)
    return HttpResponse("%s商品选择了顾客%s" % (good.g_name, customer.c_name))


def getGoodsList(request, customerId):
    customer = Customer.objects.get(pk=customerId)
    goods = customer.c_goods.all()
    return render(request, "goodlist.html", locals())


def upLoadFiles(request):
    if request.method == "GET":
        return render(request,"uploadfile.html")
    elif request.method == "POST":
        icon = request.FILES.get("icon")
        savefile = open("static/pic/1.jpg","wb")
        for part in icon.chunks():
            #chunks大块，一块一块的，这边代之吧数据切成很多片然后一点一点存储，防止内存爆炸
            savefile.write(part)
            savefile.flush()
        savefile.close()
        return redirect("../../static/pic/1.jpg")


def imageFiled(request):
    if request.method == "GET":
        return render(request, "imageFiled.html")
    elif request.method == "POST":
        icon = request.FILES.get("icon")
        uname = request.POST.get("uname")
        uploadfile = uploadFiles()
        uploadfile.up_name = uname
        uploadfile.up_file = icon
        uploadfile.save()
    return redirect("../../static/uploadFile/icon/%s" %icon)