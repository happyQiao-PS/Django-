from django.conf.urls import url

from app1 import views

urlpatterns = [
    url(r"^showgrades/", views.showgrades, name="showgradelist"),
    url("^showgrade/(\d+)*/", views.showgrade, name="showgradestudents"),
    url("^getstudent/(\d+)*/", views.getstudent, name="getstudent"),
    url(r"^delstudent/(\d+)*/", views.delete, name="deletestudent"),
    url("^addstudent/", views.addstudent, name="addstudent"),
]
