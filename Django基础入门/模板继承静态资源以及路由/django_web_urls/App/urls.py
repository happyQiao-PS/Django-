from django.urls import path

from App import views

urlpatterns = [
    path("show/<name>/<age>/",views.show,name="show"),

]