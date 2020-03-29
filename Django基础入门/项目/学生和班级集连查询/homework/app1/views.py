from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from app1.models import Grade, Student


def showgrades(request):
    name = "班级列表"
    obj_list = Grade.objects.all()
    return render(request,"showlist.html",context={
        "name":name,
        "obj_list":obj_list
    })


def showgrade(request,class_id):
    students = Student.objects.filter(s_grade_id=class_id)
    grades_name = Grade.objects.all()
    return render(request,"showstudentlist.html",locals())


def getstudent(request,stu_id):
    student = Student.objects.filter(pk=stu_id)
    return render(request,"getstudent.html",locals())


def delete(request,stu_id):
    student = Student.objects.filter(pk=stu_id)
    print(stu_id)
    class_id = student[0].s_grade.id
    student.delete()
    return render(request,"deleteScuess.html",locals())


def addstudent(request):
    Data = request.GET
    gradeClass = Grade.objects.filter(g_name=Data.get("grade"))
    student = Student()
    student.s_name = Data.get("name")
    student.s_age = int(Data.get("age"))
    student.s_sex = Data.get("sex")
    student.s_hobby = Data.get("hobby")
    student.s_grade = gradeClass[0]
    student.save()
    students = Student.objects.filter(s_grade_id=gradeClass[0])
    grades_name = Grade.objects.all()
    return render(request, "showstudentlist.html", locals())


def pushData(request,name,age,sex,hobby,grade):
    print(name,age,sex,hobby,grade)
    data = request.GET
    print(data)
    return HttpResponse("Ok")