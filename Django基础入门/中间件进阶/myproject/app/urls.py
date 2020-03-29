from django.conf.urls import url

from app import views

urlpatterns = [
    url("getMi10/",views.getMI10,name="getMI10")
]