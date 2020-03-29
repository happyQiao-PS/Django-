from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'addData/',views.addData),
    url(r'showData/',views.showData),
    url(r'showclass1/',views.showclass1),
    url(r'showclass2/', views.showclass2),
    url(r'showclass3/', views.showclass3)
]