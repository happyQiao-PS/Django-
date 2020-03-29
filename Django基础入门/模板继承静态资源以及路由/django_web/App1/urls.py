from django.conf.urls import url

from App1 import views

urlpatterns = [
    url(r"^showdemo/",views.showdemo),
    url(r"^home/",views.home),
    url(r"^hehe/$",views.hehe),
    url(r"hehe/(\d+)/$",views.hehehe),
]