from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Student_grade.models import grade, student


def showGrade(request):
    grades = grade.objects.all()
    return render(request,"grade_list.html",context=locals())


def showGrade_id(request,g_id):
    students = student.objects.filter(s_grade_id=g_id)
    if students.exists():
        return render(request,"student_list.html",context=locals())
    elif students.exists() is None:
        return HttpResponse("这里什么页没有查询到，很抱歉！")