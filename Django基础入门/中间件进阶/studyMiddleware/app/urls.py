from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'getMi10/', views.getMi10, name="getMi10"),
    url(r'login/', views.login, name='login'),
    url(r'addData/', views.addData, name='addData'),
    url(r'showData/', views.showData, name='showData'),
]
