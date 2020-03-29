from django.conf.urls import url

from app import views

urlpatterns = [

    url(r"^showdemo/(?P<name>\d+)/", views.showdemo),
    url(r"^create/", views.creat),
    url(r"createobj/", views.createobj, name="do_create_obj"),

    url(r"show", views.show, name="show"),
    url(r"showmsg/", views.showmsg),
    url(r"getCookie/", views.getCookie, name="getCookie"),

    url(r"login/", views.login, name="login"),
    url(r"setCookie/", views.setCookie, name="setCookie"),
    url(r"mine/", views.mine, name="mine"),
]
