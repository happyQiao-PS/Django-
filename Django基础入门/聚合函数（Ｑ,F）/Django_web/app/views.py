import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from app.models import Grade, Student


def addData(request):
    # for i in range(3):
    #     grade = Grade()
    #     grade.g_name = "class %d" %i
    #     grade.save()

    flag = 100
    class1 = Grade.object.get(pk=1)
    class2 = Grade.object.get(pk=2)
    class3 = Grade.object.get(pk=3)

    while flag:
        student = Student()
        student.s_name="stu %d" %flag
        student.s_fk = random.choice([class1,class2,class3])
        student.save()
        flag = flag - 1
    return HttpResponse("OK")


def showData(request):
    grades = Grade.object.filter()
    context = {
        "grade":grades
    }

    return render(request,'menu.html',context)


def showclass1(request):
    Class1 = Grade.object.get(pk=1)
    students = Class1.student_set.all()
    context = {
        "classname":Class1.g_name,
        "students":students
    }
    return render(request,'show.html',context)

def showclass2(request):
    Class1 = Grade.object.get(pk=2)
    students = Class1.student_set.all()
    context = {
        "classname":Class1.g_name,
        "students":students
    }
    return render(request,'show.html',context)

def showclass3(request):
    Class1 = Grade.object.get(pk=3)
    students = Class1.student_set.all()
    context = {
        "classname":Class1.g_name,
        "students":students
    }
    return render(request,'show.html',context)