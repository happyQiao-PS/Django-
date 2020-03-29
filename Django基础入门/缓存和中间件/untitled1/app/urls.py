from django.conf.urls import url

from app import views

urlpatterns = [
    url(r"^upload/", views.upload, name="upload"),
    url(r'^showCache/', views.showCache, name="showCache"),
    url(r"^getMi10/", views.getMi10, name="getMi10"),
]
