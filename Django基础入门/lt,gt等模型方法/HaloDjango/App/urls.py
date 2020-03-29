from django.urls import path

from App import views

urlpatterns = [
    path("showDemo/",views.show)
]