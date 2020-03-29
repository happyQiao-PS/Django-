from django.conf.urls import url

from ForeignkeySearch import views

urlpatterns = [
    url(r'^showClass1/', views.showClass1),
    url(r'^showClass2/', views.showClass2),
    url(r'^showClass3/', views.showClass3),
    url(r'^getS5/',views.getS5),
    url(r"^getMaxFoodlover/",views.getMaxFoodlover),
    url(r"^trueorfalse/",views.DemoTrueOrFalse)
]
