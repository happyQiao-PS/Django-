from django.conf.urls import url

from app1 import views

urlpatterns = [
    url(r"^showdemo/", views.hello, name="hello"),
    url(r"^login/", views.login, name="login"),
    url(r"^mine/", views.mine, name="mine"),
]
