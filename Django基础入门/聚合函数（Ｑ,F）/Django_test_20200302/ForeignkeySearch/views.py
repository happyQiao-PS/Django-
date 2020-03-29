from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from ForeignkeySearch.models import Student, Classroom, Food_lover, TrueOrFalse


def showClass1(request):
    classname = "一班"
    class1 = Classroom.objects.get(c_name="class1")
    students_one = class1.student_set.all()
    return render(request, "showStudents.html", context={
        "classname": classname,
        "students": students_one
    })


def showClass2(request):
    classname = "二班"
    class2 = Classroom.objects.get(c_name="class2")
    students_two = class2.student_set.all()
    return render(
        request,
        "showStudents.html",
        context={
            "classname":classname,
            "students":students_two
        }
    )


def showClass3(request):
    classname = "三班"
    class2 = Classroom.objects.get(c_name="class3")
    students_two = class2.student_set.all()
    return render(
        request,
        "showStudents.html",
        context={
            "classname": classname,
            "students": students_two
        }
    )


def getS5(request):
    class_s5 = Classroom.objects.filter(student__s_name="S5")
    if class_s5:
        return HttpResponse("获取成功")
    else:
        return HttpResponse("获取失败")


def getMaxFoodlover(request):
    lover = Food_lover.objects.aggregate(Max("f_Eat"))
    print(lover)
    return HttpResponse("查询成功！")


def DemoTrueOrFalse(request):
    nums = TrueOrFalse.objects.all()
    for i in nums:
        print(i.True_or_false)
    return HttpResponse("Yes")