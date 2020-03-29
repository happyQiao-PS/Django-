from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^hello/', views.hello, name="hello"),
    url(r'^addStudent/', views.addStudent, name='addStudent'),
    url(r'^addIdcard/', views.addIdcard, name="addIdcard"),
    url(r'^bindStudent/', views.bindStudent, name="bindStudent"),
    url(r'^deleteStudent/', views.deleteStudent, name="deleteStudent"),
    url(r'^deleteIdcard/', views.deleteIdcard, name="deleteIdcard"),
    url(r'^addGoods/(?P<goodsName>\w+)/', views.addGoodes, name="addGoods"),
    url(r'^addCustomer/(?P<customerName>\w+)/', views.addCustomer, name="addCustomer"),
    url(r'^addToShoppingCar/', views.addToShoppingCar, name="addToShoppingCar"),
    url(r'^addToBuyers/', views.addToBuyers, name="addToBuyers"),
    url(r'^getGoodsList/(?P<customerId>\d+)/', views.getGoodsList, name="getGoodsList"),
    url(r'^upLoadFiles/', views.upLoadFiles, name="upLoadFiles"),
    url(r'^imageFiled/', views.imageFiled, name="imageFiled"),

]
